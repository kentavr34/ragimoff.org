import os
path = r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\index.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('href="tehsil.html" class="btn btn-outline-light"', 'href="haqqinda.html" class="btn btn-outline-light"')
text = text.replace('href="tehsil.html" class="btn btn-primary"', 'href="haqqinda.html" class="btn btn-primary"')

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

# Let's add the instagram link to tehsil.html and index.html footers
def add_ig(file):
    with open(file, 'r', encoding='utf-8') as f:
        t = f.read()
    if 'instagram.com/doctor.ragimoff' not in t:
        t = t.replace('</footer>', '  <div style="margin-top:20px;text-align:center;"><a href="https://instagram.com/doctor.ragimoff" target="_blank" style="color:var(--accent); text-decoration:none;">Instagram\'da Bizi İzləyin</a></div>\n</footer>')
        with open(file, 'w', encoding='utf-8') as f:
            f.write(t)

add_ig(r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\index.html')
add_ig(r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\tehsil.html')
print("Fixed haqqinda.html reference and added Instagram links")
