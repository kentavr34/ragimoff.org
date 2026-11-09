"""Ноктюрн · единый лендинг программы обучения (Кенан 09.11.2026, ЦНС #811).

Одна схема для всех программ, разные пруфы:
  первый экран → ключевые факты → [что это] → короткий блок специалиста → программа → [что ждёт / кому] →
  документ (диплом института или сертификат IPAS) → цена (та же карточка, что на главной) → форма → вопросы.
Документы: Ümumi и Klinik psixologiya — диплом Санкт-Петербургского института ДПО (education-psy.ru);
Практикум, психоанализ, психодиагностика, семейная терапия, краткосрочные — сертификат IPAS (intpas.com, проверка по QR).
"""
import html as H

INSTITUTE_URL = 'https://education-psy.ru/'
IPAS_URL = 'https://intpas.com/'

PROGRAMS = {   # исходная страница → документ, специалист
    'program-umumi.html': {'doc': 'inst', 'who': 'haqqimda.html'},
    'program-klinik.html': {'doc': 'inst', 'who': 'haqqimda.html'},
    'program-praktikum.html': {'doc': 'ipas', 'who': 'haqqimda.html'},
    'program-psixoanaliz.html': {'doc': 'ipas', 'who': 'haqqimda.html'},
    'program-psixodiaqnostika.html': {'doc': 'ipas', 'who': 'haqqimda.html'},
    'samira.html': {'doc': 'ipas', 'who': 'samira.html'},
}
PHOTO = {'haqqimda.html': 'images/kenan/photo-hero-suit.jpg', 'samira.html': 'images/samira/samira-portret.jpg'}

T = {
 'az': {
  'who': 'Təlimi aparır', 'more': 'Mütəxəssis haqqında',
  'facts': 'Qısaca',
  'inst_eyebrow': 'Sənəd', 'inst_title': 'Sankt-Peterburq Əlavə Peşə Təhsili İnstitutunun diplomu',
  'inst_text': 'Peşəkar yenidənhazırlanma proqramı institutun rəhbərliyi tərəfindən təsdiq edilib. Dr. Rəhimovun rəhbərliyi ilə təhsil alan tələbələr institutun diplomunu alırlar; diplom FİS FRDO dövlət reyestrinə daxil edilir.',
  'inst_link': 'İnstitut haqqında ətraflı — tədris heyəti, lisenziya, digər proqramlar',
  'inst_cap': ['Diplom nümunəsi', 'Diploma əlavə', 'Təhsil lisenziyası'],
  'ipas_eyebrow': 'Sənəd', 'ipas_title': 'Beynəlxalq Psixoterapiya Assosiasiyasının (IPAS) sertifikatı',
  'ipas_text': 'Proqramı RAGIMOFF keçirir; uğurla bitirən iştirakçılar International Psychotherapy Association sertifikatını alır. Sertifikatın həqiqiliyini üzərindəki QR-kodla və ya assosiasiyanın saytında yoxlamaq olar.',
  'ipas_link': 'Sertifikatı assosiasiyanın saytında yoxlayın — intpas.com',
  'ipas_cap': ['Sertifikat nümunəsi'],
  'price': 'Qiymət', 'price_t': 'Təhsil haqqı',
  'pd_months': 'Proqram: üç ay',
 },
 'ru': {
  'who': 'Ведёт обучение', 'more': 'О специалисте',
  'facts': 'Коротко',
  'inst_eyebrow': 'Документ', 'inst_title': 'Диплом Санкт-Петербургского института дополнительного профессионального образования',
  'inst_text': 'Программа профессиональной переподготовки утверждена руководством института. Студенты, прошедшие обучение под руководством доктора Рагимова, получают диплом института; сведения о дипломе вносятся в государственный реестр ФИС ФРДО.',
  'inst_link': 'Подробнее об институте — преподаватели, лицензия, другие программы',
  'inst_cap': ['Образец диплома', 'Приложение к диплому', 'Лицензия на образовательную деятельность'],
  'ipas_eyebrow': 'Документ', 'ipas_title': 'Сертификат Международной психотерапевтической ассоциации (IPAS)',
  'ipas_text': 'Программу проводит RAGIMOFF; успешно завершившие обучение получают сертификат International Psychotherapy Association. Подлинность сертификата можно проверить по QR-коду на нём или на сайте ассоциации.',
  'ipas_link': 'Проверить сертификат на сайте ассоциации — intpas.com',
  'ipas_cap': ['Образец сертификата'],
  'price': 'Стоимость', 'price_t': 'Стоимость обучения',
  'pd_months': 'Программа: три месяца',
 },
 'en': {
  'who': 'Led by', 'more': 'About the specialist',
  'facts': 'At a glance',
  'inst_eyebrow': 'Document', 'inst_title': 'Diploma of the Saint Petersburg Institute of Additional Professional Education',
  'inst_text': 'The professional retraining programme is approved by the institute’s management. Students trained under Dr Ragimov receive the institute’s diploma, which is entered in the state register FIS FRDO.',
  'inst_link': 'More about the institute — faculty, licence, other programmes',
  'inst_cap': ['Sample diploma', 'Diploma supplement', 'Education licence'],
  'ipas_eyebrow': 'Document', 'ipas_title': 'Certificate of the International Psychotherapy Association (IPAS)',
  'ipas_text': 'The programme is run by RAGIMOFF; graduates receive a certificate of the International Psychotherapy Association. Its authenticity can be checked with the QR code on it or on the association’s website.',
  'ipas_link': 'Verify a certificate on the association’s website — intpas.com',
  'ipas_cap': ['Sample certificate'],
  'price': 'Price', 'price_t': 'Tuition',
  'pd_months': 'Programme: three months',
 },
}
INST_IMG = ['images/institute/diplom-spb-idpo.jpg', 'images/institute/diplom-spb-prilozhenie.jpg', 'images/institute/licenziya-1.jpg']
IPAS_IMG = {'samira.html': 'images/certificate/sample-cert-ipas-family.jpg', '*': 'images/certificate/sample-cert-ipas-klinik.jpg'}


