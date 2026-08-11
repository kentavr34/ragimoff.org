#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prosecheck.py — ищет следы механического перевода в трёх переводах книги.

Зачем. `paracheck.py` считает блоки и их длину, `numcheck.py` — числа,
`xrefcheck.py` — отсылки. Все три молчат, когда блок на месте, той же длины,
с теми же цифрами — но собран неправильно. А именно так и ломается перевод
с азербайджанского: язык ставит главное слово в конец
(«…müşahidə edilən, lakin … davam etdiyi ilkin psixotik pozuntudur»), и при
механическом развороте сказуемое остаётся висеть в хвосте, а придаточное
открывается заглавной буквой посреди фразы.

Пять проверок. Каждая — на класс брака, найденный чтением и подтверждённый
по первоисточнику; инструмент лишь распространяет находку на всю книгу.

  ЗАГЛАВНАЯ ПОСРЕДИ ФРАЗЫ. «дополнительно При котором», «совпадение Высокая»,
        «эпизод — Характеризуется». Список собственных имён не задаётся
        руками: слово считается именем собственным, если во ВСЁМ дереве
        языка оно ни разу не встретилось со строчной. Слово, которое где-то
        пишется строчно, а здесь стоит с заглавной посреди предложения, —
        подозреваемый.

  ВИСЯЩЕЕ СКАЗУЕМОЕ. «…не достигающие критериев полного психотического
        эпизода является клиническим состоянием». Причастие во множественном
        числе и глагол в единственном рядом — разрыв согласования, которого
        не бывает в живой речи.

  ЧУЖОЕ СЛОВО. «Curr Psychiatry Rep 2009 icmal», «2003 ikiz meta-analiz» —
        азербайджанские слова, не переведённые вовсе. Ловятся как латиница
        вне разметки языка, известная азербайджанскому дереву и неизвестная
        английскому.

  Ё И Е. «отменен» рядом с «отменён», «сохранен» рядом с «сохранён» —
        книга должна выбрать одно.

  ИМЯ КИРИЛЛИЦЕЙ. «Эскироль Ж.-Э.», «Кальбаум К.» — в книге фамилии стоят
        латиницей («Kahlbaum K.», «Kraepelin»), и запись кириллицей делает
        источник ненаходимым.

Вывод — список мест на прочтение, не приговор. Приговор выносит человек.

    python prosecheck.py             # всё, по языкам
    python prosecheck.py --lang ru
    python prosecheck.py --card 6A21
    python prosecheck.py --check caps
