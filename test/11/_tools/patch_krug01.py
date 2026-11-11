"""Правки вёрстки по первому кругу критиков (разметка, скрипт, стили). Запуск из test/11. Тексты правит content.js отдельно."""
import io, shutil, pathlib

pathlib.Path('_agent/backup').mkdir(parents=True, exist_ok=True)
for f in ('index.html', 'assets/js/site.js', 'assets/css/site.css'):
    shutil.copy(f, '_agent/backup/' + pathlib.Path(f).name + '.bak-krug01')


def edit(path, pairs):
    t = io.open(path, encoding='utf-8').read()
    for a, b in pairs:
        if a not in t:
            raise SystemExit('НЕ НАЙДЕНО в %s: %s' % (path, a[:100]))
        t = t.replace(a, b, 1)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(t)


edit('index.html', [
    ('<div class="people" id="people"></div></div></section>',
     '<div class="people" id="people"></div><p class="mentors rv" data-i="spec.mentors"></p></div></section>'),
    ('<div class="shelf" id="shelf"></div><p class="shelf__next rv" data-i="books.next"></p>',
     '<div class="shelf" id="shelf"></div><div class="shelf__nav"><button type="button" class="arw" id="bkPrev" aria-label="←"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></button><span class="shelf__pos" id="bkPos"></span><button type="button" class="arw" id="bkNext" aria-label="→"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></button></div><div class="shelf__more"><p class="shelf__next rv" data-i="books.next"></p><p class="shelf__lib rv" data-i="books.lib"></p></div>'),
    ('<ul class="topics" id="topics"></ul><div class="cons__cta rv">',
     '<ul class="topics" id="topics"></ul><p class="cons__who rv" data-i="cons.who"></p><div class="cons__cta rv">'),
    ('<div class="nums" id="nums"></div><div class="corp__row rv">',
     '<p class="corp__lead rv" data-i="corp.lead"></p><ul class="clients rv" id="corpClients"></ul><div class="nums" id="nums"></div><div class="corp__row rv">'),
    ('<span class="foot__sign">Doctor Ragimoff</span><p class="foot__addr" data-i="foot.addr"></p><p class="foot__note" data-i="foot.note"></p>',
     '<span class="foot__sign">Doctor Ragimoff</span><div class="foot__cols" id="footCols"></div><p class="foot__copy" id="footCopy"></p>'),
])

edit('assets/js/site.js', [
    # порядок обложек = порядок книг канона: клиническая психиатрия, Фрейд, Феникс, Вирус вины, Пандемия
    ("const cov = ['klinik', 'phoenix', 'guilt', 'pandemic', 'freud'];", "const cov = ['klinik', 'freud', 'phoenix', 'guilt', 'pandemic'];"),
    ("  $('#corpTags').innerHTML = t.corp.t.map(x => `<li>${esc(x)}</li>`).join('');",
     "  $('#corpTags').innerHTML = t.corp.t.map(x => `<li>${esc(x)}</li>`).join('');\n"
     "  $('#corpClients').innerHTML = (t.corp.clients || []).map(x => `<li>${esc(x)}</li>`).join('');\n"
     "  const fc = t.foot.cols || [], fl = L.foot || [];\n"
     "  $('#footCols').innerHTML = fc.map((c, i) => `<div class=\"foot__col\"><h3>${esc(c.h)}</h3><ul>${c.l.map((x, j) => { const u = (fl[i] || [])[j]; return `<li>${u ? `<a href=\"${u}\"${/^https?:/.test(u) ? ' target=\"_blank\" rel=\"noopener\"' : ''}>${esc(x)}</a>` : esc(x)}</li>`; }).join('')}</ul></div>`).join('');\n"
     "  $('#footCopy').innerHTML = (t.foot.copy || []).map(x => `<span>${esc(x)}</span>`).join('');\n"
     "  bkPos();"),
    ("  const menuOpen = $('#mob').classList.contains('is-open');",
     "  const menuOpen = $('#mob').classList.contains('is-open'); head.classList.toggle('is-menu', menuOpen);"),
    ("document.documentElement.style.overflow = open ? 'hidden' : ''; if (open) head.classList.remove('is-hidden'); }",
     "document.documentElement.style.overflow = open ? 'hidden' : ''; if (open) head.classList.remove('is-hidden'); head.classList.toggle('is-menu', open); }\n"
     "/* книги: лента по одной, стрелки и свайп */\n"
     "const shelf = $('#shelf');\n"
     "function bkIdx() { return Math.round(shelf.scrollLeft / Math.max(1, shelf.clientWidth)); }\n"
     "function bkPos() { const n = shelf.children.length, i = Math.min(n - 1, bkIdx()); $('#bkPos').textContent = n ? String(i + 1).padStart(2, '0') + ' / ' + String(n).padStart(2, '0') : ''; $('#bkPrev').disabled = i <= 0; $('#bkNext').disabled = i >= n - 1; }\n"
     "function bkGo(d) { shelf.scrollTo({ left: (bkIdx() + d) * shelf.clientWidth, behavior: 'smooth' }); }\n"
     "let bkT = 0; shelf.addEventListener('scroll', () => { clearTimeout(bkT); bkT = setTimeout(bkPos, 60); }, { passive: true });"),
    ("  const th = e.target.closest('[data-theme-btn]'); if (th) { document.documentElement.dataset.theme = th.dataset.themeBtn;",
     "  if (e.target.closest('#bkPrev')) { bkGo(-1); return; } if (e.target.closest('#bkNext')) { bkGo(1); return; }\n"
     "  let th = e.target.closest('[data-theme-btn]');\n"
     "  if (th && innerWidth < 761 && th.getAttribute('aria-pressed') === 'true') { const all = $$('[data-theme-btn]'); th = all[(all.indexOf(th) + 1) % all.length]; }   /* на телефоне одна кнопка: нажатие — следующая тема */\n"
     "  if (th) { document.documentElement.dataset.theme = th.dataset.themeBtn;"),
])

