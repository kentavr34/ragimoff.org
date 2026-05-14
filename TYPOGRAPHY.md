# TYPOGRAPHY.md — Правила вёрстки книги «Klinik Psixiatriya»

> **AI-агенты: читайте ПЕРЕД любой правкой вёрстки.** Все правила и эталон — здесь.
> Эталон стиля: **МКБ-11, русское издание, 2-е, 2022** (138×228 мм, ВОЗ + РОП).
> Локальный референс PDF: `_supplements/ICD-11_RU_2022_reference.pdf`.

## 0b. Verified disorder name list (WHO ICD-11 2024 + АзПА + 994 grammar bible)

**После любых правок проверять каждое название по этой таблице. Не отступать.**

| ICD | AZ название (canonical) | RU reference (МКБ-11 РФ 2022) |
|---|---|---|
| 6A00 | İNTELLEKTUAL İNKİŞAF POZUNTUSU | Нарушения интеллектуального развития |
| 6A01 | İNKİŞAF NİTQ VƏ DİL POZUNTULARI | Нарушения речевого развития |
| 6A02 | AUTİZM SPEKTRİ POZUNTUSU (ASP) | Расстройство аутистического спектра |
| 6A03 | SPESİFİK ÖYRƏNMƏ POZUNTUSU | Нарушение развития учебных навыков |
| 6A04 | İNKİŞAF HƏRƏKİ KOORDİNASİYA POZUNTUSU (DCD) | Нарушение развития координации движений |
| 6A05 | DİQQƏT DEFİSİTİ VƏ HİPERAKTİVLİK POZUNTUSU (DDHP) | Синдром дефицита внимания с гиперактивностью |
| 6A06 | STEREOTİPİK HƏRƏKƏT POZUNTUSU | Расстройство стереотипных движений |
| 6A07 | TİKLİ POZUNTULAR (TOURETTE SİNDROMU) | Тиковые расстройства |
| 6A20 | ŞİZOFRENİYA | Шизофрения |
| 6A21 | ŞİZOAFFEKTİV POZUNTU | Шизоаффективное расстройство |
| 6A22 | ŞİZOTİPİK POZUNTU | Шизотипическое расстройство |
| 6A23 | KƏSKİN VƏ KEÇİCİ PSİXOTİK POZUNTU | Острое транзиторное психотическое расстройство |
| 6A24 | SAYIQLAMA POZUNTUSU | Бредовое расстройство |
| 6A25 | İLKİN PSİXOTİK POZUNTULARIN SİMPTOM DOMENLƏRİ | Симптоматические проявления |
| 6A40 | KATATONİYA — ÜMUMİ PRİNSİPLƏR | Кататония |
| 6A60 | BİPOLYAR POZUNTU TİP I | Биполярное расстройство I типа |
| 6A61 | BİPOLYAR POZUNTU TİP II | Биполярное расстройство II типа |
| 6A62 | SİKLETİMİK POZUNTU | Циклотимическое расстройство |
| 6A70 | TƏK EPİZODLU DEPRESİV POZUNTU | Единичный эпизод депрессивного расстройства |
| 6A71 | TƏKRARLANAN DEPRESİV POZUNTU | Рекуррентное депрессивное расстройство |
| 6A72 | DİSTİMİK POZUNTU | Дистимическое расстройство |
| 6A73 | PREMENSTRUAL DİSFORİK POZUNTU (PMDD) | (зарезервировано) |
| 6B00 | GENERALİZƏ OLUNMUŞ NARAHATLIQ POZUNTUSU (GAD) | Генерализованное тревожное расстройство |
| 6B01 | PANİK POZUNTU | Паническое расстройство |
| 6B02 | AQORAFOBİYA | Агорафобия |
| 6B03 | SPESİFİK FOBİYA | Специфическая фобия |
| 6B04 | SOSİAL NARAHATLIQ POZUNTUSU | Социальное тревожное расстройство |
| 6B05 | AYRILMA NARAHATLIĞI POZUNTUSU | Сепарационное тревожное расстройство |
| 6B06 | SELEKTİV MUTİZM | Селективный мутизм |
| 6B20 | OBSESSİV-KOMPULSİV POZUNTU (OKP) | Обсессивно-компульсивное расстройство |
| 6B21 | BƏDƏN DİSMORFİK POZUNTUSU (BDD) | Дисморфическое расстройство |
| 6B22 | PATOLOJİ BƏDƏN QOXUSU POZUNTUSU (ORS) | Патологическая озабоченность собственным запахом |
| 6B23 | HİPOXONDRİYA | Ипохондрия |
| 6B24 | TOPLAMA POZUNTUSU | Патологическое накопительство |
| 6B25 | BƏDƏNƏ YÖNƏLMİŞ TƏKRAR DAVRANIŞLAR | Патологические телесно направленные повторяющиеся действия |
| **6B40** | POSTTRAVMATİK STRES POZUNTUSU (PTSP) | Посттравматическое стрессовое расстройство |
| **6B41** | KOMPLEKS POSTTRAVMATİK STRES POZUNTUSU (cPTSP) | Осложненное ПТСР |
| **6B42** | UZANMIŞ YAS POZUNTUSU | Затяжная патологическая реакция горя |
| **6B43** | ADAPTASİYA POZUNTUSU | Расстройство адаптации |
| 6B44 | REAKTİV BAĞLANMA POZUNTUSU | Реактивное расстройство привязанности |
| 6B45 | SOSİAL İŞTİRAKIN MƏHDUDLAŞDIRILMASI POZUNTUSU | Расстройство социализации по расторможенному типу |
| 6B60 | DİSSOSİATİV İDENTİFİKASİYA POZUNTUSU (DİP) | Диссоциативное расстройство идентичности |
| 6B61 | PARSİAL DİSSOSİATİV İDENTİFİKASİYA POZUNTUSU | Парциальное диссоциативное |
| 6B62 | DEPERSONALİZASİYA-DEREALİZASİYA POZUNTUSU | Расстройство деперсонализации-дереализации |
| 6B63 | DİSSOSİATİV NEVROLOJİ SİMPTOM POZUNTUSU | Диссоциативное расстройство с неврологическими симптомами |
| 6B64 | DİSSOSİATİV AMNEZİYA | Диссоциативная амнезия |
| **6B80** | SİNİR ANOREKSİYASI | Нервная анорексия |
| **6B81** | SİNİR BULİMİYASI | Нервная булимия |
| 6B82 | KEÇİRTMƏ İLƏ YEMƏ POZUNTUSU (BED) | Патологическое переедание |
| 6B83 | PİKA | Пика |
| 6B84 | RUMİNASİYA-GERİ QAYTARMA POZUNTUSU | Патологическое пережёвывание и срыгивание |
| 6B85 | QAÇINMA/MƏHDUDLAŞDIRICI QİDA QƏBULU POZUNTUSU (ARFID) | Патологическое избирательно-ограничительное |
| 6C00 | ENUREZ | Энурез |
| 6C01 | ENKOPREZ | Энкопрез |
| **6C20** | BƏDƏN DİSSTRES POZUNTUSU | Телесный дистресс |
| 6C40 | ALKOHOL İSTİFADƏSİ POZUNTULARI | Расстройства вследствие употребления алкоголя |
| 6C41 | OPİOİD İSTİFADƏSİ POZUNTULARI | Расстройства вследствие употребления опиоидов |
| 6C42 | KANNABİS İSTİFADƏSİ POZUNTULARI | Расстройства вследствие употребления каннабиса |
| 6C43 | SEDATİV/HİPNOTİK İSTİFADƏSİ POZUNTULARI | Расстройства вследствие употребления седативных/снотворных |
| 6C44 | KOKAİN İSTİFADƏSİ POZUNTULARI | Расстройства вследствие употребления кокаина |
| 6C45 | STİMULYANT İSTİFADƏSİ POZUNTULARI | Расстройства вследствие употребления стимуляторов |
| 6C46 | HALÜSİNOGEN İSTİFADƏSİ POZUNTULARI | Расстройства вследствие употребления галлюциногенов |
| 6C47 | NİKOTİN İSTİFADƏSİ POZUNTULARI | Расстройства вследствие употребления никотина |
| 6C50 | DAVRANIŞ ASILILIQLARI (QUMAR, OYUN) | Расстройство вследствие пристрастия (азартные игры и т.п.) |
| 6C70 | PYROMANİYA | Пиромания |
| 6C71 | KLEPTOMANİYA | Клептомания |
| 6C72 | KOMPULSİV CİNSİ DAVRANIŞ POZUNTUSU | Компульсивное расстройство сексуального поведения |
| 6C73 | ARALIQLI PATLAYICI POZUNTU (IED) | Периодическое эксплозивное расстройство |
| 6C90 | DAVRANIŞ POZUNTUSU | Расстройство поведения |
| **6C91** | MÜXALİF-İNADKAR POZUNTU (ODD) | Оппозиционно-вызывающее расстройство |
| 6D10 | ŞƏXSİYYƏT POZUNTUSU (XBT-11 VAHİD MODELİ) | Расстройство личности |
| 6D11 | ŞƏXSİYYƏT ÇƏTİNLİYİ | Выраженные личностные черты |
| 6D30 | EKSHİBİSİONİZM | Патологический эксгибиционизм |
| 6D31 | VOYERİZM | Патологический вуайеризм |
| 6D32 | PEDOFİLİK POZUNTU | Педофилическое расстройство |
| 6D33 | SADİSTİK CİNSİ POZUNTU | Патологический сексуальный садизм |
| 6D34 | FROTTEURİZM | Патологический фроттеризм |
| 6D50 | ÖZÜNƏ TƏTBİQ EDİLMİŞ FAKTİTİOZ POZUNTU (MÜNXAUZEN) | Имитированное расстройство в отношении себя |
| 6D51 | BAŞQASINA TƏTBİQ EDİLMİŞ FAKTİTİOZ POZUNTU | Имитированное расстройство в отношении другого |
| 6D70 | DELİRİUM | Делирий |
| 6D71 | YÜNGÜL NEYROKOQNİTİV POZUNTU (MCI) | Лёгкое нейрокогнитивное расстройство |
| 6D72 | AMNESTİK POZUNTU | Амнестическое расстройство |
| 6D80 | ALZHEİMER XƏSTƏLİYİNƏ GÖRƏ DEMENSİYA | Деменция вследствие болезни Альцгеймера |
| 6D81 | DAMAR DEMENSİYASI | Деменция вследствие цереброваскулярного заболевания |
| 6D82 | LEWY CİSİMCİKLƏRİ DEMENSİYASI (DLB) | Деменция с тельцами Леви |
| 6D83 | FRONTOTEMPORAL DEMENSİYA (FTD) | Лобно-височная деменция |
| 6E20 | POSTNATAL DEPRESSİYA | Послеродовая депрессия |
| 6E21 | POSTNATAL PSİXOZ | Послеродовый психоз |
| 6E40 | DİGƏR XƏSTƏLİKLƏRƏ TƏSİR EDƏN PSİXOLOJİ AMİLLƏR | Психологические/поведенческие факторы |
| 6E60 | İKİNCİLİ PSİXOTİK SİNDROM | Вторичный психотический синдром |
| 6E61 | İKİNCİLİ AFFEKTİV SİNDROM | Вторичный аффективный синдром |
| 6E62 | İKİNCİLİ NARAHATLIQ SİNDROMU | Вторичный тревожный синдром |
| 7A00 | İNSOMNİYA | Бессонница |
| 7A20 | OBSTRUKTİV YUXU APNESİ (OSA) | Обструктивное апноэ сна |
| 7A40 | SİRKADİAN RİTM YUXU-OYANMA POZUNTULARI | Расстройства циркадного ритма сна |
| 7A60 | HİPERSOMNİYA | Гиперсомния |
| 7A80 | NARKOLEPSİYA | Нарколепсия |
| HA00 | EREKTİL DİSFUNKSİYA (ED) | Эректильная дисфункция |
| **HA01** | ERKƏN EYAKULYASİYA (PE) | Преждевременная эякуляция |
| HA02 | HİPOAKTİV CİNSİ İSTƏK POZUNTUSU (HSDD) | Гипоактивное расстройство сексуального желания |
| HA03 | ANORGASMİYA | Аноргазмия |
| HA04 | GENİTO-PELVİK AĞRI / PENETRASİYA POZUNTUSU (VAGİNİSMUS) | Расстройство генитально-тазовой боли при проникновении |
| HA05 | DİGƏR XƏSTƏLİK VƏ POZUNTU İLƏ ƏLAQƏLİ CİNSİ DİSFUNKSİYALAR | Другие сексуальные дисфункции |

**Жирным выделено** — то, что было исправлено в раундах 1-5. Не возвращать к старым формам.

### Принципы перевода (закреплены навсегда, не переспрашивать)

1. **Латинизмы оставлять** (per 994 az.md §«Заимствования»): şizofreniya, bipolyar, paranoya, depressiya, katatoniya, narkolepsiya, kleptomaniya и т.п. — это профессиональная лексика.
2. **Транслитерации с английского НЕ ОСТАВЛЯТЬ**: `binge`, `follow-up`, `screening`, `compliance`, `defiant`, `disinhibe`, `premature`, `kültür` — переводить в азерб.
3. **Кальки русских/тюркских идиом не давать** (per 994 az.md §«Калька-чек»).
4. **ICD-11 коды проверять против WHO Browser** (https://icd.who.int/browse/2024-01/mms/en) — у нашего МКБ-11 РФ PDF могут быть устаревшие версии.
5. **Грамматические правила** см. 994 grammar bible: `C:\Users\SAM\Desktop\994\grammar_bibles\az.md`.
6. **При сомнении** в термине — обращаться к 994 translator-системе (production-сервер `94.156.35.89`, через jump host `185.203.116.131`).

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
