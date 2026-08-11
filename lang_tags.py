#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lang_tags.py — расставляет метки языка на иноязычные куски книги.

Зачем. Страница помечена одним языком (`<html lang="tr">`), но внутри неё
законно живут английские названия: имя расстройства по XBT-11, шкала
«Adult ADHD Self-Report Scale», руководство «Clinical Practice Guideline for
the Treatment of PTSD», список литературы целиком. Без метки такой кусок
неотличим от турецкой прозы — и любая проверка орфографии (или машинный
перевод, или экранный диктор) считает его ошибкой. Так и вышло со «stress»:
478 турецких вхождений выглядели дефектом, а на деле 476 были именами файлов
и слагами, а оставшиеся — английскими названиями.

Метка — стандартный HTML-атрибут `lang`. Он ничего не ломает, читается
браузером, экранным диктором и переводчиком, и по нему инструмент может
пропустить кусок, не гадая.

Два этапа, разные по надёжности:

  A. Контейнеры — по разметке, без догадок:
       <div class="dh-en">      английское имя болезни в шапке карточки
       <ol class="ref-list">    список литературы, целиком английский
       English-колонка в таблицах сокращений и глоссария
  B. Внутри прозы — <span lang="en"> вокруг английских оборотов. Здесь
     нужен разбор, поэтому правило узкое и проверяемое: берём подряд идущие
     латинские слова и метим только те цепочки, где есть английское служебное
     слово (for, of, the, and, in, with…) либо слово с английским окончанием
     (-tion, -ment, -ing, -ity…). «Stress» маркером НЕ считается: в
     азербайджанском это своё слово с тем же написанием.

    python lang_tags.py            # разбор, ничего не пишет
    python lang_tags.py --apply
    python lang_tags.py --show 40  # показать, что именно будет помечено
