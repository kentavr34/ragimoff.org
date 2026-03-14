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

// Generic booking form submit → mailto + modal
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
function closeModal() {
  document.getElementById('successModal')?.classList.remove('show');
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
// Open all .acc-open-default on load
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.acc-open-default').forEach(item => {
    const body = document.getElementById(item.id + '-body');
    if (body) { item.classList.add('open'); body.style.maxHeight = body.scrollHeight + 'px'; }
  });
});
