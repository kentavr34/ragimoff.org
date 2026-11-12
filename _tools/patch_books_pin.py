"""Книги: блок закрепляется, прокрутка листает книги по одной (как лента программ); одна кнопка «Читать бесплатно»;
«Общая психотерапия» — шестым слайдом в том же шаблоне. Запуск из test/11."""
import io, re, shutil, pathlib

for f in ('index.html', 'assets/js/site.js', 'assets/css/site.css', 'assets/js/content.js'):
    shutil.copy(f, '_agent/backup/' + pathlib.Path(f).name + '.bak-bookspin')

# ── разметка
p = 'index.html'
t = io.open(p, encoding='utf-8').read()
m = re.search(r'  <section class="sec" id="books">.*?</section>\n', t, re.S)
if not m:
    raise SystemExit('секция книг не найдена')
ARW = lambda d: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="%s" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>' % d
new = ('  <section class="sec sec--bk" id="books" data-bk>\n'
       '    <div class="bk__stick"><div class="wrap"><header class="sh" data-h="books"></header><div class="shelf__clip"><div class="shelf" id="shelf"></div></div>'
       '<div class="shelf__nav"><button type="button" class="arw" id="bkPrev" aria-label="←">' + ARW('M15 5l-7 7 7 7') + '</button><span class="shelf__pos" id="bkPos"></span>'
       '<button type="button" class="arw" id="bkNext" aria-label="→">' + ARW('M9 5l7 7-7 7') + '</button></div></div></div>\n'
       '  </section>\n'
       '  <div class="wrap"><p class="shelf__lib rv" data-i="books.lib"></p></div>\n')
t = t[:m.start()] + new + t[m.end():]
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

# ── скрипт
p = 'assets/js/site.js'
t = io.open(p, encoding='utf-8').read()
a = t.index("  $('#shelf').innerHTML = t.books.b.map(")
b = t.index("</div></div></article>`).join('');", a) + len("</div></div></article>`).join('');")
render = """  const bkAll = t.books.b.map((b, i) => ({ b, href: L.books[i], img: `assets/img/book-${cov[i]}-${lang}.jpg` })).concat(t.books.soon ? [{ b: t.books.soon, href: L.shop, img: '' }] : []);
  $('#shelf').innerHTML = bkAll.map(({ b, href, img }) => `<article class="bk"><div class="bk__scene"><a class="bk__obj${img ? '' : ' bk__obj--txt'}" href="${href}" aria-label="${esc(b.t)}">${img ? `<img src="${img}" alt="${esc(b.t)}" loading="lazy">` : `<span class="bk__ct"><i>${esc(b.a)}</i><b>${esc(b.t)}</b><u>Doctor Ragimoff</u></span>`}</a></div>
    <div class="bk__txt">${b.k ? `<p class="bk__k">${esc(b.k)}</p>` : ''}<h3 class="bk__t">${esc(b.t)}</h3><p class="bk__a">${esc(b.a)}</p>
    <ul class="bk__f">${b.f.map((f, j) => `<li><b>0${j + 1}</b><span>${esc(f)}</span></li>`).join('')}</ul>
    <div class="bk__btns"><a class="btn" href="${href}">${esc(t.books.read)}</a></div></div></article>`).join('');
  bkMeasure(); bkScroll();"""
t = t[:a] + render + t[b:]
t = t.replace("  bkPos();\n", "", 1)
a = t.index("const shelf = $('#shelf');")
b = t.index("let bkT = 0; shelf.addEventListener('scroll'", a)
b = t.index("\n", b) + 1
pin = """const shelf = $('#shelf'), bkSec = $('[data-bk]'), bkStick = $('.bk__stick');
let bkI = 0, bkStep = 1;
function bkMeasure() { const n = shelf.children.length; bkStep = Math.round(innerHeight * (innerWidth < 761 ? .75 : .6)); bkSec.style.height = (bkStick.offsetHeight + Math.max(0, n - 1) * bkStep) + 'px'; }
function bkScroll() {                                   /* прокрутка листает книги по одной: большую часть шага книга стоит, переход — в середине */
  const n = shelf.children.length; if (!n) return;
  const r = bkSec.getBoundingClientRect(), total = bkSec.offsetHeight - bkStick.offsetHeight, p = total > 0 ? clamp(-r.top / total) : 0;
  const x = p * (n - 1), k = Math.floor(x), f = x - k, e = f < .3 ? 0 : f > .7 ? 1 : (f - .3) / .4, pos = Math.min(n - 1, k + e * e * (3 - 2 * e));
  shelf.style.setProperty('--bx', (-pos * 100).toFixed(2) + '%');
  const i = Math.round(pos); if (i !== bkI || !$('#bkPos').textContent) { bkI = i; $('#bkPos').textContent = String(i + 1).padStart(2, '0') + ' / ' + String(n).padStart(2, '0'); $('#bkPrev').disabled = i <= 0; $('#bkNext').disabled = i >= n - 1; }
}
function bkGo(d) { const n = shelf.children.length, i = Math.max(0, Math.min(n - 1, bkI + d)); scrollTo({ top: bkSec.getBoundingClientRect().top + scrollY + i * bkStep, behavior: 'smooth' }); }
let bkX0 = null; shelf.addEventListener('touchstart', e => { bkX0 = [e.touches[0].clientX, e.touches[0].clientY]; }, { passive: true });
shelf.addEventListener('touchend', e => { if (!bkX0) return; const dx = e.changedTouches[0].clientX - bkX0[0], dy = e.changedTouches[0].clientY - bkX0[1]; bkX0 = null; if (Math.abs(dx) > 44 && Math.abs(dx) > Math.abs(dy) * 1.4) bkGo(dx < 0 ? 1 : -1); }, { passive: true });
"""
t = t[:a] + pin + t[b:]
for old, new_ in [
    ("addEventListener('scroll', onScroll, { passive: true });", "addEventListener('scroll', onScroll, { passive: true }); addEventListener('scroll', bkScroll, { passive: true });"),
    ("ribMeasure(); onScroll(); }, 120); });", "ribMeasure(); bkMeasure(); bkScroll(); onScroll(); }, 120); });"),
]:
    if old not in t:
        raise SystemExit('site.js: не найдено ' + old[:60])
    t = t.replace(old, new_, 1)
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

