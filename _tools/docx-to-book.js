/* =====================================================================
   RAGIMOFF · _tools/docx-to-book.js — конвертер книги DOCX → веб-книга
   Подструктура как у «Klinik Psixiatriya»: index.html (обложка + оглавление),
   страницы глав, style.css, сайдбар с оглавлением, навигация пред/след.

   Запуск:
     node _tools/docx-to-book.js <config.json>

   Конфиг (JSON):
   {
     "slug": "phoenix-era",
     "title": "Feniks Erası",
     "titleRu": "Эра Феникса",
     "author": "Samirə Rəhimova · Kənan Rəhimov",
     "year": "2026",
     "logo": "FE",
     "out": "books/phoenix-era",
     "styleFrom": "klinik-psixiatriya/style.css",
     "langs": [
       { "code": "az", "dir": "",    "file": "D:/…/Feniks_Erasi_v12-1 az.docx",  "title": "Feniks Erası",  "ui": "az" },
       { "code": "ru", "dir": "ru",  "file": "D:/…/Era_Feniksa_1.docx rus.docx",  "title": "Эра Феникса",   "ui": "ru" }
     ]
   }
   ===================================================================== */
'use strict';

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

/* ─────────── извлечение параграфов ─────────── */
function decode(s) {
  return s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"')
    .replace(/&apos;/g, "'").replace(/&amp;/g, '&')
    .replace(/&#(\d+);/g, (m, d) => String.fromCharCode(+d));
}

function paragraphs(file) {
  const xml = execFileSync('unzip', ['-p', file, 'word/document.xml'], { maxBuffer: 300 * 1024 * 1024 }).toString('utf8');
  const out = [];
  /* диапазоны таблиц: абзацы внутри <w:tbl> — ячейки, а не заголовки
     (в «Вирусе Вины» в таблицах встречаются «ВВЕДЕНИЕ», «РАЗДЕЛ 2» и подобное) */
  const tables = [];
  const tre = /<w:tbl>[\s\S]*?<\/w:tbl>/g;
  let tm;
  while ((tm = tre.exec(xml)) !== null) tables.push([tm.index, tm.index + tm[0].length]);
  const inTable = (pos) => tables.some(([a, b]) => pos >= a && pos < b);
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
    const bold = /<w:b\/>|<w:b w:val="(1|true)"/.test(p);
    const italic = /<w:i\/>|<w:i w:val="(1|true)"/.test(p);
    const sz = +((p.match(/<w:sz w:val="(\d+)"/) || [])[1] || 0);
    out.push({ text, bold, italic, sz, tbl: inTable(m.index) });
  }
  return out;
}

/* ─────────── распознавание структуры ─────────── */
const RX = {
  tocStart: /^(MÜNDƏRİCAT|СОДЕРЖАНИЕ|CONTENTS|İÇİNDƏKİLƏR)$/i,
  /* части: «FƏSİL 1», «ЧАСТЬ I», «PART III».
     ВАЖНО: в AZ-книге глава модели 12 помечена «FƏSİL 12. MÜNASİBƏT MODELİ» —
     это глава, а не часть; отличаем по слову «модель» в строке (modelMark). */
  part: /^(FƏSİL|FƏSIL|ЧАСТЬ|PART)\s+([IVXLC]+)(?![A-Za-zА-Яа-яƏəİıÖöÜüÇçŞşĞğ])/i,
  /* части в AZ: «I HİSSƏ»; разделы приложения («РАЗДЕЛ 1», «Part 1», «Section 2»,
     «3-CÜ BÖLMƏ») — главы, а не части */
  partAz: /^([IVXLC]+)\s+HİSSƏ(?![A-Za-zА-Яа-яƏəİıÖöÜüÇçŞşĞğ])/i,
  appendixSec: /^(РАЗДЕЛ|SECTION|PART|BÖLMƏ)\s*\d/i,
  /* интермедии: «ИНТЕРМЕДИЯ ПЕРВАЯ», «FIRST INTERLUDE», «INTERLUDE TWO», «BİRİNCİ İNTERMEDİYA» */
  intermedia: /^(ИНТЕРМЕДИЯ|ИНТЕРМЕЦЦО|ИНТЕРЛЮДИЯ|İNTERMEZZO|İntermezzo|İNTERLÜDİYA|(BİRİNCİ|İKİNCİ|ÜÇÜNCÜ|DÖRDÜNCÜ|Birinci|İkinci|Üçüncü|Dördüncü)\s+(ara səhnə|ara oyun|interlüd|İnterlüd)|INTERMEZZO|Intermezzo|INTERLUDE\s+(ONE|TWO|THREE|FOUR)|(FIRST|SECOND|THIRD|FOURTH)\s+INTERLUDE|BİRİNCİ\s+İNTERMEDİYA|İKİNCİ\s+İNTERMEDİYA|ÜÇÜNCÜ\s+İNTERMEDİYA|DÖRDÜNCÜ\s+İNTERMEDİYA)/i,
  appendix: /^(ПРИЛОЖЕНИЕ|APPENDIX|ƏLAVƏ)(?![A-Za-zА-Яа-яƏəİıÖöÜüÇçŞşĞğ])/i,
  closing: /^(ЗАКЛЮЧИТЕЛЬНОЕ\s+ПОСЛАНИЕ|CLOSING\s+MESSAGE)/i,
  /* глава AZ: «1-Cİ FƏSİL» — номер впереди */
  azChapter: /^\d+\s*[-–]?\s*(ci|cİ|cI|cı|cu|cU|cü|cÜ)\s+[fF][əƏeE][sS][iİıI][lL](?![A-Za-zА-Яа-яƏəİıÖöÜüÇçŞşĞğ])/i,
  modelMark: /MÜNASİBƏT MODELİ|МОДЕЛЬ ВЗАИМООТНОШЕНИЙ|MODEL OF RELATIONSHIPS/i,
  modelChapter: /^(FƏSİL|FƏSIL|ЧАСТЬ|PART)\s*([IVXLC]+|\d+)\b/i,
  chapter: /^(BÖLÜM|Bölüm|bÖLÜM|ГЛАВА|Глава|CHAPTER|Chapter)\s*\d+/,
  /* вводные разделы: «GİRİŞ», «ВВЕДЕНИЕ», а также «GİRİŞ. MÜƏLLİFDƏN MÜRACİƏT»,
     «ВВЕДЕНИЕ. ОБРАЩЕНИЕ АВТОРА». ВАЖНО: \b в JS не работает с кириллицей —
     границу слова задаём явным классом букв. */
  front: /^(GİRİŞ|Giriş|PROLOQ|Proloq|ВВЕДЕНИЕ|Введение|ПРОЛОГ|Пролог|INTRODUCTION|PROLOGUE|От автора|Müəllifdən|From the Author)(?![A-Za-zА-Яа-яƏəİıÖöÜüÇçŞşĞğ])/i,
  tocline: /(…|\.{3,}|\s\d{1,3}\s*$)/
};

