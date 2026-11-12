# -*- coding: utf-8 -*-
"""Заголовки как предложения в текстах программ (assets/js/programs.js): названия модулей, блоков, документов.
Правила и списки имён собственных — те же, что у sentence_case.py. Запуск: python sentence_case_js.py [show]"""
import io, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
src = io.open(os.path.join(HERE, "sentence_case.py"), encoding="utf-8").read()
src = src[:src.index("\nn = 0\nfor fn in sorted")].replace("__file__", repr(os.path.join(HERE, "sentence_case.py")))
ns = {}
exec(src, ns)
SHOW = len(sys.argv) > 1 and sys.argv[1] == "show"
P = os.path.join(HERE, "..", "assets", "js", "programs.js")
s = io.open(P, encoding="utf-8").read()
CH = []


def lang_of(t):
    if re.search(u"[А-Яа-яЁё]", t):
        return "ru"
    if re.search(u"[əƏıİğĞşŞ]", t):
        return "az"
    return "en"


def f(m):
    q, body = m.group(2), m.group(3)
    if "\\" in body:
        return m.group(0)
    new = ns["conv"](body, lang_of(body), "programs.js")
    if new != body:
        CH.append((body, new))
    return m.group(1) + q + new + q


out = re.sub(r"""(\bt: |"t": |\bh: )(['"])((?:(?!\2).)*)\2""", f, s)
for a, b in CH:
    print("  %s → %s" % (a, b))
print("строк %s: %d" % ("изменится" if SHOW else "изменено", len(CH)))
if not SHOW and out != s:
    io.open(P, "w", encoding="utf-8", newline="\n").write(out)
