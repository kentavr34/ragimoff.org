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
