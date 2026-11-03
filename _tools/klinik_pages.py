# -*- coding: utf-8 -*-
"""_tools/klinik_pages.py — «Клиническая психиатрия»: страницы сайта из утверждённых печатных DOCX (03.11.2026).

Что делает
  Для каждого из 4 языков (az, ru, en, tr) берёт утверждённый Word из D:/Projects/Psychiatry/Print/print.json,
  режет его по структуре книги на ТЕ ЖЕ страницы, что уже лежат на сайте (URL не меняются), и подставляет
  новое ТЕЛО в существующую страницу как в шаблон: шапка, навигация, сайдбар, hreflang, JSON-LD, «назад/вперёд»,
  скрипты остаются как есть. Меняются:
    · `.bk-read` (текст страницы) — целиком из DOCX;
    · `<h1 class="bk-chead__h1">`, `<title>`, og:title, description — название из DOCX;
    · имя автора в шапке/keywords/JSON-LD — как в печати (az: Kənan Rəhimov; ru: Кенан Рагимов; en/tr: Kenan Ragimov);
    · названия расстройств/глав в сайдбаре, оглавлении, «назад/вперёд» — как в печати (код → название).
  Границы страниц (одинаковы для всех языков, потому что структура DOCX параллельна):
    · 23 страницы глав NN-*.html — H1 главы (заголовок и подзаголовок; сами расстройства — отдельными страницами);
    · 97 страниц расстройств КОД.html — от таблицы кодов «XBT-11/ICD-11/МКБ-11 КОД» до следующей такой таблицы/H1;
    · mugeddime, kitab-haqqinda, melumat (хвост «Məlumat bölməsi» — служебная часть сайта — остаётся), elave-acde,
      elave-skalalar, yekun — по порядковым номерам H1 (их 42 в каждом языке);
  НЕ трогает: index.html, mundericat.html, terminoloji-luget.html, abbreviatur.html, bolme-*.html, перенаправления.

Разметка тела — как в текущих страницах: Heading3→h2 (с id), Heading4→h3, списки ul/ol (ref-list под «Mənbələr»,
method-num под «Müalicə metodikaları»), таблицы `div.tbl-wrap>table` (первая строка th), `dl`, шапка расстройства
`table.bk-codes` + `nav.page-toc`.

Запуск (из PowerShell, из корня сайта):
    python _tools/klinik_pages.py --stage D:/tmp/klp            # собрать в каталог (сайт не трогать)
    python _tools/klinik_pages.py --lang az --page 6A20         # одна страница
    python _tools/klinik_pages.py --apply                       # записать в сайт
    python _tools/klinik_pages.py --apply --names-only          # только синхронизация названий/автора
Ничего не удаляет, git не использует. Бэкап до --apply делает человек.
"""
import argparse
import collections
import glob
import html as H
import io
import json
import os
import re
import sys
import zipfile

from lxml import etree

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(SITE, 'klinik-psixiatriya')
PRINT = os.environ.get('PSY_PRINT', 'D:/Projects/Psychiatry/Print')
sys.path.insert(0, os.environ.get('TRUTHDB', 'D:/Projects/Freud/tools/truthdb'))
import docx_blocks as D  # noqa: E402

LANGS = ['az', 'ru', 'en', 'tr']
AUTHOR = {  # как в печатном издании (титул): «Dr. Kənan Rəhimov» / «Д-р Кенан Рагимов» / Kenan Ragimov
    'az': dict(full='Kənan Rəhimov', short='K.Rəhimov'),
    'ru': dict(full='Кенан Рагимов', short='К.Рагимов', ld='Кенан Рагимов'),
    'en': dict(full='Kenan Ragimov', short='K.Ragimov'),
    'tr': dict(full='Kenan Ragimov', short='K. Ragimov'),
}
OLD_AUTHOR = {  # устаревшие написания на сайте → печать
    'az': [],
    'ru': [('Кянан', 'Кенан')],
    'en': [('K.Rahimov', 'K.Ragimov'), ('Kanan Rahimov', 'Kenan Ragimov'), ('Kenan Rahimov', 'Kenan Ragimov'), ('Kanan Ragimov', 'Kenan Ragimov')],
    'tr': [('K. Rahimov', 'K. Ragimov'), ('K.Rahimov', 'K.Ragimov'), ('Kenan Rahimov', 'Kenan Ragimov'), ('Kanan Ragimov', 'Kenan Ragimov')],
}
REF_RX = re.compile(r'(Mənbələr|Источники|Sources|References|Kaynaklar|Литература|Kaynakça)', re.I)
METHOD_RX = re.compile(r'(metodik|metodları|metod|методик|методы|methods|yöntem|metodoloj)', re.I)
CODE_RX = re.compile(r'^(.+?)\n([0-9A-Z]{4})(?:[.–-][0-9A-Z.]+)?$')


