"""Полное название ассоциации в строке статуса (три языка) и короткий подзаголовок «Просвещения». Запуск из test/11."""
import io, re

p = 'assets/js/content.js'
t = io.open(p, encoding='utf-8').read()
subs = [
    (r"'Амбассадор ассоциации IPAS[^']*'", "'Амбассадор Международной психотерапевтической ассоциации с 2022 года'"),
    (r"'2022-ci ildən IPAS assosiasiyasının səfiri'", "'2022-ci ildən Beynəlxalq Psixoterapevtik Assosiasiyanın səfiri'"),
    (r"'Ambassador of the IPAS association since 2022'", "'Ambassador of the International Psychotherapy Association since 2022'"),
    (r"enlSub: 'Заблуждения, мешающие вовремя получить квалифицированную помощь\.'", "enlSub: 'Заблуждения, мешающие вовремя получить помощь специалиста.'"),
]
for a, b in subs:
    t, n = re.subn(a, b, t)
    print(n, b[:60])
    if n != 1:
        raise SystemExit('ожидалась одна замена: ' + a)
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
