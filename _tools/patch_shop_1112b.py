# -*- coding: utf-8 -*-
"""Каталог книг — одна карточка для всех книг (слово владельца 12.11.2026, вечер). Повторный запуск ничего не меняет.
 • свои книги и книги Фрейда показываются одинаково: обложка, название, сведения, цена, две кнопки;
 • кнопки на каждой карточке и на странице книги: «Читать бесплатно» и «В корзину»;
 • набор «Все книги Фрейда» со скидкой — первым в разделе Фрейда;
 • книги Фрейда — одним списком в хронологическом порядке;
 • корзина — та же, что у страницы заказа (/books/#sebet): названия и цены позиций берутся с неё
   (assets/js/shop-order.js собирается из books/index.html), оформление и оплата остаются там."""
import io, os, re, sys, json
from bs4 import BeautifulSoup
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)


def rep(s, a, b):
    assert s.count(a) == 1, "ожидалось 1, найдено %d: %s" % (s.count(a), a[:80])
    return s.replace(a, b)


def save(p, s):
    t = p + ".new"
    io.open(t, "w", encoding="utf-8", newline="\n").write(s)
    os.replace(t, p)


# 1. позиции корзины: книга → название и цена, как на странице заказа
soup = BeautifulSoup(io.open("books/index.html", encoding="utf-8").read(), "html.parser")
items, bundle = {}, None
for b in soup.select("[data-cart-btn]"):
    title, price = b.get("data-order", ""), b.get("data-price", "")
    if "kolleksiya" in title.lower():
        bundle = {"o": title, "p": price}
        continue
    c, href = b, None
    for _ in range(8):
        c = c.parent
        if c is None:
            break
        a = c.select_one('a[href^="/books/"], a[href^="/klinik"]')
        if a:
            href = a["href"]
            break
    if not href:
        continue
    bid = "klinik-psixiatriya" if href.startswith("/klinik") else href.split("/")[2]
    items[bid] = {"o": title, "p": price}
if bundle:
    bp = int(re.sub(r"\D", "", bundle["p"]) or 0)                    # цена набора со страницы заказа; полная цена и число книг — из неё (скидка 10 %, книга 30)
    full = round(bp / 0.9)
    n = full // 30
    bundle.update({"n": n, "full": full})
js = "/* Позиции корзины: название и цена каждой книги, как на странице заказа /books/ (собирает _tools/patch_shop_1112b.py). */\nexport const ORD = " + json.dumps({"items": items, "bundle": bundle}, ensure_ascii=False, indent=1) + ";\n"
save("assets/js/shop-order.js", js)
print("позиций корзины:", len(items), "набор:", bundle)

