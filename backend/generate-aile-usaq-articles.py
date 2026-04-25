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
      <a href="tehsil.html#registration" class="btn btn-fill" onclick="toggleMenu()">Qeydiyyat</a>
    </nav>

    <section class="pg-hero pg-hero-plain" data-theme="dark">
      <div class="pg-hero-inner">
        <span class="badge">UŞAQ TERAPİYASI</span>
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
        <p class="sec-sub">İlk görüşdə birlikdə yol xəritəsini hazırlayırıq</p>
        <div class="cta-band-btns">
          <a href="https://wa.me/994702200376" class="btn btn-fill" target="_blank">WhatsApp ilə Yazın</a>
          <a href="aile-terapiyasi-usaq.html" class="btn btn-line">Uşaq Terapiyası</a>
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
              <span class="blog-card-cat">Uşaq</span>
              <h3 class="blog-card-title">{title}</h3>
              <p class="blog-card-excerpt">{excerpt}</p>
            </div>
          </a>"""

ARTS = [
    {
        "slug": "blog-yeniyetme.html",
        "title": "Yeniyetməniz Sizinlə Danışmırsa — Səbəb Siz Deyilsiniz",
        "desc": "13-17 yaş arası beyin inkişafı və valideynlərlə kommunikasiya — psixoloji izahat və praktik məsləhətlər.",
        "read_time": 8,
        "cover": "images/blog/aile-usaq/art1-cover.jpg",
        "cover_alt": "Pəncərə qarşısında yeniyetmə",
        "short": "13-17 yaş — beyin inkişafının ən intensiv dövrüdür. Niyə valideynlər 'düşmən' kimi görünür?",
        "body": """          <p>"Övladım mənimlə danışmır. Otağa girib qapını bağlayır. 'Necəsən?' — 'Yaxşı'. 'Məktəbdə nə var?' — 'Heç nə'. Bu mənim günahımdır?" Bu sual valideynlərin ən çox verdiyi sualdır. Cavab — aşağıda.</p>

          <p>Qısa cavab: <strong>çox vaxt — yox</strong>. Yeniyetməlik dövrünün geri çəkilməsi — neyrobioloji prosesdir. Bu məqalədə nəyə görə baş verdiyini və nə etmək lazım olduğunu izah edirik.</p>

          <h2>13-17 Yaş — Beynin "Yenidən Qurulması"</h2>
          <p>National Institute of Mental Health (NIMH) tədqiqatlarına görə, yeniyetməlik dövrü beynin "ikinci əsas yenidənquruluşu"dur (birincisi 0-3 yaşda). Bu dövrdə:</p>
          <ul>
            <li><strong>Prefrontal qabıq inkişaf edir</strong> (məntiq, planlaşdırma, impulsların idarəsi) — lakin tam yetkinlik 25 yaşa qədər davam edir</li>
            <li><strong>Limbik sistem həssaslaşır</strong> — emosiyalar daha güclü hiss olunur</li>
            <li><strong>Dopamin reseptorları zirvədə</strong> — "yeni təcrübə" axtarışı, risk almaq meyli</li>
            <li><strong>Yuxu ritmi 2-3 saat geri sürüşür</strong> — bu fizioloji səbəbdən yeniyetmələr gec yatırlar</li>
          </ul>

          <p>Beynin bu vəziyyəti yeniyetməni "qarışıq" göstərir: bir an çox parıldayan, sonra çox impulsiv, sonra emosional çəkilmiş.</p>

          <h2>Niyə "Valideynlər = Düşmən" Hissi Yaranır?</h2>
          <p>Bu — bioloji proqramdır, şəxsi reaksiya yox. Yeniyetməlik dövründə əsas inkişaf məqsədi — <strong>identifikasiya</strong>: "mən kiməm? Mənim öz dəyərlərim, fikirlərim, seçimim nədir?" Bu sual ailədən ayrılma tələb edir.</p>

          <p>Hər insan tip yeniyetməlikdə "ata-ana köhnəlmiş, tərslədir, anlamır" hiss edir. Bu biologiyadır — sizdən yapışıq qalsa, müstəqilliyini inkişaf etdirə bilməz. Bunu şəxsən qəbul etməyin.</p>

          <h2>Yanlış Reaksiyalar — Vəziyyəti Pisləşdirir</h2>
          <ul>
            <li><strong>"Niyə danışmırsan? Mənə güvənmirsən?"</strong> — yeniyetməyə "borcsan mənə danışmaq" mesajı göndərir → daha çox geri çəkilmə</li>
            <li><strong>Telefonu yoxlamaq, sosial mediasını izləmək</strong> — kəşf olduqda etibar dağılır → əlaqə tamam itir</li>
            <li><strong>"Sənin yaşında mən..."</strong> — hər müqayisə yeniyetmənin "dəyərsizlik" hissini artırır</li>
            <li><strong>"Otaqda kompüterdə oturma, çıx ailə ilə otur"</strong> — onun şəxsi sahəsi olmalıdır</li>
            <li><strong>Suallar yağdırmaq</strong> — gündə 30 dəfə "necəsən?" iclassal təzyiqdir</li>
          </ul>

          <h2>Doğru Strategiya: "Açıq Qapı"</h2>
          <p>Yeniyetmələr tələb olunan kommunikasiyanı yox, davam edən mövcudluğu sevirlər. Strategiya:</p>

          <p><strong>1. Birgə fəaliyyət zamanı söhbət.</strong> Üz-üzə oturub "danışaq" formatı işləmir. Maşın sürərkən, yemək hazırlayarkən, gəzəndə — yan-yana olarkən söhbət açılır. Çünki gözqamaşma yoxdur, təzyiq yoxdur.</p>

          <p><strong>2. Maraq — sual yox.</strong> "Bu video nə haqqındadır? İlginc görünür" — sual yox. "Niyə bu musiqini bu qədər çox dinləyirsən?" — sorğu deyil, real maraq.</p>

          <p><strong>3. Səhvlərə icazə verin.</strong> Yeniyetmələr səhv etməlidirlər — bu şəkildə öyrənirlər. "Mən sənə demişdim!" sözü əlaqəni dağıdır. "Bu çətin oldu. Növbəti dəfə nə edə bilərsən?" qurur.</p>

          <p><strong>4. Heç vaxt başqalarının yanında həqarət etməyin.</strong> Səhvi varsa — özbaşına. İctimai utanc — illərlə qalan emosional zədədir.</p>

          <p><strong>5. Onun dünyasına maraq göstərin.</strong> Hansı oyunlar oynayır, hansı influenser-ləri izləyir, hansı mövzular onu maraqlandırır. Bu siyahını bilmək — yeniyetmənin "məni gördülər" hissini formalaşdırır.</p>

          <h2>Nə Vaxt Peşəkar Yardım Lazımdır?</h2>
          <p>Geri çəkilmə + aşağıdakılardan biri varsa — psixoloq qiymətləndirməsi lazımdır:</p>
          <ul>
            <li>Məktəb performansının kəskin pisləşməsi</li>
            <li>Yuxu pozğunluğu (ya çox az, ya da çox)</li>
            <li>İştahın əsaslı dəyişməsi</li>
            <li>Bütün dostlarla əlaqəni kəsmək</li>
            <li>Özünə zərər izləri (bilək, qollar)</li>
            <li>"Yaşamağın mənası yoxdur" düşüncələri</li>
            <li>Maddə istifadəsi şübhələri</li>
            <li>Aqressiya artımı</li>
          </ul>

          <p>Bu siqnallar — sadə "yeniyetməlik" deyil, klinik müraciət üçün əsasdır.</p>

          <h2>Yekun: Səbr — Ən Vacib Alət</h2>
          <p>Yeniyetməlik 4-5 il davam edir. Bu illərdə əlaqə tez-tez gərgin olacaq. Lakin <strong>20 yaşda — uşaq geri qayıdır</strong>. Bu illərdə qoruduğunuz "açıq qapı" — onun gələcək münasibətinin əsasıdır.</p>

          <p>Səhv etməyin: bu dövrü "necə isə keçirmək" yox, "təməl qoymaq" kimi görün. Yeniyetmənizlə indi qurduğunuz münasibət — onun 30, 40, 50 yaşda sizinlə necə danışacağını formalaşdırır.</p>""",
        "sources": """          <p><a href="https://www.nimh.nih.gov/health/publications/the-teen-brain-7-things-to-know" target="_blank" rel="noopener">NIMH — The Teen Brain: 7 Things to Know</a></p>
          <p><a href="https://www.aap.org/" target="_blank" rel="noopener">American Academy of Pediatrics — Adolescent Development</a></p>
          <p>Steinberg, L. (2014). <em>Age of Opportunity: Lessons from the New Science of Adolescence</em>. Houghton Mifflin Harcourt.</p>
          <p>Siegel, D. J. (2013). <em>Brainstorm: The Power and Purpose of the Teenage Brain</em>. Tarcher/Penguin.</p>"""
    },
    {
        "slug": "blog-aile-usaq-2.html",
        "title": "Uşaq Davranış Problemləri — Əmr-Cəza vs Anlama",
        "desc": "Uşaqdakı 'pis davranış' nə deməkdir və əmr-cəza əvəzinə hansı strategiya daha effektivdir.",
        "read_time": 9,
        "cover": "images/blog/aile-usaq/art2-cover.jpg",
        "cover_alt": "Uşaq oyuncaqlarla",
        "short": "Aqressiya, itaətsizlik, məktəbdən imtina — anlaşılmamış emosional siqnaldır.",
        "body": """          <p>"Mənim övladım tamamilə əldə tutulmazdır" — psixoloqlara ən çox müraciət səbəbidir. Lakin tədqiqatlar göstərir: <strong>davranış problemlərinin 80%-i emosional ehtiyacların ödənilməməsindən</strong> qaynaqlanır, "pis xarakter"-dən yox.</p>

          <h2>Uşaq Davranışı — Bir Mesajdır</h2>
          <p>Uşaqlar emosiyalarını ifadə etməyi yetkinlər kimi etmirlər. 4 yaşlı uşaq "mən narahat hiss edirəm, çünki uşaq bağçasında özümü tək hiss etdim" demir. Onun yerinə — qardaşına vurur, qabı yerə tullayır, "yeməyəcəyəm!" qışqırır.</p>

          <p>Bu davranışlar simptomdur — xəstəlik deyil. Termometrin civəsi qızdırmadan yüksələndə termometri qırmırıq. Davranışla da eynidir — onu "bağlamaq" deyil, səbəbə baxmaq lazımdır.</p>

          <h2>Əmr-Cəza Niyə Səmərəsizdir?</h2>
          <p>"Otaqına get!", "telefon götürdüm!", "şirniyyat yoxdur!" — qısa müddətdə davranışı dayandırır. Lakin tədqiqatlar (Skinner, 1953; Pinker, 2002):</p>
          <ul>
            <li>Cəza <em>davranışı</em> dayandırır, lakin <em>səbəbi</em> aradan qaldırmır</li>
            <li>Uşaq cəzadan qaçmağı öyrənir — gizli olmağı, yalan danışmağı</li>
            <li>Valideynlə əlaqə güvənsizliyə doğru sürüşür</li>
            <li>Self-esteem zərbə alır — "mən pis uşağam"</li>
          </ul>

          <p>Vacib fərq: <strong>nəticə vs cəza</strong>. Nəticə davranışla məntiqi bağlıdır ("oyuncağı qırdın — düzəldən qədər yenisi yoxdur"). Cəza ixtiyari ("bağırdın — telefon yoxdur 1 həftə").</p>

          <h2>5 Tipik Davranış və Əsl Səbəbləri</h2>

          <p><strong>1. Aqressiya (vurma, dişləmə).</strong> 1-3 yaş — söz qabiliyyəti çatmır, hisslər çoxdur. 4-7 yaş — hələ də fizioloji impuls idarəsi az inkişaf edib. Cavab: "Vurmaq olmaz. Qəzəbli hiss edirsən? Gəl, əvəzində bunu et..." (yastığa vurmaq, qaçmaq, dərin nəfəs).</p>

          <p><strong>2. Yalan.</strong> 3-5 yaş — fantaziya və reallıq qarışır. 6-12 yaş — cəzadan qaçma, yetkin yox, etibar olmadıqda. Cavab: "Sənin doğru danışmağın mənim üçün önəmlidir. Hətta səhv etsən, doğru de — onu birlikdə həll edərik."</p>

          <p><strong>3. İtaətsizlik.</strong> "İndi yox!" sözü tez-tez səbəbdir: zövq verən fəaliyyətdən qopmaq çətindir. Cavab: 5 dəqiqə əvvəlcədən xəbərdarlıq verin. "5 dəqiqə sonra çıxmalıyıq". Sonra 1 dəqiqə. Sonra "vaxt gəldi".</p>

          <p><strong>4. Məktəbdən imtina.</strong> Əksər vaxt sosial səbəblər (zorbalıq, izolyasiya), tələbat (anlamadığı dərs), və ya emosional (anonim narahatlıq). Cavab: söhbət açın — "məktəbdə hansı şey ən çətindir?" — sual ölçülmüş şəkildə.</p>

          <p><strong>5. Yemək rədd etmək.</strong> 2-5 yaş — "öz qərarımı verə bilərəm" inkişafı. Cavab: <em>nə ediləcəyini valideyn seçir, yeyəcəyini uşaq seçir</em>. Boşqabda 3 yemək — uşaq nə qədər yeməyini özü qərar verir. Stress yaratmaq — yemək problemi yaradır.</p>

          <h2>"Boşaltma" Vərdişi</h2>
          <p>Daniel Siegel-in modeli: hər uşaqda gündəlik "stress kovası" doldurulur — məktəb, sosial təzyiq, yorğunluq. Kova daşdıqda — davranış pozulur. Sağlam strategiya: gün sonunda kovanı boşaltmaq.</p>

          <ul>
            <li><strong>Fiziki aktivlik</strong> — qaçmaq, oynamaq, idmançıq</li>
            <li><strong>Yaradıcılıq</strong> — rəsm, hekayə yazmaq, oyuncaqlar</li>
            <li><strong>İstiraha</strong> — "heç nə etmək" də vacibdir</li>
            <li><strong>Söhbət</strong> — "Bu gün ən yaxşı və ən çətin şey nə oldu?"</li>
            <li><strong>Toxunma</strong> — qucaq, əli toxutmaq, oxşamaq</li>
          </ul>

          <h2>"Connect Before You Correct"</h2>
          <p>Karen Young-ın prinsipi: <strong>düzəliş etməzdən əvvəl bağlanın</strong>. Uşaq pis hərəkət etdikdə əvvəl emosiyaları tanıyın, sonra davranışı izah edin.</p>

          <p>Misal: uşaq qardaşını vurdu.</p>
          <p><em>Səhv:</em> "Otağa get! Vurmaq olmaz!"</p>
          <p><em>Doğru:</em> Yanına oturun. "Görürəm sən çox qəzəblisən. Qardaşın oyuncaqını aldı, bu çox haqsızdır." (5-10 saniyə pauza). "Vurmaq olmaz, çünki ona zərər verir. Növbəti dəfə nə edə bilərsən? Ona deyə bilərsən: 'Bu mənim oyuncağımdır, geri ver'."</p>

          <p>Bu yanaşma 2-3 dəfə daha çox vaxt aparır. Lakin uzun müddətdə davranış problemlərinin 50%-dən çoxunu aradan qaldırır.</p>

          <h2>Nə Vaxt Peşəkar Yardım?</h2>
          <ul>
            <li>Davranış problemləri 6 aydan çox davam edirsə</li>
            <li>Məktəbdə də həmin davranışlar baş verirsə</li>
            <li>Özünə və ya başqalarına ciddi zərər verirsə</li>
            <li>Yuxu, yemək, əhval kəskin dəyişibsə</li>
            <li>Travma, xəstəlik, ya boşanma sonrası inadcıl davranış</li>
          </ul>""",
        "sources": """          <p><a href="https://www.aap.org/en/patient-care/early-childhood/" target="_blank" rel="noopener">AAP — Early Childhood Behavioral Health</a></p>
          <p><a href="https://www.zerotothree.org/" target="_blank" rel="noopener">Zero to Three — Early Childhood Development</a></p>
          <p>Siegel, D. J., & Bryson, T. P. (2011). <em>The Whole-Brain Child</em>. Bantam.</p>
          <p>Faber, A., & Mazlish, E. (2012). <em>How to Talk So Kids Will Listen & Listen So Kids Will Talk</em>. Scribner.</p>"""
    },
    {
        "slug": "blog-aile-usaq-3.html",
        "title": "Boşanma Sonrası Uşaq — Necə Kömək Etmək Olar?",
        "desc": "Boşanma uşaq üçün travma deyil — onun necə baş verməsidir. Praktik məsləhətlər valideynlər üçün.",
        "read_time": 9,
        "cover": "images/blog/aile-usaq/art3-cover.jpg",
        "cover_alt": "Ata və qız söhbət edir",
        "short": "Boşanma faktı yox, necə baş verməsi vacibdir. Klinik məsləhətlər valideynlər üçün.",
        "body": """          <p>Hər il dünyada milyonlarla uşaq valideynlərinin boşanmasını yaşayır. Ən geniş yayılmış inanc: "boşanma uşağa zərər verir". Lakin tədqiqatlar daha incə bir fakt göstərir: <strong>uşağa zərər vuran boşanmanın özü yox, onun necə baş verməsidir</strong>.</p>

          <p>Mavis Hetherington-un 30 illik longitudinal araşdırması göstərib ki, hörmətlə baş verən boşanmadan sonra uşaqların 75-80%-i 2-3 il ərzində bütün psixoloji parametrlər üzrə öz yaşıdlarına çatır. Lakin yüksək münaqişəli boşanmadan sonra problemlər illərlə davam edir.</p>

          <h2>Uşaq Boşanmadan Niyə Daha Çox Münaqişədən Zərər Görür?</h2>
          <p>Uşaq beyini "təhlükəsizlik" axtarır. Yüksək gərginlik, qışqırıq, evdə daimi düşmənçilik — fiziologi olaraq travmadır. Boşanma faktı isə struktur dəyişikliyidir — uşaq buna uyğunlaşa bilər.</p>

          <p>Tədqiqat: Wallerstein və Lewis (2003) — yüksək münaqişəli "saxlanılan" evlərdə böyüyən uşaqlarda psixoloji problemlər boşanmış valideynlərin uşaqlarına nisbətən <strong>2-3 dəfə yüksəkdir</strong>.</p>

          <h2>5 Praktik Qayda Hər İki Valideyn üçün</h2>

          <p><strong>1. Uşağın yanında digər valideyni TƏNQİD ETMƏYİN.</strong> Hətta haqlı olduğunuz hallarda. Uşaq özünü "yarısı sənə, yarısı atana məxsus" hiss edir. Bir tərəfin tənqidi — özünün yarısının tənqidi kimi qəbul olunur.</p>

          <p><em>Səhv:</em> "Atan həmişə pul vermir, əndişəsizdir"</p>
          <p><em>Doğru:</em> "Atanla məsələləri biz, yetkinlər həll edirik. Sən narahat olma."</p>

          <p><strong>2. Uşağı "kuryer" və ya "casus" rolunda istifadə etməyin.</strong> "Atana de ki..." — uşağa stress verir. "Atan nə dedi anasına?" — uşağı düşmən cəbhələri arasında qoyur.</p>

          <p><strong>3. Predictable Schedule.</strong> Uşaq nə vaxt kimlə olacağını bilməlidir. Qarışıqlıq və "ya kimi seçirsən bu həftə sonu" sualları — narahatlıq mənbəyidir. Açıq və sabit cədvəl — təhlükəsizlik mənbəyidir.</p>

          <p><strong>4. "Sənə görə deyildi" cümləsini söyləyin.</strong> 5-12 yaş uşaqları əksər vaxt boşanmada özlərini günahkar hesab edirlər. "Pis idim, oturuş etdim, ona görə getdi". Açıq şəkildə deyilməsi lazım: "Bu sənə görə deyil. Bu yetkinlərin qərarı idi. Mən və atan səni sevirik və həmişə sevəcəyik."</p>

          <p><strong>5. Hər iki valideynlə əlaqə qoruyun.</strong> Tədqiqatlar: hər iki valideynlə yaxın əlaqə saxlayan uşaqlar boşanmadan ən az təsir alanlardır. Birinin "qaybedilməsi" — itki travmasıdır.</p>

          <h2>Uşaq Yaşına Görə Reaksiyalar</h2>

          <p><strong>0-3 yaş:</strong> sözlü olaraq başa düşmür, lakin gərginliyi hiss edir. Reaksiya — yuxu pozğunluğu, yemək rejimi dəyişikliyi, ağlamaq.</p>

          <p><em>Strategiya:</em> rituallar saxlanılsın (yatmaq vaxtı eyni, yemək saatları eyni). Fiziki yaxınlıq artırılsın.</p>

          <p><strong>4-7 yaş:</strong> "magical thinking" — özünü günahkar hesab edir. "Mənim pis hərəkətimə görə"</p>

          <p><em>Strategiya:</em> təkrar-təkrar deyilməli "sənə görə deyil". Tələblər və qaydalar saxlanılsın — predictabilty.</p>

          <p><strong>8-12 yaş:</strong> dünya "fair olmalıdır" inancı, qəzəb, valideynlərdən birini günahlandırma.</p>

          <p><em>Strategiya:</em> emosiyaları tanımağa kömək: "Qəzəbli hiss etməyin normaldır." İki valideyn arasında "vassallıq" tələb etməyin — ikisinə də sevgi göstərmək haqqı var.</p>

          <p><strong>13-18 yaş:</strong> "siz özünüzü öncə düşünürsünüz, məni sayın yox" hissi, geri çəkilmə, məktəbdə performans pisləşməsi.</p>

          <p><em>Strategiya:</em> Onun emosiyalarını qəbul edin (eybəcərləşdirməyin). Dostları və hobbiləri ilə tutarlı dəstək.</p>

          <h2>"Co-Parenting" — Sağlam Boşanmanın Modelidir</h2>
          <p>Co-parenting — boşandıqdan sonra valideynlərin uşaq üçün koordinasiyalı yetişdirmə yanaşmasıdır:</p>
          <ul>
            <li>Birgə qaydalar (yataq saatı, ekran limiti, qida)</li>
            <li>Birgə qərarlar (məktəb, idman, dostlar)</li>
            <li>Birgə iştirak (məktəb tədbirləri, doğum günü)</li>
            <li>Hörmətli kommunikasiya (mətn, e-poçt, telefon — uşaq olmadan)</li>
          </ul>

          <p>Bu yanaşmada uşaq itki yox, "iki ev" qazanır.</p>

          <h2>Yeni Tərəfdaş — Vaxt və Tədricən</h2>
          <p>Yeni romantik münasibəti uşağa təqdim etmək — ehtiyatlı proses olmalıdır. AAP məsləhətləri:</p>
          <ul>
            <li>Yeni münasibətin ən az 6 ay davamı olduqdan sonra təqdim edin</li>
            <li>İlk görüş qısa, neytral məkanda (park, kafe)</li>
            <li>Uşağın hisslərini soruşun, qəbul edin</li>
            <li>"Yeni anan / atan" sözünü işlətməyin — uşağın bioloji valideynini əvəz edə bilməz</li>
            <li>Yeni həyat yoldaşı uşağa intizam tətbiq etməsin — bu, bioloji valideynin işidir</li>
          </ul>

          <h2>Nə Vaxt Peşəkar Yardım Lazımdır?</h2>
          <ul>
            <li>Boşanmadan 6-12 ay sonra uşaq hələ də ciddi simptomlar göstərirsə</li>
            <li>Məktəb performansı kəskin pisləşibsə</li>
            <li>Yuxu pozğunluğu, qabusluq</li>
            <li>Geri qayıdış (yatağa sidik, körpələrlə kimi danışıq)</li>
            <li>Dostlardan və ya zövq verən fəaliyyətlərdən geri çəkilmə</li>
            <li>Özünə zərər və ya intihar düşüncələri (yeniyetmələrdə)</li>
          </ul>

          <p>Erkən müdaxilə — boşanmanın uzunmüddətli təsirlərini minimuma endirir.</p>""",
        "sources": """          <p><a href="https://www.apa.org/topics/divorce/children" target="_blank" rel="noopener">APA — Children and Divorce</a></p>
          <p><a href="https://www.aap.org/" target="_blank" rel="noopener">American Academy of Pediatrics — Family Life</a></p>
          <p>Hetherington, E. M., & Kelly, J. (2003). <em>For Better or for Worse: Divorce Reconsidered</em>. W. W. Norton.</p>
          <p>Wallerstein, J., Lewis, J., & Blakeslee, S. (2000). <em>The Unexpected Legacy of Divorce</em>. Hyperion.</p>"""
    },
    {
        "slug": "blog-aile-usaq-4.html",
        "title": "Məktəbdən İmtina — 5 Əsl Səbəb",
        "desc": "Niyə uşaq 'məktəbə getməyəcəyəm' deyir? Klinik 5 səbəb və müdaxilə yolları.",
        "read_time": 8,
        "cover": "images/blog/aile-usaq/art4-cover.jpg",
        "cover_alt": "Çantalı uşaq",
        "short": "Məktəbdən imtinanın 5 klinik səbəbi və müdaxilə protokolu.",
        "body": """          <p>"Məktəbə getməyəcəyəm". Hər valideynin ən çətin səhərlərindən biri. Bu cümlə tənbəllik və ya inad deyil — əksər vaxt klinik siqnaldır. Tədqiqatlar (Kearney, 2008; AAP, 2019) göstərib ki, məktəbdən imtina (school refusal) — psixoloji yardım tələb edən, müalicə olunan vəziyyətdir.</p>

          <p>School refusal sadə "məktəb sevməmək"-dən fərqlənir: davranış davamlıdır, fiziki simptomlar (qarın ağrısı, başağrısı) ilə müşayiət olunur, ev mühitində yox olur.</p>

          <h2>Səbəb 1: Sosial Anksiyete və Zorbalıq</h2>
          <p>Ən geniş yayılmış səbəb (40-50%). Uşaq müəllimlər tərəfindən qiymətləndirilməkdən, sinif yoldaşları tərəfindən mühakimə edilməkdən, və ya zorbalıqdan əziyyət çəkir.</p>

          <p>Siqnallar:</p>
          <ul>
            <li>Bazar günü axşam başlayan narahatlıq</li>
            <li>Konkret günlərdə imtina (idman, ictimai çıxış olan)</li>
            <li>Sinif yoldaşları və ya müəllim haqqında danışmaqdan qaçınma</li>
            <li>Kiçik fiziki zərbə izləri</li>
          </ul>

          <p><strong>Müdaxilə:</strong> Uşaqla təmkinli söhbət — "məktəbdə nə baş verir?" Konkretlik vacibdir: "Hansı dərsdə özünü ən pis hiss edirsən?" Zorbalıq aşkar edilərsə — sinif rəhbəri ilə dərhal görüş.</p>

          <h2>Səbəb 2: Akademik Çətinliklər</h2>
          <p>Uşaq dərsi anlamır, lakin "axmaq görünməmək" üçün heç kimə deməz. İmtina — utanc və narahatlıqdan qaçma yoludur.</p>

          <p>Siqnallar:</p>
          <ul>
            <li>Konkret fənn günlərində imtina</li>
            <li>Test və imtahanlar dövründə artma</li>
            <li>Akademik performans son zamanlarda enmiş</li>
            <li>"Mən axmağam, heç nə bacarmıram"</li>
          </ul>

          <p><strong>Müdaxilə:</strong> Akademik qiymətləndirmə (öyrənmə pozğunluqları, disleksiya, ADHD ola bilər). Repetitor lazımdırsa — utanc məsələsi olaraq deyil, "biz öyrənirik" çərçivəsində təqdim edin.</p>

          <h2>Səbəb 3: Ayrılıq Anksiyetesi</h2>
          <p>5-9 yaş uşaqlar üçün xarakterikdir. Uşaq evdən, valideyndən ayrılmaqdan qorxur. Tipik sual: "Sən mənsiz öləcəksənmi?"</p>

          <p>Səbəbləri: keçmişdə itki (qohum, ev heyvanı, valideynin ciddi xəstəliyi), ailədə son zamanlarda dəyişikliklər (boşanma, yeni qohum doğumu), ya valideynin özünün narahatlığı uşağa keçməsi.</p>

          <p><strong>Müdaxilə:</strong> Tədricən ayrılma məşqi. Səhər ritualı (qısa, sevgi dolu, lakin uzanmasın), "sənə geri gələcəm" əmin etmə, kiçik tranzisiya əşyası (sevimli oyuncaq cibdə).</p>

          <h2>Səbəb 4: Depressiya</h2>
          <p>Yeniyetmələrdə (12-18 yaş) ən tez-tez səbəb. School refusal gizli depressiya əlamətidir.</p>

          <p>Siqnallar:</p>
          <ul>
            <li>Yuxu pozğunluğu (ya çox az, ya çox)</li>
            <li>Ümumi enerjisizlik</li>
            <li>Maraq itkisi (dostlar, hobbi, oyunlar)</li>
            <li>"Mənası yoxdur" cümlələri</li>
            <li>Yataqdan qalxmaq fiziki çətinliyi</li>
          </ul>

          <p><strong>Müdaxilə:</strong> Klinik psixiatr qiymətləndirməsi. Depressiya — müalicə olunan vəziyyətdir. KDT, bəzi hallarda dərman.</p>

          <h2>Səbəb 5: Travmatik Hadisə</h2>
          <p>Məktəbdə baş verən travmatik təcrübə: müəllim tərəfindən aşağılama, fiziki zorbalıq, cinsi təcavüz, fiziki yaralanma. Uşaq danışa bilməyə bilər — bu mövzu çox yüklüdür.</p>

          <p>Siqnallar:</p>
          <ul>
            <li>Kəskin imtina (əvvəl problem yox idi, qəfildən başladı)</li>
            <li>Konkret yer, dərs, ya şəxslə bağlı qaçınma</li>
            <li>Qabuslu, gecə oyanmaq</li>
            <li>Geri qayıdış (yataqda sidik, baş barmaq əmmək)</li>
            <li>Aqressiya artımı və ya tam çəkilmə</li>
          </ul>

          <p><strong>Müdaxilə:</strong> Dərhal psixoloq müraciət. Uşağı məktəbə qaytarmaq əvvəl təhlükəsizlik təmin edilməlidir.</p>

          <h2>Yanlış Reaksiyalar</h2>
          <p>Aşağıdakılar vəziyyəti pisləşdirir:</p>
          <ul>
            <li><strong>Cəza ilə məcbur etmək</strong> — qorxu artırılır, problem dərinləşir</li>
            <li><strong>Uzun müddətə evdə qalmasına icazə</strong> — qaçınma davranışı möhkəmlənir, geri qayıtmaq getdikcə çətinləşir</li>
            <li><strong>"Səndən başqa hamı gedir, niyə sən..." müqayisəsi</strong> — utanc və alçalma artırılır</li>
            <li><strong>Səbəbi araşdırmamaq</strong> — sadəcə "tənbəldir" hökmü qoymaq</li>
          </ul>

          <h2>Doğru Strategiya: Tədricən Geri Qayıtma</h2>
          <p>School refusal müalicəsində qızıl qayda: <strong>uşağı məktəbdən nə qədər çox uzaqda saxlasanız, geri qayıtmaq bir o qədər çətin olar</strong>. Əksər mütəxəssislər tədricən geri qayıtma planı təklif edir:</p>
          <ol>
            <li>Sevimli müəllimlə qısa görüş (0.5 saat)</li>
            <li>1 dərsə getmək, sonra ev</li>
            <li>Səhərdən günortaya qədər</li>
            <li>Tam günlü</li>
            <li>Hər mərhələ ən azı 2-3 gün davam edir</li>
          </ol>

          <p>Bu prosesdə valideyn, müəllim, və psixoloq koordinasiyalı işləyir.</p>""",
        "sources": """          <p><a href="https://www.aap.org/en/patient-care/school-refusal/" target="_blank" rel="noopener">AAP — School Refusal</a></p>
          <p><a href="https://www.apa.org/topics/children/school-refusal" target="_blank" rel="noopener">APA — School Refusal</a></p>
          <p>Kearney, C. A. (2008). <em>Helping School Refusing Children and Their Parents</em>. Oxford University Press.</p>
          <p>King, N. J., & Bernstein, G. A. (2001). School refusal in children and adolescents. <em>Journal of the American Academy of Child & Adolescent Psychiatry</em>, 40(2), 197-205.</p>"""
    },
    {
        "slug": "blog-aile-usaq-5.html",
        "title": "Uşağa 'Yox' Demək — Sağlam Sərhəd Necə Qurulur?",
        "desc": "Sevgi və qaydalar bir-birinə zidd deyil. Uşaqda sağlam sərhədlər qurmaq üçün praktik prinsiplər.",
        "read_time": 7,
        "cover": "images/blog/aile-usaq/art5-cover.jpg",
        "cover_alt": "Birgə danışan ailə",
        "short": "Sevgi + qaydalar = sağlam uşaq. 4 prinsip və 5 praktik qayda.",
        "body": """          <p>"Uşağa 'yox' deyə bilmirəm — ağlayır, mən gücsüz hiss edirəm" — bu cümlə müasir psixoterapevt kabinetlərində ən tez-tez eşidilən cümlələrdən biridir. Lakin tədqiqatlar göstərir: <strong>"yox" demək uşağa zərər vermir — onu uşağı dəstəkləyir</strong>.</p>

          <p>Diana Baumrind-in 50 illik klassik tədqiqatı 4 valideyn stilini müəyyənləşdirib və bunlardan ən sağlam olanı — <strong>autoritativ</strong> stil idi: yüksək sevgi + aydın qaydalar.</p>

          <h2>4 Valideyn Stili</h2>
          <ul>
            <li><strong>Autoritativ</strong> (yüksək sevgi + yüksək qaydalar): uşaqlar self-esteem yüksək, akademik uğurlu, emosional sabit</li>
            <li><strong>Avtoritar</strong> (aşağı sevgi + yüksək qaydalar): "qoy itaət etsin" — uşaqlar narahat, aşağı self-esteem</li>
            <li><strong>Permissive</strong> (yüksək sevgi + aşağı qaydalar): "uşağa hər şey azaddır" — impulsiv, sosial çətinliklər</li>
            <li><strong>Neglectful</strong> (aşağı sevgi + aşağı qaydalar): ən pis nəticə — bütün sahələrdə problemlər</li>
          </ul>

          <p>Yəni "yox" demək — sevgisizlik deyil. "Yox" demədən sevgi göstərmək — sevgi deyil, sevgi simulyasiyasıdır.</p>

          <h2>Niyə Sağlam Sərhədlər Vacibdir?</h2>
          <p>Uşaq dünyaya gələndə tamamilə yardımsızdır — yetkinlər nə qədər ona icazə versələr, o qədər inkişaf edə bilməz. Sərhədlər ona deyir:</p>
          <ul>
            <li><strong>"Bu dünyada predictabilty var"</strong> — təhlükəsizlik hissi</li>
            <li><strong>"Mən yetkinin yanında qoyulmuşam"</strong> — psixoloji rahatlıq</li>
            <li><strong>"Bütün arzularım yerinə yetirilməyəcək — bu normaldır"</strong> — sosial bacarıq</li>
            <li><strong>"Mən frustration-u keçə bilərəm"</strong> — emosional dayanıqlılıq</li>
            <li><strong>"Yox" sözünə cavab vermək"</strong> — gələcək münasibətlərdə tələb olunan bacarıq</li>
          </ul>

          <h2>4 Prinsip — Sağlam "Yox"</h2>

          <p><strong>1. Sakit Olun.</strong> Uşaqlar valideynin emosional vəziyyətini hiss edirlər. Qışqıraraq deyilən "yox" — uşağı qorxudur, lakin öyrətmir. Sakit, möhkəm "yox" — anlam daşıyır.</p>

          <p><strong>2. Səbəb Verin (Qısa).</strong> "Çünki mən belə dedim" — yeniyetməlikdə üsyan səbəbidir. Qısa səbəb daha effektlidir: "Çünki şirniyyat yeməkdən əvvəl iştahını öldürür". 3-5 yaş uşaq üçün də səbəb anlaşılan dildə verilməlidir.</p>

          <p><strong>3. Alternativ Təklif Edin.</strong> "Telefon olmaz indi" yerinə "telefon yarım saat sonra. İndi gəl, birlikdə oyun oynayaq". "Yox" + alternativ = uşaq frustration-dan idarə olunan kanaldan keçir.</p>

          <p><strong>4. "Yox" Sözünü Geri Götürməyin.</strong> Uşaq ağlayır, qışqırır, yerə düşür. Bu — testdir. Əgər siz nəticədə "yaxşı, al" deyirsinizsə — uşaq belə öyrənir: <em>kifayət qədər ağlayım — istədiyimi alaram</em>. Bir dəfə belə oldu — gələcək 100 dəfə eyni davranış olacaq.</p>

          <h2>5 Praktik Vəziyyət</h2>

          <p><strong>Vəziyyət 1: Marketdə şokolad istəyir.</strong></p>
          <p><em>Yanlış:</em> "Susmazsan, evə getmirik!"</p>
          <p><em>Doğru:</em> "Bilirəm, sən şokolad istəyirsən. Bu gün şokolad almırıq. Səndən soruşmadan əvvəl mən qərarımı vermişdim. Hə, çətin hissdir." (uşaq ağlasa, qucağa götürün, lakin qərarı dəyişməyin).</p>

          <p><strong>Vəziyyət 2: Yatmaq vaxtı, telefonda film.</strong></p>
          <p><em>Yanlış:</em> "Yat dedim, qaynat, tezliklə!"</p>
          <p><em>Doğru:</em> "Filmin sonuna 10 dəqiqə qalıb. Bu hissəni baxırsan, sonra yatağa." Vaxtdan əvvəl xəbərdarlıq + alternativ.</p>

          <p><strong>Vəziyyət 3: Qardaşa vurur.</strong></p>
          <p><em>Yanlış:</em> "Necə cürət edirsən! Otağa get!"</p>
          <p><em>Doğru:</em> Uşağı tutub fiziki olaraq ayırın. "Vurmaq olmaz. Qardaşına ağrı verir." Sonra emosional tanıma: "Sən qəzəbli idin. Qəzəblənmək olar — vurmaq olmaz".</p>

          <p><strong>Vəziyyət 4: Uşaq dostlarına gedir, dərs məsuliyyəti var.</strong></p>
          <p><em>Yanlış:</em> "Dostların önəmlidir, dərs önəmsizdir?!"</p>
          <p><em>Doğru:</em> "Bu gün dərs günüdür. Cümə axşamı dostlarınla görüşə bilərsən. Mən cümə axşamına imza atıram."</p>

          <p><strong>Vəziyyət 5: Yeniyetmə sigarayı asanırlıqla götürür.</strong></p>
          <p><em>Yanlış:</em> "Mən sənə qadağan edirəm! Yenə sezgəm — telefon yoxdur!"</p>
          <p><em>Doğru:</em> "Sigarayı götürdüm. Səhhəti barədə mənim narahatlığım var. Niyə sigaraya başlamısan, danışa bilərikmi?" Sərhəd + söhbət açma.</p>

          <h2>"Yox" Demək Sevgi Etmir — Sevgini İnkişaf Etdirir</h2>
          <p>İllərlə "yox" deyilməyən uşaq yetkin olduqda dünya ilə ilk dəfə üzləşdikdə — uğursuzluq, rədd edilmə, "olmaz" sözləri ilə üzləşir. Bu məqamda sərhədləri yox kimi məşq etməmiş insan psixoloji baxımdan çökür.</p>

          <p>Doğru sevgi — uşağı həyatın "yox" sözlərinə hazırlayır. Sevən valideyn — qaydalar qoyan valideyndir.</p>""",
        "sources": """          <p><a href="https://www.apa.org/topics/parenting" target="_blank" rel="noopener">APA — Parenting Style</a></p>
          <p><a href="https://www.aap.org/" target="_blank" rel="noopener">American Academy of Pediatrics — Parenting</a></p>
          <p>Baumrind, D. (1991). The influence of parenting style on adolescent competence. <em>Journal of Early Adolescence</em>, 11(1), 56-95.</p>
          <p>Cline, F., & Fay, J. (2006). <em>Parenting With Love and Logic</em>. NavPress.</p>"""
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
