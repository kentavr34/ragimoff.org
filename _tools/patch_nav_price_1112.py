# -*- coding: utf-8 -*-
"""Замечания владельца 12.11.2026 (вечер). Повторный запуск ничего не меняет.
 1. Пункты главного меню ведут на свои страницы, а не на раздел главной:
    Тренинги → corporate.html, Консультации → consult.html?c=index, Обучение → program.html,
    Книги → shop.html, Блог → blog.html. (Специалисты — раздел главной: отдельной общей страницы нет.)
 2. Форма записи на долгие программы (общая, клиническая, практикум) показывает полную цену:
    в рассрочку — общая сумма, 12 месяцев и платёж в месяц; при оплате сразу — цена со скидкой;
    и пояснение, что выбор «сразу или в рассрочку» делается на странице оплаты после регистрации.
    Цены — те же, что на сервере оплаты (epoint_routes.TRAINING_PRICES): 3800/4200, 6000/6600, 3000/3600."""
import io, os, sys
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


p = "assets/js/chrome.js"
s = io.open(p, encoding="utf-8").read()
if "consult.html?c=index" not in s:
    s = rep(s, "{ k: 'books', href: home + '#books',", "{ k: 'books', href: L.shop || home + '#books',")
    s = rep(s, "{ k: 'edu', href: home + '#edu',", "{ k: 'edu', href: 'program.html',")
    s = rep(s, "{ k: 'cons', href: home + '#cons',", "{ k: 'cons', href: 'consult.html?c=index',")
    s = rep(s, "{ k: 'corp', href: home + '#corp', sub: [] }, { k: 'blog', href: home + '#blog', sub: [] }", "{ k: 'corp', href: L.corp || 'corporate.html', sub: [] }, { k: 'blog', href: L.blogAll || 'blog.html', sub: [] }")
    save(p, s)
    print("меню внутренних страниц: пункты ведут на страницы")

p = "assets/js/site.js"
s = io.open(p, encoding="utf-8").read()
if "consult.html?c=index" not in s:
    s = rep(s, "{ k: 'books', href: '#books',", "{ k: 'books', href: L.shop || '#books',")
    s = rep(s, "{ k: 'edu', href: '#edu',", "{ k: 'edu', href: 'program.html',")
    s = rep(s, "{ k: 'cons', href: '#cons',", "{ k: 'cons', href: 'consult.html?c=index',")
    s = rep(s, "{ k: 'corp', href: '#corp',", "{ k: 'corp', href: L.corp || 'corporate.html',")
    s = rep(s, "{ k: 'blog', href: '#blog', sub: [] }", "{ k: 'blog', href: L.blogAll || 'blog.html', sub: [] }")
    save(p, s)
    print("меню главной: пункты ведут на страницы")

p = "assets/js/reg.js"
s = io.open(p, encoding="utf-8").read()
if "LONG_P" not in s:
    s = rep(s, "const esc = s => String(s == null ? '' : s)", """/* долгие программы (общая, клиническая, практикум): [цена при оплате сразу, цена в рассрочку], AZN — как на сервере оплаты; слово владельца 12.11 */
const LONG_P = [[3800, 4200], [6000, 6600], [3000, 3600]], LONG_M = 12;
const LONG_T = {
  ru: { inst: 'в рассрочку на {m} месяцев — {x} AZN в месяц', now: 'При оплате сразу — {a} AZN, скидка {d} AZN', note: 'После регистрации система направит вас на страницу оплаты. Там можно оплатить всю сумму сразу со скидкой или выбрать рассрочку через официальную платёжную систему — на срок до 24 месяцев.' },
  az: { inst: '{m} aylıq hissə-hissə ödəniş — ayda {x} AZN', now: 'Birdəfəlik ödənişdə — {a} AZN, endirim {d} AZN', note: 'Qeydiyyatdan sonra sistem sizi ödəniş səhifəsinə yönləndirəcək. Orada məbləğin hamısını endirimlə birdəfəlik ödəyə və ya rəsmi ödəniş sistemi vasitəsilə 24 aya qədər hissə-hissə ödənişi seçə bilərsiniz.' },
  en: { inst: 'in instalments over {m} months — {x} AZN a month', now: 'If paid at once — {a} AZN, you save {d} AZN', note: 'After you register, the system will take you to the payment page. There you can pay the full amount at once with a discount or choose instalments through the official payment system — for up to 24 months.' },
};
const money = n => String(n).replace(/\\B(?=(\\d{3})+(?!\\d))/g, '\\u00A0');
const fill = (t, o) => t.replace(/\\{(\\w)\\}/g, (m, k) => o[k]);
const esc = s => String(s == null ? '' : s)""")
    s = rep(s, "  if (st.kind === 'edu') return { main: T.edu.p[st.prog].price, sub: T.edu.p[st.prog].m.join(' · ') };",
            "  if (st.kind === 'edu' && LONG_P[st.prog]) { const [a, b] = LONG_P[st.prog], L = LONG_T[lang] || LONG_T.ru;\n"
            "    return { main: money(b) + ' AZN', sub: fill(L.inst, { m: LONG_M, x: money(Math.round(b / LONG_M)) }), now: fill(L.now, { a: money(a), d: money(b - a) }), note: L.note }; }\n"
            "  if (st.kind === 'edu') return { main: T.edu.p[st.prog].price, sub: T.edu.p[st.prog].m.join(' · ') };")
    s = rep(s, "<p class=\"reg__ps\">${esc(pr.sub)}</p>` :", "<p class=\"reg__ps\">${esc(pr.sub)}</p>${pr.now ? `<p class=\"reg__now\">${esc(pr.now)}</p>` : ''}` :")
    s = rep(s, "<p class=\"reg__note\">${esc(k === 'b2b' ? r.noteB2b : T.cons.note)}</p>", "<p class=\"reg__note\">${esc(k === 'b2b' ? r.noteB2b : (pr.note || T.cons.note))}</p>")
    save(p, s)
    print("форма записи: полная цена, рассрочка, скидка при оплате сразу")

p = "assets/css/site.css"
s = io.open(p, encoding="utf-8").read()
if ".reg__now" not in s:
    s += "\n/* REG (12.11): цена при оплате сразу — строкой под ценой в рассрочку */\n.reg__now { font: 500 16px/1.4 var(--f-sub); color: var(--gold-hi); }\n"
    save(p, s)
