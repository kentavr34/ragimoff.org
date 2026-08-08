import os

files = [
    r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\index.html',
    r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\tehsil.html',
    r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\b2b.html',
    r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\cert.html',
]

for file in files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()

        text = text.replace('Xidmətlər', 'Konsultasiya')
        text = text.replace('20+ il', '23+ il')
        text = text.replace('20+', '23+')

        with open(file, 'w', encoding='utf-8') as f:
            f.write(text)
    except Exception as e:
        pass

# Now rewrite b2b.html entirely to feature the corporate trainings and the requested form!
b2b_content = """<!DOCTYPE html>
<html lang="az">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <meta name="description" content="Korporativ təlimlər, Satış məktəbi və Liderlik psixologiyası. Şirkətiniz üçün peşəkar həllər."/>
  <title>Korporativ Təlimlər (B2B) | RAGIMOFF</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
  <link rel="stylesheet" href="shared.css"/>
  <style>
    body { padding-top: 70px; }
    .b2b-hero { background: var(--navy); color: var(--white); padding: 100px 32px; text-align: center; }
    .b2b-hero h1 { color: var(--white); font-size: 2.8rem; margin-bottom: 20px; }
    .b2b-hero p { color: rgba(255,255,255,0.7); max-width: 600px; margin: 0 auto; font-size: 1.1rem; }
    
    .course-card { border: 1px solid var(--border); padding: 32px; border-radius: 12px; margin-bottom: 24px; transition: .2s; }
    .course-card:hover { border-color: var(--accent); box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .course-card h3 { font-size: 1.4rem; color: var(--navy); margin-bottom: 12px; }
    .course-card p { color: var(--gray); font-size: 0.95rem; }

    .order-form { background: var(--light); padding: 48px; border-radius: 12px; max-width: 800px; margin: 60px auto; }
    .order-form h2 { margin-bottom: 24px; text-align: center; }
    .form-group { margin-bottom: 20px; }
    .form-group label { display: block; font-weight: 600; font-size: 0.9rem; margin-bottom: 8px; color: var(--navy); }
    .form-group input, .form-group select, .form-group textarea { width: 100%; padding: 12px; border: 1px solid var(--border); border-radius: 6px; font-family: 'Inter', sans-serif; }
    .btn-submit { background: var(--accent); color: var(--navy); font-weight: 700; padding: 14px 28px; border: none; border-radius: 6px; cursor: pointer; width: 100%; font-size: 1rem; }
    .btn-submit:hover { background: #d9bc82; }
  </style>
</head>
<body>

<header>
  <div class="header-inner">
    <a href="index.html" class="logo">R<span>.</span>AGIMOFF</a>
    <nav class="desktop-nav">
      <a href="index.html">Ana Səhifə</a>
      <a href="tehsil.html">Təhsil</a>
      <a href="index.html#services">Konsultasiya</a>
      <a href="b2b.html" class="active" style="color:var(--accent);">Korporativ</a>
      <a href="cert.html">Sertifikat</a>
    </nav>
  </div>
</header>

<div class="b2b-hero">
  <h1>Biznes Təlimləri</h1>
  <p>Satış komandalarınızın performansını artıracaq, liderlik bacarıqlarını inkişaf etdirəcək elmi əsaslı korporativ psixologiya təlimləri.</p>
</div>

<section style="background:var(--white); padding: 80px 32px;">
  <div style="max-width: 1000px; margin: 0 auto;">
    
    <div class="course-card">
      <h3>1. Satış Məktəbi</h3>
      <p>Müştəri psixologiyası, NLP texnikaları ilə satış, etirazlarla iş və bağlama strategiyaları. Şirkətinizin satışlarını minimum 30% artırmaq üçün fərdiləşdirilmiş təlim.</p>
    </div>
    
    <div class="course-card">
      <h3>2. Liderlik və İdarəetmə Psixologiyası</h3>
      <p>Rəhbər şəxslər üçün komanda idarəetməsi, böhran vəziyyətlərində qərar qəbuletmə, emosional intellekt və motivasiya sistemləri.</p>
    </div>
    
    <div class="course-card">
      <h3>3. HR və Personalın Qiymətləndirilməsi</h3>
      <p>Kadr seçimi, işçilərin psixoloji portretinin çıxarılması və komanda daxili münaqişələrin həlli yolları.</p>
    </div>

    <!-- FORM -->
    <div class="order-form" id="order">
      <h2>Korporativ Təlim Sifariş Et</h2>
      <p style="text-align: center; color: var(--gray); margin-bottom: 32px;">Tələblərinizi bizə göndərin, şirkətiniz üçün fərdi təklif (offer) və qiymət paketi hazırlayaq.</p>
      
      <form onsubmit="event.preventDefault(); alert('Sifarişiniz qəbul olundu. Tezliklə Sizinlə əlaqə saxlayacağıq.');">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
          <div class="form-group">
            <label>Şirkətin Adı</label>
            <input type="text" required placeholder="Məsələn: 'TechMMC'" />
          </div>
          <div class="form-group">
            <label>Əlaqədar Şəxs</label>
            <input type="text" required placeholder="Ad və Soyad" />
          </div>
        </div>
        
        <div class="form-group">
          <label>Təlimin Mövzusu (Nəyə ehtiyacınız var?)</label>
          <input type="text" required placeholder="Məsələn: Satış komandası üçün intensiv təlim" />
        </div>
        
        <div class="form-group">
          <label>Proqrama Nələr Daxil Olunsun?</label>
          <textarea rows="3" placeholder="Gözləntiləriniz, praktik məşğələlər vs..."></textarea>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
          <div class="form-group">
            <label>Təqribi Saat və ya Gün</label>
            <input type="text" placeholder="Məsələn: 2 gün x 4 saat" />
          </div>
          <div class="form-group">
            <label>Hansı Vaxtdan Planlaşdırırsınız?</label>
            <input type="text" placeholder="Məsələn: Gələn ayın əvvəlinə" />
          </div>
        </div>
        
        <button type="submit" class="btn-submit">Fərdi Təklif (Offer) Al</button>
      </form>
    </div>

  </div>
</section>

<footer style="background:var(--navy); padding: 40px; color:rgba(255,255,255,0.5); text-align:center;">
  <p>© 2026 RAGIMOFF</p>
</footer>

</body>
</html>"""

with open(r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\b2b.html', 'w', encoding='utf-8') as f:
    f.write(b2b_content)

print("Menu fixes and B2B form successfully created!")