# 2. страница каталога
p = "assets/js/page-shop.js"
s = io.open(p, encoding="utf-8").read()
if "shop-order.js" not in s:
    s = rep(s, "import { fixImg } from './blocks.js", "import { ORD } from './shop-order.js?v=11122335';\nimport { fixImg } from './blocks.js")
    a = s.index("const btns = (it, d) =>")
    b = s.index("const line = it =>")
    new_cards = r'''/* корзина — общая со страницей заказа /books/ (тот же ключ в памяти браузера): здесь книга добавляется, оформление и оплата — там */
const CKEY = 'ragimoff_cart_v1';
const CT = {
  ru: { read: 'Читать бесплатно', add: 'В корзину', added: 'Добавлено', cart: 'Корзина', go: 'оформить заказ', set: 'Все книги Фрейда одним набором', setN: 'книг', setOld: 'вместо', setOff: 'скидка', setAdd: 'Весь набор в корзину' },
  az: { read: 'Pulsuz oxuyun', add: 'Səbətə at', added: 'Əlavə edildi', cart: 'Səbət', go: 'sifarişi rəsmiləşdirin', set: 'Freydin bütün kitabları bir dəstdə', setN: 'kitab', setOld: 'əvəzinə', setOff: 'endirim', setAdd: 'Bütün dəsti səbətə atın' },
  en: { read: 'Read for free', add: 'Add to cart', added: 'Added', cart: 'Cart', go: 'place the order', set: 'All of Freud’s books as one set', setN: 'books', setOld: 'instead of', setOff: 'discount', setAdd: 'Add the whole set to cart' },
};
const ct = lang => CT[lang] || CT.ru;
const cartRead = () => { try { return JSON.parse(localStorage.getItem(CKEY) || '[]') || []; } catch (e) { return []; } };
function cartAdd(o) { const a = cartRead(), x = a.find(i => i.title === o.o); if (x) x.qty = (x.qty || 1) + 1; else a.push({ title: o.o, qty: 1, price: o.p }); try { localStorage.setItem(CKEY, JSON.stringify(a)); } catch (e) {} }
function cartNote(lang) { const n = cartRead().reduce((s2, i) => s2 + (i.qty || 1), 0), T = ct(lang); $$('.shp__cart').forEach(el => { el.innerHTML = n ? `<a class="btn btn--line btn--sm" href="/books/#sebet">${esc(T.cart)}: ${n} · ${esc(T.go)}</a>` : ''; }); }
/* две кнопки книги: читать и в корзину — одни и те же в карточке каталога и на странице книги */
const acts = (it, lang) => { const T = ct(lang), o = ORD.items[it.id];
  return `<div class="shp__acts">${it.read ? `<a class="btn btn--sm" href="${esc(it.read_new || it.href)}">${esc(T.read)}</a>` : ''}${o ? `<button type="button" class="btn btn--line btn--sm" data-cart="${esc(it.id)}">${esc(T.add)}</button>` : ''}</div>`; };
const btns = (it, d, lang) => `<div class="shp__btns">${it.read ? '' : `<span class="shp__soon">${esc(d.u.soon)}</span>`}${acts(it, lang)}<p class="shp__cart"></p></div>`;

/* ЕДИНАЯ КАРТОЧКА КНИГИ: обложка, название, сведения, цена, две кнопки. Одна на все книги каталога и на блок «Другие книги» —
   изменение здесь меняет вид всех книг сразу. Малые тексты (несколько страниц) выводятся строкой без обложки. */
const card = (it, lang) => `<article class="shp__card rv"><a class="shp__cv" href="${url(it)}" aria-label="${esc(it.t)}">${cover(it, lang)}</a><div class="shp__cb"><a class="shp__ctl" href="${url(it)}"><b>${esc(it.t)}</b></a><span>${esc(it.meta)}</span>${it.price ? `<em>${esc(it.price)}</em>` : ''}${acts(it, lang)}</div></article>`;
'''
    s = s[:a] + new_cards + s[b:]
    a = s.index("function shop(d, lang) {")
    b = s.index("/* оглавление страницы книги")
    new_shop = r'''function shop(d, lang) {
  const all = d.groups.flatMap(g => g.items), T = ct(lang);
  $('#shpHero').innerHTML = `<h1 class="pp__t">${esc(d.title)}</h1><p class="pp__lead">${esc(d.lead)}</p>
    <div class="shp__chips" role="group">${[['all', d.u.all, all.length]].concat(d.groups.map(g => [g.id, g.name, g.items.length])).map(c => `<button type="button" class="chip" data-f="${c[0]}" aria-pressed="${String(filter === c[0])}">${esc(c[1])} <i>${c[2]}</i></button>`).join('')}</div><p class="shp__cart"></p>`;
  if (filter !== 'all' && !d.groups.some(g => g.id === filter)) filter = 'all';
  const yr = it => +((String(it.meta).match(/\b(1[89]\d\d|20\d\d)\b/) || [0, 9999])[1]);
  $('#shpBody').innerHTML = d.groups.filter(g => filter === 'all' || filter === g.id).map(g => {
    const books = g.items.filter(it => !it.small), small = g.items.filter(it => it.small), B = ORD.bundle;
    /* книги Фрейда — одним списком по времени написания, от ранних к поздним */
    const items = g.id === 'freud' ? books.map((it, i) => [yr(it), i, it]).sort((x, y) => x[0] - y[0] || x[1] - y[1]).map(x => x[2]) : books;
    const set = g.id === 'freud' && B ? `<div class="shp__set rv"><div><h3 class="shp__sett">${esc(T.set)}</h3><p class="shp__setm">${B.n} ${esc(T.setN)} · <b>${esc(B.p.replace('₼', 'AZN'))}</b> ${esc(T.setOld)} ${B.full} AZN · ${esc(T.setOff)} ${Math.round(100 - 100 * parseInt(B.p, 10) / B.full)} %</p></div><button type="button" class="btn" data-cart="bundle">${esc(T.setAdd)}</button></div>` : '';
    const sm = small.length ? `<h3 class="shp__sh rv"><span>${esc(((g.sub || []).find(x => x.id === 'small') || {}).t || '')}</span><i>${small.length}</i></h3><p class="shp__note rv">${esc(g.smallNote || '')}</p><ul class="shp__lines rv">${small.map(line).join('')}</ul>` : '';
    return `<section class="sec shp__grp" data-g="${g.id}"><div class="wrap"><header class="shp__gh rv"><h2 class="shp__gt">${esc(g.name)}</h2><span class="shp__gn">${g.items.length}</span></header>${set}${grid(items, lang)}${sm}</div></section>`;
  }).join('');
  document.title = d.title + ' — Doctor Ragimoff';
  cartNote(lang);
}

'''
    s = s[:a] + new_shop + s[b:]
    s = rep(s, "${price(it, d.u)}${btns(it, d)}</div></div>`;\n  const toc = ", "${price(it, d.u)}${btns(it, d, lang)}</div></div>`;\n  const toc = ")
    s = rep(s, "    ${grid(other, lang)}</div></section>`;\n  document.title = it.t + ' — Doctor Ragimoff';", "    ${grid(other, lang)}</div></section>`;\n  document.title = it.t + ' — Doctor Ragimoff';\n  cartNote(lang);")
    s = rep(s, "document.addEventListener('click', e => {\n  const c = e.target.closest('.shp__chips .chip'); if (!c) return;",
            "document.addEventListener('click', e => {\n  const cb = e.target.closest('[data-cart]');\n  if (cb) { const lang = document.documentElement.lang, o = cb.dataset.cart === 'bundle' ? ORD.bundle : ORD.items[cb.dataset.cart]; if (o) { cartAdd(o); cb.textContent = ct(lang).added; cb.classList.add('is-added'); cartNote(lang); } return; }\n  const c = e.target.closest('.shp__chips .chip'); if (!c) return;")
    save(p, s)
    print("каталог: единая карточка, кнопки, набор, корзина")

