# -*- coding: utf-8 -*-
"""Тренинги для компаний (решение владельца 12.11.2026, п. 4): два списка («3 программы» и «Корпоративные тренинги»)
объединены в один из семи программ с принятыми в бизнес-обучении названиями; заголовок и подзаголовок героя
одинаковы по смыслу на трёх языках. Повторный запуск ничего не меняет."""
import io, os, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
HERO = {"ru": ("Корпоративные тренинги", "Продажи, лидерство, управление, HR, тайм-менеджмент, командообразование и стресс-менеджмент — корпоративная психология на научной основе. Индивидуальная программа под потребности вашей компании."),
        "az": ("Korporativ təlimlər", "Satış, liderlik, idarəetmə, HR, vaxtın idarə olunması, komanda quruculuğu və stresin idarə olunması — elmi əsaslı korporativ psixologiya. Şirkətinizin ehtiyaclarına uyğun fərdi proqram."),
        "en": ("Corporate training", "Sales, leadership, management, HR, time management, team building and stress management — corporate psychology on a scientific basis. An individual programme tailored to your company’s needs.")}
HEAD = {"ru": "Семь программ", "az": "Yeddi proqram", "en": "Seven programmes"}
# порядок итогового списка: (откуда, номер, название, метка)
NAMES = {"ru": [("g", 0, "Школа продаж", "Продажи"), ("g", 1, "Лидерство", "Лидерство"), ("c", 1, "Управленческие навыки", "Менеджмент"), ("g", 2, "Управление персоналом (HR)", "HR"),
                ("c", 2, "Тайм-менеджмент", "Время"), ("c", 4, "Командообразование (тимбилдинг)", "Команда"), ("c", 5, "Стресс-менеджмент", "Стресс")],
         "az": [("g", 0, "Satış məktəbi", "Satış"), ("g", 1, "Liderlik", "Liderlik"), ("c", 1, "İdarəetmə bacarıqları", "Menecment"), ("g", 2, "İnsan resurslarının idarə olunması (HR)", "HR"),
                ("c", 2, "Vaxtın idarə olunması (taym-menecment)", "Vaxt"), ("c", 4, "Komanda quruculuğu (timbildinq)", "Komanda"), ("c", 5, "Stresin idarə olunması (stres-menecment)", "Stres")],
         "en": [("g", 0, "Sales school", "Sales"), ("g", 1, "Leadership", "Leadership"), ("c", 1, "Management skills", "Management"), ("g", 2, "Human resources management (HR)", "HR"),
                ("c", 2, "Time management", "Time"), ("c", 4, "Team building", "Team"), ("c", 5, "Stress management", "Stress")]}
for l in ("ru", "az", "en"):
    fn = "data/page/corporate.%s.json" % l
    d = json.load(io.open(fn, encoding="utf-8"))
    B = d["blocks"]
    if B[0]["type"] == "groups" and len(B[0]["items"]) == 7:
        print("уже применено:", fn)
        continue
    assert B[0]["type"] == "groups" and len(B[0]["items"]) == 3 and B[2]["type"] == "cards" and len(B[2]["items"]) == 6, fn
    g, c = B[0]["items"], B[2]["items"]
    items = []
    for kind, i, name, meta in NAMES[l]:
        if kind == "g":
            it = dict(g[i])
            it["t"], it["meta"] = name, meta
        else:
            it = {"t": name, "d": c[i]["d"], "meta": meta}
        items.append(it)
    B[0]["items"] = items
    B[0]["h"] = HEAD[l]
    del B[2]
    d["title"], d["lead"] = HERO[l]
    json.dump(d, io.open(fn, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    print("изменён", fn)
