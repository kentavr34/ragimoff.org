# -*- coding: utf-8 -*-
"""fix_sub_br.py — убирает жёсткие переносы внутри подзаголовков разделов.

Внутри `<p class="sec-sub">` стоял `<br>` как способ разбить текст на строки.
Это вредно дважды:

  * переносы решает подгонка (js-hero-fit2.js) — она считает ширину под
    заголовок и под экран, а жёсткий `<br>` ей мешает;
  * почти везде вокруг `<br>` не было пробела, и при снятии тега слова
    слипались прямо на экране: «komandamız24 saat», «çərçivəsindədir.22 fənn»,
    «более 2 недель —необходима», «learned state.Every».

Тег заменяется пробелом, двойные пробелы схлопываются. Разбивать подзаголовок
на строки следует парами `*-lead-mob` / `*-lead-desk`, а не `<br>`.

Идемпотентен: повторный запуск ничего не меняет.

    python fix_sub_br.py           # применить
    python fix_sub_br.py --check   # показать, что изменится
"""
import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).parent
SKIP_DIRS = {'klinik-psixiatriya', '_supplements', '_partials', 'graphify-out', 'node_modules'}
# Тег ищется С АТРИБУТАМИ: у части абзацев есть inline style, и правило
# «ровно <p class="sec-sub">» их не видело — именно там и сидели склейки
# «komandamız24 saat».
SUB = re.compile(r'(<p[^>]*class="[^"]*sec-sub[^"]*"[^>]*>)(.*?)(</p>)', re.S)
BR = re.compile(r'\s*<br\s*/?>\s*', re.I)

# Слипшиеся слова. Часть склеек была не от <br>, а прямо в тексте — там, где
# перенос когда-то сняли вручную и пробел не поставили. Регуляркой ловится
# только пунктуация; пары слов приходится перечислять.
LOWER = 'a-zа-яёəıöüçşğ'
UPPER = 'A-ZА-ЯЁƏİÖÜÇŞĞ'
# Только точка и запятая. Точка с запятой сюда попасть не должна: она есть в
# каждой HTML-сущности, и правило «поставить пробел после знака» превращало
# «və&nbsp;valideyn» в «və&nbsp; valideyn» — то есть портило разметку.
PUNCT_GLUE = re.compile(r'([.,])(?=[%s%s])' % (UPPER, LOWER))
DIGIT_GLUE = re.compile(r'([%s])(?=\d)' % LOWER)
# Сущности и теги прячем на время правки — внутри них пробелы ставить нельзя.
MASKABLE = re.compile(r'&[a-zA-Z]+;|&#\d+;|<[^>]+>')

WORD_GLUE = {
    # азербайджанские
    'ərzindəsizinlə': 'ərzində sizinlə',
    'şəxsbu': 'şəxs bu',
    'mütəxəssislərbu': 'mütəxəssislər bu',
    'tələbələryalnız': 'tələbələr yalnız',
    # русские
    'специалистовэта': 'специалистов эта',
    # английские
    'specialiststhis': 'specialists this',
}


def norm(s):
    """Текст без учёта пробелов и переносов — для сравнения «изменилось ли по сути»."""
    return re.sub(r'\s+', ' ', s).strip()


def unglue(s):
    for bad, good in WORD_GLUE.items():
        s = s.replace(bad, good)
    # Прячем теги и сущности, иначе правила лезут внутрь разметки.
    stash = []

    def hide(m):
        stash.append(m.group(0))
        return '\x00%d\x00' % (len(stash) - 1)

    s = MASKABLE.sub(hide, s)
    # «komandamız24 saat» — буква вплотную к цифре
    s = DIGIT_GLUE.sub(r'\1 ', s)
    # «çərçivəsindədir.22», «əsaslar,klinik» — знак препинания без пробела
    s = PUNCT_GLUE.sub(r'\1 ', s)
    s = re.sub(r'\x00(\d+)\x00', lambda m: stash[int(m.group(1))], s)
    return s


check = '--check' in sys.argv
changed, places = [], 0

for path in sorted(ROOT.rglob('*.html')):
    rel = path.relative_to(ROOT)
    if any(part in SKIP_DIRS for part in rel.parts):
        continue
    raw = path.read_bytes()
    crlf = raw.count(b'\r\n') > raw.count(b'\n') // 2
    text = raw.decode('utf-8').replace('\r\n', '\n')

    hits = [0]

    def repl(m):
        body = m.group(2)
        fixed = BR.sub(' ', body) if BR.search(body) else body
        fixed = unglue(fixed)
        fixed = re.sub(r'  +', ' ', fixed).strip()
        # Правим только там, где меняется САМ ТЕКСТ. Иначе скрипт переписывал бы
        # файлы ради схлопывания отступов — в том числе index.html, который по
        # правилам проекта не трогают без разрешения владельца.
        if norm(fixed) == norm(body):
            return m.group(0)
        hits[0] += 1
        return m.group(1) + fixed + m.group(3)

    new_text = SUB.sub(repl, text)
    if hits[0]:
        places += hits[0]
        changed.append('%s (%d)' % (rel, hits[0]))
        if not check:
            path.write_bytes((new_text.replace('\n', '\r\n') if crlf else new_text).encode('utf-8'))

print('Жёсткие переносы в подзаголовках')
print('  файлов: %d, мест: %d' % (len(changed), places))
if check:
    print('  --check: файлы НЕ изменены')
for c in changed[:40]:
    print('   ', c)
if len(changed) > 40:
    print('    … и ещё %d' % (len(changed) - 40))
