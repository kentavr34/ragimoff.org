# ragimoff.org — Working Notes & Session Progress

**Working directory:** `D:\Документы\ragimoff` (ветка `main`)
**Active branch (worktree):** `claude/stupefied-cori-5b6e4a`
**Worktree path:** `C:\Users\SAM\Desktop\sayt2\.claude\worktrees\stupefied-cori-5b6e4a`
**Remote:** `https://github.com/kentavr34/ragimoff.org.git`

> **For future Claude sessions:** Always treat `C:\Users\SAM\Desktop\sayt2` as the working directory. Read this file first to recover context. Update this file at the end of each session.

---

## Owner

Dr. Kənan Rəhimov — Klinik Psixiatriya textbook ("Klinik Psixiatriya") in Azerbaijani, published both as a website (`ragimoff.org/klinik-psixiatriya/`) and a DOCX book.

## Language & Terminology Conventions

Academic Azerbaijani medical register. Use:
- **Klinik təzahürlər** (not *mənzərə*)
- **Vahid diaqnostik meyarlar** (not *çek-list*)
- **İnstrumental müayinələr** (not *Alət*)
- **pasiyent** (not *xəstə*)
- **psixi pozuntu** (not *ruhi*)
- **metodları** (not *üsulları*)
- **təfəkkür**, **şüur**

## Approved Source Whitelist

Only these authoritative sources may be cited:
NICE · APA · WFSBP · Cochrane · DSM-5-TR · XBT-11 (ICD-11) · AAP · AACAP · FDA · EMA · CANMAT · NIMH · ISSTD · ICCS · WPATH · VA-DoD · SAMHSA · AASM · AUA · EAU · ISSWSH · ISSM · ACOG · USPSTF · RCPsych · AGS (Beers) · ISPMD

---

## Major Completed Work

### chapters-v2 — 103/103 disorders DONE ✅

All chapters in `_supplements/chapters-v2/*.html` use the unified 12-section structure:

1. Tərif və nozologiya
2. Tarixçə
3. Epidemiologiya
4. Etiologiya
5. Klinik təzahürlər
6. Diaqnoz (6.1 Vahid diaqnostik meyarlar [DSM-5-TR · XBT-11] · 6.2 Mənbə-spesifik dəqiqləşdirmələr · 6.3 Diaqnostika alqoritmi · 6.4 Differensial diaqnostika)
7. Müayinə
8. Müalicə (8.1 Ümumi prinsiplər · 8.2 Mənbə-spesifik dəqiqləşdirmələr)
9. Metodikalar
10. Mif və yanlış inanclar (5–6 myths, each: claim → niyə yayılıb → bioloji-klinik məntiq → sübut → real klinik addım)
11. Proqnoz
12. Mənbələr

Progress markers:
- `_supplements/chapters-v2/_progress.md` — table TODO/DONE per ICD code
- `_supplements/chapters-v2/_done.md` — completion summary
- Etalon (template): `_supplements/chapters-v2/6A20.html`

Final batch HA02–HA05 completed on 2026-05-14:
- HA02 Hipoaktiv Cinsi İstək Pozuntusu (HSDD)
- HA03 Anorgasmiya
- HA04 GPPPD / Vaginismus
- HA05 Digər xəstəlik/pozuntu ilə əlaqəli cinsi disfunksiyalar

### Other tooling completed

- Global terminology cleanup (e.g., 254× *mənzərə → təzahürlər*).
- Abbreviation tooltips: 4166 `<abbr title>` wrappings, 130+ term dictionary (`_inject_abbr.py`).
- "Düzəliş et" feedback widget integrated across 52 chapter HTMLs (`klinik-psixiatriya/duzelis.{js,css}`, `duzelis-gas.txt` — Google Apps Script endpoint instructions, `_inject_duzelis.py`).
- DOCX book rebuilder with title page + MÜNDƏRİCAT TOC + page breaks: `build_book.py`.

---

## Known Pending / Next Possible Tasks

(Nothing locked in — propose to user before starting.)

- Regenerate DOCX from finalized chapters-v2 via `build_book.py`.
- Verify that all chapters-v2 HTMLs are wired into the website's chapter pages (not just stored as supplements).
- Optional: shrink `_supplements/chapters-v2/_progress.md` from TODO/DONE table to a simple completion log now that all are DONE.

---

## Workflow Conventions

- **Commits:** create new commits (never amend), push to `claude/stupefied-cori-5b6e4a` after each meaningful batch.
- **Never** commit secrets/large binaries (e.g., the `pandoc-*.msi` mistake from earlier — keep an eye on `git status`).
- **CRLF warnings** in this repo are expected on Windows; do not "fix" them.
- Use `Edit` for in-place changes; `Write` only for new files or full rewrites.
- Never create extra `.md` docs unless the user asks — `PROGRESS.md` (this file) is the single source of session continuity.

---

## Session Log

### 2026-08-12 — kitab-haqqinda и yekun: блок в блок против мастера (H, часть 2)

Две вводные страницы разложены по блокам и сверены с азербайджанским
мастером: 75 блоков в «О книге» и 103 в «Итоговых рекомендациях», по
четыре языка в строку. Так видно не отдельные подозрительные слова, а
места, где перевод потерял грамматику предложения.

