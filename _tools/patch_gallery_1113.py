# -*- coding: utf-8 -*-
"""Галереи дипломов и сертификатов (слово Кенана 13.11.2026): без повторов и с оригиналами — имена студентов не закрашивать
(студенты дали согласие; сертификаты проверяются по QR-коду). Повторный запуск ничего не меняет."""
import io, json, os, re, shutil, sys
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
OLD = "D:/Projects/Ragimoff/old_versions/2026-11-12_site_before_v11/images"
ARC = "_agent/moved/gallery_20261113"
os.makedirs(ARC, exist_ok=True)


def jl(p):
    return json.load(io.open(p, encoding="utf-8"))


def js(p, o):
    s = json.dumps(o, ensure_ascii=False, indent=1) + "\n"
    if io.open(p, encoding="utf-8").read() != s:
        io.open(p + ".new", "w", encoding="utf-8", newline="\n").write(s)
        os.replace(p + ".new", p)
        print("исправлен", p)


# 1) образцы сертификатов: оригиналы с именем вместо закрашенных
for dst, src in (("assets/img/programs/proof/cert.jpg", OLD + "/certificate/sample-cert-ipas-klinik.jpg"),
                 ("assets/img/programs/proof/cert-family.jpg", OLD + "/certificate/sample-cert-ipas-family.jpg"),
                 ("assets/img/programs/proof/diploma-psy.jpg", OLD + "/institute/diplom-psy-b-spb-idpo.jpg")):
    im = Image.open(src).convert("RGB")
    if im.width > 1500:
        im = im.resize((1500, round(im.height * 1500 / im.width)), Image.LANCZOS)
    if os.path.exists(dst) and not os.path.exists(os.path.join(ARC, os.path.basename(dst))):
        shutil.copy2(dst, os.path.join(ARC, os.path.basename(dst)))       # закрашенный вариант — в архив, не удаляется
    tmp = dst + ".new.jpg"
    im.save(tmp, quality=88, optimize=True)
    if os.path.exists(dst) and open(dst, "rb").read() == open(tmp, "rb").read():
        os.remove(tmp)
    else:
        os.replace(tmp, dst)
        print("оригинал:", dst, "←", os.path.basename(src))

# 2) образец документа программы: «Общая психология» — диплом психолога, «Семейная терапия» — сертификат семейной терапии
p = "assets/js/programs.js"
s = io.open(p, encoding="utf-8").read()
o = s
idx = [m.start() for m in re.finditer(r"sample: '(\w[\w-]*)',", s)]
assert len(idx) == 7, len(idx)
# порядок программ в programs.js: general, clinical, practicum, psychodiagnostics, cbt, psychoanalysis, family
want = ["diploma-psy", "diploma", "cert", "cert", "cert", "cert", "cert-family"]
parts, last = [], 0
for i, st in enumerate(idx):
    e = s.index(",", st)
    parts.append(s[last:st])
    parts.append("sample: '%s'" % want[i])
    last = e
parts.append(s[last:])
s = "".join(parts)
if s != o:
    io.open(p + ".new", "w", encoding="utf-8", newline="\n").write(s)
    os.replace(p + ".new", p)
    print("исправлен", p)
p = "assets/js/page-program.js"
s = io.open(p, encoding="utf-8").read()
a = "assets/img/programs/proof/${P.sample === 'diploma' ? 'diploma' : 'cert'}.jpg"
b = "assets/img/programs/proof/${P.sample}.jpg"
a2 = "$('#ppLawDocs').innerHTML = d.gallery.map("
b2 = "$('#ppLawDocs').innerHTML = d.gallery.filter(x => !x.only || x.only.indexOf(slug) >= 0).map("   # документ — только на странице своей программы
if a in s or a2 + "x =>" in s:
    s = s.replace(a, b).replace(a2 + "x =>", b2 + "x =>")
    io.open(p + ".new", "w", encoding="utf-8", newline="\n").write(s)
    os.replace(p + ".new", p)
    print("исправлен", p)

