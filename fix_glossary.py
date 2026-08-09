# -*- coding: utf-8 -*-
"""
fix_glossary.py — таблица терминологического канона в переводах.

Страницы `abbreviatur.html` и `terminoloji-luget.html` содержат таблицу
«имена и термины, используемые на сайте». Первые её строки — названия
расстройств, и они законно переведены: читатель русского издания правит
русскую форму. Но строки 14–31 — это решения о словоупотреблении
АЗЕРБАЙДЖАНСКОГО текста, и их левый столбец перевели тоже. Результат:

    en: pasiyent  | patient (not 'patient')      — «пациент (не пациент)»
    ru: təqib     | Преследование ... follow-up  — «преследование» вместо наблюдения
    tr: Mədəniyyət и kultura — оба стали «kültür», то есть различие,
        ради которого строки и написаны, стёрто

Атрибут `data-az` у кнопки правки всегда хранил азербайджанский термин —
именно он ключ для виджета `duzelis.js`. Значит, видимая ячейка разошлась
с ключом, по которому правка сохраняется.

Инструмент возвращает в строки 14–31 азербайджанский термин и пишет
пояснение на языке читателя.

    python fix_glossary.py           # отчёт
    python fix_glossary.py --apply
"""
from __future__ import annotations
import re, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
BOOK = ROOT / 'klinik-psixiatriya'
PAGES = ('abbreviatur.html', 'terminoloji-luget.html')
APPLY = '--apply' in sys.argv

# азербайджанский термин → пояснение на языке издания
TERMS = [
    ('Klinik təzahürlər',
     'клинические проявления',
     'clinical manifestations',
     'klinik belirtiler'),
    ('Vahid diaqnostik meyarlar',
     'единые диагностические критерии',
     'unified diagnostic criteria',
     'birleşik tanı ölçütleri'),
    ('İnstrumental müayinələr',
     'инструментальные обследования',
     'instrumental examinations',
     'enstrümantal incelemeler'),
    ('pasiyent',
     'пациент — в книге принято «pasiyent», не «xəstə»',
     'patient — the book uses ‘pasiyent’, not ‘xəstə’',
     'hasta — kitapta “pasiyent” kullanılır, “xəstə” değil'),
    ('psixi pozuntu',
     'психическое расстройство — не «ruhi»',
     'psychiatric disorder — not ‘ruhi’',
     'ruhsal bozukluk — “ruhi” değil'),
    ('metodları',
     'методы — не «üsulları»',
     'methods — not ‘üsulları’',
     'yöntemleri — “üsulları” değil'),
    ('Mədəniyyət',
     'культура в значении культурного контекста — не «kültür»',
     'culture in the anthropological sense — not ‘kültür’',
     'kültür — kültürel bağlam anlamında; laboratuvar kültürü için “kultura” kullanılır'),
    ('kultura',
     'культура лабораторная, посев — не «kültür»',
     'laboratory culture — not ‘kültür’',
     'laboratuvar kültürü (üreme) — “Mədəniyyət” ile karıştırılmamalı'),
    ('ilkin göstəricilər',
     'исходные показатели',
     'baseline indicators',
     'başlangıç göstergeleri'),
    ('obur yemə',
     'компульсивное переедание',
     'binge eating',
     'tıkınırcasına yeme'),
    ('skrininq',
     'скрининг',
     'screening',
     'tarama'),
    ('təqib',
     'динамическое наблюдение после лечения',
     'follow-up',
     'izlem'),
    ('uyğunluq',
     'приверженность лечению',
     'adherence, compliance',
     'tedaviye uyum'),
    ('təcrid',
     'отстранённость',
     'detachment',
     'kopukluk'),
    ('Dezinhibisiya',
     'расторможенность как черта личности',
     'disinhibition as a personality trait',
     'dizinhibisyon (kişilik özelliği)'),
    ('inadkar',
     'вызывающий, непокорный',
     'defiant',
     'karşı gelen'),
    ('məhdudlaşdırılmamış',
     'расторможенный (прилагательное)',
     'disinhibited (adjective)',
     'dizinhibe (sıfat)'),
    ('meyarlar',
     'критерии — не «чек-лист»',
     'criteria — not ‘checklist’',
     'ölçütler — “çek-list” değil'),
]
FIRST = 15                      # 0 — строка заголовка, термины начинаются с 15-й
LANGS = {'ru': 1, 'en': 2, 'tr': 3}
ROW = re.compile(r'<tr><td><strong>([^<]*)</strong></td><td>([^<]*)</td>')


def main() -> int:
    changed = 0
    for page in PAGES:
        for lg, col in LANGS.items():
            fp = BOOK / lg / page
            if not fp.exists():
                continue
            raw = fp.read_bytes().decode('utf-8')
            crlf = raw.count('\r\n') > raw.count('\n') // 2
            t = raw.replace('\r\n', '\n')
            tables = [m for m in re.finditer(r'<table[\s\S]*?</table>', t)
                      if len(re.findall(r'<tr>', m.group(0))) == len(TERMS) + FIRST]
            if not tables:
                print(f'  {lg}/{page}: таблица не найдена')
                continue
            tb = tables[0]
            body = tb.group(0)
            rows = re.findall(r'<tr>[\s\S]*?</tr>', body)
            out, n = [], 0
            for i, tr in enumerate(rows):
                if i >= FIRST and i - FIRST < len(TERMS):
                    az, *gloss = TERMS[i - FIRST]
                    new = ROW.sub(
                        lambda m: f'<tr><td><strong>{az}</strong></td><td>{gloss[col - 1]}</td>',
                        tr, count=1)
                    # ключ виджета — азербайджанский термин; он же в подписи
                    new = re.sub(r'data-az="[^"]*"', f'data-az="{az}"', new)
                    if new != tr:
                        n += 1
                    tr = new
                out.append(tr)
            if not n:
                continue
            changed += 1
            print(f'  {lg}/{page}: строк выправлено {n}')
            if APPLY:
                head = body[:body.index(rows[0])]
                tail = body[body.rindex(rows[-1]) + len(rows[-1]):]
                t = t[:tb.start()] + head + ''.join(out) + tail + t[tb.end():]
                fp.write_bytes((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))
    print('применено' if APPLY else 'пробный прогон — запустить с --apply')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
