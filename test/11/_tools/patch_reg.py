"""Единая форма записи (#reg): разметка, подключение, стили, тексты на трёх языках; кнопки «Записаться» ведут на форму. Запуск из test/11."""
import io, re, shutil, pathlib

for f in ('index.html', 'assets/js/site.js', 'assets/css/site.css', 'assets/js/content.js'):
    shutil.copy(f, '_agent/backup/' + pathlib.Path(f).name + '.bak-reg')


def edit(path, pairs):
    t = io.open(path, encoding='utf-8').read()
    for a, b in pairs:
        if a not in t:
            raise SystemExit('НЕ НАЙДЕНО в %s: %s' % (path, a[:90]))
        t = t.replace(a, b, 1)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(t)


edit('index.html', [
    ('  <section class="sec sec--tg" id="tg">',
     '  <section class="sec" id="reg"><div class="wrap"><header class="sh" data-h="reg"></header><div class="reg" id="regBox"></div></div></section>\n  <section class="sec sec--tg" id="tg">'),
    ('<a class="head__cta" id="headCta" href="#cons">', '<a class="head__cta" id="headCta" href="#reg" data-reg="consult">'),
])

p = 'assets/js/site.js'
t = io.open(p, encoding='utf-8').read()
pairs = [
    ("import { initLight }", "import { regRender, regOpen } from './reg.js';\nimport { initLight }"),
    ("`<a class=\"btn mob__cta\" href=\"#cons\">", "`<a class=\"btn mob__cta\" href=\"#reg\" data-reg=\"consult\">"),
    ("cb.href = L.form; cb.removeAttribute('target');", "cb.href = '#reg'; cb.dataset.reg = 'consult'; cb.removeAttribute('target');"),
    ("kb.href = L.corp;", "kb.href = '#reg'; kb.dataset.reg = 'b2b';"),
    ("  const ea = $('#enlAll');", "  regRender(t, lang);\n  const ea = $('#enlAll');"),
    ("  const a = e.target.closest('a[href^=\"#\"]');", "  const rg = e.target.closest('[data-reg]'); if (rg) regOpen(rg.dataset.reg);\n  const a = e.target.closest('a[href^=\"#\"]');"),
]
for a, b in pairs:
    if a not in t:
        raise SystemExit('site.js: не найдено ' + a[:70])
    t = t.replace(a, b, 1)
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

# номер версии — для всех модулей
p = '_tools/stamp.py'
t = io.open(p, encoding='utf-8').read()
if 'reg' not in t:
    t = t.replace("print('версия'", "t = io.open(p, encoding='utf-8').read()\nt, e = re.subn(r\"(from '\\./reg\\.js)(\\?v=\\d+)?'\", r\"\\1?v=\" + v + \"'\", t)\nio.open(p, 'w', encoding='utf-8', newline='\\n').write(t)\nprint('версия'")
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

