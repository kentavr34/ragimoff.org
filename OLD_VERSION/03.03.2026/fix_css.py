import os

path = r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\shared.css'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace fonts globally in shared.css
text = text.replace("'Playfair Display', serif", "'Inter', -apple-system, sans-serif")
text = text.replace("'Lato', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif", "'Inter', -apple-system, sans-serif")

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("shared.css updated to Inter font")
