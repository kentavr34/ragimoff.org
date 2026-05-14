"""Round-4 terminology fix per Azerbaijani academic medical sources.

Rules sourced from МКБ-11 РФ (Нервная анорексия/булимия) adapted:
  Russian "Нервная анорексия" → Azerbaijani "Sinir anoreksiyası" (genitive,
  academic standard following AzPA convention).
  "Kültür" (Turkish/Germanism, non-academic) → "Mədəniyyət" (cultural context)
                                              → "kultura" / "əkin" (lab culture).
  Plus careful body-text replacements for "binge", "follow-up", "distress",
  protecting reference-list citations and <abbr> tooltips.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).parent

# Files to process: book only (chapters-v2 sources + injected klinik-psixiatriya HTMLs)
TARGETS = []
TARGETS += list((ROOT / "_supplements" / "chapters-v2").glob("*.html"))
TARGETS += list((ROOT / "klinik-psixiatriya").glob("*.html"))

# ── Eating disorders: full-form replacements (ALL CAPS, Title, lower) ──
EATING_TITLE_REPL = [
    # ICD-code-prefixed h1 lines and any prose mention
    ("ANOREKSİYA NERVOZA",  "SİNİR ANOREKSİYASI"),
    ("Anoreksiya Nervoza",  "Sinir anoreksiyası"),
    ("Anoreksiya nervoza",  "Sinir anoreksiyası"),
    ("Anoreksiya Nervozas", "Sinir anoreksiyas"),  # safeguard for case sensitivity
    ("anoreksiya nervoza",  "sinir anoreksiyası"),
    ("BULİMİYA NERVOZA",    "SİNİR BULİMİYASI"),
    ("Bulimiya Nervoza",    "Sinir bulimiyası"),
    ("Bulimiya nervoza",    "Sinir bulimiyası"),
    ("bulimiya nervoza",    "sinir bulimiyası"),
    # ICD/anchor slugs (anoreksiya-nervoza → sinir-anoreksiyasi)
    ("anoreksiya-nervoza",  "sinir-anoreksiyasi"),
    ("bulimiya-nervoza",    "sinir-bulimiyasi"),
]

# ── Culture replacements ──
CULTURE_REPL = [
    # Heading + body referring to cultural context
    ("Kültür və kontekstlə iş",  "Mədəniyyət və kontekstlə iş"),
    ('"kültür-və-kontekstlə-iş"', '"medeniyyet-ve-kontekstle-is"'),
    ("Kültür", "Mədəniyyət"),
    # Lab-culture context: "sidik kültürü", "qan kültürü", "kültür"
    ("sidik kültürü",  "sidik kulturası"),
    ("qan kültürü",    "qan kulturası"),
    ("sidik analizi və kültürü",  "sidik analizi və kulturası"),
    ("kültürü",  "kulturası"),
    ("kültür",   "kultura"),
]

# ── Body-text English jargon (skip refs and abbr titles) ──
BODY_REPL = [
    # binge eating in prose (not in citation refs)
    ("binge eating", "obur yemə"),
    ("Binge eating", "Obur yemə"),
    ("binge epizod",  "obur yemə epizod"),
    ("Binge epizod",  "Obur yemə epizod"),
    (" binge ",       " obur yemə "),
    (" binge,",       " obur yemə,"),
    (" binge.",       " obur yemə."),
    (" binge;",       " obur yemə;"),
    (" binge:",       " obur yemə:"),
    (" binge+",       " obur yemə +"),
    # follow-up in prose
    ("follow-up sorğu", "təqib sorğu"),
    ("follow-up qiymət", "təqib qiymət"),
    ("follow-up vaxt",  "təqib vaxtı"),
    ("follow-up dövr",  "təqib dövrü"),
    # screening → skrinning (Azeri transliteration)
    (" screening ",  " skrinninq "),
    ("Screening ", "Skrinninq "),
    # compliance
    (" compliance",  " uyğunluq"),
    # 'cultural' singular
    ("cross-cultural", "mədəniyyətlərarası"),
]

# Lines/blocks to PROTECT (skip body replacement inside):
# - <ol class="ref-list">...</ol> (reference citations stay original)
# - <abbr title="...">...</abbr> (tooltip definitions stay original)
PROTECT_REF_LIST  = re.compile(r'<ol class="ref-list">[\s\S]*?</ol>', re.IGNORECASE)
PROTECT_ABBR_ATTR = re.compile(r'title="[^"]*"', re.IGNORECASE)


def apply_protected(text: str, replacements):
    """Apply replacements but skip protected zones (ref-list, abbr title attrs)."""
    placeholders = []
    def stash(m):
        placeholders.append(m.group(0))
        return f"\x00PROTECT{len(placeholders)-1}\x00"
    work = PROTECT_REF_LIST.sub(stash, text)
    work = PROTECT_ABBR_ATTR.sub(stash, work)
    for src, dst in replacements:
        work = work.replace(src, dst)
    # Restore
    def unstash(m):
        return placeholders[int(m.group(1))]
    work = re.sub(r'\x00PROTECT(\d+)\x00', unstash, work)
    return work


def fix_file(p: Path) -> int:
    text = p.read_text(encoding="utf-8")
    orig = text
    # Titles and culture are unconditional (also fine inside refs — they don't
    # appear there anyway in our case).
    for src, dst in EATING_TITLE_REPL + CULTURE_REPL:
        text = text.replace(src, dst)
    # Body replacements: protect refs/abbr titles
    text = apply_protected(text, BODY_REPL)
    if text != orig:
        p.write_text(text, encoding="utf-8")
        return sum(orig.count(s) for s, _ in EATING_TITLE_REPL + CULTURE_REPL + BODY_REPL
                   if s in orig)
    return 0


def main():
    total = 0
    files = 0
    for p in TARGETS:
        n = fix_file(p)
        if n:
            print(f"  {p.relative_to(ROOT)}: ~{n} replacements")
            total += n
            files += 1
    print(f"\nTotal: ~{total} replacements across {files} files")


if __name__ == "__main__":
    main()
