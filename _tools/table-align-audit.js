#!/usr/bin/env node
/* table-align-audit.js — обмер центрирования заголовочного стека и ширины
 * таблиц внутри блоков (headless Chrome CLI, без DevTools).
 *
 * Отвечает на запрос владельца 04.10.2026: «в блоке Qiymətlər подзаголовок
 * идёт по центру, а после него текст и таблица идут по левому краю; сделать
 * подзаголовок в блоках под заголовком блока по центру и таблицу растянуть
 * на всю ширину, как в некоторых блоках».
 *
 * Блок считается «центрированным», если его заголовок — .sec-h2 (в gtc.css
 * он центрирован глобально). Для каждого такого блока снимается:
 *   h2align  — computed text-align заголовка (center = блок центрированный);
 *   subs     — подзаголовок/лид (.sec-sub, .sec-lead) и его text-align;
 *   tables   — таблицы (.price-table, .pricing-tbl, .art-table, .diff-table,
 *              <table>), их ширина, ширина контентной части блока и доля %.
 *
 * Запуск (из корня репозитория, сервер: python -m http.server 8765 -d .):
 *   node _tools/table-align-audit.js --out D:/ragimoff-tmp/tbl --width 1440,390 \
 *        --jobs 5 enurez.html ru/enurez.html en/enurez.html
 *   node _tools/table-align-audit.js --out out --all --width 1440
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { execFile } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const CHROME = process.env.AUDIT_CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PORT = process.env.AUDIT_PORT || '8765';
const TMPBASE = process.env.AUDIT_TMP || 'D:/ragimoff-tmp';

const argv = process.argv.slice(2);
function arg(name, def) {
  const i = argv.indexOf('--' + name);
  return i === -1 ? def : argv[i + 1];
}
const OUT = arg('out', 'D:/ragimoff-tmp/tbl-audit');
const WIDTHS = String(arg('width', '1440,390')).split(',').map(function (s) { return parseInt(s, 10); });
const JOBS = parseInt(arg('jobs', '4'), 10);
const ALL = argv.includes('--all');
const PAGES = [];
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === '--pages') { for (let j = i + 1; j < argv.length && argv[j][0] !== '-'; j++) PAGES.push(argv[j]); }
}
const SKIP_DIRS = ['books', 'klinik-psixiatriya', 'test', 'node_modules', '.git', 'backend', '_supplements', 'favicons', 'data', 'images'];

function listPages() {
  if (PAGES.length) return PAGES;
  const out = [];
  function scan(dir, prefix) {
    for (const name of fs.readdirSync(dir).sort()) {
      const full = path.join(dir, name);
      const st = fs.statSync(full);
      if (st.isDirectory()) {
        if (SKIP_DIRS.includes(name) || name.startsWith('.') || name.startsWith('_')) continue;
        if (prefix !== '') continue;
        scan(full, name + '/');
      } else if (name.endsWith('.html') && !name.startsWith('_') && !/^temp_|^test-wave/.test(name)) {
        const text = fs.readFileSync(full, 'utf8');
        if (/sec-h2/.test(text) && /price-table|pricing-tbl|art-table|diff-table|price-grid-3|<table/.test(text)) out.push(prefix + name);
      }
    }
  }
  scan(ROOT, '');
  return out;
}

const PROBE = `
(function () {
  function r1(v) { return Math.round(v * 10) / 10; }
  function cs(el) { return getComputedStyle(el); }
  function tag(el) {
    var s = el.tagName.toLowerCase();
    if (el.id) s += '#' + el.id;
    if (el.className && typeof el.className === 'string') {
      var c = el.className.trim().split(/\\s+/).slice(0, 2).join('.');
      if (c) s += '.' + c;
    }
    return s;
  }
  function text(el) { return el ? (el.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 60) : ''; }
  function emit(o) {
    var doc = document;
    try { if (window.top && window.top !== window.self) doc = window.top.document; } catch (e) {}
    var pre = doc.getElementById('__tbl_out');
    if (!pre) { pre = doc.createElement('pre'); pre.id = '__tbl_out'; (doc.body || doc.documentElement).appendChild(pre); }
    pre.textContent += btoa(unescape(encodeURIComponent(JSON.stringify(o)))) + '\\n';
  }
  function contentBox(el) {
    var st = cs(el), r = el.getBoundingClientRect();
    var l = r.left + parseFloat(st.borderLeftWidth) + parseFloat(st.paddingLeft);
    var rr = r.right - parseFloat(st.borderRightWidth) - parseFloat(st.paddingRight);
    return { l: r1(l), rr: r1(rr), w: r1(rr - l), c: r1((l + rr) / 2) };
  }
  var TABLE_SEL = '.price-table, .pricing-tbl, .art-table, .diff-table, .price-grid-3, table';
  function measure() {
    var out = { file: location.pathname, w: window.innerWidth, h: document.documentElement.scrollHeight, rows: [] };
    var secs = document.querySelectorAll('section');
    for (var i = 0; i < secs.length; i++) {
      var sec = secs[i];
      var h2 = sec.querySelector('.sec-h2');
      if (!h2) continue;
      var inner = sec.querySelector('.ps-inner, .sec-inner') || sec;
      var cb = contentBox(inner);
      var hb = h2.getBoundingClientRect(), hs = cs(h2);
      var row = {
        sec: tag(sec),
        h2: tag(h2),
        h2align: hs.textAlign,
        h2center: r1(Math.abs((hb.left + hb.right) / 2 - cb.c)),
        blockw: r1(cb.w),
        heads: text(h2),
        subs: [], tables: []
      };
      var subs = [];
      var s1 = sec.querySelector('.sec-sub'); if (s1) subs.push(s1);
      var s2 = sec.querySelector('.sec-lead'); if (s2 && subs.indexOf(s2) === -1) subs.push(s2);
      for (var si = 0; si < subs.length; si++) {
        var el = subs[si], st = cs(el), b = el.getBoundingClientRect();
        row.subs.push({ cls: tag(el), align: st.textAlign, w: r1(b.width),
          center: r1(Math.abs((b.left + b.right) / 2 - cb.c)), text: text(el) });
      }
      var tbs = sec.querySelectorAll(TABLE_SEL);
      for (var ti = 0; ti < tbs.length; ti++) {
        var t = tbs[ti], ts = cs(t), tb = t.getBoundingClientRect();
        /* «ширина блока» для таблицы — контентная часть ЕЁ контейнера
           (родителя): у .ps-inner это карточка без паддинга, у .sec-inner —
           колонка с паддингом --s-section, у обёрток tehsil — свой паддинг.
           Так «100 %» означает «таблица растянута на ширину блока». */
        var pb = contentBox(t.parentElement || sec);
        row.tables.push({ cls: tag(t), w: r1(tb.width), maxw: ts.maxWidth,
          blockw: pb.w, ratio: r1(tb.width / pb.w * 100), text: text(t) });
      }
      out.rows.push(row);
    }
    return out;
  }
  var last = null;
  function settled(tries) {
    tries = tries || 0;
    var b = measure();
    if (last && JSON.stringify(last) === JSON.stringify(b)) { emit(b); return; }
    if (tries > 30) { emit(b); return; }
    last = b;
    setTimeout(function () { settled(tries + 1); }, 300);
  }
  if (document.readyState === 'complete') settled(); else window.addEventListener('load', function () { settled(); });
  setTimeout(settled, 1500);
  window.addEventListener('load', function () {
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { setTimeout(function () { settled(); }, 500); });
  });
})();
`;

function rewriteFonts(html, on) {
  if (!on) return html;
  const P = process.env.AUDIT_FONTCACHE_PORT || '8776';
  const crypto = require('crypto');
  const h = (u) => crypto.createHash('md5').update(u).digest('hex');
  html = html.replace(/https:\/\/fonts\.googleapis\.com\/css2\?[^"'`)\s<>]+/g, (u) => 'http://127.0.0.1:' + P + '/fc/' + h(u.replace(/&amp;/g, '&')) + '.css');
  html = html.replace(/https:\/\/fonts\.gstatic\.com\/[^"'`)\s<>)]+/g, (u) => 'http://127.0.0.1:' + P + '/fc/' + h(u) + '.woff2');
  return html;
}

let dirSeq = 0;
/* Ретро-замер «до»: AUDIT_UNDO=1 возвращает состояние до волны 04.10.2026
   (лид .sec-lead — по левому краю; .price-table — max-width 780 px), чтобы
   снять «было» по тем же страницам уже после правки. */
const UNDO_CSS = '<style id="undo29">' +
  ':where(.sec-inner, .ps-inner):has(.sec-h2) > :is(.sec-lead){text-align:start !important;}' +
  ':where(.sec-inner, .ps-inner):has(.sec-h2) > .sec-header > :is(.sec-lead){text-align:start !important;}' +
  '.ps-inner > .price-table,.sec-inner > .price-table{width:auto !important;max-width:780px !important;}' +
  '</style>';
function withProbe(rel) {
  const src = path.join(ROOT, rel);
  const tmp = path.join(path.dirname(src), '_tbl.' + process.pid + '.' + (++dirSeq) + '.' + path.basename(src));
  let html = fs.readFileSync(src, 'utf8');
  html = rewriteFonts(html, !process.env.AUDIT_NO_FONTCACHE);
  if (process.env.AUDIT_UNDO) html = html.replace(/<\/head>/i, UNDO_CSS + '</head>');
  html = html.replace(/<\/body>/i, '<script>' + PROBE + '</script></body>');
  fs.writeFileSync(tmp, html, 'utf8');
  return tmp;
}

function measureOnce(rel, width) {
  return new Promise((resolve) => {
    const tmp = withProbe(rel);
    const relTmp = path.relative(ROOT, tmp).replace(/\\/g, '/');
    let url, wrapper = null, winW = width;
    if (width < 500) {
      const wtmp = path.join(ROOT, '_tbl.w.' + process.pid + '.' + (++dirSeq) + '.html');
      fs.writeFileSync(wtmp, '<!DOCTYPE html><html><head><meta charset="utf-8"><title>narrow</title>' +
        '<style>html,body{margin:0;padding:0;background:#07090E}#f{width:' + width + 'px;height:2000px;border:0;display:block}</style>' +
        '</head><body><iframe id="f" src="' + encodeURI(relTmp) + '"></iframe></body></html>', 'utf8');
      wrapper = wtmp;
      url = 'http://127.0.0.1:' + PORT + '/' + encodeURI(path.relative(ROOT, wtmp).replace(/\\/g, '/'));
      winW = 520;
    } else {
      url = 'http://127.0.0.1:' + PORT + '/' + encodeURI(relTmp);
    }
    const userDir = TMPBASE + '/tbl-prof-' + process.pid + '-' + (++dirSeq);
    execFile(CHROME, [
      '--headless=new', '--disable-gpu', '--no-sandbox', '--disable-extensions',
      '--lang=az', '--accept-lang=az',
      '--user-data-dir=' + userDir,
      '--host-resolver-rules=MAP ipapi.co 127.0.0.1:9',
      '--virtual-time-budget=12000',
      '--window-size=' + winW + ',2000',
      '--dump-dom', url
    ], { encoding: 'utf8', maxBuffer: 1 << 28, timeout: 180000, killSignal: 'SIGKILL' }, (err, stdout) => {
      try { fs.unlinkSync(tmp); } catch (e) {}
      if (wrapper) { try { fs.unlinkSync(wrapper); } catch (e) {} }
      try { fs.rmSync(userDir, { recursive: true, force: true }); } catch (e) {}
      if (err) { resolve({ file: rel, width: width, error: String(err.message || err).slice(0, 160) }); return; }
      const block = stdout.match(/<pre id="__tbl_out">([\s\S]*?)<\/pre>/);
      if (!block) { resolve({ file: rel, width: width, error: 'no __tbl_out in dump' }); return; }
      const lines = block[1].split('\n').map(function (s) { return s.trim(); }).filter(Boolean);
      const snaps = [];
      for (const ln of lines) { try { snaps.push(JSON.parse(Buffer.from(ln, 'base64').toString('utf8'))); } catch (e) {} }
      if (!snaps.length) { resolve({ file: rel, width: width, error: 'bad json' }); return; }
      const good = snaps[snaps.length - 1];
      good.file = rel; good.width = width;
      resolve(good);
    });
  });
}

async function pool(items, size, fn) {
  const out = new Array(items.length);
  let idx = 0;
  async function worker() {
    while (idx < items.length) {
      const i = idx++;
      out[i] = await fn(items[i]);
    }
  }
  await Promise.all(Array.from({ length: Math.min(size, items.length) }, () => worker()));
  return out;
}

/* Chrome в параллели изредка падает — 3 попытки на замер */
async function measureWithRetry(page, width, attempts) {
  let last = null;
  for (let a = 0; a < (attempts || 3); a++) {
    const r = await measureOnce(page, width);
    if (!r.error) return r;
    last = r;
  }
  return last;
}

(async function () {
  const pages = listPages();
  fs.mkdirSync(OUT, { recursive: true });
  const jobs = [];
  for (const p of pages) for (const w of WIDTHS) jobs.push({ page: p, width: w });
  console.log('pages: ' + pages.length + ', measurements: ' + jobs.length);
  let done = 0;
  const results = await pool(jobs, JOBS, async function (j) {
    const r = await measureWithRetry(j.page, j.width, 3);
    done++;
    if (done % 10 === 0) process.stderr.write('  ' + done + '/' + jobs.length + '\n');
    return r;
  });
  for (const w of WIDTHS) {
    const rows = [['page', 'block', 'heading', 'h2_align', 'sub', 'sub_align', 'table', 'table_w', 'block_w', 'ratio_pct', 'verdict'].join('\t')];
    for (const r of results) {
      if (r.width !== w) continue;
      if (r.error) { rows.push([r.file, '', '', '', '', '', '', '', '', '', 'ERROR: ' + r.error].join('\t')); continue; }
      for (const row of r.rows) {
        const subs = row.subs.length ? row.subs : [{ cls: '-', align: '-', text: '' }];
        const tables = row.tables.length ? row.tables : [{ cls: '-', w: '', ratio: '', maxw: '', text: '' }];
        for (const t of tables) {
          for (const s of subs) {
            const centeredH = row.h2align === 'center';
            const badSub = centeredH && s.cls !== '-' && s.align !== 'center';
            const badTbl = t.cls !== '-' && t.ratio !== '' && t.ratio < 99;
            const verdict = (badSub || badTbl) ? 'ОТКЛОНЕНИЕ' : 'ок';
            rows.push([r.file, row.sec, row.heads, row.h2align, s.cls + ' «' + s.text + '»', s.align,
              t.cls + ' «' + t.text + '»', t.w, (t.blockw !== undefined ? t.blockw : row.blockw), t.ratio, verdict].join('\t'));
          }
        }
      }
    }
    fs.writeFileSync(path.join(OUT, 'table_align_' + w + '.tsv'), rows.join('\n') + '\n', 'utf8');
    console.log('-> ' + path.join(OUT, 'table_align_' + w + '.tsv') + '  (' + (rows.length - 1) + ' строк)');
  }
  fs.writeFileSync(path.join(OUT, 'table_align_raw.json'), JSON.stringify(results, null, 1), 'utf8');
})();
