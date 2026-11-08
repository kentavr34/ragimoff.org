"""Ноктюрн · запись на консультацию в одно касание (Кенан 09.11.2026).

Специалист: Кенан Рагимов (по умолчанию) / Самира Рагимова / оба; формат: онлайн (по умолчанию, первым) / очно;
цена видна сразу: один специалист — 100 онлайн / 150 очно AZN, оба — 150 / 200 AZN (1 час).
Тема — из проблем сайта (пункты меню «Konsultasiya») или «Другое» + коротко симптомы.
«Записаться» → заявка (api training-reg, service consult|кто|формат) → оплата ePoint → страница успеха:
отправить чек на номер и согласовать время.
"""
import html as H

T = {
 'az': {'eyebrow': 'Konsultasiya', 'title': 'Konsultasiyaya yazılın', 'spec': 'Mütəxəssis', 'sp_k': 'Kənan Rəhimov', 'sp_s': 'Samirə Rəhimova',
        'sp_b': 'Hər iki mütəxəssis', 'fmt': 'Format', 'on': 'Onlayn', 'off': 'Əyani', 'topic': 'Mövzu', 'other': 'Digər',
        'symptoms': 'Qısaca vəziyyəti təsvir edin', 'name': 'Ad', 'phone': 'Telefon', 'price': '1 saat', 'send': 'Yazıl və ödə',
        'sending': 'Göndərilir…', 'after': 'Ödənişdən sonra qəbzi +994 70 220 03 76 nömrəsinə göndərin və konsultasiya vaxtını razılaşdırın.',
        'ok': 'Müraciətiniz qəbul edildi. Ödəniş qəbzini +994 70 220 03 76 nömrəsinə göndərin və vaxtı razılaşdırın.',
        'err': 'Göndərmək alınmadı. Zəhmət olmasa WhatsApp ilə yazın.', 'req': 'Bu sahəni doldurun'},
 'ru': {'eyebrow': 'Консультация', 'title': 'Записаться на консультацию', 'spec': 'Специалист', 'sp_k': 'Кенан Рагимов', 'sp_s': 'Самира Рагимова',
        'sp_b': 'Оба специалиста', 'fmt': 'Формат', 'on': 'Онлайн', 'off': 'Очно', 'topic': 'Тема', 'other': 'Другое',
        'symptoms': 'Коротко опишите симптомы', 'name': 'Имя', 'phone': 'Телефон', 'price': '1 час', 'send': 'Записаться и оплатить',
        'sending': 'Отправка…', 'after': 'После оплаты отправьте чек на номер +994 70 220 03 76 и согласуйте время консультации.',
        'ok': 'Заявка принята. Отправьте чек об оплате на номер +994 70 220 03 76 и согласуйте время.',
        'err': 'Не удалось отправить. Пожалуйста, напишите в WhatsApp.', 'req': 'Заполните это поле'},
 'en': {'eyebrow': 'Consultation', 'title': 'Book a consultation', 'spec': 'Specialist', 'sp_k': 'Kenan Ragimov', 'sp_s': 'Samira Rahimova',
        'sp_b': 'Both specialists', 'fmt': 'Format', 'on': 'Online', 'off': 'In person', 'topic': 'Topic', 'other': 'Other',
        'symptoms': 'Briefly describe the symptoms', 'name': 'Name', 'phone': 'Phone', 'price': '1 hour', 'send': 'Book and pay',
        'sending': 'Sending…', 'after': 'After payment, send the receipt to +994 70 220 03 76 and agree on the time of the consultation.',
        'ok': 'Your request has been received. Send the receipt to +994 70 220 03 76 and agree on the time.',
        'err': 'Could not send. Please write to us on WhatsApp.', 'req': 'Please fill in this field'},
}
TOPICS = ['aile-terapiyasi.html', 'aile-terapiyasi-usaq.html', 'valideyn-mektebi.html', 'depressiya.html', 'panik-ataklar.html', 'sosial-fobiya.html', 'enurez.html']
# цены для показа (сервер считает сам): (кто, формат) → AZN / руб. / $
SHOW = {'az': {('one', 'online'): '100 AZN', ('one', 'offline'): '150 AZN', ('both', 'online'): '150 AZN', ('both', 'offline'): '200 AZN'},
        'ru': {('one', 'online'): '100 AZN · 5 000 руб.', ('one', 'offline'): '150 AZN · 7 500 руб.', ('both', 'online'): '150 AZN · 7 500 руб.', ('both', 'offline'): '200 AZN · 10 000 руб.'},
        'en': {('one', 'online'): '100 AZN · $60', ('one', 'offline'): '150 AZN · $90', ('both', 'online'): '150 AZN · $90', ('both', 'offline'): '200 AZN · $120'}}


