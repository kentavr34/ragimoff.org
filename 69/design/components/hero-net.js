/* ═══════════════════════════════════════════════════════════════════
   ГЕРОЙ: СЕТЬ ИНТЕЛЛЕКТА
   ═══════════════════════════════════════════════════════════════════
   Что должно транслировать (слова владельца, 11.11.2026):
     «Doctor Ragimoff — Школа Психологии… вход в новое пространство
      интеллекта и развития — достичь своих жизненных целей пользуясь
      своим интеллектом».
     И отказ: «нет визуала который вызывает уважение».

   ПОЧЕМУ ИМЕННО СЕТЬ, А НЕ АБСТРАКТНЫЕ ЧАСТИЦЫ:
     абстрактные частицы — это «красиво» и бессмысленно, их ставит любой.
     Сеть читается как МЫШЛЕНИЕ: узлы, связи, импульсы по связям.
     Это предмет школы, а не украшение.

   ТРИ СМЫСЛА, ЗАЛОЖЕННЫЕ В ДВИЖЕНИЕ:
     1. интеллект   — узлы и связи, как нейронная сеть
     2. развитие    — импульсы бегут по связям, сеть живёт
     3. цель        — при прокрутке импульсы сходятся к ядру, сеть собирается

   ПОЧЕМУ БЕЗ BLENDER: владелец запретил держать Blender на машине
   (только через MCP). Поэтому визуал построен на Three.js —
   он работает в браузере в реальном времени, реагирует на мышь
   и весит меньше, чем 120 отрендеренных кадров.

   ТРЕБОВАНИЕ ВЛАДЕЛЬЦА: если делать — делать хорошо, иначе не тратить время.
   ═══════════════════════════════════════════════════════════════════ */

