# -*- coding: utf-8 -*-
"""Книга «Клиническая психиатрия» на сайте из итоговых версий базы истины (13.11.2026).

Источник текста — блоки итоговых версий (выгрузка D:\\Projects\\Psychiatry\\versions\\2026-11-13_b5\\b<id>.json: AZ_v25 1254,
RU_v48 1255, EN_v36 1256, TR_v46 1257; то же, что печатный Word). Блоки: заголовки (heading 1-4), абзацы, пункты списков, ячейки таблиц
(tbl, r, c), форматирование (b/i). Номера списков берутся из numbering.xml печатного Word.

Устройство сайта сохраняется (books/klinik-psixiatriya/<язык>/NNN.html + book.json: toc, trees):
  - порядок страниц: 4 вводные (index, kitab-haqqinda, mugeddime, mundericat) -> по главам: страница главы + карточки расстройств
    (по порядку печатной книги) -> 6 страниц приложений (elave-skalalar, elave-acde, yekun, melumat, terminoloji-luget, abbreviatur);
  - адреса страниц (p=<id>) прежние: id карточки — код МКБ-11 (6A04), id главы — прежний слаг (01-6A0-neyroinkisaf);
  - якоря: заголовки разделов карточек — <код>-<номер>-<слаг> (слаги прежние), остальные — слаг азербайджанского заголовка того же блока;
  - разметка как раньше: table.bk-codes (МКБ-10/DSM), nav.page-toc, h2/h3/h4, ol.method-num (8.2), ol.ref-list (Источники), div.tbl-wrap;
  - index, terminoloji-luget, abbreviatur и сайтовые вводные части melumat в печати отсутствуют — берутся из прежней копии без изменений;
  - mundericat: панель МКБ-11 пересобирается, панели DSM и МКБ-10 обновляются по названиям и кодам из базы.
Прежняя папка сохранена: _agent/klinik_before_db_20261113 (источник прежних страниц). Запуск: python -X utf8 _tools/build_klinik_db.py [--dry]
Файлы записываются через временный файл + os.replace; лишние прежние NNN.html (если страниц стало меньше) переименовываются в .old."""
import io, os, re, sys, json, time, copy, zipfile, html as H
from lxml import etree
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BID = "klinik-psixiatriya"
OUT = os.path.join(D, "books", BID)
OLD = os.path.join(D, "_agent", "klinik_before_db_20261113")
BLK = r"D:\Projects\Psychiatry\versions\2026-11-13_b5"
PRINT = r"D:\Projects\Psychiatry\Print"
LANGS = ["az", "ru", "en", "tr"]
VER = {"az": (1254, "AZ_v25"), "ru": (1255, "RU_v48"), "en": (1256, "EN_v36"), "tr": (1257, "TR_v46")}
DRY = "--dry" in sys.argv
WNS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
FRONT = ["index", "kitab-haqqinda", "mugeddime", "mundericat"]
BACK = ["elave-skalalar", "elave-acde", "yekun", "melumat", "terminoloji-luget", "abbreviatur"]
PRINT_LBL = {"az": "B5 · %d səh.", "ru": "B5 · %d стр.", "en": "B5 · %d pp."}

stats = {"written": 0, "unchanged": 0, "warn": []}


def warn(m):
    stats["warn"].append(m)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path) and io.open(path, encoding="utf-8", newline="").read() == text:
        stats["unchanged"] += 1
        return
    if DRY:
        return
    tmp = path + ".tmp"
    for _ in range(8):
        try:
            io.open(tmp, "w", encoding="utf-8", newline="\n").write(text)
            os.replace(tmp, path)
            stats["written"] += 1
            return
        except OSError:
            time.sleep(1.5)
    raise SystemExit("не записан: " + path)


# ---------- чтение блоков ----------
def M(b):
    m = dict(b.get("pmeta") or {})
    m.update(b.get("meta") or {})
    return m


def load_blocks(lang):
    return json.load(open(os.path.join(BLK, "b%d.json" % VER[lang][0]), encoding="utf-8"))


def numbering(lang):
    """numId -> {ilvl: numFmt} из печатного Word."""
    p = os.path.join(PRINT, "Klinik_Psixiatriya_%s.docx" % VER[lang][1])
    root = etree.fromstring(zipfile.ZipFile(p).read("word/numbering.xml"))
    absf = {}
    for a in root.findall(WNS + "abstractNum"):
        d = {}
        for l in a.findall(WNS + "lvl"):
            nf = l.find(WNS + "numFmt")
            d[int(l.get(WNS + "ilvl"))] = nf.get(WNS + "val") if nf is not None else "bullet"
        absf[a.get(WNS + "abstractNumId")] = d
    res = {}
    for n in root.findall(WNS + "num"):
        ab = n.find(WNS + "abstractNumId").get(WNS + "val")
        res[n.get(WNS + "numId")] = absf.get(ab, {})
    return res


