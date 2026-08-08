import os
import re

dir_path = r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff'

# Emojis regex pattern matching mostly colorful emojis, but allowing basic text symbols like ✓ (U+2713)
# We will use the emoji library if available, otherwise a simple regex.
emoji_pattern = re.compile(
    r'(?:[\U0001F300-\U0001F64F]' # symbols & pictographs
    r'|[\U0001F680-\U0001F6FF]' # transport & map
    r'|[\U0001F1E6-\U0001F1FF]' # flags
    r'|[\U0002600-\U00027BF]'   # misc symbols (some might be ok, but usually bad)
    r'|[\U0001F900-\U0001F9FF]' # supplemental symbols
    r'|[\U0001FA70-\U0001FAFF]' # symbols and pictographs extended
    r')'
)

def remove_emojis(text):
    return emoji_pattern.sub('', text)

for root, dirs, files in os.walk(dir_path):
    for f in files:
        if f.endswith('.html'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            new_content = remove_emojis(content)
            
            # we also replace any stray ✅ or ❌ just in case they slipped through
            new_content = new_content.replace('✅', '✓').replace('❌', '-').replace('🎓', '').replace('🔥', '').replace('📈', '').replace('💡', '')
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f"Cleaned emojis from {f}")

print("Emoji cleanup complete.")