def who_box(lang, new_page, orig, rel, map_url, MAP, NAMES, lead, eyebrow=None):
    t = T[lang]; e = H.escape
    return ('<section class="n-sec"><div class="n-wrap"><a class="n-who" href="%s"><img src="%s" alt="%s" loading="lazy">'
            '<span class="n-who-body"><span class="n-eyebrow">%s</span><span class="n-who-name">%s</span><span class="n-who-lead">%s</span>'
            '<span class="n-who-more">%s →</span></span></a></div></section>') % (
        rel(new_page, lang + '/' + MAP[orig]), map_url('index.html', new_page, PHOTO[orig]), e(NAMES[orig][lang]),
        e(eyebrow or t['who']), e(NAMES[orig][lang]), e(lead), e(t['more']))


def doc_block(lang, new_page, kind, orig, map_url):
    t = T[lang]; e = H.escape
    if kind == 'inst':
        imgs, url, pre = INST_IMG, INSTITUTE_URL, 'inst'
    else:
        imgs, url, pre = [IPAS_IMG.get(orig, IPAS_IMG['*'])], IPAS_URL, 'ipas'
    shots = ''.join('<button class="n-shot" type="button" data-full="%s" aria-label="%s"><img src="%s" alt="%s" loading="lazy"><span class="n-shot-cap">%s</span></button>' % (
        e(map_url('index.html', new_page, im)), e(cap), e(map_url('index.html', new_page, im)), e(cap), e(cap))
        for im, cap in zip(imgs, t[pre + '_cap']))
    return ('<section class="n-sec n-sec-alt n-doc"><div class="n-wrap"><div class="n-doc-grid"><div class="n-doc-text">'
            '<span class="n-eyebrow">%s</span><h2 class="n-h2">%s</h2><p class="n-lead">%s</p>'
            '<a class="n-doc-link" href="%s" target="_blank" rel="noopener">%s ↗</a></div>'
            '<div class="n-gallery n-doc-shots">%s</div></div></div></section>') % (
        e(t[pre + '_eyebrow']), e(t[pre + '_title']), e(t[pre + '_text']), e(url), e(t[pre + '_link']), shots)


def price_block(lang, card_html):
    t = T[lang]
    return ('<section class="n-sec n-price-one"><div class="n-wrap"><div class="n-sec-head"><div><span class="n-eyebrow">%s</span>'
            '<h2 class="n-h2">%s</h2></div></div><div class="n-price-one-card">%s</div></div></section>') % (H.escape(t['price']), H.escape(t['price_t']), card_html)


def facts_strip(lang, card):
    """Ключевые факты — строки карточки программы (без цен): подпись + значение."""
    t = T[lang]; e = H.escape
    items = []
    for row in card.select('.price-row'):
        lab = row.select_one('.price-row-label'); val = row.select_one('.price-row-value')
        if lab is None or val is None or 'AZN' in val.get_text():
            continue
        items.append('<li><span>%s</span><b>%s</b></li>' % (e(lab.get_text(' ', strip=True)), e(val.get_text(' ', strip=True))))
    if not items:
        return ''
    return '<section class="n-facts"><div class="n-wrap"><ul class="n-facts-list" aria-label="%s">%s</ul></div></section>' % (e(t['facts']), ''.join(items[:5]))


def months_block(lang, ST):
    t = ST.T[lang]; e = H.escape
    months = ''.join('<li class="n-month"><span class="n-month-n">%s</span><div><h4>%s</h4><p>%s</p></div></li>' % (e(a), e(b), e(c)) for a, b, c in t['months'])
    return ('<section class="n-sec" id="sec-curriculum"><div class="n-wrap"><div class="n-sec-head"><div><span class="n-eyebrow">%s</span>'
            '<h2 class="n-h2">%s</h2></div></div><ol class="n-months">%s</ol><p class="n-short-foot">%s</p></div></section>') % (
        e(t['pd_eyebrow']), e(t['pd_title']), months, e(t['pd_foot']))


