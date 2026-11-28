# -*- coding: utf-8 -*-
"""28.11.2026 (слово Кенана): боковое меню книги «Клиническая психиатрия» — три оглавления, в каждом названия СВОЕЙ
классификации: МКБ-11 — названия ВОЗ МКБ-11 (главы — блоки ВОЗ), DSM-5-TR — названия DSM-5-TR, МКБ-10 — названия МКБ-10.
Прежде пункты DSM и МКБ-10 несли название МКБ-11 (сборщик подставлял tit[pid]) — смешение классификаций.
Источник — шапки расстройств исправленных версий базы (dx_heads.json: EN_v81 / AZ_v60 / RU_v76 / TR_v58, страж
dx_header_guard — БРАКА НЕТ). Правит books/klinik-psixiatriya/book.json и панели оглавлений на страницах (.cls-panel).
  python _tools/klinik_trees_dx.py <dx_heads.json> [--dry]"""
import glob, io, json, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
H = json.load(open(sys.argv[1], encoding="utf-8"))
dry = "--dry" in sys.argv
BJ = os.path.join(D, "books", "klinik-psixiatriya", "book.json")
book = json.load(open(BJ, encoding="utf-8"))


def short(s):
    """длинное пояснение в скобках у названия (примечание о кодах) в меню не нужно"""
    m = re.match(r"^(.*?)\s*\(([^()]{40,})\)\s*$", s or "")
    return m.group(1) if m else (s or "")


def cf(s, L):
    if L in ("tr", "az"):
        s = s.replace("I", "ı").replace("İ", "i")
    return re.sub(r"\s+", " ", s.replace("ё", "е")).strip().casefold()


def sent(s, L, old):
    """название из шапки (ПРОПИСНЫМИ) → как в меню: оставить прежнее написание, если совпадает без учёта регистра"""
    s = re.sub(r"^\d[A-Z][0-9A-Z]{2}–\d[A-Z][0-9A-Z]{2}\s+", "", s)  # шапка-диапазон «7A21–7A26 НАЗВАНИЕ»
    if cf(s, L) == cf(old, L):
        return old
    lo = (lambda x: x.lower()) if L not in ("tr", "az") else (lambda x: x.replace("I", "ı").replace("İ", "i").lower())
    low = lo(s)
    low = low[:1].upper() + low[1:]
    oldpar = {cf(p, L): p for p in re.findall(r"\(([^()]+)\)", old or "")}

    def par(m):
        p = m.group(1)
        if cf(p, L) in oldpar:                                       # скобки как в прежнем меню
            return "(" + oldpar[cf(p, L)] + ")"
        # короткое сокращение — прописными (GAD, ГТР), остальное строчными
        return "(" + ", ".join(w.strip().upper() if len(w.strip()) <= 6 and " " not in w.strip() else w.strip() for w in p.split(",")) + ")"
    return re.sub(r"\(([^()]+)\)", par, low)


def mcode(s):
    """код DSM для колонки меню: без пояснений шапки («(… октябрь 2022)», «; G31.84 — только…», «например…»)"""
    s = re.sub(r"\s*\([^()]*\)", "", (s or "").strip())
    s = re.split(r";| — ", s)[0]
    s = re.split(r",\s+(?=[^\sA-Z])", s)[0]                  # «…, məsələn F01.A0» → до запятой
    s = re.sub(r"^[^A-Z+]*\+\s*", "", s)                     # «etioloji kod + F06.70» → «F06.70»
    return s.strip(" ,")


