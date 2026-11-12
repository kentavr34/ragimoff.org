# -*- coding: utf-8 -*-
"""Сторож дословности: каждая строка текста в data/<kind>/<slug>.<lang>.json должна быть в исходной странице (поле src).
Запуск: python verify_data.py <файл.json> [ещё файлы…]   |   python verify_data.py --all
Не проверяются адреса и служебные поля. Код возврата 1, если есть расхождения."""
import sys, re, json, html, io, glob, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\Projects\Ragimoff\old_versions\2026-11-12_site_before_v11"   # прежний сайт: источник текстов и картинок, только чтение (с 12.11.2026 версия 11 — корень сайта)
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")   # данные новой версии — в корне сайта
SKIP_KEYS = {"type", "src", "img", "yt", "set", "ids", "slug", "lang", "cover", "num", "kind", "date"}
TYPES = {"cards", "groups", "timeline", "gallery", "videos", "who", "prices", "articles", "faq", "list", "text", "stats",
         "table", "quotes", "contact", "links", "note", "figure", "cta", "prose", "sources"}


def norm(s):
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s).replace(" ", " ").replace(" ", " ").replace("­", "")
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s+([,.;:!?»)”])", r"\1", s)
    s = re.sub(r"([«(“])\s+", r"\1", s)
    return s.strip().lower().replace(u"i̇", "i").replace(u"ı", "i")      # азербайджанские İ/I/ı сравниваются как одна буква


def is_url(s):
    return bool(re.match(r"^(https?:|mailto:|tel:|/|#|\.\./)", s)) or bool(re.search(r"\.(html|jpg|jpeg|png|webp|pdf)([?#].*)?$", s))


def leaves(o, key=None, path=""):
    if isinstance(o, str):
        if key in SKIP_KEYS or is_url(o) or not o.strip():
            return
        yield path, o
    elif isinstance(o, list):
        if key == "items" and all(isinstance(x, str) for x in o) and path.endswith("articles"):
            return
        for i, x in enumerate(o):
            yield from leaves(x, key, "%s[%d]" % (path, i))
    elif isinstance(o, dict):
        t = o.get("type")
        for k, v in o.items():
            if t == "articles" and k == "items":
                continue
            yield from leaves(v, k, path + "." + k if path else k)


def check(fn):
    if os.sep + "law" + os.sep in fn:      # блок «Юридические основы» — свой формат, собирается build_law.py из проверенной страницы
        return []
    d = json.load(io.open(fn, encoding="utf-8"))
    bad = []
    for k in ("slug", "lang", "src", "title", "blocks"):
        if k not in d:
            bad.append(("корень", "нет поля " + k))
    src = os.path.join(ROOT, d.get("src", ""))
    if not os.path.isfile(src):
        return [("src", "нет исходной страницы: %s" % d.get("src"))]
    page = norm(io.open(src, encoding="utf-8").read())
    for b in d.get("blocks", []):
        if b.get("type") not in TYPES:
            bad.append(("blocks", "неизвестный type: %r" % b.get("type")))
    for path, s in leaves(d):
        if "blocks" in path and re.search(r"<(?!/?(strong|em|b|i|a|br|sup|sub)[ >/])[a-zA-Z/]", s) and not any(x.get("type") in ("prose", "sources") for x in d["blocks"]):
            bad.append((path, "неразрешённая разметка: " + s[:100]))
        n = norm(s)
        if d.get("edited"):          # страница правлена владельцем после переноса (поле edited — дата и суть правки): дословность со старой страницей не требуется
            continue
        if n and n not in page:
            bad.append((path, s[:140]))
    return bad


def main():
    files = sys.argv[1:]
    if files == ["--all"]:
        files = sorted(glob.glob(os.path.join(DATA, "*", "*.json")))
    total = 0
    for fn in files:
        if os.path.basename(fn).startswith("index."):
            continue
        bad = check(fn)
        total += len(bad)
        print("%s: %d расхождений" % (os.path.relpath(fn, DATA), len(bad)))
        for p, s in bad[:40]:
            print("   ", p, "→", s)
    print("ИТОГО: %d расхождений в %d файлах" % (total, len(files)))
    sys.exit(1 if total else 0)


main()
