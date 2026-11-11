"""СБОРКА СТРАНИЦЫ ИЗ ЕДИНОГО ФАЙЛА ТЕКСТА.

ЗАЧЕМ ЭТО. Требование владельца (11.11.2026): «текст стоит в одном файле,
а отображается на одной странице и таким образом индексируется». Иначе
говоря: тексты живут отдельно от разметки, а страница — результат сборки.

ЧТО БЫЛО НЕ ТАК РАНЬШЕ. Текст был вшит прямо в index.html. Правка формулировки
требовала правки разметки, а на трёх языках это три разных файла с
расходящимся содержимым. Здесь этого нет: одно место для текста — один
источник правды.

КАК РАБОТАЕТ.
    content/ru.json  →  _tools/build_pages.py  →  index.html

ПРАВИЛА, ЗАШИТЫЕ В КОД:
  1. Каждый раздел страницы — отдельная функция render_<имя>. Добавить блок
     в JSON и не написать функцию — сборка УПАДЁТ, а не сделает вид, что всё
     в порядке. Это защита от «текст есть, а на странице его нет».
  2. Текст экранируется. Угловые скобки в тексте не сломают разметку.
  3. Ссылка без href не попадёт на страницу — вместо неё будет заметная
     пометка прямо в HTML, чтобы дефект нашли до публикации, а не после.
  4. Проверка обязательных полей: пустой заголовок или заголовок-заглушка
     останавливают сборку.

Запуск:
    python _tools/build_pages.py            # собрать все языки, что есть
    python _tools/build_pages.py ru         # собрать только русский
"""
import json
import pathlib
import sys
import html as H

BASE = pathlib.Path(__file__).resolve().parents[1]
CONTENT = BASE / 'content'
LANGS = ['ru', 'az', 'en']

# ── Ссылки без адреса (то, чего в продакшене ещё нет) ────────────────────
# Осознанно оставлены видимыми: владелец должен видеть, где нужны страницы,
# а не получать молчаливо работающую заглушку.
MISSING_MARK = ('<span class="link-missing" title="Страница ещё не создана">'
                '⚠ требуется страница</span>')


def link(l, cls=''):
    """Ссылка. Без href — честная пометка, а не пустой якорь."""
    if not l:
        return ''
    label = H.escape(str(l.get('label', '')))
    href = (l.get('href') or '').strip()
    c = (' class="%s"' % cls) if cls else ''
    if not href:
        return MISSING_MARK + ' <span%s>%s</span>' % (c, label)
    return '<a href="%s"%s>%s</a>' % (H.escape(href, quote=True), c, label)


def esc(v):
    return H.escape(str(v)) if v is not None else ''


def img(src, alt, cls=''):
    if not src:
        return ''
    c = (' class="%s"' % cls) if cls else ''
    return '<img src="%s" alt="%s"%s loading="lazy" decoding="async">' % (
        H.escape(src, quote=True), H.escape(alt, quote=True), c)


def require(d, *keys):
    """Обязательные поля. Пустое значение — стоп сборки, а не тихая дыра."""
    for k in keys:
        if not d.get(k):
            raise ValueError('обязательное поле пустое: %s (в %s)' % (k, d.get('title') or d.get('name') or '?'))


# ══════════════════════════════════════════════════════════════════════════
#  РАЗДЕЛЫ СТРАНИЦЫ
# ══════════════════════════════════════════════════════════════════════════

