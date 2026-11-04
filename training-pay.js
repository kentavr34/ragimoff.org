/* ───────────────────────────────────────────────────────────────────────────
   ЗАЯВКА НА ТРЕНИНГ → ОПЛАТА В EPOINT. Один модуль для всех страниц программ
   (tehsil.html и program-*.html, AZ/RU/EN).

   Канон Кенана (04.11.2026): в форме только телефон, имя, фамилия,
   удостоверение личности и выбор программы. Рассрочку/предоплату в форме НЕ
   выбирают — клиент решает это на странице ePoint. После «Отправить» заявка
   сохраняется и клиент СРАЗУ уходит на страницу оплаты ePoint.

   КЕНАН 04.11.2026 (вечер): клиент либо платит сразу цену предоплаты
   («Öncədən ödənişdə», напр. 500), либо оформляет рассрочку через банк на
   ПОЛНУЮ цену («Tam qiymət», 600). ePoint за один запрос даёт ОДНУ страницу
   (проверено живыми запросами 04.11: без is_installment — карточная форма
   PashaBank; с is_installment=1 — страница рассрочки TamKart/BirKart/BolKart),
   разные суммы в одной ссылке задать нельзя. Поэтому после «Отправить» в
   форме появляются ДВЕ кнопки: «Ödə indi — 500 AZN» и «Hissə-hissə (bank) —
   600 AZN»; каждая создаёт свой платёж ePoint (сервер считает сумму сам).

   КАК РАБОТАЕТ:
     1) проверка полей (свой validate: имя, фамилия, телефон, удостоверение,
        программа — сообщения на языке страницы);
     2) JSON на /api/training-reg (файлы — base64). Сервер сохраняет заявку,
        САМ считает сумму по канону цен программы (сумма из браузера не
        принимается) и в том же ответе отдаёт redirect_url страницы ePoint;
     3) location.href = redirect_url. Если в ответе ссылки нет (сбой ePoint) —
        запасной вызов /api/billing/epoint/training; если и он не дал ссылки —
        понятное сообщение с кнопкой «повторить» и WhatsApp.
     Сумма > 2000 AZN (лимит ePoint на операцию) делится сервером на равные
     части; следующие части открывает страница успеха.

   ПОЧЕМУ ПЕРЕХВАТ НА document В ФАЗЕ CAPTURE: на страницах висят ещё два
   обработчика этой формы (wireRegForm из shared.js и встроенный в tehsil.html);
   здесь — один, остальные до формы не доходят (stopImmediatePropagation).
   ─────────────────────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  var API = 'https://api.ragimoff.org';
  var FORM_IDS = ['regForm'];
  var MAX_FILE = 5 * 1024 * 1024;

  var L = (document.documentElement.getAttribute('lang') || 'az').slice(0, 2);
  var T = ({
    az: { name: 'Ad və soyadı yazın', phone: 'Mobil nömrəni yazın', id: 'Şəxsiyyət vəsiqəsini əlavə edin',
          sending: 'Göndərilir…', toPay: 'Ödəniş səhifəsi açılır…',
          prog: 'Proqramı seçin', big: '5 MB-dan böyükdür. Faylı kiçildib yenidən cəhd edin.',
          payErr: 'Müraciətiniz qəbul edildi, lakin ödəniş səhifəsini açmaq alınmadı.',
          sendErr: 'Göndərmək alınmadı. Bir daha cəhd edin və ya',
          retry: 'Ödənişə keç', wa: 'WhatsApp ilə yazın',
          choose: 'Müraciətiniz qəbul edildi. Ödəniş üsulunu seçin:',
          payNow: 'Ödə indi', payNowHint: 'öncədən ödəniş, endirimlə',
          payInst: 'Hissə-hissə (bank)', payInstHint: 'tam qiymət, taksiti bank rəsmiləşdirir' },
    ru: { name: 'Укажите имя и фамилию', phone: 'Укажите мобильный номер', id: 'Приложите удостоверение личности',
          sending: 'Отправляем…', toPay: 'Открываем страницу оплаты…',
          prog: 'Выберите программу', big: 'больше 5 МБ. Уменьшите файл и попробуйте снова.',
          payErr: 'Заявка принята, но страницу оплаты открыть не удалось.',
          sendErr: 'Не удалось отправить. Попробуйте ещё раз или',
          retry: 'Перейти к оплате', wa: 'Напишите в WhatsApp',
          choose: 'Заявка принята. Выберите способ оплаты:',
          payNow: 'Оплатить сейчас', payNowHint: 'предоплата со скидкой',
          payInst: 'В рассрочку (банк)', payInstHint: 'полная цена, рассрочку оформляет банк' },
    en: { name: 'Enter your first and last name', phone: 'Enter your mobile number', id: 'Attach your ID document',
          sending: 'Sending…', toPay: 'Opening the payment page…',
          prog: 'Choose a programme', big: 'is larger than 5 MB. Please reduce it and try again.',
          payErr: 'Your application was received, but the payment page could not be opened.',
          sendErr: 'Could not send. Please try again or',
          retry: 'Go to payment', wa: 'Write to us on WhatsApp',
          choose: 'Your application was received. Choose how to pay:',
          payNow: 'Pay now', payNowHint: 'prepayment with discount',
          payInst: 'Instalments (bank)', payInstHint: 'full price, arranged by the bank' }
  })[L] || null;
  if (!T) T = { name: 'Name', phone: 'Phone', id: 'ID', sendErr: 'Error', sending: 'Göndərilir…', toPay: '…', prog: 'Proqramı seçin', big: '> 5 MB',
                payErr: 'Ödəniş səhifəsini açmaq alınmadı.', retry: 'Ödənişə keç', wa: 'WhatsApp',
                choose: 'Ödəniş üsulunu seçin:', payNow: 'Ödə indi', payNowHint: '',
                payInst: 'Hissə-hissə (bank)', payInstHint: '' };

  function val(form, name) {
    var el = form.querySelector('[name="' + name + '"]');
    return el ? String(el.value || '').trim() : '';
  }

  /* Файлы: на tehsil.html — пул window.regFilePool (input очищается после
     выбора), на страницах программ — обычные input[type=file]. */
  function pickFiles(form) {
    var out = [], pool = window.regFilePool || {}, seen = {};
    Object.keys(pool).forEach(function (field) {
      (pool[field] || []).forEach(function (f) { out.push({ field: field, file: f }); });
      if ((pool[field] || []).length) seen[field] = true;
    });
    Array.prototype.forEach.call(form.querySelectorAll('input[type="file"]'), function (inp) {
      if (seen[inp.name] || !inp.files) return;
      Array.prototype.forEach.call(inp.files, function (f) { out.push({ field: inp.name, file: f }); });
    });
    return out;
  }

  function toBase64(file) {
    return new Promise(function (res) {
      var r = new FileReader();
      r.onload = function () { res(String(r.result).split(',')[1] || ''); };
      r.onerror = function () { res(''); };
      r.readAsDataURL(file);
    });
  }

  function regPost(payload) {
    if (typeof submitRegistration === 'function') return submitRegistration(payload);
    return fetch(API + '/api/training-reg', {
      method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify(payload)
    }).then(function (r) { return { ok: r.ok }; }, function () { return { ok: false }; });
  }

  function payPost(pay) {
    return fetch(API + '/api/billing/epoint/training', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(pay)
    }).then(function (r) { return r.json(); });
  }

  /* Данные для ePoint — отдельной функцией, чтобы их можно было проверить
     без перехода к оплате: window.trainingPayBuild(form). */
  function buildPay(form) {
    var prog = form.querySelector('input[name="proqram"]:checked');
    var program = prog ? prog.value : '';
    return {
      name: (val(form, 'ad') + ' ' + val(form, 'soyad')).trim(),
      phone: val(form, 'telefon'),
      program: program,
      amount: 0,   /* сумму считает сервер по программе */
      months: 0,
      mode: 'prepay',   /* 'prepay' — сразу, цена предоплаты; 'installment' — полная, банк */
      folder: ''        /* папка заявки с сервера — чтобы номер заказа лёг к заявке */
    };
  }
  window.trainingPayBuild = buildPay;

  function showPayError(form, pay) {
    var box = form.querySelector('.form-error');
    if (!box) {
      box = document.createElement('p');
      box.className = 'form-error';
      box.style.cssText = 'margin:14px 0 0;padding:12px 14px;border:1px solid rgba(220,90,90,.5);' +
        'background:rgba(220,90,90,.08);color:#E8A0A0;font-size:.875rem;line-height:1.6;';
      form.appendChild(box);
    }
    box.style.display = 'block';
    box.innerHTML = T.payErr + ' <a href="#" class="tp-retry" style="color:var(--accent);font-weight:700;">' +
      T.retry + '</a> · <a href="https://wa.me/994702200376" target="_blank" rel="noopener" ' +
      'style="color:var(--accent);font-weight:700;">' + T.wa + '</a>';
    box.querySelector('.tp-retry').onclick = function (ev) {
      ev.preventDefault();
      goPay(form, pay, null);
    };
  }

  /* ДВЕ КНОПКИ ВЫБОРА СПОСОБА ОПЛАТЫ (Кенан 04.11.2026). prices — от сервера
     ({prepay, full}); суммы на кнопках только для показа, сервер считает сам. */
  function showPayChoice(form, pay, prices) {
    var old = form.querySelector('.tp-choice');
    if (old) old.parentNode.removeChild(old);
    var submit = form.querySelector('button[type="submit"]');
    if (submit) submit.style.display = 'none';
    var box = document.createElement('div');
    box.className = 'tp-choice';
    box.style.cssText = 'margin:18px 0 0;padding:16px;border:1px solid rgba(201,169,97,.45);' +
      'background:rgba(201,169,97,.07);border-radius:10px;';
    function b(id, label, sum, hint) {
      return '<button type="button" class="btn btn-fill tp-' + id + '" style="width:100%;margin-top:10px;' +
        'padding:14px 18px;">' + label + ' — ' + sum + ' AZN</button>' +
        (hint ? '<p style="margin:4px 0 0;font-size:.8rem;opacity:.75;">' + hint + '</p>' : '');
    }
    box.innerHTML = '<p style="margin:0;font-weight:700;">' + T.choose + '</p>' +
      b('now', T.payNow, prices.prepay, T.payNowHint) +
      b('inst', T.payInst, prices.full, T.payInstHint);
    var anchor = submit ? (submit.closest('.form-footer') || submit.parentNode) : null;
    if (anchor && anchor.parentNode) anchor.parentNode.insertBefore(box, anchor.nextSibling);
    else form.appendChild(box);
    box.querySelector('.tp-now').onclick = function () {
      pay.mode = 'prepay'; goPay(form, pay, this);
    };
    box.querySelector('.tp-inst').onclick = function () {
      pay.mode = 'installment'; goPay(form, pay, this);
    };
    if (box.scrollIntoView) box.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  function goPay(form, pay, btn, readyUrl) {
    if (btn) { if (!btn.getAttribute('data-label')) btn.setAttribute('data-label', btn.textContent); btn.textContent = T.toPay; btn.disabled = true; }
    var go = readyUrl
      ? Promise.resolve({ ok: true, redirect_url: readyUrl })
      : payPost(pay);
    return go.then(function (d) {
      if (d && d.ok && d.redirect_url) { location.href = d.redirect_url; return; }
      throw new Error((d && d.error) || 'no redirect_url');
    }).catch(function (err) {
      console.warn('[training-pay] ePoint:', err);
      showPayError(form, pay);
      if (btn) { btn.textContent = btn.getAttribute('data-label') || 'Göndər'; btn.disabled = false; }
    });
  }

  /* Проверка обязательных полей: имя, фамилия, телефон, удостоверение, программа. */
  function validate(form) {
    var ok = true, first = null;
    function bad(el, msg) {
      ok = false;
      if (!el) return;
      el.setAttribute('data-need', msg);
      if (typeof regFieldError === 'function') regFieldError(el, true);
      if (!first) first = el;
    }
    function good(el) { if (el && typeof regFieldError === 'function') regFieldError(el, false); }
    ['ad', 'soyad'].forEach(function (n) {
      var el = form.querySelector('[name="' + n + '"]');
      if (el && !String(el.value || '').trim()) bad(el, T.name); else good(el);
    });
    var ph = form.querySelector('[name="telefon"]');
    if (ph && String(ph.value || '').replace(/\D/g, '').length < 7) bad(ph, T.phone); else good(ph);
    var idIn = form.querySelector('[name="shexsiyyet"]');
    var n = ((window.regFilePool || {}).shexsiyyet || []).length;
    if (!n && idIn && idIn.files) n = idIn.files.length;
    if (!n) bad(idIn, T.id); else good(idIn);
    var radios = form.querySelector('input[name="proqram"]');
    if (radios && !form.querySelector('input[name="proqram"]:checked')) bad(radios, T.prog); else good(radios);
    if (!ok && first) {
      var tgt = (first.type === 'radio' || first.type === 'file') ? (first.closest('.form-group, .form-field') || first) : first;
      if (tgt.scrollIntoView) tgt.scrollIntoView({ behavior: 'smooth', block: 'center' });
      try { if (first.type !== 'radio' && first.type !== 'file') first.focus({ preventScroll: true }); } catch (e) {}
    }
    return ok;
  }

  function showSendFail(form) {
    var box = form.querySelector('.form-error');
    if (!box) {
      box = document.createElement('p');
      box.className = 'form-error';
      box.style.cssText = 'margin:14px 0 0;padding:12px 14px;border:1px solid rgba(220,90,90,.5);' +
        'background:rgba(220,90,90,.08);color:#E8A0A0;font-size:.875rem;line-height:1.6;';
      form.appendChild(box);
    }
    box.style.display = 'block';
    box.innerHTML = T.sendErr + ' <a href="https://wa.me/994702200376" target="_blank" rel="noopener" ' +
      'style="color:var(--accent);font-weight:700;">' + T.wa + '</a>.';
  }

  async function onSubmit(e) {
    var form = e.target;
    if (!form || FORM_IDS.indexOf(form.id) < 0) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    if (form.getAttribute('data-busy') === '1') return;

    if (!validate(form)) return;
    var pay = buildPay(form);

    var files = pickFiles(form);
    for (var i = 0; i < files.length; i++) {
      if (files[i].file.size > MAX_FILE) { alert('"' + files[i].file.name + '" ' + T.big); return; }
    }

    var btn = form.querySelector('button[type="submit"]');
    if (btn) {
      if (!btn.getAttribute('data-label')) btn.setAttribute('data-label', btn.textContent);
      btn.disabled = true; btn.textContent = T.sending;
    }
    form.setAttribute('data-busy', '1');

    var attachments = [];
    for (var j = 0; j < files.length; j++) {
      var data = await toBase64(files[j].file);
      if (data) attachments.push({ field: files[j].field, filename: files[j].file.name,
                                   mime: files[j].file.type || 'application/octet-stream', data: data });
    }

    var payload = {
      type: 'registration',
      fname: val(form, 'ad'), lname: val(form, 'soyad'),
      phone: pay.phone, email: '', address: '',
      service: pay.program, lang: L,
      note: '',
      source: location.pathname.replace(/^\//, '') || 'tehsil.html',
      attachments: attachments
    };

    var res = await regPost(payload);
    if (!res || !res.ok) {
      form.removeAttribute('data-busy');
      if (btn) { btn.disabled = false; btn.textContent = btn.getAttribute('data-label'); }
      showSendFail(form);
      return;
    }
    var err = form.querySelector('.form-error');
    if (err) err.style.display = 'none';
    var d = res.data || {};
    pay.folder = d.folder || '';
    form.removeAttribute('data-busy');
    if (btn) { btn.disabled = false; btn.textContent = btn.getAttribute('data-label') || btn.textContent; }
    if (d.prices && d.prices.prepay && d.prices.full) {
      showPayChoice(form, pay, d.prices);          /* две кнопки: сразу / рассрочка */
    } else {
      await goPay(form, pay, btn, d.redirect_url || '');   /* старый сервер: сразу к оплате */
    }
  }

  document.addEventListener('submit', onSubmit, true);
})();
