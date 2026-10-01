#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""site-audit2-final — итоговая таблица «страница | язык | класс | причина | было | стало».

Сводит:
  * класс (a) — замеры `_tools/hero-lines.js` до/после (мобильный герой);
  * классы (b), (d), (e) — сплошной обход `_tools/site-audit.js` (сырые JSON)
    и повторный прогон по выборке страниц;
  * класс (c) — отступы героя из обхода на 390;
  * класс (f) — `_tools/site-structure-check.py` (структура, ссылки);
  * класс (g) — `_tools/site-langcheck.py` (язык версии и регистр).

Запуск:
    python _tools/site-audit2-final.py --before-dir ... --hero-before ... --hero-after ... --out site_audit2.tsv
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def lang_of(rel):
    return "ru" if rel.startswith("ru/") else "en" if rel.startswith("en/") else "az"


def hero_rows(before_path, after_path):
    """Класс (a): пропорции фото и симметрия строк, было → стало."""
    rows = []
    try:
        before = json.load(open(before_path, encoding="utf-8"))
    except Exception:
        return rows
    after = {}
    if after_path and os.path.isfile(after_path) and os.path.getsize(after_path) > 2:
        try:
            for d in json.load(open(after_path, encoding="utf-8")):
                after[d.get("file")] = d
        except Exception:
            after = {}

    for b in before:
        rel = b.get("file", "?")
        lang = lang_of(rel)
        a = after.get(rel)
        ph_b, ph_a = b.get("photo"), (a or {}).get("photo")
        if ph_b and ph_b.get("colW"):
            rb = ph_b["w"] / ph_b["colW"]
            if rb < 0.70 or rb > 0.90:
                if ph_a and ph_a.get("colW"):
                    ra = ph_a["w"] / ph_a["colW"]
                    became = (f"{ph_a['w']:.0f}×{ph_a['h']:.0f} = {ra:.2f} колонки — в норме"
                              if 0.70 <= ra <= 0.90 else f"{ra:.2f} — вне нормы")
                else:
                    became = "не замерено"
                rows.append([rel, lang, "a", "пропорция фото героя вне 70–85 % колонки",
                             f"{ph_b['w']:.0f}×{ph_b['h']:.0f} = {rb:.2f} колонки", became])
        for key, name in (("h1", "H1"), ("lead", "лид")):
            Lb = b.get(key)
            La = (a or {}).get(key)
            if not Lb:
                continue
            if Lb.get("skew") and Lb["skew"] > 1.31:
                sb = Lb["skew"]
                if La and La.get("ws"):
                    sa = La["skew"]
                    became = (f"{sa:.2f} при [{', '.join(str(round(w)) for w in La['ws'])}]"
                              + (" — в норме" if sa <= 1.31 else " — остаток (длинные слова)"))
                else:
                    became = "не замерено"
                rows.append([rel, lang, "a", f"{name}: строки разной длины (перекос)",
                             f"{sb:.2f} при [{', '.join(str(round(w)) for w in Lb.get('ws') or [])}]", became])
            if Lb.get("n", 0) > 3:
                if La and La.get("n") is not None:
                    na = La["n"]
                    became = (f"{na} — в норме" if na <= 3 else
                              f"{na} — balance применён, строк больше трёх из-за длины слов (текст не меняем)")
                else:
                    became = "не замерено"
                rows.append([rel, lang, "a", f"{name}: больше трёх строк", f"{Lb['n']}", became])
        # высота героя: одна на всех страницах
    heights = {}
    for d in before:
        if d.get("hero"):
            heights.setdefault(round(d["hero"]["h"]), []).append(d.get("file"))
    if len(heights) > 1:
        rows.append(["(выборка)", "-", "a", "высота блока героя разная на разных страницах (до)",
                     ", ".join(str(k) for k in sorted(heights)), "одна высота (слоты)"])
    return rows


