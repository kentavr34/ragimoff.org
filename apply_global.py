# -*- coding: utf-8 -*-
"""Применяет список правок [lang, было, стало] ко всему языковому дереву."""
import sys, io, json
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
B = Path('klinik-psixiatriya')
# Изданные деревья — единственный источник истины. preview/ и
# _supplements/chapters-v2 были производными копиями со старой привязкой
# кодов (6C90↔6C91, 6C41=опиоиды, 6B60=ДРИ) и удалены 2026-08-09.
T = {
    'az': [B],
    'ru': [B / 'ru'],
    'en': [B / 'en'],
    'tr': [B / 'tr'],
}
T['*'] = [B, B / 'ru', B / 'en', B / 'tr']

data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
ok = miss = 0
for lg, a, b in data:
    n = files = 0
    for tree in T[lg]:
        if not tree.is_dir():
            continue
        for fp in sorted(tree.glob('*.html')):
            t = fp.read_text(encoding='utf-8', errors='ignore')
            k = t.count(a)
            if k:
                fp.write_text(t.replace(a, b), encoding='utf-8')
                n += k
                files += 1
    if n:
        ok += 1
        print('  OK  {} x{} в {} файлах: {}'.format(lg, n, files, a[:48]))
    else:
        miss += 1
        print('  --  {}: {}'.format(lg, a[:60]))
print('\nприменено правил {}, не найдено {}'.format(ok, miss))
