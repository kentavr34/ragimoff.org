/* =====================================================================
   _tools/epub-to-book.js — сборка веб-книги из EPUB (источники Фрейда, AZ).
   Каркас страниц — тот же, что у книг из DOCX (_tools/book-template.json),
   поэтому стили, меню, переключатель языков и навигация совпадают.
   Запуск: node _tools/epub-to-book.js _tools/configs/<book>.json
   ===================================================================== */
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const TPL = JSON.parse(fs.readFileSync(path.join(__dirname, 'book-template.json'), 'utf8'));
/* издательский мусор: эти строки в книгу не попадают */
const JUNK = /^(sigmund freud|ziqmund freyd|tərcümə|tercümə|İSBN|ISBN|©|qanun|nəşriyyat|nəşr\b|çap\b|redaktor|redaksiya|buraxılışa|müəllif hüquqları|bütün hüquqlar|kitabxana|translated by|translation|converted ebook|telegram|@)/i;
const UI = {
  az: { toc: 'Mündəricat', order: 'Kitabın sifarişi', back: 'Kitablar', prev: 'Əvvəlki', next: 'Növbəti', read: 'Oxu', home: 'Ana səhifə', up: 'Kitab', part: 'Bölmə' },
  ru: { toc: 'Содержание', order: 'Заказать книгу', back: 'Книги', prev: 'Предыдущая', next: 'Следующая', read: 'Читать', home: 'Главная', up: 'Книга', part: 'Часть' },
  en: { toc: 'Contents', order: 'Order the book', back: 'Books', prev: 'Previous', next: 'Next', read: 'Read', home: 'Home', up: 'Book', part: 'Part' },
};

function up(s, code) { const t = String(s == null ? '' : s); const c = code || global.__LANG; return (c === 'az' || c === 'tr') ? t.replace(/i/g, 'İ').toUpperCase() : t.toUpperCase(); }
function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
function slugify(s, i, lang) {
  const base = String(s).toLowerCase()
    .replace(/[əıöüçşğ]/g, (c) => ({ 'ə': 'e', 'ı': 'i', 'ö': 'o', 'ü': 'u', 'ç': 'c', 'ş': 's', 'ğ': 'g' }[c] || c))
    .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 42);
  return String(i).padStart(2, '0') + '-' + (base || 'bolme-' + i);
}

