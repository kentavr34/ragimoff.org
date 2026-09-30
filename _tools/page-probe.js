#!/usr/bin/env node
/* page-probe.js — разовый замер страницы произвольным пробником.
 *
 * Кладёт <probe> в копию страницы рядом с оригиналом (чтобы относительные
 * пути работали), гоняет headless Chrome и печатает JSON, который пробник
 * положил в <title> после метки PROBE-JSON:.
 *
 * Запуск:
 *   python -m http.server 8765 --bind 127.0.0.1 -d .        # из корня репо
 *   node _tools/page-probe.js index.html 1440 _tools/_p.js
 *   node _tools/page-probe.js index.html 1440 --inline "var x=1;document.title='PROBE-JSON:'+JSON.stringify(x)"
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const CHROME = process.env.AUDIT_CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PORT = process.env.AUDIT_PORT || '8765';

const page = process.argv[2];
const width = parseInt(process.argv[3] || '1440', 10);
const height = parseInt(process.argv[4] || '1400', 10);
let probe;
if (process.argv[5] === '--inline') {
  probe = process.argv[6];
} else {
  probe = fs.readFileSync(path.resolve(__dirname, process.argv[5] || 'site-audit-probe.js'), 'utf8');
}
if (!probe.includes('window.__PP__')) probe = 'window.__PP__=1;' + probe;

const src = path.join(ROOT, page);
const tmp = path.join(path.dirname(src), '_p.' + path.basename(src));
let html = fs.readFileSync(src, 'utf8');
html = /<\/body>/i.test(html) ? html.replace(/<\/body>/i, '<script>' + probe + '</script></body>') : html + '<script>' + probe + '</script>';
fs.writeFileSync(tmp, html, 'utf8');
const relTmp = path.relative(ROOT, tmp).replace(/\\/g, '/');
const userDir = 'D:/ragimoff-tmp/pp-' + process.pid + '-' + Math.random().toString(36).slice(2, 7);
let dom = '';
try {
  dom = execFileSync(CHROME, [
    '--headless=new', '--disable-gpu', '--no-sandbox', '--disable-extensions',
    '--lang=az', '--accept-lang=az', '--user-data-dir=' + userDir,
    '--virtual-time-budget=9000', '--window-size=' + width + ',' + height,
    '--force-device-scale-factor=1', '--dump-dom',
    'http://127.0.0.1:' + PORT + '/' + encodeURI(relTmp)
  ], { encoding: 'utf8', maxBuffer: 1 << 28, stdio: ['ignore', 'pipe', 'ignore'], timeout: 90000 });
} catch (e) { process.stderr.write('chrome error: ' + e.message + '\n'); }
finally {
  try { fs.unlinkSync(tmp); } catch (e) {}
  try { fs.rmSync(userDir, { recursive: true, force: true }); } catch (e) {}
}
const m = dom.match(/PROBE-JSON:([\s\S]*?)<\/title>/);
if (m) {
  try { console.log(JSON.stringify(JSON.parse(m[1]), null, 1)); }
  catch (e) { console.log(m[1]); }
} else {
  const t = dom.match(/<title>([\s\S]*?)<\/title>/);
  console.log('NO PROBE-JSON; title=' + (t ? t[1].slice(0, 200) : '(none)'));
}
