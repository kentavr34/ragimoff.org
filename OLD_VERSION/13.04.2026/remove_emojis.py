#!/usr/bin/env python3
"""
Emoji Removal Script for Ragimoff Site
Removes emojis and replaces with typographic symbols per UI_UX_STYLISTIC_CODEX.md
"""

import os
import re
from pathlib import Path

def remove_emojis_in_file(filepath):
    """Remove emojis from a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Remove emojis (Unicode ranges for emojis)
        emoji_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002500-\U00002BEF\U00002702-\U000027B0\U00002702-\U000027B0\U000024C2-\U0001F251\U0001f926-\U0001f937\U00010000-\U0010ffff\u2640-\u2642\u2600-\u2B55\u200d\u23cf\u23e9\u231a\ufe0f\u3030]'

        content = re.sub(emoji_pattern, '', content)

        # Replace specific emoji contexts with typographic symbols
        replacements = {
            '️ Qanuni əsaslar': '✓ Qanuni əsaslar',
            '‍️ Dr. Rəhimov haqqında': '✓ Dr. Rəhimov haqqında',
            '️ Telegram kanal': '✓ Telegram kanal',
        }

        for old_text, new_text in replacements.items():
            content = content.replace(old_text, new_text)

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Removed emojis from {filepath}")
            return True
        else:
            return False

    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")
        return False

def main():
    """Main emoji removal function"""
    workspace = Path('.')
    html_files = list(workspace.glob('*.html'))

    print("🚫 Starting Emoji Removal per UI_UX_STYLISTIC_CODEX.md")
    print(f"Found {len(html_files)} HTML files to process")

    processed_count = 0
    changed_count = 0

    for html_file in html_files:
        processed_count += 1
        if remove_emojis_in_file(html_file):
            changed_count += 1

    print(f"\n✅ Completed: {changed_count}/{processed_count} files updated")
    print("Emojis removed, replaced with typographic checkmarks ✓")

if __name__ == '__main__':
    main()