import re as _re
PRICE_H = _re.compile(r'Qiymət|Стоимост|Цена|Price|Cost|Tuition', _re.I)
FREUD_H = _re.compile(r'Freyd|Фрейд|Freud', _re.I)


def prune(main, orig, lang):
    """Убрать то, что заменяет шаблон: старые блоки цены и документов; у психодиагностики — скопированные с психоанализа
    разделы (Фрейд) и учебный план (заменяется программой Кенана по месяцам). Возвращает словарь мест вставки."""
    marks = {}
    for sec in list(main.find_all('section')):
        if sec.find_parent('section') or sec.get('id') == 'registration' or 'page-hero' in ' '.join(sec.get('class', [])):
            continue
        h = sec.find(['h2', 'h3'])
        ht = h.get_text(' ', strip=True) if h else ''
        if sec.get('id') in ('diplomas', 'certificates'):
            marks.setdefault('doc', sec.previous_sibling)
            sec.decompose()
        elif PRICE_H.search(ht) and sec.find('form') is None:
            sec.decompose()
        elif orig == 'program-psixodiaqnostika.html' and (FREUD_H.search(ht) or sec.get('id') == 'sec-curriculum'):
            sec.decompose()
    return marks


KP_URL = '/klinik-psixiatriya'
KP = {
 'az': ('Proqramın əsas mənbəyi — Kənan Rəhimovun «Klinik Psixiatriya» sorğu kitabı: dörd dildə (Azərbaycan, rus, ingilis, türk), beynəlxalq protokollar üzrə ən son diaqnostik meyarlar, diaqnostika və müalicə protokolları, dəqiq diaqnoz və dəqiq müalicə üçün lazım olan bütün alətlər bir yerdə.',
        'Əsas mənbə: «Klinik Psixiatriya» — dörd dildə, ən son beynəlxalq diaqnostik meyarlar', 'Kitabla tanış olun →'),
 'ru': ('Основной источник программы — справочник Кенана Рагимова «Клиническая психиатрия»: на четырёх языках (азербайджанский, русский, английский, турецкий), самые последние диагностические критерии по международным протоколам, протоколы диагностики и лечения и все инструменты для точной диагностики и точного лечения в одном месте.',
        'Основной источник: «Клиническая психиатрия» — на четырёх языках, последние международные диагностические критерии', 'Познакомиться с книгой →'),
 'en': ('The programme’s main source is Kenan Ragimov’s reference book “Clinical Psychiatry”: in four languages (Azerbaijani, Russian, English, Turkish), the latest diagnostic criteria under international protocols, diagnostic and treatment protocols and every tool needed for accurate diagnosis and treatment in one place.',
        'Main source: “Clinical Psychiatry” — in four languages, the latest international diagnostic criteria', 'Open the book →'),
}


def kp_bonus(main, lang, soup_new):
    """Психодиагностика: вместо бонуса «книги Фрейда» (это к психоанализу) — «Клиническая психиатрия» со ссылкой (Кенан 09.11)."""
    para, item, link = KP[lang]
    for el in main.find_all(['p', 'li']):
        if FREUD_H.search(el.get_text(' ', strip=True)) and not el.find_parent('form'):
            el.clear()
            if el.name == 'p':
                el.append(para + ' ')
                a = soup_new.new_tag('a', attrs={'href': KP_URL, 'class': 'n-inline-link'})
                a.string = link
                el.append(a)
            else:
                el.append(item)


def prune_freud_items(main):
    for el in main.find_all(['p', 'li']):
        if FREUD_H.search(el.get_text(' ', strip=True)):
            el.decompose()


KP_STAT = {'az': ('4', 'dildə «Klinik Psixiatriya»'), 'ru': ('4', 'языка «Клинической психиатрии»'), 'en': ('4', 'languages of “Clinical Psychiatry”')}
FREUD_ANY = _re.compile(r'[Bb]onus[^.;"]*?(Freyd|Фрейд|Freud)[^.;"]*|(Freyd|Фрейд|Freud)\w*\s+24\s+\w+\s+bonus\w*|(all\s+)?24\s+\w+\s+(by\s+)?(Freud|Фрейда)[^.;"]*', _re.I)


def kp_text(lang, txt):
    return FREUD_ANY.sub(KP[lang][1], txt)


def kp_stats(main, lang):
    for st in main.select('.stat-item'):
        if FREUD_H.search(st.get_text(' ', strip=True)):
            n = st.select_one('.stat-num'); lab = st.select_one('.stat-label')
            if n is not None and lab is not None:
                n.string, lab.string = KP_STAT[lang]