**Мастер оказался чистым везде, кроме одного места.** В «Итоговых
рекомендациях», в строке про ОКР, у азербайджанского стоит
`«– OKP üçün).»>ERP mütləq` — обломок разметки, застрявший в тексте.
Оба перевода его добросовестно скопировали: русский написал «Для ОКР:
ЭРП обязательно», турецкий — «OKB için). ERP mutlaka». Строка переписана
во всех четырёх деревьях.

**Двадцать четыре сломанные фразы в переводах.** Образец один и тот же:
азербайджанский порядок слов перенесён буквально, сказуемое повисает.
«Каждая клиническая глава Из 11 разделов состоит из», «Их подход — с Где
это уместно интегрирована в эту книгу», «Лечение каждого расстройства из
международных правил даются ссылки», «Соматическая презентация очень
распространено», «Наиболее основные скрининговые инструменты». В
английском то же: «Each clinical chapter From 11 sections consists of»,
«Medication names both INN, is also given under a brand name», «The
patient has reached the definitive minimal effective dose.;», «C-SSRS
Assessment structured using scales like», «Psychiatric interview – High
emotional load It is a profession». В турецком — «Farmakoterapi Çoğu
durumda adjuvan», «Somatik sunum Çok yaygındır».

**Три смысловые.** Английский звал раздел 4 «CBT» там, где мастер пишет
KTTD (то есть CDDR) — классификация превратилась в психотерапию. Там же в
списке разделов он написал «biopsychosocial approach», хотя мастер и два
других перевода говорят «подход Попова и Вида» — авторов подменили общим
словом. И «Stigma and isolation» вместо «стигма и приватность»: у мастера
`məhrəmlik` — это приватность, а не изоляция.

Проверка по факту: checkup 0 из 18 · regress 1052 строки чисто · refcheck 0 ·
numcheck 0 из 312 · paracheck 0 · xrefcheck 0 · lang_tags 0 после прогона ·
счёт блочных тегов в 8 изменённых файлах не изменился.

### 2026-08-12 — вводные страницы: что книга обещает читателю (H, часть 2)

**Книга обещала кнопку, которой нет.** Предисловие во всех четырёх
деревьях говорило: «текст здесь живой — на каждой странице есть кнопка
"Исправить"». Справочники добавляли: «нажав кнопку Исправить, вы можете
предложить правильное название». Виджет «Düzəliş et» снят 9 августа,
весь конвейер удалён 10-го — а обещание осталось и читатель ищет кнопку,
которой нет. Одиннадцать мест переписаны: приглашение написать автору
сохранено, обещание кнопки убрано.

**Числа на главной были неверны в обоих слагаемых.** «103 расстройства,
24 главы» — в книге 104 карточки и 23 страницы глав. Причём 103 стоит и в
каноне (`summary.total_cards`), то есть число отстало ещё на этапе сборки.
Исправлено на index.html и mundericat.html четырёх деревьев.

**AACE вместо AACAP.** В «Итоговых рекомендациях» всех четырёх деревьев
среди организаций, за которыми надо следить, стояло AACE — американское
общество клинических эндокринологов — вместо AACAP, детской и
подростковой психиатрии, на которую книга ссылается везде. В elave-acde
AACE стоит законно: там настоящий консенсус ADA/APA/AACE/NAASO 2004.

**В английском «XBT-11» стало «CBT»** — азербайджанская аббревиатура МКБ
превратилась в когнитивно-поведенческую терапию: «See Section 4 (CBT +
ICD-10 + DSM-5-TR comparison)». И там же в английской фразе осталось
азербайджанское «verilir».

Это начало, а не конец: страницы kitab-haqqinda и yekun в переводах полны
фраз того же рода — «Each clinical chapter From 11 sections consists of»,
«The patient has reached the definitive minimal effective dose. ;»,
«Psychiatric interview – High emotional load It is a profession». И список
«11 разделов главы» в kitab-haqqinda не совпадает с реальными разделами
карточек — он устарел. Записано в задачу как незакрытое.

Проверка по факту: checkup 0 из 18 · regress 1020 строк чисто · refcheck 0 ·
numcheck 0 из 312 · paracheck 0 · xrefcheck 0 · lang_tags 0.

### 2026-08-12 — нижняя навигация и справочные страницы (задача H, часть 1)

Кенан заметил одно место: русская нижняя навигация зовёт 6B65
«ПАРЦИАЛЬНОЕ ДИССОЦИАТИВНОЕ ИД», а заголовок карточки — «ЧАСТИЧНОЕ
ДИССОЦИАТИВНОЕ РАССТРОЙСТВО ИДЕНТИЧНОСТИ». Пересчёт показал, что это не
одно место, а **248**: az 48, ru 78, en 60, tr 62. Имена в навигации
собирались из списка названий, устаревшего ещё до перенумерации кодов,
поэтому ссылка «вперёд» могла звать соседа именем, которого у него нет
уже давно.

Все 248 пересобраны из заголовка той карточки, куда ведёт ссылка. Обрезка
по границе слова и не длиннее, чем стояло раньше, — ширина навигации не
выросла ни на одной странице, но ни одно имя больше не врёт. Правило
записано в скрипт, который можно прогнать снова: если имя — верное начало
заголовка, он его не трогает.

