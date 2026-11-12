"""Страница программы обучения: шаблон program.html, стили, подписи на трёх языках, выбор программы в форме. Запуск из test/11."""
import io, re

# ── шаблон: шапка и подвал — те же, что на главной (берём разметку из index.html, чтобы не расходились)
idx = io.open('index.html', encoding='utf-8').read()
head = idx[:idx.index('</head>')]
head = re.sub(r'<link rel="preload" as="image"[^>]*>\n', '', head)
head = re.sub(r'<script type="importmap">.*?</script>\n', '', head, flags=re.S)
head = re.sub(r'<title>.*?</title>', '<title>Doctor Ragimoff</title>', head)
hdr = idx[idx.index('<header class="head"'):idx.index('<main id="top">')]
hdr = hdr.replace('href="#top"', 'href="index.html"').replace('id="headCta" href="#reg" data-reg="consult"', 'id="headCta" href="#reg"')
foot = idx[idx.index('<footer class="foot">'):idx.index('</footer>') + len('</footer>')]
fab = idx[idx.index('<a class="fab"'):idx.index('</a>', idx.index('<a class="fab"')) + 4]
page = head + '''</head>
<body class="inner">
''' + hdr + '''<main id="top" class="pp">
  <section class="pp__hero"><div class="wrap">
    <a class="pp__back" id="ppBack"></a>
    <p class="pp__kind" id="ppKind"></p>
    <h1 class="pp__t" id="ppT"></h1>
    <p class="pp__lead" id="ppLead"></p>
    <dl class="pp__facts" id="ppFacts"></dl>
    <p class="pp__cta"><a class="btn" href="#reg" id="ppGo"></a></p>
  </div></section>
  <section class="sec" id="for"><div class="wrap pp__two"><h2 class="pp__h rv" id="hFor"></h2><ul class="facts pp__list rv" id="ppFor"></ul></div></section>
  <section class="sec" id="teach"><div class="wrap pp__two"><h2 class="pp__h rv" id="hTeach"></h2><div class="tchs" id="ppTeach"></div></div></section>
  <section class="sec" id="inc"><div class="wrap pp__two"><h2 class="pp__h rv" id="hInc"></h2><ul class="facts pp__list rv" id="ppInc"></ul></div></section>
  <section class="sec" id="prog"><div class="wrap pp__two"><h2 class="pp__h rv" id="hProg"></h2><div class="accs" id="ppProg"></div></div></section>
  <section class="sec" id="doc"><div class="wrap pp__two"><h2 class="pp__h rv" id="hDoc"></h2><div class="doc rv" id="ppDoc"></div></div></section>
  <section class="sec" id="faq"><div class="wrap pp__two"><h2 class="pp__h rv" id="hFaq"></h2><div class="accs" id="ppFaq"></div></div></section>
  <section class="sec" id="price"><div class="wrap pp__two"><h2 class="pp__h rv" id="hPrice"></h2><div class="prices rv"><div id="ppPrice"></div><p class="pp__cta"><a class="btn" href="#reg" id="ppGo2"></a></p></div></div></section>
  <section class="sec" id="reg"><div class="wrap"><header class="sh"><h2 class="sh__h rv" id="regH"></h2><p class="sh__s rv" id="regS"></p></header><div class="reg" id="regBox"></div></div></section>
  <section class="sec sec--soc"><div class="wrap"><nav class="pp__other rv" id="ppOther"></nav><div class="soc rv"><p class="soc__h" id="socH"></p><ul class="soc__l" id="socList"></ul></div></div></section>
</main>

''' + foot + '''

<div class="lb" id="lb" aria-hidden="true"><button type="button" class="lb__x" aria-label="×">×</button><figure><img id="lbImg" alt=""><figcaption id="lbCap"></figcaption></figure></div>

''' + fab + '''

<script type="module" src="assets/js/page-program.js"></script>
</body>
</html>
'''
io.open('program.html', 'w', encoding='utf-8', newline='\n').write(page)

