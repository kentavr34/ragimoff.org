#!/usr/bin/env python3
"""Сборка новой версии сайта «Ноктюрн» в test/nocturne/.

Источник текстов, цен, форм и их обработчиков — ТОЛЬКО страницы текущего сайта
(корень = AZ, ru/, en/). Ничего не сочиняется: содержимое каждой страницы
переносится как есть (секции <main>, модальные окна, скрипты форм), меняются
только адреса (новая структура папок) и оформление (шапка, первый экран,
подвал, слой стилей «Ноктюрн»).

Структура результата:
  test/nocturne/index.html          — выбор языка (сохранённый → часовой пояс → страна → язык ОС)
  test/nocturne/assets/css|js       — стили и скрипты
  test/nocturne/images/             — только используемые фото (копии из /images)
  test/nocturne/{az,ru,en}/...      — страницы по разделам

Запуск: python -I _tools/nocturne/build.py   (из папки site)
"""
import re, json, shutil, pathlib, html as H
from urllib.parse import urlsplit
from bs4 import BeautifulSoup, Comment

SITE = pathlib.Path(__file__).resolve().parents[2]
OUT = SITE / 'test' / 'nocturne'
LANGS = ['az', 'ru', 'en']
PREFIX = {'az': '', 'ru': 'ru/', 'en': 'en/'}
IMG_EXT = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif', '.svg', '.JPG', '.PNG')

MAP = {
    'index.html': 'index.html',
    'haqqimda.html': 'mutexessisler/kenan-rehimov.html',
    'samira.html': 'mutexessisler/samire-rehimova.html',
    'xidmetler.html': 'konsultasiya/index.html',
    'aile-terapiyasi.html': 'konsultasiya/aile-terapiyasi.html',
    'aile-terapiyasi-usaq.html': 'konsultasiya/aile-usaq-terapiyasi.html',
    'depressiya.html': 'konsultasiya/depressiya.html',
    'panik-ataklar.html': 'konsultasiya/panik-ataklar.html',
    'sosial-fobiya.html': 'konsultasiya/sosial-fobiya.html',
    'enurez.html': 'konsultasiya/enurez.html',
    'valideyn-mektebi.html': 'konsultasiya/valideyn-mektebi.html',
    'tehsil.html': 'telim/index.html',
    'program-umumi.html': 'telim/umumi-psixologiya.html',
    'program-klinik.html': 'telim/klinik-psixologiya.html',
    'program-praktikum.html': 'telim/psixoterapiya-praktikumu.html',
    'program-psixoanaliz.html': 'telim/psixoanaliz.html',
    'program-psixodiaqnostika.html': 'telim/psixodiaqnostika.html',
    'qanunlar.html': 'telim/qanuni-esaslar.html',
    'b2b.html': 'korporativ/index.html',
    'blog.html': 'bloq/index.html',
}
for lang in LANGS:
    for p in sorted((SITE / PREFIX[lang]).glob('blog-*.html')):
        MAP.setdefault(p.name, 'bloq/' + p.name[5:])

# Подписи, которых нет в меню оригинала (раздел «Специалисты» — слово Кенана 08.11.2026).
SPEC = {'az': 'Mütəxəssislər', 'ru': 'Специалисты', 'en': 'Specialists'}
NAMES = {  # из <title>/<h1> оригинальных страниц
    'haqqimda.html': {'az': 'Kənan Rəhimov', 'ru': 'Кенан Рагимов', 'en': 'Kenan Ragimov'},
    'samira.html': {'az': 'Samirə Rəhimova', 'ru': 'Самира Рагимова', 'en': 'Samira Rahimova'},
}
SKIP_LABEL = {'ru': {'program-psixodiaqnostika.html': 'Психодиагностика'}, 'en': {'program-psixodiaqnostika.html': 'Psychodiagnostics'}}
GROUPS = [
    ('spec', None, 'mutexessisler/index.html', ['haqqimda.html', 'samira.html']),
    ('cons', 'xidmetler.html', 'konsultasiya/index.html', ['aile-terapiyasi.html', 'aile-terapiyasi-usaq.html', 'valideyn-mektebi.html', 'depressiya.html', 'panik-ataklar.html', 'sosial-fobiya.html', 'enurez.html']),
    ('edu', 'tehsil.html', 'telim/index.html', ['program-umumi.html', 'program-klinik.html', 'program-praktikum.html', 'program-psixoanaliz.html', 'program-psixodiaqnostika.html', 'samira.html', 'qanunlar.html']),
    ('corp', 'b2b.html', 'korporativ/index.html', []),
    ('blog', 'blog.html', 'bloq/index.html', []),
]

HERO_IMG_DEFAULT = 'images/kenan/photo-portal-crop.jpg'
copied = set()
built = {l: set() for l in LANGS}
report = []


def soup_of(path):
    return BeautifulSoup(path.read_text(encoding='utf-8'), 'lxml')


def txt(el):
    return ' '.join(el.get_text(' ', strip=True).split()) if el else ''


def rel(from_new, to_new):
    """Относительный путь между двумя файлами внутри OUT (пути вида 'ru/telim/index.html')."""
    a = from_new.split('/')[:-1]
    b = to_new.split('/')
    i = 0
    while i < len(a) and i < len(b) - 1 and a[i] == b[i]:
        i += 1
    return '../' * (len(a) - i) + '/'.join(b[i:])


def root_rel(new_path):
    return '../' * new_path.count('/')


def copy_image(site_path):
    """site_path — путь от корня сайта (images/kenan/x.jpg) → копия в OUT/images/..."""
    sp = site_path.lstrip('/')
    src = SITE / sp
    if not src.is_file():
        return None
    dst_rel = 'images/' + (sp[7:] if sp.startswith('images/') else sp.replace('/', '_'))
    heavy = src.stat().st_size > 250_000 and src.suffix.lower() in ('.png', '.jpg', '.jpeg')
    if heavy:   # то же изображение в WebP: в 5–10 раз легче
        dst_rel = dst_rel.rsplit('.', 1)[0] + '.webp'
    if dst_rel not in copied:
        dst = OUT / dst_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.is_file() and dst.stat().st_mtime >= src.stat().st_mtime:
            copied.add(dst_rel)
            return dst_rel
        if heavy:
            from PIL import Image
            im = Image.open(src)
            im.thumbnail((2400, 2400))
            im.save(dst, 'WEBP', quality=84, method=6)
        else:
            shutil.copy2(src, dst)
        copied.add(dst_rel)
    return dst_rel


GEN_DIR = SITE.parent / '_assets' / 'nocturne_hero'   # картины первых экранов (DashScope wan2.5, gen_hero.py); вне репозитория


def gen_hero(slug):
    """Картина первого экрана для страницы-источника slug → OUT/images/hero-n/<slug>{,-m}.webp (или None)."""
    src = GEN_DIR / (slug + '.png')
    if not src.is_file():
        return None
    out = {}
    for suf, w in (('', 2000), ('-m', 900)):
        dst_rel = 'images/hero-n/%s%s.webp' % (slug, suf)
        dst = OUT / dst_rel
        if not (dst.is_file() and dst.stat().st_mtime >= src.stat().st_mtime):
            from PIL import Image
            dst.parent.mkdir(parents=True, exist_ok=True)
            im = Image.open(src).convert('RGB')
            if im.width > w:
                im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
            im.save(dst, 'WEBP', quality=82, method=6)
        copied.add(dst_rel)
        out[suf or 'full'] = dst_rel
    return out


VID_DIR = SITE.parent / '_assets' / 'nocturne_video'   # первый экран главной; вне репозитория
CINE_FRAMES = VID_DIR / 'jobus_frames'   # кадры видео JobTop (prep_jobus_frames.py): d/ десктоп 1600×900, m/ телефон 1000×1000


