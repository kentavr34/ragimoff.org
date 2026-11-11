"""Замечания владельца 11.11 (ночь): зазоры в шапке на компьютере, фото героя выше, одинаковый масштаб лиц специалистов,
подзаголовки крупнее, блок тренингов списком, соцсети вместо большой плашки Telegram, обложка «Общей психотерапии». Запуск из test/11."""
import io, re, shutil, pathlib

for f in ('index.html', 'assets/js/site.js', 'assets/css/site.css', 'assets/js/content.js'):
    shutil.copy(f, '_agent/backup/' + pathlib.Path(f).name + '.bak-owner1111f')


def edit(path, pairs):
    t = io.open(path, encoding='utf-8').read()
    for a, b in pairs:
        if a not in t:
            raise SystemExit('НЕ НАЙДЕНО в %s: %s' % (path, a[:90]))
        t = t.replace(a, b, 1)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(t)


t = io.open('index.html', encoding='utf-8').read()
m = re.search(r'  <section class="sec" id="corp">.*?</section>\n', t, re.S)
if not m:
    raise SystemExit('секция тренингов не найдена')
t = t[:m.start()] + '  <section class="sec" id="corp"><div class="wrap"><header class="sh" data-h="corp"></header><div class="lead__g lead__g--3 rv" id="corpList"></div><div class="vids" id="corpVids"></div><p class="sec__more rv"><a class="btn btn--line" id="corpBtn"></a></p></div></section>\n' + t[m.end():]
m = re.search(r'  <section class="sec sec--tg" id="tg">.*?</section>\n', t, re.S)
if not m:
    raise SystemExit('секция Telegram не найдена')
t = t[:m.start()] + '  <section class="sec sec--soc" id="tg"><div class="wrap"><div class="soc rv"><p class="soc__h" data-i="soc.h"></p><ul class="soc__l" id="socList"></ul></div></div></section>\n' + t[m.end():]
io.open('index.html', 'w', encoding='utf-8', newline='\n').write(t)

t = io.open('assets/js/site.js', encoding='utf-8').read()
# тренинги: список вместо лида, плиток и меток
t, n = re.subn(r"  \$\('#corpTags'\)\.innerHTML = [^\n]*\n", "", t)
t, n2 = re.subn(r"  \$\('#corpClients'\)\.innerHTML = [^\n]*\n", "  $('#corpList').innerHTML = (t.corp.list || []).map(x => `<div class=\"qual\"><b>${esc(x[0])}</b><span>${esc(x[1])}</span></div>`).join('');\n", t)
t, n3 = re.subn(r"  \$\('#tgBtn'\)\.href = L\.tg;", "  $('#socList').innerHTML = (t.soc.l || []).map((x, i) => `<li><a href=\"${L.soc[i]}\" target=\"_blank\" rel=\"noopener\">${esc(x)}</a></li>`).join('');", t)
t, n4 = re.subn(r"\{ b: t\.books\.soon, href: L\.shop, img: '' \}", "{ b: t.books.soon, href: L.shop, img: `assets/img/book-therapy-${lang}.jpg` }", t)
print('site.js замены:', n, n2, n3, n4)
if not (n2 and n3 and n4):
    raise SystemExit('site.js: не все места найдены')
io.open('assets/js/site.js', 'w', encoding='utf-8', newline='\n').write(t)

CSS = """
/* ═══ замечания владельца 11.11 (ночь) ═══ */
/* шапка на компьютере: между темой, языком и «Записаться» — нормальные зазоры */
@media (min-width: 1181px) { .head__r { gap: var(--p20); } }
@media (min-width: 1181px) and (max-width: 1500px) { .head__r { gap: var(--p14); } .nav__l { padding: 0 var(--p8); } }
/* фото героя на компьютере — выше (тёмная полоса над головой меньше); телефон не меняется */
@media (min-width: 761px) { :root { --hero-top: 64px; } }
/* специалисты: лица одного масштаба */
.person:nth-child(1) .person__ph img { transform: translateY(var(--py, 0)) scale(1.2); transform-origin: 46% 30%; }
/* подзаголовок раздела — заметный, а не «примечание мелким шрифтом» */
.sh__s { font-size: clamp(19px, 1.55vw, 23px); line-height: 1.5; color: var(--milk); opacity: .9; }
@media (max-width: 760px) { .sh__s { font-size: 18px; line-height: 1.45; } }
/* тренинги: три одинаковых модуля, как «Квалификация» */
.lead__g--3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
@media (max-width: 1100px) { .lead__g--3 { grid-template-columns: 1fr; gap: var(--r1); } }
/* соцсети: тонкая строка вместо большой плашки */
.sec--soc { padding-bottom: var(--hs); }
.soc { display: flex; align-items: center; justify-content: space-between; gap: var(--r2); padding: var(--r1) 0; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); }
.soc__h { font: 400 clamp(21px, 1.8vw, 27px)/1.2 var(--f-display); color: var(--milk); }
.soc__l { display: flex; flex-wrap: wrap; gap: var(--s2); }
.soc__l a { display: inline-flex; align-items: center; min-height: var(--tap); padding: 0 var(--p20); border-radius: 99px; border: 1px solid color-mix(in srgb, var(--gold) 55%, transparent); color: var(--milk); font: 600 15px/1 var(--f-sub); transition: background var(--t1), color var(--t1); }
.soc__l a:hover { background: var(--gold); color: var(--on-gold); }
@media (max-width: 760px) { .soc { flex-direction: column; align-items: flex-start; gap: var(--s3); } }
/* книга без обложки-заглушки больше нет: у всех шести — настоящая обложка */
"""
p = 'assets/css/site.css'
c = io.open(p, encoding='utf-8').read()
if 'замечания владельца 11.11 (ночь)' not in c:
    io.open(p, 'w', encoding='utf-8', newline='\n').write(c + CSS)

