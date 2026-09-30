#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""langcheck — «язык версии» в основном тексте книги «Klinik Psixiatriya».

Правило владельца, которое здесь измеряется:
  * основной текст языковой версии — на языке версии (AZ / RU / EN / TR);
  * иноязычное написание допустимо ТОЛЬКО в скобках или кавычках — как
    правописание имени или названия при первом упоминании;
  * коды классификаций (F20, 6A00, F70–F79, DSM-5, XBT-11, МКБ-10) — не
    «английский термин», это код, он остаётся латиницей;
  * имена собственные — авторы, шкалы, руководства, журналы, организации,
    препараты — латиница по праву;
  * библиография (список источников) сохраняет язык оригинала — это норма
    учебника, а не утечка;
  * заголовки и названия страниц живут по своему алгоритму, они считаются
    ОТДЕЛЬНОЙ колонкой и в цель «0» основного текста не входят.

Единица счёта — «английская простыня»: два и более подряд идущих английских
слова вне <span lang="en">, вне (…) и «…», вне кодов, вне имён, вне
библиографии. Английскость слова решает словарь: слово должно быть в словаре
английской версии книги и отсутствовать в словаре самой языковой версии;
плюс отдельный список английской служебной лексики.

Запуск:
    python _tools/langcheck.py                      # сводка по четырём версиям
    python _tools/langcheck.py --version az -v      # подробно, с примерами
    python _tools/langcheck.py --json _tools/_before.json
