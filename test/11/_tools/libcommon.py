# -*- coding: utf-8 -*-
"""Общее для сборщиков библиотеки: единый вид паспорта книги (book.json).
Паспорт — единственный источник сведений о книге для каталога, страницы книги и читалки:
адрес (id = имя папки), названия по языкам, обложка. Обложки лежат внутри новой версии —
assets/img/books/covers/ — и не зависят от старого сайта.
  • у авторских книг готовая обложка с названием на каждом языке: coverKey → covers/<ключ>-<язык>.jpg;
  • у остальных — фактура без надписи: cover → /images/books/covers/<файл>, название набирается поверх."""
import io, os, re, shutil
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ROOT = os.path.abspath(os.path.join(D, "..", ".."))
COVERS = os.path.join(D, "assets", "img", "books", "covers")
OWN = {"klinik-psixiatriya": "klinik", "virus-viny": "guilt", "shizofreniya": "pandemic", "phoenix-era": "phoenix"}      # папка книги → ключ готовой обложки
OWN_BY_KEY = dict((v, k) for k, v in OWN.items())


def local_cover(src):
    """/books/covers/x.jpg?v=… (старый сайт) → копия в assets/img/books/covers/x.jpg, в данных — /images/books/covers/x.jpg."""
    if not src:
        return ""
    if src.startswith("/images/"):
        return src
    name = os.path.basename(src.split("?")[0])
    old = os.path.join(ROOT, src.split("?")[0].lstrip("/").replace("/", os.sep))
    new = os.path.join(COVERS, name)
    if os.path.isfile(old) and (not os.path.isfile(new) or os.path.getsize(new) != os.path.getsize(old)):
        os.makedirs(COVERS, exist_ok=True)
        shutil.copyfile(old, new)
    return "/images/books/covers/" + name if os.path.isfile(new) else src


# названия книг на английском пишутся по правилам заглавия (как на обложке и в каталоге)
TITLE_FIX = {("virus-viny", "en"): "The Guilt Virus", ("shizofreniya", "en"): "Schizophrenia. A Pandemic of Madness"}


def finish(P):
    """Привести паспорт к единому виду перед записью."""
    for (b, l), t in TITLE_FIX.items():
        if P["id"] == b and l in P.get("t", {}):
            P["t"][l] = t
    if P["id"] in OWN:
        P["coverKey"] = OWN[P["id"]]
        P["cover"] = ""
    else:
        P["cover"] = local_cover(P.get("cover", ""))
    return P
