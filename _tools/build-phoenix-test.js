/* =====================================================================
   RAGIMOFF · _tools/build-phoenix-test.js
   Онлайн-тест «Карта моделей взаимоотношений» из книги «Эра Феникса».
   Вопросы, шкала, подсчёт и уровни — из самой книги (_tools/phoenix-test.json).
   Собирает: books/phoenix-era/test/index.html (AZ), books/phoenix-era/test/ru/index.html (RU).
   Запуск: node _tools/build-phoenix-test.js
   ===================================================================== */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const DATA = JSON.parse(fs.readFileSync(path.join(__dirname, 'phoenix-test.json'), 'utf8'));

/* уровни зрелости и группы результата — из книги (шаг 4 инструкции по подсчёту) */
const LEVELS = {
  ru: {
    12: ['Феникс', 'Вершина развития — целостность, зрелость, служение'],
    11: ['Хамелеон', 'Адаптация и поиск себя — близко к вершине'],
    10: ['Тереза', 'Служение обществу — высокий уровень'],
    9: ['Гейша', 'Талант и признание — осознанность растёт'],
    8: ['Лилит', 'Ресурс и безопасность — переходный уровень'],
    7: ['Куртизанка', 'Свобода выбора — ещё невротически окрашена'],
    6: ['Хиппи', 'Свобода без ответственности — середина пути'],
    5: ['Любовница', 'Зависимость через любовь — работа продолжается'],
    4: ['Золушка', 'Служение из вины — зависимая позиция'],
    3: ['Путана', 'Бунт и протест — точка начала осознания'],
    2: ['Попрошайка', 'Требование и манипуляция — точка старта'],
    1: ['Инфанта', 'Полная зависимость — исходная точка пути'],
  },
  az: {
    12: ['Feniks', 'İnkişafın zirvəsi — bütünlük, yetkinlik, xidmət'],
    11: ['Buqələmun', 'Adaptasiya və özünü axtarış — zirvəyə yaxın'],
    10: ['Tereza', 'Cəmiyyətə xidmət — yüksək səviyyə'],
    9: ['Geyşa', 'İstedad və tanınma — aydınlanma artır'],
    8: ['Lilit', 'Resurs və təhlükəsizlik — keçid səviyyəsi'],
    7: ['Kurtizan', 'Seçim azadlığı — hələ nevrotik çalarlı'],
    6: ['Hippi', 'Məsuliyyətsiz azadlıq — yolun ortası'],
    5: ['Məşuqə', 'Sevgi vasitəsilə asılılıq — iş davam edir'],
    4: ['Sinderella', 'Günahkarlıqdan xidmət — asılı mövqe'],
    3: ['Putana', 'Üsyan və etiraz — dərkin başlanğıcı'],
    2: ['Dilənçi', 'Tələb və manipulyasiya — başlanğıc nöqtəsi'],
    1: ['İnfanta', 'Tam asılılıq — yolun başlanğıcı'],
  },
};
const GROUPS = {
  ru: {
    low: 'Результаты 1–4: вы находитесь в моделях сильной зависимости. Это точка старта. Осознание — первый шаг к трансформации.',
    mid: 'Результаты 5–8: вы в переходном периоде. Уже есть самостоятельность, но невротические паттерны сохраняются.',
    high: 'Результаты 9–11: вы близки к вершине. Осталось сделать шаг к искренности и целостности.',
    top: 'Результат 12 (Феникс): поздравляем, вы на пути зрелости. Помните: Феникс — это процесс, а не точка прибытия.',
  },
  az: {
    low: 'Nəticələr 1–4: güclü asılılıq modellərindəsiniz. Bu, başlanğıc nöqtəsidir. Dərk — transformasiyanın ilk addımıdır.',
    mid: 'Nəticələr 5–8: keçid dövründəsiniiz. Artıq müstəqillik var, lakin nevrotik nümunələr qalır.',
    high: 'Nəticələr 9–11: zirvəyə yaxınsınız. Səmimiliyə və tamlığa doğru addım atmaq qalır.',
    top: 'Nəticə 12 (Feniks): təbriklər. Yetkinlik yolundasınız. Yadınızda saxlayın: Feniks — prosesdir, varmaq üçün nöqtə deyil.',
  },
};

