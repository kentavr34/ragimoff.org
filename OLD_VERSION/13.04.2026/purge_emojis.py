# -*- coding: utf-8 -*-
import os, re

# Comprehensive Emoji Regex
emoji_pattern = re.compile(
    u'[\U00010000-\U0010ffff]|'  # Supplementary Planes (most emojis)
    u'[\u2600-\u27BF]|'          # Miscellaneous Symbols and Dingbats
    u'[\u2300-\u23FF]|'          # Miscellaneous Technical
    u'[\u2B50]|'                 # Star
    u'[\u2934-\u2935]|'          # Arrows
    u'[\u2190-\u21FF]'           # More arrows
)

def purge_emojis(content):
    return emoji_pattern.sub('', content)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        if '.gemini' in root or '__pycache__' in root:
            continue
        for fn in files:
            if fn.endswith(('.html', '.js', '.css')):
                path = os.path.join(root, fn)
                try:
                    with open(path, 'r', encoding='utf-8', errors='replace') as f:
                        content = f.read()
                    
                    new_content = purge_emojis(content)
                    
                    if new_content != content:
                        print(f"Purging emojis from: {path}")
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                except Exception as e:
                    print(f"Error processing {path}: {e}")

if __name__ == "__main__":
    process_directory(os.getcwd())
    print("Emoji purge complete.")
