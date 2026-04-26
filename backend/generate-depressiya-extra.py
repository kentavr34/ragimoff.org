# -*- coding: utf-8 -*-
import pathlib
ROOT = pathlib.Path(r"C:\Users\SAM\Desktop\sayt2")

CHROME = r"""<!doctype html>
<html lang="az">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="{desc}" />
    <title>{title} | RAGIMOFF</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="gtc.css" />
    <style>
      .art-cover { width:100%; aspect-ratio:16/9; object-fit:cover; display:block; margin:0 0 32px; }
      .art-fig { margin:36px -20px; }
      .art-fig img { width:100%; aspect-ratio:16/10; object-fit:cover; display:block; }
      .art-fig figcaption { font-size:.8125rem; color:var(--clr-text-muted); margin-top:10px; padding:0 20px; font-style:italic; }
      .art-sources { margin-top:48px; padding-top:24px; border-top:1px solid var(--clr-border); font-size:.85rem; color:var(--clr-text-muted); }
      .art-sources strong { color:var(--clr-heading); display:block; margin-bottom:8px; }
      .art-sources a { color:var(--accent); text-decoration:none; }
      .art-sources a:hover { text-decoration:underline; }
      @media (max-width:768px) { .art-fig { margin:28px 0; } }
    </style>
  </head>
  <body>
    <header class="site-header">
      <div class="header-inner">
        <a href="index.html" class="logo-box"><span class="logo-text">RAGIMOFF<em>.</em></span><span class="logo-sub">Psixologiya Məktəbi</span></a>
        <nav class="desktop-nav">
          <a href="index.html">Ana Səhifə</a>
          <a href="tehsil.html">Təhsil</a>
          <a href="xidmetler.html">Konsultasiya</a>
          <a href="b2b.html">Korporativ</a>
          <a href="blog.html" class="nav-active">Blog</a>
          <a href="tehsil.html#registration" class="nav-cta">Qeydiyyat</a>
        </nav>
        <button class="mobile-toggle" onclick="toggleMenu()" aria-label="Menu"><svg viewBox="0 0 24 24"><path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z" /></svg></button>
      </div>
    </header>
    <nav class="mobile-nav" id="mobileNav">
      <button class="mobile-nav-close" onclick="toggleMenu()"><svg viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" /></svg></button>
      <a href="index.html">Ana Səhifə</a><a href="tehsil.html">Təhsil</a><a href="xidmetler.html">Konsultasiya</a><a href="b2b.html">Korporativ</a><a href="blog.html">Blog</a><a href="tehsil.html#registration" class="btn btn-fill">Qeydiyyat</a>
    </nav>
    <section class="pg-hero pg-hero-plain" data-theme="dark">
      <div class="pg-hero-inner"><span class="badge">{badge}</span><h1 class="hero-h1">{title}</h1><p class="hero-lead">Kənan Rəhimov · {read_time} dəq oxuma · 2026</p></div>
    </section>
    <section data-theme="light">
      <div class="sec-inner" style="padding:var(--s-section); max-width:760px; text-align:left">
        <img src="{cover}" alt="{cover_alt}" class="art-cover" loading="lazy" />
        <div class="article-body">
{body}
        </div>
        <div class="author-block" style="margin-top:48px">
          <div><strong>Kənan Rəhimov</strong><p style="color:var(--clr-text-muted); font-size:.9rem; margin:4px 0 0">Həkim-Psixiatr, Psixoterapevt. 23 il klinik təcrübə.</p></div>
        </div>
        <div class="art-sources"><strong>Mənbələr:</strong>
{sources}
        </div>
      </div>
    </section>
    <section data-theme="dark" style="background:var(--navy)">
      <div class="sec-inner" style="padding:var(--s-section)">
        <span class="badge">OXUYUN</span>
        <h2 class="sec-h2">Digər Məqalələr</h2>
        <div class="blog-grid-2" style="margin-top:32px; display:grid; grid-template-columns:repeat(3,1fr); gap:24px">
{related}
        </div>
      </div>
    </section>
    <div class="cta-band" data-theme="dark">
      <div class="cta-band-inner">
        <h2 class="sec-h2">{cta_h}</h2><p class="sec-sub">{cta_sub}</p>
        <div class="cta-band-btns"><a href="https://wa.me/994702200376" class="btn btn-fill" target="_blank">WhatsApp ilə Yazın</a><a href="{cta_link}" class="btn btn-line">{cta_link_text}</a></div>
      </div>
    </div>
    <footer class="site-footer" data-theme="dark">
      <div class="footer-inner"><div class="footer-grid">
        <div><a href="index.html" class="logo-box footer-logo"><span class="logo-text">RAGIMOFF<em>.</em></span><span class="logo-sub">Psixologiya Məktəbi</span></a><p class="footer-desc">Kənan Rəhimov — Həkim-Psixiatr, Psixoterapevt. 23 il klinik təcrübə. Bakı, Azərbaycan.</p>
        <div class="social-links"><a href="https://t.me/ragimoff" target="_blank" class="social-btn">TG</a><a href="https://www.facebook.com/Ragimoff.az" target="_blank" class="social-btn">FB</a><a href="https://www.instagram.com/dr.ragimoff" target="_blank" class="social-btn">IG</a><a href="https://youtube.com/@kragimoff" target="_blank" class="social-btn">YT</a></div></div>
        <div><span class="footer-col-title">Terapiya</span><ul class="footer-links"><li><a href="aile-terapiyasi.html" class="footer-link">Ailə Terapiyası</a></li><li><a href="enurez.html" class="footer-link">Gecə Enurezi</a></li><li><a href="panik-ataklar.html" class="footer-link">Panik Ataklar</a></li><li><a href="depressiya.html" class="footer-link">Depressiya</a></li><li><a href="sosial-fobiya.html" class="footer-link">Sosial Fobiya</a></li></ul></div>
        <div><span class="footer-col-title">Təhsil</span><ul class="footer-links"><li><a href="program-umumi.html" class="footer-link">Ümumi Psixologiya</a></li><li><a href="program-klinik.html" class="footer-link">Klinik Psixologiya DPO</a></li><li><a href="program-praktikum.html" class="footer-link">Psixoterapiya Praktikumu</a></li><li><a href="blog.html" class="footer-link">Psixologiya Bloqu</a></li></ul></div>
        <div><span class="footer-col-title">Əlaqə</span><ul class="footer-links"><li><a href="tel:+994702200376" class="footer-link">(+994) 70-220-03-76</a></li><li><a href="mailto:info@ragimoff.org" class="footer-link">info@ragimoff.org</a></li><li><a href="https://wa.me/994702200376" class="footer-link">WhatsApp</a></li></ul></div>
      </div><div class="footer-bottom"><p>© 2026 RAGIMOFF Peşəkar Psixologiya Məktəbi. Peşəkar Nüfuzun Ünvanı.</p><a href="https://www.psychotherapyru.com" target="_blank" class="footer-link">Русская версия</a></div></div>
    </footer>
    <a href="https://wa.me/994702200376" class="wa-float" target="_blank" aria-label="WhatsApp"><svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg></a>
    <script src="shared.js"></script>
  </body>
</html>
"""

CARD = """          <a href="{slug}" class="blog-card" style="text-decoration:none">
            <div class="blog-card-body">
              <span class="blog-card-cat">{cat}</span>
              <h3 class="blog-card-title">{title}</h3>
              <p class="blog-card-excerpt">{excerpt}</p>
            </div>
          </a>"""

