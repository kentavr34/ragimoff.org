# -*- coding: utf-8 -*-
"""Применяет список правок [code, lang, было, стало] из JSON ко всем деревьям."""
import sys, io, json
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
B = Path('klinik-psixiatriya')
T = {
    'az': [B, B / 'preview', Path('_supplements/chapters-v2')],
    'ru': [B / 'ru'],
    'en': [B / 'en'],
    'tr': [B / 'tr'],
}
T['*'] = [B, B / 'ru', B / 'en', B / 'tr', B / 'preview', Path('_supplements/chapters-v2')]

data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
ok = miss = 0
for code, lg, a, b in data:
    n = 0
    for tree in T[lg]:
        if not tree.is_dir():
            continue
        for fp in tree.glob(code + '.html'):
            t = fp.read_text(encoding='utf-8', errors='ignore')
            k = t.count(a)
            if k:
                fp.write_text(t.replace(a, b), encoding='utf-8')
                n += k
    if n:
        ok += 1
        print('  OK  {}/{} x{}'.format(lg, code, n))
    else:
        miss += 1
        print('  --  {}/{}: {}'.format(lg, code, a[:56]))
print('\nприменено правил {}, не найдено {}'.format(ok, miss))
