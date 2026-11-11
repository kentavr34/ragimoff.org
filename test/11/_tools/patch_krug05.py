"""Правки по пятому кругу критика и доводка закреплённых блоков. Запуск из test/11."""
import io, re


def sub1(t, pat, rep, what, flags=0, count=1):
    t2, n = re.subn(pat, rep, t, count=count, flags=flags)
    if n < 1:
        raise SystemExit('не найдено: ' + what)
    return t2


# ── скрипт: закреплённые панели по высоте содержимого, по центру экрана — после них нет пустого остатка
p = 'assets/js/site.js'
t = io.open(p, encoding='utf-8').read()
t = sub1(t, r"function ribMeasure\(\) \{\n  track\.style\.setProperty\('--x', '0px'\);",
         "function stickTop(el) { el.style.top = Math.max(innerWidth < 761 ? 60 : 0, Math.round((innerHeight - el.offsetHeight) / 2)) + 'px'; }\nfunction ribMeasure() {\n  track.style.setProperty('--x', '0px'); stickTop(ribStick);", 'ribMeasure')
t = sub1(t, r"function bkMeasure\(\) \{ const n = shelf\.children\.length;", "function bkMeasure() { const n = shelf.children.length; stickTop(bkStick);", 'bkMeasure')
# прогресс считать от момента, когда панель встала на своё место (top = её отступ)
t = sub1(t, r"const r = rib\.getBoundingClientRect\(\), total = rib\.offsetHeight - ribStick\.offsetHeight, p = total > 0 \? clamp\(-r\.top / total\) : 0;",
         "const r = rib.getBoundingClientRect(), total = rib.offsetHeight - ribStick.offsetHeight, p = total > 0 ? clamp((parseFloat(ribStick.style.top) - r.top) / total) : 0;", 'ribScroll')
t = sub1(t, r"const r = bkSec\.getBoundingClientRect\(\), total = bkSec\.offsetHeight - bkStick\.offsetHeight, p = total > 0 \? clamp\(-r\.top / total\) : 0;",
         "const r = bkSec.getBoundingClientRect(), total = bkSec.offsetHeight - bkStick.offsetHeight, p = total > 0 ? clamp((parseFloat(bkStick.style.top) - r.top) / total) : 0;", 'bkScroll')
t = sub1(t, r"scrollTo\(\{ top: bkSec\.getBoundingClientRect\(\)\.top \+ scrollY \+ i \* bkStep, behavior: 'smooth' \}\);",
         "scrollTo({ top: bkSec.getBoundingClientRect().top + scrollY - parseFloat(bkStick.style.top) + i * bkStep + 2, behavior: 'smooth' });", 'bkGo')
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

# ── разметка: кнопка галереи над рядом документов
p = 'index.html'
t = io.open(p, encoding='utf-8').read()
a = '<div class="wrap"><div class="proofs" id="proofs"></div><p class="sec__more"><button type="button" class="btn btn--line btn--sm" id="galBtn"></button></p></div>'
if a in t:
    t = t.replace(a, '<div class="wrap proofwrap"><p class="proofs__top"><button type="button" class="btn btn--line btn--sm" id="galBtn"></button></p><div class="proofs" id="proofs"></div></div>')
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

# ── стили
CSS = """
/* ═══ КРУГ 05 ═══ */
:root { --s1: calc(var(--u) * .5); --s2: var(--u); --s3: calc(var(--u) * 1.5); }
/* закреплённые панели: высота по содержимому, место на экране задаёт скрипт (по центру) */
.rib__stick, .bk__stick { min-height: 0; justify-content: flex-start; padding: 0; }
.bk__stick .sh, .rib__stick .sh { margin-bottom: var(--h); } .bk__stick .sh__s { margin-top: calc(var(--h) * .5); }
.sec--bk, .sec--rib { margin-top: var(--hs); }
@media (max-width: 760px) { .bk__stick, .rib__stick { padding: 0; } .bk__stick .sh, .rib__stick .sh { margin-bottom: var(--r2); } }
/* документы: кнопка галереи над рядом, ряд сразу под лентой */
.proofwrap { margin-top: var(--r3); } .proofs { margin-top: var(--r1); } .proofs__top { display: flex; justify-content: flex-end; } .shelf__lib { margin-top: var(--r3); }
@media (max-width: 760px) { .proofs__top { justify-content: center; } }
/* карточка программы: строка условий не обрезается, зазоры из шкалы */
.pc { gap: var(--s3); } .pc__d { min-height: 0; } .pc__m { gap: var(--s1); min-height: 0; } .pc__m span { white-space: normal; overflow: visible; }
/* мифы: ссылка сразу под текстом — внутри карточки нет дыры */
.mth { gap: var(--s2); } .mth__go { margin-top: 0; } .mth__k { min-height: 2.6em; }
@media (max-width: 760px) { .mth__k { min-height: 0; } .mth { gap: var(--s1); } .seg--lang button { min-width: var(--tap); } .head { gap: var(--s1); } .head__r { gap: var(--s1); } }
@media (max-width: 359px) { .seg--lang button { min-width: 34px; } }
/* герой на телефоне: зазоры от имени до подписи и от подписи до кнопок равны на глаз */
@media (max-width: 760px) { .cine__school { margin-top: var(--s3); } .cine__btns { margin-top: calc(var(--s3) + var(--s2)); } }
/* руководители: год — отдельной колонкой одной ширины; висячие слова */
.lead__y { grid-template-columns: 9.5em minmax(0, 1fr); } .lead__y span, .lead__l span, .topic__s, .film__d, .corp__lead { text-wrap: pretty; }
@media (max-width: 760px) { .lead__y { grid-template-columns: 1fr; } .lead__l li { grid-template-columns: 28px minmax(0, 1fr); } .lead__l b { font-size: 22px; } }
.facts li::before { top: 50%; }
"""
p = 'assets/css/site.css'
c = io.open(p, encoding='utf-8').read()
if 'КРУГ 05' not in c:
    io.open(p, 'w', encoding='utf-8', newline='\n').write(c + CSS)

