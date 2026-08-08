import os
import re

path = r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\index.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find the specific p in index.html and ensure it has text-wrap balance
# <p class="fade-in fd2" style="max-width: 500px; margin: 0 auto 32px; font-size: 1.05rem; color: rgba(255,255,255,0.7); line-height: 1.8;">
text = text.replace(
    '''<p class="fade-in fd2" style="max-width: 500px; margin: 0 auto 32px; font-size: 1.05rem; color: rgba(255,255,255,0.7); line-height: 1.8;">''',
    '''<p class="fade-in fd2" style="max-width: 500px; margin: 0 auto 32px; font-size: 1.05rem; color: rgba(255,255,255,0.7); line-height: 1.8; text-wrap: balance; text-align: center;">'''
)
# Just in case the exact string is different:
text = text.replace('Dəqiq struktur, sübuta əsaslanan metodlar və 23+ illik təcrübə ilə 3 əsas istiqamətdə fəaliyyət göstəririk.',
                    'Dəqiq struktur, sübuta əsaslanan metodlar və 23+ illik təcrübə ilə <br> 3 əsas istiqamətdə fəaliyyət göstəririk.')

# Or just use regex to add text-wrap balance to the paragraph with "Dəqiq struktur"
text = re.sub(
    r'<p[^>]*>(.*?Dəqiq struktur.*?)</p>',
    r'<p style="max-width: 550px; margin: 0 auto 32px; font-size: 1.05rem; color: rgba(255,255,255,0.8); line-height: 1.6; text-wrap: balance; text-align: center;">\1</p>',
    text,
    flags=re.DOTALL
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

# Also update tehsil.html directly to ensure the hero text is also beautifully balanced if I missed it, but I did it before.
path_t = r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\tehsil.html'
with open(path_t, 'r', encoding='utf-8') as f:
    tt = f.read()

tt = tt.replace('max-width: 580px; margin: 0 auto 32px;', 'max-width: 550px; margin: 0 auto 32px; text-wrap: balance; text-align: center;')

with open(path_t, 'w', encoding='utf-8') as f:
    f.write(tt)

# Let's add text-wrap: balance to shared.css
css_path = r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\shared.css'
if os.path.exists(css_path):
    with open(css_path, 'a', encoding='utf-8') as f:
        f.write('\n/* Global Typography Balancers */\nh1, h2, .section-title, .hub-hero p, .page-hero p, .section-sub { text-wrap: balance; }')

print("Applied strict text-wrap: balance across the project.")
