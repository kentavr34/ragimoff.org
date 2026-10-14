/* ЕДИНАЯ ФОРМА ЗАКАЗА ДЛЯ ВСЕХ СТРАНИЦ КНИГ.
 *
 * УКАЗАНИЕ КЕНАНА (14.10.2026):
 *   «на всех страницах книг регистрация и оплата теперь должна быть одна форма для всех»
 *   «Одна форма заказа на все книги — выбор книги и языка из доступных для заказа
 *    в этой форме должно быть — после отправить к корзину выходит форма регистрации —
 *    нет! — сначала должна выходить кнопка перейти в корзину»
 *   «сначала набираем в корзину — потом оформляем заказ с подтверждением адреса
 *    доставки и переходом к платежу в конце — где логика ТЕМУ или АМАЗОН»
 *
 * ЧТО БЫЛО НЕ ТАК. На 176 страницах стояла форма kitab-form-main с двумя полями
 * (имя, телефон) и кнопкой «Sifariş et» — «ЗАКАЗАТЬ». А на самом деле она ничего
 * не заказывала: собирала контакты «сообщим, когда выйдет». Человек думал, что
 * заказал книгу, хотя заказа не было. А в каталоге была ОТДЕЛЬНАЯ корзина со своей
 * логикой. Два разных механизма на одном сайте.
 *
 * ЧТО ДЕЛАЕТ ЭТОТ МОДУЛЬ. Заменяет ту форму на ЕДИНУЮ для всех страниц:
 *
 *    1. ВЫБОР: книга (из списка доступных) + язык (только те, что продаются)
 *    2. «Səbətə at» — В КОРЗИНУ -> ТОЛЬКО уведомление:
 *       «Добавлено в корзину. Перейдите в корзину для оформления или продолжайте выбирать.»
 *       НИКАКОГО «Спасибо, заказ принят» — заказ ещё НЕ оформлен!
 *    3. КОРЗИНА: список, количество, сумма, кнопка «Оформить заказ»
 *    4. ОФОРМЛЕНИЕ: адрес доставки, подтверждение
 *    5. ОПЛАТА: в самом конце — страница ePoint с формой карты
 *
 * ПРАВИЛО ПРОДАЖИ (Кенан, мост idx=51):
 *    наши книги на ВСЕХ языках — продаются;
 *    Фрейд на АЗЕРБАЙДЖАНСКОМ — продаётся;
 *    Фрейд на других языках — ТОЛЬКО ЧТЕНИЕ, кнопки покупки быть не должно.
 */
