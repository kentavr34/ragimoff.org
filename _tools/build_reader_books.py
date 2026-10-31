"""Читалка для книг Кенана Рагимова (Кенан 31.10.2026: «та же читалка, что у Фрейда — стандарт раскрытия любой книги»).
Берёт готовые страницы книги books/<slug>/[<lang>/]NN-*.html (текст — блок .bk-read, заголовок — h1) и оглавление
index.html (группы → части), собирает ОДНУ страницу-читалку books/<slug>/[<lang>/]index.html на общем
books/reader/reader.css + reader.js: глава на экране, листание, A−/A+, тема день/ночь, оглавление, место чтения.
Старые страницы глав остаются и перенаправляют на index.html#chN (см. --stubs).
usage: python _tools/build_reader_books.py <slug> [lang ...] [--stubs]"""
import html
import json
import os
import re
import sys

from bs4 import BeautifulSoup

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
READER_V = '20261031b'
esc = html.escape

BOOKS = {
    'virus-viny': {'art': '/books/covers/guilt.jpg', 'price': 30, 'order': 'Günahkarlıq Virusu'},
    'shizofreniya': {'art': '/books/covers/pandemic.jpg', 'price': 30, 'order': 'Şizofreniya. Cinnət Pandemiyası'},
    'phoenix-era': {'art': '/books/covers/phoenix.jpg', 'price': 30, 'order': 'Feniks Erası', 'title': {'ru': 'Эра Феникса'}},
}
UI = {
    'az': dict(books='Kitablar', toc='Mündəricat', minus='Şrifti kiçilt', plus='Şrifti böyüt', theme='Gecə / gündüz', buy='Kitabı al',
               buy_t='Çap nüsxəsini səbətə at', close='Bağla', title_page='Titul səhifəsi', skip='Mətnə keç', author='Müəllif',
               first='İlk nəşr', chapters='Fəsillər', start='Fəsli mündəricatdan seçin və ya səhifəni sola sürüşdürün',
               prev='← Əvvəlki', next='Növbəti →', pager='Fəsillər arasında keçid', hint='Səhifəni sürüşdürün və ya ← → düymələrindən istifadə edin',
               cur='₼'),
    'ru': dict(books='Книги', toc='Оглавление', minus='Уменьшить шрифт', plus='Увеличить шрифт', theme='Ночь / день', buy='Купить',
               buy_t='Добавить печатную книгу в корзину', close='Закрыть', title_page='Титульная страница', skip='К тексту', author='Автор',
               first='Первое издание', chapters='Глав', start='Выберите главу в оглавлении или листайте влево',
               prev='← Назад', next='Далее →', pager='Переход между главами', hint='Листайте или используйте клавиши ← →', cur='₼'),
    'en': dict(books='Books', toc='Contents', minus='Smaller text', plus='Larger text', theme='Night / day', buy='Buy',
               buy_t='Add the printed book to cart', close='Close', title_page='Title page', skip='Skip to text', author='Author',
               first='First edition', chapters='Chapters', start='Pick a chapter from the contents or swipe left',
               prev='← Previous', next='Next →', pager='Chapter navigation', hint='Swipe or use the ← → keys', cur='₼'),
}
ICON = {
    'toc': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M4 6h16M4 12h16M4 18h10"/></svg>',
    'x': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>',
    'theme': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 0 0 16z" fill="currentColor"/></svg>',
    'cart': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2.5 3h2l2.2 12.2a1.6 1.6 0 0 0 1.6 1.3h9.4a1.6 1.6 0 0 0 1.6-1.3L21 7H6"/></svg>',
    'back': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M15 5l-7 7 7 7"/></svg>',
}

