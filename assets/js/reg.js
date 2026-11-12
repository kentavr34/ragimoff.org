/* test/11 — единая форма записи: сначала «на что», дальше поля меняются. Всё, что можно, выбирается нажатием и уже выбрано по умолчанию.
   Отправка — тем же путём, что на действующем сайте: заявка на api.ragimoff.org/api/training-reg, затем переход на оплату ePoint. */
const API = 'https://api.ragimoff.org';
const WA = 'https://wa.me/994702200376';
const RATE = { one: { online: 100, offline: 150 }, both: { online: 150, offline: 200 } };          /* AZN, слово владельца 08.11 */
const ENU = 3, ENU_P = { first: 50, course: 500 };                                                    /* ночной энурез (тема № 4): слово владельца 11.11 */
const PROG = ['Общая психология', 'Клиническая психология', 'Практикум по психотерапии', 'short-psixodiaqnostika', 'short-kdt', 'short-psixoanaliz', 'short-aile'];   /* коды сервера оплаты */
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const st = { kind: 'consult', who: 'kenan', fmt: 'online', topic: 0, prog: 0, hours: 20, enu: 'first', btopic: [0], goal: 0, count: 1, blang: 0, place: 0 };
let T = null, lang = 'ru', box = null;

const chips = (name, opts, cur, multi) => `<div class="chips" role="group">${opts.map((o, i) => { const v = Array.isArray(o) ? o[0] : i, l = Array.isArray(o) ? o[1] : o; const on = multi ? cur.includes(v) : cur === v;
  return `<button type="button" class="chip${on ? ' is-on' : ''}" data-set="${name}" data-v="${esc(v)}" aria-pressed="${on}">${esc(l)}</button>`; }).join('')}</div>`;
const field = (name, label, type, extra) => `<label class="fld"><span>${esc(label)}</span><input class="inp" name="${name}" type="${type || 'text'}" ${extra || ''}></label>`;
const row = (label, html) => `<div class="frow"><span class="frow__l">${esc(label)}</span>${html}</div>`;

function price() {
  const r = T.reg, who = st.who === 'both' ? 'both' : 'one';
  if (st.kind === 'consult' && st.topic === ENU) return { main: ENU_P[st.enu] + ' AZN', sub: r.enu.sub[st.enu] };
  if (st.kind === 'consult') return { main: RATE[who][st.fmt] + ' AZN', sub: r.perHour };
  if (st.kind === 'ind') return { main: (RATE[who][st.fmt] * st.hours).toLocaleString('ru-RU').replace(/\s/g, ' ') + ' AZN', sub: st.hours + ' × ' + RATE[who][st.fmt] + ' AZN' };
  if (st.kind === 'edu') return { main: T.edu.p[st.prog].price, sub: T.edu.p[st.prog].m.join(' · ') };
  return { main: '', sub: '' };
}

