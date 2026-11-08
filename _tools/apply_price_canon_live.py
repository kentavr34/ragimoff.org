"""Канон цен Кенана 08–09.11.2026 (ЦНС #712) → живые страницы ragimoff.org (az / ru / en).

Правка только цифр в строках цен; вёрстка не меняется (правка по номерам строк исходника).
Перед правкой — копия файлов в _backups_price_canon_<дата>/.
  Тренинги (4 краткосрочных направления): 600→900 полная, 500→800 предоплата, 200→300 в месяц; дата старта убрана.
  Консультации: один специалист — онлайн 100 / очно 150 AZN; оба — 150 / 200 AZN; пакет 4 сессий — 400 / 600 AZN.
  RU — рубли по курсу Кенана (100 AZN = 5 000 руб.); EN — доллары по прежнему курсу сайта (100 AZN = $60).
Запуск из папки site: python _tools/apply_price_canon_live.py [--dry]
"""
import re, sys, shutil, pathlib, time
from bs4 import BeautifulSoup
sys.stdout.reconfigure(encoding='utf-8')
SITE = pathlib.Path(__file__).resolve().parents[1]
DRY = '--dry' in sys.argv
LANGS = {'az': '', 'ru': 'ru/', 'en': 'en/'}
SHORT_PAGES = ['program-psixoanaliz.html', 'program-psixodiaqnostika.html', 'samira.html', 'aile-terapiyasi.html', 'tehsil.html', 'aile-terapiyasi-usaq.html']
CONSULT_PAGES = ['aile-terapiyasi.html', 'aile-terapiyasi-usaq.html', 'depressiya.html', 'panik-ataklar.html', 'sosial-fobiya.html', 'xidmetler.html',
                 'enurez.html', 'valideyn-mektebi.html']
SHORT_UNITS = ['price-card', 'info-card', 'stat-item', 'mod-price', 'tile-lbl', 'form-radio-lbl']
LONG_SIG = re.compile(r'\d[  ]\d00 AZN|[3-9][  ]?\d00 AZN/ay\b|1[  ]?\d{3} AZN')
SHORT_SIG = re.compile(r'(?<!\d)(?<!\d )600 AZN')
REPL = [(re.compile(r'(?<!\d)(?<![\d] )600 AZN'), '900 AZN'), (re.compile(r'(?<!\d)(?<![\d] )500 AZN'), '800 AZN'),
        (re.compile(r'(?<!\d)(?<![\d] )200 AZN'), '300 AZN')]
START_DATE = [re.compile(r'Təlimə başlama tarixi\s*—\s*'), re.compile(r'Начало тренинга\s*—\s*'), re.compile(r'The training starts on\s*')]
# цена консультации: (вид строки, онлайн/очно) → текст суммы по языку
CONS = {
    'az': {('one', 'on'): '100 AZN', ('one', 'off'): '150 AZN', ('both', 'on'): '150 AZN', ('both', 'off'): '200 AZN', ('pack', 'on'): '400 AZN', ('pack', 'off'): '600 AZN'},
    'ru': {('one', 'on'): '5 тыс. руб.', ('one', 'off'): '7,5 тыс. руб.', ('both', 'on'): '7,5 тыс. руб.', ('both', 'off'): '10 тыс. руб.', ('pack', 'on'): '20 тыс. руб.', ('pack', 'off'): '30 тыс. руб.'},
    'en': {('one', 'on'): '$60', ('one', 'off'): '$90', ('both', 'on'): '$90', ('both', 'off'): '$120', ('pack', 'on'): '$240', ('pack', 'off'): '$360'},
}
PRICE_TOKEN = {'az': re.compile(r'\d[\d ]*\s?AZN'), 'ru': re.compile(r'[\d,]+\s?тыс\.\s?руб\.|\d[\d ]*\s?AZN'), 'en': re.compile(r'\$\d+|\d[\d ]*\s?AZN')}
ON = re.compile(r'Online|Онлайн|Onlayn', re.I)
OFF = re.compile(r'Əyani|Очно|In person', re.I)
FAQ = {  # вопрос-ответ в JSON-LD страницы консультаций (было «120 AZN»)
    'az': ('Qiymət: 120 AZN.', 'Qiymət: onlayn 100 AZN, əyani 150 AZN.'),
    'ru': ('Цена: 120 AZN.', 'Цена: онлайн 5 000 руб., очно 7 500 руб.'),
    'en': ('Price: 120 AZN.', 'Price: $60 online, $90 in person.'),
}
NOTE_AZ = ('Hər iki mütəxəssisin birgə apardığı sessiyalar Kənan Rəhimovun tarifi ilə hesablanır.',
           'Bir mütəxəssislə: onlayn 100 AZN, əyani 150 AZN; hər iki mütəxəssislə: onlayn 150 AZN, əyani 200 AZN (1 saat).')

