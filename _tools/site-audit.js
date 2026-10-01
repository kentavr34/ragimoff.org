#!/usr/bin/env node
/* site-audit.js — сплошной аудит страниц сайта (корень + ru/ + en/).
 *
 * Две половины:
 *   1) статика — Node читает HTML: alt у картинок, битые/пустые ссылки,
 *      дубли id, повтор H1, двойные пробелы, «слипшиеся» слова, пустые блоки;
 *   2) отрисовка — headless Chrome (как _tools/hero-measure.js) с пробником
 *      _tools/site-audit-probe.js: гориз. прокрутка, вылет за вьюпорт, роль
 *      гарнитуры по факту, контраст, наложения текста, светлые пятна, кнопки.
 *
 * Запуск:
 *   python -m http.server 8765 --bind 127.0.0.1 -d .      # из корня репозитория
 *   node _tools/site-audit.js --out D:/audit --width 1440
 *   node _tools/site-audit.js --out D:/audit --width 390 --jobs 6
 *   node _tools/site-audit.js --out D:/audit --pages tehsil.html ru/tehsil.html
 *   node _tools/site-audit.js --out D:/audit --static-only
 *
 * Пишет: <out>/site_audit_<width>.tsv, <out>/site_audit_raw_<width>.json
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { execFile } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const CHROME = process.env.AUDIT_CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PORT = process.env.AUDIT_PORT || '8765';
const PROBE = fs.readFileSync(path.join(__dirname, 'site-audit-probe.js'), 'utf8');
const TEXT_PROBE = fs.readFileSync(path.join(__dirname, 'site-text-probe.js'), 'utf8');
const SKIP_DIRS = ['books', 'klinik-psixiatriya', 'test', 'node_modules', '.git', 'backend', '_supplements', 'favicons', 'data', 'images'];

/* ───────────────────────── аргументы ───────────────────────── */
const argv = process.argv.slice(2);
function arg(name, def) {
  const i = argv.indexOf('--' + name);
  return i === -1 ? def : argv[i + 1];
}
const OUT = arg('out', 'D:/Документы/ZFreud/_align/site_audit');
const WIDTHS = String(arg('width', '1440')).split(',').map(function (s) { return parseInt(s, 10); });
const JOBS = parseInt(arg('jobs', '5'), 10);
const STATIC_ONLY = argv.includes('--static-only');
const TEXT_ONLY = argv.includes('--text-only') || argv.includes('--text');
const ONLY_STATIC_PAGES = arg('pages', null);
const LIMIT = parseInt(arg('limit', '0'), 10);
/* ширины, где хватает дешёвого режима (обычно телефон) */
const LIGHT_WIDTHS = String(arg('light-width', '')).split(',').filter(Boolean).map(function (s) { return parseInt(s, 10); });

/* ───────────────────────── список страниц ───────────────────────── */
function listPages() {
  if (ONLY_STATIC_PAGES) return ONLY_STATIC_PAGES.split(',').map(function (s) { return s.trim(); }).filter(Boolean);
  const out = [];
  function scan(dir, prefix) {
    for (const name of fs.readdirSync(dir).sort()) {
      const full = path.join(dir, name);
      const st = fs.statSync(full);
      if (st.isDirectory()) {
        if (SKIP_DIRS.includes(name) || name.startsWith('.') || name.startsWith('_')) continue;
        if (prefix !== '') continue;             /* только корень, ru/, en/ */
        scan(full, name + '/');
      } else if (name.endsWith('.html') && !name.startsWith('_')) {
        /* _a.* — временные копии со вставленным пробником: если предыдущий
           прогон оборвался, они остались и попадали бы в список страниц */
        out.push(prefix + name);
      }
    }
  }
  scan(ROOT, '');
  return LIMIT ? out.slice(0, LIMIT) : out;
}

/* ───────────────────────── статические проверки ───────────────────────── */
const RE_SCRIPT = /<(script|style)\b[^>]*>[\s\S]*?<\/\1>/gi;
const RE_TAG = /<[^>]+>/g;
const RE_COMMENT = /<!--[\s\S]*?-->/g;

