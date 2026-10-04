/* =====================================================================
   _tools/freud-az-book.js — азербайджанские web-книги Фрейда.
   Структура глав берётся НЕ эвристикой, а из печатных PDF
   (D:/Документы/ZFreud/_structures.txt, эталон владельца): заголовок
   главы ищется в тексте EPUB по точному совпадению с напечатанной
   строкой. Найдены все главы — книга собирается; не найдена хотя бы
   одна — сборка падает с ошибкой (молча мусор не публикуем).

   Каркас страниц — тот же, что у книг из _tools/epub-to-book.js
   (book-template.json, TOC_STYLE, сайдбар, d-nav, data-lang-url-*).

   Запуск: node _tools/freud-az-book.js [slug]
   ===================================================================== */
const fs = require('fs');
const path = require('path');
const os = require('os');
const { execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const SRC = 'D:/Документы/ZFreud/azerbaycan_freud/books';
const TPL = JSON.parse(fs.readFileSync(path.join(__dirname, 'book-template.json'), 'utf8'));
/* Единый стандарт читального слоя (Literata 18px / 1.85 / колонка 44rem),
   решение владельца от 29.09.2026. Значения НЕ дублируем — берём из
   _tools/book-template.json, ключ read (единое место для всех книг и языков). */
const READ_CSS = TPL.read.css;
const LSV = 6;                                    /* версия _lang-switch.js (?v=) */

const UI = { back: 'Kitablar', home: 'Ana səhifə', up: 'Kitab', toc: 'MÜNDƏRİCAT' };

function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
function up(s) { return String(s).replace(/i/g, 'İ').toUpperCase(); }

/* ── ключ для поиска заголовка: регистр и диакритика не важны ── */
const FOLD = { 'İ': 'i', 'I': 'i', 'ı': 'i', 'i': 'i', 'Ə': 'e', 'ə': 'e', 'Ö': 'o', 'ö': 'o', 'Ü': 'u', 'ü': 'u',
  'Ç': 'c', 'ç': 'c', 'Ş': 's', 'ş': 's', 'Ğ': 'g', 'ğ': 'g', 'Q': 'q', 'q': 'q', 'X': 'x', 'x': 'x' };
function key(s) {
  return String(s).replace(/[İIıiƏəÖöÜüÇçŞşĞğ]/g, (c) => FOLD[c] || c)
    .toLowerCase()
    .replace(/[’'«»"'`.,:;!?()\[\]{}—–\-]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

/* то же, но посимвольно (1:1) — по свёрнутой строке находим место в исходном тексте */
function foldKeep(s) {
  return String(s).replace(/[İIıiƏəÖöÜüÇçŞşĞğ]/g, (c) => FOLD[c] || c).toLowerCase();
}

/* ── издательский/служебный мусор: в книгу не идёт ──
   список владельца (проверяется скриптом _tools/check-freud-book.js по всем страницам) */
const JUNK = [
  /* конвертеры и водяные знаки */
  /^Converted Ebook$/i, /^Telegram\b/i, /kitabbul/i, /^Cover$/i,
  /* выходные данные, ISBN, права, издательство */
  /^ISBN\b/i, /^İSBN\b/i, /^©/, /^\(c\)/i, /^Qanun Nəşriyyatı\b/i, /Nəşriyyatı[, ]/i,
  /^Bakı\b/i, /^Tel(efon)?[:.]/i, /^Mobil[:.]/i, /^e-?mail\b/i, /^www\./i, /^https?:\/\//i,
  /^info@|@qanun|@kitabbul|@\w+\.(az|com|ru)$/i,
  /facebook\.com|instagram\.com|fb\.com|t\.me\//i,
  /^Çapa imzalanmışdır/i, /^Çapa\b/i, /^Sifariş/i, /^Tiraj/i, /^Kağız/i,
  /müəlliflik hüququ/i, /hüquqları .*məxsusdur/i, /hissə-hissə nəşri/i, /ziddir\.?$/i,
  /* редакторы и переводчики */
  /^Redaktor/i, /^Korrektor/i, /^Tərcümə\b/i, /^Tercümə\b/i, /^Rus dilindən tərcümə/i,
  /^Tərtib(çi)?\b/i, /^Ön sözü yazan/i, /^Buraxılışa/i, /^Nəşrə hazırlayan/i,
  /* оглавление печатного издания и английские/немецкие титулы */
  /^MÜNDƏRİCAT$/i, /^Mündəricat$/i, /^İçindəkilər$/i,
  /^Sigmund Freud\b/i, /^Ziqmund Freyd$/i, /^Moses and Monotheism$/i, /^Die Brautbriefe/i,
  /^Introduction to Psychoanalysis$/i, /^SIgmund Freud DIe Traumdeutung$/i,
  /^Annotasiya$/i, /^Annotation$/i,
];
/* колонтитул = название книги, повторённое в тексте */
const runHead = (t, bookTitle) => key(t) === key(bookTitle) || key(t) === key('Sigmund Freud ' + bookTitle);
/* примечания переводчика/издателя: концевой блок абзацев «1 …», «12 …» — не текст Фрейда */
const NOTE_TAIL = /^\d{1,3}\s+\S/;

function parasOf(file) {
  const tmp = path.join(os.tmpdir(), 'freud-az-' + Date.now() + '.epub');
  fs.copyFileSync(file, tmp);                     /* unzip не понимает не-ASCII пути */
  const list = execFileSync('unzip', ['-Z1', tmp], { maxBuffer: 64 * 1024 * 1024 }).toString('utf8')
    .split('\n').map((x) => x.trim()).filter((x) => /\.x?html?$/i.test(x)).sort();
  const out = [];
  list.forEach((f) => {
    const raw = execFileSync('unzip', ['-p', tmp, f], { maxBuffer: 256 * 1024 * 1024 }).toString('utf8');
    const clean = raw.replace(/<(script|style)[\s\S]*?<\/\1>/gi, ' ')
      .replace(/<\/(p|div|h[1-6]|li|tr)>/gi, '\n').replace(/<br\s*\/?>/gi, '\n')
      .replace(/<[^>]+>/g, ' ');
    clean.split('\n').forEach((x) => {
      const t = x.replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#(\d+);/g, (m, d) => String.fromCharCode(+d))
        .replace(/\s+/g, ' ').trim();
      if (t) out.push(t);
    });
  });
  return out;
}

/* ── склейка разорванных строк (в EPUB текст разбит по строкам PDF) ── */
const LOW = /^[a-zəıöüçşğ«„(]/;
const ENDS_SENT = /[.!?…»)"'’”]$/;
function joinBroken(paras) {
  const out = [];
  paras.forEach((p) => {
    const prev = out[out.length - 1];
    if (prev && !prev.head && p.length > 1) {
      const pHyphen = /[a-zəıöüçşğ]-$/i.test(prev.t) && LOW.test(p);
      if (pHyphen) { prev.t = prev.t.replace(/-$/, '') + p; return; }
      if (!ENDS_SENT.test(prev.t) && !/\d$/.test(prev.t) && LOW.test(p) && !/^[•*•\-–—]/.test(p)) {
        prev.t += ' ' + p; return;
      }
    }
    out.push({ t: p, head: false });
  });
  return out;
}

/* ── книги: главы = напечатанные заголовки (эталон _structures.txt) ── */
const BOOKS = [
  {
    slug: 'freud-musa', logo: 'MT', epub: 'Musa və təkallahlılıq.epub',
    title: 'Musa və təkallahlıq', titlePrinted: 'MUSA VƏ TƏKALLAHLIQ',
    author: 'Ziqmund Freyd', year: '1939', yearSub: 'İlk nəşr — 1939', ru: true, prefix: 'musa',
    chapters: [
      { title: 'I. MUSA MİSİRLİDİR', short: 'I. MUSA MİSİRLİDİR', find: ['I', 'MUSA MİSİRLİDİR'], pdfPage: 7 },
      { title: 'II. ƏGƏR MUSA MİSİRLİ OLMUŞSA', short: 'II. ƏGƏR MUSA MİSİRLİ…', find: ['II', 'ƏGƏR MUSA MİSİRLİ OLMUŞSA'], pdfPage: 13 },
      { title: 'III. MUSA, ONUN XALQI VƏ TƏKALLAHLI DİN. BİRİNCİ BÖLMƏ', short: 'III. … BİRİNCİ BÖLMƏ', find: ['III', 'MUSA, ONUN XALQI VƏ TƏKALLAHLI DİN', 'BİRİNCİ BÖLMƏ'], pdfPage: 40 },
      { title: 'III. MUSA, ONUN XALQI VƏ TƏKALLAHLI DİN. İKİNCİ BÖLMƏ', short: 'III. … İKİNCİ BÖLMƏ', find: ['İKİNCİ BÖLMƏ'], pdfPage: 76 },
    ],
  },
  {
    slug: 'freud-yuxularin-yozumu', logo: 'ZY', epub: 'Yuxuların yozumu.epub',
    title: 'Yuxuların yozumu', titlePrinted: 'YUXULARIN YOZUMU',
    author: 'Ziqmund Freyd', year: '1900', yearSub: 'İlk nəşr — 1900', ru: true, prefix: 'yuxular',
    chapters: [
      { title: 'Giriş', find: ['Giriş'], pdfPage: 7 },
      { title: 'Üçüncü nəşrə ön söz', find: ['Üçüncü nəşrə ön söz'], pdfPage: 9 },
      { title: 'Dördüncü nəşrə ön söz', find: ['Dördüncü nəşrə ön söz'], pdfPage: 10 },
      { title: 'Beşinci nəşrə ön söz', find: ['Beşinci nəşrə ön söz'], pdfPage: 10 },
      { title: 'Altıncı nəşrə ön söz', find: ['Altıncı nəşrə ön söz'], pdfPage: 11 },
      { title: 'I. Yuxugörmə məsələlərinə dair elmi ədəbiyyat (1900-cü ilədək)', find: ['I. Yuxugörmə məsələlərinə dair elmi ədəbiyyat (1900-cü ilədək)'], pdfPage: 12 },
      { title: 'II. Yuxuların yozulma üsulu. Yuxuların təhlili örnəyi', find: ['II. Yuxuların yozulma üsulu. Yuxuların təhlili örnəyi'], pdfPage: 67 },
      { title: 'III. Yuxugörmə – arzuların gerçəkləşməsidir', find: ['III. Yuxugörmə – arzuların gerçəkləşməsidir'], pdfPage: 83 },
      { title: 'IV. Yuxuların təhrifedici fəaliyyəti', find: ['IV. Yuxuların təhrifedici fəaliyyəti'], pdfPage: 90 },
      { title: 'V. Yuxuların material və mənbələri', find: ['V. Yuxuların material və mənbələri'], pdfPage: 107 },
      { title: 'VI. Yuxugörmənin işi', find: ['VI. Yuxugörmənin işi'], pdfPage: 185 },
      { title: 'VII. Yuxugörmə proseslərinin psixologiyası', find: ['VII. Yuxugörmə proseslərinin psixologiyası'], pdfPage: 271 },
      { title: 'Ədəbiyyat göstəricisi', find: ['Ədəbiyyat göstəricisi'], pdfPage: 328 },
    ],
  },
  {
    slug: 'freud-seksualligin-psixologiyasi', logo: 'SP', epub: 'Seksuallığın psixologiyası.epub',
    title: 'Seksuallığın psixologiyası', titlePrinted: 'SEKSUALLIĞIN PSİXOLOGİYASI',
    author: 'Ziqmund Freyd', year: '1905', yearSub: 'İlk nəşr — 1905', ru: true, prefix: 'seksualliq',
    chapters: [
      { title: 'Müəllifin 3-cü nəşrə ön sözü', find: ['Müəllifin 3-cü nəşrə ön sözü'], pdfPage: 2 },
      { title: 'Müəllifin 4-cü nəşrə ön sözü', find: ['Müəllifin 4-cü nəşrə ön sözü'], pdfPage: 3 },
      { title: 'I. Seksual sapmalar', find: ['1. Seksual sapmalar'], pdfPage: 5 },
      { title: 'II. İnfantil seksuallıq', find: ['11. İnfantil seksuallıq'], pdfPage: 30 },
      { title: 'III. Cinsi yetkinləşmə dövründəki ciddi dəyişikliklər', find: ['III. Cinsi yetkinləşmə dövründəki ciddi dəyişikliklər'], pdfPage: 54 },
      { title: 'Uşaq cinsiyyət orqanının təşəkkülü (seksuallıq nəzəriyyəsinə əlavələr)', find: ['Uşaq cinsiyyət orqanının təşəkkülü', '(seksuallıq nəzəriyyəsinə əlavələr)'], pdfPage: 80 },
      { title: 'Narsisizm haqqında', find: ['Narsisizm9 haqqında'], pdfPage: 99 },
      { title: 'Kişilərin xüsusi tipli “obyekt seçimi” haqqında', find: ['Kişilərin xüsusi tipli “obyekt seçimi” haqqında'], pdfPage: 133 },
      { title: 'Seksual həyatda baş verən alçaldılmalar haqqında', find: ['Seksual həyatda baş verən alçaldılmalar haqqında'], pdfPage: 133 },
      { title: 'Bakirəlik tabusu', find: ['Bakirəlik tabusu'], pdfPage: 144 },
    ],
  },
  {
    slug: 'freud-psixoanalizle-tanishliq', logo: 'PT', epub: 'Psixoanalizlə ilkin tanışlıq.epub',
    title: 'Psixoanalizlə ilkin tanışlıq', titlePrinted: 'PSİXOANALİZLƏ İLKİN TANIŞLIQ',
    author: 'Ziqmund Freyd', year: '1917', yearSub: 'İlk nəşr — 1917', ru: true, prefix: 'psixoanaliz',
    chapters: [
      { title: 'Ön söz', find: ['Ön söz'], pdfPage: 3 },
      { title: 'Birinci mühazirə. GİRİŞ', find: ['Birinci mühazirə', 'GİRİŞ'], pdfPage: 4 },
      { title: 'İkinci mühazirə. YANILMALAR', find: ['İkinci mühazirə', 'YANILMALAR'], pdfPage: 15 },
      { title: 'Üçüncü mühazirə. YANILMALAR (ardı)', find: ['Üçüncü mühazirə', 'YANILMALAR', '(ardı)'], pdfPage: 21 },
      { title: 'Dördüncü mühazirə. YANILMALAR (sonu)', find: ['Dördüncü mühazirə', 'YANILMALAR', '(sonu)'], pdfPage: 35 },
      { title: 'Beşinci mühazirə. QARŞIYA ÇIXAN ANLAŞILMAZLIQLAR VƏ ONLARI ADLAMAQ ÜÇÜN İLKİN ÇALIŞMALAR', short: 'Beşinci mühazirə. QARŞIYA ÇIXAN ANLAŞILMAZLIQLAR…', find: ['Beşinci mühazirə', 'QARŞIYA ÇIXAN ANLAŞILMAZLIQLAR VƏ ONLARI ADLAMAQ ÜÇÜN', 'İLKİN ÇALIŞMALAR'], pdfPage: 49 },
      { title: 'Altıncı mühazirə. FƏRZİYYƏLƏR VƏ YOZUM TEXNİKALARI', find: ['Altıncı mühazirə', 'FƏRZİYYƏLƏR VƏ YOZUM TEXNİKALARI'], pdfPage: 61 },
      { title: 'Yeddinci mühazirə. YUXUGÖRMƏNİN AÇIQ MƏZMUNU VƏ ONUN GİZLİN ANLAMLARI', find: ['Yeddinci mühazirə', 'YUXUGÖRMƏNİN AÇIQ MƏZMUNU VƏ ONUN GİZLİN ANLAMLARI'], pdfPage: 71 },
      { title: 'Səkkizinci mühazirə. UŞAQLARIN YUXUGÖRMƏLƏRİ', find: ['Səkkizinci mühazirə', 'UŞAQLARIN YUXUGÖRMƏLƏRİ'], pdfPage: 80 },
      { title: 'Doqquzuncu mühazirə. YUXUGÖRMƏNİN SENZURASI', find: ['Doqquzuncu mühazirə', 'YUXUGÖRMƏNİN SENZURASI'], pdfPage: 87 },
      { title: 'Onuncu mühazirə. YUXUGÖRMƏNİN SİMVOLLARI', find: ['Onuncu mühazirə', 'YUXUGÖRMƏNİN SİMVOLLARI'], pdfPage: 96 },
      { title: 'On birinci mühazirə. YUXUGÖRMƏNİN İŞİ', find: ['On birinci mühazirə', 'YUXUGÖRMƏNİN İŞİ'], pdfPage: 110 },
      { title: 'On ikinci mühazirə. BİR SIRA YUXUGÖRMƏLƏRİN ANALİZİ', find: ['On ikinci mühazirə', 'BİR SIRA YUXUGÖRMƏLƏRİN ANALİZİ'], pdfPage: 120 },
      { title: 'On üçüncü mühazirə. YUXUGÖRMƏDƏ ÖZÜNÜ GÖSTƏRƏN ƏSKİLƏŞMƏK (KÖHNƏLƏŞMƏK) VƏ KÖRPƏLƏŞMƏK ÖZƏLLİKLƏRİ', short: 'On üçüncü mühazirə. ƏSKİLƏŞMƏK VƏ KÖRPƏLƏŞMƏK…', find: ['On üçüncü mühazirə', 'YUXUGÖRMƏDƏ ÖZÜNÜ GÖSTƏRƏN ƏSKİLƏŞMƏK (KÖHNƏLƏŞMƏK)', 'VƏ KÖRPƏLƏŞMƏK ÖZƏLLİKLƏRİ'], pdfPage: 131 },
      { title: 'On dördüncü mühazirə. İSTƏKLƏRİN GERÇƏKLƏŞMƏSİ', find: ['On dördüncü mühazirə', 'İSTƏKLƏRİN GERÇƏKLƏŞMƏSİ'], pdfPage: 141 },
      { title: 'On beşinci mühazirə. ŞÜBHƏLƏR VƏ TƏNQİDLƏR', find: ['On beşinci mühazirə', 'ŞÜBHƏLƏR VƏ TƏNQİDLƏR'], pdfPage: 152 },
      { title: 'On altıncı mühazirə. PSİXOANALİZ VƏ PSİXİATRİYA', find: ['On altıncı mühazirə', 'PSİXOANALİZ VƏ PSİXİATRİYA'], pdfPage: 160 },
      { title: 'On yeddinci mühazirə. SİMPTOMLARIN MƏNASI', find: ['On yeddinci mühazirə', 'SİMPTOMLARIN MƏNASI'], pdfPage: 170 },
      { title: 'On səkkizinci mühazirə. TRAVMAYA FİKSASİYA, ŞÜURSUZ', find: ['On səkkizinci mühazirə', 'TRAVMAYA FİKSASİYA, ŞÜURSUZ'], pdfPage: 180 },
      { title: 'On doqquzuncu mühazirə. MÜQAVİMƏT VƏ SIXIŞDIRMA', find: ['On doqquzuncu mühazirə', 'MÜQAVİMƏT VƏ SIXIŞDIRMA'], pdfPage: 190 },
      { title: 'İyirminci mühazirə. İNSANIN CİNSİ HƏYATI', find: ['İyirminci mühazirə', 'İNSANIN CİNSİ HƏYATI'], pdfPage: 200 },
      { title: 'İyirmi birinci mühazirə. LİBİDONUN İNKİŞAFI VƏ CİNSİ TƏŞKİLATLANMA', find: ['İyirmi birinci mühazirə', 'LİBİDONUN İNKİŞAFI VƏ CİNSİ TƏŞKİLATLANMA'], pdfPage: 210 },
      { title: 'İyirmi ikinci mühazirə. İNKİŞAF VƏ REQRESSİYA TƏSƏVVÜRÜ. ETİOLOGİYA', find: ['İyirmi ikinci mühazirə', 'İNKİŞAF VƏ REQRESSİYA TƏSƏVVÜRÜ. ETİOLOGİYA'], pdfPage: 220 },
      { title: 'İyirmi üçüncü mühazirə. SİMPTOM YARANMA YOLLARI', find: ['İyirmi üçüncü mühazirə', 'SİMPTOM YARANMA YOLLARI'], pdfPage: 230 },
      { title: 'İyirmi dördüncü mühazirə. ADİ NERVOZLULUQ', find: ['İyirmi dördüncü mühazirə', 'ADİ NERVOZLULUQ'], pdfPage: 240 },
      { title: 'İyirmi beşinci mühazirə. QORXU', find: ['İyirmi beşinci mühazirə', 'QORXU'], pdfPage: 250 },
      { title: 'İyirmi altıncı mühazirə. LİBİDO NƏZƏRİYYƏSİ VƏ NARSİSİZM', find: ['İyirmi altıncı mühazirə', 'LİBİDO NƏZƏRİYYƏSİ VƏ NARSİSİZM'], pdfPage: 260 },
      { title: 'İyirmi yeddinci mühazirə. KÖÇÜRMƏ (TRANSFER)', find: ['İyirmi yeddinci mühazirə', 'KÖÇÜRMƏ (TRANSFER)'], pdfPage: 270 },
      { title: 'İyirmi səkkizinci mühazirə. ANALİTİK TERAPİYA', find: ['İyirmi səkkizinci mühazirə', 'ANALİTİK TERAPİYA'], pdfPage: 280 },
    ],
  },
];

/* Sevgi məktubları: главы — письма, заголовок = напечатанная строка даты */
const LETTERS = [
  ['Ön söz', 'Ön söz', 0],
  ['Vyana, 10 iyun 1882', 'Vyana, 10 iyun 1882', 1],
  ['Vyana, 27 iyun 1882', 'Vyana, 27 iyun 1882', 2],
  ['Hamburq, 23 iyul 1882', 'Hamburq, 23 iyul 1882', 3],
  ['Vyana, 18 avqust 1882', 'Vyana, 18 avqust 1882', 4],
  ['Vyana, 25 sentyabr 1882', 'Vyana, 25 sentyabr 1882', 5],
  ['Vyana, 5 oktyabr 1882', 'Vyana, 5 oktyabr 1882', 6],
  ['Vyana, 13 iyul 1883', 'Vyana, 13 iyul 1883', 7],
  ['Vyana, 29 avqust 1883', 'Vyana, 29 avqust 1883', 8],
  ['Vyana, 9 sentyabr 1883', 'Vyana, 9 sentyabr 1883', 9],
  ['Vyana, 16 sentyabr 1883', 'Vyana, 16 sentyabr 1883', 10],
  ['Vyana, 9 oktyabr 1883', 'Vyana, 9 oktyabr 1883', 11],
  ['Vyana, 23 oktyabr 1883', 'Vyana, 23 oktyabr 1883', 12],
  ['Vyana, 15 noyabr 1883', 'Vyana, 15 noyabr 1883', 13],
  ['Vyana, 10 yanvar 1884', 'Vyana, 10 yanvar 1884', 14],
  ['Vyana, 7 fevral 1884', 'Vyana, 7 fevral 1884', 15],
  ['Vyana, 20 mart 1884', 'Vyana, 20 mart 1884', 16],
  ['Vyana, 19 iyun 1884', 'Vyana, 19 iyun 1884', 17],
  ['Vyana, 30 iyun 1884', 'Vyana, 30 iyun 1884', 18],
  ['Vyana, 16 yanvar 1885', 'Vyana, 16 yanvar 1885', 19],
  ['Vyana, 7 may 1885', 'Vyana, 7 may 1885', 20],
  ['Vyana, 6 iyun 1885', 'Vyana, 6 iyun 1885', 21],
  ['Vyana, 20 iyun 1885', 'Vyana, 20 iyun 1885', 22],
  ['Modlinq, 23 iyul 1885', 'Modlinq, 23 iyul 1885', 23],
  ['Vyana, 6 avqust 1885', 'Vyana, 6 avqust 1885', 24],
  ['Vyana, 12 avqust 1885', 'Vyana, 12 avqust 1885', 25],
  ['Paris, 19 oktyabr 1885', 'Paris, 19 oktyabr 1885', 26],
  ['Paris, 8 noyabr 1885', 'Paris, 8 noyabr 1885', 27],
  ['Paris, 18 yanvar 1886', 'Paris, 18 yanvar 1886', 28],
  ['Paris, 20 yanvar 1886', 'Paris, 20 yanvar 1886', 29],
  ['Paris, 2 fevral 1886', 'Paris, 2 fevral 1886', 30],
  ['Paris, 3 fevral 1886', 'Paris, 3 fevral 1886', 31],
  ['Berlin, 10 mart 1886', 'Berlin, 10 mart 1886', 32],
  ['Berlin, 19 mart 1886', 'Berlin, 19 mart 1886', 33],
  ['Vyana, 6 may 1886', 'Vyana, 6 may 1886', 34],
  ['Vyana, 13 may 1886', 'Vyana, 13 may 1886', 35],
  ['Roma, 20 sentyabr 1912', 'Roma, 20 sentyabr 1912', 36],
];
BOOKS.push({
  slug: 'freud-sevgi-mektublari', logo: 'SM', epub: 'Sevgi məktubları.epub',
  title: 'Sevgi məktubları', titlePrinted: 'SEVGİ MƏKTUBLARI',
  author: 'Ziqmund Freyd', year: '1882–1886', yearSub: 'İlk nəşr — 1882–1886', ru: true, prefix: 'mektub',
  chapters: [].concat(LETTERS.map(([printed, short, page]) => ({ title: printed, short, find: [printed], pdfPage: page })))

});

/* «Тотем və Tabu» — НАШ перевод: печатного издания у него нет, EPUB собран нами
   из переведённых частей (_align/translations/totem). Главы ищутся по заголовкам,
   заданным при сборке EPUB. Год — первая публикация произведения (1913). */
BOOKS.push({
  slug: 'freud-totem-ve-tabu', logo: 'TT', epub: 'Totem və Tabu.epub',
  title: 'Totem və Tabu', titlePrinted: 'TOTEM VƏ TABU',
  author: 'Ziqmund Freyd', year: '1913', yearSub: 'İlk nəşr — 1913', ru: false, prefix: 'totem',
  chapters: [
    { title: 'Giriş', find: ['Giriş'], pdfPage: 5 },
    { title: 'I. İNSEST QORXUSU', find: ['I', 'İNSEST QORXUSU'], pdfPage: 12 },
    { title: 'II. TABU VƏ HİSLƏRİN AMBİVALENTLİYİ', find: ['II', 'TABU VƏ HİSLƏRİN AMBİVALENTLİYİ'], pdfPage: 30 },
    { title: 'III. ANİMIZM, MAGİYA VƏ DÜŞÜNCƏNİN HƏR ŞEYƏ QADİRLİYİ', short: 'III. ANİMIZM, MAGİYA…',
      find: ['III', 'ANİMIZM, MAGİYA VƏ DÜŞÜNCƏNİN HƏR ŞEYƏ QADİRLİYİ'], pdfPage: 75 },
    { title: 'IV. TOTEMİN İNFANTİL QAYITMASI', find: ['IV', 'TOTEMİN İNFANTİL QAYITMASI'], pdfPage: 95 },
  ],
});

/* «Mədəniyyətin sancıları» — НАШ перевод (8 разделов). У «Недовольства культурой»
   авторских названий разделов нет: в печатных изданиях стоят только римские цифры,
   а это запрещено правилом владельца (§4.1 стандарта заливки) — названия даны по
   содержанию раздела. EPUB собран нами из переведённых глав (_med_final).
   Год — первая публикация произведения (1930). Русская версия лежит в books/<slug>/ru. */
BOOKS.push({
  slug: 'freud-medeniyyetin-sancilari', logo: 'MS', epub: 'Mədəniyyətin sancıları.epub',
  title: 'Mədəniyyətin sancıları', titlePrinted: 'MƏDƏNİYYƏTİN SANCILARI',
  author: 'Ziqmund Freyd', year: '1930', yearSub: 'İlk nəşr — 1930', ru: true, prefix: 'glava',
  chapters: [
    { title: 'I. Həyatın məqsədləri və nemətlərin yanlış ölçüsü', short: 'I. Həyatın məqsədləri',
      find: ['I. Həyatın məqsədləri və nemətlərin yanlış ölçüsü'], pdfPage: 5 },
    { title: 'II. Din və onun təsəlliləri', short: 'II. Din və təsəlliləri',
      find: ['II. Din və onun təsəlliləri'], pdfPage: 17 },
    { title: 'III. Xoşbəxtlik, əzab və mədəniyyətin tələbləri', short: 'III. Xoşbəxtlik və əzab',
      find: ['III. Xoşbəxtlik, əzab və mədəniyyətin tələbləri'], pdfPage: 33 },
    { title: 'IV. Mədəniyyətin mənşəyi və insanın qüdrəti', short: 'IV. Mədəniyyətin mənşəyi',
      find: ['IV. Mədəniyyətin mənşəyi və insanın qüdrəti'], pdfPage: 50 },
    { title: 'V. Seksuallıq, sublimasiya və instinktlərdən imtina', short: 'V. Seksuallıq və imtina',
      find: ['V. Seksuallıq, sublimasiya və instinktlərdən imtina'], pdfPage: 66 },
    { title: 'VI. Aqressiya və Erosun ölüm instinkti ilə mübarizəsi', short: 'VI. Aqressiya və ölüm instinkti',
      find: ['VI. Aqressiya və Erosun ölüm instinkti ilə mübarizəsi'], pdfPage: 82 },
    { title: 'VII. Təqsir hissi mədəni tərəqqinin qiyməti kimi', short: 'VII. Təqsir hissi',
      find: ['VII. Təqsir hissi mədəni tərəqqinin qiyməti kimi'], pdfPage: 99 },
    { title: 'VIII. Nəticə: azadlıq və mədəniyyətin gələcəyi', short: 'VIII. Nəticə',
      find: ['VIII. Nəticə: azadlıq və mədəniyyətin gələcəyi'], pdfPage: 114 },
  ],
});

/* «Flissə məktublar» — НАШ перевод писем Фрейда Вильгельму Флиссу (1887–1904).
   Источник — русское зеркало freudproject (категория «Письма Флиссу», 42 поста).
   Печатной азербайджанской книги нет, EPUB собран нами из переведённых писем
   (_make_fliess_epub.py): заголовок каждой позиции — «дата — тема» (§4.3 стандарта),
   порядок — хронология источника, письма от Флисса помечены, памфлет 1906 года — отдельной позицией. */
BOOKS.push({
  slug: 'freud-fliesse-mektublari', logo: 'FM', epub: 'Flissə məktublar.epub',
  title: 'Flissə məktublar', titlePrinted: 'FLİSSƏ MƏKTUBLAR',
  author: 'Ziqmund Freyd', year: '1887–1904', yearSub: 'Yazışma illəri — 1887–1904', ru: false, prefix: 'fliess',
  chapters: [
      { title: '24 noyabr 1887 — xanım A.-nın diaqnozu və elmi işlər barədə', short: '24 noyabr 1887', find: ['24 noyabr 1887 — xanım A.-nın diaqnozu və elmi işlər barədə'], pdfPage: 1 },
      { title: '28 dekabr 1887 — Bernhaymın tərcüməsi və hipnoz uğurları barədə', short: '28 dekabr 1887', find: ['28 dekabr 1887 — Bernhaymın tərcüməsi və hipnoz uğurları barədə'], pdfPage: 2 },
      { title: '4 fevral 1888 — frau A., tibbi cəmiyyət qalmaqalı və Meynert barədə', short: '4 fevral 1888', find: ['4 fevral 1888 — frau A., tibbi cəmiyyət qalmaqalı və Meynert barədə'], pdfPage: 3 },
      { title: '28 may 1888 — yay kurortu seçimi və yazı işləri barədə', short: '28 may 1888', find: ['28 may 1888 — yay kurortu seçimi və yazı işləri barədə'], pdfPage: 4 },
      { title: '29 avqust 1888 — ümumi praktikadan imtina və təlqin kitabı barədə', short: '29 avqust 1888', find: ['29 avqust 1888 — ümumi praktikadan imtina və təlqin kitabı barədə'], pdfPage: 5 },
      { title: '21 iyul 1890 — konqres dəvəti və Berlinə səfər barədə', short: '21 iyul 1890', find: ['21 iyul 1890 — konqres dəvəti və Berlinə səfər barədə'], pdfPage: 6 },
      { title: '1 avqust 1890 — Berlinə səfərin baş tutmaması barədə', short: '1 avqust 1890', find: ['1 avqust 1890 — Berlinə səfərin baş tutmaması barədə'], pdfPage: 7 },
      { title: '11 avqust 1890 — Zalsburqda görüş və tarixin təyini barədə', short: '11 avqust 1890', find: ['11 avqust 1890 — Zalsburqda görüş və tarixin təyini barədə'], pdfPage: 8 },
      { title: '2 may 1891 — afaziya kitabı və Oliverin doğulması barədə', short: '2 may 1891', find: ['2 may 1891 — afaziya kitabı və Oliverin doğulması barədə'], pdfPage: 9 },
      { title: '17 avqust 1891 — səyahət planları və görüş istəyi barədə', short: '17 avqust 1891', find: ['17 avqust 1891 — səyahət planları və görüş istəyi barədə'], pdfPage: 10 },
      { title: '11 sentyabr 1891 — sentyabrın 15-də gözlənilən görüş barədə', short: '11 sentyabr 1891', find: ['11 sentyabr 1891 — sentyabrın 15-də gözlənilən görüş barədə'], pdfPage: 11 },
      { title: '25 may 1892 — toy təbriki və hədiyyə seçimi barədə', short: '25 may 1892', find: ['25 may 1892 — toy təbriki və hədiyyə seçimi barədə'], pdfPage: 12 },
      { title: '28 iyun 1892 — Dostun diaqnostik bacarına etimad', short: '28 iyun 1892', find: ['28 iyun 1892 — Dostun diaqnostik bacarına etimad'], pdfPage: 13 },
      { title: '12 iyul 1892 — Dostun atasını ziyarət və seçimi', short: '12 iyul 1892', find: ['12 iyul 1892 — Dostun atasını ziyarət və seçimi'], pdfPage: 14 },
      { title: '4 oktyabr 1892 — Freydin ünvanı və qəbul saatları', short: '4 oktyabr 1892', find: ['4 oktyabr 1892 — Freydin ünvanı və qəbul saatları'], pdfPage: 15 },
      { title: '21 oktyabr 1892 — Fr pasiyentini ziyarət və diaqnoz mübahisəsi', short: '21 oktyabr 1892', find: ['21 oktyabr 1892 — Fr pasiyentini ziyarət və diaqnoz mübahisəsi'], pdfPage: 16 },
      { title: '24 oktyabr 1892 — Freydin xidməti məktublaşması haqqında', short: '24 oktyabr 1892', find: ['24 oktyabr 1892 — Freydin xidməti məktublaşması haqqında'], pdfPage: 17 },
      { title: '31 oktyabr 1892 — Freydin xidməti qeydi haqqında', short: '31 oktyabr 1892', find: ['31 oktyabr 1892 — Freydin xidməti qeydi haqqında'], pdfPage: 18 },
      { title: '3 noyabr 1892 — Alınan hədiyyəyə minnətdarlıq', short: '3 noyabr 1892', find: ['3 noyabr 1892 — Alınan hədiyyəyə minnətdarlıq'], pdfPage: 19 },
      { title: '18 dekabr 1892 — Freydin məktublaşmasının başlanğıcı haqqında', short: '18 dekabr 1892', find: ['18 dekabr 1892 — Freydin məktublaşmasının başlanğıcı haqqında'], pdfPage: 20 },
      { title: '5 yanvar 1893 — Berggasse ünvanından Freydin məktubu', short: '5 yanvar 1893', find: ['5 yanvar 1893 — Berggasse ünvanından Freydin məktubu'], pdfPage: 21 },
      { title: '14 may 1893 — Nevraljiya baş ağrısı olan pasiyentin tövsiyəsi', short: '14 may 1893', find: ['14 may 1893 — Nevraljiya baş ağrısı olan pasiyentin tövsiyəsi'], pdfPage: 22 },
      { title: '15 may 1893 — Freydin sağlamlığı və dostuna məsləhət', short: '15 may 1893', find: ['15 may 1893 — Freydin sağlamlığı və dostuna məsləhət'], pdfPage: 23 },
      { title: '30 may 1893 — Sağalma və dostdan məktub sevinci', short: '30 may 1893', find: ['30 may 1893 — Sağalma və dostdan məktub sevinci'], pdfPage: 24 },
      { title: '10 iyul 1893 — tətil planları və görüş haqqında', short: '10 iyul 1893', find: ['10 iyul 1893 — tətil planları və görüş haqqında'], pdfPage: 25 },
      { title: '6 oktyabr 1893 — Şarko haqqında hökm və işin canlanması barədə', short: '6 oktyabr 1893', find: ['6 oktyabr 1893 — Şarko haqqında hökm və işin canlanması barədə'], pdfPage: 26 },
      { title: '17 noyabr 1893 — cinsi işlər və qorxu haqqında', short: '17 noyabr 1893', find: ['17 noyabr 1893 — cinsi işlər və qorxu haqqında'], pdfPage: 27 },
      { title: '7 fevral 1894 — obsesif fikirlər nəzəriyyəsi və yeni iş barədə', short: '7 fevral 1894', find: ['7 fevral 1894 — obsesif fikirlər nəzəriyyəsi və yeni iş barədə'], pdfPage: 28 },
      { title: '19 aprel 1894 — Sağlamlıq və tütün çəkilməkdən imtina', short: '19 aprel 1894', find: ['19 aprel 1894 — Sağlamlıq və tütün çəkilməkdən imtina'], pdfPage: 29 },
      { title: '25 aprel 1894 — Freydin sağlamlığı və diaqnozdakı şübhələr', short: '25 aprel 1894', find: ['25 aprel 1894 — Freydin sağlamlığı və diaqnozdakı şübhələr'], pdfPage: 30 },
      { title: '21 may 1894 — nevrozların aydınlaşdırılması və Charcot barədə', short: '21 may 1894', find: ['21 may 1894 — nevrozların aydınlaşdırılması və Charcot barədə'], pdfPage: 31 },
      { title: '14 iyul 1894 — Tütündən imtina və yeni işlər', short: '14 iyul 1894', find: ['14 iyul 1894 — Tütündən imtina və yeni işlər'], pdfPage: 32 },
      { title: '4 mart 1895 — histeriyanın terapiyası məqaləsi barədə', short: '4 mart 1895', find: ['4 mart 1895 — histeriyanın terapiyası məqaləsi barədə'], pdfPage: 33 },
      { title: '27 aprel 1895 — məktublaşmanın çətinlikləri barədə', short: '27 aprel 1895', find: ['27 aprel 1895 — məktublaşmanın çətinlikləri barədə'], pdfPage: 34 },
      { title: '25 may 1895 — psixologiya və nevroz işləri barədə', short: '25 may 1895', find: ['25 may 1895 — psixologiya və nevroz işləri barədə'], pdfPage: 35 },
      { title: '12 iyun 1895 — yeni nəzəriyyələr və siqaret çəkmə barədə', short: '12 iyun 1895', find: ['12 iyun 1895 — yeni nəzəriyyələr və siqaret çəkmə barədə'], pdfPage: 36 },
      { title: '24 iyul 1895 — Sağlamlığa diqqət və gündəlik işlər', short: '24 iyul 1895', find: ['24 iyul 1895 — Sağlamlığa diqqət və gündəlik işlər'], pdfPage: 37 },
      { title: '16 oktyabr 1895 — isteriya və nevrozun müalicəsi barədə', short: '16 oktyabr 1895', find: ['16 oktyabr 1895 — isteriya və nevrozun müalicəsi barədə'], pdfPage: 38 },
      { title: '20 oktyabr 1895 — histeriya və nevrozun həlli barədə', short: '20 oktyabr 1895', find: ['20 oktyabr 1895 — histeriya və nevrozun həlli barədə'], pdfPage: 39 },
      { title: '8 noyabr 1895 — nikotindən imtina və psixoloji əlyazmalar barədə', short: '8 noyabr 1895', find: ['8 noyabr 1895 — nikotindən imtina və psixoloji əlyazmalar barədə'], pdfPage: 40 },
      { title: '29 noyabr 1895 — iş qabiliyyəti və uşaq iflici barədə', short: '29 noyabr 1895', find: ['29 noyabr 1895 — iş qabiliyyəti və uşaq iflici barədə'], pdfPage: 41 },
      { title: '3 dekabr 1895 — qızının doğulması və elmi işlər barədə', short: '3 dekabr 1895', find: ['3 dekabr 1895 — qızının doğulması və elmi işlər barədə'], pdfPage: 42 },
      { title: '6 fevral 1896 — Robert Vilhelm və yazı işləri barədə', short: '6 fevral 1896', find: ['6 fevral 1896 — Robert Vilhelm və yazı işləri barədə'], pdfPage: 43 },
      { title: '13 fevral 1896 — tənhalıq və məktub sevinci barədə', short: '13 fevral 1896', find: ['13 fevral 1896 — tənhalıq və məktub sevinci barədə'], pdfPage: 44 },
      { title: '16 mart 1896 — elm və şeir barədə', short: '16 mart 1896', find: ['16 mart 1896 — elm və şeir barədə'], pdfPage: 45 },
      { title: '2 aprel 1896 — əsərin Deuticke-ə göndərilməsi barədə', short: '2 aprel 1896', find: ['2 aprel 1896 — əsərin Deuticke-ə göndərilməsi barədə'], pdfPage: 46 },
      { title: '4 may 1896 — neyron nəzəriyyəsi və psixologiya barədə', short: '4 may 1896', find: ['4 may 1896 — neyron nəzəriyyəsi və psixologiya barədə'], pdfPage: 47 },
      { title: '30 may 1896 — psixonevroz etiologiyası barədə', short: '30 may 1896', find: ['30 may 1896 — psixonevroz etiologiyası barədə'], pdfPage: 48 },
      { title: '30 iyun 1896 — atanın vəziyyəti və səfər barədə', short: '30 iyun 1896', find: ['30 iyun 1896 — atanın vəziyyəti və səfər barədə'], pdfPage: 49 },
      { title: '29 sentyabr 1896 — Köçməyə minnətdarlıq və xəstəlik təsviri', short: '29 sentyabr 1896', find: ['29 sentyabr 1896 — Köçməyə minnətdarlıq və xəstəlik təsviri'], pdfPage: 50 },
      { title: '2 noyabr 1896 — köhnə dostun ölümü barədə', short: '2 noyabr 1896', find: ['2 noyabr 1896 — köhnə dostun ölümü barədə'], pdfPage: 51 },
      { title: '6 dekabr 1896 — Psixik aparat qatları hipotezi haqqında', short: '6 dekabr 1896', find: ['6 dekabr 1896 — Psixik aparat qatları hipotezi haqqında'], pdfPage: 52 },
      { title: '17 dekabr 1896 — psixonevrotik məsələlər və qorxu haqqında', short: '17 dekabr 1896', find: ['17 dekabr 1896 — psixonevrotik məsələlər və qorxu haqqında'], pdfPage: 53 },
      { title: '28 aprel 1897 — yuxu və teleqram barədə', short: '28 aprel 1897', find: ['28 aprel 1897 — yuxu və teleqram barədə'], pdfPage: 54 },
      { title: '2 may 1897 — histeriyanın strukturu və fantaziyalar barədə', short: '2 may 1897', find: ['2 may 1897 — histeriyanın strukturu və fantaziyalar barədə'], pdfPage: 55 },
      { title: '7 iyul 1897 — Nadir məktublara görə üzr istəmə', short: '7 iyul 1897', find: ['7 iyul 1897 — Nadir məktublara görə üzr istəmə'], pdfPage: 56 },
      { title: '14 avqust 1897 — imtina və kədər barədə', short: '14 avqust 1897', find: ['14 avqust 1897 — imtina və kədər barədə'], pdfPage: 57 },
      { title: '18 avqust 1897 — məktublaşma və qorxular barədə', short: '18 avqust 1897', find: ['18 avqust 1897 — məktublaşma və qorxular barədə'], pdfPage: 58 },
      { title: '21 sentyabr 1897 — Neurotica-ya inamsızlıq barədə', short: '21 sentyabr 1897', find: ['21 sentyabr 1897 — Neurotica-ya inamsızlıq barədə'], pdfPage: 59 },
      { title: '3 oktyabr 1897 — Ziyarət və şəxsi işlərin müzakirəsi', short: '3 oktyabr 1897', find: ['3 oktyabr 1897 — Ziyarət və şəxsi işlərin müzakirəsi'], pdfPage: 60 },
      { title: '27 oktyabr 1897 — Edip kompleksi və özünüanaliz barədə', short: '27 oktyabr 1897', find: ['27 oktyabr 1897 — Edip kompleksi və özünüanaliz barədə'], pdfPage: 61 },
      { title: '5 noyabr 1897 — yazışma səbəbi və özünütəsdiq barədə', short: '5 noyabr 1897', find: ['5 noyabr 1897 — yazışma səbəbi və özünütəsdiq barədə'], pdfPage: 62 },
      { title: '14 noyabr 1897 — yeni şeir və diş ağrıları barədə', short: '14 noyabr 1897', find: ['14 noyabr 1897 — yeni şeir və diş ağrıları barədə'], pdfPage: 63 },
      { title: '3 dekabr 1897 — tənqidi gün və yeni ideyalar barədə', short: '3 dekabr 1897', find: ['3 dekabr 1897 — tənqidi gün və yeni ideyalar barədə'], pdfPage: 64 },
      { title: '12 dekabr 1897 — endopsixik miflər" nədir barədə', short: '12 dekabr 1897', find: ['12 dekabr 1897 — endopsixik miflər" nədir barədə'], pdfPage: 65 },
      { title: '22 dekabr 1897 — həyatın mənası və ruh haqqında', short: '22 dekabr 1897', find: ['22 dekabr 1897 — həyatın mənası və ruh haqqında'], pdfPage: 66 },
      { title: '29 dekabr 1897 — qara böcək və qorxu hücumu barədə', short: '29 dekabr 1897', find: ['29 dekabr 1897 — qara böcək və qorxu hücumu barədə'], pdfPage: 67 },
      { title: '4 yanvar 1898 — sol əlliliyin təfsiri barədə', short: '4 yanvar 1898', find: ['4 yanvar 1898 — sol əlliliyin təfsiri barədə'], pdfPage: 68 },
      { title: '9 fevral 1898 — yuxu kitabının yazılması barədə', short: '9 fevral 1898', find: ['9 fevral 1898 — yuxu kitabının yazılması barədə'], pdfPage: 69 },
      { title: '10 mart 1898 — yuxu kitabının nailiyyətləri və metapsixologiya barədə', short: '10 mart 1898', find: ['10 mart 1898 — yuxu kitabının nailiyyətləri və metapsixologiya barədə'], pdfPage: 70 },
      { title: '15 mart 1898 — Konrad Ferdinand və Meyer haqqında', short: '15 mart 1898', find: ['15 mart 1898 — Konrad Ferdinand və Meyer haqqında'], pdfPage: 71 },
      { title: '24 mart 1898 — yuxu əlyazması haqqında', short: '24 mart 1898', find: ['24 mart 1898 — yuxu əlyazması haqqında'], pdfPage: 72 },
      { title: '3 aprel 1898 — yuxular kitabı və xəyallar barədə', short: '3 aprel 1898', find: ['3 aprel 1898 — yuxular kitabı və xəyallar barədə'], pdfPage: 73 },
      { title: '14 aprel 1898 — Pasxa, yeni xəbərlər və özüm barədə', short: '14 aprel 1898', find: ['14 aprel 1898 — Pasxa, yeni xəbərlər və özüm barədə'], pdfPage: 74 },
      { title: '9 iyun 1898 — yuxunun davamı və yeni psixologiya barədə', short: '9 iyun 1898', find: ['9 iyun 1898 — yuxunun davamı və yeni psixologiya barədə'], pdfPage: 75 },
      { title: '20 iyun 1898 — Ausseedən qayıdış və işlər barədə', short: '20 iyun 1898', find: ['20 iyun 1898 — Ausseedən qayıdış və işlər barədə'], pdfPage: 76 },
      { title: '7 iyul 1898 — Yorğuların Yozumlanması" haqqında', short: '7 iyul 1898', find: ['7 iyul 1898 — Yorğuların Yozumlanması" haqqında'], pdfPage: 77 },
      { title: '20 avqust 1898 — səyahət təəssüratları və yuxu haqqında', short: '20 avqust 1898', find: ['20 avqust 1898 — səyahət təəssüratları və yuxu haqqında'], pdfPage: 78 },
      { title: '26 avqust 1898 — metapsixologiya və Lipps haqqında', short: '26 avqust 1898', find: ['26 avqust 1898 — metapsixologiya və Lipps haqqında'], pdfPage: 79 },
      { title: '31 avqust 1898 — Adriatikə səyahət və histeriya barədə', short: '31 avqust 1898', find: ['31 avqust 1898 — Adriatikə səyahət və histeriya barədə'], pdfPage: 80 },
      { title: '22 sentyabr 1898 — Vyananın narazılığı və psixologiya barədə', short: '22 sentyabr 1898', find: ['22 sentyabr 1898 — Vyananın narazılığı və psixologiya barədə'], pdfPage: 81 },
      { title: '27 sentyabr 1898 — Signorelli məqaləsi və Ziyenə göndərilməsi barədə', short: '27 sentyabr 1898', find: ['27 sentyabr 1898 — Signorelli məqaləsi və Ziyenə göndərilməsi barədə'], pdfPage: 82 },
      { title: '9 oktyabr 1898 — praktika və xəstələrlə iş barədə', short: '9 oktyabr 1898', find: ['9 oktyabr 1898 — praktika və xəstələrlə iş barədə'], pdfPage: 83 },
      { title: '23 oktyabr 1898 — ad günü təbriki və arzular barədə', short: '23 oktyabr 1898', find: ['23 oktyabr 1898 — ad günü təbriki və arzular barədə'], pdfPage: 84 },
      { title: '3 yanvar 1899 — özünü analiz etməyin qələbəsi barədə', short: '3 yanvar 1899', find: ['3 yanvar 1899 — özünü analiz etməyin qələbəsi barədə'], pdfPage: 85 },
      { title: '16 yanvar 1899 — istək nəzəriyyəsi və konqres barədə', short: '16 yanvar 1899', find: ['16 yanvar 1899 — istək nəzəriyyəsi və konqres barədə'], pdfPage: 86 },
      { title: '30 yanvar 1899 — yeni kəşf və psixologiya barədə', short: '30 yanvar 1899', find: ['30 yanvar 1899 — yeni kəşf və psixologiya barədə'], pdfPage: 87 },
      { title: '6 fevral 1899 — gündəlik xəstələr və korollarilər barədə', short: '6 fevral 1899', find: ['6 fevral 1899 — gündəlik xəstələr və korollarilər barədə'], pdfPage: 88 },
      { title: '2 mart 1899 — yazmağı unutmaq və fobiya barədə', short: '2 mart 1899', find: ['2 mart 1899 — yazmağı unutmaq və fobiya barədə'], pdfPage: 89 },
      { title: '28 may 1899 — örtük xatirələri və yuxu haqqında', short: '28 may 1899', find: ['28 may 1899 — örtük xatirələri və yuxu haqqında'], pdfPage: 90 },
      { title: '27 iyun 1899 — yazı işi və yorğunluq barədə', short: '27 iyun 1899', find: ['27 iyun 1899 — yazı işi və yorğunluq barədə'], pdfPage: 91 },
      { title: '17 iyul 1899 — yazı işləri və çap barədə', short: '17 iyul 1899', find: ['17 iyul 1899 — yazı işləri və çap barədə'], pdfPage: 92 },
      { title: '22 iyul 1899 — yuxu məsələsi və ədəbiyyat barədə', short: '22 iyul 1899', find: ['22 iyul 1899 — yuxu məsələsi və ədəbiyyat barədə'], pdfPage: 93 },
      { title: '20 avqust 1899 — tətil və yuxu haqqında yazı işləri barədə', short: '20 avqust 1899', find: ['20 avqust 1899 — tətil və yuxu haqqında yazı işləri barədə'], pdfPage: 94 },
      { title: '9 oktyabr 1899 — psixoloji əsərlər və yuxuların təfsiri barədə', short: '9 oktyabr 1899', find: ['9 oktyabr 1899 — psixoloji əsərlər və yuxuların təfsiri barədə'], pdfPage: 95 },
      { title: '27 oktyabr 1899 — yuxular kitabının göndərilməsi barədə', short: '27 oktyabr 1899', find: ['27 oktyabr 1899 — yuxular kitabının göndərilməsi barədə'], pdfPage: 96 },
      { title: '9 dekabr 1899 — nevrozların seçimi problemi barədə', short: '9 dekabr 1899', find: ['9 dekabr 1899 — nevrozların seçimi problemi barədə'], pdfPage: 97 },
      { title: '26 yanvar 1900 — yeni xəstə və kitab haqqında', short: '26 yanvar 1900', find: ['26 yanvar 1900 — yeni xəstə və kitab haqqında'], pdfPage: 98 },
      { title: '1 fevral 1900 — Xəstəliyin təkrarlanması narahatlığı', short: '1 fevral 1900', find: ['1 fevral 1900 — Xəstəliyin təkrarlanması narahatlığı'], pdfPage: 99 },
      { title: '12 fevral 1900 — anasının xəstəliyi və məktublaşma barədə', short: '12 fevral 1900', find: ['12 fevral 1900 — anasının xəstəliyi və məktublaşma barədə'], pdfPage: 100 },
      { title: '23 mart 1900 — Minna qəbulu və yuxu haqqında', short: '23 mart 1900', find: ['23 mart 1900 — Minna qəbulu və yuxu haqqında'], pdfPage: 101 },
      { title: '4 aprel 1900 — iş məsələləri və cavab barədə', short: '4 aprel 1900', find: ['4 aprel 1900 — iş məsələləri və cavab barədə'], pdfPage: 102 },
      { title: '16 may 1900 — xəstənin müalicəsi və açarların tapılması barədə', short: '16 may 1900', find: ['16 may 1900 — xəstənin müalicəsi və açarların tapılması barədə'], pdfPage: 103 },
      { title: '20 may 1900 — boş vaxt və tənbəllik barədə', short: '20 may 1900', find: ['20 may 1900 — boş vaxt və tənbəllik barədə'], pdfPage: 104 },
      { title: '12 iyun 1900 — ailə qonaqlığı və təbiət gözəlliyi barədə', short: '12 iyun 1900', find: ['12 iyun 1900 — ailə qonaqlığı və təbiət gözəlliyi barədə'], pdfPage: 105 },
      { title: '14 oktyabr 1900 — yuxu təhlili və yeni pasiyent barədə', short: '14 oktyabr 1900', find: ['14 oktyabr 1900 — yuxu təhlili və yeni pasiyent barədə'], pdfPage: 106 },
      { title: '23 oktyabr 1900 — Yaşlı nəslin getməsinə təbrik', short: '23 oktyabr 1900', find: ['23 oktyabr 1900 — Yaşlı nəslin getməsinə təbrik'], pdfPage: 107 },
      { title: '25 yanvar 1901 — İraum və Histeriya» və yeni iş barədə', short: '25 yanvar 1901', find: ['25 yanvar 1901 — İraum və Histeriya» və yeni iş barədə'], pdfPage: 108 },
      { title: '30 yanvar 1901 — yuxu və histeriya haqqında', short: '30 yanvar 1901', find: ['30 yanvar 1901 — yuxu və histeriya haqqında'], pdfPage: 109 },
      { title: '4 iyul 1901 — qəbul saatı və suallar barədə', short: '4 iyul 1901', find: ['4 iyul 1901 — qəbul saatı və suallar barədə'], pdfPage: 110 },
      { title: '7 oktyabr 1901 — xanım D. və müalicə çətinlikləri barədə', short: '7 oktyabr 1901', find: ['7 oktyabr 1901 — xanım D. və müalicə çətinlikləri barədə'], pdfPage: 111 },
      { title: '2 noyabr 1901 — xəstənin vəziyyəti və terapiya barədə', short: '2 noyabr 1901', find: ['2 noyabr 1901 — xəstənin vəziyyəti və terapiya barədə'], pdfPage: 112 },
      { title: '7 dekabr 1901 — xanım D. və müalicənin pozulması barədə', short: '7 dekabr 1901', find: ['7 dekabr 1901 — xanım D. və müalicənin pozulması barədə'], pdfPage: 113 },
      { title: '26 aprel 1904 — Elmi jurnal yaratmaqda əməkdaşlıq təklifi', short: '26 aprel 1904', find: ['26 aprel 1904 — Elmi jurnal yaratmaqda əməkdaşlıq təklifi'], pdfPage: 114 },
      { title: '27 aprel 1904 — Vilhelm Flissdən Ziqmund Freydə: Ziqmundun tanınması sevinci', short: '27 aprel 1904', find: ['27 aprel 1904 — Vilhelm Flissdən Ziqmund Freydə: Ziqmundun tanınması sevinci'], pdfPage: 115 },
      { title: '15 iyul 1904 — Mariin bacısının gəlinliyinin təbriki', short: '15 iyul 1904', find: ['15 iyul 1904 — Mariin bacısının gəlinliyinin təbriki'], pdfPage: 116 },
      { title: '20 iyul 1904 — Vilhelm Flissdən Ziqmund Freydə: Vyan otelindən məktub', short: '20 iyul 1904', find: ['20 iyul 1904 — Vilhelm Flissdən Ziqmund Freydə: Vyan otelindən məktub'], pdfPage: 117 },
      { title: '23 iyul 1904 — Freydin Vilhelm Sonnenfelusa məktubu', short: '23 iyul 1904', find: ['23 iyul 1904 — Freydin Vilhelm Sonnenfelusa məktubu'], pdfPage: 118 },
      { title: '26 iyul 1904 — Vilhelm Flissdən Ziqmund Freydə: Weiningerin əlyazmasının nəşri mübahisəsi', short: '26 iyul 1904', find: ['26 iyul 1904 — Vilhelm Flissdən Ziqmund Freydə: Weiningerin əlyazmasının nəşri mübahisəsi'], pdfPage: 119 },
    ],
});

/* ── каркас страницы ── */
const TOC_STYLE = '<style>' +
  '.home-hero{padding:16px 0 11px}' +
  '.book-toc{margin:8px auto 36px}' +
  '.book-toc .toc-title{margin:0 0 16px 0;padding-bottom:8px}' +
  '.content-wrap .toc-test{margin:0 0 34px}' +
  '.d-nav{display:flex;align-items:center;justify-content:space-between;gap:.5rem;margin:2.2rem 0 .5rem;padding:.7rem 0 0;border-top:1px solid var(--border)}' +
  '.d-nav a{color:var(--text);text-decoration:none;padding:.35rem .7rem;border-radius:6px;font-family:var(--mono,monospace);font-weight:700;font-size:.95rem;white-space:nowrap;max-width:42%;overflow:hidden;text-overflow:ellipsis}' +
  '.d-nav .up{color:var(--gold);font-family:var(--font);font-weight:600}' +
  '.d-nav .dn-name{color:var(--text2);font-weight:400;font-family:var(--font);font-size:.85rem}' +
  '.content-wrap p{margin:0 0 1.05em;color:var(--text)}' +
  '@media(max-width:600px){.content-wrap{padding-left:18px;padding-right:18px}}' +
  '.sidebar .nav-sub-link{padding:7px 14px 7px 18px;font-size:11px;gap:.5rem;line-height:1.4}' +
  '.sidebar .sub-code{flex:0 0 auto;width:auto;white-space:nowrap;margin-right:0;font-size:10px}' +
  '.sidebar .nav-sub-link.is-active{color:var(--gold);border-left-color:var(--gold);background:var(--gold-bg)}' +
  '.content-wrap h3.sub{font-size:1rem;font-weight:700;line-height:1.35;margin:1.5rem 0 .5rem;padding:0;border:0;color:var(--text)}' +
  /* титул книги: название · автор · год — ровно, без разнобоя в кегле и регистре */
  '.home-hero{padding:4px 0 2px}' +
  '.home-hero h1.home-title{font-size:clamp(22px,4.4vw,32px);line-height:1.18;letter-spacing:.01em;margin:0}' +
  '.home-hero .sub{font-size:15px;line-height:1.5;margin:10px 0 0;color:var(--text2);letter-spacing:.02em}' +
  '.home-hero .sub:first-of-type{color:var(--text)}' +
  '.home-hero .sub.year{font-variant-numeric:tabular-nums}' +
  READ_CSS +
  '</style>';

/* только для индекса книги: без пустоты снизу, без лишнего воздуха сверху */
const INDEX_STYLE = '<style>' +
  '.content-wrap{padding-top:.6rem;padding-bottom:2rem}' +
  '.book-toc{margin:16px auto 6px}' +
  '.book-toc .toc-chapter{margin:0}' +
  '</style>';

function headHtml(b, canon, title, desc, indexCss) {
  const dir = '';                                  /* AZ-страницы лежат в корне книги */
  const langs = b.ru ? 'az,ru' : 'az';
  const avail = b.ru ? 'az ru' : 'az';
  const alt = '  <link rel="canonical" href="' + canon + '" />\n\n' +
    '  <link rel="alternate" hreflang="az" href="' + canon + '" />\n\n' +
    (b.ru ? '  <link rel="alternate" hreflang="ru" href="https://ragimoff.org/books/' + b.slug + '/ru/" />\n\n' : '') +
    '  <link rel="alternate" hreflang="x-default" href="' + canon + '" />';
  return TPL.head
    .replace('<html lang="az">', '<html data-langs="' + langs + '" data-lang-url-az="/books/' + b.slug + '/"' +
      (b.ru ? ' data-lang-url-ru="/books/' + b.slug + '/ru/"' : '') + ' data-lang-avail="' + avail + '" lang="az">')
    .replace('<link rel="stylesheet" href="style.css">', '<link rel="stylesheet" href="' + dir + 'style.css">')
    .replace(/<title>[\s\S]*?<\/title>/, '<title>' + esc(title) + ' | ' + esc(b.titlePrinted) + '</title>')
    .replace(/<meta name="description" content="[^"]*"/, '<meta name="description" content="' + esc(desc) + '"')
    .replace(/<meta property="og:title" content="[^"]*"/, '<meta property="og:title" content="' + esc(title) + '"')
    .replace(/<meta property="og:description" content="[^"]*"/, '<meta property="og:description" content="' + esc(desc) + '"')
    .replace(/<meta property="og:url" content="[^"]*"/, '<meta property="og:url" content="' + canon + '"')
    .replace(/"name":"[^"]*","inLanguage":"[^"]*"/, '"name":"' + esc(b.title) + '","inLanguage":"az"')
    .replace(/"author":\{"@type":"Person","name":"[^"]*"\}/, '"author":{"@type":"Person","name":"' + esc(b.author) + '"}')
    .replace(/\n[ \t]*<link rel="canonical"[\s\S]*?x-default[^>]*>/, '\n' + alt)
    .replace('</head>', TOC_STYLE + (indexCss || '') + '</head>');
}

function bodyTop(b) {
  return TPL.bodyTop
    .replace(/<div class="hdr-logo">[^<]*<\/div>/, '<div class="hdr-logo">' + b.logo + '</div>')
    .replace(/<a href="https:\/\/ragimoff\.org" class="hdr-back"[^>]*>/, '<a href="https://ragimoff.org/" class="hdr-back" title="Ana sayta qayıt">')
    .replace(/<strong>[^<]*<\/strong>/, '<strong>' + esc(b.titlePrinted) + '</strong>')
    .replace(/<small>[^<]*<\/small>/, '<small>' + esc(b.author) + ' · ' + b.year + '</small>')
    .replace('data-lang-switch', 'data-lang-switch data-langs="' + (b.ru ? 'az,ru' : 'az') + '" data-lang-avail="' + (b.ru ? 'az ru' : 'az') + '"')
    .replace('src="/_lang-switch.js"', 'src="/_lang-switch.js?v=' + LSV + '"');
}

function sidebarHtml(list, idx, pre) {
  const items = list.map((c, i) =>
    '<div class="nav-item"><a href="' + pre + c.file + '" class="nav-sub-link' + (i === idx ? ' is-active' : '') + '">' +
    '<span class="sub-code">' + c.num + '</span><span class="sub-name">' + esc(c.short || c.title) + '</span></a></div>').join('\n      ');
  return '<aside class="sidebar" id="sb">\n    <div class="sb-hdr"><a class="sb-site" href="https://ragimoff.org/books/" title="Kitablar">← ' + UI.back + '</a>' +
    '<button class="sb-close" onclick="toggleSb()" aria-label="Bağla">✕</button></div>\n    <nav>\n      ' +
    '<div class="nav-item"><a href="' + pre + 'index.html" class="nav-link nav-front">' + UI.home + '</a></div>\n      ' +
    items + '\n    </nav>\n  </aside>';
}

function chapterPage(b, list, idx) {
  const ch = list[idx];
  const prev = idx > 0 ? list[idx - 1] : null, next = idx < list.length - 1 ? list[idx + 1] : null;
  const content = '\n<nav class="crumb"><a href="index.html">‹ ' + esc(b.title) + '</a></nav>\n' +
    '<h1 class="chap-title-wrap"><span class="chap-title">' + esc(ch.title) + '</span></h1>\n' +
    ch.body.map((p) => p.sub ? '<h3 class="sub">' + esc(p.t) + '</h3>' : '<p>' + esc(p.t) + '</p>').join('\n') + '\n' +
    '<nav class="d-nav">' +
    (prev ? '<a href="' + prev.file + '">← ' + prev.num + ' <span class="dn-name">' + esc(prev.short || prev.title) + '</span></a>' : '<span></span>') +
    '<a class="up" href="index.html">↑ ' + UI.up + '</a>' +
    (next ? '<a href="' + next.file + '"><span class="dn-name">' + esc(next.short || next.title) + '</span> ' + next.num + ' →</a>' : '<span></span>') +
    '</nav>\n' + TPL.tail;
  return headHtml(b, 'https://ragimoff.org/books/' + b.slug + '/' + ch.file, ch.title, b.title + ' — ' + ch.title) + '\n</head>\n' +
    bodyTop(b) + sidebarHtml(list, idx, '') + TPL.mid + TPL.contentOpen + content;
}

function indexPage(b, list) {
  const cards = list.map((c) =>
    '<div class="toc-chapter"><a href="' + c.file + '" class="toc-chapter-title"><span class="toc-name">' + esc(c.title) + '</span></a></div>').join('\n      ');
  const content = '\n<div class="home-hero"><h1 class="home-title"><img src="title-lockup.png" alt="' + esc(b.titlePrinted) + '" style="width:min(520px,86vw);height:auto"></h1>' +
    '<p class="sub">' + esc(b.author) + '</p>' +
    '<p class="sub year">' + esc(b.yearSub || b.year) + '</p></div>\n' +
    '<section class="book-toc"><h2 class="toc-title">' + esc(UI.toc) + '</h2>\n      ' + cards + '\n    </section>\n';
  return headHtml(b, 'https://ragimoff.org/books/' + b.slug + '/', b.title, b.title + ' — ' + b.author, INDEX_STYLE) + '\n</head>\n' +
    bodyTop(b) + sidebarHtml(list, -1, '') + TPL.mid + TPL.contentOpen + content;
}

/* ── сборка одной книги ── */
function buildBook(b) {
  const raw = parasOf(path.join(SRC, b.epub));
  /* индекс главы: последовательный поиск напечатанных заголовков */
  const keyed = raw.map(key);
  let cursor = 0;
  const marks = [];
  b.chapters.forEach((ch, ci) => {
    let found = -1, used = null;
    for (let i = cursor; i < raw.length; i++) {
      const seq = [];
      let j = i, ok = true;
      for (const k of ch.find) {
        while (j < raw.length && !keyed[j]) j++;
        const kk = key(k);
        const hit = j < raw.length && (keyed[j] === kk || (kk.length >= 18 && keyed[j].startsWith(kk)));
        if (!hit) { ok = false; break; }
        seq.push(j); j++;
      }
      if (ok) { found = i; used = seq; break; }
    }
    if (found < 0) throw new Error(b.slug + ': не найден печатный заголовок главы ' + (ci + 1) + ': ' + ch.find.join(' / '));
    marks.push({ start: found, heads: used, end: used[used.length - 1] + 1, at: raw[found] });
    cursor = found + 1;
  });
  const list = [];
  b.chapters.forEach((ch, ci) => {
    const from = marks[ci].end;
    const to = ci + 1 < marks.length ? marks[ci + 1].start : raw.length;
    /* если напечатанный заголовок склеен в источнике с первой строкой (приветствие
       письма, подзаголовок) — остаток строки остаётся в тексте главы */
    const headFull = raw[marks[ci].heads[marks[ci].heads.length - 1]];
    const lastKey = ch.find[ch.find.length - 1];
    const at = foldKeep(headFull).indexOf(foldKeep(lastKey));
    let tailLine = '';
    if (at >= 0) {
      const rest = headFull.slice(at + lastKey.length).replace(/^[\s:.,;–—-]+/, '').trim();
      if (rest.length > 2) tailLine = rest;
    }
    let paras = (tailLine ? [tailLine] : []).concat(raw.slice(from, to).filter((t) =>
      !JUNK.some((re) => re.test(t)) && !runHead(t, b.title) && t.replace(/\s+/g, '').length > 1));
    /* концевой блок нумерованных примечаний переводчика/издателя — не текст Фрейда */
    let tail = paras.length;
    while (tail > 0 && NOTE_TAIL.test(paras[tail - 1])) tail--;
    if (paras.length - tail >= 3) paras = paras.slice(0, tail);
    /* заголовок главы печатается как <h1> страницы — из тела убираем */
    const num = String(ci + 1).padStart(2, '0');
    if (paras.length < 2) throw new Error(b.slug + ': глава «' + ch.title + '» пустая (' + paras.length + ' абз.) — публиковать нельзя');
    const base = key(ch.title).replace(/^(i|ii|iii)\s+/, '').slice(0, 40)
      .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    list.push({ ...ch, num, file: num + '-' + base + '.html', body: joinBroken(paras), pages: to - from, at: marks[ci].at });
  });
  const dir = path.join(ROOT, 'books', b.slug);
  fs.mkdirSync(dir, { recursive: true });
  const style = path.join(ROOT, 'klinik-psixiatriya', 'style.css');
  if (fs.existsSync(style)) fs.copyFileSync(style, path.join(dir, 'style.css'));
  const lock = path.join(ROOT, '_tools', 'title-lockups', b.slug + '.png');
  if (fs.existsSync(lock)) fs.copyFileSync(lock, path.join(dir, 'title-lockup.png'));
  /* старые главы (от прежней эвристики) — удалить, чтобы не осталось мусора */
  const keep = new Set(list.map((c) => c.file).concat('index.html'));
  fs.readdirSync(dir).filter((f) => /^\d{2}-.*\.html$/.test(f) && !keep.has(f)).forEach((f) => fs.unlinkSync(path.join(dir, f)));
  list.forEach((ch, i) => fs.writeFileSync(path.join(dir, ch.file), chapterPage(b, list, i), 'utf8'));
  fs.writeFileSync(path.join(dir, 'index.html'), indexPage(b, list), 'utf8');
  return list;
}


/* «Yeni mühazirələr» (1933) — НАШ перевод с немецкого (1-е издание IPV, Wien 1933),
   продолжение «Psixoanalizlə ilkin tanışlıq» (лекции XXIX–XXXV). EPUB собран нами, обложка — Wan 2.7. */
BOOKS.push({
  slug: 'freud-yeni-muhazireler', logo: 'YM', epub: 'Yeni mühazirələr.epub',
  title: 'Yeni mühazirələr', titlePrinted: 'YENİ MÜHAZİRƏLƏR',
  author: 'Ziqmund Freyd', year: '1933', yearSub: 'İlk nəşr — 1933', ru: false, prefix: 'yeni',
  chapters: [
    { title: 'Ön söz', find: ['Ön söz'], pdfPage: 5 },
    { title: 'İyirmi doqquzuncu mühazirə. YUXU NƏZƏRİYYƏSİNƏ YENİDƏN BAXIŞ', find: ['İyirmi doqquzuncu mühazirə. YUXU NƏZƏRİYYƏSİNƏ YENİDƏN BAXIŞ'], pdfPage: 9 },
    { title: 'Otuzuncu mühazirə. YUXU VƏ OKKULTİZM', find: ['Otuzuncu mühazirə. YUXU VƏ OKKULTİZM'], pdfPage: 25 },
    { title: 'Otuz birinci mühazirə. PSİXİ ŞƏXSİYYƏTİN PARÇALANMASI', find: ['Otuz birinci mühazirə. PSİXİ ŞƏXSİYYƏTİN PARÇALANMASI'], pdfPage: 41 },
    { title: 'Otuz ikinci mühazirə. QORXU VƏ İNSTİNKT HƏYATI', find: ['Otuz ikinci mühazirə. QORXU VƏ İNSTİNKT HƏYATI'], pdfPage: 57 },
    { title: 'Otuz üçüncü mühazirə. QADINLIQ', find: ['Otuz üçüncü mühazirə. QADINLIQ'], pdfPage: 73 },
    { title: 'Otuz dördüncü mühazirə. İZAHLAR, TƏTBİQLƏR, ORİYENTASİYALAR', find: ['Otuz dördüncü mühazirə. İZAHLAR, TƏTBİQLƏR, ORİYENTASİYALAR'], pdfPage: 89 },
    { title: 'Otuz beşinci mühazirə. DÜNYAGÖRÜŞÜ HAQQINDA', find: ['Otuz beşinci mühazirə. DÜNYAGÖRÜŞÜ HAQQINDA'], pdfPage: 105 },
  ],
});

const only = process.argv[2];
let n = 0;
BOOKS.forEach((b) => {
  if (only && b.slug !== only) return;
  const list = buildBook(b);
  n += list.length + 1;
  console.log(b.slug + ': глав ' + list.length + ' → books/' + b.slug + '/');
  list.forEach((c) => console.log('    ' + c.num + '  ' + c.file +
    '\n         на сайте: ' + c.title + '\n         в EPUB:    ' + c.at + '   [стр. PDF ' + c.pdfPage + ']'));
});
console.log('всего страниц:', n);
