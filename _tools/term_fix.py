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
# формы, отвергнутые словом Кенана 14.11.2026 — проверяются только в азербайджанском тексте (в турецком sinirlilik, kimlik — норма)
REJECT_AZ = re.compile(r"[Mm]əcburiyyət nevroz|(?<!etik )(?<!əxlaqi )(?<!mənəvi )(?<!əxlaq )[Pp]ozğunlu[qğ]|[Mm]əcburi (?:fikir|ideya|düşüncə|təsəvvür)|[Ss]inirlili[kyğ]|[Dd]issosiativ kimlik|[Yy]etişkin")


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
        # 14.11 утро: identifikasiya — ОТМЕНЕНО. ПОСЛЕДНЕЕ слово Кенана 14.11.2026: 6B64 = «Dissosiativ identiklik pozuntusu (DİP)»
        # (identiklik однозначно указывает на диссоциативную группу); «şəxsiyyət pozuntusu» — только расстройства личности 6D10/6D11.
        ('<tr><td>DSP</td><td>Dissosiativ Şəxsiyyət Pozuntusu</td><td>Dissociative Identity Disorder (DID)</td></tr><tr><td>DİP</td><td>Dissosiativ İdentifikasiya Pozuntusu</td></tr>',
         '<tr><td>DİP</td><td>Dissosiativ İdentiklik Pozuntusu</td><td>Dissociative Identity Disorder (DID)</td></tr>'),
        ('<tr><td>DSP</td><td>Dissosiativ Şəxsiyyət Pozuntusu</td></tr><tr><td>DİP</td><td>Dissosiativ İdentifikasiya Pozuntusu</td></tr>',
         '<tr><td>DİP</td><td>Dissosiativ İdentiklik Pozuntusu</td></tr>'),
        ('<tr><td>DİP</td><td>Dissosiativ İdentifikasiya Pozuntusu</td>', '<tr><td>DİP</td><td>Dissosiativ İdentiklik Pozuntusu</td>'),
        ("Dissosiativ identifikasiya pozuntu", "Dissosiativ identiklik pozuntu"),
        ("dissosiativ identifikasiya pozuntu", "dissosiativ identiklik pozuntu"),
        ("DİSSOSİATİV İDENTİFİKASİYA POZUNTU", "DİSSOSİATİV İDENTİKLİK POZUNTU"),
        ("Dissosiativ İdentifikasiya Pozuntu", "Dissosiativ İdentiklik Pozuntu"),
        ("Dissosiativ şəxsiyyət pozuntu", "Dissosiativ identiklik pozuntu"),
        ("Dissosiativ kimlik pozuntu", "Dissosiativ identiklik pozuntu"),
        # 14.11.2026: XBT-11 AZ — протокол МЗ АР «Obsessiv-kompulsiv pozuntular…» (Kollegiya 22.10.2021 №24, F. İsmayılov və b.;
        # isim.az/upload/File/reports/OBSESSİV.pdf): 6B22 = «Qoxu pozuntusu», 6B25 = «Bədənə fokuslu təkrarlanan davranış pozuntuları»
        ("Bədənə Yönəlmiş Təkrar Davranışlar Pozuntusu", "Bədənə Fokuslu Təkrarlanan Davranış Pozuntuları"),
        ("Bədənə yönəlmiş təkrar davranışlar pozuntusu", "Bədənə fokuslu təkrarlanan davranış pozuntuları"),
        ("Bədənə yönəlmiş təkrarlanan davranış pozuntu", "Bədənə fokuslu təkrarlanan davranış pozuntu"),
        ("Bədənə yönəlmiş təkrar davranış pozuntu", "Bədənə fokuslu təkrarlanan davranış pozuntu"),
        # 14.11.2026 (проверка «Вирус вины», «Шизофрения»): тревога в диагнозе = təşviş (6B00, 6B04); 6B40 = posttravmatik; GA34.41 = pozuntu
        ("narahatlıq pozuntu", "təşviş pozuntu"), ("Narahatlıq pozuntu", "Təşviş pozuntu"),
        ("sosial narahatlıq", "sosial təşviş"), ("Sosial narahatlıq", "Sosial təşviş"),
        ("travma sonrası stress pozuntu", "posttravmatik stress pozuntu"), ("Travma sonrası stress pozuntu", "Posttravmatik stress pozuntu"),
        ("(TSSP)", "(PTSP)"),
        ("premenstrual disforik sindrom", "premenstrual disforik pozuntu"), ("Premenstrual disforik sindrom", "Premenstrual disforik pozuntu"),
        ("Bədənin Qoxusu Pozuntu", "Qoxu Pozuntu"), ("Bədənin qoxusu pozuntu", "Qoxu pozuntu"), ("bədənin qoxusu pozuntu", "qoxu pozuntu"),
        ("identikliyin formalaşması", "şəxsiyyət kimliyinin formalaşması"),     # Klinik v26: возврат исходного текста
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


