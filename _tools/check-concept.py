# -*- coding: utf-8 -*-
"""
_tools/check-concept.py — статические проверки пересборки книг по каркасу концепта.

Сравнивает рабочее дерево с коммитом-донором (по умолчанию HEAD~1 нельзя — правки
в рабочем дереве, поэтому опорный коммит задаётся аргументом) и печатает числа:

  (а) число страниц до и после;
  (б) в каждой пересобранной странице есть классы .bk- и нет .content-wrap;
  (в) все внутренние ссылки (оглавление, пред/след, языки) разрешаются в файлы;
  (г) число пунктов оглавления = числу страниц глав (по книгам);
  (д) суммарная длина текста глав не уменьшилась;
  (е) тест «Эры Феникса» (books/phoenix-era/test/) не тронут.

Запуск:  python _tools/check-concept.py --base 84b6264
"""
import argparse
import html
import os
import posixpath
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS = [
    "books/freud-yuxularin-yozumu", "books/freud-musa", "books/freud-psixoanalizle-tanishliq",
    "books/freud-seksualligin-psixologiyasi", "books/freud-sevgi-mektublari",
    "books/freud-aforizmlar", "books/freud-medeniyyetin-sancilari", "books/freud-totem-ve-tabu",
    "books/virus-viny", "books/shizofreniya", "books/phoenix-era", "klinik-psixiatriya",
]


def git(*args):
    return subprocess.run(["git"] + list(args), cwd=ROOT, capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stdout


def listed(base):
    """Список html-страниц книг в опорном коммите и в рабочем дереве."""
    tracked = [l for l in git("ls-tree", "-r", "--name-only", base).splitlines() if l.endswith(".html")]
    old = sorted(p for p in tracked if any(p.startswith(b + "/") for b in BOOKS))
    new = []
    for b in BOOKS:
        for dp, dn, fn in os.walk(os.path.join(ROOT, b)):
            for f in fn:
                if f.endswith(".html"):
                    new.append(os.path.relpath(os.path.join(dp, f), ROOT).replace("\\", "/"))
    return old, sorted(new)


def text_of(s):
    s = re.sub(r"<(script|style)\b.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def content_region(s):
    """Читальная часть страницы: старая — .content-wrap, новая — колонка .bk-main."""
    i = s.find('<div class="content-wrap">')
    if i >= 0:
        ends = [x for x in (s.rfind("</main>"),
                            s.find('<div id="kitab-modal"'),
                            s.find("<footer"), s.rfind("</body>")) if x > i]
        return s[i:min(ends)] if ends else s[i:]
    i = s.find('<main class="bk-main">')
    if i < 0:
        return s
    j = s.find('<footer class="bk-ft">', i)
    return s[i:j if j > i else s.rfind("</main>")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="HEAD", help="опорный коммит (до пересборки)")
    a = ap.parse_args()

    old, new = listed(a.base)
    print("(а) страниц до: %d | после: %d | разница: %+d" % (len(old), len(new), len(new) - len(old)))
    only_old = sorted(set(old) - set(new))
    only_new = sorted(set(new) - set(old))
    if only_old:
        print("    пропали:", only_old[:10])
    if only_new:
        print("    появились:", only_new[:10])

    # (б) каркас; (в) ссылки; (д) текст
    bad_frame, bad_cw, broken, no_bk = [], [], [], []
    old_text, new_text = 0, 0
    drops = []
    files = 0
    for rel in new:
        p = os.path.join(ROOT, rel)
        s = open(p, encoding="utf-8", errors="replace").read()
        if 'class="bk-' not in s and "class='bk-" not in s:
            no_bk.append(rel)
            continue
        files += 1
        if "content-wrap" in s:
            bad_cw.append(rel)
        if re.search(r'class="(site-header|home-hero|sidebar)"', s):
            bad_frame.append(rel)
        # ссылки
        for m in re.finditer(r'<a\b[^>]*href="([^"]+)"', s):
            href = m.group(1)
            if href.startswith(("#", "mailto:", "tel:", "http:", "https:", "//")):
                continue
            clean = href.split("#")[0].split("?")[0]
            if clean.startswith("/"):                      # ссылка от корня сайта
                target = posixpath.normpath(clean.lstrip("/"))
            else:
                target = posixpath.normpath(posixpath.join(posixpath.dirname(rel), clean))
            if not os.path.exists(os.path.join(ROOT, target)):
                broken.append((rel, href))
        # текст: опорная версия против новой
        base_s = git("show", "%s:%s" % (a.base, rel))
        ot = len(text_of(content_region(base_s)))
        nt = len(text_of(content_region(s)))
        old_text += ot
        new_text += nt
        if ot and nt < ot * 0.99:
            drops.append((nt - ot, ot, nt, rel))

    print("(б) страниц с каркасом .bk-: %d | без каркаса: %d | осталось .content-wrap: %d | старое шасси: %d"
          % (files, len(no_bk), len(bad_cw), len(bad_frame)))
    if no_bk:
        print("    без .bk-:", no_bk[:10])
    if bad_cw:
        print("    .content-wrap:", bad_cw[:10])
    if bad_frame:
        print("    старое шасси:", bad_frame[:10])
    print("(в) битых внутренних ссылок: %d" % len(broken))
    for r, h in broken[:12]:
        print("    ", r, "->", h)
    print("(д) текста в читальной части: было %d знаков → стало %d (%+d, %+.2f%%)"
          % (old_text, new_text, new_text - old_text, 100.0 * (new_text - old_text) / max(1, old_text)))
    drops.sort()
    print("    страниц с потерей >1%%: %d%s" % (len(drops), ":" if drops else ""))
    for d, o, n, rel in drops[:8]:
        print("      %+d (было %d, стало %d) %s" % (d, o, n, rel))

    # (г) пункты оглавления против числа глав
    print("(г) оглавление против числа глав:")
    for b in BOOKS:
        langs = {}
        for rel in new:
            if not rel.startswith(b + "/") or not rel.endswith("index.html"):
                continue
            s = open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace").read()
            rows = len(re.findall(r'class="bk-toc__row', s))
            if not rows:
                continue
            lang = (re.findall(r'<html[^>]*lang="([^"]+)"', s) or ["?"])[0]
            linked = len(re.findall(r'<a class="bk-toc__a" href=', s))
            langs[lang] = (rows, linked, os.path.dirname(rel) or ".")
        pages = sum(1 for rel in new if rel.startswith(b + "/"))
        if langs:
            parts = []
            for k, (rows, linked, d) in sorted(langs.items()):
                # сколько страниц книги на этом языке (без титула)
                cnt = sum(1 for rel in new if rel.startswith(b + "/")
                          and (re.findall(r'<html[^>]*lang="([^"]+)"',
                                          open(os.path.join(ROOT, rel), encoding="utf-8",
                                               errors="replace").read(600)) or ["?"])[0] == k) - 1
                parts.append("%s: пунктов %d (со ссылкой %d) / страниц языка %d" % (k, rows, linked, cnt))
            print("    %-38s страниц %4d | %s" % (b, pages, " | ".join(parts)))
        else:
            print("    %-38s страниц %4d | титула нет" % (b, pages))

    # (е) тест Феникса
    ph = sorted(p for p in old if "/test/" in p)
    diff = [p for p in ph if git("show", "%s:%s" % (a.base, p)) != open(os.path.join(ROOT, p), encoding="utf-8", errors="replace").read()]
    print("(е) books/phoenix-era/test/: файлов %d | изменено: %d" % (len(ph), len(diff)))
    if diff:
        print("    ", diff)


if __name__ == "__main__":
    main()
