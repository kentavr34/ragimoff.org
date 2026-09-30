#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""site-grammar — текстовый аудит страниц сайта (корень / ru / en).

Что проверяет по каждому языку версии:
  1. двойной пробел внутри одного текстового узла;
  2. пробел перед знаком пунктуации / отсутствие пробела после;
  3. повтор слова подряд («и и», «вə вə»);
  4. чужая письменность: кириллица или азербайджанские буквы в английской
     версии, английские служебные слова в русской/азербайджанской;
  5. незакрытые скобки/кавычки на странице;
  6. длинные латинские простыни (2+ английских слова подряд) вне скобок и
     кавычек — «полуанглийские вкрапления»;
  7. лишние пробелы в начале/конце строки в разметке, «.,», «..», «?!».

Запуск:
    python _tools/site-grammar.py --out D:/audit
    python _tools/site-grammar.py --out D:/audit --pages tehsil.html
Пишет <out>/grammar.tsv и <out>/text/<page>.txt (видимый текст).
"""
from __future__ import annotations
import argparse
import html as H
import io
import json
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RE_SCRIPT = re.compile(r"<(script|style)\b[^>]*>[\s\S]*?</\1>", re.I)
RE_COMMENT = re.compile(r"<!--[\s\S]*?-->")
RE_TAG = re.compile(r"<[^>]+>")
RE_BLOCK_END = re.compile(r"</(p|div|li|h[1-6]|td|th|section|article|figcaption|blockquote|tr)\s*>", re.I)
RE_NAV = re.compile(r"<(nav|header|footer)\b[\s\S]*?</\1>", re.I)
RE_MENU = re.compile(r'<div[^>]*id="(mobileNav|mobile-nav|kitab-modal)"[\s\S]*?</div>\s*(?=<)', re.I)

# Служебная английская лексика — в тексте AZ/RU ей делать нечего. Список
# намеренно УЗКИЙ: короткие слова вроде blog/book/menu/online в навигации и
# заголовках совпадают с азербайджанскими и давали ложные срабатывания.
EN_STOP = set("""the and with for you your our from this that these those are was were will would
should have has had not but what when where which who whom whose how why into over under between
about after before during without within through across upon onto than then also only just very
much many such same each both few own too here there while because please click details reviews
us are there their they them its it's don't doesn't isn't aren't""".split())

BRANDS = set("""WhatsApp YouTube TikTok PowerPoint LinkedIn iPhone iPad macOS iOS WiFi GitHub PayPal Zoom
Google Chrome Windows Word Excel PDF PDFs SEO SMM CRM API IPAS BPA EMDR CBT DSM ICD XBT MKБ
RAGIMOFF Instagram Facebook Telegram Viber Twitter Xbox PlayStation Netflix Spotify Coursera Udemy
AZ RU EN TR Russian English Azerbaijan Turkish""".split())

RE_EN_RUN = re.compile(r"\b(?:[A-Za-z][A-Za-z'’-]{1,})\b(?:\s+\b(?:[A-Za-z][A-Za-z'’-]{1,})\b)+")
RE_AZ_DIAC = re.compile(r"[əüöğışçƏÜÖĞİŞÇ]")
# «a)», «1)» — нумерация: закрывающая скобка без парной открывающей
RE_ENUM = re.compile(r"(?:^|[\s;:])(?:[a-zа-я]|\d{1,2})\)")
RE_LATIN_WORD = re.compile(r"[A-Za-z][A-Za-z'’-]+")
RE_CYR = re.compile(r"[\u0400-\u04FF]")
RE_AZL = re.compile(r"[əƏ]")
RE_RU_STOP = set("""и в во не что он на я с со как а то все она так его но да ты к у же вы за бы по только
ее мне было вот от меня еще нет о из ему теперь когда даже ну вдруг ли если уже или ни быть был него до
вас нибудь опять уж вам ведь там потом себя ничего ей может они тут где есть надо ней для мы тебя их чем
была сам чтоб без будто чего раз тоже себе под будет ж тогда кто этот того потому этого какой совсем ним
здесь этом один почти мой тем чтобы нее сейчас были куда зачем всех никогда можно при наконец два об
другой хоть после над больше тот через эти нас про всего них какая много разве три эту моя впрочем хорошо
свою этой перед иногда лучше чуть том нельзя такой им более всегда конечно всю между""".split())