**Метки языка в справочниках оказались каруселью.** В таблице названий
глав атрибут `lang` шёл по кругу az → en → ru, не глядя на текст: русские
названия глав помечены английским, английские — русским, турецкие —
английским. 23 строки на страницу, восемь страниц — 184 метки. Сняты;
`_build_abbreviatur.py`, который владеет азербайджанской страницей,
подтвердил, что так и должно быть — он сам их не ставит.

**Расшифровщик сокращений врал в мелочах, которые видны читателю.**
В английском «ADHD» расшифровывалось как «Opioid Use Disorder» — одно
сокращение объяснено совсем другим расстройством. Три строки там же
остались по-азербайджански: «Bipolyar II Pozuntu», «Bipolyar I Pozuntu»,
«Major Depressiv Pozuntu». У KTSSP стояла лишняя точка и не было пометки
«(Azerbaijani abbreviation)», которая есть у соседних строк.

**Шапка колонки врала во всех трёх переводах.** «Полное название на
азербайджанском языке», «Full name in Azerbaijani», «Azerbaycan dili tam
adı» — а колонка на языке самого дерева. Это калька из азербайджанского
издания, которую перевели дословно вместе с содержимым.

Азербайджанские сокращения в русском и турецком теперь помечены как
азербайджанские — так уже делал английский; в турецком добавлено, какая
форма стоит в самом дереве (OSB вместо ASP, KTSSB вместо KPTSP/KTSSP).
И вычищены пять мест, где в английском тексте осталось «ASP» и «RAS»
вместо «ASD».

**Что не стал делать сам.** Таблица сокращений во всех четырёх деревьях
латинская и почти целиком общая. Русский читатель ищет «СДВГ», «ПТСР»,
«РАС» — таких строк нет; английский ищет «PTSD», «cPTSD», «ASD» — нет;
турецкий ищет «OSB», «TSSB», «KTSSB» — нет. При этом ASP/DDHP/KPTSP есть
у всех. Добавить кириллические и турецкие строки — значит поменять
характер страницы, а это решение Кенана; записано задачей K.

Проверка по факту: checkup 0 из 18 · regress 1001 строка чисто · refcheck 0 ·
numcheck 0 из 312 · paracheck 0 · xrefcheck 0 · build_headers, build_sections,
lang_tags, fix_orthography, fix_toc_codes, fix_sidebar — ноль изменений.

### 2026-08-12 — главы 7, 8, 16, 17 против их руководств (задача G)

Тринадцать карточек — сон (7A00, 7A20, 7A21, 7A41, 7A60), тики (8A05),
ПМДР (GA34), сексуальное здоровье (HA00–HA40) — прочитаны против AASM,
AAN/ESSTS, ISPMD, ISSWSH/ISSM/AUA/EAU и против живого дерева ICD-11.

**Ошибка классификации.** Подтипы HA40 в книге были названы неверно:
«лекарство/вещество (HA40.0), медицинское заболевание (HA40.1), другое
(HA40.Y), неуточнённое (HA40.Z)». У ВОЗ HA40.0 — это медицинское
состояние, травма или последствия операции и лучевой терапии; HA40.1 —
психологические и поведенческие факторы; вещество и лекарство — это
HA40.2; и есть ещё HA40.3 (недостаток знаний или опыта), HA40.4 (факторы
отношений), HA40.5 (культуральные факторы). Кода HA40.Z не существует
вовсе. То есть два подтипа были перепутаны местами, четыре потеряны,
один выдуман. Переписано во всех четырёх деревьях.

**Ссылка не на тот источник.** Карточка бессонницы приписывала NICE
слова «эффект цифровой КПТ-И близок к очной; экономически эффективная
альтернатива». NICE HTG624 (2022) говорит ровно другое: Sleepio —
вариант, **экономящий средства** первичного звена для тех, кому иначе
предложили бы гигиену сна или снотворное, и прямого сравнения с очной
КПТ-И **нет**. Строка переписана, HTG624 добавлен в §11: до этого NICE
упоминался в карточке пять раз и в списке литературы отсутствовал.

**ISPMD не был в списке литературы ПМДР**, хотя раздел «уточнения по
источникам» на него опирается. Добавлены оба консенсуса — Nevatte 2013 и
Ismaili 2016.

**Что нашло чтение, а не сверка.** В 7A60 мастер говорит: «Non-24-hour —
у слепых людей; циркадный ритм не подстраивается под внешний световой
сигнал». Русский перевод написал «циркадный ритм **не нарушен**» — в
карточке о расстройстве стоит отрицание расстройства. Английский прочёл
азербайджанское «kor insanlarda» (у слепых людей) как «**core insomnia**»:
слепые из фразы исчезли, а вместо них появилась несуществующая «основная
бессонница». Это тот же образец, что «şiddət» → «насилие»: перевод по
звуку слова, а не по смыслу.

В 8A05 «подавление тиков в школе» стало «приступы в школе» по-русски,
«**seizure** at school» по-английски и «okulda tutma» по-турецки —
удержание тика превратилось в припадок на трёх языках сразу.
Азербайджанское «1 il» (год) уехало нетронутым в английский и турецкий.
У английского и турецкого сломалось предложение о NIMH 2017 —
«не рекомендуется» осталось дважды и повисло без подлежащего.

