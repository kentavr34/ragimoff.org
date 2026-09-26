const fs = require('fs');
const path = require('path');
const dir = process.argv[2];

/* ── 1. v8: в галерее-хронике только документы (дипломы/институт/фахри), не студенты ── */
const htmlF = path.join(dir, 'v8-ag.html');
let h = fs.readFileSync(htmlF, 'utf8');
const swap = {
  'images/students/cert-3.jpg': 'images/diplomas/internatura-2001.jpg',
  'images/students/group-outdoor.jpg': 'images/diplomas/nlp-diploma-1999.jpg',
  'images/students/korporativ-tehsil.jpg': 'images/institute/diplom-psy-spb-idpo.jpg',
  'images/students/psixologiya-mekteb.jpg': 'images/fahri/doc-fexri-ferman.jpg',
  'images/students/group-training.jpg': 'images/diplomas/sert-a2139286.jpg'
};
let swapped = 0;
for (const [from, to] of Object.entries(swap)) {
  if (h.includes(from)) { h = h.split(from).join(to); swapped++; }
}
fs.writeFileSync(htmlF, h);
console.log('v8-ag.html: заменено фото студентов в хронике —', swapped, 'из', Object.keys(swap).length);

/* ── 2. v8.css: документы вписывать целиком (contain) ── */
const cssF = path.join(dir, 'v8.css');
let c = fs.readFileSync(cssF, 'utf8');
c = c.replace(
  '.chr__item img { width: 100%; height: 100%; object-fit: cover; filter: saturate(.9); }',
  '.chr__item img { width: 100%; height: 100%; object-fit: contain; filter: saturate(.9); background: var(--bg-2); padding: clamp(10px, 1.6vw, 22px); }'
);
fs.writeFileSync(cssF, c);
console.log('v8.css: галерея → object-fit: contain (документы видны целиком)');

/* ── 3. NÜR: синхронизация в _deploy ── */
console.log('готово');