def visible_text(html: str) -> str:
    s = RE_SCRIPT.sub(" ", html)
    s = RE_COMMENT.sub(" ", s)
    s = RE_NAV.sub(" ", s)
    s = RE_BLOCK_END.sub(" \n", s)
    s = s.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    s = RE_TAG.sub(" ", s)
    s = H.unescape(s)
    return s


def text_nodes(html: str):
    s = RE_SCRIPT.sub(" ", html)
    s = RE_COMMENT.sub(" ", s)
    for chunk in RE_TAG.split(s):
        yield H.unescape(chunk)


def page_lang(html: str) -> str:
    m = re.search(r'<html[^>]*\blang\s*=\s*["\']([a-zA-Z-]+)', html)
    return (m.group(1)[:2].lower() if m else "az")


def strip_quoted(text: str) -> str:
    """Заменить содержимое скобок/кавычек и коды классификаций на «q».
    Именно на букву, а не на пробел: если стереть «…» пробелом, из
    `«X», «Y».` получится `,  ,  .` — фальшивая «сдвоенная пунктуация»."""
    t = re.sub(r"\([^()]*\)", "q", text)
    t = re.sub(r"«[^»]*»", "q", t)
    t = re.sub(r"„[^“]*“", "q", t)
    t = re.sub(r'"[^"]*"', "q", t)
    t = re.sub(r"\b(?:[A-ZА-Я]{2,}-\d+|[A-Z]\d{2}(?:\.\d+)?|[0-9][A-Z]?\d{2}[A-Z]?)\b", "q", t)
    return t


def check_page(rel: str, html: str):
    rows = []
    lang = page_lang(html)
    text = visible_text(html)

    def add(typ, desc, was):
        rows.append((rel, typ, desc, was, ""))

    # 1. двойные пробелы внутри текстового узла
    for chunk in text_nodes(html):
        for m in re.finditer(r"\S {2,}\S", chunk):
            add("text", "двойной пробел", "«" + m.group(0)[:40] + "»")

    # 2. пробелы вокруг пунктуации
    for m in re.finditer(r"\S\s+[,.;:!?](?:\s|$)", text):
        add("text", "пробел перед знаком препинания", "«" + re.sub(r"\s+", "·", m.group(0))[:40] + "»")
    for m in re.finditer(r"[,;:][А-Яа-яЁёƏəİıĞğŞşÇçÖöÜüA-Za-z]{2,}", text):
        add("text", "нет пробела после знака препинания", "«" + m.group(0)[:40] + "»")
    for m in re.finditer(r"[.,]{2,}(?![.])|\?!|\!\?", text):
        add("text", "сдвоенный знак препинания", "«" + m.group(0)[:20] + "»")

    # 3. повтор слова
    for m in re.finditer(r"\b([A-Za-zА-Яа-яЁёƏəİıĞğŞşÇçÖöÜü]{3,})\s+\1\b", text, re.I):
        add("text", "слово повторено дважды", "«" + m.group(0)[:40] + "»")

    # 4. чужая письменность
    if lang == "az":
        cy = RE_CYR.findall(strip_quoted(text))
        if cy:
            add("lang", "кириллица в азербайджанском тексте", "".join(sorted(set(cy)))[:20])
    if lang == "ru":
        az = RE_AZL.findall(strip_quoted(text))
        if az:
            add("lang", "азербайджанские буквы в русском тексте", "".join(sorted(set(az)))[:20])
    if lang == "en":
        other = RE_CYR.findall(strip_quoted(text)) + RE_AZL.findall(strip_quoted(text))
        if other:
            add("lang", "чужая письменность в английском тексте", "".join(sorted(set(other)))[:20])

    # 5. скобки/кавычки
    for op, cl, name in (("(", ")", "круглых"), ("«", "»", "ёлочек"), ("[", "]", "квадратных")):
        d = text.count(op) - text.count(cl)
        if d != 0:
            add("text", f"незакрытые {name} скобки: {d:+d}", f"{text.count(op)}/{text.count(cl)}")

    # 6. английские простыни вне скобок и кавычек
    if lang in ("az", "ru"):
        clean = strip_quoted(text)
        for m in RE_EN_RUN.finditer(clean):
            words = [w for w in re.split(r"\s+", m.group(0)) if w]
            if len(words) < 2:
                continue
            if all(w in BRANDS for w in words):
                continue
            if any(w.lower() in EN_STOP for w in words) or len(words) >= 3:
                add("lang", "английская фраза вне скобок", "«" + m.group(0)[:60] + "»")

    # 7. мусор в разметке: пробел перед закрывающим тегом текста
    return rows


