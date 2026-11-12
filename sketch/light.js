/* Живой свет: тёмная комната с лампой (ночь) или дневной свет на бумаге (бумага, сепия).
   Цвета берутся из CSS-переменных темы: сменили тему — свет перекрасился сам. */
import * as THREE from 'three';

const FRAG = `
precision highp float;
uniform vec2 uRes; uniform float uT; uniform vec2 uM; uniform vec3 uBg; uniform vec3 uA; uniform vec3 uB; uniform float uMode; uniform float uK;
float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
float noise(vec2 p){ vec2 i = floor(p), f = fract(p); f = f*f*(3.0-2.0*f);
  return mix(mix(hash(i), hash(i+vec2(1.,0.)), f.x), mix(hash(i+vec2(0.,1.)), hash(i+vec2(1.,1.)), f.x), f.y); }
float fbm(vec2 p){ float v = 0.0, a = 0.5; for(int i=0;i<5;i++){ v += a*noise(p); p = p*2.03 + 17.0; a *= 0.5; } return v; }
void main(){
  vec2 uv = gl_FragCoord.xy / uRes; float asp = uRes.x / uRes.y; vec2 p = vec2(uv.x * asp, uv.y);
  vec2 lamp = vec2(0.26 * asp + (uM.x - 0.5) * 0.30, 0.66 + (uM.y - 0.5) * 0.20);
  float d = distance(p, lamp);
  float n = fbm(p * 1.5 + vec2(uT * 0.020, -uT * 0.014));
  float n2 = fbm(p * 3.1 - vec2(uT * 0.026, uT * 0.010));
  float glow = exp(-d * 1.7) * (0.50 + 0.70 * n) + exp(-d * 5.5) * 0.30;
  float g2 = exp(-distance(p, vec2(0.92 * asp, 0.10)) * 2.2) * (0.35 + 0.65 * n2);
  vec3 col;
  float vig = smoothstep(1.20, 0.30, length((uv - 0.5) * vec2(1.15, 1.0)));
  if (uMode > 0.5) {
    col = uBg + uA * glow * 0.40 * uK + uB * g2 * 0.55 * uK;
    col *= mix(0.72, 1.0, vig);
  } else {
    col = mix(uBg * (0.955 + 0.045 * n), uA, clamp(glow * 0.80 * uK, 0.0, 1.0));
    col = mix(col, uB, clamp(g2 * 0.20 * uK + (1.0 - vig) * 0.07, 0.0, 1.0));
  }
  col += (hash(gl_FragCoord.xy + fract(uT) * 91.7) - 0.5) * 0.020;
  gl_FragColor = vec4(col, 1.0);
}`;

const DUST_V = `
attribute vec3 aSeed; uniform float uT; uniform float uPx; uniform vec2 uM;
varying float vA;
void main(){
  float sp = 0.006 + aSeed.z * 0.012;
  vec2 p = position.xy;
  p.y = mod(p.y + 1.0 + uT * sp, 2.0) - 1.0;
  p.x += sin(uT * (0.08 + aSeed.x * 0.12) + aSeed.y * 6.283) * 0.025 + (uM.x - 0.5) * 0.04 * (0.3 + aSeed.z);
  vA = (0.35 + 0.65 * abs(sin(uT * (0.25 + aSeed.y * 0.5) + aSeed.x * 6.283))) * smoothstep(-1.0, -0.6, p.y) * smoothstep(1.0, 0.5, p.y);
  gl_Position = vec4(p, 0.0, 1.0);
  gl_PointSize = (1.2 + aSeed.z * 3.4) * uPx;
}`;
const DUST_F = `
precision highp float; uniform vec3 uC; uniform float uO; varying float vA;
void main(){ float d = length(gl_PointCoord - 0.5); float a = smoothstep(0.5, 0.0, d); gl_FragColor = vec4(uC, a * a * vA * uO); }`;

