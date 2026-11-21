# -*- coding: utf-8 -*-
"""Разовая правка 21.11.2026 (слово Кенана): в меню сайта — пункт «Перевод», ссылка на переводчик translate.ragimoff.org.
Пункт стоит между «Блог» и «Контакты», открывается в новой вкладке (это отдельный сервис, не страница сайта)."""
import io, os, sys
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def sub(p, a, b):
    t = io.open(p, encoding="utf-8").read()
    if b in t:
        print("уже есть:", p)
        return
    assert a in t, (p, a[:70])
    io.open(p, "w", encoding="utf-8", newline="\n").write(t.replace(a, b, 1))
    print("изменён:", p)


c = "assets/js/content.js"
sub(c, "blog: 'Блог', contact: 'Контакты',", "blog: 'Блог', tr: 'Перевод', contact: 'Контакты',")
sub(c, "blog: 'Bloq', contact: 'Əlaqə',", "blog: 'Bloq', tr: 'Tərcümə', contact: 'Əlaqə',")
sub(c, "blog: 'Blog', contact: 'Contact',", "blog: 'Blog', tr: 'Translation', contact: 'Contact',")
# главная страница строит то же меню в своём сценарии
s = "assets/js/site.js"
sub(s, "{ k: 'blog', href: L.blogAll || 'blog.html', sub: [] }, { k: 'contact', href: L.contact, sub: [] },",
    "{ k: 'blog', href: L.blogAll || 'blog.html', sub: [] }, { k: 'tr', href: 'https://translate.ragimoff.org/', sub: [], ext: 1 }, { k: 'contact', href: L.contact, sub: [] },")
sub(s, '''`<div class="nav__i"><a class="nav__l" href="${g.href}">${esc(t.nav[g.k])}''',
    '''`<div class="nav__i"><a class="nav__l" href="${g.href}"${g.ext ? ' target="_blank" rel="noopener"' : ''}>${esc(t.nav[g.k])}''')
sub(s, '''<a class="mob__big" href="${g.href}">${esc(t.nav[g.k])}</a>''',
    '''<a class="mob__big" href="${g.href}"${g.ext ? ' target="_blank" rel="noopener"' : ''}>${esc(t.nav[g.k])}</a>''')
h = "assets/js/chrome.js"
sub(h, "{ k: 'blog', href: L.blogAll || 'blog.html', sub: [] }, { k: 'contact', href: L.contact, sub: [] },",
    "{ k: 'blog', href: L.blogAll || 'blog.html', sub: [] }, { k: 'tr', href: 'https://translate.ragimoff.org/', sub: [], ext: 1 }, { k: 'contact', href: L.contact, sub: [] },")
sub(h, '''`<div class="nav__i"><a class="nav__l" href="${g.href}">${esc(t.nav[g.k])}''',
    '''`<div class="nav__i"><a class="nav__l" href="${g.href}"${g.ext ? ' target="_blank" rel="noopener"' : ''}>${esc(t.nav[g.k])}''')
sub(h, '''<a class="mob__big" href="${g.href}">${esc(t.nav[g.k])}</a>''',
    '''<a class="mob__big" href="${g.href}"${g.ext ? ' target="_blank" rel="noopener"' : ''}>${esc(t.nav[g.k])}</a>''')
