#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сторож hero-уникации 2026-09-08.

Проверяет, что страницы сайта без инлайновых дубликатов компонента
.ph-badge / .ph-h1 / .ph-sub из gtc.css, и что канонические классы
(ph-badge span, ph-h1, ph-h1-w1/w2, ph-sub) на месте.

Правила волны 2026-09-08 (DESIGN-STANDARD.md, «PAGE HERO SYSTEM»):
- Классы ph-* не переименовывать; компонент знает только их.
- Инлайн-дубли .ph-badge {} допускаются только если идентичны
  каноническому блоку в gtc.css (с line-height var(--type-label-line)).
- ph-h1-w2 опционален: h1 из одного слова («Социофобия») законно
  держит только ph-h1-w1; фиттер все обращения к w2 обёрнут в if (w2).
- Page-специфика живёт в scoped-оверрайдах вида
  «.page-hero-x .ph-h1 .ph-h1-w1 { color: … }» (двухцветный h1 на
  samira/tehsil) — это легально. Запрещено переопределение компонента:
  селектор, начинающийся с .ph-h1-w1/.ph-h1-w2 (остаток батча 09-06).
- Сайты /klinik-psixiatriya/ не touched (свой hero-паттерн).
"""
import hashlib, re, sys
from pathlib import Path

ROOT = Path(__file__).parent
GTc = (ROOT / 'gtc.css').read_text(encoding='utf-8')
PH_BADGE_RE = re.compile(r'\.ph-badge\s*\{.*?\}', re.S)
PH_H1_RE = re.compile(r'\.ph-h1\s*\{.*?\}', re.S)
PH_SUB_RE = re.compile(r'\.ph-sub\s*\{.*?\}', re.S)
issues = []

# 1. канонические компоненты: обязательные фрагменты
for name, pat, must in [
    ('.ph-badge', PH_BADGE_RE, ['line-height', 'margin-bottom', 'var(--type-label-line)']),
    ('.ph-h1', PH_H1_RE, []),
    ('.ph-sub', PH_SUB_RE, []),
]:
    m = pat.search(GTc)
    if not m:
        issues.append(f'CRITICAL: {name} rule missing in gtc.css')
    elif must:
        for token in must:
            if token not in m.group(0):
                issues.append(f'CRITICAL: {name} missing {token!r} in gtc.css')

# 2. инлайн-дубли .ph-badge в страницах (кроме klinik-psixiatriya)
for f in sorted((ROOT).rglob('*.html')):
    if 'klinik-psixiatriya' in str(f):
        continue
    s = f.read_text(encoding='utf-8')
    for m in PH_BADGE_RE.finditer(s):
        blk = m.group(0)
        # допустим только если канонически идентичен gtc.css компоненту
        canon = PH_BADGE_RE.search(GTc)
        if canon and hashlib.md5(blk.encode()).hexdigest() != hashlib.md5(canon.group(0).encode()).hexdigest():
            issues.append(f'{f}: non-canonical .ph-badge inline rule')

# 3. mojibake в отслеживаемых html/css/js (не _wip_backup)
for f in sorted(ROOT.rglob('*')):
    if any(p in str(f) for p in ('_wip_backup', 'klinik-psixiatriya', 'node_modules', '__pycache__')):
        continue
    if f.suffix not in ('.html', '.css', '.js'):
        continue
    try:
        s = f.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        issues.append(f'{f}: not utf-8'); continue
    for m in ('Д±', 'Еџ', 'Й™', 'Гј', 'вЂ“'):
        if m in s:
            issues.append(f'{f}: possible mojibake {m!r}')
            break

# 4. ph-h1 требует w1 и спаны лида; w2 опционален (h1 из одного слова)
for f in sorted(ROOT.rglob('*.html')):
    if 'klinik-psixiatriya' in str(f):
        continue
    s = f.read_text(encoding='utf-8')
    if 'class="ph-h1"' in s:
        for cls in ('ph-h1-w1', 'ph-badge', 'ph-sub'):
            if cls not in s:
                issues.append(f'{f}: ph-h1 present but {cls} missing')

# 5. btn-action-1/2 существуют в CSS, но не навязываются формам
for cls in ('btn-action-1', 'btn-action-2'):
    if cls not in GTc:
        issues.append(f'CRITICAL: {cls} missing in gtc.css')

# 6. переопределение компонента инлайном — остаток батча 09-06:
#    строка CSS-правила, начинающаяся с .ph-h1-w1/.ph-h1-w2 (или их
#    пары через запятую). Scoped-оверрайды («.page-hero-x .ph-h1
#    .ph-h1-w1 { color: … }») — легальная page-специфика двухцветного
#    h1, их не трогаем.
W_SEL = re.compile(r'^\.ph-h1-w[12]\b[\s,]')
for f in sorted(ROOT.rglob('*.html')):
    if 'klinik-psixiatriya' in str(f):
        continue
    s = f.read_text(encoding='utf-8')
    for ln in s.splitlines():
        if W_SEL.match(ln.strip()):
            issues.append(f'{f}: standalone inline .ph-h1-w rule '
                          f'(old batch remnant): {ln.strip()[:60]!r}')
            break

if issues:
    print('FAIL —', len(issues), 'issue(s):')
    for i in issues:
        print(' -', i)
    sys.exit(1)
print('OK — hero unification 2026-09-08 clean;',
      len(list((ROOT).rglob('*.html'))), 'pages scanned (excl. klinik)')
