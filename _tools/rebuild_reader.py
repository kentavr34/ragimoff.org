# -*- coding: utf-8 -*-
"""_tools/rebuild_reader.py — пересборка читалки книги из Print одной командой (04.11.2026).

    python _tools/rebuild_reader.py <slug> [az ru en] [--stubs] [--out DIR] [--dry] [--keep-tmp]

Что делает (цепочка BOOK-UPLOAD-STANDARD.md, но во ВРЕМЕННОМ корне, а не в живом сайте):
  1. node _tools/docx-to-book.js _tools/configs/<slug>.json --root <tmp> --langs <langs>
     (DOCX читается встроенным zlib, без tar — одинаково из Git Bash и PowerShell);
  2. python _tools/rebuild-concept.py --book books/<slug> --root <tmp>  → страницы глав с .bk-read;
  3. имена файлов глав приводятся к живым (books/<slug>/<lang>/NN-*.html): глава узнаётся по тексту
     (пересечение слов ≥ 0.5), чтобы адреса не менялись, когда в Print поменялось название главы;
  4. шапки глав: hreflang на главы-близнецы других языков (как на сайте), версия /books/book.css?v=N как
     у живых страниц книги, служебные aria-label на языке страницы (fix-book-chrome-i18n.py);
  5. python _tools/build_reader_books.py <slug> <langs> --stubs --root <tmp> → index.html-читалка,
     страницы глав — заглушки-перенаправления на index.html#chN;
  6. в сайт (или в --out DIR — копию сайта для проверки) копируется index.html каждого языка;
     заглушки глав — только с --stubs. style.css, STRUCTURE.*, чужие файлы не трогаются, ничего не удаляется.
--dry: собрать во временном корне, ничего не копировать (корень остаётся, путь печатается).
Проверка после сборки: python _tools/compare_reader_build.py <DIR> <slug> [langs].
Git-операций не делает.
"""
import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

from bs4 import BeautifulSoup

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(SITE, '_tools')
BASE = 'https://ragimoff.org'
CH_RX = re.compile(r'^\d\d-.*\.html$')
WORD_RX = re.compile(r'\w+', re.U)


def say(*a):
    print(*a, flush=True)


def run(cmd, cwd=SITE):
    env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace', env=env)
    if r.returncode:
        sys.exit('ОШИБКА %s\n%s\n%s' % (' '.join(cmd), r.stdout[-3000:], r.stderr[-3000:]))
    return r.stdout


def read(p):
    with open(p, encoding='utf-8', newline='') as f:
        return f.read()


def write(p, s):
    with open(p, 'w', encoding='utf-8', newline='') as f:
        f.write(s)


def lang_dir(root, slug, lang):
    return os.path.join(root, 'books', slug, '' if lang == 'az' else lang)


def chapter_files(d):
    return sorted(f for f in os.listdir(d) if CH_RX.match(f)) if os.path.isdir(d) else []


def read_words(path):
    s = BeautifulSoup(read(path), 'html.parser').select_one('.bk-read')
    return set(w.lower() for w in WORD_RX.findall(s.get_text(' '))) if s else set()


def jaccard(a, b):
    return len(a & b) / len(a | b) if a and b else 0.0


