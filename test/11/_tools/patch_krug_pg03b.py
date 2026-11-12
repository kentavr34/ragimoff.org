# -*- coding: utf-8 -*-
"""Третий круг критика, мелочи (12.11.2026). Повторный запуск ничего не меняет.
 - азербайджанские термины по канону книги: «pozğunluq» → «pozuntu», турцизм «panik atak» → «panik tutması»;
 - названия тем одинаковы на главной и на страницах; надпись над заголовком энуреза одинакова по смыслу на трёх языках;
 - страница Кенана: азербайджанский подзаголовок 1:1 с русским и английским;
 - «e-qanun.az» не рвётся по дефису; подвал: «Юридические основы»."""
import io, os, re, sys, json, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
B = u"(?![a-zəğıöüşçA-ZƏĞIİÖÜŞÇ])"          # конец слова
AZ = [(u"ozğunluğun" + B, u"ozuntunun"), (u"ozğunluqla" + B, u"ozuntu ilə"), (u"ozğunluğu", u"ozuntusu"), (u"ozğunluq", u"ozuntu"),
      (u"anik ataklardan", u"anik tutmalarından"), (u"anik ataklarla", u"anik tutmaları ilə"), (u"anik atakların", u"anik tutmalarının"), (u"anik ataklar", u"anik tutmaları"),
      (u"anik atakdan", u"anik tutmasından"), (u"anik atakdır", u"anik tutmasıdır"), (u"anik atakın", u"anik tutmasının"), (u"anik atakı" + B, u"anik tutmasını"),
      (u"anik atak" + B, u"anik tutması"),
      (u"klinik və psixoloji mənzərəsi", u"klinik və psixoloji təzahürləri")]
n = 0
for fn in sorted(glob.glob("data/*/*.az.json")):
    raw = io.open(fn, encoding="utf-8").read()
    s = raw
    for a, b in AZ:
        s = re.sub(a, b, s)
    if s != raw:
        d = json.loads(s)
        if "blocks" in d or "items" in d:
            d.setdefault("edited", u"12.11.2026: термины по канону книги (pozuntu, panik tutması)")
        json.dump(d, io.open(fn, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=(1 if "\n" in raw.strip() else None))
        n += 1
print("азербайджанских файлов с терминами:", n)

TITLE = {"panik-ataklar": {"az": u"Panik tutmaları"}, "depressiya": {"ru": u"Депрессия", "az": u"Depressiya", "en": u"Depression"},
         "sosial-fobiya": {"ru": u"Социальная фобия"}}
EYE = {"ru": u"ДЕТСКАЯ ТЕРАПИЯ", "az": u"UŞAQ TERAPİYASI", "en": u"CHILD THERAPY"}
for slug, m in TITLE.items():
    for l, t in m.items():
        fn = "data/cons/%s.%s.json" % (slug, l)
        d = json.load(io.open(fn, encoding="utf-8"))
        if d["title"] != t:
            d["title"] = t
            d.setdefault("edited", u"12.11.2026: название темы как на главной")
            json.dump(d, io.open(fn, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
            print("название:", fn)
for l, e in EYE.items():
    fn = "data/cons/enurez.%s.json" % l
    d = json.load(io.open(fn, encoding="utf-8"))
    if d["eye"] != e:
        d["eye"] = e
        json.dump(d, io.open(fn, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
fn = "data/spec/kenan.az.json"
d = json.load(io.open(fn, encoding="utf-8"))
L = u"IPAS Ambasadoru · Həkim-psixoterapevt · Bexterev İnstitutunun məzunu. Azərbaycanda 23 il klinik psixoterapiya."
if d["lead"] != L:
    d["lead"] = L
    json.dump(d, io.open(fn, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    print("подзаголовок:", fn)

p = "_tools/build_law.py"
s = io.open(p, encoding="utf-8").read()
if u"e‑qanun.az" not in s:
    s = s.replace(u"портале e-qanun.az", u"портале e‑qanun.az").replace(u"e-qanun.az portalında", u"e‑qanun.az portalında").replace(u"on the e-qanun.az portal", u"on the e‑qanun.az portal")
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
p = "assets/js/content.js"
s = io.open(p, encoding="utf-8").read()
if u"'Правовые основы'" in s:
    s = s.replace(u"'Правовые основы'", u"'Юридические основы'")
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("подвал: Юридические основы")