# ── стили
CSS = """
/* ═══ книги: закреплённый блок, прокрутка листает по одной; одна кнопка; слайд на одном экране (владелец, 11.11 вечер) ═══ */
.sec--bk { padding: 0; }
.bk__stick { position: sticky; top: 0; min-height: 100vh; min-height: 100svh; display: flex; flex-direction: column; justify-content: center; padding: var(--hs) 0 var(--r2); overflow: hidden; }
.bk__stick .sh { margin-bottom: calc(var(--h) * .5); }
.shelf__clip { overflow: hidden; }
.shelf { overflow: visible; scroll-snap-type: none; transform: translate3d(var(--bx, 0%), 0, 0); will-change: transform; }
.bk { scroll-snap-align: none; } .bk__btns .btn { min-width: 220px; }
.shelf__lib { margin-top: var(--r3); max-width: 62ch; }
.bk__obj--txt { display: grid; place-items: center; aspect-ratio: 5 / 7; width: var(--w); background: linear-gradient(160deg, #141a2a, #07090e 70%); border: 1px solid rgba(201, 169, 97, .5); border-radius: 3px 6px 6px 3px; }
.bk__obj--txt::before, .bk__obj--txt::after { display: none; }
.bk__ct { display: flex; flex-direction: column; align-items: center; justify-content: space-between; height: 86%; padding: 0 10%; text-align: center; }
.bk__ct i { font: 500 calc(var(--w) * .042)/1.2 var(--f-sub); letter-spacing: .28em; text-transform: uppercase; color: #C9A961; font-style: normal; }
.bk__ct b { font: 400 calc(var(--w) * .12)/1.08 var(--f-display); color: #F2EDE3; text-transform: uppercase; letter-spacing: .04em; }
.bk__ct u { font: 400 calc(var(--w) * .1)/1 var(--f-hand); color: #E6CE93; text-decoration: none; }
@media (max-width: 760px) {
  .bk__stick { padding: 70px 0 var(--r1); justify-content: flex-start; } .bk__stick .sh { margin-bottom: var(--r1); } .bk__stick .sh__s { margin-top: 8px; }
  .bk__obj { --w: min(34vw, 22svh); } .bk__btns { flex-direction: row; } .bk__btns .btn { width: 100%; min-width: 0; }
  .shelf__nav { margin-top: 10px; }
}
"""
p = 'assets/css/site.css'
c = io.open(p, encoding='utf-8').read()
if 'книги: закреплённый блок' not in c:
    io.open(p, 'w', encoding='utf-8', newline='\n').write(c + CSS)

# ── тексты: шестой слайд
p = 'assets/js/content.js'
t = io.open(p, encoding='utf-8').read()
if 'BOOK_SOON' not in t:
    t += """
/* ── BOOK_SOON: «Общая психотерапия» — тем же шаблоном; кнопка пока ведёт на главную страницу книг (слово владельца 11.11) ── */
const SOON = {
  ru: { k: 'Скоро', t: 'Общая психотерапия', a: 'Кенан Рагимов', f: ['Том на русском языке уже готов.', 'Азербайджанское издание готовится.', 'Скоро книга появится среди наших книг.'] },
  az: { k: 'Tezliklə', t: 'Ümumi psixoterapiya', a: 'Kənan Rəhimov', f: ['Rus dilində cild artıq hazırdır.', 'Azərbaycan dilində nəşr hazırlanır.', 'Tezliklə kitablarımızın sırasında olacaq.'] },
  en: { k: 'Coming soon', t: 'General psychotherapy', a: 'Kenan Ragimov', f: ['The volume in Russian is ready.', 'The Azerbaijani edition is in preparation.', 'It will soon join our books.'] },
};
for (const l of Object.keys(SOON)) T[l].books.soon = SOON[l];
"""
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('patched')