/* ссылки на главы книги про каждую модель (страницы сгенерированы конвертером) */
const CHAPTER = {
  az: {
    Lilit: '03-li-li-t.html', Putana: '04-putana.html', Hippi: '05-hi-ppi.html', 'Geyşa': '06-geysa.html',
    'Məşuqə': '07-mesuqe.html', Kurtizan: '08-kurti-zan.html', Tereza: '09-tereza.html', 'İnfanta': '10-i-nfanta.html',
    Sinderella: '11-si-nderella.html', 'Dilənçi': '12-di-lenci.html', 'Buqələmun': '13-bolum-11-munasi-bet-modeli-buqelemun.html',
    Feniks: '../index.html',
  },
  ru: {
    'Лилит': '03-glava-3.html', 'Путана': '04-glava-4.html', 'Хиппи': '05-glava-5.html', 'Гейша': '06-glava-6.html',
    'Любовница': '07-glava-7.html', 'Куртизанка': '08-glava-8.html', 'Тереза': '09-glava-9.html', 'Инфанта': '10-glava-10.html',
    'Золушка': '11-glava-11.html', 'Попрошайка': '12-glava-12.html', 'Хамелеон': '14-glava-14.html', 'Феникс': '15-glava-15.html',
  },
};

const UI = {
  az: {
    lang: 'az',
    title: 'Münasibət modellərinin xəritəsi — onlayn test | Feniks Erası',
    desc: '100 sual, 12 model. Onlayn diaqnostik test «Münasibət modellərinin xəritəsi» — Feniks Erası kitabı əsasında.',
    h1: 'Münasibət modellərinin xəritəsi',
    lead: 'Bu test 100 təsdiqdən ibarətdir. Hər təsdiq münasibətlərdə müəyyən davranış modelini əks etdirir. Diqqətlə oxuyun və hazırda sizə nə dərəcədə uyğun olduğunu 1–5 bal ilə qiymətləndirin.',
    scaleTitle: 'Qiymətləndirmə şkalası',
    scale: ['Tamamilə doğru deyil', 'Daha çox doğru deyil', 'Bəzən doğrudur', 'Daha çox doğrudur', 'Tamamilə doğrudur'],
    start: 'Testə başla',
    back: '← Geri',
    next: 'Növbəti',
    of: '/ 100',
    resultTitle: 'Nəticəniz',
    dominant: 'Dominant model',
    avg: 'Orta bal',
    level: 'Güc səviyyəsi',
    allTitle: 'Bütün modellər üzrə orta ballar',
    readMore: 'Model haqqında kitabda oxu →',
    restart: 'Yenidən keç',
    toBook: '← Kitaba qayıt',
    interp: { dom: 'Dominant model — hazırda əsas davranış nümunəniz', sec: 'İkinci dərəcəli model — stresdə özünü göstərir', weak: 'Zəif model — hazırda sizə xas deyil' },
  },
  ru: {
    lang: 'ru',
    title: 'Карта моделей взаимоотношений — онлайн-тест | Эра Феникса',
    desc: '100 утверждений, 12 моделей. Онлайн-тест «Карта моделей взаимоотношений» по книге «Эра Феникса».',
    h1: 'Карта моделей взаимоотношений',
    lead: 'Тест состоит из 100 утверждений. Каждое отражает определённую модель поведения в отношениях. Прочитайте внимательно и оцените, насколько это верно для вас сейчас, по шкале 1–5.',
    scaleTitle: 'Шкала оценки',
    scale: ['Совсем не верно для меня', 'Скорее не верно', 'Иногда верно', 'Скорее верно', 'Полностью верно для меня'],
    start: 'Начать тест',
    back: '← Назад',
    next: 'Далее',
    of: '/ 100',
    resultTitle: 'Ваш результат',
    dominant: 'Доминирующая модель',
    avg: 'Средний балл',
    level: 'Сила архетипа',
    allTitle: 'Средние баллы по всем моделям',
    readMore: 'Прочитать о модели в книге →',
    restart: 'Пройти заново',
    toBook: '← Вернуться к книге',
    interp: { dom: 'Доминирующая модель — ваш основной паттерн сейчас', sec: 'Вторичная модель — проявляется в стрессе', weak: 'Слабая модель — сейчас не характерна' },
  },
};

