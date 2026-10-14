/* =====================================================================
   RAGIMOFF · books/books.js — «Kitablar»
   Заказ — та же механика, что на основном сайте: POST в Apps Script
   (сервер + Google-таблица + Telegram). Плюс: модал заказа, появление
   карточек, лёгкий тилт обложек.
   ===================================================================== */
(function () {
  'use strict';

  var root = document.documentElement;
  var reduceQ = window.matchMedia('(prefers-reduced-motion: reduce)');
  var fineQ = window.matchMedia('(hover: hover) and (pointer: fine)');
  var reduce = reduceQ.matches, fine = fineQ.matches;

  /* эндпоинты заказа — те же, что у формы «Kitabın sifarişi» на сайте:
     сервер сайта (api.ragimoff.org) + Apps Script (Google-таблица + Telegram) */
  var BOOK_API = 'https://api.ragimoff.org/api/book-order';
  /* создание платежа Epoint: сумму считает СЕРВЕР, браузеру доверять нельзя */
  var PAY_API = 'https://api.ragimoff.org/api/billing/epoint/create';
  var ORDER_API = 'https://script.google.com/macros/s/AKfycbw-ejwk4wslNpEhMB11Yknj5cjPBZJkoc4nf8BTMP8lxROc8ZxtAWkkXtgv5E8GLzxyfw/exec';

  /* строки интерфейса — из страницы (window.__booksUI), запас — азербайджанский */
  var T = window.__booksUI || {};
  function t(key, fallback) { return T[key] || fallback; }

  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }

  /* ── появление карточек ── */
  function initReveal() {
    var nodes = $$('.card, .h1');
    if (!nodes.length) return;
    nodes.forEach(function (n, i) { n.style.setProperty('--d', (i * 70) + 'ms'); });
    if (!('IntersectionObserver' in window) || reduce) return;
    root.classList.add('anim');
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.08, rootMargin: '0px 0px -8% 0px' });
    nodes.forEach(function (n) { io.observe(n); });
  }

  /* ── поиск по книгам (название, автор, год) ── */
  function initSearch() {
    var q = $('#q'); if (!q) return;
    var cards = $$('.card');
    var count = $('#count');
    var chips = $$('.chip');
    var activeAuthor = '';
    var empty = null;
    function run() {
      var v = (q.value || '').trim().toLowerCase();
      var shown = 0;
      cards.forEach(function (c) {
        var okAuthor = !activeAuthor || c.getAttribute('data-author') === activeAuthor;
        var hay = (c.textContent || '').toLowerCase().replace(/\s+/g, ' ');
        var ok = (!v || hay.indexOf(v) !== -1) && okAuthor;
        c.hidden = !ok;
        if (ok) shown++;
      });
      /* секция автора видна, только если в ней остались карточки */
      $$('.author-sec').forEach(function (h) {
        var g = h.getAttribute('data-author');
        h.hidden = !$$('.card[data-author="' + g + '"]').some(function (c) { return !c.hidden; });
      });
      if (count) count.textContent = t('count', '%n kitab').replace('%n', shown);
      var grid = $('.grid');
      if (grid) {
        if (!empty) { empty = document.createElement('p'); empty.className = 'no-results'; empty.textContent = t('empty', 'Heç nə tapılmadı'); grid.parentNode.appendChild(empty); }
        empty.hidden = shown !== 0;
      }
    }
    chips.forEach(function (b) {
      b.addEventListener('click', function () {
        activeAuthor = b.getAttribute('data-author') || '';
        chips.forEach(function (x) { x.classList.toggle('is-on', x === b); });
        run();
      });
    });
    q.addEventListener('input', run);
    run();
  }

  /* ── модал заказа ── */
  function initOrder() {
    var modal = $('[data-modal]');
    if (!modal) return;
    var form = $('#order-form');
    var ok = $('#o-ok');
    var sub = $('#o-sub');
    var select = $('#o-book');
    var nameI = $('#o-name');
    var phoneI = $('#o-phone');
    var addrI = $('#o-address');   /* 13.10.2026: адрес доставки бумажной книги */
    var current = '';
    var lastFocus = null;

    function open(book) {
      current = book || '';
      lastFocus = document.activeElement;
      ok.hidden = true;
      form.hidden = false;
      form.reset();
      /* 13.10.2026: если книги нет в списке, ДОБАВЛЯЕМ её отдельным пунктом.
         Иначе select оставался на первом пункте, и в заказ уходила ЧУЖАЯ книга
         (проверено: заказ открывался для книги серии Фрейда, а уходила
         «Klinik Psixiatriya · 100 ₼»). */
      if (select && current) {
        var idx = -1;
        for (var i = 0; i < select.options.length; i++) {
          if (select.options[i].value === current) { idx = i; break; }
        }
        if (idx < 0) {
          var opt = document.createElement('option');
          opt.value = current;
          opt.textContent = current;
          select.appendChild(opt);
          idx = select.options.length - 1;
        }
        select.selectedIndex = idx;
      }
      modal.classList.add('is-open');
      modal.setAttribute('aria-hidden', 'false');
      root.classList.add('lock');
      setTimeout(function () { if (nameI) nameI.focus(); }, 80);
    }
    function close() {
      modal.classList.remove('is-open');
      modal.setAttribute('aria-hidden', 'true');
      root.classList.remove('lock');
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    $$('[data-order]').forEach(function (b) {
      b.addEventListener('click', function () {
        var book = b.getAttribute('data-order') || '';
        var bookPrice = b.getAttribute('data-price') || '';
        var price = b.getAttribute('data-price') || '';
        open(price ? book + ' · ' + price : book);
      });
    });
    $$('[data-close]', modal).forEach(function (b) { b.addEventListener('click', close); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });

    form.addEventListener('submit', async function (e) {
      e.preventDefault();
      var name = (nameI.value || '').trim();
      var phone = (phoneI.value || '').trim();
      var address = addrI ? (addrI.value || '').trim() : '';
      if (!name || !phone || !address) {
        alert(t('fill', 'Zəhmət olmasa Ad Soyad, Telefon və Çatdırılma ünvanını daxil edin.'));
        return;
      }
      var parts = name.split(/\s+/);
      var book = (select && select.value) || current;   /* «Название · цена» */
      var payload = {
        type: 'registration',
        fname: parts[0] || '',
        lname: parts.slice(1).join(' ') || '',
        phone: phone,
        address: address,          /* сервер /api/book-order пишет это в book_orders.address */
        service: 'Kitab sifarişi — ' + book,
        note: book,
        source: 'ragimoff.org' + location.pathname
      };
      var btn = $('button[type="submit"]', form);
      if (btn) { btn.textContent = t('sending', 'Göndərilir…'); btn.disabled = true; }
      var body = JSON.stringify(payload);
      /* оба канала, как в форме «Kitabın sifarişi» на сайте:
         сервер сайта (регистрация заказа) + Apps Script (Google-таблица + Telegram) */
      try { fetch(BOOK_API, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: body }).catch(function () {}); } catch (err) {}
      try {
        await fetch(ORDER_API, {
          method: 'POST', mode: 'no-cors',
          headers: { 'Content-Type': 'text/plain;charset=utf-8' },
          body: body
        });
      } catch (err) { /* no-cors: ответ не читаем, ошибка сети не блокирует UX */ }
      if (btn) { btn.textContent = t('submit', 'Sifariş et'); btn.disabled = false; }
      form.hidden = true;
      ok.hidden = false;
    });
  }

  /* ── тилт обложек ── */
  function initTilt() {
    if (!fine) return;
    $$('.card__cover').forEach(function (el) {
      var cover = $('.cover', el);
      if (!cover) return;
      el.addEventListener('mousemove', function (e) {
        if (reduce) return;
        var b = el.getBoundingClientRect();
        var dx = (e.clientX - b.left) / b.width - 0.5;
        var dy = (e.clientY - b.top) / b.height - 0.5;
        cover.style.transform = 'perspective(1000px) rotateY(' + (dx * 6).toFixed(2) + 'deg) rotateX(' + (-dy * 6).toFixed(2) + 'deg) translateY(-8px)';
      });
      el.addEventListener('mouseleave', function () { cover.style.transform = ''; });
    });
  }

  /* ===================================================================
     КОРЗИНА (Səbət) — магазин книг, оформление заказа БЕЗ онлайн-оплаты.
     Решение владельца 13.10.2026: сначала магазин + корзина + оформление,
     приём платежей (epoint) — позже. Поэтому здесь только сбор заявки:
     состав заказа, контакт и адрес доставки уходят на сервер и в Telegram,
     оплата и доставка подтверждаются менеджером по телефону.

     Всё строится из JS: HTML каталогов править не нужно, корзина работает
     сразу в трёх языковых версиях.
     =================================================================== */

  var CART_KEY = 'ragimoff_cart_v1';

  var CART_T = {
    az: { add: 'Səbətə at', added: 'Əlavə edildi', cart: 'Səbət', empty: 'Səbət boşdur',
          total: 'Cəm', checkout: 'Sifarişi tamamla', remove: 'Sil', clear: 'Səbəti təmizlə',
          qty: 'Say', ask: 'qiymət sorğu ilə', send: 'Göndərilir…',
          done: 'Təşəkkür edirik!<br>Sifarişiniz qeydə alındı — tezliklə əlaqə saxlayacağıq.',
          nameL: 'Ad Soyad', phoneL: 'Mobil nömrə', addrL: 'Çatdırılma ünvanı',
          addrPh: 'Ölkə, şəhər, küçə, ev, mənzil, poçt indeksi',
          fill: 'Zəhmət olmasa Ad Soyad, Telefon və ünvanı daxil edin.',
          noPrice: 'Qiyməti telefonla dəqiqləşdirəcəyik.', pay: 'Ödənişə keç', payErr: 'Ödənişə keçmək alınmadı. Yenidən cəhd edin.',
          discount: 'Bütün Freyd kolleksiyasına endirim',
          payable: 'Ödəniləcək',
          buyLang: 'Kitabın dili',
          instL: 'Taksit imkanı', instNo: 'Taksitsiz — tam ödəniş',
          instMo: 'ay', instBtn: 'Taksit müraciəti göndər',
          instHint: 'Taksiti BANK rəsmiləşdirir — bu düymə yalnız müraciət göndərir, ödəniş tutulmur.',
          instPick: 'Zəhmət olmasa taksit müddətini seçin.',
          instOk: 'Taksit müraciətiniz qəbul edildi. Bank sizinlə əlaqə saxlayacaq — ödəniş hələ tutulmayıb.',
          freudAzOnly: 'Freydin kitabları yalnız Azərbaycan dilində satılır.',
          geoBtn: 'Ünvanı avtomatik təyin et',
          geoWait: 'Yer müəyyən edilir…',
          geoNo: 'Ünvanı təyin etmək alınmadı — zəhmət olmasa əl ilə yazın.' },
    ru: { add: 'В корзину', added: 'Добавлено', cart: 'Корзина', empty: 'Корзина пуста',
          total: 'Итого', checkout: 'Оформить заказ', remove: 'Удалить', clear: 'Очистить корзину',
          qty: 'Кол-во', ask: 'цена по запросу', send: 'Отправляем…',
          done: 'Спасибо!<br>Заказ принят — мы скоро свяжемся с вами.',
          nameL: 'Имя и фамилия', phoneL: 'Мобильный телефон', addrL: 'Адрес доставки',
          addrPh: 'Страна, город, улица, дом, квартира, индекс',
          fill: 'Пожалуйста, укажите имя, телефон и адрес.',
          fill: 'Пожалуйста, укажите имя, телефон и адрес.',
          noPrice: 'Цену уточним по телефону.', pay: 'Перейти к оплате', payErr: 'Не удалось перейти к оплате. Попробуйте снова.',
          discount: 'Скидка на всю коллекцию Фрейда',
          payable: 'К оплате',
          buyLang: 'Язык издания',
          instL: 'Рассрочка', instNo: 'Без рассрочки — полная оплата',
          instMo: 'мес.', instBtn: 'Отправить заявку на рассрочку',
          instHint: 'Рассрочку оформляет БАНК — эта кнопка только отправляет заявку, деньги не списываются.',
          instPick: 'Пожалуйста, выберите срок рассрочки.',
          instOk: 'Заявка на рассрочку принята. Банк свяжется с вами — оплата ещё не списана.',
          freudAzOnly: 'Книги Фрейда продаются только на азербайджанском.',
          geoBtn: 'Определить адрес автоматически',
          geoWait: 'Определяем местоположение…',
          geoNo: 'Не удалось определить адрес — введите вручную.' },
    en: { add: 'Add to cart', added: 'Added', cart: 'Cart', empty: 'Your cart is empty',
          total: 'Total', checkout: 'Place the order', remove: 'Remove', clear: 'Clear cart',
          qty: 'Qty', ask: 'price on request', send: 'Sending…',
          done: 'Thank you!<br>Your order has been received — we will contact you soon.',
          nameL: 'Full name', phoneL: 'Mobile phone', addrL: 'Delivery address',
          addrPh: 'Country, city, street, building, apartment, postal code',
          fill: 'Please provide your name, phone and address.',
          fill: 'Please provide your name, phone and address.',
          noPrice: 'We will confirm the price by phone.', pay: 'Proceed to payment', payErr: 'Could not proceed to payment. Please try again.',
          discount: 'Full Freud collection discount',
          payable: 'Payable',
          buyLang: 'Edition language',
          instL: 'Instalments', instNo: 'No instalment — full payment',
          instMo: 'months', instBtn: 'Send an instalment request',
          instHint: 'The instalment is arranged by the BANK — this button only sends a request, no money is taken.',
          instPick: 'Please choose an instalment term.',
          instOk: 'Your instalment request was accepted. The bank will contact you — no payment has been taken yet.',
          freudAzOnly: 'Books by Freud are sold in Azerbaijani only.',
          geoBtn: 'Detect my address',
          geoWait: 'Detecting location…',
          geoNo: 'Could not detect the address — please type it.' }
  };

  function cartLang() {
    var l = (document.documentElement.lang || 'az').slice(0, 2).toLowerCase();
    return CART_T[l] ? l : 'az';
  }

  /* ── ЯЗЫК ПОКУПКИ (Кенан 13.10, голосом) ────────────────────────────────
     «В книгах Фрейда язык только азербайджанский можно выбрать при покупке.
      А книги касаются клинической психиатрии, других — покупка на других языках
      тоже открыто. Клиническая психиатрия, эра Феникса, вирус ВИНИ, шизофрения —
      эти книги на всех трёх языках можно купить. И язык нужно выбирать
      опционально.»

     ПРАВИЛО:
       • в корзине ТОЛЬКО книги Фрейда → язык покупки ВСЕГДА азербайджанский,
         даже если человек читает русскую или английскую версию сайта: продаём
         только наш азербайджанский перевод;
       • есть авторская книга → язык выбирает покупатель (азербайджанский,
         русский, английский).
     Названия ниже — это data-order карточек, то есть ровно то, что попадает
     в корзину. Список менять только вместе с каталогом. */
  var MY_BOOKS = ['Klinik Psixiatriya', 'Günahkarlıq Virusu',
                  'Şizofreniya', 'Feniks Erası'];
  var BUY_LANGS = [['az', 'AZ'], ['ru', 'RU'], ['en', 'EN']];

  function isMyBook(title) {
    var s = cleanTitle(title || '');
    for (var i = 0; i < MY_BOOKS.length; i++) {
      if (s.indexOf(MY_BOOKS[i]) === 0) return true;   // \u043d\u0430\u0447\u0430\u043b\u043e \u0441\u043e\u0432\u043f\u0430\u0434\u0430\u0435\u0442
    }
    return false;
  }

  function cartHasMyBook() {
    return cartRead().some(function (x) { return isMyBook(x.title); });
  }

  function cartBuyLang() {
    if (!cartHasMyBook()) return 'az';       // \u0424\u0440\u0435\u0439\u0434 \u2014 \u0442\u043e\u043b\u044c\u043a\u043e \u0430\u0437\u0435\u0440\u0431\u0430\u0439\u0434\u0436\u0430\u043d\u0441\u043a\u0438\u0439
    var sel = document.querySelector('input[name="buy-lang"]:checked');
    return sel ? sel.value : 'az';
  }
  function cstr(k) { return CART_T[cartLang()][k]; }

  function cartRead() {
    try { return JSON.parse(localStorage.getItem(CART_KEY) || '[]') || []; } catch (e) { return []; }
  }
  function cartWrite(items) {
    try { localStorage.setItem(CART_KEY, JSON.stringify(items)); } catch (e) {}
    cartBadge(items);
  }
  /* Цена товара. Берём СОХРАНЁННУЮ цену из корзины, и только если её нет —
     разбираем из названия. Раньше цена искалась только в названии, а в
     data-order её нет, поэтому вся корзина показывала «по запросу»
     и бумажный заказ уходил без суммы. */
  function priceOf(item) {
    if (item && item.price) {
      var m0 = String(item.price).match(/(\d[\d\s]*)\s*(₼|AZN|\$|€)/);
      if (m0) {
        var n0 = parseFloat(m0[1].replace(/\s/g, ''));
        if (!isNaN(n0)) return { num: n0, cur: m0[2] };
      }
    }
    var title = item && item.title !== undefined ? item.title : item;
    var m = String(title || '').match(/(\d[\d\s]*)\s*(₼|AZN|\$|€)/);
    if (!m) return null;
    var n = parseFloat(m[1].replace(/\s/g, ''));
    return isNaN(n) ? null : { num: n, cur: m[2] };
  }
  /* Скидка 20% на всю коллекцию Фрейда: считается, если в корзине есть
     позиция-коллекция (data-collection="freud"). */
  var COLLECTION_DISCOUNT = 20;
  function isCollection(title) {
    return /bütün freyd kolleksiyası/i.test(String(title || ''));
  }
  function cleanTitle(title) {
    return String(title || '').replace(/\s*·\s*(Kağız nüsxə|Бумажный экземпляр|Paper copy)\s*$/i, '').trim();
  }

  function cartBadge(items) {
    var b = $('#cart-badge');
    if (!b) return;
    var n = (items || cartRead()).reduce(function (s, i) { return s + (i.qty || 1); }, 0);
    b.textContent = n;
    b.hidden = n === 0;
  }

  /* Всплывающее уведомление «книга в корзине» с переходом в корзину.
     Живёт 4 секунды, не мешает читать каталог, закрывается нажатием.
     Кенан 14.10.2026: без него человек не понимал, попала ли книга в корзину. */
  function showCartToast(title) {
    var L = (document.documentElement.getAttribute('lang') || 'az').slice(0, 2);
    var TXT = {
      az: ['Səbətə əlavə edildi', 'Səbətə keç'],
      ru: ['Добавлено в корзину', 'Перейти в корзину'],
      en: ['Added to cart', 'Go to cart'],
      tr: ['Sepete eklendi', 'Sepete git']
    }[L] || ['OK', 'Cart'];

    var old = document.getElementById('cart-toast');
    if (old && old.parentNode) old.parentNode.removeChild(old);

    var el = document.createElement('div');
    el.id = 'cart-toast';
    el.setAttribute('role', 'status');
    el.style.cssText =
      'position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:120;' +
      'display:flex;align-items:center;gap:14px;max-width: calc(100vw - 32px);' +
      'padding:14px 18px;border-radius:12px;background:#141821;color:#f2ede3;' +
      'border:1px solid rgba(201,169,97,.5);box-shadow:0 10px 34px rgba(0,0,0,.5);' +
      'font-size:.9375rem;line-height:1.4;';
    var txt = document.createElement('span');
    txt.innerHTML = '<b>' + TXT[0] + '</b><br><span style="opacity:.75;font-size:.8125rem;">' +
                    String(title).replace(/[<>&]/g, '') + '</span>';
    var go = document.createElement('button');
    go.type = 'button';
    go.textContent = TXT[1];
    go.style.cssText = 'flex:0 0 auto;padding:9px 14px;border-radius:8px;border:0;' +
      'background:#C9A227;color:#07090E;font-weight:700;cursor:pointer;';
    go.addEventListener('click', function () {
      if (el.parentNode) el.parentNode.removeChild(el);
      openCart();
    });
    el.appendChild(txt);
    el.appendChild(go);
    document.body.appendChild(el);
    /* На телефоне уведомление не должно закрывать кнопку корзины —
       поэтому поднимаем его над ней. */
    if (window.innerWidth <= 640) el.style.bottom = '92px';
    setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 4000);
  }

  function cartAdd(title, price) {
    var items = cartRead();
    var name = cleanTitle(title);
    for (var i = 0; i < items.length; i++) {
      if (items[i].title === name) {
        items[i].qty = (items[i].qty || 1) + 1;
        if (price && !items[i].price) items[i].price = price;
        cartWrite(items);
        return items;
      }
    }
    items.push({ title: name, qty: 1, price: price || '' });
    cartWrite(items);
    return items;
  }
  function cartRemove(idx) {
    var items = cartRead();
    items.splice(idx, 1);
    cartWrite(items);
    return items;
  }

  /* ── ПРОФИЛЬ ПОКУПАТЕЛЯ: ИДЕНТИФИКАЦИЯ ПО НОМЕРУ ─────────────────────────
     Кенан 14.10.2026:
     «Если пользователь идентифицирован, то не нужно при каждом заказе спрашивать
      личные данные — только до идентификации; после просто добавлять в корзину.
      Для идентификации достаточно мобильного номера. Совпадения могут быть,
      поэтому при повторном заказе книг нужно переспросить — Имя и Фамилия — это
      ваш профиль? Если кнопка да — автовставление данных его профиля и переход
      к оплате.»

     ПОЧЕМУ ЗДЕСЬ, А НЕ В shared.js: книжные страницы shared.js НЕ грузят —
     проверил, из трёх страниц с books.js общий файл не подключает ни одна.
     Поэтому профиль живёт прямо здесь.

     ПОЧЕМУ ДАННЫЕ НА УСТРОЙСТВЕ, А НЕ ТОЛЬКО НА СЕРВЕРЕ: отдавать имя и адрес
     по одному номеру телефона нельзя — так можно узнать чужой адрес. Храним там,
     где человек сам вводил, и подтверждение спрашиваем у него же. */
  var PROFILE_KEY = 'ragimoff_profile_v1';

  function profileGet() {
    try {
      var raw = localStorage.getItem(PROFILE_KEY);
      if (!raw) return null;
      var p = JSON.parse(raw);
      return (p && p.phone) ? p : null;
    } catch (e) { return null; }
  }

  function profileSave(p) {
    try {
      if (!p || !p.phone) return;
      localStorage.setItem(PROFILE_KEY, JSON.stringify({
        name: String(p.name || '').slice(0, 120),
        phone: String(p.phone || '').slice(0, 40),
        address: String(p.address || '').slice(0, 300),
        ts: Date.now()
      }));
    } catch (e) {}
  }

  function profileClear() { try { localStorage.removeItem(PROFILE_KEY); } catch (e) {} }

  /* Строка «это ваш профиль?» над формой. Возвращает true, если показана. */
  function profileAsk(form, onYes) {
    var p = profileGet();
    if (!p || !form) return false;
    var L = (document.documentElement.getAttribute('lang') || 'az').slice(0, 2);
    var T = {
      az: ['Bu sizin profilinizdir?', 'Bəli, mənəm', 'Xeyr, başqa şəxsdir'],
      ru: ['Это ваш профиль?', 'Да, это я', 'Нет, это другой человек'],
      en: ['Is this your profile?', 'Yes, that is me', 'No, someone else'],
      tr: ['Bu sizin profiliniz mi?', 'Evet, benim', 'Hayır, başka biri']
    }[L] || ['Is this your profile?', 'Yes', 'No'];

    var old = form.querySelector('.profile-ask');
    if (old && old.parentNode) old.parentNode.removeChild(old);

    var box = document.createElement('div');
    box.className = 'profile-ask';
    box.style.cssText = 'margin:0 0 16px;padding:14px 16px;border-radius:10px;' +
      'border:1px solid rgba(201,169,97,.45);background:rgba(201,169,97,.08);line-height:1.5;';
    var who = document.createElement('div');
    who.style.cssText = 'font-size:.9375rem;margin-bottom:10px;';
    who.innerHTML = '<b>' + p.name.replace(/[<>&]/g, '') + '</b> · ' +
                    p.phone.replace(/[<>&]/g, '') + '<br>' +
                    '<span style="opacity:.85;font-size:.875rem;">' + T[0] + '</span>';
    var yes = document.createElement('button');
    yes.type = 'button'; yes.textContent = T[1];
    yes.style.cssText = 'padding:10px 16px;margin-right:8px;border-radius:8px;border:0;' +
      'background:#C9A227;color:#07090E;font-weight:700;cursor:pointer;';
    var no = document.createElement('button');
    no.type = 'button'; no.textContent = T[2];
    no.style.cssText = 'padding:10px 16px;border-radius:8px;cursor:pointer;' +
      'border:1px solid rgba(255,255,255,.25);background:transparent;color:inherit;';

    yes.addEventListener('click', function () {
      var n = form.querySelector('#c-name'), ph = form.querySelector('#c-phone'),
          ad = form.querySelector('#c-addr');
      if (n) n.value = p.name || '';
      if (ph) ph.value = p.phone || '';
      if (ad && p.address) ad.value = p.address;
      if (box.parentNode) box.parentNode.removeChild(box);
      if (typeof onYes === 'function') onYes();
    });
    no.addEventListener('click', function () {
      profileClear();
      var n = form.querySelector('#c-name'), ph = form.querySelector('#c-phone'),
          ad = form.querySelector('#c-addr');
      if (n) n.value = ''; if (ph) ph.value = ''; if (ad) ad.value = '';
      if (box.parentNode) box.parentNode.removeChild(box);
    });

    box.appendChild(who); box.appendChild(yes); box.appendChild(no);
    form.insertBefore(box, form.firstChild);
    return true;
  }

  function initCart() {
    var cards = $$('[data-order]');
    if (!cards.length) return;

    /* 1) кнопка «В корзину» рядом с каждой кнопкой бумажного заказа */
    cards.forEach(function (btn) {
      var title = btn.getAttribute('data-order') || '';
      var price = btn.getAttribute('data-price') || '';

      function doAdd() {
        cartAdd(title, price);
        var was = btn.textContent;
        btn.textContent = cstr('added');
        setTimeout(function () { btn.textContent = was; }, 1200);
        /* УВЕДОМЛЕНИЕ О ПОПАДАНИИ В КОРЗИНУ.
           Кенан 14.10.2026: «если попадает в корзину, то должно выходить уведомление
           о попадании в корзину». Раньше менялась только надпись на самой кнопке —
           на 1,2 секунды и незаметно, особенно если кнопка ниже экрана. Теперь
           всплывает сообщение с названием книги и переходом в корзину. */
        showCartToast(title);
      }

      /* КНОПКА УЖЕ ЕСТЬ В РАЗМЕТКЕ — вешаем обработчик НА НЕЁ.
         Раньше здесь стоял `return`, и такие кнопки оставались БЕЗ обработчика:
         нажать можно, в корзину ничего не попадает. Дефект был внесён, когда
         кнопки «Kağız nüsxə» заменили на готовые data-cart-btn. */
      if (btn.getAttribute('data-cart-btn')) {
        btn.addEventListener('click', doAdd);
        return;
      }

      var add = document.createElement('button');
      add.type = 'button';
      add.className = 'btn btn--cart';
      add.textContent = cstr('add');
      add.setAttribute('data-cart-btn', '1');
      add.addEventListener('click', doAdd);
      if (btn.parentNode) btn.parentNode.insertBefore(add, btn.nextSibling);
    });

    /* 2) плавающая кнопка корзины со счётчиком */
    var fab = document.createElement('button');
    fab.type = 'button';
    fab.className = 'cart-fab';
    fab.setAttribute('aria-label', cstr('cart'));
    fab.innerHTML = '<span class="cart-fab__ico" aria-hidden="true">🛒</span>' +
                    '<span id="cart-badge" class="cart-fab__n" hidden>0</span>';
    fab.addEventListener('click', openCart);
    document.body.appendChild(fab);
    cartBadge();

    /* 3) окно корзины — своя разметка, стили модала переиспользуются */
    var box = document.createElement('div');
    box.className = 'modal cart-modal';
    box.setAttribute('aria-hidden', 'true');
    box.innerHTML =
      '<div class="modal__scrim" data-cart-close></div>' +
      '<div class="modal__box" role="dialog" aria-modal="true" aria-labelledby="cart-h">' +
        '<button class="modal__x" data-cart-close aria-label="' + t('close', 'Bağla') + '">✕</button>' +
        '<h2 class="h2" id="cart-h">' + cstr('cart') + '</h2>' +
        '<div id="cart-body"></div>' +
      '</div>';
    document.body.appendChild(box);
    $$('[data-cart-close]', box).forEach(function (b) {
      b.addEventListener('click', function () { box.classList.remove('is-open'); box.setAttribute('aria-hidden', 'true'); });
    });

    function openCart() { render(); box.classList.add('is-open'); box.setAttribute('aria-hidden', 'false'); }

    function render() {
      var items = cartRead();
      var body = $('#cart-body', box);
      if (!items.length) {
        body.innerHTML = '<p class="cart-empty">' + cstr('empty') + '</p>';
        return;
      }
      var sum = 0, hasAsk = false, rows = '', hasColl = false;
      items.forEach(function (it, i) {
        var p = priceOf(it);
        if (p) sum += p.num * (it.qty || 1); else hasAsk = true;
        if (isCollection(it.title)) hasColl = true;
        rows += '<div class="cart-row">' +
                  '<span class="cart-row__t">' + it.title + '</span>' +
                  '<span class="cart-row__p">' + (p ? (p.num + ' ' + p.cur) : cstr('ask')) + '</span>' +
                  '<input class="cart-row__q" type="number" min="1" value="' + (it.qty || 1) + '" data-q="' + i + '" aria-label="' + cstr('qty') + '">' +
                  '<button type="button" class="cart-row__x" data-x="' + i + '">' + cstr('remove') + '</button>' +
                '</div>';
      });
      /* Скидка 20% на всю коллекцию Фрейда: в корзине есть позиция-коллекция */
      var discount = hasColl ? Math.round(sum * COLLECTION_DISCOUNT / 100) : 0;
      var payable = sum - discount;

      /* Геолокация: определяем адрес доставки в ОДИН КЛИК по кнопке.
         Согласие спрашивает браузер; при отказе или ошибке — обычный ввод. */
      function geoFill() {
        var out = $('#c-addr', body);
        if (!out) return;
        if (!navigator.geolocation) { alert(cstr('geoNo')); return; }
        out.value = cstr('geoWait');
        navigator.geolocation.getCurrentPosition(function (pos) {
          var la = pos.coords.latitude.toFixed(6);
          var lo = pos.coords.longitude.toFixed(6);
          var url = 'https://nominatim.openstreetmap.org/reverse?format=json&zoom=18&addressdetails=1&lat=' + la + '&lon=' + lo;
          fetch(url, { headers: { 'Accept': 'application/json' } })
            .then(function (r) { return r.json(); })
            .then(function (d) {
              var a = (d && d.address) || {};
              var parts = [a.road || a.pedestrian, a.house_number, a.suburb || a.neighbourhood,
                           a.city || a.town || a.village || a.county, a.country].filter(Boolean);
              out.value = parts.length ? parts.join(', ')
                                       : (d && d.display_name) || (la + ', ' + lo);
            })
            .catch(function () { out.value = la + ', ' + lo; });
        }, function () { out.value = ''; alert(cstr('geoNo')); },
           { enableHighAccuracy: true, timeout: 12000, maximumAge: 60000 });
      }

      body.innerHTML =
        rows +
        '<p class="cart-sum">' + cstr('total') + ': <b>' + sum + ' ₼</b>' +
          (hasAsk ? ' <span class="cart-note">' + cstr('noPrice') + '</span>' : '') + '</p>' +
        (discount ? '<p class="cart-sum">' + cstr('discount') + ' −' + COLLECTION_DISCOUNT +
          '%: <b>−' + discount + ' ₼</b></p>' +
          '<p class="cart-sum">' + cstr('payable') + ': <b>' + payable + ' ₼</b></p>' : '') +
        '<form id="cart-form" novalidate>' +
          /* Язык покупки. Для книг Фрейда выбора НЕТ: продаём только наш
             азербайджанский перевод, поэтому вместо выбора — честное пояснение,
             а не пустой список. Для авторских книг — выбор из трёх языков. */
          (cartHasMyBook()
            ? '<div class="field"><span>' + cstr('buyLang') + '</span>' +
              '<div class="buy-langs">' +
              BUY_LANGS.map(function (p, i) {
                return '<label class="buy-lang' + (i === 0 ? ' is-on' : '') + '">' +
                  '<input type="radio" name="buy-lang" value="' + p[0] + '"' +
                  (i === 0 ? ' checked' : '') + '>' + p[1] + '</label>';
              }).join('') +
              '</div></div>'
            : '<p class="cart-note cart-note--lang">' + cstr('freudAzOnly') + '</p>') +
          '<label class="field"><span>' + cstr('nameL') + '</span>' +
            '<input id="c-name" type="text" autocomplete="name" required></label>' +
          '<label class="field"><span>' + cstr('phoneL') + '</span>' +
            '<input id="c-phone" type="tel" placeholder="+994 XX XXX XX XX" autocomplete="tel" required></label>' +
          '<label class="field"><span>' + cstr('addrL') + '</span>' +
            '<textarea id="c-addr" rows="2" placeholder="' + cstr('addrPh') + '" autocomplete="street-address" required></textarea>' +
            '<button type="button" class="btn btn--ghost" id="c-geo">' + cstr('geoBtn') + '</button></label>' +
          '<button class="btn btn--main" type="button" id="c-pay">' + cstr('pay') + '</button>' +
          /* РАССРОЧКА ДЛЯ КНИГ (Кенан 13.10): «то же самое с книгами можно сделать,
             чтобы они могли выбрать рассрочку… они через какой-то банк оформляют
             рассрочку, а не через нашу систему». Кнопка отправляет заявку с выбранным
             сроком; деньги через ePoint при этом НЕ берём — иначе вышла бы двойная
             оплата, ведь банк списывает своё. */
          '<div class="inst-wrap">' +
            '<label class="field"><span>' + cstr('instL') + '</span>' +
              '<select id="c-months">' +
                '<option value="0">' + cstr('instNo') + '</option>' +
                '<option value="6">6 ' + cstr('instMo') + '</option>' +
                '<option value="12">12 ' + cstr('instMo') + '</option>' +
                '<option value="24">24 ' + cstr('instMo') + '</option>' +
              '</select></label>' +
            '<button class="btn btn--ghost" type="button" id="c-inst">' + cstr('instBtn') + '</button>' +
            '<p class="inst-hint">' + cstr('instHint') + '</p>' +
          '</div>' +
          '<button class="btn btn--cart" type="submit">' + cstr('checkout') + '</button>' +
        '</form>' +
        '<div class="cart-ok" id="cart-ok" hidden>' + cstr('done') + '</div>' +
        '<button type="button" class="cart-clear" id="cart-clear">' + cstr('clear') + '</button>';

      var payB = $('#c-pay', body);
      if (payB) payB.addEventListener('click', epointPay);

      /* ПРОФИЛЬ: если человек уже заказывал с этого устройства — не заставляем
         вводить всё заново. Показываем «Это ваш профиль?» и по «Да» подставляем
         имя, телефон и адрес, после чего ведём к оплате.
         Кенан 14.10.2026: «после идентификации просто добавлять в корзину»,
         «если кнопка да — автовставка данных его профиля и переход к оплате». */
      (function () {
        var f = $('#cart-form', body);
        if (!f) return;
        profileAsk(f, function () {
          var pb2 = $('#c-pay', body);
          if (pb2) { pb2.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
        });
      })();

      /* Рассрочка: тот же запрос, но с выбранным сроком. Сервер по нему понимает,
         что оплату через ePoint брать нельзя — рассрочку оформляет банк. */
      var instB = $('#c-inst', body);
      if (instB) instB.addEventListener('click', function () {
        var sel = $('#c-months', body);
        var m = parseInt((sel && sel.value) || '0', 10) || 0;
        if (!m) { alert(cstr('instPick')); return; }
        epointPay(m);
      });

      var geoB = $('#c-geo', body);
      if (geoB) geoB.addEventListener('click', geoFill);

      $$('[data-x]', body).forEach(function (b) {
        b.addEventListener('click', function () { cartRemove(+b.getAttribute('data-x')); render(); });
      });
      $$('[data-q]', body).forEach(function (b) {
        b.addEventListener('change', function () {
          var items2 = cartRead(), k = +b.getAttribute('data-q');
          var v = parseInt(b.value, 10);
          items2[k].qty = (v > 0 ? v : 1);
          cartWrite(items2);
          render();
        });
      });
      $('#cart-clear', body).addEventListener('click', function () { cartWrite([]); render(); });

      /* ОПЛАТА: после формы заказчика — переход на страницу оплаты Epoint.
         Сумму считает СЕРВЕР: в браузере её можно подменить в консоли. */
      function epointPay(months) {
        var list = cartRead();
        if (!list.length) return;
        var nm = ($('#c-name', body).value || '').trim();
        var ph = ($('#c-phone', body).value || '').trim();
        var ad = ($('#c-addr', body).value || '').trim();
        if (!nm || !ph || !ad) { alert(cstr('fill')); return; }
        /* Запоминаем профиль: следующий заказ с этого устройства заполнится сам. */
        profileSave({ name: nm, phone: ph, address: ad });
        var pb = $('#c-pay', body);
        var ib = $('#c-inst', body);
        var btn = (months > 0 && ib) ? ib : pb;
        var label = btn ? btn.textContent : '';
        if (btn) { btn.disabled = true; btn.textContent = cstr('send'); }
        function back() {
          if (btn) { btn.disabled = false; btn.textContent = label; }
        }
        fetch(PAY_API, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ items: list, name: nm, phone: ph, address: ad,
                                 lang: cartBuyLang(), months: months || 0 })
        }).then(function (r) { return r.json(); }).then(function (d) {
          if (d && d.ok && d.redirect_url) { location.href = d.redirect_url; return; }
          if (d && d.ok && d.installment) {
            /* Деньги НЕ списаны: заявку примет банк. Сказать об этом прямо, иначе
               человек решит, что уже заплатил, и не станет отвечать банку. */
            alert(cstr('instOk'));
            var ok = $('#cart-ok', body);
            if (ok) { ok.hidden = false; ok.innerHTML = cstr('instOk'); }
            back();
            return;
          }
          back();
          alert((d && d.error) || cstr('payErr'));
        }).catch(function () {
          back();
          alert(cstr('payErr'));
        });
      }

      $('#cart-form', body).addEventListener('submit', function (e) {
        e.preventDefault();
        var name = ($('#c-name', body).value || '').trim();
        var phone = ($('#c-phone', body).value || '').trim();
        var addr = ($('#c-addr', body).value || '').trim();
        if (!name || !phone || !addr) { alert(cstr('fill')); return; }
        /* Запоминаем профиль и здесь: заказ оформлен — данные пригодятся в следующий раз. */
        profileSave({ name: name, phone: phone, address: addr });
        var parts = name.split(/\s+/);
        var list = cartRead();
        /* Сумма и скидка уходят в заказ: без них на складе не знают, сколько
           брать с покупателя. Скидка 20% — если в корзине вся коллекция Фрейда. */
        var tot = 0, coll = false;
        list.forEach(function (x) {
          var pp = priceOf(x);
          if (pp) tot += pp.num * (x.qty || 1);
          if (isCollection(x.title)) coll = true;
        });
        var disc = coll ? Math.round(tot * COLLECTION_DISCOUNT / 100) : 0;
        var note = list.map(function (x) {
          var pp = priceOf(x);
          return x.title + ' x' + (x.qty || 1) + (pp ? ' = ' + (pp.num * (x.qty || 1)) + ' ₼' : '');
        }).join('; ');
        note += ' | Cəm: ' + tot + ' ₼';
        if (disc) note += ' | Kolleksiya endirimi ' + COLLECTION_DISCOUNT + '%: −' + disc + ' ₼ | Ödəniləcək: ' + (tot - disc) + ' ₼';
        var payload = {
          type: 'registration',
          fname: parts[0] || '',
          lname: parts.slice(1).join(' ') || '',
          phone: phone,
          address: addr,
          service: 'Səbət sifarişi — ' + list.length + ' kitab',
          note: note,
          source: 'ragimoff.org' + location.pathname
        };
        if (disc) payload.discount = String(COLLECTION_DISCOUNT);
        var body2 = JSON.stringify(payload);
        var btn = $('button[type="submit"]', body);
        if (btn) { btn.textContent = cstr('send'); btn.disabled = true; }
        try { fetch(BOOK_API, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: body2 }).catch(function () {}); } catch (err) {}
        try {
          fetch(ORDER_API, { method: 'POST', mode: 'no-cors',
            headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: body2 });
        } catch (err) {}
        $('#cart-form', box).hidden = true;
        $('#cart-ok', box).hidden = false;
        $('#cart-clear', box).hidden = true;
        cartWrite([]);
      });
    }
  }

  function boot() {
    initReveal();
    initSearch();
    initOrder();
    /* корзина — дополнительная возможность: если она когда-нибудь упадёт
       (старый браузер, заблокированное localStorage), каталог обязан остаться
       рабочим. Поэтому ошибку глушим и сообщаем в консоль, а не на страницу. */
    try { initCart(); } catch (e) {
      if (window.console && console.warn) console.warn('cart disabled:', e);
    }
    initTilt();
    reduceQ.addEventListener && reduceQ.addEventListener('change', function () { reduce = reduceQ.matches; });
    fineQ.addEventListener && fineQ.addEventListener('change', function () { fine = fineQ.matches; });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
