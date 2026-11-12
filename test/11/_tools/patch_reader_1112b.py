# -*- coding: utf-8 -*-
"""Читалка — отдельный режим (слово владельца 12.11.2026). Повторный запуск ничего не меняет.
 • в читалке нет главного меню сайта, подвала и кнопки WhatsApp: остаётся одна полоса чтения;
 • один выбор языка: язык книги = язык текста, оглавления, кнопок и подписей (в том числе турецкий);
   выбор az/ru/en запоминается и как язык сайта — после выхода каталог открывается на нём же;
 • два выхода, как в прежнем ридере: логотип — на главную, «Все книги» — в каталог;
 • темы — в полосе чтения (на телефоне вместе с языком в панели «Содержание»)."""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)


def rep(s, a, b):
    assert s.count(a) == 1, "ожидалось 1, найдено %d: %s" % (s.count(a), a[:80])
    return s.replace(a, b)


p = "assets/js/reader.js"
s = io.open(p, encoding="utf-8").read()
if "rdr__home" not in s:
    s = rep(s, "};\nconst store = {", """  tr: { about: 'Kitap hakkında, fiyat ve basılı kitap siparişi', toc: 'İçindekiler', start: 'Okumaya başlayın', cont: 'Okumaya devam edin', prev: 'Geri', next: 'İleri', title: 'Başlık sayfası', lib: 'Tüm kitaplar', notes: 'Notlar', fs: 'Yazı boyutu',
        only: 'Bu kitabın yayımlandığı dil:', other: 'Başka dilde okuyun:', none: 'Kitap bulunamadı', ch: 'Bölüm', of: '/', close: 'Kapat', search: 'Kitapta arama', searchPh: 'Ad veya kod, örneğin 6B00', nores: 'Hiçbir şey bulunamadı', toggle: 'Grubu aç veya kapat', names: { az: 'Azerbaycan dili', ru: 'Rusça', en: 'İngilizce', tr: 'Türkçe' }, short: { az: 'Azərbaycanca', ru: 'По-русски', en: 'English', tr: 'Türkçe' } },
};
for (const k of Object.keys(U)) Object.assign(U[k], { home: { ru: 'На главную', az: 'Ana səhifə', en: 'Home', tr: 'Ana sayfa' }[k], theme: { ru: 'Тема', az: 'Mövzu', en: 'Theme', tr: 'Tema' }[k], lng: { ru: 'Язык книги', az: 'Kitabın dili', en: 'Book language', tr: 'Kitabın dili' }[k] });
const SITE = ['az', 'ru', 'en'];
const store = {""")
    # подписи читалки — на языке книги (а не сайта): заголовки и текст всегда на одном языке
    s = rep(s, "const u = () => U[site] || U.ru,", "const u = () => U[B ? lang : site] || U[site] || U.ru,")
    s = rep(s, "forced = store.get('r11_rd_lang_' + bid) || '';", "forced = '';")
    s = rep(s, "g.hidden = B.langs.length < 2; g.innerHTML = B.langs.map(l => `<button type=\"button\" data-rl=\"${l}\" aria-pressed=\"${String(l === lang)}\">${esc((t.short && t.short[l]) || l.toUpperCase())}</button>`).join(''); }",
            "g.innerHTML = (B.langs.length > 1 ? B.langs.map(l => `<button type=\"button\" data-rl=\"${l}\" aria-pressed=\"${String(l === lang)}\">${esc((t.short && t.short[l]) || l.toUpperCase())}</button>`).join('') : '') + themes(t); }")
    s = rep(s, "$('#rdBar').innerHTML = `<a class=\"rdr__lib\" href=\"shop.html\">← ${esc(t.lib)}</a>",
            "$('#rdBar').innerHTML = `<a class=\"logo rdr__home\" href=\"index.html\" aria-label=\"Doctor Ragimoff — ${esc(t.home)}\"><span class=\"logo__r\">R<i></i></span><span class=\"logo__w\">AGIMOFF</span></a><a class=\"rdr__lib\" href=\"shop.html\">← ${esc(t.lib)}</a>")
    s = rep(s, "<span class=\"rdr__lg\" role=\"group\">${B.langs.map(l => `<button type=\"button\" data-rl=\"${l}\" aria-pressed=\"${String(l === lang)}\">${l.toUpperCase()}</button>`).join('')}</span>` : ''}<button type=\"button\" id=\"rdFsM\"",
            "<span class=\"rdr__lg\" role=\"group\" aria-label=\"${esc(t.lng)}\">${B.langs.map(l => `<button type=\"button\" data-rl=\"${l}\" aria-pressed=\"${String(l === lang)}\">${l.toUpperCase()}</button>`).join('')}</span>` : ''}${themes(t)}<button type=\"button\" id=\"rdFsM\"")
    s = rep(s, "  const note = (B.langs.indexOf(site) < 0 ? `<p class=\"rdr__note\">${esc(t.only)} ${B.langs.map(l => esc(t.names[l] || l)).join(', ')}.</p>` : '') + (others.length", "  const note = (others.length")
    s = rep(s, "  document.title = B.t[lang] + ' — Doctor Ragimoff';", "  document.title = B.t[lang] + ' — Doctor Ragimoff'; document.documentElement.lang = lang;")
    s = rep(s, "function frame() {", """const themes = t => `<span class="seg rdr__th" role="group" aria-label="${esc(t.theme)}">${['night', 'paper', 'sepia'].map(k => `<button type="button" data-theme-btn="${k}" aria-label="${k}" aria-pressed="${String(document.documentElement.dataset.theme === k)}"><span class="dot dot--${k}"></span></button>`).join('')}</span>`;
/* язык книги: выбранный в читалке (турецкий хранится отдельно — у сайта его нет), иначе язык сайта, иначе первый язык издания */
function pick() {
  const f = (store.get('r11_rd_lang_' + bid) || '').split('|');
  if (f[0] && f[1] === site && B.langs.indexOf(f[0]) >= 0) return f[0];
  return B.langs.indexOf(site) >= 0 ? site : B.langs[0];
}
function frame() {""")
    s = rep(s, "    if (site !== l && B && B.langs.indexOf(l) >= 0) { forced = ''; store.set('r11_rd_lang_' + bid, ''); }\n    site = l;", "    if (!forced || SITE.indexOf(forced) < 0) site = l;")
    s = rep(s, "    const want = forced && B.langs.indexOf(forced) >= 0 ? forced : (B.langs.indexOf(site) >= 0 ? site : B.langs[0]);\n", "    const want = forced && B.langs.indexOf(forced) >= 0 ? forced : pick();\n")
    s = rep(s, "forced = rl.dataset.rl; store.set('r11_rd_lang_' + bid, forced); lang = forced; frame();",
            "forced = rl.dataset.rl; lang = forced;\n    if (SITE.indexOf(lang) >= 0) { site = lang; store.set('r11_lang', lang); store.set('r11_rd_lang_' + bid, ''); } else store.set('r11_rd_lang_' + bid, lang + '|' + site);   /* язык сайта идёт за языком книги */\n    frame();")
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("читалка: один язык, два выхода")

