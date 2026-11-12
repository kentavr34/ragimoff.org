# -*- coding: utf-8 -*-
"""Раскладка картинок по разделам сайта «как в библиотеке» (решение владельца 12.11.2026).
Было: assets/img/site/<дерево старого сайта> и два десятка файлов россыпью в assets/img.
Стало: assets/img/<раздел>/… — home, books, specialists, programs, consult, training, blog.
Скрипт переносит файлы (git mv), переписывает ссылки в данных и сценариях. Повторный запуск ничего не меняет.
Карта разделов — в _agent/docs/FILE_MAP.md, проверка — _tools/structure_check.py."""
import io, os, re, sys, glob, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
IMG = "assets/img/"
# старое место (от assets/img/) → новое место (от assets/img/); порядок важен: частное раньше общего
MOVE = [
    ("site/hero-n/b2b.webp", "training/hero.webp"),
    ("site/hero-n/qanunlar.webp", "programs/law-hero.webp"),
    ("site/hero-n/", "consult/"),
    ("site/hero/", "blog/hero/"),
    ("site/blog/", "blog/"),
    ("site/certificate/", "programs/docs/certificates/"),
    ("site/institute/", "programs/docs/institute/"),
    ("site/diplomas/", "specialists/kenan/diplomas/"),
    ("site/kenan/", "specialists/kenan/"),
    ("site/samira/", "specialists/samira/"),
    ("proof/", "programs/proof/"),
    ("kenan.jpg", "specialists/kenan.jpg"),
    ("samira.jpg", "specialists/samira.jpg"),
    ("blog-1.jpg", "home/blog-1.jpg"), ("blog-2.jpg", "home/blog-2.jpg"), ("blog-3.jpg", "home/blog-3.jpg"),
]


def new_rel(rel):
    for a, b in MOVE:
        if a.endswith("/"):
            if rel.startswith(a):
                return b + rel[len(a):]
        elif rel == a:
            return b
    m = re.match(r"^book-([a-z]+)-(az|ru|en)\.jpg$", rel)
    if m:
        return "books/covers/%s-%s.jpg" % (m.group(1), m.group(2))
    return None


moved = 0
for root, _, files in os.walk(IMG):
    for f in files:
        rel = os.path.join(root, f).replace("\\", "/")[len(IMG):]
        nr = new_rel(rel)
        if not nr or nr == rel:
            continue
        os.makedirs(os.path.dirname(IMG + nr), exist_ok=True)
        r = subprocess.run(["git", "mv", "-k", IMG + rel, IMG + nr], capture_output=True)
        if os.path.exists(IMG + rel):                     # файл не под git — переносим обычным способом
            os.replace(IMG + rel, IMG + nr)
        moved += 1
for root, dirs, files in os.walk(IMG, topdown=False):
    if not os.listdir(root):
        os.rmdir(root)
print("файлов перенесено:", moved)

# ссылки в данных: "/images/<старое дерево сайта>/…" → "/images/<раздел>/…" (fixImg добавляет assets/img/)
changed = 0
for fn in glob.glob("data/*/*.json") + glob.glob("_agent/archive/*/*.json"):
    s = io.open(fn, encoding="utf-8").read()

    def f(m):
        nr = new_rel("site/" + m.group(1))
        return '"/images/' + (nr if nr else m.group(1))
    o = re.sub(r'"/images/((?:hero-n|hero|blog|certificate|institute|diplomas|kenan|samira)/[^"]*)', f, s) if '"/images/' in s else s
    if o != s:
        for _ in range(5):
            try:
                io.open(fn, "w", encoding="utf-8", newline="\n").write(o)
                break
            except OSError:
                import time; time.sleep(1.5)
        changed += 1
print("файлов данных со ссылками:", changed)

# ссылки в сценариях
JS = [("assets/js/blocks.js", [("'assets/img/site/' + u.slice(8)", "'assets/img/' + u.slice(8)"), ("assets/img/${i ? 'samira' : 'kenan'}.jpg", "assets/img/specialists/${i ? 'samira' : 'kenan'}.jpg")]),
      ("assets/js/site.js", [("assets/img/book-${cov[i]}-${lang}.jpg", "assets/img/books/covers/${cov[i]}-${lang}.jpg"), ("assets/img/book-therapy-${lang}.jpg", "assets/img/books/covers/therapy-${lang}.jpg"),
                             ("assets/img/blog-${i + 1}.jpg", "assets/img/home/blog-${i + 1}.jpg"), ("assets/img/proof/", "assets/img/programs/proof/"), ("assets/img/${i ? 'samira' : 'kenan'}.jpg", "assets/img/specialists/${i ? 'samira' : 'kenan'}.jpg")]),
      ("assets/js/page-shop.js", [("assets/img/book-${it.id}-${lang}.jpg", "assets/img/books/covers/${it.id}-${lang}.jpg")]),
      ("assets/js/page-program.js", [("assets/img/proof/", "assets/img/programs/proof/"), ("assets/img/${sam ? 'samira' : 'kenan'}.jpg", "assets/img/specialists/${sam ? 'samira' : 'kenan'}.jpg")])]
for p, pairs in JS:
    s = io.open(p, encoding="utf-8").read()
    o = s
    for a, b in pairs:
        s = s.replace(a, b)
    if s != o:
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)
        print("ссылки:", p)
left = [l for p in glob.glob("assets/js/*.js") + glob.glob("*.html") for l in re.findall(r"assets/img/(?:site/|proof/|book-|blog-\$|\$\{)[^'\"` ]*", io.open(p, encoding="utf-8").read())]
print("старых ссылок в сценариях осталось:", len(left), left[:6])
