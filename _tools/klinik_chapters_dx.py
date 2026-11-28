# -*- coding: utf-8 -*-
"""28.11.2026: названия глав МКБ-11 «Клинической психиатрии» на сайте — по ВОЗ (блоки МКБ-11; AZ — перевод названия
ВОЗ), из заголовков блоков исправленных версий базы (dx_heads.json). ТОЛЬКО там, где это название главы:
  (1) текст ссылки, ведущей на страницу главы (…/<id главы>.html или ?p=<id главы>), в т.ч. вложенный span;
  (2) на странице самой главы: <title>, <h1 class="rdr__h">, content у meta (description/og/twitter), "name"/"headline" в JSON-LD.
Слепая замена по всем файлам (klinik_apply_rest2) задела глоссарий, таблицы и одноимённые расстройства — отменена.
  python _tools/klinik_chapters_dx.py <dx_heads.json> [--dry]"""
import glob, html, io, json, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
H = json.load(open(sys.argv[1], encoding="utf-8"))
dry = "--dry" in sys.argv
# прежние названия глав — из book.json ДО правки меню (--old <файл>; по умолчанию текущий book.json)
OLD = sys.argv[sys.argv.index("--old") + 1] if "--old" in sys.argv else "books/klinik-psixiatriya/book.json"
book = json.load(open(OLD, encoding="utf-8"))


def cf(s, L):
    if L in ("tr", "az"):
        s = s.replace("I", "ı").replace("İ", "i")
    return re.sub(r"\s+", " ", s.replace("ё", "е")).strip().casefold()


def sent(s, L, old):
    """название из шапки (ПРОПИСНЫМИ) → вид меню; прежнее написание, если совпадает без учёта регистра (как klinik_trees_dx)"""
    s = re.sub(r"^\d[A-Z][0-9A-Z]{2}–\d[A-Z][0-9A-Z]{2}\s+", "", s)
    if cf(s, L) == cf(old, L):
        return old
    lo = (lambda x: x.lower()) if L not in ("tr", "az") else (lambda x: x.replace("I", "ı").replace("İ", "i").lower())
    low = lo(s)
    return low[:1].upper() + low[1:]
tot, files = 0, 0
for L in ("az", "ru", "tr", "en"):
    if L not in H:
        continue
    CH = {}                                                     # id главы → (старое, новое)
    for g in book["trees"][L]["icd"]:
        new_up = H[L]["blocks"].get(g.get("code"))
        if new_up and g.get("id"):
            new = sent(new_up, L, g["t"])
            if new != g["t"]:
                CH[g["id"]] = (g["t"], new)
    if not CH:
        continue
    for f in sorted(glob.glob("books/klinik-psixiatriya/%s/*.html" % L) + glob.glob("%s/read/klinik-psixiatriya/*.html" % L)):
        t = io.open(f, encoding="utf-8", newline="").read()
        t2, n = t, 0
        for gid, (old, new) in CH.items():
            eo, en_ = html.escape(old, quote=False), html.escape(new, quote=False)
            # (1) ссылки на главу: <a href="…gid.html" …>[<span …>]СТАРОЕ[</span>]</a>
            rx = re.compile(r'(<a\b[^>]*href="[^"]*(?:/%s\.html|[?&]amp;p=%s|[?&]p=%s)[^"]*"[^>]*>(?:<span\b[^>]*>[^<]*</span>)*(?:<span\b[^>]*>)?)%s(?=(?:</span>)?</a>)'
                            % (re.escape(gid), re.escape(gid), re.escape(gid), re.escape(eo)))
            t2, k = rx.subn(lambda m: m.group(1) + en_, t2)
            n += k
            # (2) страница самой главы
            if os.path.basename(f) == gid + ".html":
                for prx in (r'(<title>[^<]*?)%s', r'(<h1 class="rdr__h">)%s', r'(<meta (?:property="og:title"|name="twitter:title") content="[^"]*?)%s', r'("(?:name|headline)": ")%s'):
                    # не повторять, если новое название уже стоит (новое может начинаться со старого)
                    t2, k = re.subn(prx % re.escape(eo) + "(?!" + re.escape(en_[len(eo):]) + ")" if en_.startswith(eo) else prx % re.escape(eo),
                                    lambda m: m.group(1) + en_, t2)
                    n += k
        if n:
            files += 1
            tot += n
            if not dry:
                with io.open(f + ".tmp", "w", encoding="utf-8", newline="") as w:
                    w.write(t2)
                os.replace(f + ".tmp", f)
    print(L, "глав к замене:", len(CH))
print("замен:", tot, "| файлов:", files, "(проба)" if dry else "")
