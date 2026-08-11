#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_yo.py — приводит русский перевод к последовательному «ё».

Книга писала одно и то же слово двояко: «распространённость» 50 раз и
«распространенность» 39, «ребёнка» 34 и «ребенка» 35, «отменён» 3 и
«отменен» 5. Восемьдесят семь таких семей.

Выбрано «всегда ё». Причина не в предпочтении: для КАЖДОЙ семьи форма с «ё»
уже есть в книге, то есть цель замены не придумывается, а берётся из текста.
Обратное направление (снять все «ё») потеряло бы различение и в справочнике
по медицине выглядело бы небрежностью.

Что скрипт НЕ делает. Он не восстанавливает «ё» там, где книга его нигде не
писала: угадывание «все»/«всё», «небо»/«нёбо», «падеж»/«падёж» по контексту —
задача, на которой ошибаются и люди. Список замен строится только по словам,
встреченным в книге в обоих написаниях; единственный кандидат в омографы
(«полет») прочитан по месту — обе строки о фобии полёта.

Замена идёт по видимому тексту внутри <main>, минуя <script> и <style>:
сплошная замена по файлу однажды уже сломала JavaScript на 137 страницах.

Порядок прогона: `fix_yo.py` правит и книгу, и `_codes_canon.json`; после
него нужен `fix_meta.py` (заголовок вкладки лежит вне `<main>` и заменой по
видимому тексту не задевается), и только потом `build_headers.py`.

    python fix_yo.py --dry     показать, что будет заменено
    python fix_yo.py           заменить
