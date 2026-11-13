/* test/11 — страница теста: рама сайта (шапка, меню, темы, подвал). Сам тест ведёт прежний сценарий /test/quiz.js. */
import { initChrome } from './chrome.js?v=11130541';
const page = initChrome({ onRender(t, L) { document.title = document.querySelector('h1').textContent + ' — Test · Doctor Ragimoff'; const b = document.querySelector('#tstBack'); if (b) { b.textContent = '← ' + t.nav.edu; b.href = 'index.html#edu'; } const hc = document.querySelector('#headCta'); if (hc) hc.href = L.form || 'index.html#reg'; } });
page.watch();
