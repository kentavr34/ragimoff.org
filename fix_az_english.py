# -*- coding: utf-8 -*-
"""Убирает лишний английский из азербайджанской прозы.

Владелец: «когда там много писанины и все термины, аббревиатуры и методы
подряд идут английским текстом — это не готово к публикации. Я не
англоязычный». Имена авторов, названия журналов и международные
аббревиатуры при первом упоминании остаются: они не переводятся. Убирается
другое — служебные английские слова и переводимые названия, поставленные
вместо азербайджанских.

Правило простое: если у выражения есть принятый азербайджанский
эквивалент, в тексте стоит он, а английское — в скобках и один раз.

    python fix_az_english.py            # сухой прогон
    python fix_az_english.py --apply
"""
import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent / 'klinik-psixiatriya'
APPLY = '--apply' in sys.argv

# английское выражение → азербайджанское. Английское сохраняется в скобках
# там, где оно термин и помогает узнать источник; чисто служебные слова
# переводятся без остатка.
WORDS = {
    'maintenance': 'saxlayıcı müalicə',
    'stepped care': 'pilləli yanaşma',
    'wait and see': 'gözlə və izlə',
    'bizarre': 'qəribə (bizarre)',
    'positive features': 'pozitiv əlamətlər',
    'phase-oriented': 'mərhələyönümlü',
    'bereavement exclusion': 'yas istisnası',
    'food addiction': 'qida asılılığı',
    'sex addiction': 'cinsi asılılıq',
    'internal modelling': 'daxili modelləşdirmə',
    'hand flapping': 'əl çırpma',
    'head banging': 'baş vurma',
    'long-acting injectable': 'uzunmüddətli təsirli inyeksiya',
    'doctor shopping': 'həkimdən həkimə gəzmə',
    'single physician approach': 'tək həkim prinsipi',
    'false memory': 'yalançı xatirə',
    'split personality': 'şəxsiyyətin parçalanması',
    'performance only': 'yalnız çıxış zamanı',
    'minimal brain dysfunction': 'minimal beyin disfunksiyası',
    'suffocation false alarm': 'boğulma yalançı siqnalı',
    'meth mouth': 'metamfetamin ağzı',
    'bad trip': 'pis trip',
    'gateway': 'giriş qapısı',
    'bailout': 'borcun ödənilməsi',
}

# организации: имя переводится, аббревиатура остаётся
ORGS = {
    'World Health Organization': 'Ümumdünya Səhiyyə Təşkilatı',
    'Electroconvulsive Therapy': 'Elektrokonvulsiv terapiya',
    'Deep Brain Stimulation': 'Dərin beyin stimulyasiyası',
    'Exposure and Response Prevention': 'Ekspozisiya və reaksiyanın qarşısının alınması',
    'Applied Behavior Analysis': 'Tətbiqi davranış analizi',
    'Parent Management Training': 'Valideyn idarəetmə təlimi',
    'Parent-Child Interaction Therapy': 'Valideyn-uşaq qarşılıqlı əlaqə terapiyası',
    'Mindfulness-Based Cognitive Therapy': 'Mayndfulnes əsaslı koqnitiv terapiya',
}

changed_files = 0
n_words = n_orgs = 0
for p in sorted(ROOT.glob('*.html')):
    raw = p.read_bytes()
    crlf = raw.count(b'\r\n') > raw.count(b'\n') // 2
    t = raw.decode('utf-8').replace('\r\n', '\n')
    orig = t

    for en, az in WORDS.items():
        # только помеченный английский — так не заденем имена и журналы
        pat = '<span lang="en">%s</span>' % re.escape(en)
        found = len(re.findall(pat, t))
        if found:
            n_words += found
            t = re.sub(pat, az, t)

    for en, az in ORGS.items():
        # только там, где азербайджанского эквивалента ещё нет рядом:
        # иначе повторный прогон обернёт уже развёрнутое во второй раз
        pat = r'(?<!\()<span lang="en">%s</span>' % re.escape(en)
        for m in list(re.finditer(pat, t))[::-1]:
            before = t[max(0, m.start() - len(az) - 3):m.start()]
            if az in before:
                continue
            n_orgs += 1
            t = t[:m.start()] + '%s (<span lang="en">%s</span>)' % (az, en) + t[m.end():]

    if t != orig:
        changed_files += 1
        if APPLY:
            p.write_bytes((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))

print('файлов: %d · служебных слов переведено: %d · названий развёрнуто: %d'
      % (changed_files, n_words, n_orgs))
print('ПРИМЕНЕНО' if APPLY else 'сухой прогон — запустить с --apply')