В HA00 мастер писал непонятное «(BPS-də modifikasiya)». Такого сокращения
в книге больше нигде нет. Все три перевода угадали в нём депрессию:
«модификация при БДР», «modification in MDD», «MDB'de modifikasyon». По
факту речь о чёрной рамке флибансерина, которую FDA смягчила в 2019:
после 1–2 стандартных порций подождать не менее двух часов, при трёх и
более дозу в этот вечер пропустить — риск тяжёлой гипотензии и синкопе.
Записано так во всех четырёх деревьях, включая мастер.

**Не закрыто и не выдумано.** Четыре оставшихся упоминания «NICE 2025»
привязать к документу не удалось: формального руководства NICE по
бессоннице не существует, а NICE CKS закрыт для не-британских адресов и
прямо запрещает автоматический сбор. По существу ссылка верна — NICE
действительно ставит КПТ-И первой линией, — но точного идентификатора и
даты у меня нет, поэтому даты не ставил. Записано задачей J.

Проверка по факту: checkup 0 из 18 · regress 987 строк чисто · refcheck 0 ·
numcheck 0 из 312 · paracheck 0 · xrefcheck 0. Счёт блочных тегов в 24
изменённых файлах совпадает всюду, кроме трёх намеренных новых записей
литературы (+1 в 7A00, +2 в GA34, симметрично во всех четырёх деревьях).

### 2026-08-12 — 6B80 «XBT-11 — paralel» (задача F) и найденный класс

Одна строка в §6.2 анорексии говорила: DSM-5-TR делит тяжесть по ИМТ
(≥ 17 / 16–16,99 / 15–15,99 / < 15), а «МКБ-11 — параллельно». Проверено
по браузеру ВОЗ: параллели нет. У МКБ-11 одна точка отсечения вместо
трёх — 6B80.0 значительно низкий вес (взрослые ИМТ 18,5–14,0; дети
5-й–0,3-й перцентиль), 6B80.1 опасно низкий вес (ИМТ < 14,0) — и есть
категория, которой у DSM нет вовсе: 6B80.2, восстановление при нормальном
весе, где диагноз держится до полного и устойчивого выздоровления.

Вторая половина строки была неверна отдельно: «атипичная нервная
анорексия возможна при нормальном ИМТ (6B8Y)». Такой категории в МКБ-11
нет — это термин OSFED из DSM-5-TR, а 6B8Y называется «другие уточнённые
расстройства пищевого поведения». Строка переписана в четырёх деревьях
целиком.

**Класс, а не случай.** Такая строка в книге не одна: «ICD-11 —
parallel» или «DSM-5-TR / ICD-11 — same» стоит в 26 местах. Проверили
ещё два, и оба неверны так же: у **6B82** DSM-5-TR требует эпизод раз в
неделю три месяца и даёт шкалу тяжести по числу эпизодов, а у МКБ-11 ни
порога, ни шкалы; у **6C73** DSM-5-TR требует частоты и возраста ≥ 6 лет,
а МКБ-11 не требует ни того, ни другого. Остальные 23 не проверены —
записаны отдельной задачей, потому что это проверка утверждений против
названного источника, а такие Кенан отложил.

### 2026-08-12 — названия и коды 104 карточек против ВОЗ (задача E)

Эталон брали не из памяти и не из файла 2026-08-05, а с живого браузера
ВОЗ (ICD-11 MMS, релиз 2025-01), раскрыв главу 06 целиком и нужные ветви
глав 07, 08, 16 и 17. Сняли по три языка: английский, русский, турецкий.
Азербайджанского перевода ICD-11 не существует — там источник другой
(протоколы Минздрава), поэтому аз. дерево в эту сверку не входит.

**Названия.** Английские заголовки совпали все 104 из 104. Русские — 91
из 91. Турецкие — 89 из 91, и оба расхождения содержательные.

Первое: **6C72 в турецком назывался «KOMPULSİF CİNSEL TOPLUM KARŞITI
DAVRANIM BOZUKLUĞU»**. «Toplum karşıtı davranım» — это имя 6C91,
диссоциального расстройства поведения; в заголовке компульсивного
сексуального поведения ему делать нечего. Это след старой глобальной
замены, и он разошёлся широко: 417 вхождений в 137 файлах — боковое меню
каждой страницы турецкого дерева, `<h1>`, `<title>`, `og:title`.
Правильное имя уцелело только в нижней навигации и в одном `og:title`,
поэтому глазами дефект было почти не поймать: страница называлась
по-разному в разных своих частях. Исправлено в каноне и по всему дереву.

Второе: **6E21** — у ВОЗ в турецком опечатка, «davranşsal» без «ı».
Книга пишет «DAVRANIŞSAL», то есть правильно. Не трогали: эталон здесь
ошибается, и подгонять книгу под опечатку было бы хуже, чем разойтись.

**Коды.** Имя файла карточки — это слаг, а не код; точный код живёт в
шапке. Шесть карточек уже держали в шапке подкод (GA34.41, HA01.1,
HA02.0, HA03.0, 7A21–7A26, 7A60–7A65) — здесь книга оказалась точнее,
чем можно было ждать. Но их собственный текст §1 и запись §11 ссылались
на грубый слаг: «WHO. ICD-11. HA01 Erectile dysfunction» при том, что
HA01 у ВОЗ — «Sexual arousal dysfunctions», а эректильная дисфункция это
HA01.1.

