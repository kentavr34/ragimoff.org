# -*- coding: utf-8 -*-
# Build 4 panik articles (2..5) from a single chrome + per-article body.
import os, pathlib

ROOT = pathlib.Path(r"C:\Users\SAM\Desktop\sayt2")

CHROME_HEAD = """<!doctype html>
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
      .triangle-box strong { color:var(--clr-heading); }
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
          <a href="tehsil.html#registration" class="nav-cta">QEYDİYYAT</a>
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
      <a href="tehsil.html#registration" class="btn btn-fill" onclick="toggleMenu()">QEYDİYYAT</a>
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
        <h2 class="sec-h2">Panik ataklardan əziyyət çəkirsiniz?</h2>
        <p class="sec-sub">Klinik psixoterapiya effektiv həll yolu verir</p>
        <div class="cta-band-btns">
          <a href="https://wa.me/994702200376" class="btn btn-fill" target="_blank">WhatsApp ilə Yazın</a>
          <a href="panik-ataklar.html" class="btn btn-line">Panik Ataklar</a>
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

ARTICLES = [
    {
        "slug": "blog-panik-2.html",
        "title": "Panik Atak Anında Beyində Nə Baş Verir?",
        "desc": "Amigdala, 'yalan həyəcan', simpatik sinir sistemi — panik atakın neyrobioloji mexanizmi. Kənan Rəhimov.",
        "read_time": 9,
        "cover": "images/blog/panik/art1-cover.jpg",
        "cover_alt": "Beyin və narahatlıq",
        "body": """          <p>Panik atak qəfildən gələn fiziki simptomlar fırtınasıdır: ürəkdöyüntüsü, nəfəs darlığı, başgicəllənmə, tərləmə, "öləcəyəm" hissi. Lakin bu fırtınanın mənbəyi nə ürəkdir, nə də ağciyər. Mənbə — beyində bir kiçik, qoz boyda strukturda yaşayır: <strong>amigdala</strong>.</p>

          <h2>Amigdala — Beynin Həyəcan Mərkəzi</h2>
          <p>Amigdala bədənin "təhlükə detektoru"dur. Onun funksiyası real təhlükəyə tez reaksiya vermək — fiziki olaraq qaçmaq və ya mübarizə aparmaq üçün bədəni hazırlamaqdır. Bu mexanizm <em>fight-or-flight</em> (mübarizə-qaç) adlanır və yüz minlərlə il bizim əcdadlarımızı pələngdən, ayıdan və düşməndən xilas edib.</p>

          <p>Problem: amigdala "real təhlükə" və "təsəvvür edilən təhlükə" arasında fərq qoymur. Real pələnq də, "ya başıma nəsə gələrsə" düşüncəsi də eyni reaksiyanı tetikleyə bilər. Panik pozğunluqda <strong>amigdala həssaslaşır</strong> — yalan həyəcanları daha asan və daha tez verir.</p>

          <h2>5 Saniyə İçində Bədəndə Nə Baş Verir?</h2>
          <p>Amigdala "təhlükə!" siqnalı verən kimi simpatik sinir sistemi aktivləşir. Aşağıdakı reaksiyalar 1-5 saniyə içində baş verir:</p>
          <ul>
            <li><strong>Adrenalin böyrəküstü vəzilərdən axır</strong> — qan dövranına</li>
            <li><strong>Ürək döyüntüsü 30-50 vurğu/dəq artır</strong> — qan əzələlərə daha tez çatdırılsın</li>
            <li><strong>Tənəffüs sürətlənir</strong> — bədənə daha çox oksigen daxil olsun</li>
            <li><strong>Qan əl-ayaqlardan iç orqanlara axır</strong> — keyimə hissi yaranır</li>
            <li><strong>Bəbəklər genişlənir</strong> — daha çox işıq qəbul etmək üçün</li>
            <li><strong>Həzm dayanır</strong> — qarın ağrısı, ürəkbulanma</li>
            <li><strong>Tər vəziləri açılır</strong> — bədən soyusun</li>
          </ul>

          <p>Bütün bu dəyişiklik <em>real bir təhlükə qarşısında</em> sizi xilas edə bilər. Lakin sakit-sakit metroda gedirkən və ya yataqda yatarkən baş verdikdə — bu reaksiya "pəncərədən düşmüşəm" hissi yaradır.</p>

          <h2>Niyə Bu "Yalan Həyəcan" Yaranır?</h2>
          <p>Amigdalanın artmış həssaslığı bir neçə amildən qaynaqlana bilər:</p>
          <ul>
            <li><strong>Genetik meyl</strong> — qohumlarında panik və ya narahatlıq pozğunluğu olanlarda risk 4-5 dəfə yüksəkdir</li>
            <li><strong>Uzunmüddətli stress</strong> — yüksək kortizol səviyyəsi amigdalanı "alarm rejimində" saxlayır</li>
            <li><strong>Travmatik təcrübələr</strong> — keçmiş travma amigdalanın "öyrədilmiş qorxu" şəbəkələrini güclü edir</li>
            <li><strong>Kafein, nikotin, alkoqolun çəkilmə dövrü</strong> — bədən simptomlarını tetikleyə bilər</li>
            <li><strong>Yuxu çatışmazlığı</strong> — prefrontal qabığın "fren" funksiyasını zəiflədir</li>
          </ul>

          <h2>Prefrontal Qabıq — Yetkin "Direktor"</h2>
          <p>Sağlam beyində <strong>prefrontal qabıq</strong> (alın hissəsindəki qabıq) amigdalaya nəzarət edir. O deyir: "Sakit ol, bu real təhlükə deyil — sadəcə kafe sallanır." Lakin panik atak başlayanda prefrontal qabığın səsi tutulur — amigdala özü-özünə qərar verir.</p>

          <p>Ekspozisiya terapiyası və KDT məhz bu balansı bərpa etməyə çalışır: prefrontal qabığa "amigdalanı oyatma" treninqi vermək.</p>

          <h2>Hücum Niyə 10-20 Dəqiqə Davam Edir?</h2>
          <p>Adrenalin böyrəküstü vəzilərdən atılan kimi bir-iki dəqiqə içində qan dövranı pikinə çatır. Daha sonra qaraciyər və böyrəklər onu metabolizə etməyə başlayır. <strong>Bədənin saatı belədir: 10-20 dəqiqə içində adrenalin tükənir, simptomlar yox olur</strong>.</p>

          <p>Yəni: <em>nə qədər çətin keçsə də, panik atak fizioloji olaraq özü keçir</em>. Bunu bilmək hücumla qarşılaşmağa kömək edir — "məcburi son" var.</p>

          <h2>Niyə Bu Bilik Müalicəyə Kömək Edir?</h2>
          <p>Panik dövrünün ən qorxunc hissəsi — naməlumluqdur. "Bu nədir? Niyə baş verir? Mən ölürmü?" Bu suallar atakı uzadır.</p>
          <p>Bilməklə bunlar dəyişir: "Bu adrenalin axınıdır. Amigdalam yalan həyəcan verir. Bədənim 10 dəqiqəyə bunu metabolizə edəcək. Mən təhlükədə deyiləm." Beləcə prefrontal qabıq amigdalaya nəzarəti geri qaytarır.</p>

          <p>Psikoeğitim — KDT-nin ilk addımıdır. Mexanizmi anlamaq olmadan texnikalar boş qalır.</p>""",
        "sources": """          <p><a href="https://www.nimh.nih.gov/health/publications/panic-disorder-when-fear-overwhelms" target="_blank" rel="noopener">NIMH — Panic Disorder: When Fear Overwhelms</a></p>
          <p><a href="https://www.apa.org/topics/anxiety/panic-disorder" target="_blank" rel="noopener">APA — Panic Disorder</a></p>
          <p>LeDoux, J. (2015). <em>Anxious: Using the Brain to Understand and Treat Fear and Anxiety</em>. Viking.</p>
          <p>Craske, M. G., & Barlow, D. H. (2014). <em>Mastery of Your Anxiety and Panic</em>. Oxford University Press.</p>""",
        "related": """          <a href="blog-panik.html" class="blog-card" style="text-decoration:none">
            <div class="blog-card-body">
              <span class="blog-card-cat">Klinik</span>
              <h3 class="blog-card-title">Panik Atak Anında Nə Etməli? — 3 Texnika</h3>
              <p class="blog-card-excerpt">Nəfəs, topraqlanma, qəbul.</p>
            </div>
          </a>
          <a href="blog-panik-3.html" class="blog-card" style="text-decoration:none">
            <div class="blog-card-body">
              <span class="blog-card-cat">Klinik</span>
              <h3 class="blog-card-title">Agorafobiya — Panik Atakdan Sosial Təcridə</h3>
              <p class="blog-card-excerpt">Qaçınma davranışı və həyat sahəsinin daralması.</p>
            </div>
          </a>
          <a href="blog-panik-4.html" class="blog-card" style="text-decoration:none">
            <div class="blog-card-body">
              <span class="blog-card-cat">Klinik</span>
              <h3 class="blog-card-title">KDT Panik Pozğunluqda Necə İşləyir?</h3>
              <p class="blog-card-excerpt">Mexanizm və effektivlik dəlilləri.</p>
            </div>
          </a>"""
    },
    {
        "slug": "blog-panik-3.html",
        "title": "Agorafobiya — Panik Atakdan Sosial Təcridə",
        "desc": "Agorafobiya nədir, panik pozğunluqla əlaqəsi, qaçınma davranışı və müalicə yolları. Kənan Rəhimov.",
        "read_time": 8,
        "cover": "images/blog/panik/art3-cover.jpg",
        "cover_alt": "Boş küçə",
        "body": """          <p>Agorafobiya yunan dilindən tərcümədə "bazar meydanı qorxusu" deməkdir. Lakin müasir klinik agorafobiya bazardan yox, <strong>qaça bilməyəcəyim vəziyyətdən</strong> qorxudur. Metro, market növbəsi, körpü, izdiham, hətta tək evdə qalmaq — agorafobiyalı insan üçün bunlar potensial tələdir.</p>

          <p>DSM-5 görə, agorafobiya əhalinin 1-2%-də rast gəlinir, qadınlarda 2 dəfə tez-tez. Ən kritik fakt: agorafobiyalı şəxslərin <strong>təxminən 50%-i panik pozğunluqla başlayır</strong>. Bu məqalədə bu zəncirin necə işlədiyini açırıq.</p>

          <h2>Necə Başlayır? Birinci Atak</h2>
          <p>Tipik tarix: gənc yetkin (25-35 yaş) həyatında ilk panik atakı yaşayır. Tez-tez bu kafedə, marketdə, metroda və ya küçədə baş verir. Atak qəflətən gəlir, "ölürəm" hissi və simptomlar 10-15 dəqiqə davam edir.</p>

          <p>Növbəti gün insan analiz edir: "Bu metroda baş verdi. Yenə metroda olarsa, eyni şey baş verə bilər. Onda qaça bilməyəcəyəm. Yaxşısı odur ki, metroya getməyim."</p>

          <p>Bu məqamda <strong>qaçınma</strong> başlayır. Və qaçınma — agorafobiyanın yanacağıdır.</p>

          <h2>Qaçınma Necə İşləyir?</h2>
          <p>İlk dəfə metroya getməməklə insan rahatlama hiss edir. "Atak olmadı." Bu rahatlama beyin tərəfindən belə qeyd olunur: "Metro = təhlükə. Qaçınma = təhlükəsizlik. Davam et."</p>

          <p>Növbəti həftə metro alternativi — taksi. Sonra taksi də narahat edir, çünki tıxacda qaça bilməzsən. İnsan yalnız evindən 1 km radiusda gəzir. Sonra 500 metrdə. Sonra evdən çıxmır.</p>

          <p>Bu prosesə <strong>qaçınma genişlənməsi</strong> deyilir. Hər qaçılan vəziyyət "təhlükə siyahısına" düşür və o siyahı zaman keçdikcə böyüyür.</p>

          <h2>"Təhlükəsizlik Davranışı" — Gizli Qaçınma</h2>
          <p>Açıq qaçınmadan başqa, gizli formalar var:</p>
          <ul>
            <li><strong>Yanında həmişə kimsə</strong> ("Tək çıxa bilmirəm, qardaşım hökmən gəlsin")</li>
            <li><strong>Su şüşəsi, dərmanlar, telefon</strong> — "təhlükəsizlik əşyaları"</li>
            <li><strong>Yalnız tanış marşrutla getmək</strong> — naməlum yer = potensial atak</li>
            <li><strong>Dərhal çıxa bilən yer seçmək</strong> — kinoda kənar yer, restoranın qapı yanı</li>
            <li><strong>Çox az yemək, az içmək</strong> — bədənin "fiziki simptomlarından" qorxmaq</li>
          </ul>

          <p>Bu davranışlar insana "kontrol" hissi verir. Lakin onlar problemi həll etmir — yalnız qorxunu sabitləşdirir.</p>

          <h2>Agorafobiyanın Həyata Təsiri</h2>
          <p>İrəli mərhələdə agorafobiya tam əlilliyə gətirir:</p>
          <ul>
            <li>İş itkisi (ofisə gedə bilməmək, müştəri görüşləri etməmək)</li>
            <li>Sosial təcrid (toya, doğum gününə getməmək)</li>
            <li>Tibbi yardımdan qaçınma (xəstəxana — qorxulu yer)</li>
            <li>Münasibət problemləri (tərəfdaş "azad-güzər kimi" işləməli)</li>
            <li>İkincili depressiya (50% halda agorafobiya depressiya ilə birlikdə gəlir)</li>
          </ul>

          <h2>Yaxşı Xəbər: Müalicəlik</h2>
          <p>Agorafobiya — psixoterapiya ilə effektiv həll olunan vəziyyətdir. Müalicə protokolu:</p>

          <p><strong>1. Psikoeğitim.</strong> Pasiyent panik və agorafobiyanın mexanizmini anlayır. "Bu mənim xarakterim deyil — bu öyrənilmiş davranışdır. Öyrənilən şey unudula bilər."</p>

          <p><strong>2. Hierarxiya tərtibi.</strong> Terapevtlə birlikdə qorxulu vəziyyətlər siyahısı tərtib edilir, hər birinə 1-100 narahatlıq balı verilir. Bu siyahı növbəti addımların yol xəritəsidir.</p>

          <p><strong>3. Tədricən ekspozisiya.</strong> Ən aşağı baldan başlayaraq pasiyent qorxulu vəziyyətlərə daxil olur. Məsələn: ilk həftə — evin qarşısında 5 dəqiqə dayanmaq. İkinci həftə — kvartalı dolaşmaq. Üçüncü — metroya bir dayanacaq getmək. Hər addım uğurla bitirilməlidir.</p>

          <p><strong>4. Təhlükəsizlik davranışlarının tədricən kənarlaşdırılması.</strong> Su şüşəsiz çıxmaq. Yanı kimsəsiz getmək. Dərmansız çıxmaq.</p>

          <p>Beck Institute və APA məlumatına görə, ekspozisiya terapiyası agorafobiyalı pasiyentlərin <strong>70-80%-də</strong> əhəmiyyətli yaxşılaşma verir. Müddət — 12-16 həftə.</p>

          <h2>Birinci Addım — Kömək İstəmək</h2>
          <p>Agorafobiyalı insanın ilk maneəsi tez-tez "terapevtə getmək"dir — çünki ofisə getmək özü qorxulu. Bu halda online terapiya — yaxşı başlanğıcdır. İlk seansları evdən etmək olar, sonra tədricən ofisə keçmək.</p>

          <p>Vacib: agorafobiya nə qədər tez müalicə olunsa, qaçınma siyahısı bir o qədər kiçik qalır. İllərlə təxir etmək — siyahını uzadır.</p>""",
        "sources": """          <p><a href="https://www.nimh.nih.gov/health/topics/agoraphobia" target="_blank" rel="noopener">NIMH — Agoraphobia</a></p>
          <p><a href="https://www.apa.org/ptsd-guideline/treatments/exposure-therapy" target="_blank" rel="noopener">APA — Exposure Therapy</a></p>
          <p><a href="https://beckinstitute.org/blog/cognitive-therapy-for-panic-and-agoraphobia/" target="_blank" rel="noopener">Beck Institute — Cognitive Therapy for Panic and Agoraphobia</a></p>
          <p>DSM-5: Agoraphobia (300.22), American Psychiatric Publishing, 2013.</p>""",
        "related": """          <a href="blog-panik.html" class="blog-card" style="text-decoration:none">
            <div class="blog-card-body">
              <span class="blog-card-cat">Klinik</span>
              <h3 class="blog-card-title">Panik Atak Anında Nə Etməli? — 3 Texnika</h3>
              <p class="blog-card-excerpt">Nəfəs, topraqlanma, qəbul.</p>
            </div>
          </a>
          <a href="blog-panik-2.html" class="blog-card" style="text-decoration:none">
            <div class="blog-card-body">
              <span class="blog-card-cat">Klinik</span>
              <h3 class="blog-card-title">Panik Atak Anında Beyində Nə Baş Verir?</h3>
              <p class="blog-card-excerpt">Amigdala, "yalan həyəcan", neyrobiologiya.</p>
            </div>
          </a>
          <a href="blog-panik-4.html" class="blog-card" style="text-decoration:none">
            <div class="blog-card-body">
              <span class="blog-card-cat">Klinik</span>
              <h3 class="blog-card-title">KDT Panik Pozğunluqda Necə İşləyir?</h3>
              <p class="blog-card-excerpt">Mexanizm və effektivlik dəlilləri.</p>
            </div>
          </a>"""
    },
    {
        "slug": "blog-panik-4.html",
        "title": "KDT Panik Pozğunluqda Necə İşləyir?",
        "desc": "Koqnitiv-Davranış Terapiyası panik atakların müalicəsində — mexanizm, alətlər və effektivlik dəlilləri. Kənan Rəhimov.",
        "read_time": 10,
        "cover": "images/blog/panik/art4-cover.jpg",
        "cover_alt": "Terapiya seansı",
        "body": """          <p>Panik pozğunluq üçün NICE (Britaniya) və APA (ABŞ) qaydalarının hər ikisi <strong>Koqnitiv-Davranış Terapiyasını (KDT)</strong> birinci xətt müalicəsi kimi tövsiyə edir. Ekspozisiya terapiyası və interocepetiv ekspozisiya elementləri ilə birlikdə KDT 12-16 həftə ərzində <strong>pasiyentlərin 80%-də əhəmiyyətli yaxşılaşma</strong> verir (Barlow et al., 2000).</p>

          <p>Bu məqalədə KDT-nin panik üçün xüsusi protokolunu açırıq: hansı düşüncələr işlənilir, hansı texnikalar tətbiq olunur, müalicə necə qurulur.</p>

          <h2>Panik Dövrü — KDT Modeli</h2>
          <p>Clark (1986) və Beck (1985) tədqiqatlarından əldə edilmiş "panik dövrü" modeli aşağıdakı kimidir:</p>

          <div class="triangle-box">
            <strong>Tetikleyici</strong> (məs. ürək döyüntüsü artıb)<br>
            ↓<br>
            <strong>Yanlış şərh</strong> ("ürək tutması keçirirəm")<br>
            ↓<br>
            <strong>Qorxu</strong><br>
            ↓<br>
            <strong>Bədən simptomlarının güclənməsi</strong> (adrenalin axır)<br>
            ↓<br>
            <strong>Şərh güclənir</strong> ("hə, ölürəm")<br>
            ↓<br>
            <strong>Tam panik atak</strong>
          </div>

          <p>KDT-nin əsas məqsədi — bu döngünün <strong>"yanlış şərh"</strong> mərhələsində kəsilməsidir. Beləliklə zəncir başlamaz.</p>

          <h2>Komponent 1: Psikoeğitim</h2>
          <p>İlk 1-2 seans — pasiyent panik mexanizmini tam başa düşür. "Mən niyə ölmürəm?" sualına elmi cavab verilir. Amigdala, prefrontal qabıq, adrenalin, parasempatik sistem — bütün bunlar müzakirə olunur.</p>

          <p>Bu addım vacibdir, çünki "naməlumluq qorxusu" panikın əsas yanacağıdır. Mexanizmi bilən pasiyent qorxudan azad olur — qismən.</p>

          <h2>Komponent 2: Düşüncə Yenidən Quruluşu</h2>
          <p>Pasiyent gündəlik aparmağa başlayır: hansı vəziyyətdə hansı simptom yarandı, hansı düşüncə oldu. Tipik panik düşüncələri:</p>
          <ul>
            <li>"Ürəyim dayanır" — əslində: "ürəyim artıq adrenalindən sürətlənib"</li>
            <li>"Boğuluram" — əslində: "tez-tez nəfəs alıram, oksigen artıqdır"</li>
            <li>"Ağılımı itirirəm" — əslində: "qan beynimə axdığı üçün dərinmə hissi var"</li>
            <li>"Qaça bilmirəm, tələdə" — əslində: "qapı 3 metrdədir, çıxmaq mümkündür"</li>
          </ul>

          <p>Terapevt sual verir: "Bu düşüncəni hansı dəlil təsdiqləyir? Hansı dəlil təkzib edir? Real ehtimalı nədir?" Pasiyent öz düşüncələrini "<strong>fakt</strong>" yox, "<strong>ehtimal</strong>" kimi görməyə öyrənir.</p>

          <h2>Komponent 3: Interocepetiv Ekspozisiya</h2>
          <p>Bu KDT-nin panik üçün xüsusi alətdir. Pasiyent qorxulu fiziki simptomları məqsədli şəkildə özündə yaradır — və onlardan "qorxmamağı" öyrənir.</p>

          <ul>
            <li><strong>Hiperventilyasiya məşqi</strong> — 60 saniyə tez-tez nəfəs almaq (başgicəllənmə yaranır)</li>
            <li><strong>Yerində fırlanmaq</strong> — başgicəllənmənin "qorxulu" deyil, sadə fizioloji reaksiya olduğunu göstərir</li>
            <li><strong>Stol üstündə nəfəs tutmaq</strong> — boğulma hissini simulyasiya edir</li>
            <li><strong>Saatlarla pilləkənlə qalxmaq</strong> — ürək döyüntüsünün qorxulu olmadığını sübut edir</li>
          </ul>

          <p>Bu məşqlər pasiyentə öyrədir: "Bu simptomlar mənə ziyan vermir. Bədənim bunları müntəzəm yaşadığında belə təhlükəsizdir."</p>

          <h2>Komponent 4: In Vivo Ekspozisiya</h2>
          <p>Agorafobiya komponenti varsa (panikın 50% halda olur), real-dünya ekspozisiyası başlayır. Hierarxiya tərtib olunur — ən az qorxulu (5/100) -dan ən çox qorxulu (100/100) vəziyyətə qədər.</p>

          <p>Misal hierarxiya:</p>
          <ul>
            <li>5/100 — Evin qarşısında 5 dəqiqə dayanmaq</li>
            <li>20/100 — Marketə tək getmək (boş saatda)</li>
            <li>40/100 — Marketdə növbədə dayanmaq (məşğul saatda)</li>
            <li>60/100 — Metroya 1 dayanacaq getmək</li>
            <li>80/100 — Metroya 5 dayanacaq getmək</li>
            <li>100/100 — Pik saatda metroda başqa şəhərdən qayıtmaq</li>
          </ul>

          <p>Hər addım dəfələrlə tətbiq edilir — narahatlıq normal səviyyəyə düşənə qədər.</p>

          <h2>Komponent 5: Təhlükəsizlik Davranışlarının Aradan Qaldırılması</h2>
          <p>Su şüşəsi, telefon, tablet — bunlar ekspozisiya zamanı tədricən kənarlaşdırılır. "Mən onsuz da bunu öhdəsindən gəlirəm" inancı qurulur.</p>

          <h2>Müddət və Effektivlik</h2>
          <p>Standart KDT protokolu — 12-16 həftəlik seans, gündəlik ev tapşırığı ilə. Beck Institute və Mayo Clinic tədqiqatlarına görə:</p>
          <ul>
            <li>12 həftədən sonra — pasiyentlərin 80%-də panik tezliyi 50%-dən çox azalır</li>
            <li>1 ildən sonra — pasiyentlərin 70%-i tam remissiyada qalır</li>
            <li>Yalnız medikament ilə müalicədə olanlarda residiv riski 50% — KDT alanlarda 20%</li>
          </ul>

          <p>KDT-nin üstünlüyü: <strong>biliyi və alətləri</strong> verir. Müalicədən sonra residivdə pasiyent öz-özünə müdaxilə edə bilir.</p>

          <h2>Kim üçün KDT Uyğun Deyil?</h2>
          <p>Çox az hal var. Əgər panik ataklar:</p>
          <ul>
            <li>Tibbi xəstəlik (hipertireoz, hipoqlikemiya, ürək aritmiyası) tərəfindən tətiklənirsə — əvvəlcə tibbi müalicə</li>
            <li>Çox şiddətli depressiya ilə birlikdədirsə — antidepressant + KDT kombinasiyası</li>
            <li>Aktiv alkoqol/narkotik istifadəsi ilə birlikdədir — əvvəlcə bağımlılıq müalicəsi</li>
          </ul>

          <p>Qalan əksər hallarda KDT — birinci seçim, ən etibarlı yoldur.</p>""",
        "sources": """          <p><a href="https://www.nice.org.uk/guidance/cg113" target="_blank" rel="noopener">NICE Guideline CG113 — Generalised Anxiety Disorder and Panic Disorder</a></p>
          <p><a href="https://beckinstitute.org/blog/cognitive-therapy-for-panic-and-agoraphobia/" target="_blank" rel="noopener">Beck Institute — Cognitive Therapy for Panic</a></p>
          <p>Clark, D. M. (1986). A cognitive approach to panic. <em>Behaviour Research and Therapy</em>, 24(4), 461-470.</p>
          <p>Barlow, D. H., et al. (2000). Cognitive-behavioral therapy, imipramine, or their combination for panic disorder. <em>JAMA</em>, 283(19), 2529-2536.</p>
          <p>Craske, M. G., & Barlow, D. H. (2014). <em>Mastery of Your Anxiety and Panic</em>. Oxford University Press.</p>""",
        "related": """          <a href="blog-panik.html" class="blog-card" style="text-decoration:none">
            <div class="blog-card-body">
              <span class="blog-card-cat">Klinik</span>
              <h3 class="blog-card-title">Panik Atak Anında Nə Etməli? — 3 Texnika</h3>
              <p class="blog-card-excerpt">Nəfəs, topraqlanma, qəbul.</p>
            </div>
          </a>
          <a href="blog-panik-2.html" class="blog-card" style="text-decoration:none">
            <div class="blog-card-body">
              <span class="blog-card-cat">Klinik</span>
              <h3 class="blog-card-title">Panik Atak Anında Beyində Nə Baş Verir?</h3>
              <p class="blog-card-excerpt">Amigdala, "yalan həyəcan", neyrobiologiya.</p>
            </div>
          </a>
          <a href="blog-panik-5.html" class="blog-card" style="text-decoration:none">
            <div class="blog-card-body">
              <span class="blog-card-cat">Klinik</span>
              <h3 class="blog-card-title">Panik Ataklarla Bağlı 7 Mif</h3>
              <p class="blog-card-excerpt">Ümumi yanlış inanclar və elmi cavablar.</p>
            </div>
          </a>"""
    },
    {
        "slug": "blog-panik-5.html",
        "title": "Panik Ataklarla Bağlı 7 Mif və Elmi Cavablar",
        "desc": "Panik atak xarakter zəifliyi deyil, dərman ömürlük verilmir, məşq zərərli deyil — yayılmış miflər və elmi cavablar.",
        "read_time": 7,
        "cover": "images/blog/panik/art5-cover.jpg",
        "cover_alt": "Suallar",
        "body": """          <p>Panik atak xarakter zəifliyi deyil, qadın "uydurması" deyil, "öz-özünə keçən mərhələ" deyil. Bu məqalədə ən çox yayılmış 7 mifə baxırıq və hər birinə dəlilə əsaslanan cavab veririk.</p>

          <h2>Mif 1: "Panik atak yalnız qadınlarda olur"</h2>
          <p><strong>Yalan.</strong> Statistik olaraq qadınlarda 2 dəfə tez-tez rast gəlinir, lakin <strong>kişilərin də 3-5%-i həyatı boyu panik pozğunluqdan əziyyət çəkir</strong> (NIMH məlumatı). Kişilərdə tez-tez "diaqnoz qoyulmur" çünki onlar yardım istəməyə daha az meyillidirlər. Kişilərdə panik atak tez-tez "ürək problemi" və ya "təzyiq dəyişiklikləri" şəklində maskalanır.</p>

          <h2>Mif 2: "Panik atakdan ölə bilərsən"</h2>
          <p><strong>Yalan.</strong> Panik atak sırasında baş verən fizioloji dəyişikliklər (sürətli ürək, hiperventilyasiya, tərləmə) sağlam bir orqanizmə ziyan vurmur. Sürətli ürək döyüntüsü (160-180/dəq) idmançı qaçışı zamanı normaldır. Bədəniniz bunu emal edə bilər.</p>
          <p>İstisna: əgər mövcud ciddi ürək xəstəliyi varsa (məs. uzunmüddətli aritmiya), panik atak əlavə yük ola bilər. Lakin sağlam yetkin üçün — panik atak təhlükəsizdir.</p>

          <h2>Mif 3: "Panik atak ağılımı itirməyə aparır"</h2>
          <p><strong>Yalan.</strong> Panik atak şizofreniya, psixoz və ya hər hansı psixiki xəstəliyə çevrilməz. "Dərinmə" hissi (depersonalization/derealization) panik dövrünün simptomudur — beyinə qan paylanmasının dəyişməsindən qaynaqlanır. Atak bitəndən sonra tam normal qayıdır.</p>
          <p>Tədqiqatlar (Roy-Byrne et al., 2008) göstərir ki, panik pozğunluqdan psixoz, dementia və ya digər ciddi pozğunluqlara çevrilmə yoxdur.</p>

          <h2>Mif 4: "Panik atak xarakter zəifliyidir"</h2>
          <p><strong>Yalan.</strong> Panik pozğunluq <strong>neyrobioloji vəziyyətdir</strong>. Genetik faktorlar (ailədə narahatlıq pozğunluğu olanlarda risk 4-5 dəfə yüksəkdir), beyin kimyası (serotonin, GABA balansı), travmatik təcrübələr — hamısı rol oynayır. Heç bir əlaqə "iradə zəifliyi" və ya "xarakter qüsuru" ilə yoxdur.</p>
          <p>Müqayisə: kimsə diabetdən əziyyət çəkdiyində ona "iradəsiz" demirik. Panik pozğunluqda da eyni standart tətbiq olunmalıdır.</p>

          <h2>Mif 5: "Dərman ömürlük verilməlidir"</h2>
          <p><strong>Yalan.</strong> Panik pozğunluqda dərman müalicəsi — tipik 6-12 ay arası. SSRI tipli antidepressantlar (sertralin, paroksetin) və SNRI-lar uzun müddət istifadə olunur, sonra tədricən kənarlaşdırılır. Benzodiazepinlər (alprazolam) — yalnız qısamüddətli istifadə üçün, asılılıq riski səbəbindən.</p>
          <p>NICE qaydalarına görə, KDT psixoterapiya alanlar dərman olmadan da uğurlu nəticə əldə edə bilirlər (50%-dən çox hallarda). Qərar individualdır — hər pasiyent üçün ayrıca planlaşdırılır.</p>

          <h2>Mif 6: "Fiziki məşq zərərlidir, ürək döyüntüsünü artırır"</h2>
          <p><strong>Tam əksinə — fiziki məşq panik üçün təbii anti-anksietik müalicədir.</strong> Cochrane (2013) meta-analizi göstərib ki:</p>
          <ul>
            <li>Həftədə 3 dəfə 30 dəq aerobik məşq panik tezliyini 30-40% azaldır</li>
            <li>Məşqdən sonra serotonin və endorfin səviyyəsi artır</li>
            <li>Müntəzəm məşq amigdalanın həssaslığını azaldır</li>
          </ul>
          <p>Bonus: müntəzəm məşq insanı bədəninin sürətli ürək döyüntüsünə "öyrəşdirir" — interocepetiv ekspozisiya kimi işləyir.</p>

          <h2>Mif 7: "Panik atak öz-özünə keçər"</h2>
          <p><strong>Yarım yalan.</strong> Tək bir panik atak — bəli, bəzən təkrarlanmadan keçir (cəmi 25-30% halda). Lakin <strong>panik pozğunluq</strong> (yəni təkrarlanan ataklar) müalicə olunmadığı təqdirdə aşağıdakıların ehtimalını yüksəldir:</p>
          <ul>
            <li>Agorafobiya inkişafı (50%-ə qədər)</li>
            <li>İkincili depressiya (30-50%)</li>
            <li>Alkoqol/narkotik istifadəsi (özü-müalicəsi cəhdi)</li>
            <li>İş itkisi və sosial təcrid</li>
          </ul>
          <p>Erkən müalicə — daha qısa, daha effektiv. 5 il "öz-özünə gedər" gözləyən insan tez-tez 5 il sonra daha mürəkkəb klinik şəkillə gəlir.</p>

          <h2>Yekun: Doğru Bilik — İlk Müalicə Addımıdır</h2>
          <p>Mifləri kənarlaşdırmaq panik pozğunluqdan əziyyət çəkənlər üçün rahatlıq verir: "Mən tək deyiləm. Bu xarakterimdə qüsur deyil. Bu vəziyyət öyrənilə və müalicə oluna bilər."</p>
          <p>Əgər siz və ya yaxınınız panik atakdan əziyyət çəkirsə — kömək istəmək zəiflik deyil, məsuliyyətdir. Sınıq qol kimi — özündən sağalmaz, lakin doğru müalicə ilə tam bərpa olunur.</p>""",
        "sources": """          <p><a href="https://www.nimh.nih.gov/health/statistics/panic-disorder" target="_blank" rel="noopener">NIMH — Panic Disorder Statistics</a></p>
          <p><a href="https://www.cochrane.org/CD004366/DEPRESSN_exercise-for-anxiety-disorders" target="_blank" rel="noopener">Cochrane Review — Exercise for Anxiety Disorders</a></p>
          <p>Roy-Byrne, P. P., et al. (2008). Panic disorder. <em>The Lancet</em>, 371(9606), 1085-1098.</p>
          <p>Stubbs, B., et al. (2017). An examination of the anxiolytic effects of exercise. <em>Psychiatry Research</em>, 249, 102-108.</p>""",
        "related": """          <a href="blog-panik.html" class="blog-card" style="text-decoration:none">
            <div class="blog-card-body">
              <span class="blog-card-cat">Klinik</span>
              <h3 class="blog-card-title">Panik Atak Anında Nə Etməli? — 3 Texnika</h3>
              <p class="blog-card-excerpt">Nəfəs, topraqlanma, qəbul.</p>
            </div>
          </a>
          <a href="blog-panik-3.html" class="blog-card" style="text-decoration:none">
            <div class="blog-card-body">
              <span class="blog-card-cat">Klinik</span>
              <h3 class="blog-card-title">Agorafobiya — Panik Atakdan Sosial Təcridə</h3>
              <p class="blog-card-excerpt">Qaçınma davranışı və həyat sahəsinin daralması.</p>
            </div>
          </a>
          <a href="blog-panik-4.html" class="blog-card" style="text-decoration:none">
            <div class="blog-card-body">
              <span class="blog-card-cat">Klinik</span>
              <h3 class="blog-card-title">KDT Panik Pozğunluqda Necə İşləyir?</h3>
              <p class="blog-card-excerpt">Mexanizm və effektivlik dəlilləri.</p>
            </div>
          </a>"""
    }
]

for art in ARTICLES:
    out = CHROME_HEAD
    for k, v in art.items():
        out = out.replace("{" + k + "}", str(v))
    path = ROOT / art["slug"]
    path.write_text(out, encoding="utf-8")
    print(f"WROTE: {art['slug']} ({len(out)} bytes)")

print("Done.")