function html() {
  const r = T.reg, k = st.kind, pr = price();
  const topics = T.cons.t.map(x => x[0]).concat([r.topicOther]);
  const head = `<div class="reg__kinds" role="tablist">${r.kinds.map(x => `<button type="button" role="tab" class="reg__kind${x[0] === k ? ' is-on' : ''}" data-set="kind" data-v="${x[0]}" aria-selected="${x[0] === k}">${esc(x[1])}</button>`).join('')}</div>`;
  const who = row(r.who.l, chips('who', r.who.o, st.who)), fmt = row(r.fmt.l, chips('fmt', r.fmt.o, st.fmt));
  let body = '';
  if (k === 'consult') body = row(r.topic, chips('topic', topics, st.topic)) + (st.topic === ENU ? row(r.enu.l, chips('enu', r.enu.o, st.enu)) : who + fmt) + (st.topic === topics.length - 1 ? field('other', r.f.other, 'text', 'maxlength="160"') : '');
  if (k === 'edu') body = row(r.prog, chips('prog', T.edu.p.map(p => p.t), st.prog)) + files();
  if (k === 'ind') body = who + fmt + row(r.hours.l, `<div class="step"><button type="button" class="step__b" data-step="-5" aria-label="−5">−</button><output class="step__v">${st.hours}</output><button type="button" class="step__b" data-step="5" aria-label="+5">+</button><span class="step__h">${esc(r.hours.min)}</span></div>`) + files();
  if (k === 'b2b') body = field('company', r.f.company, 'text', 'autocomplete="organization" maxlength="120"') + row(r.b2b.topic, chips('btopic', T.corp.t.concat([r.b2b.other]), st.btopic, true))
    + row(r.b2b.goal.l, chips('goal', r.b2b.goal.o, st.goal)) + row(r.b2b.count.l, chips('count', r.b2b.count.o, st.count)) + row(r.b2b.lang.l, chips('blang', r.b2b.lang.o, st.blang)) + row(r.b2b.place.l, chips('place', r.b2b.place.o, st.place));
  const who3 = `<div class="reg__me">${field('fname', r.f.fname, 'text', 'autocomplete="given-name" maxlength="60"')}${field('lname', r.f.lname, 'text', 'autocomplete="family-name" maxlength="60"')}${field('phone', r.f.phone, 'tel', 'autocomplete="tel" inputmode="tel" value="+994 " maxlength="24"')}</div>`;
  const side = `<aside class="reg__side">${pr.main ? `<p class="reg__pl">${esc(r.price)}</p><p class="reg__p">${esc(pr.main)}</p><p class="reg__ps">${esc(pr.sub)}</p>` : `<p class="reg__pl">${esc(r.b2b.free)}</p>`}
    <p class="reg__note">${esc(k === 'b2b' ? r.noteB2b : T.cons.note)}</p><button type="submit" class="btn reg__go">${esc(r.send[k])}</button><div class="reg__pay" hidden></div><p class="reg__msg" role="status" hidden></p></aside>`;
  return `${head}<form class="reg__f" novalidate><div class="reg__main">${body}${who3}</div>${side}</form>`;
}
function files() { const r = T.reg; return `<div class="reg__files"><label class="fld fld--file"><span>${esc(r.f.id)}</span><input class="inp" name="idcard" type="file" accept="image/*,.pdf"></label><label class="fld fld--file"><span>${esc(r.f.dip)}</span><input class="inp" name="diploma" type="file" accept="image/*,.pdf"></label></div>`; }

function keep() { const o = {}; box.querySelectorAll('input:not([type=file])').forEach(i => { o[i.name] = i.value; }); return o; }
function draw(vals) { box.innerHTML = html(); if (vals) Object.keys(vals).forEach(n => { const i = box.querySelector(`input[name="${n}"]`); if (i && vals[n]) i.value = vals[n]; }); }

export function regRender(t, l) { T = t; lang = l; box = document.getElementById('regBox'); if (!box || !t.reg) return; draw(box.querySelector('form') ? keep() : null); }
export function regOpen(kind, topic, prog, who) { if (!box) return; const v = keep(); if (kind) st.kind = kind; if (topic != null) st.topic = topic; if (prog != null) st.prog = prog; if (who) st.who = who; draw(v); }

const b64 = f => new Promise(res => { const r = new FileReader(); r.onload = () => res(String(r.result).split(',')[1] || ''); r.onerror = () => res(''); r.readAsDataURL(f); });
function say(text, bad, wa) { const m = box.querySelector('.reg__msg'); m.hidden = false; m.className = 'reg__msg' + (bad ? ' is-err' : ''); m.innerHTML = esc(text) + (wa ? ` <a href="${WA}" target="_blank" rel="noopener">WhatsApp</a>` : ''); }

