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
    ],
  },
];

/* Sevgi məktubları: главы — письма, заголовок = напечатанная строка даты */
const LETTERS = [
  ['Vyana, 10 iyun 1882-ci il', 'Vyana, 10 iyun 1882-ci il', 3],
  ['Vyana, ikinci gün, 27 iyun 1882-ci il', 'Vyana, 27 iyun 1882-ci il', 5],
  ['Hamburq, bazar günü, 23 iyul 1882-ci il.', 'Hamburq, 23 iyul 1882-ci il', 8],
  ['Vyana, 18 avqust 1882-ci il, gecə', 'Vyana, 18 avqust 1882-ci il', 13],
  ['Vyana, 25 sentyabr 1882-ci il', 'Vyana, 25 sentyabr 1882-ci il', 16],
  ['Vyana, bazar günü, 16 sentyabr 1883-cü il', 'Vyana, 16 sentyabr 1883-cü il', 23],
  ['Vyana, ikinci gün, 9 oktyabr 1883-cü il, gecə', 'Vyana, 9 oktyabr 1883-cü il', 31],
  ['Vyana, ikinci gün, 23 oktyabr 1883-cü il', 'Vyana, 23 oktyabr 1883-cü il', 32],
  ['Vyana, 15 noyabr, 1883-cü il, dördüncü gün, axşamüstü saat beşdə', 'Vyana, 15 noyabr 1883-cü il', 34],
  ['Vyana, dördüncü gün, 10 yanvar 1884-cü il', 'Vyana, 10 yanvar 1884-cü il', 36],
  ['Vyana, ikinci gün, 7 fevral 1884-cü il', 'Vyana, 7 fevral 1884-cü il', 39],
  ['Vyana, ikinci gün, 19 iyun 1884-cü il', 'Vyana, 19 iyun 1884-cü il', 42],
  ['Vyana, bazar ertəsi, 30 iyun 1884-cü il', 'Vyana, 30 iyun 1884-cü il', 44],
  ['Vyana, 16 yanvar 1885-ci il', 'Vyana, 16 yanvar 1885-ci il', 46],
  ['Vyana, dördüncü gün, 7 may 1885-ci il', 'Vyana, 7 may 1885-ci il', 48],
  ['Vyana, şənbə günü, 6 iyun 1885-ci il', 'Vyana, 6 iyun 1885-ci il', 48],
  ['Vyana, şənbə günü, 20 iyun 1885-ci il, axşam', 'Vyana, 20 iyun 1885-ci il', 50],
  ['Paris, 20 yanvar 1986-cı il', 'Paris, 20 yanvar 1886-cı il', 51],
  ['Paris, ikinci gün, 2 fevral 1886-cı il', 'Paris, 2 fevral 1886-cı il', 54],
  ['3 fevral 1886-cı il, gecə saat birin yarısı', '3 fevral 1886-cı il', 57],
  ['Berlin, beşinci gün, 19 mart 1886-cı il', 'Berlin, 19 mart 1886-cı il', 58],
  ['Vyana, ikinci gün, 6 may 1886-cı il', 'Vyana, 6 may 1886-cı il', 61],
  ['Vyana, 13 may 1886-cı il', 'Vyana, 13 may 1886-cı il', 62],
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
  const content = '\n<div class="home-hero"><h1 class="home-title">' + esc(b.titlePrinted) + '</h1>' +
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
  /* старые главы (от прежней эвристики) — удалить, чтобы не осталось мусора */
  const keep = new Set(list.map((c) => c.file).concat('index.html'));
  fs.readdirSync(dir).filter((f) => /^\d{2}-.*\.html$/.test(f) && !keep.has(f)).forEach((f) => fs.unlinkSync(path.join(dir, f)));
  list.forEach((ch, i) => fs.writeFileSync(path.join(dir, ch.file), chapterPage(b, list, i), 'utf8'));
  fs.writeFileSync(path.join(dir, 'index.html'), indexPage(b, list), 'utf8');
  return list;
}

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
