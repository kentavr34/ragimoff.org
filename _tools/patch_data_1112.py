# -*- coding: utf-8 -*-
"""Правки данных после переноса (12.11.2026). Повторный запуск ничего не меняет.
1. Страница «Семейная терапия»: раздел об ОБУЧЕНИИ специалистов нёс старые и противоречивые цены (900 и 600 AZN) —
   обучение живёт на своей странице (program.html?p=family, цены из programs.js). Раздел заменён ссылкой на неё; вопрос о цене обучения снят.
2. Азербайджанская страница «Семейная терапия»: таблица цен консультаций → общий набор цен (числа те же, источник один)."""
import io, os, json, glob, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def has(o, s):
    return s in json.dumps(o, ensure_ascii=False)


for lang in ("ru", "az", "en"):
    fn = os.path.join(D, "data", "cons", "aile-terapiyasi.%s.json" % lang)
    d = json.load(io.open(fn, encoding="utf-8"))
    out, skip, ch = [], 0, 0
    bl = d["blocks"]
    for i, b in enumerate(bl):
        if skip:
            skip -= 1
            ch += 1
            continue
        if b["type"] == "groups" and has(b, "900 AZN"):
            out.append({"type": "links", "items": [[b["h"], "/%s/telim/aile-terapiyasi.html" % lang, b.get("sub", "")]]})
            ch += 1
            # следом идут текст об обучении (600 AZN) и кнопка «О преподавателе» — тот же раздел
            j = i + 1
            while j < len(bl) and j <= i + 2 and bl[j]["type"] in ("text", "cta") and not bl[j].get("h"):
                skip += 1
                j += 1
            continue
        if b["type"] == "faq":
            n = len(b["items"])
            b["items"] = [q for q in b["items"] if "600 AZN" not in q[1] and "900 AZN" not in q[1]]
            ch += n - len(b["items"])
        if b["type"] == "prices" and b.get("rows") and has(b["rows"], "AZN"):
            b = {"type": "prices", "h": b.get("h", ""), "sub": b.get("sub", ""), "set": "consult"}
            ch += 1
        out.append(b)
    d["blocks"] = out
    assert not has(d, "900 AZN") and not has(d, "600 AZN<") , lang
    json.dump(d, io.open(fn, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    print(lang, "изменений:", ch, "блоков:", len(out), "| остались суммы:", [x for x in ("900 AZN", "600 AZN") if has(d, x)])
