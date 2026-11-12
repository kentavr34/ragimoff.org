# -*- coding: utf-8 -*-
"""Правки владельца от 12.11.2026 (ответы на список расхождений). Повторный запуск ничего не меняет.
 1. Энурез: фраза о возможном назначении психотропных препаратов убрана (три языка).
 2. Протоколы: практика 2003–2026 (23 года); энурез — более 1 000 детей, более 250 в 2025 году, из них более 100 бесплатно.
 5. Энурез: название «Ночной энурез (ночное недержание мочи)» и единый герой на трёх языках.
 6. Блог называется RAGIMOFF Bloq на всех языках, подзаголовок единый.
 7. Иероглиф в русском тексте семейной терапии.
 8. «Этап 4. Тщательная проработка».
 9. Языковые аномалии азербайджанской страницы тренингов для компаний.
12. Кенан: три книги в хронологии есть на всех языках.
Запуск: python patch_owner_1112.py"""
import io, os, sys, json, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
LOG = []


def edit(fn, pairs, need=True):
    """pairs: [(старое, новое)] — по тексту файла. Старого нет, а новое есть → уже применено."""
    s = io.open(fn, encoding="utf-8").read()
    o = s
    for a, b in pairs:
        if a in s:
            s = s.replace(a, b)
        elif b in s or not need:
            continue
        else:
            raise SystemExit("НЕ НАЙДЕНО в %s: %s" % (fn, a[:90]))
    if s != o:
        json.loads(s)
        io.open(fn, "w", encoding="utf-8", newline="\n").write(s)
        LOG.append(fn)


# ---------- 1. энурез: без фразы о психотропных препаратах ----------
edit("data/cons/enurez.ru.json", [(
    "следующий этап включает двунаправленное лечение — с учётом глубины сна, в исключительных случаях и только под строгим кардиологическим контролем может рассматриваться назначение психотропных препаратов. При доказанном",
    "следующий этап включает двунаправленное лечение. При доказанном")])
edit("data/cons/enurez.az.json", [(
    "növbəti mərhələdə 2 istiqamətli müalicə davam edir — yuxunun dərinliyini nəzərə alaraq yalnız ciddi kardioloji nəzarət altında istisnai hallarda psixotrop preparatların təyini nəzərə alına bilər. Bu siyahıda mayenin həcmi də çox olduqda",
    "növbəti mərhələdə 2 istiqamətli müalicə davam edir. Mayenin həcmi çox olduqda")])
edit("data/cons/enurez.en.json", [(
    "the next stage involves bidirectional treatment — taking sleep depth into account; in exceptional cases and only under strict cardiological monitoring, psychotropic drugs may be considered. Where",
    "the next stage involves bidirectional treatment. Where")])

# ---------- 5. энурез: название и герой ----------
NAME = {"ru": "Ночной энурез (ночное недержание мочи)", "az": "Gecə enurezi (gecə sidik buraxma)", "en": "Nocturnal enuresis (bedwetting)"}
LEAD = {"ru": "1 000+ детей за 23 года. Без единого медикамента. Только терапия по международным протоколам: комплексная диагностика и лечение.",
        "az": "23 ildə 1 000+ uşaq. Bir dənə də dərman olmadan. Yalnız beynəlxalq protokollar üzrə terapiya: kompleks diaqnostika və müalicə.",
        "en": "1,000+ children over 23 years. Without a single medication. Therapy only, following international protocols: comprehensive assessment and treatment."}
