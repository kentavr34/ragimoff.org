// ═══════════════════════════════════════════════
//  RAGIMOFF.ORG — Shared JS
// ═══════════════════════════════════════════════

// Auto language redirect — priority: 1) saved choice  2) browser language  3) IP
// AZ = default(/), RU = /ru/, EN = /en/
(function() {
  try {
    var path    = window.location.pathname;
    var isRu    = /\/ru\//.test(path);
    var isEn    = /\/en\//.test(path);
    var fn      = path.split('/').pop() || 'index.html';
    var saved   = localStorage.getItem('ragimoff_lang');

    // 1. Saved preference — always wins
    if (saved === 'ru' && !isRu) { window.location.replace('/ru/' + fn); return; }
    if (saved === 'en' && !isEn) { window.location.replace('/en/' + fn); return; }
    if (saved === 'az' && (isRu || isEn)) { window.location.replace('/' + fn); return; }
    if (saved) return;

    // 2. Browser / device language — instant, no network
    var navLang = ((navigator.languages && navigator.languages[0]) || navigator.language || '').toLowerCase();
    var lang2   = navLang.split('-')[0]; // 'ru-RU' → 'ru'

    if (lang2 === 'ru' && !isRu) {
      localStorage.setItem('ragimoff_lang', 'ru');
      window.location.replace('/ru/' + fn); return;
    }
    if (lang2 === 'en' && !isEn) {
      localStorage.setItem('ragimoff_lang', 'en');
      window.location.replace('/en/' + fn); return;
    }
    // 'az' or 'tr' (common in AZ) — stay on AZ version, let IP confirm
    if (lang2 === 'az' || lang2 === 'tr') {
      // skip IP, just save and stay
      localStorage.setItem('ragimoff_lang', isRu ? 'ru' : isEn ? 'en' : 'az');
      return;
    }

    // 3. IP geolocation — for any other browser language (or empty)
    fetch('https://ipapi.co/json/').then(function(r){ return r.json(); }).then(function(d){
      var cc = (d && d.country_code) ? d.country_code.toUpperCase() : '';
      if (cc === 'RU' && !isRu) {
        localStorage.setItem('ragimoff_lang', 'ru');
        window.location.replace('/ru/' + fn);
      } else if (cc !== 'AZ' && cc !== '' && !isEn) {
        // visitor from any country except AZ → EN
        localStorage.setItem('ragimoff_lang', 'en');
        window.location.replace('/en/' + fn);
      } else {
        localStorage.setItem('ragimoff_lang', isRu ? 'ru' : isEn ? 'en' : 'az');
      }
    }).catch(function(){
      localStorage.setItem('ragimoff_lang', isRu ? 'ru' : isEn ? 'en' : 'az');
    });
  } catch(e){}
})();

// Fallback click handler for any remaining .lang-switch / .mobile-lang links
document.addEventListener('click', function(e){
  var t = e.target.closest && e.target.closest('.lang-switch, .mobile-lang, .lang-drop-item, .mobile-lang-btn');
  if (!t) return;
  var href = t.getAttribute('href') || '';
  var goesRu = /\/ru\//.test(href) || /^ru\//.test(href);
  var goesEn = /\/en\//.test(href) || /^en\//.test(href);
  localStorage.setItem('ragimoff_lang', goesRu ? 'ru' : goesEn ? 'en' : 'az');
});

