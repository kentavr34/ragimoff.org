"""Ноктюрн · страница «Контакты» (Кенан 09.11.2026): адрес офиса, карта, маршрут и такси в одно касание,
запись на консультацию только через WhatsApp, почта. Адрес, телефон и почта — с оригинального сайта (подвал)."""
import html as H

PAGE = 'elaqe/index.html'
LAT, LON = '40.3846394', '49.8289682'          # Caspian Business Center (OpenStreetMap, здание way 222090647)
WA = '994702200376'
WA_SHOW = '+994 70 220 03 76'
EMAIL = 'info@ragimoff.org'
Q = 'Caspian+Business+Center,+Jafar+Jabbarly+40,+Baku'

ROUTE = 'https://www.google.com/maps/dir/?api=1&destination=%s,%s' % (LAT, LON)
MAPS = 'https://www.google.com/maps/search/?api=1&query=%s' % Q
UBER = ('https://m.uber.com/ul/?action=setPickup&pickup=my_location&dropoff[latitude]=%s&dropoff[longitude]=%s'
        '&dropoff[nickname]=Caspian%%20Business%%20Center&dropoff[formatted_address]=Jafar%%20Jabbarly%%2040%%2C%%20Baku' % (LAT, LON))
WAZE = 'https://waze.com/ul?ll=%s,%s&navigate=yes' % (LAT, LON)
EMBED = 'https://maps.google.com/maps?q=%s,%s&z=17&output=embed' % (LAT, LON)

T = {
 'az': {'nav': 'Əlaqə', 'eyebrow': 'Əlaqə', 'title': 'Bizi necə tapmaq olar',
        'lead': 'Konsultasiyalar Bakıda, Caspian Business Center-də keçirilir.',
        'addr_h': 'Ünvan', 'addr': ['AZ1065, Bakı şəhəri, Cəfər Cabbarlı 40', 'Caspian Business Center, 9-cu mərtəbə'],
        'route': 'Marşrut', 'maps': 'Xəritədə aç', 'uber': 'Uber ilə taksi', 'waze': 'Waze',
        'route_note': 'Telefonda düymə xəritə və ya taksi tətbiqini açır — ünvan artıq yazılıb.',
        'wa_h': 'Konsultasiyaya yazılmaq', 'wa_t': 'Yazılış yalnız WhatsApp ilə: %s. Mütəxəssisi, formatı və vaxtı yazışmada razılaşdırırıq.' % WA_SHOW,
        'wa_b': 'WhatsApp-da yazın', 'mail_h': 'Elektron poçt', 'mail_t': 'Sual, təklif və ya sənəd göndərmək üçün:',
        'map_t': 'Caspian Business Center xəritədə'},
 'ru': {'nav': 'Контакты', 'eyebrow': 'Контакты', 'title': 'Как нас найти',
        'lead': 'Консультации проходят в Баку, в Caspian Business Center.',
        'addr_h': 'Адрес', 'addr': ['AZ1065, г. Баку, Джафар Джаббарлы 40', 'Caspian Business Center, 9 этаж'],
        'route': 'Маршрут', 'maps': 'Открыть на карте', 'uber': 'Такси Uber', 'waze': 'Waze',
        'route_note': 'На телефоне кнопка откроет карты или приложение такси — адрес уже указан.',
        'wa_h': 'Запись на консультацию', 'wa_t': 'Запись только через WhatsApp: %s. Специалиста, формат и время согласуем в переписке.' % WA_SHOW,
        'wa_b': 'Написать в WhatsApp', 'mail_h': 'Электронная почта', 'mail_t': 'Для вопросов, предложений и документов:',
        'map_t': 'Caspian Business Center на карте'},
 'en': {'nav': 'Contact', 'eyebrow': 'Contact', 'title': 'How to find us',
        'lead': 'Consultations take place in Baku, at Caspian Business Center.',
        'addr_h': 'Address', 'addr': ['AZ1065, Baku city, Jafar Jabbarly 40', 'Caspian Business Center, 9th floor'],
        'route': 'Directions', 'maps': 'Open in Maps', 'uber': 'Uber taxi', 'waze': 'Waze',
        'route_note': 'On a phone the button opens your maps or taxi app with the address already filled in.',
        'wa_h': 'Book a consultation', 'wa_t': 'Booking is by WhatsApp only: %s. We agree on the specialist, format and time in the chat.' % WA_SHOW,
        'wa_b': 'Message on WhatsApp', 'mail_h': 'Email', 'mail_t': 'For questions, proposals and documents:',
        'map_t': 'Caspian Business Center on the map'},
}


def main_html(lang, hero):
    t = T[lang]; e = H.escape
    btn = lambda href, label, cls='btn-line': '<a class="btn %s" href="%s" target="_blank" rel="noopener">%s</a>' % (cls, e(href), e(label))
    return hero + '''<section class="n-sec n-contact"><div class="n-wrap"><div class="n-contact-grid">
<div class="n-contact-col">
<div class="n-contact-card"><span class="n-eyebrow">%s</span><p class="n-contact-addr">%s</p>
<div class="n-contact-btns n-contact-go">%s%s%s</div><p class="n-contact-note">%s</p></div>
<div class="n-contact-card"><span class="n-eyebrow">%s</span><p>%s</p><div class="n-contact-btns">%s</div></div>
<div class="n-contact-card"><span class="n-eyebrow">%s</span><p>%s</p><a class="n-contact-mail" href="mailto:%s">%s</a></div>
</div>
<div class="n-contact-map"><iframe src="%s" title="%s" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
</div></div></section>''' % (
        e(t['addr_h']), '<br>'.join(e(x) for x in t['addr']),
        btn(ROUTE, t['route'], 'btn-fill'), btn(UBER, t['uber']), btn(WAZE, t['waze']), e(t['route_note']),
        e(t['wa_h']), e(t['wa_t']), btn('https://wa.me/' + WA, t['wa_b'], 'btn-fill'),
        e(t['mail_h']), e(t['mail_t']), EMAIL, EMAIL,
        e(EMBED), e(t['map_t']))
