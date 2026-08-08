import os
import re

CSS_PATH = r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\shared.css'
HTML_FILES = [
    r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\index.html',
    r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\tehsil.html',
    r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\b2b.html',
    r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\cert.html',
    r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\haqqinda.html'
]

NEW_CSS = """/* ═══════════════════════════════════════════════
   RAGIMOFF.ORG — Premium Shared Styles (McKinsey Style)
   ═══════════════════════════════════════════════ */
:root {
  --navy:   #061826;
  --blue:   #0a2540;
  --accent: #b59b72;
  --light:  #f7f9fc;
  --white:  #ffffff;
  --gray:   #5f6e85;
  --border: #e2e8f0;
  --text:   #2d3748;
  --green:  #1a5c38;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
html, body { overflow-x: hidden; }
body { 
  font-family: 'Inter', -apple-system, blinkmacsystemfont, sans-serif; 
  color: var(--text); 
  background: var(--white); 
  line-height: 1.75; 
  font-size: 18px; /* Boosted base for reading */
  -webkit-font-smoothing: antialiased;
}

/* ── HEADER ── */
header { position: fixed; top: 0; left: 0; right: 0; z-index: 100; background: rgba(6, 24, 38, 0.98); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(255,255,255,0.05); }
.header-inner { max-width: 1120px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; padding: 0 32px; height: 76px; }
.logo { font-size: 1.25rem; font-weight: 700; color: var(--white); text-decoration: none; letter-spacing: 1.5px; text-transform: uppercase; }
.logo span { color: var(--accent); }
nav { display: flex; gap: 8px; align-items: center; }
nav a { color: rgba(255,255,255,0.7); text-decoration: none; font-size: 0.8rem; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; padding: 8px 16px; border-radius: 2px; transition: all .3s ease; }
nav a:hover, nav a.active { color: var(--accent); }
.nav-cta { background: var(--white) !important; color: var(--navy) !important; font-weight: 700; }
.nav-cta:hover { background: var(--accent) !important; color: var(--white) !important; }

/* ── LAYOUT ── */
.wrap { max-width: 1120px; margin: 0 auto; padding: 0 40px; }
section { padding: 120px 40px; }
.section-inner { max-width: 900px; margin: 0 auto; }
.section-inner.wide { max-width: 1120px; }

/* ── TYPOGRAPHY MATH ── */
.tag { font-size: 0.7rem; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; color: var(--accent); margin-bottom: 16px; display: block; }
h1, .h1 { font-size: clamp(2.5rem, 5vw, 4rem); font-weight: 700; color: var(--navy); line-height: 1.1; letter-spacing: -0.02em; margin-bottom: 24px; text-wrap: balance; }
h2, .h2 { font-size: clamp(2rem, 3.5vw, 2.75rem); font-weight: 700; color: var(--navy); line-height: 1.2; letter-spacing: -0.01em; margin-bottom: 20px; text-wrap: balance; }
h3, .h3 { font-size: 1.5rem; font-weight: 600; color: var(--navy); line-height: 1.35; margin-bottom: 12px; text-wrap: balance; }
p { margin-bottom: 24px; }
.lead { font-size: 1.25rem; color: var(--gray); line-height: 1.7; font-weight: 300; margin-bottom: 32px; }

/* ── COMPONENTS / CARDS ── */
.card { background: var(--white); border: 1px solid var(--border); border-radius: 4px; padding: 40px; transition: transform .4s ease, box-shadow .4s ease; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
.card:hover { transform: translateY(-4px); box-shadow: 0 20px 40px rgba(6,24,38,0.08); border-color: rgba(6,24,38,0.1); }
.card-dark { background: var(--navy); border: 1px solid rgba(255,255,255,0.08); color: var(--white); border-radius: 4px; padding: 48px; }

/* ── BUTTONS (Standardized proportions) ── */
.btn { display: inline-flex; align-items: center; justify-content: center; text-decoration: none; font-weight: 600; font-size: 0.85rem; letter-spacing: 1px; text-transform: uppercase; border-radius: 2px; transition: all .3s ease; cursor: pointer; border: none; padding: 18px 36px; line-height: 1; }
.btn-primary { background: var(--accent); color: var(--white); box-shadow: 0 4px 14px rgba(181,155,114,0.3); }
.btn-primary:hover { background: #a28962; transform: translateY(-2px); box-shadow: 0 8px 24px rgba(181,155,114,0.4); }
.btn-navy { background: var(--navy); color: var(--white); }
.btn-navy:hover { background: var(--blue); transform: translateY(-2px); }
.btn-outline { border: 1px solid rgba(255,255,255,0.3); color: var(--white); background: transparent; }
.btn-outline:hover { border-color: var(--white); background: rgba(255,255,255,0.05); }
.btn-outline-dark { border: 1px solid var(--border); color: var(--text); background: transparent; }
.btn-outline-dark:hover { border-color: var(--navy); color: var(--navy); }
.btn-sm { padding: 12px 24px; font-size: 0.75rem; }

/* ── FORMS ── */
.form-group { margin-bottom: 24px; }
.form-group label { display: block; font-size: 0.75rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: var(--gray); margin-bottom: 8px; }
.form-group input, .form-group select, .form-group textarea { width: 100%; padding: 16px 20px; border: 1px solid var(--border); border-radius: 2px; font-family: inherit; font-size: 1rem; color: var(--text); background: var(--light); transition: all .3s ease; }
.form-group input:focus, .form-group textarea:focus { border-color: var(--accent); background: var(--white); box-shadow: 0 0 0 4px rgba(181,155,114,0.1); outline: none; }

/* ── FOOTER ── */
footer { background: var(--navy); color: rgba(255,255,255,0.5); padding: 80px 40px 40px; }
.footer-inner { max-width: 1120px; margin: 0 auto; display: flex; flex-direction: column; gap: 40px; }
.footer-bottom { border-top: 1px solid rgba(255,255,255,0.1); padding-top: 32px; display: flex; justify-content: space-between; font-size: 0.85rem; }
.footer-bottom a { color: rgba(255,255,255,0.5); text-decoration: none; transition: color .3s; }
.footer-bottom a:hover { color: var(--accent); }

@media (max-width: 768px) {
  section { padding: 80px 24px; }
  .wrap { padding: 0 24px; }
  h1, .h1 { font-size: 2.25rem; }
  h2, .h2 { font-size: 1.75rem; }
  .btn { padding: 16px 24px; width: 100%; text-align: center; }
  nav { display: none; }
}
"""

with open(CSS_PATH, 'w', encoding='utf-8') as f:
    f.write(NEW_CSS)

# 2. Iterate HTML files and fix inline styles breaking the premium look
def convert_inline_styles(text):
    # Remove awkward inline max-widths that interfere with global balance
    text = re.sub(r'style="max-width: \d+px;.*?"', '', text)
    # Remove inline line-heights
    text = re.sub(r'line-height:\s*[\d.]+;?', '', text)
    # Clean up multiple empty style tags
    text = re.sub(r'style="\s*"', '', text)
    return text

for file_path in HTML_FILES:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # We will keep tehsil.html hero specific text align, but strip the messy manual max-widths on paragraphs
        # Specifically targeting <p style="max-width: 550px... etc
        content = re.sub(r'max-width:\s*\d+px;?', '', content)
        
        # Rewrite the menu btn slightly to match the new class
        content = content.replace('btn btn-primary btn-sm', 'btn nav-cta btn-sm')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

print("Premium Design Overhaul Applied to CSS and HTML constraints stripped.")