CSS = """
/* ═══ страница программы обучения — один шаблон на все программы ═══ */
.inner { background: var(--bg); }
.pp__hero { padding: calc(var(--hd86) + var(--r2)) 0 0; }
.pp__back { display: inline-flex; align-items: center; min-height: var(--tap); font: 600 14px/1 var(--f-sub); color: var(--gold-hi); letter-spacing: .02em; }
.pp__kind { margin-top: var(--r1); font: 600 12.5px/1.3 var(--f-sub); letter-spacing: .24em; text-transform: uppercase; color: var(--gold); }
.pp__t { margin-top: var(--s2); font: 300 clamp(40px, 6vw, 92px)/1.02 var(--f-display); letter-spacing: -.015em; color: var(--milk); max-width: 16ch; text-wrap: balance; }
.pp__lead { margin-top: var(--r2); max-width: 62ch; font: 400 clamp(19px, 1.55vw, 23px)/1.5 var(--f-read); color: var(--milk); opacity: .9; text-wrap: pretty; }
.pp__facts { margin-top: var(--r3); display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 0; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); }
.fact { padding: var(--r1) var(--r1) var(--r1) 0; display: flex; flex-direction: column; gap: var(--s1); } .fact + .fact { padding-left: var(--r1); border-left: 1px solid var(--line); }
.fact dt { font: 600 12px/1.3 var(--f-sub); letter-spacing: .18em; text-transform: uppercase; color: var(--smoke); } .fact dd { margin: 0; font: 400 clamp(19px, 1.5vw, 23px)/1.25 var(--f-display); color: var(--milk); font-variant-numeric: lining-nums; }
.pp__cta { margin-top: var(--r2); }
.pp__two { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 2fr); gap: var(--r3); align-items: start; }
.pp__h { font: 300 clamp(30px, 3.4vw, 52px)/1.05 var(--f-display); color: var(--milk); position: sticky; top: calc(var(--hd86) + var(--p8)); }
.pp__list li { font-size: 18px; } .pp .facts li { min-height: 0; padding: var(--p14) 0 var(--p14) var(--p28); }
.tchs { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--r1); }
.tch { display: flex; align-items: center; gap: var(--r1); padding: var(--r1); border-radius: var(--rad); background: var(--layer); border: 1px solid var(--line); transition: border-color var(--t1), transform var(--t2) var(--e); }
.tch:hover { border-color: color-mix(in srgb, var(--gold) 60%, transparent); transform: translateY(-3px); }
.tch__ph { flex: 0 0 76px; width: 76px; height: 76px; border-radius: 50%; overflow: hidden; } .tch__ph img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 14%; filter: grayscale(1) sepia(.2) contrast(1.05); }
.tch__b { display: flex; flex-direction: column; gap: var(--s1); min-width: 0; } .tch__b b { font: 400 clamp(22px, 1.8vw, 27px)/1.1 var(--f-display); color: var(--milk); } .tch__b span { font: 400 16px/1.4 var(--f-read); color: var(--text); }
.accs { display: flex; flex-direction: column; border-top: 1px solid var(--line); }
.acc { border-bottom: 1px solid var(--line); } .acc summary { list-style: none; display: flex; align-items: center; justify-content: space-between; gap: var(--r1); min-height: 64px; padding: var(--p12) 0; cursor: pointer; font: 400 clamp(20px, 1.6vw, 25px)/1.2 var(--f-display); color: var(--milk); }
.acc summary::-webkit-details-marker { display: none; }
.acc summary i { flex: 0 0 var(--tap); width: var(--tap); height: var(--tap); border-radius: 50%; border: 1px solid var(--line); position: relative; transition: transform var(--t1) var(--e), border-color var(--t1); }
.acc summary i::before, .acc summary i::after { content: ""; position: absolute; left: 50%; top: 50%; width: 13px; height: 1.5px; margin: -.75px 0 0 -6.5px; background: var(--gold); } .acc summary i::after { transform: rotate(90deg); transition: transform var(--t1) var(--e); }
.acc[open] summary i { border-color: var(--gold); } .acc[open] summary i::after { transform: rotate(0deg); }
.acc ul { padding: 0 0 var(--r1); display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--p8) var(--r2); } .acc li { position: relative; padding-left: var(--p20); font: 400 17px/1.45 var(--f-read); color: var(--text); }
.acc li::before { content: ""; position: absolute; left: 0; top: .72em; width: 10px; height: 1px; background: var(--gold); }
.acc p { padding: 0 var(--r3) var(--r1) 0; max-width: 66ch; font: 400 17px/1.6 var(--f-read); color: var(--text); }
.doc { display: grid; grid-template-columns: minmax(0, 1.1fr) minmax(0, 1fr); gap: var(--r2); align-items: center; }
.doc__t { font: 400 clamp(24px, 2.1vw, 32px)/1.12 var(--f-display); color: var(--milk); } .doc__d { margin-top: var(--p12); font: 400 17px/1.6 var(--f-read); color: var(--text); }
.doc__i { display: flex; flex-direction: column; gap: var(--p10); text-align: left; cursor: zoom-in; } .doc__i img { width: 100%; height: auto; border-radius: var(--p12); border: 1px solid var(--line); background: #fff; }
.doc__i span { font: 600 13px/1 var(--f-sub); letter-spacing: .14em; text-transform: uppercase; color: var(--gold); }
.prices { display: flex; flex-direction: column; } .prow { display: flex; align-items: baseline; justify-content: space-between; gap: var(--r2); padding: var(--p16) 0; border-bottom: 1px solid var(--line); } .prow:first-child { border-top: 1px solid var(--line); }
.prow span { font: 400 18px/1.4 var(--f-read); color: var(--text); } .prow b { font: 400 clamp(24px, 2.1vw, 32px)/1.1 var(--f-display); color: var(--gold-hi); white-space: nowrap; font-variant-numeric: lining-nums; }
.pnote { margin-top: var(--r1); max-width: 62ch; font: 400 16px/1.55 var(--f-read); color: var(--text); }
.pp__other { display: flex; flex-wrap: wrap; align-items: center; gap: var(--p8) var(--r1); margin-bottom: var(--r2); } .pp__other span { font: 600 12.5px/1.3 var(--f-sub); letter-spacing: .18em; text-transform: uppercase; color: var(--smoke); }
.pp__other a { display: inline-flex; align-items: center; min-height: var(--tap); font: 400 clamp(19px, 1.5vw, 23px)/1.2 var(--f-display); color: var(--milk); border-bottom: 1px solid color-mix(in srgb, var(--gold) 45%, transparent); }
.pp__other a:hover { color: var(--gold-hi); }
.inner .head { background: color-mix(in srgb, var(--bg) 82%, transparent); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); border-bottom: 1px solid var(--line); }
@media (max-width: 900px) { .pp__two { grid-template-columns: 1fr; gap: var(--r1); } .pp__h { position: static; } }
@media (max-width: 760px) {
  .pp__hero { padding-top: calc(var(--hd70) + var(--r1)); } .pp__facts { grid-template-columns: 1fr 1fr; } .fact { padding: var(--p14) var(--p12) var(--p14) 0; } .fact + .fact { padding-left: 0; border-left: 0; } .fact:nth-child(even) { padding-left: var(--p12); border-left: 1px solid var(--line); } .fact:nth-child(n+3) { border-top: 1px solid var(--line); }
  .pp__cta .btn { width: 100%; } .tchs, .doc, .acc ul { grid-template-columns: 1fr; } .acc p { padding-right: 0; } .prow { flex-direction: column; gap: var(--p4); align-items: flex-start; }
}
"""
p = 'assets/css/site.css'
c = io.open(p, encoding='utf-8').read()
if 'страница программы обучения — один шаблон' not in c:
    io.open(p, 'w', encoding='utf-8', newline='\n').write(c + CSS)

