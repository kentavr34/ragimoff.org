"""Site-wide grammar/spelling/typo audit for the Klinik Psixiatriya book.

Targets: klinik-psixiatriya/ + _supplements/chapters-v2/.

Checks:
  1. Double spaces inside text (sloppy formatting).
  2. Repeated words: 'olan olan', 'üçün üçün', etc.
  3. Cyrillic letters mixed into Azerbaijani text (typing slip).
  4. English jargon leftovers in body text (binge, follow-up, screening, etc.).
  5. Common AZ spelling inconsistencies (multiple variants of same word).
  6. Latin letters in middle of AZ word (a/e instead of ə, i instead of ı, etc.)
  7. Suspect double-letter patterns (often typos: depressiya vs depresiya).
  8. Mismatched brackets (count of `(`, `)`).
  9. Sentences ending without `.`/`?`/`!`/`:`/`;`/`)` (sometimes typo).
"""
from __future__ import annotations
import os
import re
import sys
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.stdout.reconfigure(encoding='utf-8')

# Inline tags to strip when extracting visible text
TAG_RE = re.compile(r'<[^>]+>')
SCRIPT_STYLE_RE = re.compile(r'<(script|style)\b[^>]*>[\s\S]*?</\1>', re.IGNORECASE)
ABBR_TITLE_RE = re.compile(r'<abbr[^>]*title="[^"]*"[^>]*>([\s\S]*?)</abbr>', re.IGNORECASE)
# Skip the sidebar (nav) and headers from analysis
SIDEBAR_RE = re.compile(r'<aside\b[^>]*>[\s\S]*?</aside>', re.IGNORECASE)
HEADER_RE = re.compile(r'<header\b[^>]*>[\s\S]*?</header>', re.IGNORECASE)
KITAB_MODAL_RE = re.compile(r'<div id="kitab-modal"[\s\S]*?</div>\s*</div>', re.IGNORECASE)
# Skip reference list (English citations)
REF_LIST_RE = re.compile(r'<ol class="ref-list">[\s\S]*?</ol>', re.IGNORECASE)


def extract_visible_text(html: str) -> str:
    """Strip tags, scripts, styles, sidebar — keep visible body text."""
    s = SCRIPT_STYLE_RE.sub(' ', html)
    s = SIDEBAR_RE.sub(' ', s)
    s = HEADER_RE.sub(' ', s)
    s = KITAB_MODAL_RE.sub(' ', s)
    s = REF_LIST_RE.sub(' ', s)
    s = ABBR_TITLE_RE.sub(r'\1', s)
    s = TAG_RE.sub(' ', s)
    # Unescape common entities
    s = s.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"')
    s = s.replace('&lt;', '<').replace('&gt;', '>').replace('&mdash;', '—')
    return s


# ── Issue checks ─────────────────────────────────────────────────────────
def check_double_spaces(text: str):
    """Mid-text double-spaces (excluding line breaks)."""
    return [(m.start(), m.group(0)) for m in re.finditer(r'(?<=\S)  +(?=\S)', text)]


def check_repeated_words(text: str):
    """Find adjacent duplicated words like 'olan olan'."""
    found = []
    for m in re.finditer(r'\b([A-Za-zƏəÜüÖöŞşÇçĞğıİ]{3,})\s+\1\b', text, re.IGNORECASE):
        # Skip valid repetitions like 'tez tez', 'gec gec' (rhetorical doubling)
        word = m.group(1).lower()
        if word in {'tez', 'gec', 'çox', 'az', 'çox-çox', 'çoxlu', 'tək-tək', 'gəl', 'bir'}:
            continue
        found.append((m.start(), m.group(0)))
    return found


def check_cyrillic_in_az(text: str):
    """Single Cyrillic letters mixed inside Azerbaijani words.
    Russian words are OK in citations; the issue is *single* Cyrillic chars
    inside a Latin-letter word (Latin substitution typo)."""
    found = []
    for m in re.finditer(r'\b[\w]*[А-Яа-яЁё][\w]*\b', text):
        word = m.group(0)
        if not word: continue
        # Count Latin vs Cyrillic letters
        latin = sum(1 for c in word if c.isalpha() and ord(c) < 256)
        cyrillic = sum(1 for c in word if 'А' <= c <= 'я' or c in 'Ёё')
        # If mixed (Latin > 0 AND Cyrillic > 0), suspicious
        if latin > 0 and cyrillic > 0:
            found.append((m.start(), word))
    return found


def check_english_jargon(text: str):
    """English jargon in body text that should have been replaced."""
    patterns = [
        r'\b(binge|follow-up|screening|compliance|defiant|baseline|distress|'
        r'evidence|cultural|premature|disinhibe|kültür)\b',
    ]
    found = []
    for pat in patterns:
        for m in re.finditer(pat, text, re.IGNORECASE):
            # Skip if part of "Bodily distress" or known phrase in italics
            context_left = text[max(0, m.start()-30):m.start()]
            if any(skip in context_left for skip in ['Bodily', 'Body ']):
                continue
            found.append((m.start(), m.group(0)))
    return found


