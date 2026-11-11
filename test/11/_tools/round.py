"""Круг проверки главной по канону: замеры во всех сочетаниях (язык × тема × окно) и снимки блоков для критиков.
Запуск: python round.py NN [база=http://127.0.0.1:8812/test/11/]   → _agent/shots/krug-NN/ (снимки, zamery.json)
Нужен локальный сервер из корня сайта: python -m http.server 8812"""
import asyncio, json, sys, subprocess, base64, time, urllib.request, tempfile, pathlib
import websockets

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
NN = sys.argv[1]
BASE = sys.argv[2] if len(sys.argv) > 2 else 'http://127.0.0.1:8812/test/11/'
OUT = pathlib.Path(__file__).resolve().parents[1] / '_agent' / 'shots' / ('krug-' + NN)
OUT.mkdir(parents=True, exist_ok=True)
LANGS, THEMES, WIDTHS = ['az', 'ru', 'en'], ['night', 'paper', 'sepia'], [(1440, 900), (1366, 768), (390, 844), (320, 640)]
SHOTS = [('ru', 'night'), ('az', 'paper'), ('en', 'sepia')]          # снимки: каждая тема и каждый язык по разу
SHOT_W = [(1440, 900), (390, 844)]
SECS = ['#spec', '#books', '#edu', '#cons', '#corp', '#enl', '#blog', '#tg', '.foot']

