const fs = require('fs');
const path = require('path');
const dir = process.argv[2];
const f = path.join(dir, 'nur.css');
let s = fs.readFileSync(f, 'utf8');

/* 1) ГЕРОЙ → скролл-скраб (высокая секция + sticky-сцена) */
const heroStart = s.indexOf('/* ─────────────────────────── ГЕРОЙ ─────────────────────────── */');
const heroEnd = s.indexOf('/* ───────────────────────── МАРКИЗА ───────────────────────── */');
if (heroStart < 0 || heroEnd < 0) throw new Error('не найдены границы блока героя');

const newHero = [
'/* ─────────────── ГЕРОЙ · скролл-скраб (ходьба по горизонтали) ─────────────── */',
'.hero { position: relative; height: 260vh; }',
'.hero__stage {',
'  position: sticky; top: 0; height: 100svh;',
'  display: flex; flex-direction: column; justify-content: flex-end;',
'  overflow: clip;',
'}',
'.hero__media { position: absolute; inset: 0; z-index: 0; }',
'.hero__media video, .hero__media img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }',
'.hero__media::after {',
"  content: ''; position: absolute; inset: 0;",
'  background:',
'    linear-gradient(180deg, var(--shade) 0%, transparent 34%, transparent 58%, var(--shade) 100%),',
'    linear-gradient(90deg, var(--shade) 0%, transparent 58%);',
'}',
'.hero__canvas { position: absolute; inset: 0; z-index: 1; pointer-events: none; opacity: .5; }',
'.hero__ripple {',
'  position: absolute; z-index: 3;',
'  right: clamp(70px, 13vw, 220px); bottom: clamp(120px, 24vh, 250px);',
'  width: 20px; height: 20px; border-radius: 50%;',
'  border: 2px solid var(--acc); opacity: 0;',
'  transform: translate(-50%, -50%) scale(.4);',
'  pointer-events: none;',
'}',
'html.mo .hero.is-click .hero__ripple { opacity: 1; animation: ripple 1.15s var(--e) infinite; }',
'@keyframes ripple {',
'  0% { transform: translate(-50%, -50%) scale(.4); opacity: .95; }',
'  100% { transform: translate(-50%, -50%) scale(3.6); opacity: 0; }',
'}',
'.hero__in { position: relative; z-index: 2; padding-bottom: clamp(26px, 5.5vh, 64px); }',
'.hero__badge {',
'  display: inline-flex; align-items: center; gap: 10px;',
'  padding: 7px 15px; border: var(--bd) solid var(--line-2); border-radius: var(--r-pill);',
'  font-family: var(--font-mono); font-size: var(--fs-micro); letter-spacing: var(--ls-meta);',
'  text-transform: uppercase; color: var(--acc-2);',
'  margin-bottom: clamp(20px, 4vh, 40px);',
'  backdrop-filter: blur(8px);',
'}',
'.beat { width: 7px; height: 7px; border-radius: 50%; background: var(--acc); box-shadow: 0 0 12px rgba(201,169,97,.8); }',
'html.mo .beat { animation: beat 1.9s var(--e2) infinite; }',
'@keyframes beat { 0%,100% { transform: scale(1); } 12% { transform: scale(1.6); } 24% { transform: scale(1); } 36% { transform: scale(1.35); } 48% { transform: scale(1); } }',
'.hero h1 {',
'  margin: 0; font-family: var(--font-display);',
'  font-size: var(--fs-hero); font-weight: var(--fw-light);',
'  line-height: var(--lh-hero); letter-spacing: var(--ls-mega);',
'}',
'.hero h1 em { color: var(--acc-2); font-style: italic; }',
'.h1-line { display: block; overflow: hidden; }',
'.h1-line:nth-child(1) > span { --ld: 80; }',
'.h1-line:nth-child(2) > span { --ld: 210; }',
'html.mo .h1-line > span { display: inline-block; transform: translateY(115%) rotate(2deg); transition: transform 1.15s var(--e) calc(var(--ld, 0) * 1ms); }',
'html.mo .hero.is-in .h1-line > span { transform: none; }',
'.hero__lede {',
'  margin: clamp(18px, 3.2vh, 38px) 0 0; max-width: var(--w-lede);',
'  font-family: var(--font-display); font-style: italic;',
'  font-size: var(--fs-lede); line-height: var(--lh-lede); color: var(--mid);',
'}',
'html.mo .hero__lede { opacity: 0; transform: translateY(16px); transition: opacity .9s linear .5s, transform .9s var(--e) .5s; }',
'html.mo .hero.is-in .hero__lede { opacity: 1; transform: none; }',
'.hero__cta { margin-top: clamp(20px, 3.6vh, 38px); display: flex; flex-wrap: wrap; gap: 14px; }',
'html.mo .hero.is-click .btn--main { box-shadow: 0 0 0 1px var(--acc), 0 0 40px rgba(201,169,97,.35); }',
'',
'.btn {',
'  display: inline-flex; align-items: center; gap: 14px;',
'  padding: 14px 26px; min-height: 48px;',
'  border: var(--bd) solid var(--line-2); border-radius: var(--r-pill);',
'  position: relative; overflow: hidden; isolation: isolate;',
'  font-family: var(--font-mono); font-size: var(--fs-meta);',
'  letter-spacing: var(--ls-meta); text-transform: uppercase; color: var(--fg);',
'  transition: color var(--dur-ui) linear, border-color var(--dur-ui) linear, box-shadow .5s var(--e);',
'}',
".btn::before { content: ''; position: absolute; inset: 0; z-index: -1; background: var(--acc); transform-origin: bottom; }",
'html.mo .btn::before { transform: scaleY(0); transition: transform .5s var(--e); }',
'.btn:hover { color: var(--inv-fg); border-color: var(--acc); }',
'.btn:hover::before { transform: none; }',
'.btn--ghost::before { display: none; }',
'.btn--ghost:hover { color: var(--acc); }',
'',
'.hero__chips { position: absolute; right: var(--pad-x); top: 22vh; z-index: 2; display: none; }',
'@media (min-width: 1100px) { .hero__chips { display: block; } }',
'.chip {',
'  display: block; margin-top: 10px; padding: 9px 16px;',
'  border: var(--bd) solid var(--line-2); border-radius: var(--r-pill);',
'  font-family: var(--font-mono); font-size: var(--fs-micro); letter-spacing: var(--ls-meta);',
'  text-transform: uppercase; color: var(--mid); backdrop-filter: blur(8px);',
'}',
'html.mo .chip { animation: chip-float 7s var(--e2) infinite; }',
'html.mo .chip:nth-child(2) { animation-duration: 9s; animation-delay: -2s; }',
'html.mo .chip:nth-child(3) { animation-duration: 11s; animation-delay: -4s; }',
'@keyframes chip-float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-12px); } }',
'',
'.hero__read {',
'  margin-top: clamp(22px, 4.4vh, 50px);',
'  display: flex; flex-wrap: wrap;',
'  border-top: var(--bd) solid var(--line);',
'  border-bottom: var(--bd) solid var(--line);',
'}',
'.hero__read div { flex: 1 1 150px; padding: 15px 22px 15px 0; border-right: var(--bd) solid var(--line); }',
'.hero__read div:last-child { border-right: 0; }',
'.hero__read b { display: block; font-family: var(--font-display); font-size: var(--fs-h3); font-weight: var(--fw-med); }',
'.hero__read span { display: block; margin-top: 2px; }',
'',
'.hero__cue { position: absolute; left: var(--pad-x); bottom: 16px; z-index: 2; display: flex; align-items: center; gap: 10px; }',
'.hero__cue i { display: block; width: 46px; height: var(--bd); background: var(--line-2); position: relative; overflow: hidden; }',
".hero__cue i::after { content: ''; position: absolute; inset: 0; background: var(--acc); transform-origin: left; }",
'html.mo .hero__cue i::after { animation: cue 2.4s var(--e2) infinite; }',
'@keyframes cue { 0% { transform: scaleX(0); transform-origin: left; } 55% { transform: scaleX(1); transform-origin: left; } 56% { transform-origin: right; } 100% { transform: scaleX(0); transform-origin: right; } }',
'',
''].join('\n');