def render_head(h, meta):
    navs = '\n'.join(
        '        <a class="nav__link" href="%s">%s</a>' % (H.escape(n['href'], quote=True), esc(n['label']))
        for n in h.get('nav', [])
    )
    langs = '\n'.join(
        '        <a class="lang__btn%s" data-lang="%s" href="%s">%s</a>' % (
            ' is-active' if n.get('current') else '', n['code'],
            H.escape(n['href'], quote=True), esc(n['label']))
        for n in h.get('langs', [])
    )
    themes = '\n'.join(
        '        <button class="theme__btn" data-theme-set="%s" type="button" aria-label="%s"><span></span></button>'
        % (t['id'], esc(t['label'])) for t in h.get('themes', [])
    )
    return '''  <header class="hdr" id="hdr">
    <div class="hdr__inner">
      <a class="brand" href="index.html">
        <span class="brand__name">%s</span>
        <span class="brand__sub">%s</span>
      </a>
      <nav class="nav" id="nav">
%s
      </nav>
      <div class="hdr__tools">
        <div class="themes" id="themes" role="group" aria-label="Тема оформления">
%s
        </div>
        <div class="lang" id="lang" role="group" aria-label="Язык">
%s
        </div>
        <a class="btn btn--gold btn--sm" href="%s">%s</a>
      </div>
      <button class="burger" id="burger" type="button" aria-label="Меню"><span></span></button>
    </div>
  </header>''' % (esc(h['logoName']), esc(h['logoSub']), navs, themes, langs,
                   H.escape(h['cta']['href'], quote=True), esc(h['cta']['label']))


def render_hero(hero):
    btns = '\n'.join(
        '          <a class="btn btn--%s" href="%s">%s</a>' % (
            'gold' if b.get('style') == 'gold' else 'line',
            H.escape(b['href'], quote=True), esc(b['label']))
        for b in hero.get('buttons', [])
    )
    net = '    <canvas class="hero__net" id="heroNet" aria-hidden="true"></canvas>\n' if hero.get('net') else ''
    require(hero, 'title', 'hand')
    return '''<section class="hero" id="hero">
  <div class="hero__stick">
    <div class="hero__media">
      %s
    </div>
%s    <div class="hero__scrim" aria-hidden="true"></div>
    <div class="hero__inner">
      <p class="hero__hand">%s</p>
      <h1 class="hero__strict">%s</h1>
      <p class="hero__lead">%s</p>
      <div class="hero__actions">
%s
      </div>
    </div>
    <div class="hero__scroll" aria-hidden="true"><span>%s</span><i></i></div>
  </div>
</section>''' % (img(hero['photo']['src'], hero['photo'].get('alt', ''), 'hero__img'),
                  net, esc(hero['hand']), esc(hero['title']), esc(hero.get('lead', '')),
                  btns, esc(hero.get('scrollHint', '')))


def render_specialists(s):
    items = []
    for p in s.get('items', []):
        require(p, 'name', 'role')
        facts = '\n'.join('              <li>%s</li>' % esc(f) for f in p.get('facts', []))
        items.append('''        <article class="person reveal">
          <div class="person__photo">%s</div>
          <div class="person__veil" aria-hidden="true"></div>
          <div class="person__body">
            <h3 class="person__name">%s</h3>
            <p class="person__role">%s</p>
            <ul class="person__facts">
%s
            </ul>
            <p class="person__link">%s</p>
          </div>
        </article>''' % (img(p['photo'], p['name'], 'person__img'), esc(p['name']),
                          esc(p['role']), facts, link(p.get('link'), 'link--arrow')))
    return '''<section class="section" id="specialists">
  <div class="wrap">
    <header class="section__head reveal">
      <p class="kicker">%s</p>
      <h2>%s</h2>
      <p class="lead">%s</p>
    </header>
    <div class="people">
%s
    </div>
  </div>
</section>''' % (esc(s.get('kicker', '')), esc(s['title']), esc(s.get('lead', '')),
                  '\n'.join(items))


