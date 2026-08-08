# -*- coding: utf-8 -*-
import os, re

def search_blocks():
    target_files = ['index.html', 'tehsil.html']
    results = {}
    
    for fn in target_files:
        if not os.path.exists(fn): continue
        with open(fn, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        results[fn] = {}
        
        # 1. Look for footer logo
        footer_idx = content.find('<footer')
        if footer_idx != -1:
            results[fn]['footer_snippet'] = content[footer_idx:footer_idx+800]
            
        # 2. Look for tehsil blocks
        if fn == 'tehsil.html':
            # Alumni
            alumni_idx = content.find('alumni')
            results[fn]['alumni_snippet'] = content[alumni_idx:alumni_idx+1000] if alumni_idx != -1 else 'NONE'
            
            # Certificates
            # Match certificate-like images or containers
            cert_match = re.search(r'(<div[^>]*>(?:\s*<img[^>]+(?:cert|Diploma)[^>]+>\s*)+</div>)', content, re.I | re.S)
            results[fn]['cert_snippet'] = cert_match.group(1) if cert_match else 'NONE'
            
            # Hemkarlar
            hem_idx = content.find('Təkcə həmkarlar deyil')
            results[fn]['hemkarlar_snippet'] = content[max(0, hem_idx-400):hem_idx+800] if hem_idx != -1 else 'NONE'

        # 3. Look for Hero photo in index
        if fn == 'index.html':
            hero_idx = content.find('hub-hero')
            results[fn]['hero_snippet'] = content[hero_idx:hero_idx+1500] if hero_idx != -1 else 'NONE'

    for fn, data in results.items():
        print(f"--- FILE: {fn} ---")
        for key, snippet in data.items():
            print(f"KEY: {key}")
            print(snippet)
            print("-" * 20)

if __name__ == "__main__":
    search_blocks()