# 3 əlavə depressiya məqalələri
DEPRESSIYA = [
    {
        "slug": "blog-depressiya-3.html",
        "badge": "KLİNİK",
        "title": "Antidepressantlar — Faktlar və Miflər",
        "desc": "SSRI nədir, asılılıq yaradırmı, ömürlük olarmı — antidepressantlar haqqında elmi cavablar.",
        "read_time": 9,
        "cover": "images/blog/depressiya/art3-cover.jpg",
        "cover_alt": "Antidepressant tabletlər",
        "cta_h": "Depressiya ilə bağlı sual?",
        "cta_sub": "Sertifikatlı psixiatr-psixoterapevt ilə konsultasiya",
        "cta_link": "depressiya.html",
        "cta_link_text": "Depressiya Müalicəsi",
        "short": "SSRI, asılılıq qorxusu, müddət, dayandırma — antidepressantlar haqqında elmi cavablar.",
        "cat": "Klinik",
        "body": """          <p>Antidepressantlar — psixiatriyada ən çox yazılan, lakin ən çox səhv başa düşülən dərmanlardandır. "Onlar asılılıq yaradır", "ömürlük içməli olarsan", "şəxsiyyətini dəyişir" — yayılmış inanclar. Bu məqalədə dəlilə əsaslanan cavablar veririk.</p>

          <h2>Antidepressantların Növləri</h2>
          <p><strong>SSRI</strong> (Selektiv Serotonin Geri Götürmə İnhibitorları) — birinci xətt müalicə. Sertralin (Zoloft), fluoxetin (Prozak), paroksetin (Paxil), essitalopram (Lexapro). Yan təsir profili nisbətən yumşaqdır.</p>
          <p><strong>SNRI</strong> (Serotonin-Noradrenalin) — venlafaksin (Effexor), duloksetin (Cymbalta). Yorğunluq və ağrı simptomlarında daha effektiv.</p>
          <p><strong>Triklik antidepressantlar</strong> — köhnə nəsil (amitriptilin, imipramin). Effektiv, lakin yan təsir profili daha ağırdır.</p>
          <p><strong>MAOI</strong> — qida məhdudiyyəti tələb edir, nadir hallarda istifadə olunur.</p>

          <h2>Mif 1: "Antidepressantlar asılılıq yaradır"</h2>
          <p><strong>Yalan.</strong> Antidepressantlar bağımlılıq yaratmır — yəni doza artırmaq tələb etmir, "kayf" vermir, kompulsiv axtarış davranışı yaratmır.</p>
          <p>Lakin uzun istifadədən sonra <strong>kəsmə sindromu</strong> (discontinuation syndrome) ola bilər — başgicəllənmə, başağrısı, ürəkbulanma, "elektrik şoku" hissi. Bu narkotik geri çəkilməsi deyil — sadəcə beyin kimyasının yenidən tarazlanması. Tədricən doza azaltmaqla qarşısı alınır.</p>

          <h2>Mif 2: "Antidepressantlar şəxsiyyəti dəyişir"</h2>
          <p><strong>Yalan.</strong> Antidepressantlar şəxsiyyəti dəyişdirməz — onlar depressiyanın "blok" etdiyi orijinal şəxsiyyəti geri qaytarırlar. Pasiyentlər tez-tez deyirlər: "İndi yenə özüm hiss edirəm".</p>
          <p>Yan təsir kimi ola bilən duyğusal "düz" hiss (emotional blunting) — 10-15% pasiyentdə baş verir. Bu zaman doza tənzimlənməsi və ya dərman dəyişikliyi həll edir.</p>

          <h2>Mif 3: "Bir dəfə başlayanda ömürlük içməli olarsan"</h2>
          <p><strong>Yalan.</strong> Standart kurs:</p>
          <ul>
            <li><strong>İlk epizod:</strong> 6-12 ay (remissiyadan sonra)</li>
            <li><strong>İkinci epizod:</strong> 1-2 il</li>
            <li><strong>3+ epizod:</strong> uzunmüddətli (lakin yenə də nəzərdən keçirilir)</li>
          </ul>
          <p>Pasiyentlərin əksəriyyəti müalicədən tədricən kənarlaşır.</p>

          <h2>Mif 4: "Tez işləyir"</h2>
          <p><strong>Yalan — yarımyalan.</strong> Yan təsirlər tez gəlir (mədə-bağırsaq, başağrısı, yuxu pozulması) — 1-2 həftə. Lakin <strong>terapevtik effekt 4-6 həftə tələb edir</strong>. Bu səbəbdən bir çox pasiyent "işləmir" deyə dərmanı atırlar — əslində yanlışlıq.</p>

          <h2>Effektivlik</h2>
          <p>Tədqiqatlar (Cipriani et al., 2018, meta-analiz, 522 tədqiqat):</p>
          <ul>
            <li>Antidepressantlar plasebodan əhəmiyyətli effektivdirlər (effect size 0.30)</li>
            <li>Yüngül depressiyada effektivlik məhduddur — psixoterapiya üstün</li>
            <li>Orta-ağır depressiyada — KDT + dərman birgə ən yüksək nəticə</li>
            <li>Ağır depressiyada — dərman müdaxiləsi vacibdir</li>
          </ul>

          <h2>Nə Vaxt Antidepressant Lazımdır?</h2>
          <ul>
            <li>Ağır depressiya (intihar düşüncələri, funksional çökmə)</li>
            <li>Orta dərəcəli, KDT-yə tam cavab verməyən</li>
            <li>Pasiyentin tərcihi (terapiyaya alternativ kimi)</li>
            <li>Təkrarlanan epizodlar (residiv profilaktikası)</li>
            <li>Ağır anksiyete + depressiya kombinasiyası</li>
          </ul>

          <h2>Doğru Plan</h2>
          <ol>
            <li>Psixiatr qiymətləndirməsi</li>
            <li>Birinci dərman seçimi (adətən SSRI)</li>
            <li>4-6 həftə davam — qiymətləndirmə</li>
            <li>Effekt yoxdursa — doza artırma və ya dəyişmə</li>
            <li>Remissiyadan sonra 6-12 ay davam</li>
            <li>Tədricən kəsilmə (4-8 həftə)</li>
            <li>KDT psixoterapiyası ilə birlikdə</li>
          </ol>

          <p>Antidepressant — alət, "həll" deyil. Psixoterapiya beyni öyrədir, dərman vəziyyəti idarə edir. Birgə işləyəndə nəticə ən yüksəkdir.</p>""",
        "sources": """          <p><a href="https://www.nimh.nih.gov/health/topics/mental-health-medications" target="_blank" rel="noopener">NIMH — Mental Health Medications</a></p>
          <p>Cipriani, A., et al. (2018). Comparative efficacy and acceptability of 21 antidepressant drugs. <em>The Lancet</em>, 391(10128), 1357-1366.</p>
          <p><a href="https://www.nice.org.uk/guidance/ng222" target="_blank" rel="noopener">NICE NG222 — Depression: treatment and management</a></p>
          <p>Stahl, S. M. (2021). <em>Stahl's Essential Psychopharmacology</em> (5th ed.). Cambridge University Press.</p>"""
    },
    {
        "slug": "blog-depressiya-4.html",
        "badge": "KLİNİK",
        "title": "Postpartum Depressiya — Tanımaq və Müalicə",
        "desc": "Doğuşdan sonra depressiya — 'baby blues' deyil. Tanıma, risk amilləri, müalicə yolları.",
        "read_time": 8,
        "cover": "images/blog/depressiya/art4-cover.jpg",
        "cover_alt": "Ana və körpə",
        "cta_h": "Doğuşdan sonra depressiya?",
        "cta_sub": "Anaların 15-20%-i bunu yaşayır. Müalicə var",
        "cta_link": "depressiya.html",
        "cta_link_text": "Depressiya Müalicəsi",
        "short": "Doğuşdan sonra depressiya — 'baby blues' deyil. Tanıma, risk faktorları, müalicə.",
        "cat": "Klinik",
        "body": """          <p>"Yeni doğulmuş körpəm var, hamı sevinirsə nə üçün mən belə kədərliyəm?" — postpartum depressiya yaşayan ananın tipik düşüncəsi. Statistik olaraq, doğum verən qadınların <strong>15-20%-i postpartum depressiyadan</strong> əziyyət çəkir (NICE, WHO 2023).</p>

          <p>Bu — "baby blues" deyil — klinik vəziyyətdir, müalicə tələb edir.</p>

          <h2>Baby Blues vs Postpartum Depressiya</h2>
          <p><strong>Baby Blues</strong> (50-80% qadınlarda): doğumdan 2-3 gün sonra başlayır, 1-2 həftə davam edir. Hormonal dəyişikliyə təbii cavabdır. Simptomlar: ağlamaq, narahatlıq, yorğunluq. Müalicə tələb etmir, özü keçir.</p>

          <p><strong>Postpartum Depressiya</strong>: doğumdan 2 həftədən sonra başlayır, aylar davam edir. Klinik depressiya kriteriyalarına uyğundur (DSM-5). Simptomlar daha ağırdır:</p>
          <ul>
            <li>Daimi kədər, ümidsizlik (2 həftədən çox)</li>
            <li>Körpəyə qarşı bağlanma çətinliyi</li>
            <li>İştah pozğunluğu (yox və ya çoxlu)</li>
            <li>Yuxu pozğunluğu (körpədən asılı olmayaraq)</li>
            <li>Özünü "pis ana" hesab etmə</li>
            <li>Konsentrasiya çətinliyi</li>
            <li>Zərər vermə düşüncələri (özünə və ya körpəyə)</li>
          </ul>

          <h2>Risk Amilləri</h2>
          <ul>
            <li>Keçmişdə depressiya tarixçəsi</li>
            <li>Doğum zamanı stresli təcrübə</li>
            <li>Sosial dəstək çatışmazlığı</li>
            <li>Maliyyə çətinlikləri</li>
            <li>Münasibət problemləri</li>
            <li>Hamiləlik dövründə depressiya</li>
            <li>Hormonal həssaslıq (premenstrual sindrom tarixçəsi)</li>
            <li>Genetika (ailədə depressiya)</li>
          </ul>

          <h2>Postpartum Psixoz — Acil Vəziyyət</h2>
          <p>Daha nadir (1-2/1000 doğum) lakin ciddi vəziyyət. Simptomlar: hallüsinasiyalar, bredler, konfuziya, yatmamaq. Bu — <strong>acil hospitalizasiya tələb edən vəziyyətdir</strong>. Adətən 2 həftə içində başlayır.</p>

          <h2>Müalicə</h2>
          <p>NICE və APA qaydaları:</p>

          <p><strong>Yüngül-orta postpartum depressiya:</strong></p>
          <ul>
            <li>KDT və ya İnterpersonal Terapiya (IPT)</li>
            <li>Sosial dəstək (qrup terapiyası)</li>
            <li>Müntəzəm fiziki aktivlik</li>
            <li>Yuxu rejiminin bərpası (partner kömək edir)</li>
          </ul>

          <p><strong>Orta-ağır:</strong></p>
          <ul>
            <li>Psixoterapiya + antidepressant</li>
            <li>Ana südü ilə qidalandıran qadınlar üçün təhlükəsiz dərmanlar var (sertralin)</li>
          </ul>

          <p><strong>Ağır vəziyyətdə:</strong> hospitalizasiya, antidepressant + bəzi hallarda EKT.</p>

          <h2>Atalarda Postpartum Depressiya</h2>
          <p>Tədqiqatlar göstərib ki, atalar da postpartum depressiyadan əziyyət çəkə bilər (8-10%). Simptomlar daha çox: çəkinmə, izolyasiya, qıcıqlanma, qaçma davranışı. Ailədə həm ana, həm ata yoxlanılmalıdır.</p>

          <h2>Niyə Yardım İstəmək Çətindir?</h2>
          <ul>
            <li>"Yaxşı ana belə hiss etməməlidir" inancı</li>
            <li>"Hormonaldır, keçər" üzərinə güvənmə</li>
            <li>Stiqma və ailənin "üyürdür" hesab etməsi</li>
            <li>Praktik səbəblər (körpə baxımı, vaxt yoxluğu)</li>
            <li>Maddə qoxusu körpəyə vermək qorxusu (yalnışlıq)</li>
          </ul>

          <h2>Praktik Addımlar</h2>
          <ol>
            <li><strong>İlk pediatra və ya ginekoloqa müraciət</strong> — onlar Edinburgh Postpartum Depression Scale ilə yoxlama edirlər</li>
            <li><strong>Psixiatr və ya klinik psixoloq qiymətləndirməsi</strong></li>
            <li><strong>Aile dəstəyini səfərbər etmək</strong> — körpə baxımı paylaşılmalı</li>
            <li><strong>Online qruplara qoşulma</strong> — eyni təcrübə yaşayan analar</li>
          </ol>

          <p>Vacib mesaj: <strong>postpartum depressiyadan əziyyət çəkmək sizi pis ana etmir</strong>. Müalicə almaq isə körpənizə də sizə də ən yaxşı hədiyyədir.</p>""",
        "sources": """          <p><a href="https://www.nimh.nih.gov/health/publications/postpartum-depression-facts" target="_blank" rel="noopener">NIMH — Postpartum Depression Facts</a></p>
          <p><a href="https://www.who.int/news-room/fact-sheets/detail/maternal-mental-health" target="_blank" rel="noopener">WHO — Maternal Mental Health</a></p>
          <p><a href="https://www.nice.org.uk/guidance/cg192" target="_blank" rel="noopener">NICE CG192 — Antenatal and postnatal mental health</a></p>
          <p>O'Hara, M. W., & McCabe, J. E. (2013). Postpartum depression: current status and future directions. <em>Annual Review of Clinical Psychology</em>, 9, 379-407.</p>"""
    },
    {
        "slug": "blog-depressiya-5.html",
        "badge": "KLİNİK",
        "title": "Mövsümi Depressiya (SAD) və İşıq Terapiyası",
        "desc": "Qışda başlayan, yazda keçən depressiya — Mövsümi Affektiv Pozğunluq (SAD). İşıq terapiyası mexanizmi.",
        "read_time": 7,
        "cover": "images/blog/depressiya/art5-cover.jpg",
        "cover_alt": "Qış pəncərəsi",
        "cta_h": "Mövsümi depressiya?",
        "cta_sub": "İşıq terapiyası və KDT effektiv işləyir",
        "cta_link": "depressiya.html",
        "cta_link_text": "Depressiya Müalicəsi",
        "short": "Qışda başlayan, yazda keçən depressiya — Mövsümi Affektiv Pozğunluq və işıq terapiyası.",
        "cat": "Klinik",
        "body": """          <p>"Sentyabr-oktyabrda başlayan, mart-aprildə keçən kədər" — bu sadə təsvir Mövsümi Affektiv Pozğunluq (Seasonal Affective Disorder, SAD) adlanır. Bu — "qış kədəri" deyil, klinik vəziyyətdir.</p>

          <p>Statistik olaraq, şimal yarımkürədəki ölkələrdə əhalinin <strong>1-10%-i</strong> klinik SAD-dan əziyyət çəkir (yüksək enliyə yaxınlaşdıqca artır). Azərbaycan kimi orta enliklərdə də simptomlar əhəmiyyətli rast gəlir.</p>

          <h2>SAD Simptomları</h2>
          <p>Klassik depressiya simptomlarından bir neçə fərq:</p>
          <ul>
            <li><strong>Yatma artımı</strong> (hipersomnia) — adi depressiyada əksinə</li>
            <li><strong>Karbohidrata qarşı şiddətli istək</strong> — şirniyyat, çörək</li>
            <li><strong>Çəki artımı</strong> (adi depressiyada azalma daha tez-tez)</li>
            <li><strong>Letarji</strong> — fiziki ağırlıq hissi</li>
            <li>Ümumi depressiya simptomları (kədər, anhedoniya, konsentrasiya pozğunluğu)</li>
          </ul>

          <p><strong>Atipik mövsümi:</strong> bəzilərində SAD yazda başlayır, payızda keçir — daha az tez-tez.</p>

          <h2>Niyə Baş Verir?</h2>
          <p>Əsas mexanizmlər:</p>

          <p><strong>1. Sirkadian Ritm Pozulması.</strong> Qışda günəş işığı az olduğu üçün beyinin daxili saatı pozulur. Yatma və oyanma siklləri sürüşür.</p>

          <p><strong>2. Melatonin Disregulyasiyası.</strong> Qaranlıq melatonin istehsalını artırır — qış boyu davamlı yüksək melatonin yorğunluq və depressiv əhval-ruhiyyə yaradır.</p>

          <p><strong>3. Serotonin Aşağı Düşməsi.</strong> İşıq qıtlığı serotonin reseptorlarının fəaliyyətini azaldır. Serotonin əhval-ruhiyyə tənzimləyicisidir.</p>

          <p><strong>4. D Vitamini Çatışmazlığı.</strong> Günəş D vitamini istehsalı üçün vacibdir. D vitamini reseptorlarının beynin əhval-ruhiyyə nahiyəsində olduğu məlumdur.</p>

          <h2>İşıq Terapiyası — Birinci Xətt Müalicə</h2>
          <p>İşıq terapiyası (light therapy, fototerapiya) SAD üçün ən effektiv müalicədir. Tədqiqatlar (Lam et al., 2016, meta-analiz): <strong>pasiyentlərin 60-80%-ində 2-4 həftə ərzində əhəmiyyətli yaxşılaşma</strong>.</p>

          <p><strong>Necə işləyir?</strong></p>
          <ul>
            <li>10,000 lux gücündə xüsusi lampa (UV-siz, ağ işıq)</li>
            <li>Hər səhər 30 dəqiqə (oyandıqdan sonra ilk saat ərzində)</li>
            <li>Lampa 50-60 sm məsafədə üzdən yan tərəfə yönəldilir</li>
            <li>Bu zaman digər fəaliyyət (yemək, kitab, komputer) mümkündür</li>
            <li>Birbaşa lampaya baxmaq qadağandır — gözə zərər verir</li>
          </ul>

          <p><strong>Effekt nə vaxt başlayır?</strong> 2-4 həftə. Simptomlar 6-8 həftədə minimuma enir. Müalicə qış boyu davam etməlidir.</p>

          <h2>İşıq Terapiyası ilə Yan Təsirlər</h2>
          <ul>
            <li>Başağrısı (10-15%)</li>
            <li>Göz yorğunluğu</li>
            <li>Yuxusuzluq (axşam istifadə olunduqda)</li>
            <li>Mania tetikləmə (bipolar pozğunluqda risk)</li>
          </ul>

          <p>Diqqət: bipolar pozğunluq tarixçəsi olanlarda işıq terapiyası mania tetikləyə bilər. Psixiatrla məsləhətləşmə vacibdir.</p>

          <h2>Digər Müalicə Üsulları</h2>

          <p><strong>1. KDT (Mövsümi Versiya).</strong> Mövsümi düşüncə nümunələrinə fokuslanır: "qış keçməyəcək", "həmişə yorğun olacam". Effektivlik işıq terapiyası ilə müqayisə edilir, lakin qış sonu sonra effekt daha davamlıdır.</p>

          <p><strong>2. Antidepressantlar.</strong> SSRI (xüsusən bupropion) — bəzi hallarda profilaktik olaraq sentyabrdan başlayır.</p>

          <p><strong>3. D Vitamini Suplementi.</strong> Vitamin D çatışmazlığı varsa kömək edir, lakin tək başına SAD üçün effektiv deyil.</p>

          <p><strong>4. Yuxu Gigiyenası.</strong> Müntəzəm yuxu cədvəli, hətta həftəsonu, sirkadian ritmin sabitlığını saxlayır.</p>

          <p><strong>5. Açıq Hava Aktivliyi.</strong> Qışda da gündüz işıqlı saatlarda 30-60 dəqiqəlik gəzinti — antidepresant effekti var.</p>

          <h2>Praktik Plan</h2>
          <ol>
            <li>Sentyabr-oktyabrda işıq lampası alın</li>
            <li>Hər səhər 30 dəqiqə işıq terapiyası</li>
            <li>Gündəlik 30 dəqiqə açıq hava (gündüz saatlarında)</li>
            <li>Vitamin D-3 1000-2000 IU/gün (qan analizinə əsasən)</li>
            <li>Yuxu cədvəlini sabit saxlamaq</li>
            <li>Karbohidrat qəbulunu məhdudlaşdırmaq</li>
            <li>Simptomlar şiddətlənərsə — psixiatr</li>
          </ol>

          <p>SAD — müalicə oluna bilən mövsümi vəziyyətdir. Erkən və profilaktik yanaşma qışı keçirməyi qat-qat asanlaşdırır.</p>""",
        "sources": """          <p><a href="https://www.nimh.nih.gov/health/publications/seasonal-affective-disorder" target="_blank" rel="noopener">NIMH — Seasonal Affective Disorder</a></p>
          <p>Lam, R. W., et al. (2016). Light therapy for nonseasonal major depressive disorder. <em>JAMA Psychiatry</em>, 73(1), 56-63.</p>
          <p>Rosenthal, N. E. (2012). <em>Winter Blues: Everything You Need to Know to Beat Seasonal Affective Disorder</em>. Guilford.</p>
          <p>Pjrek, E., et al. (2020). The efficacy of light therapy in the treatment of seasonal affective disorder. <em>Psychotherapy and Psychosomatics</em>, 89(1), 17-24.</p>"""
    }
]

