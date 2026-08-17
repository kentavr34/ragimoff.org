# -*- coding: utf-8 -*-
"""Правки доступности по сайту: метки полей, размеры картинок, пустой src.

Найдено замерами на живой странице 2026-08-18:

1. Метка есть, связи нет. Форма заказа книги печатает «Ad Soyad» и
   «Mobil nömrə» как <label>, но без for=; поле остаётся безымянным для
   скринридера, а клик по подписи не ставит курсор в поле.
2. Поле без метки вовсе (поиск в hero) — даётся aria-label из placeholder.
   Placeholder исчезает, как только человек начинает печатать, поэтому
   сам по себе меткой он быть не может.
3. Ни у одного изображения нет width/height — браузер не знает высоту до
   загрузки и страница прыгает. Размеры берём из самого файла.
4. <img src=""> — плейсхолдер лайтбокса. Пустой src браузер трактует как
   запрос текущей страницы: лишняя загрузка на каждой странице.

ОСТОРОЖНО, дефект первой версии этого скрипта (2026-08-18, исправлен):
регулярка вида <label ...>.*?</label> с re.DOTALL проглатывала ЧУЖОЙ
закрывающий </label> и связывала метку с полем, которое стоит много ниже
по странице. В b2b.html метки «Şirkətin Adı», «Telefon», «E-mail» получили
for="km-name" — указатель на поле формы заказа книги. Теперь тело метки
описано как (?:(?!</label>).)*? и не может пересечь границу своего тега,
а привязка сверяется с полем, идущим непосредственно за меткой.

Скрипт идемпотентен и самовосстанавливающийся: неверный for снимается.

    python fix_a11y.py            # сухой прогон
    python fix_a11y.py --apply
"""
import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
APPLY = '--apply' in sys.argv
DIRS = [ROOT, ROOT / 'ru', ROOT / 'en']

PIXEL = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'

try:
    from PIL import Image
except ImportError:
    Image = None

# Тело метки не может пересечь свой закрывающий тег — это и есть починка
# дефекта первой версии.
LABEL = re.compile(
    r'<label\b([^>]*)>((?:(?!</label>).)*?)</label>(\s*)'
    r'(<(?:input|select|textarea)\b[^>]*>)',
    re.I | re.S)
FIELD = re.compile(r'<(input|select|textarea)\b([^>]*)>', re.I)
IMG = re.compile(r'<img\b([^>]*)>', re.I)
_size_cache = {}


def img_size(src, page):
    if Image is None or not src or src.startswith(('http', 'data:', '//')):
        return None
    rel = src.split('?')[0].split('#')[0]
    p = (page.parent / rel).resolve() if not rel.startswith('/') else (ROOT / rel.lstrip('/')).resolve()
    key = str(p)
    if key in _size_cache:
        return _size_cache[key]
    out = None
    if p.exists() and p.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.avif'}:
        try:
            with Image.open(p) as im:
                out = im.size
        except Exception:
            out = None
    _size_cache[key] = out
    return out


def fix_labels(text, slug, stat):
    """Связывает метку с полем, стоящим НЕПОСРЕДСТВЕННО за ней.

    Снимает for=, если он указывает не на это поле: так чинится ошибка,
    уже записанная в страницы предыдущей версией скрипта.
    """
    used = set(re.findall(r'\bid="([^"]+)"', text))
    counter = [0]

    def one(m):
        attrs, body, gap, field = m.group(1), m.group(2), m.group(3), m.group(4)
        # у поля должен быть id, иначе выдаём свой
        fid_m = re.search(r'\bid="([^"]+)"', field)
        if fid_m:
            fid = fid_m.group(1)
            new_field = field
        else:
            if not re.sub(r'<[^>]+>', '', body).strip():
                return m.group(0)          # пустая метка — связывать нечего
            counter[0] += 1
            fid = '%s-f%d' % (slug, counter[0])
            while fid in used:
                counter[0] += 1
                fid = '%s-f%d' % (slug, counter[0])
            used.add(fid)
            tag = re.match(r'<(\w+)', field).group(1)
            new_field = '<%s id="%s"%s' % (tag, fid, field[len(tag) + 1:])
            stat['field_id'] += 1

        cur = re.search(r'\bfor="([^"]+)"', attrs)
        if cur and cur.group(1) == fid:
            return '<label%s>%s</label>%s%s' % (attrs, body, gap, new_field)
        if cur:
            stat['for_fixed'] += 1          # снимаем неверную привязку
            attrs = re.sub(r'\s*\bfor="[^"]*"', '', attrs)
        else:
            stat['for_added'] += 1
        return '<label for="%s"%s>%s</label>%s%s' % (fid, attrs, body, gap, new_field)

    prev = None
    while prev != text:                     # пары могут перекрываться
        prev = text
        text = LABEL.sub(one, text)
    return text



HEAD = re.compile(r'<h([1-6])\b([^>]*)>', re.I)


