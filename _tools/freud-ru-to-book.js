/* =====================================================================
   _tools/freud-ru-to-book.js — русские web-книги Фрейда (ragimoff.org)
   Каркас страниц — тот же, что у AZ-книг (_tools/epub-to-book.js): шаблон
   book-template.json, стили TOC_STYLE, сайдбар, нижняя навигация d-nav,
   data-lang-url-* и /_lang-switch.js. Ничего нового не изобретаем.
   Источник текстов: русское зеркало freudproject.ru
   (D:/Документы/ZFreud/site_freudproject_ru — markdown из content/).
   Выход: books/<slug>/ru/index.html + books/<slug>/ru/<глава>/index.html
   Плюс синхронизация языковых атрибутов на AZ-страницах этих же книг.
   Запуск: node _tools/freud-ru-to-book.js
   ===================================================================== */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SRC = 'D:/Документы/ZFreud/site_freudproject_ru';
const TPL = JSON.parse(fs.readFileSync(path.join(__dirname, 'book-template.json'), 'utf8'));
const LSV = 6;                                   /* версия _lang-switch.js (?v=) */

const UI = { toc: 'СОДЕРЖАНИЕ', back: 'Книги', home: 'Главная', up: 'Книга' };
const YEAR = '2026';

function up(s) { return String(s).toUpperCase(); }
function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

/* ─────────────────────────── чистка текста источника ─────────────────────────── */

