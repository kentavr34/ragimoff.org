/* app.js — приложение RAGIMOFF (восстановлено 13.11.2026 по слову Кенана, прежняя версия — 09.11.2026).
   • сервис-воркер /sw.js: открытые страницы и главы книг сохраняются на устройстве и читаются без интернета;
   • предложение установить — НЕНАВЯЗЧИВО: первый раз само (через 4 с), дальше — только когда человек нажал на логотип
     и перешёл на главную; закрыл — до следующего нажатия на логотип не появляется;
   • Android без встроенной установки — скачивание APK (/app/ragimoff.apk); iPhone — подсказка «На экран „Домой“». */
const TX = {
  az: { t: 'RAGIMOFF tətbiqi', d: 'Saytı və kitabları telefonda açın — internetsiz də oxuyun.', go: 'Quraşdır', ios: 'Safari-də «Paylaş» → «Ana ekrana əlavə et» seçin.' },
  ru: { t: 'Приложение RAGIMOFF', d: 'Сайт и книги в телефоне — читайте даже без интернета.', go: 'Установить', ios: 'В Safari нажмите «Поделиться» → «На экран „Домой“».' },
  en: { t: 'RAGIMOFF app', d: 'The site and books on your phone — read even offline.', go: 'Install', ios: 'In Safari tap Share → “Add to Home Screen”.' },
};
const st = {
  get: (s, k) => { try { return s.getItem(k); } catch (e) { return null; } },
  set: (s, k, v) => { try { s.setItem(k, v); } catch (e) {} },
};
const SEEN = 'rgm_app_seen', LOGO = 'rgm_app_logo';
let deferred = null, shown = false;

if ('serviceWorker' in navigator && location.protocol === 'https:') {
  addEventListener('load', () => { navigator.serviceWorker.register('/sw.js', { scope: '/' }).catch(() => {}); });
}
addEventListener('beforeinstallprompt', e => { e.preventDefault(); deferred = e; });

const standalone = () => matchMedia('(display-mode: standalone)').matches || navigator.standalone;
const isIOS = () => /iphone|ipad|ipod/i.test(navigator.userAgent) && /safari/i.test(navigator.userAgent) && !/crios|fxios/i.test(navigator.userAgent);
const isAndroid = () => /android/i.test(navigator.userAgent);
const isHome = () => /^\/((az|ru|en)\/)?(index\.html)?$/.test(location.pathname);

function bar(lang) {
  const T = TX[lang] || TX.az;
  if (shown || document.querySelector('.app-bar')) return;
  const install = deferred ? () => { deferred.prompt(); return deferred.userChoice; }
    : (isAndroid() ? () => { location.href = '/app/ragimoff.apk'; return Promise.resolve(); } : null);
  if (!install && !isIOS()) return;                                  /* компьютер без установки — не показываем */
  shown = true;
  const b = document.createElement('div');
  b.className = 'app-bar'; b.setAttribute('role', 'dialog'); b.setAttribute('aria-label', T.t);
  b.innerHTML = `<span class="app-bar__ico" aria-hidden="true">R<i></i></span><span class="app-bar__txt"><b>${T.t}</b><small>${install ? T.d : T.ios}</small></span>` +
    (install ? `<button type="button" class="app-bar__go">${T.go}</button>` : '') + '<button type="button" class="app-bar__x" aria-label="×">×</button>';
  document.body.appendChild(b);
  void b.offsetHeight; setTimeout(() => b.classList.add('is-in'), 30);   /* не requestAnimationFrame: на главной с анимацией героя кадр может не прийти */
  const close = () => { b.classList.remove('is-in'); st.set(localStorage, SEEN, '1'); setTimeout(() => b.remove(), 500); };
  b.querySelector('.app-bar__x').onclick = close;
  if (install) b.querySelector('.app-bar__go').onclick = () => install().then(close, close);
}

/* вызывать один раз на каждой странице: getLang — текущий язык страницы */
export function initApp(getLang) {
  document.addEventListener('click', e => { if (e.target.closest('.logo')) st.set(sessionStorage, LOGO, '1'); }, true);
  if (standalone()) return;
  const first = !st.get(localStorage, SEEN), viaLogo = st.get(sessionStorage, LOGO) && isHome();
  if (!first && !viaLogo) return;
  if (viaLogo) st.set(sessionStorage, LOGO, '');
  setTimeout(() => bar(getLang()), first ? 4000 : 1200);
}
