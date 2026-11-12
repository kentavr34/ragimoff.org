"""Шапка на телефоне: равные поля слева и справа на всех ширинах; замер — шесть ширин телефона и проверка геометрии. Запуск из test/11."""
import io

CSS = """
/* ═══ шапка на телефоне: поле слева = полю справа на любой ширине; логотип плотнее, элементы справа сдвинуты влево (владелец, 11.11) ═══ */
@media (max-width: 760px) {
  .head { justify-content: space-between; gap: var(--s2); padding-left: var(--pad); padding-right: var(--pad); }
  .logo { flex: 0 1 auto; min-width: 0; gap: 4px; } .logo__r { font-size: 25px; padding-right: 6px; } .logo__w { font-size: 11.5px; letter-spacing: .2em; }
  .head__r { flex: 0 0 auto; gap: var(--s1); margin-left: 0; }
  #themes { padding: 0; border: 0; background: none; } #themes button { min-width: var(--tap); height: var(--tap); border: 1px solid var(--line); background: color-mix(in srgb, var(--bg) 55%, transparent); }
  .seg--lang { padding: 2px; } .seg--lang button { min-width: 34px; height: 40px; padding: 0; }
  .burger { width: var(--tap); height: var(--tap); flex: 0 0 var(--tap); }
}
@media (max-width: 349px) { .logo__w { display: none; } }
"""
p = 'assets/css/site.css'
c = io.open(p, encoding='utf-8').read()
if 'поле слева = полю справа' not in c:
    io.open(p, 'w', encoding='utf-8', newline='\n').write(c + CSS)

p = '_tools/round.py'
t = io.open(p, encoding='utf-8').read()
if 'EXTRA_W' not in t:
    a = "WIDTHS = [(1440, 900), (1366, 768), (390, 844), (320, 640)]"
    if a not in t:
        raise SystemExit('round.py: WIDTHS не найден')
    t = t.replace(a, a + "\nEXTRA_W = [(430, 932), (412, 915), (375, 812), (360, 780)]          # ещё четыре ширины телефона: только геометрия, одна тема")
    a = "        for (W, H) in WIDTHS:"
    t = t.replace(a, "        for (W, H) in WIDTHS + EXTRA_W:")
    a = "                for th in THEMES:\n"
    t = t.replace(a, a + "                    if (W, H) in EXTRA_W and th != 'night':\n                        continue\n")
    a = "  // N2 имя в одну строку"
    if a not in t:
        raise SystemExit('round.py: якорь N2 не найден')
    t = t.replace(a, """  // G1: шапка — поле слева равно полю справа; элементы шапки не налезают друг на друга
  (() => { const hd = document.querySelector('.head'); if (!hd) return; const kids = [document.querySelector('.logo'), ...document.querySelectorAll('.head__r > *')].filter(e => e && vis(e)).map(e => e.getBoundingClientRect());
    if (!kids.length) return; const L = Math.round(Math.min(...kids.map(r => r.left))), Rr = Math.round(W - Math.max(...kids.map(r => r.right)));
    if (Math.abs(L - Rr) > 1) bad.push(['G1', 'шапка: поле слева ' + L + ' px, справа ' + Rr + ' px']);
    kids.sort((a, b) => a.left - b.left); for (let i = 1; i < kids.length; i++) if (kids[i].left - kids[i - 1].right < 3) bad.push(['G1', 'шапка: элементы ближе 4 px (' + Math.round(kids[i].left - kids[i - 1].right) + ')']); })();
  // G2: каждый блок внутри .wrap стоит в полях страницы (кроме лент, которые листаются)
  (() => { const w0 = document.querySelector('.sec .wrap'); if (!w0) return; const cs = getComputedStyle(w0), pl = parseFloat(cs.paddingLeft);
    document.querySelectorAll('.wrap > *, .wrap > * > *').forEach(e => { if (!vis(e) || e.closest('[data-rib-track], .shelf, .belt, .lb, .cine') || e.matches('[data-rib-track], .shelf')) return; const r = e.getBoundingClientRect(); if (r.width < 8) return;
      if (r.left < pl - 1.5 || r.right > W - pl + 1.5) bad.push(['G2', 'вне полей: ' + (e.className || e.tagName) + ' ' + Math.round(r.left) + '…' + Math.round(W - r.right) + ' при поле ' + Math.round(pl)]); }); })();
""" + a)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('patched')
