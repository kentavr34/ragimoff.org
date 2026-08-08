import re
import os

HTML_FILES = [
    r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\b2b.html',
    r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\cert.html',
    r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\haqqinda.html'
]

for file_path in HTML_FILES:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update border radius
        content = content.replace('border-radius: 12px;', 'border-radius: 4px;')
        content = content.replace('border-radius:12px;', 'border-radius:4px;')
        content = content.replace('border-radius: 8px;', 'border-radius: 4px;')
        content = content.replace('padding: 12px 24px;', 'padding: 18px 36px;')
        
        # Any 'max-width: 1000px' -> 'max-width: 1120px'
        content = content.replace('max-width: 1000px;', 'max-width: 1120px;')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

print("Fixed alternate files UI geometry.")
