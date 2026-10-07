#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_klinik_menu_regroup.py — перегруппировка бокового меню книги «Klinik Psixiatriya».

Было (на каждой из 547 страниц книги): 8 плоских «front»-строк —
Ana səhifə, Müqəddimə, Kitab haqqında, Mündəricat, Terminoloji lüğət,
Əlavələr A–E, Əlavə B — Şkalalar, Yekun tövsiyələr — и ссылка
«Məlumat bölməsi» в хвосте каждого дерева классификаций.

Стало: две сворачиваемые группы (та же механика .bk-grp/.bk-tgl/.bk-grp__sub,
что у групп расстройств):
  * первая в меню — группа «Ana səhifə» → index.html, внутри 3 пункта
    (Müqəddimə, Kitab haqqında, Mündəricat);
  * последняя в меню — группа «Məlumat bölməsi» → melumat.html, внутри 4 пункта
    (Terminoloji lüğət, Əlavələr A–E, Əlavə B — Şkalalar, Yekun tövsiyələr).
Группа текущей страницы раскрыта (data-here=1 + is-on), остальные свёрнуты.

Ярлыки и адреса берутся из существующего меню каждого языка — ничего не
придумывается.  Запуск:  python _tools/_klinik_menu_regroup.py [--apply]
"""
from __future__ import annotations
import re, sys, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent / "klinik-psixiatriya"
LANGS = ["", "ru", "en", "tr"]
APPLY = "--apply" in sys.argv

NAV_RE = re.compile(r'(<nav class="bk-sb__nav"[^>]*>)(.*?)(</nav>)', re.S)
FRONT_RE = re.compile(r'[ \t]*<a class="bk-row bk-row--front[^"]*" href="([^"]+)">'
                      r'(<span class="bk-row__n"></span><span class="bk-row__t">[^<]*)</span></a>\n?')
MEL_RE = re.compile(r'\n?[ \t]*<a class="bk-row bk-row--sec[^"]*" href="melumat\.html">'
                    r'(<span class="bk-row__n"></span><span class="bk-row__t">[^<]*)</span></a>')


def read_labels(lang: str):
    """Ярлыки берём из живого меню: index.html языкового каталога + melumat.html."""
    d = ROOT / lang if lang else ROOT
    idx = (d / "index.html").read_text(encoding="utf-8")
    mel = (d / "melumat.html").read_text(encoding="utf-8")
    nav = NAV_RE.search(idx).group(2)
    fronts = FRONT_RE.findall(nav)
    if len(fronts) != 8:
        raise SystemExit(f"{lang or 'az'}: ожидалось 8 front-строк, найдено {len(fronts)}")
    titles = [re.sub(r'^.*bk-row__t">', '', m[1]) for m in fronts]
    hrefs = [m[0] for m in fronts]
    g2_title = re.sub(r'^.*bk-row__t">', '', MEL_RE.search(NAV_RE.search(mel).group(2)).group(1))
    return dict(
        g1_title=titles[0], g1_href=hrefs[0],
        g1_items=list(zip(hrefs[1:4], titles[1:4])),
        g2_title=g2_title, g2_href="melumat.html",
        g2_items=list(zip(hrefs[4:8], titles[4:8])),
    )


def group_html(gid: str, title: str, href: str, items, page: str, indent="        ") -> str:
    """page — stem без .html; href — как в меню («index.html»)."""
    page = page + ".html"
    here = any(page == h for h, _ in items) or page == href
    on = ' is-on' if here else ''
    rows = "\n".join(
        f'{indent}<a class="bk-row bk-row--sub{" is-on" if page == h else ""}" href="{h}">'
        f'<span class="bk-row__n"></span><span class="bk-row__t">{t}</span></a>'
        for h, t in items)
    return (
        f'{indent}<div class="bk-grp" data-slug="{gid}" data-here="{1 if here else 0}">\n'
        f'{indent}<a class="bk-row bk-row--sec{on}" href="{href}">'
        f'<span class="bk-row__n"></span><span class="bk-row__t">{title}</span></a>\n'
        f'{indent}<button class="bk-tgl" type="button" tabindex="-1" '
        f'aria-expanded="{"true" if here else "false"}" aria-label="Aç / bağla">▶</button>\n'
        f'{indent}<div class="bk-grp__sub">\n{rows}\n{indent}</div>\n'
        f'{indent}</div>'
    )


def rebuild(path: pathlib.Path, lab: dict) -> bool:
    text = path.read_text(encoding="utf-8")
    m = NAV_RE.search(text)
    if not m:
        return False
    page = path.stem
    inner = m.group(2)
    n_front = len(FRONT_RE.findall(inner))
    n_mel = len(MEL_RE.findall(inner))
    if n_front != 8 or n_mel != 3:
        raise SystemExit(f"{path}: неожиданное меню (front={n_front}, melumat={n_mel})")
    inner = FRONT_RE.sub("", inner)              # убрать 8 плоских строк
    inner = MEL_RE.sub("", inner)                # убрать ссылку из хвостов деревьев
    g1 = group_html("ana-sehife", lab["g1_title"], lab["g1_href"], lab["g1_items"], page)
    g2 = group_html("melumat", lab["g2_title"], lab["g2_href"], lab["g2_items"], page)
    inner = "\n" + g1 + "\n" + inner.lstrip("\n")          # группа 1 — первая в меню
    inner = inner.rstrip("\n")
    inner = (inner + "\n        <div class=\"bk-sb__sep\" role=\"presentation\"></div>\n"
             + g2 + "\n      ")
    if APPLY:
        path.write_text(text[:m.start(2)] + inner + text[m.end(2):], encoding="utf-8")
    return True


def main():
    total = 0
    for lang in LANGS:
        lab = read_labels(lang)
        d = ROOT / lang if lang else ROOT
        n = 0
        for p in sorted(d.glob("*.html")):
            if rebuild(p, lab):
                n += 1
        print(f"{lang or 'az':>2}: страниц с меню {n}; группа1 «{lab['g1_title']}» "
              f"[{', '.join(t for _, t in lab['g1_items'])}]; "
              f"группа2 «{lab['g2_title']}» [{', '.join(t for _, t in lab['g2_items'])}]")
        total += n
    print(("ПРИМЕНЕНО. " if APPLY else "СУХОЙ ПРОГОН. ") + f"Всего страниц: {total}")


if __name__ == "__main__":
    main()