# ---------------------------------------------------------------------------------------------------------------
# Слово Кенана 14.11.2026. Обсессия = навязчивость = «sarışan»; «məcburiyyət» — вынужденность (другой смысл).
# Источники: XBT-10 AZ F42.0 «Əsasən sarışan fikirlər…», F42.2 «Qarışıq sarışan fikirlər və hərəkətlər»;
# клинический протокол Səhiyyə Nazirliyi «Obsessiv-kompulsiv pozuntular» (2021, isim.az): «obsessiv-kompulsiv pozuntuların
# (sarışan halların)», «Obsessiya – … sarışan fikirlər»; программа докторантуры АМУ по психиатрии: «sarışan hallar».
# Zwangsneurose (рус. «невроз навязчивых состояний») → «sarışan hallar nevrozu»; Zwangsvorstellung → «sarışan təsəvvür» и т. д.
# В неврологических книгах (Uşaq serebral iflici, Afaziya…) «məcburi vəziyyət» = Zwangshaltung (вынужденная поза) — не трогать.
# ---------------------------------------------------------------------------------------------------------------
NEURO = ("freud-usaq-iflici", "freud-afaziya", "freud-koka-afaziya", "freud-referatlar", "freud-kokain",
         "Cerebrallaehmung", "Aphasien", "Referatlar", "Ueber_Coca", "Coca", "GW17_cerebral",
         "klinik-psixiatriya", "Klinik_Psixiatriya")   # Klinik: «məcburi hərəkətlər» = насильственные (моторный автоматизм)
SERIES_Z = [("uşaqlıq və məcburiyyət", "uşaqlıq və sarışan hallar"),   # название Kitab 6 (GW VII: Zwangshandlungen, Zwangsneurose)
            ("məcburiyyət nevroz", "sarışan hallar nevroz"), ("məcburiyyət nevrotik", "sarışan hallar nevrotik"),
            ("məcburiyyət xəstə", "sarışan hallar xəstə"), ("məcburiyyət xəstəliy", "sarışan hallar xəstəliy")]
_ZN = "hərəkət|ideya|düşüncə|təsəvvür|fikir|fikr|ritual|mərasim|qorxu|impuls|təkan|affekt|simptom|şübhə|ittiham"
# неоднозначные («xarakter», «vəziyyət», «əmr», «qadağa», «söz», «hal», «istək», «əməl»…: Zwang = и навязчивость, и принуждение) —
# не автоматом, а по немецкому оригиналу предложения (14.11.2026: «mədəniyyətin məcburi xarakteri» = принуждение)
RX_ZADJ = re.compile(r"(?<![%s])([Mm])əcburi (?=(?:%s)(?![%s]*(?:siz|sız|suz|süz)))" % (W, _ZN, W))   # 14.11: hərəkətsizlik — не Zwang
# izafət «məcburiyyət təsəvvürləri» → «sarışan təsəvvürlər»: основа (+мн.ч.) + притяжательный + падеж → основа (+мн.ч.) + падеж
ZSTEM = ["təsəvvür", "hərəkət", "simptom", "affekt", "əlamət", "ittiham", "impuls", "ritual", "mərasim", "təkan",
         "ideya", "düşüncə", "qorxu", "şübhə", "fikir", "tip"]
RX_ZNOUN = re.compile(r"(?<![%s])([Mm])əcburiyyət (%s)([%s]*)" % (W, "|".join(sorted(ZSTEM + ["fikr"], key=len, reverse=True)), W))
_V = "aıoueəiöü"


def _v4(base):
    v = [c for c in base if c in _V][-1]
    return {"a": "ı", "ı": "ı", "o": "u", "u": "u", "e": "i", "ə": "i", "i": "i", "ö": "ü", "ü": "ü"}[v]


def _v2(base):
    return "a" if [c for c in base if c in _V][-1] in "aıou" else "ə"


