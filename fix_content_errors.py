#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Исправление контентных ошибок:
 1. bolme-11: переименование главы и расстройств 6C20/6C21
 2. bolme-13: перепутаны XBT-10 и DSM коды у 6C70/71/72/73
 3. bolme-01: перепутаны коды 6A03/6A04/6A05 в h1 и XBT-10/DSM
Плюс обновление sidebar/nav во всех файлах.
"""
import glob, os

BASE   = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"
ALL    = sorted(glob.glob(os.path.join(BASE, "*.html")))

def patch(fpath, replacements):
    with open(fpath, encoding="utf-8") as f:
        html = f.read()
    orig = html
    for old, new in replacements:
        html = html.replace(old, new)
    if html != orig:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(html)
        return True
    return False

changed = {}

# ═══════════════════════════════════════════════════════════════════════════════
# 1. BOLME-11 — переименование главы и расстройств
# ═══════════════════════════════════════════════════════════════════════════════

b11 = os.path.join(BASE, "bolme-11.html")

b11_changes = [
    # Meta + title
    ('content="Klinik Psixiatriya — BÖLMƏ 11 — BƏDƏNSƏL DISSTRES"',
     'content="Klinik Psixiatriya — BÖLMƏ 11 — BƏDƏN DİSSTRESİ"'),
    ('<title>BÖLMƏ 11 — BƏDƏNSƏL DISSTRES | KLİNİK PSİXİATRİYA</title>',
     '<title>BÖLMƏ 11 — BƏDƏN DİSSTRESİ | KLİNİK PSİXİATRİYA</title>'),

    # H2 заголовок главы (с id)
    ('<h2 id="bədənsəl-disstres-və-əlaqəli-pozuntular" class="">6C20 – 6C2Z · BƏDƏNSƏL DISSTRES VƏ ƏLAQƏLİ POZUNTULAR</h2>',
     '<h2 id="bədən-distresi-və-hissiyəti-pozuntulari" class="">6C20 – 6C2Z · BƏDƏN DİSSTRESİ VƏ HİSSİYƏTİ POZUNTULARI</h2>'),

    # H1 + XBT-11 + таблица для 6C20
    ('<h1 id="6c20-bədənsəl-disstres-pozuntusu" class="h-disorder"><span class="icd">6C20</span> BƏDƏNSƏL DISSTRES POZUNTUSU</h1>',
     '<h1 id="6c20-bədən-disstres-pozuntusu" class="h-disorder"><span class="icd">6C20</span> BƏDƏN DİSSTRES POZUNTUSU</h1>'),

    ('<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C20</span> — Bədənsəl disstres pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C20</span> — Bədən disstres pozuntusu</div>'),

    # H1 + XBT-11 для 6C21
    ('<h1 id="6c21-bədən-bütövlüyü-disforiyasi" class="h-disorder"><span class="icd">6C21</span> BƏDƏN BÜTÖVLÜYÜ DİSFORİYASI</h1>',
     '<h1 id="6c21-bədən-bütövlüyünü-qavrama-pozuntusu" class="h-disorder"><span class="icd">6C21</span> BƏDƏN BÜTÖVLÜYÜNÜ QAVRAMA POZUNTUSU</h1>'),

    ('<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C21</span> — Bədən bütövlüyü disforiyasi</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C21</span> — Bədən bütövlüyünü qavrama pozuntusu</div>'),

    # Таблица расстройств + текст параграфа
    ('<td>Bədənsəl disstres pozuntusu</td>',
     '<td>Bədən disstres pozuntusu</td>'),
    ('"Bədənsəl disstres pozuntusu"',
     '"Bədən disstres pozuntusu"'),
    ('Bədənsəl disstres pozuntusu –',
     'Bədən disstres pozuntusu –'),
]
if patch(b11, b11_changes):
    changed["bolme-11.html"] = "chapter+disorder rename"

# ── Sidebar во всех файлах ────────────────────────────────────────────────────
sidebar_b11 = [
    # nav-link span (глава 11)
    ('<span>BƏDƏNSƏL DISSTRES VƏ ƏLAQƏLİ POZUNTULAR</span>',
     '<span>BƏDƏN DİSSTRESİ VƏ HİSSİYƏTİ POZUNTULARI</span>'),

    # nav-sub-link (подпункт 6C20)
    ('href="bolme-11.html#6c20-bədənsəl-disstres-pozuntusu"',
     'href="bolme-11.html#6c20-bədən-disstres-pozuntusu"'),
    ('<span class="sub-name">BƏDƏNSƏL DISSTRES POZUNTUSU</span>',
     '<span class="sub-name">BƏDƏN DİSSTRES POZUNTUSU</span>'),
]
for fpath in ALL:
    if patch(fpath, sidebar_b11):
        changed[os.path.basename(fpath)] = "sidebar bolme-11"

# ═══════════════════════════════════════════════════════════════════════════════
# 2. BOLME-13 — исправление XBT-10 и DSM для 4 расстройств
# ═══════════════════════════════════════════════════════════════════════════════

b13 = os.path.join(BASE, "bolme-13.html")

b13_changes = [
    # ── 6C72 PİROMANİYA: неправильные XBT-10 (cinsi) и DSM (cinsi) ──────────
    ('<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F52.7</span> — Həddindən artıq cinsi əlaqə</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F63.1</span> — Patoloji oduvurma</div>'),
    ('<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> — — compulsive sexual behavior disorder</div>',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> 312.33 — Pyromania</div>'),

    # ── 6C71 KLEPTOMANİYA: XBT-10 F63.1 (piromaniya!) → F63.2, DSM piromaniya → kleptomaniya ──
    ('<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F63.1</span> — Patoloji oduvurma</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F63.2</span> — Patoloji oğurlama</div>'),
    ('<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> 312.33 — Pyromania</div>',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> 312.32 — Kleptomania</div>'),

    # ── 6C73 KOMPULSİV CİNSİ: XBT-10 F63.8 → F52.7, DSM IED → cinsi ────────
    ('<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F63.8</span> — İmpuls nəzarəti pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F52.7</span> — Həddindən artıq cinsi əlaqə</div>'),
    ('<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> 312.34 — Intermittent explosive disorder</div>',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> — — Compulsive sexual behaviour disorder</div>'),

    # ── 6C70 EPİZODİK EKSPLOSİV: XBT-10 F63.2 (oğurlama!) → F63.8, DSM kleptomaniya → IED ──
    ('<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F63.2</span> — Patoloji oğurlama</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F63.8</span> — Digər vərdiş və impuls pozuntuları</div>'),
    ('<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> 312.32 — Kleptomania</div>',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> 312.34 — Intermittent explosive disorder</div>'),

    # ── Таблица в начале главы (коды ↔ названия перепутаны) ──────────────────
    ('<td><strong><span class="icd">6C70</span></strong></td><td>Piromaniya</td>',
     '<td><strong><span class="icd">6C70</span></strong></td><td>İntermittent eksplosiv pozuntu</td>'),
    ('<td><strong><span class="icd">6C72</span></strong></td><td>Kompulsiv cinsi davranış pozuntusu</td>',
     '<td><strong><span class="icd">6C72</span></strong></td><td>Piromaniya</td>'),
    ('<td><strong><span class="icd">6C73</span></strong></td><td>İntermittent eksplosiv pozuntu</td>',
     '<td><strong><span class="icd">6C73</span></strong></td><td>Kompulsiv cinsi davranış pozuntusu</td>'),
]
if patch(b13, b13_changes):
    changed["bolme-13.html"] = "6C70/71/72/73 XBT-10+DSM fixed"

# ═══════════════════════════════════════════════════════════════════════════════
# 3. BOLME-01 — исправление кодов 6A03/6A04/6A05 + XBT-10/DSM
#    Порядок ВАЖЕН: делаем через промежуточные значения чтобы не перепутать
# ═══════════════════════════════════════════════════════════════════════════════

b01 = os.path.join(BASE, "bolme-01.html")

b01_changes = [
    # ── Блок "learning disorder" — сейчас ошибочно помечен как 6A04 ──────────
    # Меняем 6A04 → 6A03 в h1, id, XBT-11 span
    ('<h1 id="6a04-inkişaf-öyrənmə-pozuntusu" class="h-disorder"><span class="icd">6A04</span> İNKİŞAF ÖYRƏNMƏ POZUNTUSU</h1>',
     '<h1 id="6a03-inkişaf-öyrənmə-pozuntusu" class="h-disorder"><span class="icd">6A03</span> İNKİŞAF ÖYRƏNMƏ POZUNTUSU</h1>'),
    ('<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A04</span> — İnkişaf öyrənmə pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A03</span> — İnkişaf öyrənmə pozuntusu</div>'),
    # XBT-10: F82 (coordination) → F81 (learning)
    ('<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F82</span> — Hərəkət koordinasiyasının spesifik pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F81</span> — Məktəb bacarıqlarının spesifik pozuntuları</div>'),
    # DSM: 315.4 DCD → 315.00 Specific learning disorder
    ('<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> 315.4 — Developmental coordination disorder</div>',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> 315.00 — Specific learning disorder</div>'),

    # ── Блок "coordination disorder" — ошибочно помечен как 6A05 ─────────────
    ('<h1 id="6a05-inkişaf-hərəki-koordinasiya-pozuntusu" class="h-disorder"><span class="icd">6A05</span> İNKİŞAF HƏRƏKİ KOORDİNASİYA POZUNTUSU</h1>',
     '<h1 id="6a04-inkişaf-hərəki-koordinasiya-pozuntusu" class="h-disorder"><span class="icd">6A04</span> İNKİŞAF HƏRƏKİ KOORDİNASİYA POZUNTUSU</h1>'),
    ('<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A05</span> — İnkişaf hərəki koordinasiya pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A04</span> — İnkişaf hərəki koordinasiya pozuntusu</div>'),
    # XBT-10: F90 (ADHD!) → F82 (coordination)
    ('<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F90</span> — Hiperkinetik pozuntular</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F82</span> — Hərəkət koordinasiyasının spesifik pozuntusu</div>'),
    # DSM: 314.01 ADHD → 315.4 DCD
    ('<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> 314.01 — Attention-deficit/hyperactivity disorder</div>',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> 315.4 — Developmental coordination disorder</div>'),

    # ── Блок "ADHD" — ошибочно помечен как 6A03 ──────────────────────────────
    ('<h1 id="6a03-diqqət-defisiti-və-hiperaktivlik-pozuntusu-ddhp" class="h-disorder"><span class="icd">6A03</span> DİQQƏT DEFİSİTİ VƏ HİPERAKTİVLİK POZUNTUSU (DDHP)</h1>',
     '<h1 id="6a05-diqqət-defisiti-və-hiperaktivlik-pozuntusu-ddhp" class="h-disorder"><span class="icd">6A05</span> DİQQƏT DEFİSİTİ VƏ HİPERAKTİVLİK POZUNTUSU (DDHP)</h1>'),
    ('<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A03</span> — Diqqət defisiti və hiperaktivlik pozuntusu (DDHP)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A05</span> — Diqqət defisiti və hiperaktivlik pozuntusu (DDHP)</div>'),
    # XBT-10: F81 (learning!) → F90 (ADHD)
    ('<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F81</span> — Məktəb bacarıqlarının spesifik pozuntuları</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F90</span> — Hiperkinetik pozuntular</div>'),
    # DSM: 315.00 learning → 314.01 ADHD
    ('<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> 315.00 — Specific learning disorder</div>',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> 314.01 — Attention-deficit/hyperactivity disorder</div>'),
]
if patch(b01, b01_changes):
    changed["bolme-01.html"] = "6A03/04/05 codes+XBT-10+DSM fixed"

# ── Sidebar nav ссылки для bolme-01 во всех файлах ───────────────────────────
sidebar_b01 = [
    ('href="bolme-01.html#6a04-inkişaf-öyrənmə-pozuntusu"',
     'href="bolme-01.html#6a03-inkişaf-öyrənmə-pozuntusu"'),
    ('href="bolme-01.html#6a05-inkişaf-hərəki-koordinasiya-pozuntusu"',
     'href="bolme-01.html#6a04-inkişaf-hərəki-koordinasiya-pozuntusu"'),
    ('href="bolme-01.html#6a03-diqqət-defisiti-və-hiperaktivlik-pozuntusu-ddhp"',
     'href="bolme-01.html#6a05-diqqət-defisiti-və-hiperaktivlik-pozuntusu-ddhp"'),
    # nav-sub-link sub-code spans (если есть отдельно)
    ('<span class="sub-code">6A04</span><span class="sub-name">İNKİŞAF ÖYRƏNMƏ POZUNTUSU</span>',
     '<span class="sub-code">6A03</span><span class="sub-name">İNKİŞAF ÖYRƏNMƏ POZUNTUSU</span>'),
    ('<span class="sub-code">6A05</span><span class="sub-name">İNKİŞAF HƏRƏKİ KOORDİNASİYA POZUNTUSU</span>',
     '<span class="sub-code">6A04</span><span class="sub-name">İNKİŞAF HƏRƏKİ KOORDİNASİYA POZUNTUSU</span>'),
    ('<span class="sub-code">6A03</span><span class="sub-name">DİQQƏT DEFİSİTİ VƏ HİPERAKTİVLİK POZUNTUSU (DDHP)</span>',
     '<span class="sub-code">6A05</span><span class="sub-name">DİQQƏT DEFİSİTİ VƏ HİPERAKTİVLİK POZUNTUSU (DDHP)</span>'),
]
for fpath in ALL:
    if patch(fpath, sidebar_b01):
        key = os.path.basename(fpath)
        changed[key] = changed.get(key, "") + " sidebar-b01"

# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 60)
print(f"Изменено файлов: {len(changed)}")
for f, desc in sorted(changed.items()):
    print(f"  {f}: {desc}")
