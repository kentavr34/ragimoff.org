# TYPOGRAPHY.md — Правила вёрстки для книги «Klinik Psixiatriya»

> **AI-агенты: читайте этот файл ПЕРЕД любой правкой DOCX или HTML-вёрстки книги.** Не спрашивайте автора повторно — все правила здесь.

## Применяется к
- DOCX (`klinik-psixiatriya/KLINIK_PSIXIATRIYA_*.docx`)
- HTML-главам сайта (`klinik-psixiatriya/NN-*.html`)
- Книжному index/TOC (`klinik-psixiatriya/index.html`)

## 1. Титульный лист (DOCX)

**Только это, ничего лишнего:**
- **Сверху по центру (большим шрифтом):** название книги — `KLİNİK PSİXİATRİYA`
- **Под ним (средним шрифтом):** слоган/подзаголовок — `Diaqnostika və terapiya standartları` либо `XBT-11 və DSM-5-TR əsasında klinik bələdçi`
- **Внизу страницы по центру (или прижато справа):** автор, город, год — `Dr. Kənan Rəhimov · Bakı · 2026`

Никакой автоматической pandoc-страницы с большим Title + Subtitle + Author + Date в столбик. Это **единый блок** — название/слоган сверху, выходные данные снизу.

## 2. Иерархия заголовков (DOCX)

**Heading 1 (название главы) — самый крупный, самый жирный.** Пример: `NEYROİNKİŞAF POZUNTULARI`.

```
Heading 1   28pt   Bold   centered   colour: black or var(--gold)
Heading 2   20pt   Bold   left       (disorder title с ICD-кодом)
Heading 3   14pt   Bold   left       (раздел внутри расстройства: Tərif, Tarixçə …)
Heading 4   12pt   Bold   left       (под-раздел: 6.1 Vahid meyarlar и т.д.)
Heading 5   11pt   Bold-italic        (Mif N: «…»)
Normal/Body 11pt   regular
```

**Запрещено:** подразделы крупнее или жирнее, чем родительский заголовок.

## 3. Разрывы страниц (page-break-before)

**Можно начинать с новой страницы:**
- **Главу** (Heading 1)
- **Расстройство** (Heading 2, заголовок которого начинается с ICD-кода: `6A00`, `HA00`, и т.д.)

**Нельзя начинать с новой страницы:**
- Подразделы расстройства (Tərif, Diaqnoz, Müalicə …)
- Под-подразделы (6.1, 6.2 …)
- Параграфы, мифы, таблицы

Пустоты сверху/снизу текста — не более 12pt (0.42 см). Никаких 24pt+ отступов между подразделами.

## 4. Оглавление (TOC)

- На отдельной странице сразу после титульного листа.
- Заголовок: `MÜNDƏRİCAT` (16pt, bold, по центру).
- Уровень глубины: 2 (главы + расстройства). Под-разделы расстройств в TOC не выводить.
- Pandoc генерирует автоматически — `--toc --toc-depth=2`.

## 5. Сайтовая HTML-вёрстка

CSS уже настроен (`klinik-psixiatriya/style.css`):
- `section.disorder h1.h-disorder` — 26px, bold, золотой
- `section.disorder h2` — 19px
- `section.disorder h3` — 16px
- `section.disorder h4` (мифы) — 15px, золотой

Если правишь — сохраняй понижение размера на каждом уровне.

## 6. Терминология (язык)

Академический азербайджанский, медицинский регистр. Все английские/латинские термины в заголовках расстройств — **только** в азербайджанской транскрипции:

| Запрещено | Используем |
|---|---|
| Klinik mənzərə | Klinik təzahürlər |
| çek-list | meyarlar |
| baseline | ilkin göstəricilər |
| Anorexia Nervosa | Anoreksiya Nervoza |
| Bulimia Nervosa | Bulimiya Nervoza |
| Binge-Eating | Keçirtmə ilə yemə |
| Hipoxondria | Hipoxondriya |
| (HOARDING DISORDER) | (выкинуть скобку) |
| (CONDUCT DISORDER) | (выкинуть скобку) |
| (VASCULAR DEMENTIA) | (выкинуть скобку) |
| (BODILY DISTRESS) | Bədənsəl disstres |
| xəstə | pasiyent |
| ruhi | psixi |
| üsulları | metodları |

## 7. Источники (whitelist)

Только: NICE · APA · WFSBP · Cochrane · DSM-5-TR · XBT-11 (ICD-11) · AAP · AACAP · FDA · CANMAT · NIMH · ISSTD · ICCS · WPATH · VA-DoD · SAMHSA · AASM · AUA · EAU · ISSWSH · ISSM.

## 8. Düzəliş et widget

На каждой HTML-странице книги должна быть «Düzəliş et» FAB-кнопка (право-низ, z-index 9990). Подключается через `<!-- DUZELIS-WIDGET -->` маркер + `duzelis.css` + `duzelis.js`.

Скрипт-инжектор: `_inject_duzelis.py`.

## 9. Скрипты сборки

| Скрипт | Назначение |
|---|---|
| `_inject_chapters_v2.py` | Влить chapters-v2 фрагменты в 23 главы |
| `_rebuild_book_nav.py` | Перегенерировать sidebar + TOC |
| `_inject_abbr.py` | `<abbr title>` tooltips для аббревиатур |
| `_inject_duzelis.py` | Виджет «Düzəliş et» |
| `_fix_terminology3.py` | Чистка англ./лат. терминов |
| `build_book.py` | Сборка DOCX (pandoc + python-docx) |

Перезапускать в этом порядке после правок контента.