def pages_list(arg=None):
    if arg:
        return [p.strip() for p in arg.split(",") if p.strip()]
    out = []
    for name in sorted(os.listdir(ROOT)):
        if name.endswith(".html") and not name.startswith("_"):
            out.append(name)
    for sub in ("ru", "en"):
        d = os.path.join(ROOT, sub)
        if os.path.isdir(d):
            for name in sorted(os.listdir(d)):
                if name.endswith(".html") and not name.startswith("_"):
                    out.append(sub + "/" + name)
    return out


def check_rendered(rel: str, text: str, lang: str):
    """Проверки по ОТРИСОВАННОМУ тексту (innerText): то, что читает человек.
    Внутристрочные проверки идут по строкам: строка innerText — это видимый
    блок, поэтому склейки между блоками (меню, колонки) не дают ложных пар."""
    rows = []

    def add(typ, desc, was):
        rows.append((rel, typ, desc, was, ""))

    lines = [ln for ln in text.split("\n")]
    # всё от заголовка списка источников до конца — библиография: язык
    # оригинала там законен (правило владельца), поэтому блок не проверяем
    RE_BIBHEAD = re.compile(r"^\s*(Mənbələr|İstifadə (olunmuş|edilmiş)|Ədəbiyyat|Sources|References|"
                            r"Источники|Литература|Список литературы)\b", re.I)
    for i, ln in enumerate(lines):
        if RE_BIBHEAD.match(ln):
            lines = lines[:i]
            break
    # строка библиографии/источника — язык оригинала законен, не проверяем
    RE_BIB = re.compile(r"\b(?:19|20)\d{2}\b|et al\.|doi:|https?://|\bpp\.|\bvol\.|\bed\.\b")
    lines = [ln for ln in lines if not RE_BIB.search(ln)]
    for ln in lines:
        for m in re.finditer(r"\S {2,}\S", ln):
            add("text", "двойной пробел", "«" + m.group(0)[:40] + "»")
        for m in re.finditer(r"\S[ \t]+[,.;:!?](?=\s|$)", ln):
            add("text", "пробел перед знаком препинания", "«" + re.sub(r"\s+", "·", m.group(0))[:40] + "»")
        for m in re.finditer(r"\b([A-Za-zА-Яа-яЁёƏəİıĞğŞşÇçÖöÜü]{3,})[ \t]+\1\b", ln, re.I):
            add("text", "слово повторено дважды", "«" + m.group(0)[:40] + "»")
        bare = strip_quoted(ln)          # внутри «…», (…) знаки — часть примера
        for m in re.finditer(r"(?<!\.)\.\.(?!\.)|\.\s*,|,\s*\.|\?!|\!\?|!!", bare):
            add("text", "сдвоенный знак препинания", "«" + m.group(0)[:20] + "»")
        for m in re.finditer(r"[,;:][^\s\d)\"'»]", ln):
            add("text", "нет пробела после знака препинания", "«" + m.group(0)[:30] + "»")

    for w in mixed_script_words("\n".join(lines)):
        add("typo", "слово со смешанными алфавитами (латиница + кириллица)", "«" + w + "»")

    # переключатель языков («Русский») — кириллица по праву, не дефект
    content = [ln for ln in lines
               if not re.match(r"^\s*(Русский|English|Azərbaycanca|Azərbaycan dili|AZ|RU|EN)\s*$", ln, re.I)]
    clean = strip_quoted("\n".join(content))
    if lang == "az":
        cy = RE_CYR.findall(clean)
        if cy:
            add("lang", "кириллица в азербайджанском тексте", "".join(sorted(set(cy)))[:20])
    if lang == "ru":
        az = RE_AZL.findall(clean)
        if az:
            add("lang", "азербайджанские буквы в русском тексте", "".join(sorted(set(az)))[:20])
    if lang == "en":
        other = RE_CYR.findall(clean) + RE_AZL.findall(clean)
        if other:
            add("lang", "чужая письменность в английском тексте", "".join(sorted(set(other)))[:20])
    if lang in ("az", "ru"):
        for m in RE_EN_RUN.finditer(clean):
            words = [w for w in re.split(r"\s+", m.group(0)) if w]
            if len(words) < 2 or all(w in BRANDS for w in words):
                continue
            if RE_AZ_DIAC.search(m.group(0)):     # азербайджанские буквы — не английское
                continue
            stops = [w for w in words if w.lower() in EN_STOP]
            if len(stops) >= 2 or (len(stops) >= 1 and len(words) >= 3):
                add("lang", "английская фраза вне скобок", "«" + m.group(0)[:70] + "»")

    # Баланс скобок считается по строке: «a)», «b)» — это нумерация, её
    # закрывающая скобка не парная. По всей странице считать нельзя: абзац,
    # начавшийся на одной строке innerText и продолжающийся на следующей,
    # уходил в минус и давал ложные «незакрытые скобки».
    # Скобки: нумерация «a)»/«1)» даёт лишние ЗАКРЫВАЮЩИЕ, поэтому реальная
    # нехватка закрывающей видна как перебор ОТКРЫВАЮЩИХ по странице.
    # (Проверять построчно нельзя: «(week 3)» — это скобка, а не нумерация.)
    body = "\n".join(lines)
    op, cl = body.count("("), body.count(")")
    if op > cl:
        add("text", "незакрытые круглые скобки: +%d" % (op - cl), "%d/%d" % (op, cl))
    dq = body.count("«") - body.count("»")
    if dq:
        add("text", "незакрытые ёлочки: %+d" % dq, "%d/%d" % (body.count("«"), body.count("»")))
    return rows


