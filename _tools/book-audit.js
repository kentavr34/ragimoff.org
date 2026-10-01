#!/usr/bin/env node
/* book-audit.js — сплошной аудит страниц КНИГ (books/** + klinik-psixiatriya/**).
 *
 * Статика (Node, без браузера): битые ссылки, пустые href, дубли id, язык текста
 *   против языка каталога, заголовок/тайтл, «пустые» абзацы.
 * Отрисовка (headless Chrome + _tools/book-audit-probe.js): контраст, кегли ролей,
 *   структура меню (группы/ссылки/выпadaние), «пустые полосы», объём текста.
 *
 * Запуск:
 *   python -m http.server 8765 --bind 127.0.0.1 -d .     # из корня репозитория
 *   node _tools/book-audit.js --out D:/audit --tag before
 *   node _tools/book-audit.js --out D:/audit --tag after --pages books/virus-viny/index.html
 *
 * Пишет: <out>/book_audit_<tag>.tsv и <out>/book_audit_<tag>.json
 * Строка TSV: книга | язык | страница | класс | причина | было | стало | детали
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { execFile } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const CHROME = process.env.AUDIT_CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PORT = process.env.AUDIT_PORT || '8765';
const PROBE = fs.readFileSync(path.join(__dirname, 'book-audit-probe.js'), 'utf8');

const argv = process.argv.slice(2);
function arg(name, def) {
  const i = argv.indexOf('--' + name);
  return i === -1 ? def : argv[i + 1];
}
const OUT = arg('out', 'D:/Документы/ZFreud/_align/book_audit');
const TAG = arg('tag', 'audit');
const WIDTH = parseInt(arg('width', '1440'), 10);
const JOBS = parseInt(arg('jobs', '6'), 10);
const STATIC_ONLY = argv.includes('--static-only');
const PAGES_ARG = (function () {
  const i = argv.indexOf('--pages');
  if (i === -1) return null;
  const out = [];
  for (let j = i + 1; j < argv.length && argv[j][0] !== '-'; j++) out.push(argv[j]);
  return out;
})();
/* список страниц файлом (по строке) — длинный список не влезает в командную строку Windows */
const PAGES_FILE = arg('pages-file', null);
const LIMIT = parseInt(arg('limit', '0'), 10);
const SKIP_DIRS = ['.git', 'node_modules', 'test', '__pycache__'];

/* ─────────── список страниц книг ─────────── */
function listPages() {
  if (PAGES_FILE) {
    return fs.readFileSync(PAGES_FILE, 'utf8').split(/\r?\n/).map(s => s.trim()).filter(Boolean);
  }
  if (PAGES_ARG) return PAGES_ARG;
  const out = [];
  function scan(dir, rel, depth) {
    for (const name of fs.readdirSync(dir).sort()) {
      const full = path.join(dir, name);
      const st = fs.statSync(full);
      if (st.isDirectory()) {
        if (SKIP_DIRS.includes(name) || name.startsWith('.') || name.includes('.bak')) continue;
        if (depth > 3) continue;
        scan(full, rel + name + '/', depth + 1);
      } else if (name.endsWith('.html') && !name.startsWith('_') && !name.startsWith('_shot')) {
        out.push(rel + name);
      }
    }
  }
  scan(path.join(ROOT, 'books'), 'books/', 0);
  for (const name of fs.readdirSync(path.join(ROOT, 'klinik-psixiatriya')).sort()) {
    const full = path.join(ROOT, 'klinik-psixiatriya', name);
    const st = fs.statSync(full);
    if (st.isDirectory()) {
      if (name === 'test' || name.includes('.bak')) continue;
      scan(full, 'klinik-psixiatriya/' + name + '/', 1);
    } else if (name.endsWith('.html')) {
      out.push('klinik-psixiatriya/' + name);
    }
  }
  return out;
}

