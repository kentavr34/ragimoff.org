# -*- coding: utf-8 -*-
"""term_fix.py — названия болезней в азербайджанских текстах сайта: только по принятой номенклатуре (слово Кенана 13.11.2026).

Корень ошибки: переводчик калькировал прилагательное источника (нем. «infantile Cerebrallähmung», лат. «paralysis infantilis»)
вместо того, чтобы взять принятое в Азербайджане название болезни. «Детский» в названии болезни — «uşaq», не «infantil»:
  ✓ Uşaq serebral iflici (USİ) — автореферат диссертации ВАК АР, кафедра неврологии АМУ, 2022
    (aak.gov.az, «Uşaq serebral iflici ilə olan uşaqlarda epilepsiyanın…»); ✗ İnfantil serebral iflic.
«İnfantil» остаётся только как термин («infantil seksuallıq», «infantilizm», «infantil yaşantılar» у Фрейда)
и в иноязычных цитатах и библиографии («paralysis infantilis», «infantile Cerebrallähmung»).

Применение:  python term_fix.py          — показать, что будет исправлено (ничего не пишет)
             python term_fix.py --fix    — исправить books/*/book.json, books/*/az/*.html, data/shop/index.az.json, books/index.html, shop-order.js
             python term_fix.py --check  — страж: код 1, если в текстах осталась отвергнутая форма
Из других скриптов: from term_fix import fix_text  (сборщики пропускают через неё каждый текст)."""
import io, os, re, sys, glob, json

D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
W = "a-zəığüöçşA-ZƏIĞÜÖÇŞİ"

# склонение «iflic» после «uşaq serebral»: калька стояла без притяжательного аффикса (izafət III требует его)
IFLIC = {"": "i", "in": "inin", "ə": "inə", "də": "ində", "dən": "indən", "dəki": "indəki", "dir": "idir", "lə": "i ilə",
         "i": "i", "inin": "inin", "inə": "inə", "ində": "ində", "indən": "indən", "ini": "ini",
         "lər": "ləri", "lərin": "lərinin", "lərə": "lərinə", "lərdə": "lərində", "lərdən": "lərindən",
         "ləri": "ləri", "lərinin": "lərinin", "lərində": "lərində"}
IYA = {"": "sı", "nın": "sının", "ya": "sına", "da": "sında", "dan": "sından", "nı": "sını",
       "lar": "ları", "ların": "larının", "lara": "larına", "larda": "larında"}

# точные обороты (порядок важен: длинные раньше коротких)
EXACT = [
    ("«infantil psevdotserebral iflic»ini", "«uşaq psevdoserebral iflici»ni"),
    ("infantil uşaq iflic", "uşaq iflic"),
    ("serebral uşaq iflic", "uşaq serebral iflic"),          # один термин — одна форма (нем. «cerebrale Kinderlähmung» = тот же диагноз)
    ("infantil spinal iflic prosesləri", "uşaq spinal iflici prosesləri"),
    ("infantil xoreya chronica", "xroniki uşaq xoreyası"),
    ("mumi infantil xoreya", "mumi uşaq xoreyası"),
    ("infantil lobar sklerozun", "uşaq lobar sklerozunun"),
    ("infantil ensefalit məsələsində", "uşaq ensefaliti məsələsində"),
    ("infantil beyində", "uşaq beynində"),
    ("infantil beyin sklerozunun", "uşaq beyin sklerozunun"),
    ("infantil beyin atrofiyası", "uşaq beyninin atrofiyası"),
    ("infantil beyin patologiyasına", "uşaq beyninin patologiyasına"),
    ("infantil beyin təsirlənməsinin", "uşaq beyninin təsirlənməsinin"),
    ("infantil beyin iflicinin", "uşaq beyin iflicinin"),
    ("infantil beyin toxumasındakı", "uşaq beyin toxumasındakı"),
    ("infantil beyin müəyyən", "uşaq beyni müəyyən"),
    ("infantil beyin kəskin", "uşaq beyni kəskin"),
    ("infantil atetozdan", "uşaq atetozundan"),
    ("infantil ailəvi affeksiyalara", "uşaqlarda ailəvi affeksiyalara"),
    ("infantil xəstəlikdə", "uşaq xəstəliyində"),
    ("bu infantil xəstəliyi", "bu uşaq xəstəliyini"),
    # Zwangsneurose: серия Фрейда — «məcburiyyət nevrozu» (438 мест, подзаголовок Kitab 7 «Məcburiyyət nevrozu halı»); «obsessiv nevroz» — разнобой (37, письма Юнгу)
    ("obsessiv nevrozu analiz", "məcburiyyət nevrozunu analiz"),
    ("obsessiv nevrozlu", "məcburiyyət nevrozlu"),
    ("obsessiv nevrozun", "məcburiyyət nevrozunun"),
    ("obsessiv nevrozdan", "məcburiyyət nevrozundan"),
    ("obsessiv nevrozda", "məcburiyyət nevrozunda"),
    ("obsessiv nevrozdur", "məcburiyyət nevrozudur"),
    ("obsessiv nevroza", "məcburiyyət nevrozuna"),
    ("obsessiv nevrozu", "məcburiyyət nevrozu"),
    ("obsessiv nevroz", "məcburiyyət nevrozu"),
    # Neuropsychose: замок-глоссарий — «nevro-», «neyro-» — искажение (nevropsixoz 26 : neyropsixoz 4)
    ("neyropsixoz", "nevropsixoz"),
]
# отвергнутые формы для стража (после исправления их не должно остаться в азербайджанском тексте)
REJECT = re.compile(r"[İIi]nfantil ([Ss]erebral|uşaq iflic|spinal iflic|psevdo|xoreya|lobar|ensefalit|beyin|atetoz|affeksiya|ailəvi affeks)|[Ss]erebral uşaq iflic|[Oo]bsessiv nevroz|[Nn]eyropsixoz")