ch = []
for L, T in book["trees"].items():
    hd = H.get(L)
    if not hd:
        continue
    card = {}                                                        # id страницы → код МКБ-11
    for g in T["icd"]:
        if g.get("code") in hd["blocks"]:
            new = sent(hd["blocks"][g["code"]], L, g["t"])
            if new != g["t"]:
                ch.append((L, "icd-глава", g["code"], g["t"], new)); g["t"] = new
        for it in g.get("items", []):
            card[it["id"]] = it["code"]
            h = hd["heads"].get(it["code"])
            if h and h.get("n11"):
                new = sent(h["n11"], L, it["t"])
                if new != it["t"]:
                    ch.append((L, "icd", it["code"], it["t"], new)); it["t"] = new
    for key, f in (("dsm", "ndsm"), ("icd10", "n10")):
        for g in T[key]:
            for it in g.get("items", []):
                h = hd["heads"].get(card.get(it["id"], ""))
                if h and h.get(f) and h[f] != "—":
                    new = short(h[f])
                    if new != it["t"]:
                        ch.append((L, key, it.get("code", ""), it["t"], new)); it["t"] = new
                # 28.11.2026: код DSM-5-TR пункта — из шапки (ICD-10-CM FY2026, dx_dsm_code_fix); группа DSM — глава, не меняется
                cd = mcode((h or {}).get("cdsm", "")) if key == "dsm" else ""
                if cd and cd != "—" and it.get("code") and cd != it["code"]:
                    ch.append((L, "dsm-код", it["id"], it["code"], cd)); it["code"] = cd
# дерево МКБ-10: код пункта — код МКБ-10 из шапки (сверен по таблице перехода ВОЗ, страж dx_header_guard);
# сменился код — пункт переходит в группу своего кода и встаёт по порядку кодов (28.11.2026)


def grp_of(code, groups):
    if not re.match(r"^[A-Z]\d\d", code or ""):
        return next((g for g in groups if g.get("code") == "—"), None)
    for g in groups:
        m = re.match(r"^([A-Z]\d\d)(?:–([A-Z]\d\d))?$", g.get("code", ""))
        if m and m.group(1) <= code[:3] <= (m.group(2) or m.group(1)):
            return g
    return next((g for g in groups if code[:3] in g.get("code", "")), None)   # «G47 · N94»


def ckey(code):
    return (code or "~").replace("–", "-")


for L, T in book["trees"].items():
    hd = H.get(L)
    if not hd:
        continue
    card = {it["id"]: it["code"] for g in T["icd"] for it in g.get("items", [])}
    for g in list(T["icd10"]):
        for it in list(g.get("items", [])):
            h = hd["heads"].get(card.get(it["id"], "")) or {}
            new = (h.get("c10") or "").strip()
            if not new or new == it.get("code"):
                continue
            dst = grp_of(new, T["icd10"])
            if not dst:
                print("!! нет группы МКБ-10 для", L, it["id"], new); continue
            ch.append((L, "icd10-код", it["id"], it.get("code"), new + ("" if dst is g else " → группа " + dst["code"])))
            it["code"] = new
            g["items"].remove(it)                                    # и внутри той же группы — на место по порядку кодов
            pos = next((i for i, x in enumerate(dst["items"]) if dst["code"] != "—" and ckey(x.get("code")) > ckey(new)), len(dst["items"]))
            dst["items"].insert(pos, it)
# book.json → toc: главы (код диапазона) — те же названия, что в дереве МКБ-11 (по toc строится навигация снимков build_static);
# поле "en" у главы — название блока ВОЗ на английском (из EN-дерева)
ENCH = {g["code"]: g["t"] for g in book["trees"].get("en", {}).get("icd", [])}
for L, T in book["trees"].items():
    chap = {g["code"]: g["t"] for g in T["icd"]}
    icdn = {x["id"]: x["t"] for g in T["icd"] for x in g.get("items", [])}   # расстройство: название МКБ-11 из дерева
    for it in book.get("toc", {}).get(L, []):
        if it.get("id") in icdn and it.get("code") not in chap and it.get("t") != icdn[it["id"]]:
            ch.append((L, "toc-пункт", it["id"], it["t"], icdn[it["id"]])); it["t"] = icdn[it["id"]]
        cd = it.get("code")
        if cd in chap and it.get("t") != chap[cd]:
            ch.append((L, "toc-глава", cd, it["t"], chap[cd])); it["t"] = chap[cd]
        if cd in ENCH and "en" in it and it["en"] != ENCH[cd]:
            ch.append((L, "toc-en", cd, it["en"], ENCH[cd])); it["en"] = ENCH[cd]