def cine_assets():
    """Кадры первого экрана → OUT/images/hero-home/{d,m}/fNNN.webp (готовые WebP копируются как есть)."""
    n = 0
    for sub in ('d', 'm'):
        src_dir = CINE_FRAMES / sub
        files = sorted(src_dir.glob('f*.webp')) if src_dir.is_dir() else []
        for fp in files:
            rel_ = 'images/hero-home/%s/%s' % (sub, fp.name)
            dst = OUT / rel_
            if not (dst.is_file() and dst.stat().st_mtime >= fp.stat().st_mtime):
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(fp, dst)
            copied.add(rel_)
        n = len(files)
    return n


QUERY = 'Doctor Ragimoff'


def cine_hero(d, lang, new_page):
    """Первый экран главной: кадры видео по прокрутке (вперёд/назад, плавно), касание → строка поиска,
    в ней набирается имя, из неё «пишется» заголовок: рукописное «Doctor Ragimoff» + строгое «Psixologiya Məktəbi»."""
    n = cine_assets()
    w1, w2 = d.get('w1', ''), d.get('w2', '')
    hand = (w1 if w2 else '').strip('«»"“” ') or QUERY
    strong = w2 or w1
    cl = d.get('ctas') or [(rel(new_page, lang + '/' + MAP[k]), LABELS[lang].get(k), False) for k in ('xidmetler.html', 'tehsil.html') if LABELS[lang].get(k)]
    ctas = ''.join('<a class="n-btn%s" href="%s">%s</a>' % ('' if i == 0 else ' n-btn-ghost', H.escape(h), H.escape(t))
                   for i, (h, t, _) in enumerate(cl))
    f0 = rel(new_page, 'images/hero-home/d/f000.webp')
    letters = ''.join('<span style="--i:%d">%s</span>' % (i, H.escape(ch) if ch != ' ' else '&nbsp;') for i, ch in enumerate(strong))
    font = rel(new_page, 'assets/fonts/marggraff-kursiv.woff')
    return '''<style>@font-face{font-family:"Marggraff Kursiv";src:url("%s") format("woff");font-display:swap}</style>
<section class="n-cine n-cine-v" id="main-content" data-cine>
<div class="n-cine-stick">
<div class="n-cine-frame" data-frames="%d" data-fsrc="%s" data-msrc="%s">
<img class="n-cine-img" src="%s" alt="" fetchpriority="high"><canvas class="n-cine-cv" aria-hidden="true"></canvas>
<div class="n-cine-search" aria-hidden="true"><svg viewBox="0 0 24 24" width="22" height="22"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M15.5 15.5 21 21" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg><span class="n-cine-q" data-q="%s"></span><i class="n-cine-caret"></i></div>
</div>
<div class="n-cine-shade" aria-hidden="true"></div>
<div class="n-wrap n-cine-beat n-cine-b1">
<span class="n-eyebrow">%s</span>
<h1 class="n-cine-h1"><span class="n-cine-hand">%s</span><span class="n-cine-strong" aria-label="%s">%s</span></h1>
<div class="n-ctas">%s</div>
</div>
<div class="n-cine-cue" aria-hidden="true"><i></i></div>
<div class="n-cine-out" aria-hidden="true"></div>
</div></section>''' % (H.escape(font), n, H.escape(f0.replace('f000', 'f{i}')), H.escape(f0.replace('/d/f000', '/m/f{i}')), H.escape(f0),
                         H.escape(QUERY), H.escape(d.get('badge', '')), H.escape(hand), H.escape(strong), letters, ctas)


def home_about(frag):
    """«О специалисте» на главной: без второй копии портрета (он уже в блоке «Специалисты»), кнопка — под хронологией."""
    sec = frag.select_one('section.sec-2col')
    if sec is None:
        return
    sec['class'] = sec.get('class', []) + ['n-about-home']
    right = sec.select_one('.about-col-right')
    if right is not None:
        btn = right.select_one('a.about-img-btn')
        content = sec.select_one('.about-content')
        if btn is not None and content is not None:
            btn['class'] = ['n-btn', 'n-btn-ghost', 'n-about-more']
            wrap = frag.new_tag('div', attrs={'class': 'n-about-more-row'})
            wrap.append(btn.extract())
            content.append(wrap)
        right.decompose()


def resolve(orig_page, url):
    """Адрес из оригинальной страницы → путь от корня сайта (без ведущего /)."""
    u = url.strip()
    if u.startswith('https://ragimoff.org') or u.startswith('http://ragimoff.org'):
        u = u.split('ragimoff.org', 1)[1] or '/'
    parts = urlsplit(u)
    path = parts.path
    if path.startswith('/'):
        full = path.lstrip('/')
    else:
        base = orig_page.rsplit('/', 1)[0] + '/' if '/' in orig_page else ''
        segs = (base + path).split('/')
        out = []
        for s in segs:
            if s == '..':
                if out: out.pop()
            elif s and s != '.':
                out.append(s)
        full = '/'.join(out)
    return full, parts.query, parts.fragment


def map_url(orig_page, new_page, url):
    if not url or url.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'data:', 'whatsapp:')):
        return url
    if re.match(r'^https?://', url) and 'ragimoff.org' not in url:
        return url
    full, q, frag = resolve(orig_page, url)
    tail = ('?' + q if q else '') + ('#' + frag if frag else '')
    if full.endswith(IMG_EXT):
        d = copy_image(full)
        return (rel(new_page, d) if d else '/' + full) + tail
    lang = 'az'
    name = full
    if full.startswith('ru/'): lang, name = 'ru', full[3:]
    elif full.startswith('en/'): lang, name = 'en', full[3:]
    if name in ('', 'index.html') and lang:
        name = 'index.html'
    if name in MAP and '/' not in name:
        target = lang + '/' + MAP[name]
        return rel(new_page, target) + tail
    return '/' + full + tail          # всё прочее (книги, справочник, оплата) — на боевой сайт


def fix_attrs(node, orig_page, new_page):
    for el in node.find_all(True):
        for a in ('href', 'src', 'data-src', 'poster', 'action'):
            v = el.get(a)
            if v and a != 'action':
                el[a] = map_url(orig_page, new_page, v)
        if el.get('srcset'):
            el['srcset'] = ', '.join(map_url(orig_page, new_page, p.strip().split(' ')[0]) + (' ' + p.strip().split(' ', 1)[1] if ' ' in p.strip() else '') for p in el['srcset'].split(','))
        st = el.get('style')
        if st and 'url(' in st:
            el['style'] = re.sub(r"url\((['\"]?)([^'\")]+)\1\)", lambda m: "url('" + map_url(orig_page, new_page, m.group(2)) + "')", st)
        oc = el.get('onclick')
        if oc:
            el['onclick'] = re.sub(r"(['\"])([^'\"]+\.(?:jpe?g|png|webp|gif|avif|JPG|PNG))\1", lambda m: m.group(1) + map_url(orig_page, new_page, m.group(2)) + m.group(1), oc)
    for c in node.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()


def nav_labels(lang):
    s = soup_of(SITE / PREFIX[lang] / 'index.html')
    lab = {}
    for a in s.select('.desktop-nav a'):
        full, _, _ = resolve(PREFIX[lang] + 'index.html', a.get('href', ''))
        name = full[3:] if full[:3] in ('ru/', 'en/') else full
        t = txt(a)
        if t and name not in lab:
            lab[name] = t
    lab.update(SKIP_LABEL.get(lang, {}))
    # страницы, которых нет в меню оригинала: подпись = заголовок H1 самой страницы
    for name in MAP:
        if name not in lab and not name.startswith('blog-') and (SITE / PREFIX[lang] / name).is_file():
            h1 = soup_of(SITE / PREFIX[lang] / name).find('h1')
            if h1:
                lab[name] = txt(h1)
    for k, v in NAMES.items():
        lab['@' + k] = v[lang]
    return lab