/* нормализация для сопоставления названий из оглавления с телом книги */
function norm(s) {
  return String(s).toLowerCase()
    .replace(/[«»"'`.,:;!?()\[\]–—-]/g, ' ')
    .replace(/\s+/g, ' ').trim();
}

/* Список названий глав из оглавления (со страницами/выносками — чистим) */
function tocTitles(paras) {
  const start = paras.findIndex((p) => RX.tocStart.test(p.text));
  if (start < 0) return [];
  const titles = [];
  for (let i = start + 1; i < paras.length; i++) {
    const raw = paras[i].text;
    const isBody = (RX.chapter.test(raw) || RX.front.test(raw)) && !RX.tocline.test(raw) && raw.length < 120;
    if (isBody && titles.length) break;               // началось тело книги
    const clean = raw
      .replace(/[.…]{2,}/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
    /* в строке оглавления номер страницы может слипнуться со следующим разделом:
       «Proloq. Elmi əsas. 11 Fəsil 1. Yalançı Dəyərlər» → две отдельные записи */
    clean.split(/\s+(?=(?:Fəsil|FƏSİL|Сезон|Глава|Bölüm|Раздел|Школа)\s*\d)/i).forEach((piece) => {
      const p2 = piece.replace(/[.…\s]*\d{1,3}\s*$/, '').replace(/[.\s]+$/, '').replace(/\s+/g, ' ').trim();
      if (p2.length > 4 && p2.length < 130) titles.push(p2);
    });
  }
  return titles;
}

/* Разбиение тела по названиям из оглавления (первое совпадение после оглавления) */
function splitByToc(body, titles) {
  if (titles.length < 3) return null;
  const idxs = [];
  let from = 0;
  titles.forEach((title) => {
    const n = norm(title);
    const short = n.slice(0, 28);
    for (let i = from; i < body.length; i++) {
      const bn = norm(body[i].text);
      if (bn === n || (short.length > 8 && bn.startsWith(short))) { idxs.push({ i, title }); from = i + 1; return; }
    }
  });
  if (idxs.length < 3) return null;
  return idxs.map((o, k) => ({
    title: o.title,
    paras: body.slice(o.i + 1, k + 1 < idxs.length ? idxs[k + 1].i : body.length)
  }));
}

function buildChapters(paras) {
  /* разделы без маркера в DOCX — из конфига книги (cfg.extraChapters) */
  const EXTRA = global.__EXTRA || [];
  /* 1) найти область оглавления и вырезать её */
  let tocFrom = -1, tocTo = -1;
  for (let i = 0; i < paras.length; i++) {
    if (tocFrom < 0 && RX.tocStart.test(paras[i].text)) { tocFrom = i; continue; }
    if (tocFrom >= 0 && i > tocFrom) {
      const p = paras[i];
      const isHead = RX.part.test(p.text) || RX.chapter.test(p.text) || RX.front.test(p.text);
      if (isHead && !RX.tocline.test(p.text)) { tocTo = i; break; }
    }
  }
  const body = paras.slice(tocTo > 0 ? tocTo : 0).filter((p) =>
    !RX.tocline.test(p.text) || p.text.length > 120 ||
    /^(ГЛАВА|CHAPTER|BÖLMƏ|BÖLÜM|FƏSİL)\s*([IVXLC]+|\d+)\s*$/i.test(p.text));

  /* 1б) если в книге есть оглавление — режем по нему (самый надёжный путь).
     Принимаем результат только если он покрывает большинство названий из
     оглавления; иначе переходим к разбору по маркерам в тексте. */
  const titles = tocTitles(paras);
  const byToc = splitByToc(body, titles);
  /* Разбор «по оглавлению» принимаем только при почти полном совпадении:
     иначе теряются вступления, названные иначе, чем в оглавлении
     («ВВЕДЕНИЕ. ОБРАЩЕНИЕ АВТОРА» против «Введение. Пандемия, о которой молчат»). */
  if (global.__USE_TOC && byToc && titles.length && byToc.length >= Math.max(6, titles.length * 0.6)) {
    return byToc.map((ch) => ({ title: ch.title, paras: ch.paras, partTitle: '' }));
  }

  /* «Fəsil N» — часть или глава? В «Фениксе» есть маркеры «Bölüm/Глава/Chapter N»
     (там Fəsil — часть), в AZ-издании «Шизофрении» таких маркеров нет (там Fəsil — глава) */
  const fesilIsChapter = !body.some((p) => /^(BÖLÜM|Bölüm|bÖLÜM|ГЛАВА|Глава|CHAPTER|Chapter)\s*\d/.test(p.text));

  /* 2) разбить на части и главы */
  const parts = [];
  let curPart = null, curCh = null;
  function pushPart(title) { curPart = { title, chapters: [] }; parts.push(curPart); return curPart; }
  function pushCh(title, para) {
    if (!curPart) pushPart('');
    /* опечатка в файле книги: «bÖLÜM 9» — приводим маркер к «BÖLÜM» (как остальные главы) */
    curCh = { title: String(title).replace(/^bÖLÜM/, 'BÖLÜM'), paras: [], part: curPart };
    curPart.chapters.push(curCh);
    return curCh;
  }

  /* Маркер главы отдельной строкой: «ГЛАВА 1», «CHAPTER 3», «ЧАСТЬ I»,
     «7-ci bölmə» — за ним обычно идёт заголовок капсом. */
  const BARE = /^(ГЛАВА|CHAPTER|BÖLMƏ|BÖLÜM|FƏSİL)\s*([IVXLC]+|\d+)\s*$/i;
  const AZNUM = /^\d+\s*[-–]?\s*(ci|cİ|cI|cı|cu|cU|cü|cÜ)\s+[bB][öÖoO][lL][mM][əƏeE](?![A-Za-zА-Яа-яƏəİıÖöÜüÇçŞşĞğ])/i;
  let mergeTitle = false;

  body.forEach((p) => {
    const t = p.text;
    const headOk = !p.tbl;                    /* ячейка таблицы заголовком не бывает */
    const isPart = headOk && (RX.part.test(t) || RX.partAz.test(t)) && t.length < 120 && !RX.modelMark.test(t) &&
      !(fesilIsChapter && /^F[əƏ]sil/i.test(t));
    const isBare = headOk && BARE.test(t);
    const isAzNum = headOk && (AZNUM.test(t) || RX.azChapter.test(t)) && t.length < 160;
    /* глава модели, помеченная как часть: «FƏSİL 12. MÜNASİBƏT MODELİ» */
    const isModelCh = RX.modelChapter.test(t) && RX.modelMark.test(t) && t.length < 200;
    const isCh = headOk && (RX.chapter.test(t) || (fesilIsChapter && /^F[əƏ]sil\s*\d/i.test(t)) || isModelCh || RX.appendixSec.test(t) ||
      RX.intermedia.test(t) || RX.appendix.test(t) || RX.closing.test(t)) && t.length < 200;
    /* вводные разделы — только в начале книги: «ВВЕДЕНИЕ»/«GİRİŞ» посреди текста
       (в таблицах, в приложении) главой не становится */
    const isFront = headOk && RX.front.test(t) && t.length < 60 && !curCh;
    /* разделы, у которых в DOCX нет маркера (задаются в конфиге книги):
       напр. «ШКОЛА МЕТОДОЛОГИИ «ФЕНИКС»», «ПОСЛЕСЛОВИЕ.» */
    const isExtra = EXTRA.some((x) => up(t).startsWith(up(x))) && t.length < 90;
    const isBigHead = p.bold && p.sz >= 32 && t.length < 90 && !/^\d+[.)]/.test(t);

    /* короткий подзаголовок-название сразу после заголовка главы (напр. «LİLİT» / «ЛИЛИТ»)
       дописывается в название главы — проверяется ДО ветки маркеров.
       Дописываем ТОЛЬКО строки-заголовки (жирные, с размером): строки автора
       («Вы – Властелин своей судьбы.», «Дорогой читатель.») остаются в тексте главы. */
    if (curCh && curCh.paras.length === 0 && curCh.title && t.length < 34 && p.bold && p.sz >= 20 &&
        (!curCh.noMerge || (/[A-ZА-ЯƏİÖÜÇŞĞ]/.test(t) && t === t.toUpperCase())) &&
        !/^\d+[.)]/.test(t) && !/^[A-ZА-ЯƏİ]\s*[.)]/.test(t) && !isPart && !isCh && !isBare && !isAzNum && !isFront && !isBigHead) {
      curCh.title = curCh.title.replace(/\s*\.\s*$/, '') + ' · ' + t;
      return;
    }

    /* «LİLİT»/«FENİKS» крупным кеглем сразу после «Bölüm N. MÜNASİBƏT MODELİ» — это
       подзаголовок главы, а не новая глава: дописываем в название, чтобы сохранить
       «Bölüm N» (как в книге; иначе префикс терялся и глава называлась только «FENİKS») */
    if (isBigHead && curCh && curCh.paras.length === 0 && curCh.title && t.length < 34 && RX.modelMark.test(curCh.title)) {
      curCh.title = curCh.title.replace(/\s*\.\s*$/, '') + ' · ' + t;
      return;
    }

    if (isPart) { pushPart(t.replace(/\s+$/, '')); mergeTitle = false; return; }
    /* раздел из конфига (без маркера в DOCX): название уже задано точно,
       к нему дописываем только строку-капс («ПОСЛЕСЛОВИЕ.» + «ОБРАЩЕНИЕ К ПУТЕШЕСТВЕННИКУ») */
    if (isExtra) { pushCh(t, p); mergeTitle = false; curCh.noMerge = true; return; }
    if (isBare || isAzNum || isCh || isFront || isBigHead) {
      pushCh(t, p);
      /* следующая строка-капс станет частью названия: «ГЛАВА N», «1-Cİ FƏSİL»,
         а также вводные («ВВЕДЕНИЕ» + «ПАНДЕМИЯ, О КОТОРОЙ МОЛЧАТ») */
      mergeTitle = isBare || isAzNum || (isFront && t === t.toUpperCase());
      return;
    }
    /* заголовок капсом после голого маркера: «ГЛАВА 1» + «ВИРУС В ГОЛОВЕ…» */
    if (mergeTitle && curCh && curCh.paras.length === 0 && t.length < 130 && !/[.!?]$/.test(t)) {
      curCh.title = curCh.title + '. ' + t;
      mergeTitle = false;
      return;
    }
    mergeTitle = false;

    if (!curCh) pushCh('', p);
    curCh.paras.push(p);
  });

  /* 3) очистка: убрать пустые главы, склеить короткие */
  const flat = [];
  parts.forEach((pt) => {
    pt.chapters.forEach((ch) => {
      const textLen = ch.paras.reduce((n, p) => n + p.text.length, 0);
      if (textLen < 400) { if (flat.length) { flat[flat.length - 1].paras = flat[flat.length - 1].paras.concat(ch.paras); return; } }
      ch.partTitle = pt.title;
      flat.push(ch);
    });
  });
  /* первая глава без названия — служебная шапка файла: если у неё мало текста, убрать */
  if (flat.length > 1 && !String(flat[0].title || '').trim()) {
    const len0 = flat[0].paras.reduce((n, p) => n + p.text.length, 0);
    if (len0 < 1200) flat.shift();
  }
  return flat;
}

