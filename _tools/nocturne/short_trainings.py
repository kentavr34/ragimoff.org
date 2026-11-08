"""Ноктюрн · страница «Краткосрочные тренинги» (Кенан 08.11.2026, ЦНС #712).

Канон: 4 направления (Психодиагностика, КПТ, Психоанализ, Семейная терапия); каждый цикл —
3 месяца обучения + 6 месяцев супервизии в группе (раз в неделю); 300 AZN/мес × 3 или 800 AZN предоплатой;
даты не указывать; порядок — сначала Психодиагностика, затем КПТ.
Индивидуальная практическая подготовка: минимум 20 ч; один специалист — онлайн 100, очно 150 AZN/ч;
оба — онлайн 150, очно 200 AZN/ч; в форме выбор специалиста, формата и часов, цена видна сразу.
Тексты — по словам Кенана (RU), AZ/EN — перевод; термины — как на сайте (superviziya, KDT, onlayn, əyani).
"""
import html as H

PAGE = 'telim/qisamuddetli.html'
PRICE_MONTH, PRICE_PREPAY, MONTHS, SUPERV = 300, 800, 3, 6
RATES = {'one': {'online': 100, 'offline': 150}, 'both': {'online': 150, 'offline': 200}}
MIN_HOURS = 20

T = {
 'az': {
  'nav': 'Qısamüddətli təlimlər', 'title': 'Qısamüddətli təlimlər', 'eyebrow': 'Təhsil',
  'lead': 'Dörd istiqamət. Hər biri — 3 ay təhsil və 6 ay qrupda superviziya: həftədə bir dəfə praktik dəstək.',
  'order': 'Təlimlər növbə ilə keçirilir: əvvəl Psixodiaqnostika, sonra Koqnitiv-davranış terapiyası.',
  'tracks': [('psixodiaqnostika', 'Psixodiaqnostika', 'Ümumi psixologiya, psixopatologiya və diaqnozun beynəlxalq standartlar (ÜST, XBT) üzrə əsaslandırılması.'),
             ('kdt', 'Koqnitiv-davranış terapiyası (KDT)', 'Koqnitiv-davranış terapiyasının əsasları və praktik tətbiqi.'),
             ('psixoanaliz', 'Psixoanaliz', 'Psixoanalitik nəzəriyyə və praktika.'),
             ('aile', 'Ailə terapiyası', 'Ailə və cütlüklərlə iş: nəzəriyyə və praktika.')],
  'r_study': 'Təhsil', 'v_study': '3 ay', 'r_sup': 'Superviziya', 'v_sup': '6 ay, qrupda, həftədə 1 dəfə',
  'r_month': 'Aylıq ödəniş', 'v_month': '300 AZN × 3 ay',
  't_prepay': 'Birdəfəlik ödəniş', 't_prepay_sub': '3 ay təhsil + 6 ay superviziya',
  'reg': 'Qeydiyyat', 'prog': 'Proqram',
  'pd_eyebrow': 'Psixodiaqnostika', 'pd_title': 'Proqram: üç ay',
  'months': [('1-ci ay', 'Ümumi psixologiya', 'Psixi funksiyalar anlayışı; müxtəlif psixi funksiyalar və onların ölçülmə metodları.'),
             ('2-ci ay', 'Psixopatologiya', 'Psixopatoloji simptomlar — diqqət, yaddaş və digər funksiyaların pozuntuları; klinik sindromlar.'),
             ('3-cü ay', 'XBT üzrə diaqnostika', '«Klinik Psixiatriya» dərsliyi əsasında: bölmələr, simptomlar, diaqnozun əsaslandırılması, diaqnostika və təsdiq metodları, tövsiyə olunan terapiya.')],
  'pd_foot': '3 ay təhsil + 6 ay qrupda superviziya.',
  'ind_eyebrow': 'Fərdi format', 'ind_title': 'Fərdi praktik hazırlıq',
  'ind_lead': 'Proqramı mütəxəssislə fərdi qaydada keçmək. Minimum 20 saat.',
  'spec': 'Mütəxəssis', 'sp_k': 'Kənan Rəhimov', 'sp_s': 'Samirə Rəhimova', 'sp_b': 'Hər iki mütəxəssis',
  'fmt': 'Format', 'f_on': 'Onlayn', 'f_off': 'Əyani', 'hours': 'Saat sayı', 'per_h': 'saat', 'total': 'Cəmi',
  'rates': 'Bir mütəxəssis: onlayn 100 AZN/saat, əyani 150 AZN/saat. Hər iki mütəxəssis: onlayn 150 AZN/saat, əyani 200 AZN/saat.',
  'form_eyebrow': 'Qeydiyyat', 'form_title': 'Təlimə yazılın',
  'f_name': 'Ad', 'f_last': 'Soyad', 'f_phone': 'Telefon', 'f_id': 'Şəxsiyyət vəsiqəsi (şəkil və ya PDF)',
  'f_choice': 'Təlim', 'f_ind': 'Fərdi praktik hazırlıq', 'f_pay': 'Ödəniş', 'f_pay_m': 'Aylıq — 300 AZN × 3', 'f_pay_p': 'Birdəfəlik — 800 AZN',
  'f_send': 'Qeydiyyatdan keç', 'f_sending': 'Göndərilir…',
  'f_ok': 'Müraciətiniz qəbul edildi. Ödəniş və qrup barədə sizinlə əlaqə saxlayacağıq.',
  'f_err': 'Göndərmək alınmadı. Zəhmət olmasa WhatsApp ilə yazın.', 'f_req': 'Bu sahəni doldurun',
 },
 'ru': {
  'nav': 'Краткосрочные тренинги', 'title': 'Краткосрочные тренинги', 'eyebrow': 'Обучение',
  'lead': 'Четыре направления. Каждое — 3 месяца обучения и 6 месяцев супервизии в группе: практическая поддержка раз в неделю.',
  'order': 'Тренинги идут по очереди: сначала Психодиагностика, затем Когнитивно-поведенческая терапия.',
  'tracks': [('psixodiaqnostika', 'Психодиагностика', 'Общая психология, психопатология и обоснование диагноза по международным стандартам (ВОЗ, МКБ).'),
             ('kdt', 'Когнитивно-поведенческая терапия (КПТ)', 'Основы когнитивно-поведенческой терапии и практическое применение.'),
             ('psixoanaliz', 'Психоанализ', 'Психоаналитическая теория и практика.'),
             ('aile', 'Семейная терапия', 'Работа с семьями и парами: теория и практика.')],
  'r_study': 'Обучение', 'v_study': '3 месяца', 'r_sup': 'Супервизия', 'v_sup': '6 месяцев, в группе, раз в неделю',
  'r_month': 'Помесячно', 'v_month': '300 AZN × 3 месяца',
  't_prepay': 'Единовременно', 't_prepay_sub': '3 месяца обучения + 6 месяцев супервизии',
  'reg': 'Регистрация', 'prog': 'Программа',
  'pd_eyebrow': 'Психодиагностика', 'pd_title': 'Программа: три месяца',
  'months': [('1-й месяц', 'Общая психология', 'Понятие о психических функциях; различные психические функции и методы их измерения.'),
             ('2-й месяц', 'Психопатология', 'Психопатологические симптомы — нарушения внимания, памяти и других функций; клинические синдромы.'),
             ('3-й месяц', 'Диагностика по МКБ', 'На основе учебника «Клиническая психиатрия»: разделы, симптомы, обоснование диагноза, методы диагностики и подтверждения, рекомендуемая терапия.')],
  'pd_foot': '3 месяца обучения + 6 месяцев супервизии в группе.',
  'ind_eyebrow': 'Индивидуально', 'ind_title': 'Индивидуальная практическая подготовка',
  'ind_lead': 'Программа со специалистом в индивидуальном порядке. Минимум 20 часов.',
  'spec': 'Специалист', 'sp_k': 'Кенан Рагимов', 'sp_s': 'Самира Рагимова', 'sp_b': 'Оба специалиста',
  'fmt': 'Формат', 'f_on': 'Онлайн', 'f_off': 'Очно', 'hours': 'Количество часов', 'per_h': 'ч', 'total': 'Итого',
  'rates': 'Один специалист: онлайн 100 AZN/час, очно 150 AZN/час. Оба специалиста: онлайн 150 AZN/час, очно 200 AZN/час.',
  'form_eyebrow': 'Регистрация', 'form_title': 'Запись на тренинг',
  'f_name': 'Имя', 'f_last': 'Фамилия', 'f_phone': 'Телефон', 'f_id': 'Удостоверение личности (фото или PDF)',
  'f_choice': 'Тренинг', 'f_ind': 'Индивидуальная практическая подготовка', 'f_pay': 'Оплата', 'f_pay_m': 'Помесячно — 300 AZN × 3', 'f_pay_p': 'Единовременно — 800 AZN',
  'f_send': 'Зарегистрироваться', 'f_sending': 'Отправка…',
  'f_ok': 'Заявка принята. Мы свяжемся с вами по оплате и группе.',
  'f_err': 'Не удалось отправить. Пожалуйста, напишите в WhatsApp.', 'f_req': 'Заполните это поле',
 },
 'en': {
  'nav': 'Short-term trainings', 'title': 'Short-term trainings', 'eyebrow': 'Education',
  'lead': 'Four tracks. Each is 3 months of training and 6 months of group supervision — practical support once a week.',
  'order': 'The trainings run in turn: Psychodiagnostics first, then Cognitive Behavioural Therapy.',
  'tracks': [('psixodiaqnostika', 'Psychodiagnostics', 'General psychology, psychopathology and justifying a diagnosis by international standards (WHO, ICD).'),
             ('kdt', 'Cognitive Behavioural Therapy (CBT)', 'Foundations of cognitive behavioural therapy and its practical use.'),
             ('psixoanaliz', 'Psychoanalysis', 'Psychoanalytic theory and practice.'),
             ('aile', 'Family therapy', 'Working with families and couples: theory and practice.')],
  'r_study': 'Training', 'v_study': '3 months', 'r_sup': 'Supervision', 'v_sup': '6 months, in a group, once a week',
  'r_month': 'Monthly', 'v_month': '300 AZN × 3 months',
  't_prepay': 'Paid at once', 't_prepay_sub': '3 months of training + 6 months of supervision',
  'reg': 'Register', 'prog': 'Programme',
  'pd_eyebrow': 'Psychodiagnostics', 'pd_title': 'Programme: three months',
  'months': [('Month 1', 'General psychology', 'The concept of mental functions; the different mental functions and how they are measured.'),
             ('Month 2', 'Psychopathology', 'Psychopathological symptoms — disorders of attention, memory and other functions; clinical syndromes.'),
             ('Month 3', 'Diagnosis by ICD', 'Based on the textbook “Clinical Psychiatry”: chapters, symptoms, justifying the diagnosis, methods of diagnosis and confirmation, recommended therapy.')],
  'pd_foot': '3 months of training + 6 months of group supervision.',
  'ind_eyebrow': 'One-to-one', 'ind_title': 'Individual practical training',
  'ind_lead': 'The programme with a specialist, one-to-one. Minimum 20 hours.',
  'spec': 'Specialist', 'sp_k': 'Kenan Ragimov', 'sp_s': 'Samira Rahimova', 'sp_b': 'Both specialists',
  'fmt': 'Format', 'f_on': 'Online', 'f_off': 'In person', 'hours': 'Hours', 'per_h': 'h', 'total': 'Total',
  'rates': 'One specialist: online 100 AZN/hour, in person 150 AZN/hour. Both specialists: online 150 AZN/hour, in person 200 AZN/hour.',
  'form_eyebrow': 'Registration', 'form_title': 'Sign up for a training',
  'f_name': 'First name', 'f_last': 'Last name', 'f_phone': 'Phone', 'f_id': 'ID document (photo or PDF)',
  'f_choice': 'Training', 'f_ind': 'Individual practical training', 'f_pay': 'Payment', 'f_pay_m': 'Monthly — 300 AZN × 3', 'f_pay_p': 'At once — 800 AZN',
  'f_send': 'Register', 'f_sending': 'Sending…',
  'f_ok': 'Your application has been received. We will contact you about payment and the group.',
  'f_err': 'Could not send. Please write to us on WhatsApp.', 'f_req': 'Please fill in this field',
 },
}

