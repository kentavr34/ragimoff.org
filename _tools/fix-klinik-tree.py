# -*- coding: utf-8 -*-
"""
_tools/fix-klinik-tree.py — «Клиническая психиатрия»: вернуть прежнюю структуру книги.

Что делает (только klinik-psixiatriya, все языки):
 1. Раскрывающиеся группы в рейке. В прежней разметке это были
    .nav-item.nav-has-sub + .nav-toggle(▶) + .nav-sub + toggleSub(); при пересборке
    дерево стало плоским списком .bk-row--sec / .bk-row--sub, и все ~170 000
    подпунктов разом вываливались в меню. Собираем обратно: группа = .bk-grp
    (заголовок .bk-row--sec + кнопка .bk-tgl + .bk-grp__sub), закрыта по умолчанию,
    группа текущей страницы открыта — как «Auto-expand active chapter» в прежнем скрипте.
 2. Единый регистр названий: капс в рейке (OBSESSİV-KOMPULSİV) → обычный, как у
    остальных пунктов (nice_case из пересборщика; аббревиатуры OKP/DSM/XBT и коды
    F01–F05 сохраняются).
 3. Убирает лишний код в названии раздела (заголовок + код диапазона дублировался:
    «Neyroinkişaf pozuntuları6A00–6A0Z» — код уже стоит в колонке номера).
 4. Ставит скрипт раскрытия/закрытия и запоминает позицию прокрутки рейки.

Запуск:
    python _tools/fix-klinik-tree.py --dry
    python _tools/fix-klinik-tree.py
"""
import argparse
import html
import importlib.util
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = "klinik-psixiatriya"
SKIP_DIRS = ("test", ".bak")

_spec = importlib.util.spec_from_file_location("rc", os.path.join(ROOT, "_tools", "rebuild-concept.py"))
RC = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(RC)

SCRIPT = """
<script>/* дерево классификаций: раскрывающиеся группы (прежнее поведение книги) */
(function(){
  var cur = (location.pathname.split('/').pop() || '').replace(/\\.html$/, '');
  var sb = document.querySelector('.bk-sb');
  document.querySelectorAll('.bk-grp').forEach(function(g){
    var tgl = g.querySelector('.bk-tgl'), sub = g.querySelector('.bk-grp__sub');
    if (!tgl || !sub) return;
    function set(open){
      g.classList.toggle('is-open', open);
      tgl.setAttribute('aria-expanded', open ? 'true' : 'false');
    }
    set(g.getAttribute('data-here') === '1');   // группа текущей страницы — сразу раскрыта
    tgl.addEventListener('click', function(){
      var top = sb ? sb.scrollTop : 0;
      set(!g.classList.contains('is-open'));
      if (sb) requestAnimationFrame(function(){ sb.scrollTop = top; });
    });
  });
  setTimeout(function(){
    var open = sb && sb.querySelector('.bk-grp.is-open');
    if (open) { var t = open.offsetTop - Math.round(sb.offsetHeight / 3); if (t > 0) sb.scrollTop = t; }
  }, 80);
})();</script>
"""

TAG_A = re.compile(r'<a class="([^"]*bk-row--(sec|sub)[^"]*)"([^>]*)>(.*?)</a>', re.S)
T_RE = re.compile(r'(<span class="bk-row__t">)(.*?)(</span>)', re.S)


def clean_name(name, lang):
    """nice_case + снятие приклеенного кода диапазона."""
    name = re.sub(r"\s+", " ", name).strip()
    out = RC.nice_case(name, lang)
    return out


def split_rows(block):
    """Раскладывает содержимое .cls-tree на строки (a / прочее)."""
    items = []
    pos = 0
    for m in TAG_A.finditer(block):
        if block[pos:m.start()].strip():
            items.append(("raw", block[pos:m.start()]))
        items.append(("row", m))
        pos = m.end()
    if block[pos:].strip():
        items.append(("raw", block[pos:]))
    return items