function slugify(s, i, lang) {
  let base = s.toLowerCase()
    .replace(/[əıöüçşğ]/g, (c) => ({ 'ə': 'e', 'ı': 'i', 'ö': 'o', 'ü': 'u', 'ç': 'c', 'ş': 's', 'ğ': 'g' }[c] || c))
    .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 42);
  const prefix = lang === 'ru' ? 'glava' : lang === 'en' ? 'chapter' : 'bolum';
  if (!base || base.length < 3 || /^\d+$/.test(base)) base = prefix + '-' + i;
  return String(i).padStart(2, '0') + '-' + base;
}

function shortLabel(title) {
  const t0 = String(title).replace(/[‹›„“”"'‘’]/g, function (c) { return "‹„“'‘’".indexOf(c) !== -1 ? "«" : "»"; });
  const t = t0.trim().replace(/^bÖLÜM/i, 'BÖLÜM');
  const num = (t.match(/^(?:BÖLÜM|Bölüm|ГЛАВА|Глава|CHAPTER|Chapter)\s*([IVXLC]+|\d+)/) || [])[1];
  const name = (t.match(/«([^»]+)»/) || [])[1];
  if (num && name) return (t.slice(0, 2) === 'ГЛ' || t.slice(0, 2) === 'Гл' ? 'Глава ' : 'Bölüm ') + num + ' · «' + name + '»';
  if (num) return (t.slice(0, 2) === 'ГЛ' || t.slice(0, 2) === 'Гл' ? 'Глава ' : 'Bölüm ') + num + ' · ' + t.replace(/^[^.]*\.\s*/, '').slice(0, 34);
  return t.length > 46 ? t.slice(0, 44) + '…' : t;
}

function chapterName(ch) {
  const t = String(ch.title || '').replace(/[‹›„“”"'‘’]/g, function (c) { return "‹„“'‘’".indexOf(c) !== -1 ? "«" : "»"; }).trim();
  /* вводные разделы в боковом меню — только слово-маркер: «ВВЕДЕНИЕ», «GİRİŞ», «ПРОЛОГ» */
  const fr = t.match(/^(GİRİŞ|Giriş|PROLOQ|Proloq|ВВЕДЕНИЕ|Введение|ПРОЛОГ|Пролог)(?![A-Za-zА-Яа-яƏəİıÖöÜüÇçŞşĞğ])/i);
  if (fr) return up(fr[1]);
  let m = t.match(/«([^»]+)»/);
  if (!m) {
    for (let i = 0; i < Math.min(6, (ch.paras || []).length); i++) {
      const p = String((ch.paras[i] || {}).text || '').trim();
      const mm = p.match(/^«([^»]+)»/) || p.match(/^\u00ab([^\u00bb]+)\u00bb/);
      if (mm && p.length < 60) { m = mm; break; }
    }
  }
  if (m) return up(m[1]).trim();
  let name = t
    .replace(/^\s*(BÖLÜM|Bölüm|bÖLÜM|ГЛАВА|Глава|CHAPTER|Chapter|FƏSİL|Fəsil|ÇAP)\s*[IVXLC\d]*[.)]?\s*/i, '')
    .replace(/MÜNASİBƏT MODELİ|МОДЕЛЬ ВЗАИМООТНОШЕНИЙ|MODEL OF RELATIONSHIPS/gi, '')
    .replace(/^[·.\s—–-]+/, '')
    .split(/[·]/)[0]
    .replace(/[«»]/g, "")
    .trim();
  if (!name) name = t.replace(/[«»]/g, "");
  name = up(name);
  if (name.length > 44) name = name.slice(0, 42).replace(/[s—-]+S*$/, "") + "…";
  return name;
}

/* Полное название главы — для оглавления книги: как заголовок на самой
   странице главы (служебные слова убраны, кавычки-ёлочки, капс).
   Короткие имена для бокового меню даёт chapterName(). */
function tocLabel(ch) {
  const t = String(ch.title || '')
    .replace(/[‹›„“”"'‘’]/g, function (c) { return "‹„“'‘’".indexOf(c) !== -1 ? "«" : "»"; })
    .replace(/MÜNASİBƏT MODELİ|МОДЕЛЬ ВЗАИМООТНОШЕНИЙ|MODEL OF RELATIONSHIPS/gi, '')
    .replace(/\s*[.,;]\s*·\s*/g, ' · ')
    .replace(/\s*·\s*·\s*/g, ' · ')
    .replace(/^[\s·.,;—-]+|[\s·.,;—-]+$/g, '')
    .replace(/\s{2,}/g, ' ')
    .trim();
  return up(t);
}

/* названия для оглавления книги: полные, без дублей (повтор → номер главы) */
function tocNames(all) {
  const seen = {};
  return all.map((c) => {
    let n = tocLabel(c) || chapterName(c);
    if (!n) n = 'BÖLMƏ';
    if (seen[n]) n = n + ' (' + c.num + ')';
    seen[n] = 1;
    return n;
  });
}

/* имена без дублей: повтор → берём полный заголовок без номера */
function uniqueNames(all) {
  const seen = {};
  return all.map((c) => {
    let n = chapterName(c);
    if (!n) n = 'BÖLMƏ';
    if (seen[n]) {
      const full = up(String(c.short).replace(/^[^.]*\.\s*/, '').trim());
      n = full && full !== n ? full : n + ' (' + c.num + ')';
    }
    seen[n] = 1;
    return n;
  });
}

function dnName(title) {
  const t = shortLabel(title);
  return t.length > 26 ? t.slice(0, 24).trim() + "…" : t;
}

function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

/* ─────────── генерация страниц ─────────── */
const TPL = JSON.parse(fs.readFileSync(path.join(__dirname, 'book-template.json'), 'utf8'));
/* Единый стандарт читального слоя (Literata 18px / 1.85 / колонка 44rem),
   решение владельца от 29.09.2026. Значения НЕ дублируем — берём из
   _tools/book-template.json, ключ read (единое место для всех книг и языков). */
const READ_CSS = TPL.read.css;

const UI = {
  az: { toc: 'Mündəricat', order: 'Kitabın sifarişi', back: 'Kitablar', prev: 'Əvvəlki', next: 'Növbəti', read: 'Oxu', home: 'Ana səhifə', up: 'Kitab', test: '«Münasibət modellərinin xəritəsi» · 100 sual, 12 model', testBtn: 'Onlayn test' },
  ru: { toc: 'Содержание', order: 'Заказать книгу', back: 'Книги', prev: 'Предыдущая', next: 'Следующая', read: 'Читать', home: 'Главная', up: 'Книга', test: '«Карта моделей взаимоотношений» · 100 утверждений, 12 моделей', testBtn: 'Онлайн-тест' },
  en: { toc: 'Contents', order: 'Order the book', back: 'Books', prev: 'Previous', next: 'Next', read: 'Read', home: 'Home', up: 'Book', test: '“Map of relationship models” · 100 statements, 12 models', testBtn: 'Online test' }
};

function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

/* верхний регистр с учётом азербайджанского: «i» → «İ» (в JS toUpperCase даёт «I» без точки,
   отсюда «FENIKS ERASI» вместо «FENİKS ERASI»); «ı» → «I» — верно и так */
function up(s, code) {
  const t = String(s == null ? '' : s);
  const c = code || global.__LANG;
  return (c === 'az' || c === 'tr') ? t.replace(/i/g, 'İ').toUpperCase() : t.toUpperCase();
}

/* шапка: подмена бренда книги */
function bodyTop(cfg, lang) {
  return TPL.bodyTop
    .replace(/<div class="hdr-logo">[^<]*<\/div>/, '<div class="hdr-logo">' + cfg.logo + '</div>')
    .replace(/<strong>[^<]*<\/strong>/, '<strong>' + esc(up(lang.title)) + '</strong>')
    .replace(/<small>[^<]*<\/small>/, '<small>' + esc(lang.author || cfg.author) + ' · ' + cfg.year + '</small>')
    .replace('data-lang-switch', 'data-lang-switch data-langs="' + cfg.langs.map(function (l) { return l.code; }).join(',') + '"')
    /* «← ragimoff.org» в шапке — ссылка на главную сайта: для русского языка ведём
       на русскую главную, азербайджанскую — на корень (в эталонном каркасе всегда корень) */
    .replace(/<a href="https:\/\/ragimoff\.org"[^>]*class="hdr-back"[^>]*>/,
      '<a href="' + (lang.code === 'az' ? 'https://ragimoff.org/' : 'https://ragimoff.org/' + lang.code + '/') +
      '" class="hdr-back" title="' + (lang.code === 'ru' ? 'Вернуться на главную сайта' : 'Ana sayta qayıt') + '">')
    /* свежая версия переключателя языков (браузер держал старую — с ней на страницах
       книги смена языка вела в 404) */
    .replace('src="/_lang-switch.js"', 'src="/_lang-switch.js?v=4"');
}

/* сайдбар: оглавление книги в классовой структуре эталона */
function sidebarHtml(cfg, lang, all, idx, rel) {
  /* подписи в боковом меню — те же, что в оглавлении: капс, «имя», без служебных слов */
  const names = uniqueNames(all);
  const items = all.map((c, i) =>
    '<div class="nav-item"><a href="' + c.file + '" class="nav-sub-link' + (i === idx ? ' is-active' : '') + '">' +
    '<span class="sub-code">' + c.num + '</span><span class="sub-name">' + esc(names[i]) + '</span></a></div>'
  ).join('\n      ');
  return '<aside class="sidebar" id="sb">\n' +
    '    <div class="sb-hdr"><a class="sb-site" href="https://ragimoff.org/books/" title="Kitablar">← ' + (UI[lang.ui] || UI.az).back + '</a>' +
    '<button class="sb-close" onclick="toggleSb()" aria-label="Bağla">✕</button></div>\n' +
    '    <nav>\n      <div class="nav-item"><a href="index.html" class="nav-link nav-front">' + (UI[lang.ui] || UI.az).home + '</a></div>\n      ' +
    items + '\n    </nav>\n  </aside>';
}

/* хвост: поисковый индекс книги (ALL_PAGES) + текущая страница */
function tailHtml(all, idx) {
  const pages = JSON.stringify(all.map((c) => ({ slug: c.file.replace(/\.html$/, ''), title: c.short, code: c.num })));
  return TPL.tail
    .replace(/const CURRENT = "[^"]*";/, 'const CURRENT = "' + all[idx].file.replace(/\.html$/, '') + '";')
    .replace(/const ALL_PAGES = \[[\s\S]*?\];/, 'const ALL_PAGES = ' + pages + ';');
}

/* метаданные страницы */
/* стиль оглавления книги (запомнен как канон): компактные пункты, узкая колонка номера */
const TOC_STYLE = '<style>' +
  '.home-hero{padding:16px 0 11px}' +
  '.book-toc{margin:8px auto 36px}' +
  '.book-toc .toc-title{margin:0 0 16px 0;padding-bottom:8px}' +
  /* оглавление книги: части, главы, подпункты — без колонки номеров */
  '.book-toc .toc-part{margin:30px 0 12px;padding-bottom:6px;border-bottom:1px solid var(--border);font-weight:700;letter-spacing:.04em;color:var(--gold2)}' +
  '.book-toc .toc-sub{margin:3px 0 3px 26px;font-size:.86rem;color:var(--text2)}' +
  '.book-toc .toc-sub a{color:inherit;text-decoration:none}' +
  '.book-toc .toc-sub a:hover{color:var(--gold2)}' +
  '.book-toc .toc-chapter{margin:14px 0}' +
  /* .content-wrap p из каркаса задаёт свой margin — перебиваем более точным селектором */
  '.content-wrap .toc-test{margin:0 0 34px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}' +
  '.toc-test .test-btn{display:inline-block;background:var(--gold);color:var(--bg);border:none;border-radius:8px;padding:13px 26px;' +
  'font:inherit;font-weight:600;font-size:.95rem;letter-spacing:.01em;text-decoration:none;cursor:pointer;' +
  'transition:background .2s ease,transform .1s ease}' +
  '.toc-test .test-btn:hover{background:#f0c050;transform:translateY(-1px)}' +
  '.toc-test .test-note{color:var(--text2);font-size:.9rem;line-height:1.4}' +
  '@media(max-width:600px){.toc-test{gap:12px}.toc-test .test-btn{padding:12px 20px;width:100%;text-align:center}}' +
  '.d-nav{display:flex;align-items:center;justify-content:space-between;gap:.5rem;margin:2.2rem 0 .5rem;padding:.7rem 0 0;border-top:1px solid var(--border)}' +
  '.d-nav a{color:var(--text);text-decoration:none;padding:.35rem .7rem;border-radius:6px;font-family:var(--mono,monospace);font-weight:700;font-size:.95rem;white-space:nowrap;max-width:42%;overflow:hidden;text-overflow:ellipsis}' +
  '.d-nav a:hover{background:var(--bg3);color:var(--gold)}' +
  '.d-nav .up{color:var(--gold);font-family:var(--font);font-weight:600}' +
  '.d-nav .dn-name{color:var(--text2);font-weight:400;font-family:var(--font);font-size:.85rem}' +
  '@media (max-width:640px){.d-nav .dn-name{display:none}}' +
  '.sidebar .nav-sub-link{padding:7px 14px 7px 18px;font-size:11px;gap:.5rem;line-height:1.4}' +
  '.sidebar .sub-code{flex:0 0 auto;width:auto;white-space:nowrap;margin-right:0;font-size:10px}' +
  '.sidebar .nav-sub-link.is-active{color:var(--gold);border-left-color:var(--gold);background:var(--gold-bg)}' +
  READ_CSS +
  '</style>';

function headHtml(cfg, lang, title, desc) {
  const LANGS_ATTR = cfg.langs.map(function (l) { return l.code; }).join(',');
  /* адреса языковых версий книги для переключателя: слаги глав в языках разные,
     поэтому переключатель ведёт на главную книги нужного языка */
  const LANG_URLS = cfg.langs.map(function (l) {
    return ' data-lang-url-' + l.code + '="/' + cfg.out + (l.dir ? '/' + l.dir : '') + '/"';
  }).join('');
  return TPL.head
    .replace('<html ', '<html data-langs="' + LANGS_ATTR + '"' + LANG_URLS + ' ')
    .replace(/<html([^>]*?)lang="[a-z]{2}"/, '<html$1lang="' + lang.code + '"')
    .replace(/<title>[\s\S]*?<\/title>/, '<title>' + esc(title) + ' | ' + esc(up(lang.title)) + '</title>')
    .replace(/<meta name="description" content="[^"]*"/, '<meta name="description" content="' + esc(desc) + '"')
    .replace(/<meta property="og:title" content="[^"]*"/, '<meta property="og:title" content="' + esc(title) + '"')
    .replace(/<meta property="og:description" content="[^"]*"/, '<meta property="og:description" content="' + esc(desc) + '"')
    .replace(/<meta property="og:url" content="[^"]*"/, '<meta property="og:url" content="https://ragimoff.org/' + cfg.slug + '/"')
    .replace(/"name":"[^"]*","inLanguage":"[^"]*"/, '"name":"' + esc(cfg.title) + '","inLanguage":"' + lang.code + '"')
    .replace(/"about":"[^"]*"/, '"about":"' + esc(lang.subtitle || cfg.subtitle || cfg.title) + '"')
    .replace('</head>', TOC_STYLE + '</head>');
}

function chapterPage(cfg, lang, ch, idx, all, rel) {
  const ui = UI[lang.ui] || UI.az;
  const prev = idx > 0 ? all[idx - 1] : null;
  const next = idx < all.length - 1 ? all[idx + 1] : null;
  const body = ch.paras.map((p) => {
    const t = esc(p.text);
    if (p.text.length < 95 && /^\d+(\.\d+)*[.)]?\s/.test(p.text)) return '<h2>' + t + '</h2>';
    if (p.bold && p.sz >= 26 && p.text.length < 95) return '<h2>' + t + '</h2>';
    if (p.bold && p.text.length < 90 && /[:.]$/.test(p.text)) return '<h3>' + t + '</h3>';
    return '<p>' + t + '</p>';
  }).join('\n');

  return headHtml(cfg, lang, ch.short, lang.title + ' — ' + ch.short) +
    '\n</head>\n' + bodyTop(cfg, lang) + sidebarHtml(cfg, lang, all, idx, rel) + TPL.mid + TPL.contentOpen +
    '\n<nav class="crumb"><a href="index.html">‹ ' + esc(lang.title) + '</a></nav>' +
    '<header class="chap-head"><h1 class="chap-h1"><span class="chap-range">' + ch.num + '</span>' +
    '<span class="chap-title">' + esc(ch.short) + '</span></h1></header>\n' +
    body +
    /* нижняя навигация — как в эталоне: одна строка (.d-nav): ← NN имя · ↑ вверх · имя NN → */
    '\n<nav class="d-nav">' +
    (prev
      ? '<a href="' + prev.file + '">← ' + prev.num + ' <span class="dn-name">' + esc(dnName(prev.short)) + '</span></a>'
      : '<span></span>') +
    '<a class="up" href="index.html">↑ ' + (ui.up || 'Fəsil') + '</a>' +
    (next
      ? '<a href="' + next.file + '"><span class="dn-name">' + esc(dnName(next.short)) + '</span> ' + next.num + ' →</a>'
      : '<span></span>') +
    '</nav>\n' + tailHtml(all, idx);
}

/* ── оглавление книги: части, главы и подпункты — как в книге, без номеров страниц ── */
function tocStructure(paras, all) {
  const titles = tocTitles(paras || []);
  if (titles.length < 3) return null;
  const PART = /^(Сезон|Fəsil|FƏSİL|ЧАСТЬ|HİSSƏ|PART\s+[IVXLC]+(?![A-Za-z])|Школа|Şkola|Psixologiya Məktəbi|«Feniks»\s*Psixologiya)/i;
  const CHAP = /^(Глава|Chapter|CHAPTER|Bölüm|Bölmə|Раздел|Введение|Giriş|Пролог|Proloq|Послесловие|Sonluq|Список литературы|Ədəbiyyat|Интермедия|Interlude|First Interlude|Second Interlude|Third Interlude|Fourth Interlude|BİRİNCİ|İKİNCİ|ÜÇÜNCÜ|DÖRDÜNCÜ|Приложение|Appendix|Əlavə|Заключительное|Closing|Section|Part\s*\d|От автора|Müəllifdən|From the Author|Интермеццо|İntermezzo|Intermezzo|Интерлюдия|İnterlüdiya|ara səhnə|Fəsil\s*\d|\d+\s*[-–]?\s*(ci|cİ|cI|cı|cu|cU|cü|cÜ)\s+[fF][əƏeE][sS][iİıI][lL]|\d+\s*[-–]?\s*(ci|cİ|cI|cı|cu|cU|cü|cÜ)\s+[bB][öÖoO][lL][mM][əƏeE])/i;
  /* маркер+номер («Глава 3» / «Bölüm 3»): не даём одноимённым разделам
     (модель «Феникс», школа «Феникс») перепутать страницы */
  const mn = (s) => {
    let m = String(s).match(/^(BÖLÜM|Bölüm|Bölmə|ГЛАВА|Глава|Раздел|CHAPTER|Chapter|Section|Part|FƏSİL|Fəsil)\s*([IVXLC]+|\d+)/i);
    if (!m) { const a = String(s).match(/^(\d+)\s*[-–]?\s*(?:ci|cı|cu|cü)\s+(fəsil|bölmə)/i); if (a) m = [a[0], a[2], a[1]]; }
    if (!m) return '';
    const fam = /^(BÖLÜM|Bölüm|Bölmə)/i.test(m[1]) ? 'b' : /^Раздел/i.test(m[1]) ? 'r' : /^(ГЛАВА|Глава)/i.test(m[1]) ? 'g' : 'c';
    return fam + m[2].toLowerCase();
  };
  /* ключ сопоставления с главой книги: имя модели в «…», иначе начало названия.
     ВАЖНО: «İ».toLowerCase() в JS даёт «i̇» (i + точка) — приводим буквы заранее. */
  const words = (s) => {
    const q = String(s).match(/«([^»]+)»/);
    return (q ? q[1] : String(s))
      .replace(/İ/g, 'i').replace(/I/g, 'i').replace(/Ə/g, 'ə').replace(/Ğ/g, 'ğ')
      .replace(/Ş/g, 'ş').replace(/Ç/g, 'ç').replace(/Ö/g, 'ö').replace(/Ü/g, 'ü')
      .toLowerCase()
      .replace(/[«»"'`.,:;!?()\[\]–—-]/g, ' ').replace(/\s+/g, ' ').trim().split(' ');
  };
  const pages = all.map((c) => {
    const w = words(c.title || '');
    return { c, k2: w.slice(0, 2).join(' '), k1: w[0], klast: w[w.length - 1] || '', mn: mn(c.title || '') };
  });
  const used = {};
  const items = [];
  let last = null;
  /* раздел с маркером получает страницу только при совместимом маркере;
     страница без маркера — лишь если такие разделы в книге вообще есть
     (иначе «Раздел 3» из русского файла забрал бы чужую страницу) */
  const famPresent = (fam) => pages.some((q) => q.mn && q.mn[0] === fam);
  titles.forEach((t) => {
    const w = words(t);
    const k2 = w.slice(0, 2).join(' ');
    const k1 = w[0];
    const my = mn(t);
    const compat = (p) => !my || p.mn === my || (!p.mn && famPresent(my[0]));
    const hit = CHAP.test(t)
      ? (pages.find((p) => !used[p.c.file] && compat(p) && p.k2 === k2) ||
         pages.find((p) => !used[p.c.file] && compat(p) && p.k1 === k1) ||
         (my ? pages.find((p) => !used[p.c.file] && p.mn === my) : null) ||
         /* последнее слово названия: «Sonluq. Oxucuya müraciət» → «SON SÖZ · SƏYAHƏTÇİYƏ MÜRACİƏT» */
         (w.length > 1 && w[w.length - 1].length > 4
           ? pages.find((p) => !used[p.c.file] && compat(p) && p.klast === w[w.length - 1])
           : null))
      : null;
    if (PART.test(t) && !CHAP.test(t)) { items.push({ type: 'part', text: t }); last = null; return; }
    if (hit) { used[hit.c.file] = 1; last = hit.c; items.push({ type: 'chapter', text: t, file: hit.c.file }); return; }
    if (CHAP.test(t)) { items.push({ type: 'chapter', text: t, file: '' }); last = null; return; }
    items.push({ type: 'sub', text: t, file: last ? last.file : '' });
  });
  return items;
}

function tocHtml(items) {
  return items.map((it) => {
    if (it.type === 'part') return '<div class="toc-part">' + esc(it.text) + '</div>';
    if (it.type === 'sub') {
      return '<div class="toc-sub">' + (it.file ? '<a href="' + it.file + '">' + esc(it.text) + '</a>' : esc(it.text)) + '</div>';
    }
    return '<div class="toc-chapter">' + (it.file
      ? '<a href="' + it.file + '" class="toc-chapter-title"><span class="toc-name">' + esc(it.text) + '</span></a>'
      : '<span class="toc-chapter-title"><span class="toc-name">' + esc(it.text) + '</span></span>') + '</div>';
  }).join('\n      ');
}

function indexPage(cfg, lang, all, rel, paras) {
  const ui = UI[lang.ui] || UI.az;
  /* оглавление — из книжного (части, главы, подпункты); запасной путь — список глав */
  const structure = tocStructure(paras, all);
  const cards = structure ? tocHtml(structure) : tocHtml(all.map((c) => ({ type: 'chapter', text: tocLabel(c), file: c.file })));
  const content =
    '\n<div class="home-hero"><h1 class="home-title">' + esc(up(lang.title)) + '</h1>' +
    '<p class="sub">' + esc(lang.subtitle || cfg.subtitle || '') + '</p></div>\n' +
    /* ссылка на онлайн-тест книги (cfg.testUrl) — над оглавлением */
    (cfg.testUrl && cfg.testUrl[lang.code]
      ? '<div class="toc-test"><a class="test-btn" href="' + cfg.testUrl[lang.code] + '">' + esc((UI[lang.ui] || UI.az).testBtn) + '</a><span class="test-note">' + esc((UI[lang.ui] || UI.az).test) + '</span></div>\n'
      : '') +
    '<section class="book-toc"><h2 class="toc-title">' + esc(up((UI[lang.ui] || UI.az).toc)) + '</h2>\n      ' + cards + '\n    </section>\n';
  return headHtml(cfg, lang, lang.title, lang.title + ' — ' + (cfg.subtitle || '')) +
    '\n</head>\n' + bodyTop(cfg, lang) + sidebarHtml(cfg, lang, all, -1, rel) + TPL.mid + TPL.contentOpen +
    content + '\n' + tailHtml(all, 0);
}

/* ─────────── main ─────────── */
const cfgPath = process.argv[2];
const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
const outRoot = path.resolve(cfg.out);
fs.mkdirSync(outRoot, { recursive: true });

/* style.css — копия из эталонной книги */
if (cfg.styleFrom && fs.existsSync(cfg.styleFrom)) {
  fs.copyFileSync(cfg.styleFrom, path.join(outRoot, 'style.css'));
}

let totalPages = 0;
cfg.langs.forEach((lang) => {
  const dir = path.join(outRoot, lang.dir || '');
  fs.mkdirSync(dir, { recursive: true });
  if (cfg.styleFrom && fs.existsSync(cfg.styleFrom)) fs.copyFileSync(cfg.styleFrom, path.join(dir, 'style.css'));
  global.__USE_TOC = !!cfg.useToc;
  global.__LANG = lang.code;
  global.__EXTRA = (cfg.extraChapters && cfg.extraChapters[lang.code]) || [];
  const paras = paragraphs(lang.file);
  const chapters = buildChapters(paras);
  const used = {};
  const all = chapters.map((ch, i) => {
    const short = (ch.title || '').replace(/\s*\.\s*$/, '').slice(0, 120) || ('Bölmə ' + (i + 1));
    let file = slugify(short, i + 1, lang.code) + '.html';
    while (used[file]) file = file.replace(/\.html$/, '-x.html');
    used[file] = 1;
    return { short, num: String(i + 1).padStart(2, '0'), file, paras: ch.paras, partTitle: ch.partTitle, title: ch.title };
  });
  const rel = lang.dir ? '../' : '';
  all.forEach((ch, i) => {
    fs.writeFileSync(path.join(dir, ch.file), chapterPage(cfg, lang, ch, i, all, rel), 'utf8');
    totalPages++;
  });
  fs.writeFileSync(path.join(dir, 'index.html'), indexPage(cfg, lang, all, rel, paras), 'utf8');
  totalPages++;
  console.log(`${lang.code}: глав ${all.length} → ${path.relative(process.cwd(), dir) || '.'}`);
  all.slice(0, 6).forEach((c) => console.log('   · ' + c.file + '  ' + c.short.slice(0, 60)));
});

console.log('всего страниц:', totalPages);
