"""Ноктюрн · корпоративная страница (Кенан 09.11.2026, ЦНС #811).

Темы тренингов (HR, менеджмент, тайм-менеджмент, лидерство, командная работа, стресс-менеджмент), хроника
Business Party by RAGIMOFF (архив старого сайта на Wix: 25.10.2015 «Коммуникация»; 20.12.2015 «Возможности развития
бизнеса в 2016 году»; 12.04.2016, Flame Towers — «İmkanlar Kainatı — Made in Azerbaijan»), форма корпоративного запроса
без оплаты: компания, контактное лицо, телефон, email (необяз.), темы кликами + «другое», цель, число участников, язык, формат.
"""
import html as H

YT_CHANNEL = 'https://www.youtube.com/@KRagimoff'   # канал Кенана (автор роликов сайта, oEmbed 09.11)

T = {
 'az': {
  'topics_eyebrow': 'Mövzular', 'topics_title': 'Korporativ təlimlər',
  'topics': [('HR və kadrların idarə olunması', 'Kadr seçimi, işçinin psixoloji portreti, motivasiya və saxlanma sistemi.'),
             ('Menecment bacarıqları', 'Rəhbər üçün idarəetmə alətləri: tapşırıq, nəzarət, əks-əlaqə, qərar qəbulu.'),
             ('Vaxtın idarə edilməsi', 'Prioritetlər, planlaşdırma və diqqətin qorunması — fərdi və komanda səviyyəsində.'),
             ('Liderlik', 'Böhran şəraitində liderlik, təsir və etibar, komandanı nəticəyə aparmaq.'),
             ('Komanda işi', 'Komanda dinamikası və rollar, münaqişələrin həlli, uyğunluq analizi.'),
             ('Stress-menecment', 'Tükənmənin qarşısının alınması, gərginlik altında sabit iş.')],
  'events_eyebrow': 'Tədbirlər', 'events_title': 'Business Party by RAGIMOFF',
  'events_lead': 'İş adamları üçün açıq tədbirlər: mövzu, ünsiyyət və yeni əlaqələr bir axşamda.',
  'events': [('25.10.2015', 'Business Party № 1', 'Kommunikasiya'),
             ('20.12.2015', 'Business Party № 2', '2016-cı ildə biznesin inkişaf imkanları'),
             ('12.04.2016 · Flame Towers', 'Business Party № 3', '«İmkanlar Kainatı — Made in Azerbaijan»')],
  'yt': 'Təlimlərdən videolar — YouTube kanalı',
  'form_eyebrow': 'Sifariş', 'form_title': 'Korporativ təlim sifariş edin',
  'form_lead': 'Bir neçə kliklə seçin — mütəxəssisimiz sizinlə əlaqə saxlayıb məqsədlərinizə uyğun korporativ proqram tərtib edəcək.',
  'company': 'Şirkət', 'person': 'Əlaqə şəxsi', 'phone': 'Telefon', 'email': 'E-poçt (istəyə görə)',
  'topic': 'Mövzu', 'other': 'Digər', 'other_ph': 'Qısaca: nə əldə etmək istəyirsiniz',
  'goal': 'Tədbirin məqsədi', 'goals': ['Komandanın inkişafı', 'Rəhbərlərin hazırlığı', 'Satışın artırılması', 'Stress və tükənmə', 'Korporativ tədbir'],
  'count': 'İştirakçı sayı', 'lang': 'Təlimin dili', 'langs': ['Azərbaycan', 'Rus', 'İngilis'],
  'format': 'Format', 'formats': ['Ofisinizdə', 'Onlayn', 'Səyahət / retrit'],
  'send': 'Sorğu göndər', 'sending': 'Göndərilir…',
  'ok': 'Sorğunuz göndərildi. Mütəxəssisimiz sizinlə əlaqə saxlayacaq və məqsədlərinizə uyğun proqram təklif edəcək.',
  'err': 'Göndərmək alınmadı. Zəhmət olmasa WhatsApp ilə yazın.', 'req': 'Bu sahəni doldurun',
 },
 'ru': {
  'topics_eyebrow': 'Темы', 'topics_title': 'Корпоративные тренинги',
  'topics': [('HR и управление персоналом', 'Подбор кадров, психологический портрет сотрудника, мотивация и удержание.'),
             ('Management skills', 'Инструменты руководителя: постановка задач, контроль, обратная связь, решения.'),
             ('Тайм-менеджмент', 'Приоритеты, планирование и защита внимания — лично и в команде.'),
             ('Leadership', 'Лидерство в кризисе, влияние и доверие, как вести команду к результату.'),
             ('Teamwork', 'Командная динамика и роли, разрешение конфликтов, анализ совместимости.'),
             ('Стресс-менеджмент', 'Профилактика выгорания, устойчивая работа под нагрузкой.')],
  'events_eyebrow': 'Мероприятия', 'events_title': 'Business Party by RAGIMOFF',
  'events_lead': 'Открытые мероприятия для предпринимателей: тема, общение и новые связи за один вечер.',
  'events': [('25.10.2015', 'Business Party № 1', 'Коммуникация'),
             ('20.12.2015', 'Business Party № 2', 'Возможности развития бизнеса в 2016 году'),
             ('12.04.2016 · Flame Towers', 'Business Party № 3', '«İmkanlar Kainatı — Made in Azerbaijan»')],
  'yt': 'Видео с тренингов — YouTube-канал',
  'form_eyebrow': 'Заказ', 'form_title': 'Заказать корпоративный тренинг',
  'form_lead': 'Выберите в несколько касаний — наш специалист свяжется с вами и поможет составить корпоративную программу под ваши цели.',
  'company': 'Компания', 'person': 'Контактное лицо', 'phone': 'Телефон', 'email': 'Email (необязательно)',
  'topic': 'Тема', 'other': 'Другое', 'other_ph': 'Коротко: что вы хотите получить',
  'goal': 'Цель мероприятия', 'goals': ['Развитие команды', 'Подготовка руководителей', 'Рост продаж', 'Стресс и выгорание', 'Корпоративное мероприятие'],
  'count': 'Количество участников', 'lang': 'Язык тренинга', 'langs': ['Азербайджанский', 'Русский', 'Английский'],
  'format': 'Формат', 'formats': ['В вашем офисе', 'Онлайн', 'Выездной / ретрит'],
  'send': 'Отправить запрос', 'sending': 'Отправка…',
  'ok': 'Запрос отправлен. Наш специалист свяжется с вами и предложит программу под ваши цели.',
  'err': 'Не удалось отправить. Пожалуйста, напишите в WhatsApp.', 'req': 'Заполните это поле',
 },
 'en': {
  'topics_eyebrow': 'Topics', 'topics_title': 'Corporate trainings',
  'topics': [('HR and people management', 'Recruitment, an employee’s psychological profile, motivation and retention.'),
             ('Management skills', 'A manager’s tools: setting tasks, control, feedback, decisions.'),
             ('Time management', 'Priorities, planning and protecting attention — personally and as a team.'),
             ('Leadership', 'Leading in a crisis, influence and trust, taking a team to results.'),
             ('Teamwork', 'Team dynamics and roles, resolving conflict, compatibility analysis.'),
             ('Stress management', 'Preventing burnout, working steadily under pressure.')],
  'events_eyebrow': 'Events', 'events_title': 'Business Party by RAGIMOFF',
  'events_lead': 'Open evenings for business people: a topic, conversation and new connections.',
  'events': [('25.10.2015', 'Business Party No. 1', 'Communication'),
             ('20.12.2015', 'Business Party No. 2', 'Business growth opportunities in 2016'),
             ('12.04.2016 · Flame Towers', 'Business Party No. 3', '“İmkanlar Kainatı — Made in Azerbaijan”')],
  'yt': 'Videos from the trainings — YouTube channel',
  'form_eyebrow': 'Request', 'form_title': 'Request a corporate training',
  'form_lead': 'Choose in a few taps — our specialist will contact you and help build a corporate programme for your goals.',
  'company': 'Company', 'person': 'Contact person', 'phone': 'Phone', 'email': 'Email (optional)',
  'topic': 'Topic', 'other': 'Other', 'other_ph': 'Briefly: what you want to achieve',
  'goal': 'Purpose of the event', 'goals': ['Team development', 'Training managers', 'Growing sales', 'Stress and burnout', 'Corporate event'],
  'count': 'Number of participants', 'lang': 'Language', 'langs': ['Azerbaijani', 'Russian', 'English'],
  'format': 'Format', 'formats': ['At your office', 'Online', 'Off-site / retreat'],
  'send': 'Send request', 'sending': 'Sending…',
  'ok': 'Request sent. Our specialist will contact you and propose a programme for your goals.',
  'err': 'Could not send. Please write to us on WhatsApp.', 'req': 'Please fill in this field',
 },
}