def _cap(src, rep):
    return rep[0].upper().replace("i", "İ", 1) + rep[1:] if src[:1].isupper() and rep[:1] == "i" else (rep[0].upper() + rep[1:] if src[:1].isupper() else rep)


RX_SER = re.compile(r"\b([İIi]nfantil) ((?:serebral |psevdobulbar )?)(iflic|affeksiya|diplegiya)(?=([%s]*))\4(?![%s])" % (W, W))


def _ser(m):
    head, qual, noun, suf = m.group(1), m.group(2), m.group(3), m.group(4)
    table = IFLIC if noun == "iflic" else IYA
    if suf not in table:
        return m.group(0)
    out = table[suf]
    if noun == "iflic" and suf == "i":
        nxt = m.string[m.end():m.end() + 5]
        out = "i" if (nxt.startswith(" ilə") or nxt[:1] in ".:)»" or nxt == "") else "ini"
    word = "Uşaq" if head[0] in "İI" else "uşaq"
    stem = noun if noun == "iflic" else noun[:-1]             # affeksiya → affeksiy + a/sı… ; diplegiya → diplegiy
    if noun != "iflic":
        out = "a" + out
    return "%s %s%s%s" % (word, qual, stem, out)


# По базе истины truth.term_verified (✓ / ≈ medium–high; выгрузка _agent/truth_cache, сверка — term_audit.py), этап 3 от 13.11.2026.
# (было, стало) — сравнение по началу слова, окончание сохраняется; регистр «как в источнике» (строчные / Первая / Каждое Слово / ПРОПИСНЫЕ).
# ≈ low («Dissosiativ kimlik pozuntusu») не применяется — вынесено на решение Кенана.
BASE = {
    "az": [
        ("İnfantil Serebral İfliclə", "Uşaq Serebral İflici ilə"), ("İnfantil Serebral İflic", "Uşaq Serebral İflici"),
        ("Levi cisimcik", "Lewy cisimcik"),                            # Lewy cisimcikləri ✓ (имя — в оригинале)
        ("Vilson xəstəliy", "Wilson xəstəliy"),                        # Wilson xəstəliyi ✓
        ("amigdala", "amiqdala"),                                      # amiqdala ✓
        ("Generalizə olunmuş təşviş pozuntu", "Ümumiləşmiş təşviş pozuntu"),          # ÜTP ≈ medium
        ("Generalizə olunmuş Təşviş Pozuntu", "Ümumiləşmiş Təşviş Pozuntu"),
        ("Diqqət əskikliyi və hiperaktiv pozuntu", "Diqqət əskikliyi və hiperaktivlik pozuntusu"),   # DƏHP ≈
        ("Tək epizodlu depressiv pozuntu", "Təksaylı depressiv epizod pozuntusu"),     # ✓ high
        ("Təkrarlanan depressiv pozuntu", "Rekurrent depressiv pozuntu"),               # ✓ high
        ("Yığma pozuntusu", "Yığıcılıq pozuntusu"),                                    # ✓ high
        ("major depressiv pozuntu", "böyük depressiv pozuntu"),                         # ≈ medium
        ("Uzanmış kədər pozuntu", "Uzanmış yas pozuntu"),                               # ≈ medium
        ("Sosial qatılma məhdudlaşması pozuntu", "Dezinhibə olunmuş sosial qatılma pozuntu"),   # ≈ medium
        ("Aşırı qidalanma pozuntu", "Obur yemə pozuntu"),                               # ≈ medium
        ("Voyeuristik pozuntu", "Voyerist pozuntu"),                                    # ≈ medium
        ("Epizodik eksplosiv pozuntu", "Epizodik eksploziv pozuntu"),                   # ≈ medium
        ("nevrotik anoreksiyası", "sinir anoreksiyası"), ("Nevrotik anoreksiya", "Sinir anoreksiyası"),   # ✓ high
        ("halüsinogen", "hallüsinogen"), ("halüsinasiya", "hallüsinasiya"),            # ✓
        ("antidepresant", "antidepressant"),                                           # ✓ (✗ antidepresan, antidepresant)
        ("ikinci dərəcəli travma", "ikincili travma"),                                 # ✓ ikincili (мед.); «ikinci dərəcəli mənbələr» — общее слово
        # 6B64 Dissociative identity disorder (RU «…идентичности»): identiklik = идентичность; identifikasiya = идентификация (другой смысл),
        # şəxsiyyət = личность (старое «множественная личность»), kimlik — турецкое. Решение 13.11.2026 (база ≈ medium), было 3 формы в одной книге.
        ('<tr><td>DSP</td><td>Dissosiativ Şəxsiyyət Pozuntusu</td><td>Dissociative Identity Disorder (DID)</td></tr><tr><td>DİP</td><td>Dissosiativ İdentiklik Pozuntusu</td></tr>',
         '<tr><td>DİP</td><td>Dissosiativ İdentiklik Pozuntusu</td><td>Dissociative Identity Disorder (DID)</td></tr>'),
        ('<tr><td>DSP</td><td>Dissosiativ Şəxsiyyət Pozuntusu</td></tr><tr><td>DİP</td><td>Dissosiativ İdentiklik Pozuntusu</td></tr>',
         '<tr><td>DİP</td><td>Dissosiativ İdentiklik Pozuntusu</td></tr>'),
        ("Dissosiativ identifikasiya pozuntu", "Dissosiativ identiklik pozuntu"),
        ("Dissosiativ şəxsiyyət pozuntu", "Dissosiativ identiklik pozuntu"),
        ("Sosial İştirakın Məhdudlaşdırılması Pozuntusu", "Dezinhibə Olunmuş Sosial Qatılma Pozuntusu"),   # DSED 6B45 ≈ medium
        ("sado-mazoxizm", "sadomazoxizm"),                              # XBT-10 AZ F65.5 Sadomazoxizm
        ("Mani-depressiv", "Manik-depressiv"),                          # manik-depressiv (Klinik, серия)
        ("halüsinator", "hallüsinator"),                                # hallüsinasiya ✓
    ],
    "ru": [
        ("Комплексное посттравматическое стрессовое расстройство", "Осложнённое посттравматическое стрессовое расстройство"),  # МКБ-11 6B41 ✓
        ("комплексного посттравматического стрессового расстройства", "осложнённого посттравматического стрессового расстройства"),
        ("комплексному посттравматическому стрессовому расстройству", "осложнённому посттравматическому стрессовому расстройству"),
        ("комплексным посттравматическим стрессовым расстройством", "осложнённым посттравматическим стрессовым расстройством"),
        ("комплексном посттравматическом стрессовом расстройстве", "осложнённом посттравматическом стрессовом расстройстве"),
        ("комплексное ПТСР", "осложнённое ПТСР"), ("комплексного ПТСР", "осложнённого ПТСР"), ("комплексному ПТСР", "осложнённому ПТСР"),
        ("комплексным ПТСР", "осложнённым ПТСР"), ("комплексном ПТСР", "осложнённом ПТСР"),
        ("Инсулиновая коматозная терапия", "Инсулинокоматозная терапия"), ("инсулиновой коматозной терапии", "инсулинокоматозной терапии"),
        ("инсулиновую коматозную терапию", "инсулинокоматозную терапию"), ("инсулиновой коматозной терапией", "инсулинокоматозной терапией"),
    ],
    "tr": [
        ("hezeyanının", "sanrısının"), ("hezeyanında", "sanrısında"), ("hezeyanlı", "sanrılı"), ("hezeyanı", "sanrısı"), ("hezeyan", "sanrı"),  # ✓ high
        ("Kaçıngan/kısıtlayıcı yiyecek alımı bozukluğu", "Kaçıngan-kısıtlı gıda alım bozukluğu"),          # ✓ high
        ("Kaçıngan/Kısıtlayıcı Yiyecek Alımı Bozukluğu", "Kaçıngan-Kısıtlı Gıda Alım Bozukluğu"),
    ],
}


