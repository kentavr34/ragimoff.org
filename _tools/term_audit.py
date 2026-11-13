# -*- coding: utf-8 -*-
"""term_audit.py — сверка терминов всех книг сайта с базой истины (слово Кенана 13.11.2026: «корень ошибки может быть во всех книгах»).

По этапам:  python term_audit.py titles   — 1) названия и подзаголовки книг (book.json t/sub, все языки; каталог магазина)
            python term_audit.py toc      — 2) названия глав (book.json toc, все языки)
            python term_audit.py text     — 3) термины внутри книг (books/<книга>/<язык>/NNN.html)
            python term_audit.py refresh  — обновить выгрузку базы истины с сервера 994 (только чтение)
База истины (выгрузка в _agent/truth_cache/, только чтение с 164.68.114.15, БД translation):
  truth.term_verified — проверенные термины ✓/≈ с отвергнутыми вариантами ✗ (область: modern | freud_historic);
  icd10_az_terms — официальный азербайджанский МКБ-10 (XBT-10); icd11_terms — МКБ-11 (EN/RU, title_az_verified).
Правило областей: книги Фрейда — историческая норма (freud_historic), если у понятия она есть, иначе современная;
остальные книги — современная (modern). Отвергнутый вариант с пояснением в скобках — контекстный: только показывается.
Каждый этап пишет отчёт _agent/docs/TERM_AUDIT_<этап>.tsv и сводку; код выхода 1, если найдены отвергнутые формы."""
import io, os, re, sys, json, glob, collections, subprocess

D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CACHE = os.path.join(D, "_agent", "truth_cache")
OUT = os.path.join(D, "_agent", "docs")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
L = "a-zəığüöçşA-ZƏIĞÜÖÇŞİа-яёА-ЯЁ"


def jl(name):
    p = os.path.join(CACHE, name)
    return [json.loads(x) for x in io.open(p, encoding="utf-8") if x.strip()] if os.path.exists(p) else []


def refresh():
    key = os.path.expanduser("~/.ssh/claude_deploy_key")
    q = {"term_verified.jsonl": "SELECT concept,domain,scope,lang,term,status,icd11_code,icd10_code,variants_rejected,confidence,books,note FROM truth.term_verified",
         "icd10_az.jsonl": "SELECT code,title_az FROM public.icd10_az_terms",
         "icd11.jsonl": "SELECT code,title_en,title_ru,title_az_verified FROM public.icd11_terms"}
    os.makedirs(CACHE, exist_ok=True)
    for f, sql in q.items():
        r = subprocess.run(["ssh", "-i", key, "-o", "BatchMode=yes", "root@164.68.114.15",
                            'sudo -u postgres psql -d translation -At'], input="SELECT row_to_json(t) FROM (%s) t;" % sql,
                           capture_output=True, text=True, encoding="utf-8", timeout=120)
        if r.returncode:
            raise SystemExit(r.stderr[-300:])
        io.open(os.path.join(CACHE, f), "w", encoding="utf-8", newline="\n").write(r.stdout)
        print(f, len(r.stdout.splitlines()))


def low(s):
    return s.replace("İ", "i").replace("I", "ı").lower() if re.search("[əğıöüşçƏĞİÖÜŞÇ]", s) else s.lower()


MED = {"psychiatry", "neurology", "medicine", "pharmacology", "anatomy", "genetics", "immunology", "neuroimaging", "psychiatry_history", "guideline"}
MED_ONLY = "--all" not in sys.argv      # по умолчанию — названия болезней, синдромов, симптомов и медицинские термины (слово Кенана 13.11)


def rules():
    """{(lang, scope): [(variant, правильный термин, concept, контекстный?)]} и множество понятий с исторической нормой."""
    tv = jl("term_verified.jsonl")
    hist = set((r["concept"], r["lang"]) for r in tv if r["scope"] == "freud_historic")
    out = collections.defaultdict(list)
    goods = collections.defaultdict(set)
    for r in tv:
        goods[r["lang"]].add(low(re.sub(r"\s*\(.*?\)", "", r["term"])).strip())
    for r in tv:
        if MED_ONLY and r.get("domain") not in MED:
            continue
        for v in r.get("variants_rejected") or []:
            ctx = bool(re.search(r"[(（]|[а-яё]", v)) and r["lang"] != "ru"     # пояснение в скобках/по-русски = контекст
            if r["lang"] == "ru":
                ctx = "(" in v
            vv = re.sub(r"\s*\(.*$", "", v).strip(" ;")
            if len(vv) < 3 or vv.isupper() and len(vv) <= 4:                 # аббревиатуры (BED, ASP) — только показ
                ctx = True
            if low(vv) in goods[r["lang"]] or len(vv.split()) == 1 and not re.search(r"[A-Z]", vv[1:]) and r["status"] != "verified":
                ctx = True                                                   # вариант — сам верный термин другого понятия / обычное слово
            if vv:
                out[(r["lang"], r["scope"])].append((vv, r["term"], r["concept"], ctx))
    return out, hist


