/* align.js — поля карточек одного ряда на одной высоте (слово Кенана 13.11.2026, обязательное требование к дизайну).
   В карточках одного ряда меняется только длина названия; всё остальное — сведения, цена, кнопки — стоит параллельно.
   Сетки карточек выравниваются в site.css подсеткой (subgrid). Здесь — ленты, где подсетка невозможна (карточки в flex-ленте):
   каждому полю карточки ставится высота самого высокого такого же поля среди соседних карточек той же ленты.
   Проверяет страж _tools/pages_check.py («поля карточек ряда на разной высоте»). */
const SETS = [
  ['.pc', ['.pc__n', '.pc__t', '.pc__d', '.pc__m']],        /* программы обучения на главной */
  ['.bk', ['.bk__k', '.bk__t', '.bk__a']],                  /* книги на полке главной */
];
let timer = 0;

function run() {
  SETS.forEach(([card, fields]) => {
    const groups = new Map();
    document.querySelectorAll(card).forEach(c => { const p = c.parentElement; if (!groups.has(p)) groups.set(p, []); groups.get(p).push(c); });
    groups.forEach(cards => {
      if (cards.length < 2) return;
      fields.forEach(f => {
        const els = cards.map(c => c.querySelector(f)).filter(Boolean);
        els.forEach(e => { e.style.minHeight = ''; });
        const vis = els.filter(e => e.offsetParent !== null || getComputedStyle(e).display !== 'none');
        const max = Math.max(0, ...vis.map(e => e.offsetHeight));
        if (max > 0 && vis.length > 1) vis.forEach(e => { e.style.minHeight = max + 'px'; });
      });
    });
  });
}
const later = () => { clearTimeout(timer); timer = setTimeout(run, 80); };

/* вызывать один раз на странице: выравнивает сейчас, после загрузки шрифтов, при смене ширины и при перерисовке (смена языка) */
export function initAlign() {
  run();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(run);
  addEventListener('load', run);
  addEventListener('resize', later, { passive: true });
  const m = document.querySelector('main') || document.body;
  new MutationObserver(later).observe(m, { childList: true, subtree: true });
}
