# -*- coding: utf-8 -*-
"""Цены долгих программ везде приведены к одному: рассрочка до 24 месяцев от полной цены
(4 200 / 6 600 / 3 600 AZN → от 175 / 275 / 150 AZN в месяц). Слово владельца 12.11.2026.
Карточки главной (content.js) и таблицы цен на страницах программ (programs.js). Повторный запуск ничего не меняет."""
import io, os, re, sys
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)


def save(p, s):
    t = p + ".new"
    io.open(t, "w", encoding="utf-8", newline="\n").write(s)
    os.replace(t, p)


n = 0
p = "assets/js/content.js"
s = io.open(p, encoding="utf-8").read()
s0 = s
for a, b in (("от 175 AZN в месяц", "от 150 AZN в месяц"), ("от 200 AZN в месяц", "от 175 AZN в месяц"), ("от 300 AZN в месяц", "от 275 AZN в месяц"),
             ("ayda 175 AZN-dən", "ayda 150 AZN-dən"), ("ayda 200 AZN-dən", "ayda 175 AZN-dən"), ("ayda 300 AZN-dən", "ayda 275 AZN-dən"),
             ("from 175 AZN a month", "from 150 AZN a month"), ("from 200 AZN a month", "from 175 AZN a month"), ("from 300 AZN a month", "from 275 AZN a month")):
    if "от 150 AZN" in s0 or "ayda 150" in s0:      # уже применено
        break
    n += s.count(a)
    s = s.replace(a, b)
if s != s0:
    save(p, s)

p = "assets/js/programs.js"
L = io.open(p, encoding="utf-8").read().split("\n")
MIN = {"4200": "175", "6600": "275", "3600": "150"}
for i, l in enumerate(L):
    if "rows:" not in l:
        continue
    m = re.search(r"'(4[ , ]?200|6[ , ]?600|3[ , ]?600) AZN'", l)
    if not m:
        continue
    want = MIN[re.sub(r"\D", "", m.group(1))]
    new = re.sub(r"(24[^\]]*?')(\d+)( AZN)", lambda k: k.group(1) + want + k.group(3), l)
    if new != l:
        L[i] = new
        n += 1
    if i + 1 < len(L) and "note:" in L[i + 1]:
        nn = re.sub(r"(\D)(\d{3})( AZN)", lambda k: k.group(1) + want + k.group(3), L[i + 1], count=1)
        if nn != L[i + 1]:
            L[i + 1] = nn
            n += 1
save(p, "\n".join(L))
print("changed:", n)
