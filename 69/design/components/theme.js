/* ═══════════════════════════════════════════════════════════════════
   ПЕРЕКЛЮЧАТЕЛЬ ТЕМ
   ═══════════════════════════════════════════════════════════════════
   ПОЧЕМУ ЭТОТ ФАЙЛ ПОЯВИЛСЯ (11.11.2026).

   Владелец: «ты заявлял о трёх темах — а тут 2. А где 3 обещанная?»

   НАСТОЯЩАЯ ПРИЧИНА. В разметке было РОВНО ТРИ кнопки темы, и они были
   видны — но обработчика нажатия не существовало ни в одном файле.
   Нажатие не делало ничего. Со стороны это выглядело как «две темы
   вместо трёх»: страница всегда оставалась тёмной.

   УРОК: кнопка без обработчика — это картинка. Наличие элемента в
   разметке не означает наличия работы. Проверять надо нажатием, а не
   наличием кнопки.

   ЧТО ЗДЕСЬ. Переключение применяется на корень документа атрибутом
   data-theme; выбор сохраняется в хранилище и восстанавливается до
   первой отрисовки (скрипт в <head> собранной страницы) — иначе при
   загрузке мигает тёмным.
   ═══════════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  var KEY = 'ragimoff-theme';
  var THEMES = ['dark', 'light', 'sepia'];
  var root = document.documentElement;

  function apply(theme) {
    if (THEMES.indexOf(theme) < 0) theme = 'dark';
    root.setAttribute('data-theme', theme);
    try { localStorage.setItem(KEY, theme); } catch (e) { /* приватный режим */ }

    // отметка выбранной кнопки: видно, какая тема сейчас
    var btns = document.querySelectorAll('.theme__btn');
    for (var i = 0; i < btns.length; i++) {
      var on = btns[i].getAttribute('data-theme-set') === theme;
      btns[i].classList.toggle('is-active', on);
      btns[i].setAttribute('aria-pressed', on ? 'true' : 'false');
    }
    // сообщаем остальным частям страницы: сеть героя может сменить палитру
    document.dispatchEvent(new CustomEvent('themechange', { detail: { theme: theme } }));
  }

  function current() {
    try { return localStorage.getItem(KEY) || root.getAttribute('data-theme') || 'dark'; }
    catch (e) { return root.getAttribute('data-theme') || 'dark'; }
  }

  function init() {
    var box = document.getElementById('themes');
    if (!box) return;

    box.addEventListener('click', function (e) {
      var b = e.target.closest ? e.target.closest('.theme__btn') : null;
      if (!b) return;
      apply(b.getAttribute('data-theme-set'));
    });

    // стрелки с клавиатуры: переключатель должен работать и без мыши
    box.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      var list = THEMES.slice();
      var i = list.indexOf(current());
      if (i < 0) i = 0;
      i = e.key === 'ArrowRight' ? (i + 1) % list.length : (i - 1 + list.length) % list.length;
      apply(list[i]);
      var b = document.querySelector('.theme__btn[data-theme-set="' + list[i] + '"]');
      if (b) b.focus();
    });

    // отметка при загрузке: тема уже применена скриптом в <head>,
    // здесь только подсвечиваем нужную кнопку
    apply(current());
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
