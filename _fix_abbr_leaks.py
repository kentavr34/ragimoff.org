"""Fix double-injected <abbr> leaks across the book HTMLs.

Root cause: _inject_abbr.py was run twice. The second pass wrapped abbr
terms that already had abbr tags, breaking nested structure. Inner content
ended up as visible text fragments like
  'WHO), 2019, qüvvəyə minmə 2022.">XBT-11 kodu'
instead of
  'WHO XBT-11 kodu' (body) or just 'XBT-11 kodu' (table headers).

Strategy (idempotent — safe to re-run):
  1. Iteratively collapse properly-formed `<abbr title="...">X</abbr>` → X
     where X contains no `<`. Repeat until stable.
  2. Strip orphan `<abbr ...>` openings and `</abbr>` closings.
  3. Replace known leak patterns:
       - In <th> context: strip everything before the clean term ("XBT-11
         kodu", "DSM-5-TR kodu", etc.)
       - In body context: convert `<title-fragment>">TERM` to readable
         form (period + dash + term).
"""
from __future__ import annotations
import os
import re

ROOT = os.path.dirname(__file__)

# Known leak patterns from _inject_abbr.py double-injection.
# Each entry: (regex pattern, replacement-in-th, replacement-in-body)
KNOWN_LEAKS = [
    # XBT-11 / ICD-11 leak — title content includes
    # "...Ümumdünya Səhiyyə Təşkilatı (WHO), 2019, qüvvəyə minmə 2022."
    # In TH: just strip (header context wants brief). In body: clean readable.
    (r'WHO\), 2019, qüvvəyə minmə 2022\.">',
     '', 'WHO, 2019, qüvvəyə minmə 2022 — '),
    (r'WHO,?\s*2019,\s*qüvvəyə minmə 2022\.">',
     '', 'WHO, 2019, qüvvəyə minmə 2022 — '),
    (r', 2019, qüvvəyə minmə 2022\.">',
     '', ' (2019, qüvvəyə minmə 2022) — '),
    # XBT-10 leak — "Xəstəliklərin Beynəlxalq Təsnifatı, 10-cu redaksiya — WHO, 1990."
    (r'WHO,?\s*1990\.">',
     '', 'WHO, 1990 — '),
    (r', 1990\.">',
     '', ' (1990) — '),
    # ICD-11/10 leak — "International Classification of Diseases ... — WHO."
    (r'WHO\.">',
     '', 'WHO — '),
    # DSM-5-TR leaks — "...APA, 2022." / "...APA, 2013."
    (r'APA,?\s*2022\.">',
     '', 'APA, 2022 — '),
    (r'APA,?\s*2013\.">',
     '', 'APA, 2013 — '),
    (r', 2022\.">',
     '', ' (2022) — '),
    # Generic WHO title leak — "Ümumdünya Səhiyyə Təşkilatı (WHO)."
    (r'Ümumdünya Səhiyyə Təşkilatı \(WHO\)\.">',
     '', 'Ümumdünya Səhiyyə Təşkilatı (WHO) — '),
]

# After targeted replacements, any remaining `">` orphan is a stray attribute
# leak — strip it.
STRAY_QUOTE_RE = re.compile(r'\s*"\s*>(?=\s*[A-Za-zƏİ0-9])')


def collapse_valid_abbrs(text: str) -> str:
    """Iteratively replace `<abbr title="...">X</abbr>` → `X` where X has no `<`.
    This collapses well-formed nested abbrs from the innermost outwards.
    """
    prev = None
    while prev != text:
        prev = text
        text = re.sub(
            r'<abbr\b[^<>]*>([^<]*)</abbr>',
            r'\1',
            text,
            flags=re.IGNORECASE,
        )
    return text


def strip_orphan_abbr_tags(text: str) -> str:
    """After collapse, any remaining broken <abbr ...> open or </abbr> close
    is orphaned — strip the tag, keep surrounding text."""
    text = re.sub(r'<abbr\b[^>]*>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'</abbr>', '', text, flags=re.IGNORECASE)
    return text


def is_inside_th(text_before_pos: str) -> bool:
    """Crude check: was the latest opened tag a <th>?
    Look at last `<th` or `</th>` or `<td>` etc. in preceding text."""
    last_open_th = text_before_pos.rfind('<th')
    last_close_th = text_before_pos.rfind('</th>')
    last_open_td = text_before_pos.rfind('<td')
    last_close_td = text_before_pos.rfind('</td>')
    # Inside <th> if last <th opening is after both </th> and any <td/td>
    in_th = (last_open_th > last_close_th
             and last_open_th > last_close_td
             and last_open_th > last_open_td)
    return in_th


def fix_known_leaks(text: str) -> tuple[str, int]:
    """Apply known leak-pattern replacements, context-aware (th vs body)."""
    count = 0
    for pat, repl_th, repl_body in KNOWN_LEAKS:
        rx = re.compile(pat)
        out = []
        i = 0
        for m in rx.finditer(text):
            in_th = is_inside_th(text[:m.start()])
            out.append(text[i:m.start()])
            out.append(repl_th if in_th else repl_body)
            i = m.end()
            count += 1
        out.append(text[i:])
        text = ''.join(out)
    return text, count


def fix_stray_quotes(text: str) -> tuple[str, int]:
    """Remove any orphan `">` followed by content — leftover from leaks."""
    new, n = STRAY_QUOTE_RE.subn(' ', text)
    return new, n


def fix_file(path: str) -> tuple[int, int, int]:
    """Returns (collapsed_abbrs, leak_fixes, stray_quotes)."""
    text = open(path, encoding='utf-8').read()
    orig = text

    # 1. Collapse valid abbrs
    text = collapse_valid_abbrs(text)
    collapsed = (orig.count('<abbr') - text.count('<abbr'))

    # 2. Strip orphan abbr tags
    text = strip_orphan_abbr_tags(text)

    # 3. Apply known leak patterns
    text, leak_n = fix_known_leaks(text)

    # 4. NO aggressive stray-quote removal — it destroyed valid HTML like
    #    <span class="icd">F70</span>. Only rely on known leak patterns.
    stray_n = 0

    if text != orig:
        open(path, 'w', encoding='utf-8').write(text)
    return collapsed, leak_n, stray_n


def main():
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    total_collapsed = total_leaks = total_stray = 0
    n_files = 0
    for root, _, files in os.walk(os.path.join(ROOT, 'klinik-psixiatriya')):
        for f in files:
            if not f.endswith('.html'): continue
            p = os.path.join(root, f)
            c, l, s = fix_file(p)
            if c or l or s:
                print(f'  {f}: collapsed={c} leaks={l} stray={s}')
                n_files += 1
                total_collapsed += c
                total_leaks += l
                total_stray += s
    print(f'\n{n_files} files cleaned. Collapsed: {total_collapsed}, '
          f'leaks fixed: {total_leaks}, strays stripped: {total_stray}')


if __name__ == '__main__':
    main()