RE_WORDC = re.compile(r"[A-Za-zƏəÜüÖöĞğŞşÇçİıА-Яа-яЁё]{4,}")


# одинаково выглядящие буквы двух алфавитов — смесь их в одном слове это сбой
LATIN = set("ABCEHKMOPTXYacehkmopxtyi")
CYRIL_LOOK = set("АВСЕНКМОРТХУасеһкморtхуі")
CONFUSE = [("a", "ə"), ("e", "ə"), ("i", "ı"), ("i", "İ"), ("o", "ö"), ("u", "ü"),
           ("s", "ş"), ("c", "ç"), ("g", "ğ"), ("q", "g"), ("x", "h"), ("k", "q")]
DOUBLE_OK = {"nn": "n", "ll": "l", "ss": "s", "pp": "p", "tt": "t", "mm": "m", "rr": "r", "ff": "f"}


def mixed_script_words(text):
    """Слова, где латиница и кириллица перемешаны — почти всегда опечатка."""
    out = []
    for w in RE_WORDC.findall(text):
        has_l = any(c.isascii() and c.isalpha() for c in w)
        has_c = bool(RE_CYR.search(w))
        if has_l and has_c:
            out.append(w.lower())
    return out


def az_lower(w):
    """Азербайджанская пара букв: I → ı, İ → i. Обычный str.lower() делает из
    «HANSI» «hansi» и портит проверку (верная строчная форма — «hansı»)."""
    return w.replace("I", "ı").replace("İ", "i").lower()


def typo_candidates(texts, lang="az"):
    """Опечатки без словаря: редкое слово, отличающееся от частого на одну
    «подозрительную» правку — диакритику (a/ə, i/ı, s/ş…), удвоение буквы или
    смесь латиницы с кириллицей. Для агглютинативного азербайджанского любые
    другие замены — это обычно разные падежные формы, а не опечатки."""
    from collections import Counter
    fold = az_lower if lang == "az" else (lambda w: w.lower())
    cnt = Counter()
    for t in texts:
        for w in RE_WORDC.findall(t):
            cnt[fold(w)] += 1
    hot = {w: c for w, c in cnt.items() if c >= 8}
    seen = set()
    out = []
    for w, c in cnt.items():
        if c > 3 or len(w) < 5:
            continue
        for h, hc in hot.items():
            if h == w or len(h) != len(w) or hc < c * 6:
                continue
            diffs = [(a, b) for a, b in zip(h, w) if a != b]
            ok = False
            if len(diffs) == 1:
                a, b = diffs[0]
                ok = any({a, b} == set(p) for p in CONFUSE)
            if not ok:
                # удвоение буквы: «террапия» ↔ «терапия»
                for d, s in DOUBLE_OK.items():
                    if (d in h and s in w) or (d in w and s in h):
                        ok = re.sub(d, s, h) == re.sub(d, s, w)
                        if ok:
                            break
            if ok:
                key = (w, h)
                if key not in seen:
                    seen.add(key)
                    out.append((w, c, h, hc))
                break
    return sorted(out, key=lambda r: (r[1], r[0]))