def chips(name, items, multi=False, first=True):
    typ = 'checkbox' if multi else 'radio'
    return ''.join('<label class="n-chip"><input type="%s" name="%s" value="%s"%s><span>%s</span></label>' % (
        typ, name, H.escape(v), ' checked' if (first and i == 0 and not multi) else '', H.escape(v)) for i, v in enumerate(items))


def sections(lang):
    t = T[lang]; e = H.escape
    topics = ''.join('<article class="card n-topic"><h3>%s</h3><p>%s</p></article>' % (e(a), e(b)) for a, b in t['topics'])
    events = ''.join('<li class="n-event"><span class="n-event-date">%s</span><h4>%s</h4><p>%s</p></li>' % (e(a), e(b), e(c)) for a, b, c in t['events'])
    topic_names = [a for a, _ in t['topics']] + [t['other']]
    form = ('<form class="n-form n-b2b" id="b2bForm" novalidate data-lang="%s" data-ok="%s" data-err="%s" data-sending="%s" data-req="%s">'
            '<div class="n-form-grid"><label><span>%s</span><input name="company" required autocomplete="organization"></label>'
            '<label><span>%s</span><input name="person" required autocomplete="name"></label>'
            '<label><span>%s</span><input name="telefon" type="tel" required autocomplete="tel" placeholder="+994"></label>'
            '<label><span>%s</span><input name="email" type="email" autocomplete="email"></label></div>'
            '<fieldset class="n-calc-row"><legend>%s</legend>%s</fieldset>'
            '<label class="n-form-wide" data-other hidden><span>%s</span><textarea name="offer" rows="2"></textarea></label>'
            '<fieldset class="n-calc-row"><legend>%s</legend>%s</fieldset>'
            '<div class="n-form-grid"><label><span>%s</span><input name="count" type="number" min="1" step="1" inputmode="numeric" required></label>'
            '<fieldset class="n-calc-row"><legend>%s</legend>%s</fieldset></div>'
            '<fieldset class="n-calc-row"><legend>%s</legend>%s</fieldset>'
            '<button class="n-btn" type="submit">%s</button><p class="n-form-msg" role="status" hidden></p></form>') % (
        lang, e(t['ok']), e(t['err']), e(t['sending']), e(t['req']),
        e(t['company']), e(t['person']), e(t['phone']), e(t['email']),
        e(t['topic']), chips('movzu', topic_names, multi=True), e(t['other_ph']),
        e(t['goal']), chips('meqsed', t['goals']), e(t['count']), e(t['lang']), chips('dil', t['langs']),
        e(t['format']), chips('format', t['formats']), e(t['send']))
    topics_sec = ('<section class="n-sec"><div class="n-wrap"><div class="n-sec-head"><div><span class="n-eyebrow">%s</span><h2 class="n-h2">%s</h2></div></div>'
                  '<div class="n-topics">%s</div><a class="n-doc-link n-yt" href="%s" target="_blank" rel="noopener">%s ↗</a></div></section>') % (
        e(t['topics_eyebrow']), e(t['topics_title']), topics, e(YT_CHANNEL), e(t['yt']))
    events_sec = ('<section class="n-sec n-sec-alt"><div class="n-wrap"><div class="n-sec-head"><div><span class="n-eyebrow">%s</span><h2 class="n-h2">%s</h2>'
                  '<p class="n-lead">%s</p></div></div><ol class="n-events">%s</ol></div></section>') % (
        e(t['events_eyebrow']), e(t['events_title']), e(t['events_lead']), events)
    form_sec = ('<section class="n-sec" id="order"><div class="n-wrap"><div class="n-sec-head"><div><span class="n-eyebrow">%s</span><h2 class="n-h2">%s</h2>'
                '<p class="n-lead">%s</p></div></div>%s</div></section>') % (e(t['form_eyebrow']), e(t['form_title']), e(t['form_lead']), form)
    return topics_sec, events_sec, form_sec
