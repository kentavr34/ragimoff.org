# -*- coding: utf-8 -*-
"""fix-klinik-nav.py — вернуть ПРЕЖНЮЮ структуру меню «Klinik Psixiatriya».

Владелец: «в боковом меню книги не всё как было в смысле структуры — надо было
менять стиль, а не систему; переход между классификациями не соскакивал; общее
меню при клике внутри меню открывало подменю — а не как сейчас всё в один
длинный список; сейчас в МКБ-11 вроде держится, а в МКБ-10 и DSM-5 не держится».

Что сломала пересборка (596f2b5) и что делает этот скрипт:
 1. деревья DSM-5-TR и МКБ-10 (XBT-10) стали ПЛОСКИМИ списками: 19 и 12 групп
    превратились в пустые строки-заголовки, все 104 пункта вывалились сразу.
    Скрипт собирает группы обратно — .bk-grp + ▶ (.bk-tgl) + .bk-grp__sub, как в
    МКБ-11: закрыто по умолчанию, группа текущей страницы открыта (data-here=1);
 2. setCls() не помнил выбор: при переходе на другую страницу меню «соскакивало»
    на МКБ-11. Скрипт ставит localStorage-память (ключ bk-cls-klinik) и
    восстановление выбранной классификации до отрисовки меню;
 3. имена групп берутся из ПРЕЖНЕЙ разметки (596f2b5^) и приводятся к единому
    регистру по реестру CASE-REGISTER.tsv (нормализация названий и скобочных
    аббревиатур — те же функции casecheck.py).

Запуск:
    python _tools/fix-klinik-nav.py --dry
    python _tools/fix-klinik-nav.py
"""
from __future__ import annotations

import argparse
import html as H
import importlib.util
import io
import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "klinik-psixiatriya")
GROUPS_JSON = os.path.join(ROOT, "_tools", "_klinik_old_groups.json")

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

_spec = importlib.util.spec_from_file_location("cc", os.path.join(ROOT, "_tools", "casecheck.py"))
CC = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(CC)

RE_TAG = re.compile(r"<[^>]+>")
RE_TREE = re.compile(r'<div class="cls-tree" data-cls="(%s)"[^>]*>(.*?)</div>\s*(?=<div class="cls-tree"|</nav>)', re.S)
RE_ROW = re.compile(r'<a class="bk-row bk-row--(sub|sec)([^"]*)" href="([^"#]+)"([^>]*)>'
                    r'(<span class="bk-row__n">[^<]*</span>)?<span class="bk-row__t">(.*?)</span>\s*</a>', re.S)

SETCLS_OLD = re.compile(r"<script>function setCls\(k\)\{.*?\}</script>", re.S)
SETCLS_NEW = """<script>/* классификации: выбор помнится между страницами (localStorage) */
function setCls(k, save){
  document.querySelectorAll('.cls-tab').forEach(function(t){t.classList.toggle('is-active',t.getAttribute('data-cls')===k);});
  document.querySelectorAll('.cls-panel,.cls-tree').forEach(function(p){p.hidden=(p.getAttribute('data-cls')!==k);});
  if (save !== false) { try { localStorage.setItem('bk-cls-klinik', k); } catch(e){} }
}
(function(){ /* восстановление выбранной классификации до отрисовки меню */
  try {
    var k = localStorage.getItem('bk-cls-klinik');
    if (k && document.querySelector('.cls-tab[data-cls="'+k+'"]')) setCls(k, false);
  } catch(e){}
})();</script>"""


def txt(x: str) -> str:
    return re.sub(r"\s+", " ", H.unescape(RE_TAG.sub("", x))).strip()


def rows_of(tree_html: str):
    """Строки дерева в порядке следования: (kind, code, name, href, tail)."""
    out = []
    for m in RE_ROW.finditer(tree_html):
        out.append({"kind": m.group(1), "tail": m.group(2), "href": m.group(3),
                    "attrs": m.group(4), "code": txt(m.group(5) or ""), "name": txt(m.group(6))})
    return out


