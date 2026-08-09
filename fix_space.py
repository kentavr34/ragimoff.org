# -*- coding: utf-8 -*-
"""
fix_space.py — пробел там, где его быть не должно.

«IDEA Part C . Fərdi Təhsil Planı», «kök hüceyrə müalicəsi yoxdur .»,
«Şizoaffektiv pozuntu ( 6A21 )», «qiymətləndirmə , valideyn müsahibəsi» —
след ручной правки внутри готовой вёрстки. Дефект есть и в азербайджанском
мастере, и в переводах.

Двоеточие не трогаем: в книге встречается запись отношения «1,2–1,9 : 1»,
где пробелы стоят намеренно.

Правится только текст между тегами внутри <main>; атрибуты, <style>
и <script> не затрагиваются.

    python fix_space.py            # отчёт
    python fix_space.py --apply
"""
from __future__ import annotations
import re, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
BOOK = ROOT / 'klinik-psixiatriya'
DIRS = {'az': BOOK, 'ru': BOOK / 'ru', 'en': BOOK / 'en', 'tr': BOOK / 'tr'}
APPLY = '--apply' in sys.argv

BEFORE = re.compile(r'[  ]+([,.;!?)\]»”])')
AFTER = re.compile(r'([(\[«“])[  ]+')


def main() -> int:
    total = {lg: 0 for lg in DIRS}
    files = 0
    for lg, d in DIRS.items():
        for fp in sorted(d.glob('*.html')):
            raw = fp.read_bytes().decode('utf-8')
            crlf = raw.count('\r\n') > raw.count('\n') // 2
            t = raw.replace('\r\n', '\n')
            m = re.search(r'<main[\s\S]*?</main>', t, re.I)
            if not m:
                continue
            body, pos, out, cnt = m.group(0), 0, [], 0
            for tag in re.finditer(r'<[^>]*>', body):
                chunk = body[pos:tag.start()]
                chunk, a = BEFORE.subn(r'\1', chunk)
                chunk, b = AFTER.subn(r'\1', chunk)
                cnt += a + b
                out.append(chunk); out.append(tag.group(0)); pos = tag.end()
            tail = body[pos:]
            tail, a = BEFORE.subn(r'\1', tail)
            tail, b = AFTER.subn(r'\1', tail)
            cnt += a + b
            out.append(tail)
            if not cnt:
                continue
            total[lg] += cnt
            files += 1
            if APPLY:
                t = t[:m.start()] + ''.join(out) + t[m.end():]
                fp.write_bytes((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))
    print('лишних пробелов у знаков препинания: '
          + ', '.join(f'{lg} {n}' for lg, n in total.items())
          + f' — всего {sum(total.values())} в {files} файлах')
    print('применено' if APPLY else 'пробный прогон — запустить с --apply')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