# ───────────────────────── DOCX ─────────────────────────
class Doc:
    def __init__(self, path):
        r = D.read_docx(path, with_images=False)
        self.path = path
        self.blocks = r['blocks']
        z = zipfile.ZipFile(io.BytesIO(r['raw']))
        W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        q = lambda t: '{%s}%s' % (W, t)  # noqa: E731
        absf, nums = {}, {}
        if 'word/numbering.xml' in z.namelist():
            root = etree.fromstring(z.read('word/numbering.xml'))
            for a in root.findall(q('abstractNum')):
                lv = {}
                for l in a.findall(q('lvl')):
                    nf = l.find(q('numFmt'))
                    lv[int(l.get(q('ilvl')))] = nf.get(q('val')) if nf is not None else 'bullet'
                absf[a.get(q('abstractNumId'))] = lv
            for n in root.findall(q('num')):
                nums[n.get(q('numId'))] = n.find(q('abstractNumId')).get(q('val'))
        for b in self.blocks:
            b['list'] = None
            if b['kind'] == 'list_item':
                m = re.search(r'<w:ilvl w:val="(\d+)"/><w:numId w:val="(\d+)"/>', (b['meta'] or {}).get('ppr', '') or '')
                il, nid = (int(m.group(1)), m.group(2)) if m else (0, '0')
                fmt = absf.get(nums.get(nid), {}).get(il, 'bullet')  # numId без описания в numbering.xml → маркер
                b['list'] = dict(ilvl=il, num=nid, ordered=fmt not in ('bullet', 'none'))
        self.h1 = [b['i'] for b in self.blocks if b['style'] == 'Heading1' and b['kind'] == 'heading']

    def code_tables(self):
        """[(индекс первого блока таблицы, код, id таблицы)] — шапки расстройств."""
        out = []
        bl = self.blocks
        for b in bl:
            m = b['meta'] or {}
            if b['kind'] == 'table_cell' and m.get('r') == 0 and m.get('c') == 0 and 'cp' not in m:
                mm = CODE_RX.match(b['text'].strip())
                nxt = bl[b['i'] + 1] if b['i'] + 1 < len(bl) else None
                if mm and nxt and nxt['style'] == 'Heading2' and (nxt['meta'] or {}).get('tbl') == m.get('tbl'):
                    out.append((b['i'], mm.group(2), m['tbl']))
        return out


def approved():
    with open(os.path.join(PRINT, 'print.json'), encoding='utf-8') as f:
        return {k: os.path.join(PRINT, v['file']) for k, v in json.load(f)['approved'].items()}


# ───────────────────────── текст ─────────────────────────
def esc(s):
    return H.escape(s, quote=False)


def inline(b, flags=True):
    """Текст блока → HTML с <strong>/<em>/<sup>/<sub>; \n → <br>."""
    text = b['text'].replace('\x0c', ' ').replace('\x0b', ' ').replace('\t', ' ')
    n = len(text)
    fl = [''] * n
    if flags:
        # fmt считан по исходному тексту; \x0c/\x0b/\t заменены 1:1 по длине → смещения сохраняются
        for s, e, f in b['fmt']:
            for k in range(s, min(e, n)):
                fl[k] += f
    segs, i = [], 0
    while i < n:
        j = i
        while j < n and fl[j] == fl[i]:
            j += 1
        segs.append((text[i:j], fl[i]))
        i = j
    out = []
    for t, f in segs:
        h = esc(t).replace('\n', '<br>\n')
        if f and t.strip():
            if 'b' in f:
                h = '<strong>' + h + '</strong>'
            if 'i' in f:
                h = '<em>' + h + '</em>'
            if '^' in f:
                h = '<sup>' + h + '</sup>'
            if '_' in f:
                h = '<sub>' + h + '</sub>'
        out.append(h)
    s = ''.join(out)
    s = re.sub(r'^(\s|<br>\n?)+', '', s)
    s = re.sub(r'(\s|<br>\n?)+$', '', s)
    s = s.replace('</strong><strong>', '').replace('</em><em>', '')
    return s