p = "assets/css/site.css"
s = io.open(p, encoding="utf-8").read()
if "RDR, режим чтения" not in s:
    s += """
/* RDR, режим чтения (12.11): в читалке нет меню сайта, подвала и кнопки WhatsApp — одна полоса: логотип, «все книги», язык книги, тема, шрифт, содержание */
body[data-kind="read"] .head, body[data-kind="read"] .mob, body[data-kind="read"] .foot, body[data-kind="read"] .fab { display: none; }
body[data-kind="read"] .rdr__bar { top: 0; min-height: var(--hd70); }
body[data-kind="read"] .pp__hero { padding-top: var(--r2); }
.rdr__home { margin-right: var(--p6); } .rdr__bar .rdr__th { flex: 0 0 auto; background: none; } .rdr__tools { align-items: center; }
.rdr__tools .rdr__th button { min-width: 34px; min-height: 0; height: 36px; padding: 0 var(--p6); border: 0; }
.rdr__lg--toc .rdr__th { display: none; }
@media (max-width: 900px) { .rdr__bar .rdr__th { display: none; } .rdr__home .logo__w { display: none; } .rdr__lg--toc { align-items: center; } .rdr__lg--toc .rdr__th { display: inline-flex; margin-left: auto; padding: var(--p2); border: 1px solid var(--line); border-radius: 99px; }
  .rdr__lg--toc .rdr__th button { min-height: 0; min-width: 38px; height: 38px; padding: 0; border: 0; display: grid; place-items: center; background: none; } .rdr__lg--toc .rdr__th button[aria-pressed="true"] { background: var(--gold); } }
"""
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("стили режима чтения")