// ── SEO: Open Graph · JSON-LD · hreflang · canonical ──────────────────────
(function() {
  var head  = document.head;
  var title = document.title || '';
  var desc  = (document.querySelector('meta[name="description"]') || {}).content || '';
  var path  = window.location.pathname;
  var isRu  = /\/ru\//.test(path);
  var fname = path.split('/').pop() || 'index.html';
  var base  = 'https://ragimoff.org';
  var selfUrl = base + path;

  function meta(prop, val, attr) {
    if (!val) return;
    var a = attr || 'property';
    // Гард от дублей (волна 1.1 аудита 2026-09-02). Раньше сюда не смотрели:
    // статический head уже несёт og:title / og:description / og:type / og:url,
    // а build-партиал добавляет их второй раз. Третья копия из скрипта была бы
    // уже не косметикой: парсеры выбирают один тег из повторов, и угадать
    // какой — нельзя. Если тег уже объявлен, авторская строка важнее.
    if (head.querySelector('meta[' + a + '="' + prop + '"]')) return;
    var m = document.createElement('meta');
    m.setAttribute(a, prop);
    m.content = val;
    head.appendChild(m);
  }
  function link(rel, href, extra) {
    // Тот же принцип: не плодить второй canonical и вторую пачку hreflang.
    // На бою значения совпали бы и шум был бы невидим, но на любом зеркале или
    // staging скрипт добавлял бы canonical с ЧУЖИМ доменом рядом с настоящим.
    var sel = 'link[rel="' + rel + '"][href="' + href + '"]';
    if (head.querySelector(sel)) return;
    var l = document.createElement('link');
    l.rel = rel;
    l.href = href;
    if (extra) Object.keys(extra).forEach(function(k){ l.setAttribute(k, extra[k]); });
    head.appendChild(l);
  }

  // Canonical
  link('canonical', selfUrl.split('?')[0].split('#')[0]);

  // hreflang
  var isEn  = /\/en\//.test(path);
  var azUrl = base + '/' + fname;
  var ruUrl = base + '/ru/' + fname;
  var enUrl = base + '/en/' + fname;
  link('alternate', azUrl,  { hreflang: 'az' });
  link('alternate', ruUrl,  { hreflang: 'ru' });
  link('alternate', enUrl,  { hreflang: 'en' });
  link('alternate', azUrl,  { hreflang: 'x-default' });

  // ── Иконки и манифест (волна 1.1 аудита 2026-09-02) ──────────────────────
  // До этого ни одна своя страница не объявляла иконку: браузер молча просил
  // /favicon.ico и получал 404, iOS не находил apple-touch-icon, а PWA-установка
  // была невозможна без манифеста. Ссылки прописываются здесь, а не в 171 файле:
  // общего head-партиала в проекте нет (build.py рендерит только
  // header/mobile-nav/footer/hero-search/kitab-modal), а index.html — эталон.
  // Тот же приём уже чинит и книгу: её страницы (161 файл) shared.js не грузят,
  // но /favicon.ico и /apple-touch-icon.png браузеры просят от корня домена.
  function brandLink(rel, href, extra) {
    if (document.querySelector('link[rel="' + rel + '"]')) return;  // не дублируем авторскую
    link(rel, href, extra);
  }
  brandLink('icon',             base + '/favicon.ico');
  brandLink('icon',             base + '/favicons/favicon-32x32.png', { type: 'image/png', sizes: '32x32' });
  brandLink('icon',             base + '/favicons/favicon-16x16.png', { type: 'image/png', sizes: '16x16' });
  brandLink('apple-touch-icon', base + '/apple-touch-icon.png');
  brandLink('manifest',         base + '/site.webmanifest');
  if (!document.querySelector('meta[name="theme-color"]')) {
    meta('theme-color', '#061826', 'name');   // цвет шапки: rgba(6,24,38,.98), gtc.css
  }

  // Open Graph
  var isBlog   = /blog/.test(path);
  var ogType   = isBlog ? 'article' : 'website';
  var ogLocale = isRu ? 'ru_RU' : isEn ? 'en_US' : 'az_AZ';
  meta('og:type',        ogType);
  meta('og:locale',      ogLocale);
  meta('og:title',       title);
  meta('og:description', desc);
  meta('og:url',         selfUrl);
  meta('og:site_name',   'RAGIMOFF');
  meta('og:image',       base + '/images/og-cover.jpg');

  // Twitter Card
  meta('twitter:card',        'summary_large_image', 'name');
  meta('twitter:title',       title,                 'name');
  meta('twitter:description', desc,                  'name');
  meta('twitter:image',       base + '/images/og-cover.jpg', 'name');

  // JSON-LD
  var lang3 = isRu ? 'ru' : isEn ? 'en' : 'az';
  var author = {
    '@type':    'Person',
    'name':     isRu ? 'Кенан Рагимов' : isEn ? 'Kenan Ragimov' : 'Kənan Rəhimov',
    'url':      base + (isRu ? '/ru/haqqimda.html' : isEn ? '/en/haqqimda.html' : '/haqqimda.html'),
    'jobTitle': isRu ? 'Врач-психиатр, психотерапевт' : isEn ? 'Psychiatrist, Psychotherapist' : 'Həkim-Psixiatr, Psixoterapevt'
  };
  var org = {
    '@type': 'Organization',
    'name':  'RAGIMOFF',
    'url':   base,
    'logo':  base + '/images/logo.png'
  };
  var schema;
  if (isBlog) {
    schema = {
      '@context':    'https://schema.org',
      '@type':       'BlogPosting',
      'headline':    title,
      'description': desc,
      'url':         selfUrl,
      'inLanguage':  lang3,
      'author':      author,
      'publisher':   org,
      'datePublished': '2026-01-01',
      'dateModified':  '2026-04-29'
    };
  } else {
    schema = {
      '@context':    'https://schema.org',
      '@type':       'MedicalWebPage',
      'name':        title,
      'description': desc,
      'url':         selfUrl,
      'inLanguage':  lang3,
      'author':      author,
      'provider':    org
    };
  }
  var s = document.createElement('script');
  s.type = 'application/ld+json';
  s.text = JSON.stringify(schema);
  head.appendChild(s);
})();

// Google Analytics 4 (G-SF6PE3YDN1)
(function() {
  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=G-SF6PE3YDN1';
  document.head.appendChild(s);
  window.dataLayer = window.dataLayer || [];
  window.gtag = function(){ dataLayer.push(arguments); };
  gtag('js', new Date());
  gtag('config', 'G-SF6PE3YDN1');
})();

// Mobile menu
function toggleMenu() {
  const nav = document.getElementById('mobileNav');
  nav.classList.toggle('open');
}
window.toggleMenu = toggleMenu;
function closeMenu() {
  document.getElementById('mobileNav')?.classList.remove('open');
}
// Mobile nav — submenu expand/collapse
function toggleSubMenu(btn) {
  const group = btn.closest('.mobile-nav-group');
  if (group) group.classList.toggle('is-open');
}
window.toggleSubMenu = toggleSubMenu;

// Scroll animations
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('vis'); });
}, { threshold: 0.1 });
document.querySelectorAll('.fi').forEach(el => observer.observe(el));

// Header shadow on scroll
window.addEventListener('scroll', () => {
  const h = document.querySelector('header');
  if (h) h.style.boxShadow = window.scrollY > 40 ? '0 4px 28px rgba(0,0,0,0.28)' : 'none';
});

// WhatsApp message builder
function waLink(msg) {
  return 'https://wa.me/994702200376?text=' + encodeURIComponent(msg || 'Salam, məlumat almaq istəyirəm.');
}

// Backend (Apps Script) — приём форм + Telegram + Google Sheets
const RAGIMOFF_API = 'https://script.google.com/macros/s/AKfycbw-ejwk4wslNpEhMB11Yknj5cjPBZJkoc4nf8BTMP8lxROc8ZxtAWkkXtgv5E8GLzxyfw/exec';