def _plain(stem, rest):
    """izafət (притяжательная форма) → простая форма; None, если не разобрано."""
    if stem == "fikr":
        stem = "fikir"
        if not rest[:1] in "iı":
            return None
        rest = rest[1:]
        if rest == "":  # fikri (притяж.) → fikir
            return "fikir"
        m = {"nin": "fikrin", "nə": "fikrə", "ndə": "fikirdə", "ndən": "fikirdən", "ni": "fikri", "dir": "fikirdir"}
        return m.get(rest)
    base = stem
    if rest.startswith(("lər", "lar")):
        base, rest = stem + rest[:3], rest[3:]
    vowel_end = base[-1] in _V
    if vowel_end:
        if not (rest[:1] == "s" and rest[1:2] in "ıiuü"):
            return None
        rest = rest[2:]
    else:
        if not rest[:1] in "ıiuü":
            return None
        rest = rest[1:]
    v4, v2 = _v4(base), _v2(base)
    case = {"": "", "n" + v4 + "n": "gen", "n" + v2: "dat", "nd" + v2: "loc", "nd" + v2 + "n": "abl", "n" + v4: "acc",
            "d" + v4 + "r": "cop", "nd" + v2 + "kı" if v2 == "a" else "nd" + v2 + "ki": "lockı"}.get(rest)
    if case is None:
        return None
    if vowel_end:
        suf = {"": "", "gen": "n" + v4 + "n", "dat": "y" + v2, "loc": "d" + v2, "abl": "d" + v2 + "n", "acc": "n" + v4,
               "cop": "d" + v4 + "r", "lockı": "d" + v2 + ("kı" if v2 == "a" else "ki")}[case]
    else:
        suf = {"": "", "gen": v4 + "n", "dat": v2, "loc": "d" + v2, "abl": "d" + v2 + "n", "acc": v4,
               "cop": "d" + v4 + "r", "lockı": "d" + v2 + ("kı" if v2 == "a" else "ki")}[case]
    return base + suf


def fix_zwang(t, neuro=False):
    """Zwang- у Фрейда и в психиатрических текстах → sarışan (слово Кенана 14.11.2026)."""
    n = 0
    for a, b in SERIES_Z:
        for fa, fb in zip(_forms(a), _forms(b)):
            if fa in t:
                n += t.count(fa); t = t.replace(fa, fb)

    t, k3 = re.subn(r"(arışan hallar nevroz)(?=\s|[,.;:)»”])", r"\1u", t)
    n += k3
    t, k2 = re.subn(r"(arışan hallar nevroz)(da|dan|a|un|dur|dakı)(?![%s])" % W,
                    lambda m: m.group(1) + {"da": "unda", "dan": "undan", "a": "una", "un": "unun", "dur": "udur", "dakı": "undakı"}[m.group(2)], t)
    n += k2

    def noun(m):
        nonlocal n
        prev = re.findall(r"([%s]+)\s*$" % W, m.string[max(0, m.start() - 30):m.start()])
        pw = prev[0].lower() if prev else ""
        if pw in ("onun", "mənim", "sənin", "bizim", "sizin", "onların", "özünün", "öz") or (
                re.search(r"(?:nın|nin|nun|nün|[^aıoueəiöü](?:ın|in|un|ün))$", pw) and pw not in ("üçün", "bütün", "dərin", "keçmişin")):
            n += 1
            return ("Sarışan " if m.group(1) == "M" else "sarışan ") + m.group(2) + m.group(3)
        p = _plain(m.group(2), m.group(3))
        if p is None:
            p = m.group(2) + m.group(3)
        n += 1
        return ("Sarışan " if m.group(1) == "M" else "sarışan ") + p
    t = RX_ZNOUN.sub(noun, t)
    if not neuro:
        t, k = RX_ZADJ.subn(lambda m: "Sarışan " if m.group(1) == "M" else "sarışan ", t)
        n += k
    return t, n


# ---------------------------------------------------------------------------------------------------------------
# Слово Кенана 14.11.2026: расстройство = «pozuntu»; «pozğunluq» в клинической речи — «испорченность».
# Протокол Səhiyyə Nazirliyi 2021: «obsessiv-kompulsiv pozuntular»; Klinik Psixiatriya — pozuntu (решение 04.11).
# ---------------------------------------------------------------------------------------------------------------
POZ_ADJ = set("funksional birtərəfli mövcud nevrotik bir iki üç bu həmin o gəlinən üzvi psixi ruhi histerik ağır yüngül ümumi belə "
              "hər bütün orqanik organik sensor total parsial kəskin xroniki ilkin ikincili mərkəzi periferik spastik afazik asimvolik "
              "ataktik yeni başqa digər eyni oxşar həqiqi sırf sadə bənzər ciddi güclü zəif böyük kiçik müəyyən".split())