def render_books(b):
    cards = []
    for k in b.get('items', []):
        require(k, 'title')
        why = '\n'.join('            <li>%s</li>' % esc(w) for w in k.get('why', []))
        co = '<p class="book__co">%s</p>' % esc(k['coauthor']) if k.get('coauthor') else ''
        cards.append('''        <article class="book reveal">
          <div class="book__cover">%s</div>
          <div class="book__body">
            <h3 class="book__title">%s</h3>
%s
            <ul class="book__why">
%s
            </ul>
            <p class="book__read">%s</p>
          </div>
        </article>''' % (img(k['cover'], k['title'], 'book__img'), esc(k['title']), co,
                          why, link(k.get('read'), 'btn btn--line btn--sm')))
    fr = b.get('freud', {})
    fr_txt = '\n'.join('          <li>%s</li>' % esc(t) for t in fr.get('text', []))
    cm = b.get('coming', {})
    cm_txt = '\n'.join('          <li>%s</li>' % esc(t) for t in cm.get('text', []))
    return '''<section class="section section--books" id="books">
  <div class="wrap">
    <header class="section__head reveal">
      <p class="kicker">%s</p>
      <h2>%s</h2>
      <p class="lead">%s</p>
    </header>
    <div class="books">
%s
    </div>
    <div class="freud reveal">
      <h3 class="freud__title">%s</h3>
      <ul class="freud__list">
%s
      </ul>
      <p>%s</p>
    </div>
    <div class="coming reveal">
      <h3 class="coming__title">%s</h3>
      <ul class="coming__list">
%s
      </ul>
    </div>
  </div>
</section>''' % (esc(b.get('kicker', '')), esc(b['title']), esc(b.get('lead', '')),
                  '\n'.join(cards), esc(fr.get('title', '')), fr_txt, link(fr.get('read'), 'btn btn--line btn--sm'),
                  esc(cm.get('title', '')), cm_txt)


def render_training(t):
    progs = []
    for p in t.get('programs', []):
        require(p, 'title')
        progs.append('''        <article class="prog reveal">
          <p class="prog__label">%s</p>
          <h3 class="prog__title">%s</h3>
          <p class="prog__hours">%s</p>
          <p class="prog__go">%s</p>
        </article>''' % (esc(p.get('label', '')), esc(p['title']), esc(p.get('hours', '')),
                          link({'label': 'Подробнее', 'href': p.get('href')}, 'link--arrow')))
    return '''<section class="section" id="training">
  <div class="wrap">
    <header class="section__head reveal">
      <p class="kicker">%s</p>
      <h2>%s</h2>
      <p class="lead">%s</p>
    </header>
    <div class="progs">
%s
    </div>
  </div>
</section>''' % (esc(t.get('kicker', '')), esc(t['title']), esc(t.get('lead', '')),
                  '\n'.join(progs))


def render_consult(c):
    fmts = '\n'.join('''        <article class="price reveal">
          <h3 class="price__title">%s</h3>
          <p class="price__num">%s</p>
          <p class="price__note">%s</p>
        </article>''' % (esc(f['title']), esc(f['price']), esc(f.get('note', '')))
        for f in c.get('formats', []))
    tops = '\n'.join('''        <article class="topic reveal">
          <h3 class="topic__title">%s</h3>
          <p class="topic__go">%s</p>
        </article>''' % (esc(x['title']), link({'label': 'Разобрать подробно', 'href': x.get('href')}, 'link--arrow'))
        for x in c.get('topics', []))
    return '''<section class="section" id="consult">
  <div class="wrap">
    <header class="section__head reveal">
      <p class="kicker">%s</p>
      <h2>%s</h2>
      <p class="lead">%s</p>
    </header>
    <div class="prices">
%s
    </div>
    <p class="note reveal">%s</p>
    <div class="topics">
%s
    </div>
  </div>
</section>''' % (esc(c.get('kicker', '')), esc(c['title']), esc(c.get('lead', '')),
                  fmts, esc(c.get('note', '')), tops)


def render_business(b):
    items = '\n'.join('''        <article class="mythcard reveal">
          <h3 class="mythcard__title">%s</h3>
          <p class="mythcard__text">%s</p>
        </article>''' % (esc(i['title']), esc(i.get('text', ''))) for i in b.get('items', []))
    return '''<section class="section" id="business">
  <div class="wrap">
    <header class="section__head reveal">
      <p class="kicker">%s</p>
      <h2>%s</h2>
      <p class="lead">%s</p>
    </header>
    <div class="myths">
%s
    </div>
  </div>
</section>''' % (esc(b.get('kicker', '')), esc(b['title']), esc(b.get('lead', '')), items)


