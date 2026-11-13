# -*- coding: utf-8 -*-
"""shop_facts.py — ЕДИНЫЙ ИСТОЧНИК сведений карточки книги (слово Кенана 13.11.2026: у всех книг один стандарт).

Карточка в каталоге и страница книги показывают одно и то же: обложка, название, автор, год издания, число страниц B5,
цена, две кнопки. Никаких «писем», «цитат», «Kitab N» в сведениях.
  • Страницы — по печатному PDF из папки Print проекта (тот же файл, что прошёл ворота печати); язык каталога без своей
    печатной книги (Фрейд выходит только на азербайджанском) — страницы азербайджанского издания.
    Книги без печатного B5 — оценка по объёму текста на сайте: знаков на страницу = медиана серии Фрейда (помечается est).
  • Год — год нашего издания (для Фрейда — Ragimoff, 2026); порядок Фрейда в каталоге — по году написания (поле wy).
Пишет _tools/shop_facts.json (отчёт: откуда каждое число) и поля meta / y / pages / year / wy в data/shop/index.<lang>.json.
Запускать ПОСЛЕДНИМ: build_shop.py → merge_books.py → shop_facts.py. Повторный запуск ничего не меняет.
  python _tools/shop_facts.py [--check]     # --check: только показать расхождения, ничего не писать"""
import io, os, re, sys, glob, json
import pymupdf
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
P = "D:/Projects"
UNIT = {"az": "səh.", "ru": "стр.", "en": "pp."}
FK = P + "/Freud/Print/Kitab_%s *.pdf"
VS = P + "/Freud/Print/vne_serii/%s"

# id: год издания, год написания (порядок Фрейда), PDF по языкам (glob; список = части сборника, страницы складываются)
SRC = {
    "klinik-psixiatriya": (2026, 0, {"az": P + "/Psychiatry/Print/Klinik_Psixiatriya_AZ_*.pdf", "ru": P + "/Psychiatry/Print/Klinik_Psixiatriya_RU_*.pdf", "en": P + "/Psychiatry/Print/Klinik_Psixiatriya_EN_*.pdf"}),
    "virus-viny": (2024, 0, {"az": P + "/Virus/Print/Gunahkarliq_Virusu_AZ_*_B5.pdf", "ru": P + "/Virus/Print/Virus_Viny_RU_*_B5.pdf", "en": P + "/Virus/Print/Guilt_Virus_EN_*_B5.pdf"}),
    "shizofreniya": (2025, 0, {"az": P + "/Pandemia/Print/Sizofreniya_AZ_*_B5.pdf", "ru": P + "/Pandemia/Print/Shizofreniya_RU_*_B5.pdf", "en": P + "/Pandemia/Print/Schizophrenia_EN_*_B5.pdf"}),
    "phoenix-era": (2026, 0, {"az": P + "/Phoenix/Print/Feniks_Erasi_AZ_*_B5.pdf", "ru": P + "/Phoenix/Print/Era_Feniksa_RU_*_B5.pdf", "en": P + "/Phoenix/Print/Phoenix_Era_EN_*_B5.pdf"}),
    "freud-gw01": (2026, 1892, {"az": FK % "01"}), "freud-gw02": (2026, 1900, {"az": FK % "02"}), "freud-gw04": (2026, 1901, {"az": FK % "03"}),
    "freud-gw05": (2026, 1904, {"az": FK % "04"}), "freud-gw06": (2026, 1905, {"az": FK % "05"}), "freud-gw07": (2026, 1906, {"az": FK % "06"}),
    "freud-gw08": (2026, 1909, {"az": FK % "07"}), "freud-gw09": (2026, 1912, {"az": FK % "08"}), "freud-gw10": (2026, 1913, {"az": FK % "09"}),
    "freud-gw11": (2026, 1916, {"az": FK % "10"}), "freud-gw12": (2026, 1917, {"az": FK % "11"}), "freud-gw13": (2026, 1920, {"az": FK % "12"}),
    "freud-gw14": (2026, 1925, {"az": FK % "13"}), "freud-gw15": (2026, 1933, {"az": FK % "14"}), "freud-gw16": (2026, 1932, {"az": FK % "15"}),
    # 13.11: работы вне серии свёрстаны в формате Letter (не B5) — до вёрстки B5 страницы этих книг считаются оценкой по объёму
    "freud-gw17": (2026, 1892, None),                     # Kitab_16 (B5, 96) + рефераты, рецензии, предисловие, «Психопатические персонажи» (Letter)
    "freud-fliesse-mektublari": (2026, 1887, {"az": FK % "17"}),
    # 13.11: письма Марте, переписка с Цвейгом и «Афоризмы» — одна книга (merge_books.py); прежние id в каталоге больше не стоят
    "freud-mektublar-aforizmler": (2026, 1882, {"az": VS % "Mektublar_ve_aforizmler_AZ_v*.pdf"}),
    "freud-yung-mektublari": (2026, 1906, {"az": VS % "Freud_Jung_Mektublar_AZ_v*.pdf"}),   # B5 13.11.2026, 581 стр.
    "freud-usaq-iflici": (2026, 1897, None),              # Print/vne_serii — Letter, 309 стр.
    "freud-koka-afaziya": (2026, 1884, None),             # Print/vne_serii — Letter, 41 + 119 стр.
}