def rendered_pages(rdir):
    """Собирает отрисованный текст по странице из rendered/<page>.txt и @ширина."""
    by_page = {}
    for name in sorted(os.listdir(rdir)):
        if not name.endswith(".txt"):
            continue
        page = name[:-4]
        w = ""
        if "@" in page:
            page, w = page.split("@", 1)
        page = page.replace("__", "/")
        by_page.setdefault(page, []).append(os.path.join(rdir, name))
    return by_page


def lang_of(rel):
    return rel.split("/")[0] if rel.split("/")[0] in ("ru", "en") else "az"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="D:/Документы/ZFreud/_align/site_audit")
    ap.add_argument("--pages", default=None)
    ap.add_argument("--rendered", default=None,
                    help="каталог rendered/ с innerText-выгрузкой (site-audit.js --text)")
    ap.add_argument("--only", default=None, help="фильтр типа дефекта: text|lang")
    args = ap.parse_args()

    if args.rendered:
        rows = []
        typo_pool = {"az": [], "ru": [], "en": []}
        for page, files in sorted(rendered_pages(args.rendered).items()):
            text = ""
            for fp in files:
                with open(fp, encoding="utf-8") as f:
                    text += f.read() + "\n"
            if text.startswith("PROBE-FAIL"):
                rows.append((page, "file", "нет отрисованного текста", text[:80], ""))
                continue
            typo_pool.setdefault(lang_of(page), []).append(text)
            rows.extend(check_rendered(page, text, lang_of(page)))

        tsv_typos = os.path.join(args.out, "grammar_typos.tsv")
        with open(tsv_typos, "w", encoding="utf-8") as f:
            f.write("lang\tword\tcount\tnear\tcount_near\n")
            for lang, texts in typo_pool.items():
                if not texts:
                    continue
                for w, c, h, hc in typo_candidates(texts, lang):
                    f.write(f"{lang}\t{w}\t{c}\t{h}\t{hc}\n")
                    rows.append(("(все страницы " + lang + ")", "typo?", f"редкое написание «{w}» ↔ частое «{h}»", f"{c} против {hc}", ""))
        print("typos -> " + tsv_typos)
        tsv = os.path.join(args.out, "grammar_rendered.tsv")
        with open(tsv, "w", encoding="utf-8") as f:
            f.write("page\ttype\tdescription\twas\tbecame\n")
            for r in rows:
                f.write("\t".join(str(x).replace("\t", " ").replace("\n", " ") for x in r) + "\n")
        from collections import Counter
        print("rendered rows: %d -> %s" % (len(rows), tsv))
        print(Counter(r[2].split(":")[0] for r in rows).most_common(15))
        return

    os.makedirs(args.out, exist_ok=True)
    textdir = os.path.join(args.out, "text")
    os.makedirs(textdir, exist_ok=True)

    rows = []
    for rel in pages_list(args.pages):
        path = os.path.join(ROOT, rel.replace("/", os.sep))
        try:
            with open(path, encoding="utf-8") as f:
                html = f.read()
        except OSError as e:
            rows.append((rel, "file", "не читается: %s" % e, "", ""))
            continue
        with open(os.path.join(textdir, rel.replace("/", "__") + ".txt"), "w", encoding="utf-8") as f:
            f.write(visible_text(html))
        rows.extend(check_page(rel, html))

    tsv = os.path.join(args.out, "grammar.tsv")
    with open(tsv, "w", encoding="utf-8") as f:
        f.write("page\ttype\tdescription\twas\tbecame\n")
        for r in rows:
            f.write("\t".join(str(x).replace("\t", " ").replace("\n", " ") for x in r) + "\n")
    print("grammar rows: %d -> %s" % (len(rows), tsv))
    from collections import Counter
    print(Counter(r[1] for r in rows))
    print(Counter(r[2].split(":")[0] for r in rows).most_common(20))


if __name__ == "__main__":
    main()
