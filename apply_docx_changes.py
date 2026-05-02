#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Применить 3 подтверждённых изменения из нового DOCX."""
import glob, os, re

BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"
files = sorted(glob.glob(os.path.join(BASE, "bolme-*.html")))

changed_total = 0

# ── ЗАМЕНА 1: sidebar во всех файлах ──────────────────────────────────────────
# bolme-09: старое → новое название главы
OLD9  = "YEMƏ VƏ YEMƏKƏBENZƏRİ DAVRANIŞ POZUNTULARI"
NEW9  = "QİDA QƏBULU VƏ QİDA DAVRANIŞI POZUNTULARI"
# bolme-22: старое → новое название главы
OLD22 = "İKİNCİLİ PSİXİ VƏ DAVRANIŞ SİNDROMLARI"
NEW22 = "İKİNCİ DƏRƏCƏLİ PSİXİ VƏ DAVRANIŞ SİNDROMLARI"

for fpath in files:
    fname = os.path.basename(fpath)
    with open(fpath, encoding="utf-8") as f:
        html = f.read()

    original = html

    # Sidebar nav — заменяем оба названия во всех файлах
    html = html.replace(OLD9,  NEW9)
    html = html.replace(OLD22, NEW22)

    # ── ЗАМЕНА 2: bolme-09 — h2 заголовок главы ──────────────────────────────
    if fname == "bolme-09.html":
        # meta description
        html = html.replace(
            'content="Klinik Psixiatriya — BÖLMƏ 9 — YEMƏ"',
            'content="Klinik Psixiatriya — BÖLMƏ 9 — QİDA QƏBULU"'
        )
        # title
        html = html.replace(
            "<title>BÖLMƏ 9 — YEMƏ | KLİNİK PSİXİATRİYA</title>",
            "<title>BÖLMƏ 9 — QİDA QƏBULU | KLİNİK PSİXİATRİYA</title>"
        )
        # h2 (с id и текстом)
        html = html.replace(
            '<h2 id="yemə-və-yeməkəbenzəri̇-davraniş-pozuntulari" class="">6B80–6B8Z · YEMƏ VƏ YEMƏKƏBENZƏRİ DAVRANIŞ POZUNTULARI</h2>',
            '<h2 id="qi̇da-qəbulu-və-qi̇da-davranişı-pozuntulari" class="">6B80–6B8Z · QİDA QƏBULU VƏ QİDA DAVRANIŞI POZUNTULARI</h2>'
        )

    # ── ЗАМЕНА 3: bolme-ps — h1 номер BÖLMƏ 20 → 22 ─────────────────────────
    if fname == "bolme-ps.html":
        html = html.replace(
            '<h1 id="bölmə-20" class="h-bolme">BÖLMƏ 20</h1>',
            '<h1 id="bölmə-22" class="h-bolme">BÖLMƏ 22</h1>'
        )

    # ── ЗАМЕНА 4: bolme-22 — h1 номер 22→23, h2 название ────────────────────
    if fname == "bolme-22.html":
        # meta description
        html = html.replace(
            'content="Klinik Psixiatriya — BÖLMƏ 22–23 — İKİNCİLİ"',
            'content="Klinik Psixiatriya — BÖLMƏ 23 — İKİNCİ DƏRƏCƏLİ"'
        )
        # title
        html = html.replace(
            "<title>BÖLMƏ 22–23 — İKİNCİLİ | KLİNİK PSİXİATRİYA</title>",
            "<title>BÖLMƏ 23 — İKİNCİ DƏRƏCƏLİ | KLİNİK PSİXİATRİYA</title>"
        )
        # h1
        html = html.replace(
            '<h1 id="bölmə-22" class="h-bolme">BÖLMƏ 22</h1>',
            '<h1 id="bölmə-23" class="h-bolme">BÖLMƏ 23</h1>'
        )
        # h2 уже заменена выше через OLD22/NEW22

    if html != original:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(html)
        changed_total += 1
        print(f"  OK: {fname}")

print(f"\nИзменено файлов: {changed_total} из {len(files)}")
