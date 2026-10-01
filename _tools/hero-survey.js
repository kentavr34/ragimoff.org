#!/usr/bin/env node
/* Сплошной обмер блоков героя (headless Chrome CLI, N параллельных заданий).
 *
 * Дополняет _tools/hero-measure.js: тот мерит 6 контрольных чисел одного блока,
 * этот снимает ПОЛНУЮ геометрию для таблицы «до/после»:
 *   страница | высота блока | бейдж y | H1 y | лид y | поиск y | фото x,y,w,h
 * плюс зазоры между элементами, полулидинг H1 (число строк), отступы слева,
 * положение фото относительно нижней/правой грани, гориз. прокрутка.
 *
 * Запуск:
 *   node _tools/hero-survey.js --out <файл.json> --width 1440 --jobs 6 --list <файл со списком>
 *   node _tools/hero-survey.js --out <файл.json> --width 390 --jobs 6 page1.html page2.html
 * Сервер: python -m http.server 8765 --bind 127.0.0.1 -d <корень репозитория>
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { execFile } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const CHROME = process.env.HERO_CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PORT = process.env.HERO_PORT || '8765';
const TMPBASE = process.env.HERO_TMP || 'D:/ragimoff-tmp';

const PROBE = `
(function () {
  function r1(v) { return Math.round(v * 10) / 10; }
  function box(el) {
    if (!el) return null;
    var r = el.getBoundingClientRect();
    return { x: r1(r.left), y: r1(r.top), w: r1(r.width), h: r1(r.height), b: r1(r.bottom), r: r1(r.right) };
  }
  function q(root, s) { return root.querySelector(s); }
  function run(computeOnly) {
    var hero = q(document, '.page-hero, .page-hero-x, .pg-hero');
    var out = {
      w: window.innerWidth, cw: document.documentElement.clientWidth,
      docW: document.documentElement.scrollWidth,
      hScroll: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
      href: location.pathname,
      heroClass: hero ? hero.className.split(' ')[0] : null
    };
    if (!hero) { out.ts = Math.round(performance.now()); if (computeOnly) { lastSnapshot = out; return; } emit(JSON.stringify(out)); return; }
    var hb = box(hero);
    var cs = getComputedStyle(hero);
    var badge = q(hero, '.badge') || q(hero, '.ph-badge');
    var h1 = q(hero, '.hero-h1') || q(hero, '.ph-h1') || q(hero, 'h1');
    var lead = q(hero, '.hero-lead') || q(hero, '.ph-sub');
    var search = q(hero, '.hero-search-wrap') || q(hero, '.ph-search-wrap');
    var col = q(hero, '.photo-col');
    var img = q(hero, '.photo-col img');
    var inner = q(hero, '.hero-inner') || q(hero, '.page-hero-x-inner') || q(hero, '.pg-hero-inner');
    function lines(el) {
      if (!el) return 0;
      var r = document.createRange(); r.selectNodeContents(el);
      var rects = r.getClientRects(), tops = [];
      for (var i = 0; i < rects.length; i++) {
        var t = Math.round(rects[i].top);
        if (tops.indexOf(t) < 0) tops.push(t);
      }
      return tops.length;
    }
    /* Построчная мера для правила владельца «строки по возможности равной
       длины, деление по словам»: идём по текстовым узлам (а не по корню
       элемента — у корня в прямоугольники попадают блочные дети во всю
       ширину, и «строк» выходило вдвое больше), каждую видимую строку
       собираем по верхней границе, ширину берём по чернилам. */
    function lineMetrics(el) {
      if (!el) return null;
      var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
      var rows = [], node;
      while ((node = walker.nextNode())) {
        if (!node.nodeValue || !/\\S/.test(node.nodeValue)) continue;
        var pe = node.parentElement;
        if (!pe) continue;
        var pcs = getComputedStyle(pe);
        if (pcs.display === 'none' || pcs.visibility === 'hidden') continue;
        var rg = document.createRange();
        rg.selectNodeContents(node);
        var rcs = rg.getClientRects();
        for (var k = 0; k < rcs.length; k++) {
          var b = rcs[k];
          if (b.width < 1 || b.height < 1) continue;
          var top = Math.round(b.top), idx = -1;
          for (var q = 0; q < rows.length; q++) if (rows[q].top === top) { idx = q; break; }
          if (idx < 0) rows.push({ top: top, l: b.left, r: b.right });
          else { rows[idx].l = Math.min(rows[idx].l, b.left); rows[idx].r = Math.max(rows[idx].r, b.right); }
        }
      }
      rows.sort(function (a, b) { return a.top - b.top; });
      var ws = rows.map(function (o) { return r1(o.r - o.l); });
      var mn = ws.length ? Math.min.apply(null, ws) : 0;
      var mx = ws.length ? Math.max.apply(null, ws) : 0;
      return { n: ws.length, widths: ws, skew: mn ? r1(mx / mn) : null };
    }
    function rel(el) {
      if (!el) return null;
      var b = box(el);
      return { y: r1(b.y - hb.y), x: r1(b.x - hb.x), h: b.h, w: b.w, b: r1(b.b - hb.y) };
    }
    var bb = rel(badge), h1b = rel(h1), lb = rel(lead), sb = rel(search);
    out.hero = { x: hb.x, y: hb.y, w: hb.w, h: hb.h };
    out.inner = box(inner);
    out.badge = bb; out.h1 = h1b; out.lead = lb; out.search = sb;
    out.h1Lines = lines(h1);
    out.leadLines = lines(lead);
    /* точные построчные меры (текстовые узлы, чернильная ширина) */
    out.h1Metrics = lineMetrics(h1);
    out.leadMetrics = lineMetrics(lead);
    out.h1Fs = h1 ? getComputedStyle(h1).fontSize : null;
    out.h1Text = h1 ? h1.textContent.replace(/\\s+/g, ' ').trim().slice(0, 90) : null;
    out.leadText = lead ? lead.textContent.replace(/\\s+/g, ' ').trim().slice(0, 90) : null;
    if (img) {
      var ib = box(img);
      out.photo = {
        x: ib.x, y: ib.y, w: ib.w, h: ib.h,
        relY: r1(ib.y - hb.y),                 /* верх фото от верхней грани */
        gapBottom: r1(hb.b - ib.b),            /* низ фото → низ блока */
        gapRight: r1(hb.r - ib.r),             /* правый край фото → правый край блока */
        src: img.getAttribute('src'),
        natural: [img.naturalWidth, img.naturalHeight],
        objectFit: getComputedStyle(img).objectFit,
        objectPos: getComputedStyle(img).objectPosition
      };
    } else { out.photo = null; }
    out.colPos = col ? getComputedStyle(col).position : null;
    out.gaps = {
      badgeTop: bb ? bb.y : null,
      badgeToH1: (bb && h1b) ? r1(h1b.y - (bb.y + bb.h)) : null,
      h1ToLead: (h1b && lb) ? r1(lb.y - (h1b.y + h1b.h)) : null,
      leadToSearch: (lb && sb) ? r1(sb.y - (lb.y + lb.h)) : null,
      searchToBottom: (sb) ? r1(hb.h - (sb.y + sb.h)) : null
    };
    out.pad = { top: cs.paddingTop, bottom: cs.paddingBottom, bt: cs.borderTopWidth, bb: cs.borderBottomWidth };
    out.minH = cs.minHeight;
    out.leftInset = bb ? bb.x : (h1b ? h1b.x : null);
    out.errs = (window.__hroErrs || []).slice(0, 6);
    /* маркер «фиттер отработал»: на десктопе подгонка ставит кегль самому H1,
       на телефоне — каждой строке-спану .ph-h1-w1/.ph-h1-w2, а у самого H1
       стиль остаётся пустым (иначе замер 390 не проходил фильтр «до») */
    var w1El = h1 ? h1.querySelector('.ph-h1-w1, .h1-w1') : null;
    var w2El = h1 ? h1.querySelector('.ph-h1-w2, .h1-w2') : null;
    out.h1Inline = [
      h1 ? (h1.getAttribute('style') || '') : '',
      w1El ? (w1El.getAttribute('style') || '') : '',
      w2El ? (w2El.getAttribute('style') || '') : ''
    ].join(' | ').slice(0, 220);
    out.fitRan = /padding-bottom/.test(hero.getAttribute('style') || '');
    out.heroStyle = (hero.getAttribute('style') || '').slice(0, 160);
    out.ts = Math.round(performance.now());
    out.st = document.readyState;
    out.fonts = (document.fonts && document.fonts.status) || 'n/a';
    if (computeOnly) { lastSnapshot = out; return; }
    emit(JSON.stringify(out));
  }
  /* Каждый замер дописывается СТРОКОЙ (base64) — не перезаписью: под
     виртуальным временем порядок «load / таймеры» не гарантирован, и
     последняя запись не всегда самая свежая. Сборщик берёт строку с
     максимальным ts. */
  function emit(json) {
    /* На узкой ширине страница грузится в iframe (окно Chrome уже 500 px
       не сделать), поэтому результат пишем в ДОКУМЕНТ-ВЕРХУШКУ:
       --dump-dom печатает обёртку, а не вложенный документ. */
    var doc = document;
    try { if (window.top && window.top !== window.self) doc = window.top.document; } catch (e) {}
    var pre = doc.getElementById('__hro_out');
    if (!pre) { pre = doc.createElement('pre'); pre.id = '__hro_out'; (doc.body || doc.documentElement).appendChild(pre); }
    pre.textContent += btoa(unescape(encodeURIComponent(json))) + '\\n';
  }
  /* Наведение порядка перед замером: страницы сайта доводят геометрию своими
     скриптами (js-hero-fit2.js — по resize, главная — fitAll по resize).
     Если замер попадал в момент, когда фиттер ещё не отработал (или его
     сброс прошёл, а подгонка нет), фиксировалось промежуточное состояние:
     H1 32 px вместо подогнанных 48, низ поиска 10 вместо 48 — замер tehsil
     давал 400 вместо 458. Явный resize заставляет все фиттеры пересчитать
     раскладку синхронно ДО снятия чисел. */
  function nudge() { try { window.dispatchEvent(new Event('resize')); } catch (e) {} }
  /* Снимаем числа, когда состояние УСТОЯЛОСЬ: два подряд совпадающих
     замера (высота блока, кегль и число строк H1). */
  function settled(attempt) {
    nudge();
    var a = null, b = null, tries = 0;
    (function tick() {
      var prev = b;
      run(true);                       /* только считает и возвращает out */
      b = lastSnapshot;
      /* Устойчивость — по ВСЕМ узлам сетки, а не только по высоте:
         замер index.html @390 поймал состояние, где высота стояла 620, но
         поиск ещё не был прижат к низу (512 вместо 548) — гонка с
         пересчётом скриптов страницы. */
      function same(a, b2) {
        if (!a || !b2) return false;
        if (Math.abs(a.hero.h - b2.hero.h) >= 0.6) return false;
        if (a.h1Fs !== b2.h1Fs || a.h1Lines !== b2.h1Lines) return false;
        var ks = ['badge', 'h1', 'lead', 'search'];
        for (var i = 0; i < ks.length; i++) {
          var x = a[ks[i]], y = b2[ks[i]];
          if (!!x !== !!y) return false;
          if (x && Math.abs(x.y - y.y) >= 0.6) return false;
        }
        var pa = a.photo, pb2 = b2.photo;
        if (!!pa !== !!pb2) return false;
        if (pa && Math.abs(pa.relY - pb2.relY) >= 0.6) return false;
        return true;
      }
      if (prev && b && same(prev, b)) { emit(JSON.stringify(b)); return; }
      if (++tries > 20) { emit(JSON.stringify(b)); return; }
      setTimeout(tick, 250);
    })();
  }
  var lastSnapshot = null;
  if (document.readyState === 'complete') { settled(); } else { window.addEventListener('load', settled); }
  setTimeout(settled, 1500);
  window.addEventListener('load', function () {
    if (document.fonts && document.fonts.ready) { document.fonts.ready.then(function () { setTimeout(settled, 800); }); }
  });
})();
`;

let dirSeq = 0;

/* Скрипт ПЕРЕД всеми страничными скриптами: shared.js выбирает язык по
   localStorage.ragimoff_lang и с непустым значением уводит страницу на
   /ru/ или /en/. Профиль теперь переиспользуется (создание свежего стоит
   ~7 с на Windows), поэтому язык надо гасить на каждом входе. */
/* Язык страницы ЖЁСТКО фиксируется в localStorage ДО shared.js — иначе
   shared.js уводит копию на /ru/ (сохранённый выбор языка живёт в общем
   профиле, а при пустом navigator.languages включает геолокацию по IP:
   fetch('https://ipapi.co/json/') → 'ru' → location.replace('/ru/…'), и
   замер попадал на 404 вместо страницы). Замер: en/index.html и
   test-wave-elements.html не давали ни одного валидного снимка, а
   index.html @390 в iframe уезжал на /ru/_s…index.html. */
const PRESCRIPT = 'try{localStorage.setItem("ragimoff_lang",___LANG___);}catch(e){}' +
  'window.__hroErrs=[];window.addEventListener("error",function(e){try{window.__hroErrs.push(String((e&&(e.message||e.type))||"err").slice(0,140))}catch(x){}},true);' +
  'window.addEventListener("unhandledrejection",function(e){try{window.__hroErrs.push("rej:"+String((e&&e.reason&&e.reason.message)||e.reason).slice(0,100))}catch(x){}},true);';

/* локальный кэш шрифтов: ссылку на Google Fonts в копии страницы заменяем
   на http://127.0.0.1:8766/__fonts.css (см. font-cache-server.js) */
/* Локальный кэш Google Fonts (см. _tools/font-cache-server.js): с этой
   машины fonts.googleapis.com отвечает ~8 секунд, и замер одной страницы
   выходил 3 минуты (обход 171 страницы — три часа). При AUDIT_FONTCACHE=1
   ссылки в копии страницы заменяются на локальный сервер 127.0.0.1:8776. */
const crypto = require('crypto');
function fcHash(u) { return crypto.createHash('md5').update(u).digest('hex'); }
function rewriteFonts(html, on) {
  if (!on) return html;
  const P = process.env.AUDIT_FONTCACHE_PORT || '8776';
  html = html.replace(/https:\/\/fonts\.googleapis\.com\/css2\?[^"'`)\s<>]+/g, function (u) {
    return 'http://127.0.0.1:' + P + '/fc/' + fcHash(u.replace(/&amp;/g, '&')) + '.css';
  });
  html = html.replace(/https:\/\/fonts\.gstatic\.com\/[^"'`)\s<>)]+/g, function (u) {
    return 'http://127.0.0.1:' + P + '/fc/' + fcHash(u) + '.woff2';
  });
  return html;
}