p = 'assets/js/content.js'
t = io.open(p, encoding='utf-8').read()
if 'OWNER_1111F' not in t:
    NB = '\\u00a0'
    t += """
/* ── OWNER_1111F: тренинги списком и соцсети (слова владельца 11.11, ночь) ── */
const OWN2 = {
  ru: { list: [['Школа HR', 'Работает с""" + NB + """2008""" + NB + """года и""" + NB + """подготовила более 2""" + NB + """000""" + NB + """человек.'],
               ['Тренинги', 'Более 3""" + NB + """000""" + NB + """человек прошли тренинги лично у""" + NB + """Кенана Рагимова: управление персоналом, лидерство, командная работа, коммуникации и""" + NB + """продажи.'],
               ['Мероприятия для бизнеса', 'Корпоративные тренинги и""" + NB + """деловые встречи для компаний MG, Unibank, DNS""" + NB + """Computers и""" + NB + """серия Business Party by Ragimoff.']],
        soc: { h: 'Следите за""" + NB + """нами в""" + NB + """социальных сетях', l: ['Telegram', 'Instagram', 'YouTube', 'Facebook'] } },
  az: { list: [['HR məktəbi', '2008-ci ildən fəaliyyət göstərir və 2""" + NB + """000-dən çox nəfər hazırlayıb.'],
               ['Təlimlər', '3""" + NB + """000-dən çox insan Kənan Rəhimovun şəxsən keçirdiyi təlimlərdə iştirak edib: heyətin idarə olunması, liderlik, komanda işi, ünsiyyət və satış.'],
               ['Biznes üçün tədbirlər', 'MG, Unibank, DNS Computers şirkətləri üçün korporativ təlimlər və işgüzar görüşlər, Business Party by Ragimoff silsiləsi.']],
        soc: { h: 'Bizi sosial şəbəkələrdə izləyin', l: ['Telegram', 'Instagram', 'YouTube', 'Facebook'] } },
  en: { list: [['HR School', 'Working since 2008; it has trained more than 2,000 people.'],
               ['Training', 'More than 3,000 people have attended trainings led by Kenan Ragimov in person: people management, leadership, teamwork, communication and sales.'],
               ['Events for business', 'Corporate trainings and business meetings for MG, Unibank and DNS Computers, and the Business Party by Ragimoff series.']],
        soc: { h: 'Follow us on social media', l: ['Telegram', 'Instagram', 'YouTube', 'Facebook'] } },
};
for (const l of Object.keys(OWN2)) { T[l].corp.list = OWN2[l].list; T[l].soc = OWN2[l].soc; }
const _LINKS0 = LINKS;
export function LINKS2(l) { const L = _LINKS0(l); L.soc = [L.tg, 'https://www.instagram.com/dr.ragimoff', 'https://youtube.com/@kragimoff', 'https://www.facebook.com/Ragimoff.az']; return L; }
"""
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

# site.js берёт ссылки через LINKS2 (с соцсетями)
p = 'assets/js/site.js'
t = io.open(p, encoding='utf-8').read()
t2 = re.sub(r"import \{ T, LINKS \} from '(\./content\.js[^']*)';", r"import { T, LINKS2 as LINKS } from '\1';", t, count=1)
if t2 == t:
    raise SystemExit('site.js: импорт LINKS не найден')
io.open(p, 'w', encoding='utf-8', newline='\n').write(t2)
print('patched')
