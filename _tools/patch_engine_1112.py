# -*- coding: utf-8 -*-
"""Правки движка внутренних страниц по первому кругу критика (12.11.2026). Повторный запуск: «уже применено»."""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def rep(s, a, b):
    assert s.count(a) == 1, a[:70]
    return s.replace(a, b)


p = "assets/js/blocks.js"
s = io.open(p, encoding="utf-8").read()
if "pc2__n--big" in s:
    print("уже применено")
    sys.exit(0)
# 1. карточка может нести свой крупный знак (23+, 100%, IPAS)
s = rep(s, """${b.num ? `<span class="pc2__n">${String(i + 1).padStart(2, '0')}</span>` : ''}""",
        """${x.n ? `<span class="pc2__n pc2__n--big">${esc(x.n)}</span>` : b.num ? `<span class="pc2__n">${String(i + 1).padStart(2, '0')}</span>` : ''}""")
# 2. хвостовые стрелки в подписях кнопок
s = rep(s, "[→›]+", "[→›↗]+")
# 3. под ценами второй кнопки «Записаться» нет: одна в герое, форма внизу
s = rep(s, """<p class="pnote">${esc(P.note)}</p><p class="pp__cta"><a class="btn" href="#reg">${esc(u.book)}</a></p></div>`; }""",
        """<p class="pnote">${esc(P.note)}</p></div>`; }""")
# 4. номер телефона не рвётся по строкам
s = rep(s, """    .replace(/&lt;\\/a&gt;/g, '</a>');""",
        """    .replace(/&lt;\\/a&gt;/g, '</a>')
    .replace(/\\+\\d[\\d ]{8,16}\\d/g, m => `<span class="nw">${m}</span>`);        /* номер телефона не рвётся */""")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

p = "assets/js/page.js"
s = io.open(p, encoding="utf-8").read()
# 5. блог: статья из плашки «самая новая» не повторяется первой в сетке
s = rep(s, "const its = d.items.filter(x => cat === 'all' || x.cat === cat), f = d.featured,",
        "const f = d.featured, its = d.items.filter(x => (cat === 'all' ? !(f && x.slug === f.slug) : x.cat === cat)),")
# 6. таблицы: подпись колонки в каждой ячейке — на телефоне строка читается карточкой
s = rep(s, "    setTimeout(() => page && page.watch(), 0);",
        """    $$('#pgBlocks table').forEach(tb => { const hd = [...tb.querySelectorAll('thead th')].map(x => x.textContent.trim()); tb.classList.toggle('tbl--nohead', !hd.length); tb.querySelectorAll('tbody tr').forEach(tr => [...tr.children].forEach((td, i) => { if (hd[i]) td.dataset.l = hd[i]; })); });
    setTimeout(() => page && page.watch(), 0);""")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("применено")
