/* ═══════════════════════════════════════════════════════════════════
   ОТПРАВКА ЧЕТЫРЁХ ФОРМ РЕГИСТРАЦИИ
   ═══════════════════════════════════════════════════════════════════
   КУДА УХОДЯТ ЗАЯВКИ. В тот же контур, что и на текущем сайте:
       POST https://api.ragimoff.org/api/training-reg
       Content-Type: text/plain;charset=utf-8
       {type:'registration', fname, lname, phone, email, address,
        service, lang, note, source, attachments:[]}
   Это принципиально: канон (правило 69) прямо запрещает ломать
   существующую схему — «текущий сайт работает и активен, в нём есть
   админ-панель, привязанная к серверу, и форма регистрации, связанная
   с телеграм-ботом... текущий не трогаем вообще». Поэтому заявки с
   новой страницы приходят туда же, где их уже умеют обрабатывать, и
   ничего перенастраивать не нужно.

   ПОЧЕМУ service РАЗНЫЙ. Именно он отличает четыре формы друг от друга
   в админке: обучение, индивидуальный тренинг, консультация, бизнес.
   Значения взяты такие же, как в существующем коде (consult|...,
   b2b-request), чтобы приёмник не пришлось переучивать.

   ЧТО ДЕЛАЕТСЯ ПРИ ОШИБКЕ. Владелец ругал «дохлые» кнопки (канон 110).
   Поэтому: кнопка блокируется и показывает «Отправляем…», при успехе —
   подтверждение, при сбое — понятный текст и запасной путь в WhatsApp.
   Молча ничего не происходит только в одном случае — если скрипт вообще
   не загрузился; тогда форма отправляется обычным способом.
   ═══════════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  var API = 'https://api.ragimoff.org/api/training-reg';
  var WA = 'https://wa.me/994702200376';

  /* ПОДПИСИ — с самой страницы, а не зашиты в код: тексты живут в данных,
     и при смене языка меняются вместе с ними. */
  function L(root, key, fallback) {
    return root.getAttribute('data-' + key) || fallback;
  }

  function markBad(el, bad) {
    if (el) el.classList.toggle('is-bad', !!bad);
  }

  function send(payload) {
    return fetch(API, {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify(payload)
    }).then(
      function (r) { return r.ok; },
      function () { return false; }
    );
  }

  function showMsg(form, text, ok) {
    var m = form.querySelector('.reg__msg');
    if (!m) return;
    m.hidden = false;
    m.className = 'reg__msg ' + (ok ? 'is-ok' : 'is-err');
    m.innerHTML = ok ? text : (text + ' <a href="' + WA + '" target="_blank" rel="noopener">WhatsApp</a>');
  }

  /* ── ПЕРЕКЛЮЧЕНИЕ ФОРМ ───────────────────────────────────────────── */
  function initTabs(reg) {
    var tabs = reg.querySelectorAll('.reg__tab');
    var panels = reg.querySelectorAll('.reg__panel');
    Array.prototype.forEach.call(tabs, function (t) {
      t.addEventListener('click', function () {
        Array.prototype.forEach.call(tabs, function (x) {
          x.setAttribute('aria-selected', x === t ? 'true' : 'false');
        });
        Array.prototype.forEach.call(panels, function (p) {
          p.classList.toggle('is-on', p.getAttribute('data-panel') === t.getAttribute('data-tab'));
        });
      });
    });
  }

  /* ── ОБЩАЯ ОТПРАВКА ПО ФОРМЕ ─────────────────────────────────────── */
  function initForm(form, opts) {
    var need = opts.need || [];

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = form.querySelector('.reg__msg'), btn = form.querySelector('button[type="submit"]');
      var ok = true;

      need.forEach(function (n) {
        var el = form.querySelector('[name="' + n + '"]');
        var bad = !el || !el.value.trim();
        markBad(el, bad);
        if (bad) ok = false;
      });

      if (!ok) { showMsg(form, L(form, 'req', 'Заполните выделенные поля'), false); return; }

      var val = function (n) { var el = form.querySelector('[name="' + n + '"]'); return el ? el.value.trim() : ''; };
      var radios = function (n) {
        var r = form.querySelector('input[name="' + n + '"]:checked');
        return r ? r.value : '';
      };

      var note = (opts.note ? opts.note(form, val, radios) : '').trim();
      var service = opts.service(form, val, radios);

      if (btn) { btn.disabled = true; btn.setAttribute('data-lbl', btn.textContent); btn.textContent = L(form, 'sending', 'Отправляем…'); }

      send({
        type: 'registration',
        fname: val('fname'),
        lname: val('lname'),
        phone: val('phone'),
        email: val('email'),
        address: '',
        service: service,
        lang: document.documentElement.lang || 'ru',
        note: note,
        source: '69/' + location.pathname.replace(/^\//, ''),
        attachments: []
      }).then(function (okSend) {
        if (btn) { btn.disabled = false; btn.textContent = btn.getAttribute('data-lbl') || 'Отправить'; }
        if (okSend) {
          form.reset();
          showMsg(form, L(form, 'ok', 'Заявка принята. Мы свяжемся с вами.'), true);
        } else {
          showMsg(form, L(form, 'err', 'Не удалось отправить заявку.'), false);
        }
      });
    });
  }

  function start() {
    var reg = document.querySelector('.reg');
    if (!reg) return;
    initTabs(reg);

    /* 1. ОБУЧЕНИЕ — стандартные цены, ведущий известен заранее */
    var f1 = document.getElementById('regTraining');
    if (f1) initForm(f1, {
      need: ['fname', 'phone', 'program'],
      service: function (v, val) { return 'training|' + val('program'); },
      note: function (v, val) { return 'Программа: ' + val('program'); }
    });

    /* 2. ИНДИВИДУАЛЬНЫЙ ТРЕНИНГ — клиент сам выбирает ведущего,
       канон: минимум 20 часов, от 2000 AZN за одного, 3000 за двоих. */
    var f2 = document.getElementById('regIndividual');
    if (f2) initForm(f2, {
      need: ['fname', 'phone'],
      service: function (v, val, radios) { return 'individual|' + (radios('who') || 'any'); },
      note: function (v, val, radios) {
        return ['Часов: ' + (val('hours') || '20+'),
                'Ведущий: ' + (radios('who') || 'любой'),
                val('topic') ? 'Тема: ' + val('topic') : ''].filter(Boolean).join(' · ');
      }
    });

    /* 3. КОНСУЛЬТАЦИЯ — формат и число участников влияют на цену,
       значения service такие же, как в существующем коде: consult|one|online */
    var f3 = document.getElementById('regConsult');
    if (f3) initForm(f3, {
      need: ['fname', 'phone'],
      service: function (v, val, radios) {
        return 'consult|' + (radios('who') || 'one') + '|' + (radios('format') || 'online');
      },
      note: function (v, val, radios) {
        return ['Участников: ' + (radios('who') || 'один'),
                'Формат: ' + (radios('format') || 'онлайн'),
                val('topic') ? 'Тема: ' + val('topic') : ''].filter(Boolean).join(' · ');
      }
    });

    /* 4. БИЗНЕС-ТРЕНИНГ — заявка без оплаты, как в существующем коде
       (service: 'b2b-request'). */
    var f4 = document.getElementById('regB2b');
    if (f4) initForm(f4, {
      need: ['fname', 'phone', 'company'],
      service: function () { return 'b2b-request'; },
      note: function (v, val) {
        return ['Компания: ' + val('company'),
                'Участников: ' + (val('count') || '—'),
                val('goal') ? 'Задача: ' + val('goal') : ''].filter(Boolean).join(' · ');
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
