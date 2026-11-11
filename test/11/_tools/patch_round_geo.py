"""Замер: шесть ширин телефона и проверка геометрии (G1 — поля шапки, G2 — блоки в полях страницы). Запуск из test/11."""
import io

p = '_tools/round.py'
t = io.open(p, encoding='utf-8').read()
if 'EXTRA_W' in t:
    raise SystemExit('уже применено')


def rep(a, b):
    global t
    if a not in t:
        raise SystemExit('round.py: не найдено ' + a[:60])
    t = t.replace(a, b, 1)


rep("SHOTS = [", "EXTRA_W = [(430, 932), (412, 915), (375, 812), (360, 780)]          # ещё четыре ширины телефона: только геометрия, одна тема\nSHOTS = [")
rep("        for (W, H) in WIDTHS:", "        for (W, H) in WIDTHS + EXTRA_W:")
rep("                for th in THEMES:\n", "                for th in THEMES:\n                    if (W, H) in EXTRA_W and th != 'night':\n                        continue\n")
rep("  // N2 имя в одну строку", """  // G1: шапка — поле слева равно полю справа; элементы шапки не налезают друг на друга
  (() => { const hd = document.querySelector('.head'); if (!hd) return; const kids = [document.querySelector('.logo'), ...document.querySelectorAll('.head__r > *')].filter(e => e && vis(e)).map(e => e.getBoundingClientRect());
    if (!kids.length) return; const L = Math.round(Math.min(...kids.map(r => r.left))), Rr = Math.round(W - Math.max(...kids.map(r => r.right)));
    if (Math.abs(L - Rr) > 1) bad.push(['G1', 'шапка: поле слева ' + L + ' px, справа ' + Rr + ' px']);
    kids.sort((a, b) => a.left - b.left); for (let i = 1; i < kids.length; i++) if (kids[i].left - kids[i - 1].right < 3) bad.push(['G1', 'шапка: элементы ближе 4 px (' + Math.round(kids[i].left - kids[i - 1].right) + ')']); })();
  // G2: каждый блок внутри .wrap стоит в полях страницы (кроме лент, которые листаются)
  (() => { const w0 = document.querySelector('.sec .wrap'); if (!w0) return; const pl = parseFloat(getComputedStyle(w0).paddingLeft);
    document.querySelectorAll('.wrap > *, .wrap > * > *').forEach(e => { if (!vis(e) || e.closest('[data-rib-track], .shelf, .belt, .lb, .cine') || e.matches('[data-rib-track], .shelf')) return; const r = e.getBoundingClientRect(); if (r.width < 8) return;
      if (r.left < pl - 1.5 || r.right > W - pl + 1.5) bad.push(['G2', 'вне полей: ' + (e.className || e.tagName) + ' ' + Math.round(r.left) + '…' + Math.round(W - r.right) + ' при поле ' + Math.round(pl)]); }); })();
  // N2 имя в одну строку""")
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('patched')