CSS = """
/* ═══ форма записи: одна форма, выбор нажатием, всё выбрано по умолчанию (владелец, 11.11 вечер) ═══ */
.reg { max-width: 1080px; margin: 0 auto; }
.reg__kinds { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: var(--s2); }
.reg__kind { min-height: var(--btn-h); padding: 0 var(--s2); border-radius: 99px; border: 1px solid var(--line); background: var(--layer); color: var(--text); font: 600 15px/1.15 var(--f-sub); transition: background var(--t1), color var(--t1), border-color var(--t1); }
.reg__kind:hover { border-color: color-mix(in srgb, var(--gold) 60%, transparent); } .reg__kind.is-on { background: var(--gold); color: var(--on-gold); border-color: var(--gold); }
.reg__f { margin-top: var(--r2); display: grid; grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr); gap: var(--r2); align-items: start; }
.reg__main, .reg__side { padding: var(--r2); border-radius: var(--rad); background: var(--layer); border: 1px solid var(--line); display: flex; flex-direction: column; gap: var(--r1); }
.reg__side { position: sticky; top: 90px; border-color: color-mix(in srgb, var(--gold) 45%, transparent); }
.frow { display: flex; flex-direction: column; gap: var(--s2); } .frow__l, .fld > span { font: 600 12.5px/1.3 var(--f-sub); letter-spacing: .14em; text-transform: uppercase; color: var(--smoke); }
.chips { display: flex; flex-wrap: wrap; gap: var(--s2); }
.chip { min-height: var(--tap); padding: 0 var(--s3); border-radius: 99px; border: 1px solid var(--line); color: var(--text); font: 500 15px/1.2 var(--f-sub); text-align: left; transition: background var(--t1), color var(--t1), border-color var(--t1); }
.chip:hover { border-color: color-mix(in srgb, var(--gold) 60%, transparent); } .chip.is-on { background: color-mix(in srgb, var(--gold) 18%, transparent); border-color: var(--gold); color: var(--milk); }
.reg__me { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--s3); padding-top: var(--r1); border-top: 1px solid var(--line); }
.fld { display: flex; flex-direction: column; gap: var(--s1); min-width: 0; }
.inp { width: 100%; min-height: var(--btn-h-sm); padding: 0 var(--s3); border-radius: 12px; border: 1px solid var(--line); background: var(--bg); color: var(--milk); font: 400 17px/1.2 var(--f-read); transition: border-color var(--t1); }
.inp:focus { outline: none; border-color: var(--gold); } .inp.is-bad { border-color: #C0563F; } .inp[type="file"] { padding: 10px var(--s3); font-size: 14px; font-family: var(--f-sub); color: var(--text); }
.reg__files { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--s3); } .fld--file > span { letter-spacing: .04em; text-transform: none; font-weight: 500; font-size: 14px; }
.step { display: inline-flex; align-items: center; gap: var(--s3); } .step__b { width: var(--tap); height: var(--tap); border-radius: 50%; border: 1px solid var(--line); color: var(--milk); font: 400 22px/1 var(--f-sub); }
.step__b:hover { border-color: var(--gold); } .step__v { min-width: 2.2em; text-align: center; font: 400 30px/1 var(--f-display); color: var(--milk); font-variant-numeric: lining-nums tabular-nums; } .step__h { font: 400 14px/1.3 var(--f-sub); color: var(--smoke); }
.reg__pl { font: 600 12.5px/1.3 var(--f-sub); letter-spacing: .14em; text-transform: uppercase; color: var(--gold); }
.reg__p { font: 400 clamp(30px, 3vw, 44px)/1.05 var(--f-display); color: var(--milk); font-variant-numeric: lining-nums; } .reg__ps { font: 400 15px/1.4 var(--f-sub); color: var(--smoke); margin-top: calc(var(--s2) * -1); }
.reg__note { font: 400 16px/1.5 var(--f-read); color: var(--text); padding-top: var(--r1); border-top: 1px solid var(--line); } .reg__go { width: 100%; white-space: normal; text-align: center; padding: var(--s2) var(--s3); line-height: 1.2; }
.reg__pay { display: flex; flex-direction: column; gap: var(--s2); } .reg__pay .btn { white-space: normal; padding: var(--s2) var(--s3); line-height: 1.2; }
.reg__msg { font: 500 15px/1.45 var(--f-sub); color: var(--gold-hi); } .reg__msg.is-err { color: #D0705A; } .reg__msg a { text-decoration: underline; }
@media (max-width: 900px) { .reg__f { grid-template-columns: 1fr; } .reg__side { position: static; } }
@media (max-width: 760px) { .reg__kinds { grid-template-columns: 1fr 1fr; } .reg__kind { font-size: 14px; min-height: var(--btn-h-sm); } .reg__me, .reg__files { grid-template-columns: 1fr; } .reg__main, .reg__side { padding: var(--r1); } .chip { padding: 0 var(--s2); font-size: 14.5px; } }
"""
p = 'assets/css/site.css'
c = io.open(p, encoding='utf-8').read()
if 'форма записи: одна форма' not in c:
    io.open(p, 'w', encoding='utf-8', newline='\n').write(c + CSS)