export function initHeroNet(canvas, opts = {}) {
  const THREE = opts.THREE;
  if (!THREE || !canvas) return null;

  const NODES = opts.nodes || 220;
  /* предел длины связи: при большем значении в плотной правой части
     связей становится столько, что структура превращается в шум */
  const LINK_DIST = opts.linkDist || 1.75;
  const GOLD = 0xC9A961;
  const GOLD_LIGHT = 0xE8D9A8;

  /* ── СВЕЧЕНИЕ БЕЗ ПОСТОБРАБОТКИ ───────────────────────────────────
     EffectComposer/bloom требует файлов examples, которых у нас нет.
     Рисуем мягкое свечение текстурой: радиальный градиент на canvas.
     Тот же эффект, вес — ноль, работает везде. */
  function glowTexture(size = 128) {
    const c = document.createElement('canvas');
    c.width = c.height = size;
    const g = c.getContext('2d');
    const r = size / 2;
    const grad = g.createRadialGradient(r, r, 0, r, r, r);
    /* ПРИЧИНА: свечение было «мыльным» — это и читалось как дёшево.
       Теперь ядро точки резкое, ореол короткий: узел читается как
       металлическая точка, а не как размытое пятно. */
    grad.addColorStop(0.0, 'rgba(255,250,238,1)');
    grad.addColorStop(0.10, 'rgba(255,244,215,1)');
    grad.addColorStop(0.26, 'rgba(232,209,150,0.55)');
    grad.addColorStop(0.52, 'rgba(201,169,97,0.14)');
    grad.addColorStop(1.0, 'rgba(201,169,97,0)');
    g.fillStyle = grad;
    g.fillRect(0, 0, size, size);
    const t = new THREE.CanvasTexture(c);
    t.needsUpdate = true;
    return t;
  }

  const sprite = glowTexture();

  /* ── УЗЛЫ: ПОТОК, А НЕ ШАР ────────────────────────────────────────
     ПРИЧИНА ПЕРЕДЕЛКИ (оценка визуала 11.11.2026): первая версия была
     симметричной сферой — «безлико, как скринсейвер», «штамп». Проблема
     не в исполнении, а в замысле: симметричная сеть ничего не говорит.

     ЧТО ГОВОРИТ ТЕПЕРЬ: сеть — это ПОТОК. Слева он разреженный и тусклый
     (начало пути), к правому верхнему углу — плотный и яркий (цель).
     Это и есть «достичь своих жизненных целей, пользуясь интеллектом»:
     движение видно глазом, без слов.

     Асимметрия задана намеренно: центр пуст, масса смещена. Глаз идёт
     по потоку слева направо — туда же, куда смотрит текстовая часть. */
  /* ЗОНА ПОРТРЕТА, КУДА ГРАФИКЕ НЕЛЬЗЯ.
     Замер кадра 1440x900: портрет занимает x 500–1110 px (35%–77%)
     и y 125–900 px (14%–100%). Пересчёт в координаты камеры при
     FOV 46, z 17 и взгляде в точку (8, 0.9): экран покрывает
     x ≈ -3.5…19.5, y ≈ -6.3…8.1. Отсюда запретная область ниже.
     Графика туда не попадает — «паутина на лице» исключена расчётом,
     а не приглушением. */
  const FORBID = { x1: 4.2, x2: 14.4, y1: -6.4, y2: 5.6 };
  const blocked = (x, y) => x > FORBID.x1 && x < FORBID.x2 && y > FORBID.y1 && y < FORBID.y2;

  const pos = [];
  for (let i = 0; i < NODES; i++) {
    /* Смещение вправо: в центре и слева расположены лица (портрет
       специалиста), и любая графика там читается как помеха. Правая
       часть кадра — стена и свет: там сеть уместна и не спорит
       с человеком. Это главное исправление после аудита. */
    const t = Math.pow(Math.random(), 0.72);
    let x, y;
    /* Свободные зоны кадра: правая колонна (правее портрета) и верхняя
       полоса (над головой). Там сеть читается как глубина пространства,
       а не как помеха на человеке. */
    if (i % 5 < 3) {
      // правая колонна
      x = 14.6 + Math.random() * 4.6;
      y = -5.6 + Math.random() * 11.4;
    } else {
      // верхняя полоса над портретом
      x = FORBID.x1 - 8.2 + Math.random() * 10.5;
      y = 5.8 + Math.random() * 2.2;
    }
    // разброс сужается к цели — поток «собирается», но не слипается:
    // при 0.72 узлы превращались в пятно и структура терялась
    if (blocked(x, y)) { i--; continue; }   // страховка: в портрет не лезем
    const z = (Math.random() * 2 - 1) * 3.2;
    pos.push(new THREE.Vector3(x, y, z));
  }

  const geometry = new THREE.BufferGeometry();
  const positions = new Float32Array(NODES * 3);
  const sizes = new Float32Array(NODES);
  const phases = new Float32Array(NODES);
  pos.forEach((p, i) => {
    positions[i * 3] = p.x;
    positions[i * 3 + 1] = p.y;
    positions[i * 3 + 2] = p.z;
    sizes[i] = 0.55 + Math.random() * 0.75;
    phases[i] = Math.random() * Math.PI * 2;
  });
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

  const nodeMat = new THREE.PointsMaterial({
    size: 0.78,
    map: sprite,
    color: GOLD_LIGHT,
    transparent: true,
    opacity: 0.66,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
    sizeAttenuation: true
  });
  const nodePoints = new THREE.Points(geometry, nodeMat);

  /* ── СВЯЗИ: то, что превращает точки в мышление ───────────────── */
  const linkPairs = [];
  const linkVerts = [];
  for (let i = 0; i < NODES; i++) {
    for (let j = i + 1; j < NODES; j++) {
      const d = pos[i].distanceTo(pos[j]);
      if (d <= LINK_DIST) {
        linkPairs.push([i, j, d]);
        linkVerts.push(pos[i].x, pos[i].y, pos[i].z);
        linkVerts.push(pos[j].x, pos[j].y, pos[j].z);
      }
    }
  }
  const linkGeo = new THREE.BufferGeometry();
  linkGeo.setAttribute('position', new THREE.Float32BufferAttribute(linkVerts, 3));
  const linkMat = new THREE.LineBasicMaterial({
    color: GOLD,
    transparent: true,
    /* ПРИЧИНА: связи почти не читались на фоне свечения. Подняты — теперь
       видна структура, а не облако. Структуру и уважают. */
    opacity: 0.2,
    blending: THREE.AdditiveBlending,
    depthWrite: false
  });
  const linkLines = new THREE.LineSegments(linkGeo, linkMat);

  /* ── ИМПУЛЬСЫ МЫСЛИ: бегут по связям ──────────────────────────────
     Это ключевая деталь: сеть не статична, по ней идёт движение.
     Именно оно читается как «живой интеллект», а не как схема. */
  const PULSES = opts.pulses || 34;
  const pulseGeo = new THREE.BufferGeometry();
  const pulsePos = new Float32Array(PULSES * 3);
  pulseGeo.setAttribute('position', new THREE.BufferAttribute(pulsePos, 3));
  const pulseMat = new THREE.PointsMaterial({
    size: 1.5,
    map: sprite,
    color: 0xFFF3D6,
    transparent: true,
    opacity: 1,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
    sizeAttenuation: true
  });
  const pulsePoints = new THREE.Points(pulseGeo, pulseMat);

  const pulses = [];
  for (let k = 0; k < PULSES; k++) {
    pulses.push({
      link: Math.floor(Math.random() * Math.max(1, linkPairs.length)),
      t: Math.random(),
      speed: 0.12 + Math.random() * 0.34,
      dir: Math.random() > 0.5 ? 1 : -1
    });
  }

  /* ── ЯДРО: точка, к которой всё сходится ───────────────────────── */
  const coreGeo = new THREE.SphereGeometry(0.14, 16, 16);
  const coreMat = new THREE.MeshBasicMaterial({
    color: 0xFFF6E2, transparent: true, opacity: 0.9,
    blending: THREE.AdditiveBlending, depthWrite: false
  });
  const core = new THREE.Mesh(coreGeo, coreMat);
  /* ЦЕЛЬ потока: правый край, куда сеть собирается. Не центр сцены —
     центр читался бы как «нейтральное ядро», а нам нужна цель. */
  core.position.set(17.6, 1.2, 0);
  const coreHalo = new THREE.Sprite(new THREE.SpriteMaterial({
    map: sprite, color: GOLD_LIGHT, transparent: true,
    opacity: 0.55, blending: THREE.AdditiveBlending, depthWrite: false
  }));
  coreHalo.scale.set(2.6, 2.6, 1);
  core.add(coreHalo);

  /* ── ПЫЛЬ: глубина пространства ───────────────────────────────── */
  const DUST = 900;
  const dustGeo = new THREE.BufferGeometry();
  const dustPos = new Float32Array(DUST * 3);
  for (let i = 0; i < DUST; i++) {
    const r = 11 + Math.random() * 16;
    const th = Math.random() * Math.PI * 2;
    const ph = Math.acos(Math.random() * 2 - 1);
    dustPos[i * 3] = r * Math.sin(ph) * Math.cos(th);
    dustPos[i * 3 + 1] = r * Math.sin(ph) * Math.sin(th) * 0.55;
    dustPos[i * 3 + 2] = r * Math.cos(ph);
  }
  dustGeo.setAttribute('position', new THREE.BufferAttribute(dustPos, 3));
  const dust = new THREE.Points(dustGeo, new THREE.PointsMaterial({
    size: 0.26, map: sprite, color: 0x7C93B8, transparent: true,
    opacity: 0.22, depthWrite: false, blending: THREE.AdditiveBlending,
    sizeAttenuation: true
  }));

  /* ── СБОРКА СЦЕНЫ ─────────────────────────────────────────────── */
  const scene = new THREE.Scene();
  const group = new THREE.Group();
  group.add(linkLines, nodePoints, pulsePoints, dust);
  scene.add(group);
  scene.add(core);

  /* Камера смотрит на поток сбоку и чуть сверху — так видно направление
     движения. При взгляде «в лоб» поток не читается, теряется смысл. */
  const camera = new THREE.PerspectiveCamera(46, 1, 0.1, 140);
  camera.position.set(6.2, 2.2, 17.0);
  camera.lookAt(8.0, 0.9, 0);

  const renderer = new THREE.WebGLRenderer({
    canvas, antialias: true, alpha: true, powerPreference: 'high-performance'
  });
  renderer.setClearColor(0x000000, 0);

  /* ── УПРАВЛЕНИЕ: мышь + прокрутка ─────────────────────────────── */
  const state = { mx: 0, my: 0, tmx: 0, tmy: 0, progress: 0, tprogress: 0 };

  function onMove(e) {
    const x = (e.touches ? e.touches[0].clientX : e.clientX) / window.innerWidth;
    const y = (e.touches ? e.touches[0].clientY : e.clientY) / window.innerHeight;
    state.tmx = (x - 0.5) * 2;
    state.tmy = (y - 0.5) * 2;
  }
  window.addEventListener('mousemove', onMove, { passive: true });
  window.addEventListener('touchmove', onMove, { passive: true });

  function setProgress(p) { state.tprogress = Math.max(0, Math.min(1, p)); }
  function measure() {
    /* ПРИЧИНА: canvas оставался 300x150 — при инициализации размеры
       контейнера ещё не были посчитаны и вызов давал ноль. Теперь берём
       максимум из доступных источников и не полагаемся ни на один. */
    const par = canvas.parentElement;
    const w = Math.max(
      canvas.clientWidth, par ? par.clientWidth : 0,
      window.innerWidth, 1
    );
    const h = Math.max(
      canvas.clientHeight,
      par && par.clientHeight > 0 ? par.clientHeight : 0,
      window.innerHeight, 1
    );
    return { w, h };
  }
  function resize() {
    const { w, h } = measure();
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  window.addEventListener('resize', resize);
  resize();
  /* раскладка могла измениться после первой отрисовки — повторяем */
  requestAnimationFrame(resize);
  setTimeout(resize, 120);
  setTimeout(resize, 500);
  if (window.ResizeObserver && canvas.parentElement) {
    try { new ResizeObserver(resize).observe(canvas.parentElement); } catch (e) {}
  }

  /* ── АНИМАЦИЯ ─────────────────────────────────────────────────── */
  const clock = new THREE.Clock();
  const tmpA = new THREE.Vector3();
  const tmpB = new THREE.Vector3();

  function frame() {
    const dt = Math.min(clock.getDelta(), 0.05);
    const t = clock.elapsedTime;

    // плавное следование за мышью
    state.mx += (state.tmx - state.mx) * Math.min(1, dt * 3.2);
    state.my += (state.tmy - state.my) * Math.min(1, dt * 3.2);
    state.progress += (state.tprogress - state.progress) * Math.min(1, dt * 2.4);
    const p = state.progress;

    // базовое вращение + наклон за мышью
    /* ПРИЧИНА: у сферы вращение вокруг Y было основным. У ПОТОКА оно
       ломает композицию — поток уезжает вбок. Поэтому вращение слабое,
       а наклон — только от мыши: поток остаётся читаемым направлением. */
    group.rotation.y = t * 0.028 + state.mx * 0.2;
    group.rotation.x = state.my * 0.14 + Math.sin(t * 0.16) * 0.03;

    // импульсы: бегут по связям, к концу прокрутки чаще и ярче
    if (linkPairs.length) {
      const arr = pulseGeo.attributes.position.array;
      for (let k = 0; k < pulses.length; k++) {
        const pu = pulses[k];
        pu.t += dt * pu.speed * (1 + p * 1.9) * pu.dir;
        if (pu.t > 1 || pu.t < 0) {
          pu.t = pu.dir > 0 ? 0 : 1;
          pu.link = Math.floor(Math.random() * linkPairs.length);
          pu.speed = 0.12 + Math.random() * 0.34;
        }
        const L = linkPairs[pu.link];
        if (!L) continue;
        tmpA.copy(pos[L[0]]);
        tmpB.copy(pos[L[1]]);
        const x = tmpA.x + (tmpB.x - tmpA.x) * pu.t;
        const y = tmpA.y + (tmpB.y - tmpA.y) * pu.t;
        const z = tmpA.z + (tmpB.z - tmpA.z) * pu.t;
        arr[k * 3] = x; arr[k * 3 + 1] = y; arr[k * 3 + 2] = z;
      }
      pulseGeo.attributes.position.needsUpdate = true;
      pulseMat.opacity = 0.75 + p * 0.25;
    }

    // дыхание узлов
    nodeMat.opacity = 0.6 + Math.sin(t * 1.1) * 0.06 + p * 0.12;

    // к концу прокрутки сеть «собирается»: сжимается и светлеет
    const shrink = 1 - p * 0.18;
    group.scale.setScalar(shrink);
    core.scale.setScalar(0.7 + p * 0.9);
    coreHalo.material.opacity = 0.35 + p * 0.5;
    coreMat.opacity = 0.55 + p * 0.4;

    // камера подходит ближе — «вход в пространство».
    // ВАЖНО: lookAt пересчитывается каждый кадр. Если задать его один раз,
    // то после смещения position взгляд остаётся прежним и поток уходит
    // из кадра — это уже случалось при первой проверке.
    camera.position.set(6.2 + p * 0.4, 2.2 - p * 0.4, 17.0 - p * 3.0);
    camera.lookAt(8.0 + p * 0.6, 0.9 + p * 0.4, 0);

    renderer.render(scene, camera);
  }
  renderer.setAnimationLoop(frame);

  return {
    setProgress,
    dispose() {
      renderer.setAnimationLoop(null);
      window.removeEventListener('mousemove', onMove);
      window.removeEventListener('touchmove', onMove);
      window.removeEventListener('resize', resize);
      renderer.dispose();
    },
    get counts() {
      return { nodes: NODES, links: linkPairs.length, pulses: PULSES, dust: DUST };
    }
  };
}