def ppr_list(b):
    pp = M(b).get("ppr") or ""
    n = re.search(r'<w:numId w:val="(\d+)"', pp)
    l = re.search(r'<w:ilvl w:val="(\d+)"', pp)
    return (n.group(1) if n else None), (int(l.group(1)) if l else 0)


def esc(t):
    return H.escape(t, quote=False)


def inline(text, fmt, strip_b=False):
    """текст + форматирование [[start,end,kind]] -> html"""
    if not text:
        return ""
    marks = {"b": [0] * (len(text) + 1), "i": [0] * (len(text) + 1)}
    for f in (fmt or []):
        s, e, k = f[0], f[1], f[2]
        if k in marks and not (strip_b and k == "b"):
            for x in range(max(0, s), min(len(text), e)):
                marks[k][x] = 1
    out, cur = [], {"b": 0, "i": 0}
    for x, ch in enumerate(text):
        for k, tag in (("b", "strong"), ("i", "em")):
            want = marks[k][x]
            if want != cur[k]:
                out.append("<%s>" % tag if want else "</%s>" % tag)
                cur[k] = want
        out.append(esc(ch) if ch not in "\n\t\x0b" else ("<br>" if ch in "\n\x0b" else " "))
    for k, tag in (("i", "em"), ("b", "strong")):
        if cur[k]:
            out.append("</%s>" % tag)
    s = "".join(out)
    s = re.sub(r"<(strong|em)>(\s*)</\1>", r"\2", s)
    return s


def plain(b):
    return re.sub(r"\s+", " ", b["text"]).strip()


def slug(t):
    s = re.sub(r"[^\w\s-]", "", t.lower())
    s = re.sub(r"\s+", "-", s.strip())
    return s[:70].strip("-")


# ---------- блоки -> html ----------
class Ctx:
    def __init__(self, lang, nums, aztext):
        self.lang, self.nums, self.az, self.used = lang, nums, aztext, set()

    def hid(self, b, fixed=None):
        if fixed:
            base = fixed
        else:
            src = self.az.get(b["id"], b["text"])
            base = slug(src) or "s"
        i, hid = 1, base
        while hid in self.used:
            i += 1
            hid = "%s-%d" % (base, i)
        self.used.add(hid)
        return hid


def table_html(cells, hdr_plain=True):
    """cells: список блоков одной таблицы"""
    rows = {}
    for b in cells:
        m = M(b)
        rows.setdefault(m["r"], {}).setdefault(m["c"], []).append(b)
    out = ['<div class="tbl-wrap"><table>']
    for r in sorted(rows):
        first = next(iter(rows[r].values()))[0]
        is_h = "tblHeader" in (M(first).get("trpr") or "")
        out.append("<tr>")
        for c in sorted(rows[r]):
            bl = rows[r][c]
            tcpr = M(bl[0]).get("tcpr") or ""
            gs = re.search(r'gridSpan w:val="(\d+)"', tcpr)
            attr = ' colspan="%s"' % gs.group(1) if gs else ""
            if 'vMerge w:val="restart"' in tcpr:
                warn("vMerge в таблице (rowspan не строится): %s" % bl[0]["id"])
            tag = "th" if is_h else "td"
            body = "<br>".join(inline(x["text"], x.get("fmt"), strip_b=is_h) for x in bl)
            out.append("<%s%s>%s</%s>" % (tag, attr, body, tag))
        out.append("</tr>")
    out.append("</table></div>")
    return "\n".join(out)