def build_tree(cls: str, groups, rows, lang: str, here: str, abbr: dict,
               here_set=None) -> str:
    """Плоские строки → группы .bk-grp (как в прежней разметке и как в МКБ-11)."""
    used, out = set(), []
    idx = 0
    for gi, g in enumerate(groups):
        subs = g["subs"]
        if not subs:
            continue
        # строки этого дерева между двумя заголовками
        end = None
        for k, href in enumerate(subs):
            pass
        start = idx
        idx += len(subs)
        chunk = rows[start:idx]
        if len(chunk) != len(subs):
            raise SystemExit(f"{cls}: строки не совпали с прежней разметкой "
                             f"({len(chunk)} ≠ {len(subs)})")
        if [c["href"] for c in chunk] != subs:
            raise SystemExit(f"{cls}: порядок ссылок разошёлся с 596f2b5^")
        slug = os.path.splitext(os.path.basename(g["href"] or chunk[0]["href"]))[0]
        code = g["code"]
        name = CC.canon_text(g["name"], lang, abbr)
        hs = here_set if here_set else {here}
        is_here = "1" if (g["href"] in hs or
                          any(c["href"].split("#")[0] in hs for c in chunk)) else "0"
        inner = []
        on_head = " is-on" if is_here == "1" else ""
        if g["href"]:
            head = ('<a class="bk-row bk-row--sec%s" href="%s"><span class="bk-row__n">%s</span>'
                    '<span class="bk-row__t">%s</span></a>'
                    % (on_head, g["href"], H.escape(code), H.escape(name)))
        else:
            head = ('<span class="bk-row bk-row--sec%s"><span class="bk-row__n">%s</span>'
                    '<span class="bk-row__t">%s</span></span>'
                    % (on_head, H.escape(code), H.escape(name)))
        for c in chunk:
            on = " is-on" if c["href"].split("#")[0] == here else ""
            tgt = c["href"].split("#")[0]
            inner.append('<a class="bk-row bk-row--sub%s" href="%s"><span class="bk-row__n">%s</span>'
                         '<span class="bk-row__t">%s</span></a>' % (
                             on, c["href"], H.escape(c["code"]), H.escape(c["name"])))
        if len(inner) == 1:
            out.append(head + "\n" + inner[0])
        else:
            out.append(
                '<div class="bk-grp" data-slug="%s" data-here="%s">\n%s\n'
                '<button class="bk-tgl" type="button" tabindex="-1" aria-expanded="false" '
                'aria-label="Aç / bağla">\u25b6</button>\n<div class="bk-grp__sub">\n%s\n</div>\n</div>'
                % (os.path.splitext(g["href"])[0], is_here, head, "\n".join(inner)))
    return "\n".join(out)


def fix_page(path: str, lang: str, groups, maps, abbr: dict, dry: bool) -> tuple[bool, Counter, list]:
    raw = open(path, encoding="utf-8").read()
    out = raw
    here = os.path.basename(path)
    stats = Counter()
    msgs = []
    # «здесь» для главы: пункты этой главы (из дерева МКБ-11) — её группа в DSM/XBT-10
    here_set = {here}
    mi = re.search(r'<div class="cls-tree" data-cls="icd"[^>]*>(.*?)(?=<div class="cls-tree"|</nav>)',
                   out, re.S)
    if mi:
        cur = None
        for m in re.finditer(r'<div class="bk-grp" data-slug="([^"]*)"|href="([^"#]+)"', mi.group(1)):
            if m.group(1):
                cur = m.group(1)
            elif cur and os.path.splitext(os.path.basename(cur))[0] == os.path.splitext(here)[0]:
                here_set.add(os.path.basename(m.group(2)))
    for cls in ("dsm", "icd10"):
        m = re.search(r'<div class="cls-tree" data-cls="%s"[^>]*>(.*?)(?=<div class="cls-tree"|</nav>)'
                      % cls, out, re.S)
        if not m:
            continue
        rows = rows_of(m.group(1))
        if not rows:
            continue
        try:
            new = build_tree(cls, groups[lang][cls], rows, lang, here, abbr, here_set)
        except SystemExit as e:
            msgs.append(str(e))
            continue
        new_block = ('<div class="cls-tree" data-cls="%s"%s>' % (
            cls, " hidden" if ' hidden' in out[m.start():m.start() + 60] else "") + new + "</div>")
        out = out[:m.start()] + new_block + out[m.end():]
        stats["tree:" + cls] += 1
    # установим data-here и в МКБ-11 (там группы уже есть, но флаг мог протухнуть)
    def icd_repl(m):
        block = m.group(0)
        block = re.sub(r'(data-slug="%s" data-here=")\d(")' % re.escape(os.path.splitext(here)[0]),
                       r"\g<1>1\g<2>", block)
        # группа текущей страницы: открыта
        block = re.sub(r'(data-here="1")((?:(?!"?data-here).)*?)aria-expanded="false"',
                       r'\g<1>\g<2>aria-expanded="true"', block, flags=re.S)
        return block
    m = re.search(r'<div class="cls-tree" data-cls="icd"[^>]*>.*?(?=<div class="cls-tree"|</nav>)', out, re.S)
    if m:
        newb = icd_repl(m)
        if newb != m.group(0):
            stats["tree:icd-flags"] += 1
            out = out[:m.start()] + newb + out[m.end():]
    # setCls: память выбранной классификации
    if SETCLS_OLD.search(out):
        out = SETCLS_OLD.sub(SETCLS_NEW, out, count=1)
        stats["setCls:localStorage"] += 1
    elif "bk-cls-klinik" not in out and "<script>function setCls" in out:
        msgs.append("setCls не найден шаблоном")
    if out != raw:
        if not dry:
            open(path, "w", encoding="utf-8", newline="").write(out)
        return True, stats, msgs
    return False, stats, msgs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--book", default=None)
    a = ap.parse_args()
    groups = json.load(open(GROUPS_JSON, encoding="utf-8"))
    rows = CC.load_registry()
    abbr = CC.abbr_index(rows)
    base = a.book or BOOK
    total = Counter()
    msgs = Counter()
    files = 0
    for lang in ("ru", "az", "en", "tr"):
        d = base if lang == "az" else os.path.join(base, lang)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if not f.endswith(".html"):
                continue
            changed, stats, ms = fix_page(os.path.join(d, f), lang, groups, groups, abbr, a.dry)
            if changed:
                files += 1
            total.update(stats)
            for x in ms:
                msgs[x] += 1
    print(f"файлов изменено: {files} {'(dry)' if a.dry else ''}")
    print("правок:", dict(total))
    if msgs:
        print("предупреждения:", dict(msgs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