def _forms(s):
    """строчные / Первая / Каждое Слово / ПРОПИСНЫЕ (азерб. и тур. i/İ, ı/I)."""
    up = lambda x: x.replace("i", "İ").replace("ı", "I").upper()
    cap = lambda w: (up(w[0]) + w[1:]) if w else w
    lo = s[0].lower() + s[1:] if not s[:1] == "İ" else "i" + s[1:]
    return [s, lo, cap(lo), " ".join(cap(w) if w not in ("və", "и", "ve") else w for w in lo.split(" ")), up(lo)]


def _base_rules(lang):
    out, seen = [], set()
    for a, b in BASE.get(lang, []):
        for fa, fb in zip(_forms(a), _forms(b)):
            if fa not in seen:
                seen.add(fa); out.append((fa, fb))
    return sorted(out, key=lambda x: -len(x[0]))


def fix_base(t, langs=("az", "ru")):
    n = 0
    for lg in langs:
        for a, b in _base_rules(lg):
            if a in t:
                n += t.count(a); t = t.replace(a, b)
    return t, n


def fix_text(t, langs=("az", "ru")):
    t, n = fix_base(t, langs)
    for a, b in EXACT:
        for src in (a, a[:1].upper() + a[1:], ("İ" + a[1:]) if a[:1] == "i" else a):
            if src in t:
                c = t.count(src); n += c
                t = t.replace(src, _cap(src, b))
    t, k = RX_SER.subn(_ser, t)
    # после кавычки аффикс пишется со связкой: «… iflici»nə, «… iflici»nin (калька давала «… iflic»ə)
    t = re.sub(r"((?:serebral|psevdobulbar) iflici»)(ə|in|də|dən|i)(?![%s])" % W, lambda m: m.group(1) + {"ə": "nə", "in": "nin", "də": "ndə", "dən": "ndən", "i": "ni"}[m.group(2)], t)
    return t, n + k