css = io.open('assets/css/site.css', encoding='utf-8').read()
if 'КРУГ 01' not in css:
    css += r"""

/* ═══ КРУГ 01 (11.11.2026) — правки по канону: математика заголовка, шапка на телефоне, контраст светлых тем, лента книг ═══ */
:root { --tap: 44px; --txt-min: 16px; }

/* 10.13–10.15: до заголовка = его кегль, после группы = кегль, заголовок→подзаголовок = полкегля; блоки отделены одинаково */
.sec { padding: var(--hs) 0 0; } .sec--rib { padding: 0; } .sec--tg { padding-bottom: var(--hs); }
.sh { align-items: center; text-align: center; margin-bottom: var(--h); } .sh .eyebrow { display: none; }
.sh__h { margin-top: 0; max-width: 20ch; } .sh__s { margin-top: calc(var(--h) * .5); max-width: 62ch; }
.sh--row { display: flex; flex-direction: column; align-items: center; gap: 0; } .sh__g { align-items: center; } .sh--row .sh__link { margin-top: calc(var(--h) * .5); }
.sec--rib .sh { --h: var(--hs); }

/* лента программ: панель по высоте содержимого — после неё нет пустого экрана */
.rib__stick { height: auto; min-height: 0; top: 0; justify-content: flex-start; gap: 0; padding: var(--hs) 0 0; }
.rib__stick .sh { margin-bottom: var(--h); } .rib__bar { margin-top: var(--r3); }

/* шапка на телефоне: ничего за краем; тема — одной кнопкой (нажатие — следующая) */
.seg button { min-width: 34px; height: 36px; } .dot { width: 12px; height: 12px; }
.head.is-menu { --milk: inherit; --smoke: inherit; --gold: inherit; --on-gold: inherit; --line: inherit; --bg: inherit; background: var(--bg); }
[data-theme="paper"] .head.is-menu { --milk: #15130F; --smoke: #6B6457; --gold: #8A6718; --on-gold: #FBF8F1; --line: rgba(21, 19, 15, .14); --bg: #F3EEE4; }
[data-theme="sepia"] .head.is-menu { --milk: #23180A; --smoke: #75613F; --gold: #7C4A17; --on-gold: #F6ECD6; --line: rgba(35, 24, 10, .17); --bg: #E7D9BE; }
@media (max-width: 760px) {
  .head { gap: 8px; } .head__r { gap: 6px; min-width: 0; }
  #themes button[aria-pressed="false"] { display: none; } #themes button { min-width: 38px; height: 38px; } #themes .dot { width: 16px; height: 16px; }
  .seg--lang button { min-width: 30px; height: 38px; padding: 0 5px; }
  .burger { width: var(--tap); height: var(--tap); flex: 0 0 var(--tap); }
  .logo { min-height: var(--tap); display: inline-flex; align-items: center; }
}
@media (max-width: 359px) { .logo__w { display: none; } .seg--lang button { min-width: 27px; } }

/* N12: контраст в светлых темах */
[data-theme="paper"] { --smoke: #5A5347; --gold: #7A5A12; --gold-hi: #5F4609; }
[data-theme="sepia"] { --smoke: #5C4A2C; --gold: #6A3D10; --gold-hi: #4E2C08; }
.myth__b .myth__k, .myth__b .myth__btn { color: var(--myth-ink, var(--gold-hi)); } .myth__btn .arrow, .topic__a { color: currentColor; }

/* 10.4: текст не мельче 16 px */
.note { font-size: var(--txt-min); line-height: 1.55; color: var(--text); } .pc__d { font-size: var(--txt-min); } .foot__addr, .foot__col li { font-size: var(--txt-min); }

/* 10.29: одно семейство кнопок — две высоты, один шрифт */
.btn, .head__cta, .cine__btns a { font: 500 16px/1 var(--f-read); } .head__cta { height: var(--btn-h-sm); padding: 0 22px; }
.cine__btns a { min-height: var(--btn-h); } @media (max-width: 760px) { .cine__btns a { min-height: var(--btn-h-sm); } }

/* 4.2 / 4.8: специалисты — три строки у каждого; наставники одной строкой */
.facts li { min-height: calc(26px + 1.5em); } .mentors { margin: var(--r3) auto 0; max-width: 70ch; text-align: center; font: 400 italic clamp(18px, 1.5vw, 22px)/1.5 var(--f-display); color: var(--milk); }

/* 5.6: книги — лента по одной, справа налево, стрелки и свайп; 5.5: обложка стоит на тени-опоре */
.shelf { flex-direction: row; gap: 0; overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: none; overscroll-behavior-x: contain; } .shelf::-webkit-scrollbar { display: none; }
.bk { flex: 0 0 100%; scroll-snap-align: center; scroll-snap-stop: always; padding: 0 2px; }
.bk:nth-child(even) .bk__scene { order: 0; } .bk:nth-child(even) .bk__obj { transform: rotateY(var(--ry, -30deg)) rotateX(3deg); }
.bk__scene::after { opacity: 1; height: 34px; width: min(82%, 440px); }
[data-theme="night"] .bk__scene { background: radial-gradient(60% 46% at 50% 58%, color-mix(in srgb, var(--gold) 13%, transparent), transparent 70%); }
.shelf__nav { margin-top: var(--r3); display: flex; align-items: center; justify-content: center; gap: var(--r2); }
.arw { width: var(--btn-h); height: var(--btn-h); border-radius: 50%; border: 1px solid color-mix(in srgb, var(--gold) 60%, transparent); color: var(--milk); display: grid; place-items: center; transition: background var(--t1), color var(--t1), opacity var(--t1), transform var(--t1) var(--e); }
.arw svg { width: 22px; height: 22px; } .arw:hover { background: var(--gold); color: var(--on-gold); transform: translateY(-2px); } .arw:disabled { opacity: .3; pointer-events: none; }
.shelf__pos { font: 600 13px/1 var(--f-num); letter-spacing: .14em; color: var(--smoke); min-width: 64px; text-align: center; font-variant-numeric: tabular-nums; }
.shelf__more { margin-top: var(--r4); display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--r3); }
.shelf__next, .shelf__lib { margin: 0; padding: 0 0 0 var(--r2); border-left: 1px solid var(--gold); max-width: none; font: 400 italic clamp(18px, 1.5vw, 22px)/1.5 var(--f-display); color: var(--milk); }
.shelf__lib:empty, .shelf__next:empty, .mentors:empty, .cons__who:empty, .corp__lead:empty { display: none; }

/* 7.3: кто принимает; 8: тренинги без плиток-чисел — строка факта и клиенты */
.cons__who { margin-top: var(--r3); max-width: 62ch; font: 400 17px/1.6 var(--f-read); color: var(--text); }
.nums:empty { display: none; } .corp__lead { max-width: 62ch; margin: 0 auto; text-align: center; font: 400 italic clamp(19px, 1.7vw, 25px)/1.5 var(--f-display); color: var(--milk); }
.clients { margin-top: var(--r3); display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); }
.clients li { display: grid; place-items: center; min-height: 96px; padding: 0 var(--r1); text-align: center; font: 400 clamp(19px, 1.7vw, 25px)/1.15 var(--f-display); color: var(--milk); } .clients li + li { border-left: 1px solid var(--line); }

/* 9.8–9.9: подвал — имя золотом, три колонки, копирайт двумя строками */
.foot { padding: var(--hs) 0 calc(var(--r3) + 70px); } .foot__in { gap: var(--r3); align-items: stretch; }
.foot__cols { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--r3); padding-top: var(--r3); border-top: 1px solid var(--line); }
.foot__col h3 { font: 600 12.5px/1.3 var(--f-sub); letter-spacing: .22em; text-transform: uppercase; color: var(--gold); margin-bottom: var(--r1); }
.foot__col li { padding: 5px 0; color: var(--text); line-height: 1.45; } .foot__col a { color: inherit; border-bottom: 1px solid transparent; transition: color var(--t1), border-color var(--t1); } .foot__col a:hover { color: var(--milk); border-color: var(--gold); }
.foot__copy { display: flex; flex-direction: column; gap: 2px; font: 400 14px/1.5 var(--f-text); color: var(--smoke); }

@media (max-width: 760px) {
  .shelf__more { grid-template-columns: 1fr; gap: var(--r2); } .clients { grid-template-columns: 1fr 1fr; } .clients li { min-height: 78px; } .clients li:nth-child(3) { border-left: 0; } .clients li:nth-child(n+3) { border-top: 1px solid var(--line); }
  .foot__cols { grid-template-columns: 1fr; gap: var(--r2); } .arw { width: var(--btn-h-sm); height: var(--btn-h-sm); }
  .sh__h { max-width: 14ch; }
}
"""
    io.open('assets/css/site.css', 'w', encoding='utf-8', newline='\n').write(css)
print('patched')