"""
from __future__ import annotations
import re, sys, io
from pathlib import Path
from collections import Counter, defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
RU = ROOT / 'klinik-psixiatriya' / 'ru'
DRY = '--dry' in sys.argv

WORD = re.compile(r'[А-Яа-яЁё]{4,}')
BOUND_L, BOUND_R = '(?<![А-Яа-яЁё])', '(?![А-Яа-яЁё])'

# Слова, которых книга НИГДЕ не писала с «ё», — автоматически их не вывести:
# пара для сравнения отсутствует. Каждое проверено по правилу и по смыслу.
#
# Полная форма причастия от глагола на -ить/-ать с ударением на суффиксе даёт
# «ё» («завершённый», «искажённый»), а краткая форма мужского рода — тоже
# («лишён», «отражён», «запрещён»); краткие средняя и множественная идут с «е»
# («запрещено», «включены»), и поэтому в список не входят. Проверено: слова
# с ударением на корне («вы́раженный», «сни́женный», «ограни́ченный»,
# «повы́шенный», «отсро́ченный», «уполномо́ченный») тоже остались вне списка.
MANUAL = {
    'запрещен': 'запрещён', 'завершен': 'завершён', 'лишен': 'лишён',
    'отражен': 'отражён', 'искажен': 'искажён',
    'завершенный': 'завершённый', 'завершенная': 'завершённая',
    'незавершенными': 'незавершёнными', 'искаженными': 'искажёнными',
    'напряженная': 'напряжённая', 'обнаженными': 'обнажёнными',
    'возвращенных': 'возвращённых',
    'раздраженного': 'раздражённого', 'раздраженное': 'раздражённое',
    # «лечёный» — прилагательное от «лечить», пишется с «ё»
    'нелеченый': 'нелечёный', 'нелеченая': 'нелечёная', 'нелеченые': 'нелечёные',
    'нелеченого': 'нелечёного', 'нелеченом': 'нелечёном', 'нелеченых': 'нелечёных',
    # местоимение и наречие: написания «ее» и «еще» в русском не существует
    'ее': 'её', 'еще': 'ещё',
    # личные формы на «-ёт»: ударное окончание, «е» здесь невозможно
    'придет': 'придёт', 'пьет': 'пьёт',
}


def files() -> list[Path]:
    return sorted(RU.glob('*.html'))


def visible_spans(t: str):
    """Куски видимого текста внутри <main>: всё, что вне тегов и вне
    <script>/<style>. Возвращает (начало, конец) в исходной строке."""
    m = re.search(r'<main[\s\S]*</main>', t)
    if not m:
        return []
    lo, hi = m.start(), m.end()
    dead = [(mm.start(), mm.end())
            for mm in re.finditer(r'<(script|style)[\s\S]*?</\1>', t[lo:hi])]
    spans, pos = [], lo
    for mm in re.finditer(r'<[^>]*>', t[lo:hi]):
        a, b = lo + mm.start(), lo + mm.end()
        if pos < a:
            spans.append((pos, a))
        pos = b
    if pos < hi:
        spans.append((pos, hi))
    return [(a, b) for a, b in spans
            if not any(lo + d0 <= a and b <= lo + d1 for d0, d1 in dead)]


def build_map() -> dict[str, str]:
    """Пары «без ё» → «с ё» по словам, встреченным в книге в обоих видах."""
    forms = defaultdict(Counter)
    for fp in files():
        t = fp.read_text(encoding='utf-8', errors='ignore')
        for a, b in visible_spans(t):
            for w in WORD.findall(t[a:b]):
                forms[w.lower().replace('ё', 'е')][w.lower()] += 1
    out = dict(MANUAL)
    for key, variants in forms.items():
        yo = [w for w in variants if 'ё' in w]
        no = [w for w in variants if 'ё' not in w]
        if len(yo) == 1 and no:
            out[no[0]] = yo[0]

    # Сравнение слово в слово видит только те формы, которые книга написала
    # обоими способами. «Определённых» в ней есть, а «определенного» осталось
    # без пары — и прошло бы мимо. Второй проход добирает такие формы через
    # ОСНОВУ прилагательного: «определённых» без окончания «ых» даёт
    # «определённ», и по ней получают «ё» все прочие окончания той же основы.
    #
    # Основу нельзя обрезать по самой букве «ё» — так уже пробовали, и
    # «определённых» дало основу «определё», а по ней «определение» стало
    # «определёнием»: 977 замен, почти все неверные. Основа сохраняется
    # целиком, отсекается только окончание, поэтому «определённ» и
    # «определени» больше не пересекаются.
    END = ('ыми', 'ого', 'ому', 'ими', 'его', 'ему', 'ый', 'ая', 'ое', 'ые',
           'ым', 'ом', 'ой', 'ую', 'ых', 'ий', 'яя', 'ее', 'ие', 'им', 'ем',
           'ей', 'юю', 'их')
    stems = set()
    for variants in forms.values():
        for w in variants:
            for e in END:
                if w.endswith(e) and 'ё' in w[:-len(e)] and len(w) - len(e) >= 6:
                    stems.add(w[:-len(e)])
    for stem in stems:
        plain = stem.replace('ё', 'е')
        for variants in forms.values():
            for w in variants:
                if 'ё' in w or w in out or not w.startswith(plain) or w == plain:
                    continue
                if w[len(plain):] not in END:
                    continue
                out[w] = stem + w[len(plain):]
    return out


def same_case(src: str, dst: str) -> str:
    """Регистр берётся у исходного слова целиком.

    Первая версия умела только заглавную первую букву — и «ЛЕГКОЕ» в
    заголовке превратилось в «Лёгкое», а «РАССТРОЙСТВА ПРИЕМА ПИЩИ» в
    «РАССТРОЙСТВА Приёма ПИЩИ». Сломались двенадцать мест, и сборщик
    заголовков это поймал: канон требовал прежнюю строку."""
    if src.isupper() and len(src) > 1:
        return dst.upper()
    return dst[0].upper() + dst[1:] if src[0].isupper() else dst


def sync_canon(pairs: dict, dry: bool) -> int:
    """Канон должен писать те же слова, что и книга.

    Иначе `build_headers.py` возвращает «ОСЛОЖНЕННОЕ» поверх «ОСЛОЖНЁННОЕ»
    и перестаёт быть идемпотентным — это уже случалось дважды. Шаг стоит
    здесь, а не отдельным скриптом, именно чтобы его нельзя было забыть.
    После него нужен `fix_meta.py`: <title> лежит вне <main> и заменой по
    видимому тексту не задевается."""
    canon = ROOT / '_codes_canon.json'
    if not canon.exists() or not pairs:
        return 0
    t = canon.read_text(encoding='utf-8')
    rx = re.compile(BOUND_L + '(' + '|'.join(
        sorted((re.escape(w) for w in pairs), key=len, reverse=True)) + ')' + BOUND_R,
        re.IGNORECASE)
    n = 0

    def rep(m):
        nonlocal n
        src = m.group(1)
        dst = pairs.get(src.lower())
        if not dst:
            return src
        n += 1
        return same_case(src, dst)

    new = rx.sub(rep, t)
    if n and not dry:
        canon.write_bytes(new.encode('utf-8'))
    return n


def main() -> int:
    pairs = build_map()
    print('=' * 72)
    print(f'ПОСЛЕДОВАТЕЛЬНОЕ «Ё» В РУССКОМ — {len(pairs)} семей слов')
    print('=' * 72)
    if not pairs:
        print('  нечего приводить: разнобоя нет')
        return 0

    rx = re.compile(BOUND_L + '(' + '|'.join(
        sorted((re.escape(w) for w in pairs), key=len, reverse=True)) + ')' + BOUND_R,
        re.IGNORECASE)

    total, touched = 0, 0
    seen = Counter()
    for fp in files():
        raw = fp.read_bytes()
        crlf = raw.count(b'\r\n') > raw.count(b'\n') // 2
        t = raw.decode('utf-8').replace('\r\n', '\n')
        spans = visible_spans(t)
        if not spans:
            continue
        out, last, n = [], 0, 0
        for a, b in spans:
            out.append(t[last:a])
            chunk = t[a:b]

            def rep(m):
                nonlocal n
                src = m.group(1)
                dst = pairs.get(src.lower())
                if not dst:
                    return src
                n += 1
                seen[src.lower()] += 1
                return same_case(src, dst)

            out.append(rx.sub(rep, chunk))
            last = b
        out.append(t[last:])
        if not n:
            continue
        total += n
        touched += 1
        if not DRY:
            new = ''.join(out)
            fp.write_bytes((new.replace('\n', '\r\n') if crlf else new).encode('utf-8'))

    print(f'  {"нашлось" if DRY else "заменено"}: {total} в {touched} файлах')
    ncanon = sync_canon(pairs, DRY)
    if ncanon:
        print(f'  в _codes_canon.json: {ncanon} — дальше нужен fix_meta.py,'
              f' затем build_headers.py')
    for w, n in seen.most_common(20):
        print(f'      {w} → {pairs[w]}  ×{n}')
    if len(seen) > 20:
        print(f'      …ещё {len(seen) - 20} слов')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
