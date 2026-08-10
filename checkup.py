# -*- coding: utf-8 -*-
"""
checkup.py — сплошная проверка книги «Klinik Psixiatriya».

Один прогон отвечает на вопрос «где книга не в порядке» по всем осям сразу:
структура, коды трёх классификаций, параллельность четырёх языков, канон
терминов, межъязыковое загрязнение, типографика, целостность навигации.

    python checkup.py            # человекочитаемый отчёт
    python checkup.py --json     # машинный отчёт в _checkup.json

ЗАЧЕМ ОТДЕЛЬНЫЙ ФАЙЛ
====================
Проверки писались россыпью и терялись между сессиями. Здесь они собраны в
одном месте, чтобы любой прогон был воспроизводим и чтобы «готово» означало
«checkup.py чист», а не «на глаз выглядит хорошо».

ВАЖНО ПРО ЧТЕНИЕ HTML
=====================
Видимый текст извлекается так же, как это делает браузер: «<» перед не-буквой
считается обычным символом, а не началом тега. Наивное `<[^>]+>` съедает
записи вида `< 1500` вместе с куском текста и порождает несуществующие
дефекты — на этом уже был потерян день.
"""
from __future__ import annotations
import re, sys, io, html, json, html as H
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).parent
BOOK = ROOT / 'klinik-psixiatriya'
DIRS = {'az': BOOK, 'ru': BOOK / 'ru', 'en': BOOK / 'en', 'tr': BOOK / 'tr'}
CARD = re.compile(r'(6[A-E][0-9A-Z]{2}|7[AB][0-9A-Z]{2}|8A05|HA[0-9A-Z]{2}|GA34)')

LOOSE = re.compile(r'<(?![a-zA-Z/!?])')
SKIP = re.compile(r'<(script|style)\b[\s\S]*?</\1>', re.I)
HEAD = re.compile(r'<head\b[\s\S]*?</head>', re.I)


def visible(fp: Path, main_only: bool = True) -> str:
    t = fp.read_text(encoding='utf-8', errors='ignore')
    t = SKIP.sub(' ', t)
    t = HEAD.sub(' ', t)
    if main_only:
        m = re.search(r'<main[\s\S]*?</main>', t, re.I)
        if m:
            t = m.group(0)
    t = LOOSE.sub('&lt;', t)
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]*>', ' ', t)))


def raw(fp: Path) -> str:
    return fp.read_text(encoding='utf-8', errors='ignore')


# ── что считается нарушением канона ───────────────────────────────────────
CANON_AZ = [('mənzərə', 'Klinik təzahürlər'), ('çek-list', 'Vahid diaqnostik meyarlar'),
            ('pozğunluq', 'pozuntu'), (r'ruhi pozuntu', 'psixi pozuntu')]
# слова одного языка, недопустимые в другом
LEAK = {
    'ru': [r'\bpozuntu\w*', r'\bdiaqnostik\b', r'\bmeyarlar\b', r'\bmüalicə\b', r'\bxəstə\b',
           r'\bССРИ\b', r'(?<![А-Яа-я])ОКП(?![А-Яа-я])'],
    'en': [r'\bpozuntu\w*', r'\bdiaqnostik\b', r'\bmeyarlar\b', r'\bSoviet Socialist\b'],
    # tetikleyici — правильное турецкое слово; азербайджанское tətikləyici проверяется отдельно
    'tr': [r'\bpozuntu\w*', r'\bMif \d', r'\bÖmürlük\b', r'\bKDT\b', r'\bDDHP\b'],
    'az': [],
}
FALSE_FRIENDS = {
    'ru': [r'Шкала насилия', r'Цикл насилия', r'сонная одурь', r'нележание'],
    'en': [r'Violence scale', r'Violence period', r'\bUSSR\b', r'Out-of-body'],
    'tr': [r'yatak yatma', r'Ekstra bileşen', r'ekstarkib'],
    'az': [r'əkstərkib', r'adhesiya', r'SİKLETİMİK', r'Çəlik xəstəliyi', r'\bcopying\b'],
}


