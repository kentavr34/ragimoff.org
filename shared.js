// ═══════════════════════════════════════════════
//  RAGIMOFF.ORG — Shared JS
// ═══════════════════════════════════════════════

// Auto language redirect by IP geolocation (only on first visit)
// Russia → /ru/, Azerbaijan/default → /. Manual choice persists in localStorage.
(function() {
  try {
    var path = window.location.pathname;
    var isRuPage = /\/ru\//.test(path);
    var saved = localStorage.getItem('ragimoff_lang');

    if (saved === 'ru' && !isRuPage) {
      var fname = path.split('/').pop() || 'index.html';
      window.location.replace('/ru/' + fname);
      return;
    }
    if (saved === 'az' && isRuPage) {
      var fname2 = path.split('/').pop() || 'index.html';
      window.location.replace('/' + fname2);
      return;
    }
    if (saved) return;

    fetch('https://ipapi.co/json/').then(function(r){ return r.json(); }).then(function(d){
      var country = (d && d.country_code) ? d.country_code.toUpperCase() : '';
      if (country === 'RU' && !isRuPage) {
        localStorage.setItem('ragimoff_lang', 'ru');
        var fn = window.location.pathname.split('/').pop() || 'index.html';
        window.location.replace('/ru/' + fn);
      } else {
        localStorage.setItem('ragimoff_lang', isRuPage ? 'ru' : 'az');
      }
    }).catch(function(){});
  } catch(e){}
})();

document.addEventListener('click', function(e){
  var t = e.target.closest && e.target.closest('.lang-switch, .mobile-lang');
  if (!t) return;
  var href = t.getAttribute('href') || '';
  var goesToRu = /\/ru\//.test(href) || /^ru\//.test(href);
  localStorage.setItem('ragimoff_lang', goesToRu ? 'ru' : 'az');
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
  var azUrl = base + '/' + fname;
  var ruUrl = base + '/ru/' + fname;
  link('alternate', azUrl,  { hreflang: 'az' });
  link('alternate', ruUrl,  { hreflang: 'ru' });
  link('alternate', azUrl,  { hreflang: 'x-default' });

  // Open Graph
  var isBlog   = /blog/.test(path);
  var ogType   = isBlog ? 'article' : 'website';
  var ogLocale = isRu ? 'ru_RU' : 'az_AZ';
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
  var author = {
    '@type':   'Person',
    'name':    isRu ? 'Кенан Рагимов' : 'Kənan Rəhimov',
    'url':     base + (isRu ? '/ru/haqqimda.html' : '/haqqimda.html'),
    'jobTitle': isRu ? 'Врач-психиатр, психотерапевт' : 'Həkim-Psixiatr, Psixoterapevt'
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
      'inLanguage':  isRu ? 'ru' : 'az',
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
      'inLanguage':  isRu ? 'ru' : 'az',
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

// DOM Init
document.addEventListener('DOMContentLoaded', () => {
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
