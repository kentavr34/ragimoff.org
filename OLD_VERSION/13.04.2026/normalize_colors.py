#!/usr/bin/env python3
"""
Color Normalization Script for Ragimoff Site
Converts non-standard colors to 60-30-10 palette per UI_UX_STYLISTIC_CODEX.md
"""

import os
import re
from pathlib import Path

# Color mappings based on 60-30-10 rule
COLOR_MAPPINGS = {
    # Greens to accent (gold)
    '#1a2a0d': 'var(--accent)',  # Dark green
    '#1e4080': 'var(--navy)',    # Blue-green
    '#0d1b3e': 'var(--navy)',    # Dark blue
    '#1a3a6e': 'var(--navy)',    # Medium blue
    '#e8f0e8': 'var(--light)',   # Light green background
    '#1a5c38': 'var(--accent)',  # Green text
    '#fde8e8': 'var(--light)',   # Light red background
    '#8b1a1a': 'var(--navy)',    # Dark red
    '#fdf4f4': 'var(--light)',   # Very light red
    '#f0d0d0': 'rgba(181,155,114,0.1)',  # Light red border
    '#f4fdf4': 'var(--light)',   # Light green
    '#c0e0c0': 'rgba(181,155,114,0.2)',  # Green border

    # Additional colors found in audit
    '#7a3030': 'var(--navy)',    # Dark red text
    '#1e4a1e': 'var(--accent)',  # Dark green text
    '#f5f5f5': 'var(--light)',   # Light gray
    '#e8edf5': 'var(--light)',   # Light blue-gray
    '#0d2c56': 'var(--navy)',    # Dark blue
    '#5a1a1a': 'var(--navy)',    # Dark red text
    '#25D366': '#25D366',        # WhatsApp green (keep as is)
    '#1ab954': '#1ab954',        # WhatsApp hover (keep as is)
    '#d9bc82': 'var(--gold)',    # Light gold
    '#333': 'var(--gray)',      # Dark gray
    '#c0392b': 'var(--accent)',  # Red accent

    # Standardize whites and grays
    '#fff': 'var(--white)',
    '#ffffff': 'var(--white)',
    '#444': 'var(--gray)',
    '#4a5568': 'var(--gray)',

    # Accent variations
    '#b59b72': 'var(--accent)',
    '#d4af37': 'var(--gold)',
    '#061826': 'var(--navy)',
    '#0a2540': 'var(--blue)',
    '#f8f9fa': 'var(--light)',
    '#f7f9fc': 'var(--light)',
    '#e2e8f0': 'var(--border)',
}

def normalize_colors_in_file(filepath):
    """Normalize colors in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Replace hex colors
        for old_color, new_color in COLOR_MAPPINGS.items():
            # Match hex colors in CSS properties
            pattern = r'([:\s,])(' + re.escape(old_color) + r')([;\s,])'
            content = re.sub(pattern, r'\1' + new_color + r'\3', content)

            # Match in gradients
            gradient_pattern = r'(linear-gradient\([^)]*)' + re.escape(old_color) + r'([^)]*\))'
            content = re.sub(gradient_pattern, r'\1' + new_color + r'\2', content)

        # Replace rgba values that should be variables
        rgba_mappings = {
            'rgba(255,255,255,0.7)': 'rgba(255, 255, 255, 0.7)',
            'rgba(255,255,255,0.8)': 'rgba(255, 255, 255, 0.8)',
            'rgba(6,24,38,0.98)': 'rgba(6, 24, 38, 0.98)',
            'rgba(181,155,114,0.1)': 'rgba(181, 155, 114, 0.1)',
            'rgba(181,155,114,0.2)': 'rgba(181, 155, 114, 0.2)',
            'rgba(181,155,114,0.3)': 'rgba(181, 155, 114, 0.3)',
        }

        for old_rgba, new_rgba in rgba_mappings.items():
            content = content.replace(old_rgba, new_rgba)

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Normalized colors in {filepath}")
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

    print("🎨 Starting Color Normalization per UI_UX_STYLISTIC_CODEX.md")
    print(f"Found {len(html_files)} HTML files to process")

    processed_count = 0
    changed_count = 0

    for html_file in html_files:
        processed_count += 1
        if normalize_colors_in_file(html_file):
            changed_count += 1

    print(f"\n✅ Completed: {changed_count}/{processed_count} files updated")
    print("Color palette now follows 60-30-10 rule (navy/light/accent)")

if __name__ == '__main__':
    main()