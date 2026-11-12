# -*- coding: utf-8 -*-
"""Пятый круг критика, страница книги и ссылки (12.11.2026). Повторный запуск ничего не меняет.
 • страница книги берёт оглавление из паспорта книги (у всех книг, а не только у Фрейда);
 • несуществующая книга — сообщение «книга не найдена», как в читалке;
 • малые тексты без «книжной» картинки (у двух была одна чужая обложка);
 • каталог открывается сразу на нужном авторе: shop.html#freud;
 • ссылки главной на «Клиническую психиатрию» ведут в новую читалку;
 • азербайджанское название энуреза — по книге: «gecə sidik buraxma»."""
import io, os, sys, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)


def rep(s, a, b):
    assert s.count(a) == 1, "ожидалось 1, найдено %d: %s" % (s.count(a), a[:80])
    return s.replace(a, b)


p = "assets/js/page-shop.js"
s = io.open(p, encoding="utf-8").read()
if "passToc" not in s:
    s = rep(s, "const cover = (it, lang, big) => it.cov", "const cover = (it, lang, big) => it.small ? `<span class=\"shp__ct shp__ct--plain\"><i>${esc(it.a)}</i><b${it.t.length > 34 ? ' class=\"is-long\"' : ''}>${esc(it.t)}</b><u>${esc(it.y)}</u></span>` : it.cov")
    s = rep(s, "const it = all.find(x => x.id === bid); if (!it) { location.replace('shop.html'); return; }                 /* нет такой книги — в каталог */",
            "const it = all.find(x => x.id === bid);\n  if (!it) { $('#shpHero').innerHTML = `<div class=\"shp__txt\"><h1 class=\"pp__t\">${esc(d.u.none || '—')}</h1><p class=\"pp__cta\"><a class=\"btn\" href=\"shop.html\">${esc(d.title)}</a></p></div>`; $('#shpBody').innerHTML = ''; return; }   /* нет такой книги — сообщение, как в читалке */")
    s = rep(s, "  const toc = it.toc ? `<section class=\"sec\">", "  const toc = `<div id=\"shpToc\"></div>`; passToc(it, d, lang);\n  const tocOld = it.toc ? `<section class=\"sec\">")
    s = rep(s, "function book(d, lang) {", '''/* оглавление страницы книги — из паспорта книги в библиотеке (один источник с читалкой) */
async function passToc(it, d, lang) {
  let P = null;
  try { const r = await fetch('books/' + it.id + '/book.json?v=' + V); P = r.ok ? await r.json() : null; } catch (e) { P = null; }
  const box = $('#shpToc'); if (!P || !box || bid !== it.id) return;
  const l = P.langs.indexOf(lang) >= 0 ? lang : P.langs[0], list = (P.toc[l] || []).filter(x => !x.lvl), max = 24;
  if (!list.length) return;
  const idx = x => P.toc[l].indexOf(x) + 1;
  box.innerHTML = `<section class="sec"><div class="wrap pp__two"><div><h2 class="pp__h rv">${esc(d.u.toc)}</h2></div><div>${l !== lang ? `<p class="shp__note rv">${esc(d.u.azNote)}</p>` : ''}<ol class="shp__toc rv" lang="${l}">${list.slice(0, max).map(x => `<li><a href="read.html?b=${it.id}&${x.id ? 'p=' + x.id : 'c=' + idx(x)}">${esc(x.t)}</a></li>`).join('')}</ol>${list.length > max ? `<p class="shp__note">${esc(d.u.more)} ${list.length - max}…</p>` : ''}</div></div></section>`;
  setTimeout(() => page && page.watch(), 0);
}

function book(d, lang) {''')
    s = rep(s, "let turn = 0, filter = 'all';", "let turn = 0, filter = (location.hash || '').replace('#', '') || 'all';          /* shop.html#freud — каталог сразу на нужном авторе */")
    s = rep(s, "$('#shpBody').innerHTML = d.groups.filter(g => filter === 'all' || filter === g.id)", "if (filter !== 'all' && !d.groups.some(g => g.id === filter)) filter = 'all';\n  $('#shpBody').innerHTML = d.groups.filter(g => filter === 'all' || filter === g.id)")
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("страница книги обновлена")

p = "_tools/build_shop.py"
s = io.open(p, encoding="utf-8").read()
if '"none": ' not in s:
    s = rep(s, '"toc": h[9], "azNote": h[10], "more": h[11]}', '"toc": h[9], "azNote": h[10], "more": h[11], "none": {"ru": "Книга не найдена", "az": "Kitab tapılmadı", "en": "Book not found"}[lang]}')
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)

p = "assets/js/content.js"
s = io.open(p, encoding="utf-8").read()
if "toReader" not in s:
    s = rep(s, "  L.shop = 'shop.html';", '''  /* ссылки на «Клиническую психиатрию» (старые страницы книги) ведут в единую читалку: …/6A70.html#якорь → read.html?b=klinik-psixiatriya&p=6A70#якорь */
  const toReader = v => typeof v === 'string' ? v.replace(/^\\/klinik-psixiatriya\\/(?:(?:ru|en|tr)\\/)?(?:index\\.html)?(#.*)?$/, 'read.html?b=klinik-psixiatriya$1').replace(/^\\/klinik-psixiatriya\\/(?:(?:ru|en|tr)\\/)?([\\w-]+)\\.html(#.*)?$/, 'read.html?b=klinik-psixiatriya&p=$1$2') : Array.isArray(v) ? v.map(toReader) : v;
  for (const k of Object.keys(L)) L[k] = toReader(L[k]);
  L.shop = 'shop.html';''')
    s = rep(s, "L.books = ['read.html?b=klinik-psixiatriya', 'shop.html',", "L.books = ['read.html?b=klinik-psixiatriya', 'shop.html#freud',")
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("ссылки главной на книгу ведут в читалку")

n = 0
for fn in glob.glob("data/*/*.json") + ["assets/js/content.js", "_tools/patch_owner_1112.py", "_tools/patch_catalog_1112.py"]:
    t = io.open(fn, encoding="utf-8").read()
    t2 = t.replace(u"Gecə enurezi (gecə sidik saxlamama)", u"Gecə enurezi (gecə sidik buraxma)")
    if t2 != t and "patch_catalog" not in fn:
        io.open(fn, "w", encoding="utf-8", newline="\n").write(t2)
        n += 1
print("азербайджанское название энуреза:", n)

p = "assets/css/site.css"
s = io.open(p, encoding="utf-8").read()
if "shp__ct--plain" not in s:
    s += """
/* SHP, круг PG-05: малые тексты — обложка без картинки; ссылки оглавления на странице книги */
.shp__ct--plain { background: linear-gradient(160deg, color-mix(in srgb, var(--gold) 14%, #0A0D14), #07090E 70%); border: 1px solid color-mix(in srgb, var(--gold) 45%, transparent); text-shadow: none; }
.shp__toc li a { color: inherit; transition: color var(--t1); } .shp__toc li a:hover { color: var(--gold-hi); }
"""
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
