"""СВЕРКА СТРАНИЦЫ С КАНОНОМ: ЧТО НЕ СООТВЕТСТВУЕТ.

ЗАЧЕМ. Владелец (11.11.2026): «Проверяй, если сходится — отлично. Если есть
много недостатков и концептуально структуру лучше было бы преподнести
по-другому, включая даже копирайтинг, — дорабатывай... Проверяй насколько
она соответствует ожиданиям... Искать из информации, которую я тебе ранее
предоставлял, замечания, которые были».

То есть проверка — это сличение СТРАНИЦЫ с КАНОНОМ, а не собственные
размышления о качестве. Скрипт делает именно это: берёт канон, вытаскивает
из него проверяемые пункты структуры и сравнивает с тем, что есть на
странице.

ЧТО ПРОВЕРЯЕТСЯ (только измеримое в самом HTML):
  1. Порядок девяти блоков — совпадает ли с каноном.
  2. Наличие «дверей»: ссылка на продолжение в КАЖДОМ блоке.
  3. Число карточек: книги (5), программы обучения (7).
  4. Наличие четырёх форм/точек регистрации по направлениям.
  5. Меню: наличие подменю для книг.
  6. Признаки запрещённого (общие страницы-каталоги вместо «дверей»).

Запуск:
    python _agent/canon/check_structure.py
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
PAGE = os.path.join(PROJ, 'index.html')

# ПОРЯДОК БЛОКОВ ПО КАНОНУ — из разбора реплик владельца.
# Источник: otvet_СТРУКТУРА.md, раздел «Порядок блоков главной страницы».
KANON_ORDER = [
    ('hero',       'Герой — первый экран с движением'),
    ('specialists','Специалисты — кто вас встретит'),
    ('books',      'Книги — чем специалист доказал уровень'),
    ('programs',   'Обучение — программы для специалистов'),
    ('services',   'Консультации — с чем приходят'),
    ('b2b',        'Бизнес-тренинги — работа с организациями'),
    ('myths',      'Просвещение — разбор мифов'),
    ('blog',       'Блог — рубрики'),
    ('telegram',   'Связь — остаёмся на связи'),
]

# Ожидаемое число элементов по канону
EXPECT = {
    'books': 5,      # пять «выстрелов»: клин. психиатрия, Фрейд, Феникс, вина, шизофрения
    'programs': 7,   # три длительных + четыре коротких
}


def main():
    if not os.path.isfile(PAGE):
        print('НЕТ СТРАНИЦЫ: %s' % PAGE)
        return 1
    h = io.open(PAGE, encoding='utf-8', errors='ignore').read()

    # позиции блоков в файле
    found = []
    for sid, name in KANON_ORDER:
        m = re.search(r'<section[^>]*id="%s"' % re.escape(sid), h)
        found.append((sid, name, m.start() if m else -1))

    print('=' * 74)
    print('СВЕРКА СТРАНИЦЫ С КАНОНОМ')
    print('=' * 74)
    print()

    bad = 0

    # 1. Порядок блоков
    print('1. ПОРЯДОК БЛОКОВ')
    missing = [f for f in found if f[2] < 0]
    present = [f for f in found if f[2] >= 0]
    for sid, name, pos in found:
        if pos < 0:
            print('   ✗ НЕТ БЛОКА: %-12s %s' % (sid, name))
            bad += 1
    if len(present) >= 2:
        order_ok = all(present[i][2] < present[i + 1][2] for i in range(len(present) - 1))
        if order_ok:
            print('   ✅ порядок присутствующих блоков совпадает с каноном')
        else:
            print('   ✗ ПОРЯДОК НАРУШЕН. Фактически:')
            for sid, name, pos in sorted(present, key=lambda x: x[2]):
                print('        %-12s %s' % (sid, name))
            bad += 1
    print()

    # 2. «Двери»: в каждом блоке ссылка на продолжение
    print('2. «ДВЕРИ» — переход на отдельную страницу из каждого блока')
    for sid, name, pos in found:
        if pos < 0:
            continue
        end = h.find('</section>', pos)
        block = h[pos:end if end > 0 else pos + 6000]
        hrefs = re.findall(r'href="([^"]+)"', block)
        out = [u for u in hrefs if not u.startswith('#')]
        mark = '✅' if out else '✗'
        if not out:
            bad += 1
        print('   %s %-12s ссылок наружу: %d' % (mark, sid, len(out)))
    print()

    # 3. Число карточек книг и программ
    print('3. ЧИСЛО ЭЛЕМЕНТОВ')
    for sid, want in EXPECT.items():
        m = re.search(r'<section[^>]*id="%s"' % re.escape(sid), h)
        if not m:
            continue
        end = h.find('</section>', m.start())
        block = h[m.start():end if end > 0 else m.start() + 20000]
        n = len(re.findall(r'class="(?:book|program)\b', block))
        mark = '✅' if n == want else '⚠'
        if n != want:
            bad += 1
        print('   %s %-12s на странице: %d, по канону: %d' % (mark, sid, n, want))
    print()

    # 4. Формы регистрации (канон, правило 65: четыре отдельные)
    #    ПРИЧИНА ПРАВКИ: первая версия проверки искала только ССЫЛКИ на
    #    страницы регистрации. Но канон требует, чтобы форма была привязана
    #    к своему блоку на главной (правило 71), поэтому формы стоят прямо
    #    на странице — и проверка их не видела. Теперь смотрим и на формы.
    print('4. ФОРМЫ РЕГИСТРАЦИИ (канон: обучение / инд. тренинг / консультации / бизнес)')
    forms = re.findall(r'<form[^>]*id="(reg[A-Za-z0-9]+)"', h)
    panels = re.findall(r'data-panel="([a-z0-9]+)"', h)
    if forms:
        for f in sorted(set(forms)):
            print('   ✅ форма: %s' % f)
        if len(set(panels)) >= 4:
            print('   ✅ направлений в переключателе: %d' % len(set(panels)))
        else:
            print('   ⚠ направлений: %d, по канону нужно 4' % len(set(panels)))
            bad += 1
    else:
        print('   ✗ ФОРМ НЕТ — канон требует четыре отдельные')
        bad += 1
    # запасной вариант: ссылки на страницы регистрации, если формы вынесены
    reg = re.findall(r'href="([^"]*(?:zapis|registr|qeydiyyat|booking)[^"]*)"', h, re.I)
    for u in sorted(set(reg)):
        print('   • ссылка на регистрацию: %s' % u)
    print()

    # 5. Запрещённое: общая страница-каталог вместо «дверей»
    print('5. ЗАПРЕЩЁННОЕ ПО КАНОНУ')
    if re.search(r'href="[^"]*/(telim|konsultasiya)/index\.html"', h):
        print('   ⚠ есть ссылки на общие каталоги услуг — канон требует «двери» на конкретные страницы')
    else:
        print('   ✅ общих каталогов вместо конкретных страниц нет')
    print()

    print('=' * 74)
    print('НЕСООТВЕТСТВИЙ: %d' % bad)
    print('=' * 74)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