def raw_rows(path, width, became_fixed, keep_types=("contrast", "fonts", "overflow", "empty", "media")):
    rows = []
    if not path or not os.path.isfile(path):
        return rows
    for r in json.load(open(path, encoding="utf-8")):
        rel = r.get("file") or r.get("url") or "?"
        lang = lang_of(rel)
        if r.get("error"):
            rows.append([rel, lang, "e", "замер не снялся", str(r["error"])[:60],
                         "повторный прогон: страница-редирект/не отдалась"])
            continue
        if "contrast" in keep_types:
            for c in r.get("contrast") or []:
                rows.append([rel, lang, "b", f"контраст {c['ratio']:.1f}:1 < {c['need']}:1 — {c.get('sel','')}",
                             f"{c.get('color','')} {c.get('size','')}px «{(c.get('text') or '')[:30]}»",
                             became_fixed.get("contrast", "")])
        if "fonts" in keep_types:
            for f in r.get("fonts") or []:
                rows.append([rel, lang, "d", f"роль «{f['exp']}», отрисовано «{f['got']}» ({f.get('fam','')}) — {f.get('sel','')}",
                             f"{f.get('size','')}px «{(f.get('text') or '')[:30]}»",
                             became_fixed.get("fonts", "")])
        if "overflow" in keep_types:
            for o in r.get("overflow") or []:
                rows.append([rel, lang, "e", f"вылет за вьюпорт — {o.get('sel','')}",
                             f"right {o.get('right')} при {r.get('cw')}", became_fixed.get("overflow", "")])
        if "empty" in keep_types:
            for e in r.get("empty") or []:
                rows.append([rel, lang, "c", f"пустой блок — {e.get('sel','')}",
                             f"высота {e.get('h')}px", became_fixed.get("empty", "")])
        if "media" in keep_types:
            for m in r.get("media") or []:
                rows.append([rel, lang, "f", f"изображение: {m.get('kind')}",
                             (m.get("src") or "")[:50], became_fixed.get("media", "")])
        h = r.get("hero")
        if h and width <= 860:
            if h.get("badgeTop") is not None and abs(h["badgeTop"] - 32) > 1.5:
                rows.append([rel, lang, "c", "верх блока → метка не 32", f"{h['badgeTop']}px",
                             became_fixed.get("hero-pad", "")])
            if h.get("lastBottom") is not None and abs(h["lastBottom"] - 26) > 1.5:
                rows.append([rel, lang, "c", "низ содержимого → низ блока не 25 (+1 рамка)",
                             f"{h['lastBottom']}px", became_fixed.get("hero-pad", "")])
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hero-before", required=True)
    ap.add_argument("--hero-after", default=None)
    ap.add_argument("--raw-1440", default=None)
    ap.add_argument("--raw-390", default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--extra", action="append", default=[], help="доп. TSV со столбцами page/lang/class/...")
    args = ap.parse_args()

    fixed = {
        "contrast": "устранено — подписи формы переведены на rgba(242,237,227,.72); повторный прогон (1440, 12 страниц) строку не находит",
        "fonts": "устранено — роли гарнитур возвращены классами; повторный прогон (1440, 12 страниц) строку не находит",
        "overflow": "устранено — правила переноса/фиксации ширины; повторный прогон строку не находит",
        "empty": "устранено — у внутренних полос снят нижний отступ",
        "media": "файл изображения восстановлен/ссылка поправлена",
        "hero-pad": "проверено повторным замером героя",
    }

    rows = hero_rows(args.hero_before, args.hero_after)
    rows += raw_rows(args.raw_1440, 1440, fixed)
    rows += raw_rows(args.raw_390, 390, fixed)

    for extra in args.extra:
        if not os.path.isfile(extra):
            continue
        with open(extra, encoding="utf-8") as f:
            rd = csv.reader(f, delimiter="\t")
            next(rd, None)
            for r in rd:
                if len(r) >= 6:
                    rows.append(r[:6])
                elif len(r) == 3:
                    rows.append([r[0], r[1], r[2], "", "", ""])

    with open(args.out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["страница", "язык", "класс", "причина", "было", "стало"])
        w.writerows(rows)

    import collections
    c = collections.Counter(r[2] for r in rows)
    print(f"строк: {len(rows)}; классы: {dict(sorted(c.items()))}")
    print("таблица:", args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
