/* ЭСКИЗ 11 — двери, пути, нить. Тексты — по ключам, три языка. Факты — только с живого сайта и из документов владельца. */
import { initLight } from './light.js';

const T = {
  ru: {
    school: 'Школа психологии', ask: 'Что вас привело?', pathEyebrow: 'Ваш путь', other: 'Выбрать другой путь',
    overTitle: 'Четыре пути', overSub: 'Выберите дверь — и страница покажет только то, что нужно вам, и одну кнопку в конце.',
    fab: 'Выбрать путь', note: 'Эскиз test/11: первый экран и схема пути. Экраны каждого пути собираются следующим шагом.',
    doors: {
      help: { t: 'Мне нужна помощь', s: 'Консультация психотерапевта', cta: 'Написать в WhatsApp', cap: 'пульс выравнивается',
        steps: [['С чем приходят', 'Темы, с которыми работают специалисты.'], ['Драма Сабины', 'Экранизация реального случая. 31 минута.'], ['Кто ведёт', 'Кенан Рагимов и Самира Рагимова.'], ['Как проходит и сколько стоит', 'Три шага и цены — до записи.'], ['Глава об этом', 'Учебник «Клиническая психиатрия» — читать бесплатно.']] },
      prof: { t: 'Хочу профессию', s: 'Обучение и документ', cta: 'Регистрация', cap: '3 месяца обучения + 6 месяцев супервизии',
        steps: [['Что остаётся на руках', 'Диплом или сертификат с проверкой по QR.'], ['Маршрут', 'Краткосрочные тренинги: 3 месяца обучения и 6 месяцев супервизии.'], ['Программы и цены', 'Шесть программ, цены открыты.'], ['Кто учит', 'Специалисты школы.'], ['По чему учат', 'Учебник на четырёх языках.']] },
      book: { t: 'Ищу книгу', s: 'Читать и заказать', cta: 'Читать', cap: 'читать · заказать в печати',
        steps: [['Книга в руках', 'Том в объёме, настоящая обложка.'], ['Заглянуть внутрь', 'Страницы из читалки.'], ['Библиотека', 'Все издания на одной стене.'], ['Фрейд', 'Впервые на азербайджанском языке.'], ['Печать', 'Заказ печатной книги.']] },
      corp: { t: 'Для компании', s: 'Корпоративное обучение', cta: 'Оставить заявку', cap: '2008 → сегодня',
        steps: [['Хроника в цифрах', 'Более 3000 человек прошли тренинги.'], ['Темы', 'HR, управление, лидерство, командная работа.'], ['События', 'Business Party: 2015–2016.'], ['Запрос', 'Форма заявки для компании.']] },
    },
  },
  az: {
    school: 'Psixologiya Məktəbi', ask: 'Sizi bura nə gətirdi?', pathEyebrow: 'Sizin yolunuz', other: 'Başqa yol seçmək',
    overTitle: 'Dörd yol', overSub: 'Qapını seçin — səhifə yalnız sizə lazım olanı və sonda bir düyməni göstərəcək.',
    fab: 'Yol seçmək', note: 'Eskiz test/11: birinci ekran və yolun sxemi. Hər yolun ekranları növbəti addımda yığılır.',
    doors: {
      help: { t: 'Mənə kömək lazımdır', s: 'Psixoterapevt konsultasiyası', cta: 'WhatsApp-da yazın', cap: 'nəbz sakitləşir',
        steps: [['Nə ilə müraciət edirlər', 'Mütəxəssislərin işlədiyi mövzular.'], ['Səbinənin draması', 'Real hadisənin ekranlaşdırılması. 31 dəqiqə.'], ['Kim aparır', 'Kənan Rəhimov və Samirə Rəhimova.'], ['Necə keçir və qiyməti', 'Üç addım və qiymətlər — yazılışdan əvvəl.'], ['Bu barədə fəsil', '«Klinik Psixiatriya» dərsliyi — pulsuz oxu.']] },
      prof: { t: 'Peşə qazanmaq istəyirəm', s: 'Təhsil və sənəd', cta: 'Qeydiyyat', cap: '3 ay təhsil + 6 ay superviziya',
        steps: [['Əlinizdə nə qalır', 'QR ilə yoxlanılan diplom və ya sertifikat.'], ['Marşrut', 'Qısamüddətli təlimlər: 3 ay təhsil və 6 ay superviziya.'], ['Proqramlar və qiymətlər', 'Altı proqram, qiymətlər açıqdır.'], ['Kim öyrədir', 'Məktəbin mütəxəssisləri.'], ['Nədən öyrədirlər', 'Dörd dildə dərslik.']] },
      book: { t: 'Kitab axtarıram', s: 'Oxumaq və sifariş etmək', cta: 'Oxu', cap: 'oxu · çap sifarişi',
        steps: [['Kitab əlinizdə', 'Həcmli cild, əsl üz qabığı.'], ['İçinə baxmaq', 'Oxu zalından səhifələr.'], ['Kitabxana', 'Bütün nəşrlər bir divarda.'], ['Freyd', 'İlk dəfə Azərbaycan dilində.'], ['Çap', 'Çap kitabının sifarişi.']] },
      corp: { t: 'Şirkət üçün', s: 'Korporativ təlimlər', cta: 'Müraciət göndər', cap: '2008 → bu gün',
        steps: [['Rəqəmlərlə xronika', '3000-dən çox insan təlim keçib.'], ['Mövzular', 'HR, idarəetmə, liderlik, komanda işi.'], ['Tədbirlər', 'Business Party: 2015–2016.'], ['Sorğu', 'Şirkət üçün müraciət forması.']] },
    },
  },
  en: {
    school: 'School of Psychology', ask: 'What brings you here?', pathEyebrow: 'Your path', other: 'Choose another path',
    overTitle: 'Four paths', overSub: 'Choose a door — the page will show only what you need, and one button at the end.',
    fab: 'Choose a path', note: 'Sketch test/11: the first screen and the path outline. The screens of each path are built in the next step.',
    doors: {
      help: { t: 'I need help', s: 'A consultation with a psychotherapist', cta: 'Message on WhatsApp', cap: 'the pulse settles',
        steps: [['What brings people here', 'The topics the specialists work with.'], ['Sabina’s Drama', 'A real case on screen. 31 minutes.'], ['Who leads', 'Kenan Ragimov and Samira Rahimova.'], ['How it goes and what it costs', 'Three steps and prices — before you book.'], ['The chapter on it', 'The “Clinical Psychiatry” textbook — free to read.']] },
      prof: { t: 'I want a profession', s: 'Training and a document', cta: 'Register', cap: '3 months of training + 6 months of supervision',
        steps: [['What you leave with', 'A diploma or certificate verified by QR.'], ['The route', 'Short-term trainings: 3 months of training and 6 months of supervision.'], ['Programmes and prices', 'Six programmes, prices in the open.'], ['Who teaches', 'The school’s specialists.'], ['What they teach from', 'A textbook in four languages.']] },
      book: { t: 'I’m looking for a book', s: 'Read and order', cta: 'Read', cap: 'read · order in print',
        steps: [['The book in your hands', 'A volume in depth, the real cover.'], ['Look inside', 'Pages from the reader.'], ['The library', 'Every edition on one wall.'], ['Freud', 'For the first time in Azerbaijani.'], ['Print', 'Ordering a printed book.']] },
      corp: { t: 'For a company', s: 'Corporate training', cta: 'Send a request', cap: '2008 → today',
        steps: [['A chronicle in numbers', 'More than 3,000 people have completed the trainings.'], ['Topics', 'HR, management, leadership, teamwork.'], ['Events', 'Business Party: 2015–2016.'], ['Request', 'A request form for a company.']] },
    },
  },
};
const ORDER = ['help', 'prof', 'book', 'corp'];
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const store = { get: k => { try { return localStorage.getItem(k); } catch (e) { return null; } }, set: (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} } };
const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

