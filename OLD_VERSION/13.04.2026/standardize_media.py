#!/usr/bin/env python3
"""
Media Query Standardization Script for Ragimoff Site
Standardizes all media queries to use consistent breakpoints per UI_UX_STYLISTIC_CODEX.md
"""

import os
import re
from pathlib import Path

def standardize_media_queries_in_file(filepath):
    """Standardize media queries in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Standardize media query breakpoints
        # 1024px -> 1100px (tablet breakpoint)
        content = re.sub(r'@media\s*\(\s*max-width:\s*1024px\s*\)', '@media (max-width: 1100px)', content)

        # 900px -> 768px (tablet breakpoint)
        content = re.sub(r'@media\s*\(\s*max-width:\s*900px\s*\)', '@media (max-width: 768px)', content)

        # Ensure consistent spacing in media queries
        content = re.sub(r'@media\s*\(\s*max-width:\s*([0-9]+)px\s*\)', r'@media (max-width: \1px)', content)

        # Standardize padding values to use 8px grid
        # 24px -> 24px (already correct)
        # 20px -> 24px (round up)
        content = re.sub(r'padding-left:\s*20px;\s*padding-right:\s*20px', 'padding-left: 24px; padding-right: 24px', content)
        content = re.sub(r'padding:\s*104px\s*20px\s*56px', 'padding: 104px 24px 56px', content)
        content = re.sub(r'padding:\s*56px\s*20px', 'padding: 56px 24px', content)

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Standardized media queries in {filepath}")
            return True
        else:
            return False

    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")
        return False

def main():
    """Main standardization function"""
    workspace = Path('.')
    html_files = list(workspace.glob('*.html'))

    print("📱 Starting Media Query Standardization")
    print("Standardizing breakpoints: 360px, 640px, 768px, 1100px, 1280px")
    print(f"Found {len(html_files)} HTML files to process")

    processed_count = 0
    changed_count = 0

    for html_file in html_files:
        processed_count += 1
        if standardize_media_queries_in_file(html_file):
            changed_count += 1

    print(f"\n✅ Completed: {changed_count}/{processed_count} files updated")
    print("Media queries now use consistent breakpoints and 8px grid spacing")

if __name__ == '__main__':
    main()