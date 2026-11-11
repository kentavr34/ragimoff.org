# -*- coding: utf-8 -*-
"""Слова владельца 11.11 (вечер): все цены в манатах на всех языках; энурез — консультация 50, курс 500;
программа КПТ (24 занятия, заголовки); форма передаёт язык на страницу оплаты."""
import io, re, json, shutil, time, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ST = time.strftime('%m%d_%H%M')
def rd(p): return io.open(os.path.join(ROOT, p), encoding='utf-8').read()
def wr(p, s):
    os.makedirs(os.path.join(ROOT, '_agent/backup'), exist_ok=True)
    shutil.copy2(os.path.join(ROOT, p), os.path.join(ROOT, '_agent/backup', os.path.basename(p) + '.' + ST))
    io.open(os.path.join(ROOT, p), 'w', encoding='utf-8', newline='\n').write(s)
def rep(s, a, b, n=1):
    assert s.count(a) == n, 'ожидалось %d, найдено %d: %s' % (n, s.count(a), a[:80])
    return s.replace(a, b)
J = lambda o: json.dumps(o, ensure_ascii=False)

# ───────── 1. programs.js: манаты ─────────
p = rd('assets/js/programs.js')
AZN = [  # (полная, предоплата, скидка, 12 мес, 24 мес)
    ('4 200', '3 800', '400', '350', '200'), ('6 600', '6 000', '600', '550', '300'), ('3 600', '3 000', '600', '300', '175')]
def ru_price(a):
    return "rows: [['Полная стоимость', '%s AZN'], ['При полной оплате (−%s AZN)', '%s AZN'], ['Рассрочка 12 мес.', '%s AZN/мес.'], ['Рассрочка 24 мес.', '%s AZN/мес.']],\n          note: 'Рассрочка до 24 месяцев — от %s AZN в месяц.'" % (a[0], a[2], a[1], a[3], a[4], a[4])
def en_price(a):
    c = lambda x: x.replace(' ', ',')
    return "rows: [['Full price', '%s AZN'], ['Full payment (−%s AZN)', '%s AZN'], ['12-month instalment', '%s AZN/mo.'], ['24-month instalment', '%s AZN/mo.']],\n          note: 'Instalment plan up to 24 months — from %s AZN a month.'" % (c(a[0]), a[2], c(a[1]), a[3], a[4], a[4])