/* подписи переводчика/издательства/сайта-зеркала: в книгу не идут */
const JUNK_ONE = [
  /^#\s/, /^- \*\*(ID|Дата|Категории|URL)/, /^freudproject\.ru Last updated:/,
  /^https?:\/\/freudproject\.ru/, /^ПРЕДЛАГАЕМЫЙ ТЕКСТ/, /^Заметили ошибку\?/,
  /^\[Примечание freudproject\.ru\]/, /^Оставить заявку$/, /^Сверка с источником произведена$/,
  /^Читать$/, /^Сноски:$/,
  /* редакторские вставки русских изданий/зеркала — не текст Фрейда */
  /^Перевод .{0,60}дополнен редакторскими/,
  /^Tepмuн/i
];
/* выкинуть абзац-заголовок и следующий за ним абзац (редакторские примечания) */
const JUNK_DROP_NEXT = [
  /^Вводное примечание издателей/i, /^Вводное замечание издателей/i,
  /^От редакции/i, /^От переводчика/i, /^Примечание издателей/i, /^Предисловие издателей/i
];
/* «шапка: значение» — гасим и следующую строку (значение отдельным абзацем) */
const JUNK_SKIP = [
  /^Библиографический индекс:/, /^Библиографическое название:/, /^Источник( \(|:)/,
  /^Первоисточник:/, /^Оригинальное название:/, /^Оригинальный текст:/,
  /^Перевод( с немецкого)?( \(наст\.\))?:/, /^Последняя редакция текста:/,
  /^Постоянная ссылка для цитирования в научных работах:~?/
];
/* всё, что после этого заголовка в посте, — издательский аппарат: чтение прекращаем */
const JUNK_STOP = /^О письме:$/;
/* заголовок + список строк под ним (список переводов, оглавление книги) */
const JUNK_SERIES = [
  { head: /^Существующие переводы на рус\. яз\.:/, item: /^\d+\.\s/ },
  { head: /^Оглавление:$/, item: /^Очерк\s/ }
];
const SIG = /^(Бонн|Вена|Париж|Берлин|Рим|Гамбург|Лейпциг|Лондон|Цюрих), [а-яё]+ \d{4} года$/;
const BRACKET_ONLY = /^\[[^\]]{0,160}\]$/;
const NOTE = /^\[(\d+)[.\]]*\s*([\s\S]+)$/;
const NOTE_STAR = /^\[\*\]\s*([\s\S]+)$/;
const READTIME = /^Время на прочтение:.{0,40}?(?=[А-ЯЁ\[])|^Время на прочтение:.*$/;
/* строка-маркер начала очерка: «I. Египтянин Моисей» — дублирует заголовок главы */
const ROMAN = /^(I|II|III|IV|V)\.\s+\S/;

function clean(blocks, heads, opts) {
  const o = opts || {};
  const out = [];              /* {t:'p'|'h3'|'sig', text} */
  const notes = [];
  const HEAD = new Set((heads || []).map((h) => h.replace(/\s*\[\*\]\s*$/, '').replace(/\*+$/, '').trim()));
  let series = null, skipNext = false;

  for (const raw of blocks) {
    let b = raw.replace(/\r/g, '').replace(/[\u00a0\u2009\u202f]/g, ' ').replace(/\u00ad/g, '').replace(/[ \t]+/g, ' ').trim();
    b = b.split('\n').map((x) => x.trim()).filter(Boolean).join(' ');
    if (!b || b === '---') continue;
    b = b.replace(READTIME, '').trim();          /* «Время на прочтение: 13 мин.» */
    if (!b) continue;
    if (JUNK_STOP.test(b)) break;                /* дальше — только аппарат издания */
    if (skipNext) { skipNext = false; continue; }
    if (series) { if (series.test(b)) continue; series = null; }
    if (JUNK_ONE.some((re) => re.test(b))) continue;
    if (JUNK_DROP_NEXT.some((re) => re.test(b))) { skipNext = true; continue; }
    const js = JUNK_SERIES.find((x) => x.head.test(b));
    if (js) { series = js.item; continue; }
    const sk = JUNK_SKIP.find((re) => re.test(b));
    if (sk) { if (b.slice(b.match(sk)[0].length).trim() === '') skipNext = true; continue; }
    if (BRACKET_ONLY.test(b)) continue;
    if (o.dropRoman && b.length < 100 && ROMAN.test(b)) continue;

    const n = b.match(NOTE);
    if (n) { notes.push({ mark: n[1], text: n[2].trim() }); continue; }
    const ns = b.match(NOTE_STAR);
    if (ns) { notes.push({ mark: '*', text: ns[1].trim() }); continue; }

    const plain = b.replace(/\s*\[\*\]\s*$/, '').replace(/\*+$/, '').trim();
    if (HEAD.has(plain)) { out.push({ t: 'h3', text: plain }); continue; }
    if (SIG.test(b)) { out.push({ t: 'sig', text: b }); continue; }
    out.push({ t: 'p', text: b });
  }
  return { body: out, notes };
}

/* ─────────────────────────── источник: части книги ─────────────────────────── */

function mdBlocks(file) {
  const txt = fs.readFileSync(file, 'utf8');
  const i = txt.indexOf('\n---');
  const body = i >= 0 ? txt.slice(i + 4) : txt;
  return body.split(/\n\s*\n/).map((s) => s.trim()).filter(Boolean);
}
function srcFile(dir, id) {
  const list = fs.readdirSync(dir).filter((f) => f.startsWith(id + '_') && f.endsWith('.md'));
  if (!list.length) throw new Error('нет источника ' + id + ' в ' + dir);
  return path.join(dir, list[0]);
}
/* часть книги: пост (id) целиком либо срез от маркера `from` до `to`.
   `ex` — маркеры-заголовки, совпадающие с блоком ЦЕЛИКОМ («I.», «II.» — иначе
   строка «I.» поймала бы любой абзац, начинающийся с «I.»); сам маркер в тело
   не идёт — он становится заголовком главы. */
function partBlocks(id, from, to, ex) {
  const blocks = mdBlocks(srcFile(path.join(SRC, 'content/books_full_texts'), id));
  /* маркеры сверяем по нормализованному тексту: в источнике узкие/неразрывные пробелы */
  const head = (b) => b.replace(/[\u00a0\u2009\u202f]/g, ' ').replace(/\s+/g, ' ').replace(/[\s*]+$/, '').trim();
  const at = (marker, exact) => {
    const i = blocks.findIndex((b) => (exact ? head(b) === marker : head(b).startsWith(marker)));
    if (i < 0) throw new Error('маркер не найден: ' + marker);
    return i;
  };
  const fromI = from ? at(from, !!(ex && ex.from)) : 0;
  const toI = to ? at(to, !!(ex && ex.to)) : blocks.length;
  return blocks.slice(from && ex && ex.from ? fromI + 1 : fromI, toI);
}

/* ─────────────────────────── источник: письма Марте Бернайс ─────────────────────────── */

const MONTHS = { 'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8, 'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12 };
const PAD = (x) => String(x).padStart(2, '0');

function lettersList() {
  const cat = JSON.parse(fs.readFileSync(path.join(SRC, 'api/catalog_letters.json'), 'utf8')).martha;
  return cat.items.map((it) => {
    const id = (it.link.match(/\?p=(\d+)/) || [])[1];
    const [day, month] = String(it.title).trim().split(/\s+/);
    const y = Number(it.year), d = Number(day), m = MONTHS[month];
    if (!id || !y || !d || !m) throw new Error('разбор письма: ' + JSON.stringify(it));
    return { id, y, m, d,
      title: 'Письмо от ' + d + ' ' + month + ' ' + y, short: d + ' ' + month + ' ' + y,
      slug: 'pismo-' + y + '-' + PAD(m) + '-' + PAD(d),
      file: srcFile(path.join(SRC, 'content/letters'), id) };
  }).sort((a, b) => (a.y - b.y) || (a.m - b.m) || (a.d - b.d));
}

/* ─────────────────────────── книги ─────────────────────────── */

const BOOKS = [
  {
    slug: 'freud-musa', logo: 'MT', year: YEAR,
    ruTitle: 'Человек Моисей и монотеистическая религия', ruSubtitle: 'Зигмунд Фрейд', ruAuthor: 'Зигмунд Фрейд',
    intro: 'Первое издание — 1939', ruYear: '1939',
    chapters: [
      { slug: 'ocherk-i-egipcyanin-moisei', title: 'Очерк I. Египтянин Моисей', src: { id: '7485' },
        heads: ['Вводное примечание издателей немецкого Studienausgabe'] },
      { slug: 'ocherk-ii-esli-moisei-byl-egipcyanin', title: 'Очерк II. Если Моисей был египтянин…', src: { id: '7520' }, heads: [] },
      { slug: 'ocherk-iii-razdel-i', title: 'Очерк III. Моисей, его народ и монотеистическая религия. Раздел I', src: { id: '7522' },
        heads: ['Предварительное замечание 1', 'Предварительное замечание 2', 'А. Историческая предпосылка', 'В. Латентный период и традиция', 'С. Аналогия', 'D. Конкретное приложение', 'Е. Трудности'] },
      { slug: 'ocherk-iii-razdel-ii', title: 'Очерк III. Моисей, его народ и монотеистическая религия. Раздел II', src: { id: '7528' },
        heads: ['Итог и повторение', 'а) Народ израильский', 'б) Великий человек', 'в) Прогресс духовности', 'г) Отказ от влечений', 'д) Содержащаяся в религии истина', 'е) Возвращение вытесненного', 'ж) Историческая правда', 'з) Историческое развитие'] }
    ]
  },
  {
    slug: 'freud-seksualligin-psixologiyasi', logo: 'SP', year: YEAR,
    ruTitle: 'Три очерка по теории сексуальности', ruSubtitle: 'Зигмунд Фрейд', ruAuthor: 'Зигмунд Фрейд',
    intro: 'Первое издание — 1905', ruYear: '1905',
    chapters: [
      { slug: 'predisloviya', title: 'Предисловия к 3-му и 4-му изданиям', src: { id: '14242', from: 'Предисловие автора к 3-му изданию', to: 'I. Сексуальные отклонения' },
        heads: ['Предисловие автора к 3-му изданию', 'Предисловие автора к 4-му изданию'] },
      { slug: 'ocherk-i-seksualnye-otkloneniya', title: 'Очерк I. Сексуальные отклонения',
        src: { id: '14242', from: 'I. Сексуальные отклонения', to: 'II. Инфантильная сексуальность' },
        heads: ['Отступление в отношении сексуального объекта', 'А. Инверсия', 'Поведение инвертированных', 'Взгляд на инверсию', 'Дегенерация', 'Врожденность', 'Объяснение инверсии', 'Введение бисексуальности', 'Половой объект инвертированных', 'Сексуальная цель инвертированных', 'Выводы', 'Отступление в отношении сексуальной цели', 'А) Переход за анатомические границы', 'Переоценка сексуального объекта', 'Сексуальное применение слизистой оболочки рта и губ', 'Сексуальное применение заднего прохода', 'Значение других частей тела', 'Несоответствующая замена сексуального объекта — фетишизм', 'Б) Фиксации предварительных сексуальных целей', 'Возникновение новых намерений', 'Ощупывание и разглядывание', 'Садизм и мазохизм', '3. Общее о перверсиях', 'Вариации и болезнь', 'Участие психики в перверсиях', 'Два вывода', '4. Сексуальное влечение у невротиков', 'Психоанализ', 'Результаты психоанализа', 'Невроз и перверсия', 'Частичные влечения и эрогенные зоны', 'Ссылка на инфантилизм сексуальности'] },
      { slug: 'ocherk-ii-infantilnaya-seksualnost', title: 'Очерк II. Инфантильная сексуальность',
        src: { id: '14242', from: 'II. Инфантильная сексуальность', to: 'III. Преобразования при половом созревании' },
        heads: ['Недостаточное внимание к инфантильным', 'Инфантильная амнезия', 'Латентный сексуальный период детства и его нарушения', 'Сексуальные задержки', 'Реактивные образования и сублимирования', 'Прорывы латентного периода', 'Выражения инфантильной сексуальности', 'Аутоэротизм', 'Сексуальная цель инфантильной сексуальности', 'Признаки эрогенных зон', 'Инфантильная сексуальная цель', 'Мастурбационные сексуальные проявления', 'Проявление зоны заднего прохода', 'Проявление генитальной зоны', 'Вторая фаза детской мастурбации', 'Возвращение младенческой мастурбации', 'Полиморфно-перверсное предрасположение', 'Частичные влечения', 'Инфантильное сексуальное исследование', 'Влечение к познанию', 'Загадка сфинкса', 'Комплекс кастрации и зависть к пенису', 'Теория рождения', 'Садистское понимание сексуального общения', 'Типичная неудача детского сексуального исследования', 'Фазы развития сексуальной организации', 'Прегенитальные организации', 'Амбивалентность', 'Выбор объекта в два срока', 'Источники инфантильной сексуальности', 'Механические возбуждения', 'Работа мускулатуры', 'Аффективные процессы', 'Интеллектуальная работа', 'Различные сексуальные конституции', 'Пути взаимного влияния'] },
      { slug: 'ocherk-iii-preobrazovaniya-pri-polovom-sozrevanii', title: 'Очерк III. Преобразования при половом созревании',
        src: { id: '14242', from: 'III. Преобразования при половом созревании' },
        heads: ['Сексуальное возбуждение', 'Механизм предварительного наслаждения', 'Опасности предварительного наслаждения', 'Проблемы сексуального возбуждения', 'Роль сексуальных выделений', 'Оценка внутренних половых частей', 'Химическая теория', 'Теория либидо', 'Руководящие зоны у мужчины и женщины', 'Нахождение объекта', 'Сексуальный объект во время младенчества', 'Инфантильный страх', 'Ограничения инцеста', 'Влияние инфантильного выбора объекта', 'Предупреждение инверсии', 'Резюме', 'Нарушающие развитие моменты', 'Конституция и наследственность', 'Дальнейшая переработка', 'Вытеснение', 'Сублимирование', 'Пережитое случайно', 'Преждевременная зрелость', 'Временные моменты', 'Цепкость', 'Фиксация'] }
    ]
  },
  {
    slug: 'freud-sevgi-mektublari', logo: 'SM', year: YEAR,
    ruTitle: 'Письма Марте Бернайс (1882–1886)', ruSubtitle: 'Зигмунд Фрейд', ruAuthor: 'Зигмунд Фрейд',
    intro: 'Первое издание — 1882–1886', ruYear: '1882–1886',
    letters: true,
    chapters: [{ slug: 'o-pismah', title: 'Письма Марте Бернайс (1882–1886)', short: 'Предисловие', src: { id: '7020' } }]
  },
  {
    /* «Недовольство культурой» (Das Unbehagen in der Kultur, 1930).
       Русский текст — зеркало freudproject.ru, пост 818 (пер. А.М. Руткевич).
       Азербайджанского издания в архиве нет → книга выходит только на русском
       (ruOnly): переключатель языка не показываем, hreflang az не объявляем.
       Главы в источнике — римские номера отдельными абзацами («I.» … «VIII.»):
       маркеры сверяются целиком (ex), иначе «I.» поймал бы любой абзац с «I.». */
    slug: 'freud-medeniyyetin-sancilari', logo: 'MS', year: YEAR,
    ruTitle: 'Недовольство культурой', ruSubtitle: 'Зигмунд Фрейд', ruAuthor: 'Зигмунд Фрейд',
    intro: 'Первое издание — 1930', ruYear: '1930',
    ruOnly: true,
    chapters: [
      { slug: 'glava-i', title: 'I', src: { id: '818', from: 'I.', to: 'II.', ex: { from: true, to: true } }, heads: [] },
      { slug: 'glava-ii', title: 'II', src: { id: '818', from: 'II.', to: 'III.', ex: { from: true, to: true } }, heads: [] },
      { slug: 'glava-iii', title: 'III', src: { id: '818', from: 'III.', to: 'IV.', ex: { from: true, to: true } }, heads: [] },
      { slug: 'glava-iv', title: 'IV', src: { id: '818', from: 'IV.', to: 'V.', ex: { from: true, to: true } }, heads: [] },
      { slug: 'glava-v', title: 'V', src: { id: '818', from: 'V.', to: 'VI.', ex: { from: true, to: true } }, heads: [] },
      { slug: 'glava-vi', title: 'VI', src: { id: '818', from: 'VI.', to: 'VII.', ex: { from: true, to: true } }, heads: [] },
      { slug: 'glava-vii', title: 'VII', src: { id: '818', from: 'VII.', to: 'VIII.', ex: { from: true, to: true } }, heads: [] },
      { slug: 'glava-viii', title: 'VIII', src: { id: '818', from: 'VIII.', ex: { from: true } }, heads: [] }
    ]
  }
];

/* ─────────────────────────── каркас страниц (как в epub-to-book.js) ─────────────────────────── */

const TOC_STYLE = '<style>' +
  '.home-hero{padding:16px 0 11px}' +
  '.book-toc{margin:8px auto 36px}' +
  '.book-toc .toc-title{margin:0 0 16px 0;padding-bottom:8px}' +
  '.content-wrap .toc-test{margin:0 0 34px}' +
  '.d-nav{display:flex;align-items:center;justify-content:space-between;gap:.5rem;margin:2.2rem 0 .5rem;padding:.7rem 0 0;border-top:1px solid var(--border)}' +
  '.d-nav a{color:var(--text);text-decoration:none;padding:.35rem .7rem;border-radius:6px;font-family:var(--mono,monospace);font-weight:700;font-size:.95rem;white-space:nowrap;max-width:42%;overflow:hidden;text-overflow:ellipsis}' +
  '.d-nav .up{color:var(--gold);font-family:var(--font);font-weight:600}' +
  '.d-nav .dn-name{color:var(--text2);font-weight:400;font-family:var(--font);font-size:.85rem}' +
  '.content-wrap p{font-size:clamp(16.5px,1.05rem,19px);line-height:1.78;margin:0 0 1.05em;color:var(--text)}' +
  /* титул книги: название · автор · год издания — ровно, без пустоты снизу */
  '.home-hero{padding:4px 0 2px}' +
  '.home-hero h1.home-title{font-size:clamp(22px,4.4vw,32px);line-height:1.18;letter-spacing:.01em;margin:0}' +
  '.home-hero .sub{font-size:15px;line-height:1.5;margin:10px 0 0;color:var(--text2);letter-spacing:.02em}' +
  '.home-hero .sub:first-of-type{color:var(--text)}' +
  '.book-toc{margin:16px auto 6px}' +
  '.book-toc .toc-chapter{margin:0}' +
  '.content-wrap{padding-top:.6rem;padding-bottom:2rem}' +
  '@media(max-width:600px){.content-wrap{padding-left:18px;padding-right:18px}.content-wrap p{font-size:17.5px;line-height:1.8}}' +
  '.sidebar .nav-sub-link{padding:7px 14px 7px 18px;font-size:12.5px;gap:12px}' +
  '.sidebar .sub-code{flex:0 0 auto;width:auto;white-space:nowrap;margin-right:0;font-size:10.5px}' +
  '.sidebar .nav-sub-link.is-active{color:var(--gold);border-left-color:var(--gold);background:var(--gold-bg)}' +
  /* русские книги: подзаголовки внутри главы, примечания, подпись автора */
  '.content-wrap h3.sub{font-size:1rem;font-weight:700;line-height:1.35;margin:1.5rem 0 .5rem;padding:0;border:0;color:var(--text)}' +
  '.content-wrap .sig{color:var(--text2);font-style:italic;text-align:right;margin:.9rem 0 1.4rem}' +
  '.content-wrap .notes{margin:2.4rem 0 0;padding-top:1.1rem;border-top:1px solid var(--border)}' +
  '.content-wrap .notes-title{font-size:.8rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin:0 0 .7rem}' +
  '.content-wrap .note{font-size:.92rem;line-height:1.6;margin:0 0 .5em;color:var(--text2)}' +
  '.content-wrap .note .note-n{color:var(--gold)}' +
  '</style>';

function headHtml(b, href, title, desc, css) {
  const azUrl = 'https://ragimoff.org/books/' + b.slug + '/' + (href ? href : '');
  const ruUrl = 'https://ragimoff.org/books/' + b.slug + '/ru/' + (href ? href : '');
  /* книга только на русском (азербайджанского издания нет): az-адрес и hreflang az не объявляем —
     иначе переключатель предлагал бы несуществующую страницу, а alternate врал бы поисковику */
  const alt = b.ruOnly
    ? '  <link rel="canonical" href="' + ruUrl + '" />\n\n' +
      '  <link rel="alternate" hreflang="ru" href="' + ruUrl + '" />\n\n' +
      '  <link rel="alternate" hreflang="x-default" href="' + ruUrl + '" />'
    : '  <link rel="canonical" href="' + ruUrl + '" />\n\n' +
      '  <link rel="alternate" hreflang="az" href="' + azUrl + '" />\n\n' +
      '  <link rel="alternate" hreflang="ru" href="' + ruUrl + '" />\n\n' +
      '  <link rel="alternate" hreflang="x-default" href="' + azUrl + '" />';
  return TPL.head
    .replace('<html lang="az">',
      '<html data-langs="' + (b.ruOnly ? 'ru' : 'az,ru') + '" ' +
      (b.ruOnly ? '' : 'data-lang-url-az="/books/' + b.slug + '/" ') +
      'data-lang-url-ru="/books/' + b.slug + '/ru/" ' +
      'data-lang-avail="' + (b.ruOnly ? 'ru' : 'az ru') + '" lang="ru">')
    .replace('<link rel="stylesheet" href="style.css">', '<link rel="stylesheet" href="' + (css || 'style.css') + '">')
    .replace(/<title>[\s\S]*?<\/title>/, '<title>' + esc(title) + ' | ' + esc(up(b.ruTitle)) + '</title>')
    .replace(/<meta name="description" content="[^"]*"/, '<meta name="description" content="' + esc(desc) + '"')
    .replace(/<meta property="og:title" content="[^"]*"/, '<meta property="og:title" content="' + esc(title) + '"')
    .replace(/<meta property="og:description" content="[^"]*"/, '<meta property="og:description" content="' + esc(desc) + '"')
    .replace(/<meta property="og:url" content="[^"]*"/, '<meta property="og:url" content="https://ragimoff.org/books/' + b.slug + '/ru/"')
    .replace(/"name":"[^"]*","inLanguage":"[^"]*"/, '"name":"' + esc(b.ruTitle) + '","inLanguage":"ru"')
    .replace(/"author":\{"@type":"Person","name":"[^"]*"\}/, '"author":{"@type":"Person","name":"' + esc(b.ruAuthor) + '"}')
    .replace(/\n[ \t]*<link rel="canonical"[\s\S]*?x-default[^>]*>/, '\n' + alt)
    .replace('</head>', TOC_STYLE + '</head>');
}

function bodyTop(b) {
  return TPL.bodyTop
    .replace(/<div class="hdr-logo">[^<]*<\/div>/, '<div class="hdr-logo">' + b.logo + '</div>')
    .replace(/<a href="https:\/\/ragimoff\.org" class="hdr-back"[^>]*>/, '<a href="https://ragimoff.org/ru/" class="hdr-back" title="Вернуться на главную сайта">')
    .replace(/<strong>[^<]*<\/strong>/, '<strong>' + esc(up(b.ruTitle)) + '</strong>')
    .replace(/<small>[^<]*<\/small>/, '<small>' + esc(b.ruAuthor) + ' · ' + (b.ruYear || b.year) + '</small>')
    .replace('data-lang-switch', 'data-lang-switch data-langs="' + (b.ruOnly ? 'ru' : 'az,ru') +
      '" data-lang-avail="' + (b.ruOnly ? 'ru' : 'az ru') + '"')
    .replace('src="/_lang-switch.js"', 'src="/_lang-switch.js?v=' + LSV + '"');
}

function sidebarHtml(list, idx, pre) {
  const items = list.map((c, i) =>
    '<div class="nav-item"><a href="' + pre + c.slug + '/index.html" class="nav-sub-link' + (i === idx ? ' is-active' : '') + '">' +
    '<span class="sub-code">' + c.num + '</span><span class="sub-name">' + esc(c.short || c.title) + '</span></a></div>').join('\n      ');
  return '<aside class="sidebar" id="sb">\n    <div class="sb-hdr"><a class="sb-site" href="https://ragimoff.org/books/" title="' + UI.back + '">← ' + UI.back + '</a>' +
    '<button class="sb-close" onclick="toggleSb()" aria-label="Закрыть">✕</button></div>\n    <nav>\n      ' +
    '<div class="nav-item"><a href="' + pre + 'index.html" class="nav-link nav-front">' + UI.home + '</a></div>\n      ' +
    items + '\n    </nav>\n  </aside>';
}

function bodyHtml(r) {
  let html = '';
  r.body.forEach((p) => {
    if (p.t === 'h3') html += '<h3 class="sub">' + esc(p.text) + '</h3>\n';
    else if (p.t === 'sig') html += '<p class="sig">' + esc(p.text) + '</p>\n';
    else html += '<p>' + esc(p.text) + '</p>\n';
  });
  if (r.notes.length) {
    html += '<div class="notes"><h2 class="notes-title">Примечания</h2>\n' +
      r.notes.map((n) => '<p class="note"><span class="note-n">[' + esc(n.mark) + ']</span> ' + esc(n.text) + '</p>').join('\n') + '\n</div>\n';
  }
  return html;
}

function chapterPage(b, list, idx) {
  const ch = list[idx];
  const prev = idx > 0 ? list[idx - 1] : null, next = idx < list.length - 1 ? list[idx + 1] : null;
  const content = '\n<nav class="crumb"><a href="../index.html">‹ ' + esc(b.ruTitle) + '</a></nav>\n' +
    '<h1 class="chap-title-wrap"><span class="chap-title">' + esc(ch.title) + '</span></h1>\n' +
    bodyHtml(ch.parts) +
    '<nav class="d-nav">' +
    (prev ? '<a href="../' + prev.slug + '/index.html">← ' + prev.num + ' <span class="dn-name">' + esc(prev.short || prev.title) + '</span></a>' : '<span></span>') +
    '<a class="up" href="../index.html">↑ ' + UI.up + '</a>' +
    (next ? '<a href="../' + next.slug + '/index.html"><span class="dn-name">' + esc(next.short || next.title) + '</span> ' + next.num + ' →</a>' : '<span></span>') +
    '</nav>\n' + TPL.tail;
  return headHtml(b, ch.slug + '/index.html', ch.title, b.ruTitle + ' — ' + ch.title, '../style.css') + '\n</head>\n' +
    bodyTop(b) + sidebarHtml(list, idx, '../') + TPL.mid + TPL.contentOpen + content;
}

function indexPage(b, list) {
  const cards = list.map((c) =>
    '<div class="toc-chapter"><a href="' + c.slug + '/index.html" class="toc-chapter-title"><span class="toc-name">' + esc(c.title) + '</span></a></div>').join('\n      ');
  const content = '\n<div class="home-hero"><h1 class="home-title">' + esc(up(b.ruTitle)) + '</h1>' +
    '<p class="sub">' + esc(b.ruSubtitle) + '</p>' +
    '<p class="sub">' + esc(b.intro) + '</p></div>\n' +
    '<section class="book-toc"><h2 class="toc-title">' + esc(up(UI.toc)) + '</h2>\n      ' + cards + '\n    </section>\n';
  return headHtml(b, '', b.ruTitle, b.ruTitle + ' — ' + b.ruSubtitle) + '\n</head>\n' +
    bodyTop(b) + sidebarHtml(list, -1, '') + TPL.mid + TPL.contentOpen + content;
}

/* ─────────────────────────── сборка глав книги ─────────────────────────── */

function buildChapters(b) {
  const list = [];
  b.chapters.forEach((c) => {
    if (b.letters) {
      const blocks = mdBlocks(srcFile(path.join(SRC, 'content/articles'), c.src.id));
      const cut = blocks.findIndex((x) => /^(Год|18\d\d|19[01]\d)(\s|$)/.test(x.replace(/\r/g, '').trim()));
      const r = clean(cut > 0 ? blocks.slice(0, cut) : blocks, []);
      list.push({ slug: c.slug, title: c.title, short: c.short, parts: r });
    } else {
      const r = clean(partBlocks(c.src.id, c.src.from, c.src.to, c.src.ex), c.heads, { dropRoman: !c.src.ex });
      list.push({ slug: c.slug, title: c.title, short: c.short, parts: r });
    }
  });
  if (b.letters) {
    lettersList().forEach((L) => {
      const r = clean(mdBlocks(L.file), []);
      list.push({ slug: L.slug, title: L.title, short: L.short, parts: r });
    });
  }
  list.forEach((c, i) => { c.num = String(i + 1).padStart(2, '0'); });
  return list;
}

/* ─────────────────────────── языковые атрибуты AZ-страниц ─────────────────────────── */

function patchAz(slug, ru) {
  const dir = path.join(ROOT, 'books', slug);
  const langs = ru ? 'az,ru' : 'az';
  const avail = ru ? 'az ru' : 'az';
  let n = 0;
  fs.readdirSync(dir).filter((f) => f.endsWith('.html')).forEach((f) => {
    const file = path.join(dir, f);
    let h = fs.readFileSync(file, 'utf8');
    const before = h;
    const lang = (h.match(/<html[^>]*\slang="([a-z]{2})"/) || [])[1] || 'az';
    /* <html>: языки книги, адреса языковых версий, доступные языки */
    h = h.replace(/<html[^>]*>/, '<html data-langs="' + langs + '" data-lang-url-az="/books/' + slug + '/"' +
      (ru ? ' data-lang-url-ru="/books/' + slug + '/ru/"' : '') + ' data-lang-avail="' + avail + '" lang="' + lang + '">');
    /* переключатель: новая версия скрипта (обход кэша) + список языков */
    h = h.replace(/src="\/_lang-switch\.js(?:\?v=\d+)?"/, 'src="/_lang-switch.js?v=' + LSV + '"');
    h = h.replace(/<div class="lang-switch-bar"[^>]*>/,
      '<div class="lang-switch-bar" data-lang-switch data-langs="' + langs + '" data-lang-avail="' + avail +
      '" style="display:inline-flex;gap:6px;margin-left:14px;vertical-align:middle">');
    /* canonical/hreflang — на свою книгу, а не на «Клиническую психиатрию» */
    const canon = 'https://ragimoff.org/books/' + slug + '/' + (f === 'index.html' ? '' : f);
    const alt = '  <link rel="canonical" href="' + canon + '" />\n\n' +
      '  <link rel="alternate" hreflang="az" href="' + canon + '" />\n\n' +
      (ru ? '  <link rel="alternate" hreflang="ru" href="https://ragimoff.org/books/' + slug + '/ru/" />\n\n' : '') +
      '  <link rel="alternate" hreflang="x-default" href="' + canon + '" />';
    h = h.replace(/\n[ \t]*<link rel="canonical"[\s\S]*?x-default[^>]*>/, '\n' + alt);
    if (h !== before) { fs.writeFileSync(file, h, 'utf8'); n++; }
  });
  return n;
}

/* ─────────────────────────── запуск ─────────────────────────── */
/* node _tools/freud-ru-to-book.js [slug …] — без аргументов собираются все книги,
   с аргументами — только перечисленные (чтобы не переписывать уже опубликованные). */

const only = process.argv.slice(2).filter((x) => !x.startsWith('-'));
const WANTED = only.length ? BOOKS.filter((b) => only.includes(b.slug)) : BOOKS;
if (only.length && WANTED.length !== only.length) {
  throw new Error('неизвестный slug: ' + only.filter((s) => !BOOKS.some((b) => b.slug === s)).join(', '));
}

let pages = 0;
WANTED.forEach((b) => {
  const style = path.join(ROOT, 'klinik-psixiatriya', 'style.css');
  const dir = path.join(ROOT, 'books', b.slug, 'ru');
  const list = buildChapters(b);
  fs.mkdirSync(dir, { recursive: true });
  if (fs.existsSync(style)) fs.copyFileSync(style, path.join(dir, 'style.css'));
  list.forEach((ch, i) => {
    const d = path.join(dir, ch.slug);
    fs.mkdirSync(d, { recursive: true });
    fs.writeFileSync(path.join(d, 'index.html'), chapterPage(b, list, i), 'utf8');
    pages++;
  });
  fs.writeFileSync(path.join(dir, 'index.html'), indexPage(b, list), 'utf8');
  pages++;
  console.log(b.slug + ': глав ' + list.length + ' → books/' + b.slug + '/ru/');
});
/* AZ-страницы: у трёх книг появляется русская версия, у двух — только AZ.
   Книга только с русской версией (ruOnly) AZ-страниц не имеет — пропускаем. */
WANTED.filter((b) => !b.ruOnly).forEach((b) => console.log('AZ ' + b.slug + ': страниц обновлено ' + patchAz(b.slug, true)));
if (!only.length) {
  ['freud-yuxularin-yozumu', 'freud-psixoanalizle-tanishliq'].forEach((s) =>
    console.log('AZ ' + s + ': страниц обновлено ' + patchAz(s, false)));
}
console.log('всего страниц:', pages);