LABELS = {l: nav_labels(l) for l in LANGS}
import sys as _sys; _sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import short_trainings as ST
import consult_form as CF
for l in LANGS:
    # подпись кнопки «Книги» и регистрации — из оригинального меню
    pass


def header_html(lang, new_page, key):
    L = LABELS[lang]
    r = lambda p: rel(new_page, lang + '/' + p)
    items = []
    for gid, hub, hubpath, kids in GROUPS:
        label = SPEC[lang] if gid == 'spec' else L.get(hub, hub)
        on = ' is-on' if key == gid else ''
        if kids:
            sub = []
            if gid == 'edu':
                sub.append('<a href="%s">%s</a>' % (r(ST.PAGE), H.escape(ST.T[lang]['nav'])))
            for k in kids:
                lbl = L['@' + k] if (gid == 'spec' and '@' + k in L) else L.get(k, k)
                href = FAM_PAGE if (gid == 'edu' and k == 'samira.html') else MAP[k]
                sub.append('<a href="%s">%s</a>' % (r(href), H.escape(lbl)))
            hub_lbl = (L.get(hub) if hub else SPEC[lang])
            items.append('<div class="n-dd%s"><a class="n-link" href="%s" aria-haspopup="true">%s<svg width="10" height="10" viewBox="0 0 10 10" aria-hidden="true"><path d="M2 3.5l3 3 3-3" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg></a><div class="n-dd-panel"><a class="n-dd-hub" href="%s">%s →</a>%s</div></div>' % (on, r(hubpath), H.escape(label), r(hubpath), H.escape(hub_lbl), ''.join(sub)))
        else:
            items.append('<a class="n-link%s" href="%s">%s</a>' % (on, r(hubpath), H.escape(label)))
    items.append('<a class="n-link n-books" href="/books/">%s ↗</a>' % H.escape(L.get('books/', 'Books')))
    langs = []
    for l2 in LANGS:
        tgt = new_page.split('/', 1)[1]
        target = l2 + '/' + tgt if tgt in built_all[l2] else l2 + '/index.html'
        langs.append('<a href="%s" hreflang="%s" lang="%s" class="n-lang%s" data-lang="%s">%s</a>' % (rel(new_page, target), l2, l2, ' is-on' if l2 == lang else '', l2, l2.upper()))
    reg = L.get('tehsil.html#registration') or {'az': 'QEYDİYYAT', 'ru': 'РЕГИСТРАЦИЯ', 'en': 'REGISTRATION'}[lang]
    home = r('index.html')
    mob = []
    for gid, hub, hubpath, kids in GROUPS:
        label = SPEC[lang] if gid == 'spec' else L.get(hub, hub)
        sub = ''.join('<a href="%s">%s</a>' % (r(MAP[k]), H.escape(L['@' + k] if (gid == 'spec' and '@' + k in L) else L.get(k, k))) for k in kids)
        mob.append('<div class="n-m-group"><a class="n-m-big" href="%s">%s</a>%s</div>' % (r(hubpath), H.escape(label), ('<div class="n-m-sub">' + sub + '</div>') if sub else ''))
    mob.append('<div class="n-m-group"><a class="n-m-big" href="/books/">%s ↗</a></div>' % H.escape(L.get('books/', 'Books')))
    return '''<a class="n-skip" href="#main">%s</a>
<header class="n-head" id="nHead"><div class="n-head-in">
<a class="n-logo" href="%s" aria-label="RAGIMOFF"><span class="n-logo-r" aria-hidden="true">R<i></i></span><span class="n-logo-w" aria-hidden="true">AGIMOFF</span></a>
<nav class="n-nav" aria-label="Menu">%s</nav>
<div class="n-head-r"><div class="n-langs">%s</div><a class="n-cta" href="%s">%s</a><button class="n-burger" type="button" aria-expanded="false" aria-controls="nMob" aria-label="Menu"><i></i><i></i></button></div>
</div></header>
<div class="n-mob" id="nMob" aria-hidden="true"><div class="n-mob-in">%s<div class="n-m-langs">%s</div></div></div>''' % (
        {'az': 'Məzmuna keç', 'ru': 'К основному содержимому', 'en': 'Skip to content'}[lang],
        home, ''.join(items), ''.join(langs), r(MAP['tehsil.html']) + '#registration', H.escape(reg), ''.join(mob), ''.join(langs))


def hero_parts(hero, orig_page, new_page):
    d = {}
    if hero is None:
        return d
    b = hero.select_one('.ph-badge, .badge')
    d['badge'] = txt(b)
    h1 = hero.find('h1')
    w1 = h1.select_one('[class*="h1-w1"]') if h1 else None
    w2 = h1.select_one('[class*="h1-w2"]') if h1 else None
    if w1 and w2:
        d['w1'], d['w2'] = txt(w1), txt(w2)
    else:
        d['w1'], d['w2'] = txt(h1), ''
    desk = hero.select('.ph-sub-desk')
    if desk:
        d['lead'] = ' '.join(txt(x) for x in desk)
    else:
        lp = hero.select_one('.hero-lead, .ph-sub')
        if lp:
            for m in lp.select('[class*="-mob"]'):
                m.decompose()
            d['lead'] = txt(lp)
    m = re.search(r"url\(['\"]?([^'\")]+)['\"]?\)", hero.get('style', ''))
    img = m.group(1) if m else None
    ph = hero.select_one('.photo-col img')
    if ph is not None and ph.get('src'):
        d['art'] = map_url(orig_page, new_page, ph['src'])
        d['art_alt'] = ph.get('alt', '')
    if not img and ph is None:
        ph2 = hero.select_one('img')
        img = ph2.get('src') if ph2 else None
    d['img'] = map_url(orig_page, new_page, img) if img else map_url('index.html', new_page, HERO_IMG_DEFAULT)
    ctas = []
    for a in hero.select('a.btn, a.btn-fill, a.btn-line, a.hero-btn, .hero-actions a'):
        t = txt(a)
        if t and a.get('href'):
            ctas.append((map_url(orig_page, new_page, a['href']), t, 'btn-fill' in ' '.join(a.get('class', []))))
    d['ctas'] = ctas[:2]
    return d


def hero_html(d, lang, home=False, crumbs=''):
    w1 = H.escape(d.get('w1', ''))
    w2 = H.escape(d.get('w2', ''))
    h1 = '<span class="n-h1-a">%s</span>%s' % (w1, (' <em class="n-h1-b">%s</em>' % w2) if w2 else '')
    ctas = ''.join('<a class="n-btn%s" href="%s">%s</a>' % ('' if i == 0 else ' n-btn-ghost', H.escape(h), H.escape(t)) for i, (h, t, _) in enumerate(d.get('ctas', [])))
    if home:
        letters1 = ''.join('<span style="--i:%d">%s</span>' % (i, H.escape(ch) if ch != ' ' else '&nbsp;') for i, ch in enumerate(d.get('w1', '')))
        return '''<section class="n-hero n-hero-home" id="main-content" data-spot>
<div class="n-halo" aria-hidden="true"></div>
<div class="n-wrap n-hh">
<span class="n-eyebrow n-rise">%s</span>
<h1 class="n-hh-title"><span class="n-hh-a" aria-label="%s">%s</span><em class="n-hh-b n-rise" style="--d:.9s">%s</em></h1>
<img class="n-hh-photo" src="%s" alt="%s" width="392" height="600">
<div class="n-hh-foot n-rise" style="--d:1.1s"><p class="n-lead">%s</p><div class="n-ctas">%s</div></div>
</div></section>''' % (H.escape(d.get('badge', '')), w1, letters1, w2, H.escape(d['photo']), H.escape(d.get('alt', '')), H.escape(d.get('lead', '')), ctas)
    art = d.get('art')
    bg = '' if art else '<div class="n-hero-bg" aria-hidden="true"><img src="%s" alt=""></div>' % H.escape(d.get('img', ''))
    if d.get('paint'):
        full, mob = d['paint']
        bg = ('<div class="n-hero-bg n-paint" aria-hidden="true" data-paint><img src="%s" srcset="%s 900w, %s 2000w" '
              'sizes="100vw" alt="" fetchpriority="high"></div>') % (H.escape(full), H.escape(mob), H.escape(full))
    fig = ('<figure class="n-hero-art n-rise" style="--d:.35s"><img src="%s" alt="%s"></figure>' % (H.escape(art), H.escape(d.get('art_alt', '')))) if art else ''
    return '''<section class="n-hero%s" id="main-content" data-spot>
%s
<div class="n-wrap n-hero-in"><div class="n-hero-text">%s
<span class="n-eyebrow n-rise">%s</span>
<h1 class="n-h1 n-rise" style="--d:.1s">%s</h1>
%s
%s
</div>%s</div></section>''' % ((' n-hero-has-art' if art else '') + (' n-hero-paint' if d.get('paint') else ''), bg, crumbs, H.escape(d.get('badge', '')), h1,
                       ('<p class="n-lead n-rise" style="--d:.2s">%s</p>' % H.escape(d['lead'])) if d.get('lead') else '',
                       ('<div class="n-ctas n-rise" style="--d:.3s">%s</div>' % ctas) if ctas else '', fig)