s = s.slice(0, heroStart) + newHero + s.slice(heroEnd);

/* 2) Секции — как v8: волосяная линия сверху */
s = s.replace(
  '.sec { padding-block: var(--gap-sec) 0; position: relative; z-index: 1; scroll-margin-top: 90px; }',
  '.sec { padding-block: var(--gap-sec) 0; position: relative; z-index: 1; scroll-margin-top: 90px; border-top: var(--bd) solid var(--line); }'
);

/* 3) Документы в хронике — вписывать целиком (не резать) */
s = s.replace(
  '.seq__img { background-size: cover; background-position: center 18%; background-repeat: no-repeat; }',
  [
  '.seq__doc { display: grid; place-items: center; background: var(--bg-3); padding: clamp(12px, 2.4vw, 30px); min-height: 0; }',
  '.seq__doc img { max-width: 100%; max-height: 100%; width: auto; height: auto; object-fit: contain; }',
  '.seq__img { background-size: contain; background-position: center; background-repeat: no-repeat; }'
  ].join('\n')
);

/* 4) Портрет специалиста — не резать голову */
s = s.replace(
  '.spec__fig img { width: 100%; max-width: 380px; transform: translate3d(0, var(--plx, 0), 0); }',
  '.spec__fig img { width: 100%; max-width: 380px; object-fit: contain; object-position: 50% 0%; transform: translate3d(0, var(--plx, 0), 0); }'
);

/* 5) Блок «Təlimlər» — фото студентов отдельно от дипломов */
const trainCss = [
'/* ─────────── TƏLİMLƏR · фото студентов (отдельно от дипломов) ─────────── */',
'.train__grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: clamp(16px, 2.4vw, 30px); margin-top: clamp(26px, 4.4vh, 48px); }',
'.train__card { border: var(--bd) solid var(--line); border-radius: var(--r); overflow: clip; background: var(--bg-2); }',
'.train__ph { display: grid; place-items: center; background: var(--bg-3); aspect-ratio: 16 / 10; padding: 10px; }',
'.train__ph img { max-width: 100%; max-height: 100%; width: auto; height: auto; object-fit: contain; }',
'.train__cap { padding: 14px 16px 18px; display: flex; flex-direction: column; gap: 6px; }',
'@media (max-width: 900px) { .train__grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }',
'@media (max-width: 560px) { .train__grid { grid-template-columns: 1fr; } }',
'',
'/* ─────────────────── ХРОНИКА (кадр на шаг) ─────────────────── */'].join('\n');
s = s.replace('/* ─────────────────── ХРОНИКА (кадр на шаг) ─────────────────── */', trainCss);

/* 6) Мобильный герой — без скраба */
s = s.replace('  .hero { min-height: 92svh; }', '  .hero { height: auto; }\n  .hero__stage { position: relative; height: auto; min-height: 92svh; }');

fs.writeFileSync(f, s);
console.log('nur.css обновлён:', s.length, 'байт');
console.log('проверки:', /hero__stage/.test(s), /seq__doc/.test(s), /train__grid/.test(s), /is-click/.test(s));
