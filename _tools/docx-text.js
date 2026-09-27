/* Извлечение параграфов из DOCX (без зависимостей):
   unzip -p <file> word/document.xml | node _tools/docx-text.js [--json] */
'use strict';
const { execFileSync } = require('child_process');

function getXml(file) {
  return execFileSync('unzip', ['-p', file, 'word/document.xml'], { maxBuffer: 200 * 1024 * 1024 }).toString('utf8');
}

function decode(s) {
  return s
    .replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"').replace(/&apos;/g, "'")
    .replace(/&amp;/g, '&')
    .replace(/&#(\d+);/g, (m, d) => String.fromCharCode(+d));
}

function paragraphs(xml) {
  const out = [];
  const re = /<w:p[ >][\s\S]*?<\/w:p>|<w:p\/>/g;
  let m;
  while ((m = re.exec(xml)) !== null) {
    const p = m[0];
    const style = (p.match(/<w:pStyle w:val="([^"]+)"/) || [])[1] || '';
    const texts = [];
    const tr = /<w:t[^>]*>([\s\S]*?)<\/w:t>/g;
    let t;
    while ((t = tr.exec(p)) !== null) texts.push(decode(t[1]));
    let text = texts.join('').replace(/\s+/g, ' ').trim();
    // Санитайзер: в этих DOCX часть текста содержит XML-мусор (w:tab, w:spacing…),
    // попавший в содержимое при генерации файла. Убираем всё, что похоже на разметку.
    text = text
      .replace(/<[^>]*>/g, ' ')
      .replace(/\bw:[a-zA-Z]+/g, ' ')
      .replace(/[\u0000-\u001f]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
    if (!text || /^[\s"'/<>:=.-]*$/.test(text)) continue;
    const bold = /<w:b\/>|<w:b w:val="(1|true)"/.test(p);
    const italic = /<w:i\/>|<w:i w:val="(1|true)"/.test(p);
    const sz = (p.match(/<w:sz w:val="(\d+)"/) || [])[1];
    if (text) out.push({ style, text, bold, italic, sz: sz ? +sz : 0 });
  }
  return out;
}

const file = process.argv[2];
const mode = process.argv[3] || '';
const paras = paragraphs(getXml(file));
if (mode === '--json') {
  process.stdout.write(JSON.stringify(paras));
} else {
  console.log('параграфов:', paras.length);
  const styles = {};
  paras.forEach((p) => { styles[p.style || '(нет)'] = (styles[p.style || '(нет)'] || 0) + 1; });
  console.log('стили:', JSON.stringify(styles));
  const sizes = {};
  paras.forEach((p) => { if (p.sz) sizes[p.sz] = (sizes[p.sz] || 0) + 1; });
  console.log('размеры (half-points):', JSON.stringify(sizes));
  console.log('жирных:', paras.filter((p) => p.bold).length, '| курсив:', paras.filter((p) => p.italic).length);
  console.log('\n— первые 40 —');
  paras.slice(0, 40).forEach((p, i) => console.log(String(i).padStart(3) + (p.bold ? ' B' : '  ') + (p.sz ? ' s' + p.sz : '') + ' | ' + p.text.slice(0, 110)));
}