def blocks_html(blocks, ctx, hmap, code=None, card=False, skip_first_h1=False):
    """Преобразование последовательности блоков в html.
    hmap: стиль заголовка -> тег (heading 3 -> h2 для карточек и т.п.). Возвращает (html, список (id, текст) для page-toc)."""
    out, toc = [], []
    i, n = 0, len(blocks)
    cur_h = ""
    while i < n:
        b = blocks[i]
        k, st = b["kind"], M(b).get("style")
        if k == "heading":
            tag = hmap.get(st)
            if tag is None:
                i += 1
                continue
            text = plain(b)
            fixed = None
            mnum = re.match(r"^(\d+)\.\s+", text)
            if card and st == "heading 3" and mnum and code:
                fixed = ctx.sec_ids.get(int(mnum.group(1)))
            hid = ctx.hid(b, fixed)
            cls = ' class="h-section"' if (ctx.hsec and st == "heading 1") else ""
            out.append('<%s%s id="%s">%s</%s>' % (tag, cls, hid, inline(b["text"], None), tag))
            if tag == "h2":
                label = re.sub(r"^\d+\.\s+", "", text) if card else text
                toc.append((hid, label))
            cur_h = text
            i += 1
        elif k == "list_item":
            j = i
            while j < n and blocks[j]["kind"] == "list_item":
                j += 1
            out.append(list_html(blocks[i:j], ctx, cur_h, card))
            i = j
        elif k == "table_cell":
            t = M(b)["tbl"]
            j = i
            while j < n and blocks[j]["kind"] == "table_cell" and M(blocks[j])["tbl"] == t:
                j += 1
            out.append(table_html(blocks[i:j]))
            i = j
        elif k == "body":
            if st == "Definition Term":
                j = i
                dl = ["<dl>"]
                while j < n and blocks[j]["kind"] == "body" and M(blocks[j]).get("style") in ("Definition Term", "Definition"):
                    tg = "dt" if M(blocks[j]).get("style") == "Definition Term" else "dd"
                    dl.append("<%s>%s</%s>" % (tg, inline(blocks[j]["text"], blocks[j].get("fmt")), tg))
                    j += 1
                dl.append("</dl>")
                out.append("\n".join(dl))
                i = j
                continue
            if st == "Source Code":
                out.append("<pre>%s</pre>" % esc(b["text"]))
            else:
                out.append("<p>%s</p>" % inline(b["text"], b.get("fmt")))
            i += 1
        else:
            i += 1
    return "\n".join(out), toc


def list_html(items, ctx, cur_h, card):
    out, stack, cur_num = [], [], None
    prev_num = None

    def fmt_of(num, lvl):
        return (ctx.nums.get(num or "", {}) or {}).get(lvl, "bullet")

    def open_list(num, lvl):
        dec = fmt_of(num, lvl) not in ("bullet",) and fmt_of(num, lvl) != "none"
        cls = ""
        if dec and lvl == 0:
            if card and re.match(r"^8\.2\b", cur_h):
                cls = ' class="method-num"'
            elif card and ctx.in_sources:
                cls = ' class="ref-list"'
        tag = "ol" if dec else "ul"
        out.append("<%s%s>" % (tag, cls))
        stack.append(tag)

    for b in items:
        num, lvl = ppr_list(b)
        if num is None:
            num = prev_num
        if not stack:
            open_list(num, lvl)
            cur_num = num
            depth = 0
        else:
            if lvl == 0 and num != cur_num:
                while stack:
                    out[-1] += "</li>"
                    out.append("</%s>" % stack.pop())
                open_list(num, 0)
                cur_num = num
                depth = 0
            elif lvl > len(stack) - 1:
                while len(stack) - 1 < lvl:
                    open_list(num, len(stack))
                depth = lvl
            elif lvl < len(stack) - 1:
                while len(stack) - 1 > lvl:
                    out[-1] += "</li>"
                    out.append("</%s>" % stack.pop())
                out[-1] += "</li>"
                depth = lvl
            else:
                out[-1] += "</li>"
        out.append("<li>%s" % inline(b["text"], b.get("fmt")))
        prev_num = num
    while stack:
        out[-1] += "</li>"
        out.append("</%s>" % stack.pop())
    s = "\n".join(out)
    s = s.replace("<ul>\n</li>", "<ul>").replace("</li>\n<li>", "</li>\n<li>")
    return s


# ---------- разбор структуры книги ----------
def is_h1(b):
    return b["kind"] == "heading" and M(b).get("style") == "heading 1"


def parse(lang):
    blocks = load_blocks(lang)
    h1 = [k for k, b in enumerate(blocks) if is_h1(b) and b["kind"] != "toc"]
    return blocks, h1


def split_book(blocks, h1):
    """-> dict с диапазонами: front (список H1-разделов), groups (главы с карточками), appendix."""
    texts = [plain(blocks[k]) for k in h1]
    ids = [blocks[k]["id"] for k in h1]
    secs = []
    for n, k in enumerate(h1):
        e = h1[n + 1] if n + 1 < len(h1) else len(blocks)
        secs.append((n, k, e))
    return secs


def parse_header(cells):
    rows = {}
    for b in cells:
        m = M(b)
        rows.setdefault(m["r"], {}).setdefault(m["c"], []).append(b)
    r0 = {c: v[0] for c, v in rows[0].items()}
    c0 = r0[0]["text"].split("\n")
    code = c0[1].strip() if len(c0) > 1 else c0[0].strip()
    title = plain(r0[1]) if 1 in r0 else ""
    en = plain(rows[0][1][1]) if len(rows[0].get(1, [])) > 1 else (plain(r0[2]) if 2 in r0 else "")
    others = []
    for r in sorted(rows):
        if r == 0:
            continue
        a = rows[r][0][0] if 0 in rows[r] else None
        nm = rows[r][1][0] if 1 in rows[r] else None
        if a is None:
            continue
        parts = a["text"].split("\n")
        others.append((parts[0].strip(), parts[1].strip() if len(parts) > 1 else "", plain(nm) if nm else ""))
    return {"code": code, "title": title, "en": en, "others": others, "lbl0": c0[0].strip() if len(c0) > 1 else ""}


