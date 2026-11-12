# -*- coding: utf-8 -*-
"""Страж столкновения имён в стилях (урок 12.11.2026: правило «.posts» для страницы блога переопределило
одноимённый блок главной и сломало согласованный вид). Проверяет site.css: селектор, объявленный в части главной
страницы, не должен объявляться заново «голым» в части внутренних страниц (после метки PG).
Разрешённые намеренные переопределения — в css_collide_allow.txt (по одному селектору в строке, с причиной после #).
Запуск: python css_collide.py   → список столкновений, код возврата 1 при их наличии."""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
css = io.open(os.path.join(D, "assets", "css", "site.css"), encoding="utf-8").read()
MARK = "PG: внутренние страницы"
i = css.index(MARK)
allow_f = os.path.join(os.path.dirname(__file__), "css_collide_allow.txt")
ALLOW = set(l.split("#")[0].strip() for l in io.open(allow_f, encoding="utf-8").read().splitlines() if l.split("#")[0].strip()) if os.path.exists(allow_f) else set()


def selectors(text):
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    out = {}
    for m in re.finditer(r"([^{}]+)\{[^{}]*\}", text):
        for s in m.group(1).split(","):
            s = " ".join(s.split())
            if s and not s.startswith("@") and re.match(r"^\.[\w-]+$", s):
                out[s] = out.get(s, 0) + 1
    return out


home, inner = selectors(css[:i]), selectors(css[i:])
bad = sorted(s for s in inner if s in home and s not in ALLOW)
for s in bad:
    print("столкновение: %s объявлен и для главной, и заново для внутренних страниц" % s)
print("столкновений:", len(bad))
sys.exit(1 if bad else 0)
