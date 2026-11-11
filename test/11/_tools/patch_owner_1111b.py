"""Правки по замечаниям владельца 11.11 (вечер): блок «Руководители», «Наши книги», компактный слайд книги на телефоне,
стандартная карточка программы, фотогалерея с листанием, пять компактных мифов, кнопка Telegram. Запуск из test/11."""
import io, shutil, pathlib

for f in ('index.html', 'assets/js/site.js', 'assets/css/site.css', 'assets/js/content.js'):
    shutil.copy(f, '_agent/backup/' + pathlib.Path(f).name + '.bak-owner1111b')


def edit(path, pairs):
    t = io.open(path, encoding='utf-8').read()
    for a, b in pairs:
        if a not in t:
            raise SystemExit('НЕ НАЙДЕНО в %s: %s' % (path, a[:90]))
        t = t.replace(a, b, 1)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(t)


edit('index.html', [
    ('<p class="mentors rv" data-i="spec.mentors"></p>', '<div class="lead rv" id="lead"></div>'),
    ('<div class="wrap"><div class="proofs" id="proofs"></div></div>',
     '<div class="wrap"><div class="proofs" id="proofs"></div><p class="sec__more"><button type="button" class="btn btn--line btn--sm" id="galBtn"></button></p></div>'),
    ('<div class="lb" id="lb" aria-hidden="true"><button type="button" class="lb__x" aria-label="×">×</button><figure><img id="lbImg" alt=""><figcaption id="lbCap"></figcaption></figure></div>',
     '<div class="lb" id="lb" aria-hidden="true"><button type="button" class="lb__x" id="lbX" aria-label="×">×</button><button type="button" class="lb__a lb__a--p" id="lbPrev" aria-label="←">‹</button><figure><img id="lbImg" alt=""><figcaption id="lbCap"></figcaption><span class="lb__n" id="lbN"></span></figure><button type="button" class="lb__a lb__a--n" id="lbNext" aria-label="→">›</button></div>'),
    ('<div class="nums" id="nums"></div>', ''),
])

