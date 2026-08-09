# -*- coding: utf-8 -*-
"""
refcheck.py — кого книга цитирует в тексте, но не приводит в списке литературы.

Учебник ссылается на исследования прямо в тексте («Rascovsky K. et al. Brain
2011»), а §11 «Мənbələr» должен эти работы содержать. Расхождение означает,
что читатель не может проверить утверждение — для медицинского учебника это
дефект того же класса, что неверная доза.

Проверяется только азербайджанский мастер: списки литературы во всех четырёх
языках совпадают, поэтому пропуск одинаков везде.

    python refcheck.py            # отчёт
    python refcheck.py --json     # _refcheck.json
"""
from __future__ import annotations
import re, sys, io, json, html as H
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
BOOK = ROOT / 'klinik-psixiatriya'
CARD = re.compile(r'(6[A-E][0-9A-Z]{2}|7[AB][0-9A-Z]{2}|8A05|HA[0-9A-Z]{2}|GA34)')
LOOSE = re.compile(r'<(?![a-zA-Z/!?])')

# «Rascovsky K.», «Gorno-Tempini M.L.», «McKeith IG» — фамилия + инициалы
NAME = re.compile(r'\b([A-Z][a-zA-Zöüçğışä\'’-]{3,}(?:-[A-Z][a-zA-Z]+)?)\s+'
                  r'(?:[A-Z]\.){1,3}(?:\s*[A-Z]\.)?')
# «Marconi 2016», «Petersen 1999» — фамилия + год
NAMEYEAR = re.compile(r'\b([A-Z][a-zA-Zöüçğışä\'’-]{3,})\s+((?:19|20)\d{2})\b')

# слова, которые выглядят как фамилии, но ими не являются
STOP = {
    'Cochrane', 'Lancet', 'JAMA', 'NEJM', 'Neurology', 'Brain', 'NICE', 'WHO',
    'DSM', 'ICD', 'FDA', 'EMA', 'APA', 'WFSBP', 'SAMHSA', 'CANMAT', 'NIMH',
    'AACAP', 'AAP', 'ISSTD', 'ICCS', 'WPATH', 'SAMHSA', 'AASM', 'AUA', 'EAU',
    'Psychiatry', 'Psychol', 'Psychiatr', 'Bull', 'Acta', 'Arch', 'Ther',
    'Disord', 'Assoc', 'Depend', 'Alcohol', 'Drug', 'Child', 'Adolesc',
    'Neurosci', 'Neuropsychopharmacol', 'Biol', 'Clin', 'Gen', 'Int', 'Eur',
    'Behav', 'Health', 'Prof', 'Sleep', 'Pediatr', 'Urol', 'Sex', 'Marital',
    'Addict', 'Dis', 'Med', 'Rev', 'Res', 'Syst', 'Database', 'Update',
    'Guideline', 'Guidelines', 'Trial', 'Study', 'Group', 'Report',
    'Section', 'Level', 'Type', 'Scale', 'Test', 'Score', 'Index',
    'Sindromu', 'Birliyi', 'Nazirliyi', 'Respublikası', 'Xəstəlik',
}


def parts(fp: Path):
    """Видимый текст: (§3–§10 — доказательная часть, §2 «История», список литературы).

    §2 разбирается отдельно: там Charcot, Janet, Bowlby названы как авторы
    исторического приоритета, а не как доказательство утверждения. Требовать
    для них записи в списке литературы — значит завалить отчёт шумом и
    похоронить настоящие пропуски.
    """
    t = fp.read_text(encoding='utf-8', errors='ignore')
    m = re.search(r'<main[\s\S]*?</main>', t, re.I)
    t = m.group(0) if m else t
    r = re.search(r'<ol class="ref-list">[\s\S]*?</ol>', t)
    refs = r.group(0) if r else ''
    body = t.replace(refs, ' ') if refs else t
    h2 = re.search(r'<h2[^>]*id="[^"]*-2-[^"]*"[\s\S]*?(?=<h2)', body)
    hist = h2.group(0) if h2 else ''
    if hist:
        body = body.replace(hist, ' ')

    def vis(x):
        return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]*>', ' ', LOOSE.sub('&lt;', x))))
    return vis(body), vis(hist), vis(refs)


def surnames(text):
    out = set()
    for m in NAME.finditer(text):
        out.add(m.group(1))
    for m in NAMEYEAR.finditer(text):
        out.add(m.group(1))
    return {s for s in out if s not in STOP}


def main() -> int:
    codes = sorted({p.stem for p in BOOK.glob('*.html') if CARD.fullmatch(p.stem)})
    report, total = {}, 0
    for c in codes:
        body, hist, refs = parts(BOOK / f'{c}.html')
        seen = (refs + ' ' + hist).lower()
        missing = sorted(s for s in surnames(body) if s.lower() not in seen)
        if missing:
            report[c] = missing
            total += len(missing)
    if '--json' in sys.argv:
        (ROOT / '_refcheck.json').write_text(json.dumps(report, ensure_ascii=False, indent=1),
                                             encoding='utf-8')
        print('отчёт записан в _refcheck.json')
        return 1 if total else 0
    print('=' * 72)
    print('ЦИТИРУЕТСЯ В ТЕКСТЕ, ОТСУТСТВУЕТ В СПИСКЕ ЛИТЕРАТУРЫ')
    print('=' * 72)
    for c, names in report.items():
        print(f'  {c}: {", ".join(names)}')
    print(f'\nкарточек с пропусками: {len(report)}, имён: {total}')
    print('Ложные срабатывания возможны — перед правкой сверять глазами.')
    return 1 if total else 0


if __name__ == '__main__':
    raise SystemExit(main())
