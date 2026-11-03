/* ───────────────────────────────────────────────────────────────────────────
   ЗАЯВКА НА ТРЕНИНГ → ОПЛАТА В EPOINT. Один модуль для всех страниц программ
   (tehsil.html и program-*.html, AZ/RU/EN).

   Задание Кенана (02.11.2026): убрать из формы выбор «рассрочка / предоплата» —
   ePoint такую рассрочку не поддерживает. После «Göndər» заявка сохраняется, как
   раньше, и человек СРАЗУ уходит на страницу оплаты ePoint.

   КАК РАБОТАЕТ:
     1) проверка обязательных полей (validateRegForm из shared.js: имя, фамилия,
        телефон, удостоверение; диплом — для переподготовки) + выбрана программа;
     2) заявка с документами (base64) — JSON на /api/training-reg через
        submitRegistration() из shared.js (при сбое — запасной Apps Script);
     3) /api/billing/epoint/training {name, phone, program, amount, months:0} →
        сервер возвращает redirect_url ePoint → location.href.
     Сумма — цена разовой оплаты (предоплаты) программы из карточек цен.

   ПОЧЕМУ ПЕРЕХВАТ НА document В ФАЗЕ CAPTURE: на страницах висели ещё два
   обработчика той же формы (wireRegForm из shared.js и встроенный в tehsil.html),
   а старая версия этого файла слала FormData (multipart), которую сервер
   отвергал 400 «bad json». Заявка уходила дважды или не уходила вовсе.
   Здесь — один обработчик; остальные до формы не доходят (stopImmediatePropagation).
   ─────────────────────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  var API = 'https://api.ragimoff.org';
  var FORM_IDS = ['regForm'];
  var MAX_FILE = 5 * 1024 * 1024;

  /* Разовая оплата (предоплата) — канон цен Кенана, как в карточках tehsil.html. */
  var PREPAY = {
    'Ümumi Psixologiya': 3800, 'Общая психология': 3800, 'General Psychology': 3800,
    'Klinik Psixologiya': 6000, 'Клиническая психология': 6000, 'Clinical Psychology': 6000,
    'Psixoterapiya Praktikumu': 3000, 'Практикум по психотерапии': 3000, 'Psychotherapy Practicum': 3000,
    'Ailə Terapiyası': 500, 'Семейная терапия': 500, 'Family Therapy': 500,
    'Psixoanaliz': 500, 'Психоанализ': 500, 'Psychoanalysis': 500,
    'Psixodiaqnostika': 500, 'Психодиагностика': 500, 'Psychodiagnostics': 500
  };

  var L = (document.documentElement.getAttribute('lang') || 'az').slice(0, 2);
  var T = ({
    az: { sending: 'Göndərilir…', toPay: 'Ödəniş səhifəsi açılır…',
          prog: 'Proqramı seçin', big: '5 MB-dan böyükdür. Faylı kiçildib yenidən cəhd edin.',
          payErr: 'Müraciətiniz qəbul edildi, lakin ödəniş səhifəsini açmaq alınmadı.',
          retry: 'Ödənişə keç', wa: 'WhatsApp ilə yazın' },
    ru: { sending: 'Отправляем…', toPay: 'Открываем страницу оплаты…',
          prog: 'Выберите программу', big: 'больше 5 МБ. Уменьшите файл и попробуйте снова.',
          payErr: 'Заявка принята, но страницу оплаты открыть не удалось.',
          retry: 'Перейти к оплате', wa: 'Напишите в WhatsApp' },
    en: { sending: 'Sending…', toPay: 'Opening the payment page…',
          prog: 'Choose a programme', big: 'is larger than 5 MB. Please reduce it and try again.',
          payErr: 'Your application was received, but the payment page could not be opened.',
          retry: 'Go to payment', wa: 'Write to us on WhatsApp' }
  })[L] || null;
  if (!T) T = { sending: 'Göndərilir…', toPay: '…', prog: 'Proqramı seçin', big: '> 5 MB',
                payErr: 'Ödəniş səhifəsini açmaq alınmadı.', retry: 'Ödənişə keç', wa: 'WhatsApp' };

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
      amount: PREPAY[program] || 0,
      months: 0
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

  function goPay(form, pay, btn) {
    if (btn) btn.textContent = T.toPay;
    return payPost(pay).then(function (d) {
      if (d && d.ok && d.redirect_url) { location.href = d.redirect_url; return; }
      throw new Error((d && d.error) || 'no redirect_url');
    }).catch(function (err) {
      console.warn('[training-pay] ePoint:', err);
      showPayError(form, pay);
      if (btn) btn.textContent = btn.getAttribute('data-label') || 'Göndər';
    });
  }

  async function onSubmit(e) {
    var form = e.target;
    if (!form || FORM_IDS.indexOf(form.id) < 0) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    if (form.getAttribute('data-busy') === '1') return;

    if (typeof validateRegForm === 'function' && !validateRegForm(form)) return;
    var pay = buildPay(form);
    if (!pay.program || !pay.amount) {
      var grp = form.querySelector('input[name="proqram"]');
      if (grp && grp.scrollIntoView) grp.scrollIntoView({ behavior: 'smooth', block: 'center' });
      alert(T.prog);
      return;
    }

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
      phone: pay.phone, email: val(form, 'email'), address: val(form, 'unvan'),
      service: pay.program, lang: L,
      note: ['Ödəniş: ePoint — ' + pay.amount + ' AZN', val(form, 'qeyd')].filter(Boolean).join(' | '),
      source: location.pathname.replace(/^\//, '') || 'tehsil.html',
      attachments: attachments
    };

    var res = await regPost(payload);
    if (!res || !res.ok) {
      form.removeAttribute('data-busy');
      if (btn) { btn.disabled = false; btn.textContent = btn.getAttribute('data-label'); }
      if (typeof showSendError === 'function') showSendError(form); else alert('Error');
      return;
    }
    var err = form.querySelector('.form-error');
    if (err) err.style.display = 'none';
    await goPay(form, pay, btn);
    form.removeAttribute('data-busy');
    if (btn) btn.disabled = false;
  }

  document.addEventListener('submit', onSubmit, true);
})();