def books():
    for f in sorted(glob.glob(os.path.join(D, "books", "*", "book.json"))):
        d = json.load(io.open(f, encoding="utf-8"))
        yield d["id"], d


def scope_rules(bid, lang, R, hist):
    if bid.startswith("freud-"):
        h = R.get((lang, "freud_historic"), [])
        hc = set(c for _, _, c, _ in h)
        return h + [x for x in R.get((lang, "modern"), []) if x[2] not in hc and (x[2], lang) not in hist]
    return R.get((lang, "modern"), [])


def _good_words():
    """Первые слова всех проверенных терминов базы (любой язык): найденное слово, которое само начинается с верного термина
    (cinsəllik ✓ при отвергнутом «cinsəl»; Həzz ✓ при «həzz» как неверном переводе Unlust), — не ошибка."""
    s = set()
    for r in jl("term_verified.jsonl"):
        g = re.sub(r"\s*\(.*?\)", "", r["term"]).strip()
        if g:
            s.add(low(g.split()[0]))
    return tuple(sorted(s, key=len, reverse=True))


GOOD = _good_words()


def hits(text, rl):
    t = low(text)
    for v, good, concept, ctx in rl:
        lv = low(v)
        if lv == low(good) or lv in low(good):
            continue
        for m in re.finditer(r"(?<![%s])%s(?=[%s]{0,6}(?![%s]))" % (L, re.escape(lv), L, L), t):
            # не считать, если на этом месте стоит правильный термин, содержащий вариант
            if low(good) in t[max(0, m.start() - len(good)):m.end() + len(good)]:
                continue
            w = re.match(r"[%s]+" % L, t[m.start():])
            if w and any((w.group(0).startswith(g) or len(g) > 6 and w.group(0).startswith(g[:-1])) and len(g) > len(low(v)) - 1 and g != low(v) for g in GOOD):
                continue
            yield v, good, concept, ctx, text[max(0, m.start() - 40):m.end() + 40].replace("\n", " ")


# слова-признаки диагноза для перечня (этапы 1–2): по ним строится список «что из названий — болезнь» и сверяется с базой
DX = {"az": r"(afazi|histeri|isteri|nevroz|psixoz|nevropsixoz|paranoy|melanxol|nevrasteni|fobi|epilep|idiot|demensi|şizofren|kataton|ipoxondr|hipoxondr|"
            r"psixopat|homoseksual|narsis|sadizm|mazox|fetiş|perversi|kokain|alkoqol|asılılı|aludəçi|amneziya|iflic|xorey|kəkələ|enurez|nevralgi|delir|halüsin|hallüsin|"
            r"depress|mani[ak]|təşviş|travma|autiz|oliqofren|obsess|kompuls|məcburiyyət|pozuntu|pozğunluq|sindrom|disfunksiya|sayıqlama|anoreksi|bulimi|insomni|"
            r"cinnət|ensefal|skleroz|parkinson|alzheimer|panik|stress|intihar|suisid|bipolyar|psixotik|şəxsiyyət)",
      "ru": r"(афази|истери|невроз|психоз|паран|меланхол|неврастен|фоби|эпилеп|идиот|деменц|шизофрен|кататон|ипохонд|психопат|гомосексуал|нарцисс|садизм|мазох|фетиш|"
            r"перверс|кокаин|алкогол|зависимост|амнези|паралич|хоре|заикан|энурез|невралги|делири|галлюцин|депресс|маниак|тревог|травм|аутиз|олигофрен|обсесс|компульс|"
            r"навязчив|расстройств|синдром|бред|анорекс|булими|бессонниц|безуми|энцефал|склероз|паник|стресс|суицид|биполяр|психотич|личност|вины)",
      "en": r"(aphasi|hysteri|neuros|psychos|parano|melanchol|neurasthen|phobi|epilep|idiocy|dementia|schizophren|catatoni|hypochondr|psychopath|homosexual|narcissis|"
            r"sadism|masochis|fetish|pervers|cocaine|alcohol|addict|amnesia|pals|chorea|stutter|enuresis|neuralgi|delirium|hallucinat|depress|manic|anxiety|trauma|autis|"
            r"obsess|compuls|disorder|syndrome|delusion|anorexia|bulimia|insomnia|madness|encephal|sclerosis|panic|stress|suicid|bipolar|psychotic|personality|guilt)"}


