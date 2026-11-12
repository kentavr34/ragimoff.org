# -*- coding: utf-8 -*-
"""Пятый круг критика, читалка (12.11.2026). Повторный запуск ничего не меняет.
 • обложка на титуле — та же, что в каталоге (готовая обложка авторских книг; фактура из новой версии у остальных);
 • язык книги меняется в полосе чтения на любой странице (включая турецкий), выбор следует за языком сайта;
 • поиск по оглавлению понимает коды всех трёх классификаций (МКБ-11, DSM-5-TR, МКБ-10);
 • счётчик «N из M» убран из шапки главы (путался с номером главы); старые адреса #chN открывают главу N;
 • на титуле — переход на страницу книги (цена, заказ печатной книги)."""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)


def rep(s, a, b):
    assert s.count(a) == 1, "ожидалось 1, найдено %d: %s" % (s.count(a), a[:80])
    return s.replace(a, b)


p = "assets/js/reader.js"
s = io.open(p, encoding="utf-8").read()
if "rdr__lg" not in s:
    s = rep(s, "const cover = () => `<div class=\"rdr__cover\" style=\"background-image:url('${esc(B.cover)}')\"><span class=\"rdr__ca\">${esc(B.kicker[lang] || '')}</span><span class=\"rdr__ct\">${esc(B.t[lang])}</span></div>`;",
            "/* обложка — та же, что в каталоге: готовая (авторские книги, coverKey) или фактура из assets/img/books/covers с набранным названием */\n"
            "const cover = () => B.coverKey\n"
            "  ? `<div class=\"rdr__cover rdr__cover--img\"><img src=\"assets/img/books/covers/${B.coverKey}-${['az', 'ru', 'en'].indexOf(lang) >= 0 ? lang : 'en'}.jpg\" alt=\"${esc(B.t[lang])}\" width=\"600\" height=\"900\"></div>`\n"
            "  : `<div class=\"rdr__cover\" style=\"background-image:url('${esc(B.cover.indexOf('/images/') === 0 ? 'assets/img/' + B.cover.slice(8) : B.cover)}')\"><span class=\"rdr__ca\">${esc(B.kicker[lang] || '')}</span><span class=\"rdr__ct\">${esc(B.t[lang])}</span></div>`;")
    s = rep(s, "<span class=\"rdr__tools\"><button type=\"button\" id=\"rdFsM\"",
            "<span class=\"rdr__tools\">${B.langs.length > 1 ? `<span class=\"rdr__lg\" role=\"group\">${B.langs.map(l => `<button type=\"button\" data-rl=\"${l}\" aria-pressed=\"${String(l === lang)}\">${l.toUpperCase()}</button>`).join('')}</span>` : ''}<button type=\"button\" id=\"rdFsM\"")
    # выбор языка книги следует за языком сайта: сменили язык сайта — книга переходит на него, если такой перевод есть
    s = rep(s, "    site = l;\n", "    if (site !== l && B && B.langs.indexOf(l) >= 0) { forced = ''; store.set('r11_rd_lang_' + bid, ''); }\n    site = l;\n")
    s = rep(s, "const hit = []; toc().forEach((x, i) => { const h = (x.t + ' ' + (x.code || '') + ' ' + (x.en || '')).toLowerCase();",
            "const tr = trees(), extra = {};                       /* коды и названия из всех трёх классификаций: страница находится и по F41.1 */\n"
            "  if (tr) ['icd', 'dsm', 'icd10'].forEach(k => (tr[k] || []).forEach(g => (g.items || []).forEach(it => { if (it.id) extra[it.id] = (extra[it.id] || '') + ' ' + (it.code || '') + ' ' + (it.t || ''); })));\n"
            "  const hit = []; toc().forEach((x, i) => { const h = (x.t + ' ' + (x.code || '') + ' ' + (x.en || '') + ' ' + (extra[x.id] || '')).toLowerCase();")
    s = rep(s, "<p class=\"rdr__n\">${x.code ? esc(x.code) : `${cur} ${esc(t.of)} ${N()}`}</p>", "${x.code ? `<p class=\"rdr__n\">${esc(x.code)}</p>` : ''}")
    s = rep(s, "<dl class=\"rdr__meta\">${(B.meta[lang] || []).map(m => `<div><dt>${esc(m[0])}</dt><dd>${esc(m[1])}</dd></div>`).join('')}</dl>${note}\n",
            "<dl class=\"rdr__meta\">${(B.meta[lang] || []).map(m => `<div><dt>${esc(m[0])}</dt><dd>${esc(m[1])}</dd></div>`).join('')}</dl>${note}\n    <p class=\"rdr__more\"><a class=\"sh__link\" href=\"book.html?b=${bid}\">${esc(t.about)}</a></p>\n")
    for lang, word in (("ru", "О книге, цена и заказ печатного издания"), ("az", "Kitab haqqında, qiymət və çap nüsxəsinin sifarişi"), ("en", "About the book, price and ordering a printed copy")):
        key = {"ru": "  ru: { toc: 'Содержание',", "az": "  az: { toc: 'Mündəricat',", "en": "  en: { toc: 'Contents',"}[lang]
        s = rep(s, key, key.replace("{ toc:", "{ about: '%s', toc:" % word))
    # старые адреса вида read.html?b=…#ch3
    s = rep(s, "    if (init) show(Math.min(startIdx(), N()), false, location.hash);", "    const oldCh = (location.hash.match(/^#ch(\\d+)$/) || [])[1];\n    if (init) show(Math.min(oldCh ? +oldCh : startIdx(), N()), false, oldCh ? '' : location.hash);")
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("читалка обновлена")

