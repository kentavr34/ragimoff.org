"""Правки вёрстки по третьему кругу критиков. Запуск из test/11."""
import io


def edit(path, pairs):
    t = io.open(path, encoding='utf-8').read()
    for a, b in pairs:
        if a not in t:
            raise SystemExit('НЕ НАЙДЕНО в %s: %s' % (path, a[:90]))
        t = t.replace(a, b, 1)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(t)


edit('assets/js/site.js', [
    ("{ k: 'corp', href: '#corp', sub: [] }", "{ k: 'corp', href: '#corp', sub: t.corp.t.map(x => [L.corp, x]) }"),
    ("insertAdjacentHTML('beforeend', `<a class=\"btn mob__cta\"", "insertAdjacentHTML('afterbegin', `<a class=\"btn mob__cta\""),
    ("<p class=\"film__d\">${esc(fm.d)}</p></div>` : '';",
     "<p class=\"film__d\">${esc(fm.d)}</p>${fm.cta ? `<button type=\"button\" class=\"btn btn--line film__go\">${esc(fm.cta)}</button>` : ''}</div>` : '';\n"
     "  const ax = t.a11y; if (ax) { document.title = ax.title; $('#nav').setAttribute('aria-label', ax.menu); $('#burger').setAttribute('aria-label', ax.menu); $('#themes').setAttribute('aria-label', ax.theme); $('#langs').setAttribute('aria-label', ax.lang); $$('[data-theme-btn]').forEach(b => b.setAttribute('aria-label', ax[b.dataset.themeBtn])); }"),
    ("  const yt = e.target.closest('.vid[data-yt]');",
     "  const go = e.target.closest('.film__go'); const yt = go ? $('#film .vid[data-yt]') : e.target.closest('.vid[data-yt]'); if (go && !yt) return;"),
])

CSS = """
/* ═══ КРУГ 03 ═══ */
/* N3 / 3.3: подпись героя помещается на телефоне во всех языках */
.cine__school { letter-spacing: .26em; max-width: 100%; }
@media (max-width: 760px) { .cine__school { font-size: clamp(13px, 4.1vw, 18px); letter-spacing: .16em; } }
/* 10.15 / 10.16: панель программ во весь экран, содержимое по центру, без швов и боковых полос */
.rib__stick { min-height: 100vh; min-height: 100svh; justify-content: center; padding: var(--hs) 0; background: transparent; }
.rib__stick::before, .rib__stick::after { display: none; }
/* 5.5: в тёмной теме книга стоит на тёплом свету */
[data-theme="night"] .bk__scene::after { background: radial-gradient(closest-side, color-mix(in srgb, var(--gold) 46%, transparent), transparent); filter: blur(12px); height: 34px; opacity: 1; }
/* 10.23: все фото и кадры в одной тональности; цвет — по наведению */
.vid img, .proof:nth-child(3) .proof__i img { filter: grayscale(1) sepia(.2) contrast(1.05) brightness(.9); } .vid:hover img, .proof:nth-child(3):hover .proof__i img { filter: grayscale(.2) sepia(.06); }
/* 10.4 / 10.30 / 9.9 */
.pc__m span { font-size: 14px; } .myth__btn { min-height: var(--tap); } .foot__col li { text-wrap: balance; }
.film__go { margin-top: var(--r2); }
@media (max-width: 760px) { .seg--lang button { min-width: 34px; } }
@media (max-width: 359px) { .seg--lang button { min-width: 30px; } }
"""
css = io.open('assets/css/site.css', encoding='utf-8').read()
if 'КРУГ 03' not in css:
    io.open('assets/css/site.css', 'w', encoding='utf-8', newline='\n').write(css + CSS)

p = '_tools/round.py'
t = io.open(p, encoding='utf-8').read()
a = "  // N6 / 10.18 заголовки"
if a not in t:
    raise SystemExit('round.py: якорь не найден')
if 'шире экрана' not in t:
    t = t.replace(a, """  // N3: подпись героя и кнопки героя — по ширине текста, даже пока скрыты
  document.querySelectorAll('.cine__school, .sign, .cine__btns').forEach(e => { const r = document.createRange(); r.selectNodeContents(e); const b = r.getBoundingClientRect(); if (b.width > W - 16) bad.push(['N3', 'шире экрана: ' + e.className + ' ' + Math.round(b.width) + ' при окне ' + W]); });
  // 10.29: один вес и шрифт у всех кнопок
  const bw = new Set(); document.querySelectorAll('.btn, .head__cta, .cine__btns a').forEach(e => { const s = getComputedStyle(e); bw.add(s.fontFamily.split(',')[0] + ' ' + s.fontWeight + ' ' + s.fontSize); }); if (bw.size > 1) bad.push(['10.29', 'кнопки разные: ' + [...bw].join(' | ')]);
""" + a)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('patched')