def cards_of(blocks, s, e):
    """Глава блоков [s,e): возвращает (intro_blocks, [card...]) ; card = dict(head, body)."""
    starts = []
    i = s
    while i < e:
        b = blocks[i]
        if b["kind"] == "table_cell" and M(b).get("style") == "heading 2":
            t = M(b)["tbl"]
            j = i
            while j > s and blocks[j - 1]["kind"] == "table_cell" and M(blocks[j - 1]).get("tbl") == t:
                j -= 1
            k = i
            while k < e and blocks[k]["kind"] == "table_cell" and M(blocks[k]).get("tbl") == t:
                k += 1
            starts.append((j, k))
            i = k
        else:
            i += 1
    intro = blocks[s + 1: starts[0][0] if starts else e]
    cards = []
    for n, (hs, he) in enumerate(starts):
        be = starts[n + 1][0] if n + 1 < len(starts) else e
        cards.append({"head": parse_header(blocks[hs:he]), "body": blocks[he:be], "hid": blocks[hs]["id"]})
    return intro, cards


def card_id(code):
    m = re.match(r"^([0-9A-Z]{4})", code)
    return m.group(1) if m else code


def old_page(lang, name_or_n):
    return io.open(os.path.join(OLD, lang, name_or_n), encoding="utf-8").read()


CODEPFX = re.compile(r"^[0-9A-Z]{4}(?:\.\d+)?(?:\s*[–-]\s*[0-9A-Z]{4}(?:\.\d+)?)?\s+")
LOC = {"lang": "ru"}


def lower_loc(s):
    if LOC["lang"] in ("az", "tr"):
        s = s.replace("İ", "i").replace("I", "ı")
    return s.lower()


def norm(s):
    return re.sub(r"[̇\s]+", " ", lower_loc(s).replace("ı", "i")).strip()


def sentence_case(db, old):
    """Название из заголовка в верхнем регистре -> как на сайте: совпало с прежним без учёта регистра — прежнее; иначе строчные, кроме аббревиатур."""
    db = CODEPFX.sub("", db)
    if old and norm(db) == norm(old):
        return old
    oldw = set(re.findall(r"[\w-]+", old or ""))
    outw = []
    for w in re.split(r"(\s+)", db):
        core = re.sub(r"^\W+|\W+$", "", w)
        if core and core.isupper() and (core in oldw or (w.startswith("(") and len(core) >= 2 and core.isascii())):
            outw.append(w)
        else:
            outw.append(lower_loc(w))
    s = "".join(outw)
    return s[:1].upper() + s[1:] if s[:1] != "i" else "İ" + s[1:] if LOC["lang"] in ("az", "tr") else s[:1].upper() + s[1:]