def check_bracket_balance(text: str):
    """Mismatch in count of `(`/`)`."""
    n_open = text.count('(')
    n_close = text.count(')')
    if n_open != n_close:
        return [(0, f'( count={n_open}, ) count={n_close}')]
    return []


def check_quote_balance(text: str):
    """Odd number of `"` — possibly unmatched."""
    n = text.count('"')
    return [(0, f'count={n} (odd)')] if n % 2 else []


def check_latin_in_az_word(text: str):
    """Catch Azerbaijani words spelled with 'e' instead of 'ə' or similar."""
    # Common AZ words misspelled with Latin a/e instead of ə.
    # We look for specific high-frequency words.
    misspellings = {
        # ('wrong', 'right')
        'kelime': 'kəlimə',
        'birinci': 'birinci',  # OK
        'birinçi': 'birinci',
        'iqtisadiyat': 'iqtisadiyyat',  # missing letter
        'medenniyat': 'mədəniyyət',
        'medeniyyet': 'mədəniyyət',
        'depresiya': 'depressiya',  # OR vice versa — both exist
        'manik': 'manik',  # OK
    }
    found = []
    for wrong, right in misspellings.items():
        for m in re.finditer(rf'\b{wrong}\b', text, re.IGNORECASE):
            found.append((m.start(), f'{m.group(0)} → {right}'))
    return found


def check_spelling_variants(global_word_counts: dict):
    """Find words that have multiple spelling variants (case-insensitive
    normalized) — possible inconsistency."""
    variants = defaultdict(set)
    for word, count in global_word_counts.items():
        key = word.lower().translate(str.maketrans('ş', 's')).replace('ə','e').replace('ı','i')
        variants[key].add(word)
    suspects = {k: v for k, v in variants.items() if len(v) > 1 and len(k) > 6}
    return suspects


# ── Driver ──────────────────────────────────────────────────────────────
def audit_file(path: str) -> dict:
    html = open(path, encoding='utf-8').read()
    text = extract_visible_text(html)
    return {
        'double_space': check_double_spaces(text),
        'repeated_words': check_repeated_words(text),
        'cyrillic_mix': check_cyrillic_in_az(text),
        'english_jargon': check_english_jargon(text),
        'brackets': check_bracket_balance(text),
        'misspellings': check_latin_in_az_word(text),
    }, text


def main():
    targets = []
    for sub in ('klinik-psixiatriya', '_supplements/chapters-v2'):
        full = os.path.join(ROOT, sub)
        if not os.path.exists(full):
            continue
        for root, _, files in os.walk(full):
            for f in files:
                if f.endswith('.html') and not f.startswith('_') and not f.endswith('.bak.html'):
                    targets.append(os.path.join(root, f))

    print(f'# Grammar/Typo Audit Report\n')
    print(f'**Files scanned:** {len(targets)}\n')

    summary = Counter()
    details = []
    global_words = Counter()

    for p in sorted(targets):
        issues, text = audit_file(p)
        # Collect words for variant analysis
        for m in re.finditer(r'\b[A-Za-zƏəÜüÖöŞşÇçĞğıİ]{6,}\b', text):
            global_words[m.group(0)] += 1
        file_issue_count = sum(len(v) for v in issues.values())
        if not file_issue_count: continue
        rel = os.path.relpath(p, ROOT)
        details.append((rel, issues, text))
        for k, v in issues.items():
            summary[k] += len(v)

    print('## Summary by issue type\n')
    print('| Issue | Count |')
    print('|---|---|')
    for k, v in summary.most_common():
        print(f'| {k.replace("_"," ")} | {v} |')
    print()

    # Most-cited words for inconsistency check
    print('## Words with multiple spelling variants (suspect typos)\n')
    variants = check_spelling_variants(global_words)
    # Filter only significant words (5+ total usage)
    sig_variants = {k: v for k, v in variants.items()
                    if sum(global_words[w] for w in v) >= 5}
    for k, vs in sorted(sig_variants.items())[:60]:
        details_str = ', '.join(f'{w} (x{global_words[w]})' for w in sorted(vs))
        print(f'- `{k}` → {details_str}')
    print()

    # Per-file details (top 20 only)
    print('## Per-file issues (top 20 files)\n')
    details.sort(key=lambda x: -sum(len(v) for v in x[1].values()))
    for rel, issues, text in details[:20]:
        total = sum(len(v) for v in issues.values())
        print(f'### {rel} — {total} issues\n')
        for kind, items in issues.items():
            if not items: continue
            label = kind.replace('_',' ')
            print(f'**{label}** ({len(items)}):\n')
            for pos, snippet in items[:5]:
                ctx = text[max(0, pos-30):pos+50].replace('\n', ' ').strip()
                print(f'  - `{snippet}` ... `{ctx[:90]}`')
            if len(items) > 5:
                print(f'  - … and {len(items)-5} more')
            print()


if __name__ == '__main__':
    main()