let lang = T[document.documentElement.lang] ? document.documentElement.lang : 'ru';
let door = ORDER.includes(store.get('r11_door')) ? store.get('r11_door') : null;
const light = initLight($('#light'));

/* ── отрисовка текстов ── */
function render() {
  const t = T[lang];
  document.documentElement.lang = lang;
  $$('[data-i]').forEach(e => { e.textContent = t[e.dataset.i]; });
  $('#doors').innerHTML = ORDER.map((k, i) => `<button class="door" type="button" role="listitem" data-door="${k}" style="--i:${i}"${door === k ? ' aria-current="true"' : ''}>
    <span class="door__arch"><span class="door__glow"></span><span class="door__leaf"><span class="door__num">0${i + 1}</span></span></span>
    <span class="door__cap"><span class="door__title">${esc(t.doors[k].t)}</span><span class="door__sub">${esc(t.doors[k].s)}</span></span></button>`).join('');
  const steps = $('#steps');
  if (door) {
    const d = t.doors[door];
    $('#pathTitle').textContent = d.t; $('#pathSub').textContent = d.s;
    steps.className = 'steps';
    steps.innerHTML = d.steps.map((s, i) => `<li class="step" data-step><div><span class="step__n">0${i + 1}</span><h3 class="step__t">${esc(s[0])}</h3><p class="step__d">${esc(s[1])}</p></div>${
      i === (door === 'prof' ? 1 : 0) ? `<div class="motif" data-motif="${door}"><svg><path/></svg><span class="motif__cap">${esc(d.cap)}</span></div>` : '<div></div>'}</li>`).join('');
    $('#pathBtn').textContent = d.cta; $('.path__cta').hidden = false;
    $('#fabText').textContent = d.cta;
  } else {
    $('#pathTitle').textContent = t.overTitle; $('#pathSub').textContent = t.overSub;
    steps.className = 'over';
    steps.innerHTML = ORDER.map(k => `<li><button class="over__row" type="button" data-door="${k}"><span class="over__t">${esc(t.doors[k].t)}</span><span class="over__s">${esc(t.doors[k].steps.map(s => s[0]).join(' → '))}</span><span class="over__a">→</span></button></li>`).join('');
    $('.path__cta').hidden = true;
    $('#fabText').textContent = t.fab;
  }
  $('#fab').setAttribute('href', door ? '#path' : '#top');
  $$('[data-lang-btn]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.langBtn === lang)));
  $$('[data-theme-btn]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.themeBtn === document.documentElement.dataset.theme)));
  drawMotifs(); buildThread();
}

/* ── мотив первого шага: нить становится доказательством этого пути ── */
function motifPath(kind, w, h) {
  const p = []; const M = (x, y) => p.push(`M${x.toFixed(1)},${y.toFixed(1)}`), L = (x, y) => p.push(`L${x.toFixed(1)},${y.toFixed(1)}`);
  if (kind === 'help') {                      /* сбивчивый пульс, который выравнивается */
    const b = h * .5; M(0, b); let x = w * .05; L(x, b);
    const amp = [.44, .30, .38, .20, .12, .07, .04], gap = [.055, .035, .08, .07, .075, .075, .075];
    amp.forEach((a, i) => { const s = w * .028; L(x + s * .5, b - h * a * .35); L(x + s, b + h * a); L(x + s * 1.7, b - h * a * .9); L(x + s * 2.3, b); x += s * 2.3 + w * gap[i]; L(Math.min(x, w), b); });
    L(w, b);
  } else if (kind === 'prof') {               /* три ступени обучения, шесть отметок супервизии, документ */
    let x = 0, y = h * .82; M(x, y);
    for (let i = 0; i < 3; i++) { x += w * .085; L(x, y); y -= h * .19; L(x, y); }
    for (let i = 0; i < 6; i++) { x += w * .085; L(x, y); L(x, y - 9); L(x, y); }
    x += w * .06; L(x, y); const r = Math.min(13, h * .13);
    L(x + r, y - r); L(x + 2 * r, y); L(x + r, y + r); L(x, y);
  } else if (kind === 'book') {               /* раскрытая книга с закладкой */
    const c = w * .42, top = h * .22, bot = h * .78, half = Math.min(w * .2, 150);
    M(0, bot); L(c - half, bot); L(c - half, top + 8);
    p.push(`C${(c - half * .55).toFixed(1)},${(top - 12).toFixed(1)} ${(c - half * .2).toFixed(1)},${(top - 6).toFixed(1)} ${c.toFixed(1)},${(top + 12).toFixed(1)}`);
    p.push(`C${(c + half * .2).toFixed(1)},${(top - 6).toFixed(1)} ${(c + half * .55).toFixed(1)},${(top - 12).toFixed(1)} ${(c + half).toFixed(1)},${(top + 8).toFixed(1)}`);
    L(c + half, bot); L(c, bot); L(c, top + 12); L(c, bot); L(c + 9, h * .98); L(c + 18, bot); L(w, bot);
  } else {                                     /* хроника: ступени вверх по годам */
    let x = 0, y = h * .86; M(x, y);
    const st = 6; for (let i = 0; i < st; i++) { x += w / (st + .5); L(x, y); y -= h * .115; L(x, y); }
    L(w, y);
  }
  return p.join(' ');
}
function drawMotifs() {
  $$('[data-motif]').forEach(m => {
    const path = $('path', m), w = m.clientWidth, h = m.clientHeight; if (!w) return;
    path.setAttribute('d', motifPath(m.dataset.motif, w, h));
    const len = path.getTotalLength(); path.style.strokeDasharray = len; path.dataset.len = len; path.style.strokeDashoffset = len;
  });
}

/* ── нить: росчерк → порог дверей → вниз по пути → подпись в конце ── */
const svg = $('#thread'), line = $('#threadLine'), ghost = $('#threadGhost'), dotsG = $('#threadDots');
let table = [], total = 0, shown = 0, dots = [], introStart = Number.MAX_VALUE;
function buildThread() {
  const W = document.documentElement.clientWidth, H = document.documentElement.scrollHeight, sy = scrollY;
  svg.setAttribute('width', W); svg.setAttribute('height', H); svg.style.height = H + 'px';
  /* замер по раскладке (offset), а не по экрану: анимации появления сдвигают блоки, нить должна лечь на итоговое место */
  const R = el => { let x = 0, y = 0, e = el; while (e) { x += e.offsetLeft; y += e.offsetTop; e = e.offsetParent; } return { l: x, r: x + el.offsetWidth, t: y, b: y + el.offsetHeight, w: el.offsetWidth, h: el.offsetHeight }; };
  const mob = W <= 760, pad = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--pad')) || 20;
  const s = R($('#sign .sign__ink')), g = R($('#doors')), a = R($('.door__arch')), f = R($('#footSign'));
  const spine = mob ? pad * .55 : pad * .5, xr = mob ? W - pad * .55 : Math.min(W - pad * .5, g.r + pad * .5);
  const floor = mob ? g.b + 18 : a.b;
  const sx = Math.max(6, s.l - 4), sb = s.t + s.h * .80, ex = Math.min(s.r - s.w * .06, xr - 40);
  const d = [];
  d.push(`M${sx},${sb + 6}`);
  d.push(`C${sx + s.w * .22},${sb + 26} ${sx + s.w * .55},${sb - 8} ${ex},${sb + 2}`);                           /* росчерк под именем */
  d.push(`C${ex + (xr - ex) * .7},${sb + 8} ${xr},${sb + (floor - sb) * .25} ${xr},${floor - 46}`);               /* вправо и вниз */
  d.push(`Q${xr},${floor} ${xr - 46},${floor}`);
  d.push(`L${spine + 46},${floor}`);                                                                               /* порог: двери стоят на нити */
  d.push(`Q${spine},${floor} ${spine},${floor + 46}`);
  d.push(`L${spine},${f.t - 30}`);                                                                                 /* вниз вдоль пути */
  d.push(`Q${spine},${f.b - 6} ${f.l},${f.b - 8}`);
  d.push(`C${f.l + f.w * .3},${f.b + 10} ${f.l + f.w * .7},${f.b - 14} ${f.r + 14},${f.b - 6}`);                   /* возвращается в подпись */
  const D = d.join(' ');
  line.setAttribute('d', D); ghost.setAttribute('d', D);
  total = line.getTotalLength(); line.style.strokeDasharray = total;
  table = []; const N = 700; let maxY = -1;
  for (let i = 0; i <= N; i++) { const l = total * i / N, y = line.getPointAtLength(l).y; maxY = Math.max(maxY, y); table.push([l, maxY]); }
  /* точки шагов */
  dotsG.innerHTML = ''; dots = [];
  $$('[data-step]').forEach(el => {
    const r = R(el), y = r.t + 14, c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    c.setAttribute('cx', spine); c.setAttribute('cy', y); c.setAttribute('r', 4.5); dotsG.appendChild(c);
    dots.push({ el, c, y });
  });
  update(true);
}
function lenAtY(y) { let lo = 0, hi = table.length - 1; while (lo < hi) { const m = (lo + hi + 1) >> 1; if (table[m][1] <= y) lo = m; else hi = m - 1; } return table[lo][0]; }
let raf = 0;
function update(instant) {
  if (!total) return;
  const vh = innerHeight, targetY = scrollY + vh * .86;
  let target = lenAtY(targetY);
  if (scrollY + vh >= document.documentElement.scrollHeight - 4) target = total;
  const intro = Math.max(0, Math.min(1, (performance.now() - introStart) / 3400)), cap = intro < 1 ? total * (1 - Math.pow(1 - intro, 3)) : total;   /* первое появление: нить «пишется» */
  target = Math.min(target, cap);
  shown = instant && intro >= 1 ? target : shown + (target - shown) * .12;
  if (Math.abs(target - shown) < .5) shown = target;
  line.style.strokeDashoffset = (total - shown).toFixed(1);
  const pt = line.getPointAtLength(shown);
  dots.forEach(o => { const on = pt.y >= o.y - 2 || shown >= total - 1; o.c.classList.toggle('is-on', on); o.el.classList.toggle('is-on', on); });
  $$('[data-motif] path').forEach(p => {
    const r = p.ownerSVGElement.getBoundingClientRect(), k = Math.min(1, Math.max(0, (vh * .86 - r.top) / (vh * .42))), len = +p.dataset.len || 0;
    p.style.strokeDashoffset = (len * (1 - k)).toFixed(1);
  });
  if (shown !== target || intro < 1) { if (!raf) raf = requestAnimationFrame(() => { raf = 0; update(); }); }
}

/* ── шапка: уходит при движении вниз, возвращается при движении вверх; кнопка действия ── */
const head = $('#head'), fab = $('#fab'); let lastY = 0, travel = 0;
function onScroll() {
  const y = scrollY, dy = y - lastY; if ((dy > 0) !== (travel > 0)) travel = 0; travel += dy; lastY = y;
  if (y < 120) head.classList.remove('is-hidden'); else if (travel > 48) head.classList.add('is-hidden'); else if (travel < -32) head.classList.remove('is-hidden');
  fab.classList.toggle('is-on', y > innerHeight * .45);
  update();
}
addEventListener('scroll', onScroll, { passive: true });
let rt = 0; addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(() => { drawMotifs(); buildThread(); }, 120); });

/* ── выбор двери, темы, языка ── */
document.addEventListener('click', e => {
  const d = e.target.closest('[data-door]');
  if (d) { door = d.dataset.door; store.set('r11_door', door); render(); requestAnimationFrame(() => $('#path').scrollIntoView({ behavior: 'smooth', block: 'start' })); return; }
  const th = e.target.closest('[data-theme-btn]');
  if (th) { document.documentElement.dataset.theme = th.dataset.themeBtn; store.set('r11_theme', th.dataset.themeBtn); if (light) light.setTheme(); render(); return; }
  const lg = e.target.closest('[data-lang-btn]');
  if (lg) { lang = lg.dataset.langBtn; store.set('r11_lang', lang); render(); return; }
  if (e.target.closest('#pathReset')) { door = null; store.set('r11_door', ''); render(); scrollTo({ top: 0, behavior: 'smooth' }); }
});

/* ── запуск: после загрузки шрифтов, иначе нить ляжет мимо росчерка ── */
render();
(document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(() => {
  introStart = performance.now();
  drawMotifs(); buildThread();
  requestAnimationFrame(() => document.body.classList.add('is-in'));
  update();
});
addEventListener('load', () => { drawMotifs(); buildThread(); });
