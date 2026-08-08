# -*- coding: utf-8 -*-
import os, re, sys

# Set encoding for safety
sys.stdout.reconfigure(encoding='utf-8')

def purge_emojis(content):
    # Regex for various emoji ranges
    emoji_pattern = re.compile(
        u'[\U00010000-\U0010ffff]|'  # Supplementary Planes
        u'[\u2600-\u27BF]|'          # Miscellaneous Symbols and Dingbats
        u'[\u2300-\u23FF]|'          # Miscellaneous Technical
        u'[\u2B50]|'                 # Star
        u'[\u2934-\u2935]|'          # Arrows
        u'[\u2190-\u21FF]'           # More arrows
    )
    return emoji_pattern.sub('', content)

def replace_logos(content):
    # Replace the logo-box content with the new text wordmark
    new_logo_html = '''<span class="logo-text">RAGIMOFF<em>.</em></span><span class="logo-sub">Psixologiya Məktəbi</span>'''
    
    # Match any logo-box and replace its inner content (img or previous span)
    pattern = re.compile(r'(<a[^>]*class="logo-box"[^>]*>).*?(</a>)', re.DOTALL)
    content = pattern.sub(r'\1' + new_logo_html + r'\2', content)
    
    return content

def refine_tehsil(content):
    # 1. Darken finance bar
    content = content.replace('.finance-bar { background: rgba(0,0,0,0.3);', '.finance-bar { background: var(--navy);')
    
    # 2. Fix Hemkarlar heading (forced caps and wrapping)
    # The user said the text wraps poorly. I will adjust the header tag.
    content = content.replace('Təkcə həmkarlar deyil,<br>böyük bir ailə...', 'Həmkarlar Deyil — Böyük Bir Ailə')
    
    # 3. Alumni grid standardization (ensure it uses 3 cols)
    # Already set to 3 cols in previous step, but ensuring it's robust
    content = content.replace('grid-template-columns:repeat(3, 1fr)', 'grid-template-columns: repeat(3, 1fr)')

    # 4. Cert gallery to grid
    # Looking for the container of fame-items
    content = re.sub(
        r'(<div[^>]*class="[^"]*fame-container[^"]*"[^>]*>|<div>(?:\s*<div[^>]*class="fame-item"[^>]*>)+)',
        lambda m: m.group(1).replace('<div>', '<div class="grid-3-col" style="gap:20px;">') if '<div>' in m.group(1) else m.group(1).replace('class="fame-container"', 'class="grid-3-col" style="gap:20px;"'),
        content
    )
    
    return content

def refine_index(content):
    # 1. Hero photo proportions fix
    content = content.replace('grid-template-columns: 1.55fr 1fr;', 'grid-template-columns: 1.6fr 1fr;')
    content = content.replace('max-width: 360px; height: 440px;', 'max-width: 380px; height: 500px; max-height: 60vh;')
    
    return content

def process_files():
    target_dir = os.getcwd()
    html_files = [f for f in os.listdir(target_dir) if f.endswith('.html')]
    
    for fn in html_files:
        path = os.path.join(target_dir, fn)
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            
        print(f"Processing {fn}...")
        
        # Apply global changes
        content = purge_emojis(content)
        content = replace_logos(content)
        
        # Apply page-specific refinements
        if fn == 'tehsil.html':
            content = refine_tehsil(content)
        if fn == 'index.html':
            content = refine_index(content)
            
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    process_files()
    print("Design refinement complete.")