# 3) галерея документов программ (общая для «Общей» и «Клинической психологии»)
ONLY = {
    "diplom-psy-b-spb-idpo.jpg": None,            # диплом психолога — уже образцом вверху «Общей психологии»
    "diplom-spb-idpo.webp": None,                 # диплом клинического психолога — уже образцом вверху «Клинической психологии»
    "diplom-psy-spb-idpo.webp": ["general"],      # таблица дисциплин программы «Психология» (1556 ч)
    "diplom-predmety.webp": ["clinical"],         # таблица дисциплин программы «Клиническая психология» (1528 ч)
    "diplom-spb-prilozhenie.webp": ["clinical"],  # приложение к диплому «Клиническая психология»
}
CAP = {"diplom-psy-spb-idpo.webp": {"az": "Diploma əlavə: fənlər cədvəli — «Psixologiya» proqramı", "ru": "Приложение к диплому: дисциплины программы «Психология»", "en": "Diploma supplement: subjects of the Psychology programme"},
       "diplom-predmety.webp": {"az": "Diploma əlavə: fənlər cədvəli — «Klinik psixologiya» proqramı", "ru": "Приложение к диплому: дисциплины программы «Клиническая психология»", "en": "Diploma supplement: subjects of the Clinical Psychology programme"}}
for lang in ("az", "ru", "en"):
    p = "data/law/law.%s.json" % lang
    d = jl(p)
    g = []
    for x in d["gallery"]:
        f = x["src"].split("/")[-1]
        if f in ONLY and ONLY[f] is None:
            continue
        if f in ONLY:
            x["only"] = ONLY[f]
        if f in CAP:
            x["cap"] = CAP[f][lang]
        g.append(x)
    d["gallery"] = g
    js(p, d)

# 4) дипломы Кенана: два повтора убраны (удостоверение Бехтерева № 077037 и розовый сертификат 2003 стояли дважды),
#    картинки поставлены к своим подписям (подписи на трёх языках — прежние, по порядку прежних позиций)
K = "/images/specialists/kenan/diplomas/"
#           (файл, номер прежней подписи 1..11)
NEW = [("adtu-diplom-2000.jpg", 1),          # IPAS Ambassador 2022 (имя файла неверное, картинка — сертификат IPAS)
       ("nlp-diploma-1999.jpg", 2),          # Институт Бехтерева: удостоверение № 077037 (ординатура 2001–2003, психотерапия)
       ("ipas-ambassador-2022.jpg", 3),      # диплом АГМУ 2000
       ("sert-psychotherapy-2003.jpg", 5),   # сертификат «Психотерапия» 2003
       ("bekhterev-udost-2.jpg", 6),         # диплом НЛП 1999
       ("internatura-2001.jpg", 7),          # APA, курс по травме (ПТСР) 2000
       ("gtc-cert-team-2007.jpg", 11),       # удостоверение интернатуры 2001
       ("sert-a2139286.jpg", 9),             # GTC 2007
       ("sert-a2139298.jpg", 10)]            # GTC 2008
for lang in ("az", "ru", "en"):
    p = "data/spec/kenan.%s.json" % lang
    d = jl(p)
    blk = [b for b in d["blocks"] if b.get("type") == "gallery" and any("diplomas/" in x.get("src", "") for x in b.get("items", []))]
    assert len(blk) == 1, (lang, len(blk))
    items = blk[0]["items"]
    if len(items) == 11:
        cap = [x.get("cap", "") for x in items]
        blk[0]["items"] = [dict(items[0], src=K + f, cap=cap[n - 1]) for f, n in NEW]
        for it, (f, n) in zip(blk[0]["items"], NEW):
            for k in ("thumb", "w", "h"):
                it.pop(k, None)
        js(p, d)
print("готово")
