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
        <span class="badge">AİLƏ TERAPİYASI</span>
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
        <h2 class="sec-h2">Ailə terapiyası lazımdır?</h2>
        <p class="sec-sub">İlk konsultasiyada yol xəritəsini birlikdə qururuq</p>
        <div class="cta-band-btns">
          <a href="https://wa.me/994702200376" class="btn btn-fill" target="_blank">WhatsApp ilə Yazın</a>
          <a href="aile-terapiyasi.html" class="btn btn-line">Ailə Terapiyası</a>
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

CARD_TPL = """          <a href="{slug}" class="blog-card" style="text-decoration:none">
            <div class="blog-card-body">
              <span class="blog-card-cat">Ailə</span>
              <h3 class="blog-card-title">{title}</h3>
              <p class="blog-card-excerpt">{excerpt}</p>
            </div>
          </a>"""

ARTS = [
    {
        "slug": "blog-aile.html",
        "title": "Ailə Münaqişəsini Həll Etmənin 5 Prinsipi",
        "desc": "Cütlük münaqişələrini həll etmək üçün Gottman İnstitutu və KDT əsaslı 5 prinsip. Kənan Rəhimov.",
        "read_time": 9,
        "cover": "images/blog/aile/art4-cover.jpg",
        "cover_alt": "Cütlük danışır",
        "short": "Münaqişə döngüsünü qırmaq üçün 5 elmi prinsip — Gottman və KDT əsaslı.",
        "body": """          <p>Ailədə münaqişənin olmaması ailənin sağlam olduğunu göstərmir. Tədqiqatlar göstərir ki, <strong>uğurlu cütlüklər də münaqişə edirlər — sadəcə fərqli şəkildə</strong>. John Gottman İnstitutunun 40 illik araşdırmaları "yaxşı" və "pozulan" cütlükləri ayıran 5 prinsipi müəyyənləşdirib.</p>

          <p>Bu prinsiplər boşanma riskini 90% dəqiqliklə proqnozlaşdırır. Hər biri öyrənilə bilər — yəni "uyğunsuzluq" yox, alət çatışmazlığı problemi.</p>

          <h2>Prinsip 1: 5:1 Nisbəti</h2>
          <p>Sağlam cütlüklərdə hər mənfi qarşılıqlı təsirə (eleştiri, kobud baxış) <strong>5 müsbət</strong> qarşılıqlı təsir düşür: təşəkkür, gülüş, toxunma, dəstək, "səni sevirəm". Pozulan cütlüklərdə bu nisbət 1:1 və ya daha da mənfidir.</p>

          <p>Ev məşqi: bir gün ərzində partnyora 5 müsbət şey deyin — kiçik də olsa. Hər gecə 6 dəqiqə "günün ən yaxşı 3 anı" haqqında danışın. Bu sadə vərdiş 8 həftədə əlaqəni dəyişdirə bilər.</p>

          <h2>Prinsip 2: 4 Dəhşətli Atlı</h2>
          <p>Gottman boşanmaya gətirən 4 davranışı "Apokalipsisin 4 atlısı" adlandırıb:</p>
          <ul>
            <li><strong>Tənqid</strong> ("sən həmişə..." yox, "mən narahat oluram, çünki...")</li>
            <li><strong>Müdafiə</strong> ("amma sən özün də...")</li>
            <li><strong>Saymamazlıq</strong> (ən təhlükəli — gözqamaşma, masqaramaz tonu)</li>
            <li><strong>Divar</strong> (susmaq, otaqdan çıxmaq, mövzunu dəyişmək)</li>
          </ul>
          <p>Bu davranışlar partnyora "sən pissən" mesajı göndərir. Onları əvəz etmək üçün: <em>tənqid → şikayət</em>, <em>müdafiə → məsuliyyət</em>, <em>saymamazlıq → hörmət</em>, <em>divar → fasilə</em>.</p>

          <h2>Prinsip 3: Yumşaq Başlanğıc</h2>
          <p>Gottman tədqiqatları: söhbətin <strong>ilk 3 dəqiqəsi</strong> 96% dəqiqliklə nəticəsini proqnozlaşdırır. Sərt başlanğıc ("həmişə kobudsan!") sərt sonluğa aparır. Yumşaq başlanğıc ("məni narahat eden bir şey var, danışa bilərikmi?") konstruktiv həllə.</p>

          <p>Düstur: "Mən" + "hiss edirəm" + "konkret hal" + "ehtiyacım". Misal: "Mən özümü yalnız hiss edirəm, axşamlar telefonda qaldığında. Birlikdə vaxt keçirməyə ehtiyacım var."</p>

          <h2>Prinsip 4: Təmir Cəhdləri</h2>
          <p>Münaqişə zamanı hər iki tərəf "isinmiş" olur. Sağlam cütlüklər <strong>təmir cəhdləri</strong> edir: zarafat, "fasilə verək", əli toxutmaq, "səni sevirəm", "doğrudur". Bu siqnalları görüb qəbul etmək — onları görməzlikdən gəlmək yox.</p>
          <p>Tədqiqat: uğurlu cütlüklərdə təmir cəhdlərinin <strong>86%-i qəbul edilir</strong>. Boşanan cütlüklərdə — yalnız 33%.</p>

          <h2>Prinsip 5: Həll Olunmayan Problemlərlə Yaşamaq</h2>
          <p>Cütlük problemlərinin <strong>69%-i həll olunmazdır</strong>. Bunlar fundamental fərqlər (uşaq sayı, dindarlıq, pul ilə münasibət, ailə üzvləri ilə əlaqə) ilə bağlıdır. Sağlam cütlüklər onları "həll" etməyə çalışmırlar — onlar haqqında <strong>davam edən söhbət aparırlar</strong>.</p>

          <p>Strategiya: "biz bunu razılaşdırmadıq, lakin bir-birimizin baxış nöqtəsini başa düşməyə çalışırıq" — bu sağlam münasibətdir. "Yenə eyni mövzu, mənası yoxdur" — pozulanın əlamətidir.</p>

          <h2>Nə Vaxt Terapevt Lazımdır?</h2>
          <p>Bu prinsipləri tək başına tətbiq etmək çətin ola bilər. Ailə terapiyası lazım ola biləcək siqnallar:</p>
          <ul>
            <li>Saymamazlıq mərhələsindəyik (ən mühüm xəbərdarlıq)</li>
            <li>Eyni mövzularda 6 aydan çox müzakirəsiz</li>
            <li>Bir tərəf ayrılma haqqında düşünür</li>
            <li>Uşaqlar münaqişələrdən təsirlənməyə başlayıb</li>
            <li>Cinsi və emosional yaxınlıq tamamilə yoxdur</li>
          </ul>
          <p>Erkən müdaxilə — ən effektiv. Pozulmuş münasibəti bərpa etmək sağlam münasibəti möhkəmlətməkdən çox-çox qat çətindir.</p>""",
        "sources": """          <p><a href="https://www.gottman.com/about/the-research/" target="_blank" rel="noopener">Gottman Institute — The Research</a></p>
          <p><a href="https://www.aamft.org/Consumer_Updates/Marriage_and_Family_Therapy.aspx" target="_blank" rel="noopener">AAMFT — Marriage and Family Therapy</a></p>
          <p>Gottman, J., & Silver, N. (2015). <em>The Seven Principles for Making Marriage Work</em>. Harmony.</p>
          <p>Gottman, J. M., et al. (1998). Predicting marital happiness from newlywed interactions. <em>Journal of Marriage and Family</em>, 60(1), 5-22.</p>"""
    },
    {
        "slug": "blog-aile-2.html",
        "title": "Toksik Münasibətin 7 Əlaməti",
        "desc": "Tənqid, manipulyasiya, izolyasiya — sağlam və toksik münasibəti ayıran 7 klinik əlamət. Kənan Rəhimov.",
        "read_time": 8,
        "cover": "images/blog/aile/art2-cover.jpg",
        "cover_alt": "Mübahisə edən cütlük",
        "short": "Sağlam və toksik münasibəti ayıran 7 klinik əlamət və çıxış yolu.",
        "body": """          <p>"Toksik münasibət" termin sosial mediada çox işlədilir, lakin klinik mənası dəqiqdir. APA tərifi: <em>partnyorlardan birinin və ya hər ikisinin emosional, fiziki və ya psixoloji rifahını sistemli şəkildə pozan münasibət</em>.</p>

          <p>Aşağıdakı 7 əlamət — psixoloqlar tərəfindən tanınan klinik markerlərdir. Bir əlamət — narahatlıq səbəbidir. 3-dən çoxu — peşəkar müdaxilə zərurətidir.</p>

          <h2>1. Daimi Tənqid</h2>
          <p>Sağlam münasibətdə şikayət konkretdir: "qabları yumadın". Toksikdə tənqid xarakter haqqındadır: "sən həmişə tənbəlsən, heç vaxt heç nə etmirsən". Bu fərq nəzəri deyil — birinci cümlə davranışı dəyişdirir, ikincisi öz dəyəri haqqında inanc qurur.</p>

          <h2>2. Manipulyasiya və "Gaslighting"</h2>
          <p>Gaslighting — partnyorun gerçəkliyə inamını sarsıdmaq. "Bunu söyləməmişəm", "həmişə həddindən çox şişirdirsən", "sən paranoyaksan" — bu fraza sayında işlədilirsə, qızıl xəbərdarlıq bayrağıdır. Tədqiqatlar göstərir ki, gaslighting qurbanları zaman keçdikcə öz hissləri və yaddaşına inanmırlar.</p>

          <h2>3. İzolyasiya</h2>
          <p>"Dostların pis təsir edir", "anan-bacıların qarışmasın", "yalnız sən və mən kifayətik". Sağlam münasibət partnyoru sosial dünyaya bağlamır — onu açır. İzolyasiya — domestic abuse-un erkən mərhələsidir.</p>

          <h2>4. Maliyyə Kontrolu</h2>
          <p>"Sənin pulunu mən idarə edəcəm", "kartı mənə ver", "hesabat ver hansı pulu nə üçün xərcləyirsən". Sağlam münasibətdə şəffaflıq olur — kontrol yox. Maliyyə təcrid potensial qurbanı çıxış imkanlarından məhrum edir.</p>

          <h2>5. Aşağılamaq və Saymamazlıq</h2>
          <p>Gözqamaşma, masqaramaz ton, "hə dəlisən bu dünyaya", başqalarının yanında həqarət. Saymamazlıq — Gottman tədqiqatlarına görə boşanmanı ən çox proqnozlaşdıran əlamətdir. O, partnyoru "aşağı varlıq" kimi konstruktlaşdırır.</p>

          <h2>6. "Vinə-cıvələmək" Dövrü</h2>
          <p>Münaqişədən sonra hər şeyə görə partnyor günahlandırılır — hətta görkəmli haqsız vəziyyətlərdə. "Sən məni belə eddin", "mən deyildim, sən idin", "sənin günahındır ki, mən belə hərəkət edirəm". Bu — məsuliyyətin tam köçürülməsidir.</p>

          <h2>7. Fiziki və ya Cinsi Təcavüz</h2>
          <p>Bu — qara xətdir. Bir tək hadisə də — yetərlidir. İlk fiziki təcavüz ən mühüm xəbərdarlıq siqnalıdır. Statistik olaraq, "ağıl" alındığı təqdirdə də 80% halda 1 il ərzində təkrarlanır.</p>

          <h2>Tərk Etmə Niyə Çətindir?</h2>
          <p>Toksik münasibət "qaynar palçıq" kimi işləyir — tədricən qızdırılır. Qurban getdikcə daha az fərq edir. Bunun səbəbi:</p>
          <ul>
            <li><strong>Trauma bağı</strong> — qarışıq pozitiv və neqativ qarşılıqlı təsir güclü emosional bağ yaradır</li>
            <li><strong>Self-esteem aşınması</strong> — il sonra qurban "məndən başqası dözməz" inancına gəlir</li>
            <li><strong>İzolyasiya</strong> — kömək edə biləcək insanlar artıq həyatda yoxdur</li>
            <li><strong>Maliyyə asılılığı</strong> — getmək praktik mümkün deyil</li>
            <li><strong>Uşaqlar</strong> — "uşaqları görməyim azalar" qorxusu</li>
          </ul>

          <h2>Çıxış: Addım-Addım Plan</h2>
          <ol>
            <li><strong>Etibarlı bir adamla danışın</strong> — yaxın dost, qohum, terapevt. İzolyasiyanı sındırın.</li>
            <li><strong>Sənədləri toplayın</strong> — şəxsiyyət, bank, sığorta, uşaqların sənədləri.</li>
            <li><strong>Maliyyə müstəqilliyi planı qurun</strong> — gizli bank hesabı, ehtiyat pul.</li>
            <li><strong>Təhlükəsiz yer hazırlayın</strong> — qaldığa biləcək bir yer əvvəlcədən bilinsin.</li>
            <li><strong>Peşəkar yardım alın</strong> — terapevt, hüquqşünas, qadın hüquqları təşkilatları.</li>
          </ol>

          <p>Toksik münasibətdən çıxmaq — bir gecədə baş verən qərar deyil. Bu — aylar boyu davam edən proses. Lakin hər addım önəmlidir.</p>""",
        "sources": """          <p><a href="https://www.apa.org/topics/violence/intimate-partner" target="_blank" rel="noopener">APA — Intimate Partner Violence</a></p>
          <p><a href="https://www.who.int/news-room/fact-sheets/detail/violence-against-women" target="_blank" rel="noopener">WHO — Violence Against Women</a></p>
          <p>Stark, E. (2009). <em>Coercive Control: How Men Entrap Women in Personal Life</em>. Oxford University Press.</p>
          <p>Walker, L. E. (2017). <em>The Battered Woman Syndrome</em> (4th ed.). Springer Publishing.</p>"""
    },
    {
        "slug": "blog-aile-3.html",
        "title": "Boşanma Astanasında Ailə — Müalicə vs Ayrılıq",
        "desc": "Boşanma qərarından əvvəl son cəhd: hansı ailələr qurtarmağa dəyər, hansılar yox. Klinik kriteriyalar.",
        "read_time": 9,
        "cover": "images/blog/aile/art3-cover.jpg",
        "cover_alt": "Cütlük gün batımında",
        "short": "Hansı ailələri qurtarmaq mümkündür, hansılar yox? Klinik kriteriyalar və qərar matrisi.",
        "body": """          <p>"Mən hələ də onu sevirəm, lakin əziyyət çəkirəm. Boşanmalıyammı?" — ailə terapevtinə ən tez-tez verilən sual budur. Cavab universal deyil. Bəzi ailələr terapiya ilə tam bərpa olunur. Bəziləri — yalnız ayrılıqla, hər iki tərəf üçün yaxşı olur.</p>

          <p>Bu məqalədə klinik kriteriyalar verilir — qaranquşların qaranlıq düşüncələri yox, dəlilə əsaslanan markerlər.</p>

          <h2>Ailə Qurtarıla Bilər Əgər...</h2>
          <ul>
            <li><strong>Hər iki tərəf işə hazırdır.</strong> Tək bir tərəfin motivasiyası kifayət deyil. Terapiyaya yalnız "məni saxlasın deyə" gələn partnyorla əhəmiyyətli irəliləyiş çətindir.</li>
            <li><strong>Bazis hörmət qalıb.</strong> Saymamazlıq və masqaramaz ton səviyyəsindən aşağı. Cütlük "siz" forması işlətsə də, hələ də bir-birini insan kimi görür.</li>
            <li><strong>Müsbət xatirələr xatırlanır.</strong> "Niyə evləndik?" sualına müsbət cavab var. Münaqişə dövründə yaxşı dövrlər unudulmayıb.</li>
            <li><strong>Kommunikasiya problemləri əsas problemdir.</strong> Münaqişə tezliyi yüksək, lakin onun əsasında "qulağ verə bilməmək", "ifadə edə bilməmək" durur — fundamental fərqlər deyil.</li>
            <li><strong>Cinsi və emosional yaxınlıq əldə edilə bilən səviyyədədir.</strong> Tamamilə yox deyil — sadəcə zədələnmiş.</li>
          </ul>

          <p>Bu hallarda intensiv ailə terapiyası (12-20 seans) əksər vaxt vəziyyəti dəyişdirir.</p>

          <h2>Ayrılıq Daha Yaxşı Ola Bilər Əgər...</h2>
          <ul>
            <li><strong>Fiziki və ya cinsi təcavüz var.</strong> Bu — qırmızı xətdir. Terapiya yalnız təcavüz tam dayandırıldıqdan sonra mümkündür.</li>
            <li><strong>Aktiv asılılıq müalicəsiz qalır.</strong> Alkoqol, narkotik, oyun bağımlılığı — partnyor müalicəni rədd edirsə, ailə terapiyası boş yerdir.</li>
            <li><strong>Bir tərəf əsas qərarı verib.</strong> "Mən artıq getmişəm zehni olaraq" mərhələsində terapiya gec olur.</li>
            <li><strong>Saymamazlıq dövründəyik.</strong> Gottman təhlilinə görə bu mərhələ münasibətin sonunu 90% dəqiqliklə proqnozlaşdırır.</li>
            <li><strong>Gerçək yaşam dəyərləri tamamilə fərqlidir.</strong> Misal: bir tərəf dindar həyat istəyir, digəri ateist; bir tərəf uşaq istəyir, digəri kateqorik yox; bir tərəf miqrasiya, digəri qalmaq. Bu fərqlər kompromisə gəlmir.</li>
          </ul>

          <h2>"Sırf Uşaqlar üçün" Saxlanmaq</h2>
          <p>Ən populyar yanlış inanc: "uşaqlar üçün boşanmamalıyıq". Tədqiqatlar əksini göstərir.</p>
          <p>Wallerstein və Lewis-in 25 illik longitudinal tədqiqatı (2003): yüksək münaqişəli evdə böyüyən uşaqlarda psixoloji problemlər <strong>boşanmış valideynlərin uşaqlarına nisbətən 2-3 dəfə yüksəkdir</strong>.</p>
          <p>Vacib olan boşanmanın faktı yox, <em>necə baş verməsidir</em>: hörmətlə, uşağı münaqişə zonasından kənarda saxlamaqla, hər iki valideynlə yaxın əlaqə saxlamaqla — boşanma uşağa zərər vermir.</p>

          <h2>"Discernment Counseling" — Aralıq Forma</h2>
          <p>Bill Doherty (Minnesota Universiteti) yaratdığı modelə görə, qətiyyətsiz cütlüklər üçün xüsusi 5 seanslıq protokol mövcuddur. Məqsəd — boşanmanı və ya saxlanmanı seçmək yox, üç istiqamətdən birini aydınlaşdırmaq:</p>
          <ol>
            <li>Dayanmaq və hazırkı yolla davam (heç bir aktiv addım atmamaq)</li>
            <li>Boşanma prosesini başlamaq</li>
            <li>6 aylıq intensiv ailə terapiyasına girmək, sonunda yenidən qiymətləndirmək</li>
          </ol>

          <p>Bu modelin üstünlüyü: qərar verməyə təzyiq yoxdur. Pasiyentlər öz pace-də gedirlər.</p>

          <h2>Birinci Addım: Sakit Söhbət</h2>
          <p>Boşanma qərarı ailədə krizis anında alınmamalıdır. Tipik addım:</p>
          <ul>
            <li>2 həftə fiziki olaraq ayrı yaşamaq (mümkünsə)</li>
            <li>Ailə terapevtinə tək gəlmək — öz hisslərinizi aydınlaşdırmaq</li>
            <li>Sonra hər iki tərəf birlikdə discernment counseling-ə</li>
            <li>5 seans sonra qərar — və qərar etibarlı olur</li>
          </ul>

          <p>Qərar tələsməsi peşmançılıq gətirir. Ölçülmüş addım — sonradan istənilən nəticədən razı qalmaq imkanı verir.</p>""",
        "sources": """          <p><a href="https://www.gottman.com/blog/should-you-stay-or-go/" target="_blank" rel="noopener">Gottman Institute — Should You Stay or Go?</a></p>
          <p><a href="https://www.aamft.org/" target="_blank" rel="noopener">AAMFT — American Association for Marriage and Family Therapy</a></p>
          <p>Doherty, W. J. (2011). Discernment Counseling for Couples on the Brink of Divorce. <em>The Minnesota Couples on the Brink Project</em>.</p>
          <p>Wallerstein, J., & Lewis, J. (2004). The Unexpected Legacy of Divorce. <em>Psychoanalytic Psychology</em>, 21(3), 353-370.</p>"""
    },
    {
        "slug": "blog-aile-4.html",
        "title": "Cütlüklər Necə Düzgün Mübahisə Etməlidir?",
        "desc": "Gottman metodu: 4 atlı, yumşaq başlanğıc, təmir cəhdləri, fasilə qaydası — cütlük üçün konstruktiv mübahisə alətləri.",
        "read_time": 8,
        "cover": "images/blog/aile/art1-cover.jpg",
        "cover_alt": "Cütlük əl-ələ",
        "short": "Mübahisə qaçınılmazdır. Onu konstruktiv etmək — öyrənilə bilər. Gottman metodu əsasında praktik alətlər.",
        "body": """          <p>"Yaxşı cütlüklər mübahisə etmir" — yanlış inancdır. Gottman İnstitutunun 40 il davam edən laboratoriya tədqiqatları göstərir ki, <strong>uğurlu cütlüklər mübahisə edirlər — sadəcə fərqli şəkildə</strong>. Onların mübahisə "stili" pozulan cütlüklərdən aydın fərqli ölçülə bilən parametrlərlə fərqlənir.</p>

          <p>Bu məqalədə əsl klinik praktikadan və laboratoriya araşdırmalarından çıxarılan konkret alətlər verilir.</p>

          <h2>Qayda 1: Yumşaq Başlanğıc</h2>
          <p>Söhbət necə başlasa, çox vaxt belə də bitir. Gottman tədqiqatlarına görə, ilk 3 dəqiqədə baş verənlər 96% dəqiqliklə söhbətin nəticəsini proqnozlaşdırır.</p>

          <p><strong>Sərt başlanğıc:</strong> "Sən yenə qabları yumamısan, sənə güvənmək olmaz!"</p>

          <p><strong>Yumşaq başlanğıc:</strong> "Mən qab yığını gördüm və narahat oldum. Bu mövzuda razılığa gələ bilərikmi?"</p>

          <p>Düstur: <em>"Mən" + hiss + konkret hal + xahiş</em>. "Sən" sözü başlanğıcda — söhbəti hücuma çevirir.</p>

          <h2>Qayda 2: 4 Atlıdan Qaçın</h2>
          <p>Gottman boşanmanı 90% dəqiqliklə proqnozlaşdıran 4 davranışı müəyyənləşdirib:</p>
          <ul>
            <li><strong>Tənqid</strong> ("həmişə..." cümlələri) → əvəz: <em>şikayət</em> ("bu konkret halda")</li>
            <li><strong>Saymamazlıq</strong> (gözqamaşma, masqara) → əvəz: <em>hörmət</em></li>
            <li><strong>Müdafiə</strong> ("amma sən özün də...") → əvəz: <em>məsuliyyət</em> ("bu mənim də günahımdır")</li>
            <li><strong>Divar</strong> (susmaq, otaqdan çıxmaq) → əvəz: <em>fasilə</em> ("20 dəqiqəyə davam edək")</li>
          </ul>
          <p>Bu 4-dən ən təhlükəlisi <strong>saymamazlıqdır</strong>. O, partnyoru insan səviyyəsindən aşağı endirir. Bir dəfə görünsə — qızıl xəbərdarlıqdır.</p>

          <h2>Qayda 3: Fizioloji Sərinləşmə</h2>
          <p>Mübahisə zamanı ürək döyüntüsü 100/dəq-i keçəndə beyin "döyüş və ya qaç" rejiminə keçir. Bu rejimdə konstruktiv düşüncə mümkün deyil.</p>

          <p><strong>20 dəqiqə qaydası:</strong> ürək döyüntüsü yüksələndə — söhbəti dayandırın. "Mən hazırda sakitləşməliyəm. 20 dəqiqəyə davam edəcəyik." Bu vaxt ərzində <em>mübahisəni düşünməyin</em> — yürüş, dəzgah, kitab. Yalnız beynə neyrokimyəvi baxımdan bərpa imkanı verir.</p>

          <p>Vacib: söhbət <strong>geri qayıtmalıdır</strong>. "Fasilə vermək" mübahisədən qaçmaq deyil — onu effektivləşdirmək.</p>

          <h2>Qayda 4: Təmir Cəhdləri</h2>
          <p>Münaqişə zamanı təmir cəhdləri — kiçik müsbət siqnallardır: "səni sevirəm", zarafat, əli toxutmaq, "məni anlamağına çalışmağına minnətdaram". Sağlam cütlüklər bu siqnalları görür və qəbul edirlər.</p>

          <p>Pozulan cütlüklər təmir cəhdlərini görmür və ya rədd edir. Misal: bir tərəf "sənin haqqın var" deyir — digər tərəf "indi başlama" cavabı verir. Təmir rədd edildi.</p>

          <p>Praktiki məsləhət: hər mübahisədə özünüzə bir təmir cəhdi etməyə icazə verin. Nə qədər kiçik də olsa.</p>

          <h2>Qayda 5: 5:1 Nisbəti Saxlamaq</h2>
          <p>Mübahisə zamanı belə hər mənfi (eleştiri, qaş çatma) hər 5 müsbətə (təşəkkür, gülüş, hörmət göstərmə) qarşı olmalıdır. Bu nisbət avtomatik baş vermir — şüurlu səy lazımdır.</p>

          <p>Ev məşqi: mübahisədən sonra fikirləşin: bu 30 dəqiqədə 5 müsbət şey etdimmi? Yoxsa "qələbə" qazanmağa çalışdım?</p>

          <h2>Qayda 6: "Mən" vs "Sən"</h2>
          <p>"Sən mənə hörmət eləmirsən" → "Mən hörmətsiz hiss etdim". Tək sözün dəyişməsi söhbəti hücumdan paylaşılan hisslərə çevirir.</p>

          <h2>Qayda 7: Həll Olunmaz Mövzular</h2>
          <p>Gottman tədqiqatları: cütlük problemlərinin <strong>69%-i həll olunmazdır</strong>. Onlar fundamental fərqlərlə (uşaq sayı, dindarlıq, ailə üzvləri ilə əlaqə) bağlıdır.</p>

          <p>Sağlam cütlüklər bu mövzuları "həll" etmirlər — onlar haqqında <em>davam edən söhbət aparırlar</em>. "Biz bunu razılaşdırmadıq, lakin bir-birimizin baxış nöqtəsini başa düşməyə çalışırıq" — bu kifayətdir.</p>

          <h2>Praktiki Plan: 7 Günlük Eksperiment</h2>
          <ol>
            <li><strong>Gün 1-2:</strong> hər söhbətdə "yumşaq başlanğıc" düsturunu işlədin</li>
            <li><strong>Gün 3-4:</strong> hər mübahisədə "20 dəqiqə qaydası" tətbiq edin</li>
            <li><strong>Gün 5-6:</strong> 4 atlıdan birini özünüzdə tutun və düzəldin</li>
            <li><strong>Gün 7:</strong> günü təmir cəhdləri ilə tamamlayın</li>
          </ol>

          <p>7 gün — vərdiş üçün başlanğıcdır. 30 gün — yeni norma üçün.</p>""",
        "sources": """          <p><a href="https://www.gottman.com/blog/the-four-horsemen-recognizing-criticism-contempt-defensiveness-and-stonewalling/" target="_blank" rel="noopener">Gottman Institute — The Four Horsemen</a></p>
          <p><a href="https://www.gottman.com/about/the-research/" target="_blank" rel="noopener">Gottman Institute — Research Overview</a></p>
          <p>Gottman, J. M., & Levenson, R. W. (1992). Marital processes predictive of later dissolution. <em>Journal of Personality and Social Psychology</em>, 63(2), 221-233.</p>
          <p>Gottman, J., & Silver, N. (2015). <em>The Seven Principles for Making Marriage Work</em>. Harmony.</p>"""
    },
    {
        "slug": "blog-aile-5.html",
        "title": "Etibar İtirildikdə Onu Necə Qaytarmaq Olar?",
        "desc": "Xəyanət, yalan, etibar pozuntusu — bərpa mümkündürmü? 4 mərhələli klinik protokol.",
        "read_time": 9,
        "cover": "images/blog/aile/art5-cover.jpg",
        "cover_alt": "Cütlük barışıq",
        "short": "Xəyanət və ya etibar pozuntusu sonrası — 4 mərhələli klinik bərpa protokolu.",
        "body": """          <p>Etibar itirildikdə tipik sual: "Bunu bərpa etmək mümkündürmü?" Cavab: <strong>bəli, lakin avtomatik baş vermir</strong>. Tədqiqatlar (Gottman, 2018; Spring, 2012) göstərir ki, etibarın bərpası strukturlaşdırılmış proseslə 12-24 ay ərzində mümkündür — əgər hər iki tərəf bunun üçün hazırdırsa.</p>

          <p>Bu məqalədə klinik praktikadan dəlilə əsaslanan 4 mərhələli protokol verilir. Bu protokol təkcə cinsi xəyanəti yox, finansa, emosional yaxınlığa, gizli qərarlara — hər cür etibar pozuntusunu əhatə edir.</p>

          <h2>Mərhələ 1: Tam İfşaat (1-3 ay)</h2>
          <p>İlk mərhələ — bütün gerçəyin ortaya qoyulması. Yarımıfşaat ("əsasını dedim, qalanı önəmsizdir") gələcəkdə daha böyük zərbə kimi gələcək.</p>

          <p>Praktiki addımlar:</p>
          <ul>
            <li>Pozuntunu edən tərəf bütün faktları açıqlayır — terapevtin köməyi ilə, strukturlaşdırılmış formada</li>
            <li>Aldadılmış tərəfin bütün suallarına cavab verilir — "nə vaxt", "harada", "kimlə", "neçə dəfə"</li>
            <li>Detallar qədərində açıqlama — emosional ziyan vermədən, lakin gizlətmədən</li>
            <li>Aldadılmış tərəfə fikirləri əks etdirmək üçün vaxt verilir</li>
          </ul>

          <p>Bu mərhələ ağrılıdır, lakin atlanmazdır. Yalansız təməl olmadan sonrakı mərhələlər möhkəm dura bilməz.</p>

          <h2>Mərhələ 2: Məsuliyyət Qəbulu (3-6 ay)</h2>
          <p>Pozuntunu edən tərəf nə baş verdiyini izah etməyə yox, məsuliyyəti qəbul etməyə fokuslanır.</p>

          <p><strong>Səhv:</strong> "Mən bunu etdim çünki sən mənə diqqət etmirdin"</p>
          <p><strong>Doğru:</strong> "Mən bunu etdim. Bu mənim qərarım idi. Aramızda problemlər var idi, lakin onları bu yolla həll etmək — mənim seçimim idi və yanlış seçim idi."</p>

          <p>Vacib olanlar:</p>
          <ul>
            <li>Heç bir "amma" cümləsi olmamalıdır</li>
            <li>Pozuntu nəticələri tam dərk edilməlidir — tərəfdaşa nə hisslər yaratdığı</li>
            <li>Üzr — sözlər deyil, aktları daxildir: pozuntu kontekstindəki bütün fəaliyyət dayandırılır</li>
            <li>Şəffaflıq icazə verilir — telefonlar, yazışmalar açıq, sual mümkündür</li>
          </ul>

          <h2>Mərhələ 3: Yenidən Bağ Qurma (6-12 ay)</h2>
          <p>Bu mərhələdə "yeni münasibət" qurulur — köhnəsi yox. Köhnə münasibətə qayıtmaq mümkün deyil — keçmiş artıq başqadır.</p>

          <p>Yeni münasibətin elementləri:</p>
          <ul>
            <li><strong>Yeni qaydalar.</strong> Hər iki tərəf "bu ailədə nə qəbul olunur, nə yox" siyahısı tərtib edir. Bu siyahı bağlanmış müqavilə kimi hörmət edilir.</li>
            <li><strong>Müntəzəm "check-in".</strong> Həftədə 1 dəfə 30 dəqiqəlik söhbət — "necə hiss edirsən? hər şey necə gedir? hansı suallar var?"</li>
            <li><strong>Aldadılmış tərəfin "trigger"-lərinə hörmət.</strong> Müəyyən yerlərə getmək, müəyyən musiqilər — illərlə "minalı" qala bilər. Bunları zaman keçdikcə birlikdə dəf etmək.</li>
            <li><strong>Yeni müsbət xatirələr yaratmaq.</strong> Səyahət, birgə hobbi, yeni rituallar — keçmişin yaralı sahələrini yeni izlər ilə doldurmaq.</li>
          </ul>

          <h2>Mərhələ 4: Davamlı Bərpa (12+ ay)</h2>
          <p>Etibarın bərpası — hadisə deyil, prosesdir. Bir il sonra hər şey "normal" görünə bilər, lakin bəzi sahələr həssas qalır.</p>

          <p>Davamlı işlər:</p>
          <ul>
            <li><strong>Yıllıq qiymətləndirmə.</strong> Hər il "biz harda dayandığa baxırıq?" söhbəti. Daha açıq, daha qiymətli.</li>
            <li><strong>İllik üzr.</strong> Hadisənin il dönümlərində — pozuntu edən tərəf yenidən üzr istəyə bilər. Bu — "unudulmadığını" göstərir.</li>
            <li><strong>Profilaktik söhbətlər.</strong> "Hansı şərtlərdə bunun yenidən baş verə biləcəyini görürsən? Onu necə qarşısını ala bilərik?"</li>
          </ul>

          <h2>Etibar Bərpa Olunmur Əgər...</h2>
          <p>Müəyyən hallarda terapevt etibarın bərpasını rədd etməlidir:</p>
          <ul>
            <li>Pozuntu davam edir (məsələn, kontakt davam edir)</li>
            <li>Pozuntunu edən tərəf məsuliyyəti tam qəbul etmir, "günahı bölüşdürür"</li>
            <li>Aldadılmış tərəf əslində qərarını vermişdir, "çıxmaq" üçün son cəhd kimi terapiyaya gəlir</li>
            <li>Başqa böyük pozuntular var (asılılıq, fiziki təcavüz)</li>
          </ul>

          <h2>Yekun: Yeni Münasibət Köhnə Münasibətdən Daha Güclü Ola Bilər</h2>
          <p>Praktiki paradoks: <strong>uğurla bərpa olunmuş münasibətlər tez-tez heç vaxt böhran yaşamamış münasibətlərdən daha güclüdür</strong>. Çünki onlar açıq danışıq, məsuliyyət qəbulu, və münaqişənin konstruktiv həllində məşq ediblər.</p>

          <p>Bu — qızıl bilet deyil. Lakin etibarın itməsi münasibətin sonu olmaq məcburiyyətində deyil. Doğru proseslə — yeni başlanğıc ola bilər.</p>""",
        "sources": """          <p><a href="https://www.gottman.com/blog/rebuilding-trust/" target="_blank" rel="noopener">Gottman Institute — Rebuilding Trust</a></p>
          <p><a href="https://www.apa.org/topics/relationships/infidelity" target="_blank" rel="noopener">APA — Infidelity and Recovery</a></p>
          <p>Gottman, J. (2011). <em>The Science of Trust</em>. W. W. Norton & Company.</p>
          <p>Spring, J. A. (2012). <em>After the Affair: Healing the Pain and Rebuilding Trust</em>. William Morrow.</p>"""
    }
]

# Generate articles
for i, art in enumerate(ARTS):
    out = CHROME
    # Build related cards for this article (other 4 articles)
    others = [a for a in ARTS if a["slug"] != art["slug"]][:3]
    related = "\n".join(
        CARD_TPL.format(slug=o["slug"], title=o["title"], excerpt=o["short"]) for o in others
    )
    art_full = dict(art)
    art_full["related"] = related
    for k, v in art_full.items():
        out = out.replace("{" + k + "}", str(v))
    (ROOT / art["slug"]).write_text(out, encoding="utf-8")
    print(f"WROTE: {art['slug']}")

print("Done.")