def footer_html(foot, lang, orig_page, new_page):
    inner = ''
    if foot is not None:
        fix_attrs(foot, orig_page, new_page)
        strip_styles(foot)
        inner = ''.join(str(c) for c in foot.contents)
    return '''<footer class="n-foot"><div class="n-wrap">
<a class="n-foot-mark" href="%s" aria-label="RAGIMOFF">RAGIMOFF</a>
<div class="n-foot-orig site-footer">%s</div>
</div></footer>''' % (rel(new_page, lang + '/index.html'), inner)


def page_shell(lang, new_page, title, desc, head_extra, body_cls, header, main, footer, after, scripts):
    R = root_rel(new_page)
    return '''<!DOCTYPE html>
<html lang="%s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#07090E">
<link rel="icon" href="/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400;1,500&amp;family=Alegreya:ital,wght@0,400;0,500;0,700;1,400;1,500&amp;family=Manrope:wght@400;500;600;700&amp;family=Oswald:wght@400;500;600&amp;family=Monsieur+La+Doulaise&amp;display=swap">
%s
<link rel="stylesheet" href="%sassets/css/nocturne.css">
</head>
<body class="n-body %s">
<svg class="n-grain" aria-hidden="true"><filter id="nGrain"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter><rect width="100%%" height="100%%" filter="url(#nGrain)"/></svg>
%s
<main id="main" class="page-main">
%s
</main>
%s
%s
%s
<script src="%sassets/js/nocturne.js"></script>
<script src="%sassets/js/motion-gate.js"></script>
</body>
</html>
''' % (lang, H.escape(title), H.escape(desc), head_extra, R, body_cls, header, main, footer, after, scripts, R, R)


def collect_scripts(nodes, orig_page, new_page):
    R = root_rel(new_page)
    out = []
    for s in nodes:
        src = s.get('src')
        if src:
            base = src.split('?')[0].split('/')[-1]
            if base == 'shared.js':
                out.append('<script src="%sassets/js/shared.js"></script>' % R)
            elif base == 'training-pay.js':
                out.append('<script src="%sassets/js/training-pay.js"></script>' % R)
            elif base.startswith('js-hero-fit'):
                continue
            else:
                full, q, _ = resolve(orig_page, src)
                out.append('<script src="/%s%s"></script>' % (full, '?' + q if q else ''))
        else:
            t = s.string or ''
            if s.get('type') == 'application/ld+json':
                continue
            out.append('<script>%s</script>' % t)
    return '\n'.join(out)


ICONS = {  # свои линейные иконки «с точкой» (концепт RAGIM), по теме направления
    'aile-terapiyasi.html': '<circle cx="16" cy="15" r="5"/><circle cx="32" cy="15" r="5"/><path d="M6 40c0-7 4-12 10-12s10 5 10 12"/><path d="M22 40c0-7 4-12 10-12s10 5 10 12"/><circle class="d" cx="24" cy="6" r="2.6"/>',
    'aile-usaq-terapiyasi.html': '<circle cx="18" cy="12" r="5"/><path d="M8 42c0-9 4-15 10-15s10 6 10 15"/><circle cx="34" cy="24" r="3.5"/><path d="M28 42c0-6 2.5-10 6-10s6 4 6 10"/><circle class="d" cx="40" cy="14" r="2.6"/>',
    'enurez.html': '<path d="M8 26c4-10 10-15 16-15s12 5 16 15"/><path d="M24 11V5M12 16l-4-4M36 16l4-4"/><path d="M4 34h40M10 41h28"/><circle class="d" cx="24" cy="26" r="3"/>',
    'panik-ataklar.html': '<path d="M4 26h8l4-10 6 20 6-26 5 16h11"/><circle class="d" cx="44" cy="26" r="2.6"/>',
    'depressiya.html': '<path d="M14 34a10 10 0 1 1 6-18 12 12 0 0 1 22 6 7 7 0 0 1-2 13H14"/><path d="M18 42h16"/><circle class="d" cx="10" cy="12" r="3"/>',
    'sosial-fobiya.html': '<path d="M9 13h24a4 4 0 0 1 4 4v11a4 4 0 0 1-4 4H20l-8 6v-6H9a4 4 0 0 1-4-4V17a4 4 0 0 1 4-4z"/><circle class="d" cx="40" cy="10" r="3"/>',
    'valideyn-mektebi.html': '<path d="M4 18l20-10 20 10-20 10z"/><path d="M12 22v10c3 3 7 5 12 5s9-2 12-5V22"/><circle class="d" cx="42" cy="32" r="3"/>',
}
ICON_SET = {
    'edu': '<path d="M4 18l20-10 20 10-20 10z"/><path d="M12 22v10c3 3 7 5 12 5s9-2 12-5V22"/><circle class="d" cx="42" cy="32" r="3"/>',
    'check': '<rect x="5" y="8" width="38" height="25" rx="3"/><path d="M12 16h18M12 23h10"/><path d="M30 33l-2 9 6-3 6 3-2-9"/><circle class="d" cx="34" cy="27" r="3"/>',
    'law': '<path d="M24 12c-5-4-12-5-19-4v30c7-1 14 0 19 4 5-4 12-5 19-4V8c-7-1-14 0-19 4z"/><path d="M24 12v30"/><circle class="d" cx="34" cy="19" r="2.6"/>',
    'spark': '<path d="M8 26c4-10 10-15 16-15s12 5 16 15"/><path d="M24 11V5M12 16l-4-4M36 16l4-4"/><path d="M4 34h40M10 41h28"/><circle class="d" cx="24" cy="26" r="3"/>',
}
GALLERY_SEL = '.diploma-gallery, .students-grid, .dip-grid, .dip-grid-2, .dip-grid-3, .d2, .gallery-1'


def strip_styles(node):
    """Снять встроенное оформление оригинала; оставить только «скрыто» (его включают скрипты форм)."""
    for el in node.find_all(True):
        st = el.get('style')
        if st is not None:
            if re.search(r'display\s*:\s*none', st):
                el['style'] = 'display:none'
            else:
                del el['style']
        for a in ('onmouseover', 'onmouseout', 'data-theme', 'data-a11y-level', 'bgcolor', 'width' if el.name in ('table', 'td', 'th') else '_'):
            if el.has_attr(a):
                del el[a]