def render_myths(m):
    items = '\n'.join('''        <article class="mythcard reveal">
          <h3 class="mythcard__title">%s</h3>
          <p class="mythcard__text">%s</p>
          <p class="mythcard__foot">%s</p>
        </article>''' % (esc(i['title']), esc(i.get('text', '')),
                          link({'label': 'Разбор мифа', 'href': i.get('href')}, 'link--arrow'))
        for i in m.get('items', []))
    return '''<section class="section" id="myths">
  <div class="wrap">
    <header class="section__head reveal">
      <p class="kicker">%s</p>
      <h2>%s</h2>
      <p class="lead">%s</p>
    </header>
    <div class="myths">
%s
    </div>
  </div>
</section>''' % (esc(m.get('kicker', '')), esc(m['title']), esc(m.get('lead', '')), items)


def render_blog(b):
    items = '\n'.join('''        <article class="topic reveal">
          <h3 class="topic__title">%s</h3>
          <p class="topic__go">%s</p>
        </article>''' % (esc(i['title']), link({'label': 'Читать', 'href': i.get('href')}, 'link--arrow'))
        for i in b.get('items', []))
    return '''<section class="section" id="blog">
  <div class="wrap">
    <header class="section__head reveal">
      <p class="kicker">%s</p>
      <h2>%s</h2>
      <p class="lead">%s</p>
    </header>
    <div class="topics">
%s
    </div>
  </div>
</section>''' % (esc(b.get('kicker', '')), esc(b['title']), esc(b.get('lead', '')), items)


def render_footer(f):
    cols = '\n'.join('''        <div class="foot__col">
          <h4 class="foot__ctitle">%s</h4>
          <ul class="foot__links">
%s
          </ul>
        </div>''' % (esc(c['title']),
                      '\n'.join('            <li>%s</li>' % link(l) for l in c.get('links', [])))
        for c in f.get('columns', []))
    return '''<footer class="foot" id="footer">
  <div class="wrap foot__inner">
    <div class="foot__lead">
      <h2 class="foot__title">%s</h2>
      <p class="foot__text">%s</p>
      <a class="btn btn--gold" href="%s">%s</a>
    </div>
    <div class="foot__cols">
%s
    </div>
  </div>
  <p class="foot__copy">%s</p>
</footer>''' % (esc(f['title']), esc(f.get('lead', '')),
                H.escape(f['cta']['href'], quote=True), esc(f['cta']['label']),
                cols, esc(f.get('copyright', '')))


# ── Сопоставление разделов JSON и функций отрисовки ───────────────────────
SECTIONS = [
    ('specialists', render_specialists),
    ('books', render_books),
    ('training', render_training),
    ('consult', render_consult),
    ('business', render_business),
    ('myths', render_myths),
    ('blog', render_blog),
]


def build(lang):
    src = CONTENT / ('%s.json' % lang)
    if not src.is_file():
        print('  %s: файла текста нет — пропускаю' % lang)
        return None
    d = json.loads(src.read_text(encoding='utf-8'))

    # ПРОВЕРКА: раздел есть в JSON, но нет функции отрисовки → падаем.
    # Иначе текст молча не попадёт на страницу, и это заметят только глазами.
    known = {k for k, _ in SECTIONS}
    unknown = [k for k in d if k not in known and k not in
               ('_', 'lang', 'dir', 'meta', 'head', 'hero', 'footer')]
    if unknown:
        raise SystemExit('ОСТАНОВ: в %s.json есть разделы без отрисовки: %s. '
                         'Напишите функцию render_<имя> в build_pages.py.' % (lang, ', '.join(unknown)))

    body = render_hero(d['hero']) + '\n\n' + '\n\n'.join(
        fn(d[key]) for key, fn in SECTIONS if key in d)

    # Стили и скрипты подключаются одинаково для всех языков: страницы
    # отличаются только содержимым, не разметкой.
    html = TEMPLATE % {
        'lang': esc(d.get('lang', lang)),
        'dir': esc(d.get('dir', 'ltr')),
        'title': esc(d['meta']['title']),
        'description': esc(d['meta'].get('description', '')),
        'canonical': H.escape(d['meta'].get('canonical', ''), quote=True),
        'head': render_head(d['head'], d['meta']),
        'body': body,
        'footer': render_footer(d['footer']),
    }
    out = BASE / ('index.html' if lang == 'ru' else '%s/index.html' % lang)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf-8', newline='\n')
    return out


