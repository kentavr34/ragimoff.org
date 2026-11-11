"""ПРОВЕРКА ССЫЛОК В ФАЙЛАХ ТЕКСТА.

ЗАЧЕМ. При первой сборке страницы из content/ru.json оказалось 16 битых
ссылок из 27: адреса были взяты из прежней версии страницы и не проверены.
Битых ссылок на живом сайте быть не должно — каждая ведёт в пустоту и
работает против доверия, ради которого страница и делается.

ПРАВИЛО: после любой правки content/*.json запускать эту проверку ДО сборки.

Запуск:
    python _tools/check_links.py            # проверить все языки
    python _tools/check_links.py ru         # только русский

Выход: код 1, если есть битые ссылки, — чтобы это нельзя было
не заметить в цепочке команд.
"""
import json
import pathlib
import sys
import io

BASE = pathlib.Path(__file__).resolve().parents[1]
CONTENT = BASE / 'content'


def collect(node, path, out):
    """Собирает все href/src из файла текста вместе с местом, где он лежит."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k in ('href', 'src') and isinstance(v, str):
                out.append((path, v))
            elif k == 'cover' and isinstance(v, str):
                out.append((path, v))
            else:
                collect(v, '%s/%s' % (path, k) if path else k, out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            # в путь добавляем заголовок элемента — так понятно, где искать
            label = ''
            if isinstance(v, dict):
                label = v.get('title') or v.get('label') or v.get('name') or ''
            collect(v, ('%s[%s]' % (path, label)) if label else path, out)
    return out


def check_lang(lang):
    src = CONTENT / ('%s.json' % lang)
    if not src.is_file():
        print('  %s: файла текста нет — пропускаю' % lang)
        return 0, 0, []

    d = json.loads(io.open(src, encoding='utf-8').read())
    links = collect(d, '', [])

    ok, bad = 0, []
    for where, href in links:
        # внутренние якоря и внешние адреса проверке на файл не подлежат
        if not href or href.startswith('#') or href.startswith('http'):
            continue
        target = (BASE / href).resolve()
        if target.is_file() or target.is_dir():
            ok += 1
        else:
            # номер строки ищем в исходнике: так правку сделать быстрее
            line = ''
            try:
                for n, text in enumerate(io.open(src, encoding='utf-8').read().split('\n'), 1):
                    if href in text:
                        line = n
                        break
            except Exception:
                pass
            bad.append((where, href, line))
    return ok, len(links), bad


def main():
    langs = sys.argv[1:] or ['ru', 'az', 'en']
    print('ПРОВЕРКА ССЫЛОК В ФАЙЛАХ ТЕКСТА')
    total_bad = 0
    for lg in langs:
        ok, total, bad = check_lang(lg)
        if not total:
            continue
        mark = '✅' if not bad else '❌'
        print('  %s %-3s  рабочих %d из %d' % (mark, lg, ok, total))
        for where, href, line in bad:
            print('       ✗ строка %-4s %-44s → %s' % (line or '?', where.strip('/')[:44], href))
        total_bad += len(bad)

    if total_bad:
        print('\nОСТАНОВ: битых ссылок %d. Исправить или заменить на пометку «требуется страница».' % total_bad)
        return 1
    print('\nВсе ссылки рабочие.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