PAGE = '''<!doctype html>
<html lang="{lang}" data-theme="night"{alts}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} | {author}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://ragimoff.org{url}">
<meta property="og:type" content="book">
<meta property="og:title" content="{title} — {author}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://ragimoff.org{url}">
<meta property="og:image" content="https://ragimoff.org{art}">
<meta name="theme-color" content="#0B0E14">
<script>try{{var t=localStorage.getItem('rd-theme');document.documentElement.setAttribute('data-theme',t||(matchMedia('(prefers-color-scheme: light)').matches?'paper':'night'));var f=localStorage.getItem('rd-fs');if(f)document.documentElement.style.setProperty('--fs',f+'rem')}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;1,7..72,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/books/reader/reader.css?v={v}">
<script type="application/ld+json">{ld}</script>
</head>
<body data-book="{slug}-{lang}" data-title-label="{u[title_page]}">
<a class="rd-skip" href="#rd-main">{u[skip]}</a>
<header class="rd-bar">
  <a class="rd-back" href="{back}">{i_back}<span>{u[books]}</span></a>
  <button class="rd-ic" id="rd-toc-btn" type="button" aria-label="{u[toc]}" title="{u[toc]}">{i_toc}</button>
  <div class="rd-bar__title">{title}</div>
  <button class="rd-ic rd-ic--txt" id="rd-fs-minus" type="button" aria-label="{u[minus]}" title="{u[minus]}">A−</button>
  <button class="rd-ic rd-ic--txt" id="rd-fs-plus" type="button" aria-label="{u[plus]}" title="{u[plus]}">A+</button>
  <button class="rd-ic" id="rd-theme" type="button" aria-label="{u[theme]}" title="{u[theme]}">{i_theme}</button>
  <button class="rd-buy" id="rd-buy" type="button" data-order="{order}" data-price="{price} ₼" title="{u[buy_t]}">{i_cart}<span class="rd-buy__l">{u[buy]}</span><b>{price} ₼</b></button>
  <span class="rd-progress" aria-hidden="true"></span>
</header>
<aside class="rd-toc" aria-label="{u[toc]}">
  <div class="rd-toc__hd"><b>{u[toc]}</b><button class="rd-ic" id="rd-toc-close" type="button" aria-label="{u[close]}">{i_x}</button></div>
  <ol><li><a class="toc-row" href="#" data-go="0" data-i="0"><span class="toc-n">—</span><span>{u[title_page]}</span><span class="toc-p"></span></a></li>{toc}</ol>
</aside>
<div class="rd-scrim"></div>
<main class="rd" id="rd-main">
<section id="rd-title">
  <div class="rd-title">
    {cover}
    <div>
      <p class="rd-kicker">{author}</p>
      <h1 class="rd-h1">{title}</h1>
      {sub}
      <ul class="rd-meta">
        <li>{u[author]} <b>{author}</b></li>
        {year}
        <li>{u[chapters]} <b>{nch}</b></li>
      </ul>
      <p class="rd-start">{u[start]} <span aria-hidden="true">→</span></p>
    </div>
  </div>
  <nav class="rd-contents" aria-label="{u[toc]}">
    <h2>{u[toc]}</h2>
    <ol>{toc}</ol>
  </nav>
</section>
{chapters}
<nav class="rd-pager" aria-label="{u[pager]}" hidden>
  <button id="rd-prev" type="button"><small>{u[prev]}</small><span></span></button>
  <span class="pos" id="rd-pos"></span>
  <button id="rd-next" class="nx" type="button"><small>{u[next]}</small><span></span></button>
</nav>
<p class="rd-hint" hidden>{u[hint]}</p>
<footer class="rd-foot">© 2026 <a href="/">Ragimoff</a> · {author} · {title}</footer>
</main>
<script src="/books/reader/reader.js?v={v}" defer></script>
</body>
</html>
'''


def cover_html(art, author, title, foot):
    return (f'<div class="bk-cover-wrap"><div class="bk-cover" style="--art:url(\'{art}\')" role="img" aria-label="{esc(author)} — {esc(title)}">'
            f'<div class="bk-cover__in"><span class="bk-cover__a">{esc(author)}</span><span class="bk-cover__rule"></span>'
            f'<span class="bk-cover__t">{esc(title)}</span><span class="bk-cover__n">{esc(foot)}</span></div></div></div>')


def txt(el):
    return re.sub(r'\s+', ' ', el.get_text(' ')).strip() if el else ''


