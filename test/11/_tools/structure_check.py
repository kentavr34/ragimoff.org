# -*- coding: utf-8 -*-
"""Страж структуры файлов и карта файлов проекта (требование владельца 12.11.2026: «как в библиотеке —
в каждой подпапке свои разделы», «структура файлов — отдельная карта, как карта сайта»).

Проверяет, что каждый файл лежит в своём разделе, а библиотека книг цела:
  • в корне — только страницы-оболочки и описания; картинки — только в assets/img/<раздел>/;
  • данные страниц — data/<раздел>/<страница>.<язык>.json;
  • книги — books/<книга>/book.json + books/<книга>/<язык>/NN.html, главы идут подряд, оглавление совпадает с файлами,
    картотека books/index.json перечисляет ровно те книги, что лежат в папке;
  • нет картинок, на которые никто не ссылается, и ссылок на картинки, которых нет.
Запуск:  python structure_check.py        — проверка (код возврата 1 при нарушениях)
         python structure_check.py map    — проверка + пересборка FILE_MAP.md (карта файлов)"""
import io, os, re, sys, json, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
MAP = len(sys.argv) > 1 and sys.argv[1] == "map"
LANGS = ("az", "ru", "en", "tr")
ROOT_FILES = {"index.html": "главная", "program.html": "программа обучения (?p=)", "specialist.html": "специалист (?s=)", "consult.html": "консультация (?c=)",
              "contact.html": "контакты", "corporate.html": "тренинги для компаний", "blog.html": "блог", "article.html": "статья (?a=)", "law.html": "переадресация на блок «Юридические основы»",
              "shop.html": "книжный магазин", "book.html": "страница книги (?b=)", "read.html": "читалка (?b=&c=)", "test.html": "тест для студентов",
              "README.md": "описание проекта", "FILE_MAP.md": "карта файлов (собирается этим стражем)", ".gitignore": "что не публикуется"}
ROOT_DIRS = {"assets": "оформление и сценарии: css, js, img, hero", "data": "тексты страниц по разделам и языкам", "books": "библиотека: текст книг отдельно от страниц",
             "_tools": "инструменты сборки и стражи", "_agent": "служебное (не публикуется, кроме lock и archive)", "vendor": "сторонние библиотеки", "sketch": "наброски"}
IMG_DIRS = {"home": "главная", "books": "обложки книг", "specialists": "портреты и дипломы специалистов", "programs": "обучение: документы института, образцы, фото групп",
            "consult": "картины героя страниц консультаций", "training": "тренинги для компаний", "blog": "обложки статей по рубрикам"}
DATA_DIRS = {"blog": "статьи и список блога", "cons": "страницы консультаций", "page": "контакты, тренинги", "spec": "специалисты", "law": "блок «Юридические основы»", "shop": "каталог магазина"}
bad, warn = [], []

# ---------- корень ----------
for f in os.listdir("."):
    if f.startswith(".git") and f != ".gitignore":
        continue
    if os.path.isdir(f):
        if f not in ROOT_DIRS:
            bad.append("корень: лишняя папка «%s»" % f)
    elif f not in ROOT_FILES:
        bad.append("корень: лишний файл «%s» — страницам место в списке ROOT_FILES, остальному — в разделах" % f)

# ---------- картинки ----------
imgs = []
for root, dirs, files in os.walk("assets/img"):
    rel = root.replace("\\", "/")[len("assets/img"):].strip("/")
    top = rel.split("/")[0] if rel else ""
    for f in files:
        p = (rel + "/" + f).strip("/")
        imgs.append(p)
        if not rel:
            bad.append("картинка россыпью в assets/img: %s — положить в раздел (%s)" % (f, ", ".join(IMG_DIRS)))
        elif top not in IMG_DIRS:
            bad.append("картинка вне разделов: assets/img/%s" % p)
        if re.search(r"[^a-zA-Z0-9._-]", f):
            bad.append("имя картинки с пробелом или кириллицей: assets/img/%s" % p)
texts = ""
for p in glob.glob("data/*/*.json") + glob.glob("assets/js/*.js") + glob.glob("assets/css/*.css") + glob.glob("*.html") + glob.glob("_agent/archive/*/*.json"):
    texts += io.open(p, encoding="utf-8", errors="replace").read()
