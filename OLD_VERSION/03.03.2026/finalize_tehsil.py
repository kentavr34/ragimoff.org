import re
import os

path = r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\tehsil.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix "Hər iki proqram" to handle 3 tiers and text-wrap balance
ol_hero = '<p style="max-width: 580px; margin: 0 auto 32px;">Hər iki proqram sizi real peşəkar edir — həm qanunvericiliklə təsdiq olunmuş <strong>Diplom (DPO)</strong>, həm də pasiyentləri razı salacağınız qədər <strong>məqsədyönlü Praktikum</strong>.</p>'
new_hero = '<p style="max-width: 550px; margin: 0 auto 32px; text-wrap: balance; text-align: center;">Təqdim olunan proqramlar sizi real peşəkar edir — həm qanunvericiliklə təsdiq olunmuş <strong>Diplom (DPO)</strong>, həm də pasiyentləri razı salacağınız qədər <strong>məqsədyönlü Praktikum</strong>.</p>'
text = text.replace(ol_hero, new_hero)

# 2. Add the 3rd tab for Practicum only
old_tabs = '''<div class="sel-tab" id="tab-praktikum" onclick="switchTab('praktikum')">
      <div>
        <div>Tam: Klinik Psixologiya</div>
        <span class="tab-sub">Ümumi + Klinik DPO + Praktikum</span>
      </div>
    </div>'''
new_tabs = '''<div class="sel-tab" id="tab-praktikum" onclick="switchTab('praktikum')">
      <div>
        <div>Tam: Klinik Psixologiya</div>
        <span class="tab-sub">Ümumi + Klinik DPO + Praktikum</span>
      </div>
    </div>
    <div class="sel-tab" id="tab-only-prak" onclick="switchTab('only-prak')">
      <div>
        <div>Sənət: Yalnız Praktikum</div>
        <span class="tab-sub">Sertifikat + 1 illik praktika</span>
      </div>
    </div>'''
text = text.replace(old_tabs, new_tabs)

# 3. Insert the 3rd panel right after the 2nd panel ends
# We'll just look for the end of the 2nd panel which triggers the common elements
# Specifically `</div>` before `<!-- ==============================================`
prak_3rd = """
<!-- ==============================================
     TAB 3: YALNIZ PRAKTİKUM 
     ============================================== -->
<div id="panel-only-prak" class="program-panel">
  <section style="background:var(--white);">
    <div class="sanəd-grid">
      
      <!-- LEFT DESC -->
      <div class="sanəd-intro">
        <span class="tag" style="color:var(--accent);">PRAKTİKİ BACARIQLAR (1 İL)</span>
        <h2 class="h2">Psixoterapiya Praktikumu</h2>
        <p>Əgər Sizin artıq başqa yerdən diplomunuz varsa və ya sadəcə real konsultasiya aparmaq, pasiyentlərlə işləmək üçün ancaq dərin praktikaya ehtiyacınız varsa — bu paket məhz Sizin üçündür.</p>

        <div class="highlight-box">
          <h4 style="color:var(--navy);font-weight:700;margin-bottom:8px;">Real Nəticələr</h4>
          <p>Zəngin nəzəriyyədən daha çox, işin əsl "mətbəxini" - pasiyentin problemlərini həll etməyi öyrənirsiniz. Tam 1 illik məqsədyönlü praktika!</p>
        </div>
      </div>
      
      <!-- RIGHT PRICE -->
      <div class="sanəd-card">
        <div class="price-card" style="background:var(--white); border: 2px solid var(--border); color:var(--text);">
          <span class="price-card-tag" style="color:var(--gray);">DİPLOMSUZ SERTİFİKAT (YALNIZ PRAKTİKA)</span>
          <h3 style="color:var(--navy); font-size:1.4rem;">Yalnız Psixoterapiya Praktikumu</h3>
          <div class="price-main" style="color:var(--navy); font-size:2.8rem; margin:16px 0;">3 000 <span style="color:var(--gray);font-size:1.1rem;">AZN</span></div>
          <p style="font-size:0.85rem; color:var(--gray); margin-bottom:20px;">və ya aylıq ödənişlə 3 600 AZN (ayda 300 AZN × 12 ay)</p>
          <ul class="doc-list" style="margin-bottom:20px; border-top:1px solid var(--border); padding-top:20px;">
            <li style="border-bottom:none; color:var(--text);"><span style="color:var(--accent);">✓</span> 300-dən çox dərsin video arxivi sərbəst baxış üçün</li>
            <li style="border-bottom:none; color:var(--text);"><span style="color:var(--accent);">✓</span> Hər ay yeni praktiki dərslərə qatılmaq imkanı</li>
            <li style="border-bottom:none; color:var(--text);"><span style="color:var(--accent);">✓</span> Bu tədris proqramında öyrədilən metodikalar sayəsində sizin pasiyentləriniz sizi hamıya tövsiyə edəcəklər</li>
          </ul>
          <a href="#registration" class="btn-enroll" style="background:var(--navy); color:white;">Qeydiyyata yazıl</a>
        </div>
      </div>
      
    </div>
  </section>
</div>
"""
# insert before the Registration section
text = text.replace('<!-- ==============================================\n     COMMON REGISTRATION', prak_3rd + '\n<!-- ==============================================\n     COMMON REGISTRATION')

# 4. Links for YouTube, Telegram, WhatsApp
old_yt = '<a href="https://youtube.com" class="btn" style="background:#FF0000; color:white; padding:10px 18px;">YouTube-da İzlə</a>'
new_yt = '<a href="https://youtube.com/playlist?list=PLeCn6bx0D73_SVNqn3LjWj1bU1U2X9lPD&si=3MLAHlhe8e6g3VWy" target="_blank" class="btn" style="background:#FF0000; color:white; padding:10px 18px;">Dərslərin Playlisti</a>'
text = text.replace(old_yt, new_yt)

t_wa_html = '''
        <div style="margin-top:20px; display:flex; gap:12px; flex-wrap:wrap;">
          <a href="https://t.me/psyproaz" target="_blank" class="btn" style="background:#0088cc; color:white; padding:10px 18px;">Telegram Qrupu</a>
          <a href="https://chat.whatsapp.com/FvIpfHzqlk31ayZ8lCfxKj" target="_blank" class="btn" style="background:#25D366; color:white; padding:10px 18px;">WhatsApp / Networking</a>
        </div>
'''
text = text.replace('YouTube-da İzlə</a>\n        </div>', new_yt + t_wa_html + '</div>')

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

# Also fix the select options in the bottom registration form to include the 3rd option
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

sel_opt = '''<option value="Klinik Psixologiya (6000 AZN)">Tam: Klinik Psixologiya (6000 AZN)</option>
          <option value="Yalnız Praktikum (3000 AZN)">Sənət: Yalnız Praktikum (3000 AZN)</option>'''
text = text.replace('<option value="Klinik Psixologiya (6000 AZN)">Tam: Klinik Psixologiya (6000 AZN)</option>', sel_opt)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("3 Tiers added, Text Wrap Balance fixed, Links injected!")
