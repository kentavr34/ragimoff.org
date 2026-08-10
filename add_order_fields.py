#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
add_order_fields.py — язык и классификация в форме заказа книги.

Форма собирала только имя и телефон, поэтому по заявке нельзя было понять,
какое издание человек ждёт. Книга выходит на четырёх языках и строится
вокруг трёх классификаций — без этих двух полей заказ приходится
переспрашивать.

Добавляются два выпадающих списка:
  * язык издания — Azərbaycan / Русский / English / Türkçe;
  * основное оглавление — XBT-11 (ICD-11) или DSM-5-TR.

Оба уходят в ту же заявку, что и раньше: поля `lang` и `classification`
в payload и человекочитаемая строка в `service`, чтобы заказ был понятен
прямо в уведомлении, без заглядывания в таблицу.

    python add_order_fields.py            # отчёт
    python add_order_fields.py --apply
"""
from __future__ import annotations
import re, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
BOOK = ROOT / 'klinik-psixiatriya'
APPLY = '--apply' in sys.argv

# подписи по языку издания
L = {
    'az': ('Kitabın dili', 'Əsas təsnifat'),
    'ru': ('Язык издания', 'Основная классификация'),
    'en': ('Language of the edition', 'Primary classification'),
    'tr': ('Kitabın dili', 'Temel sınıflandırma'),
}
LANGS = [('az', 'Azərbaycan'), ('ru', 'Русский'), ('en', 'English'), ('tr', 'Türkçe')]
CLS = [('XBT-11', 'XBT-11 (ICD-11)'), ('DSM-5-TR', 'DSM-5-TR')]

SUBMIT = re.compile(r'(\s*)<button type="submit" class="kitab-submit">')


def fields(lg: str) -> str:
    lang_lbl, cls_lbl = L[lg]
    # lang на каждом варианте: название языка пишется на своём языке
    opts_l = ''.join(f'<option value="{c}" lang="{c}"{" selected" if c == lg else ""}>{n}</option>'
                     for c, n in LANGS)
    opts_c = ''.join(f'<option value="{v}">{n}</option>' for v, n in CLS)
    return (
        f'\n        <div class="kitab-field">\n'
        f'          <label for="kitab-lang">{lang_lbl}</label>\n'
        f'          <select id="kitab-lang" name="lang">{opts_l}</select>\n'
        f'        </div>\n'
        f'        <div class="kitab-field">\n'
        f'          <label for="kitab-cls">{cls_lbl}</label>\n'
        f'          <select id="kitab-cls" name="classification">{opts_c}</select>\n'
        f'        </div>\n'
    )


def main() -> int:
    total = 0
    for lg, folder in (('az', BOOK), ('ru', BOOK / 'ru'),
                       ('en', BOOK / 'en'), ('tr', BOOK / 'tr')):
        block = fields(lg)
        n = 0
        for fp in sorted(folder.glob('*.html')):
            raw = fp.read_bytes().decode('utf-8')
            crlf = raw.count('\r\n') > raw.count('\n') // 2
            t = raw.replace('\r\n', '\n')
            if 'kitab-form' not in t or 'id="kitab-lang"' in t:
                continue
            new = SUBMIT.sub(block + r'\1<button type="submit" class="kitab-submit">', t, count=1)
            # поля уходят в заявку
            new = new.replace(
                "var phone = (document.getElementById('kitab-phone').value || '').trim();",
                "var phone = (document.getElementById('kitab-phone').value || '').trim();\n"
                "        var langEl = document.getElementById('kitab-lang');\n"
                "        var clsEl  = document.getElementById('kitab-cls');\n"
                "        var lang = langEl ? langEl.value : '';\n"
                "        var langName = langEl ? langEl.options[langEl.selectedIndex].text : '';\n"
                "        var cls  = clsEl ? clsEl.value : '';")
            new = new.replace(
                "service: 'Kitab sifarişi',",
                "service: 'Kitab sifarişi — ' + langName + ' / ' + cls,\n"
                "          lang: lang,\n"
                "          classification: cls,")
            if new == t:
                continue
            n += 1
            if APPLY:
                fp.write_bytes((new.replace('\n', '\r\n') if crlf else new).encode('utf-8'))
        total += n
        print(f'  {lg}: страниц {n}')
    print(f'итого {total}')
    print('применено' if APPLY else 'пробный прогон — запустить с --apply')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
