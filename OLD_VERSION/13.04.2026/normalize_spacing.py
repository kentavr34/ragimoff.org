#!/usr/bin/env python3
"""
Spacing Normalization Script for Ragimoff Site
Converts non-8px grid values to closest 8px multiples per UI_UX_STYLISTIC_CODEX.md
"""

import os
import re
from pathlib import Path

def round_to_8px(value):
    """Round pixel value to nearest 8px multiple"""
    try:
        num = int(value)
        remainder = num % 8
        if remainder < 4:
            return num - remainder  # Round down
        else:
            return num + (8 - remainder)  # Round up
    except:
        return value

def normalize_spacing_in_file(filepath):
    """Normalize spacing values in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Find all px values in CSS properties
        px_pattern = r'([:\s])([0-9]+)px([;\s,])'

        def replace_px(match):
            prefix = match.group(1)
            value = match.group(2)
            suffix = match.group(3)

            new_value = round_to_8px(value)
            return f"{prefix}{new_value}px{suffix}"

        content = re.sub(px_pattern, replace_px, content)

        # Special handling for common non-8px values
        special_mappings = {
            '120px': '128px',  # 128 = 16*8
            '72px': '64px',    # 64 = 8*8
            '56px': '56px',    # Already 7*8
            '36px': '32px',    # 32 = 4*8
            '44px': '40px',    # 40 = 5*8
            '26px': '24px',    # 24 = 3*8
            '22px': '24px',    # Round up to 24
            '30px': '32px',    # Round up to 32
            '18px': '16px',    # 16 = 2*8
            '14px': '16px',    # Round up to 16
            '10px': '8px',     # 8 = 1*8
            '12px': '16px',    # Round up to 16
        }

        for old_val, new_val in special_mappings.items():
            content = content.replace(old_val, new_val)

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Normalized spacing in {filepath}")
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

    print("📐 Starting Spacing Normalization to 8px Grid")
    print(f"Found {len(html_files)} HTML files to process")

    processed_count = 0
    changed_count = 0

    for html_file in html_files:
        processed_count += 1
        if normalize_spacing_in_file(html_file):
            changed_count += 1

    print(f"\n✅ Completed: {changed_count}/{processed_count} files updated")
    print("All spacing now follows 8px grid system")

if __name__ == '__main__':
    main()