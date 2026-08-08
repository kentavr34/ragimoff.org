import os

# Update tehsil.html
tehsil_path = r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\tehsil.html'
with open(tehsil_path, 'r', encoding='utf-8') as f:
    text = f.read()

email_field = '''<div class="form-group">
        <label>Elektron Poçt (E-mail) *</label>
        <input type="email" required placeholder="Sertifikatın göndərilməsi üçün mütləqdir" />
      </div>
      <div class="form-group">
        <label>Vəzifəniz / Təhsiliniz</label>'''

if 'Elektron Poçt' not in text:
    text = text.replace('<div class="form-group">\n        <label>Vəzifəniz / Təhsiliniz</label>', email_field)
    with open(tehsil_path, 'w', encoding='utf-8') as f:
        f.write(text)

# Update b2b.html
b2b_path = r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\b2b.html'
with open(b2b_path, 'r', encoding='utf-8') as f:
    btext = f.read()

b2b_email = '''<div class="form-group">
            <label>Əlaqədar Şəxs</label>
            <input type="text" required placeholder="Ad və Soyad" />
          </div>
          <div class="form-group" style="grid-column: span 2;">
            <label>Elektron Poçt (E-mail) *</label>
            <input type="email" required placeholder="Offer faylı göndəriləcək ünvan" />
          </div>'''

if 'Elektron Poçt' not in btext:
    btext = btext.replace('<div class="form-group">\n            <label>Əlaqədar Şəxs</label>\n            <input type="text" required placeholder="Ad və Soyad" />\n          </div>', b2b_email)
    with open(b2b_path, 'w', encoding='utf-8') as f:
        f.write(btext)

print("Email fields successfully inserted")