**8A05 был неточен и в самой шапке.** MMS 8A05 = «Tic disorders»,
а «Primary tics or tic disorders» — это 8A05.0. Канон это знал
(`icd11_correct: 8A05.0`), но поле `icd11_shown` осталось «8A05», и
шапка печаталась с грубым кодом. Правка одного поля в
`_codes_canon.json` разошлась через `build_headers.py` и
`fix_toc_codes.py` по 548 файлам; §1, §6 и §11 дописаны вручную в
четырёх деревьях.

Сверка «код в тексте = код в шапке» по всем карточкам четырёх деревьев
даёт теперь ноль (было 40). Проверка по факту: checkup 0 из 18 · regress
958 строк чисто · refcheck 0 · numcheck 0 из 312 · paracheck 0 ·
xrefcheck 0 · build_sections, lang_tags, fix_orthography, fix_toc_codes,
fix_sidebar — ноль изменений. Счёт блочных тегов в 548 изменённых файлах
совпадает с прежним ровно.

### 2026-08-12 — §11 «Источники»: списки литературы четырёх деревьев (задача D)

Прицел — запись источника. Список литературы отличается от прозы тем, что
его нельзя переводить: переведённый заголовок статьи делает источник
ненаходимым. Поэтому сначала измерили строй, потом читали.

**Строй.** Записей в карточке поровну во всех четырёх деревьях — 884, ноль
расхождений. Значит, эталоном записи можно взять английское дерево, а
чтение английских списков покрывает все четыре. Перепись соединителей
подтвердила то же: «et al.» az 277 / en 277 / ru 273 / tr 235 против
5 «и др.» и 43 «ve ark.» — протечки, а не система.

**Восстановлено 76 записей** в ru/tr, где заголовок был переведён или
фамилия переписана кириллицей. Защита от ложных правок — не «латиница
против кириллицы», а список законных локализаций: имя болезни в записи
XBT-11, национальные документы Минздрава.

**Дефект мастера.** В самом азербайджанском дереве 15 записей несли
азербайджанские слова внутри английских заголовков — след старой
глобальной замены: «autism: an sübuta əsaslanan meta-analysis»,
«Mortality rates in patients with sinir anoreksiyası», «after admission:
a izləmə study». Перевод их честно скопировал. Плюс 4 дефекта записи в
английском, 14 разночтений одного источника между карточками (56 правок)
и 24 дефиса вместо тире в диапазонах страниц.

**Что нашло только чтение.** 6A22 (шизотипическое расстройство) ссылался
не на ту статью: §8.4 приписывал Coccaro E.F. исследования малых доз
антипсихотиков при шизотипическом расстройстве, а список литературы давал
его же работу о флуоксетине при периодическом эксплозивном расстройстве —
статью из совсем другой карточки, 6C73. Утверждение и ссылка были неверны
вместе. Сверено по PubMed: нужная работа — Koenigsberg H.W., Reynolds D.,
Goodman M. et al. «Risperidone in the treatment of schizotypal personality
disorder», J Clin Psychiatry 2003;64(6):628–634. Заменены и запись, и
подпись в §8.4, во всех четырёх деревьях. Автоматическая проверка того же
образца — «в списке статья про болезнь, которой в карточке нет» — по 36
именам болезней даёт ноль.

**Навигация английского дерева** (попутно, целилось не туда): «DEPRESIVE»
вместо «DEPRESSIVE» в четырёх карточках, мусор «← µ=» в 6C73 и — главное —
40 карточек из 81 без стрелки «←» в ссылке назад, тогда как в az, ru и tr
стрелка стоит во всех 81. Английский читатель видел ссылку «вперёд» со
стрелкой, а «назад» — без.

Проверка по факту: checkup 0 из 18 · regress 901 строка чисто · refcheck 0 ·
numcheck 0 из 312 · paracheck 0 · xrefcheck 0 · build_headers 0 ·
build_sections 0 · lang_tags 0 · fix_orthography 0. Счёт блочных тегов в
62 изменённых файлах совпадает с прежним ровно — правился только текст.

### 2026-08-12 — §8 «Лечение»: сплошная вычитка трёх переводов (задача C)

Прицел — структура фразы. Прочитаны §8 всех 104 карточек в русском,
английском и турецком деревьях (по шесть частей на язык, ~640 тыс. знаков).

**Клинически значимое.** tr/6A05 «birinci basamak Stimulant + Davranış
Bozukluğu» — «поведенческое вмешательство» превратилось в «расстройство
поведения», и это стояло в схеме первой линии для двух возрастных групп.
en/7A20 «SSRI/SNRI induced cataplexy» — препараты катаплексию лечат, а не
вызывают. 6A60: азербайджанское «tək başına əks-göstərişdir» потеряло
сказуемое во всех трёх переводах сразу — таблица читалась так, будто
монотерапия антидепрессантом просто требует внимания, тогда как мастер
называет её противопоказанной; в турецком на этом месте стояло
несуществующее слово «ekstakomb». 6A62 — то же «противопоказан» стало
«severe» и «дополнительный компонент». en/6A24 подменено подлежащее:
«эротомания и соматический бред считались преобладающими» вместо
«пимозид считался предпочтительным». en/6C01 «Genu reduction» вместо
«снижения тревоги». tr/HA01 из всех четырёх линий терапии выпали номера.
ru/8A05 ссылка на исследование TACT подменена другой статьёй, тогда как
мастер и два других дерева держат верную. ru/7A21 потеряно, что
солриамфетол одобрен и при обструктивном апноэ сна. «Запланированный
дневной сон» стал «грёзами» в русском, «daydreaming» в английском,
«rüyaları» в турецком.

