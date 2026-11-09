"""Ноктюрн → основной адрес ragimoff.org (Кенан 09.11.2026: «поехали»).

Порядок работы сайта после перехода:
  1) python _tools/nocturne/build.py      — сборка в test/nocturne (предпросмотр); исходники старых страниц — _legacy/
  2) python _tools/nocturne/verify.py     — сверка с исходниками (0 замечаний)
  3) python _tools/nocturne/publish_live.py — публикация в корень:
     · страницы az/ ru/ en/, картинки images/, стили и скрипты assets/, манифест, офлайн-страница, корневой выбор языка;
     · пути '/test/nocturne/' → '/', индексация открыта (robots index,follow), canonical и hreflang на каждой странице;
     · старые адреса (tehsil.html, ru/haqqimda.html, blog-*.html…) → перенаправления на новые страницы (SITEMAP.md);
     · sitemap.xml (новые страницы + все открытые страницы книг и «Клинической психиатрии»), robots.txt.
Резервная копия старого сайта: тег live-backup-2026-11-09, ветка archive/live-2026-11-09, D:/Projects/Ragimoff/_backups/.
"""
import os, re, shutil, pathlib, html as H, datetime

SITE = pathlib.Path(__file__).resolve().parents[2]
STAGE = SITE / 'test' / 'nocturne'
BASE = 'https://ragimoff.org'
LANGS = ['az', 'ru', 'en']
HREFLANG = {'az': 'az', 'ru': 'ru', 'en': 'en'}
stats = {'pages': 0, 'images': 0, 'assets': 0, 'redirects': 0}


def same(a, b):
    return b.is_file() and a.stat().st_size == b.stat().st_size and a.read_bytes() == b.read_bytes()


def copy_tree(src, dst, key):
    for p in src.rglob('*'):
        if p.is_file():
            q = dst / p.relative_to(src)
            if not same(p, q):
                q.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, q)
                stats[key] += 1


def is_redirect(text):
    return 'http-equiv="refresh"' in text[:2000]


def live_head(text, rel_path):
    """Индексация открыта; canonical и hreflang (если такая же страница есть на других языках)."""
    text = text.replace('/test/nocturne/', '/')
    text = text.replace('<meta name="robots" content="noindex,nofollow">', '<meta name="robots" content="index,follow,max-image-preview:large">')
    if 'rel="canonical"' not in text:
        lang, tail = rel_path.split('/', 1)
        links = ['<link rel="canonical" href="%s/%s">' % (BASE, rel_path)]
        for l2 in LANGS:
            if (STAGE / l2 / tail).is_file() and not is_redirect((STAGE / l2 / tail).read_text(encoding='utf-8', errors='ignore')):
                links.append('<link rel="alternate" hreflang="%s" href="%s/%s/%s">' % (HREFLANG[l2], BASE, l2, tail))
        if (STAGE / 'az' / tail).is_file():
            links.append('<link rel="alternate" hreflang="x-default" href="%s/az/%s">' % (BASE, tail))
        text = text.replace('</title>', '</title>\n' + '\n'.join(links), 1)
    return text


def redirect_html(lang, target_url):
    return ('<!DOCTYPE html><html lang="%s"><head><meta charset="utf-8"><title>RAGIMOFF</title>'
            '<meta name="robots" content="noindex,follow"><link rel="canonical" href="%s">'
            '<meta http-equiv="refresh" content="0; url=%s"><script>location.replace(%r + location.hash)</script></head>'
            '<body style="background:#07090E;color:#F2EDE3;font-family:Georgia,serif"><p><a style="color:#C9A961" href="%s">RAGIMOFF →</a></p></body></html>') % (
        lang, target_url, target_url, target_url, target_url)