def form_html(lang, labels, current=''):
    """labels — подписи меню сайта (LABELS[lang]); current — тема страницы (выбрана заранее)."""
    t = T[lang]; e = H.escape
    import json
    show = json.dumps({'%s|%s' % k: v for k, v in SHOW[lang].items()}, ensure_ascii=False)
    topics = ''
    first = current if current in TOPICS else TOPICS[0]
    for k in TOPICS:
        if labels.get(k):
            topics += '<label class="n-chip"><input type="radio" name="movzu" value="%s"%s><span>%s</span></label>' % (
                e(labels[k]), ' checked' if k == first else '', e(labels[k]))
    topics += '<label class="n-chip"><input type="radio" name="movzu" value="other"><span>%s</span></label>' % e(t['other'])
    return ('''<form class="n-form n-consult" id="consultForm" novalidate data-lang="%s" data-ok="%s" data-err="%s" data-sending="%s" data-req="%s" data-show='%s'>
<fieldset class="n-calc-row"><legend>%s</legend>
<label class="n-chip"><input type="radio" name="mutexessis" value="kenan" checked><span>%s</span></label>
<label class="n-chip"><input type="radio" name="mutexessis" value="samira"><span>%s</span></label>
<label class="n-chip"><input type="radio" name="mutexessis" value="both"><span>%s</span></label></fieldset>
<fieldset class="n-calc-row"><legend>%s</legend>
<label class="n-chip"><input type="radio" name="format" value="online" checked><span>%s</span></label>
<label class="n-chip"><input type="radio" name="format" value="offline"><span>%s</span></label></fieldset>
<div class="n-calc-out"><span class="n-calc-rate">%s</span><span class="n-calc-total"><b data-cprice></b></span></div>
<fieldset class="n-calc-row"><legend>%s</legend>%s</fieldset>
<label class="n-form-wide" data-other hidden><span>%s</span><textarea name="simptom" rows="3"></textarea></label>
<div class="n-form-grid"><label><span>%s</span><input name="ad" required autocomplete="name"></label>
<label><span>%s</span><input name="telefon" type="tel" required autocomplete="tel" placeholder="+994"></label></div>
<p class="n-form-after">%s</p>
<button class="n-btn" type="submit">%s</button><p class="n-form-msg" role="status" hidden></p></form>''' % (
        lang, e(t['ok']), e(t['err']), e(t['sending']), e(t['req']), e(show).replace('&quot;', '"'),
        e(t['spec']), e(t['sp_k']), e(t['sp_s']), e(t['sp_b']), e(t['fmt']), e(t['on']), e(t['off']), e(t['price']),
        e(t['topic']), topics, e(t['symptoms']), e(t['name']), e(t['phone']), e(t['after']), e(t['send'])))


def section_html(lang, labels, current=''):
    t = T[lang]
    return ('<section class="n-sec n-sec-alt" id="registration"><div class="n-wrap"><div class="n-sec-head"><div><span class="n-eyebrow">%s</span>'
            '<h2 class="n-h2">%s</h2></div></div>%s</div></section>') % (H.escape(t['eyebrow']), H.escape(t['title']), form_html(lang, labels, current))
