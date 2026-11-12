# -*- coding: utf-8 -*-
"""Книга сайта из печатной версии (12.11.2026): текст библиотеки собирается из свёрстанного Word папки Print —
того самого файла, что прошёл ворота печати и собран из базы истины. Сайт и печать показывают один текст.

    python _tools/build_book_print.py phoenix-era

Источник: D:/Projects/<Проект>/Print/print.json (утверждённые файлы по языкам). Результат — как у остальных книг:
books/<книга>/<язык>/NNN.html и оглавление в books/<книга>/book.json (названия, обложка и сведения паспорта сохраняются).
Глава = заголовок первого уровня печатной книги; название главы берётся из оглавления печатной книги."""
import io, os, re, sys, json, glob, html
import docx
from docx.table import Table
from docx.text.paragraph import Paragraph
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
PROJECT = {"phoenix-era": "Phoenix", "shizofreniya": "Pandemia", "virus-viny": "Virus"}          # книга сайта → папка проекта с Print
bid = sys.argv[1] if len(sys.argv) > 1 else "phoenix-era"
PR = os.path.join("D:/Projects", PROJECT[bid], "Print")
approved = json.load(io.open(os.path.join(PR, "print.json"), encoding="utf-8"))["approved"]
esc = lambda s: html.escape(s, quote=False)


def save(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path) and io.open(path, encoding="utf-8").read() == text:
        return 0
    t = path + ".new"
    io.open(t, "w", encoding="utf-8", newline="\n").write(text)
    os.replace(t, path)
    return 1


def runs(p):
    """Текст абзаца с курсивом и полужирным; абзац, набранный курсивом целиком, — один <em>."""
    parts = []
    for r in p.runs:
        t = r.text
        if not t:
            continue
        parts.append((t, bool(r.bold), bool(r.italic)))
    if not parts:
        return ""
    all_i = all(i for t, b, i in parts if t.strip())
    all_b = all(b for t, b, i in parts if t.strip())
    out = ""
    for t, b, i in parts:
        s = esc(t).replace("\n", "<br>")
        if b and not all_b:
            s = "<strong>" + s + "</strong>"
        if i and not all_i:
            s = "<em>" + s + "</em>"
        out += s
    out = re.sub(r"</strong><strong>|</em><em>", "", out)
    if all_i:
        out = "<em>" + out + "</em>"
    if all_b:
        out = "<strong>" + out + "</strong>"
    return out.strip()


def table(t):
    rows = []
    for k, r in enumerate(t.rows):
        tag = "th" if k == 0 else "td"
        seen, cells = set(), []
        for c in r.cells:
            if id(c._tc) in seen:
                continue
            seen.add(id(c._tc))
            cells.append("<%s>%s</%s>" % (tag, "<br>".join(runs(p) for p in c.paragraphs if p.text.strip()), tag))
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return "<table>" + "".join(rows) + "</table>"


def book(lang, path):
    d = docx.Document(path)
    titles = [re.sub(r"\t\d+\s*$", "", p.text).strip() for p in d.paragraphs if p.style.name in ("TOC Chapter", "TOC Part")]
    low = (lambda x: x.replace("İ", "i").replace("I", "ı").lower()) if lang == "az" else (lambda x: x.lower())   # азербайджанские İ/I
    norm = lambda x: re.sub(r"[^\w]+", "", low(x), flags=re.U)
    used = [0]

    def title_for(txt):
        """Название главы — строка оглавления печатной книги, в которой стоит этот заголовок (поиск вперёд по порядку)."""
        k = norm(txt)
        for j in range(used[0], len(titles)):
            if k and (k in norm(titles[j]) or norm(titles[j]) in k):
                used[0] = j + 1
                return titles[j]
        if used[0] < len(titles):                           # заголовок сформулирован иначе, чем строка оглавления: берётся следующая по порядку строка
            used[0] += 1
            return titles[used[0] - 1]
        return txt

    chapters, cur, part, started, lst = [], None, "", False, []

    def flush_list():
        if lst and cur is not None:
            cur["html"].append("<ol>" + "".join("<li>%s</li>" % x for x in lst) + "</ol>")
        del lst[:]

    for el in d.element.body.iterchildren():
        if el.tag.endswith("}tbl"):
            if cur is not None:
                flush_list()
                cur["html"].append(table(Table(el, d)))
            continue
        if not el.tag.endswith("}p"):
            continue
        p = Paragraph(el, d)
        st, txt = p.style.name, p.text.strip()
        if st == "Heading 1":
            flush_list()
            started = True
            cur = {"t": title_for(txt), "html": [], "part": ""}
            chapters.append(cur)
            continue
        if not txt:
            continue
        if st == "Part Title":                              # страница части (сезон): со своим текстом — отдельная глава, без текста — подпись к следующей главе
            flush_list()
            started = True
            cur = {"t": title_for(txt), "html": [], "part": ""}
            chapters.append(cur)
            continue
        if not started or st == "Part Kicker":
            continue
        if st in ("Chapter Kicker", "Chapter Subtitle", "Figure") or st.startswith("TOC"):
            continue
        h = runs(p)
        if st == "List Number":
            lst.append(h)
            continue
        flush_list()
        if st == "Heading 2":
            cur["html"].append("<h3>%s</h3>" % esc(txt))
        elif st == "Heading 3":
            cur["html"].append("<h4>%s</h4>" % esc(txt))
        elif st in ("Epigraph", "Quote"):
            cur["html"].append("<blockquote><p>%s</p></blockquote>" % h)
        elif st == "Verse":
            cur["html"].append('<p class="verse">%s</p>' % h)
        elif st == "Bibliography Head":
            cur["html"].append("<h3>%s</h3>" % esc(txt))
        else:
            cur["html"].append("<p>%s</p>" % h)
    flush_list()
    out, label = [], ""
    for c in chapters:
        size = len(re.sub(r"<[^>]+>", "", "".join(c["html"])))
        if size < 150:                                      # пустая страница части или раздела: её название — подпись к следующей главе
            label = c["t"]
            continue
        c["part"], label = label, ""
        out.append(c)
    return out


pj = "books/%s/book.json" % bid
P = json.load(io.open(pj, encoding="utf-8"))
wrote = 0
for lang in P["langs"]:
    a = approved.get(lang)
    if not a:
        print("нет утверждённой печатной версии:", lang)
        continue
    ch = book(lang, os.path.join(PR, a["file"]))
    toc = []
    for i, c in enumerate(ch, 1):
        body = "\n".join(c["html"])
        wrote += save("books/%s/%s/%03d.html" % (bid, lang, i), body + "\n")
        it = {"t": c["t"], "n": len(re.sub(r"<[^>]+>", "", body))}
        if c["part"]:
            it["part"] = c["part"]
        toc.append(it)
    for old in glob.glob("books/%s/%s/*.html" % (bid, lang)):
        if int(os.path.basename(old)[:-5]) > len(toc):
            os.replace(old, old + ".old")                 # лишняя глава прежней сборки — не удаляется, а откладывается
    P["toc"][lang] = toc
    print("%s %s: глав %d, знаков %d — из %s" % (bid, lang, len(toc), sum(x["n"] for x in toc), a["file"]))
P["src"] = "Print: " + ", ".join(approved[l]["file"] for l in P["langs"] if l in approved)
wrote += save(pj, json.dumps(P, ensure_ascii=False, indent=1) + "\n")
print("файлов записано:", wrote)