function visibleText(html) {
  let s = html.replace(RE_SCRIPT, ' ').replace(RE_COMMENT, ' ');
  /* сохраняем границы блоков как пробел */
  s = s.replace(/<\/(p|div|li|h[1-6]|td|th|span|a|section|article|figcaption|blockquote|strong|em|b|i|br)>/gi, ' ');
  s = s.replace(RE_TAG, ' ');
  s = s.replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&laquo;/g, '«').replace(/&raquo;/g, '»')
    .replace(/&mdash;/g, '—').replace(/&ndash;/g, '–').replace(/&quot;/g, '"').replace(/&#39;/g, "'")
    .replace(/&times;/g, '×').replace(/&hellip;/g, '…').replace(/&rsquo;/g, '’').replace(/&lsquo;/g, '‘');
  s = s.replace(/&#\d+;/g, ' ').replace(/&[a-z]+;/gi, ' ');
  return s;
}
function decodeEntities(s) {
  return String(s).replace(/&amp;/g, '&').replace(/&laquo;/g, '«').replace(/&raquo;/g, '»')
    .replace(/&mdash;/g, '—').replace(/&nbsp;/g, ' ').replace(/&quot;/g, '"').replace(/&#39;/g, "'")
    .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&times;/g, '×').replace(/&hellip;/g, '…');
}

function staticChecks(rel, html) {
  const rows = [];
  const add = (type, desc, was) => rows.push({ page: rel, type, desc, was: was == null ? '' : was, became: '' });
  const pageDir0 = path.posix.dirname(rel);

  /* 1. img без alt + проверка, что файл картинки вообще есть (надёжнее
     рантайма: ленивые картинки браузер не грузит и naturalWidth = 0) */
  const imgs = html.match(/<img\b[^>]*>/gi) || [];
  imgs.forEach(function (tag) {
    const src = (tag.match(/src\s*=\s*["']([^"']*)["']/i) || [])[1] || '';
    if (!/\balt\s*=/.test(tag)) add('img-alt', 'изображение без alt', src);
    if (src && !/^(https?:|data:|\/\/)/i.test(src)) {
      const relPath = src.startsWith('/') ? src.slice(1) : path.posix.normalize(path.posix.join(pageDir0 === '.' ? '' : pageDir0, decodeURIComponent(src)));
      if (!fs.existsSync(path.join(ROOT, relPath))) add('media', 'файл картинки не найден', src);
    }
  });

  /* 2. пустые/битые ссылки */
  const links = html.match(/<a\b[^>]*>/gi) || [];
  const ids = new Set();
  (html.match(/\bid\s*=\s*["']([^"']+)["']/gi) || []).forEach(function (m) {
    ids.add(m.replace(/^id\s*=\s*["']|["']$/gi, ''));
  });
  const pageDir = path.posix.dirname(rel);
  links.forEach(function (tag) {
    const m = tag.match(/href\s*=\s*["']([^"']*)["']/i);
    if (!m) { add('link', 'ссылка без href', tag.slice(0, 60)); return; }
    let href = m[1].trim();
    if (href === '' || href === '#') { add('link', 'пустая ссылка (href="' + href + '")', tag.slice(0, 70)); return; }
    if (/^(mailto:|tel:|javascript:|https?:|data:|\/\/)/i.test(href)) return;
    let file = href, frag = '';
    const h = href.indexOf('#');
    if (h !== -1) { file = href.slice(0, h); frag = href.slice(h + 1); }
    file = decodeURIComponent(file);
    if (file === '') {
      if (frag && !ids.has(frag)) add('link', 'якорь #' + frag + ' не найден на странице', href);
      return;
    }
    const relPath = file.startsWith('/') ? file.slice(1) : path.posix.normalize(path.posix.join(pageDir === '.' ? '' : pageDir, file));
    const abs = path.join(ROOT, relPath);
    if (!fs.existsSync(abs)) { add('link', 'ссылка ведёт на несуществующий файл', href); return; }
    if (frag && /\.html?$/i.test(relPath)) {
      const target = fs.readFileSync(abs, 'utf8');
      const re = new RegExp('id\\s*=\\s*["\']' + frag.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '["\']');
      if (!re.test(target)) add('link', 'якорь #' + frag + ' не найден в ' + relPath, href);
    }
  });

  /* 3. дубли id */
  const idCount = {};
  (html.match(/\bid\s*=\s*["']([^"']+)["']/gi) || []).forEach(function (m) {
    const v = m.replace(/^id\s*=\s*["']|["']$/gi, '');
    idCount[v] = (idCount[v] || 0) + 1;
  });
  Object.keys(idCount).forEach(function (k) { if (idCount[k] > 1) add('dup-id', 'дубль id обновлён в ' + k, 'x' + idCount[k]); });

  /* 4. H1 */
  const h1n = (html.match(/<h1\b/gi) || []).length;
  if (h1n === 0) add('headings', 'на странице нет H1', '0');
  else if (h1n > 1) add('headings', 'несколько H1 на странице', 'x' + h1n);

  /* 5. двойные пробелы внутри одного текстового узла (в отрисовке они
     схлопываются, поэтому шум от отступов разметки здесь не считается) */
  const noCode = html.replace(RE_SCRIPT, ' ').replace(RE_COMMENT, ' ');
  /* 4b. HTML-сущности в верхнем регистре: валидны только строчные, иначе
     браузер печатает «&MIDDOT;» прямо в тексте (аудит 30.09.2026, ru/en
     enurez.html — так и висело в бейдже героя) */
  (noCode.match(/&[A-Z]{2,10};/g) || []).forEach(function (e) {
    add('html-entity', 'HTML-сущность в верхнем регистре — печатается как есть', e);
  });
  const dbl = [];
  noCode.split(/<[^>]*>/).forEach(function (chunk) {
    const parts = chunk.match(/[^\s] {2,}[^\s]/g);
    if (parts) parts.forEach(function (p) { dbl.push(p.replace(/ {2,}/, '··')); });
  });
  if (dbl.length) add('text-spacing', 'двойные пробелы в тексте', dbl.length + ' шт, напр. «' + dbl.slice(0, 3).join('», «').slice(0, 60) + '»');

  /* 6. слипшиеся слова: строчная + заглавная без разделителя, вне брендов */
  const BRANDS = /(WhatsApp|YouTube|TikTok|PowerPoint|LinkedIn|iPhone|iPad|macOS|iOS|WiFi|GitHub|PayPal|Zoom|Neuro|CBT|EMDR|IPAS|BPA|RAGIMOFF|DSM|ICD|XBT|MKБ|BirBank|TamKart|BolKart|WorldKart|NavPress|BetterHelp|Talkspace|Toastmasters|Gottman|Stark|Walker|Bowlby|Ainsworth)/;
  const text = visibleText(html);
  const stuck = [];
  const reStuck = /([a-zəüöğışç])([A-ZƏÜÖĞİŞÇ][a-zəüöğışç])/g;
  let mm;
  while ((mm = reStuck.exec(text)) !== null) {
    const w = text.slice(Math.max(0, mm.index - 16), mm.index + 24).trim();
    if (/[-–/\d]/.test(w) || BRANDS.test(w)) continue;
    stuck.push(w);
  }
  if (stuck.length) add('text-spacing?', 'возможные слипшиеся слова (проверить глазами)', stuck.slice(0, 3).join(' | '));

  return rows;
}

/* ───────────────────────── прогон Chrome ───────────────────────── */
/* Локальный кэш Google Fonts (см. _tools/font-cache-server.js): с этой машины
   fonts.googleapis.com отвечает ~8 секунд, и замер одной страницы выходил
   3 минуты (обход 171 страницы — три часа). При AUDIT_FONTCACHE=1 ссылки в
   копии страницы заменяются на локальный сервер 127.0.0.1:8776. */
const crypto = require('crypto');
function fcHash(u) { return crypto.createHash('md5').update(u).digest('hex'); }
function rewriteFonts(html) {
  if (!process.env.AUDIT_FONTCACHE) return html;
  const P = process.env.AUDIT_FONTCACHE_PORT || '8776';
  html = html.replace(/https:\/\/fonts\.googleapis\.com\/css2\?[^"'`)\s<>]+/g, function (u) {
    return 'http://127.0.0.1:' + P + '/fc/' + fcHash(u.replace(/&amp;/g, '&')) + '.css';
  });
  html = html.replace(/https:\/\/fonts\.gstatic\.com\/[^"'`)\s<>)]+/g, function (u) {
    return 'http://127.0.0.1:' + P + '/fc/' + fcHash(u) + '.woff2';
  });
  return html;
}

function withProbe(rel, probeSrc, prefix) {
  const src = path.join(ROOT, rel);
  const dir = path.dirname(src);
  const tmp = path.join(dir, '_a.' + path.basename(src));
  let html = rewriteFonts(fs.readFileSync(src, 'utf8'));
  let probe = (prefix || '') + (probeSrc || PROBE);
  /* текст страницы снимаем тем же прогоном: innerText дешёв, а грамматика
     потом проверяется по отрисованному, а не по разметке */
  if (!probeSrc) probe += ';' + TEXT_PROBE;
  if (/<\/body>/i.test(html)) html = html.replace(/<\/body>/i, '<script>' + probe + '</script></body>');
  else html += '<script>' + probe + '</script>';
  fs.writeFileSync(tmp, html, 'utf8');
  return path.relative(ROOT, tmp).replace(/\\/g, '/');
}

/* Chrome запускается АСИНХРОННО: execFileSync блокирует цикл событий и
   превращает всех воркеров в один последовательный поток. */
function chromeDump(args) {
  return new Promise(function (resolve) {
    execFile(CHROME, args, { encoding: 'utf8', maxBuffer: 1 << 28, timeout: 120000 },
      function (err, stdout) { resolve(stdout || ''); });
  });
}

/* Аргументы виртуального времени: по умолчанию 9000 мс, AUDIT_VTB=off снимает
   бюджет вовсе (Chrome тогда отдаёт DOM сразу после load и +300 мс зонда). */
function vtbArgs() {
  const v = process.env.AUDIT_VTB;
  return (v === 'off' || v === '0') ? [] : ['--virtual-time-budget=' + (v || '9000')];
}

async function measure(rel, width, job, probeSrc, marker, prefix) {
  const relTmp = withProbe(rel, probeSrc, prefix);
  const url = 'http://127.0.0.1:' + PORT + '/' + encodeURI(relTmp);
  const userDir = 'D:/ragimoff-tmp/audit-' + process.pid + '-' + job + '-' + Math.random().toString(36).slice(2, 7);
  let dom = '';
  try {
    dom = await chromeDump([
      '--headless=new', '--disable-gpu', '--no-sandbox', '--disable-extensions',
      '--lang=az', '--accept-lang=az',
      '--user-data-dir=' + userDir,
      /* ipapi.co — заглушка: shared.js на каждой странице делает внешний
         запрос геолокации, и виртуальное время ждёт его (замер одной
         страницы выходил 3 минуты вместо секунд). Приём взят из
         _tools/hero-survey.js. */
      '--host-resolver-rules=MAP ipapi.co 127.0.0.1:9',
      /* Бюджет виртуального времени настраивается, а AUDIT_VTB=off его
         снимает. С бюджетом Chrome на этой машине держит страницу ~2 минуты
         (виртуальные часы стоят, пока висят сетевые задачи), без него —
         ~7 секунд; зонд при снятом бюджете фиксирует состояние по load и
         через 300 мс (см. site-audit-probe.js). */
      '--window-size=' + width + ',1400',
      '--force-device-scale-factor=1',
      '--dump-dom', url
    ].concat(vtbArgs()));
  } finally {
    try { fs.unlinkSync(path.join(ROOT, relTmp)); } catch (e) {}
    try { fs.rmSync(userDir, { recursive: true, force: true }); } catch (e) {}
  }
  if (marker === 'TEXT-PROBE') {
    const tm = dom.match(/<pre id="__audit_text" style="[^"]*">([\s\S]*?)<\/pre>/);
    if (!tm) return { file: rel, width: width, error: 'no __audit_text', title: (dom.match(/<title>([\s\S]*?)<\/title>/) || [])[1] };
    const text = tm[1].replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"')
      .replace(/&#39;/g, "'").replace(/&nbsp;/g, '\u00a0').replace(/&amp;/g, '&');
    return { file: rel, width: width, text: text };
  }
  const tm = dom.match(/<pre id="__audit_text" style="[^"]*">([\s\S]*?)<\/pre>/);
  const text = tm ? tm[1].replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'").replace(/&nbsp;/g, '\u00a0').replace(/&amp;/g, '&') : null;

  const m = dom.match(/AUDIT-JSON:(\{[\s\S]*?\})<\/title>/);
  if (!m) {
    const t = dom.match(/<title>([\s\S]*?)<\/title>/);
    return { file: rel, width: width, error: 'no AUDIT-JSON', title: t ? t[1].slice(0, 80) : '', text: text };
  }
  try {
    const data = JSON.parse(m[1]);
    data.file = rel; data.width = width; data.text = text;
    return data;
  } catch (e) {
    return { file: rel, width: width, error: 'bad json', text: text };
  }
}

/* ───────────────────────── TSV из замеров ───────────────────────── */
const RE_MUTE = /rgba?\(242,\s*237,\s*227,\s*0?\.5\)|rgba?\(255,\s*255,\s*255,\s*0?\.5\)/;

function rowsFromMeasure(d) {
  const rows = [];
  const add = (type, desc, was) => rows.push({ page: d.file, type, desc, was, became: '' });
  if (d.error) { add('measure', 'страница не замерилась: ' + d.error + (d.title ? ' (' + d.title + ')' : ''), ''); return rows; }

  if (d.hScroll) add('overflow', 'горизонтальная прокрутка страницы', 'scrollW=' + d.scrollW + ' > ' + d.cw + ' (maxRight=' + d.maxRight + ' @ ' + d.maxRightSel + ')');
  (d.overflow || []).forEach(function (o) {
    add('overflow', 'элемент выходит за вьюпорт: ' + o.sel + ' [' + o.cls + ']', 'right=' + o.right + ' left=' + o.left + ' w=' + o.w + ' «' + o.text + '»');
  });
  (d.fonts || []).forEach(function (f) {
    add('font-role', (f.exp === 'read(no-uppercase)' ? 'лид набран капителью' : 'роль «' + f.exp + '», отрисовано «' + f.got + '» (' + f.fam + ')') + ': ' + f.sel + ' [' + f.cls + ']', f.size + 'px/' + f.weight + '/' + f.transform + ' «' + f.text + '»');
  });
  (d.contrast || []).forEach(function (c) {
    /* приглушённый токен (--mute) — системное решение, не дефект страницы */
    const type = RE_MUTE.test(c.color) ? 'contrast-token' : 'contrast';
    add(type, 'контраст ' + c.ratio + ':1 < ' + c.need + ':1 — ' + c.sel + ' [' + c.cls + ']', c.color + ' ' + c.size + 'px/' + c.weight + ' «' + c.text + '»');
  });
  (d.media || []).forEach(function (m) {
    add('media', m.kind === 'no-alt' ? 'картинка без alt' : m.kind === 'empty-alt' ? 'крупная картинка с пустым alt' : 'битая картинка (naturalWidth=0)', m.src + ' [' + m.w + 'x' + m.h + ']');
  });
  (d.empty || []).forEach(function (e) { add('empty-block', 'пустой блок без текста и медиа: ' + e.sel, 'h=' + e.h); });
  (Array.isArray(d.light) ? d.light : []).forEach(function (l) { add('light-spot', 'светлое пятно в тёмном шаблоне: ' + l.sel, l.bg + ' area=' + l.area); });
  (d.overlaps || []).forEach(function (o) { add('overlap', 'наложение текста: ' + o.a + ' ↔ ' + o.b, 'k=' + o.k + ' «' + o.at + '» / «' + o.bt + '»'); });
  /* кнопки одного класса — одной высоты (иначе «кнопки разных размеров») */
  if (d.btnList && d.btnList.length) {
    const byCls = {};
    d.btnList.forEach(function (b) { (byCls[b.cls] = byCls[b.cls] || []).push(b); });
    Object.keys(byCls).forEach(function (cls) {
      const hs = byCls[cls].map(function (b) { return b.h; });
      const lo = Math.min.apply(null, hs), hi = Math.max.apply(null, hs);
      if (hi - lo > 2) add('button-size', 'кнопки одного класса разной высоты: ' + cls, 'h=' + lo + '…' + hi + ' («' + byCls[cls][0].text + '»)');
    });
  }
  if (d.hero) {
    const h = d.hero;
    if (d.w > 860) {
      if (h.top !== null && Math.abs(h.top - 50) > 2) add('hero', 'верх блока → верх фото ≠ 50', String(h.top));
      if (h.bottom !== null && Math.abs(h.bottom) > 2) add('hero', 'низ фото → низ блока ≠ 0', String(h.bottom));
      if (h.badgeTop !== null && Math.abs(h.badgeTop - 88) > 3) add('hero', 'верх блока → метка ≠ 88', String(h.badgeTop));
    } else {
      if (h.badgeTop !== null && Math.abs(h.badgeTop - 32) > 3) add('hero', 'верх блока → метка ≠ 32', String(h.badgeTop));
      if (h.lastBottom !== null && Math.abs(h.lastBottom - 25) > 3) add('hero', 'низ содержимого → низ блока ≠ 25', String(h.lastBottom));
    }
    if (h.photoNat && h.photoNat[0] && (h.photoNat[0] < 200)) add('hero', 'кадр героя мельче эталона', h.photoNat.join('x'));
  }
  return rows;
}

/* ───────────────────────── main ───────────────────────── */
/* Экспорт для разбора уже собранных JSON без повторного прогона Chrome:
   node -e "const a=require('./_tools/site-audit.js'); ..." */
module.exports = { rowsFromMeasure: rowsFromMeasure, staticChecks: staticChecks };

async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  fs.mkdirSync('D:/ragimoff-tmp', { recursive: true });
  const pages = listPages();

  /* режим снятия отрисованного текста (для грамматики) */
  if (TEXT_ONLY) {
    const dir = path.join(OUT, 'rendered');
    fs.mkdirSync(dir, { recursive: true });
    for (const width of WIDTHS) {
      let idx = 0;
      await Promise.all(new Array(Math.min(JOBS, pages.length)).fill(0).map(async function (_, w) {
        while (true) {
          const i = idx++;
          if (i >= pages.length) break;
          const rel = pages[i];
          const d = await measure(rel, width, w, TEXT_PROBE, 'TEXT-PROBE');
          const suffix = width === WIDTHS[0] ? '' : '@' + width;
          const file = path.join(dir, rel.replace(/\//g, '__') + suffix + '.txt');
          if (d && d.text != null) fs.writeFileSync(file, d.text, 'utf8');
          else fs.writeFileSync(file, 'PROBE-FAIL: ' + JSON.stringify(d && d.error || d), 'utf8');
        }
      }));
      console.log('rendered text @' + width + ': ' + pages.length + ' -> ' + dir);
    }
    return;
  }

  console.log('pages: ' + pages.length + '  widths: ' + WIDTHS.join(',') + '  out: ' + OUT);

  const renderedDir = path.join(OUT, 'rendered');
  fs.mkdirSync(renderedDir, { recursive: true });
  const allRows = [];
  /* статика */
  for (const rel of pages) {
    let html;
    try { html = fs.readFileSync(path.join(ROOT, rel), 'utf8'); }
    catch (e) { allRows.push({ page: rel, type: 'file', desc: 'нет файла', was: '', became: '' }); continue; }
    allRows.push(...staticChecks(rel, html));
  }
  console.log('static rows: ' + allRows.length);

  /* отрисовка */
  if (!STATIC_ONLY) {
    for (const width of WIDTHS) {
      const light = LIGHT_WIDTHS.includes(width);
      let idx = 0, done = 0;
      const results = [];
      const workers = new Array(Math.min(JOBS, pages.length)).fill(0).map(async function (_, w) {
        while (true) {
          const i = idx++;
          if (i >= pages.length) break;
          const rel = pages[i];
          const d = await measure(rel, width, w, null, null, light ? 'window.__AUDIT_LIGHT__=1;' : '');
          d.isLight = light;   /* не путать с d.light — это список светлых пятен */
          results[i] = d;
          if (d.text) {
            const suffix = width === WIDTHS[0] ? '' : '@' + width;
            fs.writeFileSync(path.join(renderedDir, rel.replace(/\//g, '__') + suffix + '.txt'), d.text, 'utf8');
          }
          done++;
          if (done % 10 === 0) process.stdout.write('  @' + width + ' ' + done + '/' + pages.length + '\n');
        }
      });
      await Promise.all(workers);
      process.stdout.write('  @' + width + ' ' + pages.length + '/' + pages.length + '\n');
      const rawFile = path.join(OUT, 'site_audit_raw_' + width + '.json');
      fs.writeFileSync(rawFile, JSON.stringify(results.map(function (d) {
        if (d && typeof d === 'object') { const c = Object.assign({}, d); delete c.text; return c; }
        return d;
      }), null, 1), 'utf8');
      results.forEach(function (d) { allRows.push(...rowsFromMeasure(d)); });
    }
  }

  /* TSV */
  const tsv = ['page\ttype\tdescription\twas\tbecame'];
  allRows.forEach(function (r) {
    tsv.push([r.page, r.type, r.desc, r.was, r.became].map(function (v) { return String(v).replace(/\t/g, ' ').replace(/\r?\n/g, ' '); }).join('\t'));
  });
  const tsvFile = path.join(OUT, 'site_audit.tsv');
  fs.writeFileSync(tsvFile, tsv.join('\n') + '\n', 'utf8');
  console.log('TSV: ' + tsvFile + '  rows: ' + allRows.length);
  const byType = {};
  allRows.forEach(function (r) { byType[r.type] = (byType[r.type] || 0) + 1; });
    console.log('by type: ' + JSON.stringify(byType));
}

if (require.main === module) {
  main();
}
