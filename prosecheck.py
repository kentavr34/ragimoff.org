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
    # «ГнРГ», «мРНК» — аббревиатура со строчной внутри, а не слово с
    # заглавной: без этого «Агонист ГнРГ» отдавал мнимое слово «Гн»
    r'(?:-[' + CYR_UP + CYR_LO + r'][' + CYR_LO + r']+)?)(?![' + CYR_UP + r'])')
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
    # Мастер сам объявляет, какие латинские слова у него английские: они
    # стоят в <span lang="en">. «bailout», «Q-tip» — английские термины,
    # и в переводе им место; азербайджанскими их считать нельзя.
    az_en = set()
    for fp in pages('az'):
        for m in re.finditer(r'<span lang="en"[^>]*>([\s\S]*?)</span>',
                             fp.read_text(encoding='utf-8', errors='ignore')):
            az_en |= {w.lower() for w in LATIN_WORD.findall(H.unescape(m.group(1)))}
    hits = []
    for fp in pages(lg):
        raw = fp.read_text(encoding='utf-8', errors='ignore')
        v = visible(raw, keep_marks=True)
        # Обходится только вставка на СВОЁМ языке: «<span lang="az">» в
        # русском тексте — осознанный азербайджанский термин.
        #
        # Помеченное как английское НЕ обходится. Однажды lang_tags.py принял
        # азербайджанское «network meta-analiz» за английское и обернул его в
        # <span lang="en"> — утечка спряталась за меткой и стала невидимой.
        # Частотный признак ниже (известно аз., неизвестно англ.) отличает
        # настоящий английский сам, метка ему не нужна.
        v = re.sub(chr(2) + r'(?!en)[a-z]{2}' + chr(2) + r'[\s\S]*?' + chr(3), ' ', v)
        # Только сами маркеры. Отдельной заменой «en» на пробел здесь стоять
        # не может: подстрока «en» сидит внутри слов, и «Impulsiveness»
        # распадалось на «Impulsiv» и «ess», «Levenson» — на «Lev» и «son».
        v = re.sub('[' + chr(2) + chr(3) + chr(4) + ']', ' ', v)
        for m in LATIN_WORD.finditer(v):
            tok = m.group(0)
            w = tok.lower()
            # аббревиатура и римская цифра пишутся одинаково на всех языках
            if len(w) < 3 or tok.isupper() or ROMAN.match(tok):
                continue
            # известно азербайджанскому и неизвестно английскому — утечка
            if az[w] >= 2 and en[w] == 0 and w not in az_en:
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


# ── 6. имя, пропавшее в переводе ───────────────────────────────────────────
# Проверка выше ловит фамилию, записанную кириллицей С ИНИЦИАЛАМИ. Но
# «Эскироль (1838)» и «Акискаль — 15–50% конверсия» инициалов не имеют, и
# шаблон их не видел. Здесь другой признак: латинское слово, которое стоит
# и в мастере, и в английском переводе на одном и том же месте, а в третьем
# переводе исчезло. Согласие двух источников делает пропажу однозначной.
#
# Именем считается только ЦИТАТНАЯ форма: фамилия с инициалами, с годом или
# с «et al.». Без этого сужения проверка дала 1521 срабатывание — она ловила
# всякий английский термин, законно переведённый («Mental Retardation» →
# «Умственная отсталость»), и эпонимы, которые по-русски и пишутся кириллицей
# («синдром Дауна», «синдром Эдвардса»). Ни то, ни другое дефектом не является.
NAMEISH = re.compile(
    r'(?<![\w-])([A-Z][a-zA-Zöäüéèçß]{3,})'
    r'(?=\s(?:[A-Z]\.|et al|\(\d{4}))')
# Обычное английское слово, за которым случайно стоит год: «Guideline (2010)»,
# «Definition (2002, обновление)», «Schedule I».
NOT_NAME = {'Diagnostic', 'Clinical', 'International', 'World', 'American',
            'Definition', 'Commitments', 'Guideline', 'Guidelines', 'Schedule',
            'Practice', 'Report', 'Update', 'Consensus', 'Statement', 'Edition',
            'Version', 'Manual', 'Criteria', 'Study', 'Trial', 'Review'}


def check_lostname(lg: str) -> list:
    if lg in ('az', 'en'):
        return []
    hits = []
    for c in cards():
        fps = [DIRS[x] / f'{c}.html' for x in ('az', 'en', lg)]
        if not all(f.exists() for f in fps):
            continue
        bl = [blocks(f.read_text(encoding='utf-8', errors='ignore')) for f in fps]
        if len({len(b) for b in bl}) != 1:
            continue                    # рассинхрон блоков — забота paracheck.py
        for az_b, en_b, ot_b in zip(*bl):
            shared = ({m.group(1) for m in NAMEISH.finditer(az_b[0])}
                      & {m.group(1) for m in NAMEISH.finditer(en_b[0])}) - NOT_NAME
            for w in sorted(shared):
                # русская фамилия по-русски и пишется кириллицей — см. NATIVE
                if lg == 'ru' and w in ('Korsakoff', 'Bekhterev', 'Pavlov'):
                    continue
                if w not in ot_b[0]:
                    hits.append((lg + '/' + c, w, ot_b[0][:120]))
    return hits


