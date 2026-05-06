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
    var m = document.createElement('meta');
    m.setAttribute(attr || 'property', prop);
    m.content = val;
    head.appendChild(m);
  }
  function link(rel, href, extra) {
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

async function submitToAPI(payload) {
  try {
    const res = await fetch(RAGIMOFF_API, {
      method: 'POST',
      mode: 'no-cors',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify(payload)
    });
    return { ok: true };
  } catch (err) {
    console.error('submitToAPI error:', err);
    return { ok: false, error: String(err) };
  }
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
    if (btn) { btn.textContent = 'Göndərilir...'; btn.disabled = true; }
    await submitToAPI(payload);
    form.style.opacity = '0.5';
    form.style.pointerEvents = 'none';
    if (success) {
      success.style.display = 'block';
      success.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  });
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
