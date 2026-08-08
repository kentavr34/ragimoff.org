import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

# The standard font link
NEW_FONT_LINK = '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,800;1,400&family=Lato:wght@300;400;700&family=Noto+Sans:wght@300;400;700&display=swap" rel="stylesheet"/>'

# Regex for old Inter font links
OLD_FONT_REGEX = re.compile(r'<link [^>]*?family=Inter[^>]*?>', re.IGNORECASE)

# Legacy file name cleanup
REPLACEMENTS = {
    'haqqinda.html': 'haqqimda.html',
    'photo-portal-crop -2.jpg': 'photo-portal-crop.jpg' # Fixing a likely typo found in index.html
}

for file in html_files:
    # Skip haqqinda.html as it's the legacy version we are moving AWAY from
    if file == 'haqqinda.html':
        continue
        
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update Font Links
    if re.search(OLD_FONT_REGEX, content):
        content = re.sub(OLD_FONT_REGEX, NEW_FONT_LINK, content)
    elif 'Playfair+Display' not in content:
        # If no Inter link but also no Playfair link, inject before shared.css
        if '<link rel="stylesheet" href="shared.css"/>' in content:
            content = content.replace('<link rel="stylesheet" href="shared.css"/>', f'{NEW_FONT_LINK}\n  <link rel="stylesheet" href="shared.css"/>')
            
    # 2. Bulk text replacements
    for old, new in REPLACEMENTS.items():
        content = content.replace(old, new)
        
    # 3. Remove Inter font overrides in <style>
    content = content.replace("font-family: 'Inter', -apple-system, sans-serif;", "")
    content = content.replace("font-family: 'Inter', sans-serif;", "")
    
    # 4. Remove extra newlines (optional but keeps it cleaner)
    # content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Bulk standardization complete.")
