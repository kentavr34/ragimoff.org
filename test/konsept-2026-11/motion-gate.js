/* Concept pages respect "reduce motion". When the OS asks for it, offer a one-click
   override so the motion concepts can still be evaluated. The choice is remembered. */
(function () {
  var mq = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)');
  if (!mq || !mq.matches) return;
  var forced = /[?&]motion=1/.test(location.search);
  try { forced = forced || localStorage.getItem('rgm-motion') === '1'; } catch (e) {}
  if (/[?&]motion=0/.test(location.search)) { forced = false; try { localStorage.removeItem('rgm-motion'); } catch (e) {} }
  window.RGM_FORCE_MOTION = forced;
  if (forced) {
    Array.prototype.forEach.call(document.styleSheets, function (ss) {
      try {
        for (var i = ss.cssRules.length - 1; i >= 0; i--) {
          var r = ss.cssRules[i];
          if (r.media && /prefers-reduced-motion/.test(r.media.mediaText)) ss.deleteRule(i);
        }
      } catch (e) {}
    });
  }
  var b = document.createElement('div');
  b.setAttribute('role', 'region');
  b.setAttribute('aria-label', 'Анимации');
  b.style.cssText = 'position:fixed;left:12px;bottom:12px;z-index:300;max-width:calc(100% - 24px);display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:10px 10px 10px 16px;border-radius:16px;background:#111215;color:#F2EDE3;font:500 13px/1.4 system-ui,-apple-system,"Segoe UI",sans-serif;box-shadow:0 16px 40px -16px rgba(0,0,0,.6)';
  var t = document.createElement('span');
  t.textContent = forced ? 'Анимации включены вручную' : 'В системе отключены анимации — концепт показан статично';
  var btn = document.createElement('button');
  btn.type = 'button';
  btn.textContent = forced ? 'Выключить' : 'Показать анимации';
  btn.style.cssText = 'height:36px;padding:0 14px;border-radius:99px;border:0;background:#F2EDE3;color:#111215;font:600 13px system-ui,-apple-system,"Segoe UI",sans-serif;cursor:pointer';
  btn.addEventListener('click', function () {
    try { forced ? localStorage.removeItem('rgm-motion') : localStorage.setItem('rgm-motion', '1'); } catch (e) {}
    location.href = location.pathname + (forced ? '?motion=0' : '?motion=1') + location.hash;
  });
  var x = document.createElement('button');
  x.type = 'button'; x.textContent = '×'; x.setAttribute('aria-label', 'Скрыть');
  x.style.cssText = 'width:36px;height:36px;border-radius:50%;border:0;background:transparent;color:#BDB6A8;font:400 20px system-ui;cursor:pointer';
  x.addEventListener('click', function () { b.remove(); });
  b.appendChild(t); b.appendChild(btn); b.appendChild(x);
  function mount() { document.body.appendChild(b); }
  document.body ? mount() : document.addEventListener('DOMContentLoaded', mount);
})();
