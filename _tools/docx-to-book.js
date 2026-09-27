/* =====================================================================
   RAGIMOFF · _tools/docx-to-book.js — конвертер книги DOCX → веб-книга
   Подструктура как у «Klinik Psixiatriya»: index.html (обложка + оглавление),
   страницы глав, style.css, сайдбар с оглавлением, навигация пред/след.

   Запуск:
     node _tools/docx-to-book.js <config.json>

   Конфиг (JSON):
   {
     "slug": "phoenix-era",
     "title": "Feniks Erası",
     "titleRu": "Эра Феникса",
     "author": "Samirə Rəhimova · Kənan Rəhimov",
     "year": "2026",
     "logo": "FE",
     "out": "books/phoenix-era",
     "styleFrom": "klinik-psixiatriya/style.css",
     "langs": [
       { "code": "az", "dir": "",    "file": "D:/…/Feniks_Erasi_v12-1 az.docx",  "title": "Feniks Erası",  "ui": "az" },
       { "code": "ru", "dir": "ru",  "file": "D:/…/Era_Feniksa_1.docx rus.docx",  "title": "Эра Феникса",   "ui": "ru" }
     ]
   }
   ===================================================================== */
'use strict';

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

/* ─────────── извлечение параграфов ─────────── */
function decode(s) {
  return s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"')
    .replace(/&apos;/g, "'").replace(/&amp;/g, '&')
    .replace(/&#(\d+);/g, (m, d) => String.fromCharCode(+d));
}

function paragraphs(file) {
  const xml = execFileSync('unzip', ['-p', file, 'word/document.xml'], { maxBuffer: 300 * 1024 * 1024 }).toString('utf8');
  const out = [];
  const re = /<w:p[ >][\s\S]*?<\/w:p>|<w:p\/>/g;
  let m;
  while ((m = re.exec(xml)) !== null) {
    const p = m[0];
    const texts = [];
    const tr = /<w:t[^>]*>([\s\S]*?)<\/w:t>/g;
    let t;
    while ((t = tr.exec(p)) !== null) texts.push(decode(t[1]));
    let text = texts.join('').replace(/\s+/g, ' ').trim();
    text = text.replace(/<[^>]*>/g, ' ').replace(/\bw:[a-zA-Z]+/g, ' ')
      .replace(/[\u0000-\u001f]/g, ' ').replace(/\s+/g, ' ').trim();
    if (!text) continue;
    const bold = /<w:b\/>|<w:b w:val="(1|true)"/.test(p);
    const italic = /<w:i\/>|<w:i w:val="(1|true)"/.test(p);
    const sz = +((p.match(/<w:sz w:val="(\d+)"/) || [])[1] || 0);
    out.push({ text, bold, italic, sz });
  }
  return out;
}

/* ─────────── распознавание структуры ─────────── */
const RX = {
  tocStart: /^(MÜNDƏRİCAT|СОДЕРЖАНИЕ|CONTENTS|İÇİNDƏKİLƏR)$/i,
  /* части: «FƏSİL 1», «ЧАСТЬ I», «PART III» */
  part: /^(FƏSİL|FƏSIL|ЧАСТЬ|PART)\s*([IVXLC]+|\d+)\b/i,
  chapter: /^(BÖLÜM|Bölüm|bÖLÜM|ГЛАВА|Глава|CHAPTER|Chapter)\s*\d+/,
  /* вводные разделы — только как отдельная строка-заголовок */
  front: /^(GİRİŞ|Giriş|PROLOQ|Proloq|ВВЕДЕНИЕ|Введение|ПРОЛОГ|Пролог|INTRODUCTION|PROLOGUE)\s*$/i,
  tocline: /(…|\.{3,}|\s\d{1,3}\s*$)/
};

/* нормализация для сопоставления названий из оглавления с телом книги */
function norm(s) {
  return String(s).toLowerCase()
    .replace(/[«»"'`.,:;!?()\[\]–—-]/g, ' ')
    .replace(/\s+/g, ' ').trim();
}

/* Список названий глав из оглавления (со страницами/выносками — чистим) */
function tocTitles(paras) {
  const start = paras.findIndex((p) => RX.tocStart.test(p.text));
  if (start < 0) return [];
  const titles = [];
  for (let i = start + 1; i < paras.length; i++) {
    const raw = paras[i].text;
    const isBody = (RX.chapter.test(raw) || RX.front.test(raw)) && !RX.tocline.test(raw) && raw.length < 120;
    if (isBody && titles.length) break;               // началось тело книги
    const clean = raw
      .replace(/[.…\s]*\d{1,3}\s*$/, '')
      .replace(/[.…]{2,}/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
    if (clean.length > 4 && clean.length < 130) titles.push(clean);
  }
  return titles;
}

/* Разбиение тела по названиям из оглавления (первое совпадение после оглавления) */
function splitByToc(body, titles) {
  if (titles.length < 3) return null;
  const idxs = [];
  let from = 0;
  titles.forEach((title) => {
    const n = norm(title);
    const short = n.slice(0, 28);
    for (let i = from; i < body.length; i++) {
      const bn = norm(body[i].text);
      if (bn === n || (short.length > 8 && bn.startsWith(short))) { idxs.push({ i, title }); from = i + 1; return; }
    }
  });
  if (idxs.length < 3) return null;
  return idxs.map((o, k) => ({
    title: o.title,
    paras: body.slice(o.i + 1, k + 1 < idxs.length ? idxs[k + 1].i : body.length)
  }));
}

function buildChapters(paras) {
  /* 1) найти область оглавления и вырезать её */
  let tocFrom = -1, tocTo = -1;
  for (let i = 0; i < paras.length; i++) {
    if (tocFrom < 0 && RX.tocStart.test(paras[i].text)) { tocFrom = i; continue; }
    if (tocFrom >= 0 && i > tocFrom) {
      const p = paras[i];
      const isHead = RX.part.test(p.text) || RX.chapter.test(p.text) || RX.front.test(p.text);
      if (isHead && !RX.tocline.test(p.text)) { tocTo = i; break; }
    }
  }
  const body = paras.slice(tocTo > 0 ? tocTo : 0).filter((p) => !RX.tocline.test(p.text) || p.text.length > 120);

  /* 1б) если в книге есть оглавление — режем по нему (самый надёжный путь).
     Принимаем результат только если он покрывает большинство названий из
     оглавления; иначе переходим к разбору по маркерам в тексте. */
  const titles = tocTitles(paras);
  const byToc = splitByToc(body, titles);
  if (byToc && titles.length && byToc.length >= Math.max(6, titles.length * 0.6)) {
    return byToc.map((ch) => ({ title: ch.title, paras: ch.paras, partTitle: '' }));
  }

  /* 2) разбить на части и главы */
  const parts = [];
  let curPart = null, curCh = null;
  function pushPart(title) { curPart = { title, chapters: [] }; parts.push(curPart); return curPart; }
  function pushCh(title, para) {
    if (!curPart) pushPart('');
    curCh = { title, paras: [], part: curPart };
    curPart.chapters.push(curCh);
    return curCh;
  }

  /* Маркер главы отдельной строкой: «ГЛАВА 1», «CHAPTER 3», «ЧАСТЬ I»,
     «7-ci bölmə» — за ним обычно идёт заголовок капсом. */
  const BARE = /^(ГЛАВА|CHAPTER|BÖLMƏ|BÖLÜM|FƏSİL)\s*([IVXLC]+|\d+)\s*$/i;
  const AZNUM = /^\d+\s*[-–]?\s*(ci|cı|cu|cü)\s+bölmə\b/i;
  let mergeTitle = false;

  body.forEach((p) => {
    const t = p.text;
    const isPart = RX.part.test(t) && t.length < 120;
    const isBare = BARE.test(t);
    const isAzNum = AZNUM.test(t) && t.length < 140;
    const isCh = RX.chapter.test(t) && t.length < 200;
    const isFront = RX.front.test(t) && t.length < 120;
    const isBigHead = p.bold && p.sz >= 32 && t.length < 90 && !/^\d+[.)]/.test(t);

    /* короткий подзаголовок-название сразу после заголовка главы (напр. «LİLİT» / «ЛИЛИТ»)
       дописывается в название главы — проверяется ДО ветки маркеров */
    if (curCh && curCh.paras.length === 0 && curCh.title && t.length < 34 &&
        !/^\d+[.)]/.test(t) && !isPart && !isCh && !isBare && !isAzNum && !isFront && !isBigHead) {
      curCh.title = curCh.title.replace(/\s*\.\s*$/, '') + ' · ' + t;
      return;
    }

    if (isPart) { pushPart(t.replace(/\s+$/, '')); mergeTitle = false; return; }
    if (isBare || isAzNum || isCh || isFront || isBigHead) {
      pushCh(t, p);
      mergeTitle = isBare || isAzNum;   /* следующая строка-капс станет частью названия */
      return;
    }
    /* заголовок капсом после голого маркера: «ГЛАВА 1» + «ВИРУС В ГОЛОВЕ…» */
    if (mergeTitle && curCh && curCh.paras.length === 0 && t.length < 130 && !/[.!?]$/.test(t)) {
      curCh.title = curCh.title + '. ' + t;
      mergeTitle = false;
      return;
    }
    mergeTitle = false;

    if (!curCh) pushCh('', p);
    curCh.paras.push(p);
  });

  /* 3) очистка: убрать пустые главы, склеить короткие */
  const flat = [];
  parts.forEach((pt) => {
    pt.chapters.forEach((ch) => {
      const textLen = ch.paras.reduce((n, p) => n + p.text.length, 0);
      if (textLen < 400) { if (flat.length) { flat[flat.length - 1].paras = flat[flat.length - 1].paras.concat(ch.paras); return; } }
      ch.partTitle = pt.title;
      flat.push(ch);
    });
  });
  return flat;
}

function slugify(s, i, lang) {
  let base = s.toLowerCase()
    .replace(/[əıöüçşğ]/g, (c) => ({ 'ə': 'e', 'ı': 'i', 'ö': 'o', 'ü': 'u', 'ç': 'c', 'ş': 's', 'ğ': 'g' }[c] || c))
    .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 42);
  const prefix = lang === 'ru' ? 'glava' : lang === 'en' ? 'chapter' : 'bolum';
  if (!base || base.length < 3 || /^\d+$/.test(base)) base = prefix + '-' + i;
  return String(i).padStart(2, '0') + '-' + base;
}

function shortLabel(title) {
  const t = String(title).trim();
  const num = (t.match(/^(?:BÖLÜM|Bölüm|ГЛАВА|Глава|CHAPTER|Chapter)\s*([IVXLC]+|\d+)/) || [])[1];
  const name = (t.match(/«([^»]+)»/) || [])[1];
  if (num && name) return (t.slice(0, 2) === 'ГЛ' || t.slice(0, 2) === 'Гл' ? 'Глава ' : 'Bölüm ') + num + ' · «' + name + '»';
  if (num) return (t.slice(0, 2) === 'ГЛ' || t.slice(0, 2) === 'Гл' ? 'Глава ' : 'Bölüm ') + num + ' · ' + t.replace(/^[^.]*\.\s*/, '').slice(0, 34);
  return t.length > 46 ? t.slice(0, 44) + '…' : t;
}

function dnName(title) {
  const t = shortLabel(title);
  return t.length > 26 ? t.slice(0, 24).trim() + "…" : t;
}

function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

/* ─────────── генерация страниц ─────────── */
const TPL = JSON.parse(fs.readFileSync(path.join(__dirname, 'book-template.json'), 'utf8'));

const UI = {
  az: { toc: 'Mündəricat', order: 'Kitabın sifarişi', back: 'Kitablar', prev: 'Əvvəlki', next: 'Növbəti', read: 'Oxu', home: 'Ana səhifə', up: 'Kitab' },
  ru: { toc: 'Содержание', order: 'Заказать книгу', back: 'Книги', prev: 'Предыдущая', next: 'Следующая', read: 'Читать', home: 'Главная', up: 'Книга' },
  en: { toc: 'Contents', order: 'Order the book', back: 'Books', prev: 'Previous', next: 'Next', read: 'Read', home: 'Home', up: 'Book' }
};

function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

/* шапка: подмена бренда книги */
function bodyTop(cfg, lang) {
  return TPL.bodyTop
    .replace(/<div class="hdr-logo">[^<]*<\/div>/, '<div class="hdr-logo">' + cfg.logo + '</div>')
    .replace(/<strong>[^<]*<\/strong>/, '<strong>' + esc(lang.title.toUpperCase()) + '</strong>')
    .replace(/<small>[^<]*<\/small>/, '<small>' + esc(lang.author || cfg.author) + ' · ' + cfg.year + '</small>')
    .replace('data-lang-switch', 'data-lang-switch data-langs="' + cfg.langs.map(function (l) { return l.code; }).join(',') + '"');
}

/* сайдбар: оглавление книги в классовой структуре эталона */
function sidebarHtml(cfg, lang, all, idx, rel) {
  const items = all.map((c, i) =>
    '<div class="nav-item"><a href="' + c.file + '" class="nav-sub-link' + (i === idx ? ' is-active' : '') + '">' +
    '<span class="sub-code">' + c.num + '</span><span class="sub-name">' + esc(shortLabel(c.short)) + '</span></a></div>'
  ).join('\n      ');
  return '<aside class="sidebar" id="sb">\n' +
    '    <div class="sb-hdr"><a class="sb-site" href="https://ragimoff.org/books/" title="Kitablar">← ' + (UI[lang.ui] || UI.az).back + '</a>' +
    '<button class="sb-close" onclick="toggleSb()" aria-label="Bağla">✕</button></div>\n' +
    '    <nav>\n      <div class="nav-item"><a href="' + rel + 'index.html" class="nav-link nav-front">' + (UI[lang.ui] || UI.az).home + '</a></div>\n      ' +
    items + '\n    </nav>\n  </aside>';
}

/* хвост: поисковый индекс книги (ALL_PAGES) + текущая страница */
function tailHtml(all, idx) {
  const pages = JSON.stringify(all.map((c) => ({ slug: c.file.replace(/\.html$/, ''), title: c.short, code: c.num })));
  return TPL.tail
    .replace(/const CURRENT = "[^"]*";/, 'const CURRENT = "' + all[idx].file.replace(/\.html$/, '') + '";')
    .replace(/const ALL_PAGES = \[[\s\S]*?\];/, 'const ALL_PAGES = ' + pages + ';');
}

/* метаданные страницы */
/* стиль оглавления книги (запомнен как канон): компактные пункты, узкая колонка номера */
const TOC_STYLE = '<style>' +
  '.home-hero{padding:16px 0 22px}' +
  '.d-nav{display:flex;align-items:center;justify-content:space-between;gap:.5rem;margin:2.2rem 0 .5rem;padding:.7rem 0 0;border-top:1px solid var(--border)}' +
  '.d-nav a{color:var(--text);text-decoration:none;padding:.35rem .7rem;border-radius:6px;font-family:var(--mono,monospace);font-weight:700;font-size:.95rem;white-space:nowrap;max-width:42%;overflow:hidden;text-overflow:ellipsis}' +
  '.d-nav a:hover{background:var(--bg3);color:var(--gold)}' +
  '.d-nav .up{color:var(--gold);font-family:var(--font);font-weight:600}' +
  '.d-nav .dn-name{color:var(--text2);font-weight:400;font-family:var(--font);font-size:.85rem}' +
  '@media (max-width:640px){.d-nav .dn-name{display:none}}' +
  '.sidebar .nav-sub-link{padding:7px 14px 7px 18px;font-size:12.5px;gap:8px}' +
  '.sidebar .sub-code{flex:0 0 30px;width:30px;font-size:10.5px}' +
  '.sidebar .nav-sub-link.is-active{color:var(--gold);border-left-color:var(--gold);background:var(--gold-bg)}' +
  '</style>';

function headHtml(cfg, lang, title, desc) {
  const LANGS_ATTR = cfg.langs.map(function (l) { return l.code; }).join(',');
  return TPL.head
    .replace('<html ', '<html data-langs="' + LANGS_ATTR + '" ')
    .replace(/<html([^>]*?)lang="[a-z]{2}"/, '<html$1lang="' + lang.code + '"')
    .replace(/<title>[\s\S]*?<\/title>/, '<title>' + esc(title) + ' | ' + esc(lang.title.toUpperCase()) + '</title>')
    .replace(/<meta name="description" content="[^"]*"/, '<meta name="description" content="' + esc(desc) + '"')
    .replace(/<meta property="og:title" content="[^"]*"/, '<meta property="og:title" content="' + esc(title) + '"')
    .replace(/<meta property="og:description" content="[^"]*"/, '<meta property="og:description" content="' + esc(desc) + '"')
    .replace(/<meta property="og:url" content="[^"]*"/, '<meta property="og:url" content="https://ragimoff.org/' + cfg.slug + '/"')
    .replace(/"name":"[^"]*","inLanguage":"[^"]*"/, '"name":"' + esc(cfg.title) + '","inLanguage":"' + lang.code + '"')
    .replace(/"about":"[^"]*"/, '"about":"' + esc(cfg.subtitle || cfg.title) + '"')
    .replace('</head>', TOC_STYLE + '</head>');
}

function chapterPage(cfg, lang, ch, idx, all, rel) {
  const ui = UI[lang.ui] || UI.az;
  const prev = idx > 0 ? all[idx - 1] : null;
  const next = idx < all.length - 1 ? all[idx + 1] : null;
  const body = ch.paras.map((p) => {
    const t = esc(p.text);
    if (p.text.length < 95 && /^\d+(\.\d+)*[.)]?\s/.test(p.text)) return '<h2>' + t + '</h2>';
    if (p.bold && p.sz >= 26 && p.text.length < 95) return '<h2>' + t + '</h2>';
    if (p.bold && p.text.length < 90 && /[:.]$/.test(p.text)) return '<h3>' + t + '</h3>';
    return '<p>' + t + '</p>';
  }).join('\n');

  return headHtml(cfg, lang, ch.short, lang.title + ' — ' + ch.short) +
    '\n</head>\n' + bodyTop(cfg, lang) + sidebarHtml(cfg, lang, all, idx, rel) + TPL.mid + TPL.contentOpen +
    '\n<nav class="crumb"><a href="' + rel + 'index.html">‹ ' + esc(lang.title) + '</a></nav>' +
    '<header class="chap-head"><h1 class="chap-h1"><span class="chap-range">' + ch.num + '</span>' +
    '<span class="chap-title">' + esc(ch.short) + '</span></h1></header>\n' +
    body +
    /* нижняя навигация — как в эталоне: одна строка (.d-nav): ← NN имя · ↑ вверх · имя NN → */
    '\n<nav class="d-nav">' +
    (prev
      ? '<a href="' + prev.file + '">← ' + prev.num + ' <span class="dn-name">' + esc(dnName(prev.short)) + '</span></a>'
      : '<span></span>') +
    '<a class="up" href="' + rel + 'index.html">↑ ' + (ui.up || 'Fəsil') + '</a>' +
    (next
      ? '<a href="' + next.file + '"><span class="dn-name">' + esc(dnName(next.short)) + '</span> ' + next.num + ' →</a>'
      : '<span></span>') +
    '</nav>\n' + tailHtml(all, idx);
}

