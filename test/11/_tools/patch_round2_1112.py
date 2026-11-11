# -*- coding: utf-8 -*-
"""Правки по второму кругу критика (12.11.2026). Повторный запуск: «уже применено» / 0 изменений.
ДАННЫЕ
 1. Кенан, дипломы: четыре файла названы не по содержимому (сверено глазами 12.11): подпись теперь стоит под своим документом.
ДВИЖОК
 2. список: содержимое пункта одним блоком (курсив внутри не разваливает строку на колонки и не раздвигает страницу);
 3. пустые заголовки h3 не выводятся; длинный заголовок карточки — меньшим кеглем;
 4. блог: пустые рубрики не показываются;
 5. последний блок-призыв перед формой записи и второй подряд список статей не выводятся;
 6. форма записи открывается с темой страницы (Самира → семейная терапия; статья → тема статьи);
 7. ссылка «Тесты» ведёт на страницу теста, а не на архив версий дизайна."""
import io, os, json, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)


def rep(s, a, b, n=1):
    assert s.count(a) == n, "ожидалось %d: %s" % (n, a[:80])
    return s.replace(a, b)


# 1. дипломы: подпись → файл с этим документом
SWAP = {"/images/diplomas/ipas-ambassador-2022.jpg": "/images/diplomas/adtu-diplom-2000.jpg",      # под «Амбассадор IPAS» — сертификат IPAS
        "/images/diplomas/bekhterev-udost-2.jpg": "/images/diplomas/nlp-diploma-1999.jpg",          # под «Институт Бехтерева» — удостоверение института
        "/images/diplomas/adtu-diplom-2000.jpg": "/images/diplomas/ipas-ambassador-2022.jpg",       # под «АГМУ Диплом 2000» — диплом университета
        "/images/diplomas/nlp-diploma-1999.jpg": "/images/diplomas/bekhterev-udost-2.jpg"}          # под «Диплом НЛП 1999» — диплом НЛП
for lang in ("ru", "az", "en"):
    fn = "data/spec/kenan.%s.json" % lang
    d = json.load(io.open(fn, encoding="utf-8"))
    if d.get("_gal_fixed"):
        continue
    for b in d["blocks"]:
        if b["type"] == "gallery":
            for it in b["items"]:
                it["src"] = SWAP.get(it["src"], it["src"])
    d["_gal_fixed"] = True
    json.dump(d, io.open(fn, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    print("дипломы:", fn)

p = "assets/js/blocks.js"
s = io.open(p, encoding="utf-8").read()
if "grp__t--long" in s:
    print("движок: уже применено")
    sys.exit(0)
s = rep(s, """<ul class="facts pp__list rv">${b.items.map(x => `<li>${rich(x)}</li>`).join('')}</ul>`""",
        """<ul class="facts pp__list rv">${b.items.map(x => `<li><span>${rich(x)}</span></li>`).join('')}</ul>`""")
s = rep(s, """<h3 class="pc2__t">${rich(x.t)}</h3>""", """${x.t ? `<h3 class="pc2__t">${rich(x.t)}</h3>` : ''}""")
s = rep(s, """<h3 class="tl__t">${rich(x.t)}</h3>""", """${x.t ? `<h3 class="tl__t">${rich(x.t)}</h3>` : ''}""")
s = rep(s, """<h3 class="grp__t">${rich(x.t)}</h3>""", """<h3 class="grp__t${String(x.t || '').length > 70 ? ' grp__t--long' : ''}">${rich(x.t)}</h3>""")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

p = "assets/js/page.js"
s = io.open(p, encoding="utf-8").read()
s = rep(s, "${d.cats.map(c => `<button", "${d.cats.filter(c => c[0] === 'all' || d.items.some(x => x.cat === c[0])).map(c => `<button")
s = rep(s, "    let blocks = d.blocks || [];",
        """    let blocks = (d.blocks || []).slice();
    while (blocks.length && blocks[blocks.length - 1].type === 'cta') blocks.pop();                    /* призыв прямо перед формой записи лишний: форма ниже */
    let seenArt = false; blocks = blocks.filter(b => { if (b.type !== 'articles') return true; if (seenArt) return false; seenArt = true; return true; });   /* второй список статей подряд не нужен */""")
s = rep(s, "    if (kind === 'spec') regOpen('consult', null, null, slug);",
        """    const TOPIC = [['panik', 0], ['depressiya', 1], ['sosial-fobiya', 2], ['enurez', 3], ['aile', 4], ['yeniyetme', 4]];
    if (kind === 'spec') regOpen('consult', slug === 'samira' ? 4 : null, null, slug);
    else if (kind === 'post') { const m = TOPIC.find(x => slug.indexOf(x[0]) === 0); if (m) regOpen('consult', m[1], null, m[1] === 4 ? 'samira' : 'kenan'); }""")
s = rep(s, "$('#pgBlocks').innerHTML = kind === 'blog' ? blogPage(d, u) + (d.cta ? renderBlocks([Object.assign({ type: 'cta' }, d.cta)], u, { t, blog }) : '') : renderBlocks(blocks, u, { t, blog });",
        "$('#pgBlocks').innerHTML = kind === 'blog' ? blogPage(d, u) : renderBlocks(blocks, u, { t, blog });")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

p = "assets/js/content.js"
s = io.open(p, encoding="utf-8").read()
s = rep(s, "L.tests = '/test/';", "L.tests = '/test/aile.html';")
s = rep(s, "['index.html#edu', 'index.html#edu', 'law.html', '/test/']", "['index.html#edu', 'index.html#edu', 'law.html', '/test/aile.html']")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

p = "_tools/pages_check.py"
s = io.open(p, encoding="utf-8").read()
s = rep(s, "  const W = innerWidth;", "  const W = __W__;                      /* заданная ширина экрана: при переполнении браузер сам расширяет окно просмотра */")
s = rep(s, 'expression=JS, returnByValue', 'expression=JS.replace("__W__", str(W)), returnByValue')
s = rep(s, "  out.tap = W < 700 ?", "  out.vw = innerWidth;\n  out.tap = W < 700 ?")
s = rep(s, '                        if o.get("over", 0) > 1:', '                        if o.get("vw", W) > W + 1: v.append("страница раздвинута до %d px" % o["vw"])\n                        if o.get("over", 0) > 1:')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("движок: применено")
