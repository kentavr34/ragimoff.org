# -*- coding: utf-8 -*-
import sys, os

def fix_print():
    # Force output to utf-8
    sys.stdout.reconfigure(encoding='utf-8')
    
    target_files = ['index.html', 'tehsil.html']
    
    for fn in target_files:
        if not os.path.exists(fn): continue
        with open(fn, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        print(f"--- FILE: {fn} ---")
        
        # Footer Logo
        footer_idx = content.find('<footer')
        if footer_idx != -1:
            print("KEY: footer_logo_area")
            # Look for logo-box within footer
            logo_start = content.find('logo-box', footer_idx)
            if logo_start != -1:
                print(content[max(0, logo_start-100):logo_start+500])
        
        # Hero Index
        if fn == 'index.html':
            print("KEY: hero_section")
            hero_idx = content.find('hub-hero')
            if hero_idx != -1:
                print(content[hero_idx:hero_idx+2000])
        
        # Tehsil Blocks
        if fn == 'tehsil.html':
            print("KEY: alumni_section")
            alumni_idx = content.find('alumni')
            if alumni_idx != -1:
                print(content[alumni_idx:alumni_idx+1500])
                
            print("KEY: hemkarlar_section")
            hem_idx = content.find('Təkcə həmkarlar deyil')
            if hem_idx != -1:
                print(content[max(0, hem_idx-200):hem_idx+800])
                
            print("KEY: cert_gallery")
            # Usually images with 'cert'
            cert_idx = content.find('cert')
            if cert_idx != -1:
                # Find the nearest container div
                div_start = content.rfind('<div', 0, cert_idx)
                print(content[div_start:div_start+2000])

        print("-" * 50)

if __name__ == "__main__":
    fix_print()
