# CLAUDE.md — Initialization Brief for AI Agents

> **First action in any new session:** read this file, then `PROGRESS.md`, then `README.md`, then `HISTORY.json`, then `PROJECTS.json`. Only after that, touch code.

## Working directory
`D:\Документы\ragimoff` — always operate from here.

The old path `C:\Users\SAM\Desktop\sayt2` no longer exists. 41 legacy scripts still
hardcode it and will fail if run; the live toolchain resolves paths from
`Path(__file__).parent`. See "Script inventory" below before running anything.

## Owner
Dr. Kənan Rəhimov — clinical psychiatrist. The repository serves his practice site (`ragimoff.org`) and his Azerbaijani-language Clinical Psychiatry textbook ("Klinik Psixiatriya").

## Two parallel projects in this repo
1. **Main website** — multilingual (AZ / RU / EN) static site on GitHub Pages. See `README.md` for the partials/build.py architecture.
2. **Klinik Psixiatriya textbook** — separate subsystem under `klinik-psixiatriya/` + master sources under `_supplements/`. Excluded from `build.py` by design.

`build.py`'s `SKIP_DIRS` / `SKIP_FILES` keep these two from interfering.

## Language and terminology (textbook)
Academic Azerbaijani medical register. Always use:
- `Klinik təzahürlər` (not *mənzərə*)
- `Vahid diaqnostik meyarlar` (not *çek-list*)
- `İnstrumental müayinələr` (not *Alət*)
- `pasiyent` (not *xəstə*)
- `psixi pozuntu` (not *ruhi*)
- `metodları` (not *üsulları*)
- `təfəkkür`, `şüur`

## Source whitelist (textbook citations)
Only authoritative sources are allowed:
NICE · APA · WFSBP · Cochrane · DSM-5-TR · XBT-11 (ICD-11) · AAP · AACAP · FDA · EMA · CANMAT · NIMH · ISSTD · ICCS · WPATH · VA-DoD · SAMHSA · AASM · AUA · EAU · ISSWSH · ISSM · ACOG · USPSTF · RCPsych · AGS (Beers) · ISPMD

## Session-start ritual (читай каждый раз)
В начале сессии, перед любой содержательной работой над книгой:
1. Прочитать `TYPOGRAPHY.md` (правила, особенно §0c — терминологический синхронизм)
2. Прочитать `PROGRESS.md` (последняя сессия)
3. **Запустить `python _term_sync.py`** — подтянуть одобренные правки из `_corrections/PENDING.json` (статус `approved`), применить их, доложить пользователю что было применено. Без `--apply` скрипт ничего не пишет.
4. Если правки применены — выполнить пересборку: `_build_abbreviatur.py` → `_rebuild_book_nav.py` → `build_book.py`.
5. **Проверить по факту:** `checkup.py` (12 проверок) → `regress.py` (сторож исправленных дефектов) → `refcheck.py` (цитаты против списка литературы) → `build_headers.py` и `build_sections.py` (должны показать 0 изменений).

## Script inventory (2026-08-09)
74 скрипта в корне. Прежде чем запускать любой — посмотрите, в какую группу он входит.

**Живые, идемпотентные — можно запускать всегда:**
`checkup.py`, `regress.py`, `refcheck.py`, `wordcheck.py`, `progress_map.py`,
`build_headers.py`, `build_sections.py`, `apply_global.py`, `apply_fixes.py`,
`fix_quotes.py`, `fix_space.py`, `fix_dash.py`, `fix_punct.py`, `fix_strong.py`,
`fix_glossary.py`, `_build_abbreviatur.py`, `_rebuild_book_nav.py`, `_term_sync.py`.

**Мёртвые — путь `C:\Users\SAM\Desktop\sayt2` не существует (41 шт.):**
все `fix_dsm_*`, `fix_xbt_*`, `fix_nav_*`, `fix_search_*`, `add_*`, `build_terminoloji.py`,
`build_search_index.py`, `merge_qisaltmalar.py`, `update_docx.py`, `read_docx.py` и др.
Запуск завершится ошибкой пути — это единственное, что защищает данные.

**Одноразовые и опасные — НЕ запускать (проверено в изолированном worktree):**
| скрипт | что сделает при запуске |
|---|---|
| `_fix_terminology3.py` | 1310 замен в 228 файлах |
| `_inject_abbr.py` | обернёт 4215 сокращений в `<abbr>` |
| `_unwrap_abbr.py` | снимет их обратно в 160 файлах |
| `_replace_pille.py` | 10 файлов |
| `_sync_17_23.py` | перезапишет 7 страниц глав из `_supplements` |
| `_fix_terminology4.py` | 7 файлов; именно он когда-то ввёл опечатку `skrinninq` |
| `_fix_all_v5.py` | 4 файла |
| `_reorder_front.py` | переставит вводные страницы |

**Конфликт генераторов:** `abbreviatur.html` умеют перезаписывать девять скриптов;
источник истины — `_build_abbreviatur.py`. `build_terminoloji.py` — его старый
конкурент с другими данными (в нём AAP всё ещё «атипичные антипсихотики»).

## Typography / verstka rules
**Read `TYPOGRAPHY.md` BEFORE any DOCX or book-HTML layout work.**

The book follows **ICD-11 РФ 2022** visual style (138×228 mm reference, but our pages are A4). Reference PDF: `_supplements/ICD-11_RU_2022_reference.pdf`. Our font stays Times New Roman (professional medical textbook proportions).

Skill: `.claude/skills/book-typography-icd11/SKILL.md` (also mirrored at `~/.claude/skills/book-typography-icd11/SKILL.md`).

Covers: title page, heading hierarchy (H1 28pt > H2 20pt > H3 14pt > H4 12pt > H5 11pt), page-break (only chapters + disorder ICD-titled H2, never sub-sections), TOC depth 2 with dot leaders, alternating page headers/footers, terminology blacklist, source whitelist, Düzəliş et widget. Do not ask the user to repeat these rules.

## Hard rules
- `index.html` (root AZ) is the design etalon. Never modify without explicit user permission. `build.py` skips it via `SKIP_FILES`.
- `klinik-psixiatriya/` has its own structure; `build.py` skips it via `SKIP_DIRS`.
- Before mass edits, create a `backup-before-<topic>` git tag.
- Never push without committing. Never commit secrets or large binaries (a `pandoc-*.msi` was caught and unstaged earlier).
- Never amend commits — always create new ones.
- Do not auto-create `.md` docs unless the user asks; `PROGRESS.md`, `HISTORY.json`, `PROJECTS.json` are the canonical state files.
- CRLF warnings on Windows are expected — do not "fix" them.

## Active state snapshot (update at end of every session)
- See `PROGRESS.md` for the human-readable session log.
- See `HISTORY.json` for the structured transformation log.
- See `PROJECTS.json` for the per-project status.

## Editor preferences
- Use `Edit` for in-place changes; `Write` only for new files or full rewrites.
- Prefer minimal, surgical diffs. Match existing style exactly.
- No emojis in files unless explicitly requested.