# 5 psixoloq-olmaq məqalələri
PSIXOLOQ = [
    {
        "slug": "blog-psixolog-olmaq.html",
        "badge": "PSIXOLOQLAR ÜÇÜN",
        "title": "Yaxşı Psixoloq Heç Vaxt İşsiz Qalmır — Niyə?",
        "desc": "Peşəkar psixoloqun karyera yolu — niyə bu sahədə daimi tələb var və necə yaxşı psixoloq olmaq.",
        "read_time": 8,
        "cover": "images/blog/psixoloq-olmaq/art1-cover.jpg",
        "cover_alt": "Psixoloq konsultasiyada",
        "cta_h": "Psixoloji təhsil almaq istəyirsiniz?",
        "cta_sub": "Beynəlxalq sertifikatlı DPO proqramı",
        "cta_link": "tehsil.html",
        "cta_link_text": "Təhsil Proqramları",
        "short": "Niyə peşəkar psixoloqlar daim tələbatdadır və yaxşı psixoloq olmaq üçün nə lazımdır.",
        "cat": "Psixoloqlar üçün",
        "body": """          <p>"Psixologiya peşəsi gələcəkdə tələb olunacaqmı?" — universitetə girən hər tələbənin verdiyi sual. Cavab: WHO və BƏƏT-ın 2023-cü il proqnozlarına görə, <strong>2030-ci ilə qədər dünyada psixoloji yardım sahəsində 5 milyon mütəxəssis çatışmazlığı yaranacaq</strong>.</p>

          <p>Lakin "psixoloq olmaq" və "yaxşı psixoloq olmaq" — fərqli şeylərdir. Bu məqalədə peşənin tələbat dinamikası və peşəkar psixoloq olmağın əsas elementlərini açırıq.</p>

          <h2>Niyə Psixoloji Yardım Tələbi Artır?</h2>

          <p><strong>1. Stiqmanın Azalması.</strong> 20 il əvvəl "psixoloqa getmək" utanc idi. Bu gün — özünə hörmətin əlamətidir. Yeniyetmə nəsillər (Z, Alpha) terapiyaya açıq yanaşır.</p>

          <p><strong>2. Stress Səviyyəsinin Artması.</strong> Sosial media, məlumat artıqlığı, iqlim narahatlığı, geosiyasi qeyri-müəyyənlik — müasir həyatın çətinlikləri stress yükünü artırır.</p>

          <p><strong>3. Korporativ Sektorun Tələbatı.</strong> Şirkətlər iş yerində psixoloji rifahı vacib hesab etməyə başlayıblar. EAP (Employee Assistance Programs) — sürətlə inkişaf edir.</p>

          <p><strong>4. Sosial Mediada Görünürlük.</strong> "Burnout", "anxiety", "boundaries" terminləri popularlaşıb. İnsanlar simptomları tanıyır və yardım axtarırlar.</p>

          <p><strong>5. Telepsixologiya.</strong> COVID-19 sonrası online terapiya normallaşıb — bu coğrafi maneələri qaldırır, tələbat artır.</p>

          <h2>"Yaxşı Psixoloq" Nədir?</h2>
          <p>Tədqiqatlar (Wampold, 2015): klinik nəticədə pasiyentin 30%-i terapevt-pasiyent əlaqəsindən, yalnız 15%-i texnikadan asılıdır. Yəni <strong>insan keyfiyyətləri texnikadan iki dəfə vacibdir</strong>.</p>

          <p>"Yaxşı psixoloq" qiymətləndirmə kriteriyaları:</p>
          <ul>
            <li><strong>Empati qabiliyyəti</strong> — müştərinin daxili dünyasına girə bilmək</li>
            <li><strong>Aktiv dinləmə</strong> — sözlərdən başqa hisslər, susqunluqlar oxumaq</li>
            <li><strong>Özünü tanıma</strong> — öz triggerləri, məhdudiyyətləri görmək</li>
            <li><strong>Etik bütövlük</strong> — sərhədləri qorumaq, gizliliyi saxlamaq</li>
            <li><strong>Davamlı öyrənmə</strong> — yeni metodlar, tədqiqatlar izləmək</li>
            <li><strong>Süpervizyon</strong> — peşəkar nəzarət altında işləmək</li>
            <li><strong>Şəxsi terapiya</strong> — özün də müştəri olmaq təcrübəsi</li>
          </ul>

          <h2>5 Əsas Karyera Addımı</h2>

          <p><strong>1. Bazis Təhsil.</strong> Bakalavr səviyyəsində psixologiya və ya yaxın sahə (sosial işçi, pediatriya). Yalnız bu səviyyə peşəkar psixoloji yardım üçün kifayət deyil.</p>

          <p><strong>2. Klinik İxtisaslaşma.</strong> Sertifikatlı DPO (Дополнительное Профессиональное Образование) və ya magistr proqramı klinik psixoloji bilik və bacarıqları verir.</p>

          <p><strong>3. Klinik Texnika İxtisaslaşması.</strong> KDT, EMDR, gestalt, sistem terapiya, EFT və s. Birini seçib dərinə getmək tövsiyə olunur — universal "her şey edən" yox.</p>

          <p><strong>4. Süpervizyon.</strong> İlk 100-200 saat müştəri işi mütləq sertifikatlı supervizorla. Bu peşəkar inkişafın ən sürətli yoludur.</p>

          <p><strong>5. Davamlı Təhsil.</strong> Hər il konfrans, kurs, kitab. Psixologiya sahəsi sürətlə inkişaf edir.</p>

          <h2>Karyera Yolları</h2>
          <ul>
            <li><strong>Özəl praktika</strong> — ən geniş yayılmış</li>
            <li><strong>Klinika və xəstəxana</strong> — multidisiplinar komandada iş</li>
            <li><strong>Korporativ sektor</strong> — HR, EAP proqramları</li>
            <li><strong>Məktəb psixoloqu</strong> — uşaq və yeniyetmələrlə</li>
            <li><strong>Akademik tədqiqat</strong> — universitet, institut</li>
            <li><strong>Online platformalar</strong> — BetterHelp, Talkspace tipli</li>
            <li><strong>Müəllim/treninq</strong> — gələcək psixoloqları öyrətmək</li>
          </ul>

          <h2>Maliyyə Perspektivi</h2>
          <p>Yaxşı psixoloqların gəlirlər (Bakı bazarında, 2026):</p>
          <ul>
            <li>Yeni başlayan: 800-1500 AZN/ay</li>
            <li>3-5 il təcrübə: 2000-4000 AZN/ay</li>
            <li>10+ il, sertifikatlı: 5000-12000 AZN/ay</li>
            <li>Korporativ konsultant: 8000-25000 AZN/ay</li>
          </ul>

          <h2>Real Çətinliklər</h2>
          <p>Yalnız real şəkilini göstərmək üçün:</p>
          <ul>
            <li>İlk 2-3 il müştəri tapmaq çətindir</li>
            <li>Emosional yüklənmə — pasiyentin travmasını içində aparmaq</li>
            <li>Burnout riski yüksəkdir — özünüqayğı vacibdir</li>
            <li>Daimi öyrənmə tələbi — peşə durmadan dəyişir</li>
            <li>Uğursuz halların məsuliyyəti</li>
          </ul>

          <h2>Yekun</h2>
          <p>Psixoloqluq — sadəcə peşə deyil, vokasiyadır (vocation). İnsanlara kömək etmək, özünü davamlı inkişaf etdirmək, dərin şəxsi mənaya sahib olmaq istəyənlər üçün — ən yaxşı seçimlərdən biridir.</p>

          <p>Yaxşı psixoloq heç vaxt işsiz qalmır, çünki insanların psixoloji yardıma ehtiyacı heç vaxt bitmir.</p>""",
        "sources": """          <p><a href="https://www.who.int/news-room/fact-sheets/detail/mental-health-strengthening-our-response" target="_blank" rel="noopener">WHO — Mental Health Strengthening</a></p>
          <p><a href="https://www.apa.org/career-guide/" target="_blank" rel="noopener">APA — Psychology Career Guide</a></p>
          <p>Wampold, B. E. (2015). How important are the common factors in psychotherapy? <em>World Psychiatry</em>, 14(3), 270-277.</p>
          <p>Norcross, J. C., & VandenBos, G. R. (2018). <em>Leaving It at the Office: A Guide to Psychotherapist Self-Care</em>. Guilford Press.</p>"""
    },
    {
        "slug": "blog-psixolog-olmaq-2.html",
        "badge": "PSIXOLOQLAR ÜÇÜN",
        "title": "Klinik vs Ümumi Psixologiya — Fərq və Seçim",
        "desc": "Klinik və ümumi psixologiyanın fərqi, hansı yolu seçmək lazım və hansı təhsil tələb olunur.",
        "read_time": 8,
        "cover": "images/blog/psixoloq-olmaq/art2-cover.jpg",
        "cover_alt": "Kitablar və tədqiqat",
        "cta_h": "Hansı yolu seçəcəyinizi bilmirsiniz?",
        "cta_sub": "Konsultasiyaya yazılın — birlikdə müəyyənləşdirək",
        "cta_link": "tehsil.html",
        "cta_link_text": "Təhsil Proqramları",
        "short": "Klinik və ümumi psixologiyanın əsas fərqləri, kim hansı yolu seçməlidir.",
        "cat": "Psixoloqlar üçün",
        "body": """          <p>Psixologiya təhsilinə girməyə qərar vermisiniz. Növbəti sual: "Klinik psixologiya, yoxsa ümumi?" Bu seçim karyera trayektoriyasını, gündəlik işin mahiyyətini, hətta gəlir səviyyəsini formalaşdırır. Bu məqalədə əsas fərqlər və düzgün seçim kriteriyaları.</p>

          <h2>Ümumi Psixologiya — Geniş Baxış</h2>
          <p>Ümumi psixologiya bütün insan davranış və zehni proseslərini öyrənir:</p>
          <ul>
            <li>Koqnitiv psixologiya (yaddaş, diqqət, dil)</li>
            <li>Sosial psixologiya (qrup davranışı, münasibətlər)</li>
            <li>İnkişaf psixologiyası (uşaqlıq, yetkinlik, qocalıq)</li>
            <li>Sənaye-təşkilat psixologiyası</li>
            <li>Təhsil psixologiyası</li>
            <li>İdman psixologiyası</li>
          </ul>

          <p><strong>Ümumi psixoloq nə edir?</strong> Tədqiqat, tədris, məsləhət (klinik olmayan), HR, marketinq, məktəb, idman psixoloqu.</p>

          <p><strong>İş sahələri:</strong></p>
          <ul>
            <li>Universitet (akademik tədqiqat)</li>
            <li>Korporativ sektor (HR, təlim, marketinq tədqiqatı)</li>
            <li>Məktəb psixoloqu</li>
            <li>İctimai sektorda təşkilatlar (UNICEF, WHO)</li>
            <li>Sertifikatlı testlərdən istifadə edən qiymətləndirmə</li>
          </ul>

          <h2>Klinik Psixologiya — Tibbi Sahə</h2>
          <p>Klinik psixologiya psixoloji pozğunluqları (depressiya, narahatlıq, PTSB, psixoz, asılılıq) qiymətləndirir, diaqnostika edir və psixoterapiya ilə müalicə edir.</p>

          <p><strong>Klinik psixoloq nə edir?</strong></p>
          <ul>
            <li>Klinik müsahibə və qiymətləndirmə</li>
            <li>Standardlaşdırılmış testlər (MMPI, Rorschach, Beck Depression)</li>
            <li>Diaqnoz qoyma (DSM-5, ICD-11)</li>
            <li>Psixoterapiya (KDT, gestalt, sistem terapiya, EMDR)</li>
            <li>Krizis müdaxiləsi</li>
            <li>Multidisiplinar komandada iş (psixiatr, sosial işçi, pediatr)</li>
          </ul>

          <p><strong>İş sahələri:</strong></p>
          <ul>
            <li>Özəl praktika</li>
            <li>Psixiatrik klinika və xəstəxana</li>
            <li>Reabilitasiya mərkəzləri</li>
            <li>Hərbi və veteran qulluqları</li>
            <li>Forensik psixologiya (məhkəmə)</li>
            <li>Onkologiya, paliyativ qulluq</li>
          </ul>

          <h2>Əsas Fərqlər</h2>
          <table style="width:100%; border-collapse:collapse; margin:24px 0;">
            <tr style="background:rgba(181,155,114,0.08);"><th style="padding:12px; text-align:left; border:1px solid var(--clr-border);">Element</th><th style="padding:12px; text-align:left; border:1px solid var(--clr-border);">Ümumi</th><th style="padding:12px; text-align:left; border:1px solid var(--clr-border);">Klinik</th></tr>
            <tr><td style="padding:12px; border:1px solid var(--clr-border);"><strong>Fokus</strong></td><td style="padding:12px; border:1px solid var(--clr-border);">Tipik insan davranışı</td><td style="padding:12px; border:1px solid var(--clr-border);">Psixoloji pozğunluqlar</td></tr>
            <tr><td style="padding:12px; border:1px solid var(--clr-border);"><strong>Müştəri</strong></td><td style="padding:12px; border:1px solid var(--clr-border);">Sağlam əhali</td><td style="padding:12px; border:1px solid var(--clr-border);">Klinik vəziyyəti olan pasiyentlər</td></tr>
            <tr><td style="padding:12px; border:1px solid var(--clr-border);"><strong>Diaqnoz</strong></td><td style="padding:12px; border:1px solid var(--clr-border);">Yox</td><td style="padding:12px; border:1px solid var(--clr-border);">Bəli (DSM-5)</td></tr>
            <tr><td style="padding:12px; border:1px solid var(--clr-border);"><strong>Tibbi mühit</strong></td><td style="padding:12px; border:1px solid var(--clr-border);">Az</td><td style="padding:12px; border:1px solid var(--clr-border);">Çox</td></tr>
            <tr><td style="padding:12px; border:1px solid var(--clr-border);"><strong>Təhsil müddəti</strong></td><td style="padding:12px; border:1px solid var(--clr-border);">4-6 il</td><td style="padding:12px; border:1px solid var(--clr-border);">6-8 il</td></tr>
            <tr><td style="padding:12px; border:1px solid var(--clr-border);"><strong>Gəlir</strong></td><td style="padding:12px; border:1px solid var(--clr-border);">Sektor-dependent</td><td style="padding:12px; border:1px solid var(--clr-border);">Adətən daha yüksək</td></tr>
          </table>

          <h2>Hansını Seçməli?</h2>

          <p><strong>Ümumi psixologiya uyğundur, əgər:</strong></p>
          <ul>
            <li>Akademik tədqiqat sevirsiniz</li>
            <li>Korporativ sektor maraqlıdır</li>
            <li>Sağlam insanlarla işləməyə üstünlük verirsiniz</li>
            <li>Pedaqogika maraqlandırır</li>
            <li>Tibbi mühitdə (xəstəxana) işləməyi sevmirsiniz</li>
          </ul>

          <p><strong>Klinik psixologiya uyğundur, əgər:</strong></p>
          <ul>
            <li>Pasiyentlərlə dərin işləmək istəyirsiniz</li>
            <li>Psixoloji pozğunluqlar maraqlıdır</li>
            <li>Tibbi mühitdə işləməyə hazırsınız</li>
            <li>Psixoterapiya əsas işiniz olsun istəyirsiniz</li>
            <li>Daha intensiv emosional yük qəbul edə bilirsiniz</li>
          </ul>

          <h2>Hibrid Yol</h2>
          <p>Bəzi peşəkarlar həm ümumi, həm klinik təhsil alırlar. Bu daha geniş karyera fürsətləri verir, lakin daha çox vaxt və maliyyə sərmayəsi tələb edir.</p>

          <p>RAGIMOFF-da bu hibrid yanaşma mümkündür: <strong>Ümumi Psixologiya</strong> bazis təhsili + sonra <strong>Klinik Psixologiya DPO</strong> əlavə təhsili. İki diplomla bütün karyera yolları açıqdır.</p>""",
        "sources": """          <p><a href="https://www.apa.org/topics/psychology-careers" target="_blank" rel="noopener">APA — Psychology Career Information</a></p>
          <p><a href="https://www.bps.org.uk/" target="_blank" rel="noopener">BPS — British Psychological Society</a></p>
          <p>Plante, T. G. (2010). <em>Contemporary Clinical Psychology</em> (3rd ed.). Wiley.</p>
          <p>Sternberg, R. J. (2017). <em>Career Paths in Psychology</em>. APA Books.</p>"""
    },
    {
        "slug": "blog-psixolog-olmaq-3.html",
        "badge": "PSIXOLOQLAR ÜÇÜN",
        "title": "Yeni Psixoloq Üçün İlk Müştəri Necə Alınır?",
        "desc": "Universitetdən sonra psixoloji praktika başlatmaq üçün marketinq, networking və ilk addımlar.",
        "read_time": 9,
        "cover": "images/blog/psixoloq-olmaq/art3-cover.jpg",
        "cover_alt": "İş masası və qeyd dəftəri",
        "cta_h": "Praktikadan başlamağa hazırsınız?",
        "cta_sub": "Praktikum və supervizyon proqramı sizi işə hazırlayır",
        "cta_link": "program-praktikum.html",
        "cta_link_text": "Praktikum Proqramı",
        "short": "Universitetdən sonra ilk müştəriləri tapmaq — networking, marketinq və ilk addımlar.",
        "cat": "Psixoloqlar üçün",
        "body": """          <p>Diplom alındı, sertifikat var, ofis kirayələnib — lakin müştəri yoxdur. Bu — yeni psixoloqun ən tipik problemidir. Tədqiqatlar göstərir ki, <strong>yeni psixoloqun ilk il ərzində orta hesabla 8-15 müştərisi olur</strong> — bu kifayət gəlir vermir. İlk 100 müştərini necə tapmaq?</p>

          <h2>Bazis Hazırlıq</h2>
          <p>Müştəri tapmaqdan əvvəl bunlar olmalıdır:</p>
          <ul>
            <li><strong>İxtisaslaşma sahəsi</strong> — "psixologiya" çox geniş. "Cütlük münaqişələri", "yeniyetmə anksiyetesi" — daha aydın</li>
            <li><strong>Açıq tarif</strong> — şəffaf qiymət (saatlıq və paket)</li>
            <li><strong>Etik kodeks tanıma</strong> — APA və ya yerli birlik</li>
            <li><strong>Sığorta</strong> — peşəkar məsuliyyət sığortası</li>
            <li><strong>Süpervizor müqaviləsi</strong> — ilk 100-200 saat üçün</li>
          </ul>

          <h2>Strategiya 1: Networking</h2>
          <p>Tədqiqatlar göstərib ki, yeni psixoloqun ilk müştərilərinin <strong>60-70%-i şəxsi tövsiyələrlə</strong> gəlir. Networking strategiyaları:</p>

          <p><strong>1. Tibbi peşəkarlarla əlaqə.</strong> Pediatr, ginekoloq, ailə həkimi — onların pasiyentləri tez-tez psixoloji yardıma ehtiyacı duyur. Onlara peşəkar profilinizi təqdim edin, vizit kartları buraxın.</p>

          <p><strong>2. Digər psixoloqlarla əlaqə.</strong> Təcrübəli kolleqalar tez-tez "vaxtım yoxdur" və ya "öz ixtisasım deyil" mənada müştəriləri başqalarına yönləndirirlər. Sizi onların radarında tutmaq vacibdir.</p>

          <p><strong>3. Sosial işçilər və müəllimlər.</strong> Onlar uşaqlardakı problemləri ilk görənlərdir, valideynlərə tez-tez psixoloq tövsiyə edirlər.</p>

          <p><strong>4. Konfranslar və seminarlar.</strong> Sahənin liderləri və kolleqalarla şəxsi əlaqə qurmaq imkanı.</p>

          <h2>Strategiya 2: Onlayn Görünürlük</h2>

          <p><strong>1. Peşəkar Veb-sayt.</strong> Sadə, peşəkar görünüşlü, mobil cihaz uyğun. Daxil olmalıdır:</p>
          <ul>
            <li>Sizin haqqınızda (tarixçə, təhsil, yanaşma)</li>
            <li>İxtisaslaşma sahələri</li>
            <li>Tariflər (şəffaflıq vacibdir)</li>
            <li>Görüş bron formu</li>
            <li>Blog (haftada 1 məqalə — SEO üçün)</li>
            <li>Pasiyent rəyləri (icazə alındıqdan sonra, anonim)</li>
          </ul>

          <p><strong>2. Sosial Media — İxtiyatlı.</strong> Instagram, LinkedIn, hətta TikTok — bilik paylaşmaq mümkündür. Lakin etika qaydalarına ehtiyatlı yanaşma:</p>
          <ul>
            <li>Müştəri detalları paylaşmamaq</li>
            <li>Ümumi məlumat və savadlılıq</li>
            <li>Konkret diaqnoz "məsləhəti" verməmək</li>
            <li>Peşəkar tonu saxlamaq</li>
          </ul>

          <p><strong>3. Yandex/Google psixoloq kataloqları.</strong> Pasiyentlər tez-tez "Bakıda yaxşı psixoloq" axtarırlar. Bu kataloqlarda peşəkar profilinizi yerləşdirin.</p>

          <h2>Strategiya 3: Pulsuz Dəyər Yaratmaq</h2>

          <p><strong>1. Pulsuz Vebinarlar.</strong> Konkret mövzuda 1 saatlıq webinar. "Yeniyetmə ilə kommunikasiya", "İlk panik atak nə etmək" və s. Pulsuz dəyər müştəri etibar yaradır.</p>

          <p><strong>2. Pulsuz İlk Konsultasiya (15-30 dəq).</strong> "Tanış olma" görüşü — pasiyent sizinlə uyğun olub-olmadığını, siz problemin sizin ixtisasınız olub-olmadığını qiymətləndirir. Konversiya nisbəti yüksəkdir.</p>

          <p><strong>3. Bloqlama.</strong> Hər ay 4-8 məqalə. "Stress idarəsi", "münasibətlər", "uşaq tərbiyəsi". Google və Yandex sizi tapmağa kömək edir.</p>

          <p><strong>4. YouTube/TikTok Videolar.</strong> Qısa, faydalı videolar. Pasiyentlər sizin sifətinizi və danışıq tərzinizi görüb daha rahat müraciət edirlər.</p>

          <h2>Strategiya 4: Korporativ Müştərilər</h2>
          <p>Yeni psixoloq üçün şirkətlər ilə əməkdaşlıq sürətli müştəri axını verir:</p>
          <ul>
            <li>EAP (Employee Assistance Programs) — şirkətin əməkdaşlarına psixoloji yardım</li>
            <li>Korporativ vebinarlar (stress idarəsi, kommunikasiya)</li>
            <li>HR departamentlərinə təlim</li>
            <li>Aqressiv işləyən komandalarla iş</li>
          </ul>

          <h2>Birinci 6 Ay Üçün Realistik Plan</h2>
          <ol>
            <li>Veb-sayt + sosial media profillər (1 ay)</li>
            <li>Sertifikatlı supervizor ilə müqavilə (1 ay)</li>
            <li>Tibbi peşəkarlarla 20 görüş (3 ay)</li>
            <li>Aylıq 1-2 pulsuz vebinar (davamlı)</li>
            <li>Aylıq 4 məqalə bloga (davamlı)</li>
            <li>Pulsuz ilk konsultasiya təklif (davamlı)</li>
            <li>İlk 10 müştəri — şəxsi tövsiyələrlə (gözlənti)</li>
            <li>İlk 30 müştəri — onlayn marketinglə (gözlənti)</li>
          </ol>

          <h2>Maliyyə Realizmi</h2>
          <p>İlk il çətindir. Plan:</p>
          <ul>
            <li>3-6 ay digər gəlir mənbəyi saxlayın (yarı ştat, tədris)</li>
            <li>Praktikadan əldə olunan ilk gəliri biznesə yenidən investisiya edin (sığorta, sayt, kurs, supervizor)</li>
            <li>İl sonu profitabel olmağı gözləməyin — bu marafondur, sprint deyil</li>
          </ul>

          <p>Yeni psixoloqun "ilk müştəri" çətinliyi normaldır. Strateji yanaşma, peşəkar inkişaf, və əsl müştəri xidməti — 1-2 il ərzində praktikanı sabit qurur.</p>""",
        "sources": """          <p><a href="https://www.apa.org/practice/management" target="_blank" rel="noopener">APA — Practice Management</a></p>
          <p>Walfish, S., & Barnett, J. E. (2009). <em>Financial Success in Mental Health Practice</em>. APA.</p>
          <p>Crawford, S. F. (2018). <em>Psychotherapist's Guide to Marketing</em>. Routledge.</p>
          <p>Wedding, D., & Niemiec, R. M. (2015). The clinical use of cinema. <em>Cinema Therapy</em>, 25-46.</p>"""
    },
    {
        "slug": "blog-psixolog-olmaq-4.html",
        "badge": "PSIXOLOQLAR ÜÇÜN",
        "title": "Süpervizyon — Psixoloqun Davamlı Müəllimi",
        "desc": "Süpervizyon nədir, kim üçün vacibdir, necə düzgün süpervizor seçmək.",
        "read_time": 7,
        "cover": "images/blog/psixoloq-olmaq/art4-cover.jpg",
        "cover_alt": "İki kolleqa danışır",
        "cta_h": "Süpervizyon proqramı?",
        "cta_sub": "Beynəlxalq sertifikatlı supervizorlarla iş",
        "cta_link": "program-praktikum.html",
        "cta_link_text": "Praktikum Proqramı",
        "short": "Süpervizyon — peşəkar inkişafın əsas alətindir. Necə işləyir, kim üçün vacibdir.",
        "cat": "Psixoloqlar üçün",
        "body": """          <p>"Mən təhsilimi bitirdim, sertifikat aldım — niyə hələ də nəyəsə öyrətmək lazımdır?" — yeni psixoloqların tipik sualı. Cavab: psixoloji praktikada <strong>süpervizyon — bütün peşəkar inkişafın bel sütunudur</strong>. APA və beynəlxalq birliklərə görə, sertifikatlı süpervizor olmadan klinik praktika qeyri-etikidir.</p>

          <h2>Süpervizyon Nədir?</h2>
          <p>Süpervizyon (supervision) — təcrübəli psixoloqun gənc kolleqasının klinik işini sistemli şəkildə nəzərdən keçirməsi və istiqamətləndirməsi prosesidir.</p>

          <p>Süpervizyonun məqsədləri:</p>
          <ul>
            <li><strong>Müştəri qoruması</strong> — pasiyent yanlış müdaxilədən qorunur</li>
            <li><strong>Peşəkar inkişaf</strong> — supervisi öz iş bacarığını qiymətləndirir və artırır</li>
            <li><strong>Etik dəstək</strong> — çətin etik qərarlarda yardım</li>
            <li><strong>Emosional yük idarəsi</strong> — pasiyent travmalarının özünüzə təsirini idarə</li>
            <li><strong>Akkreditasiya</strong> — bir çox sertifikat və lisenziya saatları tələb edir</li>
          </ul>

          <h2>İndividual vs Qrup Süpervizyonu</h2>

          <p><strong>İndividual süpervizyon (1:1):</strong></p>
          <ul>
            <li>Sayda az hadisəyə dərin baxış</li>
            <li>Şəxsi triggerlərlə işləmək imkanı</li>
            <li>Konfidensial mühit</li>
            <li>Tipik: 1 saat həftədə</li>
            <li>Tarif: 50-150 AZN/saat</li>
          </ul>

          <p><strong>Qrup süpervizyonu:</strong></p>
          <ul>
            <li>Daha çox hadisə, müxtəlif perspektivlər</li>
            <li>Kolleqalardan öyrənmək imkanı</li>
            <li>Daha çox sayda problem</li>
            <li>Tipik: 2-3 saat həftədə, 4-8 nəfər</li>
            <li>Tarif: 30-80 AZN/seans</li>
          </ul>

          <p>Optimal: hər ikisinin kombinasiyası. Həftədə 1 dəfə qrup + ayda 1 dəfə individual.</p>

          <h2>Necə Süpervizor Seçmək?</h2>

          <p><strong>1. Sertifikatlaşma.</strong> Süpervizor olmaq üçün:</p>
          <ul>
            <li>Klinik psixoloji və ya psixiatrik təhsil</li>
            <li>10+ il klinik təcrübə</li>
            <li>Süpervizor sertifikatı (xüsusi proqramdan keçmiş)</li>
            <li>Davamlı supervisi-supervizor münasibətdə öz təcrübəsi olan</li>
          </ul>

          <p><strong>2. İxtisaslaşma uyğunluğu.</strong> Sizin əsas işiniz hansıdır? Cütlük terapiyası işləyirsinizsə, ümumi psixiatr supervizoru tam uyğun deyil. İdeallıq: eyni və ya yaxın sahədə olan supervizor.</p>

          <p><strong>3. Yaxınlaşma uyğunluğu.</strong> KDT istifadə edirsinizsə, psixoanalitik supervizor məhdud kömək verə bilər. Eyni və ya tamamlayıcı yanaşmalı supervizor seçin.</p>

          <p><strong>4. Şəxsi uyğunluq.</strong> Süpervizor sizi qorxutmamalı, lakin çağırış da etməlidir. İlk 1-2 görüşdə "bu adamla iş asan oldumu" qiymətləndirin.</p>

          <p><strong>5. Coğrafi və maliyyə baxımdan əldə edilən.</strong> Online süpervizyon mümkündür və geniş yayılmışdır.</p>

          <h2>Süpervizyon Nə Vaxt Tələb Olunur?</h2>
          <ul>
            <li><strong>İlk 100-200 saat müştəri işi</strong> — beynəlxalq standart</li>
            <li><strong>Yeni klinik sahə öyrənmə</strong> — məsələn, uşaq psixologiyasından travma terapiyasına keçid</li>
            <li><strong>Çətin müştəri</strong> — özünü zədələyən, intihar düşüncəli, sərhəd pozğunluğu</li>
            <li><strong>Etik dilemmalar</strong> — gizlilik, ikili münasibətlər</li>
            <li><strong>Burnout simptomları</strong> — özünüzü qoruma üçün</li>
          </ul>

          <h2>Süpervizyon Seansında Nə Olur?</h2>
          <ol>
            <li>Konkret hadisənin təqdimatı (5-10 dəq)</li>
            <li>Çətinlik və sual ifadəsi (5 dəq)</li>
            <li>Süpervizorun reflektiv sualları (10-15 dəq)</li>
            <li>Alternativ yanaşmalar müzakirəsi (15-20 dəq)</li>
            <li>Özünüqavrayış üzərində iş — "bu hadisədə özünüzdə nə oyandı?" (10 dəq)</li>
            <li>Növbəti seansa hazırlıq planı (5 dəq)</li>
          </ol>

          <h2>"Pis" Süpervizyon Əlamətləri</h2>
          <ul>
            <li>Süpervizor "necə doğru" kateqorik deyir, alternativlər müzakirə etmir</li>
            <li>Süpervisinin emosional yükünə diqqət yox</li>
            <li>Etik məsələlər atlanır</li>
            <li>Şəxsi məsləhət və ya terapiya formasına çevrilir</li>
            <li>İkili münasibətlər (məsələn, supervizor sizin özünüzün də terapevtidir)</li>
          </ul>

          <h2>Yekun</h2>
          <p>Süpervizyon — peşəkar psixoloqun seçim deyil, məcburi praktika. Ən təcrübəli psixoloqlar belə həyatları boyu süpervizyonu davam etdirirlər. Pasiyentlər üçün, peşənin keyfiyyəti üçün, və supervisi-psixoloqun şəxsi sağlamlığı üçün — bu prosesin əhəmiyyəti həddən artıq qiymətləndirilməyəcək.</p>""",
        "sources": """          <p><a href="https://www.apa.org/about/policy/guidelines-supervision.pdf" target="_blank" rel="noopener">APA — Guidelines for Clinical Supervision</a></p>
          <p>Bernard, J. M., & Goodyear, R. K. (2018). <em>Fundamentals of Clinical Supervision</em> (6th ed.). Pearson.</p>
          <p>Falender, C. A., & Shafranske, E. P. (2017). <em>Supervision Essentials for the Practice of Competency-Based Supervision</em>. APA.</p>
          <p>Hewson, J. (1999). Training supervisors to use a supervisory framework. <em>The Clinical Supervisor</em>, 18(2), 67-78.</p>"""
    },
    {
        "slug": "blog-psixolog-olmaq-5.html",
        "badge": "PSIXOLOQLAR ÜÇÜN",
        "title": "Psixoloqun Özünüqayğısı — Burnoutdan Qorunma",
        "desc": "Psixoloji peşədə tükənmə yüksəkdir. Özünüqayğı strategiyaları və profilaktik tədbirlər.",
        "read_time": 8,
        "cover": "images/blog/psixoloq-olmaq/art5-cover.jpg",
        "cover_alt": "Yorğun mütəxəssis",
        "cta_h": "Peşəkar dəstəyə ehtiyac?",
        "cta_sub": "Özünüqayğı və supervizyon proqramı",
        "cta_link": "tehsil.html",
        "cta_link_text": "Təhsil Proqramları",
        "short": "Psixoloji peşədə burnout — yüksək risk. Özünüqayğı və profilaktik tədbirlər.",
        "cat": "Psixoloqlar üçün",
        "body": """          <p>"Müştərilərimə kömək etmək istəyirəm, lakin özüm yorulmuşam" — psixoloqların ən tez-tez səs vermədiyi cümlədir. Tədqiqatlar göstərir ki, <strong>psixoloji peşədə burnout 40-60% mütəxəssisdə müşahidə olunur</strong> (Lim et al., 2010). Bu sadə yorğunluq deyil — ciddi peşəkar və şəxsi risk.</p>

          <h2>Burnout Nədir?</h2>
          <p>Burnout (Maslach modeli, 1981) üç komponentdən ibarətdir:</p>
          <ul>
            <li><strong>Emosional tükənmə</strong> — "boşalmış" hissi</li>
            <li><strong>Depersonalizasiya</strong> — müştərilərə qarşı sinik münasibət, "obyektləşdirmə"</li>
            <li><strong>Şəxsi nailiyyət hissinin azalması</strong> — "mən kömək etmirəm"</li>
          </ul>

          <p>İlk simptomlar tez-tez gözardı edilir: yorğunluq, qıcıqlanma, sosial geriçəkilmə. Aylar sonra — depressiya, anksiyete, fiziki simptomlar (başağrısı, mədə-bağırsaq, yuxu pozğunluğu).</p>

          <h2>Psixoloqlarda Niyə Risk Yüksəkdir?</h2>
          <ul>
            <li><strong>Vicarious traumatization</strong> — pasiyentin travmasını "udmaq"</li>
            <li><strong>Emosional əmək</strong> — daimi empati ödəmə</li>
            <li><strong>Sərhəd qoyma çətinliyi</strong> — "kömək etmək" yardımdan asılı olmağa çevrilir</li>
            <li><strong>İzolyasiya</strong> — pasiyent detalları kolleqalarla paylaşa bilmirsiniz</li>
            <li><strong>Bilinməz nəticələr</strong> — terapiyanın effekti illər sonra görünə bilər</li>
            <li><strong>Yüksək məsuliyyət</strong> — pasiyent intihar və ya travma riskinin daimi yüklənməsi</li>
          </ul>

          <h2>Erkən Xəbərdarlıq Siqnalları</h2>
          <ul>
            <li>Pasiyentlərə qarşı qıcıqlanma</li>
            <li>Bəzi seansları "lazımsız" hesab etmə</li>
            <li>Pasiyent zəng və mesajlarına cavab gecikdirilməsi</li>
            <li>Seans öncəsi və sonrası əhəmiyyətli yorğunluq</li>
            <li>Şəxsi həyatda izolyasiya</li>
            <li>Yuxu pozğunluğu, qabuslar pasiyent mövzularında</li>
            <li>Alkoqol, qida və ya başqa maddə istifadəsinin artması</li>
            <li>Süpervizyona getmək istəməmək</li>
          </ul>

          <p>Bu siqnalların 3-4-ü varsa — peşəkar müdaxilə tələb olunur.</p>

          <h2>Özünüqayğı Strategiyaları</h2>

          <p><strong>1. Strukturlaşdırılmış Sərhədlər.</strong></p>
          <ul>
            <li>Maksimum gündəlik müştəri sayı (5-6 yetkin və ya 8 uşaq)</li>
            <li>Seanslar arasında 15 dəq pauza (sıxılma çıxışı)</li>
            <li>İş saatlarından sonra mesaj cavab verməmək</li>
            <li>Həftəsonu — pasiyent yox</li>
            <li>İllik məzuniyyət — minimum 4 həftə</li>
          </ul>

          <p><strong>2. Müntəzəm Süpervizyon.</strong> Bunu yuxarıda təsvir etdik. Süpervizyon emosional yük idarəsinin əsas alətidir.</p>

          <p><strong>3. Şəxsi Terapiya.</strong> Hər psixoloq özü də terapiyada olmalıdır — ən azı dövri olaraq. Bu hem peşəkar inkişaf, hem özünüqayğıdır.</p>

          <p><strong>4. Fiziki Sağlamlıq.</strong></p>
          <ul>
            <li>Müntəzəm məşq (həftədə 3-5 dəfə)</li>
            <li>Yuxu gigiyenası (7-9 saat)</li>
            <li>Sağlam qida</li>
            <li>Müntəzəm tibbi yoxlama</li>
          </ul>

          <p><strong>5. Mindfulness və Meditasiya.</strong> Tədqiqatlar göstərib ki, müntəzəm meditasiya psixoloqlarda burnout riskini 40%-ə qədər azaldır (Goodman & Schorling, 2012). Gündə 10-20 dəqiqə kifayətdir.</p>

          <p><strong>6. Sosial Dəstək.</strong> Peşəkar olmayan dostlar, ailə əlaqəsi, hobbi qruplar. İş xaricində kim olduğunuzu xatırlamaq.</p>

          <p><strong>7. Professional Dəstək Qrupları.</strong> Peer consultation qrupları, kolleqalarla peşəkar mövzularda söhbət (gizlilik saxlanılmaqla).</p>

          <p><strong>8. Pasiyent Tipini Şaxələndirmək.</strong> Yalnız travma və ya yalnız depressiya pasiyentlər ilə işləmək — burnoutu sürətləndirir. Müxtəliflik vacibdir.</p>

          <h2>Vicarious Traumatization (VT)</h2>
          <p>VT — pasiyent travmasının tədricən psixoloqun öz dünyagörüşünü dəyişdirməsidir. Simptomlar:</p>
          <ul>
            <li>Dünyaya qarşı pessimizm</li>
            <li>İnsanlara qarşı güvənsizlik</li>
            <li>Şəxsi həyatda intim əlaqədə çətinlik</li>
            <li>Pasiyent mövzularında qabuslar</li>
            <li>Yüksək riskli vəziyyətlərdə hipersensitivlik</li>
          </ul>

          <p>VT — burnout-dan fərqlidir, lakin tez-tez birlikdə baş verir. Travma ilə işləyən mütəxəssislər üçün xüsusi risk.</p>

          <h2>Praktik 30-Günlük Plan</h2>
          <ol>
            <li><strong>Gün 1-7:</strong> Burnout qiymətləndirmə (Maslach Burnout Inventory online)</li>
            <li><strong>Gün 8-14:</strong> Sərhədləri qurmaq (gündəlik müştəri limiti, mesaj saatları)</li>
            <li><strong>Gün 15-21:</strong> Müntəzəm süpervizyon və ya peer consultation qoşulmaq</li>
            <li><strong>Gün 22-30:</strong> Fiziki sağlamlıq və mindfulness rejiminin başlaması</li>
          </ol>

          <h2>Vacib Mesaj</h2>
          <p>Özünüqayğı — eqoizm deyil. Əksinə: <strong>burnout-da olan psixoloq pasiyentlərinə zərər verir</strong>. Etik baxımdan özünüqayğı pasiyentinin haqqıdır.</p>

          <p>"Müştəri qədər özümə də qayğı göstərirəm" — bu cümlə peşəkar psixoloqun başlıca prinsipi olmalıdır.</p>""",
        "sources": """          <p><a href="https://www.apa.org/topics/burnout" target="_blank" rel="noopener">APA — Burnout in Psychology Practice</a></p>
          <p>Maslach, C., Schaufeli, W. B., & Leiter, M. P. (2001). Job burnout. <em>Annual Review of Psychology</em>, 52, 397-422.</p>
          <p>Lim, N., et al. (2010). Stress and burnout in clinical psychologists. <em>Psychotherapy Research</em>, 20(6), 717-731.</p>
          <p>Norcross, J. C., & VandenBos, G. R. (2018). <em>Leaving It at the Office: A Guide to Psychotherapist Self-Care</em>. Guilford.</p>"""
    }
]

ALL_ARTS = DEPRESSIYA + PSIXOLOQ

for art in ALL_ARTS:
    out = CHROME
    # Related: choose 3 from same category if possible, else mix
    if art in DEPRESSIYA:
        pool = DEPRESSIYA
    else:
        pool = PSIXOLOQ
    others = [a for a in pool if a["slug"] != art["slug"]][:3]
    related = "\n".join(CARD.format(slug=o["slug"], cat=o["cat"], title=o["title"], excerpt=o["short"]) for o in others)
    af = dict(art); af["related"] = related
    for k, v in af.items():
        out = out.replace("{" + k + "}", str(v))
    (ROOT / art["slug"]).write_text(out, encoding="utf-8")
    print(f"WROTE: {art['slug']}")
print("Done.")