POZ_PART = set("olan edən gələn gəlinən yaranan edilən deyilən göstərilən törədilən yaradan doğuran mövcud funksional mental "
               "normal sensor".split())
RX_POZ = re.compile(r"(?<!etik )(?<!əxlaqi )(?<!mənəvi )(?<!əxlaq )(?<![%s])([Pp])ozğunlu(q|ğ)([%s]*)" % (W, W))   # 14.11: etik pozğunluq = испорченность (Depravation) — оставить
POZ_Q = {"": "", "da": "da", "dan": "dan", "dur": "dur", "dır": "dur", "suz": "suz", "lu": "lu", "la": " ilə", "dakı": "dakı",
         "un": "nun", "a": "ya", "dir": "dur"}
POZ_G = {"un": "nun", "a": "ya", "unun": "sunun", "una": "suna", "unda": "sunda", "undan": "sundan", "unu": "sunu",
         "udur": "sudur", "uyla": "su ilə", "undakı": "sundakı", "umun": "mun", "umuz": "muz", "um": "m", "umu": "mu",
         "ları": "ları"}


def _poz(m):
    s, kind, rest = m.group(0), m.group(2), m.group(3)
    head = "Pozuntu" if m.group(1) == "P" else "pozuntu"
    if kind == "q" and rest.startswith("lar"):
        return head + rest
    if (kind == "ğ" and rest == "u") or (kind == "q" and rest == "u"):
        before = m.string[max(0, m.start() - 40):m.start()]
        prev = re.findall(r"([%s]+)([^%s]*)$" % (W, W), before)
        pw, sep = (prev[0][0].lower(), prev[0][1]) if prev else ("", "")
        after = re.match(r"\s*([%s]+)" % W, m.string[m.end():m.end() + 30])
        nxt = after.group(1).lower() if after else ""
        gen_near = re.search(r"(?:nın|nin|nun|nün|[^aıoueəiöü\s](?:ın|in|un|ün))\s+(?:[%s]+\s+){0,2}$" % W, before) and not re.search(r"(?:üçün|bütün)\s+(?:[%s]+\s+){0,2}$" % W, before)
        nom_next = nxt in ("kimi", "olan", "olduğu", "olduqda", "var", "yoxdur", "idi", "ilə", "və", "ya", "isə", "deyil", "üçün",
                           "zamanı", "halında", "nəticəsində", "səbəbindən", "müəyyən", "aşkar", "baş", "qalır", "yaranır", "mövcuddur") or nxt.endswith(("dır", "dir", "dur", "dür"))
        adj = ((pw in POZ_ADJ or pw in POZ_PART or re.search(r"(?:tik|nik|rik|zik|sik)$", pw)
                or re.search(r"(?:lar|lər)(?:da|də|dan|dən|a|ə)$", pw) or re.search(r"[,;:.()«»“”\"—–-]", sep) or not pw)
               and not gen_near and not nom_next)
        return head + ("nu" if adj else "su")
    tab = POZ_Q if kind == "q" else POZ_G
    if rest in tab:
        return head + tab[rest]
    return s


POZ_AFTER = [("rast gəlinən pozuntunu libidonun", "rast gəlinən pozuntusu libidonun"),   # GW14: funksiyasının … pozuntusu
             ("mənbə.) pozuntunu həkim", "mənbə.) pozuntusu həkim")]                     # GW02 07.312


def fix_pozg(t):
    t2, n = RX_POZ.subn(_poz, t)
    for a_, b_ in POZ_AFTER:
        t2 = t2.replace(a_, b_)
    return t2, sum(1 for _ in RX_POZ.finditer(t)) - sum(1 for _ in RX_POZ.finditer(t2))


# «batil inanc» (суеверие) допустим, но не часто (слово Кенана 14.11.2026): в одном абзаце — один раз, повтор → «xurafat».
RX_BATIL = re.compile(r"(?<![%s])([Bb])atil inanc(?!lı)([%s]*)" % (W, W))