def plain(b):
    return re.sub(r'\s+', ' ', b['text'].replace('\x0c', ' ')).strip()


def is_turkic(lang):
    return lang in ('az', 'tr')


def lower_l(s, lang):
    if is_turkic(lang):
        s = s.replace('İ', 'i').replace('I', 'ı')
    return s.lower()


def slug(t, lang='az'):
    s = re.sub(r'[^\w\s-]', '', plain({'text': t}).lower())
    s = re.sub(r'[\s_]+', '-', s).strip('-')
    return s[:70] or 'x'


def sentence_case(t, lang):
    """ВЕРХНИЙ РЕГИСТР печатного заголовка → «Предложение»: скобки/цифры/коды сохраняются."""
    t = plain({'text': t})
    mt = re.match(r'^(.*?)(\s\([^()]*[a-z][^()]*\))$', t)
    if mt and mt.group(1) == mt.group(1).upper():
        return sentence_case(mt.group(1), lang) + mt.group(2)
    if t != t.upper():
        return t
    keep_rx = re.compile(r'\(([^()\s]{1,5})\)')
    keep = set(m.start(1) for m in keep_rx.finditer(t))  # (ASP), (DƏHP): одно слово ≤5 знаков в скобках — аббревиатура
    out, pos = [], 0
    for w in t.split(' '):
        start = pos
        pos += len(w) + 1
        k = w.find('(')
        is_keep = k >= 0 and (start + k + 1) in keep or bool(re.search(r'\d', w))
        out.append(w if is_keep else lower_l(w, lang))
    s = ' '.join(out)
    # первая буква заглавная
    for k, ch in enumerate(s):
        if ch.isalpha():
            up = ch.upper()
            if is_turkic(lang) and ch == 'i':
                up = 'İ'
            s = s[:k] + up + s[k + 1:]
            break
    return s


def display_name(docx_title, old_name, lang):
    """Название страницы: если слова те же, что на сайте, оставляем регистр сайта (аббревиатуры), иначе — из печати."""
    new = sentence_case(docx_title, lang)
    if old_name and lower_l(re.sub(r'\s+', ' ', old_name).strip(), lang) == lower_l(new, lang):
        return old_name
    return new


# ───────────────────────── рендер блоков ─────────────────────────
class Ids:
    def __init__(self, reuse=None):
        self.used = set()
        self.reuse = reuse or {}

    def get(self, text, lang, key=None):
        if key is not None and key in self.reuse and self.reuse[key] not in self.used:
            i = self.reuse[key]
        else:
            base = slug(text, lang)
            i, n = base, 2
            while i in self.used:
                i = '%s-%d' % (base, n)
                n += 1
        self.used.add(i)
        return i


