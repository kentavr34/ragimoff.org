/* =====================================================================
   RAGIMOFF · _tools/dsgen.js — генерация изображений и видео через DashScope
   (ключи irada/jobus, воркспейс MaaS).
   Использование:
     node _tools/dsgen.js img "<prompt>" <out.jpg> [size]
     node _tools/dsgen.js vid "<prompt>" <out.mp4> [--img=<url>] [model]
   Модели: img → qwen-image-plus | qwen-image | wan2.5-t2i-preview
           vid → wan2.5-i2v-preview (i2v) | wan2.6-t2v (t2v) | wan2.2-i2v-plus
   ===================================================================== */
'use strict';
const fs = require('fs');
const https = require('https');

const KEYS = [
  { k: 'sk-ws-H.DHIIIPP.CZHl.MEQCIEaBzGBGC2dlNRVO4UaP7Cmi-5yjMSliby31Iq0zifF3AiBGYAUz8iCyg0oYdBJ8TWrP0T0IU-GBK7yLVZhR1Qpr2g', h: 'ws-hjjvdfh3rd6k4o9g', n: 'irada' },
  { k: 'sk-ws-H.DDMPDIH.9dZ1.MEYCIQCuwtVIELZ7JzZn9LAzfLsEpD8hctmRGSYRokmEWxe6NgIhAKg73JNg4J8FadBlvM1ho8OeHJVZpJMSYfXgMYhdRoh3', h: 'ws-mucsfuhay761ev1c', n: 'jobus' }
];
let keyIdx = 0;

function req(method, url, headers, body) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const r = https.request({ method, hostname: u.hostname, path: u.pathname + u.search, headers: headers || {} }, (res) => {
      let data = '';
      res.on('data', (d) => (data += d));
      res.on('end', () => resolve({ status: res.statusCode, body: data }));
    });
    r.on('error', reject);
    r.setTimeout(120000, () => { r.destroy(new Error('timeout')); });
    if (body) r.write(typeof body === 'string' ? body : JSON.stringify(body));
    r.end();
  });
}

function dl(url, out) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    https.get({ hostname: u.hostname, path: u.pathname + u.search }, (res) => {
      if (res.statusCode !== 200) return reject(new Error('HTTP ' + res.statusCode));
      const f = fs.createWriteStream(out);
      res.pipe(f);
      f.on('finish', () => { f.close(() => resolve(out)); });
    }).on('error', reject);
  });
}

async function start(path, payload) {
  const K = KEYS[keyIdx % KEYS.length];
  const r = await req('POST', `https://${K.h}.ap-southeast-1.maas.aliyuncs.com/api/v1${path}`,
    { 'Authorization': 'Bearer ' + K.k, 'Content-Type': 'application/json', 'X-DashScope-Async': 'enable' },
    payload);
  let j = {};
  try { j = JSON.parse(r.body); } catch (e) {}
  const id = j.output && j.output.task_id;
  if (!id) throw new Error('нет task_id: ' + r.body.slice(0, 300));
  return { id, key: K };
}

async function wait(id, key, out, tries) {
  for (let i = 0; i < (tries || 40); i++) {
    await new Promise((r) => setTimeout(r, 5000));
    const r = await req('GET', `https://${key.h}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/${id}`,
      { 'Authorization': 'Bearer ' + key.k });
    let j = {};
    try { j = JSON.parse(r.body); } catch (e) {}
    const o = j.output || {};
    const st = o.task_status;
    process.stdout.write('  [' + (i + 1) + '] ' + st + '\n');
    if (st === 'SUCCEEDED') {
      const v = o.video_url || (o.results && o.results[0] && (o.results[0].url || o.results[0].video_url));
      if (!v) throw new Error('нет URL в ответе: ' + r.body.slice(0, 300));
      await dl(v, out);
      return out;
    }
    if (st === 'FAILED' || st === 'CANCELED') throw new Error('задача ' + st + ': ' + JSON.stringify(o).slice(0, 300));
  }
  throw new Error('таймаут ожидания');
}

(async function main() {
  const [mode, prompt, out, extra, model] = process.argv.slice(2);
  if (!mode || !prompt || !out) {
    console.log('использование: node dsgen.js img "<prompt>" out.jpg [size] | vid "<prompt>" out.mp4 [--img=URL] [model]');
    process.exit(1);
  }
  if (mode === 'img') {
    const size = extra || '1664*928';
    console.log('▶ изображение:', model || 'qwen-image-plus', size);
    const t = await start('/services/aigc/text2image/image-synthesis',
      { model: model || 'qwen-image-plus', input: { prompt }, parameters: { size, n: 1, prompt_extend: true } });
    console.log('  task:', t.id);
    await wait(t.id, t.key, out);
    console.log('✅ ' + out + ' (' + Math.round(fs.statSync(out).size / 1024) + ' КБ)');
  } else {
    const m = model || (extra && extra.indexOf('--img=') === 0 ? 'wan2.5-i2v-preview' : 'wan2.6-t2v');
    const input = { prompt };
    if (extra && extra.indexOf('--img=') === 0) input.img_url = extra.slice(6);
    console.log('▶ видео:', m, input.img_url ? '(image-to-video)' : '(text-to-video)');
    const t = await start('/services/aigc/video-generation/video-synthesis',
      { model: m, input, parameters: { resolution: '720P', duration: 5 } });
    console.log('  task:', t.id);
    await wait(t.id, t.key, out, 60);
    console.log('✅ ' + out + ' (' + Math.round(fs.statSync(out).size / 1024) + ' КБ)');
  }
})().catch((e) => { console.error('❌ ' + e.message); process.exit(1); });
