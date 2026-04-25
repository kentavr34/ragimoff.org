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
      .triangle-box { background:rgba(181,155,114,0.06); border:1px solid var(--clr-border); border-left:3px solid var(--accent); padding:20px 24px; margin:24px 0; }
      @media (max-width:768px) { .art-fig { margin:28px 0; } .art-fig figcaption { padding:0; } }
    </style>
  </head>
  <body>
    <header class="site-header">
      <div class="header-inner">
        <a href="index.html" class="logo-box">
          <span class="logo-text">RAGIMOFF<em>.</em></span>
          <span class="logo-sub">Psixologiya Məktəbi</span>
        </a>
        <nav class="desktop-nav">
          <a href="index.html">Ana Səhifə</a>
          <a href="tehsil.html">Təhsil</a>
          <a href="xidmetler.html">Konsultasiya</a>
          <a href="b2b.html">Korporativ</a>
          <a href="blog.html" class="nav-active">Blog</a>
          <a href="tehsil.html#registration" class="nav-cta">Qeydiyyat</a>
        </nav>
        <button class="mobile-toggle" onclick="toggleMenu()" aria-label="Menu">
          <svg viewBox="0 0 24 24"><path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z" /></svg>
        </button>
      </div>
    </header>
    <nav class="mobile-nav" id="mobileNav" role="navigation" aria-label="Mobil menyu">
      <button class="mobile-nav-close" onclick="toggleMenu()">
        <svg viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" /></svg>
      </button>
      <a href="index.html" onclick="toggleMenu()">Ana Səhifə</a>
      <a href="tehsil.html" onclick="toggleMenu()">Təhsil</a>
      <a href="xidmetler.html" onclick="toggleMenu()">Konsultasiya</a>
      <a href="b2b.html" onclick="toggleMenu()">Korporativ</a>
      <a href="blog.html" onclick="toggleMenu()">Blog</a>
      <a href="tehsil.html#registration" class="btn btn-fill" onclick="toggleMenu()">Qeydiyyat</a>
    </nav>

    <section class="pg-hero pg-hero-plain" data-theme="dark">
      <div class="pg-hero-inner">
        <span class="badge">KLİNİK</span>
        <h1 class="hero-h1">{title}</h1>
        <p class="hero-lead">Kənan Rəhimov · {read_time} dəq oxuma · 2026</p>
      </div>
    </section>

    <section data-theme="light">
      <div class="sec-inner" style="padding:var(--s-section); max-width:760px; text-align:left">
        <img src="{cover}" alt="{cover_alt}" class="art-cover" loading="lazy" />
        <div class="article-body">
{body}
        </div>

        <div class="author-block" style="margin-top:48px">
          <div>
            <strong>Kənan Rəhimov</strong>
            <p style="color:var(--clr-text-muted); font-size:.9rem; margin:4px 0 0">Həkim-Psixiatr, Psixoterapevt. 23 il klinik təcrübə.</p>
          </div>
        </div>

        <div class="art-sources">
          <strong>Mənbələr:</strong>
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
        <h2 class="sec-h2">Sosial fobiya ilə yaşamaq məcburi deyil</h2>
        <p class="sec-sub">KDT və ekspozisiya terapiyası — sübut edilmiş yol</p>
        <div class="cta-band-btns">
          <a href="https://wa.me/994702200376" class="btn btn-fill" target="_blank">WhatsApp ilə Yazın</a>
          <a href="sosial-fobiya.html" class="btn btn-line">Sosial Fobiya</a>
        </div>
      </div>
    </div>

    <footer class="site-footer" data-theme="dark">
      <div class="footer-inner">
        <div class="footer-grid">
          <div>
            <a href="index.html" class="logo-box footer-logo">
              <span class="logo-text">RAGIMOFF<em>.</em></span>
              <span class="logo-sub">Psixologiya Məktəbi</span>
            </a>
            <p class="footer-desc">Kənan Rəhimov — Həkim-Psixiatr, Psixoterapevt. 23 il klinik təcrübə. Bakı, Azərbaycan.</p>
            <div class="social-links">
              <a href="https://t.me/ragimoff" target="_blank" class="social-btn">TG</a>
              <a href="https://www.facebook.com/Ragimoff.az" target="_blank" class="social-btn">FB</a>
              <a href="https://www.instagram.com/dr.ragimoff" target="_blank" class="social-btn">IG</a>
              <a href="https://youtube.com/@kragimoff" target="_blank" class="social-btn">YT</a>
            </div>
          </div>
          <div>
            <span class="footer-col-title">Terapiya</span>
            <ul class="footer-links">
              <li><a href="aile-terapiyasi.html" class="footer-link">Ailə Terapiyası</a></li>
              <li><a href="enurez.html" class="footer-link">Gecə Enurezi</a></li>
              <li><a href="panik-ataklar.html" class="footer-link">Panik Ataklar</a></li>
              <li><a href="depressiya.html" class="footer-link">Depressiya</a></li>
              <li><a href="sosial-fobiya.html" class="footer-link">Sosial Fobiya</a></li>
            </ul>
          </div>
          <div>
            <span class="footer-col-title">Təhsil</span>
            <ul class="footer-links">
              <li><a href="program-umumi.html" class="footer-link">Ümumi Psixologiya</a></li>
              <li><a href="program-klinik.html" class="footer-link">Klinik Psixologiya DPO</a></li>
              <li><a href="program-praktikum.html" class="footer-link">Psixoterapiya Praktikumu</a></li>
              <li><a href="blog.html" class="footer-link">Psixologiya Bloqu</a></li>
              <li><a href="https://youtube.com/@kragimoff" target="_blank" class="footer-link">YouTube Dərslər</a></li>
            </ul>
          </div>
          <div>
            <span class="footer-col-title">Əlaqə</span>
            <ul class="footer-links">
              <li><a href="tel:+994702200376" class="footer-link">(+994) 70-220-03-76</a></li>
              <li><a href="mailto:info@ragimoff.org" class="footer-link">info@ragimoff.org</a></li>
              <li><a href="https://wa.me/994702200376" class="footer-link">WhatsApp</a></li>
              <li><a href="https://t.me/dockenan" class="footer-link">Telegram</a></li>
              <li><a href="https://instagram.com/doctor.ragimoff" target="_blank" class="footer-link">Instagram</a></li>
            </ul>
          </div>
        </div>
        <div class="footer-bottom">
          <p>© 2026 RAGIMOFF Peşəkar Psixologiya Məktəbi. Peşəkar Nüfuzun Ünvanı.</p>
          <a href="https://www.psychotherapyru.com" target="_blank" class="footer-link">Русская версия</a>
        </div>
      </div>
    </footer>
    <a href="https://wa.me/994702200376" class="wa-float" target="_blank" aria-label="WhatsApp">
      <svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
    </a>
    <script src="shared.js"></script>
  </body>