def render(doc, ranges, lang, hmap, ids, skip_h1=False, code_page=None, reuse_key=None):
    """Блоки → HTML. hmap: {уровень заголовка docx: (тег, класс|None)}."""
    bl = doc.blocks
    out = []
    heads = []  # (тег, id, текст)
    last_h = {3: '', 4: ''}  # последний заголовок уровней docx 3 и 4 (для ref-list/method-num)
    i_list = []

    def flush_list(stack):
        pass

    for lo, hi in ranges:
        i = lo
        while i < hi:
            b = bl[i]
            m = b['meta'] or {}
            k = b['kind']
            if k == 'table_cell':
                # собрать всю таблицу
                tid = m.get('tbl')
                j = i
                cells = collections.OrderedDict()
                while j < hi and bl[j]['kind'] == 'table_cell' and (bl[j]['meta'] or {}).get('tbl') == tid:
                    mj = bl[j]['meta']
                    cells.setdefault((mj['r'], mj['c']), []).append(bl[j])
                    j += 1
                rows = collections.OrderedDict()
                for (r, c), ps in cells.items():
                    rows.setdefault(r, []).append(ps)
                first = rows[0][0][0]
                if code_page and CODE_RX.match(first['text'].strip()) and len(rows[0]) == 2 and rows[0][1][0]['style'] == 'Heading2':
                    out.append(code_table(rows))
                else:
                    out.append(plain_table(rows))
                i = j
                continue
            if k in ('empty', 'toc', 'image'):
                i += 1
                continue
            if k == 'heading':
                lv = b['level'] or 1
                if lv == 1 and skip_h1 and not out:
                    i += 1
                    continue
                spec = hmap.get(lv) or hmap.get('*')
                txt = plain(b)
                if lv in (3, 4):
                    last_h[lv] = txt
                    if lv == 3:
                        last_h[4] = ''
                if spec is None:
                    out.append('<p><strong>%s</strong></p>' % esc(txt))
                    i += 1
                    continue
                tag, cls = spec
                attrs = ''
                if tag in ('h2', 'h3', 'h4', 'h5'):
                    hid = ids.get(txt, lang, reuse_key(txt, tag) if reuse_key else None)
                    attrs = ' id="%s"' % hid
                    heads.append((tag, hid, txt, cls))
                if cls:
                    attrs += ' class="%s"' % cls
                out.append('<%s%s>%s</%s>' % (tag, attrs, inline(b, flags=False).replace('<br>\n', ' '), tag))
                i += 1
                continue
            if k == 'list_item':
                j = i
                items = []
                while j < hi and bl[j]['kind'] in ('list_item', 'empty'):
                    if bl[j]['kind'] == 'list_item':
                        items.append(bl[j])
                    j += 1
                out.append(render_list(items, last_h))
                i = j
                continue
            st = b['style']
            if st in ('DefinitionTerm', 'Definition'):
                j = i
                dl = []
                while j < hi and bl[j]['style'] in ('DefinitionTerm', 'Definition', None) and bl[j]['kind'] in ('body', 'empty'):
                    if bl[j]['kind'] == 'body':
                        dl.append('<%s>%s</%s>' % ('dt' if bl[j]['style'] == 'DefinitionTerm' else 'dd', inline(bl[j]),
                                                   'dt' if bl[j]['style'] == 'DefinitionTerm' else 'dd'))
                    j += 1
                out.append('<dl>\n' + '\n'.join(dl) + '\n</dl>')
                i = j
                continue
            if st == 'SourceCode':
                out.append('<p class="pre-line">%s</p>' % inline(b, flags=False))
                i += 1
                continue
            t = inline(b)
            if t:
                out.append('<p>%s</p>' % t)
            i += 1
    return out, heads


def render_list(items, last_h):
    ref = REF_RX.search(last_h.get(3, '')) or REF_RX.search(last_h.get(4, ''))
    meth = METHOD_RX.search(last_h.get(4, '') or last_h.get(3, ''))
    out, stack = [], []  # stack: dict(tag, il, num)
    for b in items:
        li = b['list']
        tag = 'ol' if li['ordered'] else 'ul'
        il = li['ilvl']
        while stack and stack[-1]['il'] > il:
            out.append('</li></%s>' % stack.pop()['tag'])
        if stack and stack[-1]['il'] == il and (stack[-1]['num'] != li['num'] or stack[-1]['tag'] != tag):
            out.append('</li></%s>' % stack.pop()['tag'])
        if stack and stack[-1]['il'] == il:
            out.append('</li>\n')
        else:
            cls = ''
            if not stack and tag == 'ol':
                cls = ' class="ref-list"' if ref else (' class="method-num"' if meth else '')
            out.append('<%s%s>\n' % (tag, cls))
            stack.append(dict(tag=tag, il=il, num=li['num']))
        out.append('<li>' + inline(b))
    while stack:
        out.append('</li></%s>' % stack.pop()['tag'])
    return ''.join(out)


def cell_html(paras, th=False):
    return '<br>'.join(x for x in (inline(p, flags=not th) for p in paras) if x)