def fix_batil(t):
    n = 0
    out = []
    for chunk in re.split(r"(</p>|\n)", t):
        seen = [0]

        def rep(m):
            nonlocal n
            seen[0] += 1
            if seen[0] == 1:
                return m.group(0)
            n += 1
            return ("X" if m.group(1) == "B" else "x") + "urafat" + m.group(2)
        out.append(RX_BATIL.sub(rep, chunk))
    return "".join(out), n


def fix_text(t, langs=("az", "ru"), path=""):
    t, n = fix_base(t, langs)
    for a, b in EXACT:
        for src in (a, a[:1].upper() + a[1:], ("İ" + a[1:]) if a[:1] == "i" else a):
            if src in t:
                c = t.count(src); n += c
                t = t.replace(src, _cap(src, b))
    t, k = RX_SER.subn(_ser, t)
    # после кавычки аффикс пишется со связкой: «… iflici»nə, «… iflici»nin (калька давала «… iflic»ə)
    t = re.sub(r"((?:serebral|psevdobulbar) iflici»)(ə|in|də|dən|i)(?![%s])" % W, lambda m: m.group(1) + {"ə": "nə", "in": "nin", "də": "ndə", "dən": "ndən", "i": "ni"}[m.group(2)], t)
    if "az" in langs:
        t, z = fix_az(t, path)
        k += z
    return t, n + k


def _az_rules(t, path=""):
    t, z = fix_zwang(t, neuro=any(x in (path or "") for x in NEURO))
    t, p = fix_pozg(t)
    t, b = fix_batil(t)
    t, r = fix_turk(t, path)
    t, o = fix_freud_obs(t, path)
    # 14.11 вечер: последнее слово Кенана — 6B64/6B65 = «identiklik» (правила в списке выше), identifikasiya отменено
    t = t.replace("təmizlikə", "təmizliyə")              # опечатка (GW05)
    return t, z + p + b + r + o


def fix_az(t, path=""):
    """слово Кенана 14.11.2026; в многоязычном JSON (book.json: {"az": …, "tr": …}) — только значения под «az»,
    турецкий и русский текст не трогается (kimlik, sinirli, bölüm, yetişkin — обычные турецкие слова)."""
    s = t.lstrip()
    if s[:1] in "{[" and ('"tr"' in t or '"ru"' in t or '"en"' in t):
        try:
            o = json.loads(t)
        except ValueError:
            o = None

        def multilang(x):
            if isinstance(x, dict):
                if "az" in x and any(k in x for k in ("ru", "en", "tr")):
                    return True
                return any(multilang(v) for v in x.values())
            if isinstance(x, list):
                return any(multilang(v) for v in x)
            return False
        if o is not None and multilang(o):
            fmt = None
            for ind in (1, None, 2):
                for end in ("", "\n"):
                    if json.dumps(o, ensure_ascii=False, indent=ind) + end == t:
                        fmt = (ind, end); break
                if fmt: break
            if fmt:
                cnt = [0]

                def walk(x, az):
                    if isinstance(x, str):
                        if not az:
                            return x
                        y, c = _az_rules(x, path); cnt[0] += c
                        return y
                    if isinstance(x, list):
                        return [walk(v, az) for v in x]
                    if isinstance(x, dict):
                        ml = "az" in x and any(k in x for k in ("ru", "en", "tr"))
                        return {k: walk(v, (k == "az") if ml else az) for k, v in x.items()}
                    return x
                o2 = walk(o, True)
                return json.dumps(o2, ensure_ascii=False, indent=fmt[0]) + fmt[1], cnt[0]
    return _az_rules(t, path)