</html>
"""

CARD = """          <a href="{slug}" class="blog-card" style="text-decoration:none">
            <div class="blog-card-body">
              <span class="blog-card-cat">Klinik</span>
              <h3 class="blog-card-title">{title}</h3>
              <p class="blog-card-excerpt">{excerpt}</p>
            </div>
          </a>"""

ARTS = [
    {
        "slug": "blog-sosial-fobiya.html",
        "title": "Sosial Fobiya — Sadəcə Utancaqlıq Deyil",
        "desc": "Utancaqlıq və sosial fobiya arasındakı klinik fərq. DSM-5 kriteriyaları və müalicə yolları.",
        "read_time": 8,
        "cover": "images/blog/sosial-fobiya/art1-cover.jpg",
        "cover_alt": "Pəncərə qarşısında düşünən",
        "short": "Utancaqlıq və sosial anksiyete arasındakı klinik fərq, DSM-5 kriteriyaları.",
        "body": """          <p>"Mən utancağam, hər kəsdə var, problem yoxdur" — sosial anksiyete pozğunluğundan əziyyət çəkənlərin tipik özünüqavrayışıdır. Lakin tədqiqatlar göstərir: <strong>insanların 12-15%-i həyatı boyu klinik sosial anksiyete pozğunluğundan əziyyət çəkir</strong> (NIMH, 2023). Bu — utancaqlıq deyil. Bu — müalicə olunan klinik vəziyyətdir.</p>

          <h2>Utancaqlıq vs Klinik Sosial Anksiyete</h2>

          <p>Sadə fərq: <strong>utancaqlıq həyatı məhdudlaşdırmır, sosial anksiyete məhdudlaşdırır</strong>.</p>

          <ul>
            <li><strong>Utancaq insan</strong> yeni adamla tanış olduqda 5-10 dəqiqə narahatlıq hiss edir, sonra rahatlaşır</li>
            <li><strong>Sosial anksiyetəli insan</strong> bir həftə əvvəldən narahat olur, 3 saat əvvəldən fiziki simptomlar yaşayır, hadisədən sonra 2-3 gün ona görə əzab çəkir</li>
            <li><strong>Utancaq insan</strong> kafeyə girəndə bir az diqqət edilməsindən rahatsızlaşır</li>
            <li><strong>Sosial anksiyetəli insan</strong> kafeyə girməkdən tamamilə imtina edir, ya yalnız konkret saatlarda, konkret yerlərə gedir</li>
          </ul>

          <h2>DSM-5 Klinik Kriteriyaları</h2>
          <p>Sosial Anksiyete Pozğunluğu (Sosial Fobiya) diaqnozu üçün:</p>
          <ul>
            <li><strong>A.</strong> Bir və ya bir neçə sosial vəziyyətdən kəskin qorxu (mühakimə edilmək, alçaldılmaq qorxusu)</li>
            <li><strong>B.</strong> Şəxs həmin vəziyyətdə narahatlıq simptomlarını göstərəcəyindən qorxur</li>
            <li><strong>C.</strong> Sosial vəziyyətlər həmişə qorxu yaradır</li>
            <li><strong>D.</strong> Vəziyyətlərdən qaçınılır və ya çox əzabla yaşanılır</li>
            <li><strong>E.</strong> Qorxu real təhlükə ilə proporsional deyil</li>
            <li><strong>F.</strong> Simptomlar 6 aydan çox davam edir</li>
            <li><strong>G.</strong> Klinik əhəmiyyətli pozulma yaranır (iş, sosial həyat, münasibətlər)</li>
          </ul>

          <h2>Tipik Sosial Vəziyyətlər</h2>
          <ul>
            <li>İctimai çıxış (prezentasiya, yığıncaqda söz alma)</li>
            <li>Naməlum adamla tanışlıq</li>
            <li>Telefon zəngləri</li>
            <li>Restoranda sifariş vermə</li>
            <li>Ofisdə yemək yemə (başqaları yanında)</li>
            <li>İctimai yerdə tualetdən istifadə</li>
            <li>Yığıncaqda görünmə (toy, doğum günü)</li>
            <li>Müəllimə sual vermə</li>
            <li>Otorid figura (rəhbər, müəllim) ilə danışma</li>
          </ul>

          <h2>Fiziki Simptomlar</h2>
          <p>Sosial anksiyete bədəndə güclü reaksiyalar yaradır:</p>
          <ul>
            <li><strong>Qızarma</strong> (ən tipik) — üzdə qan dövranı artımı</li>
            <li><strong>Tərləmə</strong> (xüsusən əllər, üz, qoltuq altı)</li>
            <li><strong>Titrəmə</strong> (səs, əllər)</li>
            <li><strong>Ürəkdöyüntüsü</strong></li>
            <li><strong>Nəfəs daralması</strong></li>
            <li><strong>Mədə-bağırsaq problemləri</strong> (ürəkbulanma, ishal)</li>
            <li><strong>Səs qırıqlığı, "boğazda yumru"</strong></li>
          </ul>

          <p>Trick: bu simptomlardan qorxmaq simptomları gücləndirir. "Qızararammı?" düşüncəsi qızarmanı tetikleyir.</p>

          <h2>Niyə Sosial Anksiyete Diaqnoz Qoyulmur?</h2>
          <p>Pasiyentlərin yalnız 1/4-i kömək axtarır. Səbəblər:</p>
          <ul>
            <li>"Hamı belədir, normaldır" — özünü vəziyyətə uyğunlaşdırma</li>
            <li>"Bir şeyim olmaz, sadəcə xarakterimdir"</li>
            <li>Psixoloqa getmək özü sosial vəziyyətdir — qorxulu</li>
            <li>"Mən zəifəm, kömək istəməyə utanıram"</li>
            <li>Mədəniyyətdə "kömək istəmək" zəiflik kimi qəbul olunur</li>
          </ul>

          <h2>Müalicə — Effektiv Var</h2>
          <p>Yaxşı xəbər: sosial anksiyete <strong>ən yaxşı müalicə olunan narahatlıq pozğunluqlarından biridir</strong>. KDT (Koqnitiv-Davranış Terapiyası) və ekspozisiya terapiyası 12-16 həftədə pasiyentlərin 70-80%-də əhəmiyyətli yaxşılaşma verir (NICE, 2013).</p>

          <p>Müalicə komponentləri:</p>
          <ol>
            <li>Psixoeğitim (vəziyyəti anlama)</li>
            <li>Düşüncə yenidən quruluşu (KDT)</li>
            <li>Tədricən ekspozisiya (qorxulu sosial vəziyyətlərə)</li>
            <li>Sosial bacarıq məşqi</li>
            <li>Bəzi hallarda — SSRI tipli dərmanlar (psixiatrın nəzarətində)</li>
          </ol>

          <h2>Əgər Bunu Tanıdınızsa...</h2>
          <p>Bu məqalədəki əlamətlərin 4-5-i sizdə varsa — bu xarakter qüsuru deyil, klinik vəziyyətdir. Müalicə oluna bilər. Birinci addım — psixoloq və ya psixiatra müraciət. İlk konsultasiya online da mümkündür — beləliklə birbaşa kabineti getməyin streseini azaltmaq mümkündür.</p>""",
        "sources": """          <p><a href="https://www.nimh.nih.gov/health/topics/social-anxiety-disorder-more-than-just-shyness" target="_blank" rel="noopener">NIMH — Social Anxiety Disorder: More Than Just Shyness</a></p>
          <p><a href="https://www.nice.org.uk/guidance/cg159" target="_blank" rel="noopener">NICE Guideline CG159 — Social Anxiety Disorder</a></p>
          <p>DSM-5: Social Anxiety Disorder (300.23), American Psychiatric Publishing, 2013.</p>
          <p>Hofmann, S. G. (2007). Cognitive factors that maintain social anxiety disorder. <em>Cognitive Behaviour Therapy</em>, 36(4), 193-209.</p>"""
    },
    {
        "slug": "blog-sosial-fobiya-2.html",
        "title": "İctimai Çıxış Qorxusu — KDT və Ekspozisiya",
        "desc": "Prezentasiya, yığıncaq, mikrofon qarşısında qorxu — Toastmasters və KDT əsaslı praktik plan.",
        "read_time": 8,
        "cover": "images/blog/sosial-fobiya/art2-cover.jpg",
        "cover_alt": "Mikrofon qarşısında",
        "short": "İctimai çıxış qorxusu (glossofobiya) — yayılmış sosial fobiya. KDT və ekspozisiya planı.",
        "body": """          <p>İctimai çıxış qorxusu (glossofobiya) — sosial anksiyetenin ən geniş yayılmış formasıdır. Tədqiqatlar (Stein & Stein, 2008) göstərir ki, dünyada insanların <strong>74%-i</strong> ictimai çıxışdan əhəmiyyətli narahatlıq hiss edir. Bu — sadə narahatlıq deyil — bəzilərində iş üçün təklif rədd etmək, karyera fürsətlərini buraxmaq səviyyəsinə çatır.</p>

          <h2>Niyə Beyin Ictimai Çıxışı "Təhlükə" Hesab Edir?</h2>
          <p>Evolyusion baxımdan: ata-bababa qrupdan ayrılmaq və ya rədd edilmək — fiziki həyat təhlükəsi idi (qrupdan kənar yalnız insan kainatda yaşaya bilməzdi). Bu mexanizm hələ də işləyir.</p>

          <p>Ictimai çıxış zamanı amigdala "rədd edilmə = təhlükə" siqnalı verir. Bədən "fight-or-flight" rejiminə girir: ürəkdöyüntüsü artır, tər, titrəmə, nəfəs daralması.</p>

          <h2>Əsas Düşüncə Təhrifələri</h2>
          <ul>
            <li><strong>"Hər kəs məni mühakimə edir"</strong> — əslində dinləyicilər çox vaxt öz işləri ilə məşğul olurlar</li>
            <li><strong>"Səhv etsəm rüsvay olaram"</strong> — kiçik səhvlər unudulur, sadəcə natiq onları yadında saxlayır</li>
            <li><strong>"Səs titrəyəcək, hamı görəcək"</strong> — narahatlıq daxili 10/10, görünüşdə 2/10</li>
            <li><strong>"İnsanlar mənim üzərimə fokuslanırlar"</strong> — spotlight effect — psixoloji araşdırmalar göstərir ki, insanlar başqalarına bizdən yarısı qədər diqqət edir</li>
          </ul>

          <h2>Praktik Plan — KDT + Ekspozisiya</h2>

          <p><strong>Mərhələ 1: Düşüncə Yenidən Quruluşu (Həftə 1-2)</strong></p>
          <p>Hər çıxışdan əvvəl gündəlik aparın: hansı düşüncələr yarandı? Onların alternativlərini yazın.</p>
          <ul>
            <li>"Səhv etsəm pis görünərəm" → "Hər natiq səhv edir. İnsanlar səhvlərə diqqət etmirlər"</li>
            <li>"Mən hazır deyiləm" → "Mən bu mövzunu kifayət qədər bilirəm. Hazır olmaq mümkün deyil — hazır olduğun an heç vaxt gəlmir"</li>
            <li>"Səs titrəyəcək" → "Səs titrəsə, davam edəcəyəm. Bu mənim peşəkarlığımı azaltmır"</li>
          </ul>

          <p><strong>Mərhələ 2: Hierarxiya (Həftə 2)</strong></p>
          <p>Ictimai çıxış vəziyyətlərini narahatlıq dərəcəsinə görə sıralayın (1-100):</p>
          <ul>
            <li>10/100 — Bir-iki dosta ideyanı izah etmək</li>
            <li>25/100 — Ailə yığıncağında tost demək</li>
            <li>40/100 — İş yığıncağında kommentariya vermək</li>
            <li>60/100 — Komandaya 5 dəqiqəlik məruzə</li>
            <li>80/100 — 30 nəfərlik konfrensda prezentasiya</li>
            <li>100/100 — TEDx kimi müstəvidə çıxış</li>
          </ul>

          <p><strong>Mərhələ 3: Ekspozisiya (Həftə 3-12)</strong></p>
          <p>Hər həftə bir səviyyə yuxarı qalxın. Ən aşağıdan başlayın. Hər ekspozisiyada:</p>
          <ol>
            <li>Əvvəldən narahatlıq qiymətləndirin (1-100)</li>
            <li>Ekspozisiyanı edin (səhv etsəniz də)</li>
            <li>Ekspozisiyadan sonra narahatlıq qiymətləndirin</li>
            <li>Daxili dialoq: "Ən pis halda nə oldu? Faktiki olaraq nə oldu?"</li>
          </ol>

          <p>Vacib qayda: <strong>ekspozisiya tək başına kifayət deyil — onu tez-tez təkrarlamaq lazımdır</strong>. Həftədə 1 dəfə effektsizdir, həftədə 3-4 dəfə optimaldır.</p>

          <h2>Toastmasters Strategiyası</h2>
          <p>Toastmasters International — ictimai çıxış qorxusunu aradan qaldırmaq üçün dünya səviyyəsində ən effektiv qrup məşqi proqramıdır. Strukturu:</p>
          <ul>
            <li>Hər həftə kiçik qrupda (10-30 nəfər) çıxışlar</li>
            <li>Hər çıxış konstruktiv geri qaytarma alır</li>
            <li>Tədricən mürəkkəbləşən çağırışlar</li>
            <li>"Rabit Speech" — gözləmədən söz almaq</li>
          </ul>

          <p>Tədqiqatlar: Toastmasters üzvlərinin 70%-ində 1 il ərzində glossofobiya səviyyəsi əhəmiyyətli azalır.</p>

          <h2>Praktik Texnikalar — Anında Tətbiq</h2>
          <ul>
            <li><strong>4-7-8 nəfəs</strong> çıxışdan əvvəl 5 dəqiqə</li>
            <li><strong>"Power pose"</strong> — 2 dəqiqə əllər yuxarı, geniş duruş (kortizolu azaldır)</li>
            <li><strong>Su sürtmək</strong> — biləyə soyuq su, vagal siniri stimullaşdırır</li>
            <li><strong>Bir dostluq üzünə fokuslanmaq</strong> — bütün auditoriya yox, bir kişi ilə danışın</li>
            <li><strong>Kameraya yox, insana baxmaq</strong> — virtual çıxışda da</li>
          </ul>

          <h2>Sıfırdan Başlamağın 3 Yolu</h2>
          <ol>
            <li><strong>YouTube videolar yazın</strong> — kameraya danışmaq alış-verişinin əldə etmənin asan yolu</li>
            <li><strong>Ailə daxilində məşq edin</strong> — uşaqlara hekayə danışmaq, ev yığıncaqlarında ad gününü dilə gətirmək</li>
            <li><strong>Online qruplara qoşulun</strong> — Zoom-da fəaliyyət göstərən Toastmasters klubları az təzyiqli mühit verir</li>
          </ol>""",
        "sources": """          <p><a href="https://www.nimh.nih.gov/health/topics/social-anxiety-disorder-more-than-just-shyness" target="_blank" rel="noopener">NIMH — Social Anxiety</a></p>
          <p><a href="https://www.toastmasters.org/about/research" target="_blank" rel="noopener">Toastmasters — Research on Communication Skills</a></p>
          <p>Stein, M. B., & Stein, D. J. (2008). Social anxiety disorder. <em>The Lancet</em>, 371(9618), 1115-1125.</p>
          <p>Hope, D. A., et al. (2010). <em>Managing Social Anxiety: A Cognitive-Behavioral Therapy Approach</em>. Oxford University Press.</p>"""
    },
    {
        "slug": "blog-sosial-fobiya-3.html",
        "title": "Qızarma və Tərləmə — Sosial Reaksiyalar",
        "desc": "Qızarma, tərləmə, titrəmə — sosial anksiyetinin fiziki əlamətləri və onlarla işləmək üsulları.",
        "read_time": 7,
        "cover": "images/blog/sosial-fobiya/art3-cover.jpg",
        "cover_alt": "Üzdə qızarma",
        "short": "Sosial qızarma (eritrofobiya) və tərləmə — bədənin avtomatik reaksiyası ilə necə işləmək.",
        "body": """          <p>Sosial situasiyada qəfildən qızarmaq, əllərin tərləməsi, səsin titrəməsi — bunlar utancaqlıq deyil, <strong>simpatik sinir sisteminin avtomatik reaksiyalarıdır</strong>. Bu reaksiyaları "düz başlamaq" mümkün deyil — onları idarə etmək olar.</p>

          <h2>Qızarma (Eritrofobiya)</h2>
          <p>Üzdə qızarma — qan damarlarının genişləməsi nəticəsidir. Bu reaksiya beyin tərəfindən "diqqət edilmə" siqnalı kimi tetikleyir. Paradoks: <strong>qızarmaqdan qorxmaq qızarmanı gücləndirir</strong>.</p>

          <p>Cəmiyyətdə yayılmış inanc: "Hər kəs görər mənim qızardığımı". Tədqiqatlar göstərir: insanlar başqalarının qızarmasını yalnız <strong>30%-də</strong> qeyd edir. Yəni qızardığınız hallarda 70%-i heç kim görmür.</p>

          <p>Müalicə yanaşması:</p>
          <ul>
            <li><strong>Paradoksal niyyət</strong> — "qızar, mənə fərq etməz" düsturu — Frankl yanaşması</li>
            <li><strong>Kortizol idarəsi</strong> — müntəzəm məşq, kafein azaltma</li>
            <li><strong>Soyuq su biləklərə</strong> — anlıq rahatlama</li>
            <li><strong>KDT — düşüncə yenidən quruluşu</strong></li>
          </ul>

          <p>Əgər qızarma ciddi dərəcədə həyata təsir edirsə — nadir hallarda dərman müalicəsi (beta-blokatorlar) tətbiq olunur. Lakin əksər hallarda KDT kifayətdir.</p>

          <h2>Tərləmə</h2>
          <p>Hiperhidroz (artıq tərləmə) — başqa fizioloji səbəblə də ola bilər (genetik, hormonal). Sosial anksiyete tərləməsi bu özəlliklərlə fərqlənir:</p>
          <ul>
            <li>Sosial vəziyyətdə artır, tək olduqda azalır</li>
            <li>Əllər və qoltuqaltı ən çox</li>
            <li>"Hamı görər tərimi" düşüncəsi onu gücləndirir</li>
          </ul>

          <p>Strategiyalar:</p>
          <ul>
            <li><strong>Antiperspirant</strong> — gecə tətbiq edin, daha effektiv</li>
            <li><strong>Soyuq əl tutuşu</strong> — kontaktdan əvvəl əlləri yuyun, soyuq su ilə</li>
            <li><strong>Botulinum (botox)</strong> — şiddətli halda, dermatoloji prosedur</li>
            <li><strong>KDT</strong> — düşüncələrlə işləmə tərləmənin tezliyini azaldır</li>
          </ul>

          <h2>Titrəmə</h2>
          <p>Səs titrəməsi və əl titrəməsi — adrenalin dövranının nəticəsidir. Bunu tamamilə qarşısını almaq mümkün deyil, lakin azaltmaq olar:</p>
          <ul>
            <li><strong>Dərin nəfəs</strong> 4-7-8 düsturu ilə</li>
            <li><strong>Mikrofon istifadə edin</strong> — səs titrəməsi az hiss olunur</li>
            <li><strong>Əlləri masaya qoyun</strong> — titrəmə görünməz</li>
            <li><strong>Beta-blokatorlar</strong> (psixiatrın nəzarətində) — adrenalin reaksiyasını blok edir</li>
          </ul>

          <h2>"Spotlight Effect"</h2>
          <p>Cornell Universitetinin klassik tədqiqatı (Gilovich, 2000): tələbələrdən biri uğursuz köynək geyinib otağa girdi. Sonra digər tələbələrdən soruşuldu — yalnız <strong>23%-i</strong> köynəyi xatırladı. Halbuki köynəyi geyinən tələbə "hamı görüb" hesab edirdi.</p>

          <p>Bu effekt sosial anksiyete üçün qızıl bilikdir: <strong>başqaları sənə düşündüyündən 2-3 dəfə az diqqət edir</strong>. Onların öz işləri, narahatlıqları, fikirləri var.</p>

          <h2>Praktik Tapşırıq: 1 Həftəlik Eksperiment</h2>
          <p>Bir həftə ərzində:</p>
          <ol>
            <li><strong>Gündə 1 dəfə qəsdən "diqqət çəkən" hərəkət edin</strong> — fərqli rəngli paltar geymək, hər kəsdən fərqli yer seçmək, məzəli hekayə danışmaq</li>
            <li><strong>Ertəsi gün analiz edin:</strong> nə qədər insanın diqqətini çəkdi? Real cavab nədir?</li>
            <li><strong>Nəticələri qeyd edin</strong></li>
          </ol>

          <p>Əksər vaxt nəticə şokverici olur: heç kim demək olar ki diqqət etmədi. Bu eksperiment "hamı məni izləyir" inancını sındırır.</p>

          <h2>Yekun: Bədəninizə Düşmən Olmayın</h2>
          <p>Qızarma, tərləmə, titrəmə — bunlar bədənin "diqqət edilmə!" siqnallarına avtomatik reaksiyasıdır. Onları tamamilə yox etmək məqsəd deyil. <strong>Onlardan qorxmamaq</strong> — məqsəddir. Qorxu yox olduqda — reaksiyanın özü də zaman keçdikcə zəifləyir.</p>""",
        "sources": """          <p><a href="https://my.clevelandclinic.org/health/diseases/24221-erythrophobia" target="_blank" rel="noopener">Cleveland Clinic — Erythrophobia (Fear of Blushing)</a></p>
          <p><a href="https://www.mayoclinic.org/diseases-conditions/hyperhidrosis/symptoms-causes/syc-20367152" target="_blank" rel="noopener">Mayo Clinic — Hyperhidrosis</a></p>
          <p>Gilovich, T., Medvec, V. H., & Savitsky, K. (2000). The spotlight effect in social judgment. <em>Journal of Personality and Social Psychology</em>, 78(2), 211-222.</p>
          <p>Bögels, S. M., et al. (2002). Cognitive-behavioral group treatment for social phobia. <em>Behaviour Research and Therapy</em>, 40(8), 869-883.</p>"""
    },
    {
        "slug": "blog-sosial-fobiya-4.html",
        "title": "Sosial Anksiyete vs İntrovertlik — Fərq Nədə?",
        "desc": "İntrovertlik — şəxsiyyət xüsusiyyəti, sosial anksiyete — klinik vəziyyət. Fərqi tanımaq və düzgün identifikasiya etmək.",
        "read_time": 7,
        "cover": "images/blog/sosial-fobiya/art4-cover.jpg",
        "cover_alt": "Tək insan kütlədə",
        "short": "İntrovert olmaq — sağlamdır. Sosial anksiyete — müalicə tələb edir. İki vəziyyəti necə ayırd etmək?",
        "body": """          <p>"Mən introverttəm" və "mənim sosial anksiyetəm var" — bu iki cümlə tez-tez bir-biri ilə qarışdırılır. Lakin <strong>introvertlik şəxsiyyət xüsusiyyətidir, sosial anksiyete isə klinik pozğunluqdur</strong>. Fərqi tanımaq vacibdir, çünki müalicə yanaşmaları tamamilə fərqlidir.</p>

          <h2>İntrovertlik Nədir?</h2>
          <p>İntrovertlik — Carl Jung tərəfindən təsvir edilən və müasir Big Five şəxsiyyət modelinə daxil olan dimensiondur. İntrovertlər:</p>
          <ul>
            <li>Enerjini <strong>təklikdə</strong> bərpa edirlər</li>
            <li>Dərin söhbətləri ictimai təbəssümdən üstün tuturlar</li>
            <li>Az, lakin yaxın dostlar dairəsinə üstünlük verirlər</li>
            <li>Sosial qarşılıqlı təsirdən sonra "yorulur"-lar</li>
            <li>Düşünərək cavab verirlər, çox impulsiv olmurlar</li>
          </ul>

          <p>İntrovertlik 30-50% əhalidə var və <strong>tamamilə sağlamdır</strong>. İntrovert olmaq problem deyil — bu xüsusi bir növ enerji idarəsidir.</p>

          <h2>Sosial Anksiyete Nədir?</h2>
          <p>Sosial anksiyete — sosial vəziyyətlərdə <strong>kəskin qorxu və qaçınma davranışı</strong> ilə xarakterizə olunan klinik pozğunluq. DSM-5 diaqnozudur. Pasiyentlər:</p>
          <ul>
            <li>Sosial vəziyyətlərdən <strong>qorxurlar</strong> (yox enerjini "saxlayır"-lar)</li>
            <li>Mühakimə edilməkdən, alçaldılmaqdan qaçırlar</li>
            <li>Fiziki simptomlar (qızarma, tərləmə, titrəmə) keçirirlər</li>
            <li>Vəziyyətdən sonra "necə oldu" düşüncələri ilə əzab çəkirlər</li>
            <li>İş, məktəb, münasibətlər ciddi pozulur</li>
          </ul>

          <h2>Əsas Fərq: Enerji vs Qorxu</h2>

          <p>Sadə test:</p>
          <ul>
            <li><strong>İntrovert:</strong> "Tədbirə getdim, gözəl idi. İndi 2 saat tək qalmaq istəyirəm — enerji bərpa etmək üçün."</li>
            <li><strong>Sosial Anksiyetəli:</strong> "Tədbirə gedə bilmədim. Getsəm — fiziki simptomlar başlayacaq, hamı görəcək, mən rüsvay olacam."</li>
          </ul>

          <p>İntrovert "gəlmək istəmir-ə bilər", lakin gedə bilər. Sosial anksiyetəli — getmək istəyər, lakin gedə bilməz.</p>

          <h2>Çoxlu Yayılmış Səhv İnanclar</h2>

          <p><strong>"Sosial anksiyetəli — extreme introvertdir"</strong> → <em>Yalan.</em> Tədqiqatlar göstərir ki, sosial anksiyete extravert adamlarda da baş verə bilər. Onlar sosial dünyaya can atırlar — lakin qorxu icazə vermir.</p>

          <p><strong>"İntrovertin sosial anksiyetəsi olur"</strong> → <em>Tamamilə doğru deyil.</em> İntrovertlərin əksəriyyəti psixoloji baxımdan sağlamdır. Sosial anksiyete onların yalnız 20%-də var.</p>

          <p><strong>"Sosial anksiyete keçər, böyüsün"</strong> → <em>Yalan.</em> Müalicəsiz qaldıqda 60%-də ömür boyu davam edir.</p>

          <p><strong>"İntrovertin müalicəsi gərəklidir"</strong> → <em>Yalan.</em> İntrovertlik müalicə tələb etmir — yaşam tərzinə uyğunlaşmaq tələb edir.</p>

          <h2>Tipik Səhv: İntrovertə Sosial Anksiyetenin Müalicəsi</h2>
          <p>Bəzi insanlar (xüsusən cəmiyyətdə) introvertliyi "patoloji" hesab edir və introvert insanı "müalicə etməyə" çalışır. Bu səhvdir.</p>

          <p>İntrovertə uyğun yanaşma:</p>
          <ul>
            <li>Sosial təcrübələri zorla artırmaq <em>lazım deyil</em></li>
            <li>Onun yaşam tərzinə (kiçik dostlar dairəsi, sakit hobbi) hörmət</li>
            <li>"Daha sosial ol" tövsiyələri yox — "tarazlıq tap" tövsiyəsi</li>
            <li>İntrovertin güclü tərəflərini görmək (dərin düşüncə, dinləmə bacarığı, fokus)</li>
          </ul>

          <h2>Hibrid Vəziyyət — Yüksək Funksiyalı Sosial Anksiyete</h2>
          <p>Bəzi insanlar sosial anksiyete + introvertlik kombinasiyası yaşayırlar. Bu hallarda işləri təsvir edilmiş gibi görünür — lakin daxili həyat ciddi əzabdır.</p>

          <p>Yüksək funksiyalı sosial anksiyetenin əlamətləri:</p>
          <ul>
            <li>İşdə uğurlu çıxışlar, lakin saatlarca əvvəldən narahatlıq və saatlarca sonra fiziki yorğunluq</li>
            <li>Lazımi sosial fəaliyyətləri yerinə yetirmək, lakin onlardan zövq almamaq</li>
            <li>"Hər kəs məni introvert hesab edir, lakin əslində qorxudan susuram"</li>
            <li>Tükənmə, depressiya əlamətləri</li>
          </ul>

          <p>Bu hal müalicə tələb edir — özünü idarə edən sosial anksiyete də klinik pozğunluqdur.</p>

          <h2>Yekun: Özünüzü Tanıyın</h2>
          <ul>
            <li>"Mən tək olmağı sevirəm, lakin sosial olduqda da rahatam" → İntrovert (sağlam)</li>
            <li>"Mən sosial olmağı istəyirəm, lakin qorxudan bacara bilmirəm" → Sosial anksiyete (müalicə)</li>
            <li>"Mən sosial olduqda da daxili əzab çəkirəm, lakin gizlədirəm" → Yüksək funksiyalı sosial anksiyete (müalicə)</li>
          </ul>

          <p>Düzgün identifikasiya — düzgün müdaxilə deməkdir. Səhv identifikasiya — illərlə əzab.</p>""",
        "sources": """          <p><a href="https://www.psychologytoday.com/us/basics/introversion" target="_blank" rel="noopener">Psychology Today — Introversion</a></p>
          <p><a href="https://www.nimh.nih.gov/health/topics/social-anxiety-disorder-more-than-just-shyness" target="_blank" rel="noopener">NIMH — Social Anxiety</a></p>
          <p>Cain, S. (2012). <em>Quiet: The Power of Introverts</em>. Crown.</p>
          <p>Heimberg, R. G., & Becker, R. E. (2002). <em>Cognitive-Behavioral Group Therapy for Social Phobia</em>. Guilford Press.</p>"""
    },
    {
        "slug": "blog-sosial-fobiya-5.html",
        "title": "Sosial Mediada Anksiyete — Yeni Forma",
        "desc": "Instagram, TikTok, Facebook — yeni sosial mühit və yeni psixoloji çətinliklər. FOMO, müqayisə, axtarış.",
        "read_time": 7,
        "cover": "images/blog/sosial-fobiya/art5-cover.jpg",
        "cover_alt": "Telefon ekranı",
        "short": "FOMO, sonsuz müqayisə, beğeni axtarışı — sosial medianın yeni psixoloji çətinlikləri.",
        "body": """          <p>20 il əvvəl sosial anksiyete fiziki dünyada idi: yığıncaq, prezentasiya, naməlum adamla tanışlıq. Bu gün yeni sosial mühit yaranıb — və onunla yeni psixoloji çətinliklər. <strong>Sosial medianın insan psixikası üzərindəki təsiri</strong> son 10 ildə tədqiqatçıların ən çox araşdırdığı mövzulardan biridir.</p>

          <h2>FOMO — "İmkanı Buraxma" Qorxusu</h2>
          <p>FOMO (<em>Fear of Missing Out</em>) — sosial mediadan yaranan ən geniş yayılmış psixoloji vəziyyətdir. Tədqiqat (Przybylski et al., 2013): yeniyetmələrin <strong>69%-i</strong> FOMO əlamətləri yaşayır.</p>

          <p>FOMO əlamətləri:</p>
          <ul>
            <li>Telefonu yatağa apartmaq, gecə-gündüz yoxlamaq</li>
            <li>"Hamı məsə bilir, mən bilmirəm" hissi</li>
            <li>Hər tədbirə getmək məcburiyyəti — hətta yorğun olduqda</li>
            <li>Vacib xəbəri buraxmaqdan qorxmaq</li>
            <li>Sosial mediadan ayrılmaq fiziki narahatlıq yaratmaq</li>
          </ul>

          <p>FOMO müalicəsi: <strong>JOMO</strong> (<em>Joy of Missing Out</em>) — buraxmağın zövqünü kəşf etmə. Bilərəkdən bəzi şeylərə qatılmamaq və özünü kompromis etmək.</p>

          <h2>Sosial Müqayisə Tələsi</h2>
          <p>Festinger-in 1954-cü il klassik nəzəriyyəsi: insan özünü <strong>başqaları ilə müqayisə edərək</strong> qiymətləndirir. Sosial media bu mexanizmi 100 dəfə gücləndirir.</p>

          <p>Problem: sosial mediada gördüyümüz <strong>başqalarının ən yaxşı 5 dəqiqəsidir</strong>, bizim isə tam 24 saatımızdır. Müqayisə qeyri-bərabərdir.</p>

          <p>Tədqiqat (Verduyn et al., 2017): Facebook 1 saat passiv istifadəsi (scrollla) sonra <strong>əhval-ruhiyyə kəskin enir</strong>. Aktiv istifadə (post yazmaq, kommentariya) bu effekti yaratmır.</p>

          <h2>"Bəyəni" Asılılığı</h2>
          <p>Hər "like", "view", "follower" bizdə dopamin axını yaradır — sıxlaşmış uşağa şokolad verən qədər güclü. Bu mexanizm bilərəkdən sosial media tərəfindən qurulub (variable reinforcement schedule).</p>

          <p>Nəticə: posta cavab az olduqda — özümüzü "kifayətsiz" hiss edirik. Bu hisslər real münasibətlərə də yansıyır.</p>

          <p>Strategiya: <strong>analytics-i bağlayın</strong>. Like saysını, view saysını görməyin. Yalnız substance üzərinə fokuslanın.</p>

          <h2>Onlayn vs Oflayn Anksiyete</h2>
          <p>Maraqlı paradoks: sosial mediadan əziyyət çəkənlərin əksəriyyəti orada <strong>daha çox</strong> aktiv olur. Niyə?</p>
          <ul>
            <li>Onlayn — mətnli kommunikasiya — fiziki simptomlar görünmür (qızarma, titrəmə)</li>
            <li>Cavabı düşünmək üçün vaxt var</li>
            <li>Birbaşa rədd edilmə daha az ağrılıdır</li>
            <li>"Görmə" hissi olmadan da "məşğul olma" hissi var</li>
          </ul>

          <p>Lakin bu "rahatlıq" tələdir. Onlayn dünyada təcrübə oflayn dünyaya keçmir. Hər kəslə chat-da raat olan adam, real görüşdə yenə dilini itirir.</p>

          <h2>Cyberbullying və Sosial İdentifikasiya Pozğunluğu</h2>
          <p>Sosial mediada zorbalıq daha keçici, lakin daha geniş yayılmışdır. Bir şərh 100,000 insan tərəfindən görülə bilər. Yeniyetmələr üçün xüsusən təhlükəlidir.</p>

          <p>Tədqiqatlar (Kowalski et al., 2014): cyberbullying qurbanlarında depressiya, anksiyete, intihar düşüncələri ənənəvi zorbalıq qurbanlarına nisbətən 2-3 dəfə yüksəkdir.</p>

          <h2>Praktik Strategiyalar</h2>

          <p><strong>1. "Detox" sınayın.</strong> 1 həftə tam olmadan, ya da gündə 2 saatla məhdud. Çox vaxt nəticə şaşırdıcı olur — depressiya əlamətləri 30%-dən çox azalır (Hunt et al., 2018).</p>

          <p><strong>2. Bildirimləri söndürün.</strong> Hər bildirim — dopamin axınıdır. Sosial media səndən asılı olmaq əvəzinə — sən onu istədiyində açmalısan.</p>

          <p><strong>3. "Greyscale" tətbiq edin.</strong> Telefonu qara-ağ rejimə keçirin. Tədqiqatlar göstərir: rəngsiz ekranda istifadə vaxtı 30%-dən çox azalır.</p>

          <p><strong>4. Ən dəyişdirici izləyin.</strong> Hər həftə 1-2 hesab izləməyi dayandırın — bu sizdə "kifayətsiz" hissi yaradan hesablar. Fərqi 1 ay sonra hiss edəcəksiniz.</p>

          <p><strong>5. Yatağa telefon aparmayın.</strong> Yataq otağı — telefon yox zonası olsun. Yuxu pozğunluqları kəskin yaxşılaşır.</p>

          <h2>Nə Vaxt Peşəkar Yardım?</h2>
          <ul>
            <li>Sosial mediadan ayrılmaq fiziki narahatlıq yaradır (titrəmə, panik)</li>
            <li>Real münasibətlər zərbə alır</li>
            <li>İş və ya təhsil performansı pisləşir</li>
            <li>Yuxu pozulur</li>
            <li>İntihar düşüncələri yaranır (xüsusən cyberbullying-dən sonra)</li>
          </ul>

          <p>Sosial media asılılığı — yeni klinik vəziyyətdir, lakin ənənəvi narahatlıq və depressiya kimi müalicə oluna bilir.</p>""",
        "sources": """          <p><a href="https://www.apa.org/news/press/releases/2017/08/lonely-isolated" target="_blank" rel="noopener">APA — Social Media and Loneliness</a></p>
          <p><a href="https://www.nimh.nih.gov/health/publications/social-media-and-mental-health" target="_blank" rel="noopener">NIMH — Social Media and Mental Health</a></p>
          <p>Przybylski, A. K., et al. (2013). Motivational, emotional, and behavioral correlates of fear of missing out. <em>Computers in Human Behavior</em>, 29(4), 1841-1848.</p>
          <p>Hunt, M. G., et al. (2018). No more FOMO: Limiting social media decreases loneliness and depression. <em>Journal of Social and Clinical Psychology</em>, 37(10), 751-768.</p>"""
    }
]

for i, art in enumerate(ARTS):
    out = CHROME
    others = [a for a in ARTS if a["slug"] != art["slug"]][:3]
    related = "\n".join(CARD.format(slug=o["slug"], title=o["title"], excerpt=o["short"]) for o in others)
    art_full = dict(art); art_full["related"] = related
    for k, v in art_full.items():
        out = out.replace("{" + k + "}", str(v))
    (ROOT / art["slug"]).write_text(out, encoding="utf-8")
    print(f"WROTE: {art['slug']}")
print("Done.")
