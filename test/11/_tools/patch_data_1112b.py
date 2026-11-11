# -*- coding: utf-8 -*-
"""Правки данных по первому кругу критика (12.11.2026). Повторный запуск ничего не меняет.
1. corporate: карточки «23+ / 100% / IPAS» — крупные знаки с исходной страницы возвращены (поле n).
2. law: подзаголовок героя на исходной странице оборван на запятой — оставлено законченное предложение.
3. Русские заголовки карточек и разделов: «Стойкая Грусть» → «Стойкая грусть» (на новом сайте заголовки пишутся как предложения);
   имена собственные и сокращения не трогаются. Список изменений печатается.
Запуск: python patch_data_1112b.py [show] — show только показывает, что изменится."""
import io, os, re, json, glob, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ROOT = os.path.abspath(os.path.join(D, "..", ".."))
SHOW = len(sys.argv) > 1 and sys.argv[1] == "show"
KEEP = set("""Кенан Кенана Кенаном Рагимов Рагимова Рагимовой Рагимову Самира Самиры Самирой Рустамова Бехтерева Карвасарского Карвасарский Вид Баку Азербайджан Азербайджана
Азербайджане Азербайджанской Республики Россия России Российской Федерации Санкт-Петербург Санкт-Петербурга Петербург Шотландия Гонконг Гянджа Школа Институт Институте Института Министерства
Закон Закона Соглашение Соглашения Рособрнадзор Рособрнадзора Интернет Бога Фрейд Фрейда Бек Бека Готтман Готтмана Международной Международная Клиническая Психиатрия Общая Психотерапия Эра Феникса
Вирус Вины Драма Сабины""".split())


def sentence(s):
    """Каждое Слово С Заглавной → как в предложении. Не трогаем: первое слово, слова после точки/двоеточия/тире-вопроса, имена из KEEP, сокращения, слова в кавычках «…»."""
    if "<" in s or len(s) > 90:
        return s
    words = s.split(" ")
    caps = [w for w in words[1:] if re.match(r"^[А-ЯЁ][а-яё]{2,}", w)]
    if not caps:
        return s
    out, inq, prev = [], False, ""
    for i, w in enumerate(words):
        core = re.sub(r"^[«(\"“]+|[»).,:;!?\"”]+$", "", w)
        opened = w.startswith("«") or w.startswith("“")
        if i > 0 and not inq and not opened and re.match(r"^[А-ЯЁ][а-яё]{2,}$", core) and core not in KEEP and not re.search(r"[.!?:]$", prev) and prev not in ("—", "–", "·", "/"):
            w = w.replace(core, core[0].lower() + core[1:], 1)
        if w.count("«") > w.count("»"):
            inq = True
        if w.count("»") > w.count("«"):
            inq = False
        out.append(w)
        prev = w
    return " ".join(out)


def walk(o, f, key=None):
    if isinstance(o, dict):
        for k, v in list(o.items()):
            if isinstance(v, str) and k in ("t", "h", "title"):
                n = f(v)
                if n != v:
                    o[k] = n
            else:
                walk(v, f, k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            if isinstance(v, list) and key == "items" and v and isinstance(v[0], str) and len(v) == 2:   # вопрос-ответ
                continue
            walk(v, f, key)


changed = []
for fn in sorted(glob.glob(os.path.join(D, "data", "*", "*.json"))):
    name = os.path.relpath(fn, os.path.join(D, "data"))
    if "index." in name or name.startswith("blog"):
        continue
    d = json.load(io.open(fn, encoding="utf-8"))
    before = json.dumps(d, ensure_ascii=False)
    lang = d.get("lang")
    if d.get("slug") == "corporate" or name.startswith("page" + os.sep + "corporate"):
        src = io.open(os.path.join(ROOT, d["src"]), encoding="utf-8").read()
        nums = re.findall(r'class="why-num">([^<]+)<', src)
        for b in d["blocks"]:
            if b["type"] == "cards" and b.get("num") and len(b["items"]) == len(nums) == 3 and "n" not in b["items"][0] and nums[0].startswith("23"):
                for it, n in zip(b["items"], nums):
                    it["n"] = n
    if name.startswith("page" + os.sep + "law") and d.get("lead", "").rstrip().endswith(","):
        m = re.match(r"^(.*?[.!?])\s+[^.!?]*,\s*$", d["lead"], flags=re.S)
        if m:
            d["lead"] = m.group(1)
    if lang == "ru":
        def f(v, name=name):
            n = sentence(v)
            if n != v:
                changed.append((name, v, n))
            return n
        walk(d, f)
    after = json.dumps(d, ensure_ascii=False)
    if after != before and not SHOW:
        json.dump(d, io.open(fn, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
        print("изменён", name)
for n, a, b in changed:
    print("  %s: %s → %s" % (n, a, b))
print("заголовков изменено:", len(changed))