**Классы, закрытые целиком.** Лишняя точка внутри выделения — 45 (первый
проход пропустил метки с вложенными тегами: регулярное выражение не
пускало теги внутрь). Точка в конце ячейки таблицы — 66. Потерянная
заглавная: 96 меток и 62 ячейки. Шапки таблиц — 55, включая ru
«нарушение» вместо «Расстройство», tr «ihlal» (нарушение закона),
обломок «Преиму», словарную подсказку «karışma, müdahale etme».
Чужие сокращения: в турецком ASP/RAS/ID/ZD/ZY вместо OSB и İD, GAD
вместо YAB (24 места) и ГТР (6 в русском), пять форм РКИ сведены к RKÇ;
в русском ЭКТ→ЭСТ, УО/ИД/ИН→ИР, ДБТ/МБТ→DBT/MBT, РПБДГ/ППСД→RBD/BPSD.
Капслок вместо `<strong>` — 14 мест в четырёх деревьях. Три удвоенные
фразы в турецком (предложение напечатано дважды).

**Проверка по факту.** checkup 0 из 18 · regress 726 → 895 строк, чисто ·
prosecheck 0 · numcheck 0 из 312 · paracheck 0 · xrefcheck 0 · refcheck 0 ·
build_headers и build_sections идемпотентны на 416 файлах · lang_tags 0 ·
fix_yo 0 · fix_meta 0. Структура не сдвинулась: по 241 изменённому файлу
счётчики h1/h2/h3/h4/p/li/table/tr/td/th/ul/ol/section/div совпадают с
состоянием до правок — 0 расхождений.


