import builtins

html_content = """<!DOCTYPE html>
<html lang="az">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <meta name="description" content="Klinik Psixoloq Diplomu və Psixoterapiya Praktikumu. Təhsil Nazirliyi nostrifikasiyası tələb olunmayan qanuni proqram."/>
  <title>Peşəkar Psixoloji Təhsil | RAGIMOFF</title>
  
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
  <link rel="stylesheet" href="shared.css"/>
  
  <style>
    /* PAGE SPECIFIC CSS */
    .page-hero {
      background: linear-gradient(135deg, var(--navy) 0%, #162d58 100%);
      padding: 130px 32px 80px; text-align: center; position: relative; overflow: hidden;
    }
    .page-hero::before {
      content: ''; position: absolute; top: -30%; left: 50%; transform: translateX(-50%);
      width: 800px; height: 800px; border-radius: 50%;
      background: radial-gradient(circle, rgba(200,169,110,0.10) 0%, transparent 65%);
      pointer-events: none;
    }
    .page-hero-tag { display: inline-block; border: 1px solid rgba(255,255,255,0.2); background: rgba(255,255,255,0.05); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); color: var(--accent); font-size: 0.72rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; padding: 5px 16px; border-radius: 20px; margin-bottom: 20px; }
    .page-hero h1 { font-family: 'Inter', -apple-system, sans-serif; font-size: clamp(2rem, 4vw, 3.2rem); font-weight: 700; color: var(--white); line-height: 1.2; margin-bottom: 18px; }
    .page-hero h1 em { color: var(--accent); font-style: normal; }
    .page-hero p { font-size: 1.05rem; color: rgba(255,255,255,0.7); max-width: 540px; margin: 0 auto 32px; font-weight: 300; }
    .hero-pills { display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; }
    .pill { background: rgba(255,255,255,0.06); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.15); box-shadow: 0 4px 15px rgba(0,0,0,0.1); color: rgba(255,255,255,0.85); font-size: 0.82rem; padding: 7px 18px; border-radius: 20px; }
    .pill strong { color: var(--accent); }

    /* TAB SELECTOR */
    .selector-section { background: var(--white); padding: 0 32px; position: sticky; top: 70px; z-index: 50; border-bottom: 1px solid var(--border); }
    .selector-inner { max-width: 1200px; margin: 0 auto; display: flex; gap: 0; }
    .sel-tab {
      flex: 1; padding: 22px 24px; text-align: center; cursor: pointer;
      border-bottom: 3px solid transparent; transition: all .25s;
      font-weight: 700; font-size: 0.88rem; letter-spacing: 0.5px;
      color: var(--gray); display: flex; align-items: center; justify-content: center; gap: 10px;
    }
    .sel-tab:hover { color: var(--navy); background: var(--light); }
    .sel-tab.active { color: var(--navy); border-bottom-color: var(--accent); background: rgba(200,169,110,0.04); }
    .sel-tab .tab-icon { font-size: 1.3rem; }
    .sel-tab .tab-sub { font-size: 0.72rem; font-weight: 400; color: var(--gray); display: block; margin-top: 2px; letter-spacing: 0; }
    .sel-tab.active .tab-sub { color: var(--accent); }

    .program-panel { display: none; animation: fadeUp .4s ease; }
    .program-panel.active { display: block; }
    @keyframes fadeUp { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: translateY(0); } }

    /* Grid layouts */
    .sanəd-grid { display: grid; grid-template-columns: 1.1fr 1fr; gap: 64px; align-items: start; max-width: 1240px; margin: 0 auto; }
    .sanəd-intro p { color: var(--gray); font-size: 0.95rem; margin-bottom: 16px; line-height: 1.8; }
    
    .highlight-box {
      background: linear-gradient(135deg, rgba(13,27,62,0.04), rgba(200,169,110,0.08));
      border: 1px solid rgba(200,169,110,0.3); border-radius: 10px;
      padding: 28px; margin: 28px 0;
    }
    
    /* ACORDEON */
    .accordion { margin-top: 36px; }
    .accordion-item { border: 1px solid var(--border); border-radius: 8px; margin-bottom: 12px; overflow: hidden; }
    .accordion-head {
      display: flex; align-items: center; justify-content: space-between;
      padding: 18px 22px; cursor: pointer; background: var(--white);
      transition: background .2s; gap: 16px;
    }
    .accordion-head:hover { background: var(--light); }
    .accordion-head-left { display: flex; align-items: center; gap: 14px; }
    .accordion-icon { width: 38px; height: 38px; border-radius: 8px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; }
    .icon-doc { background: rgba(13,27,62,0.08); color: var(--navy); }
    .icon-prak { background: rgba(200,169,110,0.15); color: var(--accent); }
    .accordion-title { font-weight: 700; font-size: 0.95rem; color: var(--navy); }
    .accordion-subtitle { font-size: 0.78rem; color: var(--gray); margin-top: 2px; }
    .accordion-arrow { width: 24px; height: 24px; flex-shrink: 0; transition: transform .3s; color: var(--gray); }
    .accordion-item.open .accordion-arrow { transform: rotate(180deg); }
    .accordion-body { max-height: 0; overflow: hidden; transition: max-height .45s ease; }
    .accordion-body-inner { padding: 0 22px 24px; border-top: 1px solid var(--border); }
    
    .doc-list { list-style: none; margin-top: 16px; }
    .doc-list li { display: flex; align-items: flex-start; gap: 10px; padding: 10px 0; border-bottom: 1px solid var(--border); font-size: 0.88rem; color: var(--text); }
    .doc-list li:last-child { border-bottom: none; }
    .doc-check { color: var(--accent); font-weight: 700; flex-shrink: 0; margin-top: 1px; }
    
    .law-links { margin-top: 16px; display:flex; flex-direction:column; gap:8px; }
    .law-link { display: flex; align-items: center; gap: 10px; padding: 10px 14px; border: 1px solid var(--border); border-radius: 6px; text-decoration: none; color: var(--blue); font-size: 0.85rem; transition: all .2s; }
    .law-link:hover { border-color: var(--accent); background: var(--light); }
    
    /* RIGHT CARD */
    .sanəd-card { position: sticky; top: 130px; }
    .price-card { background: var(--navy); border-radius: 14px; padding: 36px; color: var(--white); margin-bottom: 20px; box-shadow: 0 15px 40px rgba(13,27,62,0.15); }
    .price-card-tag { font-size: 0.7rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: rgba(200,169,110,0.8); margin-bottom: 12px; display: block; }
    .price-card h3 { font-family: 'Inter', sans-serif; font-size: 1.3rem; color: var(--white); margin-bottom: 20px; line-height: 1.3; }
    .price-main { font-family: 'Inter', sans-serif; font-size: 2.6rem; font-weight: 700; color: var(--accent); line-height: 1; }
    .price-main span { font-size: 1rem; font-weight: 400; color: rgba(255,255,255,0.5); }
    .btn-enroll { display: block; text-align: center; background: var(--accent); color: var(--navy); font-weight: 700; font-size: 0.9rem; padding: 15px; border-radius: 6px; text-decoration: none; transition: background .2s; margin-top:20px; }
    .btn-enroll:hover { background: #d9bc82; }
    
    /* COMMON PRAK ELEMENTS */
    .prak-hero { background: linear-gradient(135deg, #0a1628, #162d58); border-radius: 16px; padding: 48px; margin-bottom: 48px; margin-top: 40px; }
    .prak-hero h2 { font-size: 1.9rem; color: var(--white); margin-bottom: 14px; }
    .prak-hero p { color: rgba(255,255,255,0.7); font-size: 0.95rem; line-height: 1.8; }
    
    .free-lesson { background: var(--light); border-radius: 14px; padding: 40px; margin-bottom: 48px; display: grid; grid-template-columns: 1fr 1fr; gap: 40px; align-items: center; }
    
    .curriculum-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; margin-bottom: 48px; }
    .curr-card { border: 1px solid var(--border); border-radius: 10px; padding: 22px; }
    .curr-num { font-size: 0.78rem; font-weight: 700; color: var(--accent); letter-spacing: 1px; margin-bottom: 8px; }
    .curr-title { font-weight: 700; font-size: 0.92rem; color: var(--navy); margin-bottom: 8px; }

    @media (max-width: 900px) {
      .sanəd-grid, .free-lesson { grid-template-columns: 1fr; }
      .sanəd-card { position: static; }
      .curriculum-grid { grid-template-columns: 1fr 1fr; }
    }
    @media (max-width: 640px) {
      .curriculum-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>

<header>
  <div class="header-inner">
    <a href="index.html" class="logo">R<span>.</span>AGIMOFF</a>
    <nav class="desktop-nav">
      <a href="index.html">Ana Səhifə</a>
      <a href="tehsil.html" class="active">Təhsil</a>
      <a href="index.html#services">Xidmətlər</a>
      <a href="b2b.html">Korporativ</a>
      <a href="cert.html">Sertifikat</a>
    </nav>
    <div class="burger" onclick="toggleMenu()"><span></span><span></span><span></span></div>
  </div>
</header>

<div class="mobile-nav" id="mobileNav">
  <a href="index.html" onclick="closeMenu()">Ana Səhifə</a>
  <a href="tehsil.html" onclick="closeMenu()">Təhsil</a>
  <a href="index.html#services" onclick="closeMenu()">Xidmətlər</a>
  <a href="b2b.html" onclick="closeMenu()">Korporativ</a>
  <a href="cert.html" onclick="closeMenu()">Sertifikat</a>
</div>

<div class="page-hero">
  <div class="page-hero-tag">PEŞƏKAR TƏHSİL</div>
  <h1>İki imkan: <em>Sənəd</em> və <em>Sənət</em></h1>
  <p style="max-width: 580px; margin: 0 auto 32px;">Hər iki proqram sizi real peşəkar edir — həm qanunvericiliklə təsdiq olunmuş <strong>Diplom (DPO)</strong>, həm də pasiyentləri razı salacağınız qədər <strong>məqsədyönlü Praktikum</strong>.</p>
  <div class="hero-pills">
    <span class="pill"><strong>20+</strong> il təcrübə</span>
    <span class="pill"><strong>Beynəlxalq</strong> səviyyə</span>
    <span class="pill"><strong>Onlayn</strong> + <strong>Offline</strong></span>
  </div>
</div>

<div class="selector-section">
  <div class="selector-inner">
    <div class="sel-tab active" id="tab-sanəd" onclick="switchTab('sanəd')">
      <div>
        <div>Baza: Ümumi Psixologiya</div>
        <span class="tab-sub">DPO Diplomu + Praktikum</span>
      </div>
    </div>
    <div class="sel-tab" id="tab-praktikum" onclick="switchTab('praktikum')">
      <div>
        <div>Tam: Klinik Psixologiya</div>
        <span class="tab-sub">Ümumi + Klinik DPO + Praktikum</span>
      </div>
    </div>
  </div>
</div>

<!-- ==============================================
     TAB 1: BAZA ÜMUMİ PSİXOLOGİYA 
     ============================================== -->
<div id="panel-sanəd" class="program-panel active">
  <section style="background:var(--white);">
    <div class="sanəd-grid">
      
      <!-- LEFT DESC -->
      <div class="sanəd-intro">
        <span class="tag">BAZA İXTİSAS (1 İL)</span>
        <h2 class="h2">Ümumi Psixologiya və Praktikum</h2>
        <p>Başqa sahə üzrə ali təhsiliniz var, amma psixoloq olmaq istəyirsiniz? Yenidən 4 il bakalavr oxumağa ehtiyac yoxdur. Azərbaycan qanunvericiliyi (163 nömrəli qərar) 1 illik rəsmi yenidənhazırlanma yolunu - DPO-nu təklif edir.</p>

        <div class="highlight-box">
          <h4 style="color:var(--navy);font-weight:700;margin-bottom:8px;">Nostrifikasiya Tələb Olunmur!</h4>
          <p>Tibb diplomlarından fərqli olaraq, <strong>Əlavə Peşə Təhsili (DPO)</strong> diplomu ilə Azərbaycanda fəaliyyət göstərmək üçün heç bir nostrifikasiya tələb olunmur.</p>
        </div>

        <div class="accordion">
          <!-- Item 1 -->
          <div class="accordion-item open" id="acc1">
            <div class="accordion-head" onclick="toggleAcc('acc1')">
              <div class="accordion-head-left">
                <div class="accordion-icon icon-doc">D</div>
                <div>
                  <div class="accordion-title">Sənəd — Rəsmi Diplom və Hüquqi Əsas</div>
                  <div class="accordion-subtitle">Qanunvericilik tərəfi (163 n. Qərar)</div>
                </div>
              </div>
              <svg class="accordion-arrow" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/></svg>
            </div>
            <div class="accordion-body" id="acc1-body" style="max-height:1000px;">
              <div class="accordion-body-inner">
                <ul class="doc-list">
                  <li><span class="doc-check">✓</span> Rəsmi DPO Diplomu (FRDO reyestrinə daxil edilir)</li>
                  <li><span class="doc-check">✓</span> IPAS Beynəlxalq Üzvlük forması</li>
                </ul>
                <div class="law-links">
                  <a href="qanunlar.html" class="law-link">"Psixoloji Yardım haqqında" Qanun</a>
                  <a href="qanunlar.html" class="law-link">Əlavə Peşə Təhsili haqqında Tənzimləmə</a>
                </div>
              </div>
            </div>
          </div>
          <!-- Item 2 -->
          <div class="accordion-item" id="acc2">
            <div class="accordion-head" onclick="toggleAcc('acc2')">
              <div class="accordion-head-left">
                <div class="accordion-icon icon-prak">P</div>
                <div>
                  <div class="accordion-title">Sənət — Praktikum Məzmunu</div>
                  <div class="accordion-subtitle">Peşəkar bacarıq, real nəticələr</div>
                </div>
              </div>
              <svg class="accordion-arrow" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/></svg>
            </div>
            <div class="accordion-body" id="acc2-body">
              <div class="accordion-body-inner">
                <p>Nəzəriyyə deyil, birbaşa müştərilərinizdə gözlənilən effekti verəcək praktiki alətləri öyrənirsiniz.</p>
                <div style="margin-top:14px;">
                   <a href="proqram.html" class="btn btn-outline-dark btn-sm">Bütün Tədris Proqramını Bax →</a>
                </div>
              </div>
            </div>
          </div>
        </div>
        
      </div>
      
      <!-- RIGHT PRICE -->
      <div class="sanəd-card">
        <div class="price-card">
          <span class="price-card-tag">ÜMUMİ PSİXOLOGİYA DİPLOMU</span>
          <h3>1 İllik Baza DPO Proqramı</h3>
          <div class="price-main">3 600 <span>AZN</span></div>
          <p style="font-size:0.85rem; color:rgba(255,255,255,0.7); margin-bottom:20px;">Praktikum proqrama tam daxildir.</p>
          <ul class="doc-list" style="margin-bottom:20px; border-top:1px solid rgba(255,255,255,0.1); padding-top:20px;">
            <li style="border-bottom:none; color:rgba(255,255,255,0.85)"><span style="color:var(--accent);">✓</span> 300-dən çox dərsin video arxivi sərbəst baxış üçün</li>
            <li style="border-bottom:none; color:rgba(255,255,255,0.85)"><span style="color:var(--accent);">✓</span> Hər ay yeni praktiki dərslərə qatılmaq imkanı</li>
            <li style="border-bottom:none; color:rgba(255,255,255,0.85)"><span style="color:var(--accent);">✓</span> Bu tədris proqramında öyrədilən metodikalar sayəsində sizin pasiyentləriniz sizi hamıya tövsiyə edəcəklər</li>
          </ul>
          <a href="#registration" class="btn-enroll">Qeydiyyata yazıl</a>
        </div>
      </div>
    
    </div>

    <!-- PERSUASION ELEMENTS (Applies to both) -->
    <div style="max-width:1240px; margin: 40px auto 0;">
      
      <div class="free-lesson">
        <div>
          <span class="tag">🎁 PULSUZ QİYMƏTLƏNDİR</span>
          <h3 class="h3">Tədris formatını test edin</h3>
          <p style="color:var(--gray); margin-bottom:16px;">Sözlə vermədiyimiz zəmanəti bir videoda göstəririk. Ailə terapiyası dərsimizi izlədikdən sonra "Mən bu pasiyent yerində olsaydım, pul ödəməyə hazır idimmi?" sualına hə cavab verəcəksiniz.</p>
          <a href="https://youtube.com" class="btn" style="background:#FF0000; color:white; padding:10px 18px;">YouTube-da İzlə</a>
        </div>
        <div style="background:var(--white); padding:24px; border-left:4px solid var(--accent); border-radius:8px;">
          <p style="font-style:italic; font-size:0.95rem; color:var(--text);">"Metodika o qədər aydın idi ki, bir dərsdən sonra artıq öz sınaq konsultasiyamda fərqi hiss etdim. Hər kəs nəzəriyyə danışır, Dr. Rəhimov isə birbaşa problemi kəsən qılıncı verir."</p>
          <cite style="display:block; margin-top:10px; font-size:0.8rem; color:var(--gray);">&mdash; Məzun Rəyi</cite>
        </div>
      </div>

    </div>
  </section>
</div>

<!-- ==============================================
     TAB 2: TAM KLİNİK PSİXOLOGİYA 
     ============================================== -->
<div id="panel-praktikum" class="program-panel">
  <section style="background:var(--white);">
    <div class="sanəd-grid">
      
      <!-- LEFT DESC -->
      <div class="sanəd-intro">
        <span class="tag" style="color:var(--navy);">TAM İXTİSASLAŞMA</span>
        <h2 class="h2">Klinik Psixologiya və Praktikum</h2>
        <p>Həm Ümumi Psixologiya, həm Klinik Psixiatriya, həm də Praktikum modulları birbaşa bir yerdə. Bu paket yalnız sənəd deyil, ağır psixiatrik patologiyaları KBT və digər dərin metodlarla tanımaq və müalicə etmək üçün real icazədir.</p>

        <div class="prak-hero">
          <h2 style="font-size:1.6rem;">Peşəkar bacarıq, real nəticələr.</h2>
          <p>Yalnız diplom müştəri gətirmir, razı qalan müştərilər tövsiyə ilə yeni müştərilər gətirir. Bizim əsas strategiyamız Sizi bu nəticələrə çatdırmaqdır.</p>
        </div>

        <h3 class="h3" style="margin-top:40px;">Proqramın məzmunu</h3>
        <p style="color:var(--gray);">Tam tədris strukturunu görmək üçün ətraflı cədvələ baxa bilərsiniz.</p>
        <a href="proqram.html" class="btn btn-outline-dark btn-sm" style="margin-top:10px;">Proqram detalları →</a>

      </div>
      
      <!-- RIGHT PRICE -->
      <div class="sanəd-card">
        <div class="price-card" style="background:#0a1628; border-top:4px solid var(--accent);">
          <span class="price-card-tag" style="color:var(--accent);">KLİNİK PSİXOLOQ DİPLOMU</span>
          <h3>Klinik + Ümumi Psixologiya + Praktikum</h3>
          <div class="price-main">6 000 <span>AZN</span></div>
          <p style="font-size:0.85rem; color:rgba(255,255,255,0.7); margin-bottom:20px;">Bütün proqramlar və praktikum daxildir.</p>
          <ul class="doc-list" style="margin-bottom:20px; border-top:1px solid rgba(255,255,255,0.1); padding-top:20px;">
            <li style="border-bottom:none; color:rgba(255,255,255,0.85)"><span style="color:var(--accent);">✓</span> Təhsil Nazirliyi nostrifikasiyası tələb olunmayan Rəsmi DPO (1 il)</li>
            <li style="border-bottom:none; color:rgba(255,255,255,0.85)"><span style="color:var(--accent);">✓</span> 300-dən çox dərsin video arxivi sərbəst baxış üçün</li>
            <li style="border-bottom:none; color:rgba(255,255,255,0.85)"><span style="color:var(--accent);">✓</span> Hər ay yeni praktiki dərslərə qatılmaq imkanı</li>
            <li style="border-bottom:none; color:rgba(255,255,255,0.85)"><span style="color:white; font-weight:700;">✓ Bu tədris proqramında öyrədilən metodikalar sayəsində sizin pasiyentləriniz sizi hamıya tövsiyə edəcəklər</span></li>
          </ul>
          <a href="#registration" class="btn-enroll">Qeydiyyata yazıl</a>
        </div>
      </div>
      
    </div>
  </section>
</div>

<!-- ==============================================
     COMMON REGISTRATION & FOOTER
     ============================================== -->
<section style="background:var(--light);" id="registration">
  <div class="section-inner" style="max-width:600px; text-align:center;">
    <h2 class="h2">Başlamağa hazırsınız?</h2>
    <p class="lead" style="margin-bottom:30px;">Formanı doldurun, 24 saat ərzində sizinlə əlaqə saxlanılacaq.</p>
    <div style="background:var(--white); padding:32px; border-radius:12px; box-shadow:0 10px 30px rgba(0,0,0,0.05); text-align:left;">
      <div class="form-group">
        <label>Ad və Soyad</label>
        <input type="text" placeholder="Məsələn, Aygün Məmmədova" />
      </div>
      <div class="form-group">
        <label>Telefon Nömrəsi</label>
        <input type="text" placeholder="+994 (__) ___-__-__" />
      </div>
      <div class="form-group">
        <label>Vəzifəniz / Təhsiliniz</label>
        <input type="text" placeholder="Universitet, ixtisasınız" />
      </div>
      <div class="form-group">
        <label>Təhsil İstiqaməti</label>
        <select id="program-select">
          <option value="Ümumi Psixologiya (3600 AZN)">Baza: Ümumi Psixologiya (3600 AZN)</option>
          <option value="Klinik Psixologiya (6000 AZN)">Tam: Klinik Psixologiya (6000 AZN)</option>
        </select>
      </div>
      <button class="btn btn-primary" style="width:100%; margin-top:10px;">Müraciət Et</button>
    </div>
  </div>
</section>

<footer>
  <div class="footer-simple" style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:16px;">
    <a href="index.html" class="logo">R<span style="color:var(--accent);">.</span>AGIMOFF</a>
    <div style="display:flex; gap:16px;">
      <a href="tehsil.html">Təhsil</a>
      <a href="b2b.html">Korporativ</a>
      <a href="cert.html">Sertifikat</a>
    </div>
    <span style="font-size:0.8rem;">© 2026 Ragimoff.org</span>
  </div>
</footer>

<script>
  function switchTab(id) {
    document.querySelectorAll('.sel-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.program-panel').forEach(p => p.classList.remove('active'));
    document.getElementById('tab-' + id).classList.add('active');
    document.getElementById('panel-' + id).classList.add('active');
  }
  function toggleAcc(id) {
    let item = document.getElementById(id);
    let body = document.getElementById(id+'-body');
    if (item.classList.contains('open')) {
      item.classList.remove('open');
      body.style.maxHeight = '0';
    } else {
      item.classList.add('open');
      body.style.maxHeight = body.scrollHeight + 'px';
    }
  }
</script>
</body>
</html>"""

with open(r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\tehsil.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Restored tehsil.html with the correct sales/AIDA structure, Tabs, and the required exact pain-point bullets.")
