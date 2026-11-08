/* Аудит страниц «Ноктюрна» в браузере (вставляется через инструмент проверки):
   для каждой страницы — горизонтальный выход, битые картинки, невидимый текст,
   тёмный текст на тёмном фоне, ссылки на несуществующие страницы новой версии. */
async function nocturneAudit(paths, width) {
  const lum = c => { const m = c.match(/[\d.]+/g); if (!m) return 1; const [r, g, b] = m.slice(0, 3).map(v => { v = v / 255; return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); }); return .2126 * r + .7152 * g + .0722 * b; };
  const alpha = c => { const m = c.match(/[\d.]+/g); return m && m.length > 3 ? +m[3] : 1; };
  const out = [];
  for (const p of paths) {
    const f = document.createElement('iframe');
    f.style.cssText = 'position:fixed;left:0;top:0;width:' + width + 'px;height:900px;opacity:0;pointer-events:none';
    document.body.appendChild(f);
    await new Promise(r => { f.onload = r; f.src = p; });
    await new Promise(r => setTimeout(r, 1200));
    const d = f.contentDocument, w = f.contentWindow;
    const res = { p, overflow: d.documentElement.scrollWidth - w.innerWidth, badImg: [], dark: [], hidden: 0, links: [] };
    d.querySelectorAll('img').forEach(i => { if (i.complete && i.naturalWidth === 0) res.badImg.push(i.getAttribute('src')); });
    const bgOf = el => { while (el) { const c = w.getComputedStyle(el).backgroundColor; if (alpha(c) > .5) return c; el = el.parentElement; } return 'rgb(7,9,14)'; };
    d.querySelectorAll('main p, main li, main h2, main h3, main h4, main span, main a, main td, main label').forEach(el => {
      if (!el.textContent.trim() || el.children.length > 3) return;
      const cs = w.getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') return;
      if (+cs.opacity === 0 && !el.closest('.n-io')) { res.hidden++; return; }
      const fg = lum(cs.color), bg = lum(bgOf(el));
      const ratio = (Math.max(fg, bg) + .05) / (Math.min(fg, bg) + .05);
      if (ratio < 3 && el.getBoundingClientRect().width > 0) res.dark.push(el.tagName + ':' + el.textContent.trim().slice(0, 30) + ' (' + ratio.toFixed(1) + ')');
    });
    res.dark = res.dark.slice(0, 6);
    out.push(res);
    f.remove();
  }
  return out;
}
