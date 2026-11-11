"""ПРОВЕРКА ЦИТАТ В ФАЙЛАХ КАНОНА.

ЗАЧЕМ. Разборы реплик делали отдельные агенты, и каждый отчитался, что
«все цитаты проверены». Отчёт агента — не доказательство: агент может
ошибиться или приукрасить. Владелец неоднократно получал именно такое:
заявлено «готово», а на деле не так.

ЧТО ДЕЛАЕТ. Берёт все цитаты вида «...» из файлов канона и проверяет,
что каждая дословно присутствует в исходных репликах владельца. Цитата,
которой нет в источнике, — выдумка, и она должна быть видна.

ИСТОЧНИКИ (из архива ЦНС, извлечены extract.py):
    _агент/cns_dialogs/_все_реплики.json       — 368 реплик
    _агент/cns_dialogs/_реплики_о_сайте.json   — 185 реплик

Запуск:
    python _agent/canon/verify_quotes.py
"""
import glob
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DLG = os.path.join(os.path.dirname(HERE), 'cns_dialogs')

# Цитаты записаны в кавычках-ёлочках «...». Внутри могут быть любые символы,
# включая переводы строк, поэтому берём нежадно и с DOTALL.
QUOTE = re.compile(r'«(.+?)»', re.S)

# Короткие фрагменты пропускаем: в служебных подписях тоже есть кавычки,
# и проверять «правила» длиной 5 символов бессмысленно.
MIN_LEN = 30


def norm(s):
    """Приводит текст к виду, пригодному для сравнения: убирает различия
    в пробелах и переводах строк, которые не меняют смысл."""
    s = s.replace('\u00a0', ' ')
    s = re.sub(r'\s+', ' ', s)
    return s.strip().lower()


def load_sources():
    src = []
    for name in ('_все_реплики.json', '_реплики_о_сайте.json'):
        p = os.path.join(DLG, name)
        if not os.path.isfile(p):
            print('  ⚠ нет источника: %s' % p)
            continue
        d = json.loads(io.open(p, encoding='utf-8').read())
        for x in d:
            src.append(x.get('text', ''))
    return norm(' \n '.join(src))


def main():
    src = load_sources()
    if not src:
        print('НЕТ ИСХОДНЫХ РЕПЛИК — проверять не с чем')
        return 1
    print('исходных реплик: суммарно %d символов' % len(src))
    print()

    files = sorted(glob.glob(os.path.join(HERE, 'otvet_*.md')))
    if not files:
        print('НЕТ ФАЙЛОВ КАНОНА')
        return 1

    total = ok = 0
    problems = []
    for f in files:
        text = io.open(f, encoding='utf-8', errors='ignore').read()
        quotes = [q for q in QUOTE.findall(text) if len(q.strip()) >= MIN_LEN]
        good, bad = 0, []
        for q in quotes:
            if norm(q) in src:
                good += 1
            else:
                bad.append(q)
        total += len(quotes)
        ok += good
        mark = '✅' if not bad else '⚠'
        print('%s %-34s цитат: %3d | подтверждено: %3d | не найдено: %d'
              % (mark, os.path.basename(f), len(quotes), good, len(bad)))
        for b in bad[:3]:
            problems.append((os.path.basename(f), b))

    print()
    print('ИТОГО: подтверждено %d из %d (%.0f%%)' % (ok, total, 100.0 * ok / max(1, total)))

    if problems:
        print()
        print('ЦИТАТЫ, КОТОРЫХ НЕТ В ИСХОДНИКАХ (первые):')
        for name, q in problems:
            print('  %s: «%s…»' % (name, q[:90].replace('\n', ' ')))
        print()
        print('Важно: часть таких цитат — пересказ агента, часть — из сводок')
        print('сжатия контекста. Их нельзя использовать как требование владельца.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
