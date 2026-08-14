#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_headers.py — собирает шапку каждой карточки книги из _codes_canon.json.

ЗАЧЕМ
=====
Шапка карточки (три классификации: XBT-11 / XBT-10 / DSM-5-TR, каждая со своим
кодом и своим названием) раньше правилась вручную на каждой из 412 страниц.
Из-за этого она разъезжалась: под всеми тремя кодами стояло одно и то же
название, коды DSM были обрезаны, английский подзаголовок был на половине
страниц. Теперь источник один — _codes_canon.json, раздел header_source.

КАК ПОЛЬЗОВАТЬСЯ
================
    python build_headers.py              # пробный прогон: показать расхождения
    python build_headers.py --apply      # записать

Правите данные в _codes_canon.json → запускаете с --apply → изменение
расходится по всем четырём языкам одинаково.

ПРОВЕРКА ЦЕЛОСТНОСТИ
====================
Скрипт идемпотентен: второй запуск подряд не должен менять ни одного файла.
Если меняет — значит, данные и страницы разошлись, и это надо разобрать.
"""
from __future__ import annotations
import json, re, sys, html
from pathlib import Path

ROOT = Path(__file__).parent
BOOK = ROOT / "klinik-psixiatriya"
CANON = ROOT / "_codes_canon.json"
DIRS = {"az": BOOK, "ru": BOOK / "ru", "en": BOOK / "en", "tr": BOOK / "tr"}
DH_RE = re.compile(r'<table class="dh">.*?</table>', re.S)


def esc(s: str) -> str:
    return html.escape(s or "", quote=False)


def render(row: dict, lang: str, labels: dict) -> str:
    """Собирает шапку: три строки, у каждой свой код и своё название."""
    title = row["title"].get(lang) or ""
    official = row["icd11_official"].get(lang) or ""
    # английский подзаголовок ВОЗ — один и тот же во всех языках
    subtitle = row["icd11_official"].get("en") or ""

    parts = ['<table class="dh"><tbody>']
    # 1. МКБ-11 — заголовок страницы
    parts.append(
        # Три колонки: ярлык | код | название. Раньше ярлык и код стояли
        # стопкой в одной ячейке, и при любом выравнивании край получался
        # рваным — разная длина и разный кегль давали лесенку. Решение
        # Кенана 2026-08-14: у каждого своя вертикаль.
        f'<tr class="dh-main"><td class="dh-lbl-c">'
        f'<span class="dh-lbl">{labels["icd11"][lang]}</span></td>'
        f'<td class="dh-code-c">'
        f'<span class="dh-code">{esc(row["icd11_shown"])}</span></td>'
        f'<td class="dh-name"><h1>{esc(title)}</h1>'
        # lang="en" — английское имя болезни внутри страницы на другом
        # языке; ставится здесь, чтобы пересборка его не стирала
        + (f'<div class="dh-en" lang="en">{esc(subtitle)}</div>' if subtitle else "")
        + "</td></tr>"
    )
    # 2. МКБ-10 — своё название
    c10 = row.get("icd10_code") or "—"
    n10 = row["icd10_name"].get(lang) or "—"
    parts.append(
        f'<tr><td class="dh-lbl-c"><span class="dh-lbl">{labels["icd10"][lang]}</span></td>'
        f'<td class="dh-code-c"><span class="dh-code">{esc(c10)}</span></td>'
        f'<td class="dh-name">{esc(n10)}</td></tr>'
    )
    # 3. DSM-5-TR — своё название (официальный перевод есть не на всех языках)
    cd = row.get("dsm_code") or "—"
    nd = row["dsm_name"].get(lang) or "—"
    parts.append(
        f'<tr><td class="dh-lbl-c"><span class="dh-lbl">{labels["dsm"]}</span></td>'
        f'<td class="dh-code-c"><span class="dh-code">{esc(cd)}</span></td>'
        f'<td class="dh-name">{esc(nd)}</td></tr>'
    )
    parts.append("</tbody></table>")
    return "".join(parts)


def main() -> int:
    apply = "--apply" in sys.argv
    canon = json.loads(CANON.read_text(encoding="utf-8"))
    src = canon.get("header_source")
    if not src:
        print("В _codes_canon.json нет раздела header_source — нечего собирать.")
        return 1
    labels = src["labels"]

    changed, same, missing = 0, 0, []
    diffs = []
    for row in src["rows"]:
        code = row["code"]
        for lang, d in DIRS.items():
            fp = d / f"{code}.html"
            if not fp.exists():
                missing.append(f"{lang}/{code}")
                continue
            t = fp.read_text(encoding="utf-8", errors="ignore")
            m = DH_RE.search(t)
            if not m:
                missing.append(f"{lang}/{code} (нет шапки)")
                continue
            new = render(row, lang, labels)
            if m.group(0) == new:
                same += 1
                continue
            changed += 1
            if len(diffs) < 12:
                old_t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " | ", m.group(0))).strip()
                new_t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " | ", new)).strip()
                diffs.append((f"{lang}/{code}", old_t[:96], new_t[:96]))
            if apply:
                fp.write_text(t[: m.start()] + new + t[m.end():], encoding="utf-8")

    print(f"{'ПРИМЕНЕНО' if apply else 'ПРОБНЫЙ ПРОГОН'}: "
          f"совпадает {same}, отличается {changed}, нет файла/шапки {len(missing)}")
    if missing:
        print("  отсутствуют:", ", ".join(missing[:10]))
    if diffs:
        print()
        for name, o, n in diffs:
            print(f"  {name}")
            print(f"     было : {o}")
            print(f"     стало: {n}")
    if not apply and changed:
        print("\nДля записи: python build_headers.py --apply")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
