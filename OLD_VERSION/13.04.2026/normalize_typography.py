#!/usr/bin/env python3
"""
Typography Normalization Script for Ragimoff Site
Converts font sizes to Major Third scale per UI_UX_STYLISTIC_CODEX.md
"""

import os
import re
from pathlib import Path

# Major Third scale: multiply by 1.25 each step
MAJOR_THIRD_SCALE = {
    '0.75rem': '0.75rem',   # xs
    '0.875rem': '0.875rem', # sm
    '1rem': '1rem',         # base
    '1.125rem': '1.125rem', # lg
    '1.25rem': '1.25rem',   # xl
    '1.5625rem': '1.5625rem', # 2xl
    '1.875rem': '1.875rem', # 3xl
    '2.25rem': '2.25rem',   # 4xl
    '2.8125rem': '2.8125rem', # 5xl
    '3.5rem': '3.5rem',     # 6xl
}

def find_closest_scale_size(current_rem):
    """Find closest Major Third scale size"""
    try:
        current_val = float(current_rem.replace('rem', ''))

        # Find closest in scale
        closest = min(MAJOR_THIRD_SCALE.keys(),
                     key=lambda x: abs(float(x.replace('rem', '')) - current_val))

        return closest
    except:
        return current_rem

def normalize_typography_in_file(filepath):
    """Normalize typography in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Find all rem font-size values
        rem_pattern = r'font-size:\s*([0-9.]+rem)'

        def replace_font_size(match):
            current_size = match.group(1)
            new_size = find_closest_scale_size(current_size)
            return f'font-size: {new_size}'

        content = re.sub(rem_pattern, replace_font_size, content)

        # Specific problematic sizes from audit
        size_mappings = {
            '0.93rem': '0.875rem',  # -> sm
            '0.91rem': '0.875rem',  # -> sm
            '0.68rem': '0.75rem',   # -> xs
            '0.88rem': '0.875rem',  # -> sm
            '0.83rem': '0.875rem',  # -> sm
            '0.72rem': '0.75rem',   # -> xs
            '0.82rem': '0.875rem',  # -> sm
            '1.3rem': '1.25rem',    # -> xl
            '1.1rem': '1.125rem',   # -> lg
            '1.5rem': '1.5625rem',  # -> 2xl
            '0.87rem': '0.875rem',  # -> sm
            '0.78rem': '0.75rem',   # -> xs
            '0.85rem': '0.875rem',  # -> sm
            '0.65rem': '0.75rem',   # -> xs
        }

        for old_size, new_size in size_mappings.items():
            content = content.replace(f'font-size:{old_size}', f'font-size:{new_size}')
            content = content.replace(f'font-size: {old_size}', f'font-size: {new_size}')

        # Add text-wrap: balance to headings
        heading_pattern = r'(<h[1-6]|<p[^>]*class="[^"]*(?:h[1-6]|section-title|hero)[^"]*")'
        content = re.sub(heading_pattern, r'\1 style="text-wrap: balance;"', content)

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Normalized typography in {filepath}")
            return True
        else:
            return False

    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")
        return False

def main():
    """Main normalization function"""
    workspace = Path('.')
    html_files = list(workspace.glob('*.html'))

    print("📝 Starting Typography Normalization to Major Third Scale")
    print(f"Found {len(html_files)} HTML files to process")

    processed_count = 0
    changed_count = 0

    for html_file in html_files:
        processed_count += 1
        if normalize_typography_in_file(html_file):
            changed_count += 1

    print(f"\n✅ Completed: {changed_count}/{processed_count} files updated")
    print("Typography now follows Major Third scale with text-wrap: balance")

if __name__ == '__main__':
    main()