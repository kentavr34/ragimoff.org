#!/usr/bin/env node
/* standard-shot.js — полные скриншоты страниц headless Chrome'ом для отчёта
 * «единый стандарт». Тёплый профиль + локальный кэш шрифтов (как
 * standard-audit.js), ширина <500 — через iframe-обёртку.
 *
 * Запуск:
 *   python -m http.server 8767 --bind 127.0.0.1 -d <каталог>   # сервер
 *   node _tools/standard-shot.js --port 8767 --out D:/out --prefix before \
 *        --width 1440,390 aile-terapiyasi.html samira.html
 */
'use strict';
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const CHROME = process.env.SHOT_CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const argv = process.argv.slice(2);
function arg(name, def) {
  const i = argv.indexOf('--' + name);
  return i === -1 ? def : argv[i + 1];
}
const PORT = arg('port', '8765');
const OUT = arg('out', 'D:/ragimoff-tmp/shots');
const PREFIX = arg('prefix', 'shot');
const WIDTHS = String(arg('width', '1440,390')).split(',').map(Number);
const MAXH = parseInt(arg('maxh', '13000'), 10);
const ARGWITH = ['port', 'out', 'prefix', 'width', 'maxh', 'pages'];
const PAGES = [];
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === '--pages') { for (let j = i + 1; j < argv.length && argv[j][0] !== '-'; j++) { PAGES.push(argv[j]); i = j; } }
  else if (argv[i][0] === '-' && ARGWITH.indexOf(argv[i].slice(2)) >= 0) { i++; }
  else if (argv[i][0] !== '-') PAGES.push(argv[i]);
}
if (!PAGES.length) { console.error('no pages'); process.exit(1); }
const FC_PORT = process.env.FONTCACHE_PORT || '8766';
fs.mkdirSync(OUT, { recursive: true });

const PROBE = `(function(){ function r(){ var h=Math.max(document.documentElement.scrollHeight, document.body?document.body.scrollHeight:0);
  var doc=document; try{ if(window.top&&window.top!==window.self) doc=window.top.document; }catch(e){}
  var pre=doc.getElementById('__sh'); if(!pre){pre=doc.createElement('pre');pre.id='__sh';(doc.body||doc.documentElement).appendChild(pre);}
  pre.textContent = String(h); }
  if(document.readyState==='complete')r(); else window.addEventListener('load', r); setTimeout(r,1500); setTimeout(r,3200); })();`;

function rewrite(html) {
  const h = (u) => crypto.createHash('md5').update(u).digest('hex');
  html = html.replace(/https:\/\/fonts\.googleapis\.com\/css2\?[^"'`)\s<>]+/g,
    (u) => 'http://127.0.0.1:' + FC_PORT + '/fc/' + h(u.replace(/&amp;/g, '&')) + '.css');
  html = html.replace(/https:\/\/fonts\.gstatic\.com\/[^"'`)\s<>)]+/g,
    (u) => 'http://127.0.0.1:' + FC_PORT + '/fc/' + h(u) + '.woff2');
  html = html.replace(/(href|src)="([^"]*\.(?:css|js))(\?[^"]*)?"/g, function (m, a, u, q) {
    if (/^(https?:)?\/\//.test(u)) return m;
    return a + '="' + u + (q ? q + '&' : '?') + 'sa=1"';
  });
  return html;
}
let seq = 0;
function prep(rel, withProbe) {
  const src = path.join(ROOT, rel);
  const tmp = path.join(path.dirname(src), '_sn.' + process.pid + '.' + (++seq) + '.' + path.basename(src));
  let html = fs.readFileSync(src, 'utf8');
  const lang = /(^|[\/\\])ru[\/\\]/.test(rel) ? 'ru' : (/(^|[\/\\])en[\/\\]/.test(rel) ? 'en' : 'az');
  html = html.replace(/<head([^>]*)>/i, '<head$1><script>try{localStorage.setItem("ragimoff_lang","' + lang + '");}catch(e){}</script>');
  html = rewrite(html);
  if (withProbe) {
    html = html.replace(/<\/body>/i, '<script>' + PROBE + '</script></body>');
    if (html.indexOf('__sh') === -1) html += '<script>' + PROBE + '</script>';
  }
  fs.writeFileSync(tmp, html, 'utf8');
  return tmp;
}
function urlOf(p) { return 'http://127.0.0.1:' + PORT + '/' + encodeURI(path.relative(ROOT, p).replace(/\\/g, '/')); }

function chrome(args) {
  return execFileSync(CHROME, ['--headless=new', '--disable-gpu', '--no-sandbox', '--disable-extensions',
    '--lang=az', '--accept-lang=az', '--no-first-run', '--no-default-browser-check',
    '--host-resolver-rules=MAP ipapi.co 127.0.0.1:9',
    '--user-data-dir=' + (process.env.SHOT_PROFILE || 'D:/ragimoff-tmp/shotprof')].concat(args),
    { encoding: 'utf8', maxBuffer: 1 << 28, stdio: ['ignore', 'pipe', 'ignore'] });
}

function heightOf(rel, w) {
  const tmp = prep(rel, true);
  let h = 4000;
  try {
    const dom = chrome(['--virtual-time-budget=12000', '--window-size=' + Math.max(w, 520) + ',1200', '--dump-dom', urlOf(tmp)]);
    const m = dom.match(/<pre id="__sh">\s*(\d+)/);
    if (m) h = Math.min(MAXH, Math.max(1500, parseInt(m[1], 10) + 40));
  } catch (e) { /* останемся на 4000 */ }
  try { fs.unlinkSync(tmp); } catch (e) {}
  return h;
}

const done = [];
for (const w of WIDTHS) {
  for (const p of PAGES) {
    const h = heightOf(p, w);
    const name = PREFIX + '-' + w + '-' + p.replace(/[\/\\]/g, '_').replace(/\.html$/, '') + '.png';
    const out = path.join(OUT, name);
    if (w < 500) {
      /* iframe-обёртка: Chrome не даёт окно уже 500 px */
      const inner = prep(p, false);
      const relSrc = path.relative(ROOT, inner).replace(/\\/g, '/');
      const wrapper = path.join(ROOT, '_sn.w.' + process.pid + '.' + (++seq) + '.html');
      fs.writeFileSync(wrapper,
        '<!DOCTYPE html><html><head><meta charset="utf-8">' +
        '<style>html,body{margin:0;padding:0;background:#07090E}#f{width:' + w + 'px;height:' + h + 'px;border:0;display:block}</style>' +
        '</head><body><iframe id="f" src="' + encodeURI(relSrc) + '"></iframe></body></html>', 'utf8');
      chrome(['--virtual-time-budget=16000', '--window-size=' + (w + 20) + ',' + h, '--screenshot=' + out, urlOf(wrapper)]);
      try { fs.unlinkSync(wrapper); } catch (e) {}
      try { fs.unlinkSync(inner); } catch (e) {}
    } else {
      const tmp = prep(p, false);
      chrome(['--virtual-time-budget=16000', '--window-size=' + w + ',' + h, '--screenshot=' + out, urlOf(tmp)]);
      try { fs.unlinkSync(tmp); } catch (e) {}
    }
    done.push(out);
    process.stderr.write('  shot ' + PREFIX + ' ' + w + ' ' + p + ' (' + h + 'px)\n');
  }
}
console.log(done.join('\n'));