for l in NAME:
    fn = "data/cons/enurez.%s.json" % l
    d = json.load(io.open(fn, encoding="utf-8"))
    if d["title"] != NAME[l] or d["lead"] != LEAD[l]:
        d["title"], d["lead"] = NAME[l], LEAD[l]
        json.dump(d, io.open(fn, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
        LOG.append(fn)
    fn = "data/cons/index.%s.json" % l
    d = json.load(io.open(fn, encoding="utf-8"))
    for it in d["items"]:
        if it["slug"] == "enurez" and it["title"] != NAME[l]:
            it["title"] = NAME[l]
            json.dump(d, io.open(fn, "w", encoding="utf-8", newline="\n"), ensure_ascii=False)
            LOG.append(fn)

# ---------- 2. протоколы: годы практики ----------
edit("data/blog/depressiya-protokol.ru.json", [("клиническая практика 2008–2025", "клиническая практика 2003–2026"), ("Клиническая практика 2008–2025", "Клиническая практика 2003–2026"),
                                               ("17 лет", "23 года"), ("Этап 4. Всестороннее проработка", "Этап 4. Тщательная проработка")], need=False)
edit("data/blog/depressiya-protokol.az.json", [("klinik praktika 2008–2025", "klinik praktika 2003–2026"), ("Klinik praktika 2008–2025", "Klinik praktika 2003–2026"),
                                               ("17 illik", "23 illik"), ("Etap 4. Hərtərəfli işləmə", "Etap 4. Dərindən işləmə")], need=False)
edit("data/blog/depressiya-protokol.en.json", [("clinical practice 2008–2025", "clinical practice 2003–2026"), ("Clinical practice 2008–2025", "Clinical practice 2003–2026"),
                                               ("17 years", "23 years"), ("Stage 4. Comprehensive Working-Through", "Stage 4. Thorough working-through")], need=False)
edit("data/blog/enurez-protokol.ru.json", [
    ("клиническая практика 2018–2025", "клиническая практика 2003–2026"),
    ("на основе клинической практики n=240 пациентов: 80% полная ремиссия", "на основе клинической практики 2003–2026 годов (более 1 000 детей): 80% полная ремиссия"),
    ("Клиническая практика 2018–2025 (детский энурез). Баку, n=240.", "Клиническая практика 2003–2026, Баку. Детский энурез: более 1 000 детей; только в 2025 году — более 250, из них более 100 бесплатно (дети шахидов, гази, ветеранов и малообеспеченных семей).")], need=False)
edit("data/blog/enurez-protokol.az.json", [
    ("klinik praktika 2018–2025", "klinik praktika 2003–2026"),
    ("n=240 pasiyent klinik praktikası əsasında 80% halda tam remissiya nəticəsi", "2003–2026-cı illərin klinik praktikası (1 000-dən çox uşaq) əsasında 80% halda tam remissiya nəticəsi"),
    ("Klinik praktika 2018–2025 (uşaq enurezi). Bakı, n=240.", "Klinik praktika 2003–2026, Bakı. Uşaq enurezi: 1 000-dən çox uşaq; yalnız 2025-ci ildə 250-dən çox, onlardan 100-dən çoxu ödənişsiz (şəhid, qazi, veteran və aztəminatlı ailələrin uşaqları).")], need=False)
edit("data/blog/enurez-protokol.en.json", [
    ("clinical practice 2018–2025", "clinical practice 2003–2026"),
    ("based on clinical practice with n=240 patients: 80% full remission", "based on clinical practice in 2003–2026 (more than 1,000 children): 80% full remission"),
    ("Clinical practice 2018–2025 (childhood enuresis). Baku, n=240.", "Clinical practice 2003–2026, Baku. Childhood enuresis: more than 1,000 children; over 250 in 2025 alone, more than 100 of them free of charge (children of martyrs, war veterans and low-income families).")], need=False)
edit("data/blog/index.ru.json", [("клиническая практика 2008–2025", "клиническая практика 2003–2026"), ("17 лет практики", "23 года практики"), ("На основе 17 лет клинической практики", "На основе 23 лет клинической практики"),
                                 ("n=240 клинических случаев, полная ремиссия в 80% случаев", "Более 1 000 детей за 2003–2026 годы, полная ремиссия в 80% случаев")], need=False)
edit("data/blog/index.az.json", [("klinik praktika 2008–2025", "klinik praktika 2003–2026"), ("17 illik", "23 illik"),
                                 ("n=240 klinik praktika, 80% halda tam remissiya", "2003–2026-cı illərdə 1 000-dən çox uşaq, 80% halda tam remissiya")], need=False)
edit("data/blog/index.en.json", [("clinical practice 2008–2025", "clinical practice 2003–2026"), ("17 years", "23 years"),
                                 ("n=240 clinical cases, full remission in 80% of cases", "More than 1,000 children in 2003–2026, full remission in 80% of cases")], need=False)

# ---------- 6. блог ----------
BLOG = {"ru": ("RAGIMOFF Bloq", "Клинические статьи, научные исследования, психологические решения и терапевтические протоколы."),
        "az": ("RAGIMOFF Bloq", "Klinik məqalələr, elmi araşdırmalar, psixoloji həll yolları və terapevtik protokollar."),
        "en": ("RAGIMOFF Bloq", "Clinical articles, scientific research, psychological solutions and therapeutic protocols.")}
for l, (t, ld) in BLOG.items():
    fn = "data/blog/index.%s.json" % l
    d = json.load(io.open(fn, encoding="utf-8"))
    if d.get("title") != t or d.get("lead") != ld:
        d["title"], d["lead"] = t, ld
        json.dump(d, io.open(fn, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
        LOG.append(fn)

# ---------- 7. иероглиф ----------
edit("data/cons/aile-terapiyasi.ru.json", [("более長 длительной", "более длительной")], need=False)

# ---------- 9. азербайджанская страница тренингов ----------
edit("data/page/corporate.az.json", [("Oflayn / Online", "Əyani / Onlayn"), ("Fərdi offer", "Fərdi təklif"), ("Burn-out profilaktikası", "Tükənmənin profilaktikası"),
                                     ("Onboarding psixologiyası", "Yeni işçinin adaptasiyası psixologiyası"), ("Metodologiya: KBT, NLP", "Metodologiya: KDT, NLP"),
                                     ("Stres idarəetməsi sahə işçiləri üçün", "Səyyar işçilər üçün stresin idarə olunması"), ("Emosional intellekt satışda", "Satışda emosional intellekt")], need=False)
edit("data/page/corporate.ru.json", [("Офлайн / Онлайн", "Очно / Онлайн"), ("Методология: КБТ, НЛП", "Методология: КПТ, НЛП"), ("Психология онбординга", "Психология адаптации нового сотрудника")], need=False)
edit("data/page/corporate.en.json", [("Offline / Online", "In person / Online")], need=False)

# ---------- 12. Кенан: книги в хронологии на всех языках ----------
BOOKS = {
    "ru": [{"y": "2026", "t": "Зигмунд Фрейд — на азербайджанском языке", "d": "Впервые в Азербайджане — перевод всех книг Зигмунда Фрейда на азербайджанский язык.", "a": ["Познакомиться с книгами →", "/books/"]},
           {"y": "2025", "t": "Шизофрения: пандемия безумия", "d": "Книга о клинической и психологической картине психоза.", "a": ["Познакомиться с книгой →", "/books/shizofreniya/"]},
           {"y": "2024", "t": "Вирус вины", "d": "Книга об освобождении от чувства вины, разрушающего жизнь.", "a": ["Познакомиться с книгой →", "/books/virus-viny/"]}],
    "en": [{"y": "2026", "t": "Sigmund Freud — in Azerbaijani", "d": "A first for Azerbaijan — the translation of all of Sigmund Freud’s books into Azerbaijani.", "a": ["See the books →", "/books/"]},
           {"y": "2025", "t": "Schizophrenia: the pandemic of madness", "d": "A book on the clinical and psychological picture of psychosis.", "a": ["See the book →", "/books/shizofreniya/"]},
           {"y": "2024", "t": "The guilt virus", "d": "A book about freeing yourself from the guilt that ruins a life.", "a": ["See the book →", "/books/virus-viny/"]}]}
for l, add in BOOKS.items():
    fn = "data/spec/kenan.%s.json" % l
    d = json.load(io.open(fn, encoding="utf-8"))
    for b in d["blocks"]:
        if b["type"] == "timeline" and len(b["items"]) == 12:
            b["items"][1:1] = add
            json.dump(d, io.open(fn, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
            LOG.append(fn)

for f in sorted(set(LOG)):
    print("изменён", f)
print("файлов изменено:", len(set(LOG)))