# панели оглавлений на страницах: пункт = ссылка ?p=<id>, вторая span — название
NAMES = {L: {k: {it["id"]: it["t"] for g in T[k] for it in g.get("items", [])} for k in ("icd", "dsm", "icd10")} for L, T in book["trees"].items()}
CHAP = {L: {g["code"]: g["t"] for g in T["icd"]} for L, T in book["trees"].items()}
CODES = {L: {k: {it["id"]: it.get("code", "") for g in T[k] for it in g.get("items", [])} for k in ("dsm",)} for L, T in book["trees"].items()}
pages = 0
for f in glob.glob(os.path.join(D, "books", "klinik-psixiatriya", "*", "*.html")) + glob.glob(os.path.join(D, "*", "read", "klinik-psixiatriya", "*.html")):
    t = io.open(f, encoding="utf-8", newline="").read()
    if "cls-panel" not in t:
        continue
    L = next((x for x in ("az", "ru", "en", "tr") if re.search(r"[\\/]%s[\\/]" % x, f)), None)
    if not L or L not in NAMES:
        continue
    # точечно, регулярными выражениями: разметка страницы не пересобирается (BeautifulSoup менял весь документ)
    import html as _h
    cuts = [(m.start(), m.group(1)) for m in re.finditer(r'<div class="cls-panel" data-cls="(icd|dsm|icd10)"', t)]
    if not cuts:
        continue
    n = 0
    out, last = [], 0
    for ci, (pos, key) in enumerate(cuts):
        end = cuts[ci + 1][0] if ci + 1 < len(cuts) else len(t)
        out.append(t[last:pos])
        seg = t[pos:end]

        def it_sub(m):
            global n
            pid, code, name = m.group(2), m.group(4), _h.unescape(m.group(6))
            want = NAMES[L][key].get(pid) or name
            wcode = CODES[L][key].get(pid) if key == "dsm" else None
            wcode = _h.escape(wcode, quote=False) if wcode else code
            if want != name or wcode != code:
                n += 1
                return m.group(1) + m.group(3) + wcode + m.group(5) + _h.escape(want, quote=False) + m.group(7)
            return m.group(0)
        if key == "icd10":
            # состав и порядок групп — из дерева (код мог смениться и пункт — перейти в другую группу); ссылки — прежние
            A = {m.group(2): m.group(1) for m in re.finditer(r'<a href="([^"]*?p=([^"&#]+))"><span class="sc">', seg)}
            G = {g["code"]: g["items"] for g in book["trees"][L]["icd10"]}

            def grp_sub(m):
                global n
                its = G.get(_h.unescape(m.group(2)))
                if its is None or any(x["id"] not in A for x in its):
                    return m.group(0)
                if not its:
                    body = m.group(4) if "tc-empty" in m.group(4) else m.group(4)
                else:
                    body = "".join('<a href="%s"><span class="sc">%s</span><span>%s</span></a>' % (A[x["id"]], _h.escape(x["code"], quote=False), _h.escape(x["t"], quote=False)) for x in its)
                if body != m.group(4):
                    n += 1
                return m.group(1) + body + m.group(5)
            seg = re.sub(r'(<div class="toc-ch"><div class="tc-head"><span class="tc-range">([^<]*)</span><span>[^<]*</span></div>(<div class="tc-list">))(.*?)(</div></div>)', grp_sub, seg)
        seg = re.sub(r'(<a href="read\.html\?b=klinik-psixiatriya&amp;p=([^"&#]+)">)(<span class="sc">)([^<]*)(</span><span>)([^<]*)(</span></a>)', it_sub, seg)
        if key == "icd":
            def ch_sub(m):
                global n
                rng, name = m.group(2), _h.unescape(m.group(4))
                want = CHAP[L].get(rng)
                if want and want != name:
                    n += 1
                    return m.group(1) + m.group(2) + m.group(3) + _h.escape(want, quote=False) + m.group(5)
                return m.group(0)
            seg = re.sub(r'(<div class="toc-ch"><a href="[^"]*"><span class="tc-range">)([^<]*)(</span><span>)([^<]*)(</span></a>)', ch_sub, seg)
        out.append(seg)
        last = end
    t2 = "".join(out) + t[last:] if last < len(t) else "".join(out)
    if n:
        pages += 1
        if not dry:
            with io.open(f + ".tmp", "w", encoding="utf-8", newline="") as w:
                w.write(t2)
            os.replace(f + ".tmp", f)
for r in ch:
    print(*r, sep=" | ")
print("изменений в book.json:", len(ch), "| страниц с панелями изменено:", pages, "(проба)" if dry else "")
if not dry:
    json.dump(book, open(BJ, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
