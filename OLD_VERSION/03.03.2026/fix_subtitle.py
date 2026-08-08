import re

path = r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\tehsil.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

old_subtitle = '<p style="max-width: 550px; margin: 0 auto 32px; text-wrap: balance; text-align: center;">Təqdim olunan proqramlar sizi real peşəkar edir — həm qanunvericiliklə təsdiq olunmuş <strong>Diplom (DPO)</strong>, həm də pasiyentləri razı salacağınız qədər <strong>məqsədyönlü Praktikum</strong>.</p>'

new_subtitle = '''<p style="max-width: 580px; margin: 0 auto 32px; text-align: center; color: rgba(255,255,255,0.85); font-size: 1.1rem; line-height: 1.8; letter-spacing: 0.2px;">
  Sankt-Peterburq Əlavə Peşə Təhsili İnstitutunun rəsmi <strong>DPO Diplomu</strong><br>
  və beynəlxalq standartlara cavab verən <strong>Peşəkar Psixoterapiya Praktikumu</strong>
</p>'''

text = text.replace(old_subtitle, new_subtitle)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("tehsil.html subtitle perfectly updated to strict 2 lines matching Sənəd and Sənət.")
