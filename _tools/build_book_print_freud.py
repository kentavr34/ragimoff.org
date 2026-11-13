# -*- coding: utf-8 -*-
"""Книги серии Фрейда на сайте — из печатных версий (13.11.2026).
Текст библиотеки собирается из свёрстанного Word D:/Projects/Freud/Print/Kitab_NN*.docx (его собирает Freud/tools/print/build_b5.js).

    python _tools/build_book_print_freud.py            # все 17 книг
    python _tools/build_book_print_freud.py freud-gw01 # одна книга

Разметка Word: Heading 1 — работа/глава (глава сайта), Heading 2 — подзаголовок (<h3>), стиль Part — подпись части (part в оглавлении),
всё остальное до первого Heading 1 (титул, выходные данные, оглавление) пропускается. Сноски (footnotes.xml) остаются сносками:
ссылка <sup class="fn-ref"> в тексте и список <aside class="rd-notes"> в конце главы — та же разметка, что у прежних глав (читалка открывает их окном).
Нумерация сносок сквозная по книге, как в печати. Курсив и полужирный сохраняются. Паспорт: toc и src обновляются, названия, обложка и сведения остаются.
Для Книги 16 (freud-gw17) после сборки надо снова запустить merge_books.py: в паспорте записывается own (число собственных глав)."""
import io, os, re, sys, json, glob, html, zipfile
import docx
from docx.text.run import Run
from docx.text.paragraph import Paragraph
from lxml import etree
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
PR = "D:/Projects/Freud/Print"
BOOKS = {"freud-gw01": 1, "freud-gw02": 2, "freud-gw04": 3, "freud-gw05": 4, "freud-gw06": 5, "freud-gw07": 6, "freud-gw08": 7, "freud-gw09": 8,
         "freud-gw10": 9, "freud-gw11": 10, "freud-gw12": 11, "freud-gw13": 12, "freud-gw14": 13, "freud-gw15": 14, "freud-gw16": 15,
         "freud-gw17": 16, "freud-fliesse-mektublari": 17,          # книга сайта → номер Kitab_NN
         "freud-mektublar-aforizmler": "vne_serii/Mektublar_ve_aforizmler_AZ_v*.docx"}   # 13.11: книга вне серии — путь в Print
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
esc = lambda s: html.escape(s, quote=False)
NOTES_H = {"az": "Qeydlər", "ru": "Примечания", "en": "Notes"}
NOTE_L = {"az": "Qeyd", "ru": "Примечание", "en": "Note"}


def save(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path) and io.open(path, encoding="utf-8").read() == text:
        return 0
    t = path + ".new"
    io.open(t, "w", encoding="utf-8", newline="\n").write(text)
    os.replace(t, path)
    return 1


def footnotes(path):
    """id → список (текст, жирный, курсив) частей сноски из footnotes.xml."""
    z = zipfile.ZipFile(path)
    out = {}
    if "word/footnotes.xml" not in z.namelist():
        return out
    root = etree.fromstring(z.read("word/footnotes.xml"))
    for fn in root.findall(W + "footnote"):
        i = fn.get(W + "id")
        if fn.get(W + "type") in ("separator", "continuationSeparator", "continuationNotice") or i in ("-1", "0"):
            continue
        out[i] = fn
    return out


def TXT(c):
    if c.tag == W + "t":
        return c.text or ""
    if c.tag == W + "tab":
        return " "
    if c.tag in (W + "br", W + "cr"):
        return "\n"
    return ""


def pieces(p_el, doc_part):
    """Части абзаца: ('t', текст, жирный, курсив) и ('f', id сноски) в порядке следования."""
    res = []
    for r in p_el.iter(W + "r"):
        ref = r.find(W + "footnoteReference")
        if ref is not None:
            res.append(("f", ref.get(W + "id")))
            continue
        t = "".join(TXT(c) for c in r)
        if t:
            rp = r.find(W + "rPr")
            fl = lambda tag: rp is not None and rp.find(W + tag) is not None and rp.find(W + tag).get(W + "val") not in ("0", "false", "off")
            res.append(("t", t, fl("b"), fl("i")))
    return res


def render(parts, fnum):
    """HTML абзаца: курсив/полужирный как в Word; абзац, набранный целиком курсивом, — один <em>; ссылки на сноски — <sup class=fn-ref>."""
    txt = [x for x in parts if x[0] == "t" and x[1].strip()]
    if not txt and not any(x[0] == "f" for x in parts):
        return ""
    all_i = bool(txt) and all(x[3] for x in txt)
    all_b = bool(txt) and all(x[2] for x in txt)
    out, buf = "", ""

    def flush():
        nonlocal out, buf
        if not buf:
            return
        s = buf
        if all_i:
            s = "<em>" + s + "</em>"
        if all_b:
            s = "<strong>" + s + "</strong>"
        out += s
        buf = ""

    for x in parts:
        if x[0] == "f":
            flush()
            n = fnum(x[1])
            out += '<sup class="fn-ref"><a aria-label="Qeyd %d" href="#fn%d" id="fnr%d">%d</a></sup>' % (n, n, n, n)
            continue
        _, t, b, i = x
        s = esc(t).replace("\n", "<br>")
        if b and not all_b:
            s = "<strong>" + s + "</strong>"
        if i and not all_i:
            s = "<em>" + s + "</em>"
        buf += s
    flush()
    out = re.sub(r"</strong><strong>|</em><em>", "", out)
    return out.strip()


