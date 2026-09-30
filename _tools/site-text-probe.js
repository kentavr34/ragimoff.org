/* site-text-probe.js — снимает ОТРИСОВАННЫЙ текст страницы (innerText:
 * скрытые меню, display:none и служебные узлы не попадают) и кладёт его в
 * узел pre с идентификатором __audit_text, откуда драйвер достаёт его из
 * dump-dom. Так грамматика проверяется по тому, что читает человек, а не по
 * разметке. (Идентификатор в этом комментарии не пишем: он попал бы в текст
 * скрипта, а драйвер ищет узел регуляркой по сериализованному DOM.)
 */
(function () {
  'use strict';
  if (document.getElementById('__audit_text')) return;
  function dump() {
    try {
      var t = (document.body && document.body.innerText) || '';
      var pre = document.getElementById('__audit_text');
      if (!pre) {
        pre = document.createElement('pre');
        pre.id = '__audit_text';
        pre.style.cssText = 'display:none!important;position:absolute;left:-99999px;top:0;';
        document.body.appendChild(pre);
      }
      pre.textContent = t;
    } catch (e) {
      var p2 = document.getElementById('__audit_text');
      if (p2) p2.textContent = 'PROBE-ERROR: ' + e;
    }
  }
  if (document.readyState === 'complete') dump();
  window.addEventListener('load', function () { setTimeout(dump, 300); });
  setTimeout(dump, 1500);
  setTimeout(dump, 3500);
})();
