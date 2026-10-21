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


/* ═══════════════════════════════════════════════════════════════════════════
   КНОПКА В ШАПКЕ СТРАНИЦЫ КНИГИ = «В КОРЗИНУ»
   Задание Кенана (21.10.2026): «она должна вести себя также как добавить
   в корзину — та же функция».

   ЧТО БЫЛО СЛОМАНО: книга добавлялась в ДРУГУЮ корзину (ragimoff_cart_v2),
   а каталог books.js читает ragimoff_cart_v1. Две корзины на одном сайте:
   то, что человек положил со страницы книги, в каталоге не появлялось.

   ТЕПЕРЬ: та же корзина и тот же формат элемента, что у каталога —
   { title, qty, price } в localStorage['ragimoff_cart_v1'].
   ═══════════════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var CART_KEY = 'ragimoff_cart_v1';
  var CATALOG_URL = '/books/';
  var MAP = {"virus-viny":{"az":{"t":"Günahkarlıq Virusu","p":"30 ₼"},"ru":{"t":"Вирус вины","p":"30 ₼"},"en":{"t":"The Guilt Virus","p":"30 ₼"}},"shizofreniya":{"az":{"t":"Şizofreniya. Cinnət pandemiyası","p":"30 ₼"},"ru":{"t":"Шизофрения. Пандемия безумия","p":"30 ₼"},"en":{"t":"Schizophrenia. A Pandemic of Madness","p":"30 ₼"}},"phoenix-era":{"az":{"t":"Feniks Erası","p":"30 ₼"},"ru":{"t":"Эра Феникса","p":"30 ₼"},"en":{"t":"Phoenix Era","p":"30 ₼"}},"freud-yuxularin-yozumu":{"az":{"t":"Yuxuların yozumu","p":"30 ₼"},"ru":{"t":"Толкование сновидений","p":"30 ₼"},"en":{"t":"The Interpretation of Dreams","p":"30 ₼"}},"freud-musa":{"az":{"t":"Musa və təkallahlılıq","p":"30 ₼"},"ru":{"t":"Человек Моисей и монотеистическая религия","p":"30 ₼"},"en":{"t":"Moses and Monotheism","p":"30 ₼"}},"freud-totem-ve-tabu":{"az":{"t":"Totem və Tabu","p":"30 ₼"},"ru":{"t":"Тотем и табу","p":"30 ₼"},"en":{"t":"Totem and Taboo","p":"30 ₼"}},"freud-psixoanalizle-tanishliq":{"az":{"t":"Psixoanalizlə ilkin tanışlıq","p":"30 ₼"},"ru":{"t":"Введение в психоанализ. Лекции","p":"30 ₼"},"en":{"t":"Introduction to Psychoanalysis","p":"30 ₼"}},"freud-seksualligin-psixologiyasi":{"az":{"t":"Seksuallığın psixologiyası","p":"30 ₼"},"ru":{"t":"Три очерка по теории сексуальности","p":"30 ₼"},"en":{"t":"Three Essays on the Theory of Sexuality","p":"30 ₼"}},"freud-sevgi-mektublari":{"az":{"t":"Sevgi məktubları (1882–1912)","p":"30 ₼"},"ru":{"t":"Письма Марте Бернайс (1882–1912)","p":"30 ₼"},"en":{"t":"Letters to Martha Bernays (1882–1912)","p":"30 ₼"}},"freud-aforizmlar":{"az":{"t":"Aforizmlər","p":"30 ₼"},"ru":{"t":"Афоризмы","p":"30 ₼"},"en":{"t":"Aphorisms","p":"30 ₼"}},"freud-medeniyyetin-sancilari":{"az":{"t":"Mədəniyyətin sancıları","p":"30 ₼"},"ru":{"t":"Недовольство культурой","p":"30 ₼"},"en":{"t":"Civilization and Its Discontents","p":"30 ₼"}},"freud-fliesse-mektublari":{"az":{"t":"Flissə məktublar (1887–1904)","p":"30 ₼"},"ru":{"t":"Письма Вильгельму Флиссу (1887–1904)","p":"30 ₼"},"en":{"t":"Letters to Wilhelm Fliess (1887–1904)","p":"30 ₼"}},"freud-zweig-mektublari":{"az":{"t":"Freyd–Tsveyq məktubları (1908–1939)","p":"30 ₼"},"ru":{"t":"Переписка Фрейда и Цвейга (1908–1939)","p":"30 ₼"},"en":{"t":"Freud–Zweig Letters (1908–1939)","p":"30 ₼"}},"freud-folklor":{"az":{"t":"Yuxu və folklor","p":"30 ₼"}},"freud-abriss":{"az":{"t":"Psixoanalizin qısa xülasəsi","p":"30 ₼"},"ru":{"t":"Краткое изложение психоанализа","p":"30 ₼"},"en":{"t":"An Outline of Psycho-Analysis","p":"30 ₼"}},"freud-bir-illuziyanin-geleceyi":{"az":{"t":"Bir illüziyanın gələcəyi","p":"30 ₼"},"ru":{"t":"Будущее одной иллюзии","p":"30 ₼"},"en":{"t":"The Future of an Illusion","p":"30 ₼"}},"freud-gundelik-heyat":{"az":{"t":"Gündəlik həyatın psixopatologiyası","p":"30 ₼"},"ru":{"t":"Психопатология обыденной жизни","p":"30 ₼"},"en":{"t":"The Psychopathology of Everyday Life","p":"30 ₼"}},"freud-gwx":{"az":{"t":"Seçilmiş əsərlər 1913–1917","p":"30 ₼"},"ru":{"t":"Избранные произведения","p":"30 ₼"},"en":{"t":"Selected Works","p":"30 ₼"}},"freud-histeriya":{"az":{"t":"Histeriya üzrə tədqiqatlar","p":"30 ₼"},"ru":{"t":"Исследования истерии","p":"30 ₼"},"en":{"t":"Studies on Hysteria","p":"30 ₼"}},"freud-jenseits":{"az":{"t":"Həzz prinsipinin o tayında","p":"30 ₼"},"ru":{"t":"По ту сторону принципа удовольствия","p":"30 ₼"},"en":{"t":"Beyond the Pleasure Principle","p":"30 ₼"}},"freud-manee-simptom-qorxu":{"az":{"t":"Maneə, simptom və qorxu","p":"30 ₼"},"ru":{"t":"Торможение, симптом и тревога","p":"30 ₼"},"en":{"t":"Inhibitions, Symptoms and Anxiety","p":"30 ₼"}},"freud-massen":{"az":{"t":"Kütlə psixologiyası və Mən-analizi","p":"30 ₼"},"ru":{"t":"Психология масс и анализ «Я»","p":"30 ₼"},"en":{"t":"Group Psychology and the Analysis of the Ego","p":"30 ₼"}},"freud-men-ve-o":{"az":{"t":"Mən və O","p":"30 ₼"},"ru":{"t":"«Я» и «Оно»","p":"30 ₼"},"en":{"t":"The Ego and the Id","p":"30 ₼"}},"freud-metapsixologiya":{"az":{"t":"Metapsixologiya","p":"30 ₼"},"ru":{"t":"Метапсихология","p":"30 ₼"},"en":{"t":"Metapsychology","p":"30 ₼"}},"freud-yeni-muhazireler":{"az":{"t":"Yeni mühazirələr","p":"30 ₼"},"ru":{"t":"Новые лекции по психоанализу","p":"30 ₼"},"en":{"t":"New Introductory Lectures on Psycho-Analysis","p":"30 ₼"}},"freud-yumor":{"az":{"t":"Yumor və onun qeyri-şüurla əlaqəsi","p":"30 ₼"},"ru":{"t":"Остроумие и его отношение к бессознательному","p":"30 ₼"},"en":{"t":"Jokes and Their Relation to the Unconscious","p":"30 ₼"}},"freud-krankengeschichten":{"az":{"t":"Xəstəlik tarixçələri","p":"30 ₼"},"ru":{"t":"Истории болезни","p":"30 ₼"},"en":{"t":"Case Histories","p":"30 ₼"}},"freud-psixoanaliz-texnikasi":{"az":{"t":"Psixoanaliz texnikasına dair","p":"30 ₼"},"ru":{"t":"К технике психоанализа","p":"30 ₼"},"en":{"t":"On the Technique of Psycho-Analysis","p":"30 ₼"}},"freud-kicik-eserler":{"az":{"t":"Seksuallıq və nevrozlar haqqında kiçik əsərlər","p":"30 ₼"},"ru":{"t":"Малые работы о сексуальности и неврозах","p":"30 ₼"},"en":{"t":"Papers on Sexuality and Neurosis","p":"30 ₼"}},"freud-ozunu-tesvir":{"az":{"t":"Özünü təsvir","p":"30 ₼"},"ru":{"t":"Автобиография","p":"30 ₼"},"en":{"t":"An Autobiographical Study","p":"30 ₼"}},"freud-muxtelif-eserler":{"az":{"t":"Müxtəlif əsərlər (1908–1928)","p":"30 ₼"},"ru":{"t":"Разные сочинения (1908–1928)","p":"30 ₼"},"en":{"t":"MISCELLANEOUS WORKS (1908–1928)","p":"30 ₼"}},"freud-elyazmalar":{"az":{"t":"Əlyazmalardan yazılar (1892–1938)","p":"30 ₼"},"ru":{"t":"Из рукописей (1892–1938)","p":"30 ₼"},"en":{"t":"Posthumous Writings (1892–1938)","p":"30 ₼"}},"freud-incesenet":{"az":{"t":"İncəsənət və ədəbiyyat","p":"30 ₼"},"ru":{"t":"Искусство и литература","p":"30 ₼"},"en":{"t":"ART AND LITERATURE","p":"30 ₼"}},"freud-tetbiqi-yazilar":{"az":{"t":"Psixoanalizin tətbiqi üzrə yazılar","p":"30 ₼"},"ru":{"t":"Прикладной психоанализ","p":"30 ₼"},"en":{"t":"Applied Psycho-Analysis","p":"30 ₼"}},"freud-ilk-nevroz-isleri":{"az":{"t":"Nevroz təliminə dair ilk işlər","p":"30 ₼"},"ru":{"t":"Ранние работы по теории неврозов","p":"30 ₼"},"en":{"t":"EARLY PAPERS ON THE THEORY OF THE NEUROSES","p":"30 ₼"}},"freud-gec-analitik-yazilar":{"az":{"t":"Gec analitik yazılar (1922–1937)","p":"30 ₼"},"ru":{"t":"Поздние аналитические работы (1922–1937)","p":"30 ₼"},"en":{"t":"Late Analytical Papers (1922–1937)","p":"30 ₼"}},"freud-yuxu-haqqinda":{"az":{"t":"Yuxu haqqında və kiçik yazılar (1901–1925)","p":"30 ₼"},"ru":{"t":"О сновидении и малые работы (1901–1925)","p":"30 ₼"},"en":{"t":"ON DREAMS AND SHORTER WORKS","p":"30 ₼"}},"freud-psixoanaliz-haqqinda":{"az":{"t":"Psixoanaliz haqqında (Klark mühazirələri)","p":"30 ₼"},"ru":{"t":"О психоанализе (Кларковские лекции)","p":"30 ₼"},"en":{"t":"On Psychoanalysis (Clark Lectures)","p":"30 ₼"}},"freud-kicik-fragmenler":{"az":{"t":"Kiçik fragmenler (1924–1942)","p":"30 ₼"},"ru":{"t":"Малые фрагменты (1924–1942)","p":"30 ₼"},"en":{"t":"Little Fragments (1924–1942)","p":"30 ₼"}},"freud-kicik-eserler-ii":{"az":{"t":"Kiçik əsərlər II (1898, 1925)","p":"30 ₼"},"ru":{"t":"Малые работы II (1898, 1925)","p":"30 ₼"},"en":{"t":"Shorter Works II (1898, 1925)","p":"30 ₼"}},"freud-on-sozler":{"az":{"t":"Ön sözlər (1886–1930)","p":"30 ₼"},"ru":{"t":"Предисловия (1886–1930)","p":"30 ₼"},"en":{"t":"Prefaces (1886–1930)","p":"30 ₼"}},"freud-referatlar":{"az":{"t":"Referatlar (1884–1885)","p":"30 ₼"},"ru":{"t":"Referatlar (1884–1885)","p":"30 ₼"},"en":{"t":"Referatlar (1884–1885)","p":"30 ₼"}},"freud-resenziyalar":{"az":{"t":"Resenziyalar (1887–1910)","p":"30 ₼"},"ru":{"t":"Resenziyalar (1887–1910)","p":"30 ₼"},"en":{"t":"Resenziyalar (1887–1910)","p":"30 ₼"}},"freud-kokain":{"az":{"t":"Kokain haqqında yazılar","p":"30 ₼"}},"freud-afaziya":{"az":{"t":"Afaziyaya dair anlayışa doğru","p":"30 ₼"}},"freud-usaq-iflici":{"az":{"t":"Uşaq serebral iflici","p":""}}};

  var L = (document.documentElement.getAttribute('lang') || 'az').slice(0, 2).toLowerCase();
  if (!MAP || !Object.keys(MAP).length) return;
  if (L !== 'ru' && L !== 'en') L = 'az';

  var TXT = {
    az: { add: 'Səbətə at', short: 'Səbət', added: 'Səbətə əlavə edildi',
          go: 'Səbətə keç', more: 'Davam et' },
    ru: { add: 'В корзину', short: 'Корзина', added: 'Добавлено в корзину',
          go: 'Перейти в корзину', more: 'Продолжить' },
    en: { add: 'Add to cart', short: 'Cart', added: 'Added to cart',
          go: 'Go to cart', more: 'Continue' }
  }[L];

  function slug() {
    var m = location.pathname.match(/^\/books\/([^\/]+)/);
    return m ? m[1] : '';
  }

  function book() {
    var s = slug();
    var byLang = MAP[s] || {};
    return byLang[L] || byLang.az || byLang.ru || byLang.en || null;
  }

  function read() {
    try { return JSON.parse(localStorage.getItem(CART_KEY) || '[]') || []; } catch (e) { return []; }
  }
  function write(list) {
    try { localStorage.setItem(CART_KEY, JSON.stringify(list)); } catch (e) {}
  }

  function addToCart() {
    var b = book();
    if (!b) return null;
    var items = read(), hit = false;
    for (var i = 0; i < items.length; i++) {
      if (items[i].title === b.t) {
        items[i].qty = (items[i].qty || 1) + 1;
        if (b.p && !items[i].price) items[i].price = b.p;
        hit = true;
        break;
      }
    }
    if (!hit) items.push({ title: b.t, qty: 1, price: b.p || '' });
    write(items);
    return b;
  }

  function count() {
    return read().reduce(function (s, i) { return s + (i.qty || 1); }, 0);
  }

  function toast(b) {
    var old = document.getElementById('cfg-toast');
    if (old && old.parentNode) old.parentNode.removeChild(old);
    var d = document.createElement('div');
    d.id = 'cfg-toast';
    d.setAttribute('role', 'status');
    d.style.cssText =
      'position:fixed;left:50%;top:24px;transform:translateX(-50%);z-index:99999;' +
      'background:#0f131b;color:#f2ede3;border:1px solid #c9a961;border-radius:10px;' +
      'padding:14px 18px;max-width:440px;width:calc(100% - 32px);' +
      'box-shadow:0 12px 40px rgba(0,0,0,.55);font-size:14px;line-height:1.55;' +
      'box-sizing:border-box;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;';
    d.innerHTML =
      '<div style="display:flex;gap:10px;align-items:flex-start;">' +
      '<span style="color:#c9a961;font-size:18px;line-height:1;">\u2713</span>' +
      '<div style="flex:1;">' +
      '<b style="display:block;margin-bottom:4px;">' + TXT.added + '</b>' +
      '<span style="color:#a8a296;">' + String(b.t).replace(/[<>&]/g, '') +
      (b.p ? ' \u00b7 ' + b.p : '') + '</span>' +
      '<div style="margin-top:12px;display:flex;gap:10px;flex-wrap:wrap;">' +
      '<a href="' + CATALOG_URL + '" style="background:#c9a961;color:#07090e;text-decoration:none;' +
      'padding:9px 16px;border-radius:7px;font-weight:700;font-size:13px;">' + TXT.go +
      ' (' + count() + ')</a>' +
      '<button type="button" data-cfg-close style="background:transparent;color:#a8a296;' +
      'border:1px solid rgba(255,255,255,.15);padding:9px 16px;border-radius:7px;' +
      'cursor:pointer;font-size:13px;">' + TXT.more + '</button>' +
      '</div></div></div>';
    document.body.appendChild(d);
    d.querySelector('[data-cfg-close]').onclick = function () { d.parentNode.removeChild(d); };
    setTimeout(function () { if (d.parentNode) d.parentNode.removeChild(d); }, 12000);
  }

  function relabel(btn) {
    var full = btn.querySelector('.kitab-full');
    var short = btn.querySelector('.kitab-short');
    if (full) { full.textContent = TXT.add; }
    if (short) { short.textContent = TXT.short; }
    if (!full && !short) { btn.textContent = TXT.add; }
  }

  function bind() {
    var btns = document.querySelectorAll('button[onclick*="openKitabModal"]');
    for (var i = 0; i < btns.length; i++) {
      (function (btn) {
        if (btn.getAttribute('data-cfg') === '1') return;
        btn.setAttribute('data-cfg', '1');
        btn.removeAttribute('onclick');
        btn.setAttribute('type', 'button');
        relabel(btn);
        btn.addEventListener('click', function (e) {
          e.preventDefault();
          var b = addToCart();
          if (b) toast(b);
        });
      })(btns[i]);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bind);
  } else { bind(); }
})();
