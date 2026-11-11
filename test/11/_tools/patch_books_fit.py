"""Книги: закреплённый блок точно по высоте видимой области; кнопка «Читать бесплатно» всегда видна, одной ширины по тексту
и на одной линии у всех книг. Проверка G4 в замер; правило в канон. Запуск из test/11."""
import io

CSS = """
/* ═══ книги: блок по высоте видимой области, кнопки всех книг на одной линии (владелец, 11.11) ═══ */
.bk__stick { --w: clamp(230px, 22vw, 330px); }
.shelf { align-items: stretch; } .bk { align-items: stretch; }
.bk__txt { display: flex; flex-direction: column; justify-content: flex-start; min-height: 0; } .bk__scene { align-self: center; }
.bk__t { min-height: 2.1em; display: flex; align-items: flex-end; } .bk__f { margin-bottom: var(--r1); }
.bk__btns { margin-top: auto; } .bk__btns .btn { width: auto; min-width: 0; flex: 0 0 auto; padding: 0 var(--r2); }
@media (max-width: 760px) {
  .bk__stick { --w: min(30vw, 17svh); height: 100vh; height: 100svh; min-height: 0; padding: 62px 0 var(--s3); justify-content: flex-start; }
  .bk__stick > .wrap { flex: 1; min-height: 0; display: flex; flex-direction: column; }
  .bk__stick .sh { margin-bottom: var(--s3); --h: 30px; } .bk__stick .sh__s { margin-top: var(--s1); font-size: 15px; line-height: 1.35; }
  .shelf__clip { flex: 1; min-height: 0; position: relative; display: flex; } .shelf { flex: 1; min-height: 0; }
  .bk { display: flex; flex-direction: column; gap: var(--s2); min-height: 0; } .bk__scene { padding: 0; background: none; } .bk__scene::after { display: none; }
  .bk__obj { --w: inherit; } .bk__txt { flex: 1; }
  .bk__t { font-size: 23px; line-height: 1.1; min-height: 2.2em; margin: 0; } .bk__a { margin: 2px 0 0; font-size: 14.5px; }
  .bk__f { margin: var(--s2) 0 var(--s2); } .bk__f li { padding: 6px 0; font-size: 15px; line-height: 1.35; }
  .bk__btns { flex-direction: row; margin-top: auto; } .bk__btns .btn { width: auto; min-height: var(--btn-h-sm); padding: 0 var(--r1); }
  .shelf__nav { position: absolute; left: 0; right: 0; top: calc(var(--w) * .7 - 22px); margin: 0; justify-content: space-between; pointer-events: none; z-index: 3; }
  .shelf__nav .arw { pointer-events: auto; width: var(--tap); height: var(--tap); background: color-mix(in srgb, var(--bg) 60%, transparent); } .shelf__pos { display: none; }
  .bk__stick > .wrap { position: relative; }
}
"""
p = 'assets/css/site.css'
c = io.open(p, encoding='utf-8').read()
if 'книги: блок по высоте видимой области' not in c:
    io.open(p, 'w', encoding='utf-8', newline='\n').write(c + CSS)

p = 'index.html'
t = io.open(p, encoding='utf-8').read()
a = '<div class="shelf__clip"><div class="shelf" id="shelf"></div></div><div class="shelf__nav">'
if a in t:                                             # стрелки — внутри области слайда, по бокам обложки
    i = t.index(a); j = t.index('</div></div></div>\n  </section>', i)
    nav = t[i + len('<div class="shelf__clip"><div class="shelf" id="shelf"></div></div>'):j]
    t = t[:i] + '<div class="shelf__clip"><div class="shelf" id="shelf"></div>' + nav + '</div>' + t[j:]
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

p = 'assets/js/site.js'
t = io.open(p, encoding='utf-8').read()
a = "function bkMeasure() { const n = shelf.children.length; stickTop(bkStick);"
if a not in t:
    raise SystemExit('site.js: bkMeasure не найден')
t = t.replace(a, "function bkMeasure() { const n = shelf.children.length; if (innerWidth < 761) bkStick.style.top = '0px'; else stickTop(bkStick);")
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

p = '_tools/round.py'
t = io.open(p, encoding='utf-8').read()
if "'G4'" not in t:
    a = "  // N2 имя в одну строку"
    t = t.replace(a, """  // G4: закреплённые блоки — в момент закрепления всё содержимое в видимой области; кнопки всех книг на одной линии и одной ширины
  (() => { const y0 = scrollY, sec = document.querySelector('[data-bk]'); if (!sec) return;
    scrollTo(0, sec.getBoundingClientRect().top + scrollY + 6); const H = innerHeight;
    const bs = [...sec.querySelectorAll('.bk__btns .btn')].map(b => b.getBoundingClientRect()); const tops = bs.map(r => Math.round(r.top)), ws = bs.map(r => Math.round(r.width));
    if (bs.length && Math.max(...tops) - Math.min(...tops) > 1) bad.push(['G4', 'книги: кнопки на разной высоте ' + [...new Set(tops)].join('/')]);
    if (bs.length && (bs[0].bottom > H - 6 || bs[0].top < 56)) bad.push(['G4', 'книги: кнопка вне видимой области (низ ' + Math.round(bs[0].bottom) + ' при высоте экрана ' + H + ')']);
    if (bs.length && W < 761 && bs[0].width > (W - 40) * .8) bad.push(['G4', 'книги: кнопка слишком широкая ' + Math.round(bs[0].width) + ' px']);
    const cov = sec.querySelector('.bk__obj'); if (cov && cov.getBoundingClientRect().top < 56) bad.push(['G4', 'книги: обложка под шапкой']);
    const rib = document.querySelector('[data-rib]'), st = rib && rib.querySelector('.rib__stick'); if (rib && st) { scrollTo(0, rib.getBoundingClientRect().top + scrollY - parseFloat(st.style.top || 0) + 6);
      const pc = rib.querySelector('.pc'); if (pc) { const r = pc.getBoundingClientRect(); if (r.bottom > H - 4 || r.top < 56) bad.push(['G4', 'программы: карточка не целиком на экране (' + Math.round(r.top) + '…' + Math.round(r.bottom) + ' при ' + H + ')']); } }
    scrollTo(0, y0); })();
""" + a)
    t = t.replace("EXTRA_W = [(430, 932), (412, 915), (375, 812), (360, 780)]", "EXTRA_W = [(430, 932), (412, 915), (375, 812), (360, 780), (390, 700), (360, 620)]   # последние две — экран с панелями браузера")
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

p = '_agent/docs/КАНОН_ГЛАВНАЯ.md'
t = io.open(p, encoding='utf-8').read()
if '15.25' not in t:
    t = t.replace("### Самопроверка перед показом", """- 15.25 [К] **авто (G4)** Одинаковые элементы стоят на одной линии: кнопки «Читать бесплатно» у всех книг — на одной высоте и одной ширины (по тексту, не во всю ширину); то же для любых повторяющихся кнопок в лентах и рядах. «Одни и те же кнопки на разных высотах» — грубая ошибка.
- 15.26 [К] **авто (G4)** Закреплённый блок целиком помещается в видимую область браузера, включая экраны небольшой высоты (панели браузера съедают часть экрана): в момент закрепления видны обложка, текст и кнопка; ничего не «выскакивает» при листании. Проверяется на высотах 620, 700, 780, 844 и 932 px.

### Самопроверка перед показом""")
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('patched')
