import os

files = [
    r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\index.html',
    r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\tehsil.html',
    r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\b2b.html',
    r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\cert.html',
]

menu_html = """<nav class="desktop-nav">
      <a href="index.html">Ana Səhifə</a>
      <a href="tehsil.html">Təhsil</a>
      <a href="index.html#services">Konsultasiya</a>
      <a href="b2b.html">Korporativ</a>
      <a href="cert.html">Sertifikat</a>
      <a href="tehsil.html#registration" class="btn btn-primary btn-sm" style="margin-left:14px; background:var(--accent); color:var(--navy); padding: 8px 16px;">Qeydiyyat</a>
    </nav>"""

for file in files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()

        import re
        # Find the nav block
        pattern = re.compile(r'<nav class="desktop-nav">.*?</nav>', re.DOTALL)
        
        # Determine active class
        custom_menu = menu_html
        if 'index.html' in file:
            custom_menu = custom_menu.replace('href="index.html"', 'href="index.html" class="active" style="color:var(--accent);"')
        elif 'tehsil.html' in file:
            custom_menu = custom_menu.replace('href="tehsil.html"', 'href="tehsil.html" class="active" style="color:var(--accent);"')
        elif 'b2b.html' in file:
            custom_menu = custom_menu.replace('href="b2b.html"', 'href="b2b.html" class="active" style="color:var(--accent);"')
        elif 'cert.html' in file:
            custom_menu = custom_menu.replace('href="cert.html"', 'href="cert.html" class="active" style="color:var(--accent);"')

        # Substitute
        new_text = pattern.sub(custom_menu, text)

        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_text)

    except Exception as e:
        print(f"Error on {file}: {e}")

print("Nav synced!")