function indexPage(cfg, lang, all, rel) {
  const ui = UI[lang.ui] || UI.az;
  const cards = all.map((c) =>
    '<a class="ch-disorder" href="' + c.file + '"><span class="ch-code">' + c.num + '</span><span class="ch-name">' + esc(shortLabel(c.short)) + '</span></a>'
  ).join('\n      ');
  const content =
    '\n<div class="home-hero"><h1 class="home-title">' + esc(lang.title.toUpperCase()) + '</h1>' +
    '<p class="sub">' + esc(cfg.subtitle || '') + '</p></div>\n' +
    '<div class="chapter-menu">\n      ' + cards + '\n    </div>\n';
  return headHtml(cfg, lang, lang.title, lang.title + ' — ' + (cfg.subtitle || '')) +
    '\n</head>\n' + bodyTop(cfg, lang) + sidebarHtml(cfg, lang, all, -1, rel) + TPL.mid + TPL.contentOpen +
    content + '\n' + tailHtml(all, 0);
}

/* ─────────── main ─────────── */
const cfgPath = process.argv[2];
const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
const outRoot = path.resolve(cfg.out);
fs.mkdirSync(outRoot, { recursive: true });

/* style.css — копия из эталонной книги */
if (cfg.styleFrom && fs.existsSync(cfg.styleFrom)) {
  fs.copyFileSync(cfg.styleFrom, path.join(outRoot, 'style.css'));
}