blocks = [m for m in re.finditer(r"rows: \[[^\n]*\],\n\s*note: '[^\n]*'", p) if ('руб' in m.group(0) or '$' in m.group(0))]
assert len(blocks) == 6, len(blocks)
out, last = [], 0
for i, m in enumerate(blocks):
    out.append(p[last:m.start()]); out.append((ru_price if i % 2 == 0 else en_price)(AZN[i // 2])); last = m.end()
out.append(p[last:]); p = ''.join(out)
assert 'руб' not in p and not re.search(r"\$\d", p)

# ───────── 2. programs.js: программа КПТ ─────────
CBT = {
 'ru': dict(
  title='Когнитивно-поведенческая терапия', lead='Основы когнитивно-поведенческой терапии (КПТ): модель, техники, протоколы и современные направления — с практикой на каждом занятии.',
  forWhom=['Психологи, психотерапевты и врачи', 'Студенты психологических факультетов и начинающие специалисты', 'Те, кто хочет освоить структурированный метод работы с тревогой и депрессией'],
  vol='48 часов: 2 занятия в неделю по 2 часа + 24 сессии супервизии', fmt='Очно или онлайн',
  includes=['24 занятия: теория, демонстрация и практика в парах', 'Рабочие бланки: дневник мыслей, концептуализация случая, иерархия экспозиции', '6 месяцев групповой супервизии на собственных случаях', 'Аттестация по завершении программы'],
  program=[
   {'t': 'Модуль 1 — Основы КПТ', 'items': ['История КПТ и три «волны». Когнитивная модель А. Бека и модель ABC А. Эллиса', 'Структура терапии и сессии. Терапевтический альянс, совместный эмпиризм', 'Когнитивная концептуализация случая', 'Оценка, цели, психообразование, план лечения']},
   {'t': 'Модуль 2 — Когнитивные техники', 'items': ['Автоматические мысли. Дневник мыслей', 'Когнитивные искажения. Сократовский диалог', 'Когнитивная реструктуризация. Промежуточные убеждения и правила', 'Глубинные убеждения. «Падающая стрела». Поведенческие эксперименты']},
   {'t': 'Модуль 3 — Поведенческие техники', 'items': ['Поведенческая активация и планирование активности', 'Экспозиция: принципы, иерархия, типичные ошибки', 'Навыки: решение проблем, ассертивность, релаксация и дыхание', 'Домашние задания, профилактика рецидива, завершение терапии']},
   {'t': 'Модуль 4 — Протоколы КПТ', 'items': ['Депрессия', 'Паническое расстройство и агорафобия', 'Социальная тревога и генерализованное тревожное расстройство', 'Обсессивно-компульсивное расстройство: экспозиция с предотвращением реакции', 'ПТСР: травма-фокусированная КПТ и пролонгированная экспозиция', 'Бессонница и расстройства пищевого поведения — обзор']},
   {'t': 'Модуль 5 — Современные направления', 'items': ['Рационально-эмотивно-поведенческая терапия А. Эллиса', 'Схема-терапия Дж. Янга', 'Терапия принятия и ответственности (ACT)', 'Диалектическая поведенческая терапия, терапия на основе осознанности, терапия, сфокусированная на сострадании']},
   {'t': 'Модуль 6 — Сравнение школ и интеграция', 'items': ['КПТ и другие школы: логотерапия, личностно-ориентированная (реконструктивная) психотерапия, клиент-центрированная терапия — в чём разница', 'Разбор случаев, итоговая аттестация, переход к супервизии']},
   {'t': 'Супервизия · 6 месяцев (1 раз в неделю)', 'items': ['Еженедельные супервизионные сессии на собственных случаях (материал анонимизируется, разбор — в группе) · 24 сессии']}]),
 'az': dict(
  title='Koqnitiv-davranış terapiyası', lead='Koqnitiv-davranış terapiyasının (KDT) əsasları: model, texnikalar, protokollar və müasir istiqamətlər — hər dərsdə praktika ilə.',
  forWhom=['Psixoloqlar, psixoterapevtlər və həkimlər', 'Psixologiya fakültələrinin tələbələri və fəaliyyətə yeni başlayan mütəxəssislər', 'Təşviş və depressiya ilə strukturlaşdırılmış iş metodunu mənimsəmək istəyənlər'],
  vol='48 saat: həftədə 2 dərs, hər biri 2 saat + 24 superviziya sessiyası', fmt='Əyani və ya onlayn',
  includes=['24 dərs: nəzəriyyə, nümayiş və cütlərdə praktika', 'İş blankları: fikir gündəliyi, hadisənin konseptuallaşdırılması, ekspozisiya iyerarxiyası', 'Öz hadisələriniz üzrə 6 ay qrup superviziyası', 'Proqramın sonunda attestasiya'],
  program=[
   {'t': 'Modul 1 — KDT-nin əsasları', 'items': ['KDT-nin tarixi və üç «dalğa». A. Bekin koqnitiv modeli və A. Ellisin ABC modeli', 'Terapiyanın və sessiyanın strukturu. Terapevtik alyans, birgə empirizm', 'Hadisənin koqnitiv konseptuallaşdırılması', 'Qiymətləndirmə, məqsədlər, psixoloji maarifləndirmə, müalicə planı']},
   {'t': 'Modul 2 — Koqnitiv texnikalar', 'items': ['Avtomatik fikirlər. Fikir gündəliyi', 'Koqnitiv təhriflər. Sokrat dialoqu', 'Koqnitiv restrukturizasiya. Aralıq inanclar və qaydalar', 'Dərin inanclar. «Düşən ox» texnikası. Davranış eksperimentləri']},
   {'t': 'Modul 3 — Davranış texnikaları', 'items': ['Davranış aktivasiyası və fəaliyyətin planlaşdırılması', 'Ekspozisiya: prinsiplər, iyerarxiya, tipik səhvlər', 'Bacarıqlar: problem həlli, assertivlik, relaksasiya və nəfəs', 'Ev tapşırıqları, residivin profilaktikası, terapiyanın tamamlanması']},
   {'t': 'Modul 4 — KDT protokolları', 'items': ['Depressiya', 'Panik pozuntusu və aqorafobiya', 'Sosial təşviş və generalizə olunmuş təşviş pozuntusu', 'Obsessiv-kompulsiv pozuntu: ekspozisiya və reaksiyanın qarşısının alınması', 'PTSP: travmaya fokuslanmış KDT və uzadılmış ekspozisiya', 'Yuxusuzluq və qida qəbulu pozuntuları — icmal']},
   {'t': 'Modul 5 — Müasir istiqamətlər', 'items': ['A. Ellisin rasional-emotiv-davranış terapiyası', 'C. Yanqın sxem-terapiyası', 'Qəbul və məsuliyyət terapiyası (ACT)', 'Dialektik davranış terapiyası, şüurluluğa əsaslanan terapiya, şəfqətə fokuslanmış terapiya']},
   {'t': 'Modul 6 — Məktəblərin müqayisəsi və inteqrasiya', 'items': ['KDT və digər məktəblər: loqoterapiya, şəxsiyyətə yönəlmiş (rekonstruktiv) psixoterapiya, kliyentə mərkəzləşmiş terapiya — fərq nədədir', 'Hadisələrin təhlili, yekun attestasiya, superviziyaya keçid']},
   {'t': 'Superviziya · 6 ay (həftədə 1 dəfə)', 'items': ['Öz hadisələriniz üzrə həftəlik superviziya sessiyaları (material anonimləşdirilir, təhlil qrupda aparılır) · 24 sessiya']}]),
 'en': dict(
  title='Cognitive Behavioural Therapy', lead='Foundations of cognitive behavioural therapy (CBT): the model, techniques, protocols and modern approaches — with practice in every class.',
  forWhom=['Psychologists, psychotherapists and physicians', 'Psychology students and early-career specialists', 'Those who want a structured method for working with anxiety and depression'],
  vol='48 hours: 2 classes a week, 2 hours each + 24 supervision sessions', fmt='In person or online',
  includes=['24 classes: theory, demonstration and practice in pairs', 'Worksheets: thought record, case conceptualisation, exposure hierarchy', '6 months of group supervision on your own cases', 'Assessment at the end of the programme'],
  program=[
   {'t': 'Module 1 — Foundations of CBT', 'items': ['History of CBT and its three “waves”. A. Beck’s cognitive model and A. Ellis’s ABC model', 'Structure of therapy and of a session. Therapeutic alliance, collaborative empiricism', 'Cognitive case conceptualisation', 'Assessment, goals, psychoeducation, treatment plan']},
   {'t': 'Module 2 — Cognitive techniques', 'items': ['Automatic thoughts. Thought record', 'Cognitive distortions. Socratic dialogue', 'Cognitive restructuring. Intermediate beliefs and rules', 'Core beliefs. The downward arrow. Behavioural experiments']},
   {'t': 'Module 3 — Behavioural techniques', 'items': ['Behavioural activation and activity scheduling', 'Exposure: principles, hierarchy, common mistakes', 'Skills: problem solving, assertiveness, relaxation and breathing', 'Homework, relapse prevention, ending therapy']},
   {'t': 'Module 4 — CBT protocols', 'items': ['Depression', 'Panic disorder and agoraphobia', 'Social anxiety and generalised anxiety disorder', 'Obsessive-compulsive disorder: exposure and response prevention', 'PTSD: trauma-focused CBT and prolonged exposure', 'Insomnia and eating disorders — an overview']},
   {'t': 'Module 5 — Modern approaches', 'items': ['A. Ellis’s rational emotive behaviour therapy', 'J. Young’s schema therapy', 'Acceptance and commitment therapy (ACT)', 'Dialectical behaviour therapy, mindfulness-based cognitive therapy, compassion-focused therapy']},
   {'t': 'Module 6 — Comparing schools and integration', 'items': ['CBT and other schools: logotherapy, personality-oriented (reconstructive) psychotherapy, client-centred therapy — what differs', 'Case reviews, final assessment, transition to supervision']},
   {'t': 'Supervision · 6 months (weekly)', 'items': ['Weekly supervision sessions on your own cases (material is anonymised and discussed in the group) · 24 sessions']}]),
}
i = p.index('    cbt: {'); j = p.index('psychoanalysis: {', i)
blk = p[i:j]
for l, c in CBT.items():
    a = blk.index('      %s: {' % l); b = min([x for x in [blk.find('      %s: {' % o, a + 5) for o in ('ru', 'az', 'en')] if x > a] + [len(blk)])
    seg = blk[a:b]
    seg = re.sub(r"title: '[^']*'", lambda m: 'title: ' + J(c['title']), seg, 1)
    seg = re.sub(r"lead: '[^']*'", lambda m: 'lead: ' + J(c['lead']), seg, 1)
    seg = rep(seg, 'forWhom: []', 'forWhom: ' + J(c['forWhom']))
    seg = rep(seg, 'includes: []', 'includes: ' + J(c['includes']))
    seg = rep(seg, 'program: []', 'program: ' + J(c['program']))
    rows = re.findall(r"\['[^']*', '[^']*'\]", seg[seg.index('facts:'):seg.index('includes:')])
    assert len(rows) == 5, rows
    lab = lambda r: re.match(r"\['([^']*)'", r).group(1)
    seg = rep(seg, rows[1], J([lab(rows[1]), c['vol']])); seg = rep(seg, rows[2], J([lab(rows[2]), c['fmt']]))
    blk = blk[:a] + seg + blk[b:]
p = p[:i] + blk + p[j:]
wr('assets/js/programs.js', p)

# ───────── 3. content.js: подписи энуреза ─────────
c = rd('assets/js/content.js')
if 'ENUREZ_1112' not in c:
    c += """
/* ── ENUREZ_1112: ночной энурез — своя цена (слово владельца 11.11): первичная консультация 50 AZN, курс лечения 500 AZN, ведёт Кенан Рагимов ── */
const ENU = {
  ru: { l: 'Что нужно', o: [['first', 'Первичная консультация'], ['course', 'Курс лечения']], sub: { first: 'первичная консультация · Кенан Рагимов', course: 'курс лечения · Кенан Рагимов' } },
  az: { l: 'Nə lazımdır', o: [['first', 'İlkin konsultasiya'], ['course', 'Müalicə kursu']], sub: { first: 'ilkin konsultasiya · Kənan Rəhimov', course: 'müalicə kursu · Kənan Rəhimov' } },
  en: { l: 'What you need', o: [['first', 'First consultation'], ['course', 'Treatment course']], sub: { first: 'first consultation · Kenan Ragimov', course: 'treatment course · Kenan Ragimov' } },
};
for (const l of Object.keys(ENU)) T[l].reg.enu = ENU[l];
"""
    wr('assets/js/content.js', c)

# ───────── 4. reg.js: энурез и язык страницы оплаты ─────────
r = rd('assets/js/reg.js')
if 'ENU_P' not in r:
    r = rep(r, "const PROG = [", "const ENU = 3, ENU_P = { first: 50, course: 500 };                                                    /* ночной энурез (тема № 4): слово владельца 11.11 */\nconst PROG = [")
    r = rep(r, "hours: 20, btopic:", "hours: 20, enu: 'first', btopic:")
    r = rep(r, "  if (st.kind === 'consult') return { main: RATE[who][st.fmt] + ' AZN', sub: r.perHour };",
               "  if (st.kind === 'consult' && st.topic === ENU) return { main: ENU_P[st.enu] + ' AZN', sub: r.enu.sub[st.enu] };\n  if (st.kind === 'consult') return { main: RATE[who][st.fmt] + ' AZN', sub: r.perHour };")
    r = rep(r, "  if (k === 'consult') body = who + fmt + row(r.topic, chips('topic', topics, st.topic)) + (",
               "  if (k === 'consult') body = row(r.topic, chips('topic', topics, st.topic)) + (st.topic === ENU ? row(r.enu.l, chips('enu', r.enu.o, st.enu)) : who + fmt) + (")
    r = rep(r, "  if (k === 'consult') { service = `consult|${st.who}|${st.fmt}`; const tp =", "  if (k === 'consult') { const en = st.topic === ENU; service = en ? 'consult|kenan|enurez-' + st.enu : `consult|${st.who}|${st.fmt}`; const tp =")
    r = rep(r, "note = [lab(r.who.o, st.who), lab(r.fmt.o, st.fmt), tp].join(' · '); }", "note = (en ? [lab(r.who.o, 'kenan'), tp, lab(r.enu.o, st.enu)] : [lab(r.who.o, st.who), lab(r.fmt.o, st.fmt), tp]).join(' · '); }")
    r = rep(r, "program: service, folder: reg.folder || '' };", "program: service, folder: reg.folder || '', lang };")
    wr('assets/js/reg.js', r)
print('готово')
