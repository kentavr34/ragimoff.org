"""Terminology sync — применяет ОДОБРЕННЫЕ правки из _corrections/PENDING.json.

WORKFLOW
========
1. Читатель нажимает ✎ Düzəlt на странице → POST в Cloudflare Worker
   → Worker дописывает {status:"pending", original, proposed, note, url} в
     _corrections/PENDING.json через GitHub API.
2. Вы открываете _corrections/PENDING.json на GitHub и меняете
   "status": "pending" → "approved" у тех правок, что принимаете.
3. Запускаете `python _term_sync.py --dry-run` — смотрите, что будет изменено.
4. Запускаете `python _term_sync.py --apply` — правка применяется.

ЧТО ИЗМЕНИЛОСЬ И ПОЧЕМУ (2026-08-06)
====================================
Прежняя версия обходила klinik-psixiatriya рекурсивно через os.walk и делала
слепой str.replace. В результате правка, сделанная на азербайджанской странице,
записывалась ещё и в ru/, en/, tr/ и preview/ — 1967 файлов вместо 427. Именно
так в турецкую версию попали 2953 азербайджанских слова.

Теперь:
  * язык берётся из поля url записи и правка применяется ТОЛЬКО к этому языку;
  * замена идёт по границам слова, а не по подстроке;
  * защищены все атрибуты тегов, а не только title (раньше href/id/class/data-*
    можно было испортить молча);
  * preview/ не трогается — это производная сборка;
  * правки, где original совпадает с proposed, отклоняются как пустые;
  * без флага --apply скрипт ничего не пишет.
"""
from __future__ import annotations
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent
PENDING_FILE = ROOT / "_corrections" / "PENDING.json"
BOOK = ROOT / "klinik-psixiatriya"

# каталог каждого языка; preview/ намеренно отсутствует — это сборка, не источник
LANG_DIRS = {
    "az": [BOOK, ROOT / "_supplements" / "chapters-v2"],
    "ru": [BOOK / "ru"],
    "en": [BOOK / "en"],
    "tr": [BOOK / "tr"],
}

PROTECT_REF = re.compile(r'<ol class="ref-list">[\s\S]*?</ol>', re.IGNORECASE)
PROTECT_TAG = re.compile(r'<[^>]+>')            # любой тег целиком, вместе с атрибутами
PROTECT_HEAD = re.compile(r'<head\b[\s\S]*?</head>', re.IGNORECASE)
PROTECT_SCRIPT = re.compile(r'<(script|style)\b[\s\S]*?</\1>', re.IGNORECASE)

WORD = r'[0-9A-Za-zА-Яа-яЁёƏəĞğIıİiÖöŞşÜüÇç]'


def lang_of(url: str) -> str:
    """Язык страницы, на которой сделана правка. По умолчанию — азербайджанский мастер."""
    m = re.search(r'/klinik-psixiatriya/(ru|en|tr)/', url or '')
    return m.group(1) if m else 'az'


def files_for(lang: str):
    out = []
    for d in LANG_DIRS.get(lang, []):
        if d.is_dir():
            out += sorted(d.glob('*.html'))
    return out


def apply_replacement(orig: str, prop: str, files):
    """Заменяет orig → prop только в видимом тексте, по границам слова.
    Возвращает (число замен, число файлов)."""
    if not orig or not prop or orig == prop:
        return 0, 0
    # границы слова только там, где строка начинается/кончается буквой или цифрой
    left = rf'(?<!{WORD})' if re.match(WORD, orig) else ''
    right = rf'(?!{WORD})' if re.search(WORD + r'$', orig) else ''
    rx = re.compile(left + re.escape(orig) + right)

    total_count = total_files = 0
    for p in files:
        try:
            d = p.read_text(encoding="utf-8")
        except Exception:
            continue
        stash = []

        def stash_fn(m):
            stash.append(m.group(0))
            return f"\x00P{len(stash)-1}\x00"

        work = PROTECT_HEAD.sub(stash_fn, d)
        work = PROTECT_SCRIPT.sub(stash_fn, work)
        work = PROTECT_REF.sub(stash_fn, work)
        work = PROTECT_TAG.sub(stash_fn, work)      # теги и все их атрибуты
        work, n = rx.subn(prop, work)
        if not n:
            continue
        work = re.sub(r'\x00P(\d+)\x00', lambda m: stash[int(m.group(1))], work)
        if work != d:
            p.write_text(work, encoding="utf-8")
            total_count += n
            total_files += 1
    return total_count, total_files


def main():
    apply_mode = '--apply' in sys.argv
    entries = json.loads(PENDING_FILE.read_text(encoding="utf-8")) if PENDING_FILE.exists() else []
    if not entries:
        print("PENDING.json пуст — делать нечего.")
        return

    approved = [e for e in entries if e.get("status") == "approved"]
    print(f"записей всего: {len(entries)}")
    for st in ("pending", "approved", "applied", "rejected"):
        print(f"   {st}: {sum(1 for e in entries if e.get('status') == st)}")
    if not approved:
        print("\nОдобренных правок нет.")
        return

    print()
    grand = 0
    for entry in approved:
        orig = (entry.get("original") or "").strip()
        prop = (entry.get("proposed") or "").strip()
        lang = lang_of(entry.get("url", ""))

        if not orig or not prop:
            print(f"  ПРОПУСК (пустое поле): {orig[:40]!r}")
            continue
        if orig == prop:
            entry["status"] = "rejected"
            entry["reject_reason"] = "original и proposed совпадают — правка пустая"
            print(f"  ОТКЛОНЕНО (пустая правка): {orig[:50]!r}")
            continue

        files = files_for(lang)
        if apply_mode:
            cnt, nf = apply_replacement(orig, prop, files)
            entry["status"] = "applied"
            entry["applied_ts"] = datetime.now(timezone.utc).isoformat()
            entry["applied_count"] = cnt
            entry["applied_lang"] = lang
        else:
            cnt = sum(1 for p in files if orig in p.read_text(encoding="utf-8", errors="ignore"))
            nf = cnt
        grand += cnt
        print(f"  [{lang}] {orig[:44]!r} → {prop[:44]!r}: {cnt} в {nf} файлах "
              f"(область: {len(files)} файлов языка {lang})")
        if cnt == 0:
            print(f"        ⚠ ни одного вхождения — текст мог быть уже изменён")

    if apply_mode:
        PENDING_FILE.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n",
                                encoding="utf-8")
        print(f"\nПРИМЕНЕНО: {grand} замен. PENDING.json обновлён.")
        print("Дальше вручную: _build_abbreviatur.py · _rebuild_book_nav.py · build_book.py")
    else:
        print(f"\nПРОБНЫЙ ПРОГОН: было бы затронуто {grand} вхождений.")
        print("Для применения запустите: python _term_sync.py --apply")


if __name__ == "__main__":
    main()
