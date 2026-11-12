# -*- coding: utf-8 -*-
"""Сборка KPT_programma.docx и KPT_programma.pptx из kpt_data.py одним запуском."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

from pptx import Presentation
from pptx.dml.color import RGBColor as PRGB
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt as PPt, Emu

import kpt_data as D

NAVY = "14213D"
GOLD = "C9A227"
CREAM = "F7F4EE"

STAGES = [
    ("0:00-0:10", "Проверка домашнего задания", 10, "check"),
    ("0:10-0:35", "Теория", 25, "theory"),
    ("0:35-0:50", "Демонстрация", 15, "demo"),
    ("0:50-1:15", "Практика в парах и тройках", 25, "practice"),
    ("1:15-1:25", "Разбор", 10, "debrief"),
    ("1:25-1:30", "Домашнее задание", 5, None),
]
HW_TEXT = "Постановка домашнего задания (см. раздел «Домашнее задание слушателю»), проверка понимания, репетиция первого шага."

MOD_BY_LESSON = {}
for m in D.MODULES:
    for n in range(m["lessons"][0], m["lessons"][1] + 1):
        MOD_BY_LESSON[n] = m


def week_of(n):
    return (n + 1) // 2


def lesson_range(m):
    a, b = m["lessons"]
    return f"{a}-{b}"


# ================================================================= DOCX
def set_run_font(run, name="Times New Roman", size=None, bold=None, italic=None, color=None):
    run.font.name = name
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.insert(0, rf)
    for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rf.set(qn(a), name)
    if size:
        run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def style_font(style, size, bold=False, color=None, italic=False):
    style.font.name = "Times New Roman"
    style.font.size = Pt(size)
    style.font.bold = bold
    style.font.italic = italic
    if color:
        style.font.color.rgb = RGBColor.from_string(color)
    rpr = style.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.insert(0, rf)
    for a in list(rf.attrib):
        del rf.attrib[a]
    for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rf.set(qn(a), "Times New Roman")


def shade(cell, hexcolor):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)


def thin_borders(table):
    tbl = table._element
    tblPr = tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "4")
        e.set(qn("w:space"), "0")
        e.set(qn("w:color"), "808080")
        b.append(e)
    tblPr.append(b)


def repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    h = OxmlElement("w:tblHeader")
    h.set(qn("w:val"), "true")
    trPr.append(h)


def no_split(row):
    trPr = row._tr.get_or_add_trPr()
    c = OxmlElement("w:cantSplit")
    c.set(qn("w:val"), "true")
    trPr.append(c)



def apply_widths(t, widths_cm):
    tblPr = t._element.tblPr
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    tblPr.append(lay)
    tw = tblPr.find(qn("w:tblW"))
    if tw is None:
        tw = OxmlElement("w:tblW")
        tblPr.append(tw)
    tw.set(qn("w:type"), "dxa")
    tw.set(qn("w:w"), str(int(sum(widths_cm) * 567)))
    grid = t._element.find(qn("w:tblGrid"))
    for i, gc in enumerate(grid.findall(qn("w:gridCol"))):
        gc.set(qn("w:w"), str(int(widths_cm[i] * 567)))
    for r in t.rows:
        for i, c in enumerate(r._tr.findall(qn("w:tc"))):
            pass
    for r in t.rows:
        cells = r._tr.findall(qn("w:tc"))
        if len(cells) == len(widths_cm):
            for i, tc in enumerate(cells):
                tcPr = tc.get_or_add_tcPr()
                w = tcPr.find(qn("w:tcW"))
                if w is None:
                    w = OxmlElement("w:tcW")
                    tcPr.insert(0, w)
                w.set(qn("w:type"), "dxa")
                w.set(qn("w:w"), str(int(widths_cm[i] * 567)))

def cell_text(cell, text, size=11, bold=False, italic=False, align=None):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.line_spacing = 1.0
    if align:
        p.alignment = align
    r = p.add_run(text)
    set_run_font(r, size=size, bold=bold, italic=italic)


def make_table(doc, header, rows, widths_cm, size=11, center_cols=()):
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    thin_borders(t)
    for i, h in enumerate(header):
        c = t.rows[0].cells[i]
        cell_text(c, h, size=size, bold=True)
        shade(c, "E4E7EE")
    repeat_header(t.rows[0])
    for row in rows:
        cells = t.add_row().cells
        no_split(t.rows[-1])
        for i, v in enumerate(row):
            cell_text(cells[i], v, size=size, align=WD_ALIGN_PARAGRAPH.CENTER if i in center_cols else None)
    apply_widths(t, widths_cm)
    sp = doc.add_paragraph()
    sp.paragraph_format.space_after = Pt(0)
    sp.paragraph_format.line_spacing = 0.6
    return t


def add_page_number(section):
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    set_run_font(run, size=11)
    for t, txt in (("begin", None), (None, "PAGE"), ("end", None)):
        if t:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), t)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = txt
        run._r.append(el)


def para(doc, text, bold=False, italic=False, size=12, align=None, after=4, before=0, indent=None, first=None, keep=False):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_after = Pt(after)
    pf.space_before = Pt(before)
    if indent is not None:
        pf.left_indent = Cm(indent)
    if first is not None:
        pf.first_line_indent = Cm(first)
    if align:
        p.alignment = align
    if keep:
        pf.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, size=size, bold=bold, italic=italic)
    return p


def bullets(doc, items, after=0.5):
    for it in items:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = Cm(0.9)
        pf.first_line_indent = Cm(-0.5)
        pf.space_after = Pt(after)
        r = p.add_run("•  " + it)
        set_run_font(r, size=12)


def numbered(doc, items):
    for i, it in enumerate(items, 1):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = Cm(1.1)
        pf.first_line_indent = Cm(-0.6)
        pf.space_after = Pt(1)
        r = p.add_run(f"{i}.  {it}")
        set_run_font(r, size=12)


def build_docx(path):
    doc = Document()
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.PORTRAIT
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, side, Cm(2.5))
    sec.footer_distance = Cm(1.2)
    sec.different_first_page_header_footer = True
    add_page_number(sec)

    st = doc.styles
    style_font(st["Normal"], 12)
    st["Normal"].paragraph_format.line_spacing = 1.0
    st["Normal"].paragraph_format.space_after = Pt(4)
    for name, size, before, after in (("Heading 1", 16, 0, 10), ("Heading 2", 14, 10, 4), ("Heading 3", 13, 6, 2)):
        s = st[name]
        style_font(s, size, bold=True, color=NAVY)
        s.paragraph_format.space_before = Pt(before)
        s.paragraph_format.space_after = Pt(after)
        s.paragraph_format.keep_with_next = True
        s.paragraph_format.line_spacing = 1.1

    # ---- титул
    for _ in range(4):
        doc.add_paragraph()
    para(doc, D.SCHOOL.upper(), bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
    para(doc, D.CITY, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, after=70)
    para(doc, "УЧЕБНАЯ ПРОГРАММА КУРСА", size=14, align=WD_ALIGN_PARAGRAPH.CENTER, after=14)
    para(doc, "«" + D.COURSE + "»", bold=True, size=26, align=WD_ALIGN_PARAGRAPH.CENTER, after=14)
    para(doc, "Первая основа КПТ и обзор современных направлений", italic=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, after=60)
    para(doc, "3 месяца обучения: 24 занятия, 48 академических часов", size=13, align=WD_ALIGN_PARAGRAPH.CENTER, after=3)
    para(doc, "6 месяцев групповой супервизии, одна встреча в неделю", size=13, align=WD_ALIGN_PARAGRAPH.CENTER, after=3)
    para(doc, "Документ по окончании: сертификат школы", size=13, align=WD_ALIGN_PARAGRAPH.CENTER, after=40)
    para(doc, "Ведущий курса: " + D.LEAD, size=13, align=WD_ALIGN_PARAGRAPH.CENTER, after=3)
    para(doc, f"{D.CITY}, {D.YEAR}", size=12, align=WD_ALIGN_PARAGRAPH.CENTER)

    # ---- пояснительная записка
    h = doc.add_heading("Пояснительная записка", level=1)
    h.paragraph_format.page_break_before = True
    for title, paras in D.NOTE:
        doc.add_heading(title, level=2)
        for ptxt in paras:
            para(doc, ptxt, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        if title.startswith("Формат"):
            rows = []
            tl = 0
            for m in D.MODULES:
                a, b = m["lessons"]
                k = b - a + 1
                tl += k
                rows.append([f"Модуль {m['n']}. {m['title']}", f"{a}-{b}", str(k), str(k * 2)])
            rows.append(["Итого теоретическая часть", "1-24", str(tl), str(tl * 2)])
            rows.append(["Групповая супервизия", "6 месяцев, 1 встреча в неделю", "-", "-"])
            para(doc, "Объём часов по модулям (академических часов)", bold=True, after=3, keep=True)
            make_table(doc, ["Модуль", "Занятия", "Число занятий", "Часов"], rows, [8.0, 3.6, 2.6, 1.8], center_cols=(1, 2, 3))

    # ---- сводная таблица
    h = doc.add_heading("Сводная таблица занятий", level=1)
    h.paragraph_format.page_break_before = True
    para(doc, "Два занятия в неделю по 2 академических часа (90 минут). Всего 12 недель.", after=6)
    t = doc.add_table(rows=1, cols=4)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    thin_borders(t)
    widths = [1.9, 2.3, 10.2, 1.6]
    for i, hd in enumerate(["Неделя", "Занятие", "Тема", "Часы"]):
        cell_text(t.rows[0].cells[i], hd, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER if i != 2 else None)
        shade(t.rows[0].cells[i], "E4E7EE")
    repeat_header(t.rows[0])
    total = 0
    for m in D.MODULES:
        r = t.add_row()
        no_split(r)
        mc = r.cells[0].merge(r.cells[3])
        cell_text(mc, f"Модуль {m['n']}. {m['title']}", bold=True)
        mc.paragraphs[0].paragraph_format.keep_with_next = True
        shade(mc, "F1EEE4")
        for L in D.LESSONS:
            if m["lessons"][0] <= L["n"] <= m["lessons"][1]:
                r = t.add_row()
                no_split(r)
                vals = [str(week_of(L["n"])), str(L["n"]), L["title"], "2"]
                total += 2
                for i, v in enumerate(vals):
                    cell_text(r.cells[i], v, align=WD_ALIGN_PARAGRAPH.CENTER if i != 2 else None)
    r = t.add_row()
    mc = r.cells[0].merge(r.cells[2])
    cell_text(mc, "Итого", bold=True)
    cell_text(r.cells[3], str(total), bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    apply_widths(t, widths)
    assert total == 48

    # ---- модули и занятия
    for m in D.MODULES:
        h = doc.add_heading(f"Модуль {m['n']}. {m['title']}", level=1)
        h.paragraph_format.page_break_before = True
        a, b = m["lessons"]
        para(doc, f"Занятия {a}-{b}, {(b - a + 1) * 2} академических часа.".replace("часа", "часов" if (b - a + 1) * 2 not in (2, 3, 4) else "часа"), italic=True, after=4)
        para(doc, m["intro"], align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        for L in D.LESSONS:
            if a <= L["n"] <= b:
                lesson_docx(doc, L)

    # ---- супервизия
    S = D.SUPERVISION
    h = doc.add_heading("Программа групповой супервизии (6 месяцев)", level=1)
    h.paragraph_format.page_break_before = True
    para(doc, S["intro"], align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    doc.add_heading("Этапы супервизии", level=2)
    make_table(doc, ["Период", "Содержание"], [[a, b] for a, b in S["phases"]], [4.6, 11.4])
    doc.add_heading("Формат встречи (90 минут)", level=2)
    make_table(doc, ["Время", "Содержание"], [[a, b] for a, b in S["format"]], [2.6, 13.4])
    doc.add_heading("Как представлять случай", level=2)
    para(doc, "Каждый слушатель готовит краткое письменное представление случая по единому шаблону:", after=3)
    numbered(doc, S["case_fields"])
    doc.add_heading("Правила работы группы", level=2)
    bullets(doc, S["rules"])
    doc.add_heading("Критерии завершения супервизии", level=2)
    para(doc, "Для получения сертификата необходимо выполнить следующее:", after=3)
    numbered(doc, S["criteria"])

    # ---- литература
    h = doc.add_heading("Рекомендуемая литература", level=1)
    h.paragraph_format.space_before = Pt(18)
    numbered(doc, D.LITERATURE)
    para(doc, D.LIT_NOTE, italic=True, size=11, before=8)

    doc.core_properties.title = "Учебная программа курса КПТ"
    doc.core_properties.author = D.SCHOOL
    doc.save(path)


def lesson_docx(doc, L):
    n = L["n"]
    doc.add_heading(f"Занятие {n}. {L['title']}", level=2)
    para(doc, f"Модуль {L['module']}  |  неделя {week_of(n)}  |  2 академических часа (90 минут)", italic=True, size=11, after=4, keep=True)

    doc.add_heading("Цель занятия", level=3)
    para(doc, L["goal"], align=WD_ALIGN_PARAGRAPH.JUSTIFY)

    doc.add_heading("Ключевые понятия", level=3)
    para(doc, "; ".join(L["concepts"]) + ".", align=WD_ALIGN_PARAGRAPH.JUSTIFY, after=2)

    doc.add_heading("Структура занятия (2 академических часа)", level=3)
    rows = []
    for tm, name, mins, key in STAGES:
        if key is None:
            txt = HW_TEXT
        else:
            txt = L["plan"][key]
        if n == 1 and key == "check":
            name = "Знакомство и правила работы"
        rows.append([tm, name, txt, str(mins)])
    assert sum(s[2] for s in STAGES) == 90
    make_table(doc, ["Время", "Этап", "Содержание", "Мин."], rows, [1.9, 3.0, 9.8, 1.3], size=9.5, center_cols=(0, 3))

    doc.add_heading("Техники и как они выполняются", level=3)
    for tq in L["techniques"]:
        p = para(doc, tq["name"] + ". ", bold=True, after=1, before=3, keep=True)
        r = p.add_run(tq["desc"])
        set_run_font(r, size=12, italic=True)
        numbered(doc, tq["steps"])

    if L.get("compare"):
        doc.add_heading("Сравнение с классической КПТ", level=3)
        make_table(doc, D_CMP_HEAD(), L["compare"], [2.6, 3.0, 3.4, 3.5, 3.5], size=9.5)

    doc.add_heading("Рабочие бланки и материалы", level=3)
    para(doc, "; ".join(L["forms"]) + ".", align=WD_ALIGN_PARAGRAPH.JUSTIFY, after=2)

    doc.add_heading("Домашнее задание слушателю", level=3)
    bullets(doc, L["homework"])

    doc.add_heading("Типичные ошибки начинающего терапевта", level=3)
    bullets(doc, L["mistakes"])


def D_CMP_HEAD():
    from kpt_lessons_4 import CMP_HEAD
    return CMP_HEAD


# ================================================================= PPTX
def rgb(h):
    return PRGB.from_string(h)


def est_lines(text, width_in, pt, factor):
    cpl = max(1, int(width_in * 72 / (pt * factor)))
    lines = 0
    for part in text.split("\n"):
        words = part.split(" ")
        cur = 0
        n = 1
        for w in words:
            L = len(w)
            if cur == 0:
                cur = L
            elif cur + 1 + L <= cpl:
                cur += 1 + L
            else:
                n += 1
                cur = L
        lines += n
    return lines


WARN = []
CAL, GEO = 0.53, 0.60


def check_fit(label, paras, width_in, height_in):
    """paras: list of (text, pt, font, indent_in, spacing_after_pt)"""
    h = 0.0
    for text, pt, font, ind, sp in paras:
        f = GEO if font == "Georgia" else CAL
        n = est_lines(text, width_in - ind - 0.2, pt, f)
        h += n * pt * 1.2 / 72 + sp / 72
    h += 0.1
    if h > height_in:
        WARN.append(f"{label}: нужно {h:.2f} дюйма, есть {height_in:.2f}")
    return h


def add_tb(slide, x, y, w, h, paras, label, anchor=MSO_ANCHOR.TOP, check=True):
    """paras: list of dict(text,size,font,color,bold,italic,bullet,after,align)"""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.1)
    tf.margin_top = tf.margin_bottom = Inches(0.05)
    chk = []
    for i, p in enumerate(paras):
        para_ = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para_.alignment = p.get("align", PP_ALIGN.LEFT)
        para_.space_after = PPt(p.get("after", 0))
        r = para_.add_run()
        r.text = p["text"]
        f = r.font
        f.name = p.get("font", "Calibri")
        f.size = PPt(p["size"])
        f.bold = p.get("bold", False)
        f.italic = p.get("italic", False)
        f.color.rgb = rgb(p.get("color", NAVY))
        ind = 0.0
        if p.get("bullet"):
            ind = 0.4
            pPr = para_._p.get_or_add_pPr()
            pPr.set("marL", str(int(0.4 * 914400)))
            pPr.set("indent", str(-int(0.4 * 914400)))
            bc = OxmlElement("a:buClr")
            sc = OxmlElement("a:srgbClr")
            sc.set("val", GOLD)
            bc.append(sc)
            pPr.append(bc)
            bu = OxmlElement("a:buChar")
            bu.set("char", "•")
            pPr.append(bu)
        chk.append((p["text"], p["size"], p.get("font", "Calibri"), ind, p.get("after", 0)))
        assert p["size"] >= 18, "кегль меньше 18"
    if check:
        check_fit(label, chk, w, h)
    return tb


def bg(slide, color):
    f = slide.background.fill
    f.solid()
    f.fore_color.rgb = rgb(color)


def rect(slide, x, y, w, h, color, line=None):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = rgb(color)
    if line:
        s.line.color.rgb = rgb(line)
        s.line.width = PPt(1)
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    return s


def slide_number(slide, dark):
    tb = slide.shapes.add_textbox(Inches(12.0), Inches(6.85), Inches(1.0), Inches(0.45))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = Inches(0.05)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    fld = OxmlElement("a:fld")
    fld.set("id", "{B6F15528-21DE-4FAA-801E-634DDDAF4B2B}")
    fld.set("type", "slidenum")
    rpr = OxmlElement("a:rPr")
    rpr.set("lang", "ru-RU")
    rpr.set("sz", "1800")
    sf = OxmlElement("a:solidFill")
    c = OxmlElement("a:srgbClr")
    c.set("val", GOLD if dark else NAVY)
    sf.append(c)
    rpr.append(sf)
    lat = OxmlElement("a:latin")
    lat.set("typeface", "Calibri")
    rpr.append(lat)
    fld.append(rpr)
    t = OxmlElement("a:t")
    t.text = "‹#›"
    fld.append(t)
    p._p.append(fld)


def light_slide(prs, title, label=None, title_size=28):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s, CREAM)
    rect(s, 0, 0, 0.25, 7.5, NAVY)
    rect(s, 0.25, 0, 0.06, 7.5, GOLD)
    if label:
        add_tb(s, 0.65, 0.3, 11.5, 0.45, [dict(text=label, size=18, color="8A6D0B", bold=True)], "label:" + title)
    add_tb(s, 0.65, 0.72, 12.0, 1.3, [dict(text=title, size=title_size, font="Georgia", bold=True)], "title:" + title, anchor=MSO_ANCHOR.TOP)
    rect(s, 0.75, 2.08, 1.8, 0.06, GOLD)
    slide_number(s, False)
    return s


def dark_slide(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s, NAVY)
    rect(s, 0.7, 0, 0.08, 7.5, GOLD)
    return s


def build_pptx(path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # 1 титул
    s = dark_slide(prs)
    add_tb(s, 1.2, 0.9, 11.2, 0.9, [dict(text=D.SCHOOL.upper(), size=20, color=GOLD, bold=True)], "t1-school")
    add_tb(s, 1.2, 2.0, 11.2, 2.0, [dict(text="Когнитивно-поведенческая терапия (КПТ)", size=44, font="Georgia", color="FFFFFF", bold=True)], "t1-title")
    rect(s, 1.3, 4.1, 2.2, 0.07, GOLD)
    add_tb(s, 1.2, 4.3, 11.2, 1.8, [
        dict(text="Учебная программа курса. Первая основа КПТ и обзор современных направлений", size=24, color="FFFFFF", after=6),
        dict(text="3 месяца обучения (48 академических часов) и 6 месяцев групповой супервизии", size=20, color="E8E2CC"),
    ], "t1-sub")
    add_tb(s, 1.2, 6.2, 11.2, 0.9, [dict(text=f"Ведущий: {D.LEAD}. {D.CITY}, {D.YEAR}", size=20, color=GOLD)], "t1-lead")

    # 2 о курсе
    s = light_slide(prs, "О курсе")
    add_tb(s, 0.65, 2.4, 12.0, 4.3, [
        dict(text="Формат: 24 занятия, 2 раза в неделю по 2 академических часа", size=26, bullet=True, after=8),
        dict(text="Объём: 48 академических часов за 3 месяца", size=26, bullet=True, after=8),
        dict(text="Далее: 6 месяцев групповой супервизии, раз в неделю", size=26, bullet=True, after=8),
        dict(text="Ведущий: Кенан Рагимов, врач-психиатр", size=26, bullet=True, after=8),
        dict(text="Результат: умение построить сессию и концептуализацию, применять базовые техники", size=26, bullet=True, after=8),
        dict(text="Документ: сертификат школы", size=26, bullet=True),
    ], "about")

    # 3 карта модулей
    s = light_slide(prs, "Карта курса: шесть модулей")
    shorts = {1: "История, модель, сессия, случай", 2: "Мысли, искажения, убеждения", 3: "Активация, экспозиция, навыки",
              4: "Депрессия, тревога, ОКР, ПТСР, сон", 5: "РЭПТ, схемы, ACT, DBT, MBCT, CFT", 6: "Другие школы, интеграция"}
    for i, m in enumerate(D.MODULES):
        cx = 0.65 + (i % 3) * 4.1
        cy = 2.35 + (i // 3) * 2.3
        rect(s, cx, cy, 3.9, 2.1, "FFFFFF", line=GOLD)
        add_tb(s, cx + 0.05, cy + 0.05, 3.8, 2.0, [
            dict(text=f"Модуль {m['n']}. Занятия {lesson_range(m)}", size=18, color="8A6D0B", bold=True, after=2),
            dict(text=m["title"], size=24, font="Georgia", bold=True, after=2),
            dict(text=shorts[m["n"]], size=20),
        ], f"map{m['n']}")

    lessons = {L["n"]: L for L in D.LESSONS}

    def divider(m):
        s = dark_slide(prs)
        a, b = m["lessons"]
        add_tb(s, 1.2, 1.9, 11.2, 0.7, [dict(text=f"Модуль {m['n']}", size=28, color=GOLD, bold=True)], f"div{m['n']}-a")
        add_tb(s, 1.2, 2.7, 11.2, 1.9, [dict(text=m["title"], size=44, font="Georgia", color="FFFFFF", bold=True)], f"div{m['n']}-t")
        rect(s, 1.3, 4.7, 2.2, 0.07, GOLD)
        add_tb(s, 1.2, 4.95, 11.2, 1.3, [
            dict(text=f"Занятия {a}-{b}", size=24, color="FFFFFF", after=4),
            dict(text=shorts[m["n"]], size=22, color="E8E2CC"),
        ], f"div{m['n']}-s")
        slide_number(s, True)

    def lesson_slide(L):
        title = L["stitle"]
        lab = f"Модуль {L['module']}. Занятие {L['n']} из 24, неделя {week_of(L['n'])}"
        s = light_slide(prs, title, label=lab)
        add_tb(s, 0.65, 2.3, 12.0, 3.7, [dict(text=b, size=26, bullet=True, after=7) for b in L["bullets"]], f"L{L['n']}-bul")
        rect(s, 0.65, 6.15, 11.0, 0.04, GOLD)
        add_tb(s, 0.65, 6.25, 11.2, 0.95, [dict(text="Практика: " + L["practice_line"], size=22, bold=True, color=NAVY)], f"L{L['n']}-prac")

    def compare_slide(spec):
        s = light_slide(prs, spec["title"])
        cols = [3.3, 4.2, 4.5]
        rows = [spec["head"]] + spec["rows"]
        x0, y0 = 0.65, 2.35
        # оценка высот строк
        heights = []
        for ri, row in enumerate(rows):
            ln = max(est_lines(c, cols[i] - 0.3, 20, CAL) for i, c in enumerate(row))
            heights.append(ln * 20 * 1.2 / 72 + 0.2)
        total = sum(heights)
        if y0 + total > 6.9:
            WARN.append(f"compare '{spec['title']}': таблица {total:.2f} дюйма не помещается")
        gt = s.shapes.add_table(len(rows), 3, Inches(x0), Inches(y0), Inches(sum(cols)), Inches(total))
        tbl = gt.table
        for i, w in enumerate(cols):
            tbl.columns[i].width = Inches(w)
        for ri, row in enumerate(rows):
            tbl.rows[ri].height = Inches(heights[ri])
            for ci, txt in enumerate(row):
                c = tbl.cell(ri, ci)
                c.fill.solid()
                c.fill.fore_color.rgb = rgb(NAVY if ri == 0 else ("FFFFFF" if ri % 2 else "EFEBDD"))
                c.margin_left = c.margin_right = Inches(0.1)
                c.margin_top = c.margin_bottom = Inches(0.05)
                c.vertical_anchor = MSO_ANCHOR.MIDDLE
                tf = c.text_frame
                tf.word_wrap = True
                p = tf.paragraphs[0]
                r = p.add_run()
                r.text = txt
                r.font.size = PPt(20)
                r.font.name = "Georgia" if ri == 0 else "Calibri"
                r.font.bold = ri == 0 or ci == 0
                r.font.color.rgb = rgb(GOLD if ri == 0 else NAVY)

    for m in D.MODULES:
        divider(m)
        a, b = m["lessons"]
        for n in range(a, b + 1):
            lesson_slide(lessons[n])
            if n == 22:
                compare_slide(D.SLIDE_COMPARE_1)
            if n == 23:
                compare_slide(D.SLIDE_COMPARE_2)

    # супервизия
    s = light_slide(prs, "Групповая супервизия: 6 месяцев")
    add_tb(s, 0.65, 2.3, 12.0, 4.5, [
        dict(text="Одна встреча в неделю, ориентировочно 2 академических часа", size=26, bullet=True, after=6),
        dict(text="На встрече два случая: презентация, вопросы, ролевая практика", size=26, bullet=True, after=6),
        dict(text="Случай по шаблону: вопрос, оценка, концептуализация, фрагмент сессии", size=26, bullet=True, after=6),
        dict(text="Этапы: вход в практику, углубление, автономия", size=26, bullet=True, after=6),
        dict(text="Завершение: не менее двух случаев, самооценка, план развития", size=26, bullet=True, after=6),
        dict(text="Итог: сертификат школы", size=26, bullet=True),
    ], "sup")

    # заключение
    s = light_slide(prs, "Итог курса")
    add_tb(s, 0.65, 2.4, 12.0, 3.2, [
        dict(text="Вы получаете первую основу КПТ: модель, сессию, концептуализацию, техники", size=26, bullet=True, after=8),
        dict(text="Вы знакомитесь с протоколами и современными направлениями", size=26, bullet=True, after=8),
        dict(text="Вы закрепляете навык на шестимесячной супервизии", size=26, bullet=True),
    ], "final")
    add_tb(s, 0.65, 5.9, 11.0, 1.2, [
        dict(text=f"{D.SCHOOL}. {D.CITY}", size=20, bold=True, color="8A6D0B"),
        dict(text="Ведущий: Кенан Рагимов", size=20),
    ], "final-foot")

    prs.save(path)
    return len(prs.slides)


if __name__ == "__main__":
    out_docx = os.path.join(HERE, "KPT_programma.docx")
    out_pptx = os.path.join(HERE, "KPT_programma.pptx")
    build_docx(out_docx)
    n = build_pptx(out_pptx)
    print("docx:", out_docx)
    print("pptx:", out_pptx, "слайдов:", n)
    if WARN:
        print("ПРЕДУПРЕЖДЕНИЯ ВМЕСТИМОСТИ:")
        for w in WARN:
            print("  ", w)
    else:
        print("Проверка вместимости: замечаний нет")
