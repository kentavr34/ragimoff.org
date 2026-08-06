#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_sections.py — собирает заголовки разделов и внутристраничное оглавление
карточек из _codes_canon.json (раздел section_source).

ЗАЧЕМ
=====
Названия разделов правились россыпью скриптов по каждому языку отдельно, из-за
чего расходились: в турецком разделы 3, 6 и 9 оставались азербайджанскими, в
переводах пять пунктов оглавления были набраны строчными, раздел 5 назывался
вопреки канону. Теперь источник один.

КАК ПОЛЬЗОВАТЬСЯ
================
    python build_sections.py             # пробный прогон: показать расхождения
    python build_sections.py --apply     # записать
    python build_sections.py --lang ru   # только один язык

Меняете название раздела в _codes_canon.json → запускаете → оно меняется и в
заголовке, и в оглавлении, на всех страницах этого языка сразу.

ЧТО НЕ ТРОГАЕТСЯ
================
Текст внутри разделов. Скрипт правит только строку <h2> и блок page-toc;
содержимое между разделами остаётся как есть.

ПРОВЕРКА
========
Идемпотентен: второй запуск подряд не должен менять ни одного файла.
"""
from __future__ import annotations
import json, re, sys, html
from pathlib import Path

ROOT = Path(__file__).parent
BOOK = ROOT / "klinik-psixiatriya"
CANON = ROOT / "_codes_canon.json"
DIRS = {"az": BOOK, "ru": BOOK / "ru", "en": BOOK / "en", "tr": BOOK / "tr"}

H2_RE = re.compile(r'<h2 id="([^"]+)">(.*?)</h2>', re.S)
TOC_RE = re.compile(r'<nav class="page-toc">.*?</nav>', re.S)


def esc(s: str) -> str:
    return html.escape(s or "", quote=False)


def layout_for(src: dict, code: str):
    for name, lay in src["layouts"].items():
        if code in lay["codes"]:
            return lay
    return None


def main() -> int:
    apply = "--apply" in sys.argv
    only = None
    if "--lang" in sys.argv:
        only = sys.argv[sys.argv.index("--lang") + 1]

    canon = json.loads(CANON.read_text(encoding="utf-8"))
    src = canon.get("section_source")
    if not src:
        print("В _codes_canon.json нет раздела section_source.")
        return 1

    codes = sorted({c for lay in src["layouts"].values() for c in lay["codes"]})
    changed_h2 = changed_toc = same = 0
    diffs = []

    for code in codes:
        lay = layout_for(src, code)
        if not lay:
            continue
        for lang, d in DIRS.items():
            if only and lang != only:
                continue
            fp = d / f"{code}.html"
            if not fp.exists():
                continue
            titles = lay["titles"].get(lang)
            if not titles:
                continue
            slugs = lay["slugs"]
            prefix = code.lower()
            t = fp.read_text(encoding="utf-8", errors="ignore")
            orig = t

            # 1. заголовки разделов
            idx = [0]

            def fix_h2(m):
                k = idx[0]
                idx[0] += 1
                if k >= len(titles):
                    return m.group(0)
                return f'<h2 id="{prefix}-{slugs[k]}">{esc(titles[k])}</h2>'

            t = H2_RE.sub(fix_h2, t)

            # 2. внутристраничное оглавление — без номера, как в книге
            toc = '<nav class="page-toc">' + "".join(
                f'<a href="#{prefix}-{slugs[k]}">'
                f'{esc(re.sub(chr(94) + r"[0-9]+[.] *", "", titles[k]))}</a>'
                for k in range(len(titles))
            ) + "</nav>"
            t2, n = TOC_RE.subn(lambda m: toc, t, count=1)
            if n:
                t = t2

            if t == orig:
                same += 1
                continue
            if H2_RE.search(orig) and [m.group(0) for m in H2_RE.finditer(orig)] != \
               [m.group(0) for m in H2_RE.finditer(t)]:
                changed_h2 += 1
            else:
                changed_toc += 1
            if len(diffs) < 10:
                o = TOC_RE.search(orig)
                n2 = TOC_RE.search(t)
                diffs.append((f"{lang}/{code}",
                              re.sub(r"<[^>]+>", " ", o.group(0))[:90].strip() if o else "",
                              re.sub(r"<[^>]+>", " ", n2.group(0))[:90].strip() if n2 else ""))
            if apply:
                fp.write_text(t, encoding="utf-8")

    print(f'{"ПРИМЕНЕНО" if apply else "ПРОБНЫЙ ПРОГОН"}: '
          f"без изменений {same}, изменено заголовков {changed_h2}, оглавлений {changed_toc}")
    for name, o, n in diffs:
        print(f"  {name}")
        print(f"     было : {o}")
        print(f"     стало: {n}")
    if not apply and (changed_h2 or changed_toc):
        print("\nДля записи: python build_sections.py --apply")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
