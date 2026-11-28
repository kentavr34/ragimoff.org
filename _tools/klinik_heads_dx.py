# -*- coding: utf-8 -*-
"""28.11.2026 (слово Кенана: на странице расстройства — все три названия по трём классификациям, не путать):
сверка и правка таблицы шапки (.bk-codes: строки МКБ-10 и DSM-5-TR — код и название) на страницах расстройств
с шапками исправленных версий базы (dx_heads.json; страж dx_header_guard — БРАКА НЕТ).
Страница → код МКБ-11 по якорю первого раздела (id="6a00-1-…") и пунктам дерева МКБ-11 (id → code).
Правится только текст ячейки dh-name (и dh-code, если код короткий и отличается); остальное не трогается.
  python _tools/klinik_heads_dx.py <dx_heads.json> [--dry]   — отчёт: _agent/klinik_heads_dx.tsv"""
import glob, html, io, json, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
H = json.load(open(sys.argv[1], encoding="utf-8"))
dry = "--dry" in sys.argv
book = json.load(open("books/klinik-psixiatriya/book.json", encoding="utf-8"))
LBL = {"10": r"(?:МКБ-10|XBT-10|ICD-10|İCD-10)", "dsm": r"DSM-5-TR"}
ROW = re.compile(r'(<span class="dh-lbl">)([^<]+)(</span><span class="dh-code">)([^<]*)(</span></td><td class="dh-name">)([^<]*)(</td>)')
rep, nfile, nfix = [], 0, 0
for L in ("az", "ru", "tr", "en"):
    if L not in H:
        continue
    code_of = {it["id"].lower(): it["code"] for g in book["trees"][L]["icd"] for it in g.get("items", [])}
    for f in sorted(glob.glob("books/klinik-psixiatriya/%s/*.html" % L) + glob.glob("%s/read/klinik-psixiatriya/*.html" % L)):
        t = io.open(f, encoding="utf-8", newline="").read()
        if "bk-codes" not in t:
            continue
        m = re.search(r'<h2 id="([0-9a-z]+)-1-', t)
        k = code_of.get(m.group(1)) if m else None
        h = H[L]["heads"].get(k or "")
        if not h:
            rep.append((L, f, k or "?", "", "страница не сопоставлена с шапкой базы", "", ""))
            continue

        def fix(mm):
            global nfix
            lbl, code, name = mm.group(2), html.unescape(mm.group(4)), html.unescape(mm.group(6))
            if re.match(LBL["10"], lbl):
                want_c, want_n = h.get("c10"), h.get("n10")
            elif re.match(LBL["dsm"], lbl):
                want_c, want_n = h.get("cdsm"), h.get("ndsm")
            else:
                return mm.group(0)
            out = list(mm.groups())
            if want_n and want_n != name:
                rep.append((L, f, k, lbl, "название", name, want_n))
                out[5] = html.escape(want_n, quote=False); nfix += 1
            if want_c and want_c != code and len(want_c) <= 30:
                rep.append((L, f, k, lbl, "код", code, want_c))
                out[3] = html.escape(want_c, quote=False); nfix += 1
            return "".join(out)
        t2 = ROW.sub(fix, t)
        if t2 != t:
            nfile += 1
            if not dry:                          # через временный файл: прямая запись в 6A22.html на Windows давала EINVAL
                with io.open(f + ".tmp", "w", encoding="utf-8", newline="") as w:
                    w.write(t2)
                os.replace(f + ".tmp", f)
with open("_agent/klinik_heads_dx.tsv", "w", encoding="utf-8") as w:
    w.write("язык\tфайл\tкод МКБ-11\tклассификация\tчто\tбыло на сайте\tпо базе\n")
    for r in rep:
        w.write("\t".join(str(x) for x in r) + "\n")
print("правок ячеек:", nfix, "| файлов:", nfile, "| несопоставленных страниц:", sum(1 for r in rep if r[4].startswith("страница")), "(проба)" if dry else "")