async function submit(form) {
  const r = T.reg, k = st.kind, g = n => (form.querySelector(`[name="${n}"]`) || {}).value || '';
  const need = ['fname', 'lname', 'phone'].concat(k === 'b2b' ? ['company'] : []).concat(k === 'consult' && st.topic === T.cons.t.length ? ['other'] : []);
  let ok = true;
  need.forEach(n => { const el = form.querySelector(`[name="${n}"]`); const bad = !el || el.value.replace(/[+\s\d]/g, n === 'phone' ? '' : '$&').trim().length < (n === 'phone' ? 0 : 2) || (n === 'phone' && el.value.replace(/\D/g, '').length < 9); if (el) el.classList.toggle('is-bad', bad); if (bad) ok = false; });
  const idf = form.querySelector('[name="idcard"]'); if (idf && !idf.files[0]) { idf.classList.add('is-bad'); ok = false; } else if (idf) idf.classList.remove('is-bad');
  if (!ok) { say(r.req, true); return; }
  const lab = (o, v) => { const x = o.find(a => a[0] === v); return x ? x[1] : ''; };
  let service = '', note = '';
  if (k === 'consult') { const en = st.topic === ENU; service = en ? 'consult|kenan|enurez-' + st.enu : `consult|${st.who}|${st.fmt}`; const tp = st.topic < T.cons.t.length ? T.cons.t[st.topic][0] : r.topicOther + ': ' + g('other'); note = (en ? [lab(r.who.o, 'kenan'), tp, lab(r.enu.o, st.enu)] : [lab(r.who.o, st.who), lab(r.fmt.o, st.fmt), tp]).join(' · '); }
  if (k === 'edu') { service = PROG[st.prog]; note = T.edu.p[st.prog].t; }
  if (k === 'ind') { const rate = RATE[st.who === 'both' ? 'both' : 'one'][st.fmt]; service = `individual|${st.who}|${st.fmt}|${st.hours}`; note = [lab(r.who.o, st.who), lab(r.fmt.o, st.fmt), `${st.hours} × ${rate} = ${st.hours * rate} AZN`].join(' · '); }
  if (k === 'b2b') { service = 'b2b-request'; const all = T.corp.t.concat([r.b2b.other]); note = [g('company'), r.b2b.topic + ': ' + st.btopic.map(i => all[i]).join(', '), r.b2b.goal.l + ': ' + r.b2b.goal.o[st.goal], r.b2b.count.l + ': ' + r.b2b.count.o[st.count], r.b2b.lang.l + ': ' + r.b2b.lang.o[st.blang], r.b2b.place.l + ': ' + r.b2b.place.o[st.place]].join(' · '); }
  const btn = form.querySelector('.reg__go'), lbl = btn.textContent; btn.disabled = true; btn.textContent = r.sending;
  const att = [];
  for (const fn of ['idcard', 'diploma']) { const fe = form.querySelector(`[name="${fn}"]`), f = fe && fe.files[0]; if (f && f.size < 10 * 1024 * 1024) att.push({ field: fn === 'idcard' ? 'shexsiyyet' : 'diplom', filename: f.name, mime: f.type || 'application/octet-stream', data: await b64(f) }); }
  const payload = { type: 'registration', fname: g('fname').trim(), lname: g('lname').trim(), phone: g('phone').trim(), email: '', address: '', service, lang, note, source: location.pathname.replace(/^\//, ''), attachments: att };
  const reg = await fetch(API + '/api/training-reg', { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(payload) })
    .then(x => x.ok ? x.json().catch(() => ({ ok: true })) : null, () => null);
  btn.textContent = lbl; btn.disabled = false;
  if (!reg) { say(r.err, true, true); return; }
  if (k === 'b2b' || !reg.prices) { say(r.ok); return; }
  try { localStorage.setItem('rgm_pay_lang', lang); } catch (e) {}
  const data = { name: payload.fname + ' ' + payload.lname, phone: payload.phone, program: service, folder: reg.folder || '', lang };
  const go = (mode, b) => { if (b) b.disabled = true; data.mode = mode;
    return fetch(API + '/api/billing/epoint/training', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }).then(x => x.json())
      .then(d => { if (d && d.ok && d.redirect_url) { location.href = d.redirect_url; return; } throw new Error('pay'); }).catch(() => { if (b) b.disabled = false; say(r.err, true, true); }); };
  const p = reg.prices, single = k !== 'edu' || p.prepay === p.full;
  if (single) { btn.disabled = true; go('prepay', btn); return; }
  btn.hidden = true; const pb = box.querySelector('.reg__pay'); pb.hidden = false;
  pb.innerHTML = `<button type="button" class="btn" data-m="prepay">${esc(r.pay.now)} — ${esc(p.prepay)} AZN</button><button type="button" class="btn btn--line" data-m="installment">${esc(r.pay.inst)} — ${esc(p.full)} AZN</button>`;
  pb.querySelectorAll('button').forEach(b => { b.onclick = () => go(b.dataset.m, b); });
}

document.addEventListener('click', e => {
  if (!box) return;
  const c = e.target.closest('#regBox [data-set]');
  if (c) { const n = c.dataset.set, raw = c.dataset.v, v = /^\d+$/.test(raw) ? +raw : raw, vals = keep();
    if (n === 'btopic') { const i = st.btopic.indexOf(v); if (i >= 0) { if (st.btopic.length > 1) st.btopic.splice(i, 1); } else st.btopic.push(v); } else st[n] = v;
    draw(vals); const f = box.querySelector(`[data-set="${n}"][data-v="${raw}"]`); if (f) f.focus({ preventScroll: true }); return; }
  const s = e.target.closest('#regBox [data-step]'); if (s) { const vals = keep(); st.hours = Math.max(20, Math.min(200, st.hours + (+s.dataset.step))); draw(vals); return; }
});
document.addEventListener('submit', e => { const f = e.target.closest('#regBox form'); if (f) { e.preventDefault(); submit(f); } });
document.addEventListener('input', e => { if (e.target.closest('#regBox') && e.target.classList) e.target.classList.remove('is-bad'); });