def known_terms():
    """Все известные базе формы по языкам (✓/≈ термины, официальные названия МКБ) — для пометки «есть в базе»."""
    k = collections.defaultdict(set)
    for r in jl("term_verified.jsonl"):
        k[r["lang"]].add(low(re.sub(r"\s*\(.*?\)", "", r["term"])))
    for r in jl("icd10_az.jsonl"):
        k["az"].add(low(r["title_az"] or ""))
    for r in jl("icd11.jsonl"):
        k["ru"].add(low(r.get("title_ru") or "")); k["en"].add(low(r.get("title_en") or ""))
        if r.get("title_az_verified"):
            k["az"].add(low(r["title_az_verified"]))
    return k


def stem(w):
    return low(w)[:max(5, len(w) - 3)]


def stage_names(kind):
    R, hist = rules()
    K = known_terms()
    idx = {lg: collections.defaultdict(set) for lg in K}
    for lg, ts in K.items():
        for t_ in ts:
            for w_ in re.findall("[%s]{5,}" % L, t_):
                idx[lg][w_[:5]].add(w_)
    def known(lg, w):
        w = low(w)
        for k in idx.get(lg, {}).get(w[:5], ()):
            p = max(5, min(len(k), len(w)) - 3)
            if k[:p] == w[:p]:
                return True
        return False
    rows, bad = [], 0
    for bid, d in books():
        items = []
        if kind == "titles":
            for fld in ("t", "sub", "kicker"):
                for lg, v in (d.get(fld) or {}).items():
                    if isinstance(v, str) and v.strip():
                        items.append((lg, fld, v))
        else:
            for lg, lst in (d.get("toc") or {}).items():
                for e in lst:
                    items.append((lg, "toc", e.get("t", "")))
        for lg, fld, text in items:
            for v, good, concept, ctx, around in hits(text, scope_rules(bid, lg, R, hist)):
                rows.append((bid, lg, fld, "✗ контекст" if ctx else "✗ ОТВЕРГНУТО", v, good, text)); bad += 0 if ctx else 1
            rx = DX.get(lg)
            if not rx:
                continue
            for m in re.finditer(r"[%s-]*%s[%s-]*" % (L, rx, L), text, re.I):
                w = m.group(0)
                st = "есть в базе" if known(lg, w) else "НЕТ В БАЗЕ"
                rows.append((bid, lg, fld, st, w, "", text))
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, "TERM_AUDIT_%s.tsv" % kind)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write("книга\tязык\tполе\tстатус\tслово\tправильно\tстрока\n")
        for r in rows:
            f.write("\t".join(x.replace("\t", " ") for x in r) + "\n")
    c = collections.Counter(r[3] for r in rows)
    print("ЭТАП %s: строк %d; %s; отчёт %s" % (kind, len(rows), dict(c), os.path.relpath(p, D)))
    return bad


def stage_text():
    R, hist = rules()
    rows, bad = [], 0
    agg = collections.Counter()
    for bid, d in books():
        for lg in d.get("langs") or []:
            rl = scope_rules(bid, lg, R, hist)
            if not rl:
                continue
            for f in sorted(glob.glob(os.path.join(D, "books", bid, lg, "*.html"))):
                t = re.sub(r"<[^>]+>", " ", io.open(f, encoding="utf-8").read())
                t = re.sub(r"&[a-z]+;", " ", t)
                for v, good, concept, ctx, around in hits(t, rl):
                    rows.append((bid, lg, os.path.basename(f), "✗ контекст" if ctx else "✗ ОТВЕРГНУТО", v, good, around))
                    agg[(bid, lg, v, good, "контекст" if ctx else "ОТВЕРГНУТО")] += 1
                    bad += 0 if ctx else 1
    p = os.path.join(OUT, "TERM_AUDIT_text.tsv")
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write("книга\tязык\tглава\tстатус\tвариант\tправильно\tконтекст\n")
        for r in rows:
            f.write("\t".join(x.replace("\t", " ") for x in r) + "\n")
    print("ЭТАП text: находок %d (отвергнутых %d, контекстных %d); отчёт %s" % (len(rows), bad, len(rows) - bad, os.path.relpath(p, D)))
    for (bid, lg, v, good, st), n in sorted(agg.items(), key=lambda x: -x[1])[:60]:
        print("  %5d  %-32s %s  %s → %s  [%s]" % (n, bid, lg, v, good, st))
    return bad


if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 1 else "titles"
    if a == "refresh":
        refresh(); sys.exit()
    n = stage_text() if a == "text" else stage_names(a)
    sys.exit(1 if n else 0)