refs = set(re.findall(r'"/images/([^"?]+)', texts))
for r in sorted(refs):
    if not os.path.isfile("assets/img/" + r):
        bad.append("ссылка на отсутствующую картинку: /images/%s" % r)
used = set(refs)
for p in imgs:
    base = p.rsplit("/", 1)[-1]
    if p in used or ("assets/img/" + p) in texts:
        continue
    stem = re.sub(r"-(az|ru|en)\.(jpg|webp|png)$|-?\d*\.(jpg|webp|png)$", "", base)          # собираемые имена: covers/<книга>-<язык>.jpg, home/blog-N.jpg
    if stem and ("/" + stem in texts or stem + "-${" in texts or stem + "${" in texts or "'" + stem + "'" in texts or '"' + stem + '"' in texts or "? '" + stem in texts):
        continue
    warn.append("картинка без ссылок: assets/img/%s" % p)

# ---------- данные ----------
for root, dirs, files in os.walk("data"):
    rel = root.replace("\\", "/")[len("data"):].strip("/")
    for f in files:
        if not rel:
            bad.append("файл данных вне раздела: data/%s" % f)
        elif rel not in DATA_DIRS:
            bad.append("неизвестный раздел данных: data/%s/%s" % (rel, f))
        elif not re.match(r"^[a-z0-9-]+\.(az|ru|en)\.json$", f):
            bad.append("имя файла данных не «страница.язык.json»: data/%s/%s" % (rel, f))

# ---------- библиотека ----------
books = sorted(d for d in os.listdir("books") if os.path.isdir(os.path.join("books", d))) if os.path.isdir("books") else []
cat = json.load(io.open("books/index.json", encoding="utf-8"))["books"] if os.path.isfile("books/index.json") else []
cat_ids = [b["id"] for b in cat]
if sorted(cat_ids) != books:
    bad.append("картотека books/index.json не совпадает с папками: нет в картотеке %s; нет папки %s" % (sorted(set(books) - set(cat_ids)), sorted(set(cat_ids) - set(books))))
ALLOW_DIFF = set(l.split("#")[0].strip() for l in io.open("_tools/structure_allow.txt", encoding="utf-8").read().splitlines() if l.split("#")[0].strip()) if os.path.isfile("_tools/structure_allow.txt") else set()
stat = []
for b in books:
    pj = "books/%s/book.json" % b
    if not os.path.isfile(pj):
        bad.append("книга без паспорта: %s" % pj)
        continue
    P = json.load(io.open(pj, encoding="utf-8"))
    for x in os.listdir("books/" + b):
        if x != "book.json" and x not in LANGS:
            bad.append("лишнее в папке книги: books/%s/%s" % (b, x))
    counts = {}
    for l in P.get("langs", []):
        files = sorted(os.listdir("books/%s/%s" % (b, l))) if os.path.isdir("books/%s/%s" % (b, l)) else []
        want = ["%03d.html" % i for i in range(1, len(P["toc"].get(l, [])) + 1)]
        if files != want:
            bad.append("книга %s, язык %s: файлы глав не совпадают с оглавлением (файлов %d, в оглавлении %d)" % (b, l, len(files), len(want)))
        if not P["t"].get(l):
            bad.append("книга %s, язык %s: нет названия" % (b, l))
        for f in files[:400]:
            if os.path.getsize("books/%s/%s/%s" % (b, l, f)) < 40:
                bad.append("пустая глава: books/%s/%s/%s" % (b, l, f))
        counts[l] = len(files)
    for l in LANGS:
        if os.path.isdir("books/%s/%s" % (b, l)) and l not in P.get("langs", []):
            bad.append("книга %s: папка языка %s не указана в паспорте" % (b, l))
    if len(set(counts.values())) > 1 and b not in ALLOW_DIFF:
        bad.append("книга %s: число глав по языкам разное %s — сверить переводы (или внести в _tools/structure_allow.txt с причиной)" % (b, counts))
    stat.append((b, P, counts))

for x in bad:
    print("✗", x)
for x in warn[:40]:
    print("·", x)
print("НАРУШЕНИЙ СТРУКТУРЫ: %d, замечаний: %d (книг %d, картинок %d)" % (len(bad), len(warn), len(books), len(imgs)))