# ── 3. имена файлов глав как на сайте ─────────────────────────────────────────
def preserve_names(tmp_dir, live_dir, label):
    new_files = chapter_files(tmp_dir)
    live_files = chapter_files(live_dir)
    if not live_files:
        say(f'  {label}: на сайте глав нет — имена новые ({len(new_files)})')
        return {}
    nw = {f: read_words(os.path.join(tmp_dir, f)) for f in new_files}
    lw = {f: read_words(os.path.join(live_dir, f)) for f in live_files}
    pairs = sorted(((jaccard(nw[n], lw[l]), n, l) for n in new_files for l in live_files), reverse=True)
    target, taken = {}, set()
    for score, n, l in pairs:
        if score < 0.5:
            break
        if n in target or l in taken:
            continue
        target[n], taken = l, taken | {l}
    # главы без пары на сайте оставляют своё имя; занятое другим — получают суффикс -x (как в конвертере)
    for n in new_files:
        if n in target:
            continue
        name = n
        while name in taken:
            name = name[:-5] + '-x.html'
        target[n], taken = name, taken | {name}
    renamed = {n: t for n, t in target.items() if n != t}
    unmatched = [n for n in new_files if target[n] not in live_files]
    orphans = sorted(set(live_files) - set(target.values()))
    say(f'  {label}: глав {len(new_files)}, имена с сайта {len(new_files) - len(unmatched)}, '
        f'переименовано {len(renamed)}, новых имён {len(unmatched)}, живых без пары {len(orphans)}')
    for n, t in renamed.items():
        say(f'     {n} → {t}')
    if unmatched:
        say('     без пары на сайте:', ', '.join(target[n] for n in unmatched))
    if orphans:
        say('     на сайте остаются нетронутыми:', ', '.join(orphans))
    if renamed:
        # сначала во временные имена, потом в целевые — иначе цепочка «02→03, 03→04» затирает файлы
        for n in renamed:
            os.rename(os.path.join(tmp_dir, n), os.path.join(tmp_dir, n + '.tmp'))
        for n, t in renamed.items():
            os.rename(os.path.join(tmp_dir, n + '.tmp'), os.path.join(tmp_dir, t))
        rx = re.compile(r'(href=")(%s)(")' % '|'.join(re.escape(n) for n in renamed))
        for f in os.listdir(tmp_dir):
            if f.endswith('.html'):
                p = os.path.join(tmp_dir, f)
                s = read(p)
                s2 = rx.sub(lambda m: m.group(1) + renamed[m.group(2)] + m.group(3), s)
                if s2 != s:
                    write(p, s2)
    return target


# ── 4. шапки глав ─────────────────────────────────────────────────────────────
def css_version(live_dir):
    """Версия book.css у живых страниц книги (bump-css-version.py правит страницы, не генератор)."""
    cnt = {}
    for f in chapter_files(live_dir) + (['index.html'] if os.path.isfile(os.path.join(live_dir, 'index.html')) else []):
        for v in re.findall(r'/books/book\.css\?v=(\d+)', read(os.path.join(live_dir, f))):
            cnt[v] = cnt.get(v, 0) + 1
    return max(cnt, key=cnt.get) if cnt else None


def fix_heads(tmp, slug, cfg, langs, i18n_fix):
    """hreflang на главы других языков с тем же номером NN (как на сайте), версия CSS, aria-label."""
    files = {}
    for L in cfg['langs']:
        code = L['code']
        # живые имена + имена этой сборки (живые страницы без пары остаются на сайте)
        files[code] = {f[:2]: f for f in chapter_files(lang_dir(SITE, slug, code))}
        if code in langs:
            files[code].update({f[:2]: f for f in chapter_files(lang_dir(tmp, slug, code))})
    for code in langs:
        d = lang_dir(tmp, slug, code)
        ver = css_version(lang_dir(SITE, slug, code))
        n_alt = n_css = n_aria = 0
        for f in chapter_files(d):
            p = os.path.join(d, f)
            s = read(p)
            alts = []
            for L in cfg['langs']:
                twin = files[L['code']].get(f[:2])
                if twin:
                    alts.append((L['code'], f'{BASE}/books/{slug}/' + ('' if L['code'] == 'az' else L['code'] + '/') + twin))
            if alts:
                x_default = dict(alts).get('az') or alts[0][1]
                tags = ''.join(f'\n<link rel="alternate" hreflang="{c}" href="{h}">' for c, h in alts)
                tags += f'\n<link rel="alternate" hreflang="x-default" href="{x_default}">'
                s2 = re.sub(r'\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*"\s*/?>', '', s)
                s2 = re.sub(r'(<title>.*?</title>)', lambda m: m.group(1) + '\n' + tags, s2, count=1, flags=re.S)
                if s2 != s:
                    n_alt += 1
                s = s2
            if ver:
                s2 = re.sub(r'/books/book\.css\?v=\d+', '/books/book.css?v=' + ver, s)
                if s2 != s:
                    n_css += 1
                s = s2
            write(p, s)
            if i18n_fix:
                n_aria += i18n_fix(p)
        say(f'  {code}: hreflang {n_alt} стр., book.css?v={ver or "—"} ({n_css} стр.), aria-label {n_aria} правок')