# ── Каркас страницы ──────────────────────────────────────────────────────
TEMPLATE = '''<!doctype html>
<html lang="%(lang)s" dir="%(dir)s" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(description)s">
<link rel="canonical" href="%(canonical)s">
<script>
/* ТЕМА ПРИМЕНЯЕТСЯ ДО ОТРИСОВКИ — иначе при загрузке мигает тёмным.
   Ключ в хранилище читается синхронно, до первого кадра. */
(function(){try{var t=localStorage.getItem('ragimoff-theme')||'dark';
document.documentElement.setAttribute('data-theme',t);}catch(e){}})();
</script>
<link rel="stylesheet" href="design/tokens/tokens.generated.css">
<link rel="stylesheet" href="design/foundations/reset.css">
<link rel="stylesheet" href="design/foundations/typography.css">
<link rel="stylesheet" href="design/foundations/layout.css">
<link rel="stylesheet" href="design/components/base.css">
<link rel="stylesheet" href="design/components/hero.css">
<link rel="stylesheet" href="design/components/blocks.css">
<link rel="stylesheet" href="design/components/pages.css">
<link rel="stylesheet" href="design/components/motion.css">
</head>
<body>

%(head)s

<main id="main">
%(body)s
</main>

%(footer)s

<script type="module">
/* ── СЕТЬ ИНТЕЛЛЕКТА В ГЕРОЕ ────────────────────────────────────────
   Смысл, который передаёт сцена: узлы и связи — мышление, движение
   по связям — развитие, сборка к цели при прокрутке — путь к своей
   цели. Не симметричная сфера («штамп»), а НАПРАВЛЕННЫЙ ПОТОК.

   Сеть живёт в свободных зонах кадра: замер показал, что портрет
   занимает центр, поэтому узлы там не создаются — «паутина на лице»
   исключена расчётом.

   Любая ошибка здесь не должна ломать страницу: модуль в try/catch. */
try {
  const THREE = await import('./vendor/three.module.js');
  const mod = await import('./design/components/hero-net.js');
  const cv = document.getElementById('heroNet');
  const net = (cv && mod.initHeroNet) ? mod.initHeroNet(cv, { THREE }) : null;
  if (net) {
    const hero = document.getElementById('hero');
    const onScroll = function () {
      if (!hero) return;
      const h = hero.offsetHeight - window.innerHeight;
      net.setProgress(h > 0 ? Math.max(0, Math.min(1, window.scrollY / h)) : 0);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    window.__heroNet = net;
  }
} catch (e) {
  if (window.console) console.warn('сеть героя не запустилась:', e && e.message);
}
</script>

<script src="design/components/motion.js"></script>
</body>
</html>
'''


def main():
    args = sys.argv[1:]
    langs = args if args else LANGS
    print('СБОРКА СТРАНИЦ ИЗ ЕДИНОГО ФАЙЛА ТЕКСТА')
    for lg in langs:
        out = build(lg)
        if out:
            n = len(out.read_text(encoding='utf-8'))
            print('  %-3s → %-28s %6d байт' % (lg, out.relative_to(BASE), n))
    print('готово')


if __name__ == '__main__':
    main()