/* ── разбор EPUB: части = файлы index_split_*.html в порядке из content.opf ── */
function readEpub(file) {
  /* unzip в Windows не понимает не-ASCII пути — копируем во временный файл */
  const __epubTmp = path.join(require("os").tmpdir(), "book-src-" + Date.now() + ".epub");
  fs.copyFileSync(file, __epubTmp);
  file = __epubTmp;
  const list = execFileSync('unzip', ['-Z1', file], { maxBuffer: 64 * 1024 * 1024 }).toString('utf8')
    .split('\n').map((x) => x.trim()).filter(Boolean);
  const parts = list.filter((f) => /\.x?html?$/i.test(f)).sort();
  const out = [];
  parts.forEach((f) => {
    const raw = execFileSync('unzip', ['-p', file, f], { maxBuffer: 128 * 1024 * 1024 }).toString('utf8');
    /* текст: убираем скрипты/стили, теги → абзацы */
    const clean = raw.replace(/<(script|style)[\s\S]*?<\/\1>/gi, ' ')
      .replace(/<\/(p|div|h[1-6]|li|tr)>/gi, '\n').replace(/<br\s*\/?>/gi, '\n')
      .replace(/<[^>]+>/g, ' ');
    const paras = clean.split('\n')
      .map((x) => x.replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
        .replace(/&quot;/g, '"').replace(/&#(\d+);/g, (m, d) => String.fromCharCode(+d))
        .replace(/\s+/g, ' ').trim())
      .filter((x) => x.length > 2 && !/^index$/i.test(x) && !JUNK.test(x));
    if (paras.length) out.push({ file: f, paras });
  });
  return out;
}

const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const outRoot = path.resolve(cfg.out);
fs.mkdirSync(outRoot, { recursive: true });
if (cfg.styleFrom && fs.existsSync(cfg.styleFrom)) fs.copyFileSync(cfg.styleFrom, path.join(outRoot, 'style.css'));

let total = 0;
cfg.langs.forEach((lang) => {
  global.__LANG = lang.code;
  const dir = path.join(outRoot, lang.dir || '');
  fs.mkdirSync(dir, { recursive: true });
  if (cfg.styleFrom && fs.existsSync(cfg.styleFrom)) fs.copyFileSync(cfg.styleFrom, path.join(dir, 'style.css'));

  const parts = readEpub(lang.file);
  /* титул книги, повторённый в начале (в т.ч. капсом) — в книгу не попадает */
  const normT = (x) => String(x).toLowerCase().replace(/[«»"'`.,:;!?()\[\]–—-]/g, ' ').replace(/\s+/g, ' ').trim();
  const bookTitle = normT(lang.title);
  parts.forEach((part) => {
    part.paras = part.paras.filter((x, i) => !(i < 15 && (normT(x) === bookTitle ||
      /^(bakı|\(c\)|©|isbn|qanun|nəşriyyat|tərcümə|tercümə|redaktor)/i.test(x.trim()) ||
      (x.length < 60 && /qanun nəşriyyatı|nəşriyyatı/i.test(x)))));
  });
  const ui = UI[lang.ui] || UI.az;
  const all = parts.map((p, i) => {
    /* заголовок — первая осмысленная строка части, без нумерации */
    const first = (p.paras.find((x) => x.length > 20 && !JUNK.test(x)) || '').replace(/\s+/g, ' ').trim();
    const looksHead = first && first.length <= 70 && !/[.!?…]$/.test(first) && first.split(' ').length <= 9;
    const title = looksHead ? first : (lang.title || '');
    return { num: String(i + 1).padStart(2, '0'), file: slugify(title, i + 1, lang.code) + '.html', title, short: title, paras: p.paras };
  });
  const rel = lang.dir ? '../' : '';
  const name = lang.title;

  function headHtml(title, desc) {
    const langs = cfg.langs.map((l) => l.code).join(',');
    const urls = cfg.langs.map((l) => ' data-lang-url-' + l.code + '="/' + cfg.out + (l.dir ? '/' + l.dir : '') + '/"').join('');
    return TPL.head
      .replace('<html ', '<html data-langs="' + langs + '"' + urls + ' ')
      .replace(/<html([^>]*?)lang="[a-z]{2}"/, '<html$1lang="' + lang.code + '"')
      .replace(/<title>[\s\S]*?<\/title>/, '<title>' + esc(title) + ' | ' + esc(up(name)) + '</title>')
      .replace(/<meta name="description" content="[^"]*"/, '<meta name="description" content="' + esc(desc) + '"')
      .replace(/<meta property="og:title" content="[^"]*"/, '<meta property="og:title" content="' + esc(title) + '"')
      .replace(/<meta property="og:description" content="[^"]*"/, '<meta property="og:description" content="' + esc(desc) + '"')
      .replace(/<meta property="og:url" content="[^"]*"/, '<meta property="og:url" content="https://ragimoff.org/' + cfg.slug + '/"')
      .replace(/"name":"[^"]*","inLanguage":"[^"]*"/, '"name":"' + esc(name) + '","inLanguage":"' + lang.code + '"')
      .replace(/"author":\{"@type":"Person","name":"[^"]*"\}/, '"author":{"@type":"Person","name":"' + esc(lang.author || cfg.author) + '"}')
      .replace('</head>', TOC_STYLE + '</head>')
      .replace(/<a href="https:\/\/ragimoff\.org"[^>]*class="hdr-back"[^>]*>/,
        '<a href="' + (lang.code === 'az' ? 'https://ragimoff.org/' : 'https://ragimoff.org/' + lang.code + '/') +
        '" class="hdr-back" title="' + (lang.code === 'ru' ? 'Вернуться на главную сайта' : 'Ana sayta qayıt') + '">')
      .replace('src="/_lang-switch.js?v=4"', 'src="/_lang-switch.js?v=5"');
  }
  const TOC_STYLE = '<style>' +
    '.home-hero{padding:16px 0 11px}' +
    '.book-toc{margin:8px auto 36px}' +
    '.book-toc .toc-title{margin:0 0 16px 0;padding-bottom:8px}' +
    '.content-wrap .toc-test{margin:0 0 34px}' +
    '.d-nav{display:flex;align-items:center;justify-content:space-between;gap:.5rem;margin:2.2rem 0 .5rem;padding:.7rem 0 0;border-top:1px solid var(--border)}' +
    '.d-nav a{color:var(--text);text-decoration:none;padding:.35rem .7rem;border-radius:6px;font-family:var(--mono,monospace);font-weight:700;font-size:.95rem;white-space:nowrap;max-width:42%;overflow:hidden;text-overflow:ellipsis}' +
    '.d-nav .up{color:var(--gold);font-family:var(--font);font-weight:600}' +
    '.d-nav .dn-name{color:var(--text2);font-weight:400;font-family:var(--font);font-size:.85rem}' +
    /* чтение с телефона на тёмном фоне: крупнее кегль, просторнее строки */
    '.content-wrap p{font-size:clamp(16.5px,1.05rem,19px);line-height:1.78;margin:0 0 1.05em;color:var(--text)}' +
    '@media(max-width:600px){.content-wrap{padding-left:18px;padding-right:18px}.content-wrap p{font-size:17.5px;line-height:1.8}}' +
    '.sidebar .nav-sub-link{padding:7px 14px 7px 18px;font-size:11px;gap:.5rem;line-height:1.4}' +
    '.sidebar .sub-code{flex:0 0 auto;width:auto;white-space:nowrap;margin-right:0;font-size:10px}' +
    '.sidebar .nav-sub-link.is-active{color:var(--gold);border-left-color:var(--gold);background:var(--gold-bg)}' +
    '</style>';

  function bodyTop() {
    return TPL.bodyTop
      .replace(/<div class="hdr-logo">[^<]*<\/div>/, '<div class="hdr-logo">' + cfg.logo + '</div>')
      .replace(/<strong>[^<]*<\/strong>/, '<strong>' + esc(up(name)) + '</strong>')
      .replace(/<small>[^<]*<\/small>/, '<small>' + esc(lang.author || cfg.author) + ' · ' + cfg.year + '</small>')
      .replace('data-lang-switch', 'data-lang-switch data-langs="' + cfg.langs.map((l) => l.code).join(',') + '"');
  }
  function sidebarHtml(idx) {
    const items = all.map((c, i) =>
      '<div class="nav-item"><a href="' + c.file + '" class="nav-sub-link' + (i === idx ? ' is-active' : '') + '">' +
      '<span class="sub-code">' + c.num + '</span><span class="sub-name">' + esc(c.short) + '</span></a></div>').join('\n      ');
    return '<aside class="sidebar" id="sb">\n    <div class="sb-hdr"><a class="sb-site" href="https://ragimoff.org/books/" title="Kitablar">← ' + ui.back + '</a>' +
      '<button class="sb-close" onclick="toggleSb()" aria-label="Bağla">✕</button></div>\n    <nav>\n      <div class="nav-item"><a href="index.html" class="nav-link nav-front">' + ui.home + '</a></div>\n      ' +
      items + '\n    </nav>\n  </aside>';
  }
  function chapterPage(ch, idx) {
    const prev = idx > 0 ? all[idx - 1] : null, next = idx < all.length - 1 ? all[idx + 1] : null;
    const content = '\n<nav class="crumb"><a href="index.html">‹ ' + esc(name) + '</a></nav>\n' +
      '<h1 class="chap-title-wrap"><span class="chap-title">' + esc(ch.title) + '</span></h1>\n' +
      ch.paras.map((p) => '<p>' + esc(p) + '</p>').join('\n') + '\n' +
      '<nav class="d-nav">' +
      (prev ? '<a href="' + prev.file + '">← ' + prev.num + ' <span class="dn-name">' + esc(prev.short) + '</span></a>' : '<span></span>') +
      '<a class="up" href="index.html">↑ ' + ui.up + '</a>' +
      (next ? '<a href="' + next.file + '"><span class="dn-name">' + esc(next.short) + '</span> ' + next.num + ' →</a>' : '<span></span>') +
      '</nav>\n' + TPL.tail;
    return headHtml(ch.title, name + ' — ' + ch.title) + '\n</head>\n' + bodyTop() + sidebarHtml(idx) + TPL.mid + TPL.contentOpen + content;
  }
  function indexPage() {
    const cards = all.map((c) => '<div class="toc-chapter"><a href="' + c.file + '" class="toc-chapter-title"><span class="toc-name">' + esc(c.title) + '</span></a></div>').join('\n      ');
    const content = '\n<div class="home-hero"><h1 class="home-title">' + esc(up(name)) + '</h1>' +
      '<p class="sub">' + esc(lang.subtitle || cfg.subtitle || '') + '</p></div>\n' +
      '<section class="book-toc"><h2 class="toc-title">' + esc(up(ui.toc)) + '</h2>\n      ' + cards + '\n    </section>\n';
    return headHtml(name, name + ' — ' + (cfg.subtitle || '')) + '\n</head>\n' + bodyTop() + sidebarHtml(-1) + TPL.mid + TPL.contentOpen + content;
  }

  all.forEach((ch, i) => { fs.writeFileSync(path.join(dir, ch.file), chapterPage(ch, i), 'utf8'); total++; });
  fs.writeFileSync(path.join(dir, 'index.html'), indexPage(), 'utf8'); total++;
  console.log(lang.code + ': частей ' + all.length + ' → ' + (path.relative(process.cwd(), dir) || '.'));
});
console.log('всего страниц:', total);
