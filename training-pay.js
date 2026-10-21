/* ───────────────────────────────────────────────────────────────────────────
   ЗАЯВКА НА ТРЕНИНГ + ОПЛАТА — один модуль для всех страниц программ.
   Задание Кенана (21.10.2026):
     • одна кнопка «Göndər» вместо «Qeydiyyat Formasını Göndər»;
     • по нажатию — уведомление, что заявка отправлена и её нужно оплатить;
     • следующий шаг оплаты: адрес, город, e-mail, сумма;
     • убрать кнопки «Ödəniş et» и «Taksitlə ödəniş üçün müraciət», которые
       раньше дописывались к форме из этого файла;
     • «Ali Təhsil Diplomu» — необязательное и второе поле (сделано в HTML).

   ПОЧЕМУ БЫЛО СЛОМАНО: форма постила на относительный /api/training-reg —
   на статическом сайте это 404, заявки не доходили вообще. Теперь адрес
   абсолютный: https://api.ragimoff.org/api/training-reg (CORS открыт).
   ─────────────────────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  var API_REG = 'https://api.ragimoff.org/api/training-reg';
  var API_PAY = 'https://api.ragimoff.org/api/billing/epoint/training';

  var TXT = {
    sending: 'Göndərilir…',
    sent: 'Müraciətiniz göndərildi',
    sentSub: 'Qeydiyyatı tamamlamaq üçün ödəniş etməlisiniz. Aşağıdakı düymə ilə ödəniş addımına keçin.',
    pay: 'Ödəniş et',
    later: 'Sonra',
    payTitle: 'Ödəniş',
    paySub: 'Məlumatları təsdiqləyin və ödənişi tamamlayın.',
    addr: 'Ünvan',
    city: 'Şəhər',
    email: 'E-poçt',
    amount: 'Məbləğ',
    confirm: 'Ödənişə keç',
    back: 'Geri',
    need: 'Ad, soyad və telefon lazımdır',
    errSend: 'Müraciət göndərilmədi. Yenidən cəhd edin.',
    errPay: 'Ödənişə keçmək alınmadı. Yenidən cəhd edin.'
  };

  function $(s, c) { return (c || document).querySelector(s); }
  function val(sel) { var el = $(sel); return el ? String(el.value || '').trim() : ''; }

  /* ── цена программы ───────────────────────────────────────────────────── */
  function findAmount() {
    var el = $('[data-price], .price, .program-price, .tariff-price');
    if (el) {
      var m = String(el.textContent || '').replace(/\s/g, '').match(/(\d{3,6})/);
      if (m) return parseInt(m[1], 10);
    }
    var body = String(document.body.innerText || document.body.textContent || '').replace(/\s/g, '');
    var m2 = body.match(/(\d{3,6})(?:₼|AZN)/i);
    return m2 ? parseInt(m2[1], 10) : 0;
  }

  function findProgram() {
    var h = $('h1');
    return (h ? String(h.textContent || '').trim() : document.title).replace(/\s+/g, ' ').slice(0, 120);
  }

  /* ── модальное окно ───────────────────────────────────────────────────── */
  function ui() {
    var style = document.createElement('style');
    style.textContent =
      '.trp-scrim{position:fixed;inset:0;background:rgba(8,8,10,.72);z-index:99990;display:none;' +
      'align-items:center;justify-content:center;padding:20px;opacity:0;transition:opacity .18s}' +
      '.trp-scrim.is-on{opacity:1}' +
      '.trp-box{background:#121214;border:1px solid rgba(201,169,97,.45);max-width:520px;width:100%;' +
      'padding:28px 26px;color:#eee;font:15px/1.65 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;' +
      'max-height:90vh;overflow:auto}' +
      '.trp-box h3{margin:0 0 8px;font-size:19px;color:#e8d9a8;font-weight:600}' +
      '.trp-box p{margin:0 0 16px;color:#c9c9cf;font-size:14.5px}' +
      '.trp-f{margin:0 0 12px}' +
      '.trp-f label{display:block;font-size:12.5px;letter-spacing:.04em;text-transform:uppercase;' +
      'color:#8f8f98;margin-bottom:6px}' +
      '.trp-f input{width:100%;box-sizing:border-box;background:#0c0c0e;border:1px solid #2b2b31;' +
      'color:#eee;padding:11px 13px;font-size:15px;outline:none}' +
      '.trp-f input:focus{border-color:#c9a961}' +
      '.trp-row{display:flex;gap:10px;margin-top:18px}' +
      '.trp-btn{flex:1;padding:14px 16px;border:1px solid #c9a961;background:#c9a961;color:#141414;' +
      'font:600 14px/1 system-ui,sans-serif;letter-spacing:.05em;text-transform:uppercase;cursor:pointer}' +
      '.trp-btn--ghost{background:transparent;color:#c9a961}' +
      '.trp-btn[disabled]{opacity:.55;cursor:default}' +
      '.trp-amt{display:flex;justify-content:space-between;align-items:baseline;padding:12px 0;' +
      'border-top:1px solid #2b2b31;margin-top:6px;font-size:15px}' +
      '.trp-amt b{color:#e8d9a8;font-size:19px}';
    document.head.appendChild(style);

    var scrim = document.createElement('div');
    scrim.className = 'trp-scrim';
    scrim.innerHTML = '<div class="trp-box" role="dialog" aria-modal="true"></div>';
    document.body.appendChild(scrim);
    return {
      scrim: scrim,
      box: $('.trp-box', scrim),
      open: function (html) {
        this.box.innerHTML = html;
        scrim.style.display = 'flex';
        requestAnimationFrame(function () { scrim.classList.add('is-on'); });
      },
      close: function () { scrim.classList.remove('is-on'); scrim.style.display = 'none'; }
    };
  }

  /* ── шаг 1: заявка отправлена ─────────────────────────────────────────── */
  function stepSent(m, onPay) {
    m.open(
      '<h3>' + TXT.sent + '</h3><p>' + TXT.sentSub + '</p>' +
      '<div class="trp-row"><button class="trp-btn trp-btn--ghost" data-x="later">' + TXT.later +
      '</button><button class="trp-btn" data-x="pay">' + TXT.pay + '</button></div>'
    );
    $('[data-x="later"]', m.box).onclick = function () { m.close(); };
    $('[data-x="pay"]', m.box).onclick = function () { stepPay(m, onPay); };
  }

  /* ── шаг 2: оплата — адрес, город, e-mail, сумма ──────────────────────── */
  function stepPay(m, data) {
    var amount = data.amount || findAmount();
    m.open(
      '<h3>' + TXT.payTitle + '</h3><p>' + TXT.paySub + '</p>' +
      '<div class="trp-f"><label>' + TXT.addr + '</label><input id="trp-addr" autocomplete="street-address"></div>' +
      '<div class="trp-f"><label>' + TXT.city + '</label><input id="trp-city" autocomplete="address-level2"></div>' +
      '<div class="trp-f"><label>' + TXT.email + '</label><input id="trp-email" type="email" autocomplete="email"></div>' +
      (amount ? '<div class="trp-amt"><span>' + TXT.amount + '</span><b>' + amount + ' ₼</b></div>' : '') +
      '<div class="trp-row"><button class="trp-btn trp-btn--ghost" data-x="back">' + TXT.back +
      '</button><button class="trp-btn" data-x="go">' + TXT.confirm + '</button></div>'
    );
    $('[data-x="back"]', m.box).onclick = function () {
      stepSent(m, data);
    };

    var go = $('[data-x="go"]', m.box);
    go.onclick = function () {
      var payload = {
        name: data.name, phone: data.phone, program: data.program,
        amount: amount, months: 0,
        address: val('#trp-addr'), city: val('#trp-city'),
        email: val('#trp-email') || data.email
      };
      go.disabled = true; go.textContent = TXT.sending;
      fetch(API_PAY, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }).then(function (r) { return r.json(); }).then(function (d) {
        if (d && d.ok && d.redirect_url) { location.href = d.redirect_url; return; }
        go.disabled = false; go.textContent = TXT.confirm;
        alert((d && d.error) || TXT.errPay);
      }).catch(function () {
        go.disabled = false; go.textContent = TXT.confirm;
        alert(TXT.errPay);
      });
    };
  }

  /* ── перехват отправки формы ──────────────────────────────────────────── */
  function boot() {
    var form = document.getElementById('regForm');
    if (!form) return;

    var submit = form.querySelector('button[type="submit"]');
    if (submit) submit.textContent = 'Göndər';

    var m = ui();

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = (val('[name="ad"]') + ' ' + val('[name="soyad"]')).trim();
      var phone = val('[name="telefon"]');
      if (!name || !phone) { alert(TXT.need); return; }

      var label = submit ? 'Göndər' : '';
      if (submit) { submit.disabled = true; submit.textContent = TXT.sending; }

      var data = {
        name: name, phone: phone,
        email: val('[name="email"]'),
        program: findProgram(),
        amount: findAmount()
      };

      var fd = new FormData(form);
      fetch(API_REG, { method: 'POST', body: fd })
        .then(function (r) { return r.ok ? r : Promise.reject(r.status); })
        .then(function () {
          if (submit) { submit.disabled = false; submit.textContent = label; }
          try { form.reset(); } catch (err) {}
          stepSent(m, data);
        })
        .catch(function (status) {
          if (submit) { submit.disabled = false; submit.textContent = label; }
          alert(TXT.errSend + (status ? ' (' + status + ')' : ''));
        });
    });

    console.log('[training-pay] заявка перехвачена; кнопки оплаты больше не добавляются');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else { boot(); }
})();