def main():
    oldbook = json.load(open(os.path.join(OLD, "book.json"), encoding="utf-8"))
    P = copy.deepcopy(oldbook)
    old_toc = {l: oldbook["toc"][l] for l in LANGS}
    old_ids = [x["id"] for x in old_toc["ru"]]
    old_idx = {l: {x["id"]: n + 1 for n, x in enumerate(old_toc[l])} for l in LANGS}
    old_t = {l: {x["id"]: x for x in old_toc[l]} for l in LANGS}
    # id глав — прежние слаги по порядку
    group_ids = [x["id"] for x in old_toc["ru"] if x["lvl"] == 0 and x["id"] not in FRONT + BACK]
    data = {l: parse(l) for l in LANGS}
    # --- азербайджанские тексты заголовков по id блока (якоря общие для языков)
    aztext = {b["id"]: plain(b) for b in data["az"][0] if b["kind"] == "heading" or (b["kind"] == "table_cell" and M(b).get("style") == "heading 2")}
    # --- старые якоря разделов карточек (номер -> id) по азербайджанским страницам
    sec_old = {}
    for pid in old_ids:
        if re.match(r"^[0-9A-Z]{4}$", pid):
            s = old_page("az", "%03d.html" % old_idx["az"][pid])
            sec_old[pid] = {int(m.group(2)): m.group(0)[len('<h2 id="'):-2] if False else "%s-%s-%s" % (m.group(1), m.group(2), m.group(3)) for m in re.finditer(r'<h2 id="([0-9a-z]{4})-(\d+)-([^"]+)"', s)}
    toc_new = {}
    pages = {l: {} for l in LANGS}   # l -> id -> html
    tocs = {l: [] for l in LANGS}
    infos = {}
    for lang in LANGS:
        blocks, h1 = data[lang]
        nums = numbering(lang)
        secs = split_book(blocks, h1)
        names = [plain(blocks[k]) for _, k, _ in secs]
        # границы: первая глава с карточками, приложения
        first_dis = next(n for n, (_, k, e) in enumerate(secs) if re.match(r"^6A00", names[n]))
        app_start = next(n for n, nm in enumerate(names) if n > first_dis and re.match(r"^(ПРИЛОЖЕНИЯ|APPENDICES|EKLER|ƏLAVƏLƏR)$", nm, re.I)) if True else None
        ctx = Ctx(lang, nums, aztext)
        ctx.hsec = False
        ctx.in_sources = False
        ctx.sec_ids = {}

        def conv(bl, hmap, **kw):
            return blocks_html(bl, ctx, hmap, **kw)

        # -- вводная часть: разделы 0..first_dis-1
        front_secs = secs[:first_dis]
        # какие из front относятся к melumat: ВВЕДЕНИЕ В ПСИХОПАТОЛОГИЮ, КЛИНИЧЕСКОЕ ИНТЕРВЬЮ, ПРАВОВЫЕ (по номеру 649/813/1001 -> позиции в списке)
        # определяем по порядку: в печати подряд идут после «ГЛОБАЛЬНЫЙ КРИЗИС»
        melum_idx = [n for n, (_, k, e) in enumerate(front_secs) if blocks[k]["id"] in MELUM_IDS]
        if len(melum_idx) != 3:
            raise SystemExit("[%s] не найдены три раздела для melumat: %s" % (lang, melum_idx))
        preface = front_secs[0]
        intro_n = 1  # «ВВЕДЕНИЕ» — раздел 1
        # kitab-haqqinda: раздел ВВЕДЕНИЕ без заголовка-названия
        ctx.used = set()
        sec_intro = front_secs[1]
        html2, _ = conv(blocks[sec_intro[1] + 1: sec_intro[2]], {"heading 2": "h2", "heading 3": "h3", "heading 4": "h4"})
        # mugeddime
        ctx.used = set()
        parts = []
        html3, _ = conv(blocks[preface[1] + 1: preface[2]], {"heading 2": "h2", "heading 3": "h3", "heading 4": "h4"})
        parts.append(html3)
        for n, (_, k, e) in enumerate(front_secs[1:], 1):
            if n in melum_idx:
                continue
            h, _ = conv(blocks[k:e], {"heading 1": "h2", "heading 2": "h3", "heading 3": "h4", "heading 4": "h4"})
            parts.append(h)
        page3 = '<article class="front-page">\n' + "\n".join(parts) + "\n</article>"
        # melumat: прежняя сайтовая часть + три раздела из базы
        ctx.used = set()
        mel_html = []
        for n in melum_idx:
            _, k, e = front_secs[n]
            h, _ = conv(blocks[k:e], {"heading 1": "h2", "heading 2": "h3", "heading 3": "h4", "heading 4": "h4"})
            mel_html.append(h)
        oldm = old_page(lang, "%03d.html" % old_idx[lang]["melumat"])
        hs = [m.start() for m in re.finditer(r"<h2[ >]", oldm)]
        head_end = hs[3] if len(hs) > 3 else len(oldm)
        mhead = oldm[:head_end]
        mhead = re.sub(r'<nav class="page-toc">.*?</nav>\s*', "", mhead, flags=re.S)
        body_m = mhead + "\n".join(mel_html)
        tocm = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body_m, flags=re.S)
        nav = '<nav class="page-toc">' + "".join('<a href="#%s">%s</a>' % (a, re.sub(r"<[^>]+>", "", t)) for a, t in tocm) + "</nav>\n"
        mm = re.match(r"^(<p class=\"bk-chead__sub\">.*?</p>\s*)", body_m, flags=re.S)
        body_m = (mm.group(1) + nav + body_m[mm.end():]) if mm else nav + body_m
        # page 2: nav
        tocs2 = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', html2, flags=re.S)
        page2 = '<nav class="page-toc">' + "".join('<a href="#%s">%s</a>' % (a, re.sub(r"<[^>]+>", "", t)) for a, t in tocs2) + "</nav>\n" + html2
        pages[lang]["kitab-haqqinda"] = page2
        pages[lang]["mugeddime"] = page3
        pages[lang]["melumat"] = body_m
        pages[lang]["index"] = old_page(lang, "%03d.html" % old_idx[lang]["index"]).rstrip("\n")
        for nm in ("terminoloji-luget", "abbreviatur"):
            pages[lang][nm] = old_page(lang, "%03d.html" % old_idx[lang][nm]).rstrip("\n")
        # -- главы и карточки
        glist = []
        for n in range(first_dis, app_start):
            _, k, e = secs[n]
            intro, cards = cards_of(blocks, k, e)
            gtitle = plain(blocks[k])
            mcode = re.match(r"^(\S+(?:\s·\s\S+)?)\s+(.*)$", gtitle)
            gcode, gname = (mcode.group(1), mcode.group(2)) if mcode else ("", gtitle)
            gen = plain(intro[0]) if intro and intro[0]["kind"] == "body" else ""
            glist.append({"code": gcode, "name": gname, "en": gen, "cards": cards})
        if len(glist) != len(group_ids):
            raise SystemExit("[%s] глав %d, ожидалось %d" % (lang, len(glist), len(group_ids)))
        for gi, g in enumerate(glist):
            g["id"] = group_ids[gi]
            for c in g["cards"]:
                c["id"] = card_id(c["head"]["code"])
        # карточки
        for g in glist:
            for c in g["cards"]:
                pid = c["id"]
                ctx.used = set()
                ctx.sec_ids = sec_old.get(pid, {})
                ctx.in_sources = False
                body = c["body"]
                # метки «Источники»: последний раздел карточки (heading 3 с номером, наибольшим)
                last_src = None
                for bi, b in enumerate(body):
                    if b["kind"] == "heading" and M(b).get("style") == "heading 3" and re.match(r"^\d+\.", plain(b)):
                        last_src = bi
                # отрисовка с признаком источников
                htm, toc = [], []
                seg_idx = [bi for bi, b in enumerate(body) if b["kind"] == "heading" and M(b).get("style") == "heading 3"]
                cut = seg_idx[-1] if seg_idx else None
                if cut is not None:
                    h1_, t1 = blocks_html(body[:cut], ctx, {"heading 3": "h2", "heading 4": "h3"}, code=pid.lower(), card=True)
                    ctx.in_sources = True
                    h2_, t2 = blocks_html(body[cut:], ctx, {"heading 3": "h2", "heading 4": "h3"}, code=pid.lower(), card=True)
                    ctx.in_sources = False
                    htm, toc = [h1_, h2_], t1 + t2
                else:
                    h1_, toc = blocks_html(body, ctx, {"heading 3": "h2", "heading 4": "h3"}, code=pid.lower(), card=True)
                    htm = [h1_]
                hd = c["head"]
                bk = '<table class="bk-codes"><tbody>' + "".join(
                    '<tr><td class="dh-meta"><span class="dh-lbl">%s</span><span class="dh-code">%s</span></td><td class="dh-name">%s</td></tr>' % (esc(a), esc(b_), esc(cn))
                    for a, b_, cn in hd["others"]) + "</tbody></table>\n"
                nav = '<nav class="page-toc">' + "".join('<a href="#%s">%s</a>' % (a, esc(t)) for a, t in toc) + "</nav>\n"
                pages[lang][pid] = bk + nav + "\n".join(x for x in htm if x)
        # приложения
        ctx.hsec = True
        sapp = {plain(blocks[k]): (k, e) for _, k, e in secs[app_start:]}
        order_app = [(plain(blocks[k]), k, e) for _, k, e in secs[app_start:]]
        # Б
        def find(prefix_re):
            return [(t, k, e) for t, k, e in order_app if re.match(prefix_re, t, re.I)]
        # ПРИЛОЖЕНИЕ А/Б/В/Г/Д (и переводы) — по порядку в печати: А, Б, В, Г, Д, ОБЩИЕ ИСТОЧНИКИ, ИТОГОВЫЕ
        rest = order_app[1:]
        if len(rest) != 7:
            raise SystemExit("[%s] разделов приложений %d, ожидалось 7: %s" % (lang, len(rest), [t for t, _, _ in rest]))
        hm = {"heading 1": "h2", "heading 2": "h2", "heading 3": "h3", "heading 4": "h4"}
        ctx.used = set()
        pb, _ = conv(blocks[rest[1][1]: rest[1][2]], hm)
        pages[lang]["elave-skalalar"] = pb
        ctx.used = set()
        pa = []
        for idx in (0, 2, 3, 4, 5):
            h, _ = conv(blocks[rest[idx][1]: rest[idx][2]], hm)
            pa.append(h)
        pages[lang]["elave-acde"] = "\n".join(pa)
        ctx.used = set()
        ctx.hsec = False
        py, _ = conv(blocks[rest[6][1] + 1: rest[6][2]], {"heading 2": "h2", "heading 3": "h3", "heading 4": "h4"})
        pages[lang]["yekun"] = py
        infos[lang] = glist
    # ---------- общая сборка ----------
    totals = {}
    for lang in LANGS:
        LOC["lang"] = lang
        glist = infos[lang]
        order = list(FRONT)
        gpage = {}
        for g in glist:
            order.append(g["id"])
            order += [c["id"] for c in g["cards"]]
        order += BACK
        # страница mundericat и страницы глав — ниже
        ot = old_t[lang]
        disord = set(c["id"] for g in glist for c in g["cards"])
        # страницы глав
        for g in glist:
            old_g = ot[g["id"]]
            oldp = old_page(lang, "%03d.html" % old_idx[lang][g["id"]])
            sub = re.search(r'<p class="bk-chead__sub">(.*?)</p>', oldp, flags=re.S)
            subtxt = sub.group(1) if sub else ""
            lis = []
            for c in g["cards"]:
                ct = sentence_case(c["head"]["title"], ot.get(c["id"], {}).get("t", ""))
                c["t"] = ct
                lis.append('<li class="bk-toc__row">\n<a class="bk-toc__a" href="read.html?b=%s&amp;p=%s">\n<span class="bk-toc__n">%s</span>\n<span class="bk-toc__t">%s</span>\n</a>\n</li>' % (BID, c["id"], esc(c["head"]["code"]), esc(ct)))
            pages[lang][g["id"]] = '<p class="bk-chead__sub">%s</p>\n<ul class="bk-toc__list">\n%s\n</ul>' % (subtxt, "\n".join(lis))
            g["t"] = old_g["t"]
        # дерево и toc
        toc = []
        for pid in order:
            old_i = ot.get(pid)
            body = pages[lang].get(pid)
            if pid == "mundericat":
                continue
            toc.append(pid)
        # mundericat (после того как знаем названия)
        pages[lang]["mundericat"] = build_mundericat(lang, old_page(lang, "%03d.html" % old_idx[lang]["mundericat"]), glist, oldbook["trees"][lang])
        # ссылки внутри страниц: нет (в базе их нет)
        tl = []
        gset = set(g["id"] for g in glist)
        for pid in order:
            body = pages[lang][pid].rstrip("\n") + "\n"
            pages[lang][pid] = body
            o = ot.get(pid, {})
            item = {"t": o.get("t", pid), "n": len(re.sub(r"<[^>]+>", "", body)), "id": pid, "lvl": 1 if pid in disord else 0, "code": o.get("code", "")}
            if pid in disord:
                c = next(c for g in glist for c in g["cards"] if c["id"] == pid)
                item["t"] = c["t"]
                item["code"] = c["head"]["code"]
                en = CODEPFX.sub("", c["head"]["en"])
                if en and en.lower() != item["t"].lower():
                    item["en"] = en
            elif pid in gset:
                g = next(g for g in glist if g["id"] == pid)
                item["t"] = g["t"]
                item["code"] = g["code"]
                if g["en"] and g["en"].lower() != item["t"].lower():
                    item["en"] = g["en"]
                if o.get("sub"):
                    item["sub"] = o["sub"]
            else:
                if o.get("en"):
                    item["en"] = o["en"]
                if o.get("sub"):
                    item["sub"] = o["sub"]
            tl.append(item)
        P["toc"][lang] = tl
        # деревья
        P["trees"][lang] = build_trees(lang, oldbook["trees"][lang], glist)
        nch, ndis = len(glist), sum(len(g["cards"]) for g in glist)
        meta = P["meta"][lang]
        meta[4][1] = str(nch)
        meta[5][1] = str(ndis)
        pf = os.path.join(BLK, "Klinik_Psixiatriya_%s_pages_final.json" % VER[lang][1])
        if lang in PRINT_LBL and os.path.exists(pf):
            meta[3][1] = PRINT_LBL[lang] % json.load(open(pf, encoding="utf-8"))["total_pages"]
        totals[lang] = (len(tl), nch, ndis)
        # запись страниц
        d = os.path.join(OUT, lang)
        for n, pid in enumerate(order, 1):
            write(os.path.join(d, "%03d.html" % n), pages[lang][pid])
        for f in os.listdir(d):
            m = re.match(r"^(\d{3})\.html$", f)
            if m and int(m.group(1)) > len(order) and not DRY:
                os.replace(os.path.join(d, f), os.path.join(d, f + ".old"))
        print("[%s] страниц %d, глав %d, расстройств %d" % (lang, len(tl), nch, ndis))
    base = [x["id"] for x in P["toc"]["az"]]
    for l in LANGS[1:]:
        if [x["id"] for x in P["toc"][l]] != base:
            warn("порядок id в %s отличается от az" % l)
    write(os.path.join(OUT, "book.json"), json.dumps(P, ensure_ascii=False, indent=1) + "\n")
    print("записано: %d, без изменений: %d" % (stats["written"], stats["unchanged"]))
    for w in stats["warn"][:30]:
        print("ПРЕДУПРЕЖДЕНИЕ:", w)
    print("предупреждений всего:", len(stats["warn"]))


