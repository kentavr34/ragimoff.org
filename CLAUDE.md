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

## Typography / verstka rules
**Read `TYPOGRAPHY.md` BEFORE any DOCX or book-HTML layout work.** It covers: title page format, heading hierarchy (H1 28pt > H2 20pt > H3 14pt > H4 12pt), page-break rules (only chapters + disorder ICD-titled H2, never sub-sections), TOC format, terminology blacklist, source whitelist, widget injection. Do not ask the user to repeat these rules — they live in `TYPOGRAPHY.md`.

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
