const fs = require('fs');
const path = require('path');
const f = path.join(process.argv[2], 'nur.js');
let s = fs.readFileSync(f, 'utf8');
const log = [];

/* 1) initHero: не запускать автоплей — режимом видео управляет скраб-модуль */
s = s.replace(
  "    heroVid = $('.hero__media video', hero);\n    if (heroVid) { var p = heroVid.play(); if (p && p.catch) p.catch(function () {}); }",
  "    heroVid = $('.hero__media video', hero);   /* режимом видео управляет initScrub */"
);
log.push('initHero: автоплей убран');

/* 2) Новый модуль: скролл-скраб видео в герое */
const scrub = `
  /* ─────────── ГЕРОЙ: скролл-скраб (ходьба вперёд/назад + «клик») ─────────── */
  var scrubHero = null, scrubVid = null, scrubDur = 0, scrubCur = 0, scrubScrub = false;
  function applyScrubMode() {
    if (!scrubVid) return;
    var canScrub = fine && !reduce && innerWidth > 980;
    var canLoop = !reduce && !canScrub;
    scrubScrub = canScrub;
    try {
      if (canScrub) {
        scrubVid.pause();
        scrubVid.loop = false;
        if (!scrubDur) scrubVid.currentTime = 0;
      } else if (canLoop) {
        scrubVid.loop = true;
        scrubVid.muted = true;
        var p = scrubVid.play();
        if (p && p.catch) p.catch(function () {});
      } else {
        scrubVid.pause();
        scrubVid.loop = false;
        scrubVid.currentTime = 0.08;
      }
    } catch (e) {}
  }
  function initScrub() {
    scrubHero = $('.hero');
    scrubVid = $('[data-scrub]');
    if (!scrubHero || !scrubVid) return;
    scrubVid.addEventListener('loadedmetadata', function () { scrubDur = scrubVid.duration || 0; });
    scrubVid.addEventListener('canplay', function () { if (!scrubDur) scrubDur = scrubVid.duration || 0; });
    applyScrubMode();
    window.addEventListener('resize', applyScrubMode);
  }
  function runScrub() {
    if (!scrubHero) return;
    var r = scrubHero.getBoundingClientRect();
    var span = scrubHero.offsetHeight - innerHeight;
    if (span <= 1) return;
    var p = clamp(-r.top / span, 0, 1);
    scrubHero.style.setProperty('--hero-p', p.toFixed(4));
    scrubHero.classList.toggle('is-click', p > 0.84);
    if (!scrubScrub || !scrubVid || !scrubDur) return;
    var t = p * (scrubDur - 0.06);
    scrubCur += (t - scrubCur) * 0.22;
    if (Math.abs(t - scrubCur) > 0.008) {
      try { scrubVid.currentTime = scrubCur; } catch (e) {}
    }
  }

`;
s = s.replace('  /* ──────────────── ЗОЛОТЫЕ ЧАСТИЦЫ (canvas) ──────────────── */', scrub + '  /* ──────────────── ЗОЛОТЫЕ ЧАСТИЦЫ (canvas) ──────────────── */');
log.push('добавлен модуль скраба');

/* 3) вызов в прокрутке */
s = s.replace('    lastY = y;\n    runSeq(); runPlx();', '    lastY = y;\n    runSeq(); runPlx(); runScrub();');
log.push('runScrub в runScroll');

/* 4) инициализация */
s = s.replace('    initHero();\n    initDust();', '    initHero();\n    initScrub();\n    initDust();');
log.push('initScrub в boot');

/* 5) в no-mo (reduce) сбрасывать клик-состояние */
s = s.replace("html.no-mo .hero__canvas { display: none; }", "html.no-mo .hero__canvas { display: none; }");

fs.writeFileSync(f, s);
console.log('nur.js обновлён:', s.length, 'байт');
log.forEach((l) => console.log(' • ' + l));
console.log('проверки:', /initScrub/.test(s), /runScrub/.test(s), /applyScrubMode/.test(s));
