/* Извлекает диагностический тест «Карта моделей взаимоотношений» из DOCX книги
   «Эра Феникса» (AZ и RU) → _tools/phoenix-test.json
   Структура теста в книге: 12 блоков по моделям, 8 утверждений в блоке
   (у «Феникса» — 12), шкала 1–5, средний балл = сумма ÷ число вопросов блока. */
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

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
    text = text.replace(/<[^>]*>/g, ' ').replace(/\bw:[a-zA-Z]+/g, ' ').replace(/[\u0000-\u001f]/g, ' ').replace(/\s+/g, ' ').trim();
    if (text) out.push(text);
  }
  return out;
}

/* Блоки: «БЛОК 1. Модель «Лилит» (Вопросы 1–8)» / «BLOK 1. «Lilit» Modeli (Suallar 1–8)» */
const BLOCK_RX = /^(?:БЛОК|BLOK)\s*(\d+)[.\s]*[^\n]*?«([^»]+)»[^\n]*?\(?(?:Вопросы|Suallar)\s*(\d+)\s*[–-]\s*(\d+)\)?/i;
const Q_RX = /^(\d{1,3})\.\s+(.{12,})$/;
/* Раздел описания модели: «1. AD VƏ MƏNA» / «1. НАЗВАНИЕ И ЗНАЧЕНИЕ», до «2. …» */
const DESC_START = /^1\.\s*(AD VƏ MƏNA|НАЗВАНИЕ И ЗНАЧЕНИЕ)/i;
const DESC_END = /^2\.\s*(ŞÜAR VƏ İNANCLAR|СЛОГАН И УБЕЖДЕНИЯ)/i;
/* Сколько предложений брать в краткое описание модели (владелец: 8–10) */
const DESC_SENTENCES = 9;

function sentences(text) {
  return String(text).split(/(?<=[.!?…])\s+/).filter((s) => s.trim().length > 3);
}

function extract(file, lang) {
  const P = paragraphs(file);
  const blocks = [];
  let cur = null;
  let inTest = false;
  P.forEach((text) => {
    if (/ДИАГНОСТИЧЕСКИЙ ТЕСТ|DİAQNOSTİK TEST|DIAQNOSTIK TEST/i.test(text) && /РАЗДЕЛ\s*2|BÖLÜM\s*2|BÖLMƏ\s*2/i.test(text)) { inTest = true; return; }
    if (!inTest) return;
    if (/ИНСТРУКЦИЯ ПО ПОДСЧЁТУ|HESABLAMA QAYDASI|ПОДСЧЁТ РЕЗУЛЬТАТ/i.test(text)) { inTest = false; return; }
    const b = text.match(BLOCK_RX);
    if (b) { cur = { n: +b[1], model: b[2], from: +b[3], to: +b[4], questions: [] }; blocks.push(cur); return; }
    const q = text.match(Q_RX);
    if (q && cur) {
      const n = +q[1];
      if (n >= cur.from && n <= cur.to) cur.questions.push({ n, text: q[2].trim() });
    }
  });

  /* описания моделей — из глав книги: раздел «1. Название и значение» */
  let desc = null;
  const descriptions = {};
  P.forEach((text) => {
    const h = text.match(/^(?:BÖLÜM|Bölüm|bÖLÜM|ГЛАВА|Глава)\s*(\d+)\s*[.\s]+(?:MÜNASİBƏT MODELİ|МОДЕЛЬ ВЗАИМООТНОШЕНИЙ)/i);
    if (h) { desc = { n: +h[1], on: false, text: [] }; return; }
    if (!desc) return;
    if (DESC_START.test(text)) { desc.on = true; return; }
    if (DESC_END.test(text)) { desc.on = false; return; }
    if (desc.on) desc.text.push(text);
  });
  /* собираем по номеру модели (desc.n — номер главы: 1..12) */
  const byNumber = {};
  let cur2 = null;
  P.forEach((text) => {
    const h = text.match(/^(?:BÖLÜM|Bölüm|bÖLÜM|ГЛАВА|Глава)\s*(\d+)\s*[.\s]+(?:MÜNASİBƏT MODELİ|МОДЕЛЬ ВЗАИМООТНОШЕНИЙ)/i);
    if (h) { cur2 = { n: +h[1], on: false, parts: [] }; byNumber[cur2.n] = cur2; return; }
    if (!cur2) return;
    if (DESC_START.test(text)) { cur2.on = true; return; }
    if (DESC_END.test(text)) { cur2.on = false; return; }
    if (cur2.on) cur2.parts.push(text);
  });
  Object.values(byNumber).forEach((d) => {
    const model = blocks[d.n - 1] ? blocks[d.n - 1].model : null;
    if (!model) return;
    const out = [];
    let count = 0;
    for (const p of d.parts) {
      const ss = sentences(p);
      for (const s of ss) {
        if (count >= DESC_SENTENCES) break;
        out.push(s.trim());
        count++;
      }
      if (count >= DESC_SENTENCES) break;
    }
    if (out.length) descriptions[model] = out.join(' ');
  });

  return { lang, file: path.basename(file), blocks, descriptions };
}

const data = {
  note: 'Тест «Карта моделей взаимоотношений» из книги «Эра Феникса». Источник — DOCX книги.',
  scale: {
    ru: ['Совсем не верно для меня', 'Скорее не верно', 'Иногда верно', 'Скорее верно', 'Полностью верно для меня'],
    az: null, // заполнится из книги, если найдётся
  },
  langs: {
    ru: extract('D:/Документы/BOOKS/Phoenix/Era_Feniksa_1.docx rus.docx', 'ru'),
    az: extract('D:/Документы/BOOKS/Phoenix/Feniks_Erasi_v12-1 az.docx', 'az'),
  },
};

Object.entries(data.langs).forEach(([code, d]) => {
  console.log('=== ' + code + ': блоков ' + d.blocks.length + ', вопросов ' + d.blocks.reduce((n, b) => n + b.questions.length, 0));
  d.blocks.forEach((b) => console.log('   ' + b.n + '. «' + b.model + '» ' + b.from + '–' + b.to + ' → ' + b.questions.length + ' вопросов; первый: ' + (b.questions[0] ? b.questions[0].text.slice(0, 60) : 'НЕТ')));
});

fs.writeFileSync(path.join(__dirname, 'phoenix-test.json'), JSON.stringify(data, null, 2), 'utf8');
console.log('записано: _tools/phoenix-test.json');