def restyle(main, s):
    """Содержимое оригинала → разметка под компоненты «Ноктюрна». Текст не меняется."""
    for el in main.find_all(True):
        if any(c.endswith('-mob') for c in el.get('class', [])):
            el.decompose()          # мобильные дубли подзаголовков (тот же текст есть в -desk)
    strip_styles(main)
    # галереи: каждый кадр целиком, в своих пропорциях, просмотр крупно
    for g in main.select(GALLERY_SEL):
        imgs = g.find_all('img')
        if not imgs:
            continue
        new = s.new_tag('div', attrs={'class': 'n-gallery'})
        for i in imgs:
            b = s.new_tag('button', attrs={'type': 'button', 'class': 'n-shot', 'data-full': i.get('src', ''), 'aria-label': i.get('alt', '') or 'photo'})
            im = s.new_tag('img', attrs={'src': i.get('src', ''), 'alt': i.get('alt', ''), 'loading': 'lazy'})
            if i.get('width') and i.get('height'):
                im['width'], im['height'] = i['width'], i['height']
            b.append(im)
            if i.get('alt'):
                cap = s.new_tag('span', attrs={'class': 'n-shot-cap'})
                cap.string = i['alt']
                b.append(cap)
            new.append(b)
        g.replace_with(new)
    for band in main.select('.gallery-band'):
        band.unwrap()
    # статьи законов — раскрываются по нажатию (обработчик в nocturne.js)
    for h in main.select('.law-card-head'):
        if h.has_attr('onclick'):
            del h['onclick']
        h['role'] = 'button'; h['tabindex'] = '0'; h['aria-expanded'] = 'false'
    # обложки видео с YouTube
    for v in main.select('a.video-thumb'):
        m = re.search(r'(?:youtu\.be/|v=|embed/)([\w-]{11})', v.get('href', ''))
        if m and not v.find('img'):
            im = s.new_tag('img', attrs={'src': 'https://i.ytimg.com/vi/%s/hqdefault.jpg' % m.group(1), 'alt': '', 'loading': 'lazy'})
            v.insert(0, im)
    # списки «полезное чтение» (ссылка + обложка) → карточки статей
    for ul in main.find_all('ul'):
        lis = ul.find_all('li', recursive=False)
        if len(lis) >= 2 and all(li.find('a') and li.find('img') for li in lis):
            ul['class'] = ul.get('class', []) + ['n-reading']
    # иконки направлений консультаций
    for c in main.select('.xid-card'):
        a = c.find('a')
        name = (a.get('href', '') if a else '').split('/')[-1].split('#')[0]
        if name in ICONS:
            svg = BeautifulSoup('<svg class="n-ico" viewBox="0 0 48 48" aria-hidden="true">%s</svg>' % ICONS[name], 'html.parser')
            c.insert(0, svg)
    # иконки концепта в карточках программ, условий, статей законов
    for c in main.select('.price-card, .req-block, .law-card-head, .opp-card, .adv-card'):
        kind = 'edu' if 'price-card' in c.get('class', []) else ('check' if 'req-block' in c.get('class', []) else ('law' if 'law-card-head' in c.get('class', []) else 'spark'))
        svg = BeautifulSoup('<svg class="n-ico n-ico-sm" viewBox="0 0 48 48" aria-hidden="true">%s</svg>' % ICON_SET[kind], 'html.parser')
        c.insert(0, svg)
    # карточки программ с ценами → горизонтальная лента
    for par in {pc.parent for pc in main.select('.price-card')}:
        if len(par.find_all(class_='price-card', recursive=False)) >= 3:
            par['class'] = par.get('class', []) + ['n-strip']


# ═══ Канон цен Кенана 08.11.2026 (ЦНС #712) — применяется к Ноктюрну при сборке, боевой сайт не трогается ═══
SHORT_PAGES = {'program-psixoanaliz.html', 'program-psixodiaqnostika.html', 'samira.html', 'aile-terapiyasi.html', 'tehsil.html', 'aile-terapiyasi-usaq.html'}
SHORT_UNITS = ['price-card', 'info-card', 'stats-strip', 'mod-price', 'mod-meta', 'tile-lbl', 'form-radio-lbl', 'stat-item']
LONG_SIG = re.compile(r'\d[  ]\d00 AZN|[3-9][  ]?\d00 AZN/ay\b|1[  ]?\d{3} AZN')   # Практикум/ДПО (3 600, 4 200, 6 600…)
SHORT_SIG = re.compile(r'(?<!\d)(?<!\d )600 AZN')
REPL = [(re.compile(r'(?<!\d)(?<!\d )600 AZN'), '900 AZN'), (re.compile(r'(?<!\d)(?<!\d )500 AZN'), '800 AZN'), (re.compile(r'(?<!\d)(?<!\d )200 AZN'), '300 AZN')]
START_DATE = [re.compile(r'Təlimə başlama tarixi\s*—\s*'), re.compile(r'Начало тренинга\s*—\s*'), re.compile(r'The training starts on\s*')]
canon_log = []


def canon_prices(main, orig_name, lang, new_page):
    name = orig_name.rsplit('/', 1)[-1]
    if name in SHORT_PAGES:
        units = set()
        for el in main.find_all(class_=lambda c: c and any(u in c.split() if isinstance(c, str) else u in c for u in SHORT_UNITS)):
            units.add(el)
        for u in units:
            t = u.get_text(' ', strip=True)
            if not SHORT_SIG.search(t) and not (('mod-price' in u.get('class', [])) and '300 AZN' not in t):
                continue
            if LONG_SIG.search(t):
                continue
            for node in u.find_all(string=True):
                new = str(node)
                for rx, rep in REPL:
                    new = rx.sub(rep, new)
                if new != str(node):
                    canon_log.append((new_page, str(node).strip()[:70], new.strip()[:70]))
                    node.replace_with(new)
        for intro in main.select('.mod-intro'):
            for node in intro.find_all(string=True):
                new = str(node)
                for rx in START_DATE:
                    new = rx.sub('', new)
                if new != str(node):
                    canon_log.append((new_page, str(node).strip()[:70], new.strip()[:70]))
                    node.replace_with(new)
    # консультации (AZ, в манатах): один специалист — онлайн 100 / əyani 150; оба — онлайн 150 / əyani 200
    if lang == 'az':
        for row in main.select('.pricing-tbl-row'):
            title = row.get_text(' ', strip=True)
            both = 'Birgə' in title or 'hər iki' in title
            single = 'Fərdi Sessiya' in title or title.startswith('1 Sessiya')
            if not (both or single):
                continue
            for cell in row.select('.pricing-tbl-cell'):
                ct = cell.get_text(' ', strip=True)
                val = None
                if ct.lower().startswith('online') or ct.lower().startswith('onlayn'):
                    val = 150 if both else 100
                elif ct.startswith('Əyani'):
                    val = 200 if both else 150
                if val is None:
                    continue
                for node in cell.find_all(string=re.compile(r'\d+\s*AZN')):
                    new = re.sub(r'\d+\s*AZN', '%d AZN' % val, str(node))
                    if new != str(node):
                        canon_log.append((new_page, str(node).strip(), new.strip()))
                        node.replace_with(new)
        for node in main.find_all(string=re.compile('Kənan Rəhimovun tarifi ilə hesablanır')):
            new = re.sub(r'Hər iki mütəxəssisin birgə apardığı sessiyalar Kənan Rəhimovun tarifi ilə hesablanır\.?',
                         'Bir mütəxəssislə: onlayn 100 AZN, əyani 150 AZN; hər iki mütəxəssislə: onlayn 150 AZN, əyani 200 AZN (1 saat).', str(node))
            canon_log.append((new_page, str(node).strip()[:70], new.strip()[:70]))
            node.replace_with(new)


