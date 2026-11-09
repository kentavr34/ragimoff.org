/* Сторож ритма «Ноктюрна» (Кенан 09.11.2026, DESIGN-STANDARD §10).
   Запуск: открыть любую страницу сайта с того же адреса, подключить этот файл и вызвать
     await rhythmScan(['az/index.html', ...], 375)
   Каждая страница грузится в скрытую рамку нужной ширины; возвращаются только нарушения:
     S — пустота между секциями вне 40…230 px (два поля r4 = 128 + поле карточки/плашки до 32×2 + запас);
     H — шапка блока → содержимое вне 28…64 px (норма r3 = 40 на телефоне);
     B — текст/цена → кнопка меньше 20 px (норма r2 = 24);
     C — текст по центру длиннее двух строк. */
window.rhythmScan = async function (pages, W, base) {
  base = base || '/test/nocturne/';
  const res = {};
  for (const pg of pages) {
    const f = document.createElement('iframe');
    f.style.cssText = 'position:absolute;left:-9999px;top:0;width:' + W + 'px;height:812px;border:0';
    f.src = base + pg; document.body.appendChild(f);
    await new Promise(r => f.onload = r);
    const d = f.contentDocument, w = f.contentWindow;
    const st = d.createElement('style');
    st.textContent = '*{transition:none!important;animation:none!important} .n-io,.n-rise{transform:none!important;opacity:1!important} .n-app{display:none!important}';
    d.head.appendChild(st);
    await new Promise(r => setTimeout(r, 700));
    const R = e => e.getBoundingClientRect();
    const vis = e => { if (e.closest('details:not([open])') && !e.closest('summary')) return false; const r = R(e); if (r.height < 2 || r.width < 2) return false; const cs = w.getComputedStyle(e); return cs.visibility !== 'hidden' && cs.display !== 'none' && cs.opacity !== '0'; };
    const nm = e => (e.className || e.tagName).toString().split(' ')[0];
    const main = d.querySelector('main') || d.body;
    const out = { sec: [], hdr: [], btn: [], cen: [] };
    const leafSel = 'h1,h2,h3,h4,p,li,img,a.btn,.btn,button,input,textarea,select,.n-eyebrow,.sec-label,.badge,.price-total,.n-who,iframe,.n-shot,table';
    const ownText = e => [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    const leaves = sc => [...sc.querySelectorAll('*')].filter(e => (e.matches(leafSel) || ownText(e)) && vis(e));
    let prevB = null, prevName = '';
    for (const s of [...main.children].filter(e => vis(e) && !e.matches('script,style'))) {
      const L = leaves(s); if (!L.length) continue;
      const top = Math.min(...L.map(e => R(e).top)), bot = Math.max(...L.map(e => R(e).bottom));
      if (prevB !== null && !s.matches('.n-hero,.n-cine') && !prevName.match(/n-hero|n-cine/)) {
        const g = Math.round(top - prevB); if (g > 230 || g < 40) out.sec.push(g + ':' + prevName + '→' + nm(s));
      }
      prevB = bot; prevName = nm(s);
    }
    for (const h of main.querySelectorAll('h2')) {
      if (!vis(h) || h.closest('.article-body,.cta-band,.legal-block,.tg-band,.n-person,.n-who,.n-hero')) continue;
      let hb = R(h).bottom, n = h.nextElementSibling;
      while (n && (!vis(n) || n.matches('.sec-sub,.sec-lead,.n-lead,p.stud-sub'))) { if (vis(n)) hb = R(n).bottom; n = n.nextElementSibling; }
      if (!n) { let p = h.parentElement; while (p && p !== main && !p.nextElementSibling) p = p.parentElement; n = p && p !== main ? p.nextElementSibling : null; while (n && !vis(n)) n = n.nextElementSibling; }
      if (n && !n.matches('a.btn,.btn,.n-btn,.n-doc-link') && !(n.firstElementChild && n.firstElementChild.matches('a.btn,.btn,button'))) { const g = Math.round(R(n).top - hb); if (g < 28 || g > 64) out.hdr.push(g + ':' + h.textContent.trim().slice(0, 22) + '→' + nm(n)); }
    }
    const L = leaves(main);
    for (const b of L.filter(e => e.matches('a.btn,.btn,button[type=submit]'))) {
      const br = R(b); let bb = -1e9, best = null;
      for (const o of L) {
        if (o === b || b.contains(o) || o.contains(b) || o.closest('.btn,a.btn,button,.n-btn')) continue;
        const r = R(o); if (r.bottom <= br.top + 1 && r.right > br.left && r.left < br.right && r.bottom > bb) { best = o; bb = r.bottom; }
      }
      if (best) { const g = Math.round(br.top - bb); if (g < 20 && g >= 0) out.btn.push(g + ':' + nm(best) + '→' + b.textContent.trim().slice(0, 16)); }
    }
    for (const p of main.querySelectorAll('p,li,.sec-sub,.n-lead')) {
      if (!vis(p)) continue; const cs = w.getComputedStyle(p); const lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.5;
      if (cs.textAlign === 'center' && R(p).height / lh > 2.4) out.cen.push(p.textContent.trim().slice(0, 30));
    }
    if (out.sec.length + out.hdr.length + out.btn.length + out.cen.length) res[pg] = out;
    f.remove();
  }
  return res;
};
