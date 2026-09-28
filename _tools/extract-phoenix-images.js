/* Извлекает картинки моделей из DOCX книги «Эра Феникса» и привязывает их к моделям.
   Пишет: books/phoenix-era/test/img/<модель>.jpg (общие для AZ и RU) + карту в
   _tools/phoenix-test-images.json. Запуск: node _tools/extract-phoenix-images.js */
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const IMG_DIR = path.join(ROOT, 'books/phoenix-era/test/img');
const TEST = JSON.parse(fs.readFileSync(path.join(__dirname, 'phoenix-test.json'), 'utf8'));

function decode(s) {
  return s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"')
    .replace(/&apos;/g, "'").replace(/&amp;/g, '&').replace(/&#(\d+);/g, (m, d) => String.fromCharCode(+d));
}
function xmlOf(file, part) {
  return execFileSync('unzip', ['-p', file, part], { maxBuffer: 300 * 1024 * 1024 }).toString('utf8');
}
function rels(file) {
  const x = xmlOf(file, 'word/_rels/document.xml.rels');
  const map = {};
  for (const m of x.matchAll(/<Relationship\b[^>]*>/g)) {
    const tag = m[0];
    const id = (tag.match(/Id="([^"]+)"/) || [])[1];
    const target = (tag.match(/Target="([^"]+)"/) || [])[1];
    if (id && target) map[id] = target;
  }
  return map;
}
/* картинки по порядку появления в документе + индекс абзаца.
   ВАЖНО: абзацы с картинками текста не имеют — их нельзя пропускать */
function images(file) {
  const R = rels(file);
  const xml = xmlOf(file, 'word/document.xml');
  const out = [];
  const re = /<w:p[ >][\s\S]*?<\/w:p>|<w:p\/>/g;
  let m, i = 0;
  while ((m = re.exec(xml)) !== null) {
    const p = m[0];
    const texts = [];
    const tr = /<w:t[^>]*>([\s\S]*?)<\/w:t>/g;
    let t;
    while ((t = tr.exec(p)) !== null) texts.push(decode(t[1]));
    let text = texts.join('').replace(/\s+/g, ' ').trim()
      .replace(/<[^>]*>/g, ' ').replace(/\bw:[a-zA-Z]+/g, ' ').replace(/[\u0000-\u001f]/g, ' ').replace(/\s+/g, ' ').trim();
    const imgs = [...p.matchAll(/r:embed="([^"]+)"/g)].map((x) => R[x[1]]).filter(Boolean);
    if (!text && !imgs.length) continue;
    out.push({ i, text, imgs });
    i++;
  }
  return out;
}
/* заголовки глав моделей: «Bölüm N. MÜNASİBƏT MODELİ» */
function modelHeads(paras) {
  const heads = [];
  paras.forEach((p) => {
    const m = p.text.match(/^(?:BÖLÜM|Bölüm|bÖLÜM|ГЛАВА|Глава)\s*(\d+)\s*[.\s]+(?:MÜNASİBƏT MODELİ|МОДЕЛЬ ВЗАИМООТНОШЕНИЙ)/i);
    if (m) heads.push({ n: +m[1], i: p.i });
  });
  return heads;
}

fs.mkdirSync(IMG_DIR, { recursive: true });
const map = {};
let saved = 0;

['az', 'ru'].forEach((code) => {
  const file = code === 'az'
    ? 'D:/Документы/BOOKS/Phoenix/Feniks_Erasi_v12-1 az.docx'
    : 'D:/Документы/BOOKS/Phoenix/Era_Feniksa_1.docx rus.docx';
  const paras = images(file);
  const heads = modelHeads(paras);
  const blocks = TEST.langs[code].blocks;
  console.log('=== ' + code + ': глав-моделей ' + heads.length + ', картинок ' + paras.reduce((n, p) => n + p.imgs.length, 0));
  heads.forEach((h, k) => {
    const next = heads[k + 1] ? heads[k + 1].i : 1e9;
    const model = blocks[h.n - 1] ? blocks[h.n - 1].model : null;
    const found = [];
    paras.forEach((p) => { if (p.i > h.i && p.i < next) p.imgs.forEach((im) => found.push(im)); });
    if (model && found.length) {
      map[model] = map[model] || { az: null, ru: null };
      if (!map[model][code]) map[model][code] = found[0];
      console.log('   ' + h.n + '. ' + model + ' → ' + found.join(', '));
    } else if (model) {
      console.log('   ' + h.n + '. ' + model + ' → картинки НЕТ');
    }
  });
});

/* копируем по одной картинке на модель (берём AZ, если есть, иначе RU).
   Имена файлов — латиницей (кириллица в URL нежелательна), дубликаты не плодим. */
const fileFor = (code) => code === 'az'
  ? 'D:/Документы/BOOKS/Phoenix/Feniks_Erasi_v12-1 az.docx'
  : 'D:/Документы/BOOKS/Phoenix/Era_Feniksa_1.docx rus.docx';
const TRANSLIT = {
  'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i',
  'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
  'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
  'э': 'e', 'ю': 'yu', 'я': 'ya', 'ə': 'e', 'ı': 'i', 'ö': 'o', 'ü': 'u', 'ç': 'c', 'ş': 's', 'ğ': 'g',
};
function slug(name) {
  return String(name).toLowerCase().split('').map((ch) => (TRANSLIT[ch] !== undefined ? TRANSLIT[ch] : ch))
    .join('').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}
const crypto = require('crypto');
const out = {};
const written = {};      /* md5 → имя файла: одинаковые картинки не дублируем */
Object.entries(map).forEach(([model, src]) => {
  const pick = src.az || src.ru;
  if (!pick) return;
  const code = src.az ? 'az' : 'ru';
  const ext = path.extname(pick) || '.jpeg';
  const name = slug(model) + ext;
  const tmp = path.join(IMG_DIR, name);
  try {
    execFileSync('unzip', ['-p', fileFor(code), 'word/' + pick], { maxBuffer: 300 * 1024 * 1024, stdio: ['ignore', fs.openSync(tmp, 'w'), 'ignore'] });
    const md5 = crypto.createHash('md5').update(fs.readFileSync(tmp)).digest('hex');
    if (written[md5]) { fs.unlinkSync(tmp); out[model] = written[md5]; return; }
    written[md5] = '/books/phoenix-era/test/img/' + name;
    out[model] = written[md5];
    saved++;
  } catch (e) { console.log('ошибка извлечения ' + model + ': ' + e.message.slice(0, 60)); }
});
fs.writeFileSync(path.join(__dirname, 'phoenix-test-images.json'), JSON.stringify(out, null, 2), 'utf8');
console.log('=== сохранено картинок: ' + saved + ' → _tools/phoenix-test-images.json');