def person_hero(lang, orig_name, d, photo, new_page, crumbs):
    d = dict(d)
    name = NAMES[orig_name][lang].split(' ', 1)
    d['w1'], d['w2'] = name[0], name[1] if len(name) > 1 else ''
    d['art'] = map_url('index.html', new_page, photo)
    d['art_alt'] = NAMES[orig_name][lang]
    return hero_html(d, lang, crumbs=crumbs).replace('class="n-hero n-hero-has-art"', 'class="n-hero n-hero-has-art n-hero-person"', 1)


def specialists_block(lang, new_page, head=True):
    cards = []
    for orig, photo in (('haqqimda.html', 'images/kenan/photo-hero-suit.jpg'), ('samira.html', 'images/samira/samira-portret.jpg')):
        op = PREFIX[lang] + orig
        hero = soup_of(SITE / op).select_one('section.page-hero, section.page-hero-x')
        d = hero_parts(hero, op, new_page)
        cards.append('''<a class="n-person" href="%s"><img src="%s" alt="%s" loading="lazy"><span class="n-person-tint" aria-hidden="true"></span>
<span class="n-person-body"><span class="n-eyebrow">%s</span><span class="n-person-name">%s</span><span class="n-person-lead">%s</span></span></a>''' % (
            rel(new_page, lang + '/' + MAP[orig]), map_url('index.html', new_page, photo), H.escape(NAMES[orig][lang]), H.escape(d.get('badge', '')),
            H.escape(NAMES[orig][lang]), H.escape(d.get('lead') or (d.get('w1', '') + ' ' + d.get('w2', '')))))
    hd = ('<div class="n-sec-head"><div><span class="n-eyebrow">RAGIMOFF</span><h2 class="n-h2">%s</h2></div></div>' % H.escape(SPEC[lang])) if head else ''
    return '<section class="n-sec"><div class="n-wrap">%s<div class="n-people">%s</div></div></section>' % (hd, ''.join(cards))


def programs_block(lang, new_page):
    """Лента программ с ценами — секция «Учебные программы» страницы Обучение (тексты и цены оттуда)."""
    op = PREFIX[lang] + 'tehsil.html'
    t = soup_of(SITE / op)
    sec = t.select_one('section#programs')
    if sec is None:
        return ''
    fix_attrs(sec, op, new_page)
    restyle(sec, t)
    for a in sec.select('a[href^="#registration"]'):
        a['href'] = rel(new_page, lang + '/' + MAP['tehsil.html']) + '#registration'
    sec['class'] = sec.get('class', []) + ['n-home-programs']
    if sec.has_attr('id'):
        del sec['id']
    return str(sec)


def build_page(lang, orig_name, new_rel, key):
    orig_page = PREFIX[lang] + orig_name
    src = SITE / orig_page
    if not src.is_file():
        return False
    new_page = lang + '/' + new_rel
    s = soup_of(src)
    title = txt(s.title) or 'RAGIMOFF'
    md = s.find('meta', attrs={'name': 'description'})
    desc = md.get('content', '') if md else ''
    head_extra = []
    for js in s.find_all('script', type='application/ld+json'):
        head_extra.append(str(js))
    main = s.find('main')
    if main is None:
        # У части страниц (AZ главная) нет <main>: содержимое — всё между шапкой/меню и подвалом.
        main = s.new_tag('main')
        foot0 = s.body.find('footer', recursive=False)
        moving = []
        for ch in s.body.find_all(recursive=False):
            if ch is foot0:
                break
            if ch.name in ('header', 'script') or ch.get('id') == 'mobileNav' or 'skip-link' in ch.get('class', []) or 'mobile-nav' in ch.get('class', []):
                continue
            moving.append(ch)
        for ch in moving:
            main.append(ch.extract())
        if foot0 is not None:
            foot0.insert_before(main)
        else:
            s.body.append(main)
    hero = main.select_one('section.page-hero, section.page-hero-x')
    d = hero_parts(hero, orig_page, new_page)
    if orig_name == 'samira.html':      # тренинг — на своей странице (telim/aile-terapiyasi.html), здесь только о Самире
        for sec in main.find_all('section'):
            if sec.select_one('.mod-panel') and not sec.find_parent('section'):
                sec.decompose()
    g = gen_hero(orig_name.rsplit('/', 1)[-1][:-5])
    if g:   # новая картина вместо старой иллюстрации-«лампы»
        d['paint'] = (rel(new_page, g['full']), rel(new_page, g['-m']))
        d.pop('art', None)
    if hero is not None:
        hero.extract()
    if key == 'cons':     # запись на консультацию в одно касание (Кенан 09.11): вместо старой формы
        reg = main.select_one('section#registration')
        frag_cf = BeautifulSoup(CF.section_html(lang, LABELS[lang], orig_name.rsplit('/', 1)[-1]), 'html.parser')
        if reg is not None:
            reg.replace_with(frag_cf)
        else:             # страницы без формы записи — форма в конце содержимого
            main.append(frag_cf)
    for el in main.find_all(True):
        if el.get('data-theme'):
            pass
    fix_attrs(main, orig_page, new_page)
    restyle(main, s)
    canon_prices(main, orig_name, lang, new_page)
    content = ''.join(str(c) for c in main.contents)
    foot = s.find('footer')
    footer = footer_html(foot.extract() if foot else None, lang, orig_page, new_page)
    after, scripts = [], []
    started = False
    for ch in s.body.find_all(recursive=False):
        if ch.name in ('header', 'main', 'footer') or 'skip-link' in ch.get('class', []) or ch.get('id') == 'mobileNav' or 'mobile-nav' in ch.get('class', []):
            continue
        if ch.name == 'script':
            scripts.append(ch)
            continue
        fix_attrs(ch, orig_page, new_page)
        after.append(str(ch))
    home = (orig_name == 'index.html')
    crumbs = ''
    if not home:
        L = LABELS[lang]
        sec = {'spec': SPEC[lang], 'cons': L.get('xidmetler.html'), 'edu': L.get('tehsil.html'), 'corp': L.get('b2b.html'), 'blog': L.get('blog.html')}.get(key)
        hubp = {'spec': 'mutexessisler/index.html', 'cons': 'konsultasiya/index.html', 'edu': 'telim/index.html', 'corp': 'korporativ/index.html', 'blog': 'bloq/index.html'}.get(key)
        home_lbl = L.get('index.html', 'RAGIMOFF')
        crumbs = '<nav class="n-crumbs n-rise" aria-label="breadcrumbs"><a href="%s">%s</a>' % (rel(new_page, lang + '/index.html'), H.escape(home_lbl))
        if sec and hubp and lang + '/' + hubp != new_page:
            crumbs += '<span>/</span><a href="%s">%s</a>' % (rel(new_page, lang + '/' + hubp), H.escape(sec))
        crumbs += '</nav>'
    if home:
        d['photo'] = map_url('index.html', new_page, 'images/kenan/photo-portal-crop-removebg-preview.png')
        d['alt'] = NAMES['haqqimda.html'][lang]
        L = LABELS[lang]
        words = [L.get(k) for k in GROUPS[1][3] if L.get(k)]
        dot = '<i aria-hidden="true"></i>'
        belt = dot.join('<span>%s</span>' % H.escape(w) for w in words) + dot
        marquee = '<div class="n-marquee" aria-hidden="true"><div class="n-belt">%s%s</div></div>' % (belt, belt)
        # главная по прототипу B: имя и портрет → бегущая строка → цифры → специалисты → программы → остальное
        frag = BeautifulSoup(content, 'html.parser')
        stats = frag.select_one('.stats-strip')
        stats_html = str(stats.extract()) if stats else ''
        home_about(frag)
        main_html = cine_hero(d, lang, new_page) + marquee + stats_html + specialists_block(lang, new_page) + programs_block(lang, new_page) + str(frag)
    elif orig_name in ('haqqimda.html', 'samira.html'):
        photo = 'images/kenan/haqqimda-kenan.jpg' if orig_name == 'haqqimda.html' else 'images/samira/samira-portret.jpg'
        main_html = person_hero(lang, orig_name, d, photo, new_page, crumbs) + content
        if orig_name == 'samira.html':
            lbl = {'az': ('Təlim proqramı', 'Ətraflı'), 'ru': ('Программа тренинга', 'Подробнее'), 'en': ('Training programme', 'Details')}[lang]
            main_html += ('<section class="n-sec n-sec-alt"><div class="n-wrap"><div class="n-cta-box"><div><span class="n-eyebrow">%s</span>'
                          '<h2 class="n-h2">%s</h2><p class="n-lead">%s</p></div><a class="n-btn" href="%s">%s</a></div></div></section>') % (
                H.escape(lbl[0]), H.escape(LABELS[lang].get('samira.html', '')), H.escape(FAM_T[lang]['cta_l']),
                rel(new_page, lang + '/' + FAM_PAGE), H.escape(lbl[1]))
    else:
        main_html = hero_html(d, lang, crumbs=crumbs) + content
    page = page_shell(lang, new_page, title, desc, '\n'.join(head_extra), 'n-k-' + key + (' n-home' if home else ''),
                      header_html(lang, new_page, key), main_html, footer, '\n'.join(after),
                      collect_scripts(scripts, orig_page, new_page))
    dst = OUT / new_page
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(page, encoding='utf-8', newline='\n')
    report.append((new_page, orig_page))
    return True