def pdf_pages(pat):
    fs = sorted(f for f in glob.glob(pat) if "_replaced" not in f)
    if len(fs) != 1:
        raise SystemExit("ожидался один PDF по шаблону %s, найдено %d: %s" % (pat, len(fs), fs))
    return pymupdf.open(fs[0]).page_count, os.path.basename(fs[0])


ix = {b["id"]: b for b in json.load(io.open("books/index.json", encoding="utf-8"))["books"]}
ratio = []
for k, v in SRC.items():
    if k.startswith("freud-gw") and k != "freud-gw17" and v[2]:
        n, _ = pdf_pages(v[2]["az"])
        ratio.append(ix[k]["chars"]["az"] / n)
ratio.sort()
CPP = ratio[len(ratio) // 2]

facts = {"_": "собрано _tools/shop_facts.py; страницы — печатные PDF B5 (Print), est — оценка по объёму, %d знаков на страницу" % CPP}
for k, (year, wy, pdfs) in SRC.items():
    f = {"year": year, "wy": wy, "pages": {}, "src": {}}
    if pdfs is None:
        f["pages"]["az"] = max(1, round(ix[k]["chars"]["az"] / CPP))
        f["src"]["az"] = "оценка: %d знаков / %d" % (ix[k]["chars"]["az"], CPP)
        f["est"] = True
    else:
        for lang, pat in pdfs.items():
            parts = pat if isinstance(pat, list) else [pat]
            got = [pdf_pages(x) for x in parts]
            f["pages"][lang] = sum(n for n, _ in got)
            f["src"][lang] = " + ".join("%s (%d)" % (nm, n) for n, nm in got)
    facts[k] = f


def meta(f, lang):
    n = f["pages"].get(lang) or f["pages"]["az"]
    return "%d · %d %s" % (f["year"], n, UNIT[lang])


check = "--check" in sys.argv
changed, seen = 0, set()
for lang in ("az", "ru", "en"):
    p = "data/shop/index.%s.json" % lang
    d = json.load(io.open(p, encoding="utf-8"))
    for g in d["groups"]:
        for it in g["items"]:
            if it.get("small"):
                continue
            f = facts.get(it["id"])
            if not f:
                raise SystemExit("книги %s нет в SRC shop_facts.py — добавь её (страницы по печатному PDF)" % it["id"])
            seen.add(it["id"])
            new = {"meta": meta(f, lang), "y": str(f["year"]), "year": f["year"], "wy": f["wy"],
                   "pages": f["pages"].get(lang) or f["pages"]["az"]}
            for kk, vv in new.items():
                if it.get(kk) != vv:
                    if check:
                        print("%s %s %s: %r → %r" % (lang, it["id"], kk, it.get(kk), vv))
                    it[kk] = vv
                    changed += 1
    if not check:
        s = json.dumps(d, ensure_ascii=False, indent=1) + "\n"
        if io.open(p, encoding="utf-8").read() != s:
            io.open(p + ".new", "w", encoding="utf-8", newline="\n").write(s)
            os.replace(p + ".new", p)
miss = sorted(set(SRC) - seen)
if not check:
    s = json.dumps(facts, ensure_ascii=False, indent=1) + "\n"
    io.open("_tools/shop_facts.json.new", "w", encoding="utf-8", newline="\n").write(s)
    os.replace("_tools/shop_facts.json.new", "_tools/shop_facts.json")
print("сведения книг: изменено полей %d%s; книг в каталоге %d; оценок по объёму: %s%s" % (
    changed, " (только показ)" if check else "", len(seen), ", ".join(k for k in facts if k != "_" and facts[k].get("est")) or "нет",
    "; нет в каталоге: " + ", ".join(miss) if miss else ""))