MEASURE = r"""
(() => {
  const bad = [], info = {};
  const vis = e => { const r = e.getBoundingClientRect(), s = getComputedStyle(e); return r.width > 1 && r.height > 1 && s.visibility !== 'hidden' && s.display !== 'none' && +s.opacity > .05; };
  const lines = e => Math.round(e.getBoundingClientRect().height / parseFloat(getComputedStyle(e).lineHeight));
  const txt = e => (e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40);
  const W = innerWidth, de = document.documentElement;
  // N3 выход за край
  if (de.scrollWidth > W + 1) bad.push(['N3', 'горизонтальная прокрутка: ширина страницы ' + de.scrollWidth + ' при окне ' + W]);
  document.querySelectorAll('header.head *, .cine__copy *, .sh *, .people *, .topics *, .nums *, .myths *, .posts *, .tg *, .foot *, .mob *').forEach(e => {
    if (!vis(e) || e.closest('[data-rib-track],.belt,.shelf')) return; const r = e.getBoundingClientRect();
    if (r.right > W + 1 || r.left < -1) bad.push(['N3', 'за краем: ' + (e.className || e.tagName) + ' «' + txt(e) + '» ' + Math.round(r.left) + '…' + Math.round(r.right)]); });
  // N2 имя в одну строку
  const sign = document.querySelector('.sign'); if (sign) { const l = lines(sign); info.signLines = l; if (l > 1) bad.push(['N2', '«Doctor Ragimoff» в ' + l + ' строки']); }
  // N3: подпись героя и кнопки героя — по ширине текста, даже пока скрыты
  document.querySelectorAll('.cine__school, .sign, .cine__btns').forEach(e => { const r = document.createRange(); r.selectNodeContents(e); const b = r.getBoundingClientRect(); if (b.width > W - 16) bad.push(['N3', 'шире экрана: ' + e.className + ' ' + Math.round(b.width) + ' при окне ' + W]); });
  // 10.29: один вес и шрифт у всех кнопок
  const bw = new Set(); document.querySelectorAll('.btn, .head__cta, .cine__btns a').forEach(e => { const s = getComputedStyle(e); bw.add(s.fontFamily.split(',')[0] + ' ' + s.fontWeight + ' ' + s.fontSize); }); if (bw.size > 1) bad.push(['10.29', 'кнопки разные: ' + [...bw].join(' | ')]);
  // N6 / 10.18 заголовки и подзаголовки; 10.13 / 10.14 математика отступов
  document.querySelectorAll('section.sec').forEach(sec => {
    const h = sec.querySelector('.sh__h'), s = sec.querySelector('.sh__s'); if (!h) return;
    const fs = parseFloat(getComputedStyle(h).fontSize), hl = lines(h), id = sec.id;
    if (hl > 2) bad.push(['N6', id + ': заголовок в ' + hl + ' строки «' + txt(h) + '»']);
    if (s && vis(s)) { const sl = lines(s); if (sl > 2) bad.push(['N6', id + ': подзаголовок в ' + sl + ' строки «' + txt(s) + '»']);
      const gap = s.getBoundingClientRect().top - h.getBoundingClientRect().bottom; if (Math.abs(gap - fs / 2) > 6) bad.push(['10.14', id + ': заголовок→подзаголовок ' + Math.round(gap) + ' px при кегле ' + Math.round(fs) + ' (нужно ' + Math.round(fs / 2) + ')']);
      if (s.getBoundingClientRect().width > h.closest('.sh').getBoundingClientRect().width + 1) bad.push(['10.18', id + ': подзаголовок шире шапки блока']); }
    const top = h.getBoundingClientRect().top - sec.getBoundingClientRect().top; if (Math.abs(top - fs) > 8 && !sec.matches('.sec--rib')) bad.push(['10.13', id + ': до заголовка ' + Math.round(top) + ' px при кегле ' + Math.round(fs)]);
    const sh = h.closest('.sh'), nx = sh && sh.nextElementSibling; if (nx && vis(nx)) { const after = nx.getBoundingClientRect().top - sh.getBoundingClientRect().bottom; if (Math.abs(after - fs) > 8) bad.push(['10.13', id + ': после группы заголовка ' + Math.round(after) + ' px при кегле ' + Math.round(fs)]); }
  });
  // N7 равная высота в рядах
  [['#people', 'специалисты'], ['#progs', 'программы'], ['#nums', 'числа'], ['#myths', 'мифы'], ['#posts', 'блог']].forEach(([q, n]) => {
    const p = document.querySelector(q); if (!p) return; const rows = {};
    [...p.children].filter(vis).forEach(c => { const r = c.getBoundingClientRect(); (rows[Math.round(r.top / 8)] = rows[Math.round(r.top / 8)] || []).push(Math.round(r.height)); });
    const rr = Object.values(rows); rr.forEach(a => { if (Math.max(...a) - Math.min(...a) > 2) bad.push(['N7', n + ': разная высота в ряду ' + a.join('/')]); });
    if (rr.length > 1 && q !== '#progs') { const c = rr.map(a => a.length); if (new Set(c).size > 1 && c[c.length - 1] !== c[0]) bad.push(['N7', n + ': неполный ряд ' + c.join('-')]); } });
  // N12 контраст
  const rgb = c => { const m = (c.match(/[\d.]+/g) || []).map(Number); if (/^color\(/.test(c)) { const a = m.slice(0, 3).map(v => v * 255); if (m.length > 3) a.push(m[3]); return a; } return m.length ? m : [0, 0, 0, 0]; };
  const lum = c => { const a = c.slice(0, 3).map(v => { v /= 255; return v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; }); return .2126 * a[0] + .7152 * a[1] + .0722 * a[2]; };
  const bgOf = e => { for (let n = e; n; n = n.parentElement) { const c = rgb(getComputedStyle(n).backgroundColor); if (c.length < 4 || c[3] > .9) { if (c[0] + c[1] + c[2] > 0 || c.length < 4 || c[3] > .9) return c; } } return rgb(getComputedStyle(de).getPropertyValue('--bg') ? getComputedStyle(document.body).backgroundColor : 'rgb(0,0,0)'); };
  const seen = new Set();
  document.querySelectorAll('.sec p, .sec li, .sec a, .sec span, .sec h2, .sec h3, .foot *, .nav a').forEach(e => {
    if (!vis(e) || e.closest('.cine, .head.on-dark, .myth:not(.is-flip) .myth__b, .myth.is-flip .myth__f') || ![...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return;
    const s = getComputedStyle(e), fg = rgb(s.color), bg = bgOf(e), L1 = lum(fg), L2 = lum(bg), k = (Math.max(L1, L2) + .05) / (Math.min(L1, L2) + .05), big = parseFloat(s.fontSize) >= 24;
    if (k < (big ? 3 : 4.5)) { const key = (e.className || e.tagName) + k.toFixed(1); if (!seen.has(key)) { seen.add(key); bad.push(['N12', 'контраст ' + k.toFixed(1) + ' у ' + (e.className || e.tagName) + ' «' + txt(e) + '»']); } } });
  // 10.1 гарнитуры; 10.4 кегль текста; 10.30 зона нажатия
  const fam = {}; document.querySelectorAll('body *').forEach(e => { if (vis(e) && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) { const f = getComputedStyle(e).fontFamily.split(',')[0].replace(/["']/g, '').trim(); fam[f] = (fam[f] || 0) + 1; } });
  info.fonts = fam; if (Object.keys(fam).length > 4) bad.push(['10.1', 'гарнитур больше четырёх: ' + Object.keys(fam).join(', ')]);
  const small = new Set(); document.querySelectorAll('.sec p, .sec li').forEach(e => { if (vis(e)) { const f = parseFloat(getComputedStyle(e).fontSize); if (f < (W < 700 ? 15 : 15.5)) small.add((e.className || e.tagName) + ' ' + f); } });
  small.forEach(v => bad.push(['10.4', 'мелкий текст: ' + v + ' px']));
  if (W < 700) { const t = new Set(); document.querySelectorAll('a, button').forEach(e => { if (!vis(e) || e.closest('.mob')) return; const r = e.getBoundingClientRect(); if (r.height < 40 && r.width < 200 && !e.closest('p,li.topic')) t.add((e.className || e.id || e.tagName) + ' ' + Math.round(r.width) + '×' + Math.round(r.height)); }); t.forEach(v => bad.push(['10.30', 'зона нажатия меньше 44: ' + v])); }
  // 11.4 битые картинки; 2.1 меню
  const br = [...document.images].filter(i => i.getAttribute('src') && i.complete && !i.naturalWidth).map(i => i.src.split('/').pop()); if (br.length) bad.push(['11.4', 'битые картинки: ' + br.join(', ')]);
  info.menu = [...document.querySelectorAll('#nav > *')].map(e => (e.querySelector('a,button') || e).textContent.trim().split('\n')[0].trim());
  info.order = [...document.querySelectorAll('main > section, main > div.belt')].map(e => e.id || e.className);
  info.cards = { people: document.querySelectorAll('#people > *').length, books: document.querySelectorAll('#shelf > *').length, progs: document.querySelectorAll('#progs > *').length, topics: document.querySelectorAll('#topics > *').length, myths: document.querySelectorAll('#myths > *').length, posts: document.querySelectorAll('#posts > *').length };
  info.links = [...new Set([...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')))].filter(h => h && !h.startsWith('#'));
  return { bad, info };
})()
"""