# ── тексты
p = 'assets/js/content.js'
t = io.open(p, encoding='utf-8').read()
NB = ' '
pairs = [
    (r"booksSub: 'Авторские книги и переводы профессиональных учебников\.'", "booksSub: 'Книги наших специалистов и переводы учебников.'"),
    (r"booksSub: 'Müəllif kitabları və peşəkar dərsliklərin tərcümələri\.'", "booksSub: 'Mütəxəssislərimizin kitabları və dərslik tərcümələri.'"),
    (r"booksSub: 'Our own books and translations of professional textbooks\.'", "booksSub: 'Books by our specialists and translated textbooks.'"),
    (r"enlSub: 'Заблуждения, мешающие вовремя получить помощь специалиста\.'", "enlSub: 'Частые заблуждения на" + NB + "пути к" + NB + "квалифицированной помощи.'"),
    (r"enlSub: 'Vaxtında ixtisaslı kömək almağa mane olan yanlış təsəvvürlər\.'", "enlSub: 'İxtisaslı köməyə mane olan ən çox yayılmış yanlış təsəvvürlər.'"),
    (r"enlSub: 'Misconceptions that keep people from qualified help in time\.'", "enlSub: 'Common misconceptions on the way to qualified help.'"),
    (r"now: \['С 2003 года', 'По настоящее время сотрудничает", "now: ['С 2003" + NB + "года', 'Сотрудничает"),
    (r"now: \['2003-cü ildən', 'Bu günədək Karvasarski", "now: ['2003-cü ildən', 'Karvasarski"),
    (r"now: \['Since 2003', 'To this day he works", "now: ['Since 2003', 'He works"),
]
for a, b in pairs:
    t = sub1(t, a, b, a[:50])
# условия краткосрочных программ — короткой строкой, которая не обрезается
t, n1 = re.subn(r"'3[  ]месяца \+ 6[  ]месяцев групповой супервизии'", "'3" + NB + "месяца + 6" + NB + "месяцев супервизии'", t)
t, n2 = re.subn(r"'3 ay \+ 6 ay qrup superviziyası'", "'3 ay + 6 ay superviziya'", t)
t, n3 = re.subn(r"'3 months \+ 6 months of group supervision'", "'3 months + 6 months of supervision'", t)
t, n4 = re.subn(r"'1[  ]год — 6\+6[  ]мес\.'", "'1" + NB + "год: 6 + 6" + NB + "месяцев'", t)
t, n5 = re.subn(r"'1 il — 6\+6 ay'", "'1 il: 6 + 6 ay'", t)
t, n6 = re.subn(r"'1 year — 6\+6 months'", "'1 year: 6 + 6 months'", t)
t, n7 = re.subn(r"более 100 — в[  ]этом\.'", "более 100 — в" + NB + "этом году.'", t)
t, n8 = re.subn(r"more: 'Более 3[  ]000 человек прошли тренинги лично у[  ]Кенана Рагимова\.'", "more: 'Ещё более 3" + NB + "000 прошли тренинги лично у" + NB + "Кенана Рагимова.'", t)
print('чипы и строки:', n1, n2, n3, n4, n5, n6, n7, n8)
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

# ── замер: закреплённые блоки не входят в проверку «до заголовка»
p = '_tools/round.py'
t = io.open(p, encoding='utf-8').read()
t = t.replace("!sec.matches('.sec--rib')", "!sec.matches('.sec--rib, .sec--bk')")
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('patched')