def publish():
    # 1) страницы
    for l in LANGS:
        for p in (STAGE / l).rglob('*.html'):
            rel_path = p.relative_to(STAGE).as_posix()
            text = p.read_text(encoding='utf-8')
            text = text if is_redirect(text) else live_head(text, rel_path)
            q = SITE / rel_path
            q.parent.mkdir(parents=True, exist_ok=True)
            if not q.is_file() or q.read_text(encoding='utf-8', errors='ignore') != text:
                q.write_text(text, encoding='utf-8', newline='\n')
                stats['pages'] += 1
    # 2) картинки, стили, скрипты, шрифты
    copy_tree(STAGE / 'images', SITE / 'images', 'images')
    copy_tree(STAGE / 'assets', SITE / 'assets', 'assets')
    # 3) манифест приложения, офлайн-страница, выбор языка в корне
    for name in ('app.webmanifest', 'offline.html'):
        t = (STAGE / name).read_text(encoding='utf-8').replace('/test/nocturne/', '/')
        (SITE / name).write_text(t, encoding='utf-8', newline='\n')
    router = (STAGE / 'index.html').read_text(encoding='utf-8').replace('/test/nocturne/', '/')
    router = router.replace('<meta name="robots" content="noindex,nofollow">', '<meta name="robots" content="index,follow">')
    if 'rel="canonical"' not in router:
        router = router.replace('</title>', '</title>\n<link rel="canonical" href="%s/">\n<link rel="alternate" hreflang="x-default" href="%s/">' % (BASE, BASE), 1)
    (SITE / 'index.html').write_text(router, encoding='utf-8', newline='\n')
    # 4) старые адреса → новые страницы
    pairs = [l.split('  ←  ') for l in (SITE / '_tools' / 'nocturne' / 'SITEMAP.md').read_text(encoding='utf-8').splitlines() if '  ←  ' in l]
    new_paths = {p.relative_to(STAGE).as_posix() for l in LANGS for p in (STAGE / l).rglob('*.html')}
    for new, orig in pairs:
        orig = orig.strip()
        if not orig.endswith('.html') or orig in new_paths or orig == 'index.html':
            continue
        lang = orig.split('/', 1)[0] if orig.split('/', 1)[0] in ('ru', 'en') else 'az'
        (SITE / orig).write_text(redirect_html(lang, '%s/%s' % (BASE, new.strip())), encoding='utf-8', newline='\n')
        stats['redirects'] += 1
    # бывшие хабы «Обучение» и «Консультации» (страниц больше нет) → блоки главной
    for pre, lang in (('', 'az'), ('ru/', 'ru'), ('en/', 'en')):
        for orig, anchor in (('tehsil.html', '#programs'), ('xidmetler.html', '#services')):
            if (SITE / (pre + orig)).is_file():
                (SITE / (pre + orig)).write_text(redirect_html(lang, '%s/%s/index.html%s' % (BASE, lang, anchor)), encoding='utf-8', newline=chr(10))
                stats['redirects'] += 1
    # 5) карта сайта и robots.txt
    write_sitemap()
    write_robots()


def indexable(p):
    t = p.read_text(encoding='utf-8', errors='ignore')[:6000]
    return not is_redirect(t) and not re.search(r'name="robots" content="[^"]*noindex', t, re.I)


def write_sitemap():
    today = datetime.date.today().isoformat()
    urls = []
    for l in LANGS:
        for p in sorted((SITE / l).rglob('*.html')):
            rel_path = p.relative_to(SITE).as_posix()
            if indexable(p):
                tail = rel_path.split('/', 1)[1]
                alts = ''.join('<xhtml:link rel="alternate" hreflang="%s" href="%s/%s/%s"/>' % (l2, BASE, l2, tail)
                               for l2 in LANGS if (SITE / l2 / tail).is_file() and indexable(SITE / l2 / tail))
                pr = '1.0' if tail == 'index.html' else '0.8'
                urls.append('<url><loc>%s/%s</loc><lastmod>%s</lastmod><priority>%s</priority>%s</url>' % (BASE, rel_path, today, pr, alts))
    for root in ('books', 'klinik-psixiatriya'):
        for p in sorted((SITE / root).rglob('*.html')):
            if indexable(p):
                rel_path = p.relative_to(SITE).as_posix()
                loc = '%s/%s' % (BASE, rel_path[:-len('index.html')] if rel_path.endswith('/index.html') else rel_path)
                lm = datetime.date.fromtimestamp(p.stat().st_mtime).isoformat()
                urls.append('<url><loc>%s</loc><lastmod>%s</lastmod><priority>0.7</priority></url>' % (loc, lm))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n<url><loc>%s/</loc><lastmod>%s</lastmod><priority>1.0</priority></url>\n%s\n</urlset>\n') % (BASE, today, '\n'.join(urls))
    (SITE / 'sitemap.xml').write_text(xml, encoding='utf-8', newline='\n')
    stats['sitemap_urls'] = len(urls) + 1


def write_robots():
    (SITE / 'robots.txt').write_text('''# robots.txt — RAGIMOFF.org (новая версия сайта, 09.11.2026)
# Открыто всё содержимое: страницы на az/ru/en, книги и читалки на всех языках.
User-agent: *
Allow: /
Disallow: /_legacy/
Disallow: /test/
Disallow: /_tools/
Disallow: /_partials/
Disallow: /_print_az/
Disallow: /_table/
Disallow: /_supplements/
Disallow: /backend/
Disallow: /data/
Disallow: /payment/

Sitemap: https://ragimoff.org/sitemap.xml
''', encoding='utf-8', newline='\n')


if __name__ == '__main__':
    publish()
    print(stats)
