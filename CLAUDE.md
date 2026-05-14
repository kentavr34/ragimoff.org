# CLAUDE.md — Initialization Brief for AI Agents

> **First action in any new session:** read this file, then `PROGRESS.md`, then `README.md`, then `HISTORY.json`, then `PROJECTS.json`. Only after that, touch code.

## Working directory
`C:\Users\SAM\Desktop\sayt2` — always operate from here. Active long-running work happens inside the git worktree at `.claude\worktrees\stupefied-cori-5b6e4a` on branch `claude/stupefied-cori-5b6e4a`.

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
NICE · APA · WFSBP · Cochrane · DSM-5-TR · XBT-11 (ICD-11) · AAP · AACAP · FDA · CANMAT · NIMH · ISSTD · ICCS · WPATH · VA-DoD · SAMHSA · AASM · AUA · EAU · ISSWSH · ISSM

## Session-start ritual (читай каждый раз)
В начале сессии, перед любой содержательной работой над книгой:
1. Прочитать `TYPOGRAPHY.md` (правила, особенно §0c — терминологический синхронизм)
2. Прочитать `PROGRESS.md` (последняя сессия)
3. **Запустить `python _term_sync.py`** — подтянуть одобренные правки из Google Sheet (или локального `_terms_approved.json`), применить их по всему сайту/книге, доложить пользователю что было применено.
4. Если правки применены — выполнить пересборку: `_build_abbreviatur.py` → `_rebuild_book_nav.py` → `build_book.py`.

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