"""
from __future__ import annotations
import re, sys, io
from pathlib import Path
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
BOOK = ROOT / 'klinik-psixiatriya'
DIRS = {'az': BOOK, 'ru': BOOK / 'ru', 'en': BOOK / 'en', 'tr': BOOK / 'tr'}
APPLY = '--apply' in sys.argv
SHOW = int(sys.argv[sys.argv.index('--show') + 1]) if '--show' in sys.argv else 0

# ── A. контейнеры ───────────────────────────────────────────────────────────
CONTAINERS = [
    (re.compile(r'<div class="dh-en">(?![\s\S]{0,4}lang=)'), '<div class="dh-en" lang="en">'),
    (re.compile(r'<ol class="ref-list">'), '<ol class="ref-list" lang="en">'),
]

# ── B. английские обороты внутри прозы ──────────────────────────────────────
# Буквы, которых в английском не бывает: встретилась — цепочка не английская.
NATIVE = 'əƏğĞıİşŞüÜöÖçÇА-Яа-яЁё'
# Служебные слова, встречающиеся ВНУТРИ английских названий. Короткие «on»,
# «at», «to», «by» отсюда убраны намеренно: «on» — турецкое и азербайджанское
# «десять», и на нём разбор уезжал в родную прозу.
FN = {'for', 'of', 'the', 'and', 'with', 'from', 'in', 'otherwise', 'specified',
      'associated', 'due', 'without', 'versus', 'among', 'related', 'across',
      'into', 'through'}
# Метим только то, что имеет форму английского названия: цепочка слов
# с заглавной буквы, между ними допустимы служебные слова. Именно так
# выглядят в книге шкалы, руководства и официальные имена болезней.
CAP = re.compile(r"^(?:[A-Z][A-Za-z'’-]*|[A-Z]{2,})$")
MIN_CAPS = 2

TOKEN = r"[A-Za-z][A-Za-z'’-]*"
# Родные буквы вплотную к цепочке значат, что это обрубок родного слова:
# «haftalık» даёт латинское «haftal», «başlangıç» — «ba». Без этой границы
# турецкая проза выглядела английской.
EDGE = "A-Za-z" + NATIVE
RUN = re.compile(r'(?<![' + EDGE + r'-])' + TOKEN + r'(?:[\s/-]+' + TOKEN +
                 r')+(?![' + EDGE + r'-])')
# куски, внутрь которых лезть нельзя
SKIP = re.compile(r'<(script|style|nav|aside|head|title|h1)[\s\S]*?</\1>|'
                  r'<ol class="ref-list"[\s\S]*?</ol>|'
                  r'<div class="dh-en"[\s\S]*?</div>|'
                  # уже помеченное не метим повторно — иначе второй прогон
                  # вложит метку в метку. Правило общее: любой элемент,
                  # несущий lang, разобран и внутрь него лезть незачем
                  # (так, колонка <td lang="en"> в таблице терминов).
                  r'<(span|td|th|div|p|li)[^>]*\blang="[^"]*"[^>]*>[\s\S]*?</\2>|'
                  r'<[^>]*>|<!--[\s\S]*?-->', re.I)


# ── словарь улик: строится из самой книги, а не из головы ───────────────────
# Английский корпус — дерево en/, оно одноязычно по построению. Родной корпус —
# те куски своего дерева, где есть родная буква: такой отрезок точно не
# английский, и его латинские слова — родные. Слово считается уликой, если оно
# заметно живёт в английском корпусе и практически не встречается в родном.
# Так «Guideline», «Therapy», «Scale» становятся уликами, а «Klinik»,
# «Taban», «Bozukluklar» — нет, и турецкое название в заглавном регистре
# больше не выглядит английским.
TOKRX = re.compile(r"[A-Za-z][A-Za-z'’-]*")
BRAND = {'ragimoff', 'rahimov', 'kenan', 'azerbaijan', 'azerbaycan'}


def _visible(t: str) -> str:
    t = re.sub(r'<(script|style|nav|aside|head)[\s\S]*?</\1>', ' ', t)
    t = re.sub(r'<ol class="ref-list"[^>]*>[\s\S]*?</ol>', ' ', t)
    t = re.sub(r'<div class="dh-en"[^>]*>[\s\S]*?</div>', ' ', t)
    return re.sub(r'<[^>]*>', ' ', t)


def build_vocab(folder: Path) -> set:
    en = Counter()
    for f in (BOOK / 'en').glob('*.html'):
        for w in TOKRX.findall(_visible(f.read_text(encoding='utf-8', errors='ignore'))):
            en[w.lower()] += 1
    nat = Counter()
    for f in folder.glob('*.html'):
        for seg in re.split(r'[.;:!?()«»„“”\[\]]',
                            _visible(f.read_text(encoding='utf-8', errors='ignore'))):
            if re.search('[' + NATIVE + ']', seg):
                for w in TOKRX.findall(seg):
                    nat[w.lower()] += 1
    ev = {w for w, c in en.items()
          if c >= 5 and nat[w] <= 2 and len(w) > 2 and w not in BRAND}
    # Родное слово — частое в родных отрезках И редкое в английском корпусе.
    # Без второго условия сюда попадали «disorder», «psychiatry», «program»:
    # они часто стоят внутри английских названий посреди родной фразы, и
    # подрезка съедала у названия хвост («British Journal» вместо
    # «British Journal of Psychiatry»).
    return ev, {w for w, c in nat.items() if c >= 3 and en[w] < 5}


EVIDENCE: set = set()
NATIVE_WORDS: set = set()
# «ABD'de», «Kanada'da», «PPD'yi» — родное слово с апострофом и падежом:
# в английских названиях такой формы не бывает.
APOS = re.compile(r"[A-Za-z]['’](?:de|da|te|ta|ye|ya|yi|yı|nin|nın|in|ın|nun|nün|ni|nı|n)$")


def trim(run: str) -> str:
    """Срезает с краёв родные слова, случайно попавшие в цепочку."""
    parts = re.split(r"([^A-Za-z'’-]+)", run)
    while parts and (not parts[0].strip() or parts[0].lower() in NATIVE_WORDS
                     or APOS.search(parts[0])):
        parts = parts[2:] if len(parts) > 1 else []
    while parts and (not parts[-1].strip() or parts[-1].lower() in NATIVE_WORDS
                     or APOS.search(parts[-1])):
        parts = parts[:-2] if len(parts) > 1 else []
    return ''.join(parts)


def is_english(run: str) -> bool:
    toks = re.findall(TOKEN, run)
    if len(toks) < 2 or re.search('[' + NATIVE + ']', run):
        return False
    # «Bohus M.», «LaFrance W.» — фамилия с инициалом, не английская фраза.
    if any(len(t) == 1 for t in toks):
        return False
    caps = [t for t in toks if CAP.match(t)]
    if len(caps) < MIN_CAPS:
        return False
    # каждое слово — либо часть названия с заглавной, либо служебное
    if not all(CAP.match(t) or t.lower() in FN for t in toks):
        return False
    # и хотя бы одно слово должно быть уликой английского
    return any(t.lower() in EVIDENCE for t in toks)


def tag_inline(text: str, found: list) -> str:
    """Оборачивает английские цепочки в <span lang="en">, минуя разметку."""
    out, pos = [], 0
    for skip in SKIP.finditer(text):
        chunk = text[pos:skip.start()]
        out.append(mark(chunk, found))
        out.append(skip.group(0))
        pos = skip.end()
    out.append(mark(text[pos:], found))
    return ''.join(out)


def mark(chunk: str, found: list) -> str:
    if not chunk.strip():
        return chunk
    res, last = [], 0
    for m in RUN.finditer(chunk):
        if not is_english(m.group(0)):
            continue
        whole = m.group(0)
        run = trim(whole).rstrip("-'’")
        if not is_english(run):
            continue
        # Два порядка важны. Первый: префикс дописываем ТОЛЬКО когда цепочка
        # принята, иначе при отбраковке он уходит в вывод, а указатель не
        # сдвигается — и текст удваивается. Второй: trim() срезает слова и
        # СЛЕВА, поэтому остаток нельзя брать по длине: «Top Lang Disord»
        # давало «Lang Disord» + «sord», теряя начало и дублируя хвост.
        i = whole.find(run)
        res.append(chunk[last:m.start()])
        res.append(whole[:i])
        res.append('<span lang="en">' + run + '</span>')
        res.append(whole[i + len(run):])
        found.append(run)
        last = m.end()
    res.append(chunk[last:])
    return ''.join(res)


# ── C. азербайджанские вставки в переводах ─────────────────────────────────
# В русском и английском деревьях азербайджанский узнаётся по любой из букв
# ə ı ş ğ ç ü ö — латиница там сама по себе чужая. В турецком все они, кроме
# «ə», свои, поэтому там маркер только один. Так помечаются столбцы
# азербайджанских терминов в справочных таблицах и имя автора.
# «ü» и «ö» из набора убраны: на них ловились шведская фамилия Öst L.G.,
# немецкая Wölfling и турецкое слово «kültür», процитированное в глоссарии.
# Букв ə ı İ ş ğ ç хватает, чтобы узнать азербайджанский, и они не бывают
# в немецком, шведском и английском.
AZ_MARK = {'ru': 'əƏıİşŞğĞçÇ', 'en': 'əƏıİşŞğĞçÇ', 'tr': 'əƏ'}
AZ_RUN = r"[A-Za-zəƏıİşŞğĞçÇüÜöÖ][A-Za-zəƏıİşŞğĞçÇüÜöÖ'’.-]*"


def mark_az(chunk: str, marks: str, found: list) -> str:
    rx = re.compile(AZ_RUN + r'(?:[  ]' + AZ_RUN + r')*')
    res, last = [], 0
    for m in rx.finditer(chunk):
        run = m.group(0).rstrip('.-')
        if not run or not re.search('[' + marks + ']', run):
            continue
        res.append(chunk[last:m.start()])
        res.append('<span lang="az">' + run + '</span>')
        res.append(m.group(0)[len(run):])
        found.append(run)
        last = m.end()
    res.append(chunk[last:])
    return ''.join(res)


def tag_az(text: str, marks: str, found: list) -> str:
    out, pos = [], 0
    for skip in SKIP.finditer(text):
        out.append(mark_az(text[pos:skip.start()], marks, found))
        out.append(skip.group(0))
        pos = skip.end()
    out.append(mark_az(text[pos:], marks, found))
    return ''.join(out)


# ── D. английский термин, поясняемый в кавычках или скобках ────────────────
# Кенан описал этот случай прямо: на странице всё на родном языке, а в скобках
# рядом стоит термин по-английски. Такая глосса опознаётся по обрамлению, а не
# по форме слов, поэтому правило надёжнее общего разбора прозы и берёт то, что
# этап B пропускает: строчные обороты («doctor shopping», «wait and see») и
# одиночные слова («maintenance», «bizarre»).
#
# Что сюда НЕ попадает и почему:
#   «Barkley», «Frank E.», «Azrin N.H.», «Blank et al.» — фамилии авторов;
#       фамилия не английский текст, помечать её языком неверно;
#   «EIP», «HBOT», «M-CHAT-R/F» — аббревиатуры, это не проза;
#   «lupus», «herpes» — латынь, а не английский.
GLOSS = re.compile("([«“„‘(]\s*)"
                   "([A-Za-z][A-Za-z ’'./+-]{2,60}?)"
                   "(\s*[»”“’)])")
INITIAL = re.compile(r"^[A-Z]\.?(?:[A-Z]\.)?$")


def is_gloss(txt: str) -> bool:
    toks = re.findall(r"[A-Za-z][A-Za-z'’-]*", txt)
    if not toks or ' et al' in txt.lower():
        return False
    if any(INITIAL.match(t) for t in re.findall(r"[A-Za-z]\.?", txt)):
        return False
    if all(t.isupper() for t in toks):          # чистая аббревиатура
        return False
    if not any(t.islower() for t in toks):      # только имена с заглавной
        return False
    # «animal toplama» — половина фразы азербайджанская; целиком английской
    # её метить нельзя (сама фраза — отдельный дефект, не дело метки)
    if any(t.lower() in NATIVE_WORDS for t in toks):
        return False
    return any(t.lower() in EVIDENCE for t in toks)


def tag_gloss(text: str, found: list) -> str:
    out, pos = [], 0
    for skip in SKIP.finditer(text):
        out.append(mark_gloss(text[pos:skip.start()], found))
        out.append(skip.group(0))
        pos = skip.end()
    out.append(mark_gloss(text[pos:], found))
    return ''.join(out)


def mark_gloss(chunk: str, found: list) -> str:
    def rep(m):
        if not is_gloss(m.group(2)):
            return m.group(0)
        found.append(m.group(2))
        return m.group(1) + '<span lang="en">' + m.group(2) + '</span>' + m.group(3)
    return GLOSS.sub(rep, chunk)


# ── E. русские вставки в остальных деревьях ────────────────────────────────
# Трёхъязычные таблицы сокращений и глоссария держат русскую колонку на
# азербайджанской, английской и турецкой страницах. Кириллица опознаётся
# однозначно — гадать не о чем.
CYR_RUN = re.compile(r'[А-яЁё][А-яЁё-]*'
                     r'(?:[  ][А-яЁё][А-яЁё-]*)*')


def mark_ru(chunk: str, found: list) -> str:
    res, last = [], 0
    for m in CYR_RUN.finditer(chunk):
        run = m.group(0).strip('- ')
        if len(run) < 3:
            continue
        res.append(chunk[last:m.start()])
        res.append('<span lang="ru">' + run + '</span>')
        res.append(m.group(0)[len(run):])
        found.append(run)
        last = m.end()
    res.append(chunk[last:])
    return ''.join(res)


def tag_ru(text: str, found: list) -> str:
    out, pos = [], 0
    for skip in SKIP.finditer(text):
        out.append(mark_ru(text[pos:skip.start()], found))
        out.append(skip.group(0))
        pos = skip.end()
    out.append(mark_ru(text[pos:], found))
    return ''.join(out)


# ── A2. таблица кодов: три языковые колонки ────────────────────────────────
# «Kod | Azərbaycanca | English (ICD-11) | Русский (МКБ-11)» — смысл таблицы
# в том, что колонки на РАЗНЫХ языках, и в каждом издании они одни и те же.
# Помечаем сразу столбцами: гадать не о чем, шапка сама это объявляет.
CODE_ROW = re.compile(r'(<tr><td class="kod-cell">[^<]*</td>)'
                      r'(<td[^>]*>)([\s\S]*?)(</td>)'
                      r'(<td[^>]*>)([\s\S]*?)(</td>)'
                      r'(<td[^>]*>)([\s\S]*?)(</td>)')


def tag_code_table(text: str) -> tuple[str, int]:
    n = 0

    def row(m):
        nonlocal n
        g = list(m.groups())
        for idx, lg in ((1, 'az'), (4, 'en'), (7, 'ru')):
            if 'lang=' not in g[idx]:
                g[idx] = g[idx][:-1] + f' lang="{lg}">'
                n += 1
        return ''.join(g)

    text, k = CODE_ROW.subn(row, text)
    # ячейка уже несёт язык — вложенная метка того же языка избыточна
    text = re.sub(r'(<td lang="(\w\w)">)<span lang="\2">((?:(?!</span>)[\s\S])*)</span>(</td>)',
                  r'\1\3\4', text)
    return text, n


def main() -> int:
    grand, examples = Counter(), []
    for lg, folder in DIRS.items():
        if not folder.is_dir():
            continue
        global EVIDENCE, NATIVE_WORDS
        EVIDENCE, NATIVE_WORDS = build_vocab(folder)
        cont = inline = files = azn = gln = run_ = 0
        for fp in sorted(folder.glob('*.html')):
            raw = fp.read_bytes().decode('utf-8')
            crlf = raw.count('\r\n') > raw.count('\n') // 2
            t = raw.replace('\r\n', '\n')
            new = t
            for rx, rep in CONTAINERS:
                new, n = rx.subn(rep, new)
                cont += n
            new, n = tag_code_table(new)
            cont += n
            body = re.search(r'<main[\s\S]*</main>', new) if lg != 'en' else None
            if body:
                found = []
                tagged = tag_inline(body.group(0), found)
                if found:
                    new = new[:body.start()] + tagged + new[body.end():]
                    inline += len(found)
                    for f in found:
                        grand[f] += 1
                    if len(examples) < 400:
                        examples += [(fp.stem, f) for f in found[:4]]
            if lg != 'en':
                body = re.search(r'<main[\s\S]*</main>', new)
                if body:
                    gl = []
                    tagged = tag_gloss(body.group(0), gl)
                    if gl:
                        new = new[:body.start()] + tagged + new[body.end():]
                        gln += len(gl)
            if lg != 'ru':
                body = re.search(r'<main[\s\S]*</main>', new)
                if body:
                    ru = []
                    tagged = tag_ru(body.group(0), ru)
                    if ru:
                        new = new[:body.start()] + tagged + new[body.end():]
                        run_ += len(ru)
            if lg in AZ_MARK:
                body = re.search(r'<main[\s\S]*</main>', new)
                if body:
                    az = []
                    tagged = tag_az(body.group(0), AZ_MARK[lg], az)
                    if az:
                        new = new[:body.start()] + tagged + new[body.end():]
                        azn += len(az)
            if new == t:
                continue
            files += 1
            if APPLY:
                fp.write_bytes((new.replace('\n', '\r\n') if crlf else new).encode('utf-8'))
        print(f'  {lg}: файлов {files}, контейнеров {cont}, '
              f'английских оборотов {inline}, глосс {gln}, '
              f'азербайджанских {azn}, русских {run_}')
    if SHOW:
        print('\nчто помечено (по убыванию частоты):')
        for k, v in grand.most_common(SHOW):
            print(f'    ×{v:<4} {k}')
    print(f'\nвсего оборотов {sum(grand.values())}, уникальных {len(grand)}')
    print('применено' if APPLY else 'пробный прогон — запустить с --apply')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
