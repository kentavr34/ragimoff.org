# TYPOGRAPHY.md — Правила вёрстки книги «Klinik Psixiatriya»

> **AI-агенты: читайте ПЕРЕД любой правкой вёрстки.** Все правила и эталон — здесь.
> Эталон стиля: **МКБ-11, русское издание, 2-е, 2022** (138×228 мм, ВОЗ + РОП).
> Локальный референс PDF: `_supplements/ICD-11_RU_2022_reference.pdf`.

## 0a. Цвет текста — ОБЯЗАТЕЛЬНО ЧЁРНЫЙ

**Весь текст в книге — `#000000` (чистый чёрный).** Никакого синего/голубого/blue (`#4F81BD`, `#0563C1` и пр.), никаких тематических акцентов Office, никаких подсветок ссылок.

Применяется к:
- Всем уровням заголовков (Heading 1–9) — `RGBColor(0, 0, 0)`
- Стилю `Hyperlink` — `#000000`, без подчёркивания (выглядит как обычный текст)
- Inline-run-ам внутри параграфов и таблиц — после сборки делается финальный проход по `<w:color>`, всё переопределяется на `000000`
- HTML/CSS сайта (`klinik-psixiatriya/style.css`) — `var(--gold)` отменяется для текста, остаётся только в декоративных элементах (border, icd-фон)

**Исключение:** только серый `#555555` для второстепенных подписей на титульном листе (под-слоган, год+город). Этот единственный grey сохраняется проходом-исключением в `fix_docx()`.

> Это правило закреплено в правиле автомата (см. `fix_docx()` секция 6): после всех манипуляций производится сметающий проход по `<w:color>` элементам — любой цвет → `000000` (кроме `555555`).

## 0. Эталонный источник стиля

**ICD-11 / МКБ-11, русское издание** (Глава 06: Психические и поведенческие расстройства, 2-е изд. 2022, изд. «КДУ»/«Университетская книга»). Формат **138×228 мм**, сверстано в Adobe InDesign. Дизайн и вёрстка: О.Н. Бугаёва, А.А. Анисимов.

Что заимствуем:
- Иерархия заголовков (титул → глава → блок → расстройство → подкод)
- Структуру титульного листа (название сверху, выходные данные на отдельной стр.)
- Формат TOC (имя главы + лидер + номер страницы)
- Колонтитулы (левая стр. — источник/глава, правая — название книги, наружный номер)
- Чистую правую полосу для начала каждой главы

Что **НЕ** заимствуем:
- Шрифт (МКБ-11 использует Calibri/Arial sans-serif) — **наш шрифт Times New Roman** (профессиональный медицинский учебник)
- Формат страницы — у нас A4 (более универсально для печати/PDF в Бакы)

## 1. Титульный лист

**Одна страница, без лишнего.**

| Позиция | Содержание | Стиль |
|---|---|---|
| ~25% сверху, по центру | `ICD-11 · DSM-5-TR` (мелкая атрибуция, серый) | 11pt, грей |
| ~30% сверху | `KLİNİK PSİXİATRİYA` (название книги) | 44pt, **bold**, по центру |
| Сразу под | `Diaqnostika və terapiya standartları` (слоган) | 18pt, italic, по центру |
| Сразу под | `XBT-11 və DSM-5-TR əsasında klinik bələdçi` (под-слоган) | 14pt, italic, серый |
| ~80% сверху | пустая зона | — |
| Снизу по центру | `Dr. Kənan Rəhimov` | 14pt, **bold** |
| Под ним | `Bakı · 2026` | 12pt, серый |

**Запрещено:** автогенерируемый pandoc title block с Title/Subtitle/Author/Date в столбик. Используется ручная вёрстка через `build_title_page_xml()`.

## 2. Иерархия заголовков (TYPOGRAPHY proportions, professional textbook)

| Уровень | Размер | Жирность | Выравн. | Сlassname в HTML | Где используется |
|---|---|---|---|---|---|
| Heading 1 | **28pt** | Bold | Center | `<h1>` (после shift_levels) | Глава: `NEYROİNKİŞAF POZUNTULARI` |
| Heading 2 | **20pt** | Bold | Left | `<h1 class="h-disorder">` | Расстройство: `6A00 İNTELLEKTUAL …` |
| Heading 3 | **14pt** | Bold | Left | `<h2>` | Раздел: `1. Tərif`, `6. Diaqnoz` |
| Heading 4 | **12pt** | Bold | Left | `<h3>` | Под-раздел: `6.1 Vahid meyarlar` |
| Heading 5 | **11pt** | Bold-italic | Left | `<h4>` | Миф: `Mif 1: "…"` |
| Body | 11pt | Regular | Justify | `<p>` | Основной текст |

**Правило монотонного убывания:** каждый следующий уровень меньше или равен предыдущему, и никогда не жирнее. Подразделы крупнее или жирнее родителя — **запрещено**.

## 3. Page-break-before

