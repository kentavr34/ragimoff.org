// ═══════════════════════════════════════════════
//  RAGIMOFF.ORG — Shared JS
// ═══════════════════════════════════════════════

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