AZ_LETTERS = r"""
(async () => {
  const chars = ['Ə', 'ə', 'İ', 'ı', 'Ş', 'ş', 'Ğ', 'ğ', 'Ç', 'ç', 'Ö', 'ö', 'Ü', 'ü', 'Ж', 'я'];
  const fams = new Set(); document.querySelectorAll('body *').forEach(e => { const r = e.getBoundingClientRect(); if (r.width > 1 && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) fams.add(getComputedStyle(e).fontFamily.split(',')[0].replace(/["']/g, '').trim()); });
  const out = [];
  for (const f of fams) { for (const w of ['300', '400', '500', '600']) { try { await document.fonts.load(w + ' 40px "' + f + '"', chars.join('')); } catch (e) {} } }
  await new Promise(r => setTimeout(r, 1200));
  const c = document.createElement('canvas').getContext('2d'); const w = (f, ch) => { c.font = '40px ' + f; return c.measureText(ch).width; };
  for (const f of fams) { const hand = /Monsieur/.test(f); const m = chars.filter(ch => !(hand && /[Жя]/.test(ch)) && Math.abs(w('"' + f + '", monospace', ch) - w('"' + f + '", serif', ch)) > .01); if (m.length && !hand) out.push('в гарнитуре ' + f + ' нет букв: ' + m.join(' ')); }
  return out;
})()
"""