"""
from __future__ import annotations
import re, sys, io, html as H
from pathlib import Path
from collections import Counter, defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
BOOK = ROOT / 'klinik-psixiatriya'
DIRS = {'az': BOOK, 'ru': BOOK / 'ru', 'en': BOOK / 'en', 'tr': BOOK / 'tr'}

ONE = sys.argv[sys.argv.index('--card') + 1] if '--card' in sys.argv else None
LANG = sys.argv[sys.argv.index('--lang') + 1] if '--lang' in sys.argv else None
CHECK = sys.argv[sys.argv.index('--check') + 1] if '--check' in sys.argv else None
LIMIT = int(sys.argv[sys.argv.index('--limit') + 1]) if '--limit' in sys.argv else 40
if LIMIT <= 0:
    LIMIT = 10 ** 9                    # «--limit 0» — показать всё

LOOSE = re.compile(r'<(?![a-zA-Z/!?])')
CYR_UP = 'А-ЯЁ'
CYR_LO = 'а-яё'

# Буквы, по которым язык узнаётся: они есть только в своём алфавите.
LATIN_WORD = re.compile(r"[A-Za-zÀ-ÿĀ-ſəƏıİşŞğĞçÇüÜöÖ][\w'’-]*")


def visible(raw: str, keep_marks: bool = False) -> str:
    """Видимый текст <main>. Список литературы выкидывается: там своя
    типографика — инициалы, сокращения журналов, латиница вперемешку."""
    m = re.search(r'<main[\s\S]*</main>', raw)
    if not m:
        return ''
    s = re.sub(r'<(script|style|nav|aside)[\s\S]*?</\1>', ' ', m.group(0))
    s = re.sub(r'<ol class="ref-list"[^>]*>[\s\S]*?</ol>', ' ', s)
    s = LOOSE.sub('&lt;', s)
    if keep_marks:
        # оставляем след от span lang=… и кода XBT, чтобы отличить
        # осознанную иноязычную вставку от невычищенного оригинала
        s = re.sub(r'<span lang="([a-z]{2})"[^>]*>([\s\S]*?)</span>',
                   lambda m: ' \x02' + m.group(1) + '\x02 ' + m.group(2) + ' \x03 ', s)
        # шаблон замены НЕ raw: «\x04» в raw-строке re считает неизвестным
        # экранированием и падает, а не подставляет символ
        s = re.sub(r'<span class="icd"[^>]*>([\s\S]*?)</span>', ' ' + chr(4) + ' ', s)
    return re.sub(r'[ \t]+', ' ', H.unescape(re.sub(r'<[^>]*>', ' ', s)))


def blocks(raw: str) -> list[str]:
    """Абзацы, пункты и ячейки — по отдельности: брак живёт внутри блока,
    а сплошной текст склеивает конец одного с началом другого."""
    m = re.search(r'<main[\s\S]*</main>', raw)
    if not m:
        return []
    s = re.sub(r'<(script|style|nav|aside)[\s\S]*?</\1>', ' ', m.group(0))
    s = re.sub(r'<ol class="ref-list"[^>]*>[\s\S]*?</ol>', ' ', s)
    s = LOOSE.sub('&lt;', s)
    out = []
    for mm in re.finditer(r'<(p|li|td|h3|h4)\b[^>]*>((?:(?!</\1>)[\s\S])*)</\1>', s):
        body = mm.group(2)
        marks = set(re.findall(r'<span lang="([a-z]{2})"', body))
        icd = '<span class="icd"' in body
        txt = re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]*>', ' ', body))).strip()
        if txt:
            out.append((txt, marks, icd, body))
    return out


def cards() -> list[str]:
    return [p.stem for p in sorted(BOOK.glob('*.html'))
            if re.fullmatch(r'[0-9A-Z]{4}', p.stem) and (ONE is None or p.stem == ONE)]


def pages(lg: str) -> list[Path]:
    """Карточки расстройств. Справочные страницы (алфавитный указатель,
    список сокращений) живут по своим правилам и сюда не входят."""
    return [DIRS[lg] / f'{c}.html' for c in cards() if (DIRS[lg] / f'{c}.html').exists()]


# ── имена собственные: не список, а наблюдение ─────────────────────────────
def proper_nouns(lg: str) -> set[str]:
    """Слово считается собственным, если во всём дереве языка оно ни разу
    не встретилось со строчной буквы. Список руками не задаётся — иначе он
    отражал бы мои представления, а не книгу.

    Корпус берётся по ВСЕМУ дереву, а не по разбираемой карточке: с ключом
    `--card` наблюдение свелось бы к одной странице, и всякое имя, названное
    там единожды, объявлялось бы нарицательным."""
    lower, upper = Counter(), Counter()
    for c in [p.stem for p in sorted(BOOK.glob('*.html'))
              if re.fullmatch(r'[0-9A-Z]{4}', p.stem)]:
        fp = DIRS[lg] / f'{c}.html'
        if not fp.exists():
            continue
        v = visible(fp.read_text(encoding='utf-8', errors='ignore'))
        # дефис держит фамилию целой: «Крафт-Эбинг», «Буш-Фрэнсис»
        for w in re.findall(r'[' + CYR_UP + CYR_LO + r']{3,}(?:-[' + CYR_UP + CYR_LO + r']{2,})?', v):
            (upper if w[0] in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ' else lower)[w.lower()] += 1
    return {w for w, n in upper.items() if lower[w] == 0}


# ── 1. заглавная посреди фразы ─────────────────────────────────────────────
# «дополнительно При котором» · «совпадение Высокая» · «дислексией Не является»
MID_CAP = re.compile(
    r'[' + CYR_LO + r'»)] ([' + CYR_UP + r'][' + CYR_LO + r']+'
    r'(?:-[' + CYR_UP + CYR_LO + r'][' + CYR_LO + r']+)?)')
# слово после точки, «:», «;», «!», «?» и в начале блока — законная заглавная
AFTER_STOP = re.compile(r'[.:;!?•]\s*$')


def check_caps(lg: str) -> list:
    if lg != 'ru':
        return []                       # правило разное в каждом языке; пока русский
    proper = proper_nouns(lg)
    hits = []
    for fp in pages(lg):
        for txt, marks, icd, body in blocks(fp.read_text(encoding='utf-8', errors='ignore')):
            for m in MID_CAP.finditer(txt):
                w = m.group(1)
                if w.lower() in proper:
                    continue
                if AFTER_STOP.search(txt[:m.start(1)]):
                    continue
                hits.append((fp.parent.name + '/' + fp.stem, w,
                             txt[max(0, m.start() - 45):m.end() + 25]))
    return hits


# ── 1b. заглавная после тире — но только против мастера ────────────────────
# Само по себе «<strong>DSM-III (1980)</strong> — Термин…» дефектом не
# является: азербайджанский мастер пишет так 455 раз и строчной 395 раз, то
# есть разнобой у книги СВОЙ, а не привнесён переводом, и решать его владельцу.
# Проверяется другое: место, где мастер дал строчную, а перевод — заглавную.
DASH_CAP = re.compile(r'</strong>\s*—\s*([^\s<])')


def check_dash(lg: str) -> list:
    if lg == 'az':
        return []
    hits = []
    for c in cards():
        base = DIRS['az'] / f'{c}.html'
        fp = DIRS[lg] / f'{c}.html'
        if not fp.exists():
            continue
        a = [(t, DASH_CAP.search(b)) for t, m_, i_, b in blocks(base.read_text(encoding='utf-8', errors='ignore'))]
        o = [(t, DASH_CAP.search(b)) for t, m_, i_, b in blocks(fp.read_text(encoding='utf-8', errors='ignore'))]
        if len(a) != len(o):
            continue                    # рассинхрон блоков — забота paracheck.py
        for (at, am), (ot, om) in zip(a, o):
            if not (am and om):
                continue
            if am.group(1).islower() and om.group(1).isupper():
                hits.append((lg + '/' + c, om.group(1), ot[:120]))
    return hits


# ── 2. висящее сказуемое ───────────────────────────────────────────────────
# причастие во множественном + глагол-связка в единственном рядом
HANG = re.compile(
    r'([' + CYR_LO + r']{3,}(?:ющие|щие|нные|емые))'
    r'([^.!?]{0,80}?)\s(является|характеризуется|относится)\b')
# Связка сразу за выделенным куском: «<strong>При котором … эпизода</strong>
# является первичным психотическим расстройством». В целом тексте <strong>
# выделяет термин, и связка стоит ПЕРЕД ним, а не после.
#
# Раньше здесь стояла проверка «глагол в последней четверти длинного блока»,
# и она давала 34 ложных срабатывания из 36: «не является основным лечением»,
# «ОАТ является золотым стандартом» — обычная русская речь. Признак заменён
# на разметочный, потому что ломается именно разметка.
AFTER_STRONG = re.compile(
    r'</strong>\s*(является|захватывает|занимает|представляет собой)\b')


def check_hang(lg: str) -> list:
    if lg != 'ru':
        return []
    hits = []
    for fp in pages(lg):
        for txt, marks, icd, body in blocks(fp.read_text(encoding='utf-8', errors='ignore')):
            name = fp.parent.name + '/' + fp.stem
            for m in HANG.finditer(txt):
                hits.append((name, 'согласование', txt[max(0, m.start() - 40):m.end() + 30]))
            for m in AFTER_STRONG.finditer(body):
                plain = re.sub(r'\s+', ' ', re.sub(r'<[^>]*>', '', body))
                hits.append((name, 'связка за выделением', plain[:130]))
    return hits


# ── 3. чужое слово, не переведённое вовсе ──────────────────────────────────
def vocab(lg: str) -> Counter:
    c = Counter()
    for fp in pages(lg):
        for w in LATIN_WORD.findall(visible(fp.read_text(encoding='utf-8', errors='ignore'))):
            c[w.lower()] += 1
    return c


ROMAN = re.compile(r'^[IVXLC]+$')


def check_alien(lg: str) -> list:
    # Турецкий и азербайджанский — родственные языки с общим словарём, и
    # «известно азербайджанскому» там не признак утечки: проверка дала 12 418
    # срабатываний на обычных турецких словах. Для турецкого неприменима.
    if lg in ('az', 'tr'):
        return []
    az, en = vocab('az'), vocab('en')
    hits = []
    for fp in pages(lg):
        raw = fp.read_text(encoding='utf-8', errors='ignore')
        v = visible(raw, keep_marks=True)
        # выкидываем то, что помечено как иноязычная вставка осознанно
        v = re.sub(r'\x02[a-z]{2}\x02[\s\S]*?\x03', ' ', v)
        v = v.replace('\x04', ' ')
        for m in LATIN_WORD.finditer(v):
            tok = m.group(0)
            w = tok.lower()
            # аббревиатура и римская цифра пишутся одинаково на всех языках
            if len(w) < 3 or tok.isupper() or ROMAN.match(tok):
                continue
            # известно азербайджанскому и неизвестно английскому — утечка
            if az[w] >= 2 and en[w] == 0:
                hits.append((fp.parent.name + '/' + fp.stem, m.group(0),
                             v[max(0, m.start() - 50):m.end() + 30].strip()))
    return hits


# ── 4. ё и е в одном слове ─────────────────────────────────────────────────
def check_yo(lg: str) -> list:
    if lg != 'ru':
        return []
    forms = defaultdict(Counter)
    where = defaultdict(set)
    for fp in pages(lg):
        v = visible(fp.read_text(encoding='utf-8', errors='ignore'))
        for w in re.findall(r'[' + CYR_UP + CYR_LO + r']{4,}', v):
            wl = w.lower()
            forms[wl.replace('ё', 'е')][wl] += 1
            where[wl].add(fp.stem)
    hits = []
    for key, variants in forms.items():
        if len(variants) < 2:
            continue
        yo = [w for w in variants if 'ё' in w]
        no = [w for w in variants if 'ё' not in w]
        if not (yo and no):
            continue
        hits.append(('ru', key,
                     ' · '.join(f'{w}×{variants[w]} ({",".join(sorted(where[w])[:3])})'
                                for w in sorted(variants, key=lambda x: -variants[x]))))
    return hits


# ── 5. фамилия кириллицей ──────────────────────────────────────────────────
# «Эскироль Ж.-Э.», «Кальбаум К. (1863)», «Лингам Р.»
CYR_NAME = re.compile(
    r'\b([' + CYR_UP + r'][' + CYR_LO + r']{2,}(?:-[' + CYR_UP + r'][' + CYR_LO + r']{2,})?)'
    r' ([' + CYR_UP + r']\.(?:\s?-?[' + CYR_UP + r']\.)?)')


# Русская фамилия кириллицей — не транслитерация, а родное написание;
# «синдром Корсакова» идёт кириллицей по всей карточке 6D72.
NATIVE = {'Корсаков', 'Бехтерев', 'Ганнушкин', 'Снежневский', 'Павлов'}


def check_names(lg: str) -> list:
    if lg != 'ru':
        return []
    hits = []
    for fp in pages(lg):
        for txt, marks, icd, body in blocks(fp.read_text(encoding='utf-8', errors='ignore')):
            for m in CYR_NAME.finditer(txt):
                if m.group(1) in NATIVE:
                    continue
                hits.append((fp.parent.name + '/' + fp.stem, m.group(0),
                             txt[max(0, m.start() - 40):m.end() + 30]))
    return hits


CHECKS = [
    ('caps',  'ЗАГЛАВНАЯ ПОСРЕДИ ФРАЗЫ', check_caps),
    ('dash',  'ПОСЛЕ ТИРЕ ЗАГЛАВНАЯ, В МАСТЕРЕ СТРОЧНАЯ', check_dash),
    ('hang',  'ВИСЯЩЕЕ СКАЗУЕМОЕ', check_hang),
    ('alien', 'ЧУЖОЕ СЛОВО БЕЗ ПЕРЕВОДА', check_alien),
    ('yo',    'Ё И Е В ОДНОМ СЛОВЕ', check_yo),
    ('names', 'ФАМИЛИЯ КИРИЛЛИЦЕЙ', check_names),
]


def main() -> int:
    langs = [LANG] if LANG else ['ru', 'en', 'tr']
    total = 0
    print('=' * 72)
    print('СЛЕДЫ МЕХАНИЧЕСКОГО ПЕРЕВОДА')
    print('=' * 72)
    for key, title, fn in CHECKS:
        if CHECK and CHECK != key:
            continue
        rows = []
        for lg in langs:
            rows += fn(lg)
        total += len(rows)
        print(f'\n{title}: {len(rows)}')
        for r in rows[:LIMIT]:
            print(f'   {r[0]:14} {r[1]}')
            print(f'                  …{r[2]}…')
        if len(rows) > LIMIT:
            print(f'   …ещё {len(rows) - LIMIT}')
    print(f'\nвсего мест на разбор: {total}')
    return 1 if total else 0


if __name__ == '__main__':
    raise SystemExit(main())
