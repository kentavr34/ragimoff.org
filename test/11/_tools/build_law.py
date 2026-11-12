# -*- coding: utf-8 -*-
"""Блок «Юридические основы деятельности» для страниц «Общая психология» и «Клиническая психология».
Решение владельца (11.11 и 12.11.2026): отдельной страницы нет; это блок сразу после фото дипломов —
вопросы и ответы с цитатами из законов и ссылками на законы на портале e‑qanun.az.
Источник: перенесённая страница qanuni-esaslar (data/page/law.<lang>.json, после сборки лежит в _agent/archive/law_page/)
и общие вопросы программ (assets/js/programs.js, FAQ_*). Результат: data/law/law.<lang>.json.
Запуск: python build_law.py   (повторный запуск даёт тот же файл)."""
import io, os, sys, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
H = {"ru": ("Юридические основы деятельности", "Вопросы и ответы с цитатами из законов Азербайджанской Республики. Каждый документ можно открыть на портале e‑qanun.az и проверить самостоятельно.",
            "Документы и лицензия института", "Цитата из закона"),
     "az": ("Fəaliyyətin hüquqi əsasları", "Azərbaycan Respublikasının qanunlarından sitatlarla suallar və cavablar. Hər sənədi e‑qanun.az portalında açıb özünüz yoxlaya bilərsiniz.",
            "İnstitutun sənədləri və lisenziyası", "Qanundan sitat"),
     "en": ("Legal basis for practice", "Questions and answers with quotations from the laws of the Republic of Azerbaijan. Every document can be opened on the e‑qanun.az portal and checked independently.",
            "The institute’s documents and licence", "Quotation from the law")}
# вопрос (номер в FAQ_*) → группа закона на старой странице
LAWMAP = {3: 0, 4: 1, 5: 2, 6: 3}

js = "import('./assets/js/programs.js').then(m => { const o = {}; for (const l of ['ru','az','en']) o[l] = m.LAW_FAQ[l]; process.stdout.write(JSON.stringify(o)); })"
faq = json.loads(subprocess.run(["node", "--input-type=module", "-e", js.replace("import('./", "import('file:///" + D.replace("\\", "/") + "/")], capture_output=True, check=True).stdout.decode("utf-8"))

def split_quote(q):
    """«Статья 1.0.2 — Понятие «психолог» «Психолог — лицо…»» → [подпись, текст, это_цитата].
    Цитата начинается с кавычки, за которой идёт заглавная буква или ещё одна кавычка; без кавычек — деление после года."""
    marks = u"«\"“'"
    cand = [i for i in range(8, min(len(q) - 2, 75)) if q[i] == " " and q[i + 1] in marks and (q[i + 2].isupper() or q[i + 2] in marks) and u"—" in q[:i]]
    if cand:                                   # в подписи тоже бывает слово в кавычках с заглавной — цитата начинается с последней такой кавычки
        i = cand[-1]
        return [q[:i].strip(), q[i + 1:].strip(), True]
    w = q.split(" ")
    for k, t in enumerate(w[:14]):
        if len(t) == 4 and t.isdigit() and t[:2] in ("19", "20"):
            return [" ".join(w[:k + 1]), " ".join(w[k + 1:]), False]
    return ["", q, False]


for l in ("ru", "az", "en"):
    src = "data/page/law.%s.json" % l
    if not os.path.exists(src):
        src = "_agent/archive/law_page/law.%s.json" % l
    d = json.load(io.open(src, encoding="utf-8"))
    B = d["blocks"]
    groups = [b for b in B if b["type"] == "groups"][0]["items"]
    links = [b for b in B if b["type"] == "links"]
    gal = [b for b in B if b["type"] == "gallery"][0]["items"]
    assert len(groups) == 4 and len(links[0]["items"]) == 4 and len(links[1]["items"]) == 3 and len(faq[l]) == 7
    items = []
    for i, (q, a) in enumerate(faq[l]):
        it = {"q": q, "a": a}
        if i in LAWMAP:
            g = groups[LAWMAP[i]]
            lk = links[0]["items"][LAWMAP[i]]
            it["law"] = g["t"]
            it["quotes"] = [split_quote(x) for x in g["list"]]
            it["link"] = [lk[0], lk[1]]
        if i == 1:
            it["links"] = [links[1]["items"][0][:2]]
        if i == 2:
            it["links"] = [x[:2] for x in links[1]["items"][1:]]
        items.append(it)
    out = {"lang": l, "src": d["src"], "h": H[l][0], "sub": H[l][1], "docs": H[l][2], "quote": H[l][3], "gallery": gal, "items": items}
    os.makedirs("data/law", exist_ok=True)
    json.dump(out, io.open("data/law/law.%s.json" % l, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    print("data/law/law.%s.json: вопросов %d, документов %d" % (l, len(items), len(gal)))
