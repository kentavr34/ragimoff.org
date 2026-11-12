/* test/11 — кнопка «наверх»: одна на все страницы (главная и внутренние). Появляется после первого экрана, стоит над кнопкой WhatsApp. */
export function initTop() {
  if (document.getElementById('toTop')) return;
  const b = document.createElement('button');
  b.type = 'button'; b.id = 'toTop'; b.className = 'totop'; b.setAttribute('aria-label', '↑');
  b.innerHTML = '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  document.body.appendChild(b);
  /* на телефоне кнопка не лежит на тексте во время чтения: показывается, когда человек повёл страницу вверх или дошёл до конца */
  let last = scrollY, up = false;
  const on = () => { const y = scrollY; if (Math.abs(y - last) > 6) { up = y < last; last = y; }
    const end = innerHeight + y > document.documentElement.scrollHeight - 80, wide = innerWidth >= 1100;
    b.classList.toggle('is-on', y > innerHeight * .9 && (wide || up || end)); };
  addEventListener('scroll', on, { passive: true }); on();
  b.addEventListener('click', () => scrollTo({ top: 0, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' }));
}
