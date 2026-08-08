import re
import os

path = r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\tehsil.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix the top hero text
text = text.replace('İki imkan: <em>Sənəd</em> və <em>Sənət</em>', 'Peşəkar Psixologiya Təhsili')
text = text.replace('Hər iki proqram sizi real peşəkar edir — biri rəsmi diplom ilə, digəri isə dərin praktik bacarıqla.', 'Bütün təhsil proqramlarımızda həm rəsmi <strong>DPO Diplomu (Sənəd)</strong>, həm də reallıqda tətbiq edilən <strong>Praktikum (Sənət)</strong> birləşir.')

# 2. Extract from "<!-- TAB SELECTOR -->" to "<!-- REGISTER -->" / "<!-- REGISTRATION -->"
# We'll use split.
parts1 = text.split('<!-- TAB SELECTOR -->')
top = parts1[0]
middle_down = parts1[1]

# Now split middle_down by the registration section
# Let's find exactly where the registration section starts.
parts2 = middle_down.split('<section class="reg-section" id="registration">')
if len(parts2) == 2:
    bottom = '<section class="reg-section" id="registration">' + parts2[1]
else:
    # fallback
    bottom = '<section class="reg-section"' + text.split('<section class="reg-section"')[1]

# 3. Create the new middle logic
middle_new = """
<!-- MAIN CONTENT -->
<section style="background:var(--white); padding: 60px 32px;">
  <div class="section-inner" style="max-width: 1240px; margin: 0 auto;">
    
    <!-- INTRO & LEGAL -->
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: start; margin-bottom: 80px;">
      <div>
        <span class="section-tag">Əlavə Peşə Təhsili (DPO)</span>
        <h2 class="section-title">Niyə məhz bu proqram?</h2>
        <p style="font-size:1.05rem; color:var(--gray); line-height: 1.8; margin-bottom: 20px;">Başqa sahə üzrə ali təhsiliniz var, amma psixoloq olmaq istəyirsiniz? Yenidən 4 il bakalavr oxumağa ehtiyac yoxdur. Azərbaycan qanunvericiliyi (163 nömrəli qərar) qısa və rəsmi yol təklif edir — Əlavə Peşə Təhsili (DPO).</p>
        <p style="font-size:1.05rem; color:var(--gray); line-height: 1.8;">Siz 1 il ərzində həm psixopatologiyanı diaqnostika etmə bacarıqlarını öyrənir, həm də <strong>Rusiya FRDO reyestrinə daxil olunan</strong> rəsmi diplom alırsınız.</p>
        <a href="proqram.html" class="btn btn-outline-dark" style="margin-top: 24px;">Tədris proqramı ilə detallı tanış ol →</a>
      </div>
      
      <div style="background: rgba(13,27,62,0.03); border: 1px solid rgba(13,27,62,0.06); padding: 32px; border-radius: 12px;">
        <h4 style="color:var(--navy); font-size:1.15rem; margin-bottom: 12px; display:flex; align-items:center; gap:8px;">
          <span style="color:var(--accent);">✓</span> Nostrifikasiya Tələb Olunmur
        </h4>
        <p style="font-size:0.95rem; color:var(--text); margin-bottom:20px;">Digər xarici tibb diplomlarından fərqli olaraq, <strong>Əlavə Peşə Təhsili (DPO)</strong> diplomu ilə Azərbaycanda fəaliyyət göstərmək üçün heç bir nostrifikasiya (Təhsil Nazirliyindən təsdiq) tələb olunmur.</p>
        
        <h4 style="color:var(--navy); font-size:1.15rem; margin-bottom: 12px; display:flex; align-items:center; gap:8px;">
          <span style="color:var(--accent);">✓</span> Praktikum – Real Təcrübə
        </h4>
        <p style="font-size:0.95rem; color:var(--text);">Yaxşı psixoloq heç vaxt işsiz qalmır. Hər iki proqramımıza Praktikum daxildir — müalicə aparmaq, qazanc əldə etmək və şəxsi psixoloji mərkəz açmaq üçün bilavasitə tətbiqi bacarıqlar verilir.</p>
      </div>
    </div>

    <!-- PRICING TIERS -->
    <div style="text-align: center; margin-bottom: 40px;">
      <span class="section-tag">2 İSTİQAMƏT</span>
      <h2 class="section-title">Özünüzə uyğun proqramı seçin</h2>
      <p style="color:var(--gray); font-size: 1.05rem;">Hər iki istiqamət DPO Diplomu və Praktikumla təmin edilir.</p>
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 40px;">
      <!-- TIER 1 -->
      <div style="border: 1px solid var(--border); border-top: 4px solid var(--navy); border-radius: 12px; padding: 40px; background: var(--white); box-shadow: 0 10px 30px rgba(0,0,0,0.03);">
        <span style="display:inline-block; font-size: 0.75rem; font-weight:700; color:var(--gray); text-transform:uppercase; letter-spacing:2px; margin-bottom:12px;">BAZA PROQRAMI</span>
        <h3 style="font-size: 1.6rem; color: var(--navy); margin-bottom: 16px;">Ümumi Psixologiya + Praktikum</h3>
        <p style="color: var(--gray); font-size: 0.95rem; margin-bottom: 24px; line-height: 1.6;">Ümumi psixologiya üzrə rəsmi DPO Diplomu və psixoterapevtik texnikalara yiyələnmək üçün 1 illik Praktikum.</p>
        
        <div style="font-size: 2.8rem; font-weight: 700; color: var(--navy); line-height: 1; margin-bottom: 8px;">3 600 <span style="font-size: 1rem; font-weight: 400; color: var(--gray);">AZN</span></div>
        <div style="font-size: 0.85rem; color: var(--gray); margin-bottom: 32px;">Birlikdə və ya hissə-hissə ödəniş imkanı</div>

        <ul style="list-style: none; padding: 0; margin-bottom: 32px; display: flex; flex-direction: column; gap: 12px;">
          <li style="display:flex; align-items:flex-start; gap:10px; font-size:0.95rem;">
            <span style="color:var(--accent); font-weight:700;">✓</span> "Ümumi Psixologiya" üzrə rəsmi DPO Diplomu
          </li>
          <li style="display:flex; align-items:flex-start; gap:10px; font-size:0.95rem;">
            <span style="color:var(--accent); font-weight:700;">✓</span> Psixoterapiya Praktikumu (1 il)
          </li>
          <li style="display:flex; align-items:flex-start; gap:10px; font-size:0.95rem;">
            <span style="color:var(--accent); font-weight:700;">✓</span> 3+ illik video arxivinə tam giriş
          </li>
          <li style="display:flex; align-items:flex-start; gap:10px; font-size:0.95rem;">
            <span style="color:var(--accent); font-weight:700;">✓</span> IPAS beynəlxalq Assosiasiya üzvlüyü
          </li>
        </ul>
        <a href="#registration" onclick="setProgram('Ümumi Psixologiya (3600 AZN)')" class="btn btn-outline-dark" style="width: 100%; text-align: center;">Qeydiyyata yazıl</a>
      </div>

      <!-- TIER 2 -->
      <div style="background: var(--navy); color: var(--white); border-top: 4px solid var(--accent); border-radius: 12px; padding: 40px; box-shadow: 0 15px 40px rgba(13,27,62,0.15); position: relative; transform: translateY(-10px);">
        <div style="position: absolute; top: -14px; left: 50%; transform: translateX(-50%); background: var(--accent); color: var(--navy); font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; padding: 6px 16px; border-radius: 20px;">TÖVSİYƏ EDİLİR</div>
        
        <span style="display:inline-block; font-size: 0.75rem; font-weight:700; color:rgba(255,255,255,0.6); text-transform:uppercase; letter-spacing:2px; margin-bottom:12px;">TAM İXTİSAS</span>
        <h3 style="font-size: 1.6rem; color: var(--white); margin-bottom: 16px;">Klinik Psixologiya + Praktikum</h3>
        <p style="color: rgba(255,255,255,0.7); font-size: 0.95rem; margin-bottom: 24px; line-height: 1.6;">Həm ümumi, həm də klinik psixologiya. Psixiatrik patologiyalarla işləmək və klinikalarda fəaliyyət imkanı.</p>
        
        <div style="font-size: 2.8rem; font-weight: 700; color: var(--accent); line-height: 1; margin-bottom: 8px;">6 000 <span style="font-size: 1rem; font-weight: 400; color: rgba(255,255,255,0.5);">AZN</span></div>
        <div style="font-size: 0.85rem; color: rgba(255,255,255,0.6); margin-bottom: 32px;">Birlikdə və ya hissə-hissə ödəniş imkanı</div>

        <ul style="list-style: none; padding: 0; margin-bottom: 32px; display: flex; flex-direction: column; gap: 12px;">
          <li style="display:flex; align-items:flex-start; gap:10px; font-size:0.95rem;">
            <span style="color:var(--accent); font-weight:700;">✓</span> "Klinik Psixoloq" kvalifikasiyası üzrə Rəsmi DPO Diplomu
          </li>
          <li style="display:flex; align-items:flex-start; gap:10px; font-size:0.95rem;">
            <span style="color:var(--accent); font-weight:700;">✓</span> "Ümumi Psixologiya" modulu (Daxildir)
          </li>
          <li style="display:flex; align-items:flex-start; gap:10px; font-size:0.95rem;">
            <span style="color:var(--accent); font-weight:700;">✓</span> Psixoterapiya Praktikumu (1 il)
          </li>
          <li style="display:flex; align-items:flex-start; gap:10px; font-size:0.95rem;">
            <span style="color:var(--accent); font-weight:700;">✓</span> Bütün video arxivlərə və canlı dərslərə giriş
          </li>
        </ul>
        <a href="#registration" onclick="setProgram('Klinik Psixologiya (6000 AZN)')" class="btn btn-primary" style="width: 100%; text-align: center;">Qeydiyyata yazıl</a>
      </div>
    </div>
  </div>
</section>

<!-- TEACHING METHOD -->
<section style="background:var(--light); padding: 80px 32px;">
  <div class="section-inner" style="text-align: center; max-width: 900px;">
    <span class="section-tag">TƏLİM METODİKASI</span>
    <h2 class="section-title">Ən yaxşılardan öyrənin</h2>
    <p style="font-size: 1.05rem; color: var(--gray); margin-bottom: 40px; line-height: 1.8;">Tədris prosesi Həkim-psixiatr, psixoterapevt Kənan Rəhimov tərəfindən aparılır. O, Rusiya Federasiyasının Baş Psixoterapevti professor B.D.Karvasarskinin rəhbərliyi altında təhsil almışdır və bu gün həmin beynəlxalq standartları Azərbaycanda tətbiq edir.</p>
  </div>
</section>
"""

with open(path, 'w', encoding='utf-8') as f:
    f.write(top + middle_new + bottom)

print("tehsil.html heavily refactored with the new tier logic!")