def build_spec_index(lang):
    new_page = lang + '/mutexessisler/index.html'
    L = LABELS[lang]
    crumbs = '<nav class="n-crumbs n-rise" aria-label="breadcrumbs"><a href="%s">%s</a></nav>' % (rel(new_page, lang + '/index.html'), H.escape(L.get('index.html', 'RAGIMOFF')))
    hero = hero_html({'badge': 'RAGIMOFF', 'w1': SPEC[lang], 'w2': '', 'img': map_url('index.html', new_page, HERO_IMG_DEFAULT)}, lang, crumbs=crumbs)
    main_html = hero + specialists_block(lang, new_page, head=False)
    R = root_rel(new_page)
    scripts = '<script src="%sassets/js/shared.js"></script>' % R
    foot = soup_of(SITE / (PREFIX[lang] + 'index.html')).find('footer')
    page = page_shell(lang, new_page, SPEC[lang] + ' | RAGIMOFF', '', '', 'n-k-spec', header_html(lang, new_page, 'spec'), main_html,
                      footer_html(foot, lang, PREFIX[lang] + 'index.html', new_page), '', scripts)
    (OUT / new_page).parent.mkdir(parents=True, exist_ok=True)
    (OUT / new_page).write_text(page, encoding='utf-8', newline=chr(10))
    report.append((new_page, 'generated from haqqimda.html + samira.html heroes'))


def build_short(lang):
    """Краткосрочные тренинги (ЦНС #712) — страница целиком из short_trainings.py."""
    new_page = lang + '/' + ST.PAGE
    t = ST.T[lang]
    L = LABELS[lang]
    crumbs = '<nav class="n-crumbs n-rise" aria-label="breadcrumbs"><a href="%s">%s</a><span>/</span><a href="%s">%s</a></nav>' % (
        rel(new_page, lang + '/index.html'), H.escape(L.get('index.html', 'RAGIMOFF')), rel(new_page, lang + '/telim/index.html'), H.escape(L.get('tehsil.html', '')))
    d = {'badge': t['eyebrow'], 'w1': t['title'], 'w2': '', 'lead': t['lead']}
    g = gen_hero('tehsil')
    if g:
        d['paint'] = (rel(new_page, g['full']), rel(new_page, g['-m']))
    else:
        d['img'] = map_url('index.html', new_page, HERO_IMG_DEFAULT)
    main_html = ST.page_main(lang, new_page, rel, MAP, hero_html(d, lang, crumbs=crumbs))
    R = root_rel(new_page)
    scripts = '<script src="%sassets/js/shared.js"></script>' % R
    foot = soup_of(SITE / (PREFIX[lang] + 'index.html')).find('footer')
    page = page_shell(lang, new_page, t['title'] + ' | RAGIMOFF', t['lead'], '', 'n-k-edu', header_html(lang, new_page, 'edu'), main_html,
                      footer_html(foot, lang, PREFIX[lang] + 'index.html', new_page), '', scripts)
    (OUT / new_page).parent.mkdir(parents=True, exist_ok=True)
    (OUT / new_page).write_text(page, encoding='utf-8', newline=chr(10))
    report.append((new_page, 'generated: short_trainings.py'))


FAM_PAGE = 'telim/aile-terapiyasi.html'
FAM_T = {
    'az': {'lead_by': 'Təlimi aparır', 'more': 'Mütəxəssis haqqında', 'reg': 'Qeydiyyat', 'cta_t': 'Təlimə yazılın', 'cta_l': '3 ay təhsil + 6 ay qrupda superviziya. Ayda 300 AZN × 3 və ya birdəfəlik 800 AZN.'},
    'ru': {'lead_by': 'Ведёт тренинг', 'more': 'О специалисте', 'reg': 'Регистрация', 'cta_t': 'Запись на тренинг', 'cta_l': '3 месяца обучения + 6 месяцев супервизии в группе. 300 AZN в месяц × 3 или 800 AZN единовременно.'},
    'en': {'lead_by': 'Led by', 'more': 'About the specialist', 'reg': 'Register', 'cta_t': 'Sign up for the training', 'cta_l': '3 months of training + 6 months of group supervision. 300 AZN a month × 3 or 800 AZN at once.'},
}


def build_family(lang):
    """Тренинг «Семейная терапия» (Кенан 08.11): короткий блок «кто ведёт» + подробно о тренинге; без даты; новые цены."""
    orig_page = PREFIX[lang] + 'samira.html'
    src = SITE / orig_page
    if not src.is_file():
        return
    new_page = lang + '/' + FAM_PAGE
    s = soup_of(src)
    main = s.find('main')
    hero = main.select_one('section.page-hero, section.page-hero-x')
    d = hero_parts(hero, orig_page, new_page)
    d.pop('art', None)
    g = gen_hero('samira') or gen_hero('aile-terapiyasi')
    if g:
        d['paint'] = (rel(new_page, g['full']), rel(new_page, g['-m']))
    trains = [sec for sec in main.find_all('section') if sec.select_one('.mod-panel') and not sec.find_parent('section')]
    for sec in trains:
        fix_attrs(sec, orig_page, new_page)
    holder = s.new_tag('main')
    for sec in trains:
        holder.append(sec.extract())
    restyle(holder, s)
    canon_prices(holder, 'samira.html', lang, new_page)
    F = FAM_T[lang]
    spec_hero = soup_of(src).select_one('section.page-hero, section.page-hero-x')
    sd = hero_parts(spec_hero, orig_page, new_page)
    who = ('<section class="n-sec"><div class="n-wrap"><a class="n-who" href="%s"><img src="%s" alt="%s" loading="lazy">'
           '<span class="n-who-body"><span class="n-eyebrow">%s</span><span class="n-who-name">%s</span><span class="n-who-lead">%s</span>'
           '<span class="n-who-more">%s →</span></span></a></div></section>') % (
        rel(new_page, lang + '/' + MAP['samira.html']), map_url('index.html', new_page, 'images/samira/samira-portret.jpg'),
        H.escape(NAMES['samira.html'][lang]), H.escape(F['lead_by']), H.escape(NAMES['samira.html'][lang]), H.escape(sd.get('lead', '')), H.escape(F['more']))
    cta = ('<section class="n-sec n-sec-alt"><div class="n-wrap"><div class="n-cta-box"><div><span class="n-eyebrow">%s</span>'
           '<h2 class="n-h2">%s</h2><p class="n-lead">%s</p></div><a class="n-btn" href="%s">%s</a></div></div></section>') % (
        H.escape(F['reg']), H.escape(F['cta_t']), H.escape(F['cta_l']), rel(new_page, lang + '/' + ST.PAGE) + '#qeydiyyat', H.escape(F['reg']))
    L = LABELS[lang]
    crumbs = '<nav class="n-crumbs n-rise" aria-label="breadcrumbs"><a href="%s">%s</a><span>/</span><a href="%s">%s</a></nav>' % (
        rel(new_page, lang + '/index.html'), H.escape(L.get('index.html', 'RAGIMOFF')), rel(new_page, lang + '/telim/index.html'), H.escape(L.get('tehsil.html', '')))
    main_html = hero_html(d, lang, crumbs=crumbs) + who + ''.join(str(c) for c in holder.contents) + cta
    title = (d.get('w1', '') + ' ' + d.get('w2', '')).strip() or 'RAGIMOFF'
    R = root_rel(new_page)
    scripts = '<script src="%sassets/js/shared.js"></script>' % R
    foot = soup_of(SITE / (PREFIX[lang] + 'index.html')).find('footer')
    page = page_shell(lang, new_page, title + ' | RAGIMOFF', d.get('lead', ''), '', 'n-k-edu', header_html(lang, new_page, 'edu'), main_html,
                      footer_html(foot, lang, PREFIX[lang] + 'index.html', new_page), '', scripts)
    (OUT / new_page).parent.mkdir(parents=True, exist_ok=True)
    (OUT / new_page).write_text(page, encoding='utf-8', newline=chr(10))
    report.append((new_page, 'generated: samira.html training sections'))