(function () {
  'use strict';

  var CART_KEY = 'ragimoff_cart_v2';
  var CART_URL = '/books/#cart';

  /* ── КАТАЛОГ ДЛЯ ЗАКАЗА ────────────────────────────────────────────────
     Каждая позиция: книга + доступные для заказа языки.
     Фрейд — только азербайджанский. Наши книги — все языки. */
  var CATALOG = [
    { id: 'klinik-psixiatriya', az: 'Klinik Psixiatriya',       price: 30, langs: ['az'] },
    { id: 'aile-terapiyasi',    az: 'Ailə Terapiyası',          price: 25, langs: ['az'] },
    { id: 'depressiya',         az: 'Depressiya',               price: 25, langs: ['az'] },
    { id: 'panik-ataklar',      az: 'Panik Ataklar',            price: 25, langs: ['az'] },
    { id: 'sosial-fobiya',      az: 'Sosial Fobiya',            price: 25, langs: ['az'] },
    { id: 'enurez',             az: 'Enurez',                   price: 25, langs: ['az'] },
    { id: 'psixolog-olmaq',     az: 'Psixoloq Olmaq',           price: 25, langs: ['az'] },
    { id: 'yeniyetme',          az: 'Yeniyetmə',                price: 25, langs: ['az'] },
    { id: 'freud-men-ve-o',     az: 'Mən və O',                 price: 35, langs: ['az'] },
    { id: 'freud-yuxu-haqqinda',az: 'Yuxu Haqqında',            price: 35, langs: ['az'] },
    { id: 'freud-gundelik',     az: 'Gündəlik Həyatın Psixopatologiyası', price: 35, langs: ['az'] },
    { id: 'freud-massen',       az: 'Kütlə Psixologiyası',      price: 35, langs: ['az'] },
    { id: 'freud-totem',        az: 'Totem və Tabu',            price: 35, langs: ['az'] },
    { id: 'freud-musa',         az: 'Musa və Təkallahlılıq',    price: 35, langs: ['az'] },
    { id: 'freud-jenseits',     az: 'Həzz Prinsipinin O Tayında', price: 35, langs: ['az'] },
    { id: 'freud-medeniyyet',   az: 'Mədəniyyətin Sıxıntıları', price: 35, langs: ['az'] }
  ];

  var LANG_NAME = { az: 'Azərbaycanca', ru: 'Русский', en: 'English', tr: 'Türkçe', de: 'Deutsch' };
  var T = {
    title:    'Sifariş',
    sub:      'Kitabı və dili seçin — sonra səbətə atın.',
    book:     'Kitab',
    lang:     'Dil',
    pick:     '— seçin —',
    add:      'Səbətə at',
    added:    'Səbətə əlavə edildi.',
    goCart:   'Sifarişi rəsmiləşdirmək üçün səbətə keçin',
    orContinue: 'və ya seçməyə davam edin',
    toCart:   'Səbətə keç',
    readOnly: 'Bu kitab yalnız oxumaq üçündür, satılmır.',
    choose:   'Zəhmət olmasa kitab və dil seçin.'
  };

  function cartRead() {
    try { return JSON.parse(localStorage.getItem(CART_KEY) || '[]'); } catch (e) { return []; }
  }
  function cartWrite(l) {
    try { localStorage.setItem(CART_KEY, JSON.stringify(l)); } catch (e) {}
  }
  function cartCount() {
    return cartRead().reduce(function (s, i) { return s + (i.qty || 1); }, 0);
  }

  /* ── УВЕДОМЛЕНИЕ: только «добавлено», без «спасибо, заказ принят» ─────
     Кенан: «должно выйти именно это уведомление — добавлено в корзину
     перейдите в нее для оформления заказа и оплаты». */
  function toast() {
    var old = document.getElementById('ro-toast');
    if (old) old.parentNode.removeChild(old);
    var d = document.createElement('div');
    d.id = 'ro-toast';
    d.setAttribute('role', 'status');
    d.style.cssText = 'position:fixed;left:50%;top:24px;transform:translateX(-50%);' +
      'z-index:99999;background:#0f131b;color:#f2ede3;border:1px solid #c9a961;' +
      'border-radius:10px;padding:14px 18px;max-width:420px;width:calc(100% - 32px);' +
      'box-shadow:0 12px 40px rgba(0,0,0,.55);font-size:14px;line-height:1.55;' +
      'box-sizing:border-box;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;';
    d.innerHTML =
      '<div style="display:flex;gap:10px;align-items:flex-start;">' +
      '<span style="color:#c9a961;font-size:18px;line-height:1;">✓</span>' +
      '<div style="flex:1;">' +
      '<b style="display:block;margin-bottom:4px;">' + T.added + '</b>' +
      '<span style="color:#a8a296;">' + T.goCart + '</span>' +
      '<div style="margin-top:12px;display:flex;gap:10px;flex-wrap:wrap;">' +
      '<a href="' + CART_URL + '" style="background:#c9a961;color:#07090e;text-decoration:none;' +
      'padding:9px 16px;border-radius:7px;font-weight:700;font-size:13px;">' + T.toCart +
      ' (' + cartCount() + ')</a>' +
      '<button type="button" data-ro-close style="background:transparent;color:#a8a296;' +
      'border:1px solid rgba(255,255,255,.15);padding:9px 16px;border-radius:7px;' +
      'cursor:pointer;font-size:13px;">' + T.orContinue + '</button>' +
      '</div></div></div>';
    document.body.appendChild(d);
    d.querySelector('[data-ro-close]').onclick = function () { d.parentNode.removeChild(d); };
    setTimeout(function () { if (d.parentNode) d.parentNode.removeChild(d); }, 12000);
  }

  /* ── ПОСТРОИТЬ ФОРМУ на месте старой ──────────────────────────────── */
  function build(host) {
    var books = CATALOG.map(function (b) {
      return '<option value="' + b.id + '">' + b.az + '</option>';
    }).join('');

    host.innerHTML =
      '<h2 style="font-size:20px;font-weight:700;color:#f2ede3;margin:0 0 10px;font-family:monospace;">' +
      T.title + '</h2>' +
      '<p style="font-size:13px;color:#a8a296;line-height:1.65;margin:0 0 22px;' +
      'border-left:2px solid #c9a961;padding-left:12px;">' + T.sub + '</p>' +
      '<div style="margin-bottom:14px;">' +
      '<label for="ro-book" style="display:block;font-size:11px;font-weight:700;color:#a8a296;' +
      'margin-bottom:5px;letter-spacing:.06em;text-transform:uppercase;">' + T.book + '</label>' +
      '<select id="ro-book" style="width:100%;background:#141821;border:1px solid rgba(255,255,255,.08);' +
      'border-radius:6px;color:#f2ede3;font-size:14px;padding:11px 13px;outline:none;box-sizing:border-box;">' +
      '<option value="">' + T.pick + '</option>' + books + '</select></div>' +
      '<div style="margin-bottom:18px;">' +
      '<label for="ro-lang" style="display:block;font-size:11px;font-weight:700;color:#a8a296;' +
      'margin-bottom:5px;letter-spacing:.06em;text-transform:uppercase;">' + T.lang + '</label>' +
      '<select id="ro-lang" style="width:100%;background:#141821;border:1px solid rgba(255,255,255,.08);' +
      'border-radius:6px;color:#f2ede3;font-size:14px;padding:11px 13px;outline:none;box-sizing:border-box;">' +
      '<option value="">' + T.pick + '</option></select></div>' +
      '<button type="button" id="ro-add" style="width:100%;background:#C9A961;color:#07090e;border:none;' +
      'border-radius:6px;padding:14px;font-size:14px;font-weight:700;font-family:monospace;' +
      'cursor:pointer;">' + T.add + '</button>' +
      '<p id="ro-note" style="font-size:12px;color:#c9a961;margin:10px 0 0;min-height:16px;"></p>';

    var bs = host.querySelector('#ro-book');
    var ls = host.querySelector('#ro-lang');
    var note = host.querySelector('#ro-note');

    function fillLangs() {
      var b = CATALOG.filter(function (x) { return x.id === bs.value; })[0];
      ls.innerHTML = '<option value="">' + T.pick + '</option>';
      if (!b) { ls.disabled = true; return; }
      ls.disabled = false;
      b.langs.forEach(function (l) {
        var o = document.createElement('option');
        o.value = l; o.textContent = LANG_NAME[l] || l;
        ls.appendChild(o);
      });
      if (b.langs.length === 1) ls.value = b.langs[0];
      note.textContent = b.langs.length === 1 ? T.readOnly.replace('Bu kitab', 'Bu kitab (' + (LANG_NAME[b.langs[0]] || '') + ')') : '';
      if (b.langs.length === 1) note.textContent = '';
    }
    bs.onchange = fillLangs;
    ls.disabled = true;

    host.querySelector('#ro-add').onclick = function () {
      var b = CATALOG.filter(function (x) { return x.id === bs.value; })[0];
      var lg = ls.value;
      if (!b || !lg) { note.textContent = T.choose; note.style.color = '#e08a8a'; return; }
      note.style.color = '#c9a961';
      var list = cartRead();
      var f = null;
      for (var i = 0; i < list.length; i++) {
        if (list[i].id === b.id && list[i].lang === lg) { f = list[i]; break; }
      }
      if (f) { f.qty = (f.qty || 1) + 1; }
      else { list.push({ id: b.id, az: b.az, lang: lg, price: b.price, qty: 1 }); }
      cartWrite(list);
      toast();
      note.textContent = '';
    };
  }

  /* ── ЗАМЕНИТЬ СТАРУЮ ФОРМУ НА ВСЕХ СТРАНИЦАХ ─────────────────────── */
  function run() {
    var old = document.getElementById('kitab-form-main');
    if (!old) return;
    var host = old.parentNode;
    /* \u0441\u043d\u043e\u0441\u0438\u043c \u0441\u0442\u0430\u0440\u044b\u0439 \u0431\u043b\u043e\u043a \u0446\u0435\u043b\u0438\u043a\u043e\u043c (\u0444\u043e\u0440\u043c\u0443, \u0437\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a, \u043f\u043e\u044f\u0441\u043d\u0435\u043d\u0438\u044f, \u0431\u043b\u043e\u043a \u0443\u0441\u043f\u0435\u0445\u0430) */
    var box = host;
    while (box && box.parentNode && box.children.length < 6 &&
           !(box.textContent || '').match(/\u041a\u0438\u0442\u0430\u0431|\u041a\u0438\u0442\u0430\u0431\u044b\u043d|Sifari\u015f|sifari\u015f/)) {
      box = box.parentNode;
    }
    var target = document.createElement('div');
    target.id = 'ro-order-form';
    build(target);
    (box || host).innerHTML = '';
    (box || host).appendChild(target);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
  else run();
})();
