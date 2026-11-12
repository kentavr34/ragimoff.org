# -*- coding: utf-8 -*-
"""Заголовки как предложения (решение владельца 12.11.2026, п. 10: «исправить как полагается с точки зрения
грамматики и орфографии языка»). «Каждое Слово С Заглавной» → с заглавной только первое слово и имена собственные.
Работает по всем data/**/*.json на трёх языках: заголовки блоков и карточек, вопросы, подписи кнопок и ссылок,
заголовки h2–h4 внутри статей. Имена собственные и сокращения — список KEEP (пополняется по отчёту).
Запуск: python sentence_case.py show   — только показать, какие слова будут опущены (для просмотра глазами)
        python sentence_case.py        — применить. Повторный запуск: 0 изменений."""
import io, os, re, json, glob, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SHOW = len(sys.argv) > 1 and sys.argv[1] == "show"
UP = "A-ZА-ЯЁƏÖÜĞŞÇİI"
LO = "a-zа-яёəöüğşçıi̇"
CAPW = re.compile("^[%s][%s’']+$" % (UP, LO))
KEEP = set(io.open(os.path.join(os.path.dirname(__file__), "sentence_case_keep.txt"), encoding="utf-8").read().split())
# составные имена собственные: программы, книги, учреждения — внутри них регистр не трогаем
PHR = set(x.strip() for x in io.open(os.path.join(os.path.dirname(__file__), "sentence_case_phrases.txt"), encoding="utf-8").read().splitlines() if x.strip())
# строка с названием учреждения или фирмы не правится вовсе
MARK = re.compile(u"İnstitut|Universitet|Assosiasiya|Akademiya|Nazirliy|Institute|University|Association|Academy|Ministry|Society|Ltd| LP |Институт|Университет|Ассоциац|Академи|Министерств|GTC|Training")
HEAD_KEYS = {"title", "h", "t", "meta", "catLabel", "label", "cap", "law", "docs", "q"}
STAT = {}


def low(w, lang):
    if lang == "az":
        return (w[0].replace("I", "ı").replace("İ", "i") if w[0] in "Iİ" else w[0].lower()) + w[1:]
    return w[0].lower() + w[1:]


def conv(s, lang, name):
    if not isinstance(s, str) or "<" in s or len(s) > 140 or len(s) < 4 or MARK.search(s):
        return s
    words = s.split(" ")
    if len(words) < 2:
        return s
    cores = [re.sub(u"^[«(\"“‘'„]+|[»).,:;!?\"”’'…]+$", "", w) for w in words]
    # заголовок считается «с заглавными в каждом слове», если таких слов большинство
    cand = [c for c in cores[1:] if len(c) >= 4 and re.match("^[%s%s’'-]+$" % (UP, LO), c)]
    caps = [c for c in cand if all(CAPW.match(p) for p in c.split("-") if p) and c[0] in "ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯƏÖÜĞŞÇİ"]
    free = [c for c in caps if not any(p in KEEP for p in c.split("-")) and c not in KEEP]
    if not free or len(caps) * 10 < len(cand) * 6:
        return s
    out, inq, prev = [], False, ""
    for i, w in enumerate(words):
        c = cores[i]
        opened = w[:1] in u"«“„"
        if opened:
            inq = True
        if i > 0 and c and not inq and not re.search(u"[.!?…:]$", prev) and prev not in (u"·", "/", "|", u"•"):
            parts = c.split("-")
            if (cores[i - 1] + " " + c) in PHR or (i + 1 < len(cores) and (c + " " + cores[i + 1]) in PHR):
                out.append(w); prev = w                      # составное имя собственное — слово остаётся как есть
                if u"»" in w or u"”" in w:
                    inq = False
                continue
            newp = [low(p, lang) if (CAPW.match(p) and p not in KEEP and c not in KEEP) else p for p in parts]
            nc = "-".join(newp)
            if nc != c:
                for a, b in zip(parts, newp):
                    if a != b:
                        STAT.setdefault(lang, {}).setdefault(a, [0, name, s])[0] += 1
                w = w.replace(c, nc, 1)
        if u"»" in w or u"”" in w:
            inq = False
        out.append(w)
        prev = w
    return " ".join(out)


def html_heads(h, lang, name):
    def f(m):
        inner = m.group(2)
        if "<" in inner:
            return m.group(0)
        return m.group(1) + conv(inner, lang, name) + m.group(3)
    return re.sub(r"(<h[234][^>]*>)(.*?)(</h[234]>)", f, h, flags=re.S)


def walk(o, lang, name, key=None, btype=None):
    if isinstance(o, dict):
        bt = o.get("type", btype)
        for k, v in list(o.items()):
            if isinstance(v, str):
                if k == "html":
                    o[k] = html_heads(v, lang, name)
                elif k in HEAD_KEYS and not (k == "t" and bt == "quotes") and not (name.startswith("spec/") and (bt in ("timeline", "gallery") or k in ("title", "cap"))):
                    o[k] = conv(v, lang, name)
            else:
                walk(v, lang, name, k, bt)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            if isinstance(v, list) and v and all(isinstance(x, str) for x in v):
                if key in ("items", "btns", "cats") and btype in ("faq", "cta", "links", "stats", None, "articles") or key in ("btns", "cats", "head"):
                    j = 1 if (btype == "stats" or key == "cats") else 0          # stats: [число, подпись]; cats: [id, название]
                    if key == "head":
                        o[i] = [conv(x, lang, name) for x in v]
                    elif len(v) > j:
                        v[j] = conv(v[j], lang, name)
            elif isinstance(v, str) and key == "head":
                o[i] = conv(v, lang, name)
            else:
                walk(v, lang, name, key, btype)


n = 0
for fn in sorted(glob.glob(os.path.join(D, "data", "*", "*.json"))):
    name = os.path.relpath(fn, os.path.join(D, "data")).replace(os.sep, "/")
    raw = io.open(fn, encoding="utf-8").read()
    d = json.loads(raw)
    lang = d.get("lang") or name.split(".")[-2]
    before = json.dumps(d, ensure_ascii=False)
    walk(d, lang, name)
    if json.dumps(d, ensure_ascii=False) != before:
        n += 1
        if not SHOW:
            ind = None if "\n" not in raw.strip() else 1
            json.dump(d, io.open(fn, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=ind)
for lang in sorted(STAT):
    ws = sorted(STAT[lang].items(), key=lambda x: x[0])
    print("== %s: слов %d" % (lang, len(ws)))
    print("  ".join("%s·%d" % (w, v[0]) for w, v in ws))
print("файлов %s: %d" % ("изменится" if SHOW else "изменено", n))
