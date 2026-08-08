import os
import re

target_file = 'tehsil.html'

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Header Logo & Qeydiyyat Button
content = content.replace(
    '<a href="index.html" class="logo">R<span>.</span>AGIMOFF</a>',
    '<a href="index.html" class="logo" style="display:flex; align-items:center;"><img src="images/Logo-Ragimoff-Psy.jpg" alt="RAGIMOFF Logo" style="height:48px; border-radius:2px;"></a>'
)
content = content.replace(
    '<a href="#registration" class="btn btn-sm btn-accent">Qeydiyyat</a>',
    '<a href="#registration" class="btn nav-cta btn-sm" style="margin-left:14px; background:var(--accent); color:var(--navy); padding: 10px 20px; font-weight: 800; border-radius: 2px;">QEYDİYYAT</a>'
)

# 2. Update Hero Brand Tag and H1
old_hero = '<span class="hero-brand" style="color:var(--accent); margin-bottom:16px;">R.AGIMOFF PEŞƏKAR PSİXOLOGİYА MƏКТƏBİ</span>\n  <h1 style="font-size: clamp(2.2rem, 5vw, 4rem); letter-spacing:-0.02em; margin-bottom:40px;">PEŞƏKAR PSİXOLOJİ TƏHSİL</h1>'
new_hero = '<span class="hero-brand" style="border: 1px solid rgba(181,155,114,0.4); background: rgba(181,155,114,0.05); color:var(--accent); padding: 10px 24px; border-radius: 2px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 24px; display: inline-block;">RAGIMOFF Psixologiya Məktəbi</span>\n  <h1 style="font-size: clamp(2.2rem, 5vw, 4rem); letter-spacing:-0.02em; margin-bottom:40px;">İki yol: Sənəd və Sənət</h1>'
content = content.replace(old_hero, new_hero)