p = "_tools/libcommon.py"
s = io.open(p, encoding="utf-8").read()
if "TITLE_FIX" not in s:
    s = rep(s, "def finish(P):", '''# названия книг на английском пишутся по правилам заглавия (как на обложке и в каталоге)
TITLE_FIX = {("virus-viny", "en"): "The Guilt Virus", ("shizofreniya", "en"): "Schizophrenia. A Pandemic of Madness"}


def finish(P):''')
    s = rep(s, '    if P["id"] in OWN:\n', '    for (b, l), t in TITLE_FIX.items():\n        if P["id"] == b and l in P.get("t", {}):\n            P["t"][l] = t\n    if P["id"] in OWN:\n')
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("libcommon: названия")

p = "assets/css/site.css"
s = io.open(p, encoding="utf-8").read()
if "круг PG-05" not in s:
    s += """
/* RDR, круг PG-05: язык книги в полосе чтения, непрозрачная полоса, крупная область сноски, готовая обложка на титуле, поиск всегда на виду */
.rdr__bar { background: var(--bg); }
.rdr__lg { display: inline-flex; padding: var(--p2); border-radius: 99px; border: 1px solid var(--line); } .rdr__tools .rdr__lg button { min-width: 0; min-height: calc(var(--tap) - var(--p4) - 2px); padding: 0 var(--p10); border: 0; font: 600 12.5px/1 var(--f-sub); letter-spacing: .08em; color: var(--smoke); }
.rdr__tools .rdr__lg button[aria-pressed="true"] { background: var(--gold); color: var(--on-gold); }
.rdr__cover--img { padding: 0; background: none; } .rdr__cover--img::before { display: none; } .rdr__cover--img img { width: 100%; height: 100%; object-fit: cover; }
.rdr__body .fn-ref a { display: inline-block; min-width: 1.9em; padding: .55em .35em; margin: -.55em -.1em; text-align: center; font-size: .78em; }
.rdr__more { font-size: 15.5px; }
.rdr__toch { position: sticky; top: calc(var(--r2) * -1); z-index: 2; margin: calc(var(--r2) * -1) calc(var(--r1) * -1) var(--p14); padding: var(--r1) var(--r1) var(--p10); background: var(--bg); }
@media (max-width: 760px) { .rdr__bt { display: none; } .rdr__tools { flex: 1 1 auto; justify-content: flex-end; } .rdr__tools #rdTocB { padding: 0 var(--p10); } }
"""
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("стили читалки дополнены")
