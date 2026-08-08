# -*- coding: utf-8 -*-
"""Fix index.html hero proportions and tehsil.html layout issues"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ===== INDEX.HTML =====
print('[index.html] Hero proportions fix')
with open('index.html', 'r', encoding='utf-8', errors='replace') as f:
    c = f.read()

# Fix hero grid - text gets more space, photo constrained
c = c.replace(
    '.hub-hero { background: linear-gradient(135deg, var(--navy) 0%, #162d58 100%); padding: 120px 32px 80px; color: var(--white); overflow: hidden; position: relative; }',
    '.hub-hero { background: linear-gradient(160deg, #061826 0%, #0d2240 100%); padding: 100px 40px 80px; color: var(--white); overflow: hidden; position: relative; }'
)
c = c.replace(
    '.hub-hero-inner {  margin: 0 auto; display: grid; grid-template-columns: 1.2fr 1fr; gap: 60px; align-items: center; }',
    '.hub-hero-inner { max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 1.55fr 1fr; gap: 80px; align-items: center; }'
)
c = c.replace(
    '.hub-badge { display: inline-block; border: 1px solid rgba(255,255,255,0.2); background: rgba(255,255,255,0.05); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); color: var(--accent); font-size: 0.75rem; font-weight: 700; padding: 6px 18px; border-radius: 20px; margin-bottom: 24px; letter-spacing: 1px; text-transform: uppercase; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }',
    '.hub-badge { display: inline-block; border: 1px solid rgba(181,155,114,0.4); background: rgba(181,155,114,0.06); color: var(--accent); font-size: 0.72rem; font-weight: 700; padding: 7px 16px; border-radius: 2px; margin-bottom: 28px; letter-spacing: 2px; text-transform: uppercase; }'
)
c = c.replace(
    '.hub-hero h1 { font-size: clamp(2.2rem, 4vw, 3.5rem); color: var(--white); margin-bottom: 16px; line-height: 1.15; }',
    '.hub-hero h1 { font-size: clamp(2.4rem, 3.4vw, 3.6rem); color: var(--white); margin-bottom: 20px; line-height: 1.1; font-weight: 800; letter-spacing: -0.03em; }'
)
c = c.replace(
    '.hub-hero p { font-size: 1.05rem; color: rgba(255,255,255,0.7);  margin-bottom: 30px; line-height: 1.7; }',
    '.hub-hero p { font-size: 1rem; color: rgba(255,255,255,0.68); margin-bottom: 36px; line-height: 1.75; max-width: 520px; }'
)
# Fix photo container - constrain height, crop portrait
c = c.replace(
    '.hero-photo-container { position: relative; }',
    '.hero-photo-container { position: relative; display: flex; justify-content: flex-end; }'
)
c = c.replace(
    '.hero-photo-container img { width: 100%;  border-radius: 12px; box-shadow: 0 20px 40px rgba(0,0,0,0.3); border: 2px solid rgba(200,169,110,0.2); }',
    '.hero-photo-container img { width: 100%; max-width: 360px; height: 440px; object-fit: cover; object-position: center top; border-radius: 4px; box-shadow: 0 32px 64px rgba(0,0,0,0.45); border: 1px solid rgba(181,155,114,0.2); }'
)

# Fix about section - image too large
c = c.replace(
    '.about-sec img { width: 100%; border-radius: 12px; box-shadow: 15px 15px 0 rgba(200,169,110,0.1); }',
    '.about-sec img { width: 100%; max-width: 380px; height: 460px; object-fit: cover; border-radius: 4px; box-shadow: 8px 8px 0 rgba(181,155,114,0.12); display: block; }'
)
c = c.replace(
    '.about-inner {  margin: 0 auto; display: grid; grid-template-columns: 1fr 1.2fr; gap: 60px; align-items: center; }',
    '.about-inner { max-width: 1100px; margin: 0 auto; display: grid; grid-template-columns: 1fr 1.5fr; gap: 70px; align-items: center; }'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('  + Saved\n')


# ===== TEHSIL.HTML - fix alumni grid and cert gallery =====
print('[tehsil.html] Layout fixes')
with open('tehsil.html', 'rb') as f:
    raw = f.read()
c = raw.decode('utf-8', errors='replace')

# Fix alumni grid - was repeat(auto-fit, minmax(300px, 1fr)) which on wide screens gives 1 col with too-wide cards
# Change to fixed 3 cols
c = c.replace(
    'display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:32px;',
    'display:grid; grid-template-columns:repeat(3, 1fr); gap:28px;'
)

# Fix the "HEMKARLAR" section - text is all-caps because of CSS, and title wraps badly
# Find and fix the h2 in that section
old_hemkar = 'Təkcə həmkarlar deyil,<br>böyük bir ailə...'
new_hemkar = 'Həmkarlar Deyil — <br>Böyük Bir Ailə'
c = c.replace(old_hemkar, new_hemkar)

# Fix ANY text-transform:uppercase on large h2 blocks in tehsil
# The section with big all-caps text - remove text-transform from panel-col dark sections
# Find panel dark sections with oversized text
c = re.sub(
    r'(style="[^"]*?)text-transform:\s*uppercase([^"]*?"[^>]*>)(\s*(?:Təkcə|TƏKCƏ|Sertifikat|SERTIFIKAT))',
    r'\1\2\3',
    c
)

# Fix cert gallery - currently single col, make 3-col grid
# Find the gallery container (images stacked vertically)
# Look for the pattern of cert images in a flex/single column
cert_single = 'display:flex; flex-direction:column; gap:20px; align-items:center;'
if cert_single in c:
    c = c.replace(
        cert_single,
        'display:grid; grid-template-columns:repeat(3,1fr); gap:20px; align-items:start;'
    )
    print('  + Cert gallery fixed to 3-col grid')
else:
    print('  ! Cert gallery pattern not found - checking alternatives')
    # Check for another pattern
    if 'lightbox' in c.lower():
        # Find the gallery section
        gal_idx = c.find('lightbox')
        print('  Lightbox found at:', gal_idx)
        print('  Context:', repr(c[max(0,gal_idx-200):gal_idx+200]))

with open('tehsil.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('  + Saved\n')

print('Done!')
