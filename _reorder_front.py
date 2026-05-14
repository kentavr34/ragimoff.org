"""Reorganize the book's front matter per user's TOC vision.

Source files: klinik-psixiatriya/mugeddime.html + giris-yekun.html
Target structure:
  mugeddime.html (rewritten — front matter in this order):
    H1 MÜQƏDDİMƏ
      H2 Oxucuya müraciət
      H2 MÜƏLLİF HAQQINDA
    H1 GİRİŞ              (moved from giris-yekun)
      H2 Bu kitab haqqında, Niyə XBT-11?, Kitabın strukturu, ...
    H1 YEKUN TÖVSIYƏLƏR   (moved from giris-yekun)
      H2 Diaqnoz həmişə ikinci..., Psixoterapiya birinci..., ...
    H2 BU KİTAB NİYƏ MƏHZ İNDİ VƏ AZƏRBAYCANDA?
      H2 Bu kitab nədir, Kitabın strukturu, Mənbələr və yanaşma, ...
    H2 DÜNYADA PSİXİ SAĞLAMLIQ BÖHRANI
    H2 PSİXOTERAPİYANIN KLİNİK STRATEGİYALARI
    H2 MÜƏLLİF KLİNİK PROTOKOLU №1
    H2 MÜƏLLİF KLİNİK PROTOKOLU №2
    H2 AKKREDİTASİYA VƏ KEYFİYYƏT NƏZARƏTİ

  melumat.html (new — appendix at the very end, after main chapters):
    H1 TERMİNOLOJİ LÜĞƏT
    H1 PSİXOPATOLOGİYAYA GİRİŞ
    H1 KLİNİK MÜSAHİBƏ VƏ PSİXİ STATUSUN QİYMƏTLƏNDİRİLMƏSİ
    H1 HÜQUQİ-ETİK ASPEKTLƏR

  giris-yekun.html: redirect → mugeddime.html (kept for backward compat).
"""
from __future__ import annotations
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
BOOK = ROOT / "klinik-psixiatriya"
MUG = BOOK / "mugeddime.html"
GY  = BOOK / "giris-yekun.html"
MEL = BOOK / "melumat.html"


def extract_main(html: str) -> tuple[str, str, str]:
    """Returns (pre_main, inside_content_wrap, post_main)."""
    m_main = re.search(r'(<main\b[^>]*>\s*<div class="content-wrap">)', html)
    if not m_main:
        raise RuntimeError("no <main><div.content-wrap> found")
    main_start = m_main.end()
    # Find matching </div></main>
    m_close = re.search(r'(\s*</div>\s*</main>)', html[main_start:])
    if not m_close:
        raise RuntimeError("no </div></main> found")
    content = html[main_start:main_start + m_close.start()]
    return (html[:main_start], content, html[main_start + m_close.start():])


def split_sections_by_heading(content: str, level: str) -> list[tuple[str, str, str]]:
    """Split into sections by h1 or h2 boundaries.
    Returns list of (heading_html, heading_text, body_after_heading_until_next_split)."""
    pattern = re.compile(rf'(<{level}\b[^>]*>[\s\S]*?</{level}>)', re.IGNORECASE)
    parts = pattern.split(content)
    if not parts: return []
    sections = []
    # parts[0] = preamble; parts[1] = heading; parts[2] = body; parts[3] = heading; ...
    preamble = parts[0]
    if preamble.strip():
        sections.append(('', '', preamble))
    i = 1
    while i < len(parts):
        heading_html = parts[i]
        body = parts[i+1] if i+1 < len(parts) else ''
        text = re.sub(r'<[^>]+>', '', heading_html).strip()
        sections.append((heading_html, text, body))
        i += 2
    return sections


def find_section(sections: list, name_substr: str) -> tuple[str, str] | None:
    """Returns (heading_html + body) for section whose heading text contains substr."""
    for heading_html, text, body in sections:
        if name_substr.lower() in text.lower():
            return (heading_html + body)
    return None