async def main():
    prof = tempfile.mkdtemp()
    p = subprocess.Popen([CHROME, '--headless=new', '--remote-debugging-port=9398', '--user-data-dir=' + prof, '--hide-scrollbars', '--window-size=1440,900', 'about:blank'],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ws_url = None
    for _ in range(60):
        try:
            tabs = json.load(urllib.request.urlopen('http://127.0.0.1:9398/json'))
            ws_url = [t for t in tabs if t['type'] == 'page'][0]['webSocketDebuggerUrl']; break
        except Exception:
            time.sleep(.2)
    report, errors = {}, []
    async with websockets.connect(ws_url, max_size=80_000_000) as ws:
        n = [0]

        async def cmd(m, **pr):
            n[0] += 1; i = n[0]
            await ws.send(json.dumps({'id': i, 'method': m, 'params': pr}))
            while True:
                r = json.loads(await ws.recv())
                if r.get('method') == 'Runtime.exceptionThrown':
                    d = r['params']['exceptionDetails']; errors.append((d.get('text') or '') + ' ' + ((d.get('exception') or {}).get('description') or '')[:200])
                if r.get('id') == i:
                    return r.get('result', {})

        async def ev(expr):
            return (await cmd('Runtime.evaluate', expression=expr, returnByValue=True, awaitPromise=True)).get('result', {}).get('value')

        await cmd('Page.enable'); await cmd('Runtime.enable')
        for (W, H) in WIDTHS:
            await cmd('Emulation.setDeviceMetricsOverride', width=W, height=H, deviceScaleFactor=1, mobile=W < 700)
            for lg in LANGS:
                for th in THEMES:
                    await cmd('Page.navigate', url=BASE + 'index.html')
                    await asyncio.sleep(.6)
                    await ev("localStorage.setItem('r11_lang','%s');localStorage.setItem('r11_theme','%s');1" % (lg, th))
                    await cmd('Page.navigate', url=BASE + 'index.html?k=%s%s%d' % (lg, th, W))
                    await asyncio.sleep(3.0)
                    await ev("document.querySelectorAll('.rv').forEach(e=>e.classList.add('is-in'));1")
                    await asyncio.sleep(1.5)                                  # дождаться конца появления: замер после движения
                    key = '%s|%s|%d' % (lg, th, W)
                    res = await ev(MEASURE) or {'bad': [['?', 'замер не выполнен']], 'info': {}}
                    if lg == 'az' and th == 'night':                             # N4: все буквы азербайджанского алфавита и кириллица есть в каждой гарнитуре страницы
                        miss = await ev(AZ_LETTERS)
                        for m in (miss or []):
                            res['bad'].append(['N4', m])
                    report[key] = res
                    print(key, 'нарушений', len(res['bad']))
                    if (lg, th) in SHOTS and (W, H) in SHOT_W:
                        tag = '%s-%s-%d' % (lg, th, W)
                        hh = await ev("document.querySelector('#hero').offsetHeight")
                        for k, fr in enumerate([0, .35, .7, .97]):          # герой: четыре момента движения
                            await ev('scrollTo(0,%f)' % ((hh - H) * fr)); await asyncio.sleep(1.4)
                            s = await cmd('Page.captureScreenshot', format='jpeg', quality=68)
                            (OUT / ('%s_hero%d.jpg' % (tag, k))).write_bytes(base64.b64decode(s['data']))
                        for q in SECS:
                            top = await ev("(()=>{const e=document.querySelector(%r);return e?e.getBoundingClientRect().top+scrollY:0})()" % q)
                            hsec = await ev("(()=>{const e=document.querySelector(%r);return e?e.offsetHeight:0})()" % q)
                            parts = 1 if hsec <= H * 1.15 else min(4, int(hsec / H) + 1)
                            for part in range(parts):
                                y = top - (70 if part == 0 else 0) + part * (H - 90)
                                cur = await ev('scrollY')
                                for st in range(1, 9):
                                    await ev('scrollTo(0,%f)' % (cur + (y - cur) * st / 8)); await asyncio.sleep(.05)
                                await asyncio.sleep(1.3)
                                s = await cmd('Page.captureScreenshot', format='jpeg', quality=68)
                                (OUT / ('%s_%s%s.jpg' % (tag, q.strip('#.'), '' if parts == 1 else '_%d' % (part + 1)))).write_bytes(base64.b64decode(s['data']))
                        if W < 700:                                          # мобильное меню
                            await ev("scrollTo(0,0);document.querySelector('.burger')&&document.querySelector('.burger').click();1"); await asyncio.sleep(1.0)
                            s = await cmd('Page.captureScreenshot', format='jpeg', quality=68)
                            (OUT / ('%s_menu.jpg' % tag)).write_bytes(base64.b64decode(s['data']))
    p.terminate()
    # проверка ссылок (один раз, по русской версии)
    links = set()
    for k, v in report.items():
        for h in v.get('info', {}).get('links', []):
            links.add((k.split('|')[0], h))
    dead = []
    for lg, h in sorted(links):
        if h.startswith(('http://', 'https://', 'mailto:', 'tel:')):
            continue
        u = urllib.request.urljoin(BASE, h.split('#')[0])
        try:
            urllib.request.urlopen(u, timeout=15)
        except Exception as e:
            dead.append('%s: %s → %s' % (lg, h, str(e)[:60]))
    summary = {}
    for k, v in report.items():
        for cid, msg in v['bad']:
            summary.setdefault(cid + ' | ' + msg, []).append(k)
    out = {'errors_js': sorted(set(errors)), 'dead_links': sorted(set(dead)), 'violations': {m: (ks if len(ks) < 12 else ['во всех или почти всех сочетаниях: %d из %d' % (len(ks), len(report))] + ks[:4]) for m, ks in sorted(summary.items())},
           'info_ru_1440': report.get('ru|night|1440', {}).get('info', {}), 'info_az_390': report.get('az|night|390', {}).get('info', {})}
    for d in (out['info_ru_1440'], out['info_az_390']):
        d.pop('links', None)
    (OUT / 'zamery.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print('сочетаний', len(report), '| разных нарушений', len(summary), '| битых ссылок', len(dead), '| ошибок JS', len(set(errors)), '->', OUT)

asyncio.run(main())
