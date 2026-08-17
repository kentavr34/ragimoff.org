# -*- coding: utf-8 -*-
"""apply_style.py — перевод сайта на стиль страницы samira.html.

Что делает: подключает `js-hero-fit2.js` вместо `js-hero-fit.js`.
Этот скрипт и есть «стиль samira» в исполняемом виде:

  * ритм разделов 48 / 27 / 48, посчитанный ОПТИЧЕСКИ (с вычетом полулидинга),
    а не по рамкам элементов;
  * правило владельца «подзаголовок по ширине ≈ заголовку ±10 %»;
  * единый кегль заголовков одного уровня на мобильном;
  * нижняя граница кегля заголовка (24px) и верхняя у подзаголовка (18px) —
    чтобы подзаголовок не сравнялся с заголовком и не перерос его.

Старый `js-hero-fit.js` умеет только шапку: ритма разделов и правила пары
там нет вовсе.

Идемпотентен: повторный запуск ничего не меняет. Файлы без `.page-hero-x`
пропускаются — им подгонять нечего.

Запуск:
    python apply_style.py            # применить
    python apply_style.py --check    # только показать, что изменится
"""
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).parent
OLD = '<script src="js-hero-fit.js"></script>'
NEW = '<script src="js-hero-fit2.js"></script>'
# Языковые деревья подключают скрипт по относительному пути «../»
OLD_UP = '<script src="../js-hero-fit.js"></script>'
NEW_UP = '<script src="../js-hero-fit2.js"></script>'

# Книга живёт своей жизнью и в этот конвейер не входит (см. CLAUDE.md).
SKIP_DIRS = {'klinik-psixiatriya', '_supplements', '_partials', 'graphify-out', 'node_modules'}

check = '--check' in sys.argv

changed, skipped_no_hero, already, untouched = [], [], [], []

for path in sorted(ROOT.rglob('*.html')):
    rel = path.relative_to(ROOT)
    if any(part in SKIP_DIRS for part in rel.parts):
        continue

    raw = path.read_bytes()
    crlf = raw.count(b'\r\n') > raw.count(b'\n') // 2
    text = raw.decode('utf-8').replace('\r\n', '\n')

    if NEW in text or NEW_UP in text:
        already.append(str(rel))
        continue
    if OLD not in text and OLD_UP not in text:
        untouched.append(str(rel))
        continue
    # Подгонять нечего, если на странице нет шапки нужного типа.
    if 'page-hero-x' not in text:
        skipped_no_hero.append(str(rel))
        continue

    new_text = text.replace(OLD, NEW).replace(OLD_UP, NEW_UP)
    if not check:
        path.write_bytes((new_text.replace('\n', '\r\n') if crlf else new_text).encode('utf-8'))
    changed.append(str(rel))

print('Стиль samira → сайт')
print('  переведено:      %4d' % len(changed))
print('  уже на стиле:    %4d' % len(already))
print('  без шапки:       %4d' % len(skipped_no_hero))
print('  скрипт не нужен: %4d' % len(untouched))
if check:
    print('\n--check: файлы НЕ изменены')
if skipped_no_hero:
    print('\nБез .page-hero-x (пропущены):')
    for s in skipped_no_hero[:20]:
        print('   ', s)