def load_i18n():
    p = os.path.join(TOOLS, 'fix-book-chrome-i18n.py')
    if not os.path.isfile(p):
        return None
    spec = importlib.util.spec_from_file_location('fix_book_chrome_i18n', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return lambda path: m.fix_file(path)


# ── актуальный файл Print ─────────────────────────────────────────────────────
def print_md_files(print_dir):
    """PRINT.md папки Print: {lang: имя .docx} из таблицы «Утверждено к печати»
    (строки «| az | `Файл.docx` + `Файл.pdf` | …»). Старые версии print_gate уносит в versions\\ —
    конфиг с прежним именем тогда указывает в пустоту."""
    p = os.path.join(print_dir, 'PRINT.md')
    if not os.path.isfile(p):
        return {}
    out = {}
    for m in re.finditer(r'^\|\s*(az|ru|en|tr)\s*\|\s*`([^`]+\.docx)`', read(p), re.M | re.I):
        out[m.group(1).lower()] = m.group(2)
    return out


def sync_config_with_print(cfg, langs):
    """Файл языка в конфиге ≠ утверждённому в PRINT.md той же папки → берём PRINT.md. True, если менял."""
    changed = False
    for L in cfg['langs']:
        if L['code'] not in langs:
            continue
        d = os.path.dirname(L['file'])
        cur = print_md_files(d).get(L['code'])
        if cur and cur != os.path.basename(L['file']):
            say(f'  {L["code"]}: в конфиге {os.path.basename(L["file"])}, в PRINT.md — {cur}: беру PRINT.md')
            L['file'] = d + '/' + cur
            changed = True
    return changed


# ── проверки между шагами ─────────────────────────────────────────────────────
def check(tmp, slug, langs, need, what):
    for code in langs:
        d = lang_dir(tmp, slug, code)
        idx = os.path.join(d, 'index.html')
        if not os.path.isfile(idx):
            sys.exit(f'{what}: нет {idx}')
        if need['index'] not in read(idx):
            sys.exit(f'{what}: в {idx} нет {need["index"]}')
        chs = chapter_files(d)
        if not chs:
            sys.exit(f'{what}: в {d} нет страниц глав NN-*.html')
        bad = [f for f in chs if any(k not in read(os.path.join(d, f)) for k in need['chapter'])]
        if bad:
            sys.exit(f'{what}: страницы без {need["chapter"]}: {bad[:5]}')


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
    ap = argparse.ArgumentParser(description='Пересборка читалки книги из Print (см. docstring).')
    ap.add_argument('slug')
    ap.add_argument('langs', nargs='*', help='языки (по умолчанию все из конфига)')
    ap.add_argument('--stubs', action='store_true', help='обновить и заглушки глав (по умолчанию только index.html)')
    ap.add_argument('--out', help='корень КОПИИ сайта для проверки (по умолчанию — сам сайт)')
    ap.add_argument('--dry', action='store_true', help='собрать во временном корне, никуда не копировать')
    ap.add_argument('--keep-tmp', action='store_true')
    a = ap.parse_args()

    cfg_path = os.path.join(TOOLS, 'configs', a.slug + '.json')
    if not os.path.isfile(cfg_path):
        sys.exit('нет конфига ' + cfg_path)
    cfg = json.load(open(cfg_path, encoding='utf-8'))
    all_langs = [L['code'] for L in cfg['langs']]
    langs = a.langs or all_langs
    bad = [l for l in langs if l not in all_langs]
    if bad:
        sys.exit(f'в конфиге {a.slug} нет языков {bad} (есть {all_langs})')
    if sync_config_with_print(cfg, langs):
        with open(cfg_path, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
            f.write('\n')
        say('  конфиг обновлён по PRINT.md:', cfg_path)
    for L in cfg['langs']:
        if L['code'] in langs and not os.path.isfile(L['file']):
            sys.exit('нет файла Print: ' + L['file'])
    say(f'{a.slug}: {", ".join(langs)} ← ' + '; '.join(os.path.basename(L['file']) for L in cfg['langs'] if L['code'] in langs))

    tmp = tempfile.mkdtemp(prefix='rebuild_%s_' % a.slug.replace('-', '_'))
    try:
        # 1. DOCX → страницы старого каркаса
        out = run(['node', os.path.join(TOOLS, 'docx-to-book.js'), cfg_path, '--root', tmp, '--langs', ','.join(langs)])
        say('  ' + ' | '.join(l for l in out.splitlines() if re.match(r'^(az|ru|en|tr):', l)))
        check(tmp, a.slug, langs, {'index': 'class="book-toc"', 'chapter': ['class="content-wrap"']}, 'docx-to-book')

        # 2. каркас концепта (.bk-read)
        out = run([sys.executable, os.path.join(TOOLS, 'rebuild-concept.py'), '--book', 'books/' + a.slug, '--root', tmp, '--quiet'])
        say('  ' + out.strip().splitlines()[0])
        check(tmp, a.slug, langs, {'index': 'bk-toc__list', 'chapter': ['class="bk-read"', 'bk-chead__h1']}, 'rebuild-concept')

        # 3. имена файлов как на сайте
        for code in langs:
            preserve_names(lang_dir(tmp, a.slug, code), lang_dir(SITE, a.slug, code), code)

        # 4. шапки
        fix_heads(tmp, a.slug, cfg, langs, load_i18n())

        # 5. читалка + заглушки
        out = run([sys.executable, os.path.join(TOOLS, 'build_reader_books.py'), a.slug] + langs + ['--stubs', '--root', tmp])
        for l in out.strip().splitlines():
            say('  ' + l.strip())
        for code in langs:
            idx = read(os.path.join(lang_dir(tmp, a.slug, code), 'index.html'))
            if 'class="rd-bar"' not in idx or 'article class="rd-chap"' not in idx:
                sys.exit(f'build_reader_books: {code}/index.html — не читалка')

        if a.dry:
            say('dry: собрано в', tmp, '— ничего не скопировано')
            return

        # 6. в сайт / в копию
        dest_root = os.path.abspath(a.out) if a.out else SITE
        for code in langs:
            src, dst = lang_dir(tmp, a.slug, code), lang_dir(dest_root, a.slug, code)
            os.makedirs(dst, exist_ok=True)
            copied = ['index.html']
            shutil.copyfile(os.path.join(src, 'index.html'), os.path.join(dst, 'index.html'))
            if a.stubs:
                for f in chapter_files(src):
                    shutil.copyfile(os.path.join(src, f), os.path.join(dst, f))
                    copied.append(f)
            else:
                live = set(chapter_files(dst))
                new = set(chapter_files(src))
                if live != new:
                    say(f'  {code}: заглушки не обновлялись (без --stubs); набор глав отличается: '
                        f'нет на сайте {sorted(new - live)}, лишние на сайте {sorted(live - new)}')
                stale = []
                for f in sorted(live & new):
                    old_go = re.search(r'url=index\.html#(ch\d+)', read(os.path.join(dst, f)))
                    new_go = re.search(r'url=index\.html#(ch\d+)', read(os.path.join(src, f)))
                    if old_go and new_go and old_go.group(1) != new_go.group(1):
                        stale.append(f'{f}: {old_go.group(1)}→{new_go.group(1)}')
                if stale:
                    say(f'  {code}: ВНИМАНИЕ — перенаправления живых заглушек не совпадают с новой читалкой '
                        f'({len(stale)}): ' + ', '.join(stale[:6]) + ' — повторите с --stubs')
            say(f'  {code}: → {dst}: {len(copied)} файл(ов)')
        say('готово' + (' (копия сайта: %s)' % dest_root if a.out else ''))
    finally:
        if a.keep_tmp or a.dry:
            say('временный корень:', tmp)
        else:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    main()