const FONTS_LINK = 'http://127.0.0.1:8766/__fonts.css';

function withProbe(rel) {
  const src = path.join(ROOT, rel);
  const dir = path.dirname(src);
  const tmp = path.join(dir, '_s.' + process.pid + '.' + (++dirSeq) + '.' + path.basename(src));
  let html = fs.readFileSync(src, 'utf8');
  const lang = /(^|[\/])ru[\/]/.test(rel) ? 'ru' : (/(^|[\/])en[\/]/.test(rel) ? 'en' : 'az');
  html = html.replace(/<head([^>]*)>/i,
    '<head$1><script>' + PRESCRIPT.replace('___LANG___', '"' + lang + '"') + '</script>');
  /* кэш шрифтов: каждая ссылка — на свой файл по хешу URL
     (один __fonts.css на все страницы давал чужой набор семейств) */
  html = rewriteFonts(html, !process.env.HERO_NO_FONTCACHE);
  html = html.replace(/<\/body>/i, '<script>' + PROBE + '</script></body>');
  if (html.indexOf('__hro_out') === -1) html += '<script>' + PROBE + '</script>';
  fs.writeFileSync(tmp, html, 'utf8');
  return tmp;
}

function measureOnce(rel, width, height, profileDir) {
  return new Promise((resolve) => {
    const tmp = withProbe(rel);
    const relTmp = path.relative(ROOT, tmp).replace(/\\/g, '/');
    /* Окно Chrome на Windows не бывает уже 500 px: --window-size=390 даёт
       innerWidth 500 (проверено и в --headless=new, и в --headless=old).
       Узкую ширину меряем в обёртке: iframe нужной ширины, страница живёт
       во фрейме, результат пишется в документ-верхушку (см. emit). */
    let url, wrapper = null, winW = width;
    if (width < 500) {
      const wtmp = path.join(ROOT, '_s.w.' + process.pid + '.' + (++dirSeq) + '.html');
      fs.writeFileSync(wtmp,
        '<!DOCTYPE html><html><head><meta charset="utf-8"><title>narrow</title>' +
        '<style>html,body{margin:0;padding:0;background:#07090E}#f{width:' + width +
        'px;height:1000px;border:0;display:block}</style>' +
        '</head><body><iframe id="f" src="' + encodeURI(relTmp) + '"></iframe></body></html>', 'utf8');
      wrapper = wtmp;
      url = 'http://127.0.0.1:' + PORT + '/' + encodeURI(path.relative(ROOT, wtmp).replace(/\\/g, '/'));
      winW = 520;
    } else {
      url = 'http://127.0.0.1:' + PORT + '/' + encodeURI(relTmp);
    }
    const userDir = profileDir || (TMPBASE + '/chrome-s' + process.pid + '-' + (dirSeq) + '-' + Math.floor(Math.random() * 1e6));
    const args = [
      '--headless=new', '--disable-gpu', '--no-sandbox', '--disable-extensions',
      '--lang=az', '--accept-lang=az',
      '--user-data-dir=' + userDir,
      /* ipapi.co — заглушка: иначе shared.js делает внешний запрос геолокации
         (и по IP уводит копию на /ru/), плюс это лишние секунды загрузки */
      '--host-resolver-rules=MAP ipapi.co 127.0.0.1:9',
      '--virtual-time-budget=12000',
      '--window-size=' + winW + ',' + (height || 1600),
      '--dump-dom', url
    ];
    /* timeout обязателен: без него зависший Chrome останавливает весь
       пакетный обход — node ждёт ответа бесконечно */
    execFile(CHROME, args, { encoding: 'utf8', maxBuffer: 1 << 28, timeout: 300000, killSignal: 'SIGKILL' }, (err, stdout) => {
      try { fs.unlinkSync(tmp); } catch (e) {}
      if (wrapper) { try { fs.unlinkSync(wrapper); } catch (e) {} }
      if (!profileDir) { try { fs.rmSync(userDir, { recursive: true, force: true }); } catch (e) {} }
      if (err) { resolve({ error: (String(err.message || err) + ' | signal=' + (err.signal || '-') + ' code=' + (err.code || '-') + ' killed=' + (err.killed || '-')).slice(0, 200) }); return; }
      const block = stdout.match(/<pre id="__hro_out">([\s\S]*?)<\/pre>/);
      if (!block) { resolve({ error: 'no __hro_out in dump' }); return; }
      const lines = block[1].split('\n').map(s => s.trim()).filter(Boolean);
      const snaps = [];
      for (const ln of lines) {
        try { snaps.push(JSON.parse(Buffer.from(ln, 'base64').toString('utf8'))); } catch (e) {}
      }
      if (!snaps.length) { resolve({ error: 'bad json' }); return; }
      resolve({ snaps });
    });
  });
}

