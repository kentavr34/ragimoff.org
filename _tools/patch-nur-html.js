const fs = require('fs');
const path = require('path');
const f = path.join(process.argv[2], 'index.html');
let s = fs.readFileSync(f, 'utf8');
const log = [];

/* 1) ГЕРОЙ → sticky-сцена + скраб-видео ходьбы + рябь клика */
const heroOld = s.slice(s.indexOf('<section class="hero"'), s.indexOf('<!-- ───────────────────────── МАРКИЗА'));
const heroNew = `<section class="hero" id="ana" data-rail="Başlanğıc">
      <div class="hero__stage">
        <div class="hero__media" data-hx="0.006">
          <video data-scrub src="assets/walk.mp4" poster="assets/hero-bg.jpg" muted playsinline preload="auto" aria-hidden="true"></video>
        </div>
        <canvas class="hero__canvas" aria-hidden="true"></canvas>
        <span class="hero__ripple" aria-hidden="true"></span>

        <div class="hero__chips" aria-hidden="true">
          <span class="chip">IPAS Ambassador</span>
          <span class="chip">XBT-11 · DSM-5</span>
          <span class="chip">23 il təcrübə</span>
        </div>

        <div class="wrap hero__in">
          <div data-hx="0.012">
            <span class="hero__badge"><i class="beat"></i> Klinik psixiatr · psixoterapevt</span>
            <h1>
              <span class="h1-line"><span>Peşəkar</span></span>
              <span class="h1-line"><span><em>Psixologiya</em> Məktəbi</span></span>
            </h1>
            <p class="hero__lede">2003-cü ildən həkim-psxoterapevt kvallifikasiyası, terapiya və klinik təcrübə,<br>psixologiya sahəsində - peşəkar keryera mentoru, XBT-11 üzrə tədris vəsaitinin müəllifi</p>
            <div class="hero__cta">
              <a class="btn btn--main" href="https://wa.me/994702200376" data-magnet data-cursor-label="Yaz">Qəbula yazıl <span aria-hidden="true">→</span></a>
              <a class="btn btn--ghost" href="#xidmet" data-magnet data-cursor-label="Bax">Xidmətlər</a>
            </div>
          </div>
          <div class="hero__read">
            <div><b>23</b><span class="meta">İl klinik təcrübə</span></div>
            <div><b>3000<sup>+</sup></b><span class="meta">Peşəkar təlim</span></div>
            <div><b>300<sup>+</sup></b><span class="meta">Davamlı müştəri</span></div>
            <div><b>11</b><span class="meta">Diplom və sertifikat</span></div>
          </div>
        </div>
        <div class="hero__cue meta" aria-hidden="true"><i></i> Skroll</div>
      </div>
    </section>

    `;
s = s.replace(heroOld, heroNew);
log.push('герой → скраб-сцена');

/* 2) ХРОНИКА → документы вписываются целиком (img + contain) */
s = s.replace(/<div class="seq__img" style="background-image:url\('([^']+)'\)"><\/div>/g,
  (m, src) => '<div class="seq__doc"><img src="' + src + '" alt="" loading="lazy"></div>');
log.push('хроника: background-image → <img> contain');

/* 3) ПОРТРЕТ специалиста — фото владельца (вписывание, без обрезки головы) */
s = s.replace('../../images/kenan/kenan-removebg-preview.png', '../../images/kenan/photo-hero-suit.jpg');
log.push('портрет → photo-hero-suit.jpg');

/* 4) БЛОК «TƏLİMLƏR» — фото студентов отдельно от дипломов (после хроники) */
const trainBlock = `
    <!-- ─────────────── TƏLİMLƏR · фото студентов (не смешивать с дипломами) ─────────────── -->
    <section class="sec" id="telim" data-rail="Təlimlər">
      <div class="wrap">
        <div class="sec__head" data-rv>
          <h2 class="h2" data-split><span class="h2__serif">Təlimlər</span> <span class="h2__script">nəticələr</span></h2>
          <span class="meta">03 — Qrup işi · korporativ</span>
        </div>
        <p class="sub" data-rv><span>Qrup təlimləri, korporativ proqramlar və məktəb buraxılışları — <b class="sub__m">3000+</b> iştirakçı. Bu bölmə təlim nəticələridir; diplom və sertifikatlar yuxarıdaki xronikadadır.</span></p>
        <div class="train__grid">
          <figure class="train__card" data-rv>
            <div class="train__ph"><img src="../../images/students/group-training.jpg" alt="Qrup təlimi" loading="lazy"></div>
            <figcaption class="train__cap"><span class="meta">Qrup təlimi</span><span>Psixoterapiya praktikumu — işçi qruplarla sessiyalar.</span></figcaption>
          </figure>
          <figure class="train__card" data-rv data-stagger="90">
            <div class="train__ph"><img src="../../images/students/korporativ-tehsil.jpg" alt="Korporativ təhsil" loading="lazy"></div>
            <figcaption class="train__cap"><span class="meta">Korporativ</span><span>Şirkətlər üçün liderlik və komanda proqramları.</span></figcaption>
          </figure>
          <figure class="train__card" data-rv data-stagger="180">
            <div class="train__ph"><img src="../../images/students/psixologiya-mekteb.jpg" alt="Psixologiya məktəbi" loading="lazy"></div>
            <figcaption class="train__cap"><span class="meta">Məktəb buraxılışı</span><span>Psixologiya Məktəbi məzunları ilə yekun görüşü.</span></figcaption>
          </figure>
          <figure class="train__card" data-rv>
            <div class="train__ph"><img src="../../images/students/group-outdoor.jpg" alt="Açıq havada təlim" loading="lazy"></div>
            <figcaption class="train__cap"><span class="meta">Açıq format</span><span>Komanda və qrup dinamikası üzrə açıq təlim.</span></figcaption>
          </figure>
          <figure class="train__card" data-rv data-stagger="90">
            <div class="train__ph"><img src="../../images/students/psixoterapiya-praktikum.jpg" alt="Psixoterapiya praktikumu" loading="lazy"></div>
            <figcaption class="train__cap"><span class="meta">Praktikum</span><span>Real klinik bacarıqlar üzrə praktik məşğələlər.</span></figcaption>
          </figure>
          <figure class="train__card" data-rv data-stagger="180">
            <div class="train__ph"><img src="../../images/students/cert-3.jpg" alt="Tələbə sertifikatı" loading="lazy"></div>
            <figcaption class="train__cap"><span class="meta">Məzun sertifikatı</span><span>Təlimi bitirən iştirakçının sertifikatı.</span></figcaption>
          </figure>
        </div>
      </div>
    </section>

`;
s = s.replace('    <!-- ───────────────────────── СЧЁТЧИКИ ───────────────────────── -->', trainBlock + '    <!-- ───────────────────────── СЧЁТЧИКИ ───────────────────────── -->');
log.push('добавлен блок Təlimlər (6 фото студентов)');

/* 5) Нумерация секций после вставки */
s = s.replace('<span class="meta">03 — Faktlar</span>', '<span class="meta">04 — Faktlar</span>');
s = s.replace('<span class="meta">04 — Sorğu vəsaiti · 2026</span>', '<span class="meta">05 — Sorğu vəsaiti · 2026</span>');
s = s.replace('<span class="meta">02 — Təcrübə yolu</span>', '<span class="meta">02 — Təcrübə yolu · diplomlar</span>');
log.push('перенумерованы секции');

fs.writeFileSync(f, s);
console.log('index.html обновлён:', s.length, 'байт');
log.forEach((l) => console.log(' • ' + l));