def build(slug, lang, stubs=False):
    cfg, u = BOOKS[slug], UI[lang]
    d = os.path.join(SITE, 'books', slug, '' if lang == 'az' else lang)
    idx = BeautifulSoup(open(os.path.join(d, 'index.html'), encoding='utf-8').read(), 'html.parser')
    if idx.select_one('.rd-bar'):
        sys.exit(f'{d}/index.html уже читалка — исходное оглавление в git: git show HEAD~:books/{slug}/...')
    title = txt(idx.select_one('.bk-tp__title')) or txt(idx.find('h1'))
    if title == title.lower():  # в RU-оглавлении название набрано строчными (регистр делал CSS)
        title = re.sub(r'(^|\.\s+)(\w)', lambda m: m.group(1) + m.group(2).upper(), title)
    title = cfg.get('title', {}).get(lang, title)
    sub = txt(idx.select_one('.bk-tp__sub'))
    author = txt(idx.select_one('.bk-tp__author')) or 'Kənan Rəhimov'
    year = txt(idx.select_one('.bk-tp__year'))
    # оглавление: строки-ссылки = главы (по файлу, без повторов), группы и ссылки без номера = части
    rows, files, seen = [], [], set()
    for li in idx.select('.bk-toc__list > li, .bk-toc__list li'):
        a = li.select_one('a.bk-toc__a')
        n = txt(li.select_one('.bk-toc__n'))
        t = txt(li.select_one('.bk-toc__t')) or txt(li.select_one('.bk-toc__g')) or txt(li)
        if a is None:
            rows.append(('part', t))
            continue
        if not n:  # ссылка без номера: «II HİSSƏ» — часть; «Modeldən çıxış…» (Феникс) — подраздел той же главы
            if re.search(r'\b(HİSSƏ|Hissə|hissə|ЧАСТЬ|Часть|PART|Part)\b', t):
                rows.append(('part', t))
            continue
        f = a['href'].split('#')[0]
        if f in seen or not os.path.exists(os.path.join(d, f)):
            continue
        seen.add(f)
        files.append(f)
        rows.append(('ch', t, f))
    # главы, пропущенные в оглавлении (Феникс 13), — на место по номеру файла, сразу после предыдущей главы
    for f in sorted(x for x in os.listdir(d) if re.match(r'\d\d-.*\.html$', x) and x not in seen):
        h = txt(BeautifulSoup(open(os.path.join(d, f), encoding='utf-8').read(), 'html.parser').select_one('.bk-chead__h1')) or f
        prev = [i for i, r in enumerate(rows) if r[0] == 'ch' and r[2] < f]
        at = prev[-1] + 1 if prev else 0
        rows.insert(at, ('ch', h, f))
        seen.add(f)
        print('  добавлена глава вне оглавления:', f)
    # часть без глав (в RU «Эры Феникса» разделов 1–5 нет на сайте) — не показывать пустой заголовок
    rows = [r for i, r in enumerate(rows) if r[0] == 'ch' or (i + 1 < len(rows) and rows[i + 1][0] == 'ch')]
    files = [r[2] for r in rows if r[0] == 'ch']
    chapters, toc, k, pend = [], [], 0, None
    N = len(files)
    for r in rows:
        if r[0] == 'part':
            pend = r[1]
            toc.append(f'<li class="toc-part">{esc(r[1])}</li>')
            continue
        k += 1
        page = BeautifulSoup(open(os.path.join(d, r[2]), encoding='utf-8').read(), 'html.parser')
        body = page.select_one('.bk-read')
        h1 = txt(page.select_one('.bk-chead__h1')) or r[1]
        for h in body.find_all('h1'):
            h.name = 'h3'
        for h in body.find_all('h2'):
            h.name = 'h3'
        for a in body.find_all('a', href=True):  # ссылки на соседние главы → якоря читалки
            f = a['href'].split('#')[0]
            if f in files:
                a['href'] = f'#ch{files.index(f) + 1}'
                a['data-go'] = str(files.index(f) + 1)
        part = f'<p class="rd-chap__part">{esc(pend)}</p>' if pend else ''
        pend = None
        chapters.append(f'<article class="rd-chap" id="ch{k}" data-title="{esc(h1)}" aria-label="{esc(h1)}">{part}'
                        f'<p class="rd-chap__n">{k} / {N}</p><h2>{esc(h1)}</h2><span class="rd-orn" aria-hidden="true"></span>'
                        f'{body.decode_contents().strip()}</article>')
        toc.append(f'<li><a class="toc-row" href="#ch{k}" data-go="{k}" data-i="{k}"><span class="toc-n">{k:02d}</span>'
                   f'<span class="toc-t">{esc(r[1])}</span><span class="toc-dots" aria-hidden="true"></span><span class="toc-p"></span></a></li>')
        if stubs:
            stub(os.path.join(d, r[2]), k, h1)
    url = f'/books/{slug}/' + ('' if lang == 'az' else f'{lang}/')
    alts = ''.join(f' data-lang-url-{L}="/books/{slug}/{"" if L == "az" else L + "/"}"' for L in UI)
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'Book', 'name': title, 'author': {'@type': 'Person', 'name': author},
                     'inLanguage': lang, 'bookFormat': 'EBook', 'publisher': 'Ragimoff', 'url': f'https://ragimoff.org{url}'}, ensure_ascii=False)
    yr = re.search(r'\d{4}', year)
    out = PAGE.format(
        lang=lang, alts=alts, title=esc(title), author=esc(author), desc=esc(f'{title} — {author}. {sub}'.strip()), url=url, art=cfg['art'],
        v=READER_V, ld=ld, slug=slug, u=u, back='/books/' + ('' if lang == 'az' else f'{lang}/'), i_back=ICON['back'], i_toc=ICON['toc'],
        i_theme=ICON['theme'], i_cart=ICON['cart'], i_x=ICON['x'], order=esc(cfg['order'] if lang == 'az' else title), price=cfg['price'], toc=''.join(toc),
        cover=cover_html(cfg['art'], author, title, yr.group() if yr else ''),
        sub=f'<p class="rd-sub">{esc(sub)}</p>' if sub else '',
        year=f'<li>{u["first"]} <b>{yr.group()}</b></li>' if yr else '', nch=N, chapters='\n'.join(chapters))
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='\n').write(out)
    print(slug, lang, 'chapters', N, 'parts', sum(1 for r in rows if r[0] == 'part'), len(out) // 1024, 'KB')


def stub(path, k, title):
    """Старая страница главы → тот же текст в читалке (ссылки из поиска и закладки не ломаются)."""
    s = open(path, encoding='utf-8').read()
    if 'data-rd-redirect' in s:
        return
    tag = (f'<meta http-equiv="refresh" content="0; url=index.html#ch{k}" data-rd-redirect>'
           f'<script>location.replace("index.html#ch{k}")</script>')
    s = s.replace('<head>', '<head>' + tag, 1)
    s = re.sub(r'<link rel="canonical"[^>]*>', '', s)
    open(path, 'w', encoding='utf-8', newline='\n').write(s)


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    for lang in (args[1:] or ['az']):
        build(args[0], lang, stubs='--stubs' in sys.argv)
