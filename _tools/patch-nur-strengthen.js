const fs = require('fs');
const path = require('path');
const dir = process.argv[2];
const log = [];

/* ── 1. CSS: новые фоны + миниатюры услуг + полоса «Məkan» ── */
let c = fs.readFileSync(path.join(dir, 'nur.css'), 'utf8');
c = c.replace("url('assets/spec-bg.jpg')", "url('assets/spec-bg-v2.jpg')");
c = c.replace("url('assets/book-bg.jpg')", "url('assets/book-bg-v2.jpg')");
c = c.replace("url('assets/cta-bg.jpg')", "url('assets/cta-bg-v2.jpg')");
log.push('фоны: spec/book/cta → v2');

c = c.replace(
  '.svc__row {\n  display: grid; grid-template-columns: 66px minmax(0, 2.4fr) minmax(0, 3.4fr) 66px;',
  '.svc__row {\n  display: grid; grid-template-columns: 54px 96px minmax(0, 2.2fr) minmax(0, 3.2fr) 60px;'
);
c = c.replace(
  '.svc__n { font-family: var(--font-mono);',
  `.svc__ph { width: 96px; aspect-ratio: 16 / 10; overflow: clip; border: var(--bd) solid var(--line); border-radius: var(--r); background: var(--bg-3); }
.svc__ph img { width: 100%; height: 100%; object-fit: cover; transition: transform .8s var(--e); }
html.mo .svc__row:hover .svc__ph img { transform: scale(1.08); }
.svc__n { font-family: var(--font-mono);`
);
log.push('услуги: миниатюры в строках');

const atmos = [
'/* ─────────────── MƏKAN · атмосфера (сгенерированные виды) ─────────────── */',
'.atmos__grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: clamp(14px, 2vw, 28px); margin-top: clamp(26px, 4.4vh, 48px); }',
'.atmos__item { margin: 0; }',
'.atmos__item img { width: 100%; aspect-ratio: 16 / 10; object-fit: cover; border: var(--bd) solid var(--line); border-radius: var(--r); }',
'.atmos__item figcaption { margin-top: 10px; }',
'@media (max-width: 800px) { .atmos__grid { grid-template-columns: 1fr; } }',
'',
'/* ─────────────────── ХРОНИКА (кадр на шаг) ─────────────────── */'].join('\n');
c = c.replace('/* ─────────────────── ХРОНИКА (кадр на шаг) ─────────────────── */', atmos);

/* мобильная сетка услуг: убрать миниатюру, оставить номер/текст/стрелку */
c = c.replace(
  '  .svc__row { grid-template-columns: 46px minmax(0, 1fr) 50px; }',
  '  .svc__row { grid-template-columns: 40px 74px minmax(0, 1fr) 46px; }\n  .svc__d { display: none; }\n  .svc__ph { width: 74px; }'
);
fs.writeFileSync(path.join(dir, 'nur.css'), c);
log.push('полоса Məkan + мобильные правки');

/* ── 2. HTML ── */
let h = fs.readFileSync(path.join(dir, 'index.html'), 'utf8');

/* постер из AI-видео */
h = h.replace('poster="assets/hero-bg.jpg"', 'poster="assets/hero-poster.jpg"');
log.push('постер героя → кадр из AI-видео');

/* миниатюры в строках услуг */
const thumbs = {
  'sosial-fobiya': '../../images/blog/sosial-fobiya/art1-cover.jpg',
  'depressiya.html': '../../images/blog/depressiya/art1-cover.jpg',
  'panik-ataklar': '../../images/blog/panik/art1-cover.jpg',
  'enurez.html': '../../images/blog/enurez/art1-cover.jpg',
  'aile-terapiyasi-usaq': '../../images/blog/aile-usaq/art1-cover.jpg',
  'aile-terapiyasi.html': '../../images/blog/aile/art1-cover.jpg'
};
h = h.replace(/<a class="svc__row" href="\.\.\/\.\.\/([^"]+)" data-rv data-cursor-label="Bax" data-img="([^"]+)">\s*\n\s*<span class="svc__n">(\d+)<\/span>/g,
  (m, href, img, n) => `<a class="svc__row" href="../../${href}" data-rv data-cursor-label="Bax" data-img="${img}">\n            <span class="svc__n">${n}</span>\n            <span class="svc__ph"><img src="${img}" alt="" loading="lazy"></span>`);
log.push('миниатюры вставлены в услуги');

/* полоса «Məkan» перед счётчиками */
const atmosBlock = `
    <!-- ─────────────── MƏKAN · атмосфера ─────────────── -->
    <section class="sec" id="mekan" data-rail="Məkan">
      <div class="wrap">
        <div class="sec__head" data-rv>
          <h2 class="h2" data-split><span class="h2__serif">Məkan</span> <span class="h2__script">atmosfer</span></h2>
          <span class="meta">05 — Bakı · Caspian Business Center</span>
        </div>
        <p class="sub" data-rv><span>Konsultasiya otağı, təlim zalı və studiya — <b class="sub__m">9-cu</b> mərtəbə, mərkəzi Bakı.</span></p>
        <div class="atmos__grid">
          <figure class="atmos__item" data-rv><img src="assets/clinic.jpg" alt="Konsultasiya otağı" loading="lazy"><figcaption class="meta">Konsultasiya otağı</figcaption></figure>
          <figure class="atmos__item" data-rv data-stagger="90"><img src="assets/hall.jpg" alt="Təlim zalı" loading="lazy"><figcaption class="meta">Təlim zalı</figcaption></figure>
          <figure class="atmos__item" data-rv data-stagger="180"><img src="assets/studio.jpg" alt="Studiya" loading="lazy"><figcaption class="meta">Studiya</figcaption></figure>
        </div>
      </div>
    </section>

`;
h = h.replace('    <!-- ───────────────────────── СЧЁТЧИКИ ───────────────────────── -->', atmosBlock + '    <!-- ───────────────────────── СЧЁТЧИКИ ───────────────────────── -->');
log.push('блок Məkan добавлен');

/* перенумерация после вставки */
h = h.replace('<span class="meta">04 — Faktlar</span>', '<span class="meta">06 — Faktlar</span>');
h = h.replace('<span class="meta">05 — Sorğu vəsaiti · 2026</span>', '<span class="meta">07 — Sorğu vəsaiti · 2026</span>');

/* навигация: добавить Məkan */
h = h.replace('<a href="#kitab" data-scramble>Kitab</a>', '<a href="#mekan" data-scramble>Məkan</a>\n        <a href="#kitab" data-scramble>Kitab</a>');

fs.writeFileSync(path.join(dir, 'index.html'), h);
log.push('перенумерация + навигация');

console.log('патч применён:');
log.forEach((l) => console.log(' • ' + l));
console.log('проверки:', /svc__ph/.test(h), /atmos__grid/.test(h), /hero-poster/.test(h));