PROG_LINK = {'psixodiaqnostika': 'program-psixodiaqnostika.html', 'psixoanaliz': 'program-psixoanaliz.html', 'aile': 'samira.html'}


def calc_html(t, prefix):
    """Калькулятор индивидуальной подготовки: специалист × формат × часы → цена сразу."""
    e = H.escape
    return ('<div class="n-calc" data-calc data-rates=\'{"one":{"online":100,"offline":150},"both":{"online":150,"offline":200}}\' data-min="%d">'
            '<fieldset class="n-calc-row"><legend>%s</legend>'
            '<label class="n-chip"><input type="radio" name="%smutexessis" value="kenan" checked><span>%s</span></label>'
            '<label class="n-chip"><input type="radio" name="%smutexessis" value="samira"><span>%s</span></label>'
            '<label class="n-chip"><input type="radio" name="%smutexessis" value="both"><span>%s</span></label></fieldset>'
            '<fieldset class="n-calc-row"><legend>%s</legend>'
            '<label class="n-chip"><input type="radio" name="%sformat" value="online" checked><span>%s</span></label>'
            '<label class="n-chip"><input type="radio" name="%sformat" value="offline"><span>%s</span></label></fieldset>'
            '<label class="n-calc-row n-calc-hours"><span class="n-calc-lbl">%s</span>'
            '<input type="number" name="%ssaat" min="%d" step="1" value="%d" inputmode="numeric"></label>'
            '<div class="n-calc-out"><span class="n-calc-rate" data-rate></span><span class="n-calc-total"><small>%s</small><b data-total></b></span></div>'
            '</div>') % (MIN_HOURS, e(t['spec']), prefix, e(t['sp_k']), prefix, e(t['sp_s']), prefix, e(t['sp_b']),
                         e(t['fmt']), prefix, e(t['f_on']), prefix, e(t['f_off']), e(t['hours']), prefix, MIN_HOURS, MIN_HOURS, e(t['total']))