/* ─────────── статические проверки ─────────── */
function langOf(rel) {
  const parts = rel.split('/');
  for (const L of ['ru', 'en', 'tr']) if (parts.includes(L)) return L;
  return 'az';
}
function bookOf(rel) {
  const parts = rel.split('/');
  if (parts[0] === 'klinik-psixiatriya') return 'klinik';
  if (parts[0] === 'books') {
    if (parts.length === 2) return 'gallery';                       /* books/index.html */
    if (parts.length === 3 && (parts[1] === 'ru' || parts[1] === 'en')) return 'gallery';
    return parts[1];
  }
  return parts[0];
}
function staticChecks(rel) {
  const findings = [];
  const abs = path.join(ROOT, rel);
  const html = fs.readFileSync(abs, 'utf8');
  const lang = langOf(rel);
  const dir = path.dirname(abs);
  const push = (cls, reason, was, became, extra) =>
    findings.push({ cls, reason, was, became, extra: extra || null });

  /* битые относительные ссылки и якоря */
  const hrefs = [...html.matchAll(/href="([^"]+)"/g)].map(m => m[1]);
  const ids = new Set([...html.matchAll(/\sid="([^"]+)"/g)].map(m => m[1]));
  let broken = 0, brokenList = [];
  let selfAnchor = 0, selfList = [];
  for (const h of hrefs) {
    if (/^(https?:|mailto:|tel:|javascript:|#)/.test(h)) {
      if (h.startsWith('#') && h.length > 1 && !ids.has(h.slice(1))) { selfAnchor++; if (selfList.length < 5) selfList.push(h); }
      continue;
    }
    const clean = h.split('#')[0].split('?')[0];
    if (!clean) continue;
    const target = clean.startsWith('/')
      ? path.join(ROOT, clean.slice(1))
      : path.join(dir, clean);
    if (!fs.existsSync(target)) { broken++; if (brokenList.length < 8) brokenList.push(h); }
  }
  if (broken) push('ссылки', 'битая относительная ссылка', broken + ' шт.', 'ссылка на существующий файл', brokenList.join(' '));
  if (selfAnchor) push('ссылки', 'ссылка на несуществующий якорь', selfAnchor + ' шт.', 'якорь существует', selfList.join(' '));

  /* дубли id */
  const allIds = [...html.matchAll(/\sid="([^"]+)"/g)].map(m => m[1]);
  const dup = allIds.filter((v, i) => allIds.indexOf(v) !== i);
  if (dup.length) push('ссылки', 'дублирующийся id', [...new Set(dup)].join(' '), 'id уникален', null);

  /* пустые href */
  const emptyHref = (html.match(/href=""/g) || []).length + (html.match(/href="#"/g) || []).length;
  if (emptyHref) push('ссылки', 'пустая ссылка (href="" или "#")', emptyHref + ' шт.', 'осмысленный адрес', null);

  /* тайтл и h1 */
  const t = (html.match(/<title>([\s\S]*?)<\/title>/) || [])[1];
  if (!t || !t.trim()) push('пустые страницы', 'нет <title>', '(пусто)', 'заголовок страницы', null);
  const h1n = (html.match(/<h1\b/g) || []).length;
  if (h1n === 0) push('структура страницы', 'нет h1', '0', 'один h1 на страницу', null);
  if (h1n > 1) push('структура страницы', 'больше одного h1', h1n + ' шт.', 'один', null);

  /* canonical чужой книги */
  const canon = (html.match(/<link rel="canonical" href="([^"]*)"/) || [])[1] || '';
  const book = bookOf(rel);
  const canonBook = canon.includes('/klinik-psixiatriya') ? 'klinik'
    : (canon.match(/\/books\/([^\/"]+)/) || [])[1] || null;
  if (canon && canonBook && canonBook !== book && !(book === 'klinik' && canonBook === 'klinik')) {
    push('ссылки', 'canonical ведёт в другую книгу', canon, 'canonical своей страницы', book + ' → ' + canonBook);
  }

  /* языковые утечки: по доле алфавита, а не по одному знаку
     (цитата на русском внутри азербайджанской страницы — не утечка; страница,
     где кириллица dominates — утечка) */
  const visible = html.replace(/<script[\s\S]*?<\/script>/g, ' ')
    .replace(/<style[\s\S]*?<\/style>/g, ' ')
    .replace(/<!--[\s\S]*?-->/g, ' ')
    .replace(/<[^>]+>/g, ' ');
  const cyr = (visible.match(/[А-Яа-яЁё]/g) || []).length;
  const lat = (visible.match(/[A-Za-zÀ-ÿƏəĞğİıÖöŞşÜüÇç]/g) || []).length;
  const cyrShare = (cyr + lat) ? cyr / (cyr + lat) : 0;
  if ((lang === 'az' || lang === 'en' || lang === 'tr') && cyrShare > 0.3) {
    push('языковые утечки', 'текст страницы не на языке каталога (кириллица)',
      Math.round(cyrShare * 100) + '% кириллицы (' + cyr + ' знаков)', '≤ 5%', null);
  } else if ((lang === 'az' || lang === 'en' || lang === 'tr') && cyr > 120 && cyrShare > 0.05) {
    push('языковые утечки', 'крупные вкрапления чужого алфавита (проверить)',
      cyr + ' знаков кириллицы (' + Math.round(cyrShare * 100) + '%)', '≤ 5%', null);
  }
  const azWords = (visible.match(/\b(və|üçün|ilə|haqqında|səhifə|kitab)\b/gi) || []).length;
  if ((lang === 'ru' || lang === 'en') && azWords > 3) {
    push('языковые утечки', 'азербайджанские слова в не-азербайджанском тексте', azWords + ' слов', '0', null);
  }
  /* атрибут lang против языка каталога */
  const htmlLang = (html.match(/<html[^>]*\slang="([^"]*)"/) || [])[1] || '';
  if (htmlLang && !htmlLang.toLowerCase().startsWith(lang)) {
    push('языковые утечки', '<html lang> не совпадает с языком каталога', 'lang="' + htmlLang + '"', 'lang="' + lang + '"', null);
  }
  /* азербайджанские служебные подписи в aria (по реестру должно быть на языке страницы) */
  const ariaAz = [...html.matchAll(/aria-label="([^"]*)"/g)].map(m => m[1])
    .filter(v => /Aç \/ bağla|Naviqasiya|Futermenü|Fəsil keçidi|Bağla/.test(v));
  if ((lang === 'ru' || lang === 'en' || lang === 'tr') && ariaAz.length) {
    push('языковые утечки', 'служебная подпись (aria-label) чужого языка', ariaAz.length + ' шт.: ' + [...new Set(ariaAz)].join(', '), 'язык страницы', null);
  }
  /* латиница в названиях, где реестр требует кириллицу, и наоборот — грубо, по буквам-двойникам */
  const mixed = (visible.match(/[А-Яа-яЁё][A-Za-z]|[A-Za-z][А-Яа-яЁё]/g) || []).length;
  if (mixed > 20) push('языковые утечки', 'смешанные алфавиты в тексте', mixed + ' переходов', 'по языку страницы', null);

  /* заголовки разделов книги в тексте идут КАПСОМ целым абзацем */
  const capsHeads = [...html.matchAll(/<h([234])[^>]*>([^<]{12,})<\/h\1>/g)]
    .filter(m => {
      const s = m[2].trim();
      const letters = s.replace(/[^A-Za-zÀ-ÿА-Яа-яЁёƏəĞğİıÖöŞşÜüÇç]/g, '');
      return letters.length > 8 && letters === letters.toUpperCase();
    });
  if (capsHeads.length) push('типографика', 'заголовок раздела набран капсом', capsHeads.length + ' шт.: ' + capsHeads.slice(0, 3).map(m => m[2].trim().slice(0, 24)).join(' | '), 'обычный регистр', null);

  /* «пустые» абзацы-заглушки (кроме служебного <p class="bk-chead__top"> с чертой) */
  const filler = (html.match(/<p[^>]*>\s*(?:&nbsp;|\s|<\/p>|<br\s*\/?>)+\s*<\/p>/g) || [])
    .filter(s => !/bk-chead__top/.test(s)).length;
  if (filler) push('отступы', 'пустые абзацы-заполнители', filler + ' шт.', '0', null);

  /* пустые пункты меню: строка без текста и без href */
  const emptyRows = (html.match(/<a class="[^"]*bk-row[^"]*"[^>]*>\s*<span class="bk-row__n">\s*<\/span>\s*<span class="bk-row__t">\s*<\/span>\s*<\/a>/g) || []).length
    + (html.match(/<span class="[^"]*bk-row--sub[^"]*">\s*<span class="bk-row__n">\s*<\/span>\s*<span class="bk-row__t">\s*<\/span>\s*<\/span>/g) || []).length;
  if (emptyRows) push('структура меню', 'пустой пункт меню (без текста)', emptyRows + ' шт.', '0', null);

  return findings;
}

/* ─────────── отрисовка ─────────── */
function chrome(rel, page, cb) {
  const src = path.join(ROOT, rel);
  const tmp = path.join(path.dirname(src), '_ba.' + path.basename(src));
  let html = fs.readFileSync(src, 'utf8');
  const inject = '<script>' + PROBE + '</script>';
  html = /<\/body>/i.test(html) ? html.replace(/<\/body>/i, inject + '</body>') : html + inject;
  try { fs.writeFileSync(tmp, html, 'utf8'); } catch (e) { cb(null); return; }
  const relTmp = path.relative(ROOT, tmp).split(path.sep).join('/');
  const userDir = 'D:/ragimoff-tmp/book-audit-' + process.pid + '-' + Math.random().toString(36).slice(2, 7);
  execFile(CHROME, ['--headless=new', '--disable-gpu', '--no-sandbox', '--disable-extensions',
    '--lang=ru', '--user-data-dir=' + userDir, '--virtual-time-budget=5000', '--blink-settings=imagesEnabled=false',
    '--window-size=' + WIDTH + ',1200', '--dump-dom',
    'http://127.0.0.1:' + PORT + '/' + encodeURI(relTmp)], { timeout: 90000, maxBuffer: 64 * 1024 * 1024 },
    function (err, stdout) {
      try { fs.rmSync(userDir, { recursive: true, force: true }); } catch (e) {}
      try { fs.unlinkSync(tmp); } catch (e) {}
      const html2 = String(stdout || '');
      const m = html2.match(/BOOK-AUDIT-JSON:([\s\S]*?)<\/title>/);
      if (!m) { cb(null); return; }
      let data = null;
      try { data = JSON.parse(m[1]); } catch (e) { cb(null); return; }
      cb(data);
    });
}

(async function () {
  fs.mkdirSync(OUT, { recursive: true });
  let pages = listPages();
  if (LIMIT) pages = pages.slice(0, LIMIT);
  const rows = [];
  const json = { tag: TAG, width: WIDTH, pages: {} };

  /* статика — синхронно и быстро */
  for (const rel of pages) {
    const book = bookOf(rel), lang = langOf(rel);
    for (const f of staticChecks(rel)) {
      rows.push([book, lang, rel, f.cls, f.reason, f.was, f.became, f.extra || ''].join('\t'));
    }
    json.pages[rel] = { static: (json.pages[rel] || {}).static || [] };
  }

  if (!STATIC_ONLY) {
    let i = 0, done = 0;
    await Promise.all(new Array(Math.min(JOBS, pages.length)).fill(0).map(async function () {
      while (true) {
        const k = i++;
        if (k >= pages.length) break;
        const rel = pages[k];
        await new Promise(function (resolve) {
          chrome(rel, rel, function (data) {
            done++;
            if (done % 50 === 0) process.stderr.write('  ... ' + done + '/' + pages.length + '\n');
            if (data) {
              json.pages[rel] = Object.assign(json.pages[rel] || {}, data);
              const lang = langOf(rel), book = bookOf(rel);
              for (const f of (data.findings || [])) {
                const extra = f.extra ? (typeof f.extra === 'string' ? f.extra : JSON.stringify(f.extra).slice(0, 400)) : '';
                rows.push([book, lang, rel, f.cls, f.reason, f.was, f.became, extra].join('\t'));
              }
            }
            resolve();
          });
        });
      }
    }));
  }

  const header = ['книга', 'язык', 'страница', 'класс', 'причина', 'было', 'стало', 'детали'].join('\t');
  const tsv = path.join(OUT, 'book_audit_' + TAG + '.tsv');
  const jsf = path.join(OUT, 'book_audit_' + TAG + '.json');
  fs.writeFileSync(tsv, header + '\n' + rows.join('\n') + '\n', 'utf8');
  fs.writeFileSync(jsf, JSON.stringify(json, null, 1), 'utf8');
  console.log('страниц: ' + pages.length + '; строк аудита: ' + rows.length);
  console.log('-> ' + tsv);
})();