p = 'assets/js/content.js'
t = io.open(p, encoding='utf-8').read()
if 'REG_FORM' not in t:
    t += """
/* ── REG_FORM: единая форма записи — подписи на трёх языках ── */
const REG = {
  ru: { eye: '', h: 'Запись', sub: 'Выберите, на\u00a0что записаться, — остальное в\u00a0несколько нажатий.',
    kinds: [['consult', 'Консультация'], ['edu', 'Обучение'], ['ind', 'Индивидуальная подготовка'], ['b2b', 'Для компании']],
    f: { fname: 'Имя', lname: 'Фамилия', phone: 'Телефон', company: 'Компания', other: 'Ваша тема', id: 'Удостоверение личности — фото или скан', dip: 'Диплом о\u00a0высшем образовании — если есть' },
    who: { l: 'Специалист', o: [['kenan', 'Кенан Рагимов'], ['samira', 'Самира Рагимова'], ['both', 'Оба специалиста']] }, fmt: { l: 'Формат', o: [['online', 'Онлайн'], ['offline', 'Очно']] },
    topic: 'Тема', topicOther: 'Другая тема', prog: 'Программа', hours: { l: 'Количество часов', min: 'минимум 20' },
    b2b: { topic: 'Тематика', other: 'Другое', free: 'Заявка без оплаты', goal: { l: 'Цель', o: ['Развитие команды', 'Подготовка руководителей', 'Рост продаж', 'Стресс и выгорание', 'Корпоративное мероприятие'] },
      count: { l: 'Участников', o: ['до 10', '10–20', '20–50', 'более 50'] }, lang: { l: 'Язык', o: ['Азербайджанский', 'Русский', 'Английский'] }, place: { l: 'Где', o: ['В вашем офисе', 'Онлайн', 'Выездной формат'] } },
    price: 'Стоимость', perHour: 'за встречу, 1 час', noteB2b: 'Оплаты на этом шаге нет: с вами свяжется наш специалист.',
    send: { consult: 'Записаться и перейти к оплате', edu: 'Отправить заявку', ind: 'Записаться и перейти к оплате', b2b: 'Отправить заявку' },
    pay: { now: 'Оплатить сейчас', inst: 'В рассрочку (банк)' }, req: 'Заполните выделенные поля.', sending: 'Отправляем…', ok: 'Заявка принята. Мы свяжемся с вами.', err: 'Не удалось отправить заявку. Напишите нам в' },
  az: { eye: '', h: 'Qeydiyyat', sub: 'Nəyə yazılmaq istədiyinizi seçin — qalanı bir neçə toxunuşla.',
    kinds: [['consult', 'Konsultasiya'], ['edu', 'Təhsil'], ['ind', 'Fərdi hazırlıq'], ['b2b', 'Şirkət üçün']],
    f: { fname: 'Ad', lname: 'Soyad', phone: 'Telefon', company: 'Şirkət', other: 'Sizin mövzunuz', id: 'Şəxsiyyət vəsiqəsi — foto və ya skan', dip: 'Ali təhsil haqqında diplom — varsa' },
    who: { l: 'Mütəxəssis', o: [['kenan', 'Kənan Rəhimov'], ['samira', 'Samirə Rəhimova'], ['both', 'Hər iki mütəxəssis']] }, fmt: { l: 'Format', o: [['online', 'Onlayn'], ['offline', 'Əyani']] },
    topic: 'Mövzu', topicOther: 'Başqa mövzu', prog: 'Proqram', hours: { l: 'Saatların sayı', min: 'ən azı 20' },
    b2b: { topic: 'Mövzu', other: 'Digər', free: 'Ödənişsiz müraciət', goal: { l: 'Məqsəd', o: ['Komandanın inkişafı', 'Rəhbərlərin hazırlanması', 'Satışların artırılması', 'Stress və tükənmə', 'Korporativ tədbir'] },
      count: { l: 'İştirakçı sayı', o: ['10-a qədər', '10–20', '20–50', '50-dən çox'] }, lang: { l: 'Dil', o: ['Azərbaycan dili', 'Rus dili', 'İngilis dili'] }, place: { l: 'Harada', o: ['Sizin ofisdə', 'Onlayn', 'Səyyar format'] } },
    price: 'Qiymət', perHour: 'bir görüş, 1 saat', noteB2b: 'Bu mərhələdə ödəniş yoxdur: mütəxəssisimiz sizinlə əlaqə saxlayacaq.',
    send: { consult: 'Yazılın və ödənişə keçin', edu: 'Müraciəti göndərin', ind: 'Yazılın və ödənişə keçin', b2b: 'Müraciəti göndərin' },
    pay: { now: 'İndi ödəyin', inst: 'Hissə-hissə (bank)' }, req: 'İşarələnmiş xanaları doldurun.', sending: 'Göndərilir…', ok: 'Müraciətiniz qəbul edildi. Sizinlə əlaqə saxlayacağıq.', err: 'Müraciəti göndərmək mümkün olmadı. Bizə yazın:' },
  en: { eye: '', h: 'Booking', sub: 'Choose what you are booking — the rest takes a few taps.',
    kinds: [['consult', 'Consultation'], ['edu', 'Education'], ['ind', 'Individual training'], ['b2b', 'For a company']],
    f: { fname: 'First name', lname: 'Last name', phone: 'Phone', company: 'Company', other: 'Your topic', id: 'Identity document — photo or scan', dip: 'Higher-education diploma — if you have one' },
    who: { l: 'Specialist', o: [['kenan', 'Kenan Ragimov'], ['samira', 'Samira Ragimova'], ['both', 'Both specialists']] }, fmt: { l: 'Format', o: [['online', 'Online'], ['offline', 'In person']] },
    topic: 'Topic', topicOther: 'Another topic', prog: 'Programme', hours: { l: 'Number of hours', min: '20 minimum' },
    b2b: { topic: 'Subject', other: 'Other', free: 'Request without payment', goal: { l: 'Goal', o: ['Team development', 'Training managers', 'Sales growth', 'Stress and burnout', 'Corporate event'] },
      count: { l: 'Participants', o: ['up to 10', '10–20', '20–50', 'more than 50'] }, lang: { l: 'Language', o: ['Azerbaijani', 'Russian', 'English'] }, place: { l: 'Where', o: ['At your office', 'Online', 'Off-site'] } },
    price: 'Price', perHour: 'per session, 1 hour', noteB2b: 'No payment at this step: our specialist will contact you.',
    send: { consult: 'Book and go to payment', edu: 'Send the request', ind: 'Book and go to payment', b2b: 'Send the request' },
    pay: { now: 'Pay now', inst: 'In instalments (bank)' }, req: 'Please fill in the highlighted fields.', sending: 'Sending…', ok: 'Your request has been received. We will contact you.', err: 'The request could not be sent. Write to us on' },
};
for (const l of Object.keys(REG)) T[l].reg = REG[l];
"""
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

p = '_tools/round.py'
t = io.open(p, encoding='utf-8').read()
if "'#reg'" not in t:
    t = t.replace("'#blog', '#tg', '.foot']", "'#blog', '#reg', '#tg', '.foot']")
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('patched')