def plain_table(rows):
    out = ['<div class="tbl-wrap"><table>']
    for r, cells in rows.items():
        tag = 'th' if r == 0 else 'td'
        out.append('<tr>' + ''.join('<%s>%s</%s>' % (tag, cell_html(ps, th=(r == 0)), tag) for ps in cells) + '</tr>')
    out.append('</table></div>')
    return '\n'.join(out)


def code_table(rows):
    """Шапка расстройства: строки XBT-10/DSM-5-TR (строка XBT-11 вынесена в заголовок страницы)."""
    out = ['<table class="bk-codes"><tbody>']
    for r, cells in rows.items():
        if r == 0:
            continue
        lab = cells[0][0]['text'].strip().split('\n')
        l1, l2 = (lab[0], ' '.join(lab[1:])) if len(lab) > 1 else (lab[0], '')
        name = cell_html(cells[1]) if len(cells) > 1 else ''
        out.append('<tr><td class="dh-meta"><span class="dh-lbl">%s</span><span class="dh-code">%s</span></td><td class="dh-name">%s</td></tr>'
                   % (esc(l1.strip()), esc(l2.strip()), name))
    out.append('</tbody></table>')
    return ''.join(out)


# ───────────────────────── сегментация ─────────────────────────
def segment(doc):
    """{имя файла: параметры}. Одинаково для всех языков."""
    bl = doc.blocks
    h1 = doc.h1
    assert len(h1) == 42, 'ожидалось 42 заголовка H1, найдено %d' % len(h1)
    ct = doc.code_tables()
    starts = [s for s, _, _ in ct]
    seg = {}
    bounds = sorted(set(starts + h1 + [len(bl)]))

    def nxt(i):
        return min(b for b in bounds if b > i)

    for s, code, _ in ct:
        seg[code + '.html'] = dict(kind='code', code=code, ranges=[(s, nxt(s))])
    chap = h1[11:34]
    for k, hi in enumerate(chap):
        first = min([s for s in starts if s > hi] + [len(bl)])
        seg['chapter%02d' % k] = dict(kind='chapter', h1=hi, ranges=[(hi, first)])
    seg['mugeddime.html'] = dict(kind='front', ranges=[(h1[0] + 1, h1[1], 'under'), (h1[1], h1[4], 'std'), (h1[7], h1[11], 'std')])
    seg['kitab-haqqinda.html'] = dict(kind='front', ranges=[(h1[1] + 1, h1[2], 'under')])
    seg['melumat.html'] = dict(kind='front', ranges=[(h1[4], h1[7], 'std')], keep_prefix=True)
    seg['elave-acde.html'] = dict(kind='appx', ranges=[(h1[35], h1[36], 'appx'), (h1[37], h1[41], 'appx')])
    seg['elave-skalalar.html'] = dict(kind='appx', ranges=[(h1[36], h1[37], 'appx')])
    seg['yekun.html'] = dict(kind='front', ranges=[(h1[41] + 1, len(bl), 'under')])
    return seg


HMAPS = {
    'code': {3: ('h2', None), 4: ('h3', None), 5: ('h4', None), 2: ('h2', None)},
    'std': {1: ('h2', 'book-chapter'), 2: ('h3', None), 3: ('h4', None), 4: ('h5', None)},
    'under': {2: ('h2', None), 3: ('h3', None), 4: ('h4', None), 1: ('h2', 'book-chapter')},
    'appx': {1: ('h2', 'h-section'), 2: ('h2', None), 3: ('h3', None), 4: ('h4', None)},
}


# ───────────────────────── страница ─────────────────────────
READ_OPEN = '<div class="bk-read">'


def split_page(s):
    i = s.index(READ_OPEN) + len(READ_OPEN)
    j = s.index('<nav class="bk-pn"')
    k = s.rfind('</div>', i, j)
    return s[:i], s[i:k], s[k:]


def old_ids(body):
    ids = {}
    for m in re.finditer(r'<h([234]) id="([^"]+)"[^>]*>(.*?)</h\1>', body, re.S):
        t = re.sub(r'<[^>]+>', '', m.group(3)).strip()
        mm = re.match(r'^(\d+)\.', t)
        ids[('n', m.group(1), mm.group(1)) if mm else ('t', re.sub(r'\s+', ' ', t).lower())] = m.group(2)
    return ids


