# -*- coding: utf-8 -*-
"""Правки движка по решениям владельца от 12.11.2026. Повторный запуск: «уже применено».
 3. «Юридические основы деятельности» — не страница, а блок на программах «Общая» и «Клиническая психология»;
    law.html остаётся переадресацией, все ссылки ведут на блок.
 5. Название «Ночной энурез (ночное мочеиспускание)» в общих текстах.
14. «Тревожные расстройства» и «ОКР» — две отдельные темы и две страницы (названия — по книге «Клиническая психиатрия»)."""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)


def rep(s, a, b, n=1):
    assert s.count(a) == n, "ожидалось %d, найдено %d: %s" % (n, s.count(a), a[:80])
    return s.replace(a, b)


p = "assets/js/content.js"
s = io.open(p, encoding="utf-8").read()
if "tesvis-pozuntulari" in s:
    print("уже применено")
    sys.exit(0)

# --- 14: две темы вместо одной (главная, форма записи, подвал)
s = rep(s, "['Тревожные расстройства и ОКР', 'У тревоги и навязчивостей есть чёткие критерии диагноза и лечение.']",
        "['Тревожные расстройства', 'Постоянная тревога, страхи и фобии: есть чёткие критерии диагноза и лечение.'],\n          ['Обсессивно-компульсивное расстройство (ОКР)', 'Навязчивые мысли и действия — расстройство, а не черта характера.']")
s = rep(s, "['Təşviş pozuntuları və OKP', 'Təşviş və obsessiyaların aydın diaqnostik meyarları və müalicəsi var.']",
        "['Təşviş və qorxu ilə əlaqəli pozuntular', 'Daimi təşviş, qorxular və fobiyalar: aydın diaqnostik meyarları və müalicəsi var.'],\n          ['Obsessiv-kompulsiv pozuntu (OKP)', 'Sarışan fikirlər və hərəkətlər xarakter xüsusiyyəti deyil, pozuntudur.']")
s = rep(s, "['Anxiety disorders and OCD', 'Anxiety and obsessions have clear diagnostic criteria and treatment.']",
        "['Anxiety disorders', 'Constant anxiety, fears and phobias have clear diagnostic criteria and treatment.'],\n          ['Obsessive-compulsive disorder (OCD)', 'Intrusive thoughts and actions are a disorder, not a character trait.']")
s = rep(s, "'Семейная терапия', 'Тревожные расстройства и ОКР']", "'Семейная терапия', 'Тревожные расстройства', 'Обсессивно-компульсивное расстройство (ОКР)']")
s = rep(s, "'Ailə terapiyası', 'Təşviş pozuntuları və OKP']", "'Ailə terapiyası', 'Təşviş və qorxu ilə əlaqəli pozuntular', 'Obsessiv-kompulsiv pozuntu (OKP)']")
s = rep(s, "'Family therapy', 'Anxiety disorders and OCD']", "'Family therapy', 'Anxiety disorders', 'Obsessive-compulsive disorder (OCD)']")
s = rep(s, "export const CONS = ['panik-ataklar', 'depressiya', 'sosial-fobiya', 'enurez', 'aile-terapiyasi', 'aile-usaq-terapiyasi', 'valideyn-mektebi'];",
        "export const CONS = ['panik-ataklar', 'depressiya', 'sosial-fobiya', 'enurez', 'aile-terapiyasi', 'tesvis-pozuntulari', 'okp', 'aile-usaq-terapiyasi', 'valideyn-mektebi'];\n"
        "/* страница консультации → номер темы в форме записи (порядок тем — T[l].cons.t) */\n"
        "export const CONS_TOPIC = { 'panik-ataklar': 0, depressiya: 1, 'sosial-fobiya': 2, enurez: 3, 'aile-terapiyasi': 4, 'aile-usaq-terapiyasi': 4, 'tesvis-pozuntulari': 5, okp: 6 };")
s = rep(s, "L.cons = ['panik-ataklar', 'depressiya', 'sosial-fobiya', 'enurez', 'aile-terapiyasi'].map(c => 'consult.html?c=' + c).concat('index.html#cons');",
        "L.cons = ['panik-ataklar', 'depressiya', 'sosial-fobiya', 'enurez', 'aile-terapiyasi', 'tesvis-pozuntulari', 'okp'].map(c => 'consult.html?c=' + c);")