edit('assets/js/site.js', [
    # заголовок секции без пустой метки
    ('<p class="eyebrow rv">${esc(s.eye)}</p>', ''),
    # мифы: компактная карточка — тема, миф, «Подробнее» в раздел учебника
    ("""  $('#myths').innerHTML = t.enl.m.map((m, i) => `<div class="myth rv" style="--d:${i * .08}s"><div class="myth__in">
    <button class="myth__f" type="button"><span class="myth__k">${esc(m[0])}</span><span class="myth__q">${esc(m[1])}</span><span class="myth__btn">${esc(t.enl.flip)}</span></button>
    <div class="myth__b"><span class="myth__k">${esc(m[0])}</span><p class="myth__a">${esc(m[2])}</p><a class="myth__btn" href="${L.myths[i]}">${esc(t.enl.more)} ${ARR}</a></div></div></div>`).join('');""",
     """  $('#myths').innerHTML = t.enl.m.map((m, i) => `<a class="mth rv" href="${L.myths[i] || L.books[0]}" style="--d:${i * .06}s"><span class="mth__k">${esc(t.enl.myth)} · ${esc(m[0])}</span><span class="mth__q">${esc(m[1])}</span><span class="mth__go">${esc(t.enl.go)} ${ARR}</span></a>`).join('');"""),
    ("  $('#nums').innerHTML = t.corp.n.map((n, i) => `<div class=\"num rv\" style=\"--d:${i * .08}s\"><b data-count=\"${esc(n[0])}\">${esc(n[0])}</b><span>${esc(n[1])}</span></div>`).join('');\n", ""),
    # документы и фото: первые три на странице, остальные — в галерее
    ("  $('#proofs').innerHTML = (t.edu.proofs || []).map((c, i) => `<button type=\"button\" class=\"proof rv\" data-lb=\"assets/img/proof/${['diploma', 'cert', 'group'][i]}.jpg\" style=\"--d:${i * .08}s\"><span class=\"proof__i\"><img src=\"assets/img/proof/${['diploma', 'cert', 'group'][i]}.jpg\" alt=\"${esc(c)}\" loading=\"lazy\" width=\"1500\" height=\"1070\"></span><span class=\"proof__c\">${esc(c)}</span></button>`).join('');",
     "  GAL = (t.edu.gal || []).map(g => ({ src: 'assets/img/proof/' + g[0] + '.jpg', cap: g[1] }));\n"
     "  $('#proofs').innerHTML = GAL.slice(0, 3).map((g, i) => `<button type=\"button\" class=\"proof rv\" data-gal=\"${i}\" style=\"--d:${i * .08}s\"><span class=\"proof__i\"><img src=\"${g.src}\" alt=\"${esc(g.cap)}\" loading=\"lazy\" width=\"1500\" height=\"1070\"></span><span class=\"proof__c\">${esc(g.cap)}</span></button>`).join('');\n"
     "  $('#galBtn').textContent = t.edu.galBtn + ' · ' + GAL.length;\n"
     "  const ld = t.spec.lead; $('#lead').innerHTML = ld ? `<h3 class=\"lead__h\">${esc(ld.h)}</h3><ol class=\"lead__l\">${ld.items.map(x => `<li><b>${esc(x[0])}</b><span>${esc(x[1])}</span></li>`).join('')}</ol><p class=\"lead__y\"><b>${esc(ld.study[0])}</b><span>${esc(ld.study[1])}</span></p><p class=\"lead__y\"><b>${esc(ld.now[0])}</b><span>${esc(ld.now[1])}</span></p>` : '';\n"
     "  if (t.a11y && t.a11y.prev) { $('#bkPrev').setAttribute('aria-label', t.a11y.prev); $('#bkNext').setAttribute('aria-label', t.a11y.next); $('#lbPrev').setAttribute('aria-label', t.a11y.prev); $('#lbNext').setAttribute('aria-label', t.a11y.next); $('#lbX').setAttribute('aria-label', t.a11y.close); }"),
    ("const shelf = $('#shelf');",
     "function galShow(i) { if (!GAL.length) return; galI = (i + GAL.length) % GAL.length; $('#lbImg').src = GAL[galI].src; $('#lbCap').textContent = GAL[galI].cap; $('#lbN').textContent = (galI + 1) + ' / ' + GAL.length; $('#lb').classList.add('is-open'); $('#lb').setAttribute('aria-hidden', 'false'); }\n"
     "function galClose() { $('#lb').classList.remove('is-open'); $('#lb').setAttribute('aria-hidden', 'true'); }\n"
     "addEventListener('keydown', e => { if (!$('#lb').classList.contains('is-open')) return; if (e.key === 'Escape') galClose(); if (e.key === 'ArrowRight') galShow(galI + 1); if (e.key === 'ArrowLeft') galShow(galI - 1); });\n"
     "let lbX0 = null; $('#lb').addEventListener('touchstart', e => { lbX0 = e.touches[0].clientX; }, { passive: true }); $('#lb').addEventListener('touchend', e => { if (lbX0 == null) return; const d = e.changedTouches[0].clientX - lbX0; lbX0 = null; if (Math.abs(d) > 40) galShow(galI + (d < 0 ? 1 : -1)); }, { passive: true });\n"
     "const shelf = $('#shelf');"),
    ("  const pf = e.target.closest('[data-lb]'); if (pf) { $('#lbImg').src = pf.dataset.lb; $('#lbCap').textContent = pf.querySelector('.proof__c').textContent; $('#lb').classList.add('is-open'); $('#lb').setAttribute('aria-hidden', 'false'); return; }\n"
     "  if (e.target.closest('#lb')) { $('#lb').classList.remove('is-open'); $('#lb').setAttribute('aria-hidden', 'true'); return; }",
     "  const pf = e.target.closest('[data-gal]'); if (pf) { galShow(+pf.dataset.gal); return; }\n"
     "  if (e.target.closest('#galBtn')) { galShow(0); return; }\n"
     "  if (e.target.closest('#lbNext')) { galShow(galI + 1); return; } if (e.target.closest('#lbPrev')) { galShow(galI - 1); return; }\n"
     "  if (e.target.closest('#lb')) { if (!e.target.closest('figure') || e.target.closest('#lbX')) galClose(); return; }"),
    ("let lang = ", "let GAL = [], galI = 0;\nlet lang = "),
])

