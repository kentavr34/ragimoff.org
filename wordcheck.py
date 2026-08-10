# -*- coding: utf-8 -*-
"""
wordcheck.py — редкие слова азербайджанского мастера как след порчи текста.

«həyətəm», «rağın», «qıçtı», «qıdaşdırma», «çiknə», «tezbir», «kütəbə»,
«weksloid», «qaz-zəkam» — все обломки, которые уже нашлись в книге,
объединяет одно: каждый встречается один-два раза на весь корпус.
Настоящий термин повторяется, обломок — нет.

Инструмент строит частотный словарь азербайджанского мастера и показывает
слова, встречающиеся реже порога, отсеивая то, что редко по естественным
причинам: латиницу (названия шкал и препаратов), числа, аббревиатуры,
имена собственные из списков литературы.

    python wordcheck.py               # редкие слова с контекстом
    python wordcheck.py --min 3       # порог частоты
    python wordcheck.py --latin       # английские вкрапления в тексте
"""
from __future__ import annotations
import re, sys, io, html as H
from collections import Counter
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
BOOK = ROOT / 'klinik-psixiatriya'
LOOSE = re.compile(r'<(?![a-zA-Z/!?])')
AZ = 'a-zçəğıöşüA-ZÇƏĞİÖŞÜ'
WORD = re.compile(f'[{AZ}]{{4,}}(?:-[{AZ}]{{2,}})?')
LATIN_ONLY = re.compile(r'^[a-zA-Z-]+$')
MIN = int(sys.argv[sys.argv.index('--min') + 1]) if '--min' in sys.argv else 2


def pages():
    for fp in sorted(BOOK.glob('*.html')):
        if fp.stem.startswith('bolme-') or fp.stem in {'index', 'mundericat'}:
            continue
        yield fp


def visible(fp: Path) -> str:
    t = fp.read_text(encoding='utf-8', errors='ignore')
    t = re.sub(r'<(script|style)\b[\s\S]*?</\1>', ' ', t, flags=re.I)
    m = re.search(r'<main[\s\S]*?</main>', t, re.I)
    if not m:
        return ''
    b = m.group(0)
    r = re.search(r'<ol class="ref-list"[^>]*>[\s\S]*?</ol>', b)
    if r:                      # список литературы — там законно много латиницы
        b = b.replace(r.group(0), ' ')
    b = re.sub(r'<nav[\s\S]*?</nav>', ' ', b, flags=re.I)
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]*>', ' ', LOOSE.sub('&lt;', b))))


def main() -> int:
    freq, where = Counter(), {}
    texts = {}
    for fp in pages():
        v = visible(fp)
        texts[fp.stem] = v
        for w in WORD.findall(v):
            lw = w.lower()
            freq[lw] += 1
            where.setdefault(lw, []).append(fp.stem)

    if '--latin' in sys.argv:
        # английские служебные и общеупотребительные слова внутри
        # азербайджанской прозы — однозначная утечка исходника
        EN = set('''the with and for from that this are was were been have has had will
        would should could when where which while after before between during without
        within through however therefore although because their there these those such
        into upon than then them they what does doing done being also more most other
        others some many much than each both under over about against across among
        around behind below beside besides beyond despite except inside outside since
        toward towards until unless whereas whether about above already always another
        anything become becomes becoming cannot certain clearly common commonly compared
        complete consider considered depending especially even every following further
        given greater high higher important including increased instead least less like
        likely long longer lower made make making may might must need needed often only
        overall particularly per possible present provide provided rather related report
        reported require required result results same seen several show shown significant
        similar since specific still study studies such support supported take taken
        term terms therefore thus time times together toward treat treated treatment
        typically use used using usually various very well were what when whether which
        while with within without would year years'''.split())
        bad = [(w, n) for w, n in freq.items() if w in EN]
        bad.sort(key=lambda x: -x[1])
        print(f'английских слов в азербайджанской прозе: {sum(n for _, n in bad)} '
              f'({len(bad)} различных)')
        for w, n in bad:
            page = where[w][0]
            m = re.search(r'.{0,40}' + w + r'.{0,40}', texts[page], re.I)
            print(f'  {w:<16}{n:>3}  {page:<14}…{m.group(0).strip() if m else ""}…')
        return 0

    rare = sorted(w for w, n in freq.items()
                  if n <= MIN and not LATIN_ONLY.match(w) and re.search('[çəğıöşü]', w))
    print(f'словоформ всего: {len(freq)}; встречаются ≤{MIN} раз: {len(rare)}')
    for w in rare:
        page = where[w][0]
        m = re.search(r'.{0,44}\b' + re.escape(w) + r'\b.{0,44}', texts[page], re.I)
        ctx = m.group(0).strip() if m else ''
        print(f'  {w:<26}{freq[w]}  {page:<16}…{ctx}…')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
