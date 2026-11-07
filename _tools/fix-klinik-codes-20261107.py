# -*- coding: utf-8 -*-
"""_tools/fix-klinik-codes-20261107.py — «Клиническая психиатрия»: правки кодов и названий глав по проверке
CODES_CHECK_AZ_20261107 (WHO ICD API МКБ-11 2024-01 / МКБ-10 2019, APA DSM-5-TR). Все языки, идемпотентно.
  A. 6B64: код XBT-10 F44.81 → F44.8 (F44.81 — код МКБ-10-CM/DSM-5-TR, в МКБ-10 ВОЗ его нет) + название.
  B. Названия глав: «(XBT-11)», обрезанное «Maddə ilə əlaqəli», «Perinatal…», «İkincili psixiatriya»,
     «Psychosomatic factors…» → названия по МКБ-11 ВОЗ (по языкам).
  C. Артефакты заголовков AZ: «((ing. …))», «(X (ing. …))», «(6D71)».
Запуск:  python _tools/fix-klinik-codes-20261107.py [--dry]
"""
import os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "klinik-psixiatriya")
DRY = "--dry" in sys.argv

A_ROW = {  # язык → (новое имя в строке XBT-10 для 6B64)
    "": "Digər dissosiativ [konversion] pozuntular (çoxlu şəxsiyyət pozuntusu daxil olmaqla; F44.81 — XBT-10-un ABŞ modifikasiyasının (ICD-10-CM) və DSM-5-TR kodudur, ÜST-in XBT-10-da yoxdur)",
    "en": "Other dissociative [conversion] disorders (including multiple personality disorder; F44.81 is an ICD-10-CM / DSM-5-TR code and does not exist in WHO ICD-10)",
    "tr": "Diğer disosiyatif [konversiyon] bozukluklar (çoklu kişilik bozukluğu dâhil; F44.81 ICD-10-CM / DSM-5-TR kodudur, DSÖ ICD-10'da yoktur)",
    "ru": "Другие диссоциативные [конверсионные] расстройства (включая расстройство множественной личности; F44.81 — код МКБ-10-CM / DSM-5-TR, в МКБ-10 ВОЗ его нет)",
}
B = {  # язык → [(старое, новое)]
    "": [("Təşviş və qorxu ilə əlaqəli pozuntular (XBT-11)", "Təşviş və qorxu ilə əlaqəli pozuntular"),
         ("Maddə ilə əlaqəli", "Maddə istifadəsi və ya asılılıq davranışları ilə əlaqəli pozuntular"),
         ("Perinatal pozuntular", "Hamiləlik, doğuş və zahılıq dövrü ilə əlaqəli pozuntular"),
         ("İkincili psixiatriya", "İkincili psixi və ya davranış sindromları"),
         ("Yuxu-oyanıqlıq pozuntuları (Sleep-wake disorders)", "Yuxu-oyanıqlıq pozuntuları")],
    "en": [("Perinatal disorders", "Pregnancy, childbirth and puerperium disorders"),
           ("Psychosomatic factors", "Psychological and behavioural factors"),
           ("Secondary psychiatry", "Secondary mental or behavioural syndromes")],
    "tr": [("Perinatal bozukluklar", "Gebelik, doğum ve lohusalık dönemi bozuklukları"),
           ("Psikosomatik faktörler", "Psikolojik ve davranışsal faktörler")],
    "ru": [("Перинатальные расстройства", "Расстройства, связанные с беременностью, родами и послеродовым периодом"),
           ("Психосоматические факторы", "Психологические и поведенческие факторы"),
           ("Вторичная психиатрия", "Вторичные психические и поведенческие синдромы")],
}
GLOSS_AZ = [("(Substance-related)", "(Substance use or addictive behaviours)"),
            ("(Perinatal disorders)", "(Pregnancy, childbirth and puerperium disorders)"),
            ("(Secondary psychiatry)", "(Secondary mental or behavioural syndromes)"),
            ("(Psychosomatic factors)", "(Psychological and behavioural factors)"),
            ("Yuxu-oyanıqlıq pozuntuları (Sleep disorders)", "Yuxu-oyanıqlıq pozuntuları (Sleep-wake disorders)")]
stat = {}


def bump(k, n=1):
    stat[k] = stat.get(k, 0) + n


def rule_sub(pat, rep, s, key, flags=0):
    s2, n = re.subn(pat, rep, s, flags=flags)
    if n:
        bump(key, n)
    return s2


for lang in ("", "en", "tr", "ru"):
    d = os.path.join(BOOK, lang) if lang else BOOK
    files = sorted(glob.glob(os.path.join(d, "*.html")) + glob.glob(os.path.join(d, "search-index.json")))
    for f in files:
        s = open(f, encoding="utf-8", newline="").read()
        o = s
        base = os.path.basename(f)
        L = lang or "az"
        if base == "6B64.html":
            s = rule_sub(r'(<span class="dh-lbl">(?:XBT-10|ICD-10|МКБ-10)</span><span class="dh-code">)F44\.81(</span></td><td class="dh-name">)[^<]*(</td>)',
                         lambda m: m.group(1) + "F44.8" + m.group(2) + A_ROW[lang] + m.group(3), s, L + ":A 6B64")
        for old, new in B[lang]:
            s = rule_sub(r'([>"]|— )' + re.escape(old) + r'( \||[<"]| \()', lambda m, n=new: m.group(1) + n + m.group(2), s, L + ":B " + old[:24])
        # D. дубль скобок в h1 страниц глав: «Name (OKP) (OKP)» → «Name (OKP)»
        s = rule_sub(r'(<h1 class="bk-chead__h1">[^<]*?)(\s\(([^()]+)\))\s\(\3\)(</h1>)', r'\1\2\4', s, L + ":D h1 dup")
        if lang == "":
            for old, new in GLOSS_AZ:
                if old in s:
                    bump("az:B gloss " + old[:20], s.count(old)); s = s.replace(old, new)
            # C. артефакты заголовков
            h1 = re.compile(r'(<h1 class="bk-chead__h1">)(.*?)(</h1>)', re.S)
            def fixh1(m):
                t = m.group(2)
                t = re.sub(r'\(\(ing\. ([^()]+)\)\)', r'(\1)', t)
                t = re.sub(r'\((?:[^()]+) \(ing\. ([^()]+)\)\)', r'(\1)', t)
                t = re.sub(r' \(ing\. [^()]+\) \(', ' (', t)
                t = t.replace(' (6D71)', '')
                return m.group(1) + t + m.group(3)
            s2 = h1.sub(fixh1, s)
            if s2 != s: bump("az:C h1 artefacts"); s = s2
            s = rule_sub(r' \(ing\. [^()]*\)(</span>)', r'\1', s, "az:C menu '(ing. …)'", flags=0) if base.startswith(("index", "6", "7", "8", "G", "H", "0", "1", "2", "mundericat")) or True else s
            s = rule_sub(r'(<title>[^<]*?|<meta (?:property="og:title"|name="description"|property="og:description") content="[^"]*?) \(ing\. [^()]*\)', r'\1', s, "az:C title/meta '(ing. …)'")
            s = rule_sub(r'(?i)(pozuntu) \(6D71\)', r'\1', s, "az:C (6D71)")
        if s != o:
            bump("files " + (lang or "az"))
            if not DRY:
                open(f, "w", encoding="utf-8", newline="").write(s)
for k in sorted(stat):
    print(k, stat[k])
print("[DRY]" if DRY else "[OK]")