# 3. Insert Alumni Section
alumni_section = """
<!-- ALUMNI SUCCESS & COMMUNITY SECTION -->
<section style="padding: 100px 40px; background:var(--light); border-top:1px solid var(--border);">
  <div class="section-inner" style="max-width:1200px; margin:0 auto;">
    <div style="text-align:center;">
      <span class="status-tag" style="background:var(--navy); color:var(--white);">BİZİM İCMA VƏ NƏTİCƏLƏR</span>
      <h2 class="h2" style="color:var(--navy); margin-top:16px; margin-bottom:24px;">Məzunlarımızın Uğur Hekayələri</h2>
      <p style="color:var(--gray); font-size:1.15rem; line-height:1.7; max-width:800px; margin:0 auto 48px;">
        Tədrisi uğurla bitirib sərbəst fəaliyyətə başlayan istedadlı mütəxəssislərimiz öz mərkəzlərini açır və minlərlə insanın həyatına müsbət təsir edirlər.
      </p>
    </div>

    <!-- SUCCESS GRID -->
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:24px; margin-bottom:64px;">
      
      <!-- Ülkər Ərəbxanova -->
      <div style="background:var(--white); padding:32px; border:1px solid #e1e4e8; border-radius:4px; box-shadow:0 4px 12px rgba(0,0,0,0.02); transition:transform 0.3s ease;" onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
        <span style="color:var(--accent); font-weight:700; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px; display:block; margin-bottom:12px;">Məzun və Koordinator</span>
        <h4 style="font-size:1.3rem; margin-bottom:12px; color:var(--navy);">Ülkər Ərəbxanova</h4>
        <p style="font-size:0.95rem; color:var(--gray); line-height:1.6; margin-bottom:20px;">Psixologiya Məktəbinin istedadlı məzunu, hazırda isə məktəbin koordinatoru kimi peşəkar fəaliyyətdədir.</p>
        <a href="https://instagram.com/dr.arabxanova" target="_blank" style="color:var(--navy); font-weight:700; text-decoration:none; font-size:0.9rem; display:flex; align-items:center; gap:6px;">
          <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204...M12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg> 
          @dr.arabxanova
        </a>
      </div>

      <!-- Xanım Abdullayeva -->
      <div style="background:var(--white); padding:32px; border:1px solid #e1e4e8; border-radius:4px; box-shadow:0 4px 12px rgba(0,0,0,0.02); transition:transform 0.3s ease;" onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
        <span style="color:var(--accent); font-weight:700; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px; display:block; margin-bottom:12px;">Mərkəz Təsisçisi</span>
        <h4 style="font-size:1.3rem; margin-bottom:12px; color:var(--navy);">Xanım Abdullayeva</h4>
        <p style="font-size:0.95rem; color:var(--gray); line-height:1.6; margin-bottom:12px;">"İnam Academy" psixoloji mərkəzini təsis edərək fəaliyyətini tam müstəqil şəkildə inkişaf etdirir.</p>
        <div style="display:flex; flex-direction:column; gap:8px;">
            <a href="https://instagram.com/inam.academy" target="_blank" style="color:var(--navy); font-weight:700; text-decoration:none; font-size:0.9rem; display:flex; align-items:center; gap:6px;">
              @inam.academy
            </a>
            <a href="https://instagram.com/psixoloq_xanim_abdullayeva" target="_blank" style="color:var(--gray); font-weight:500; text-decoration:none; font-size:0.85rem; display:flex; align-items:center; gap:6px;">
              @psixoloq_xanim_abdullayeva
            </a>
        </div>
      </div>

      <!-- Aysel Mustafayeva -->
      <div style="background:var(--white); padding:32px; border:1px solid #e1e4e8; border-radius:4px; box-shadow:0 4px 12px rgba(0,0,0,0.02); transition:transform 0.3s ease;" onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
        <span style="color:var(--accent); font-weight:700; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px; display:block; margin-bottom:12px;">Mərkəz Rəhbəri</span>
        <h4 style="font-size:1.3rem; margin-bottom:12px; color:var(--navy);">Aysel Mustafayeva</h4>
        <p style="font-size:0.95rem; color:var(--gray); line-height:1.6; margin-bottom:20px;">Uğurlu məzunumuz hazırda Ayıes Tədris və İnkişaf Mərkəzinin rəhbəri olaraq fəaliyyət göstərir.</p>
        <a href="https://www.instagram.com/ayles.tedris.inkisaf_merkezi" target="_blank" style="color:var(--navy); font-weight:700; text-decoration:none; font-size:0.9rem; display:flex; align-items:center; gap:6px;">
          @ayles.tedris.inkisaf_merkezi
        </a>
      </div>

      <!-- Klinik psixoloq Nur -->
      <div style="background:var(--white); padding:32px; border:1px solid #e1e4e8; border-radius:4px; box-shadow:0 4px 12px rgba(0,0,0,0.02); transition:transform 0.3s ease;" onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
        <span style="color:var(--accent); font-weight:700; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px; display:block; margin-bottom:12px;">Klinik Psixoloq</span>
        <h4 style="font-size:1.3rem; margin-bottom:12px; color:var(--navy);">Klinik psixoloq Nur</h4>
        <p style="font-size:0.95rem; color:var(--gray); line-height:1.6; margin-bottom:20px;">Peşəkar fəaliyyətini uğurla davam etdirərək cəmiyyətə dərindən fayda verən dəyərli mütəxəssis.</p>
        <a href="https://www.instagram.com/klinik_psixoloqnur/" target="_blank" style="color:var(--navy); font-weight:700; text-decoration:none; font-size:0.9rem; display:flex; align-items:center; gap:6px;">
          @klinik_psixoloqnur
        </a>
      </div>

    </div>

    <!-- COMMUNITY BANNER -->
    <div style="background:#061826; border-radius:4px; overflow:hidden; display:flex; flex-wrap:wrap; align-items:center; border-bottom:5px solid var(--accent);">
       <div style="flex:1.5; min-width:320px; padding:60px 40px;">
          <span style="color:var(--accent); font-weight:800; font-size:0.75rem; letter-spacing:1px; text-transform:uppercase; margin-bottom:12px; display:block;">PEŞƏKARDAN DA ÖTƏ</span>
          <h3 style="color:var(--white); font-size:1.8rem; margin-bottom:16px; font-weight:800; line-height:1.3;">Təkcə həmkarlar deyil, böyük bir ailə...</h3>
          <p style="color:rgba(255,255,255,0.8); font-size:1.1rem; line-height:1.7; margin-bottom:32px;">
             Biz sadəcə tədris zamanı deyil, hər zaman həmkar və dost olmağı bacarırıq. Birlikdə ad günləri qeyd edir, bir-birimizə dəstək oluruq. Məzunlarımızın iştirakı ilə ssenarisini yazdığım bu gülməli sosial çarx (evli kişi rolunda) artıq <strong>187 000 baxış</strong> toplayıb! 
          </p>
          <a href="https://www.instagram.com/reel/CxQq3IIoL3E" target="_blank" class="btn btn-accent" style="font-weight:700; display:inline-flex; align-items:center; gap:8px;">
             VİDEO ÇARXI İZLƏ (187K Baxış) →
          </a>
       </div>
       <div style="flex:1; min-width:280px; background:var(--navy); position:relative; min-height:400px; display:flex; justify-content:center; align-items:center;">
          <div style="width:100%; height:100%; background:url('images/group-outdoor.jpg') left/cover; opacity:0.6; position:absolute; top:0; left:0;"></div>
          <a href="https://www.instagram.com/reel/CxQq3IIoL3E" target="_blank" style="position:relative; z-index:2; text-decoration:none; display:flex; flex-direction:column; align-items:center;">
             <div style="width:90px; height:90px; background:var(--accent); border-radius:50%; display:flex; justify-content:center; align-items:center; margin-bottom:16px; box-shadow:0 0 30px rgba(181,155,114,0.3); transition:transform 0.4s ease;" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">
                 <svg width="34" height="34" fill="var(--navy)" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
             </div>
          </a>
       </div>
    </div>
  </div>
</section>

<!-- REVIEWS SECTION -->
"""

if "<!-- ALUMNI SUCCESS & COMMUNITY SECTION -->" not in content:
    content = content.replace("<!-- REVIEWS SECTION -->", alumni_section)

# 4. Update Footer Logo
content = content.replace(
    '<a href="#" class="logo">R<span>.</span>AGIMOFF</a>',
    '<a href="#" class="logo" style="display:flex; align-items:center;"><img src="images/Logo-Ragimoff-Psy.jpg" alt="RAGIMOFF Logo" style="height:40px; border-radius:2px; opacity:0.8;"></a>'
)

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully updated {target_file}")