def key_for(new_rel):
    top = new_rel.split('/')[0]
    return {'mutexessisler': 'spec', 'konsultasiya': 'cons', 'telim': 'edu', 'korporativ': 'corp', 'bloq': 'blog'}.get(top, 'home')


def main():
    global built_all
    if OUT.exists():
        for p in OUT.iterdir():
            if p.name in ('assets', 'images'):     # фото переиспользуются (кеш WebP); лишние чистит prune_images()
                continue
            shutil.rmtree(p) if p.is_dir() else p.unlink()
    OUT.mkdir(parents=True, exist_ok=True)
    built_all = {l: set() for l in LANGS}
    for l in LANGS:
        for o, n in MAP.items():
            if (SITE / PREFIX[l] / o).is_file():
                built_all[l].add(n)
        built_all[l].add('mutexessisler/index.html')
        built_all[l].add(ST.PAGE)
        built_all[l].add(FAM_PAGE)
    for l in LANGS:
        for o, n in MAP.items():
            build_page(l, o, n, key_for(n))
        build_spec_index(l)
        build_short(l)
        build_family(l)
    # общие скрипты/стили — точные копии с боевого сайта
    js = OUT / 'assets' / 'js'; css = OUT / 'assets' / 'css' / 'legacy'
    js.mkdir(parents=True, exist_ok=True); css.mkdir(parents=True, exist_ok=True)
    for f in ('shared.js', 'training-pay.js'):
        shutil.copy2(SITE / f, js / f)
    shutil.rmtree(css, ignore_errors=True)       # старые стили больше не нужны
    for extra in ('images/kenan/photo-portal-crop-removebg-preview.png', 'images/kenan/photo-hero-suit.jpg', 'images/kenan/haqqimda-kenan.jpg', 'images/samira/samira-portret.jpg', HERO_IMG_DEFAULT):
        copy_image(extra)
    write_router()
    write_sitemap()
    prune_images()
    print('pages', len(report), 'images', len(copied))
    (pathlib.Path(__file__).resolve().parent / 'canon_log.txt').write_text(chr(10).join('%s | %s  ->  %s' % x for x in canon_log), encoding='utf-8')


ROUTER = '''<!DOCTYPE html>
<html lang="az">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RAGIMOFF</title>
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#07090E">
<link rel="icon" href="/favicon.ico">
<link rel="alternate" hreflang="az" href="az/index.html">
<link rel="alternate" hreflang="ru" href="ru/index.html">
<link rel="alternate" hreflang="en" href="en/index.html">
<style>
body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;background:#07090E;color:#F2EDE3;font:400 15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
.box{text-align:center;padding:24px}
.mark{font:300 44px/1 Georgia,serif;letter-spacing:.18em;color:#F2EDE3}
.mark b{color:#C9A961;font-weight:300}
.row{margin-top:28px;display:flex;gap:10px;justify-content:center}
.row a{min-width:64px;height:44px;display:inline-flex;align-items:center;justify-content:center;border:1px solid rgba(201,169,97,.5);border-radius:99px;color:#F2EDE3;text-decoration:none;font-weight:600;letter-spacing:.08em}
.row a:hover{background:#C9A961;color:#07090E}
</style>
<script>
/* Выбор языка новой версии: 1) ?lang= 2) сохранённый выбор (клик переключателя)
   3) часовой пояс Asia/Baku → az 4) страна по IP (≤1,5 с) 5) язык системы. */
(function () {
  var L = ['az', 'ru', 'en'];
  function go(l) { try { localStorage.setItem('ragimoff_lang', l); } catch (e) {} location.replace(l + '/index.html' + location.hash); }
  var q = (location.search.match(/[?&]lang=(az|ru|en)/) || [])[1];
  if (q) return go(q);
  var saved = null; try { saved = localStorage.getItem('ragimoff_lang'); } catch (e) {}
  if (L.indexOf(saved) >= 0) return go(saved);
  var tz = ''; try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ''; } catch (e) {}
  if (tz === 'Asia/Baku') return go('az');
  var nav = ((navigator.languages && navigator.languages[0]) || navigator.language || '').toLowerCase().split('-')[0];
  function byNav() { return nav === 'az' || nav === 'tr' ? 'az' : (['ru', 'uk', 'be', 'kk', 'ky', 'uz', 'tg', 'hy', 'ka'].indexOf(nav) >= 0 ? 'ru' : 'en'); }
  var done = false;
  var t = setTimeout(function () { if (!done) { done = true; go(byNav()); } }, 1500);
  fetch('https://get.geojs.io/v1/ip/country.json').then(function (r) { return r.json(); }).then(function (d) {
    if (done) return; done = true; clearTimeout(t);
    var c = String((d && d.country) || '').toUpperCase();
    if (c === 'AZ') return go('az');
    if (['RU', 'BY', 'KZ', 'KG', 'UZ', 'TJ', 'AM', 'GE', 'MD', 'UA'].indexOf(c) >= 0) return go(nav === 'en' ? 'en' : 'ru');
    go(byNav());
  }).catch(function () { if (!done) { done = true; clearTimeout(t); go(byNav()); } });
})();
</script>
</head>
<body>
<div class="box">
<div class="mark">RAGIMOFF<b>.</b></div>
<div class="row"><a href="az/index.html" hreflang="az">AZ</a><a href="ru/index.html" hreflang="ru">RU</a><a href="en/index.html" hreflang="en">EN</a></div>
</div>
</body>
</html>
'''


def prune_images():
    """Удалить из images/ то, на что больше не ссылается ни одна страница."""
    for f in (OUT / 'images').rglob('*'):
        if f.is_file() and f.relative_to(OUT).as_posix() not in copied:
            f.unlink()


def write_router():
    (OUT / 'index.html').write_text(ROUTER, encoding='utf-8', newline='\n')


def write_sitemap():
    """Карта новой версии: каждая страница на трёх языках (для проверки полноты, не для поисковиков)."""
    rows = ['# Карта сайта «Ноктюрн» — новая страница ← страница-источник боевого сайта', '']
    for new, orig in sorted(report):
        rows.append('%s  ←  %s' % (new, orig))
    (SITE / '_tools' / 'nocturne' / 'SITEMAP.md').write_text('\n'.join(rows) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