let totalPages = 0;
cfg.langs.forEach((lang) => {
  const dir = path.join(outRoot, lang.dir || '');
  fs.mkdirSync(dir, { recursive: true });
  if (cfg.styleFrom && fs.existsSync(cfg.styleFrom)) fs.copyFileSync(cfg.styleFrom, path.join(dir, 'style.css'));
  const paras = paragraphs(lang.file);
  const chapters = buildChapters(paras);
  const used = {};
  const all = chapters.map((ch, i) => {
    const short = (ch.title || '').replace(/\s*\.\s*$/, '').slice(0, 120) || ('Bölmə ' + (i + 1));
    let file = slugify(short, i + 1, lang.code) + '.html';
    while (used[file]) file = file.replace(/\.html$/, '-x.html');
    used[file] = 1;
    return { short, num: String(i + 1).padStart(2, '0'), file, paras: ch.paras, partTitle: ch.partTitle };
  });
  const rel = lang.dir ? '../' : '';
  all.forEach((ch, i) => {
    fs.writeFileSync(path.join(dir, ch.file), chapterPage(cfg, lang, ch, i, all, rel), 'utf8');
    totalPages++;
  });
  fs.writeFileSync(path.join(dir, 'index.html'), indexPage(cfg, lang, all, rel), 'utf8');
  totalPages++;
  console.log(`${lang.code}: глав ${all.length} → ${path.relative(process.cwd(), dir) || '.'}`);
  all.slice(0, 6).forEach((c) => console.log('   · ' + c.file + '  ' + c.short.slice(0, 60)));
});

console.log('всего страниц:', totalPages);
