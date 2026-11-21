# -*- coding: utf-8 -*-
"""Разовая правка 21.11.2026 (слово Кенана): чтение английских версий четырёх книг на сайте закрыто.
Вносит правило libcommon.CLOSED_READ в сборщики, сценарий магазина, читалку и стили. Повторный запуск ничего не меняет."""
import io, os, sys
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def sub(p, a, b):
    t = io.open(p, encoding="utf-8").read()
    if b in t:
        print("уже есть:", p)
        return
    assert a in t, (p, a[:70])
    io.open(p, "w", encoding="utf-8", newline="\n").write(t.replace(a, b, 1))
    print("изменён:", p)


# сборщик книги из Print: вместо отрывка — закрытое чтение
p = "_tools/build_book_print.py"
t = io.open(p, encoding="utf-8").read()
if "EXCERPT" in t:
    a, b = t.index("# Слово Кенана 21.11.2026: английская электронная"), t.index('pj = "books/%s/book.json" % bid')
    t = t[:a] + "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport libcommon\n" + t[b:]
    a, b = t.index("    if (bid, lang) in EXCERPT:"), t.index("    toc = []\n")
    t = t[:a] + "    closed = (bid, lang) in libcommon.CLOSED_READ           # чтение закрыто: оглавление остаётся, текст на сайт не пишется\n" + t[b:]
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("изменён:", p, "(отрывок убран)")
sub(p, r'''        wrote += save("books/%s/%s/%03d.html" % (bid, lang, i), body + "\n")''',
    r'''        if not closed:
            wrote += save("books/%s/%s/%03d.html" % (bid, lang, i), body + "\n")''')
sub(p, "        if int(os.path.basename(old)[:-5]) > len(toc):", "        if closed or int(os.path.basename(old)[:-5]) > len(toc):")
sub(p, '    P["toc"][lang] = toc\n',
    '    P["toc"][lang] = toc\n    P["closed"] = sorted((set(P.get("closed", [])) - {lang}) | ({lang} if closed else set()))\n')

# учебник
sub("_tools/build_klinik.py", r'''            wrote += write(os.path.join(OUT, lang, "%03d.html" % n), body + "\n")''',
    r'''            if ("klinik-psixiatriya", lang) not in libcommon.CLOSED_READ:   # закрытое чтение: текст на сайт не пишется
                wrote += write(os.path.join(OUT, lang, "%03d.html" % n), body + "\n")''')

# каталог магазина
sub("_tools/build_shop.py", '''            it["read_new"] = "read.html?b=" + lib               # единая читалка новой системы\n''',
    '''            it["read_new"] = "read.html?b=" + lib               # единая читалка новой системы
        if (lib, lang) in libcommon.CLOSED_READ:                # чтение закрыто: кнопка «Читать» неактивна
            it["read"], it["closed"] = False, True
''')

# сценарий магазина: неактивная кнопка, оглавление без ссылок
p = "assets/js/page-shop.js"
sub(p, '''${it.read ? `<a class="btn btn--sm" href="${esc(it.read_new || it.href)}">${esc(T.read)}</a>` : ''}''',
    '''${it.read ? `<a class="btn btn--sm" href="${esc(it.read_new || it.href)}">${esc(T.read)}</a>` : (it.closed ? `<span class="btn btn--sm btn--off" aria-disabled="true">${esc(T.read)}</span>` : '')}''')
sub(p, '''${it.read ? '' : `<span class="shp__soon">${esc(d.u.soon)}</span>`}''',
    '''${it.read || it.closed ? '' : `<span class="shp__soon">${esc(d.u.soon)}</span>`}''')
sub(p, '''map(x => `<li><a href="read.html?b=${it.id}&${x.id ? 'p=' + x.id : 'c=' + idx(x)}">${esc(x.t)}</a></li>`)''',
    '''map(x => (P.closed || []).indexOf(l) >= 0 ? `<li><span>${esc(x.t)}</span></li>` : `<li><a href="read.html?b=${it.id}&${x.id ? 'p=' + x.id : 'c=' + idx(x)}">${esc(x.t)}</a></li>`)''')

# читалка: закрытый язык не предлагается
sub("assets/js/reader.js", "B = r.ok ? await r.json() : false; } catch (e) { B = false; }",
    "B = r.ok ? await r.json() : false; } catch (e) { B = false; }\n"
    "  if (B && B.closed) B.langs = B.langs.filter(l => B.closed.indexOf(l) < 0);   /* чтение на этом языке закрыто (libcommon.CLOSED_READ) */")

# вид неактивной кнопки
sub("assets/css/site.css", ".btn--sm { min-height: 46px;",
    ".btn--off, .btn--off:hover { background: transparent; color: var(--smoke); border: 1px solid color-mix(in srgb, var(--smoke) 45%, transparent); box-shadow: none; cursor: not-allowed; opacity: .7; }\n.btn--sm { min-height: 46px;")