css = io.open('assets/css/site.css', encoding='utf-8').read()
if 'ЗАМЕЧАНИЯ ВЛАДЕЛЬЦА 11.11 (вечер)' not in css:
    css += r"""

/* ═══ ЗАМЕЧАНИЯ ВЛАДЕЛЬЦА 11.11 (вечер) ═══ */
/* руководители: слева, с золотой линией — разрыв между специалистами и книгами */
.lead { margin-top: var(--r4); padding-left: var(--r3); border-left: 2px solid var(--gold); max-width: 900px; text-align: left; } .lead:empty { display: none; }
.lead__h { font: 600 12.5px/1.3 var(--f-sub); letter-spacing: .24em; text-transform: uppercase; color: var(--gold); margin-bottom: var(--r2); }
.lead__l { display: flex; flex-direction: column; gap: var(--r2); counter-reset: ld; }
.lead__l li { display: grid; grid-template-columns: 34px minmax(0, 1fr); column-gap: 8px; counter-increment: ld; } .lead__l li::before { content: counter(ld, decimal-leading-zero); grid-row: 1 / 3; font: 600 13px/2.2 var(--f-num); color: var(--gold); }
.lead__l b { font: 400 clamp(23px, 2.1vw, 31px)/1.15 var(--f-display); color: var(--milk); } .lead__l span { margin-top: 6px; font: 400 17px/1.55 var(--f-read); color: var(--text); max-width: 60ch; }
.lead__y { margin-top: var(--r2); padding-top: var(--r2); border-top: 1px solid var(--line); display: grid; grid-template-columns: minmax(120px, max-content) minmax(0, 1fr); gap: var(--r2); align-items: baseline; }
.lead__y b { font: 400 clamp(21px, 1.8vw, 27px)/1.2 var(--f-display); color: var(--gold-hi); font-variant-numeric: lining-nums; white-space: nowrap; } .lead__y span { font: 400 17px/1.55 var(--f-read); color: var(--text); max-width: 60ch; }

/* карточка программы: один стандарт — название в одну строку, документ в две, две строки условий, цена, кнопка; без пустот */
.pc { gap: 14px; } .pc__t { font-size: clamp(21px, 1.6vw, 24px); line-height: 1.15; min-height: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.pc__d { min-height: 2.9em; } .pc__m { flex-direction: column; align-items: flex-start; gap: 6px; min-height: 68px; } .pc__m span { white-space: nowrap; max-width: 100%; overflow: hidden; text-overflow: ellipsis; }
.pc__p { margin-top: 0; }

/* мифы: пять компактных карточек — на телефоне две видны сразу */
.myths { grid-template-columns: repeat(5, minmax(0, 1fr)); gap: var(--r1); }
.mth { display: flex; flex-direction: column; gap: 10px; padding: var(--r2) var(--r1) var(--r1); border-radius: calc(var(--rad) * .7); background: var(--layer); border: 1px solid var(--line); text-align: left; transition: transform var(--t2) var(--e), border-color var(--t1); }
.mth:hover { transform: translateY(-4px); border-color: color-mix(in srgb, var(--gold) 60%, transparent); }
.mth__k { font: 600 11.5px/1.3 var(--f-sub); letter-spacing: .18em; text-transform: uppercase; color: var(--gold); }
.mth__q { font: 400 italic clamp(19px, 1.45vw, 22px)/1.25 var(--f-display); color: var(--milk); } .mth__q::before { content: "«"; } .mth__q::after { content: "»"; }
.mth__go { margin-top: auto; min-height: var(--tap); display: inline-flex; align-items: center; gap: 8px; font: 600 14px/1 var(--f-sub); color: var(--gold-hi); }

/* галерея: листание в окне просмотра */
.lb figure { position: relative; } .lb__n { font: 600 12.5px/1 var(--f-num); letter-spacing: .14em; color: #B9B3A7; }
.lb__a { position: absolute; top: 50%; width: 54px; height: 54px; margin-top: -27px; border-radius: 50%; border: 1px solid rgba(242, 237, 227, .4); color: #F2EDE3; font: 300 30px/1 var(--f-sub); display: grid; place-items: center; z-index: 2; background: rgba(5, 6, 9, .5); }
.lb__a--p { left: 14px; } .lb__a--n { right: 14px; } .lb { cursor: default; } .lb img { cursor: default; }

/* Telegram: кнопка обычного размера */
.tg .btn { min-height: var(--btn-h-sm); padding: 0 26px; width: auto; align-self: center; } .tg { padding: var(--r3) var(--r2); gap: var(--r1); } .tg__h { font-size: clamp(30px, 3.6vw, 54px); }

@media (max-width: 1100px) { .myths { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
@media (max-width: 760px) {
  .lead { padding-left: var(--r2); margin-top: var(--r3); } .lead__y { grid-template-columns: 1fr; gap: 4px; }
  .myths { grid-template-columns: 1fr; } .mth { padding: var(--r1) var(--r1) 4px; gap: 6px; } .mth__q { font-size: 19px; }
  /* книга на телефоне: обложка сверху, описание под ней — всё на одном экране */
  .bk { gap: 10px; align-content: start; } .bk__scene { padding: 6px 0 0; } .bk__obj { --w: 34vw; } .bk__scene::after { height: 16px; margin-top: 2px; }
  .bk__t { margin-top: 0; font-size: 27px; } .bk__a { margin-top: 4px; font-size: 15.5px; } .bk__f { margin-top: 10px; } .bk__f li { padding: 8px 0; font-size: 16px; line-height: 1.4; grid-template-columns: 28px 1fr; }
  .bk__btns { margin-top: 12px; gap: 8px; flex-wrap: nowrap; } .bk__btns .btn { width: auto; flex: 1 1 0; min-height: var(--btn-h-sm); padding: 0 10px; font-size: 14px; }
  .shelf__nav { margin-top: var(--r1); }
  .pc { width: 82vw; } .rib__stick { padding: 76px 0 var(--r2); }
  .lb__a { width: 44px; height: 44px; margin-top: -22px; } .lb__a--p { left: 4px; } .lb__a--n { right: 4px; }
}
"""
    io.open('assets/css/site.css', 'w', encoding='utf-8', newline='\n').write(css)