# турцизмы (слово Кенана 14.11.2026: «не путай азербайджанские фразы с турецкими»); (регэксп основы, замена основы)
_B = r"(?<![%s])" % W
TURK = [(re.compile(_B + a), b) for a, b in [
    (r"sinirlilik", "əsəbilik"), (r"Sinirlilik", "Əsəbilik"), (r"sinirliliy", "əsəbiliy"), (r"sinirliy", "əsəbiliy"), (r"Sinirliliy", "Əsəbiliy"), (r"Sinirliy", "Əsəbiliy"),
    (r"sinirli(?![%s])" % W, "əsəbi"), (r"Sinirli(?![%s])" % W, "Əsəbi"),         # тур. sinirli; az. əsəbi (Nervosität)
    (r"anlamına gəl", "mənasına gəl"),
    (r"yetişkin", "yetkin"), (r"Yetişkin", "Yetkin"),
    (r"ilgisiz", "əhəmiyyətsiz"), (r"İlginc", "Maraqlı"), (r"ilginc", "maraqlı"),
    (r"bölümdə(?![%s])" % W, "bölmədə"), (r"bölümə(?![%s])" % W, "bölməyə"), (r"bölüm(?![%s])" % W, "bölmə"),
    (r"yönəlikdir", "yönəlmişdir"), (r"yönəlik(?![%s])" % W, "yönəlmiş"),
    (r"özgüvən", "özünəinam"), (r"Özgüvən", "Özünəinam"),
    (r"önəmlidir", "vacibdir"), (r"önəmsizdir", "əhəmiyyətsizdir"), (r"Önəmli", "Vacib"), (r"önəmli", "vacib"),
    (r"söz konusudur", "söhbət gedir"),
    (r"dəyərləndir", "qiymətləndir"), (r"Dəyərləndir", "Qiymətləndir"),
    # 14.11: «üzgün/üzgünlük» — азерб. «изнурённый/изнурение» (obastan): правило снято
    (r"özəlliklər", "xüsusiyyətlər"), (r"özəllik", "xüsusiyyət"),
    (r"bilginin", "biliyin"), (r"olması bilgisi", "olması haqqında bilik"),
    (r"endişələrsiz", "narahatlıqsız"), (r"səbəb-sonuç", "səbəb-nəticə"), (r"uyqu yürüşü", "yuxugəzmə"),
    (r"təsvir edilmiş gibi", "təsvir edilmiş kimi"),
    (r"suçüstü", "cinayət başında"),
]]


# 14.11 (слово Кенана): «kimlik» — азербайджанское (milli kimlik: au.edu.az, bqu.edu.az; Google «национальная идентичность» → «milli kimlik»);
# правила kimlik → identiklik/şəxsiyyət сняты (identiklik = тождество предметов, obastan). Тексты пересчитаны от исходных версий.


OBS_FREUD = re.compile(r"(?<![%s])([Oo]bsess?iv|[Zz]orlayıcı)(?=\s+(?:fikir|fikr|təsəvvür|hərəkət|ideya|düşüncə|simptom|hiss|şübhə|qorxu|"
                       r"məşğuliyyət|ədəd|impuls|ritual|mərasim|affekt|təfəkkür))" % W)


def fix_freud_obs(t, path=""):
    """у Фрейда «obsessiv fikir…», «zorlayıcı təsəvvür…» на месте Zwangs- → «sarışan» (в Klinik «obsessiv» — термин МКБ, не трогать)"""
    p = (path or "").lower()
    if not ("freud" in p or "kitab_" in p or "jung" in p or "fliess" in p):
        return t, 0
    return OBS_FREUD.subn(lambda m: "Sarışan" if m.group(1)[0] in "OZ" else "sarışan", t)


def fix_turk(t, path=""):
    n = 0
    for rx, rep in TURK:
        t, k = rx.subn(rep, t)
        n += k
    return t, n


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


def _az_part(txt):
    """текст для стража AZ: в многоязычном JSON — только значения под «az»; HTML — без тегов."""
    try:
        o = json.loads(txt)
    except ValueError:
        return re.sub(r"<[^>]+>", " ", txt)
    out = []

    def walk(x, az):
        if isinstance(x, str):
            if az:
                out.append(x)
        elif isinstance(x, list):
            for v in x:
                walk(v, az)
        elif isinstance(x, dict):
            ml = "az" in x and any(k in x for k in ("ru", "en", "tr"))
            for k, v in x.items():
                walk(v, (k == "az") if ml else az)
    walk(o, True)
    return re.sub(r"<[^>]+>", " ", "\n".join(out))


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
        nt, n = fix_text(t, lg, path=f)
        if n and nt != t:
            total += n
            print("%4d  %s" % (n, os.path.relpath(f, D)))
            if mode == "--fix":
                tmp = f + ".tmp"
                io.open(tmp, "w", encoding="utf-8", newline="\n").write(nt)
                os.replace(tmp, f)
        chk = nt if mode == "--fix" else t
        txt = re.sub(r"<[^>]+>", " ", chk)
        for m in list(REJECT.finditer(txt)) + (list(REJECT_AZ.finditer(_az_part(chk))) if "az" in lg else []):
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