def build(bid, no):
    f = glob.glob("%s/%s" % (PR, no)) if isinstance(no, str) else glob.glob("%s/Kitab_%02d *.docx" % (PR, no))
    assert len(f) == 1, (no, f)
    path = f[0]
    d = docx.Document(path)
    fx = footnotes(path)
    cnt = [0]
    seen = {}

    def fnum(i):
        if i not in seen:
            cnt[0] += 1
            seen[i] = cnt[0]
        return seen[i]

    chapters, cur, label, started = [], None, "", False
    nref = 0
    for el in d.element.body.iterchildren():
        if not el.tag.endswith("}p"):
            continue
        p = Paragraph(el, d)
        st, txt = p.style.name, p.text.strip()
        if st == "Heading 1":
            started = True
            cur = {"t": txt, "html": [], "part": label, "notes": [], "lead": ""}
            label = ""
            chapters.append(cur)
            hp = pieces(el, None)
            for x in hp:                                      # сноска, стоящая в заголовке: ссылка ставится в начало текста главы
                if x[0] == "f":
                    n = fnum(x[1])
                    cur["notes"].append((n, x[1]))
                    cur["lead"] += '<sup class="fn-ref"><a aria-label="Qeyd %d" href="#fn%d" id="fnr%d">%d</a></sup>' % (n, n, n, n)
            continue
        if st == "Part":                                      # страница части: подпись к следующей главе
            label = txt
            continue
        if not started:
            continue
        parts = pieces(el, None)
        if not txt and not any(x[0] == "f" for x in parts):
            continue
        before = cnt[0]
        h = render(parts, fnum)
        for i, n in sorted(((i, n) for i, n in seen.items() if n > before), key=lambda z: z[1]):
            cur["notes"].append((n, i))
        if st == "Heading 2":
            cur["html"].append("<h3>%s</h3>" % h)
        elif st == "Heading 3":
            cur["html"].append("<h4>%s</h4>" % h)
        else:
            cur["html"].append("<p>%s</p>" % h)
    for c in chapters:
        if c["lead"]:
            if c["html"] and c["html"][0].startswith("<p>"):
                c["html"][0] = "<p>" + c["lead"] + c["html"][0][3:]
            else:
                c["html"].insert(0, "<p>%s</p>" % c["lead"])
        if c["notes"]:
            items = []
            for n, i in c["notes"]:
                body = []
                for fp in fx[i].findall(W + "p"):
                    h = render(pieces(fp, None), lambda z: 0)
                    if h:
                        body.append(h)
                items.append('<p id="fn%d"><a class="fn-back" href="#fnr%d">%d</a> %s</p>' % (n, n, n, "<br>".join(body)))
            c["html"].append('<aside class="rd-notes"><h4>%s</h4>%s</aside>' % (NOTES_H["az"], "".join(items)))
    return chapters, cnt[0], os.path.basename(path), len(fx)


def main():
    only = sys.argv[1:]
    stat = []
    wrote = 0
    for bid, no in BOOKS.items():
        if only and bid not in only:
            continue
        pj = "books/%s/book.json" % bid
        P = json.load(io.open(pj, encoding="utf-8"))
        old = P["toc"].get("az", [])
        if P.get("parts") and P.get("own"):
            old = old[:P["own"]]
        ch, nfn, fname, nfx = build(bid, no)
        toc = []
        for i, c in enumerate(ch, 1):
            body = "\n".join(c["html"])
            wrote += save("books/%s/az/%03d.html" % (bid, i), body + "\n")
            it = {"t": c["t"], "n": len(re.sub(r"<[^>]+>", "", body))}
            if c["part"]:
                it["part"] = c["part"]
            toc.append(it)
        keep = len(toc)
        for oldf in glob.glob("books/%s/az/*.html" % bid):
            if int(os.path.basename(oldf)[:-5]) > keep and not (P.get("parts") and P.get("own")):
                os.replace(oldf, oldf + ".old")                # лишняя глава прежней сборки — не удаляется, а откладывается
        P["toc"]["az"] = toc
        if P.get("parts"):
            P["own"] = len(toc)                                # merge_books.py дополняет книгу присоединёнными разделами после собственных глав
        for row in P["meta"]["az"]:
            if row[0] == "Fəsillər":
                row[1] = str(len(toc))
        P["src"] = "Print: " + fname
        wrote += save(pj, json.dumps(P, ensure_ascii=False, indent=1) + "\n")
        stat.append((bid, len(old), sum(x["n"] for x in old), len(toc), sum(x["n"] for x in toc), nfn, nfx))
        print("%s: глав %d→%d, знаков %d→%d, сносок на сайте %d (в Word %d) — из %s" % (bid, len(old), len(toc), sum(x["n"] for x in old), sum(x["n"] for x in toc), nfn, nfx, fname))
    ix = json.load(io.open("books/index.json", encoding="utf-8"))          # картотека: число глав и знаков
    for b in ix["books"]:
        if b["id"] in BOOKS and (not only or b["id"] in only):
            T = json.load(io.open("books/%s/book.json" % b["id"], encoding="utf-8"))["toc"]["az"]
            b["chapters"] = {"az": len(T)}
            b["chars"] = {"az": sum(x["n"] for x in T)}
    wrote += save("books/index.json", json.dumps(ix, ensure_ascii=False, indent=1) + "\n")
    print("файлов записано:", wrote)


main()