def page_main(lang, new_page, rel, MAP, hero):
    t = T[lang]; e = H.escape
    cards = []
    for code, name, desc in t['tracks']:
        prog = ''
        if code in PROG_LINK:
            prog = '<a class="btn btn-line" href="%s">%s</a>' % (e(rel(new_page, lang + '/' + MAP[PROG_LINK[code]])), e(t['prog']))
        cards.append(
            '<article class="price-card n-short-card" id="t-%s"><div class="price-card-head"><h3>%s</h3></div>'
            '<p class="price-card-desc">%s</p>'
            '<div class="price-row"><span>%s</span><span>%s</span></div>'
            '<div class="price-row"><span>%s</span><span>%s</span></div>'
            '<div class="price-row"><span>%s</span><span>%s</span></div>'
            '<div class="price-total"><span>%s<small>%s</small></span><b>%d AZN</b></div>'
            '<a class="btn btn-fill" href="#qeydiyyat" data-pick="%s">%s</a>%s</article>' % (
                code, e(name), e(desc), e(t['r_study']), e(t['v_study']), e(t['r_sup']), e(t['v_sup']),
                e(t['r_month']), e(t['v_month']), e(t['t_prepay']), e(t['t_prepay_sub']), PRICE_PREPAY, code, e(t['reg']), prog))
    months = ''.join('<li class="n-month"><span class="n-month-n">%s</span><div><h4>%s</h4><p>%s</p></div></li>' % (e(a), e(b), e(c)) for a, b, c in t['months'])
    radios = ''.join('<label class="n-chip"><input type="radio" name="proqram" value="short-%s"%s><span>%s</span></label>' % (c, ' checked' if i == 0 else '', e(n))
                     for i, (c, n, _) in enumerate(t['tracks']))
    radios += '<label class="n-chip"><input type="radio" name="proqram" value="individual"><span>%s</span></label>' % e(t['f_ind'])
    form = ('<form class="n-form" id="shortForm" novalidate data-ok="%s" data-err="%s" data-sending="%s" data-req="%s" data-lang="%s">'
            '<div class="n-form-grid"><label><span>%s</span><input name="ad" required autocomplete="given-name"></label>'
            '<label><span>%s</span><input name="soyad" required autocomplete="family-name"></label>'
            '<label><span>%s</span><input name="telefon" type="tel" required autocomplete="tel" placeholder="+994"></label>'
            '<label><span>%s</span><input name="shexsiyyet" type="file" accept="image/*,.pdf" required></label></div>'
            '<fieldset class="n-calc-row"><legend>%s</legend>%s</fieldset>'
            '<div class="n-form-group" data-for="short"><fieldset class="n-calc-row"><legend>%s</legend>'
            '<label class="n-chip"><input type="radio" name="odenis" value="monthly" checked><span>%s</span></label>'
            '<label class="n-chip"><input type="radio" name="odenis" value="prepay"><span>%s</span></label></fieldset></div>'
            '<div class="n-form-group" data-for="individual" hidden>%s</div>'
            '<button class="n-btn" type="submit">%s</button><p class="n-form-msg" role="status" hidden></p></form>') % (
                e(t['f_ok']), e(t['f_err']), e(t['f_sending']), e(t['f_req']), lang,
                e(t['f_name']), e(t['f_last']), e(t['f_phone']), e(t['f_id']), e(t['f_choice']), radios,
                e(t['f_pay']), e(t['f_pay_m']), e(t['f_pay_p']), calc_html(t, 'f_'), e(t['f_send']))
    body = '''<section class="n-sec"><div class="n-wrap">
<p class="n-short-order">%s</p>
<div class="n-short-grid">%s</div>
</div></section>
<section class="n-sec n-sec-alt"><div class="n-wrap">
<div class="n-sec-head"><div><span class="n-eyebrow">%s</span><h2 class="n-h2">%s</h2></div></div>
<ol class="n-months">%s</ol>
<p class="n-short-foot">%s</p>
</div></section>
<section class="n-sec"><div class="n-wrap n-ind">
<div class="n-sec-head"><div><span class="n-eyebrow">%s</span><h2 class="n-h2">%s</h2><p class="n-lead">%s</p></div></div>
<div class="n-ind-box">%s<p class="n-ind-rates">%s</p></div>
</div></section>
<section class="n-sec n-sec-alt" id="qeydiyyat"><div class="n-wrap">
<div class="n-sec-head"><div><span class="n-eyebrow">%s</span><h2 class="n-h2">%s</h2></div></div>
%s
</div></section>''' % (e(t['order']), ''.join(cards), e(t['pd_eyebrow']), e(t['pd_title']), months, e(t['pd_foot']),
                       e(t['ind_eyebrow']), e(t['ind_title']), e(t['ind_lead']), calc_html(t, 'c_'), e(t['rates']),
                       e(t['form_eyebrow']), e(t['form_title']), form)
    return hero + body
