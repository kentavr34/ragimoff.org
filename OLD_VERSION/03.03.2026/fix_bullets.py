import os

path = r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\tehsil.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix unethical text
old_prak_text = 'müalicə aparmaq, qazanc əldə etmək və şəxsi psixoloji mərkəz açmaq üçün bilavasitə tətbiqi bacarıqlar verilir.'
new_prak_text = 'pasiyentlərdə real nəticələr əldə etmək, müalicə aparmaq və şəxsi psixoloji mərkəz açmaq üçün bilavasitə tətbiqi bacarıqlar verilir.'
text = text.replace(old_prak_text, new_prak_text)

# Fix video archive text
old_video_text1 = '3+ illik video arxivinə tam giriş'
new_video_text1 = '300-dən çox dərsin video arxivi (sərbəst baxış üçün)'
text = text.replace(old_video_text1, new_video_text1)

# Fix live classes text
old_live_text = 'Bütün video arxivlərə və canlı dərslərə giriş'
new_live_text = 'Hər ay yeni praktiki dərslərə qatılmaq imkanı'
text = text.replace(old_live_text, new_live_text)

# Add the powerful word-of-mouth bullet
new_bullet = '''
          <li style="display:flex; align-items:flex-start; gap:10px; font-size:0.95rem;">
            <span style="color:var(--accent); font-weight:700;">✓</span> Bu proqramda öyrədilən metodikalar sayəsində pasiyentləriniz sizi hamıya tövsiyə edəcəklər
          </li>'''

# Insert in Tier 1
old_ul_1 = '''<li style="display:flex; align-items:flex-start; gap:10px; font-size:0.95rem;">
            <span style="color:var(--accent); font-weight:700;">✓</span> IPAS beynəlxalq Assosiasiya üzvlüyü
          </li>'''
text = text.replace(old_ul_1, old_ul_1 + new_bullet)

# Insert in Tier 2
old_ul_2 = '''<li style="display:flex; align-items:flex-start; gap:10px; font-size:0.95rem;">
            <span style="color:var(--accent); font-weight:700;">✓</span> Hər ay yeni praktiki dərslərə qatılmaq imkanı
          </li>'''
text = text.replace(old_ul_2, old_ul_2 + new_bullet)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("tehsil.html practicing bullets and ethical texts updated successfully!")