def fix_headings(text, stat):
    """Чинит пропуск уровня заголовка, не трогая внешний вид.

    Голых правил h3{} и h4{} в таблицах стилей нет — кегль этих заголовков
    задаёт браузер, поэтому смена тега h4 на h3 увеличила бы его примерно
    на 17 %. Вместо тега правим объявленный уровень: role="heading" плюс
    aria-level. Для скринридера иерархия становится сплошной, для глаза
    страница остаётся прежней.
    """
    last = [0]

    def one(m):
        lvl, attrs = int(m.group(1)), m.group(2)
        prev = last[0]
        want = lvl
        if prev and lvl > prev + 1:
            want = prev + 1
        last[0] = want
        if want == lvl:
            # уровень в норме: снимаем свой прежний костыль, если он лишний
            if 'data-a11y-level' in attrs:
                stat['heading'] += 1
                attrs = re.sub(r'\s*role="heading"|\s*aria-level="\d"|\s*data-a11y-level', '', attrs)
                return '<h%d%s>' % (lvl, attrs)
            return m.group(0)
        if 'aria-level="%d"' % want in attrs:
            return m.group(0)
        stat['heading'] += 1
        attrs = re.sub(r'\s*role="heading"|\s*aria-level="\d+"|\s*data-a11y-level', '', attrs)
        return '<h%d%s role="heading" aria-level="%d" data-a11y-level>' % (lvl, attrs, want)

    return HEAD.sub(one, text)


SKIP_HTML = ('<a class="skip-link" href="#main-content">'
             'Əsas məzmuna keç</a>')


def fix_skip_link(text, stat):
    """Ссылка «к основному содержимому» — первое, что слышит скринридер.

    Без неё человек на клавиатуре проходит всю шапку и меню на каждой
    странице заново. Цель — первая секция после навигации; отдельный
    <main> не добавляем, чтобы не менять структуру, от которой зависят
    селекторы вида body > section.
    """
    if 'class="skip-link"' in text:
        return text
    m = re.search(r'<section\b(?![^>]*\bid=)', text)
    if not m:
        m2 = re.search(r'<section\b[^>]*\bid="([^"]+)"', text)
        if not m2:
            return text
        target = m2.group(1)
    else:
        target = 'main-content'
        text = text[:m.end()] + ' id="main-content"' + text[m.end():]
    b = re.search(r'<body\b[^>]*>', text, re.I)
    if not b:
        return text
    stat['skip_link'] += 1
    link = SKIP_HTML.replace('#main-content', '#' + target)
    return text[:b.end()] + '\n    ' + link + text[b.end():]


def fix_page(text, page, stat):
    slug = re.sub(r'[^a-z0-9]+', '-', page.stem.lower()).strip('-')[:14] or 'f'
    text = fix_labels(text, slug, stat)
    text = fix_headings(text, stat)
    text = fix_skip_link(text, stat)

    labelled = set(re.findall(r'<label\b[^>]*\bfor="([^"]+)"', text, re.I))
    for m in re.finditer(r'<label\b[^>]*>((?:(?!</label>).)*?)</label>', text, re.I | re.S):
        labelled |= set(re.findall(r'\bid="([^"]+)"', m.group(1)))

    def aria(m):
        tag, attrs = m.group(1), m.group(2)
        if re.search(r'\baria-label(?:ledby)?=', attrs, re.I):
            return m.group(0)
        if re.search(r'type="(hidden|submit|button|checkbox|radio)"', attrs, re.I):
            return m.group(0)
        fid = re.search(r'\bid="([^"]+)"', attrs)
        if fid and fid.group(1) in labelled:
            return m.group(0)
        ph = re.search(r'\bplaceholder="([^"]+)"', attrs)
        if not ph:
            return m.group(0)
        stat['aria_label'] += 1
        return '<%s%s aria-label="%s">' % (tag, attrs.rstrip(' /'), ph.group(1))
    text = FIELD.sub(aria, text)

    def image(m):
        attrs = m.group(1)
        src = re.search(r'\bsrc="([^"]*)"', attrs)
        if src is not None and src.group(1) == '':
            stat['empty_src'] += 1
            return '<img%s>' % attrs.replace('src=""', 'src="%s"' % PIXEL)
        if re.search(r'\bwidth=', attrs) or 'aspect-ratio' in attrs or src is None:
            return m.group(0)
        size = img_size(src.group(1), page)
        if not size:
            return m.group(0)
        stat['img_dim'] += 1
        w, h = size
        end = ' />' if attrs.rstrip().endswith('/') else '>'
        return '<img%s width="%d" height="%d"%s' % (attrs.rstrip(' /'), w, h, end)
    return IMG.sub(image, text)


def main():
    total = {'for_added': 0, 'for_fixed': 0, 'field_id': 0,
             'aria_label': 0, 'img_dim': 0, 'empty_src': 0,
             'heading': 0, 'skip_link': 0}
    touched = 0
    for d in DIRS:
        if not d.exists():
            continue
        for p in sorted(d.glob('*.html')):
            raw = p.read_bytes()
            crlf = raw.count(b'\r\n') > raw.count(b'\n') // 2
            t = raw.decode('utf-8').replace('\r\n', '\n')
            stat = {k: 0 for k in total}
            new = fix_page(t, p, stat)
            if new != t:
                touched += 1
                for k in total:
                    total[k] += stat[k]
                if APPLY:
                    p.write_bytes((new.replace('\n', '\r\n') if crlf else new).encode('utf-8'))
    print('файлов затронуто: %d' % touched)
    print('  for= проставлено      %d' % total['for_added'])
    print('  for= ИСПРАВЛЕНО       %d  (указывал на чужое поле)' % total['for_fixed'])
    print('  id полю выдано        %d' % total['field_id'])
    print('  aria-label            %d' % total['aria_label'])
    print('  width/height картинке %d' % total['img_dim'])
    print('  пустой src            %d' % total['empty_src'])
    print('  уровень заголовка     %d' % total['heading'])
    print('  skip-link             %d' % total['skip_link'])
    print('ПРИМЕНЕНО' if APPLY else 'сухой прогон — запустить с --apply')


if __name__ == '__main__':
    main()