def find_h1_block(content: str, h1_text_substr: str) -> str | None:
    """Find h1 block (h1 heading + all content until next h1 or end)."""
    h1_re = re.compile(r'(<h1\b[^>]*>[\s\S]*?</h1>)', re.IGNORECASE)
    matches = list(h1_re.finditer(content))
    for idx, m in enumerate(matches):
        text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if h1_text_substr.lower() in text.lower():
            start = m.start()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(content)
            return content[start:end].strip()
    return None


def find_h2_block(content: str, h2_text_substr: str, all_h2: bool = False) -> str | None:
    """Find h2 section content (heading + body until next h1/h2)."""
    h2_re = re.compile(r'(<h[12]\b[^>]*>[\s\S]*?</h[12]>)', re.IGNORECASE)
    matches = list(h2_re.finditer(content))
    for idx, m in enumerate(matches):
        text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if h2_text_substr.lower() in text.lower():
            start = m.start()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(content)
            return content[start:end].strip()
    return None


def main():
    print("Reading source files...")
    mug_html = MUG.read_text(encoding="utf-8")
    gy_html = GY.read_text(encoding="utf-8")

    mug_pre, mug_content, mug_post = extract_main(mug_html)
    gy_pre,  gy_content,  gy_post  = extract_main(gy_html)

    print("Extracting sections...")
    # ── From giris-yekun ──
    giris_block = find_h1_block(gy_content, "GİRİŞ")
    yekun_block = find_h1_block(gy_content, "YEKUN")

    # ── From mugeddime ──
    # H1 MÜQƏDDİMƏ block needs to be reconstructed without the H1 sections
    # we'll strip out and move (TERMİNOLOJİ, PSİXOPATOLOGİYA, KLİNİK, HÜQUQİ).
    # We use H2 sub-sections from inside the H1 MÜQƏDDİMƏ block.
    muqeddime_block = find_h1_block(mug_content, "MÜQƏDDİMƏ")
    if not muqeddime_block:
        # Fallback: take everything before first non-MÜQƏDDİMƏ H1
        muqeddime_block = mug_content

    # H1 blocks at the END of mugeddime — move to melumat.html
    terminoloji_block = find_h1_block(mug_content, "TERMİNOLOJİ LÜĞƏT")
    psixopatologiya_block = find_h1_block(mug_content, "PSİXOPATOLOGİYAYA GİRİŞ")
    klinik_musahibe_block = find_h1_block(mug_content, "KLİNİK MÜSAHİBƏ")
    huquqi_etik_block = find_h1_block(mug_content, "HÜQUQİ-ETİK")

    # ── Reassemble mugeddime.html ──
    # H1 MÜQƏDDİMƏ block with H2s (Oxucuya müraciət + MÜƏLLİF HAQQINDA)
    # Pick the first 2 h2 (Oxucuya, MÜƏLLİF) from muqeddime_block, then
    # insert GİRİŞ + YEKUN, then continue with rest of muqeddime H2s.
    h1_muq_match = re.search(r'<h1\b[^>]*>[\s\S]*?</h1>', muqeddime_block)
    h1_muq_tag = h1_muq_match.group(0) if h1_muq_match else '<h1>MÜQƏDDİMƏ</h1>'

    oxucuya = find_h2_block(muqeddime_block, "Oxucuya müraciət")
    muellif = find_h2_block(muqeddime_block, "MÜƏLLİF HAQQINDA")
    bu_kitab_niye = find_h2_block(muqeddime_block, "BU KİTAB NİYƏ MƏHZ İNDİ")
    bu_kitab_nedir = find_h2_block(muqeddime_block, "Bu kitab nədir")
    kitab_strukturu = find_h2_block(muqeddime_block, "Kitabın strukturu")
    menbeler = find_h2_block(muqeddime_block, "Mənbələr və yanaşma")
    kitab_istifade = find_h2_block(muqeddime_block, "Kitabın istifadə qaydası")
    mesuliyyet = find_h2_block(muqeddime_block, "Məsuliyyət qeydi")
    muellifler = find_h2_block(muqeddime_block, "Müəlliflər və əməkdaşlar")
    dunyada = find_h2_block(muqeddime_block, "DÜNYADA PSİXİ SAĞLAMLIQ")
    psixoterapiyanin = find_h2_block(muqeddime_block, "PSİXOTERAPİYANIN KLİNİK STRATEGİYALARI")
    protokol1 = find_h2_block(muqeddime_block, "PROTOKOLU №1")
    protokol2 = find_h2_block(muqeddime_block, "PROTOKOLU №2")
    akkreditasiya = find_h2_block(muqeddime_block, "AKKREDİTASİYA VƏ KEYFİYYƏT")

    def safe(x): return x if x else ''

    new_mug_content = "\n\n".join(filter(None, [
        h1_muq_tag,
        safe(oxucuya),
        safe(muellif),
        safe(giris_block),
        safe(yekun_block),
        safe(bu_kitab_niye),
        safe(bu_kitab_nedir),
        safe(kitab_strukturu),
        safe(menbeler),
        safe(kitab_istifade),
        safe(mesuliyyet),
        safe(muellifler),
        safe(dunyada),
        safe(psixoterapiyanin),
        safe(protokol1),
        safe(protokol2),
        safe(akkreditasiya),
    ]))

    # Preserve pnav at end if present
    pnav_match = re.search(r'<nav class="page-nav">[\s\S]*?</nav>', mug_content)
    pnav = pnav_match.group(0) if pnav_match else ''

    new_mug = mug_pre + "\n" + new_mug_content + "\n" + pnav + "\n    " + mug_post
    MUG.write_text(new_mug, encoding="utf-8")
    print(f"  mugeddime.html rewritten ({len(new_mug):,} chars)")

    # ── Build melumat.html: copy mugeddime.html as base, replace content ──
    melumat_content = "\n\n".join(filter(None, [
        safe(terminoloji_block),
        safe(psixopatologiya_block),
        safe(klinik_musahibe_block),
        safe(huquqi_etik_block),
    ]))
    # Use mugeddime.html as TEMPLATE — replace main content + adjust meta
    template = (BOOK / "mugeddime.html").read_text(encoding="utf-8")
    # Adjust title
    template = re.sub(r'<title>[^<]*</title>',
                      '<title>MƏLUMAT BÖLMƏSİ | KLİNİK PSİXİATRİYA</title>',
                      template)
    template = re.sub(r'<meta name="description"[^/]*/?>',
                      '<meta name="description" content="Klinik Psixiatriya — Terminoloji lüğət, psixopatologiya, klinik müsahibə və hüquqi-etik aspektlər">',
                      template, count=1)
    # Now replace main content
    pre, _content, post = extract_main(template)
    melumat = pre + "\n" + melumat_content + "\n" + post
    MEL.write_text(melumat, encoding="utf-8")
    print(f"  melumat.html created ({len(melumat):,} chars)")

    # ── giris-yekun.html: keep file but turn into a redirect to mugeddime ──
    redirect_html = '''<!DOCTYPE html>
<html lang="az">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0;url=mugeddime.html#giri%C5%9F">
<link rel="canonical" href="mugeddime.html#giriş">
<title>Redirecting…</title>
</head>
<body>
<p>Bu səhifə birləşdirilib. <a href="mugeddime.html#giriş">Mugeddiməyə keçin</a></p>
<script>window.location.replace("mugeddime.html#giriş");</script>
</body>
</html>
'''
    GY.write_text(redirect_html, encoding="utf-8")
    print(f"  giris-yekun.html → redirect to mugeddime.html")


if __name__ == "__main__":
    main()
