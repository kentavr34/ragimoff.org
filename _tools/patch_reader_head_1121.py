# -*- coding: utf-8 -*-
"""Разовая правка 21.11.2026 (слово Кенана): на телефоне в читалке кнопки A− и A+ теснили логотип в шапке.
Шапка читалки на узком экране становится такой же, как на остальных страницах (логотип, тема, язык, меню),
а A− и A+ переезжают в меню книги (боковая панель оглавления). На широком экране всё по-прежнему."""
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


p = "assets/js/reader.js"
sub(p, '''aria-label="${esc((t.short && t.short[l]) || l)}">${l.toUpperCase()}</button>`).join('')}</span>` : ''); }''',
    '''aria-label="${esc((t.short && t.short[l]) || l)}">${l.toUpperCase()}</button>`).join('')}</span>` : '')
      + `<span class="rdr__fs" role="group" aria-label="${esc(t.fs)}"><button type="button" data-fs="m" aria-label="${esc(t.fs)} −">A−</button><button type="button" data-fs="p" aria-label="${esc(t.fs)} +">A+</button></span>`; }''')
sub(p, "const fm = e.target.closest('#rdFsM'), fp = e.target.closest('#rdFsP');",
    "const fm = e.target.closest('#rdFsM, [data-fs=\"m\"]'), fp = e.target.closest('#rdFsP, [data-fs=\"p\"]');")
css = '''
/* ШАПКА ЧИТАЛКИ НА ТЕЛЕФОНЕ (слово Кенана 21.11.2026): та же, что на всех страницах — логотип, тема, язык, меню.
   Кнопки размера шрифта A− и A+ на узком экране стоят в меню книги, а не в шапке: пять кругляшек теснили логотип. */
.rdr__fs { display: none; }
@media (max-width: 600px) {
  .rdr__bar #rdFsM, .rdr__bar #rdFsP { display: none !important; }
  .rdr__lg--toc .rdr__fs { display: inline-flex; gap: var(--p6); margin-left: auto; }
  .rdr__lg--toc .rdr__fs button { min-width: var(--tap); min-height: var(--tap); padding: 0 var(--p12); border-radius: 99px; border: 1px solid var(--line); font: 600 14px/1 var(--f-sub); color: var(--text); }
}
'''
p = "assets/css/site.css"
t = io.open(p, encoding="utf-8").read()
if ".rdr__fs { display: none; }" not in t:
    io.open(p, "w", encoding="utf-8", newline="\n").write(t.rstrip("\n") + "\n" + css)
    print("изменён:", p)
