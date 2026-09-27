const { execFileSync } = require('child_process');
function decode(s) {
  return s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"')
    .replace(/&apos;/g, "'").replace(/&amp;/g, '&')
    .replace(/&#(\d+);/g, (m, d) => String.fromCharCode(+d));
}
function paragraphs(file) {
  const xml = execFileSync('unzip', ['-p', file, 'word/document.xml'], { maxBuffer: 300 * 1024 * 1024 }).toString('utf8');
  const out = [];
  const re = /<w:p[ >][\s\S]*?<\/w:p>|<w:p\/>/g;
  let m;
  while ((m = re.exec(xml)) !== null) {
    const p = m[0];
    const texts = [];
    const tr = /<w:t[^>]*>([\s\S]*?)<\/w:t>/g;
    let t;
    while ((t = tr.exec(p)) !== null) texts.push(decode(t[1]));
    let text = texts.join('').replace(/\s+/g, ' ').trim();
    text = text.replace(/<[^>]*>/g, ' ').replace(/\bw:[a-zA-Z]+/g, ' ')
      .replace(/[\u0000-\u001f]/g, ' ').replace(/\s+/g, ' ').trim();
    if (!text) continue;
    out.push({ text, sz: +((p.match(/<w:sz w:val="(\d+)"/) || [])[1] || 0), bold: /<w:b\/>|<w:b w:val="(1|true)"/.test(p) });
  }
  return out;
}
const file = process.argv[2];
const P = paragraphs(file);
const RX = /^(Глава|ГЛАВА|CHAPTER|Chapter|BÖLMƏ|Bölmə|bÖLÜM|BÖLÜM|FƏSİL|Fəsil|FƏSİL)\s*\d+|^(Глава|CHAPTER)\s*\d+\s*$/i;
const hits = P.map((p, i) => ({ i, ...p })).filter((p) => RX.test(p.text) && p.text.length < 90);
console.log('=== ' + file.split('/').pop() + ' | параграфов ' + P.length + ' | маркеров ' + hits.length + ' ===');
hits.slice(0, 26).forEach((p) => console.log(String(p.i).padStart(5) + (p.bold ? ' B' : '  ') + ' s' + p.sz + ' | ' + p.text.slice(0, 70)));
