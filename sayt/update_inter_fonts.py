from pathlib import Path

html_files = list(Path('.').glob('*.html')) + list(Path('ru').glob('*.html'))

def replace_all(text):
    replacements = [
        (
            "https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,800;1,400&family=Lato:wght@300;400;700&family=Noto+Sans:wght@300;400;700&display=swap",
            "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap",
        ),
        (
            "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Noto+Sans:wght@300;400;500;700&display=swap&subset=latin,cyrillic",
            "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap&subset=latin,cyrillic",
        ),
        ("font-family:'Playfair Display',serif;", "font-family:'Inter',sans-serif;"),
        ("font-family:\"Playfair Display\",serif;", "font-family:'Inter',sans-serif;"),
        ("font-family: 'Playfair Display', serif;", "font-family: 'Inter', sans-serif;"),
        ("font-family: \"Playfair Display\", Georgia, 'Times New Roman', serif;", "font-family: 'Inter', sans-serif;"),
        ("font-family: 'Lato', 'Noto Sans', 'Segoe UI', Arial Unicode MS, sans-serif;", "font-family: 'Inter', 'Segoe UI', 'Arial Unicode MS', sans-serif;"),
        ("font-family: 'Noto Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;", "font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Arial Unicode MS', sans-serif;"),
        ("font-family: 'Noto Sans', 'Lato', 'Segoe UI', 'Arial Unicode MS', sans-serif;", "font-family: 'Inter', 'Segoe UI', 'Arial Unicode MS', sans-serif;"),
        ("font-family: 'Inter', sans-serif;", "font-family: 'Inter', sans-serif;"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text

for path in html_files:
    text = path.read_text(encoding='utf-8', errors='ignore')
    new_text = replace_all(text)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        print(f'Updated {path}')