t = io.open('assets/js/content.js', encoding='utf-8').read()
if 'OWNER_1111B' not in t:
    t += """
/* ── OWNER_1111B: слова владельца 11.11 (вечер) — руководители, «Наши книги», частые заблуждения, галерея, короткие названия ── */
const OWN = {
  ru: {
    lead: { h: 'Руководители',
      items: [['Профессор Борис Дмитриевич Карвасарский', 'Главный психотерапевт Министерства здравоохранения Российской Федерации до 2012 года.'],
              ['Профессор Виктор Давыдович Вид', 'Первый в странах СНГ психоаналитик, официально дипломированный Международной психоаналитической ассоциацией.']],
      study: ['2001–2003', 'Кенан Рагимов учился под их руководством в Институте имени Бехтерева.'],
      now: ['С 2003 года', 'По настоящее время сотрудничает с Институтом имени Карвасарского и Санкт-Петербургским институтом дополнительного профессионального образования: преподаватель и член аттестационной комиссии.'] },
    booksH: 'Наши книги', booksSub: 'Книги наших специалистов и переводы профессиональных учебников. С некоторыми из них можно ознакомиться здесь.',
    enlSub: 'Самые частые заблуждения, из-за которых люди не получают вовремя квалифицированную помощь. Читайте и разбирайтесь.',
    myth: 'Миф', go: 'Подробнее', kpt: 'КПТ', galBtn: 'Фотогалерея',
    gal: [['diploma', 'Диплом о профессиональной переподготовке — образец'], ['cert', 'Международный сертификат — образец'], ['group', 'Группа «Школы психологии» с преподавателем'],
          ['supplement', 'Приложение к диплому: дисциплины и часы'], ['cert-family', 'Международный сертификат по семейной терапии — образец'], ['meeting', 'Кенан Рагимов на встрече с группой'], ['outdoor', 'Группа слушателей']] },
  az: {
    lead: { h: 'Rəhbərlər',
      items: [['Professor Boris Dmitriyeviç Karvasarski', '2012-ci ilədək Rusiya Federasiyası Səhiyyə Nazirliyinin baş psixoterapevti.'],
              ['Professor Viktor Davidoviç Vid', 'MDB ölkələrində Beynəlxalq Psixoanaliz Assosiasiyasının rəsmi diplomunu almış ilk psixoanalitik.']],
      study: ['2001–2003', 'Kənan Rəhimov Bexterev adına İnstitutda onların rəhbərliyi altında təhsil alıb.'],
      now: ['2003-cü ildən', 'Bu günədək Karvasarski adına İnstitut və Sankt-Peterburq Əlavə Təhsil İnstitutu ilə əməkdaşlıq edir: müəllim və attestasiya komissiyasının üzvüdür.'] },
    booksH: 'Kitablarımız', booksSub: 'Mütəxəssislərimizin kitabları və peşəkar dərsliklərin tərcümələri. Bəziləri ilə burada tanış ola bilərsiniz.',
    enlSub: 'İnsanların vaxtında ixtisaslı kömək almasına mane olan ən çox yayılmış yanlış təsəvvürlər. Oxuyun və aydınlaşdırın.',
    myth: 'Mif', go: 'Ətraflı', kpt: 'KDT', galBtn: 'Fotoqalereya',
    gal: [['diploma', 'Peşə yenidənhazırlığı haqqında diplom — nümunə'], ['cert', 'Beynəlxalq sertifikat — nümunə'], ['group', '«Psixologiya Məktəbi»nin qrupu müəllimlə birlikdə'],
          ['supplement', 'Diploma əlavə: fənlər və saatlar'], ['cert-family', 'Ailə terapiyası üzrə beynəlxalq sertifikat — nümunə'], ['meeting', 'Kənan Rəhimov qrupla görüşdə'], ['outdoor', 'Dinləyicilər qrupu']] },
  en: {
    lead: { h: 'Mentors',
      items: [['Professor Boris Dmitrievich Karvasarsky', 'Chief psychotherapist of the Ministry of Health of the Russian Federation until 2012.'],
              ['Professor Viktor Davydovich Vid', 'The first psychoanalyst in the CIS countries officially certified by the International Psychoanalytical Association.']],
      study: ['2001–2003', 'Kenan Ragimov studied under their supervision at the Bekhterev Institute.'],
      now: ['Since 2003', 'To this day he works with the Karvasarsky Institute and the Saint Petersburg Institute of Continuing Professional Education as a lecturer and a member of the attestation commission.'] },
    booksH: 'Our books', booksSub: 'Books by our specialists and translations of professional textbooks. You can explore some of them here.',
    enlSub: 'The most common misconceptions that keep people from getting qualified help in time. Read and find out.',
    myth: 'Myth', go: 'Read more', kpt: 'CBT', galBtn: 'Photo gallery',
    gal: [['diploma', 'Diploma of professional retraining — sample'], ['cert', 'International certificate — sample'], ['group', 'A School of Psychology group with their teacher'],
          ['supplement', 'Diploma supplement: subjects and hours'], ['cert-family', 'International certificate in family therapy — sample'], ['meeting', 'Kenan Ragimov at a meeting with a group'], ['outdoor', 'A group of students']] },
};
for (const l of Object.keys(OWN)) { const o = OWN[l], t = T[l];
  t.spec.lead = o.lead; t.books.h = o.booksH; t.books.sub = o.booksSub; t.enl.sub = o.enlSub; t.enl.myth = o.myth; t.enl.go = o.go; t.edu.gal = o.gal; t.edu.galBtn = o.galBtn;
  t.edu.p[4].t = o.kpt;                                   /* короткое название — в одну строку на карточке */
  if (t.a11y) Object.assign(t.a11y, l === 'ru' ? { prev: 'Назад', next: 'Вперёд', close: 'Закрыть' } : l === 'az' ? { prev: 'Geri', next: 'İrəli', close: 'Bağla' } : { prev: 'Previous', next: 'Next', close: 'Close' });
}
"""
    io.open('assets/js/content.js', 'w', encoding='utf-8', newline='\n').write(t)
print('patched')
