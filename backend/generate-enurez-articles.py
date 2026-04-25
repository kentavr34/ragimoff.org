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
        <span class="badge">UŞAQ SAĞLAMLIĞI</span>
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
        <h2 class="sec-h2">Uşağınız üçün konsultasiya?</h2>
        <p class="sec-sub">Beynəlxalq protokollarla — dərmansız müalicə</p>
        <div class="cta-band-btns">
          <a href="https://wa.me/994702200376" class="btn btn-fill" target="_blank">WhatsApp ilə Yazın</a>
          <a href="enurez.html" class="btn btn-line">Gecə Enurezi</a>
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
              <span class="blog-card-cat">Enurez</span>
              <h3 class="blog-card-title">{title}</h3>
              <p class="blog-card-excerpt">{excerpt}</p>
            </div>
          </a>"""

ARTS = [
    {
        "slug": "blog-enurez.html",
        "title": "Uşağınız Gecələr Yatağı Isladırsa — 5 Yanlış İnanc",
        "desc": "Enurez haqqında 5 ən yayılmış səhv inanc və elmi cavablar. ICCS, NICE, EAU/ESPU protokolu.",
        "read_time": 8,
        "cover": "images/blog/enurez/art1-cover.jpg",
        "cover_alt": "Yatan uşaq",
        "short": "«Özü keçər», «su içməsin», «danlamaq lazımdır» — yayılmış inanclar və elmi cavablar.",
        "body": """          <p>Uşağınız 6, 7, hətta 10 yaşındadır və hələ də gecələr yatağı isladır. Ailənin qulağına yetişən məsləhətlər: "özü keçər", "su içməsin gecə", "hər saat oyat", "danla, utan ki, etməsin". Tədqiqatlar göstərir: bu məsləhətlərin <strong>heç biri işə yaramır, hətta zərərlidir</strong>.</p>

          <p>Beynəlxalq Uşaq Sidik Tutmama Cəmiyyəti (ICCS, 2020) və NICE (Britaniya) qaydalarına əsasən, gecə enurezi (BMGE) — müalicə olunan klinik vəziyyətdir. Bu məqalədə 5 yanlış inanca baxırıq və elmi cavablar veririk.</p>

          <h2>Mif 1: "Özü keçər, gözləməli olarsınız"</h2>
          <p><strong>Yanlış.</strong> Statistik olaraq doğrudur ki, hər il enurezli uşaqların 15%-i kortəkim sağalır. Lakin bu o deməkdir ki, <strong>uşaqların 50%-i 12 yaşa qədər müalicəsiz qaldıqda hələ də enurezdən əziyyət çəkir</strong>.</p>

          <p>Erkən müalicə daha effektivdir. 7 yaşda başlanan müalicədə uğur 80-85%, 12 yaşda 60-65%-dir. Lazımsız ağrıdan və sosial təcriddən uşağı qorumaq üçün — gözləmək yox, müraciət etmək lazımdır.</p>

          <h2>Mif 2: "Su içməsin axşam"</h2>
          <p><strong>Yarımyalan.</strong> Axşam saatlarında <em>artıq</em> maye qəbulunu məhdudlaşdırmaq doğrudur. Lakin <strong>tam susuz qoymaq zərərlidir</strong>. Susuzluq adekvat yuxu səviyyəsini pozur, böbrəklərə yük yaradır.</p>

          <p>ICCS qaydası: ümumi gündəlik mayenin 40%-i səhər (07-12), 40%-i günorta (12-17), 20%-i axşam (17-19). Yatmazdan 2 saat əvvəl maye qəbul edilməməlidir.</p>

          <h2>Mif 3: "Gecə hər saat oyatmaq lazımdır"</h2>
          <p><strong>Yanlış və zərərlidir.</strong> Bu məsləhət uşağın yuxu strukturunu pozur. Yuxu dövrlərinin parçalanması — beyin inkişafına ziyan vurur, gündəlik diqqət və əhval-ruhiyyəni pisləşdirir.</p>

          <p>Doğru yanaşma — <strong>alarm cihazı</strong> (enuresis alarm). Bu cihaz uşaq sidikləməyə başlayanda avtomatik alarm verir — beyin tədricən bu siqnalı tutur və uşaq özü oyanmağa başlayır. Beynəlxalq protokollarda 70-80% effektivlik göstərir.</p>

          <h2>Mif 4: "Danlama uşağı utandırsın, ki etməsin"</h2>
          <p><strong>Tam əksinə — bu uşağa zərər verir və enurezi gücləndirir.</strong></p>

          <p>Enurez fizioloji vəziyyətdir, "iradə zəifliyi" yox. Beyin antidiuretik hormon istehsalında və ya sidik kisəsinin idarə olunmasında yetkin deyil. Uşaq bunu kontrol edə bilməz.</p>

          <p>Danlama nəticələri:</p>
          <ul>
            <li>Self-esteem aşınması — "mən pis uşağam"</li>
            <li>Stress səviyyəsinin artması — bu öz-özünə enurezi gücləndirir</li>
            <li>Yatmaq qorxusu yaranır — yuxu pozğunluğuna gətirir</li>
            <li>Valideyn-uşaq əlaqəsi pozulur</li>
            <li>İkincili emosional problemlər (anksiyete, depressiya)</li>
          </ul>

          <p>Doğru yanaşma: <strong>uşağa "bu sənin günahın deyil"</strong> deyilməlidir. Uşaq müalicə komandasının üzvüdür, günahkar deyil.</p>

          <h2>Mif 5: "Bu psixoloji problem, psixoloqa apar"</h2>
          <p><strong>Yarım doğru.</strong> Birincili monosimptomatik gecə enurezi (BMGE) — fizioloji vəziyyətdir, klinik psixoloji yox. Lakin bunu fizioloji baxımdan başa düşmək və elmi protokol tətbiq etmək psixoloji bilikdir.</p>

          <p>Doğru mütəxəssis ardıcıllığı:</p>
          <ol>
            <li><strong>Pediatr</strong> — fiziki səbəbləri istisna edir (sidik yolları infeksiyası, diabet, sidik kisəsinin anomaliyaları)</li>
            <li><strong>Klinik psixoloq və ya nevrolog</strong> — BMGE diaqnozu və müalicə protokolu</li>
            <li><strong>Lazım gələrsə uroloji konsiltasiya</strong> — şiddətli halda</li>
          </ol>

          <p>Müalicə protokolunda <strong>alarm cihazı</strong> birinci xətt müdaxilədir. İkinci — desmopressin (sintetik antidiuretik hormon, məhdud halda). Hər iki yanaşma psixoloji dəstəklə birlikdə işləyir.</p>

          <h2>Yekun: Doğru Bilik — Doğru Müalicə</h2>
          <p>Enurez ilə bağlı miflər — uşağa və ailəyə zərər vurur. Doğru bilik:</p>
          <ul>
            <li>Erkən müraciət edin (5-6 yaşdan)</li>
            <li>Maye qəbulu rejimi kafidir, tam yasaq yox</li>
            <li>Alarm cihazı + protokol — qızıl standart</li>
            <li>Heç vaxt danlama, utandırma yoxdur</li>
            <li>Pediatr → klinik mütəxəssis ardıcıllığı</li>
          </ul>

          <p>Doğru protokol ilə uşaqların 70-85%-i 8-12 həftə ərzində tam quruyur. Bu — illərlə əzab çəkməkdən qat-qat asandır.</p>""",
        "sources": """          <p><a href="https://i-c-c-s.org/" target="_blank" rel="noopener">ICCS — International Children's Continence Society</a></p>
          <p><a href="https://www.nice.org.uk/guidance/cg111" target="_blank" rel="noopener">NICE Guideline CG111 — Bedwetting in under 19s</a></p>
          <p><a href="https://www.aap.org/" target="_blank" rel="noopener">American Academy of Pediatrics — Bedwetting</a></p>
          <p>Nevéus, T., et al. (2020). Management and treatment of nocturnal enuresis. <em>Journal of Pediatric Urology</em>, 16(1), 10-19.</p>"""
    },
    {
        "slug": "blog-enurez-2.html",
        "title": "BMGE — Birincili Monosimptomatik Gecə Enurezi: Tam Bələdçi",
        "desc": "BMGE nədir, hansı növləri var, diaqnostika kriteriyaları və müalicə yolları. Beynəlxalq protokol.",
        "read_time": 9,
        "cover": "images/blog/enurez/art3-cover.jpg",
        "cover_alt": "Pediatr və uşaq",
        "short": "BMGE diaqnozunun tam bələdçisi: növlər, kriteriyalar, müalicə protokolu (ICCS 2020).",
        "body": """          <p>"Mənim övladımın enurezi var" — geniş termin. Lakin klinik baxımdan enurezin <strong>4 fərqli növü</strong> var, və hər birinin özünəməxsus müalicə yolu mövcuddur. Düzgün diaqnoz — düzgün müalicə deməkdir.</p>

          <h2>BMGE Nədir?</h2>
          <p>BMGE — Birincili Monosimptomatik Gecə Enurezi:</p>
          <ul>
            <li><strong>Birincili</strong> — uşaq heç vaxt 6 ay ərzində quru gecələr keçirməmişdir (ikincili — qurudu, sonra başladı)</li>
            <li><strong>Monosimptomatik</strong> — yalnız gecə sidik tutmama, gündüz simptomu yoxdur</li>
            <li><strong>Gecə</strong> — yalnız yuxu zamanı</li>
            <li><strong>Enurez</strong> — sidiyin idarəsiz buraxılması</li>
          </ul>

          <p>BMGE — enurez halların <strong>70-80%-ni</strong> təşkil edir. Ən yaxşı proqnoz bu növdədir.</p>

          <h2>BMGE Kriteriyaları (DSM-5 və ICCS 2020)</h2>
          <ul>
            <li>Yaş 5 və yuxarı (5 yaşa qədər normal hesab olunur)</li>
            <li>Həftədə ən azı 2 dəfə, 3 ay ərzində baş verir</li>
            <li>Klinik əhəmiyyətli stress yaradır</li>
            <li>Tibbi səbəblər (dərman, narkotik, neyroloji vəziyyət) istisna edilmiş</li>
            <li>Gündüz sidik problemləri yox</li>
          </ul>

          <h2>Patofiziologiya — Niyə Baş Verir?</h2>
          <p>Üç əsas mexanizm:</p>

          <p><strong>1. Antidiuretik hormonun (ADH) gecə istehsalında çatışmazlıq.</strong> Normal insanda gecə vasopressin (ADH) artır — böbrəklər daha az sidik istehsal edirlər. BMGE-li uşaqlarda bu hormonal ritm pozulub — gecə də gündüz qədər sidik istehsal olunur.</p>

          <p><strong>2. Sidik kisəsinin az kapasiteti və ya yüksək həssaslığı.</strong> Sidik kisəsi tam dolmadan kasılma siqnalı verir.</p>

          <p><strong>3. Yüksək yuxu dərinliyi.</strong> BMGE-li uşaqlar 3-cü mərhələ yuxuda (dərin yuxu) çox vaxt keçirirlər. Sidik kisəsindən gələn siqnalları beyin "almır" — uşaq oyanmadan sidik gedir.</p>

          <p>Genetik komponent güclüdür: hər iki valideyn enurez tarixçəsi varsa, uşaqda risk <strong>77%</strong>-dir. Bir valideyn — 44%. Heç bir valideyn — 15%.</p>

          <h2>4 Növ Enurez — Müalicə Fərqləri</h2>

          <p><strong>1. BMGE</strong> (yuxarıda təsvir edildi) — <em>Müalicə:</em> alarm cihazı + maye rejimi.</p>

          <p><strong>2. Polisimptomatik Gecə Enurezi (PGE)</strong> — gecə + gündüz simptomları (gündüz tezliyi, çox gecikdirə bilməmək). <em>Müalicə:</em> uroloji qiymətləndirmə + sidik kisəsi məşqi + bəzi hallarda dərman.</p>

          <p><strong>3. İkincili Enurez</strong> — uşaq quru olub, sonra yenidən başlayıb. Adətən psixoloji stress (boşanma, doğulma, məktəb dəyişikliyi) və ya tibbi (sidik yolu infeksiyası, diabet) tetikleyicidir. <em>Müalicə:</em> əsas səbəbə müdaxilə + standart enurez protokolu.</p>

          <p><strong>4. Gündüz Enurezi (Daytime Wetting)</strong> — yalnız gündüz, gecə quru. Adətən sidik kisəsinin disfunksiyası, bəzi hallarda davranış problemi. <em>Müalicə:</em> uroloji qiymətləndirmə birinci.</p>

          <h2>Diaqnostika Addımları</h2>
          <ol>
            <li><strong>Anamnez</strong> — sidik tezliyi (gecə, gündüz), miqdar, su qəbulu, ailə tarixçəsi</li>
            <li><strong>Sidik analizi</strong> — infeksiya, qlükoza, protein</li>
            <li><strong>Fiziki müayinə</strong> — neyroloji və genitouroloji</li>
            <li><strong>Sidik dövrü cədvəli</strong> — 2-3 gün uşağın sidik tezliyi və miqdarı qeydə alınır</li>
            <li><strong>Lazım gələrsə uzi (ultrasəs)</strong> — sidik kisəsinin və böbrəklərin qiymətləndirilməsi</li>
          </ol>

          <h2>BMGE Müalicə Protokolu (Beynəlxalq)</h2>
          <p>ICCS 2020 və EAU/ESPU 2019 qaydaları:</p>

          <p><strong>Birinci Xətt:</strong></p>
          <ol>
            <li>Psikoeğitim (uşaq və valideyn)</li>
            <li>Maye rejimi və yuxu gigiyenası</li>
            <li>Alarm cihazı (12 həftə)</li>
          </ol>

          <p><strong>İkinci Xətt</strong> (alarm cihazı kifayət etmədikdə):</p>
          <ol start="4">
            <li>Desmopressin (sintetik ADH) — qısa müddət üçün</li>
          </ol>

          <p><strong>Üçüncü Xətt</strong> (nadir hallarda):</p>
          <ol start="5">
            <li>Antikolinerjik dərmanlar (oksibutinin) — sidik kisəsi disfunksiyası varsa</li>
            <li>Kombinə müalicə</li>
          </ol>

          <p><strong>İmipramin tövsiyə edilmir</strong> birinci xətt üçün — ürək-damar yan təsirləri səbəbindən.</p>

          <h2>Müalicə Müddəti və Effektivlik</h2>
          <ul>
            <li>Alarm cihazı: 8-12 həftə, 70-80% uğur</li>
            <li>Desmopressin: tez nəticə, lakin dayandırıldıqda 60% residiv</li>
            <li>Birgə yanaşma: ən yüksək effektivlik (85%-dən çox), aşağı residiv</li>
          </ul>

          <p>Vacib: müalicə tamamlandıqdan sonra <strong>14 ardıcıl quru gecə</strong> tələb olunur ki, uğur sayılsın. Bu — beynəlxalq standartdır.</p>""",
        "sources": """          <p><a href="https://i-c-c-s.org/" target="_blank" rel="noopener">ICCS Standardization Documents 2020</a></p>
          <p><a href="https://uroweb.org/guidelines/paediatric-urology" target="_blank" rel="noopener">EAU/ESPU Guidelines on Paediatric Urology 2019</a></p>
          <p>Nevéus, T., et al. (2020). Management and treatment of nocturnal enuresis. <em>Journal of Pediatric Urology</em>, 16(1), 10-19.</p>
          <p>Caldwell, P. H., et al. (2020). Bedwetting and toileting problems in children. <em>The Medical Journal of Australia</em>, 213(2), 96-101.</p>"""
    },
    {
        "slug": "blog-enurez-3.html",
        "title": "Alarm Cihazı Necə İşləyir? — Beynəlxalq Protokol",
        "desc": "Enurez alarm cihazı — birinci xətt müalicə. Necə işləyir, necə tətbiq edilir, hansı növləri var.",
        "read_time": 7,
        "cover": "images/blog/enurez/art2-cover.jpg",
        "cover_alt": "Alarm saatı",
        "short": "Enurez alarm cihazının işləmə prinsipi və 12 həftəlik tətbiq protokolu.",
        "body": """          <p>Enurez müalicəsində <strong>alarm cihazı (enuresis alarm)</strong> — qızıl standartdır. NICE, ICCS, AAP — bütün beynəlxalq qaydalar onu birinci xətt müalicə kimi tövsiyə edir. Effektivlik 70-80%, residiv riski dərmanlardan 3-4 dəfə aşağı.</p>

          <p>Lakin bu cihaz hələ də Azərbaycanda az tanınır. Bu məqalədə işləmə prinsipini və düzgün tətbiqini izah edirik.</p>

          <h2>Necə İşləyir?</h2>
          <p>Cihaz iki hissədən ibarətdir:</p>
          <ul>
            <li><strong>Sensor</strong> — uşağın iç paltarına və ya yatağa yerləşdirilir, rütubətə həssasdır</li>
            <li><strong>Alarm</strong> — sensorla naqillə və ya simsiz qoşulur, səs və/və ya vibrasiya verir</li>
          </ul>

          <p>İşləmə mexanizmi: uşaq sidikləməyə başlayan kimi sensor rütubət aşkar edir və alarmı işə salır. Səs uşağı oyadır.</p>

          <h2>Niyə İşləyir? Klassik Şərtlənmə</h2>
          <p>Burada Pavlov şərtləndirməsi prinsipi tətbiq olunur:</p>
          <ul>
            <li><strong>Şərtsiz stimul:</strong> alarm səsi → şərtsiz reaksiya: oyanma</li>
            <li><strong>Şərtli stimul:</strong> sidik kisəsinin dolması (sensiya)</li>
            <li><strong>Tədricən yaranan əlaqə:</strong> sidik kisəsinin doluluğu → oyanma</li>
          </ul>

          <p>Yəni 8-12 həftə ərzində beyin sidik kisəsi siqnallarını tanımağa öyrənir və alarm gəlmədən uşaq özü oyanır.</p>

          <h2>Cihaz Növləri</h2>

          <p><strong>1. Yastıq tipli (mat type):</strong> Yatağın altına qoyulan döşəmə. Bütün yatağı qoruyur. Üstünlük: sensor uşaqla təmasda deyil, rahatdır. Çatışmazlıq: bəzən kifayət qədər tez işləmir.</p>

          <p><strong>2. Iç paltarına bərkidilən (body-worn):</strong> Sensor iç paltarına bərkidilir, alarm boyunda və ya bilekdə. Üstünlük: tez reaksiya verir. Çatışmazlıq: uşağa narahatlıq verə bilər.</p>

          <p><strong>3. Simsiz tip (wireless):</strong> Sensor uşağın yataq otağında, alarm valideynin otağında. Beləcə valideyn də uşağa kömək edə bilər. Daha bahadır.</p>

          <h2>12 Həftəlik Protokol</h2>

          <p><strong>Həftə 1-2: Adaptasiya</strong></p>
          <ul>
            <li>Cihazın necə bağlanacağını uşağa öyrətmək</li>
            <li>Hər gecə yatmazdan əvvəl birgə quraşdırma</li>
            <li>Alarm zamanı protokol: dərhal qalxmaq → tualet → cihazı yenidən bağlamaq → yatağa</li>
            <li>Uşaq özü iştirak edir — passiv qurban deyil</li>
          </ul>

          <p><strong>Həftə 3-6: Effekt formalaşır</strong></p>
          <ul>
            <li>Adətən bu mərhələdə alarm sayı azalır</li>
            <li>Bəzi gecələrdə alarm gəlmədən uşaq özü oyanır</li>
            <li>Quru gecələrin sayı artmağa başlayır</li>
          </ul>

          <p><strong>Həftə 7-12: Bərpa</strong></p>
          <ul>
            <li>14 ardıcıl quru gecə hədəfdir</li>
            <li>Tam quru səhər — kiçik sevinc anı (təbrik etmək, lakin "qonaqlıq" deyil)</li>
            <li>Sıçrayış olduqda — danlama yox, "bu da yoldur" yanaşması</li>
          </ul>

          <p><strong>Müalicə uğurla bitdikdə:</strong> 14 ardıcıl quru gecədən sonra cihaz tədricən kəsilir — 1 həftə hər ikinci gecə, sonra dayandırılır.</p>

          <h2>Praktik Məsləhətlər</h2>
          <ul>
            <li><strong>Cihazı uşağın yox, valideynin otağında yox — uşağın yatdığı otaqda yerləşdirin</strong>. Bəzən uşaq alarmı eşitmir, ona görə valideyn də yaxınlıqda olmalıdır</li>
            <li><strong>Müalicəyə həvəslə başlayın</strong> — uşağa "kömək alır" hissi verin, "cəza" yox</li>
            <li><strong>Şəkər və tort vermədən uşağı motivasiya etməyin</strong> — bu davranış asılılığını yaradır</li>
            <li><strong>Yataq paltarını uşaq özü dəyişmir</strong> — bu cəza kimi qəbul edilir; valideyn dəyişir, uşaq sadəcə kömək edir (məsələn, çirkli paltarı çamaşır maşınına qoyur)</li>
            <li><strong>Yenidən başlamaqdan qorxmayın</strong> — bəzi uşaqlarda 1-ci protokol uğursuz olur, 2-ci uğurlu</li>
          </ul>

          <h2>Çatışmazlıqlar və Maneələr</h2>
          <ul>
            <li>Cihaz uğursuz olduqda — adətən tətbiqdə səhvlər (uşaq sidiklədikdən sonra alarmı eşitmir, valideyn yardım etmir)</li>
            <li>Bəzi uşaqlar dərin yuxu səbəbindən alarmı eşitməzlər — bu zaman valideynin köməyi vacibdir</li>
            <li>Müalicə tamamlandıqdan sonra residiv (15-20%-də) — qısa müddətli yenidən tətbiq həll edir</li>
          </ul>

          <h2>Cihaz Necə Almaq Olar?</h2>
          <p>Azərbaycanda alarm cihazları hələ az tapılır. Beynəlxalq olaraq:</p>
          <ul>
            <li>Wet-Stop, Malem (ABŞ)</li>
            <li>Anzacare DRI Sleeper (Yeni Zelandiya)</li>
            <li>Pjama (İsveç)</li>
          </ul>

          <p>Klinikada müalicə alındıqda cihaz tez-tez verilir, müalicə bitdikdə geri qaytarılır.</p>""",
        "sources": """          <p><a href="https://www.nice.org.uk/guidance/cg111" target="_blank" rel="noopener">NICE Guideline CG111 — Bedwetting</a></p>
          <p><a href="https://i-c-c-s.org/" target="_blank" rel="noopener">ICCS — Standardization Documents</a></p>
          <p>Caldwell, P. H., et al. (2020). Alarm interventions for nocturnal enuresis. <em>Cochrane Database</em>, CD002911.</p>
          <p>Glazener, C. M., & Evans, J. H. (2005). Alarm interventions for nocturnal enuresis in children. <em>Cochrane Review</em>.</p>"""
    },
    {
        "slug": "blog-enurez-4.html",
        "title": "Desmopressin və İmipramin — Enurezdə Dərmanlar",
        "desc": "Hansı dərmanlar enurezdə tətbiq olunur, nə vaxt, hansı yan təsirləri ilə. Beynəlxalq protokollar.",
        "read_time": 7,
        "cover": "images/blog/enurez/art4-cover.jpg",
        "cover_alt": "Valideyn və uşaq",
        "short": "Desmopressin nə vaxt verilir, imipramin niyə tövsiyə edilmir — beynəlxalq cavablar.",
        "body": """          <p>"Dərman var ki, uşaq sidik buraxmasın?" — pediatr kabinetlərinin ən tez-tez verilən sualıdır. Cavab — bəli, lakin bu sual kompleksdir. Bu məqalədə iki ən tanınmış enurez dərmanına baxırıq və beynəlxalq protokollarda onların yerini izah edirik.</p>

          <h2>Desmopressin (DDAVP)</h2>
          <p>Desmopressin — sintetik vasopressin (antidiuretik hormon). İşləmə mexanizmi: <strong>böbrəklərə "daha az sidik istehsal et" siqnalı verir</strong>. Yatmazdan 1-2 saat əvvəl alındıqda gecə sidik istehsalını 30-50% azaldır.</p>

          <p>Nə vaxt verilir?</p>
          <ul>
            <li>Alarm cihazı kifayət etmədikdə (ikinci xətt)</li>
            <li>Səfər, düşərgə, gecə qonaqlıq kimi xüsusi hallarda — qısa müddət</li>
            <li>Ailədə alarm cihazını dəstəkləmək mümkün olmadıqda</li>
            <li>Sürətli nəticə tələb olunduqda</li>
          </ul>

          <p>Forması:</p>
          <ul>
            <li><strong>Tablet</strong> — ən geniş yayılmış (Minirin, DDAVP)</li>
            <li><strong>Tilim altı (sublingual)</strong> — uşaq tableti udmaqda çətinlik çəkdikdə</li>
            <li>Burun spreyi <strong>artıq tövsiyə edilmir</strong> — hiponatremi riski səbəbindən</li>
          </ul>

          <p><strong>Doza:</strong> 0.2 mg yatmazdan 1 saat əvvəl. Effekt göstərmədikdə — 0.4 mg. Maksimum 0.6 mg.</p>

          <p><strong>Müddət:</strong> Tipik kurs — 3 ay. Hər 3 aydan bir 1 həftə pauza ilə qiymətləndirmə.</p>

          <h2>Desmopressin Üstünlükləri</h2>
          <ul>
            <li><strong>Sürətli effekt</strong> — bir gecədə görünə bilər</li>
            <li><strong>Yataq paltarı az dəyişdirilir</strong> — gündəlik həyat asanlaşır</li>
            <li><strong>Səfər və ictimai gecələr üçün xüsusilə faydalıdır</strong></li>
            <li><strong>Yaxşı tədqiq olunmuş təhlükəsizlik profili</strong></li>
          </ul>

          <h2>Desmopressin Çatışmazlıqları</h2>
          <ul>
            <li><strong>Yüksək residiv riski</strong> — dərmanı kəsdikdə 60%-də enurez geri qayıdır</li>
            <li><strong>"Müalicə"-dən çox "simptom idarəsi"</strong> — beyni öyrətmir</li>
            <li><strong>Hiponatremi riski</strong> — qan natriumunun düşməsi (nadir, lakin ciddi)</li>
            <li><strong>Maye qəbulu məhdudiyyəti vacibdir</strong> — yatmazdan əvvəl və gecə az içilməlidir</li>
            <li><strong>Yan təsirlər</strong> — başağrısı (5-10%), ürəkbulanma, qarın ağrısı</li>
          </ul>

          <p><strong>Hiponatremi xəbərdarlığı:</strong> Maye sərbəst qəbulu — qanın natrium səviyyəsini təhlükəli aşağı sala bilər. Simptomlar: başağrısı, ürəkbulanma, qıcolma, koma. Buna görə desmopressin alan uşaq yatmazdan əvvəl çox maye qəbul etməməlidir.</p>

          <h2>İmipramin — Niyə Tövsiyə Edilmir</h2>
          <p>İmipramin (Melipramin, Tofranil) — köhnə nəsil triklik antidepressant. 1960-cı illərdən enurez üçün istifadə edilir. Lakin müasir qaydalar (NICE 2010, ICCS 2020) <strong>imipramini birinci xətt müalicədən çıxardıb</strong>.</p>

          <p>Niyə?</p>
          <ul>
            <li><strong>Ürək-damar yan təsirləri</strong> — aritmiya, taxikardiya, hipotensiya</li>
            <li><strong>Antikolinergik effektlər</strong> — quru ağız, qəbizlik, görmə pozğunluğu</li>
            <li><strong>Mərkəzi sinir sistemi yan təsirləri</strong> — yuxulu hal, başgicəllənmə, davranış dəyişiklikləri</li>
            <li><strong>Yüksək doza dölük üçün təhlükəlidir</strong> — bəzi hallarda fataldır</li>
            <li><strong>Effektivlik orta — </strong> 40-60% (alarm cihazından aşağı)</li>
            <li><strong>Yüksək residiv riski</strong> — dərmanı kəsdikdə 80%-də enurez qayıdır</li>
          </ul>

          <p>Ölkəmizdə hələ də bəzən pediatr və nevrologlar tərəfindən imipramin verilir — bu beynəlxalq protokollara zidd təcrübədir.</p>

          <h2>Antikolinerjiklər (Oksibutinin)</h2>
          <p>Bu dərmanlar sidik kisəsinin yığılmalarını azaldır. Yalnız <strong>polisimptomatik enurezdə</strong> (gündüz və gecə simptomları olan) tətbiq edilir, BMGE-də deyil. Yan təsirlər: quru ağız, qəbizlik, üzdə qızarma.</p>

          <h2>Birgə Yanaşma — Ən Effektiv</h2>
          <p>Klinik təcrübə və tədqiqatlar göstərir: <strong>alarm cihazı + desmopressin birgə</strong> tətbiq edildikdə nəticə hər birindən tək başına yüksəkdir.</p>

          <p>Tipik plan:</p>
          <ol>
            <li>Həftə 1-4: alarm cihazı + desmopressin (sürətli rahatlama)</li>
            <li>Həftə 5-8: desmopressin azaldılır, alarm davam edir</li>
            <li>Həftə 9-12: yalnız alarm</li>
            <li>14 quru gecədən sonra: hər iki müalicə tamamlanır</li>
          </ol>

          <p>Bu protokol residiv riskini 15%-ə qədər azaldır.</p>

          <h2>Dərmanlar Niyə Tək Başına Kifayət Deyil?</h2>
          <p>Dərmanlar simptomu idarə edir, lakin beyin-sidik kisəsi əlaqəsini öyrətmir. Dərman dayandırıldıqda — orijinal vəziyyət geri qayıdır. Alarm cihazı isə beyni öyrədir — və öyrəndiyini unutmur.</p>

          <p>Bu səbəbdən beynəlxalq protokollar həmişə davranış müalicəsini (alarm + maye rejimi + psixoloji dəstək) əsas hesab edir. Dərmanlar — alət, "həll" deyil.</p>""",
        "sources": """          <p><a href="https://www.nice.org.uk/guidance/cg111" target="_blank" rel="noopener">NICE Guideline CG111 — Bedwetting</a></p>
          <p><a href="https://i-c-c-s.org/" target="_blank" rel="noopener">ICCS — Treatment Recommendations</a></p>
          <p>Glazener, C. M., et al. (2003). Tricyclic and related drugs for nocturnal enuresis. <em>Cochrane Database</em>.</p>
          <p>Vande Walle, J., et al. (2012). Practical consensus guidelines for the management of enuresis. <em>European Journal of Pediatrics</em>, 171(6), 971-983.</p>"""
    },
    {
        "slug": "blog-enurez-5.html",
        "title": "Valideynlər Üçün 7 Praktik Məsləhət",
        "desc": "Müalicə zamanı və ondan sonra valideynlərin uşağa necə kömək edə biləcəyi — 7 praktik məsləhət.",
        "read_time": 7,
        "cover": "images/blog/enurez/art5-cover.jpg",
        "cover_alt": "Ailə birgə yemək",
        "short": "Müalicə zamanı və ondan sonra valideynin necə kömək edəcəyi — 7 konkret addım.",
        "body": """          <p>Enurez müalicəsi yalnız uşağın işi deyil — bütün ailənin birgə işidir. Tədqiqatlar göstərir: <strong>valideyn dəstəyi olan uşaqların müalicə uğuru 30-40% yüksəkdir</strong>. Bu məqalədə klinik təcrübədən əldə edilmiş 7 praktik məsləhət verilir.</p>

          <h2>Məsləhət 1: "Sənin Günahın Deyil" Cümləsini İlk Söyləyin</h2>
          <p>Enurez utanc və günahkarlıq hissi yaradır. Uşaq özünü "axmaq", "körpə", "pis" hesab etməyə başlayır. Bu hisslər müalicəyə əngəl olur — stres səviyyəsi enurezi gücləndirir.</p>

          <p>İlk söhbətdə açıq deyilməli:</p>
          <ul>
            <li>"Bu xəstəlik xarakterli vəziyyətdir, sənin günahın deyil"</li>
            <li>"Çox uşaqlarda olur — sən tək deyilsən"</li>
            <li>"Bu keçəcək, biz birlikdə işləyəcəyik"</li>
            <li>"Sən pis uşaq deyilsən, sən yaxşı uşaqsan"</li>
          </ul>

          <p>Bu mesajları <em>tək dəfə yox</em>, müalicə dövründə təkrar-təkrar verməli.</p>

          <h2>Məsləhət 2: Maye Rejimini Düzgün Qurun</h2>
          <p>Enurezin əsas idarə alətlərindən biri — gündəlik maye paylanması. Doğru rejim:</p>
          <ul>
            <li><strong>Səhər 7-9:</strong> böyük stəkan su (ümumi mayenin 30%)</li>
            <li><strong>Səhər 9-12:</strong> normal su qəbulu (20%)</li>
            <li><strong>Günorta 12-16:</strong> maksimum içmə dövrü (30%)</li>
            <li><strong>Axşam 16-19:</strong> normal su qəbulu (15%)</li>
            <li><strong>Axşam 19+:</strong> minimal — hətta sıfıra yaxın (5%)</li>
          </ul>

          <p>Şirin və qazlı içkilər (kola, fanta) sidik istehsalını <strong>2 dəfə artırır</strong>. Onları gündəlik içkilərdən ümumiyyətlə xaric edin. Çay (xüsusilə qara çay) — diuretik təsiri var, axşam saatlarında yox.</p>

          <h2>Məsləhət 3: Yatmazdan Əvvəl Tualet</h2>
          <p>"Double void" prinsipi: yatmazdan 30 dəqiqə əvvəl tualetə getmək, yatmazdan 5 dəqiqə əvvəl bir də tualetə getmək. İki dəfə getmək sidik kisəsini tam boşaldır.</p>

          <p>Vacib: zorla göndərmə yox — uşaq özü getsin, valideyn yalnız xatırladır.</p>

          <h2>Məsləhət 4: Yataq Paltarını Uşaq Dəyişməsin</h2>
          <p>Bu məsələ həssasdır. Bəzi məsləhətlər (xüsusən ənənəvi) deyir ki, "yataq paltarını özü dəyişsin, məsuliyyətli olar". Bu yanaşma yanlış və zərərlidir — uşaq bunu cəza kimi qəbul edir, utanc hissi artır.</p>

          <p>Doğru yanaşma:</p>
          <ul>
            <li>Çirkli paltarı uşaq sadəcə çamaşır maşınına qoyur (texniki addım)</li>
            <li>Yatağı valideyn dəyişir</li>
            <li>"İncidim" yox, "biz birgə həll edirik" mesajı</li>
            <li>Bütün proses sakit, dramatursız</li>
          </ul>

          <p>Vinil yataq qoruyucu istifadə edin — çamaşırı asanlaşdırır.</p>

          <h2>Məsləhət 5: Quru Gecələri Qeyd Edin, Lakin Mübaliğə Etməyin</h2>
          <p>"Quru gecə şəbəkəsi" — uşağın motivasiyası üçün effektivdir:</p>
          <ul>
            <li>Hər səhər kiçik şəkil və ya stiker (quru gecə = günəş, sıçrayış = bulud)</li>
            <li>14 ardıcıl günəşli gün — kiçik təbrik (hədiyyə yox, məsələn birgə gəzinti)</li>
          </ul>

          <p>Ehtiyatlı olun: <strong>çox böyük hədiyyələr nəticəsiz</strong>. Uşaq "müvəffəq olmadığında" gecənin sıxıntısı yaranır — bu özü-özünə enurezi gücləndirir.</p>

          <h2>Məsləhət 6: Sıçrayışları Dramatik Etməyin</h2>
          <p>14 quru gecədən sonra bir nəm gecə oldu. Səhər valideynin reaksiyası — kritik məqamdır. Yanlış: "Yenə? Düşündük ki keçib! İndi yenə başlayaq!"</p>

          <p>Doğru: "Bu da olur. Sıçrayışlar normal hissəsi müalicənin. Davam edirik. Heç bir şey itirmədik."</p>

          <p>Müalicə xətti deyil, dalğavari prosesdir. Bu gerçəklikdir — buna hazır olmaq lazım.</p>

          <h2>Məsləhət 7: Düşərgə, Səfər, Qonaqlıq — Hazırlıqlı Olmaq</h2>
          <p>Sosial baxımdan ən çətin məqamlardan biri — uşağın evdən kənar gecələməsidir. Bu çağırışla işləmək üçün:</p>
          <ul>
            <li><strong>Pediatra desmopressin yazıdır</strong> — yalnız bu xüsusi hallar üçün, daimi yox</li>
            <li><strong>Vinil yataq qoruyucu çantaya qoyun</strong> — uşaq özü görmədən, lakin orada</li>
            <li><strong>Dostluq ailəsinə qabaqcadan deyin</strong> — uşaqdan xəbər vermədən, yalnız valideyn-valideyn</li>
            <li><strong>Cihaz aparmayın</strong> — bu uşağa daha çox utanc gətirə bilər</li>
            <li><strong>Yedək paltar gizli yerdə</strong> — ehtiyac olarsa</li>
          </ul>

          <h2>Yekun: Səbr — Ən Vacib Alət</h2>
          <p>Enurez müalicəsi 8-12 həftə davam edir. Bu illərlə əzab çəkməkdən qat-qat qısadır, lakin bu 12 həftə içində valideynin səbri sınanır. Vacib olan:</p>
          <ul>
            <li>Hər səhər yataqdan qalxmaq və "biz davam edirik" hissi</li>
            <li>Sıçrayışları yox, ümumi trayektoriyanı görmək</li>
            <li>Uşağa "biz komandayıq" mesajını saxlamaq</li>
            <li>Lazım gəldikdə peşəkar mütəxəssisdən kömək almaq</li>
          </ul>

          <p>Müalicə bitdikdə uşaq nəinki quru olur — özünə hörməti də artmış olur. Bu uzun müddətli psixoloji uğurdur.</p>""",
        "sources": """          <p><a href="https://www.nice.org.uk/guidance/cg111" target="_blank" rel="noopener">NICE Guideline CG111 — Bedwetting</a></p>
          <p><a href="https://www.aap.org/" target="_blank" rel="noopener">American Academy of Pediatrics — Family Guidance</a></p>
          <p>Caldwell, P. H., et al. (2020). Family-based interventions for bedwetting. <em>Pediatric Nephrology</em>, 35(3), 401-409.</p>
          <p>Butler, R. J., & Stenberg, A. (2001). Treatment of childhood nocturnal enuresis. <em>Acta Paediatrica</em>, 90(8), 875-881.</p>"""
    }
]

for art in ARTS:
    out = CHROME
    others = [a for a in ARTS if a["slug"] != art["slug"]][:3]
    related = "\n".join(CARD.format(slug=o["slug"], title=o["title"], excerpt=o["short"]) for o in others)
    af = dict(art); af["related"] = related
    for k, v in af.items():
        out = out.replace("{" + k + "}", str(v))
    (ROOT / art["slug"]).write_text(out, encoding="utf-8")
    print(f"WROTE: {art['slug']}")
print("Done.")