const BOOK = { az: '/books/phoenix-era/', ru: '/books/phoenix-era/ru/' };
const TEST = { az: '/books/phoenix-era/test/', ru: '/books/phoenix-era/test/ru/' };

function page(code) {
  const ui = UI[code];
  const d = DATA.langs[code];
  const chapters = CHAPTER[code];
  const levels = LEVELS[code];
  /* модель → сила */
  const strength = {};
  Object.entries(levels).forEach(([k, v]) => { strength[v[0]] = +k; });
  const payload = {
    lang: code,
    blocks: d.blocks.map((b) => ({ model: b.model, count: b.questions.length, questions: b.questions.map((q) => q.text) })),
    levels: Object.entries(levels).map(([k, v]) => ({ strength: +k, model: v[0], maturity: v[1] })),
    groups: GROUPS[code],
    chapters,
    book: BOOK[code],
    test: TEST[code],
    scale: ui.scale,
    interp: ui.interp,
    ui: { of: ui.of, back: ui.back, next: ui.next, readMore: ui.readMore, restart: ui.restart, resultTitle: ui.resultTitle, dominant: ui.dominant, avg: ui.avg, level: ui.level, allTitle: ui.allTitle },
  };
  const scaleRows = ui.scale.map((s, i) =>
    '          <tr><td class="t-num">' + (i + 1) + '</td><td>' + s + '</td></tr>').join('\n');
  return `<!doctype html>
<html lang="${code}" data-langs="az,ru" data-lang-url-az="${TEST.az}" data-lang-url-ru="${TEST.ru}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#07090E">
  <title>${ui.title}</title>
  <meta name="description" content="${ui.desc}">
  <link rel="canonical" href="https://ragimoff.org${TEST[code]}">
  <link rel="alternate" hreflang="az" href="https://ragimoff.org${TEST.az}">
  <link rel="alternate" hreflang="ru" href="https://ragimoff.org${TEST.ru}">
  <link rel="icon" href="/favicon.ico">
  <link rel="stylesheet" href="${code === 'ru' ? '/books/phoenix-era/ru/style.css' : '/books/phoenix-era/style.css'}">
  <style>
    .t-wrap{max-width:760px;margin:0 auto;padding:24px 20px 90px}
    .t-h1{font-family:var(--font);font-size:clamp(1.5rem,3.4vw,2.1rem);line-height:1.2;margin:0 0 14px}
    .t-lead{color:var(--text2);margin:0 0 22px}
    .t-scale{width:100%;border-collapse:collapse;margin:0 0 26px;font-size:.95rem}
    .t-scale td{border-bottom:1px solid var(--border);padding:8px 10px}
    .t-num{color:var(--gold2);font-family:var(--mono,monospace);width:3rem}
    .t-btn{display:inline-block;border:1px solid var(--gold2);background:transparent;color:var(--text);border-radius:8px;padding:12px 22px;font:inherit;cursor:pointer}
    .t-btn:hover{background:var(--gold-bg)}
    .t-btn--main{background:var(--gold2);color:#10151c;border-color:var(--gold2);font-weight:600}
    .t-top{display:flex;justify-content:space-between;align-items:center;gap:12px;font-family:var(--mono,monospace);font-size:.8rem;color:var(--text2);margin-bottom:10px}
    .t-bar{height:4px;background:var(--border);border-radius:3px;overflow:hidden;margin-bottom:26px}
    .t-bar i{display:block;height:100%;width:0;background:var(--gold2);transition:width .25s}
    .t-q{font-size:clamp(1.05rem,2.4vw,1.3rem);line-height:1.45;margin:0 0 22px;min-height:3.2em}
    .t-opts{display:grid;gap:10px;margin-bottom:18px}
    .t-opt{display:flex;gap:12px;align-items:center;border:1px solid var(--border);background:transparent;color:var(--text);border-radius:10px;padding:13px 16px;font:inherit;text-align:left;cursor:pointer}
    .t-opt:hover{border-color:var(--gold2);background:var(--gold-bg)}
    .t-opt b{font-family:var(--mono,monospace);color:var(--gold2);min-width:1.1rem}
    .t-card{border:1px solid var(--border);border-radius:12px;padding:20px;margin-bottom:18px}
    .t-big{font-size:1.5rem;margin:0 0 6px}
    .t-mut{color:var(--text2);font-size:.92rem}
    .t-tab{width:100%;border-collapse:collapse;font-size:.92rem}
    .t-tab th,.t-tab td{border-bottom:1px solid var(--border);padding:8px 10px;text-align:left}
    .t-tab th{color:var(--text2);font-weight:500;font-size:.8rem;text-transform:uppercase;letter-spacing:.04em}
    .t-tab .t-avg{font-family:var(--mono,monospace);color:var(--gold2);white-space:nowrap}
    .t-tab tr.is-top td{background:var(--gold-bg)}
    .t-actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:8px}
    [hidden]{display:none !important}
  </style>
</head>
<body>
  <header class="site-header">
    <a class="hdr-back" href="${BOOK[code]}">${ui.toBook}</a>
    <span data-lang-switch data-langs="az,ru"></span>
  </header>
  <main class="t-wrap">
    <section id="intro">
      <h1 class="t-h1">${ui.h1}</h1>
      <p class="t-lead">${ui.lead}</p>
      <h2 class="t-h1" style="font-size:1.05rem">${ui.scaleTitle}</h2>
      <table class="t-scale">
${scaleRows}
      </table>
      <button class="t-btn t-btn--main" id="start">${ui.start}</button>
    </section>

    <section id="quiz" hidden>
      <div class="t-top"><span id="pos">1 / 100</span><span id="pct">1%</span></div>
      <div class="t-bar"><i id="fill"></i></div>
      <p class="t-q" id="qtext"></p>
      <div class="t-opts" id="opts"></div>
      <div class="t-actions">
        <button class="t-btn" id="prev">${ui.back}</button>
      </div>
    </section>

    <section id="result" hidden>
      <h2 class="t-h1">${ui.resultTitle}</h2>
      <div class="t-card">
        <p class="t-mut" id="r-level"></p>
        <p class="t-big" id="r-model"></p>
        <p class="t-mut" id="r-maturity"></p>
        <p class="t-mut" id="r-avg"></p>
        <p id="r-group" style="margin-top:12px"></p>
        <p style="margin-top:16px"><a class="t-btn" id="r-link" href="#"></a></p>
      </div>
      <h3 class="t-h1" style="font-size:1.05rem">${ui.allTitle}</h3>
      <table class="t-tab">
        <thead><tr><th>#</th><th>${ui.dominant}</th><th>${ui.avg}</th></tr></thead>
        <tbody id="r-table"></tbody>
      </table>
      <div class="t-actions">
        <button class="t-btn" id="again">${ui.restart}</button>
        <a class="t-btn" href="${BOOK[code]}">${ui.toBook}</a>
      </div>
    </section>
  </main>

  <script>window.__TEST = ${JSON.stringify(payload)};</script>
  <script>
  (function () {
    'use strict';
    var D = window.__TEST;
    var intro = document.getElementById('intro'), quiz = document.getElementById('quiz'), res = document.getElementById('result');
    var qtext = document.getElementById('qtext'), opts = document.getElementById('opts'), pos = document.getElementById('pos'),
        pct = document.getElementById('pct'), fill = document.getElementById('fill');
    var order = [], idx = 0, answers = [];

    function shuffle(a) { for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
    function build() {
      order = [];
      D.blocks.forEach(function (b) { b.questions.forEach(function (q) { order.push({ model: b.model, text: q }); }); });
      shuffle(order);                       /* вопросы идут в случайном порядке */
      answers = new Array(order.length).fill(0);
      idx = 0;
    }
    function render() {
      var q = order[idx];
      pos.textContent = (idx + 1) + ' ' + D.ui.of;
      var p = Math.round((idx + 1) / order.length * 100);
      pct.textContent = p + '%'; fill.style.width = p + '%';
      qtext.textContent = q.text;
      opts.innerHTML = '';
      D.scale.forEach(function (label, i) {
        var b = document.createElement('button');
        b.className = 't-opt';
        b.innerHTML = '<b>' + (i + 1) + '</b><span>' + label + '</span>';
        b.addEventListener('click', function () { answers[idx] = i + 1; next(); });
        opts.appendChild(b);
      });
    }
    function next() { if (idx < order.length - 1) { idx++; render(); } else { finish(); } }
    function finish() {
      var sums = {};
      D.blocks.forEach(function (b) { sums[b.model] = 0; });
      order.forEach(function (q, i) { sums[q.model] += answers[i]; });
      var rows = D.blocks.map(function (b) {
        return { model: b.model, avg: sums[b.model] / b.count, strength: 0, maturity: '' };
      });
      var lv = {};
      D.levels.forEach(function (l) { lv[l.model] = l; });
      rows.forEach(function (r) { if (lv[r.model]) { r.strength = lv[r.model].strength; r.maturity = lv[r.model].maturity; } });
      rows.sort(function (a, b) { return b.avg - a.avg; });
      var top = rows[0];
      document.getElementById('r-level').textContent = D.ui.level + ': ' + top.strength + ' / 12';
      document.getElementById('r-model').textContent = top.model;
      document.getElementById('r-maturity').textContent = top.maturity;
      document.getElementById('r-avg').textContent = D.ui.avg + ': ' + top.avg.toFixed(2);
      document.getElementById('r-group').textContent = top.strength <= 4 ? D.groups.low : (top.strength <= 8 ? D.groups.mid : (top.strength <= 11 ? D.groups.high : D.groups.top));
      var link = document.getElementById('r-link');
      link.href = D.chapters[top.model] || D.book;
      link.textContent = D.ui.readMore;
      var tb = document.getElementById('r-table');
      tb.innerHTML = rows.map(function (r) {
        var cls = r.model === top.model ? ' class="is-top"' : '';
        return '<tr' + cls + '><td class="t-avg">' + r.strength + '</td><td>' + r.model + '</td><td class="t-avg">' + r.avg.toFixed(2) + '</td></tr>';
      }).join('');
      quiz.hidden = true; res.hidden = false;
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    document.getElementById('start').addEventListener('click', function () { build(); intro.hidden = true; quiz.hidden = false; render(); });
    document.getElementById('prev').addEventListener('click', function () { if (idx > 0) { idx--; render(); } });
    document.getElementById('again').addEventListener('click', function () { build(); res.hidden = true; quiz.hidden = false; render(); });
  })();
  </script>
  <script src="/_lang-switch.js?v=4" defer></script>
</body>
</html>
`;
}

['az', 'ru'].forEach((code) => {
  const dir = code === 'az' ? path.join(ROOT, 'books/phoenix-era/test') : path.join(ROOT, 'books/phoenix-era/test/ru');
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'index.html'), page(code), 'utf8');
  console.log('собрано:', path.relative(ROOT, path.join(dir, 'index.html')));
});