**Можно (всегда):**
- Heading 1 (новая глава) — на новой странице
- Heading 2, если текст начинается с ICD-кода (`^[0-9][A-Z][0-9][0-9A-Z]?\b` или `^HA[0-9]{2}\b`) — новое расстройство

**Нельзя:**
- Любые подразделы (Heading 3/4/5) — flow внутри расстройства
- Heading 2 интро-главы (`Bu bölmənin tərkibi`, `Konseptual yenilik`)
- Параграфы, таблицы, мифы, списки

**Первый заголовок книги** — page-break снимается, чтобы не было пустой первой страницы.

## 4. Body text — пропорции профессионального учебника

- **Шрифт:** Times New Roman 11pt
- **Межстрочное:** 1.25 (≈14pt)
- **Абзац:** отступ первой строки **0.5 см** (русско-академический стиль) — кроме первого абзаца после заголовка
- **Выравнивание:** по ширине (justify)
- **`space_before` / `space_after`** для Normal: 0pt / 4pt
- Расстояние между параграфом и заголовком: фиксируется через `space_before` заголовка (12pt)

## 5. TOC — оглавление

- Заголовок: `MÜNDƏRİCAT` (28pt, bold, centered) — отдельная страница после титула
- Глубина: 2 (главы + расстройства). Подразделы расстройств **не** включаются
- Pandoc-генерация: `--toc --toc-depth=2 --metadata=toc-title:MÜNDƏRİCAT`
- Между названием главы и номером страницы — точечный лидер (`....`), автогенерируется pandoc
- Расстройства (Heading 2) — с одним уровнем отступа от глав

## 6. Колонтитулы (header/footer)

| Сторона | Содержание |
|---|---|
| Чётная (левая) | Название главы текущей секции |
| Нечётная (правая) | `KLİNİK PSİXİATRİYA · Diaqnostika və terapiya standartları` |
| Снизу | Номер страницы (наружный угол: лев. — слева, прав. — справа) |

Реализация: `section.header_distance` + `section.footer_distance` в python-docx.

## 7. Терминология

Академический азербайджанский, медицинский регистр.

| Запрещено | Используем |
|---|---|
| Klinik mənzərə | Klinik təzahürlər |
| çek-list | meyarlar |
| baseline | ilkin göstəricilər |
| Anorexia Nervosa | Anoreksiya Nervoza |
| Bulimia Nervosa | Bulimiya Nervoza |
| Binge-Eating | Keçirtmə ilə yemə |
| Hipoxondria | Hipoxondriya |
| (HOARDING / CONDUCT / VASCULAR DEMENTIA / BODILY DISTRESS) | выкинуть скобку, оставить азерб. термин |
| xəstə | pasiyent |
| ruhi | psixi |
| üsulları | metodları |

Чистка автоматически через `_fix_terminology3.py`.

## 8. Источники (whitelist)

NICE · APA · WFSBP · Cochrane · DSM-5-TR · XBT-11 (ICD-11) · AAP · AACAP · FDA · CANMAT · NIMH · ISSTD · ICCS · WPATH · VA-DoD · SAMHSA · AASM · AUA · EAU · ISSWSH · ISSM.

## 9. Düzəliş et widget (HTML)

На каждой HTML-странице книги. Маркер `<!-- DUZELIS-WIDGET -->` + `duzelis.css` + `duzelis.js`. FAB-кнопка фикс. справа-снизу (z-index 9990). Инжектор: `_inject_duzelis.py`.

## 10. Скрипты сборки

| Скрипт | Назначение |
|---|---|
| `_inject_chapters_v2.py` | Влить chapters-v2 фрагменты в 23 главы |
| `_rebuild_book_nav.py` | Перегенерировать sidebar + TOC сайта |
| `_inject_abbr.py` | `<abbr title>` tooltips |
| `_inject_duzelis.py` | Виджет «Düzəliş et» |
| `_fix_terminology3.py` | Чистка англ./лат. терминов |
| `build_book.py` | DOCX (pandoc + python-docx + manual title page + ICD-11 styling) |

Перезапуск в этом порядке после изменения контента.

## 11. Проверка после сборки

```python
from docx import Document
from docx.oxml.ns import qn
import re
doc = Document('klinik-psixiatriya/KLINIK_PSIXIATRIYA_*.docx')
ICD = re.compile(r'^\s*([0-9][A-Z][0-9][0-9A-Z]?|HA[0-9]{2})\b')
intro_h2_pbb = sum(
    1 for p in doc.element.body.findall(qn('w:p'))
    if (pPr := p.find(qn('w:pPr'))) is not None
    and (s := pPr.find(qn('w:pStyle'))) is not None
    and 'Heading 2' in (s.get(qn('w:val')) or '')
    and pPr.find(qn('w:pageBreakBefore')) is not None
    and not ICD.match(''.join(t.text or '' for t in p.iter(qn('w:t'))))
)
assert intro_h2_pbb == 0, f"non-ICD H2 has page break: {intro_h2_pbb}"
```