# --- 5: название энуреза в списках услуг
s = rep(s, "['Ночной энурез', 'За годы практики", "['Ночной энурез (ночное мочеиспускание)', 'За годы практики")
s = rep(s, "['Gecə enurezi', 'Təcrübə illərində", "['Gecə enurezi (gecə sidik ifrazı)', 'Təcrübə illərində")
s = rep(s, "['Nocturnal enuresis', 'More than 1,000", "['Nocturnal enuresis (bedwetting)', 'More than 1,000")
s = rep(s, "'Социальная фобия', 'Ночной энурез', 'Семейная терапия'", "'Социальная фобия', 'Ночной энурез (ночное мочеиспускание)', 'Семейная терапия'")
s = rep(s, "'Sosial fobiya', 'Gecə enurezi', 'Ailə terapiyası'", "'Sosial fobiya', 'Gecə enurezi (gecə sidik ifrazı)', 'Ailə terapiyası'")
s = rep(s, "'Social phobia', 'Nocturnal enuresis', 'Family therapy'", "'Social phobia', 'Nocturnal enuresis (bedwetting)', 'Family therapy'")
# --- 3: правовой блок
s = rep(s, "L.contact = 'contact.html'; L.law = 'law.html';", "L.contact = 'contact.html'; L.law = 'program.html?p=general#law';")
s = rep(s, "['index.html#edu', 'index.html#edu', 'law.html', '/test/aile.html']", "['index.html#edu', 'index.html#edu', 'program.html?p=general#law', '/test/aile.html']")
s = rep(s, "cta: 'Записаться', law: 'Правовые основы' }", "cta: 'Записаться', law: 'Юридические основы' }")
s = rep(s, "law: 'Правовые основы', tests: 'Тесты'", "law: 'Юридические основы деятельности', tests: 'Тесты'")
s = rep(s, "law: 'Qanuni əsaslar', tests: 'Testlər'", "law: 'Fəaliyyətin hüquqi əsasları', tests: 'Testlər'")
s = rep(s, "law: 'Legal basis', tests: 'Tests'", "law: 'Legal basis for practice', tests: 'Tests'")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

p = "assets/js/page.js"
s = io.open(p, encoding="utf-8").read()
s = rep(s, "['law.html', u.pages.law, 'law']", "[L.law, u.pages.law, 'law']")
s = rep(s, "{ const i = CONS.indexOf(slug); regOpen('consult', i >= 0 && i < 5 ? i : (slug === 'aile-usaq-terapiyasi' ? 4 : t.cons.t.length), null, i >= 4 ? 'samira' : null); }",
        "{ const i = CONS_TOPIC[slug]; regOpen('consult', i != null ? i : t.cons.t.length, null, /^(aile|valideyn)/.test(slug) ? 'samira' : null); }")
assert "CONS_TOPIC" in s
s = s.replace("CONS,", "CONS, CONS_TOPIC,", 1) if "CONS," in s.split("from './content.js")[0] else s
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

p = "assets/js/blocks.js"
s = io.open(p, encoding="utf-8").read()
s = rep(s, "if (/^\\/telim\\/qanuni-esaslar/.test(q)) return 'law.html';", "if (/^\\/telim\\/qanuni-esaslar/.test(q)) return 'program.html?p=general#law';")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

p = "assets/js/page-program.js"
s = io.open(p, encoding="utf-8").read()
s = rep(s, "  sec('law', true); setTimeout(() => page && page.watch(), 0);",
        "  sec('law', true); setTimeout(() => page && page.watch(), 0);\n  if (location.hash === '#law' && !lawRender.done) { lawRender.done = true; setTimeout(() => $('#law').scrollIntoView(), 60); }   /* переход по ссылке «Юридические основы» */")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

p = "_tools/make_shells.py"
s = io.open(p, encoding="utf-8").read()
s = rep(s, '          "law": ("page", "law"), "blog"', '          "blog"')
s = rep(s, 'CONS = ["panik-ataklar", "depressiya", "sosial-fobiya", "enurez", "aile-terapiyasi", "aile-usaq-terapiyasi", "valideyn-mektebi"]',
        'CONS = ["panik-ataklar", "depressiya", "sosial-fobiya", "enurez", "aile-terapiyasi", "tesvis-pozuntulari", "okp", "aile-usaq-terapiyasi", "valideyn-mektebi"]')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

p = "_tools/pages_check.py"
s = io.open(p, encoding="utf-8").read()
s = rep(s, '"corporate.html", "law.html", "blog.html"]', '"corporate.html", "blog.html"]')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

# law.html — переадресация на блок (старые ссылки не ломаются)
io.open("law.html", "w", encoding="utf-8", newline="\n").write("""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex,nofollow">
<meta http-equiv="refresh" content="0; url=program.html?p=general#law">
<title>Doctor Ragimoff</title>
<script>location.replace('program.html?p=general#law');</script>
</head>
<body><a href="program.html?p=general#law">Doctor Ragimoff</a></body>
</html>
""")
print("применено")