/* Готовый замер — последний снимок при условии, что он СОГЛАСУЕТСЯ с
   предыдущим по высоте блока (±1.5 px) и не является известным «до-CSS»
   состоянием (min-height 452/532 из gtc.css). Иначе страница мерилась в
   момент, когда стили/шрифты ещё доехали, — повторяем замер. */
async function measure(rel, width, height, profileDir, attempts, requireFit) {
  attempts = attempts || 3;
  let lastErr = null;
  for (let a = 0; a < attempts; a++) {
    const r = await measureOnce(rel, width, height, profileDir);
    if (r.error) { lastErr = r.error; continue; }
    const snaps = r.snaps
      .filter(d => d && d.hero && d.minH !== '452px' && d.minH !== '532px'
                && d.st === 'complete' && (d.fonts === 'loaded' || d.fonts === 'n/a')
                /* «до»: фиттер подгоняет кегль H1 инлайном; снимок без него —
                   промежуточное состояние (замер tehsil: 400 вместо 458) */
                && (!requireFit || /font-size/.test(d.h1Inline || '')))
      .sort((x, y) => (y.ts || 0) - (x.ts || 0));
    if (!snaps.length) { lastErr = 'no valid snapshot'; continue; }
    const good = snaps[0], prev = snaps[1];
    if (prev && Math.abs(good.hero.h - prev.hero.h) > 1.5) {
      lastErr = 'unstable: ' + prev.hero.h + ' -> ' + good.hero.h;
      continue;
    }
    good.file = rel; good.width = width; good.attempts = a + 1;
    return good;
  }
  return { file: rel, width, error: lastErr || 'failed' };
}