"""
from __future__ import annotations

import argparse
import html as H
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "klinik-psixiatriya"
if "--book" in sys.argv:                       # замер чужого дерева (до/после)
    BOOK = Path(sys.argv[sys.argv.index("--book") + 1]).resolve()
VERSIONS = {"az": BOOK, "ru": BOOK / "ru", "en": BOOK / "en", "tr": BOOK / "tr"}
REGISTRY = {"abbreviatur.html", "terminoloji-luget.html"}
# AZ/RU/TR-тексты, которые в версии EN законны как цитата названия
NATIVE = {"az": re.compile(r"[əƏ]"), "tr": re.compile(r"[ığşçöüİĞŞÇÖÜ]"),
          "ru": re.compile(r"[\u0400-\u04FF]"), "en": None}

RE_TAG = re.compile(r"<[a-zA-Z/!][^>]*>")
RE_SPAN_EN = re.compile(r'<span[^>]*lang="en"[^>]*>.*?</span>', re.S)
RE_COMMENT = re.compile(r"<!--.*?-->", re.S)
RE_SCRIPT = re.compile(r"<(script|style)\b.*?</\1>", re.S | re.I)
RE_ITEM = re.compile(r"<li\b[^>]*>(.*?)</li>", re.S | re.I)
RE_BIB = re.compile(r"(?:\b(?:19|20)\d{2}\b.{0,40}[;:,]|\bet al\.|[A-Z][a-z]+ [A-Z]\.\s)")
VOID = {"br", "hr", "img", "input", "meta", "link", "source", "col", "area", "wbr"}
FOREIGN_LANG = re.compile(r'lang\s*=\s*"(en|ru|az|tr|de|fr|it|es)"', re.I)
QUOTES = "«»„“”\"\u2018\u2019''()"

RE_WORD = re.compile(r"[\u00C0-\u02AF\u1E00-\u1EFF\u0400-\u04FFA-Za-z]+")

RE_CODE = re.compile(r"^(?:[A-Z]\d{2}(?:\.\d+)?x?|\d[A-Z]\d{2}(?:\.\d+)?|"
                     r"\d{2,3}(?:\.\d+)?[A-Z]?|G\d{2}(?:\.\d+)?)$")
ABBR_OK = set("""DSM ICD XBT IDC WHO APA NICE AAIDD AAP AAD CDC NIH FDA EMA
IQ EQ PTSD ADHD ASD OCD ODD CD IED GAD SAD MDD PDD CBT DBT ACT IPT EMDR ECT TMS
rTMS DBS tDCS VNS MST ABA PBS DTT PRT ESDM SSRI SNRI TCA MAOI NARI NaSSA NDRI
GABA BDNF HPA CRF ACTH TSH MRI fMRI CT PET SPECT EEG ECG EMG DNA RNA PCR CRP
ESR CSF BMI BP HR RR CI SD SE OR HIV AIDS SARS COVID MERS TB HBV HCV HPV MMR
BCG WISC WAIS WPPSI WIAT PANSS HAM-D MADRS Y-BOCS BDI ADOS ADI-R M-CHAT SCQ SRS
ASRS AQ MINI SCID CIDI CGI SANS SAPS BPRS MMSE MoCA CDR ADL IADL GAF NPI PSQI
ESS MSLT MWT ISI AHI OSA ICSD DOT IDEA EHCP IEP ICF BPD ASP DDHP MMPI WFSBP
CANMAT ISBD ISSTD ISTSS ISPMD ISSWSH ESSTS AACAP APSAC ACNP SAMHSA AASM
CADDRA AAN EACD RCSLT ASHA AAPOS AAO DCD DCDQ DLD RAD DSED BED ARFID LAI MDQ
MCI DLB FTD HbA CPAP IGD EDS SORREM QTc BDD PMDD VMAT MTA NNT NRI BAP ACOG
RCPsych FINGER PANDAS AUD BPSD IPS CO-OP RTI MTSS DIVA YGTSS CBIT SPQ SIDP
ICU TRF CBCL SNAP STEPPS TFP ITQ PAINE PEERS PECS TEACCH TOWRE GORT KTEA TEMA
KeyMath BRIEF CTOPP MABC BOT ASQ CBCL NOS FCTC NIH
""".split())
NAMES_OK = set("""
Kaplan Sadock Bleuler Kraepelin Freud Jung Adler Schneider Jaspers Wernicke
Kanner Asperger Rutter Wing Volkmar Lord Risi Ramey Campbell Eldevik Howlin
Magiati Reichow Dawson Green Sallows Sturmey Lovaas Cohen Bearss Ducharme
Scahill Bishop Felsenfeld Maguire Onslow Fairburn Petersen Moeschler Shevell
Maulik Pfeiffer Hyman Xiong Berkowitz Sandin Brown Foster Polatajko Missiuna
Cairney Gaines Adams Edwards Smits-Engelsman Thornton Wilson Webb Stevens
Bruck Shaywitz Pennington Butterworth Shalev Berninger Olsen Reynolds Nicolson
Handler Fierson Snowling Hulme Stanovich Vellutino Munro Perala Wakefield
Clayton Endicott Bohus Linehan Shapiro Resick Kernberg Beck Ellis Young
Sullivan Muller-Vahl Tiihonen Kane Olfson Siskind Wykes Drake Bond Goldman
Robinson Schooler Fromm-Reichmann Ernst Levenson Eisendrath Still Mowrer
Overholser Pontes Griffiths Zendle Cairns Han Renshaw Thomas Koegel Ost
Asher Meadow Maski Wells Barlow Clark Foa Najavits Shapiro Herman Linehan
Cochrane Lancet JAMA BMJ NEJM Psychiatry Pediatrics Psychosomatics Vaccine
Science Dyslexia Journal Arch Acta Trends Curr Mol Nat Perspect Dev Res Clin
Ther Behav Bull Disord Neurol Med Gen Hum Brain Sleep Stress Health Aff
Millwood Oxford Cambridge Springer Kluwer Wiley Wolters Publishing
Stanford Binet Raven Wechsler Denver Bayley Griffiths Vineland Kaufman
Lidcombe Hanen Conners Vanderbilt Eyberg Swanson Nolan Pelham
Maski Rumpf Muller Davis Popov Vid
""".split())
EN_STOP = set("""
the of and with for from that this which when where were was are is be been to
in on by as at or not no due use used using among between during after before
under over without within including such than then also only more most other
others its their his her has have had can may should will would into upon
these those because although however therefore there what does doing done
being each both while about against across around behind below beside beyond
despite except inside outside since toward towards until unless whereas whether
already always another anything become becomes becoming certain clearly common
commonly compared complete consider considered depending especially even every
following further given greater high higher important increased instead least
less like likely long longer lower made make making might must need needed
often overall particularly per possible present provide provided rather related
report reported require required result results same seen several show shown
significant similar specific still study studies support supported take taken
term terms thus time times together treat treated treatment typically usually
various very well year years based flexible planned combined versus vs
""".split())

RE_STOP_SEQ = re.compile(r"(?<![A-Za-z])(?:" + "|".join(sorted(EN_STOP, key=len, reverse=True))
                         + r")(?![A-Za-z])", re.I)

# Слова языка версии, совпавшие по написанию с английскими: в словаре
# английского они есть, но в тексте это свои слова, а не утечка.
NATIVE_WORDS = {
    "az": set("""lakin aid ola qat anus pis metin ise varan yox kat qapı qan
    premonitor
    olan oldu onun onda bunu buna özü özü-özünə və ya ilə kimi daha həm""".split()),
    "tr": set("""her ise ila yok kat varan hasta metin kalan his araba Mit
    premonitor premonitör
    Mit Anne Aile Sert on bir yıl gün ay kez doz yaş un tam az çok da de en
    al ver gel git bul kal ol var yap et""".split()),
    "ru": set(),
}


def read_region(html: str) -> str:
    m = re.search(r'<div\s+class="bk-read"[^>]*>', html)
    if not m:
        return ""
    tail = html[m.end():]
    for stop in ('<nav class="bk-pn"', '<footer class="bk-ft"'):
        i = tail.find(stop)
        if i > 0:
            tail = tail[:i]
    return tail


def drop_bibliography(html: str) -> str:
    """Записи списка источников — язык оригинала, из счёта выходят."""
    def keep(m: re.Match) -> str:
        inner = m.group(1)
        return " " if RE_BIB.search(H.unescape(re.sub(r"<[^>]*>", " ", inner))) else m.group(0)
    return RE_ITEM.sub(keep, html)


def clean(html: str) -> str:
    html = RE_SCRIPT.sub(" ", html)
    html = RE_COMMENT.sub(" ", html)
    return drop_bibliography(html)


def segments(html: str):
    """(текст, иноязычный_по_разметке, глубина_скобок) — посимвольно по абзацам."""
    stack: list[tuple[str, bool]] = []
    pos = 0
    for m in RE_TAG.finditer(html):
        chunk = html[pos:m.start()]
        pos = m.end()
        if chunk:
            yield chunk, bool(stack and stack[-1][1])
        tag = m.group(0)
        name = (re.match(r"</?([a-zA-Z0-9]+)", tag) or [None, ""])[1].lower()
        if name in VOID:
            continue
        if tag.startswith("</"):
            for i in range(len(stack) - 1, -1, -1):
                if stack[i][0] == name:
                    del stack[i:]
                    break
        else:
            inherit = bool(stack and stack[-1][1]) or bool(FOREIGN_LANG.search(tag))
            stack.append((name, inherit))
    tail = html[pos:]
    if tail:
        yield tail, bool(stack and stack[-1][1])


def depth_map(text: str, start: int = 0) -> list[bool]:
    """Для каждого символа текста: внутри (…) или «…»? start — глубина на входе."""
    out = [False] * len(text)
    d = start
    for i, ch in enumerate(text):
        if ch in "«„“":        # открывающие: « „ “
            d += 1
        elif ch in "»”":          # закрывающие: » ”
            d = max(0, d - 1)
        out[i] = d > 0
        if ch == "(":
            d += 1
        elif ch == ")":
            d = max(0, d - 1)
    return out


def close_depth(text: str, start: int) -> int:
    return depth_map(text, start)[-1] if text else start


def scan(html: str, lex: set[str], shared: set[str], native: set[str]) -> list[dict]:
    runs: list[dict] = []
    buf: list[str] = []
    buf_ctx = ""

    def flush():
        nonlocal buf, buf_ctx
        if len(buf) >= 2:
            runs.append({"words": list(buf), "n": len(buf), "context": buf_ctx[:230]})
        buf, buf_ctx = [], ""

    depth = 0     # глубина (…) и «…» — сквозная по всей странице, не по куску
    for chunk, foreign in segments(html):
        if not chunk.strip():
            continue
        ctx_text = re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]*>", "", chunk)))
        if not foreign:
            dm = depth_map(ctx_text, depth)
            for m in RE_WORD.finditer(ctx_text):
                w = m.group(0)
                i = m.start()
                if i >= len(dm) or dm[i]:
                    flush()
                    continue
                if not w.isascii() or re.search(r"[\u0400-\u04FF]", w):
                    flush()
                    continue
                low = w.lower()
                if RE_CODE.match(w) or w.upper() in ABBR_OK or w in NAMES_OK:
                    flush()
                    continue
                if low in native:
                    flush()
                    continue
                if low in EN_STOP or (low in lex and low not in shared):
                    buf.append(w)
                    buf_ctx = buf_ctx or ctx_text[max(0, i - 80):i + 130]
                else:
                    flush()
        depth = close_depth(ctx_text, depth)
        flush()
    flush()
    return runs


RE_FOREIGN_W = re.compile(r"[^\s]{0,20}(?:[əƏ]|[ıİ])[^\s]{0,20}|[\u0400-\u04FF][\u0400-\u04FF\-]{2,}")


def scan_foreign(html: str, lang: str) -> list[dict]:
    """Для английской версии: вставка на языке соседних версий (диакритика, кириллица)."""
    runs: list[dict] = []
    for chunk, foreign in segments(html):
        if foreign:
            continue
        txt = H.unescape(re.sub(r"<[^>]*>", " ", chunk))
        txt = re.sub(r"&[a-z]+;|&#x?[0-9a-f]+;", " ", txt)
        for m in RE_FOREIGN_W.finditer(txt):
            tok = m.group(0)
            if lang == "en" and re.fullmatch(r"[A-Za-z'\- ']*", tok):
                continue
            runs.append({"words": [tok], "n": 1,
                         "context": re.sub(r"\s+", " ", txt[max(0, m.start() - 80):m.end() + 80])})
    return runs


def page_html(f: Path) -> str:
    return clean(read_region(f.read_text(encoding="utf-8", errors="replace")))


def load_lexicon() -> set[str]:
    f = Path(__file__).with_name("en-lexicon.txt")
    if not f.exists():
        raise SystemExit("нет _tools/en-lexicon.txt — соберите: langcheck.py --build-lexicon")
    return {w.strip() for w in f.read_text(encoding="utf-8").split() if w.strip()}


def build_lexicon() -> set[str]:
    """Английская лексика книги = слова EN-версии, подтверждённые словарём."""
    dic = {w.strip().lower() for w in
           Path(__file__).with_name("_words_en.txt").read_text(encoding="utf-8").split()}
    voc: set[str] = set()
    for lg, folder in VERSIONS.items():
        for f in sorted(folder.glob("*.html")):
            for m in re.finditer(r"[A-Za-z][A-Za-z'\-]+",
                                 f.read_text(encoding="utf-8", errors="replace")):
                voc.add(m.group(0).lower())
    lex = sorted(w for w in voc if w in dic and len(w) >= 3 and re.fullmatch(r"[a-z][a-z'\-]*", w))
    Path(__file__).with_name("en-lexicon.txt").write_text(chr(10).join(lex) + chr(10), encoding="utf-8")
    return set(lex)


def vocab(folder: Path, drop_en: bool = True) -> set[str]:
    v: set[str] = set()
    for f in sorted(folder.glob("*.html")):
        if f.name in REGISTRY:
            continue
        html = page_html(f)
        if drop_en:
            html = RE_SPAN_EN.sub(" ", html)
        for chunk, _ in segments(html):
            for m in RE_WORD.finditer(H.unescape(chunk)):
                w = m.group(0)
                if re.fullmatch(r"[A-Za-z]+", w) and len(w) >= 2:
                    v.add(w.lower())
    return v


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", choices=list(VERSIONS))
    ap.add_argument("--json")
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("--examples", type=int, default=12)
    ap.add_argument("--book", help="каталог книги вместо klinik-psixiatriya/")
    a = ap.parse_args()

    if "--build-lexicon" in sys.argv:
        lex = build_lexicon()
        print(f"английская лексика книги: {len(lex)} слов → _tools/en-lexicon.txt")
        return 0
    LEX = load_lexicon()
    # интернациональные заимствования: слово идёт минимум в двух НЕанглийских
    # версиях — это общая медицинская лексика (test, risk, plan, faktor…),
    # а не английский термин
    vv = {lg: vocab(VERSIONS[lg]) for lg in ("az", "ru", "tr", "en")}
    shared = set()
    for w in LEX:
        if sum(1 for lg in ("az", "ru", "tr") if w in vv[lg]) >= 2:
            shared.add(w)
    # словарь самого языка версии: латиница версии, которой нет в английской
    # версии, — это её собственные слова (lakin, qat, her, ise…), не английский
    for lg in ("az", "ru", "tr"):
        vv[lg] |= NATIVE_WORDS[lg]
    native = {lg: set(NATIVE_WORDS[lg]) for lg in ("az", "ru", "tr")}
    report: dict = {}
    print(f"{'версия':<8}{'англ. простыней':>16}{'англ. слов':>12}"
          f"{'в заголовках':>14}{'страниц':>10}{'  цель':>8}")
    print("-" * 70)
    for lg in ([a.version] if a.version else list(VERSIONS)):
        per_file: Counter = Counter()
        detail: list[dict] = []
        for f in sorted(VERSIONS[lg].glob("*.html")):
            if f.name in REGISTRY:
                continue
            html = page_html(f)
            if not html:
                continue
            heads = list(re.finditer(r"<(h[1-4])\b[^>]*>(.*?)</\1>", html, re.S))
            parts, pos = [], 0
            for m in heads:
                parts.append(("body", html[pos:m.start()]))
                parts.append(("head", m.group(2)))
                pos = m.end()
            parts.append(("body", html[pos:]))
            hits = []
            if lg == "en":
                for kind, frag in parts:
                    for r in scan_foreign(frag, lg):
                        r["kind"] = kind
                        hits.append(r)
                for r in hits:
                    r["file"] = f.name
                    detail.append(r)
                if hits:
                    per_file[f.name] = len(hits)
                continue
            for kind, frag in parts:
                frag = RE_SPAN_EN.sub(" ", frag) if kind == "head" else frag
                for r in scan(frag, LEX, shared, native[lg]):
                    r["kind"] = kind
                    hits.append(r)
            for r in hits:
                r["file"] = f.name
                detail.append(r)
            if hits:
                per_file[f.name] = len(hits)
        body = [x for x in detail if x["kind"] == "body"]
        head = [x for x in detail if x["kind"] == "head"]
        print(f"{lg:<8}{len(body):>16}{sum(x['n'] for x in body):>12}"
              f"{len(head):>14}{len(per_file):>10}{'0':>8}")
        report[lg] = {"runs_body": len(body), "words_body": sum(x["n"] for x in body),
                      "runs_head": len(head), "files": len(per_file),
                      "detail": [{"file": x["file"], "kind": x["kind"],
                                  "words": x["words"], "context": x["context"]}
                                 for x in detail]}
        if a.verbose:
            print(f"\n  по файлам: {per_file.most_common(20)}\n")
            for x in detail[:a.examples]:
                print(f"    {x['file']:<16}{x['kind']:<6} {' '.join(x['words'])[:60]}")
                print(f"        …{x['context'][:170]}")
            print()
    if a.json:
        Path(a.json).write_text(json.dumps(report, ensure_ascii=False, indent=1),
                                encoding="utf-8")
        print(f"\nотчёт: {a.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
