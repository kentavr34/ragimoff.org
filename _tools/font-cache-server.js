#!/usr/bin/env node
/* font-cache-server.js — локальный кэш Google Fonts для замеров headless Chrome.
 *
 * Зачем. fonts.googleapis.com отвечает с этой машины ~8 секунд, а каждая
 * страница тянет свой css2?… и по 4–8 файлов woff2; замер одной страницы
 * выходил 3 минуты, сплошной обход 171 страницы — три часа. Сервер один раз
 * скачивает каждый css и все его woff2 в D:/ragimoff-tmp/fontcache и отдаёт
 * их с 127.0.0.1:8766; страницы при замере переписываются на этот адрес
 * (site-audit.js / hero-survey.js — при AUDIT_FONTCACHE=1).
 *
 * Запуск (в фоне, до обхода):
 *   node _tools/font-cache-server.js            # слушает 8766
 *   node _tools/font-cache-server.js --warm     # скачать всё и выйти
 * Адресация: /fc/<md5 от исходного URL>.css — тот же хеш, что в переписывателе.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');
const crypto = require('crypto');

const ROOT = path.resolve(__dirname, '..');
const CACHE = process.env.FONTCACHE_DIR || 'D:/ragimoff-tmp/fontcache';
const PORT = parseInt(process.env.FONTCACHE_PORT || '8766', 10);
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36';

fs.mkdirSync(CACHE, { recursive: true });

function hash(url) {
  return crypto.createHash('md5').update(url).digest('hex');
}

function collectFontUrls() {
  const urls = new Set();
  const dirs = ['', 'ru', 'en', '_tools', 'test'];
  for (const d of dirs) {
    const base = path.join(ROOT, d);
    if (!fs.existsSync(base)) continue;
    for (const name of fs.readdirSync(base)) {
      if (!name.endsWith('.html') && !name.endsWith('.js') && !name.endsWith('.css')) continue;
      const full = path.join(base, name);
      let s;
      try { s = fs.readFileSync(full, 'utf8'); } catch (e) { continue; }
      const re = /https:\/\/fonts\.googleapis\.com\/css2\?[^"'`)\s<>]+/g;
      let m;
      while ((m = re.exec(s)) !== null) urls.add(m[0].replace(/&amp;/g, '&'));
    }
  }
  return [...urls];
}

function get(url, binary) {
  return new Promise(function (resolve, reject) {
    https.get(url, { headers: { 'User-Agent': UA, 'Accept': '*/*' } }, function (res) {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        get(res.headers.location, binary).then(resolve, reject); return;
      }
      if (res.statusCode !== 200) { reject(new Error('HTTP ' + res.statusCode + ' ' + url)); return; }
      const chunks = [];
      res.on('data', function (c) { chunks.push(c); });
      res.on('end', function () {
        const buf = Buffer.concat(chunks);
        resolve(binary ? buf : buf.toString('utf8'));
      });
    }).on('error', reject);
  });
}

async function warm() {
  const urls = collectFontUrls();
  let cssN = 0, fontN = 0, fail = 0;
  for (const url of urls) {
    const cssPath = path.join(CACHE, hash(url) + '.css');
    let css;
    if (fs.existsSync(cssPath)) { css = fs.readFileSync(cssPath, 'utf8'); }
    else {
      try { css = await get(url, false); } catch (e) { fail++; console.error('css fail:', url, e.message); continue; }
    }
    const fonts = [...css.matchAll(/url\((https:\/\/fonts\.gstatic\.com\/[^)]+)\)/g)].map(function (m) { return m[1]; });
    for (const f of fonts) {
      const name = hash(f) + '.woff2';
      const p = path.join(CACHE, name);
      if (!fs.existsSync(p)) {
        try { fs.writeFileSync(p, await get(f, true)); fontN++; }
        catch (e) { fail++; }
      }
      css = css.split(f).join('http://127.0.0.1:' + PORT + '/fc/' + name);
    }
    if (!fs.existsSync(cssPath)) { fs.writeFileSync(cssPath, css, 'utf8'); cssN++; }
  }
  console.log('font cache: css ' + cssN + ', woff2 ' + fontN + ', ошибок ' + fail + ' → ' + CACHE);
}

if (process.argv.includes('--warm')) {
  warm().then(function () { process.exit(0); });
} else {
  warm().then(function () {
    http.createServer(function (req, res) {
      const m = req.url.match(/^\/fc\/([A-Za-z0-9._-]+)$/);
      if (!m) { res.writeHead(404); res.end('not found'); return; }
      const p = path.join(CACHE, m[1]);
      if (!fs.existsSync(p)) { res.writeHead(404); res.end('miss'); return; }
      res.writeHead(200, { 'Content-Type': /\.css$/.test(p) ? 'text/css; charset=utf-8' : 'font/woff2', 'Cache-Control': 'max-age=86400' });
      fs.createReadStream(p).pipe(res);
    }).listen(PORT, '127.0.0.1', function () {
      console.log('font cache server → http://127.0.0.1:' + PORT + '/fc/<md5>.css  (dir ' + CACHE + ')');
    });
  });
}
