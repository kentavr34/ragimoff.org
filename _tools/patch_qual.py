"""Блок после специалистов: «Квалификация» — четыре одинаковых модуля в одну линию, без номеров (слова владельца 11.11). Запуск из test/11."""
import io, re

p = 'assets/js/site.js'
t = io.open(p, encoding='utf-8').read()
a = t.index("  const ld = t.spec.lead; $('#lead').innerHTML = ld ?")
b = t.index("\n", a)
t = t[:a] + "  const ld = t.spec.lead; $('#lead').innerHTML = ld ? `<h3 class=\"lead__h\">${esc(ld.h)}</h3><div class=\"lead__g\">${ld.items.map(x => `<div class=\"qual\"><b>${esc(x[0])}</b><span>${esc(x[1])}</span></div>`).join('')}</div>` : '';" + t[b:]
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

p = 'assets/js/content.js'
t = io.open(p, encoding='utf-8').read()
NB = ' '
QUAL = {
    'ru': "lead: { h: 'Квалификация', items: [['2001–2003', 'Кенан Рагимов получил образование по" + NB + "психотерапии в" + NB + "Институте имени В." + NB + "М." + NB + "Бехтерева.'], ['Руководитель', 'Профессор Б." + NB + "Д." + NB + "Карвасарский — главный психотерапевт Министерства здравоохранения Российской Федерации до" + NB + "2012" + NB + "года.'], ['Руководитель', 'Профессор В." + NB + "Д." + NB + "Вид — первый в" + NB + "странах СНГ психоаналитик, официально дипломированный Международной психоаналитической ассоциацией.'], ['С" + NB + "2003" + NB + "года', 'Сотрудничает с" + NB + "Институтом имени Б." + NB + "Д." + NB + "Карвасарского и" + NB + "Санкт-Петербургским институтом дополнительного профессионального образования: преподаёт и" + NB + "входит в" + NB + "аттестационную комиссию.']] },",
    'az': "lead: { h: 'Kvalifikasiya', items: [['2001–2003', 'Kənan Rəhimov V." + NB + "M." + NB + "Bexterev adına İnstitutda psixoterapiya üzrə təhsil alıb.'], ['Rəhbəri', 'Professor B." + NB + "D." + NB + "Karvasarski — 2012-ci ilədək Rusiya Federasiyası Səhiyyə Nazirliyinin baş psixoterapevti.'], ['Rəhbəri', 'Professor V." + NB + "D." + NB + "Vid — MDB ölkələrində Beynəlxalq Psixoanaliz Assosiasiyasının rəsmi diplomunu almış ilk psixoanalitik.'], ['2003-cü ildən', 'B." + NB + "D." + NB + "Karvasarski adına İnstitut və Sankt-Peterburq Əlavə Təhsil İnstitutu ilə əməkdaşlıq edir, tədris aparır və attestasiya komissiyasının üzvüdür.']] },",
    'en': "lead: { h: 'Qualifications', items: [['2001–2003', 'Kenan Ragimov trained in psychotherapy at the V." + NB + "M." + NB + "Bekhterev Institute.'], ['Supervisor', 'Professor B." + NB + "D." + NB + "Karvasarsky — chief psychotherapist of the Ministry of Health of the Russian Federation until 2012.'], ['Supervisor', 'Professor V." + NB + "D." + NB + "Vid — the first psychoanalyst in the CIS countries officially certified by the International Psychoanalytical Association.'], ['Since 2003', 'He works with the B." + NB + "D." + NB + "Karvasarsky Institute and the Saint Petersburg Institute of Continuing Professional Education: he teaches and sits on the attestation commission.']] },",
}
hits = list(re.finditer(r"lead: \{ h: .*?now: \[.*?\] \},", t, re.S))
if len(hits) != 3:
    raise SystemExit('ожидалось три блока lead, найдено %d' % len(hits))
for m, l in reversed(list(zip(hits, ['ru', 'az', 'en']))):
    t = t[:m.start()] + QUAL[l] + t[m.end():]
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

CSS = """
/* ═══ квалификация: четыре одинаковых модуля в одну линию, текст по одной вертикали (владелец, 11.11) ═══ */
.lead { max-width: none; padding-left: 0; border-left: 0; margin-top: var(--r4); }
.lead__h { text-align: left; margin-bottom: var(--r1); }
.lead__g { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: var(--r2); }
.qual { display: flex; flex-direction: column; gap: var(--s2); padding-left: var(--r1); border-left: 2px solid var(--gold); }
.qual b { font: 400 clamp(21px, 1.7vw, 26px)/1.15 var(--f-display); color: var(--gold-hi); font-variant-numeric: lining-nums; }
.qual span { font: 400 17px/1.55 var(--f-read); color: var(--text); text-wrap: pretty; }
@media (max-width: 1100px) { .lead__g { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 760px) { .lead { margin-top: var(--r3); padding-left: 0; } .lead__g { grid-template-columns: 1fr; gap: var(--r1); } .qual { padding-left: var(--r1); } .qual b { font-size: 21px; } }
"""
p = 'assets/css/site.css'
c = io.open(p, encoding='utf-8').read()
if 'квалификация: четыре одинаковых модуля' not in c:
    io.open(p, 'w', encoding='utf-8', newline='\n').write(c + CSS)

p = '_agent/docs/КАНОН_ГЛАВНАЯ.md'
t = io.open(p, encoding='utf-8').read()
t += "- 14.19 [К] Блок после специалистов называется «Квалификация» (отменяет «Руководители» в 14.1): четыре одинаковых модуля одного формата, без номеров, текст по одной вертикальной линии, на компьютере — в один ряд равной ширины, высота текста примерно одинаковая. Порядок: 1) 2001–2003 — образование по психотерапии в Институте имени В. М. Бехтерева; 2) руководитель — профессор Б. Д. Карвасарский; 3) руководитель — профессор В. Д. Вид; 4) с 2003 года — сотрудничество с Институтом имени Б. Д. Карвасарского и Институтом ДПО Санкт-Петербурга, преподаёт и входит в аттестационную комиссию. Азербайджанский текст — дословно по словам владельца. С+Т\n"
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('patched')