def build(block, lang, here):
    """Плоский список строк → группы с раскрытием."""
    out = []
    grp = None      # открытая группа: (slug, [строки])

    def flush():
        nonlocal grp
        if grp is None:
            return
        slug, rows = grp
        if len(rows) == 1:                       # раздел без подпунктов — как был
            out.append(rows[0])
        else:
            # группа текущей страницы раскрыта сразу: совпал сам раздел или его подпункт
            is_here = "1" if (slug == here or re.search(r'href="%s\.html"' % re.escape(here),
                                                        "".join(rows[1:]))) else "0"
            out.append('<div class="bk-grp" data-slug="%s" data-here="%s">\n%s\n'
                       '<button class="bk-tgl" type="button" tabindex="-1" aria-expanded="false" '
                       'aria-label="Aç / bağla">\u25b6</button>\n'
                       '<div class="bk-grp__sub">\n%s\n</div>\n</div>'
                       % (slug, is_here, rows[0], "\n".join(rows[1:])))
        grp = None

    for kind, item in split_rows(block):
        if kind == "raw":
            flush()
            out.append(item.strip())
            continue
        cls, kind, attrs, body = item.group(1), item.group(2), item.group(3), item.group(4)
        href = (re.search(r'href="([^"]*)"', attrs) or [None, ""])[1]
        slug = href.rsplit("/", 1)[-1]
        slug = slug[:-5] if slug.endswith(".html") else slug
        # имя: единый регистр + без приклеенного кода диапазона
        code = re.search(r'<span class="bk-row__n">(.*?)</span>', body, re.S)
        code_txt = html.unescape(RC.strip_tags(code.group(1))) if code else ""
        nm = re.search(r'<span class="bk-row__t">(.*?)</span>', body, re.S)
        if nm:
            name = html.unescape(RC.strip_tags(nm.group(1)))
            fixed = clean_name(name, lang)
            if code_txt and fixed.endswith(code_txt):
                fixed = fixed[: -len(code_txt)].strip()
            body = body[:nm.start(1)] + html.escape(fixed) + body[nm.end(1):]
        row = '<a class="%s"%s>%s</a>' % (cls, attrs, body)
        if kind == "sec":
            flush()
            grp = (slug, [row])
        else:
            if grp is None:
                out.append(row)                  # подпункт без раздела — оставляем как есть
            else:
                grp[1].append(row)
    flush()
    return "\n".join(out)


def fix_page(raw, lang, here):
    """Возвращает (текст, сколько групп собрано). Каждое дерево правим по границам div."""
    ngroups = 0
    out = raw
    # идём с конца, чтобы позиции не сдвигались
    opens = [m for m in re.finditer(r'<div class="cls-tree"[^>]*>', raw)]
    for m in reversed(opens):
        close = raw.find("</div>", m.end())
        if close < 0:
            continue
        inner = raw[m.end():close]
        if "<div" in inner:          # вложенные блоки — не наш случай, не трогаем
            continue
        body = build(inner, lang, here)
        ngroups += body.count('class="bk-grp"')
        out = out[:m.end()] + body + out[close:]
    # скрипт раскрытия — один раз, перед </body>
    if 'class="bk-tgl"' in out and "bk-grp__sub" in out and "дерево классификаций: раскрывающиеся" not in out:
        out = out.replace("</body>", SCRIPT.strip() + "\n</body>", 1)
    return out, ngroups


def lang_of(raw):
    m = re.search(r'<html[^>]*\blang="([a-z-]+)"', raw)
    return m.group(1) if m else "az"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    files = total = 0
    for dp, dn, fn in os.walk(os.path.join(ROOT, BOOK)):
        dn[:] = [d for d in dn if not any(s in d for s in SKIP_DIRS)]
        for f in sorted(fn):
            if not f.endswith(".html"):
                continue
            fp = os.path.join(dp, f)
            with open(fp, encoding="utf-8", newline="") as fh:
                raw = fh.read()
            if 'class="cls-tree"' not in raw:
                continue
            out, n = fix_page(raw, lang_of(raw), f[:-5])
            if out == raw:
                continue
            files += 1
            total += n
            if not a.dry:
                with open(fp, "w", encoding="utf-8", newline="") as fh:
                    fh.write(out)
            print("  %-58s групп: %d" % (os.path.relpath(fp, ROOT).replace(os.sep, "/"), n))
    print("файлов: %d | собрано групп: %d%s" % (files, total, "  (dry-run)" if a.dry else ""))


if __name__ == "__main__":
    main()
