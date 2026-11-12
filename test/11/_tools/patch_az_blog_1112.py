# -*- coding: utf-8 -*-
"""Азербайджанские статьи блога: типовые турцизмы и кальки по канону книги «Klinik Psixiatriya» (вычитка 12.11.2026).
anksiyete → təşviş, stress → stres, online → onlayn, oflayn → əyani, atak → tutma, tetiklə- → tətiklə-, yaşam → həyat.
Списки литературы (английские названия работ) не трогаются. Повторный запуск ничего не меняет.
Заодно: число книг Фрейда — 25, как в действующем магазине."""
import io, os, re, sys, json, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
W = u"(?![a-zəğıöüşçA-ZƏĞIİÖÜŞÇ])"
B = u"(?<![a-zəğıöüşçA-ZƏĞIİÖÜŞÇ])"
RULES = [(u"nksiyetenin", u"əşvişin"), (u"nksiyet[eə]si", u"əşvişi"), (u"nksiyetəli", u"əşvişli"), (u"nksiyetəm" + W, u"əşvişim"), (u"nksiyete", u"əşviş")]
# первая буква слова заменяется отдельно: anksiyete → təşviş, Anksiyete → Təşviş
PAIRS = [(B + u"a(?=əşviş)", u"t"), (B + u"A(?=əşviş)", u"T"),
         (u"tress", u"tres"), (u"TRESS", u"TRES"),
         (B + u"online" + W, u"onlayn"), (B + u"Online" + W, u"Onlayn"), (B + u"oflayn" + W, u"əyani"), (B + u"Oflayn" + W, u"Əyani"),
         (u"sixoeğitim", u"sixoedukasiya"), (u"etikle", u"ətiklə"), (u"etiklə", u"ətiklə"),
         (B + u"ataklar", u"tutmalar"), (B + u"Ataklar", u"Tutmalar"), (B + u"atakı" + W, u"tutmanı"), (B + u"atakdan" + W, u"tutmadan"),
         (B + u"atak" + W, u"tutma"), (B + u"Atak" + W, u"Tutma"), (B + u"yaşam" + W, u"həyat"), (B + u"Yaşam" + W, u"Həyat")]


def fix(s):
    for a, b in RULES + PAIRS:
        s = re.sub(a, b, s)
    return s


def walk(o):
    if isinstance(o, dict):
        if o.get("type") == "sources":
            return
        for k, v in list(o.items()):
            if k in ("slug", "src", "img", "cover", "cat", "edited", "lang", "sources"):
                continue
            if isinstance(v, str):
                if k == "html":                      # в статье список литературы стоит после заголовка «Mənbələr» — его не трогаем
                    i = v.find(u"Mənbələr")
                    o[k] = fix(v[:i]) + v[i:] if i > 0 else fix(v)
                else:
                    o[k] = fix(v)
            else:
                walk(v)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            if isinstance(v, str):
                o[i] = fix(v)
            else:
                walk(v)


n = 0
for fn in sorted(glob.glob("data/blog/*.az.json")):
    raw = io.open(fn, encoding="utf-8").read()
    d = json.loads(raw)
    before = json.dumps(d, ensure_ascii=False)
    walk(d)
    if json.dumps(d, ensure_ascii=False) != before:
        d.setdefault("edited", u"12.11.2026: термины по канону книги (təşviş, stres, tutma, onlayn)")
        for _ in range(5):
            try:
                json.dump(d, io.open(fn, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=(1 if "\n" in raw.strip() else None))
                break
            except OSError:
                import time; time.sleep(1.5)
        n += 1
print("азербайджанских статей исправлено:", n)

# число книг Фрейда — как в действующем магазине (25)
for p, pairs in (("assets/js/content.js", [(u"вошли 22 книги Фрейда", u"вошли 25 книг Фрейда"), (u"Freydin 22 kitabı", u"Freydin 25 kitabı"), (u"22 books by Freud", u"25 books by Freud"), (u"22 of Freud’s books", u"25 of Freud’s books")]),
                 ("assets/js/programs.js", [(u"все 24 книги", u"все 25 книг"), (u"24 kitabı", u"25 kitabı"), (u"24 books", u"25 books")])):
    s = io.open(p, encoding="utf-8").read()
    o = s
    for a, b in pairs:
        s = s.replace(a, b)
    if s != o:
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)
        print("число книг Фрейда:", p)