// Раньше здесь стоял mode:'no-cors'. Ответ сервера в этом режиме непрозрачен,
// поэтому функция всегда возвращала {ok:true} — форма рапортовала «отправлено»
// и когда заявка терялась. Проверено 2026-08-17: обычный запрос к тому же
// адресу отдаёт 200 и {"ok":true}, Apps Script чтение ответа разрешает.
// Повтор при ошибке НЕ делаем: первый запрос мог уйти на сервер даже с
// исключением, и повтор создал бы вторую заявку на одного человека.
async function submitToAPI(payload) {
  try {
    const res = await fetch(RAGIMOFF_API, {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) return { ok: false, error: 'HTTP ' + res.status };
    try {
      const data = await res.json();
      if (data && data.ok === false) return { ok: false, error: data.error || 'server' };
    } catch (e) {
      /* тело неJSON — но статус 200, значит запрос принят */
    }
    return { ok: true };
  } catch (err) {
    console.error('submitToAPI error:', err);
    return { ok: false, error: String(err) };
  }
}

// ── Wave 1.4: New API endpoints on api.ragimoff.org ──────────────────────
// Book orders → /api/book-order
// Training registrations → /api/training-reg
// Both with Supabase + Telegram, Apps Script as fallback

const RAGIMOFF_API_BASE = 'https://api.ragimoff.org';

async function submitToEndpoint(endpoint, payload) {
  try {
    const res = await fetch(`${RAGIMOFF_API_BASE}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      const data = await res.json().catch(function () { return null; });
      /* data отдаём НАРУЖУ: сервер считает сумму тренинга и возвращает её вместе
         с признаком рассрочки. Без этого сайт не мог показать кнопку оплаты —
         человек регистрировался и оставался со словом «спасибо», хотя заявка
         на тренинги предполагает оплату. */
      if (!data || data.ok !== false) return { ok: true, data: data || null };
    }
  } catch (err) {
    console.warn(`API ${endpoint} unavailable, falling back:`, err);
  }
  return submitToAPI(payload); // Apps Script fallback
}

async function submitBookOrder(payload) {
  return submitToEndpoint('/api/book-order', payload);
}

/* ── ПРОВЕРКА ЗАПОЛНЕНИЯ ФОРМЫ РЕГИСТРАЦИИ ────────────────────────────────
   Кенан 14.10.2026: «при неполном заполнении обязательных ячеек он не показывает
   красными предупреждениями пустые ячейки».
   Причина была двойная: у формы стоит novalidate (браузерная проверка выключена),
   а своей проверки не было вовсе. Человек нажимал кнопку — и ничего не происходило.

   ОБЯЗАТЕЛЬНЫЕ ПОЛЯ (указание Кенана):
      • имя и фамилия;
      • мобильный номер;
      • удостоверение личности (файл).
   ОСТАЛЬНЫЕ — необязательные: почта, адрес, программа, форма оплаты, заметки,
   сертификаты.
   ОСОБЫЙ СЛУЧАЙ: при выборе переподготовки по Общей или Клинической психологии
   обязательным становится ещё и ДИПЛОМ о высшем образовании.

   Проверка показывает КАЖДОЕ пустое поле красным и подписывает, чего не хватает. */
var REG_RETRAIN = ['Ümumi Psixologiya', 'Klinik Psixologiya'];

function regFieldError(input, on) {
  if (!input) return;
  var box = input.closest ? input.closest('.field, .form-field, .form-group') : null;
  if (on) {
    input.classList.add('field-invalid');
    input.style.borderColor = '#e06b6b';
    input.style.boxShadow = '0 0 0 2px rgba(224,107,107,.18)';
    if (box) {
      var msg = box.querySelector('.field-invalid-msg');
      if (!msg) {
        msg = document.createElement('span');
        msg.className = 'field-invalid-msg';
        msg.style.cssText = 'display:block;margin-top:6px;color:#e88;font-size:.8125rem;';
        box.appendChild(msg);
      }
      msg.textContent = input.getAttribute('data-need') || '';
    }
  } else {
    input.classList.remove('field-invalid');
    input.style.borderColor = '';
    input.style.boxShadow = '';
    if (box) {
      var m2 = box.querySelector('.field-invalid-msg');
      if (m2) m2.textContent = '';
    }
  }
}

/* Возвращает true, если форма заполнена верно. Иначе — красит пустые поля. */
function validateRegForm(form) {
  var L = (document.documentElement.getAttribute('lang') || 'az').slice(0, 2);
  var NEED = {
    az: { name: 'Ad və soyadı yazın', phone: 'Mobil nömrəni yazın',
          id: 'Şəxsiyyət vəsiqəsini əlavə edin', dip: 'Ali təhsil diplomunu əlavə edin',
          prog: 'Proqramı seçin' },
    ru: { name: 'Укажите имя и фамилию', phone: 'Укажите мобильный номер',
          id: 'Приложите удостоверение личности', dip: 'Приложите диплом о высшем образовании',
          prog: 'Выберите программу' },
    en: { name: 'Enter your first and last name', phone: 'Enter your mobile number',
          id: 'Attach your ID document', dip: 'Attach your university diploma',
          prog: 'Choose a programme' },
    tr: { name: 'Ad və soyadı yazın', phone: 'Mobil nömrəni yazın',
          id: 'Şəxsiyyət vəsiqəsini əlavə edin', dip: 'Ali təhsil diplomunu əlavə edin',
          prog: 'Proqramı seçin' }
  }[L] || null;
  if (!NEED) NEED = { name: 'Name', phone: 'Phone', id: 'ID', dip: 'Diploma', prog: 'Programme' };

  var ok = true;
  function need(el, text) {
    if (!el) return;
    var empty = !String(el.value || '').trim();
    if (empty) { ok = false; el.setAttribute('data-need', text); regFieldError(el, true); }
    else { regFieldError(el, false); }
  }

  need(form.querySelector('[name="ad"], [name="fname"]'), NEED.name);
  need(form.querySelector('[name="soyad"], [name="lname"]'), NEED.name);
  need(form.querySelector('[name="telefon"], [name="phone"]'), NEED.phone);

  /* Программа: если выбрана переподготовка — диплом обязателен. */
  var prog = form.querySelector('[name="proqram"]:checked, [name="service"]:checked');
  var progVal = prog ? prog.value : '';
  var needDip = REG_RETRAIN.indexOf(progVal) >= 0;

  /* Удостоверение личности — обязательный ФАЙЛ. Файлы лежат в пуле
     (window.regFilePool), потому что input очищается после выбора. */
  var pool = window.regFilePool || {};
  var idCount = (pool['shexsiyyet'] || []).length;
  var dipCount = (pool['diplom'] || []).length;
  /* Если файлы отправляются обычным input (без пула) — считаем по input.files */
  var idInput = form.querySelector('[name="shexsiyyet"]');
  var dipInput = form.querySelector('[name="diplom"]');
  if (!idCount && idInput && idInput.files) idCount = idInput.files.length;
  if (!dipCount && dipInput && dipInput.files) dipCount = dipInput.files.length;

  if (!idCount) { ok = false; if (idInput) { idInput.setAttribute('data-need', NEED.id); regFieldError(idInput, true); } }
  else if (idInput) regFieldError(idInput, false);

  if (needDip && !dipCount) { ok = false; if (dipInput) { dipInput.setAttribute('data-need', NEED.dip); regFieldError(dipInput, true); } }
  else if (dipInput) regFieldError(dipInput, false);
  /* Диплом НЕ обязателен, если программа не переподготовка — снимаем красноту. */

  if (prog) regFieldError(prog, false);

  if (!ok) {
    var first = form.querySelector('.field-invalid');
    if (first) {
      first.scrollIntoView({ behavior: 'smooth', block: 'center' });
      try { first.focus({ preventScroll: true }); } catch (e) {}
    }
  }
  return ok;
}

/* Снимаем красноту, как только человек начал заполнять поле. */
document.addEventListener('input', function (e) {
  if (e.target && e.target.classList && e.target.classList.contains('field-invalid')) {
    if (String(e.target.value || '').trim()) regFieldError(e.target, false);
  }
}, true);
document.addEventListener('change', function (e) {
  if (e.target && e.target.type === 'file') regFieldError(e.target, false);
}, true);

async function submitTrainingReg(payload) {
  return submitToEndpoint('/api/training-reg', payload);
}

/* submitRegistration() — САМАЯ ЧАСТАЯ ПОЛОМКА ФОРМ НА САЙТЕ.
   Эту функцию ВЫЗЫВАЛИ в трёх местах: tehsil.html (az/ru/en) и handleB2BForm().
   А ОПРЕДЕЛЕНА ОНА НЕ БЫЛА НИГДЕ. Что происходило при отправке:
      ReferenceError: submitRegistration is not defined
   → ошибка внутри async-обработчика, поймать её некому;
   → кнопка навсегда остаётся в положении «Göndərilir…» и заблокирована;
   → человек видит, что «форма не работает», и не понимает почему.
   Именно на это жаловался Кенан 14.10.2026: «заполнил, но не могу отправить».

   Теперь функция есть: она шлёт заявку на наш сервер, при неудаче — в Apps Script,
   и умеет прикладывать файлы (документы абитуриента уходят в архив на сервере). */
async function submitRegistration(payload) {
  try {
    const res = await fetch(`${RAGIMOFF_API_BASE}/api/training-reg`, {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      const data = await res.json().catch(function () { return null; });
      if (!data || data.ok !== false) return { ok: true, data: data || null };
    }
  } catch (err) {
    console.warn('training-reg unavailable, falling back:', err);
  }
  return submitToAPI(payload);   // Apps Script: заявка не должна потеряться
}

// Сообщение о неудаче: заявка не ушла, человека нельзя оставлять с ощущением,
// что всё в порядке. Даём прямой путь — WhatsApp.
function showSendError(form) {
  let box = form.querySelector('.form-error');
  if (!box) {
    box = document.createElement('p');
    box.className = 'form-error';
    box.style.cssText = 'margin:14px 0 0;padding:12px 14px;border:1px solid rgba(220,90,90,.5);' +
      'background:rgba(220,90,90,.08);color:#E8A0A0;font-size:.875rem;line-height:1.6;';
    form.appendChild(box);
  }
  // Текст на языке страницы: форма живёт в четырёх деревьях, и сообщение об
  // ошибке на чужом языке читается как сбой сайта, а не как подсказка.
  var L = (document.documentElement.getAttribute('lang') || 'az').slice(0, 2);
  var MSG = {
    az: ['Göndərmək alınmadı. Zəhmət olmasa bir daha cəhd edin və\u00a0ya ', 'WhatsApp ilə yazın'],
    ru: ['Не удалось отправить. Попробуйте ещё раз или ', 'напишите в WhatsApp'],
    en: ['Could not send. Please try again or ', 'write to us on WhatsApp'],
    tr: ['Gönderilemedi. Lütfen tekrar deneyin ya\u00a0da ', 'WhatsApp üzerinden yazın']
  };
  var m = MSG[L] || MSG.az;
  box.innerHTML = m[0] +
    '<a href="https://wa.me/994702200376" target="_blank" rel="noopener" ' +
    'style="color:var(--accent);font-weight:700;">' + m[1] + '</a>.';
  box.style.display = 'block';
}

// Универсальный обработчик регистрационной формы
function wireRegForm(formId, successId, source) {
  const form = document.getElementById(formId);
  if (!form) return;
  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    const btn = form.querySelector('button[type="submit"]');
    const success = document.getElementById(successId);
    const fd = new FormData(form);
    const payload = {
      type: 'registration',
      fname: fd.get('ad') || fd.get('fname') || fd.get('name') || '',
      lname: fd.get('soyad') || fd.get('lname') || '',
      phone: fd.get('telefon') || fd.get('phone') || '',
      email: fd.get('email') || '',
      service: fd.get('proqram') || fd.get('service') || fd.get('xidmet') || '',
      note: [
        fd.get('odenis') ? 'Ödəniş: ' + fd.get('odenis') : '',
        fd.get('qeyd') || fd.get('note') || fd.get('mesaj') || ''
      ].filter(Boolean).join(' | '),
      source: source || location.pathname.replace(/^\//, '') || 'unknown'
    };
    const btnText = btn ? btn.textContent : '';
    if (btn) { btn.textContent = 'Göndərilir...'; btn.disabled = true; }
    const result = await submitTrainingReg(payload);
    if (!result.ok) {
      /* Форму НЕ блокируем: человек должен иметь возможность повторить. */
      if (btn) { btn.textContent = btnText; btn.disabled = false; }
      showSendError(form);
      return;
    }
    const err = form.querySelector('.form-error');
    if (err) err.style.display = 'none';
    form.style.opacity = '0.5';
    form.style.pointerEvents = 'none';
    if (success) {
      success.style.display = 'block';
      // ── Оплата после регистрации (Кенан 13.10, голосом) ──────────────────
      // «Регистрация на тренинге — сделать так, чтобы люди после регистрации
      //  переходили к оплате через ePoint… должна быть форма выбора рассрочки.»
      // Регистрация — это ещё не конец: тренинг платный, и человек должен
      // иметь возможность сразу оплатить, а не ждать звонка.
      showTrainingPay(success, payload, result.data);
      success.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  });
}

// Кнопка оплаты тренинга: полная сумма через ePoint либо заявка на рассрочку,
// которую оформляет БАНК (Кенан: «они через какой-то банк оформляют рассрочку,
// а не через нашу систему»).
function showTrainingPay(box, payload, data) {
  if (!data || !data.amount) return;              // \u0441\u0443\u043c\u043c\u0430 \u043d\u0435 \u043f\u0440\u0438\u0448\u043b\u0430 \u2014 \u043d\u0435 \u043e\u0431\u0435\u0449\u0430\u0435\u043c \u043e\u043f\u043b\u0430\u0442\u0443
  if (box.querySelector('.training-pay')) return;
  var L = (document.documentElement.getAttribute('lang') || 'az').slice(0, 2);
  var T = {
    az: { pay: 'İndi ödə', inst: 'Taksitlə ödə', payHint: 'Kartla tam ödəniş',
          instHint: 'Taksiti BANK rəsmiləşdirir', sent: 'Göndərilir…',
          ok: 'Taksit müraciətiniz qəbul edildi. Bank sizinlə əlaqə saxlayacaq.',
          err: 'Ödənişi başlada bilmədik. Yenidən cəhd edin.' },
    ru: { pay: 'Оплатить', inst: 'Оплатить в рассрочку', payHint: 'Полная оплата картой',
          instHint: 'Рассрочку оформляет БАНК', sent: 'Отправляем…',
          ok: 'Заявка на рассрочку принята. Банк свяжется с вами.',
          err: 'Не удалось начать оплату. Попробуйте ещё раз.' },
    en: { pay: 'Pay now', inst: 'Pay in instalments', payHint: 'Full card payment',
          instHint: 'The instalment is arranged by the BANK', sent: 'Sending…',
          ok: 'Your instalment request was accepted. The bank will contact you.',
          err: 'Could not start the payment. Please try again.' },
    tr: { pay: 'Şimdi öde', inst: 'Taksitle öde', payHint: 'Kartla tam ödeme',
          instHint: 'Taksiti BANKA düzenler', sent: 'Gönderiliyor…',
          ok: 'Taksit talebiniz alındı. Banka sizinle iletişime geçecek.',
          err: 'Ödeme başlatılamadı. Lütfen tekrar deneyin.' }
  }[L] || null;
  if (!T) T = { pay: 'Ödə', inst: 'Taksit', payHint: '', instHint: '', sent: '…',
                ok: 'OK', err: 'Error' };

  var wrap = document.createElement('div');
  wrap.className = 'training-pay';
  wrap.style.cssText = 'margin-top:18px;padding-top:18px;border-top:1px solid rgba(255,255,255,.12);';
  var sum = document.createElement('p');
  sum.style.cssText = 'margin:0 0 14px;font-size:15px;';
  sum.innerHTML = '<b>' + data.amount + ' ₼</b>' +
    (data.months ? ' / ' + data.months + ' ay' : '');
  wrap.appendChild(sum);

  function mkBtn(label, hint, months) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'btn btn-fill';
    b.style.cssText = 'display:block;width:100%;margin:0 0 8px;padding:14px 20px;';
    b.innerHTML = label + (hint ? '<span style="display:block;font-size:12px;opacity:.75;font-weight:400;">' + hint + '</span>' : '');
    b.onclick = async function () {
      b.disabled = true;
      var old = b.innerHTML;
      b.textContent = T.sent;
      try {
        var r = await fetch(RAGIMOFF_API_BASE + '/api/billing/epoint/training', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: ((payload.fname || '') + ' ' + (payload.lname || '')).trim(),
            phone: payload.phone || '', program: payload.service || '',
            amount: data.amount, months: months || 0
          })
        });
        var j = await r.json();
        if (j && j.redirect_url) { location.href = j.redirect_url; return; }
        if (j && j.installment) { sum.innerHTML = '<b>' + T.ok + '</b>'; b.remove(); return; }
      } catch (e) { /* ниже покажем честную ошибку */ }
      b.disabled = false;
      b.innerHTML = old;
      sum.insertAdjacentHTML('beforeend',
        '<span style="display:block;margin-top:8px;color:#E8A0A0;font-size:13px;">' + T.err + '</span>');
    };
    return b;
  }

  wrap.appendChild(mkBtn(T.pay, T.payHint, 0));
  wrap.appendChild(mkBtn(T.inst, T.instHint, 12));
  box.appendChild(wrap);
}

// B2B-заявка со страницы b2b.html (AZ/RU/EN). До аудита 2026-09-02 обработчик
// сидел в inline-<script> каждой из трёх страниц и делал только preventDefault()
// с немедленной надписью «Отправлено»: запрос не уходил никуда, весь B2B-поток
// терялся молча. Канон тот же, что у рабочих регистрационных форм:
// submitRegistration() — сначала свой сервер (api.ragimoff.org), при неудаче
// Apps Script; если не сработали оба — showSendError(), а не ложный успех.
// Форму при ошибке НЕ блокируем, чтобы человек мог повторить.
// Текст кнопки берётся из data-done / data-sending самой страницы: форма живёт
// в трёх языках, а shared.js — один на всех.
async function handleB2BForm(e) {
  e.preventDefault();
  const form = e.target;
  /* Проверка заполнения — та же, что у формы переподготовки: пустые обязательные
     поля краснеют и подписываются. Кенан 14.10.2026. */
  if (typeof validateRegForm === 'function' && !validateRegForm(form)) return;
  const val = function (id) {
    const el = document.getElementById(id);
    return el ? el.value.trim() : '';
  };
  // Подписи полей в note берутся с самой страницы — они уже на нужном языке,
  // и в реестре заявок не приходится догадываться, что за строка пришла.
  const pair = function (id) {
    const el = document.getElementById(id);
    if (!el || !el.value.trim()) return '';
    const lab = form.querySelector('label[for="' + id + '"]');
    const name = lab ? lab.textContent.replace(/[*?]/g, '').trim() : id;
    return name + ': ' + el.value.trim();
  };
  const sel = document.getElementById('b2b-f5');
  const direction = (sel && sel.selectedIndex > 0) ? sel.options[sel.selectedIndex].text : '';
  const payload = {
    type: 'registration',
    fname: val('b2b-f1'),        // название компании
    lname: val('b2b-f2'),        // контактное лицо
    phone: val('b2b-f3'),
    email: val('b2b-f4'),
    service: direction,          // выбранное направление программы
    note: ['B2B', pair('b2b-f6'), pair('b2b-f7')].filter(Boolean).join(' | '),
    source: location.pathname.replace(/^\//, '') || 'b2b.html'
  };
  const btn = form.querySelector('button[type="submit"]');
  const btnText = btn ? btn.textContent : '';
  if (btn) {
    btn.textContent = form.getAttribute('data-sending') || 'Göndərilir...';
    btn.disabled = true;
  }
  const result = await submitRegistration(payload);
  if (!result.ok) {
    if (btn) { btn.textContent = btnText; btn.disabled = false; }
    showSendError(form);
    return;
  }
  const err = form.querySelector('.form-error');
  if (err) err.style.display = 'none';
  if (btn) {
    btn.textContent = form.getAttribute('data-done') || 'Göndərildi.';
    btn.style.background = 'var(--navy)';
    btn.style.color = 'var(--white)';
  }
  form.style.opacity = '0.5';
  form.style.pointerEvents = 'none';
}

// Generic booking form submit  mailto + modal
function submitBooking(emailTo) {
  const fields = ['fname','lname','phone','email','service','note'];
  const vals = {};
  let ok = true;
  fields.forEach(f => {
    const el = document.getElementById(f);
    if (el) vals[f] = el.value.trim();
  });
  if (!vals.fname || !vals.phone) {
    alert('Zəhmət olmasa Ad və Telefon sahələrini doldurun.');
    return;
  }
  const subject = `Müraciət: ${vals.service || 'Konsultasiya'} — ${vals.fname} ${vals.lname || ''}`;
  const body = [
    `Ad Soyad: ${vals.fname} ${vals.lname || ''}`,
    `Telefon: ${vals.phone}`,
    `Email: ${vals.email || '—'}`,
    `Xidmət: ${vals.service || '—'}`,
    `Qeyd: ${vals.note || '—'}`,
  ].join('\n');
  window.location.href = `mailto:${emailTo || 'info@ragimoff.org'}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  setTimeout(() => {
    const m = document.getElementById('successModal');
    if (m) m.classList.add('show');
  }, 500);
}
// Modal handling
function toggleModal(id, show) {
  const m = document.getElementById(id);
  if (m) m.classList.toggle('show', show);
}

function closeModal(id) {
  toggleModal(id, false);
}

// Lightbox handling
function openLightbox(src) {
  const lb = document.getElementById('lightbox-overlay');
  const img = document.getElementById('lightbox-img');
  if (lb && img) {
    img.src = src;
    lb.style.display = 'flex';
  }
}

function closeLightbox() {
  const lb = document.getElementById('lightbox-overlay');
  if (lb) lb.style.display = 'none';
}

// Accordion
function toggleAcc(id) {
  const item = document.getElementById(id);
  const body = document.getElementById(id + '-body');
  if (!item || !body) return;
  const isOpen = item.classList.contains('open');
  item.classList.toggle('open');
  body.style.maxHeight = isOpen ? '0' : body.scrollHeight + 'px';
}


// ── GALLERY ONE CONTROLLER ──
let galleryX = 0;
function initGalleryOne(id) {
  const gallery = document.getElementById(id);
  if (!gallery) return;

  const slides = gallery.querySelectorAll('.slide');
  let currentIdx = 0;
  let startX = 0;

  // Collection for Stage Mode
  const collection = Array.from(slides).map(s => s.querySelector('img')?.src).filter(Boolean);

  function updateActive() {
    slides.forEach((s, i) => {
      s.classList.toggle('active', i === currentIdx);
    });
  }

  slides.forEach((s, i) => {
    s.addEventListener('click', (e) => {
      if (i === currentIdx || window.innerWidth > 768) {
        const img = s.querySelector('img');
        if (img) openGalleryStage(img.src, collection);
      } else {
        currentIdx = i;
        updateActive();
      }
    });
  });

  // Swipe support for Accordion
  gallery.addEventListener('touchstart', (e) => { startX = e.touches[0].clientX; }, {passive: true});
  gallery.addEventListener('touchend', (e) => {
    const delta = e.changedTouches[0].clientX - startX;
    if (Math.abs(delta) > 50) {
      if (delta > 0 && currentIdx > 0) currentIdx--;
      else if (delta < 0 && currentIdx < slides.length - 1) currentIdx++;
      updateActive();
    }
  }, {passive: true});

  updateActive();
}

let stageCollection = [];
let stageIdx = 0;
let stageStartX = 0;

function openGalleryStage(src, collection = []) {
  stageCollection = collection.length ? collection : [src];
  stageIdx = stageCollection.indexOf(src);
  if (stageIdx === -1) stageIdx = 0;

  let stage = document.querySelector('.gallery-1-stage');
  if (!stage) {
    stage = document.createElement('div');
    stage.className = 'gallery-1-stage';
    stage.innerHTML = `
      <div class="stage-nav stage-prev" onclick="event.stopPropagation(); navigateStage(-1)">‹</div>
      <div class="stage-content"><img src="${src}" alt="Focus view"></div>
      <div class="stage-nav stage-next" onclick="event.stopPropagation(); navigateStage(1)">›</div>
      <div class="stage-counter"></div>
    `;
    stage.onclick = closeGalleryStage;
    
    // Swipe support in Stage Mode
    stage.addEventListener('touchstart', (e) => { stageStartX = e.touches[0].clientX; }, {passive: true});
    stage.addEventListener('touchend', (e) => {
      const delta = e.changedTouches[0].clientX - stageStartX;
      if (Math.abs(delta) > 60) {
        if (delta > 0) navigateStage(-1);
        else navigateStage(1);
      }
    }, {passive: true});

    document.body.appendChild(stage);
    setTimeout(() => stage.classList.add('open'), 10);
  }
  
  updateStage();
  stage.classList.add('open');
}

function navigateStage(dir) {
  stageIdx = (stageIdx + dir + stageCollection.length) % stageCollection.length;
  updateStage();
}

function updateStage() {
  const stage = document.querySelector('.gallery-1-stage');
  if (!stage) return;
  const img = stage.querySelector('img');
  if (img) {
    img.style.opacity = '0';
    setTimeout(() => {
      img.src = stageCollection[stageIdx];
      img.style.opacity = '1';
    }, 150);
  }
  const counter = stage.querySelector('.stage-counter');
  if (counter) counter.innerText = `${stageIdx + 1} / ${stageCollection.length}`;
}

function closeGalleryStage() {
  document.querySelector('.gallery-1-stage')?.classList.remove('open');
}

// ── Language dropdown widget ──────────────────────────────────────────────
function initLangDropdown() {
  var nav = document.querySelector('.desktop-nav');
  if (!nav) return;

  // Determine current language from URL path
  var pth   = window.location.pathname;
  var fn    = pth.split('/').pop() || 'index.html';
  var isRu  = /\/ru\//.test(pth);
  var isEn  = /\/en\//.test(pth);
  var cur   = isRu ? 'ru' : isEn ? 'en' : 'az';

  // All 3 language options — built from path, not DOM
  var options = [
    { code: 'az', label: 'AZ', href: '/' + fn },
    { code: 'ru', label: 'RU', href: '/ru/' + fn },
    { code: 'en', label: 'EN', href: '/en/' + fn }
  ];

  // Remove old .lang-switch links (cleanup HTML remnants)
  nav.querySelectorAll('.lang-switch').forEach(function(a) {
    a.parentNode && a.parentNode.removeChild(a);
  });

  // Wrapper
  var wrap = document.createElement('div');
  wrap.className = 'lang-drop-wrap';

  // Button shows current language
  var btn = document.createElement('button');
  btn.className = 'lang-drop-btn';
  btn.setAttribute('type', 'button');
  btn.setAttribute('aria-haspopup', 'listbox');
  btn.setAttribute('aria-expanded', 'false');
  btn.innerHTML = cur.toUpperCase() + '<svg class="lang-caret" viewBox="0 0 10 6" width="10" height="6" aria-hidden="true"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  // Panel
  var panel = document.createElement('div');
  panel.className = 'lang-drop-panel';
  panel.setAttribute('role', 'listbox');

  options.forEach(function(lg) {
    var isCurrent = (lg.code === cur);
    var item = document.createElement('a');
    item.className = 'lang-drop-item' + (isCurrent ? ' current' : '');
    item.href = isCurrent ? '#' : lg.href;
    item.textContent = lg.label;
    item.setAttribute('role', 'option');
    item.setAttribute('aria-selected', isCurrent ? 'true' : 'false');
    if (isCurrent) {
      item.addEventListener('click', function(e) { e.preventDefault(); });
    } else {
      item.addEventListener('click', function() {
        localStorage.setItem('ragimoff_lang', lg.code);
      });
    }
    panel.appendChild(item);
  });

  wrap.appendChild(btn);
  wrap.appendChild(panel);

  var cta = nav.querySelector('.nav-cta');
  if (cta) nav.insertBefore(wrap, cta);
  else nav.appendChild(wrap);

  // Toggle open/close
  btn.addEventListener('click', function(e) {
    e.stopPropagation();
    var open = wrap.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  document.addEventListener('click', function() {
    wrap.classList.remove('open');
    btn.setAttribute('aria-expanded', 'false');
  });
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') { wrap.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }
  });
}

// ── Mobile language row ────────────────────────────────────────────────────
function initMobileLangRow() {
  var mobileNav = document.getElementById('mobileNav');
  if (!mobileNav) return;
  var oldLinks = Array.from(mobileNav.querySelectorAll('.mobile-lang'));
  if (!oldLinks.length) return;

  var pth  = window.location.pathname;
  var fn   = pth.split('/').pop() || 'index.html';
  var isRu = /\/ru\//.test(pth);
  var isEn = /\/en\//.test(pth);
  var cur  = isRu ? 'ru' : isEn ? 'en' : 'az';

  var langs = [
    { code: 'az', label: 'AZ', href: '/' + fn },
    { code: 'ru', label: 'RU', href: '/ru/' + fn },
    { code: 'en', label: 'EN', href: '/en/' + fn }
  ];

  var row = document.createElement('div');
  row.className = 'mobile-lang-row';

  langs.forEach(function(lg) {
    var a = document.createElement('a');
    a.className = 'mobile-lang-btn' + (lg.code === cur ? ' current' : '');
    a.href = lg.code === cur ? '#' : lg.href;
    a.textContent = lg.label;
    if (lg.code === cur) {
      a.addEventListener('click', function(e) { e.preventDefault(); });
    } else {
      a.addEventListener('click', function() {
        localStorage.setItem('ragimoff_lang', lg.code);
      });
    }
    row.appendChild(a);
  });

  oldLinks.forEach(function(a) { a.parentNode && a.parentNode.removeChild(a); });

  var bookBtn = mobileNav.querySelector('.btn.btn-fill');
  if (bookBtn) mobileNav.insertBefore(row, bookBtn);
  else mobileNav.appendChild(row);
}

// DOM Init
document.addEventListener('DOMContentLoaded', () => {
  // Language UI
  initLangDropdown();
  initMobileLangRow();

  // Global components
  document.querySelectorAll('.acc-open-default').forEach(item => {
    const body = document.getElementById(item.id + '-body');
    if (body) { item.classList.add('open'); body.style.maxHeight = body.scrollHeight + 'px'; }
  });


  // Gallery 1 Init (Automatic for all instances)
  document.querySelectorAll('.gallery-1').forEach(g => {
    if (g.id) initGalleryOne(g.id);
  });

  // Generic Grid Init for other pages (like haqqimda.html)
  document.querySelectorAll('.dip-grid, .dip-grid-2, .dip-grid-3, .d2').forEach(grid => {
    grid.querySelectorAll('a').forEach(link => {
      // If it points to an image, hook it up
      if (link.href.match(/\.(jpg|jpeg|png|webp|gif)/i)) {
        const imgSrc = link.href;
        link.href = 'javascript:void(0)';
        link.onclick = () => openGalleryStage(imgSrc);
      }
    });
  });
});

// ═══════════════════════════════════════════════
//  HERO SEARCH (page-hero-x system) — works on any page
//  with <input id="hero-si"> + <div id="hero-sd">
// ═══════════════════════════════════════════════
(function(){
  function init(){
    var si = document.getElementById('hero-si');
    var sd = document.getElementById('hero-sd');
    if (!si || !sd) return;
    if (window.__heroSearchInited) return;
    window.__heroSearchInited = true;
    var idx = null, loading = false;
    function load(cb){
      if (idx) { cb(idx); return; }
      if (loading) { setTimeout(function(){ load(cb); }, 80); return; }
      loading = true;
      fetch('/search-index.json').then(function(r){ return r.json(); })
        .then(function(d){ idx = d; loading = false; cb(d); })
        .catch(function(){ idx = []; loading = false; cb([]); });
    }
    function showResults(q, data){
      var ql = q.toLowerCase();
      var esc = ql.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      var re = new RegExp(esc, 'gi');
      function hl(s){ return s ? String(s).replace(re, function(m){ return '<mark>' + m + '</mark>'; }) : ''; }
      var res = data.filter(function(x){
        return (x.title + ' ' + (x.text||'')).toLowerCase().indexOf(ql) >= 0;
      }).slice(0, 15);
      if (!res.length) {
        sd.innerHTML = '<div class="ssr"><div class="ssr-title">Nəticə tapılmadı</div></div>';
        sd.classList.add('on'); return;
      }
      sd.innerHTML = res.map(function(r){
        var snip = ''; var txt = r.text || ''; var lo = txt.toLowerCase(); var i2 = lo.indexOf(ql);
        if (i2 >= 0) { var s = Math.max(0, i2-50); snip = txt.slice(s, s+120).trim(); }
        var url = r.url || ((r.page||'') + '.html' + (r.id ? '#' + r.id : ''));
        return '<div class="ssr" onclick="window.location.href=\'' + url + '\'">'
             + '<div class="ssr-title">' + hl(r.title) + '</div>'
             + (snip ? '<div class="ssr-snip">' + hl(snip) + '</div>' : '')
             + '<div class="ssr-sub">' + (r.sub||'') + '</div></div>';
      }).join('');
      sd.classList.add('on');
    }
    function closeSD(){ sd.classList.remove('on'); }
    window.heroSearch = function(){
      var q = si.value.trim();
      if (q.length < 2) return;
      load(function(data){ showResults(q, data); });
    };
    si.addEventListener('focus', function(){ load(function(){}); }, { once: true });
    var tmr;
    si.addEventListener('input', function(){
      clearTimeout(tmr);
      tmr = setTimeout(function(){
        var q = si.value.trim();
        if (q.length < 2) { closeSD(); return; }
        load(function(data){ showResults(q, data); });
      }, 200);
    });
    si.addEventListener('keydown', function(e){
      if (e.key === 'Enter') { window.heroSearch(); }
      if (e.key === 'Escape') { si.value = ''; closeSD(); }
    });
    document.addEventListener('click', function(e){
      if (!si.contains(e.target) && !sd.contains(e.target)) closeSD();
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

/* ── ПОЛОСЫ ВО ВСЮ ШИРИНУ ОКНА (единый стандарт, 05.10.2026) ──────────────
   .gallery-band/.books-band растягиваются формулой width:100vw; margin-left:
   calc(50% - 50vw). Формула верна, если контентная часть родителя
   отцентрована в окне; при вертикальной полосе прокрутки это не так —
   замер: окно 1424, клиентская ширина 1418, полоса уезжала на -3 px влево и
   справа оголяла кромку (аудит 05.10.2026: 20 строк «CLIPPED» на 8
   страницах ×3 языка, класс gallery-band). Здесь кромки ставятся точно по
   клиентской ширине: width = clientWidth, margin-left = -left. Идемпотентно:
   перед замером инлайновые значения снимаются, поэтому resize сходится. */
(function () {
  function fitBands() {
    var cw = document.documentElement.clientWidth;
    var list = document.querySelectorAll(".gallery-band, .books-band");
    for (var i = 0; i < list.length; i++) {
      var b = list[i];
      if (!b.getClientRects().length) continue;
      /* Сначала margin-left = 0: измеряем НАТУРАЛЬНУЮ левую грань (левый
         край контентной части родителя). Без этого в замер попадала бы
         сама формула calc(50% - 50vw) из gtc.css и кромка уезжала. */
      b.style.setProperty("margin-left", "0px", "important");
      b.style.removeProperty("width");
      var left = b.getBoundingClientRect().left;
      b.style.setProperty("width", cw + "px", "important");
      b.style.setProperty("margin-left", (-left) + "px", "important");
      b.style.setProperty("margin-right", "0px", "important");
    }
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", fitBands);
  } else { fitBands(); }
  window.addEventListener("resize", fitBands, { passive: true });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitBands);
})();
