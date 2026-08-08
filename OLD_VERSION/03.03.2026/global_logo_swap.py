# -*- coding: utf-8 -*-
import os, re

# New Logo Wordmark Template
LOGO_AZ = '<span class="logo-text">RAGIMOFF<em>.</em></span><span class="logo-sub">Psixologiya Məktəbi</span>'
LOGO_RU = '<span class="logo-text">RAGIMOFF<em>.</em></span><span class="logo-sub">Школа Психологии</span>'

def replace_logo_box(content, is_ru=False):
    logo_content = LOGO_RU if is_ru else LOGO_AZ
    # Targets any tag with class containing "logo-box" or "logo" (if in header/footer)
    # We prioritize logo-box
    pattern = re.compile(r'(<a[^>]*class="[^"]*logo(?:-box)?[^"]*"[^>]*>).*?(</a>)', re.DOTALL)
    return pattern.sub(lambda m: m.group(1) + logo_content + m.group(2), content)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        if '.gemini' in root or '__pycache__' in root:
            continue
        for fn in files:
            if fn.endswith('.html'):
                path = os.path.join(root, fn)
                is_ru = 'ru' in root or fn == '2.html' or fn == '3.html' or fn == '5.html' # Conservative RU check
                # Better RU check: check lang attribute
                
                try:
                    with open(path, 'r', encoding='utf-8', errors='replace') as f:
                        content = f.read()
                    
                    # Finalize RU check
                    if 'lang="ru"' in content:
                        is_ru = True
                    
                    new_content = replace_logo_box(content, is_ru)
                    
                    if new_content != content:
                        print(f"Swapping logo in: {path} (RU: {is_ru})")
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                except Exception as e:
                    print(f"Error processing {path}: {e}")

if __name__ == "__main__":
    process_directory(os.getcwd())
    print("Logo swap complete.")