# ── 7. дефект мастера, уцелевший в переводе ────────────────────────────────
# `regress.py` помнит строки, вычищенные ИЗ МАСТЕРА, — но перевод мог их
# сохранить. Так уцелело турецкое «resmiyet» (девять мест), английские
# «neglect», «fostering», «D-cycloserine» в русском.
#
# Английское дерево из проверки исключено: там английское слово на месте.
# Границы слова обязательны — иначе «tikler» находится внутри
# «antipsikotikler», а «erjik» внутри законного «serotonerjik».
AZLET = 'əƏıİşŞğĞçÇöÖüÜ'


def gone_latin() -> list[str]:
    import ast
    src = (ROOT / 'regress.py').read_text(encoding='utf-8')
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], 'id', '') == 'GONE':
            gone = ast.literal_eval(node.value)
            return [s for s in gone['az']
                    if re.fullmatch(r"[A-Za-z][A-Za-z '-]{3,}", s)
                    and not any(ch in AZLET for ch in s)]
    return []


def check_survived(lg: str) -> list:
    if lg in ('az', 'en'):
        return []
    # Строка засчитывается, только если она есть в АНГЛИЙСКОМ дереве, то есть
    # это настоящий английский, не переведённый. Без этого условия проверка
    # ловила «apnesi» и «erjik» — формы, которые в азербайджанском запрещены
    # решением владельца, а в турецком как раз правильны.
    en = vocab('en')
    words = [s for s in gone_latin()
             if all(en[w.lower()] for w in re.findall(r"[A-Za-z'-]+", s))]
    if not words:
        return []
    rx = re.compile(r'(?<![\w-])(' + '|'.join(
        sorted(map(re.escape, words), key=len, reverse=True)) + r')(?![\w-])')
    hits = []
    for fp in pages(lg):
        v = visible(fp.read_text(encoding='utf-8', errors='ignore'))
        for m in rx.finditer(v):
            hits.append((lg + '/' + fp.stem, m.group(1),
                         v[max(0, m.start() - 55):m.end() + 40]))
    return hits


# ── разобрано и признано нормой ────────────────────────────────────────────
# Строки, прочитанные глазами и сверенные с мастером. Инструмент должен
# давать ноль на здоровом дереве: отчёт, где всегда висит десяток известных
# срабатываний, приучает не смотреть в отчёт.
ACCEPTED = {
    # имя собственное или устойчивое написание
    'болезни Пика', 'Болезнь Пика', 'тельца Пика', 'во Второй мировой',
    # название инструмента и документа
    'и Интервью для диагностики', ') Международные клинические',
    # официальное название программы EMA/MHRA
    'условий Программы предотвращения',
    # «Доказательства: является …» повторяет эллипсис мастера, где подлежащее
    # тоже опущено: «Sübut: qurban üçün travmadır»
    'Доказательства: является', 'Доказательства: БДСМ по согласию',
    # «<strong>не</strong> является» — связка относится к выделенному «не»
    'Билингвизм', 'логопедом (SLP)',
    # имя гена: английский и русский тоже пишут его латиницей
    'clock gen mutasyonları',
    # обычная речь, а не разрыв согласования
    'связанное с волосами и кожей, не является',
    'именно эта цифра является заглавной', 'не является «излечением»',
}


def accepted(fragment: str) -> bool:
    return any(a in fragment for a in ACCEPTED)


CHECKS = [
    ('caps',  'ЗАГЛАВНАЯ ПОСРЕДИ ФРАЗЫ', check_caps),
    ('hang',  'ВИСЯЩЕЕ СКАЗУЕМОЕ', check_hang),
    ('alien', 'ЧУЖОЕ СЛОВО БЕЗ ПЕРЕВОДА', check_alien),
    ('yo',    'Ё И Е В ОДНОМ СЛОВЕ', check_yo),
    ('names', 'ФАМИЛИЯ КИРИЛЛИЦЕЙ', check_names),
    ('lostname', 'ИМЯ ЕСТЬ В МАСТЕРЕ И В АНГЛИЙСКОМ, В ПЕРЕВОДЕ НЕТ', check_lostname),
    ('survived', 'ВЫЧИЩЕНО ИЗ МАСТЕРА, УЦЕЛЕЛО В ПЕРЕВОДЕ', check_survived),
]

# Справочная проверка: в общий прогон не входит, запускается по требованию
# (`--check dash`). Это не брак, а вопрос типографики к владельцу: 90–96%
# пунктов следуют выбору мастера, оставшиеся 137 разошлись, но читаются
# правильно («— Тревога/депрессия (СИОЗС + КПТ)»), а русская заглавная после
# тире зависит ещё и от того, полное ли предложение следует. Держать её в
# постоянном отчёте — приучать не смотреть в отчёт.
ON_DEMAND = [('dash', 'ПОСЛЕ ТИРЕ ЗАГЛАВНАЯ, В МАСТЕРЕ СТРОЧНАЯ', check_dash)]


def main() -> int:
    langs = [LANG] if LANG else ['ru', 'en', 'tr']
    total = 0
    print('=' * 72)
    print('СЛЕДЫ МЕХАНИЧЕСКОГО ПЕРЕВОДА')
    print('=' * 72)
    for key, title, fn in CHECKS + ON_DEMAND:
        if CHECK != key and (CHECK or (key, title, fn) in ON_DEMAND):
            continue
        rows = []
        for lg in langs:
            rows += fn(lg)
        rows = [r for r in rows if not accepted(str(r[2]))]
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