def main() -> int:
    as_json = '--json' in sys.argv
    codes = sorted({p.stem for p in BOOK.glob('*.html') if CARD.fullmatch(p.stem)})
    report: dict = {'cards': len(codes), 'checks': {}}
    fails = 0

    def check(name: str, bad, detail=None):
        nonlocal fails
        n = len(bad) if hasattr(bad, '__len__') else bad
        report['checks'][name] = {'failures': n, 'detail': detail or (bad if isinstance(bad, list) else None)}
        if n:
            fails += 1
        return n

    # 1. полнота: карточка есть во всех четырёх языках
    missing = [f'{lg}/{c}' for c in codes for lg, d in DIRS.items() if not (d / f'{c}.html').exists()]
    check('полнота_4_языка', missing)

    # 2. структурная параллельность
    keys = ('h2', 'h3', 'h4', 'li', 'table', 'tr')
    struct = []
    for c in codes:
        prof = {}
        for lg, d in DIRS.items():
            fp = d / f'{c}.html'
            if not fp.exists():
                continue
            m = re.search(r'<main[\s\S]*?</main>', raw(fp), re.I)
            b = m.group(0) if m else raw(fp)
            prof[lg] = {k: len(re.findall(rf'<{k}\b', b)) for k in keys}
        for k in keys:
            vals = {lg: prof[lg][k] for lg in prof}
            if len(set(vals.values())) > 1:
                struct.append(f'{c}.{k}={"/".join(str(vals.get(l, "-")) for l in ("az", "ru", "en", "tr"))}')
    check('структура_параллельна', struct)

    # 3. навигация
    nav = []
    for lg, d in DIRS.items():
        ids = {fp.name: set(re.findall(r'id="([^"]+)"', raw(fp))) for fp in d.glob('*.html')}
        for fp in d.glob('*.html'):
            for h in re.findall(r'href="([^"]+)"', raw(fp)):
                if h.startswith('#') and h[1:] not in ids[fp.name]:
                    nav.append(f'якорь {lg}/{fp.stem}{h}')
                elif h.endswith('.html') and '/' not in h and not (d / h).exists():
                    nav.append(f'ссылка {lg}/{fp.stem}→{h}')
    check('навигация_цела', nav)

    # 4. шапка: три классификации на месте
    hdr = []
    for c in codes:
        for lg, d in DIRS.items():
            fp = d / f'{c}.html'
            if not fp.exists():
                continue
            t = raw(fp)
            m = re.search(r'<table class="dh">[\s\S]*?</table>', t)
            if not m:
                hdr.append(f'{lg}/{c}: нет шапки')
                continue
            rows = len(re.findall(r'<tr\b', m.group(0)))
            if rows != 3:
                hdr.append(f'{lg}/{c}: строк в шапке {rows}')
    check('шапка_три_классификации', hdr)

    # 5. канон азербайджанского
    canon = []
    for c in codes:
        t = visible(BOOK / f'{c}.html')
        for pat, want in CANON_AZ:
            if re.search(pat, t, re.I):
                canon.append(f'{c}: «{pat}» → должно быть «{want}»')
    check('канон_az', canon)

    # 6. межъязыковое загрязнение
    # словари и списки сокращений исключены: там иноязычный термин — предмет описания,
    # а не непереведённый остаток («pasiyent | пациент (не 'xəstə')»)
    GLOSSARY = {'abbreviatur', 'terminoloji-luget', 'elave-acde', 'elave-skalalar'}
    # bolme-NN — заглушки-редиректы, в них видимый текст это имя файла
    leak = []
    for lg, pats in LEAK.items():
        for fp in sorted(DIRS[lg].glob('*.html')):
            if fp.stem in GLOSSARY or fp.stem.startswith('bolme-'):
                continue
            t = visible(fp)
            for p in pats:
                n = len(re.findall(p, t))
                if n:
                    leak.append(f'{lg}/{fp.stem}: {p} ×{n}')
    check('чужой_язык', leak)

    # 7. известные ложные друзья
    ff = []
    for lg, pats in FALSE_FRIENDS.items():
        for fp in sorted(DIRS[lg].glob('*.html')):
            t = visible(fp)
            for p in pats:
                n = len(re.findall(p, t))
                if n:
                    ff.append(f'{lg}/{fp.stem}: {p} ×{n}')
    check('ложные_друзья', ff)

    # 8. типографика: неэкранированный «<», перевёрнутые вложенные кавычки
    typo = []
    W = r'[0-9A-Za-zА-Яа-яЁёƏəĞğIıİiÖöŞşÜüÇç]'
    for lg, d in DIRS.items():
        for fp in sorted(d.glob('*.html')):
            t = SKIP.sub(' ', raw(fp))
            n = len(re.findall(r'<(?![a-zA-Z/!?])', t))
            if n:
                typo.append(f'{lg}/{fp.stem}: неэкранированный < ×{n}')
            v = visible(fp)
            # только полная перевёрнутая пара »X« / ”X“ — одиночный » перед буквой
            # это законный падежный суффикс: «İkili depresiya»da, “Kök hücre turizmi”nin
            n2 = len(re.findall('»(?=' + W + ')[^«»]{1,90}?(?<=' + W + ')«', v))
            n2 += len(re.findall('”(?=' + W + ')[^“”]{1,90}?(?<=' + W + ')“', v))
            if n2:
                typo.append(f'{lg}/{fp.stem}: перевёрнутая вложенная кавычка ×{n2}')
    check('типографика', typo)

    # 9. слипшийся </strong>: жирная метка вплотную к заглавной букве или цифре
    # («<strong>Probable DLB</strong>2+ core features»). Аффикс после тега —
    # законная тюркская типографика («</strong>dır», «</strong>nda»), поэтому
    # строчная буква нарушением НЕ считается; подробности в fix_strong.py
    GLUED = re.compile(r'</strong>(?=[A-ZÀ-ÖØ-ÞĞİÖŞÜÇƏА-ЯЁ0-9])')
    glued = []
    for lg, d in DIRS.items():
        for fp in sorted(d.glob('*.html')):
            m = re.search(r'<main[\s\S]*?</main>', raw(fp), re.I)
            n = len(GLUED.findall(m.group(0) if m else raw(fp)))
            if n:
                glued.append(f'{lg}/{fp.stem}: слипшийся </strong> ×{n}')
    check('разделитель_после_strong', glued)

    # 10. турецкое правило процента: знак перед числом (%15), а не после
    pct = []
    for fp in sorted(DIRS['tr'].glob('*.html')):
        n = len(re.findall(r'\d+(?:[.,–-]\d+)?%', visible(fp)))
        if n:
            pct.append(f'tr/{fp.stem}: процент после числа ×{n}')
    check('турецкий_процент', pct)

    # 11. источники: у каждой карточки есть список литературы
    refs = []
    for c in codes:
        for lg, d in DIRS.items():
            fp = d / f'{c}.html'
            if not fp.exists():
                continue
            # атрибуты у тега допустимы: lang_tags.py ставит lang="en"
            m = re.search(r'<ol class="ref-list"[^>]*>[\s\S]*?</ol>', raw(fp))
            n = len(re.findall(r'<li\b', m.group(0))) if m else 0
            if n == 0:
                refs.append(f'{lg}/{c}: источников 0')
    check('источники_есть', refs)

    # 12. кавычки: закрывающая не должна слипаться со следующим словом.
    # Ловушка языка: в азербайджанском и русском второй уровень — „…“,
    # то есть “ ЗАКРЫВАЕТ, а в английском и турецком тот же знак открывает.
    # Пока fix_space.py этого не различал, он снимал пробел, который ставил
    # fix_quotes.py, и обе правки молча отменяли друг друга при каждом прогоне.
    CLOSE = {'az': '»“', 'ru': '»“', 'en': '”', 'tr': '”'}
    AFFIX = (r'(?:n?[ıiuü]n|n?[ıiuü]|[yn]?[aeə]|d[aeə]|nd[aeə]|d[aeə]n|nd[aeə]n|'
             r'[dt][ıiuü]r|[dt][ıiuü]rl[aeə]r|l[aeə]r|l[aeə]r[ıi]|l[aeə]rd[aeə]|'
             r's[ıiuü]|[yi]l[aeə]|d[aeə]k[ıi]|ç[ıi]|l[ıi]|s[aeə])')
    UP = r'[A-ZÀ-ÖØ-ÞĞİÖŞÜÇƏА-ЯЁ0-9«„]'
    quotes = []
    for lg, d in DIRS.items():
        if lg in ('az', 'tr'):      # строчная может быть падежным аффиксом
            pat = re.compile(f'([{CLOSE[lg]}])(?={UP}|(?!{AFFIX}(?![a-zçəğıöşü]))[a-zçəğıöşü])')
        else:
            pat = re.compile(f'([{CLOSE[lg]}])(?={UP}|[a-zа-яё])')
        for fp in sorted(d.glob('*.html')):
            m = re.search(r'<main[\s\S]*?</main>', raw(fp), re.I)
            n = len(pat.findall(m.group(0) if m else ''))
            if n:
                quotes.append(f'{lg}/{fp.stem}: кавычка слиплась со словом ×{n}')
    check('кавычки_отбиты', quotes)

    # 13. таблица кодов на справочных страницах должна совпадать с каноном.
    # Она дважды разъезжалась со старой привязкой (6A60↔6A70, 6B83↔6B84↔6B85),
    # причём в terminoloji-luget.html правка 2026-08-09 её не достала.
    import json as _json
    tbl = []
    canon_path = ROOT / '_codes_canon.json'
    if canon_path.exists():
        rows_c = _json.loads(canon_path.read_text(encoding='utf-8'))['header_source']['rows']
        official = {r['code']: (r.get('icd11_official') or {}).get('en', '') for r in rows_c}
        cellrx = re.compile(r'<td[^>]*>([\s\S]*?)</td>')
        for lg, d in DIRS.items():
            for page in ('abbreviatur.html', 'terminoloji-luget.html'):
                fp = d / page
                if not fp.exists():
                    continue
                t2 = raw(fp)
                big = [m.group(0) for m in re.finditer(r'<table[^>]*>[\s\S]*?</table>', t2)
                       if 'kod-cell' in m.group(0) and len(re.findall(r'<tr>', m.group(0))) > 50]
                if not big:
                    continue
                for r in re.findall(r'<tr>[\s\S]*?</tr>', big[0]):
                    c = [re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]*>', '', x))).strip()
                         for x in cellrx.findall(r)]
                    if len(c) < 3 or not re.fullmatch(r'[0-9][A-Z][0-9A-Z]{2}', c[0]):
                        continue
                    ref = official.get(c[0], '')
                    a = re.sub(r'[^a-z]', '', c[2].lower())
                    b = re.sub(r'[^a-z]', '', ref.lower())
                    if ref and a and a[:14] not in b and b[:14] not in a:
                        tbl.append(f'{lg}/{page} {c[0]}: «{c[2][:40]}»')
    check('таблица_кодов_по_канону', tbl)

    # 10. сборка из данных идемпотентна (шапки и разделы совпадают с _codes_canon.json)
    # проверяется отдельными скриптами; здесь только напоминание в отчёте
    report['напоминание'] = 'после правок прогнать build_headers.py и build_sections.py — оба должны показать 0 изменений'

    if as_json:
        (ROOT / '_checkup.json').write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding='utf-8')
        print('отчёт записан в _checkup.json')
        return 1 if fails else 0

    print('=' * 72)
    print(f'ПРОВЕРКА КНИГИ — {len(codes)} карточек × 4 языка')
    print('=' * 72)
    for name, r in report['checks'].items():
        mark = 'OK  ' if not r['failures'] else 'СБОЙ'
        print(f'  [{mark}] {name}: {r["failures"]}')
        if r['failures'] and r['detail']:
            for x in r['detail'][:6]:
                print(f'          {x}')
            if len(r['detail']) > 6:
                print(f'          … ещё {len(r["detail"]) - 6}')
    print()
    print(f'проверок со сбоями: {fails} из {len(report["checks"])}')
    return 1 if fails else 0


if __name__ == '__main__':
    raise SystemExit(main())