async function pool(items, size, fn) {
  const out = new Array(items.length);
  let idx = 0;
  async function worker(slot) {
    while (idx < items.length) {
      const i = idx++;
      /* у каждого воркера СВОЙ постоянный профиль: создание свежего профиля
         на Windows стоит ~7 с на запуск (замер: 11.2 с против 3.8 с) */
      /* порт в имени профиля обязателен: два обхода (до и после) идут
         параллельно на разных серверах и с одинаковым числом воркеров —
         общий профиль давал блокировку и каскад «Command failed» */
      const profile = TMPBASE + '/hero-prof-' + PORT + '-' + size + '-' + slot;
      out[i] = await fn(items[i], profile);
      process.stderr.write('.');
    }
  }
  await Promise.all(Array.from({ length: Math.min(size, items.length) }, (_, k) => worker(k)));
  process.stderr.write('\n');
  return out;
}

(async () => {
  const argv = process.argv.slice(2);
  let width = 1440, height = 1600, jobs = 6, outFile = null, listFile = null, requireFit = 1;
  const pages = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--width') width = parseInt(argv[++i], 10);
    else if (a === '--height') height = parseInt(argv[++i], 10);
    else if (a === '--jobs') jobs = parseInt(argv[++i], 10);
    else if (a === '--out') outFile = argv[++i];
    else if (a === '--list') listFile = argv[++i];
    else if (a === '--require-fit') requireFit = parseInt(argv[++i], 10);
    else pages.push(a);
  }
  let list = pages;
  if (listFile) {
    list = fs.readFileSync(listFile, 'utf8').split(/\r?\n/).map(s => s.trim()).filter(Boolean);
  }
  /* Прогрев профилей: на холодном профиле первая загрузка медленнее, и
     страница успевает «застрять» в промежуточном состоянии (замер index.html:
     827 вместо 521). Один холостой замер на воркера — и профили горячие. */
  const warmPage = list.find(p => /(^|\/)index\.html$/.test(p)) || list[0];
  await pool(Array.from({ length: jobs }, () => warmPage), jobs, (p, profile) => measure(p, width, height, profile, 1, requireFit));
  const res = await pool(list, jobs, (p, profile) => measure(p, width, height, profile, 3, requireFit));
  if (outFile) fs.writeFileSync(outFile, JSON.stringify(res, null, 1), 'utf8');
  else console.log(JSON.stringify(res, null, 1));
})();