### 2026-07-22 — Book translation EN+RU: pipeline + waves 1-3 (IN PROGRESS, cloud session)
**Goal:** full copies of the book (161 pages) in English and Russian at `klinik-psixiatriya/en/` and `klinik-psixiatriya/ru/`, identical structure.
**Branch:** `claude/clinical-psychiatry-menu-mkb-nnz1bt` (recreated from main after menu-PR #2 merge; also in this session: XBT-11 top-level menu item shipped in PR #2).
**Infrastructure (committed):**
- `_translate/pipeline.py` — extract / chunk / inject / status. HTML tokenised; agents translate ONLY text segments; markup is byte-identical by construction. `status <lang>` shows todo/invalid chunk ids; `inject <lang>` writes final pages into `klinik-psixiatriya/<lang>/` with localized meta (lang, og:locale, canonical→self under /<lang>/, JSON-LD inLanguage) and copies style.css/duzelis.*.
- `_translate/glossary_en.md`, `glossary_ru.md` — built by `build_glossary.py` from abbreviatur.html trilingual tables + _codes_map.json (en11) + TYPOGRAPHY.md §0b.
- `_translate/az/*.json` — 93 493 segments from 160 pages (admin-corrections.html excluded); `chunks/` — 425 chunks × 2 langs; `INSTRUCTIONS_EN.md` / `INSTRUCTIONS_RU.md` — translator-agent instructions (agent prompt = "Прочитай и выполни инструкцию ... для чанков: id1, id2, id3").
- Translated output goes to `_translate/{en,ru}/out/<chunk-id>.json`.
**Progress:** EN 41/425 chunks, RU 36/425 (all 23 chapter overviews both langs + 6A00-6A01 partially). Pilot pages injected: `klinik-psixiatriya/en/{index,6C50}.html`, `ru/{index,6C50}.html` — verified.
**Wave scheme:** 12 background agents per wave (6 EN + 6 RU, 3 chunks each); commit `_translate` after each wave. Waves hit Claude session-limits twice (resets were 11:10 and 16:30 UTC) — resume via `status` (it lists exactly what's missing; nothing is retranslated).
**PAUSED by owner (16:40 UTC):** owner will upload a file with translations/parallels (994 corpus) to the repo — incorporate it before continuing waves. 994 term DB itself unreachable from cloud (SSH key only on local Windows machine).
**Next steps:** (1) read owner's parallels file, adapt pipeline; (2) finish waves until `status` = 0 todo both langs; (3) `inject en`, `inject ru`; (4) per-language search-index (adapt `build_search_index.py` BASE), hreflang, commit, draft PR.

### 2026-05-14 — chapters-v2 finalized
- Completed final 8 disorders across two autonomous batches:
  - Batch: 7A60, 7A80, HA00, HA01 → commit `0057c68`
  - Batch: HA02, HA03, HA04, HA05 → commit `85fff99`
- Marked all 103 disorders DONE in `_progress.md`; created `_done.md`.
- Autonomous wakeup loop terminated.
- Created this `PROGRESS.md` at user's request for cross-session memory.

### 2026-05-14 — Terminology sync workflow + canonical-terms header
- New workflow: `Düzəlt` button (site) → Google Sheet row → manual approval (`Status=ok`) → `_term_sync.py` (session-start) → site/book/abbreviatur all updated.
- `_term_sync.py` fetches GAS `?action=approved` endpoint or reads local `_terms_approved.json` fallback. Applies via protected substitution (refs + abbr titles preserved).
- `_build_abbreviatur.py CANONICAL_TERMS` — single source of truth for all canonical site terms. Renders into `#cari-terminler` header in `abbreviatur.html` showing "Saytda istifadə olunan adlar və terminlər (cari)".
- Rule codified in TYPOGRAPHY.md §0c, CLAUDE.md (session-start ritual), `book-typography-icd11` skill (global + project), HISTORY.json.
- duzelis-gas.txt extended with doGet handler for `?action=approved`.

### 2026-05-14 — book deployed to site + DOCX rebuilt
- Injected all 103 v2 disorder fragments into the 23 `klinik-psixiatriya/NN-*.html` chapter files via `_inject_chapters_v2.py` (each disorder wrapped in `<section class="disorder" data-icd="…">`).
- Regenerated `<aside class="sidebar">` in 27 pages and the book TOC in `klinik-psixiatriya/index.html` (between `<!-- BOOK-TOC:START/END -->` markers) via `_rebuild_book_nav.py`.
- Added academic-textbook CSS for `section.disorder` and `.book-toc` to `klinik-psixiatriya/style.css`.
- Re-ran `_inject_abbr.py` (now 4231 wrappings, +65 from new content).
- Rebuilt `klinik-psixiatriya/KLINIK_PSIXIATRIYA_6.docx` via `build_book.py + pandoc`:
  - Title page from pandoc metadata (Title style, kept out of TOC)
  - `MÜNDƏRİCAT` TOC (depth 2)
  - Page break before every Heading 1 (chapter) and Heading 2 (disorder); first heading's page break stripped to avoid leading blank page
  - 13,621 paragraphs, 195 tables, 15 Heading 1, 219 Heading 2, 1467 Heading 3
- `.gitignore` updated to exclude `_build/` and `pandoc-*.msi`.
- Commit `155bebf` pushed to `claude/stupefied-cori-5b6e4a`.

---

## Сессия 2026-08-09 — сплошная сверка книги и мобильная вёрстка

**Состояние:** 104 карточки × 4 языка. `python checkup.py` — 0 сбоев из 11.
`build_headers.py` и `build_sections.py` идемпотентны на 416 файлах.

### Инструменты (в корне репозитория)

| Файл | Что делает |
|---|---|
| `checkup.py` | 11 проверок: полнота, параллельность, навигация, три классификации, канон az, межъязыковое загрязнение, ложные друзья, типографика, разделитель после `</strong>`, турецкий процент, наличие источников |
| `refcheck.py` | кого текст цитирует как доказательство, а в §11 нет (только упоминания без года — остальные проверяемы по самому тексту) |
| `fix_strong.py` | восстанавливает потерянный разделитель после `</strong>`; НЕ трогает тюркский аффикс и английское множественное |
| `fix_punct.py` | точка в конце пункта, потерянная в переводе; решение по большинству языков |
| `progress_map.py` | `PROGRESS_MAP.md` из фактического состояния файлов и истории git |
| `apply_fixes.py`, `apply_global.py` | применение списков правок по карточкам / по всему дереву |

### Что закрыто

- **Восемь осиротевших карточек удалены** (48 файлов): 6A07, 6C42, 6C47, 6E60,
  7A40, 7A80, HA04, HA05 — дубликаты под кодами, которые МКБ-11 отдала другим
  расстройствам, со сфабрикованной ссылкой на ВОЗ.
- **Столбец DSM-5-TR**: восемь строк указывали на чужое расстройство, 262 имени
  пустовали в азербайджанском и русском изданиях. Коды переведены с ICD-9-CM
  на ICD-10-CM — 100 в шапке и 31 206 в тексте и навигации.
- **Столбец МКБ-10**: диапазоны вместо одной подрубрики (6A00 F70 → F70–F79,
  6B60, 6C91), пустые ячейки закрыты.
- **6D11 переписана** — описывала personality difficulty (QE50.7) вместо того,
  что заявлено её кодом; добавлен отсутствовавший домен 6D11.5.
- **6D82** — McKeith 2017: четыре основных признака, а не три; РПБДГ перенесён
  в основные, чувствительность к антипсихотикам — в поддерживающие.
- Сверены по первоисточникам: Lancet Commission 45%, Freeman n=597,
  Verhulst 49%, Caldwell ~50%, Marconi дозозависимо, ВОЗ 2,6 млн,
  ОВР 1–11%, расстройство поведения 2–10%, Scared Straight ОШ 1,68,
  педофилия 3–5%, фроттеризм 30% / 10–14%.
- Сфабрикованные ссылки заменены: TACT, Montejo, Davis, WFSBP 2020, Linehan,
  Leckman, химера Roessner.
- **Турецкое издание**: 108 азербайджанских форм, PTSB → TSSB ×34, порядок слов
  в рубриках МКБ-10, 52 нарушения правила процента.
- 642 потерянных разделителя после `</strong>`, 98 пропавших точек,
  432 сломанных canonical.
- **Мобильная вёрстка**: иерархия заголовков (было 17,9 / 17,0 / 15,4 px при
  тексте 16 px → стало 24 / 19,2 / 16,6), зоны нажатия 44 px в навигации книги,
  оглавлении и хлебной крошке. Шапка сайта не тронута — так помечено в коде.

### Что осталось

`refcheck.py` — 14 упоминаний в 11 карточках, названных фамилией без года.
Выходные данные надо брать из того издания, которым пользовался автор,
иначе ссылка окажется такой же ложной, как была «Montejo J Sex Marital Ther
2018». Подробности — `BLOCKERS.md`.

---

## Сессия 2026-08-11 — сплошная вычитка переводов

Читалось глазами, не машиной: определения §1 всех 104 карточек в трёх
переводах и все 103 раздела мифов §10 в русском — НОВЫМ прицелом
«структура фразы». Сами эти разделы были пройдены раньше (6–10 августа,
все четыре языка), но прежние проходы смотрели на коды, ложных друзей,
первоисточники и орфографию. Новый прицел нашёл брак в трижды прочитанном
тексте — 57 мест в русском и слой в английском. Инструменты строились
только под классы брака, найденные чтением.

### Что найдено чтением и исправлено

**Развёрнутая причастная конструкция.** Азербайджанский ставит главное слово
в конец («…davam etdiyi ilkin psixotik pozuntudur»); при механическом
развороте сказуемое остаётся висеть, а придаточное открывается заглавной
посреди фразы. Целый слой в русском (57 мест) и в английском. Примеры:
«дополнительно **При котором** психотические симптомы… **является первичным
психотическим расстройством**», «at least one hypomanic **Episode** and at
least one major depressive **Characterized by episodes**».

**Фактические ошибки.**
- `6A70` в русском называла себя рекуррентным расстройством, будучи карточкой
  ЕДИНИЧНОГО эпизода; `6A71` ссылалась на 6A70 как на рекуррентное. Шапки при
  этом были верны — ошибка жила только в первой строке §1.
- `6B23` во всех четырёх языках: «Illness Anxiety Disorder (F45.22)» — в
  DSM-5-TR это F45.21, а F45.22 занят дисморфическим расстройством.
- `6B22` во всех трёх переводах: «DSM-5-TR: F42.2» вместо F42.8 из мастера.
- Синдром назван по Willi **Kleine** и Max Levin — «Klein-Levin» стояло в
  английском раз, в турецком дважды, а в русском четырежды «Клейна-Левина».
- `6C4A`: русский и турецкий потеряли «ведущая» — никотин назван ГЛАВНОЙ
  предотвратимой причиной смертности, а не одной из.

**Служебные данные `<head>`, которых не видно при чтении.** 79 карточек
держали в `<title>` старое, доканоническое имя («SINGLE EPISODE DEPRESIVE
DISORDER» с одной s, «LIGHT NEUROCOGNITIVE» вместо MILD); 158 файлов
показывали в `og:title` не то, что во вкладке; все 411 переведённых страниц
объявляли `"inLanguage": "az"` — сообщали поисковику, что русская,
английская и турецкая книги написаны по-азербайджански.

**Терминология.** Одно расстройство называлось шестью именами
(«имитированное», «фактитивное», «фактициозное», «симулятивное»,
«фактитное»); «идентификация» стояла вместо «идентичности» в 19 местах;
сокращения разъезжались — BDD/ДТР/БДД/ДТД, RAD/РАД/РРП/РП, DSED/ДСЭД/ДРСП,
DLB/ДТЛ, FTD/ЛВД, AChEI/АХЭИ/ИАХЭ, PPD/ППД/ППР, К-ПТСР/кПТСР, ДДГП вместо
СДВГ. Всё сведено к формам мастера.

**Дефекты, вычищенные из мастера, но уцелевшие в переводах.** Турецкое
«resmiyet» вместо сказуемого — девять мест; английские слова в русском и
турецком («neglect», «fostering», «subthreshold», «Lisdexamfetamine») — 38.

**«Ё» в русском.** Книга писала одно слово двояко — 95 семей
(«распространённость» 50 против «распространенность» 39). Выбрано «всегда
ё»: для каждой семьи форма с «ё» уже стояла в книге. 613 замен.

### Новые инструменты

| файл | что делает |
|---|---|
| `prosecheck.py` | семь проверок на след механического перевода |
| `fix_yo.py` | последовательное «ё»; правит и книгу, и канон |
| `fix_meta.py` | `<title>`, `og:title`, язык документа из канона |

`checkup.py` вырос с 14 проверок до 18: таблица кодов по канону, парность
тегов в блоках, согласие `<head>` со страницей, слово не приросло к
выделению, скобки сбалансированы, кавычка не склеена с тире. Каждая новая
проверка доказана на подложенном дефекте.

`regress.py` вырос с 484 строк до 726.

### Порядок прогона (важно)

`fix_yo.py` → `fix_meta.py` → `build_headers.py`. Первый правит и книгу, и
`_codes_canon.json`; второй — заголовок вкладки, который лежит вне `<main>`.
Иначе канон возвращает старое написание и сборка перестаёт быть
идемпотентной. Проверено дважды на живом сбое.

### Состояние на конец сессии

`checkup` 0 из 18 · `regress` 726 · `refcheck` 0 · `numcheck` 0 из 312 ·
`paracheck` 0 · `xrefcheck` 0 · `prosecheck` 0 из 7 · сборки идемпотентны
на 416 файлах.

Решения, ждущие владельца, — в `PROOFREADING.md` §2 (девять пунктов).
