#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""langfix — приводит основной текст языковой версии к правилу «язык версии».

Что делает (и только это — смысл, объём и разметка не меняются):

  1. Утечки: английская фраза в прозе версии заменяется термином языка версии;
     английское написание остаётся один раз, в скобках, при первом упоминании.

  2. Двойное наименование: «Термин (АББР — термин (<en>English</en>))» —
     нативный термин дублируется внутри скобки. Схлопывается до
     «Термин (АББР — <en>English</en>)», как в учебнике.

  3. Глоссарий версии: термин → как пишем в этой версии. Одна форма на всю
     книгу, в том числе внутри <span lang="en"> и в заголовках.

Заголовки не переписываются: их алгоритм отдельный. Глоссарий трогает
заголовок только тогда, когда внутри нашлась форма, которой в языке версии
нет вовсе (случайный английский, не код и не латинское название).

    python _tools/langfix.py az            # разбор, ничего не пишет
    python _tools/langfix.py az --apply
"""
from __future__ import annotations

import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "klinik-psixiatriya"
DIRS = {"az": BOOK, "ru": BOOK / "ru", "en": BOOK / "en", "tr": BOOK / "tr"}

# ── 1. Утечки: точная фраза → замена целиком ────────────────────────────────
# Ключ — файл, значение — список (было, стало). Строка «было» уникальна.
LEAKS: dict[str, list[tuple[str, str]]] = {
    "az": [
        ("6A05.html",
         "— restrictive elimination diet bəzi uşaqlarda",
         "— məhdudlaşdırıcı eliminasiya pəhrizi (restrictive elimination diet) bəzi uşaqlarda"),
        ("6A06.html",
         "(sensor input axtarışı)",
         "(sensor girişi axtarışı)"),
        ("6A06.html",
         "alternativ sensor input.",
         "alternativ sensor girişi."),
        ("6A06.html",
         "pasiyentə sensor input təmin edən",
         "pasiyentə sensor girişi təmin edən"),
        ("6A21.html",
         "ailə psixoedukasiya, supportiv terapiya, IPS supported employment.",
         "ailə psixoedukasiya, dəstəkləyici terapiya, IPS dəstəkli məşğulluq."),
        ("6A72.html",
         "kvalifikatorlar — early/late onset, with/without anxious distress, melanxolik",
         "kvalifikatorlar — erkən/gec başlanğıc (early/late onset), "
         "narahatlıq əlamətləri ilə və ya olmadan (with/without anxious distress), melanxolik"),
        ("6C51.html",
         "bildirilir. American Academy of Sleep Medicine konsensus",
         "bildirilir. Amerika Yuxu Tibbi Akademiyası "
         "(<span lang=\"en\">American Academy of Sleep Medicine</span>) konsensus"),
        ("7A41.html",
         "<strong>CPAP — Continuous Positive Airway Pressure birinci sıra</strong>",
         "<strong>CPAP — davamlı müsbət hava təzyiqi (Continuous Positive Airway Pressure) "
         "— birinci sıra</strong>"),
        ("6C00.html",
         "<td>Specific gravity aşağı.</td>",
         "<td>Xüsusi çəki aşağı.</td>"),
        ("HA02.html",
         "— directed masturbation; vibratör.",
         "— yönləndirilmiş masturbasiya (directed masturbation); vibratör."),
        ("kitab-haqqinda.html",
         "Gender incongruence-in psixiatrik fəsildən çıxarılması;",
         "Gender inkongruensiyasının (gender incongruence) psixiatrik fəsildən çıxarılması;"),
    ],
    "ru": [],
    "en": [],
    "tr": [
        ("6C51.html",
         "bir Netherlands Twin Register çalışmasıdır",
         "Hollanda İkiz Kaydı (Netherlands Twin Register) çalışmasıdır"),
        ("8A05.html",
         "ardışık hareketler — hopping, touching, pirouette;",
         "ardışık hareketler — sıçrama (hopping), dokunma (touching), "
         "dönme (pirouette);"),
    ],
}

# ── 2. Двойное наименование: нативный дубль внутри скобки ───────────────────
# «(<нативный термин> (<span lang="en">English</span>))» → «(<span lang="en">…</span>)»
RE_DOUBLE = re.compile(
    r"\(([^()]{1,40}?—\s*)[^()<>]{4,70}?\(\s*(<span[^>]*lang=\"en\"[^>]*>.*?</span>)\s*\)\s*\)",
    re.S)

# ── 3. Глоссарий версии: как пишем термин в этой версии ─────────────────────
# Ничего не выдумываем: формы взяты из самой книги; каждая пара — это выбор
# одной из уже существующих в книге форм.
GLOSSARY: dict[str, list[tuple[str, str, str]]] = {
    # (что ищем, чем заменяем, почему)
    "az": [
        (r"\bpasiyentə sensor input\b", "pasiyentə sensor girişi", "AZ: sensor girişi"),
        (r"(?<![\w])cravings(?![\w])", "craving", "AZ: без английского мн. -s"),
        (r"\bMayndfulnes\b", "Mindfulness", "одна форма на книгу: Mindfulness"),
        (r"\bsupportiv\b", "dəstəkləyici", "AZ: dəstəkləyici"),
        (r"\bkoqnitiv remediation\b", "koqnitiv bərpa (remediation)", "AZ: bərpa"),
        (r"\blate talker\b", "gec danışan uşaq (late talker)", "AZ: gec danışan uşaq"),
        (r"\bMindfulness əsaslı\b", "Mindfulness-əsaslı", "дефисное написание"),
        # premonitor — заимствованный термин AZ-глоссария («premonitor hissi»);
        # правится только именительная форма, косвенные (hissinə, hissinin) верны
        (r"\bpremonitor hiss\b", "premonitor hissi", "AZ: premonitor hissi"),
        # AZ официальная форма — distres (одна s): так названа глава 6C20
        # («Bədən distresi pozuntusu») и так назван её файл. distress в
        # азербайджанской прозе — та же форма в английском написании.
        (r"Distress", "Distres", "AZ: distres, одна s"),
        (r"distress", "distres", "AZ: distres, одна s"),
    ],
    "ru": [
        (r"(?<![\w])Mindfulness(?![-\w])", "осознанность (mindfulness)", "RU: осознанность"),
        (r"\bМайндфулнес\b", "осознанность", "RU: осознанность"),
        (r"(?<![\w])distress(?![\w])", "дистресс", "RU: дистресс"),
        (r"\bremissiya\b", "ремиссия", "RU: опечатка из AZ"),
        (r"(?<![\w])cravings(?![\w])", "craving", "RU: без английского мн. -s"),
        (r"\bдля late talker\b", "для поздно заговоривших детей (late talker)",
         "RU: расшифровка термина"),
    ],
    "tr": [
        (r"\bPremonitor\b", "Premonitör", "TR: premonitör"),
        (r"\bpremonitor\b", "premonitör", "TR: premonitör"),
        (r"Distress", "Distres", "TR: distres, одна s"),
        (r"distress", "distres", "TR: distres, одна s"),
        (r"(?<![\w])cravings(?![\w])", "craving", "TR: без английского мн. -s"),
    ],
    "en": [],
}

# Заголовки: единственное, что здесь правится, — форма, которой в языке
# версии нет вовсе. Коды и латинские названия не трогаются.
# ── 4. Каркас страницы (шапка, подвал, форма заказа, aria-метки) ─────────────
# Это тоже видимый текст страницы, и на русской странице он не может быть
# азербайджанским. Значения value= и service= не трогаются: их читает бэкенд.
CHROME: dict[str, list[tuple[str, str]]] = {
    "az": [],
    "ru": [
        ('<option value="XBT-11">XBT-11 (ICD-11)</option>',
         '<option value="XBT-11">МКБ-11 (ICD-11)</option>'),
        ('aria-label="Aç / bağla"', 'aria-label="Открыть / закрыть"'),
        ('aria-label="Bağla / Закрыть"', 'aria-label="Закрыть"'),
        ('aria-label="Futermenü"', 'aria-label="Меню подвала"'),
        ("btn.textContent = 'Göndərilir...'", "btn.textContent = 'Отправляется...'"),
        ('<span class="bk-logo__s">Peşəkar nüfuzun ünvanı</span>',
         '<span class="bk-logo__s">Адрес профессиональной репутации</span>'),
    ],
    "en": [
        ('<option value="XBT-11">XBT-11 (ICD-11)</option>',
         '<option value="XBT-11">ICD-11</option>'),
        ('aria-label="Aç / bağla"', 'aria-label="Open / close"'),
        ('aria-label="Bağla / Закрыть"', 'aria-label="Close"'),
        ('aria-label="Futermenü"', 'aria-label="Footer menu"'),
        ("btn.textContent = 'Göndərilir...'", "btn.textContent = 'Sending...'"),
        ('<span class="bk-logo__s">Peşəkar nüfuzun ünvanı</span>',
         '<span class="bk-logo__s">The address of professional reputation</span>'),
    ],
    "tr": [
        ('<option value="XBT-11">XBT-11 (ICD-11)</option>',
         '<option value="XBT-11">ICD-11</option>'),
        ('aria-label="Aç / bağla"', 'aria-label="Aç / kapat"'),
        ('aria-label="Bağla / Закрыть"', 'aria-label="Kapat"'),
        ('aria-label="Futermenü"', 'aria-label="Alt menü"'),
        ("btn.textContent = 'Göndərilir...'", "btn.textContent = 'Gönderiliyor...'"),
        ('<span class="bk-logo__s">Peşəkar nüfuzun ünvanı</span>',
         '<span class="bk-logo__s">Profesyonel itibarın adresi</span>'),
        ('<span class="bk-book__m">ICD-11 · K.Rəhimov · 2026</span>',
         '<span class="bk-book__m">ICD-11 · K. Rahimov · 2026</span>'),
        ('<span class="bk-tp__author">K.Rəhimov</span>',
         '<span class="bk-tp__author">K. Rahimov</span>'),
    ],
}

HEAD_FIXES: dict[str, list[tuple[str, str]]] = {
    "az": [], "ru": [], "en": [], "tr": [],   # заголовок правит глоссарий
}

RE_HEAD = re.compile(r"<(h[1-4])\b([^>]*)>(.*?)</\1>", re.S)
RE_HEAD_BLOCK = re.compile(r"<head\b.*?</head>", re.S | re.I)
RE_ENSPAN = re.compile(r'<span[^>]*lang="en"[^>]*>.*?</span>', re.S)
RE_QUOTED = re.compile(r"«[^»]*»|\u201c[^\u201d]*\u201d")
RE_PLAIN_PAREN = re.compile(r"\([^()]{2,90}\)")


def frozen_ranges(text: str) -> list[tuple[int, int]]:
    """Что не трогаем: head, <span lang="en">, кавычки, английские скобки."""
    out = []
    for rx in (RE_HEAD_BLOCK, RE_ENSPAN, RE_QUOTED):
        out += [(m.start(), m.end()) for m in rx.finditer(text)]
    for m in RE_PLAIN_PAREN.finditer(text):
        inner = m.group(0)[1:-1]
        if (inner.isascii() and " " in inner
                and not re.search(r"[əıƏİşŞğĞçÇöÖüÜ]", inner)):
            out.append((m.start(), m.end()))
    return out


def sub_outside(text: str, pat: str, repl: str) -> tuple[str, int]:
    """re.sub, но только вне «замороженных» участков."""
    frozen = frozen_ranges(text)
    if not frozen:
        return re.subn(pat, repl, text)
    mark = [False] * len(text)
    for a, b in frozen:
        for i in range(a, min(b, len(text))):
            mark[i] = True
    rx = re.compile(pat)
    out, pos, n = [], 0, 0
    while True:
        m = rx.search(text, pos)
        if not m:
            out.append(text[pos:])
            break
        if any(mark[i] for i in range(m.start(), min(m.end(), len(text)))):
            out.append(text[pos:m.end()])
            pos = m.end()
            continue
        out.append(text[pos:m.start()])
        out.append(m.expand(repl))
        pos = m.end()
        n += 1
    return "".join(out), n


def main() -> int:
    lg = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in DIRS else "az"
    apply = "--apply" in sys.argv
    folder = DIRS[lg]
    by_file: dict[str, list[tuple[str, str]]] = {}
    for fname, old, new in LEAKS[lg]:
        by_file.setdefault(fname, []).append((old, new))

    stat, files = Counter(), 0
    for fp in sorted(folder.glob("*.html")):
        raw = fp.read_bytes().decode("utf-8")
        crlf = raw.count("\r\n") > raw.count("\n") // 2
        t = new = raw.replace("\r\n", "\n")

        # 1 — утечки: заменяется ровно то место, которое названо в таблице
        for old, rep in by_file.get(fp.name, []):
            if old not in new:
                stat[f"НЕ НАЙДЕНО [{fp.name}]: {old[:50]}"] += 1
                continue
            new = new.replace(old, rep, 1)
            stat["утечка: английская фраза → термин версии"] += 1

        # 2 — двойное наименование: нативный дубль внутри скобки схлопывается
        def collapse(m: re.Match) -> str:
            stat["двойное наименование (ABB — дубль (English))"] += 1
            return f"({m.group(1)}{m.group(2)})"
        new = RE_DOUBLE.sub(collapse, new)

        # 3 — глоссарий версии: вне <head>, <span lang="en">, кавычек и
        #     английских скобок (там иноязычное написание стоит по праву)
        for pat, rep, why in GLOSSARY[lg]:
            new, n = sub_outside(new, pat, rep)
            if n:
                stat[f"{why} ×{n}"] += n

        # 4 — каркас страницы: шапка, подвал, форма заказа, aria-метки
        for a, b in CHROME[lg]:
            if a in new:
                stat[f"каркас: {a[:40]}…"] += new.count(a)
                new = new.replace(a, b)

        # 5 — заголовки: только форма, которой в языке версии нет вовсе
        if HEAD_FIXES[lg]:
            def head(m: re.Match) -> str:
                inner = m.group(3)
                for a, b in HEAD_FIXES[lg]:
                    if a in inner:
                        stat[f"заголовок: {a} → {b}"] += 1
                        inner = inner.replace(a, b)
                return f"<{m.group(1)}{m.group(2)}>{inner}</{m.group(1)}>"
            new = RE_HEAD.sub(head, new)

        if new == t:
            continue
        files += 1
        if apply:
            fp.write_bytes((new.replace("\n", "\r\n") if crlf else new).encode("utf-8"))
    print(f"[{lg}] файлов затронуто: {files}")
    for k, v in stat.most_common():
        print(f"    {k}  ×{v}")
    print("применено" if apply else "пробный прогон — запустить с --apply")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
