"""Доводка после замечаний владельца и четвёртого круга: подзаголовки в две строки, зоны нажатия, зазоры у документов,
полное название ассоциации, образцы сертификатов без имени выпускника. Запуск из test/11."""
import io, re
from PIL import Image, ImageDraw

p = 'assets/js/content.js'
t = io.open(p, encoding='utf-8').read()
R = [
    ("booksSub: 'Книги наших специалистов и переводы профессиональных учебников. С некоторыми из них можно ознакомиться здесь.'", "booksSub: 'Авторские книги и переводы профессиональных учебников.'"),
    ("booksSub: 'Mütəxəssislərimizin kitabları və peşəkar dərsliklərin tərcümələri. Bəziləri ilə burada tanış ola bilərsiniz.'", "booksSub: 'Müəllif kitabları və peşəkar dərsliklərin tərcümələri.'"),
    ("booksSub: 'Books by our specialists and translations of professional textbooks. You can explore some of them here.'", "booksSub: 'Our own books and translations of professional textbooks.'"),
    ("enlSub: 'Самые частые заблуждения, из-за которых люди не получают вовремя квалифицированную помощь. Читайте и разбирайтесь.'", "enlSub: 'Заблуждения, мешающие вовремя получить квалифицированную помощь.'"),
    ("enlSub: 'İnsanların vaxtında ixtisaslı kömək almasına mane olan ən çox yayılmış yanlış təsəvvürlər. Oxuyun və aydınlaşdırın.'", "enlSub: 'Vaxtında ixtisaslı kömək almağa mane olan yanlış təsəvvürlər.'"),
    ("enlSub: 'The most common misconceptions that keep people from getting qualified help in time. Read and find out.'", "enlSub: 'Misconceptions that keep people from qualified help in time.'"),
]
for a, b in R:
    a2 = a
    if a2 not in t:                      # агент мог поставить неразрывные пробелы — ищем по началу строки
        key = a.split(':')[0]
        m = re.search(re.escape(key) + r": '[^']*'", t)
        hits = [x for x in re.finditer(re.escape(key) + r": '[^']*'", t)]
        idx = {'booksSub': 0, 'enlSub': 0}
        lang_i = 0 if 'Авторские' in b or 'Заблуждения' in b else 1 if 'ə' in b else 2
        if len(hits) != 3:
            raise SystemExit('не найдено: ' + key)
        t = t[:hits[lang_i].start()] + b + t[hits[lang_i].end():]
    else:
        t = t.replace(a, b, 1)
n = len(re.findall(r"Амбассадор ассоциации IPAS с 2022\S*года", t))
t = re.sub(r"Амбассадор ассоциации IPAS с 2022\S*года", "Амбассадор Международной психотерапевтической ассоциации с 2022 года", t)
print('строка амбассадора RU возвращена:', n)
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

CSS = """
/* ═══ доводка: зоны нажатия, зазоры, кегль ═══ */
.person__more, .sh__link { min-height: var(--tap); display: inline-flex; align-items: center; gap: 8px; }
.facts li, .proof__c, .vids__i figcaption { font-size: 17px; }
.proofs { margin-top: var(--r2); } .rib__bar { margin-top: var(--r2); }
@media (min-width: 761px) { .rib__stick { padding-bottom: var(--r2); } }
@media (max-width: 760px) { .seg--lang button { min-width: 40px; } .bk__btns .btn { font-size: 15px; padding: 0 8px; } .head { gap: 6px; } .head__r { gap: 5px; } }
@media (max-width: 359px) { .seg--lang button { min-width: 32px; } }
"""
p = 'assets/css/site.css'
c = io.open(p, encoding='utf-8').read()
if 'доводка: зоны нажатия' not in c:
    io.open(p, 'w', encoding='utf-8', newline='\n').write(c + CSS)

# образцы сертификатов: без имени выпускника (на образце личные данные не нужны)
for name in ('cert', 'cert-family'):
    f = 'assets/img/proof/%s.jpg' % name
    im = Image.open(f).convert('RGB'); w, h = im.size
    d = ImageDraw.Draw(im)
    d.rectangle([round(w * .28), round(h * .385), round(w * .74), round(h * .492)], fill=(255, 255, 255))
    d.line([round(w * .30), round(h * .492), round(w * .72), round(h * .492)], fill=(214, 178, 74), width=max(2, h // 300))
    im.save(f, quality=86, optimize=True, progressive=True)
print('patched')
