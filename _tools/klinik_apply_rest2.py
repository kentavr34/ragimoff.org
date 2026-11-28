# -*- coding: utf-8 -*-
"""Второй дожим NEXT (28.11.2026) для того, что klinik_apply_paras/klinik_apply_rest не нашли из-за разметки сайта:
  1) коды DSM-5-TR в шапках разделов: блок «DSM-5-TR <код>» -> <span class="dh-code">код</span> (и <span class="sc">код</span>
     в содержании, только если новый код короткий, ≤ 30 знаков); замена только при единственном совпадении в копии;
  2) названия глав МКБ-11 («<коды> <НАЗВАНИЕ>» в печати): на сайте — без кода и с заглавной буквы; старое название
     находится без учёта регистра и заменяется новым в том же виде во всех файлах книги языка и в book.json.
Строки печатного оглавления с номером страницы в конце пропускаются (на сайте их нет).
  python _tools/klinik_apply_rest2.py <paras.json> --lang az [--dry]"""
import glob, html, io, json, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
dry = "--dry" in sys.argv
L = sys.argv[sys.argv.index("--lang") + 1]
P = json.load(io.open(sys.argv[1], encoding="utf-8"))
BJ = "books/klinik-psixiatriya/book.json"
files = [f.replace(os.sep, "/") for f in glob.glob("books/klinik-psixiatriya/%s/*.html" % L) + glob.glob("%s/read/klinik-psixiatriya/*.html" % L)] + [BJ]
T = {f: io.open(f, encoding="utf-8", newline="").read() for f in files}
orig = dict(T)
esc = lambda s: html.escape(s, quote=False)


def low(s):
    if L in ("az", "tr"):
        s = s.replace("I", "ı").replace("İ", "i")
    return s.lower()


def cap(s):
    f = s[:1]
    f = "İ" if (L in ("az", "tr") and f == "i") else f.upper()
    return f + s[1:]


log = []
CODE = re.compile(r"^(?:\d[A-Z0-9]{2,3}(?:\.[0-9A-Z]+)?–\d[A-Z0-9]{2,3}(?:\.[0-9A-Z]+)?|[A-Z]\.\d+\.)\s+(.+)$")
for key, v in P.items():
    old, new = (v.get("old") or ""), (v.get("new") or "")
    if old == new or re.search(r"\s\d{2,4}$", old):
        continue
    # 1) коды DSM-5-TR
    if re.match(r"DSM-5-TR\s", old) and re.match(r"DSM-5-TR\s", new):
        co, cn = old[9:].strip(), new[9:].strip()
        for cls, lim in (("dh-code", 10**6), ("sc", 30)):
            if len(cn) > lim:
                continue
            for copy in ("books/", "%s/read/" % L):
                pat = '<span class="%s">%s</span>' % (cls, esc(co))
                hits = [f for f in T if f.startswith(copy) and pat in T[f]]
                cnt = sum(T[f].count(pat) for f in hits)
                if cnt == 1:
                    f = hits[0]
                    T[f] = T[f].replace(pat, '<span class="%s">%s</span>' % (cls, esc(cn)))
                    log.append((key, "код %s" % cls, f, co, cn))
                elif cnt > 1:
                    log.append((key, "код %s: %d совпадений — не тронуто" % (cls, cnt), copy, co, cn))
        continue
    # 2) названия глав
    mo, mn = CODE.match(old), CODE.match(new)
    if mo and mn and old.split()[0] == new.split()[0]:
        no, nn = mo.group(1).strip(), mn.group(1).strip()
        lo = low(no)
        forms = set()
        for t in T.values():
            for m in re.finditer(r"[>\"]([^<>\"]{%d,%d})[<\"]" % (len(no) - 2, len(no) + 2), t):
                s = m.group(1)
                if low(s) == lo:
                    forms.add(s)
        for s in forms:
            target = cap(low(nn)) if s[:1].isupper() and not s.isupper() else (nn if s.isupper() else low(nn))
            for f in T:
                n = T[f].count(">%s<" % s) + T[f].count('"%s"' % s)
                if n:
                    T[f] = T[f].replace(">%s<" % s, ">%s<" % target).replace('"%s"' % s, '"%s"' % target)
            log.append((key, "глава", "%d вида" % len(forms), s, target))
        if not forms:
            log.append((key, "глава не найдена", "", no, nn))
changed = [f for f in T if T[f] != orig[f]]
if not dry:
    for f in changed:
        io.open(f, "w", encoding="utf-8", newline="").write(T[f])
with io.open("_agent/klinik_rest2_%s.tsv" % L, "w", encoding="utf-8") as w:
    for r in log:
        w.write("\t".join(str(x) for x in r) + "\n")
for r in log:
    print(" ", r[1], "|", r[3][:60], "→", r[4][:70])
print(L, "файлов изменено:", len(changed), "(проба)" if dry else "")