log, touched = [], {}


def span(el):
    a = el.sourceline - 1
    return a, a + str(el).count('\n')


def edit(lines, a, b, fn, f):
    for i in range(a, min(b, len(lines) - 1) + 1):
        new = fn(lines[i])
        if new != lines[i]:
            log.append('%s:%d  %s  →  %s' % (f, i + 1, re.sub(r'<[^>]+>', '', lines[i]).strip()[:80], re.sub(r'<[^>]+>', '', new).strip()[:80]))
            lines[i] = new
            touched[f] = lines


def short_fix(line):
    for rx, rep in REPL:
        line = rx.sub(rep, line)
    return line


def drop_date(line):
    for rx in START_DATE:
        line = rx.sub('', line)
    return line


def run(f, lang):
    p = SITE / f
    if not p.is_file():
        return
    raw = touched.get(f) or p.read_text(encoding='utf-8').split('\n')
    s = BeautifulSoup('\n'.join(raw), 'html.parser')
    name = f.rsplit('/', 1)[-1]
    if name in SHORT_PAGES:
        for el in s.find_all(class_=True):
            if not any(u in el.get('class', []) for u in SHORT_UNITS):
                continue
            t = el.get_text(' ', strip=True)
            is_mp = 'mod-price' in el.get('class', [])
            if not (SHORT_SIG.search(t) or (is_mp and '300 AZN' not in t)) or LONG_SIG.search(t):
                continue
            a, b = span(el)
            edit(raw, a, b, short_fix, f)
        for el in s.select('.mod-intro'):
            a, b = span(el)
            edit(raw, a, b, drop_date, f)
    if name in CONSULT_PAGES:
        for row in s.select('.pricing-tbl-row'):
            title = row.get_text(' ', strip=True)
            kind = 'pack' if re.search(r'Paket|пакет|Package', title, re.I) else ('both' if re.search(r'Birgə|hər iki|Совместн|оба специалиста|Joint|both specialists', title, re.I) else 'one')
            a, b = span(row)

            def fix(line, kind=kind):
                if 'pricing-tbl-price' not in line:
                    return line
                mode = 'on' if ON.search(line) else ('off' if OFF.search(line) else None)
                if not mode:
                    return line
                return PRICE_TOKEN[lang].sub(CONS[lang][(kind, mode)], line, count=1)
            edit(raw, a, b, fix, f)
        for i, l in enumerate(raw):
            if FAQ[lang][0] in l:
                edit(raw, i, i, lambda x: x.replace(FAQ[lang][0], FAQ[lang][1]), f)
            if lang == 'az' and NOTE_AZ[0] in l:
                edit(raw, i, i, lambda x: x.replace(NOTE_AZ[0], NOTE_AZ[1]), f)


for lang, pre in LANGS.items():
    for name in sorted(set(SHORT_PAGES + CONSULT_PAGES)):
        run(pre + name, lang)

print('\n'.join(log))
print('\nстрок изменено: %d, файлов: %d' % (len(log), len(touched)))
if not DRY and touched:
    bak = SITE / ('_backups_price_canon_' + time.strftime('%Y%m%d_%H%M'))
    for f in touched:
        dst = bak / f
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SITE / f, dst)
    for f, lines in touched.items():
        (SITE / f).write_text('\n'.join(lines), encoding='utf-8', newline='')
    print('записано; копия до правки:', bak.name)