p = 'assets/js/content.js'
t = io.open(p, encoding='utf-8').read()
if 'PP_LABELS' not in t:
    t += """
/* ── PP_LABELS: подписи страницы программы (один шаблон на все программы) ── */
const PP = {
  ru: { back: 'Все программы', long: 'Долгосрочная программа', short: 'Краткосрочная программа', forWhom: 'Для кого', teachers: 'Кто ведёт', includes: 'Что входит', program: 'Программа', doc: 'Документ', faq: 'Вопросы и ответы', price: 'Стоимость', reg: 'Пройти регистрацию', sample: 'Образец документа', other: 'Другие программы' },
  az: { back: 'Bütün proqramlar', long: 'Uzunmüddətli proqram', short: 'Qısamüddətli proqram', forWhom: 'Kimlər üçün', teachers: 'Dərsləri kim aparır', includes: 'Nə daxildir', program: 'Proqram', doc: 'Sənəd', faq: 'Suallar və cavablar', price: 'Qiymət', reg: 'Qeydiyyatdan keçin', sample: 'Sənəd nümunəsi', other: 'Digər proqramlar' },
  en: { back: 'All programmes', long: 'Long programme', short: 'Short programme', forWhom: 'Who it is for', teachers: 'Who teaches', includes: 'What is included', program: 'Curriculum', doc: 'Document', faq: 'Questions and answers', price: 'Price', reg: 'Register', sample: 'Sample document', other: 'Other programmes' },
};
for (const l of Object.keys(PP)) T[l].pp = PP[l];
"""
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

# форма: при открытии со страницы программы эта программа уже выбрана
p = 'assets/js/reg.js'
t = io.open(p, encoding='utf-8').read()
a = "export function regOpen(kind, topic) { if (!box) return; const v = keep(); if (kind) st.kind = kind; if (topic != null) st.topic = topic; draw(v); }"
if a in t:
    t = t.replace(a, "export function regOpen(kind, topic, prog) { if (!box) return; const v = keep(); if (kind) st.kind = kind; if (topic != null) st.topic = topic; if (prog != null) st.prog = prog; draw(v); }")
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

# номер версии — и для новой страницы
p = '_tools/stamp.py'
t = io.open(p, encoding='utf-8').read()
if 'program.html' not in t:
    t = t.replace("print('версия'", "import os\nfor pg, js in (('program.html', 'page-program'),):\n    if os.path.exists(pg):\n        x = io.open(pg, encoding='utf-8').read()\n        x = re.sub(r'(assets/css/site\\.css)(\\?v=\\d+)?', r'\\1?v=' + v, x); x = re.sub(r'(assets/js/' + js + r'\\.js)(\\?v=\\d+)?', r'\\1?v=' + v, x)\n        io.open(pg, 'w', encoding='utf-8', newline='\\n').write(x)\nfor js in ('chrome', 'page-program'):\n    f = 'assets/js/' + js + '.js'\n    if os.path.exists(f):\n        x = io.open(f, encoding='utf-8').read()\n        x = re.sub(r\"(from '\\./[a-z-]+\\.js)(\\?v=\\d+)?'\", r\"\\1?v=\" + v + \"'\", x)\n        io.open(f, 'w', encoding='utf-8', newline='\\n').write(x)\nprint('версия'", 1)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('patched')
