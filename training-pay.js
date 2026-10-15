/* ───────────────────────────────────────────────────────────────────────────
   ОПЛАТА ТРЕНИНГОВ — ОДИН МОДУЛЬ ДЛЯ ВСЕХ СТРАНИЦ ПРОГРАММ.

   ЗАЧЕМ (задание Кенана 15.10.2026): «Проверь и почини платежку также на тренинги».

   ЧТО НАШЁЛ:
     • на страницах программ (program-*.html, tehsil.html) есть только ЗАЯВКА —
       форма шлёт данные на /api/training-reg. ОНЛАЙН-ОПЛАТЫ НЕТ ВООБЩЕ.
     • при этом на сервере ОПЛАТА ТРЕНИНГОВ УЖЕ ЕСТЬ:
       POST /api/billing/epoint/training
       поля: name, phone, program, amount, months
       Ответ: { ok, redirect_url } — ссылка на страницу банка.
     • сервер сам делит сумму на части по 480 AZN (лимит ePoint) и проводит подряд.
     • при months > 0 сервер НЕ берёт деньги, а принимает заявку на рассрочку —
       её оформляет банк (иначе была бы двойная оплата).

   ЧТО ДЕЛАЕТ ЭТОТ МОДУЛЬ:
     находит цену программы и кнопку на странице, добавляет кнопку «Ödəniş et»
     и по нажатию ведёт на страницу банка. Никаких своих форм — берёт то, что
     человек уже ввёл в форме заявки.
   ─────────────────────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  var API = 'https://api.ragimoff.org/api/billing/epoint/training';

  /* Тексты: страница может быть на азербайджанском, русском или английском. */
  var L = (document.documentElement.getAttribute('lang') || 'az').slice(0, 2);
  var TXT = {
    az: { pay: 'Ödəniş et', wait: 'Göndərilir…', need: 'Ad, telefon və proqram lazımdır',
          err: 'Ödənişə keçmək alınmadı. Yenidən cəhd edin.', ask: 'Taksitlə ödəniş üçün müraciət' },
    ru: { pay: 'Оплатить', wait: 'Отправляем…', need: 'Нужны имя, телефон и программа',
          err: 'Не удалось перейти к оплате. Попробуйте снова.', ask: 'Заявка на рассрочку' },
    en: { pay: 'Pay now', wait: 'Sending…', need: 'Name, phone and program are required',
          err: 'Could not open the payment page. Please try again.', ask: 'Installment request' }
  }[L] || { pay: 'Ödəniş et', wait: '…', need: '—', err: '—', ask: '—' };

  /* Цена программы: ищем первое число с манатом в блоке цены. */
  function findAmount() {
    var el = document.querySelector('[data-price], .price, .program-price, .tariff-price');
    if (el) {
      var m = String(el.textContent || '').replace(/\s/g, '').match(/(\d{3,6})/);
      if (m) return parseInt(m[1], 10);
    }
    var m2 = String(document.body.innerText || '').replace(/\s/g, '').match(/(\d{3,6})(?:₼|AZN)/i);
    return m2 ? parseInt(m2[1], 10) : 0;
  }

  /* Программа: заголовок страницы — самое надёжное имя. */
  function findProgram() {
    var h = document.querySelector('h1');
    var t = h ? String(h.textContent || '').trim() : document.title;
    return t.replace(/\s+/g, ' ').slice(0, 120);
  }

  function field(name) {
    return document.querySelector('[name="' + name + '"], #' + name + ', #reg-' + name) || null;
  }

  function pay(btn, months) {
    var nm = field('name') || field('fname');
    var ph = field('phone');
    var name = nm ? String(nm.value || '').trim() : '';
    var phone = ph ? String(ph.value || '').trim() : '';
    if (!name || !phone) { alert(TXT.need); if (nm) nm.focus(); return; }

    var amount = findAmount();
    if (!amount) { amount = parseInt(btn.getAttribute('data-amount') || '0', 10) || 0; }
    if (!amount) { alert(TXT.err); return; }

    var label = btn.textContent;
    btn.disabled = true; btn.textContent = TXT.wait;

    fetch(API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: name, phone: phone, program: findProgram(),
                             amount: amount, months: months || 0 })
    }).then(function (r) { return r.json(); }).then(function (d) {
      if (d && d.ok && d.redirect_url) { location.href = d.redirect_url; return; }
      btn.disabled = false; btn.textContent = label;
      /* Рассрочку оформляет банк: деньги не списаны — говорим об этом прямо. */
      if (d && d.ok && d.installment) { alert(TXT.ask); return; }
      alert((d && d.error) || TXT.err);
    }).catch(function () {
      btn.disabled = false; btn.textContent = label; alert(TXT.err);
    });
  }

  function place() {
    var f = document.getElementById('regForm');
    if (!f || f.querySelector('.tr-pay-btn')) return;

    var box = document.createElement('div');
    box.className = 'tr-pay-box';
    box.style.cssText = 'margin:16px 0 0;display:flex;gap:10px;flex-wrap:wrap;';

    var b1 = document.createElement('button');
    b1.type = 'button'; b1.className = 'btn btn-fill tr-pay-btn';
    b1.textContent = TXT.pay;
    b1.addEventListener('click', function (e) { e.preventDefault(); pay(b1, 0); });

    var b2 = document.createElement('button');
    b2.type = 'button'; b2.className = 'btn btn-ghost tr-pay-btn';
    b2.textContent = TXT.ask;
    b2.addEventListener('click', function (e) { e.preventDefault(); pay(b2, 12); });

    box.appendChild(b1); box.appendChild(b2);
    f.appendChild(box);
    console.log('[training-pay] кнопки оплаты добавлены на страницу');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', place);
  } else { place(); }
})();