def files():
    out = glob.glob(os.path.join(D, "books", "*", "book.json"))
    for lg in ("az", "ru", "en", "tr"):
        out += glob.glob(os.path.join(D, "books", "*", lg, "*.html"))
    out += [os.path.join(D, "data", "shop", "index.%s.json" % lg) for lg in ("az", "ru", "en")]
    out += [os.path.join(D, "books", "index.html"), os.path.join(D, "assets", "js", "shop-order.js")]
    # тексты страниц сайта (статьи, консультации, услуги): те же названия болезней (13.11.2026)
    out += [f for f in glob.glob(os.path.join(D, "data", "**", "*.json"), recursive=True) if not f.replace("\\", "/").count("/data/shop/")]
    out += [os.path.join(D, "assets", "js", "content.js")]
    return sorted(set(f for f in out if os.path.exists(f)))


def langs_of(path):
    p = path.replace("\\", "/")
    for lg in ("az", "ru", "en", "tr"):
        if p.endswith(".%s.json" % lg) and "/data/shop/" not in p:
            return {"en": ()}.get(lg, (lg,))
    for lg in ("tr", "en", "ru", "az"):
        if "/%s/" % lg in p:
            return (lg,) if lg != "en" else ()
    return ("az", "ru")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    total, left = 0, []
    for f in files():
        t = io.open(f, encoding="utf-8").read()
        lg = langs_of(f)
        nt, n = fix_text(t, lg)
        if n and nt != t:
            total += n
            print("%4d  %s" % (n, os.path.relpath(f, D)))
            if mode == "--fix":
                tmp = f + ".tmp"
                io.open(tmp, "w", encoding="utf-8", newline="\n").write(nt)
                os.replace(tmp, f)
        chk = nt if mode == "--fix" else t
        txt = re.sub(r"<[^>]+>", " ", chk)
        for m in REJECT.finditer(txt):
            left.append("%s: …%s…" % (os.path.relpath(f, D), txt[max(0, m.start() - 40):m.end() + 30].replace("\n", " ")))
        for l_ in lg:
            for a_, b_ in _base_rules(l_):
                if a_ in txt:
                    left.append("%s: «%s» ×%d (→ %s)" % (os.path.relpath(f, D), a_, txt.count(a_), b_))
    print("ИСПРАВЛЕНИЙ: %d%s" % (total, " (записано)" if mode == "--fix" else " (не записано)"))
    if mode in ("--check", "--fix"):
        print("ОТВЕРГНУТЫХ ФОРМ ОСТАЛОСЬ: %d" % len(left))
        for x in left[:40]:
            print("  ✗", x)
        if mode == "--check" and left:
            sys.exit(1)


if __name__ == "__main__":
    main()
