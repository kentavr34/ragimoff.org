# -*- coding: utf-8 -*-
"""Названия диагнозов в оглавлении «Клинической психиатрии» (14.11.2026).
В прежнем сайте у части заголовков было отрезано первое слово («Ve geçici…» вместо «Akut ve geçici…»).
Верные формы: EN/RU/TR — официальная МКБ-11 (icd11_terms), AZ — форма самого текста главы.
Использование: python klinik_title_fix.py [--fix]   (без --fix — только показать)
build_klinik.py вызывает apply_title(lang, code, t) — пересборка ошибку не вернёт."""
import io, os, re, sys, json, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

FIX = {   # (язык, код): (как было, как верно)
    ("az", "6B82"): ("Yemə pozuntusu", "Obur yemə pozuntusu"),
    ("az", "6C51"): ("Oynama pozuntusu", "Oyun oynama pozuntusu"),
    ("tr", "6A23"): ("Ve geçici psikotik bozukluk", "Akut ve geçici psikotik bozukluk"),
    ("tr", "6B43"): ("Bozukluğu", "Uyum bozukluğu"),
    ("tr", "6C51"): ("Oynama bozukluğu", "Oyun oynama bozukluğu"),
    ("tr", "6D33"): ("Dayalı cinsel sadizm bozukluğu", "Zora dayalı cinsel sadizm bozukluğu"),
    ("tr", "6D82"): ("Cisimciği hastalığı nedenli demans", "Lewy cisimciği hastalığı nedenli demans"),
    ("en", "6B21"): ("Dysmorphic disorder", "Body dysmorphic disorder"),
    ("en", "6B40"): ("Traumatic stress disorder", "Post-traumatic stress disorder"),
    ("en", "6D71"): ("Neurocognitive disorder", "Mild neurocognitive disorder"),
    ("en", "HA01.1"): ("Erectile dysfunction", "Male erectile dysfunction"),
    ("en", "HA03.0"): ("Early ejaculation (premature ejaculation, PE)", "Male early ejaculation (PE)"),
    ("ru", "6D80"): ("Деменция вследствие болезни альцгеймера", "Деменция вследствие болезни Альцгеймера"),
    ("ru", "6D82"): ("Деменция вследствие болезни с тельцами леви", "Деменция вследствие болезни с тельцами Леви"),
}


def apply_title(lang, code, t):
    f = FIX.get((lang, code))
    if f and t and (t == f[0] or t.startswith(f[0] + " (")):
        return f[1] + t[len(f[0]):]
    return t


def main(write):
    B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "books", "klinik-psixiatriya")
    p = os.path.join(B, "book.json")
    raw = io.open(p, encoding="utf-8").read()
    book = json.loads(raw)
    n = 0
    for lang, toc in book["toc"].items():
        for e in toc:
            new = apply_title(lang, e.get("code"), e.get("t"))
            if new != e.get("t"):
                print("toc", lang, e["code"], "«%s» → «%s»" % (e["t"], new)); e["t"] = new; n += 1
    for lang, tree in book.get("trees", {}).items():
        for sysname in ("icd", "dsm", "icd10"):
            for grp in tree.get(sysname, []):
                for it in grp.get("items", []):
                    new = apply_title(lang, it.get("id") or it.get("code"), it.get("t"))
                    if new != it.get("t"):
                        print("tree", lang, sysname, it.get("id"), "→", new); it["t"] = new; n += 1
    # страницы глав: подписи оглавления внутри страниц (span.bk-toc__t и подобные) — только точное совпадение текста элемента
    for (lang, code), (old, new) in FIX.items():
        for f in glob.glob(os.path.join(B, lang, "*.html")):
            s = io.open(f, encoding="utf-8").read()
            s2 = re.sub(r">(\s*)%s(\s*(?:\([^()<]*\))?\s*)<" % re.escape(old), lambda m: ">" + m.group(1) + new + m.group(2) + "<", s)
            if s2 != s:
                k = len(re.findall(r">(\s*)%s(\s*(?:\([^()<]*\))?\s*)<" % re.escape(old), s))
                print("html", lang, os.path.basename(f), k, "×", new); n += k
                if write:
                    io.open(f, "w", encoding="utf-8", newline="\n").write(s2)
    if write and n:
        io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(book, ensure_ascii=False, separators=(",", ":")) if "\n" not in raw.strip() else json.dumps(book, ensure_ascii=False, indent=1))
    print("ИСПРАВЛЕНИЙ:", n, "(записано)" if write else "(не записано)")


if __name__ == "__main__":
    main("--fix" in sys.argv)
