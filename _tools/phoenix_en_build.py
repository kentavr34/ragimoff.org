# -*- coding: utf-8 -*-
"""_tools/phoenix_en_build.py — английская читалка «The Phoenix Era» из печатного DOCX (03.11.2026).

Почему отдельный скрипт: штатный конвейер docx-to-book.js → rebuild-concept.py → build_reader_books.py
пересобирает ВСЕ языки книги, а az/ru «Эры Феникса» уже собраны и проверены. Здесь конвейер гоняется во
временном корне (в сайт ничего не пишется), а в books/phoenix-era/en/ копируются только английские страницы.

Шаги: (1) docx-to-book.js по _tools/configs/phoenix-era.json (az, ru, en) во временном корне;
(2) rebuild-concept.py там же; (3) en/* → сайт; (4) head страниц глав: hreflang/og:url/ld на книгу, а не на
Klinik Psixiatriya (шаблон генератора); (5) build_reader_books.py phoenix-era en --stubs —
en/index.html становится читалкой, страницы глав — редиректами на неё.

    python _tools/phoenix_en_build.py            # вся цепочка
Требует: node, python + bs4. Не делает git-операций.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://ragimoff.org'
SLUG = 'phoenix-era'


def run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding='utf-8')
    if r.returncode:
        sys.exit('ОШИБКА %s\n%s\n%s' % (cmd, r.stdout[-2000:], r.stderr[-2000:]))
    return r.stdout


def fix_head(path, title_en, author_en):
    s = open(path, encoding='utf-8').read()
    idx = f'{BASE}/books/{SLUG}/'
    s = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*"\s*/?>\s*', '', s)
    alts = (f'<link rel="alternate" hreflang="az" href="{idx}">\n'
            f'<link rel="alternate" hreflang="ru" href="{idx}ru/">\n'
            f'<link rel="alternate" hreflang="en" href="{idx}en/">\n'
            f'<link rel="alternate" hreflang="x-default" href="{idx}">\n')
    s = re.sub(r'<link rel="canonical" href="[^"]*"\s*/?>', f'<link rel="canonical" href="{idx}en/">' + '\n' + alts.rstrip('\n'), s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*"', f'<meta property="og:url" content="{idx}en/"', s, count=1)
    s = s.replace('<meta property="og:locale" content="az_AZ">', '<meta property="og:locale" content="en_US">')
    s = re.sub(r'<meta name="keywords" content="[^"]*"',
               f'<meta name="keywords" content="{author_en}, {title_en}, relationship models, psychotherapy, Baku"', s, count=1)
    s = re.sub(r'"name":"Feniks Erası"', f'"name":"{title_en}"', s)
    s = re.sub(r'"author":\{"@type":"Person","name":"[^"]*"\}', f'"author":{{"@type":"Person","name":"{author_en}"}}', s)
    s = re.sub(r'"url":"https://ragimoff.org/klinik-psixiatriya/"', f'"url":"{idx}en/"', s)
    s = re.sub(r'"keywords":"[^"]*"\}</script>', f'"keywords":"psychotherapy, relationship models, {title_en}"}}</script>', s)
    open(path, 'w', encoding='utf-8', newline='').write(s)


def main():
    cfg = os.path.join(SITE, '_tools', 'configs', f'{SLUG}.json')
    tmp = tempfile.mkdtemp(prefix='phoenix_en_')
    try:
        os.makedirs(os.path.join(tmp, '_tools', 'configs'))
        os.makedirs(os.path.join(tmp, 'klinik-psixiatriya'))
        for f in ('docx-to-book.js', 'book-template.json', 'rebuild-concept.py'):
            shutil.copy(os.path.join(SITE, '_tools', f), os.path.join(tmp, '_tools', f))
        shutil.copy(cfg, os.path.join(tmp, '_tools', 'configs', f'{SLUG}.json'))
        shutil.copy(os.path.join(SITE, 'klinik-psixiatriya', 'style.css'), os.path.join(tmp, 'klinik-psixiatriya', 'style.css'))
        print(run(['node', '_tools/docx-to-book.js', f'_tools/configs/{SLUG}.json'], tmp).splitlines()[-1])
        print(run([sys.executable, '_tools/rebuild-concept.py', '--book', f'books/{SLUG}', '--quiet'], tmp).strip().splitlines()[0])
        src = os.path.join(tmp, 'books', SLUG, 'en')
        dst = os.path.join(SITE, 'books', SLUG, 'en')
        os.makedirs(dst, exist_ok=True)
        for f in os.listdir(src):
            shutil.copy(os.path.join(src, f), os.path.join(dst, f))
        n = 0
        for f in sorted(os.listdir(dst)):
            if f.endswith('.html') and f != 'index.html':
                fix_head(os.path.join(dst, f), 'The Phoenix Era', 'Samira Ragimova')
                n += 1
        print('en: страниц глав', n, '→', dst)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(run([sys.executable, '_tools/build_reader_books.py', SLUG, 'en', '--stubs'], SITE).strip())


if __name__ == '__main__':
    main()