p = "assets/css/site.css"
s = io.open(p, encoding="utf-8").read()
if ".shp__acts" not in s:
    s += """
/* SHP (12.11, вечер): единая карточка книги с двумя кнопками, набор «Все книги Фрейда», ссылка на корзину */
.shp__ctl { color: inherit; } .shp__cb em { margin-top: 0; }
.shp__acts { display: flex; flex-wrap: wrap; gap: var(--p8); margin-top: auto; padding-top: var(--p10); }
.shp__acts .btn { flex: 1 1 auto; min-height: var(--tap); padding: 0 var(--p14); font-size: 14px; white-space: nowrap; }
.shp__acts .btn.is-added { background: var(--gold); color: var(--on-gold); }
.shp__btns { flex-direction: column; align-items: flex-start; } .shp__btns .shp__acts { margin-top: 0; padding-top: 0; } .shp__btns .shp__acts .btn { flex: 0 1 auto; min-height: var(--btn-h); padding: 0 var(--p24); font-size: 15px; }
.shp__cart { min-height: 0; } .shp__cart:empty { display: none; } .shp__cart .btn { min-height: var(--tap); }
.shp__set { display: flex; align-items: center; justify-content: space-between; gap: var(--r1); flex-wrap: wrap; margin-top: var(--r2); padding: var(--r1) var(--r2); border: 1px solid color-mix(in srgb, var(--gold) 50%, transparent); border-radius: var(--p16); background: color-mix(in srgb, var(--gold) 7%, transparent); }
.shp__sett { font: 400 clamp(22px, 2.2vw, 30px)/1.15 var(--f-display); color: var(--milk); } .shp__setm { font: 400 15px/1.5 var(--f-sub); color: var(--text); margin-top: var(--p6); } .shp__setm b { color: var(--gold-hi); font-weight: 600; }
@media (max-width: 760px) { .shp__acts .btn { flex: 1 1 100%; } .shp__set { padding: var(--r1); } .shp__set .btn { width: 100%; white-space: normal; } }
"""
    save(p, s)
    print("стили карточки")