def reuse_key_fn(old):
    def f(txt, tag):
        mm = re.match(r'^(\d+)\.', txt)
        if mm and tag == 'h2':
            return old.get(('n', '2', mm.group(1))) and ('n', '2', mm.group(1))
        return ('t', re.sub(r'\s+', ' ', txt).lower())
    return f


def page_toc(heads, lang):
    items = ['<a href="#%s">%s</a>' % (hid, esc(re.sub(r'^\d+\.\s*', '', t))) for tag, hid, t, cls in heads if tag == 'h2']
    return '<nav class="page-toc">%s</nav>' % ''.join(items) if items else ''


def set_title(s, name, lang, booktitle=None):
    s = re.sub(r'(<title>)(.*?)( \| [^<]*</title>)', lambda m: m.group(1) + esc(name) + m.group(3), s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")(.*?)( \| [^"]*")', lambda m: m.group(1) + esc(name) + m.group(3), s, count=1)
    s = re.sub(r'(<meta name="description" content="[^"]*?— )([^"]*)(")', lambda m: m.group(1) + esc(name) + m.group(3), s, count=1)
    s = re.sub(r'(<meta property="og:description" content="[^"]*?— )([^"]*)(")', lambda m: m.group(1) + esc(name) + m.group(3), s, count=1)
    return s


def old_h1(s):
    m = re.search(r'<h1 class="bk-chead__h1">(.*?)</h1>', s, re.S)
    return re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else ''


def old_name_from_title(s):
    m = re.search(r'<title>(.*?) \| [^<]*</title>', s)
    return H.unescape(m.group(1)).strip() if m else ''


def code_title(doc, rng):
    """(название из шапки, англ. название) первой таблицы кода."""
    bl = doc.blocks
    i = rng[0]
    name = en = ''
    j = i
    while j < rng[1] and bl[j]['kind'] == 'table_cell' and (bl[j]['meta'] or {}).get('tbl') == bl[i]['meta']['tbl']:
        m = bl[j]['meta']
        if m['r'] == 0 and m['c'] == 1:
            if bl[j]['style'] == 'Heading2':
                name = re.sub(r'^[0-9A-Z]{4}(?:\s*[–-]\s*[0-9A-Z]{4})?\s+', '', plain(bl[j]))
            else:
                en = plain(bl[j])
        j += 1
    return name, en