MELUM_IDS = None


def build_trees(lang, oldtree, glist):
    T = copy.deepcopy(oldtree)
    icd = []
    code_of = {}
    for g in glist:
        items = []
        for c in g["cards"]:
            items.append({"t": c["t"], "code": c["head"]["code"], "id": c["id"]})
        icd.append({"t": g["t"], "code": g["code"], "items": items, "id": g["id"]})
        for c in g["cards"]:
            code_of[c["id"]] = {a: b for a, b, _ in c["head"]["others"]}
    T["icd"] = icd
    tit = {c["id"]: c["t"] for g in glist for c in g["cards"]}
    lbl = {}
    for g in glist:
        for c in g["cards"]:
            for a, b_, _ in c["head"]["others"]:
                lbl.setdefault(c["id"], []).append((a, b_))
    for key, pat in (("dsm", r"DSM"), ("icd10", r"(МКБ|XBT|ICD|İCD)-?10")):
        for grp in T[key]:
            for it in grp["items"]:
                pid = it["id"]
                if pid in tit:
                    it["t"] = tit[pid]
                    for a, b_ in lbl.get(pid, []):
                        if re.search(pat, a, re.I) and b_ and b_ != "—":
                            it["code"] = b_
    return T


def build_mundericat(lang, old, glist, oldtree):
    s = BeautifulSoup(old, "html.parser")
    ndis = sum(len(g["cards"]) for g in glist)
    tit = {c["id"]: c["head"]["title"] for g in glist for c in g["cards"]}
    lbl = {}
    for g in glist:
        for c in g["cards"]:
            lbl[c["id"]] = c["head"]["others"]
    # панель МКБ-11
    panel = s.select_one('.cls-panel[data-cls="icd"]')
    frag = []
    for g in glist:
        a = '<div class="toc-ch"><a href="read.html?b=%s&amp;p=%s"><span class="tc-range">%s</span><span>%s</span></a><div class="tc-list">' % (BID, g["id"], esc(g["code"]), esc(g["t"]))
        for c in g["cards"]:
            a += '<a href="read.html?b=%s&amp;p=%s"><span class="sc">%s</span><span>%s</span></a>' % (BID, c["id"], esc(c["head"]["code"]), esc(c["head"]["title"]))
        a += "</div></div>"
        frag.append(a)
    endch = [str(x) for x in panel.select(".toc-ch") if x.select_one(".tc-empty")]
    frag += endch
    meta_txt = panel.select_one(".toc-meta").get_text()
    meta_new = re.sub(r"\d+", "%d", meta_txt, count=2) % (ndis, len(glist))
    newp = BeautifulSoup('<div class="cls-panel" data-cls="icd"><p class="toc-meta">%s</p><div class="toc-preview">%s</div></div>' % (esc(meta_new), "".join(frag)), "html.parser")
    panel.replace_with(newp.div)
    for key, pat in (("dsm", r"DSM"), ("icd10", r"(МКБ|XBT|ICD|İCD)-?10")):
        pn = s.select_one('.cls-panel[data-cls="%s"]' % key)
        for a in pn.select(".tc-list a"):
            m = re.search(r"[?&]p=([^&#]+)", a["href"])
            pid = m.group(1) if m else ""
            if pid in tit:
                spans = a.find_all("span")
                spans[1].string = tit[pid]
                for lb, cd, _ in lbl.get(pid, []):
                    if re.search(pat, lb, re.I) and cd and cd != "—":
                        spans[0].string = cd
        mt = pn.select_one(".toc-meta")
        if mt:
            mt.string = re.sub(r"\d+", str(ndis), mt.get_text(), count=1)
    return s.decode(formatter="html5") if False else str(s)


if __name__ == "__main__":
    # три раздела печати, которые на сайте стоят на странице melumat: по id заголовков (общие для языков)
    _b = load_blocks("ru")
    MELUM_IDS = set(b["id"] for b in _b if is_h1(b) and plain(b) in ("ВВЕДЕНИЕ В ПСИХОПАТОЛОГИЮ", "КЛИНИЧЕСКОЕ ИНТЕРВЬЮ И ОЦЕНКА ПСИХИЧЕСКОГО СТАТУСА", "ПРАВОВЫЕ И ЭТИЧЕСКИЕ АСПЕКТЫ"))
    if len(MELUM_IDS) != 3:
        raise SystemExit("не найдены три раздела melumat")
    main()
