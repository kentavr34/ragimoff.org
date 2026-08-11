#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_yo.py — приводит русский перевод к последовательному «ё».

Книга писала одно и то же слово двояко: «распространённость» 50 раз и
«распространенность» 39, «ребёнка» 34 и «ребенка» 35, «отменён» 3 и
«отменен» 5. Восемьдесят семь таких семей.

Выбрано «всегда ё». Причина не в предпочтении: для КАЖДОЙ семьи форма с «ё»
уже есть в книге, то есть цель замены не придумывается, а берётся из текста.
Обратное направление (снять все «ё») потеряло бы различение и в справочнике
по медицине выглядело бы небрежностью.

Что скрипт НЕ делает. Он не восстанавливает «ё» там, где книга его нигде не
писала: угадывание «все»/«всё», «небо»/«нёбо», «падеж»/«падёж» по контексту —
задача, на которой ошибаются и люди. Список замен строится только по словам,
встреченным в книге в обоих написаниях; единственный кандидат в омографы
(«полет») прочитан по месту — обе строки о фобии полёта.

Замена идёт по видимому тексту внутри <main>, минуя <script> и <style>:
сплошная замена по файлу однажды уже сломала JavaScript на 137 страницах.

    python fix_yo.py --dry     показать, что будет заменено
    python fix_yo.py           заменить
"""
from __future__ import annotations
import re, sys, io
from pathlib import Path
from collections import Counter, defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
RU = ROOT / 'klinik-psixiatriya' / 'ru'
DRY = '--dry' in sys.argv

WORD = re.compile(r'[А-Яа-яЁё]{4,}')
BOUND_L, BOUND_R = '(?<![А-Яа-яЁё])', '(?![А-Яа-яЁё])'


def files() -> list[Path]:
    return sorted(RU.glob('*.html'))


def visible_spans(t: str):
    """Куски видимого текста внутри <main>: всё, что вне тегов и вне
    <script>/<style>. Возвращает (начало, конец) в исходной строке."""
    m = re.search(r'<main[\s\S]*</main>', t)
    if not m:
        return []
    lo, hi = m.start(), m.end()
    dead = [(mm.start(), mm.end())
            for mm in re.finditer(r'<(script|style)[\s\S]*?</\1>', t[lo:hi])]
    spans, pos = [], lo
    for mm in re.finditer(r'<[^>]*>', t[lo:hi]):
        a, b = lo + mm.start(), lo + mm.end()
        if pos < a:
            spans.append((pos, a))
        pos = b
    if pos < hi:
        spans.append((pos, hi))
    return [(a, b) for a, b in spans
            if not any(lo + d0 <= a and b <= lo + d1 for d0, d1 in dead)]


def build_map() -> dict[str, str]:
    """Пары «без ё» → «с ё» по словам, встреченным в книге в обоих видах."""
    forms = defaultdict(Counter)
    for fp in files():
        t = fp.read_text(encoding='utf-8', errors='ignore')
        for a, b in visible_spans(t):
            for w in WORD.findall(t[a:b]):
                forms[w.lower().replace('ё', 'е')][w.lower()] += 1
    out = {}
    for key, variants in forms.items():
        yo = [w for w in variants if 'ё' in w]
        no = [w for w in variants if 'ё' not in w]
        if len(yo) == 1 and no:
            out[no[0]] = yo[0]
    return out


def same_case(src: str, dst: str) -> str:
    return dst[0].upper() + dst[1:] if src[0].isupper() else dst


def main() -> int:
    pairs = build_map()
    print('=' * 72)
    print(f'ПОСЛЕДОВАТЕЛЬНОЕ «Ё» В РУССКОМ — {len(pairs)} семей слов')
    print('=' * 72)
    if not pairs:
        print('  нечего приводить: разнобоя нет')
        return 0

    rx = re.compile(BOUND_L + '(' + '|'.join(
        sorted((re.escape(w) for w in pairs), key=len, reverse=True)) + ')' + BOUND_R,
        re.IGNORECASE)

    total, touched = 0, 0
    seen = Counter()
    for fp in files():
        raw = fp.read_bytes()
        crlf = raw.count(b'\r\n') > raw.count(b'\n') // 2
        t = raw.decode('utf-8').replace('\r\n', '\n')
        spans = visible_spans(t)
        if not spans:
            continue
        out, last, n = [], 0, 0
        for a, b in spans:
            out.append(t[last:a])
            chunk = t[a:b]

            def rep(m):
                nonlocal n
                src = m.group(1)
                dst = pairs.get(src.lower())
                if not dst:
                    return src
                n += 1
                seen[src.lower()] += 1
                return same_case(src, dst)

            out.append(rx.sub(rep, chunk))
            last = b
        out.append(t[last:])
        if not n:
            continue
        total += n
        touched += 1
        if not DRY:
            new = ''.join(out)
            fp.write_bytes((new.replace('\n', '\r\n') if crlf else new).encode('utf-8'))

    print(f'  {"нашлось" if DRY else "заменено"}: {total} в {touched} файлах')
    for w, n in seen.most_common(20):
        print(f'      {w} → {pairs[w]}  ×{n}')
    if len(seen) > 20:
        print(f'      …ещё {len(seen) - 20} слов')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
