#!/usr/bin/env node
/* site-shot.js — скриншоты страниц headless Chrome'ом (CLI, без DevTools).
 *
 * Пишет в ASCII-каталог: chrome не умеет писать в путь с кириллицей
 * («Системе не удается найти указанный путь»), поэтому имя файла и папка —
 * только латиница, а копию в отчётный каталог делает вызывающий.
 *
 * Запуск:
 *   python -m http.server 8765 --bind 127.0.0.1 -d .       # из корня репозитория
 *   node _tools/site-shot.js --out D:/ragimoff-tmp/audit --prefix before \
 *        --width 1440 --pages index.html tehsil.html
 *   node _tools/site-shot.js --out D:/ragimoff-tmp/audit --prefix after \
 *        --width 390 --pages blog-aile-2.html
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { execFile } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const CHROME = process.env.AUDIT_CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PORT = process.env.AUDIT_PORT || '8765';

const argv = process.argv.slice(2);
function arg(name, def) {
  const i = argv.indexOf('--' + name);
  return i === -1 ? def : argv[i + 1];
}
const OUT = arg('out', 'D:/ragimoff-tmp/audit');
const PREFIX = arg('prefix', 'shot');
const WIDTH = parseInt(arg('width', '1440'), 10);
const HEIGHT = parseInt(arg('height', WIDTH <= 480 ? '1400' : '1600'), 10);
const PAGES = [];
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === '--pages') { for (let j = i + 1; j < argv.length && argv[j][0] !== '-'; j++) PAGES.push(argv[j]); }
}
const JOBS = parseInt(arg('jobs', '3'), 10);
/* ширина кадра внутри обёртки: 0 — снимать окно как есть */
const FRAME = parseInt(arg('frame', '0'), 10);

/* Chrome на Windows не даёт окно уже 500 px (проверено и в new-, и в old-
   headless: --window-size=390 всё равно даёт layout 500 и картинку-обрезку).
   Поэтому узкую версию снимаем через кадр: страница открывается в iframe
   нужной ширины, а скриншот делается по обёртке. В имени файла — ширина
   кадра, чтобы 500 и 390 не путались. */
function shot(rel, n) {
  return new Promise(function (resolve) {
    const framed = FRAME > 0;
    const name = PREFIX + '-' + (framed ? FRAME : WIDTH) + '-' + rel.replace(/[\/\\]/g, '_').replace(/\.html$/, '') + '.png';
    const out = path.join(OUT, name);
    const userDir = 'D:/ragimoff-tmp/shot-profile-' + process.pid + '-' + n;
    let target = 'http://127.0.0.1:' + PORT + '/' + rel;
    let winW = WIDTH, winH = HEIGHT;
    let wrap = null;
    if (framed) {
      const src = path.join(ROOT, rel);
      wrap = path.join(path.dirname(src), '_shot.' + path.basename(src));
      winW = FRAME + 40; winH = HEIGHT + 40;
      fs.writeFileSync(wrap, '<!doctype html><html><head><meta charset="utf-8">' +
        '<style>html,body{margin:0;padding:0;background:#07090E}iframe{display:block;margin:0 auto;width:' +
        FRAME + 'px;height:' + HEIGHT + 'px;border:0}</style></head><body><iframe src="' +
        path.basename(rel) + '"></iframe></body></html>', 'utf8');
      target = 'http://127.0.0.1:' + PORT + '/' + path.relative(ROOT, wrap).replace(/\\/g, '/');
    }
    execFile(CHROME, [
      '--headless=new', '--disable-gpu', '--no-sandbox', '--disable-extensions',
      '--lang=az', '--accept-lang=az',
      '--user-data-dir=' + userDir,
      '--virtual-time-budget=9000',
      '--window-size=' + winW + ',' + winH,
      '--force-device-scale-factor=1',
      '--hide-scrollbars',
      '--screenshot=' + out,
      target
    ], { timeout: 120000 }, function (err) {
      try { fs.rmSync(userDir, { recursive: true, force: true }); } catch (e) {}
      if (wrap) { try { fs.unlinkSync(wrap); } catch (e) {} }
      const ok = fs.existsSync(out);
      console.log((ok ? '  ok   ' : '  FAIL ') + name + (err && !ok ? '  ' + String(err).slice(0, 80) : ''));
      resolve(ok);
    });
  });
}

(async function () {
  fs.mkdirSync(OUT, { recursive: true });
  let i = 0;
  await Promise.all(new Array(Math.min(JOBS, PAGES.length || 1)).fill(0).map(async function (_, w) {
    while (true) {
      const k = i++;
      if (k >= PAGES.length) break;
      await shot(PAGES[k], w);
    }
  }));
  console.log('-> ' + OUT);
})();
