"""Strip all <abbr title="...">X</abbr> wrappings (also nested) and remove
the injected duzelis-abbr-style CSS, so we can re-inject cleanly."""
import re
from pathlib import Path

ROOT = Path(__file__).parent
for p in (ROOT / "klinik-psixiatriya").glob("*.html"):
    t = p.read_text(encoding="utf-8")
    orig = t
    prev = None
    while prev != t:
        prev = t
        t = re.sub(r'<abbr[^>]*>(.*?)</abbr>', r'\1', t, flags=re.DOTALL | re.IGNORECASE)
    # Remove our CSS block
    t = re.sub(r'<style>/\* duzelis-abbr-style \*/.*?</style>\s*', '', t, flags=re.DOTALL)
    if t != orig:
        p.write_text(t, encoding="utf-8")
        print(f"unwrapped: {p.name}")
print("done")
