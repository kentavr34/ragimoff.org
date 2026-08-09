# -*- coding: utf-8 -*-
"""
fix_quotes.py — кавычки и то, что прилипло к ним при переводе.

Три дефекта, найденные сплошным чтением §10 «Мифы»:

1. Пропал пробел после закрывающей кавычки:
   «Hamiləlikdə „stress“və ya „pis düşüncələr“İD-yə səbəb olur»,
   “…compulsory in DSM-IV”Brief Reactive Psychosis.

2. Вложенные кавычки того же рисунка: «Tip II bipolyar «yüngül forma»dır».
   Второй уровень в азербайджанском и русском — немецкие лапки „…“.

3. Пробел между кавычкой и падежным аффиксом: «magik təfəkkür» ünü.

Осторожность здесь важнее полноты. В азербайджанском и турецком падежный
аффикс пишется вплотную к закрывающей кавычке («İkili depresiya»da), и
строчная буква сразу после кавычки означает либо аффикс, либо потерянный
пробел перед следующим словом. Различает их закрытый список аффиксов:
всё, что в него не входит, — слово, и перед ним ставится пробел.
В русском и английском строчная после закрывающей кавычки — всегда
следующее слово. По той же причине «„» и «“» разбираются по языку:
в азербайджанском и русском „…“ закрывается знаком “, в английском
и турецком тот же знак — открывающий.

    python fix_quotes.py            # отчёт
    python fix_quotes.py --apply
"""
from __future__ import annotations
import re, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
BOOK = ROOT / 'klinik-psixiatriya'
TREES = {
    'az': [BOOK, BOOK / 'preview', ROOT / '_supplements' / 'chapters-v2'],
    'ru': [BOOK / 'ru'],
    'en': [BOOK / 'en'],
    'tr': [BOOK / 'tr'],
}
APPLY = '--apply' in sys.argv

# закрывающая кавычка по языку; в az/ru „…“ — второй уровень, в en/tr “ открывает
CLOSERS = {'az': '»“', 'ru': '»“', 'en': '”', 'tr': '”'}
UPPER = r'[A-ZÀ-ÖØ-ÞĞİÖŞÜÇƏА-ЯЁ0-9«„]'
# аффиксы тюркской словоизменительной парадигмы, какие в книге пристают
# к закрытой кавычке: принадлежность, падеж, число, сказуемость
SUFFIX = (r'(?:n?[ıiuü]n|n?[ıiuü]|[yn]?[aeə]|d[aeə]|nd[aeə]|d[aeə]n|nd[aeə]n|'
          r'[dt][ıiuü]r|[dt][ıiuü]rl[aeə]r|l[aeə]r|l[aeə]r[ıi]|l[aeə]rd[aeə]|'
          r's[ıiuü]|[yi]l[aeə]|d[aeə]k[ıi]|ç[ıi]|l[ıi]|s[aeə])')
TAIL = re.compile(f'[a-zçəğıöşü]')


FOREIGN = {                       # чужой рисунок кавычек внутри языка
    'az': (re.compile(r'“([^“”]*)”'), r'„\1“'),
    'ru': (re.compile(r'“([^“”]*)”'), r'„\1“'),
    'en': (re.compile(r'«([^«»]*)»'), r'“\1”'),
    'tr': (re.compile(r'«([^«»]*)»'), r'“\1”'),
}
# машинописный апостроф вместо кавычек: 'sadece psikolojik bir çöküş'.
# В турецком тот же знак законно отделяет аффикс от имени собственного
# (Wakefield'ın, ICD-11'de), поэтому пара опознаётся по окружению:
# открывающий стоит после пробела или скобки, закрывающий — перед
# пробелом или знаком препинания.
STRAIGHT = re.compile(r"(?<=[\s“«(—])'([^'’<>\n]{2,80}?)'(?=[\s.,;:!?)»”—]|$)")
PRIMARY = {'az': '«»', 'ru': '«»', 'en': '“”', 'tr': '“”'}
SCRIPT = re.compile(r'<(script|style)\b[\s\S]*?</\1>', re.I)


def nest(text: str, outer: str, close_outer: str, inner: str, close_inner: str) -> tuple[str, int]:
    """Второй уровень кавычек внутри первого — лапками, а не ёлочками."""
    out, depth, n = [], 0, 0
    for ch in text:
        if ch == outer:
            depth += 1
            if depth > 1:
                out.append(inner); n += 1; continue
        elif ch == close_outer:
            if depth > 1:
                out.append(close_inner); n += 1; depth -= 1; continue
            depth = max(0, depth - 1)
        out.append(ch)
    return ''.join(out), n


def main() -> int:
    stat = {lg: [0, 0] for lg in TREES}      # [пробелов, вложенных]
    seen = set()
    for lg, trees in TREES.items():
        closers = CLOSERS[lg]
        if lg in ('az', 'tr'):
            # заглавная, цифра, открывающая кавычка — точно новое слово;
            # строчная — новое слово, только если это не аффикс
            space = re.compile(f'([{closers}])(?={UPPER}|(?!{SUFFIX}(?![a-zçəğıöşü]))[a-zçəğıöşü])')
        else:
            space = re.compile(f'([{closers}])(?={UPPER}|[a-zа-яё])')
        for tree in trees:
            if not tree.is_dir():
                continue
            for fp in sorted(tree.glob('*.html')):
                if fp in seen:
                    continue
                seen.add(fp)
                raw = fp.read_bytes().decode('utf-8')
                crlf = raw.count('\r\n') > raw.count('\n') // 2
                t = raw.replace('\r\n', '\n')
                m = re.search(r'<main[\s\S]*?</main>', t, re.I)
                if not m:
                    continue
                body, pos, out, a, b = m.group(0), 0, [], 0, 0
                foreign, repl = FOREIGN[lg]
                op, cl = PRIMARY[lg]
                skip = [(s.start(), s.end()) for s in SCRIPT.finditer(body)]
                spans = list(re.finditer(r'<[^>]*>', body)) + [None]
                for tag in spans:
                    start = pos
                    chunk = body[pos:tag.start()] if tag else body[pos:]
                    if not any(s <= start < e for s, e in skip):
                        chunk, k = STRAIGHT.subn(f'{op}\\1{cl}', chunk)
                        b += k
                    chunk, k = foreign.subn(repl, chunk)
                    b += k
                    if lg in ('az', 'ru'):
                        chunk, k = nest(chunk, '«', '»', '„', '“')
                    else:
                        chunk, k = nest(chunk, '“', '”', '‘', '’')
                    b += k
                    chunk, k = space.subn(r'\1 ', chunk)
                    a += k
                    out.append(chunk)
                    if tag:
                        out.append(tag.group(0)); pos = tag.end()
                if not (a or b):
                    continue
                stat[lg][0] += a; stat[lg][1] += b
                if APPLY:
                    t = t[:m.start()] + ''.join(out) + t[m.end():]
                    fp.write_bytes((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))
    print('пробел после закрывающей кавычки / второй уровень лапками:')
    for lg, (a, b) in stat.items():
        print(f'  {lg}: пробелов {a}, вложенных пар {b}')
    print('применено' if APPLY else 'пробный прогон — запустить с --apply')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
