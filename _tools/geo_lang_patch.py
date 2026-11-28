# -*- coding: utf-8 -*-
"""28.11.2026 (слово Кенана): язык сайта по умолчанию — по стране посетителя: Азербайджан → AZ, Россия → RU,
Турция → турецкий (у книг — турецкая версия, reader.js; интерфейса на турецком пока нет — интерфейс AZ, ближайший
к турецкому), США и прочие страны → EN. Страна — по часовому поясу браузера, затем по языку браузера.
Ручной выбор (localStorage r11_lang) главнее. Правит строку выбора языка в шаблонах корня (снимки /az/ /ru/ /en/
задают window.__LANG сами и пересобираются build_static.py из этих шаблонов).
  python _tools/geo_lang_patch.py [--dry]"""
import glob, io, os, sys

D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OLD = "(b === 'ru' || b === 'en' ? b : 'az')"
NEW = ("(function () { var z = ''; try { z = Intl.DateTimeFormat().resolvedOptions().timeZone || ''; } catch (e) {}"
       " if (z === 'Asia/Baku' || b === 'az') return 'az';"
       " if (z === 'Europe/Istanbul' || z === 'Asia/Istanbul' || b === 'tr') return 'az';"
       " if (b === 'ru' || /^Europe\\/(Moscow|Samara|Volgograd|Kirov|Ulyanovsk|Saratov|Astrakhan|Kaliningrad)$|^Asia\\/(Yekaterinburg|Omsk|Novosibirsk|Barnaul|Tomsk|Novokuznetsk|Krasnoyarsk|Irkutsk|Chita|Yakutsk|Khandyga|Vladivostok|Ust-Nera|Magadan|Sakhalin|Srednekolymsk|Kamchatka|Anadyr)$/.test(z)) return 'ru';"
       " return 'en'; })()")
n = 0
for f in sorted(glob.glob(os.path.join(D, "*.html"))):
    t = io.open(f, encoding="utf-8", newline="").read()
    if OLD not in t:
        continue
    n += 1
    print(os.path.basename(f))
    if "--dry" not in sys.argv:
        io.open(f + ".bak_geo_20261128", "w", encoding="utf-8", newline="").write(t)
        io.open(f, "w", encoding="utf-8", newline="").write(t.replace(OLD, NEW).replace("/* 13.11: по умолчанию AZ, иначе язык браузера */", "/* 28.11: по стране посетителя (geo_lang_patch.py) */"))
print("шаблонов:", n)