def build_lang(lang, only=None, stage=None, apply=False, log=print):
    ap = approved()
    doc = Doc(ap[lang])
    seg = segment(doc)
    d = BOOK if lang == 'az' else os.path.join(BOOK, lang)
    chap_files = sorted(os.path.basename(f) for f in glob.glob(os.path.join(d, '[0-9][0-9]-*.html')))
    assert len(chap_files) == 23, (lang, len(chap_files))
    for k, f in enumerate(chap_files):
        seg[f] = dict(seg.pop('chapter%02d' % k), kind='chapter')
    names = {}
    upper = {}
    res = {}
    bl = doc.blocks
    for fname, sp in seg.items():
        if only and fname.replace('.html', '') not in only and fname not in only:
            continue
        path = os.path.join(d, fname)
        if not os.path.exists(path):
            log('  нет файла', path)
            continue
        s = open(path, encoding='utf-8').read()
        pre, body, post = split_page(s)
        if sp['kind'] == 'code':
            rng = sp['ranges'][0]
            ttl, en = code_title(doc, rng)
            old_nm = old_name_from_title(s)
            nm = display_name(ttl, old_nm, lang)
            ids = Ids()
            ids.reuse = old_ids(body)
            parts, heads = render(doc, [rng], lang, HMAPS['code'], ids, code_page=True, reuse_key=reuse_key_fn(ids.reuse))
            content = [p for p in parts]
            toc = page_toc(heads, lang)
            if toc:
                # nav.page-toc — сразу после таблицы кодов
                if content and content[0].startswith('<table class="bk-codes"'):
                    content.insert(1, toc)
                else:
                    content.insert(0, toc)
            h1 = nm + (' (%s)' % en if en and lower_l(en, lang) != lower_l(nm, lang) else '')
            new_body = '\n' + '\n\n'.join(content) + '\n'
            pre = re.sub(r'(<h1 class="bk-chead__h1">)(.*?)(</h1>)', lambda m: m.group(1) + esc(h1) + m.group(3), pre, count=1, flags=re.S)
            pre = set_title(pre, nm, lang)
            names[fname] = nm
            upper[fname] = ttl
        elif sp['kind'] == 'chapter':
            hi = sp['h1']
            raw = plain(bl[hi])
            title = re.sub(r'^[0-9A-Z]{4}(?:\s*[–-]\s*[0-9A-Z]{4})?\s+', '', raw)
            old_nm = old_name_from_title(s)
            nm = display_name(title, re.sub(r'\s*\(.*\)$', '', old_nm) or old_nm, lang)
            sub = []
            for b in bl[sp['ranges'][0][0] + 1: sp['ranges'][0][1]]:
                if b['kind'] == 'body' and plain(b):
                    sub.append(plain(b))
            suff = re.search(r'(\s\([^()]*\))$', old_h1(s))
            h1 = nm + (suff.group(1) if suff else '')
            pre = re.sub(r'(<h1 class="bk-chead__h1">)(.*?)(</h1>)', lambda m: m.group(1) + esc(h1) + m.group(3), pre, count=1, flags=re.S)
            pre = re.sub(r'\s*<p class="bk-chead__en">.*?</p>', '', pre, flags=re.S)
            if sub:
                pre = pre.replace('</h1>', '</h1>\n        ' + '\n        '.join('<p class="bk-chead__en">%s</p>' % esc(x) for x in sub), 1)
            pre = set_title(pre, nm, lang)
            new_body = body
            names[fname] = nm
        else:
            ids = Ids()
            ids.reuse = old_ids(body)
            content, heads = [], []
            for lo, hi, mode in sp['ranges']:
                parts, hh = render(doc, [(lo, hi)], lang, HMAPS[mode], ids, reuse_key=reuse_key_fn(ids.reuse))
                content += parts
                heads += hh
            keep = ''
            if sp.get('keep_prefix'):
                mm = re.search(r'<h2 id="[^"]*" class="book-chapter"', body)
                keep = body[:mm.start()] if mm else ''
                # nav.page-toc перестраиваем: служебные якоря + новые главы
                svc = re.findall(r'<a href="#([^"]+)">([^<]*)</a>', keep.split('</nav>')[0]) if '<nav class="page-toc">' in keep else []
                svc = [(a, t) for a, t in svc if not re.search(r'id="%s"[^>]*class="book-chapter"' % re.escape(a), body)]
                svc = svc[:3]
                nav = '<nav class="page-toc">' + ''.join('<a href="#%s">%s</a>' % (a, esc(t)) for a, t in svc) + \
                      ''.join('<a href="#%s">%s</a>' % (hid, esc(t)) for tag, hid, t, cls in heads if cls == 'book-chapter') + '</nav>'
                keep = re.sub(r'<nav class="page-toc">.*?</nav>', lambda m: nav, keep, count=1, flags=re.S)
            elif fname == 'kitab-haqqinda.html':
                nav = page_toc(heads, lang).replace('page-toc', 'page-toc')
                keep = nav
                hh = [h for h in heads if h[0] == 'h2']
                keep = '<nav class="page-toc">' + ''.join('<a href="#%s">%s</a>' % (hid, esc(t)) for tag, hid, t, cls in hh) + '</nav>'
                content = ['<article class="front-page">'] + content + ['</article>']
            elif fname == 'mugeddime.html':
                content = ['<article class="front-page">'] + content + ['</article>']
            new_body = '\n' + (keep.strip('\n') + '\n\n' if keep else '') + '\n\n'.join(content) + '\n'
            tt = None
            # заголовок страницы-раздела: H1 из печати (если страница его показывает)
            if fname in ('mugeddime.html', 'kitab-haqqinda.html', 'yekun.html'):
                idx = {'mugeddime.html': 0, 'kitab-haqqinda.html': 1, 'yekun.html': 41}[fname]
                tt = plain(bl[doc.h1[idx]])
                old_nm = old_name_from_title(s)
                nm = display_name(tt if fname != 'kitab-haqqinda.html' else old_nm, old_nm, lang) if fname != 'kitab-haqqinda.html' else old_nm
                if fname != 'kitab-haqqinda.html':
                    suff = re.search(r'(\s\([^()]*\))$', old_h1(s))
                    pre = re.sub(r'(<h1 class="bk-chead__h1">)(.*?)(</h1>)',
                                 lambda m: m.group(1) + esc(nm + (suff.group(1) if suff else '')) + m.group(3), pre, count=1, flags=re.S)
                    pre = set_title(pre, nm, lang)
                    names[fname] = nm
        out = fix_author(pre, lang) + new_body + fix_author(post, lang)
        res[fname] = out
        if stage:
            p = os.path.join(stage, lang, fname)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, 'w', encoding='utf-8', newline='').write(out)
        if apply:
            open(path, 'w', encoding='utf-8', newline='').write(out)
    build_lang.upper = upper
    return res, names


