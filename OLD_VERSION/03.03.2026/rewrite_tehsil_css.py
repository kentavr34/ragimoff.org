import os
import re

path = r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\tehsil.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Extract everything between <style> and </style>
pattern = re.compile(r'<style>.*?</style>', re.DOTALL)

NEW_STYLE = """<style>
    /* PAGE SPECIFIC PREMIUM CSS */
    .page-hero {
      background: var(--navy);
      padding: 180px 40px 100px; text-align: center; position: relative; overflow: hidden;
    }
    .page-hero::before {
      content: ''; position: absolute; top: -50%; left: 50%; transform: translateX(-50%);
      width: 1000px; height: 1000px; border-radius: 50%;
      background: radial-gradient(circle, rgba(181,155,114,0.08) 0%, transparent 70%);
      pointer-events: none;
    }
    .page-hero-tag { display: inline-block; border: 1px solid rgba(181,155,114,0.3); background: rgba(0,0,0,0.2); color: var(--accent); font-size: 0.75rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; padding: 8px 16px; border-radius: 2px; margin-bottom: 32px; }
    
    .hero-pills { display: flex; justify-content: center; gap: 16px; flex-wrap: wrap; margin-top: 40px;}
    .pill { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); color: var(--white); font-size: 0.85rem; padding: 10px 24px; border-radius: 2px; font-weight: 500; letter-spacing: 0.5px; }
    .pill strong { color: var(--accent); font-weight: 700; }

    /* TAB SELECTOR (Premium Layout) */
    .selector-section { background: var(--light); padding: 0 40px; position: sticky; top: 76px; z-index: 50; border-bottom: 1px solid var(--border); border-top: 1px solid var(--border); }
    .selector-inner { max-width: 1120px; margin: 0 auto; display: flex; align-items: stretch; justify-content: space-between; gap: 24px; padding: 32px 0; }
    .sel-tab {
      flex: 1; padding: 32px; text-align: left; cursor: pointer;
      border: 1px solid rgba(6,24,38,0.08); border-radius: 4px; transition: all .4s cubic-bezier(0.16, 1, 0.3, 1);
      display: flex; flex-direction: column; justify-content: center;
      background: var(--white);
    }
    .sel-tab:hover { border-color: var(--accent); transform: translateY(-4px); box-shadow: 0 12px 32px rgba(6,24,38,0.06); }
    .sel-tab.active { border-color: var(--navy); background: var(--navy); box-shadow: 0 16px 48px rgba(6,24,38,0.15); }
    
    .sel-tab > div > div { font-size: 1.15rem; font-weight: 700; color: var(--navy); margin-bottom: 8px; transition: color .3s; }
    .sel-tab .tab-sub { font-size: 0.85rem; font-weight: 400; color: var(--gray); display: block; line-height: 1.6; transition: color .3s; }
    .sel-tab.active > div > div { color: var(--white); }
    .sel-tab.active .tab-sub { color: rgba(255,255,255,0.7); }

    .program-panel { display: none; animation: fadeUp .5s cubic-bezier(0.16, 1, 0.3, 1); }
    .program-panel.active { display: block; }
    @keyframes fadeUp { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: translateY(0); } }

    /* Grid layouts */
    .sanəd-grid { display: grid; grid-template-columns: 1fr 400px; gap: 80px; align-items: start; max-width: 1120px; margin: 0 auto; }
    .sanəd-intro p { font-size: 1.125rem; font-weight: 300; line-height: 1.8; margin-bottom: 24px; }
    
    .highlight-box {
      background: var(--light);
      border-left: 4px solid var(--accent);
      padding: 32px; margin: 40px 0;
    }
    
    /* ACCOORDION */
    .accordion { margin-top: 48px; }
    .accordion-item { border: 1px solid var(--border); border-radius: 4px; margin-bottom: 16px; overflow: hidden; background: var(--light); transition: background .3s; }
    .accordion-head {
      display: flex; align-items: center; justify-content: space-between;
      padding: 24px 32px; cursor: pointer;
    }
    .accordion-head:hover { background: var(--white); }
    .accordion-head-left { display: flex; align-items: center; gap: 24px; }
    .accordion-icon { width: 48px; height: 48px; border-radius: 4px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; font-weight: 700; }
    .icon-doc { background: rgba(6,24,38,0.06); color: var(--navy); }
    .icon-prak { background: rgba(181,155,114,0.15); color: var(--accent); }
    .accordion-title { font-weight: 700; font-size: 1.1rem; color: var(--navy); }
    .accordion-subtitle { font-size: 0.85rem; color: var(--gray); margin-top: 4px; }
    .accordion-arrow { width: 24px; height: 24px; flex-shrink: 0; transition: transform .4s ease; color: var(--gray); }
    .accordion-item.open .accordion-arrow { transform: rotate(180deg); color: var(--navy); }
    .accordion-item.open { background: var(--white); box-shadow: 0 8px 32px rgba(6,24,38,0.04); border-color: var(--border); }
    .accordion-body { max-height: 0; overflow: hidden; transition: max-height .5s cubic-bezier(0.16, 1, 0.3, 1); }
    .accordion-body-inner { padding: 0 32px 32px 80px; } /* Indented to match icon */
    
    .doc-list { list-style: none; margin-top: 16px; }
    .doc-list li { display: flex; align-items: flex-start; gap: 16px; padding: 12px 0; border-bottom: 1px solid var(--border); font-size: 0.95rem; }
    .doc-list li:last-child { border-bottom: none; }
    .doc-check { color: var(--accent); font-weight: 700; flex-shrink: 0; }
    
    .law-links { margin-top: 24px; display:flex; flex-direction:column; gap:12px; }
    .law-link { display: flex; align-items: center; gap: 12px; padding: 16px 20px; border: 1px solid var(--border); border-radius: 4px; text-decoration: none; color: var(--navy); font-size: 0.9rem; font-weight: 500; transition: all .3s; }
    .law-link:hover { border-color: var(--navy); background: rgba(6,24,38,0.03); }
    
    /* RIGHT CARD */
    .sanəd-card { position: sticky; top: 180px; }
    .price-card { background: var(--navy); border-radius: 4px; padding: 48px; color: var(--white); margin-bottom: 24px; box-shadow: 0 24px 64px rgba(6,24,38,0.2); border: 1px solid rgba(255,255,255,0.05); }
    .price-card-tag { font-size: 0.75rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: var(--accent); margin-bottom: 16px; display: block; }
    .price-card h3 { font-size: 1.5rem; color: var(--white); margin-bottom: 24px; line-height: 1.3; }
    .price-main { font-size: 4rem; font-weight: 700; color: var(--white); line-height: 1; margin: 24px 0; letter-spacing: -0.03em; }
    .price-main span { font-size: 1.25rem; font-weight: 400; color: rgba(255,255,255,0.5); }
    .btn-enroll { display: block; text-align: center; background: var(--white); color: var(--navy); font-weight: 700; font-size: 0.95rem; padding: 20px; border-radius: 2px; text-decoration: none; transition: all .3s ease; text-transform: uppercase; letter-spacing: 1px; margin-top:40px; border: none; }
    .btn-enroll:hover { background: var(--accent); color: var(--white); transform: translateY(-2px); box-shadow: 0 10px 24px rgba(181,155,114,0.2); }
    
    /* COMMON PRAK ELEMENTS */
    .prak-hero { background: var(--navy); border-radius: 4px; padding: 64px; margin-bottom: 64px; margin-top: 64px; text-align: center; }
    .prak-hero h2 { font-size: 2.25rem; color: var(--white); margin-bottom: 16px; }
    .prak-hero p { color: rgba(255,255,255,0.7); font-size: 1.125rem; line-height: 1.8; max-width: 700px; margin: 0 auto; }
    
    .free-lesson { background: var(--light); border: 1px solid var(--border); border-radius: 4px; padding: 64px; margin-bottom: 64px; display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: center; }
    
    .curriculum-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-bottom: 64px; }
    .curr-card { border: 1px solid var(--border); border-radius: 4px; padding: 32px; background: var(--white); transition: all .3s ease; }
    .curr-card:hover { border-color: var(--navy); box-shadow: 0 12px 32px rgba(6,24,38,0.06); transform: translateY(-4px); }
    .curr-num { font-size: 0.85rem; font-weight: 700; color: var(--accent); letter-spacing: 2px; margin-bottom: 12px; display: block;}
    .curr-title { font-weight: 700; font-size: 1.1rem; color: var(--navy); margin-bottom: 12px; line-height: 1.4; }

    /* Fix Only Prak Tab specific style */
    .prak-card-alt { background: var(--white); border: 1px solid var(--border); color: var(--text); }
    .prak-card-alt .price-card-tag { color: var(--gray); }
    .prak-card-alt h3 { color: var(--navy); }
    .prak-card-alt .price-main { color: var(--navy); }
    .prak-card-alt .price-main span { color: var(--gray); }
    .prak-card-alt .btn-enroll { background: var(--navy); color: var(--white); }
    .prak-card-alt .btn-enroll:hover { background: var(--accent); color: var(--white); }

    @media (max-width: 1024px) {
      .sanəd-grid, .free-lesson { grid-template-columns: 1fr; }
      .sanəd-card { position: static; }
      .selector-inner { flex-direction: column; padding: 24px 0; gap: 16px; }
      .curriculum-grid { grid-template-columns: 1fr 1fr; }
      .accordion-body-inner { padding: 0 24px 24px 24px; }
    }
    @media (max-width: 640px) {
      .curriculum-grid { grid-template-columns: 1fr; }
    }
  </style>"""

new_text = pattern.sub(NEW_STYLE, text)

# Ensure the Only Prak tab has the alternate card style
if 'class="price-card" style="background:var(--white)' in new_text:
    new_text = new_text.replace('class="price-card" style="background:var(--white); border: 2px solid var(--border); color:var(--text);"', 'class="price-card prak-card-alt"')

# Fix inline YouTube / Networking buttons padding 
new_text = new_text.replace('padding:10px 18px;', 'padding: 16px 32px; font-weight: 600; text-transform: uppercase; font-size: 0.85rem; letter-spacing: 1px; border-radius: 4px;')
new_text = new_text.replace('border-radius:12px;', 'border-radius:4px;')
new_text = new_text.replace('border-radius: 12px;', 'border-radius: 4px;')

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_text)

print("tehsil.html perfectly rewritten with McKinsey grid and typography rules.")