if MAP:
    L = ["# Карта файлов новой версии сайта (test/11)", "",
         "Собирается автоматически: `python _tools/structure_check.py map`. Правила раскладки проверяет тот же страж — файл не на своём месте останавливает публикацию.", "",
         "## Корень — страницы", "", "| файл | что это |", "|---|---|"]
    L += ["| `%s` | %s |" % (f, ROOT_FILES[f]) for f in ROOT_FILES if os.path.exists(f)]
    L += ["", "## Папки", "", "| папка | что лежит |", "|---|---|"] + ["| `%s/` | %s |" % (d, ROOT_DIRS[d]) for d in ROOT_DIRS if os.path.isdir(d)]
    L += ["", "## Тексты страниц — `data/<раздел>/<страница>.<язык>.json`", "", "| раздел | что лежит | страниц × языков |", "|---|---|---|"]
    for d, t in DATA_DIRS.items():
        fs = glob.glob("data/%s/*.json" % d)
        L.append("| `data/%s/` | %s | %d файлов (%d страниц) |" % (d, t, len(fs), len(set(os.path.basename(f).split(".")[0] for f in fs))))
    L += ["", "## Картинки — `assets/img/<раздел>/`", "", "| раздел | что лежит | файлов |", "|---|---|---|"]
    for d, t in IMG_DIRS.items():
        L.append("| `assets/img/%s/` | %s | %d |" % (d, t, sum(1 for p in imgs if p.startswith(d + "/"))))
    L += ["", "В данных картинка записывается как `/images/<раздел>/…` — сценарий подставляет `assets/img/`.", "",
          "## Библиотека — `books/`", "",
          "Текст книги хранится один раз и отдельно от страниц. Читает его одна читалка `read.html?b=<книга>&c=<глава>`; новая книга или новый язык — это новая папка с текстом, новых страниц не появляется.", "",
          "- `books/index.json` — картотека: все книги, языки, число глав и объём.",
          "- `books/<книга>/book.json` — паспорт: названия на языках, сведения, обложка, оглавление.",
          "- `books/<книга>/<язык>/NN.html` — текст главы NN.",
          "- Найти, где что написано: `python _tools/library_find.py <слова> [--book книга] [--lang язык]` — выдаёт книгу, главу и абзац.", "",
          "| книга (папка) | название | языки | глав | знаков, тыс. |", "|---|---|---|---|---|"]
    for b, P, counts in stat:
        l0 = P["langs"][0]
        L.append("| `%s` | %s | %s | %s | %s |" % (b, P["t"].get("ru") or P["t"][l0], " ".join(P["langs"]), "/".join(str(counts.get(l, 0)) for l in P["langs"]),
                                                "/".join(str(round(sum(x["n"] for x in P["toc"][l]) / 1000)) for l in P["langs"])))
    L += ["", "## Сценарии и стили — `assets/`", "", "| файл | назначение |", "|---|---|"]
    for f in sorted(glob.glob("assets/js/*.js")) + sorted(glob.glob("assets/css/*.css")):
        first = io.open(f, encoding="utf-8", errors="replace").read(400)
        m = re.search(r"/\*\s*(.*?)(\*/|\n)", first, flags=re.S)
        L.append("| `%s` | %s |" % (f, re.sub(r"\s+", " ", m.group(1)).strip()[:150] if m else ""))
    L += ["", "## Инструменты — `_tools/`", "", "| файл | назначение |", "|---|---|"]
    for f in sorted(glob.glob("_tools/*.py")):
        if os.path.basename(f).startswith(("patch_", "pull_", "chunk_", "extract_", "filter_")):
            continue
        first = io.open(f, encoding="utf-8", errors="replace").read(700)
        m = re.search(r'"""(.*?)(\n|""")', first, flags=re.S)
        L.append("| `%s` | %s |" % (f, re.sub(r"\s+", " ", m.group(1)).strip()[:160] if m else ""))
    L += ["", "Скрипты `patch_*.py` — разовые правки с датой в имени; они сохранены как журнал изменений и повторно ничего не меняют.", ""]
    io.open("FILE_MAP.md", "w", encoding="utf-8", newline="\n").write("\n".join(L))
    print("карта файлов записана: FILE_MAP.md")
sys.exit(1 if bad else 0)
