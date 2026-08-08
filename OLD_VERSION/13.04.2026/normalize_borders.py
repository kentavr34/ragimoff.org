#!/usr/bin/env python3
"""
Border-Radius Normalization Script for Ragimoff Site
Converts border-radius to 2px or 8px only per UI_UX_STYLISTIC_CODEX.md
"""

import os
import re
from pathlib import Path

def normalize_border_radius(value):
    """Normalize border-radius to 2px or 8px"""
    try:
        num = int(value.replace('px', ''))
        if num <= 4:
            return '2px'  # Staccato (sharp)
        else:
            return '8px'  # Soft
    except:
        return value

def normalize_border_radius_in_file(filepath):
    """Normalize border-radius in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Find all border-radius values
        radius_pattern = r'border-radius:\s*([0-9]+px)'

        def replace_radius(match):
            current_value = match.group(1)
            new_value = normalize_border_radius(current_value)
            return f'border-radius: {new_value}'

        content = re.sub(radius_pattern, replace_radius, content)

        # Specific problematic values from audit
        radius_mappings = {
            '10px': '8px',
            '12px': '8px',
            '14px': '8px',
            '6px': '8px',   # Round up to 8px
            '20px': '8px',
            '16px': '8px',
            '4px': '2px',   # Staccato
        }

        for old_radius, new_radius in radius_mappings.items():
            content = content.replace(f'border-radius:{old_radius}', f'border-radius:{new_radius}')
            content = content.replace(f'border-radius: {old_radius}', f'border-radius: {new_radius}')

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Normalized border-radius in {filepath}")
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

    print("🔲 Starting Border-Radius Normalization (2px or 8px only)")
    print(f"Found {len(html_files)} HTML files to process")

    processed_count = 0
    changed_count = 0

    for html_file in html_files:
        processed_count += 1
        if normalize_border_radius_in_file(html_file):
            changed_count += 1

    print(f"\n✅ Completed: {changed_count}/{processed_count} files updated")
    print("Border-radius now follows 2px/8px rule (staccato/soft)")

if __name__ == '__main__':
    main()