def sync_names(lang, names, upper, apply=False, log=print):
    """Название страниц (код/глава → имя из печати) в сайдбаре, оглавлении, «назад/вперёд», крошках, mundericat;
    имя автора — во всех страницах языка (в т.ч. не пересобираемых: index, mundericat, словари, перенаправления)."""
    d = BOOK if lang == 'az' else os.path.join(BOOK, lang)
    rx_row = re.compile(r'(<a class="bk-row[^"]*" href=")([^"#]+)("[^>]*><span class="bk-row__n">[^<]*</span><span class="bk-row__t">)([^<]*)(</span>)')
    rx_toc = re.compile(r'(<a class="bk-toc__a" href=")([^"#]+)("[^>]*>\s*<span class="bk-toc__n">[^<]*</span>\s*<span class="bk-toc__t">)([^<]*)(</span>)')
    rx_pn = re.compile(r'(<a class="bk-pn__a" href=")([^"#]+)(">\s*<span class="bk-pn__dir">[^<]*</span>\s*<span class="bk-pn__t">)([^<]*)(</span>)')
    rx_cr = re.compile(r'(<nav class="bk-crumb"[^>]*>\s*<a href=")([^"#]+)(">)([^<]*)(</a>)')
    rx_tc = re.compile(r'(<a href=")([0-9A-Z]{4}\.html)("><span class="sc">[^<]*</span><span>)([^<]*)(</span></a>)')
    rx_ch = re.compile(r'(<a href=")(\d\d-[^"#]+\.html)("><span class="tc-range">[^<]*</span><span>)([^<]*)(</span></a>)')
    changed = 0
    for f in sorted(glob.glob(os.path.join(d, '*.html'))):
        t = open(f, encoding='utf-8').read()
        o = t

        def mk(table):
            def r(m):
                new = table.get(m.group(2))
                return m.group(1) + m.group(2) + m.group(3) + (esc(new) if new else m.group(4)) + m.group(5)
            return r
        for rx in (rx_row, rx_toc, rx_pn, rx_cr):
            t = rx.sub(mk(names), t)
        t = rx_tc.sub(mk(upper), t)
        t = rx_ch.sub(mk(names), t)
        t = fix_author(t, lang)
        if t != o:
            changed += 1
            if apply:
                open(f, 'w', encoding='utf-8', newline='').write(t)
    log(lang, 'синхронизация названий/автора: изменено страниц', changed)


def fix_author(s, lang):
    a = AUTHOR[lang]
    if lang != 'az':
        nm = a.get('ld') or a['full']
        s = re.sub(r'("author":\s*\{"@type":\s*"Person",\s*"name":\s*")[^"]*(")', lambda m: m.group(1) + nm + m.group(2), s)
    for old, new in OLD_AUTHOR[lang]:
        s = s.replace(old, new)
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lang', action='append')
    ap.add_argument('--page', action='append', help='код/имя страницы без .html')
    ap.add_argument('--stage')
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--names-only', action='store_true', help='только названия/автор, без пересборки тел')
    a = ap.parse_args()
    for lang in a.lang or LANGS:
        full = not a.page
        res, names = build_lang(lang, only=set(a.page) if a.page else None, stage=a.stage, apply=(a.apply and not a.names_only))
        print(lang, 'страниц', len(res))
        if full and (a.apply or a.names_only):
            sync_names(lang, names, build_lang.upper, apply=True)


if __name__ == '__main__':
    main()