export function initLight(canvas) {
  let renderer;
  try { renderer = new THREE.WebGLRenderer({ canvas, antialias: false, alpha: false, powerPreference: 'high-performance' }); }
  catch (e) { return null; }                                   /* нет WebGL — остаётся ровный фон темы */
  const small = matchMedia('(max-width: 760px)').matches;
  const dpr = Math.min(window.devicePixelRatio || 1, small ? 1.25 : 1.5);
  renderer.setPixelRatio(dpr);
  const scene = new THREE.Scene(), cam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const U = { uRes: { value: new THREE.Vector2(1, 1) }, uT: { value: 0 }, uM: { value: new THREE.Vector2(.5, .5) },
    uBg: { value: new THREE.Color() }, uA: { value: new THREE.Color() }, uB: { value: new THREE.Color() }, uMode: { value: 1 }, uK: { value: 1 } };
  scene.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), new THREE.ShaderMaterial({ uniforms: U, vertexShader: 'void main(){ gl_Position = vec4(position.xy, 0.0, 1.0); }', fragmentShader: FRAG, depthTest: false, depthWrite: false })));

  const N = small ? 70 : 190, pos = new Float32Array(N * 3), seed = new Float32Array(N * 3);
  for (let i = 0; i < N; i++) { pos[i * 3] = Math.random() * 2 - 1; pos[i * 3 + 1] = Math.random() * 2 - 1; seed[i * 3] = Math.random(); seed[i * 3 + 1] = Math.random(); seed[i * 3 + 2] = Math.random(); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos, 3)); g.setAttribute('aSeed', new THREE.BufferAttribute(seed, 3));
  const DU = { uT: U.uT, uM: U.uM, uPx: { value: dpr }, uC: { value: new THREE.Color() }, uO: { value: .5 } };
  const dustMat = new THREE.ShaderMaterial({ uniforms: DU, vertexShader: DUST_V, fragmentShader: DUST_F, transparent: true, depthTest: false, depthWrite: false, blending: THREE.AdditiveBlending });
  const dust = new THREE.Points(g, dustMat); dust.frustumCulled = false; scene.add(dust);

  const T = { bg: new THREE.Color(), a: new THREE.Color(), b: new THREE.Color(), dust: new THREE.Color(), mode: 1, o: .5 };
  function readTheme(instant) {
    const cs = getComputedStyle(document.documentElement), v = n => cs.getPropertyValue(n).trim();
    T.bg.set(v('--bg')); T.a.set(v('--light-a')); T.b.set(v('--light-b')); T.dust.set(v('--dust'));
    T.mode = parseFloat(v('--light-mode')) || 0; T.o = T.mode > .5 ? .55 : .42;
    dustMat.blending = T.mode > .5 ? THREE.AdditiveBlending : THREE.NormalBlending; dustMat.needsUpdate = true;
    if (instant) { U.uBg.value.copy(T.bg); U.uA.value.copy(T.a); U.uB.value.copy(T.b); DU.uC.value.copy(T.dust); U.uMode.value = T.mode; DU.uO.value = T.o; }
  }
  function size() { const w = innerWidth, h = innerHeight; renderer.setSize(w, h, false); U.uRes.value.set(w * dpr, h * dpr); }
  const mouse = { x: .5, y: .5 };
  addEventListener('pointermove', e => { mouse.x = e.clientX / innerWidth; mouse.y = 1 - e.clientY / innerHeight; }, { passive: true });
  addEventListener('resize', size);
  let k = 1, raf = 0, t0 = performance.now();
  function frame(now) {
    raf = requestAnimationFrame(frame);
    U.uT.value = (now - t0) / 1000;
    U.uM.value.x += (mouse.x - U.uM.value.x) * .04; U.uM.value.y += (mouse.y - U.uM.value.y) * .04;
    const target = 1 - Math.min(1, scrollY / (innerHeight * 1.1)) * .5;           /* за героем свет вдвое тише, но не гаснет */
    k += (target - k) * .06; U.uK.value = k;
    U.uBg.value.lerp(T.bg, .07); U.uA.value.lerp(T.a, .07); U.uB.value.lerp(T.b, .07); DU.uC.value.lerp(T.dust, .07);
    U.uMode.value += (T.mode - U.uMode.value) * .2; if (Math.abs(T.mode - U.uMode.value) < .02) U.uMode.value = T.mode;
    DU.uO.value += (T.o - DU.uO.value) * .07;
    renderer.render(scene, cam);
  }
  document.addEventListener('visibilitychange', () => { if (document.hidden) { cancelAnimationFrame(raf); raf = 0; } else if (!raf) raf = requestAnimationFrame(frame); });
  readTheme(true); size(); raf = requestAnimationFrame(frame);
  canvas.classList.add('is-on');
  return { setTheme: () => readTheme(false) };
}
