#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""add_own_abbr.py — справочник должен расшифровывать сокращения СВОЕГО дерева.
Кенан 2026-08-12.

Аудит показал: таблица сокращений во всех деревьях латинская и почти целиком
общая. Русский читатель ищет «СДВГ» (560 раз в тексте) — строки нет; английский
ищет «PTSD» (511) — нет; турецкий «TSSB» (495) — нет. При этом азербайджанские
ASP, DDHP, KPTSP есть у всех троих.

Скрипт добавляет недостающие строки в `abbreviatur.html` (две колонки) и
`terminoloji-luget.html` (три колонки) каждого перевода. Список — только те
сокращения, которые дерево реально пишет в тексте не меньше 20 раз.

Идемпотентен: если строка уже есть, не добавляет.

    python add_own_abbr.py            # показать
    python add_own_abbr.py --apply
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent / 'klinik-psixiatriya'

# сокращение → (расшифровка на языке дерева, английское соответствие)
ROWS = {
    'ru': [
        ('ОКР', 'Обсессивно-компульсивное расстройство', 'Obsessive-Compulsive Disorder (OCD)'),
        ('СДВГ', 'Синдром дефицита внимания и гиперактивности',
         'Attention-Deficit/Hyperactivity Disorder (ADHD)'),
        ('ПТСР', 'Посттравматическое стрессовое расстройство',
         'Post-Traumatic Stress Disorder (PTSD)'),
        ('ГТР', 'Генерализованное тревожное расстройство', 'Generalised Anxiety Disorder (GAD)'),
        ('ДРИ', 'Диссоциативное расстройство идентичности',
         'Dissociative Identity Disorder (DID)'),
        ('К-ПТСР', 'Комплексное посттравматическое стрессовое расстройство',
         'Complex Post-Traumatic Stress Disorder (cPTSD)'),
        ('КПТ', 'Когнитивно-поведенческая терапия', 'Cognitive Behavioural Therapy (CBT)'),
        ('БДР', 'Большое депрессивное расстройство', 'Major Depressive Disorder (MDD)'),
        ('ПРЛ', 'Пограничное расстройство личности', 'Borderline Personality Disorder (BPD)'),
        ('ЭСТ', 'Электросудорожная терапия', 'Electroconvulsive Therapy (ECT)'),
        ('РАС', 'Расстройство аутистического спектра', 'Autism Spectrum Disorder (ASD)'),
    ],
    'en': [
        ('OCD', 'Obsessive-compulsive disorder', 'Obsessive-Compulsive Disorder (OCD)'),
        ('PTSD', 'Post-traumatic stress disorder', 'Post-Traumatic Stress Disorder (PTSD)'),
        ('ASD', 'Autism spectrum disorder', 'Autism Spectrum Disorder (ASD)'),
        ('DID', 'Dissociative identity disorder', 'Dissociative Identity Disorder (DID)'),
        ('BED', 'Binge eating disorder', 'Binge Eating Disorder (BED)'),
        ('PMDD', 'Premenstrual dysphoric disorder', 'Premenstrual Dysphoric Disorder (PMDD)'),
        ('cPTSD', 'Complex post-traumatic stress disorder',
         'Complex Post-Traumatic Stress Disorder (cPTSD)'),
        ('CBT', 'Cognitive behavioural therapy', 'Cognitive Behavioural Therapy (CBT)'),
        ('MDD', 'Major depressive disorder', 'Major Depressive Disorder (MDD)'),
        ('SSRI', 'Selective serotonin reuptake inhibitor',
         'Selective Serotonin Reuptake Inhibitor (SSRI)'),
        ('ECT', 'Electroconvulsive therapy', 'Electroconvulsive Therapy (ECT)'),
    ],
    'tr': [
        ('TSSB', 'Travma sonrası stres bozukluğu', 'Post-Traumatic Stress Disorder (PTSD)'),
        ('OSB', 'Otizm spektrum bozukluğu', 'Autism Spectrum Disorder (ASD)'),
        ('YAB', 'Yaygın anksiyete bozukluğu', 'Generalised Anxiety Disorder (GAD)'),
        ('DKB', 'Disosiyatif kimlik bozukluğu', 'Dissociative Identity Disorder (DID)'),
        ('KTSSB', 'Karmaşık travma sonrası stres bozukluğu',
         'Complex Post-Traumatic Stress Disorder (cPTSD)'),
    ],
}

TABLE = re.compile(r'(id="abbreviaturalar"[\s\S]*?<table[^>]*>)([\s\S]*?)(</table>)')


def main(apply: bool = False) -> None:
    total = 0
    for lang, rows in ROWS.items():
        for name in ('abbreviatur.html', 'terminoloji-luget.html'):
            p = ROOT / lang / name
            raw = p.read_bytes()
            crlf = raw.count(b'\r\n') > raw.count(b'\n') // 2
            t = raw.decode('utf-8').replace('\r\n', '\n')
            m = TABLE.search(t)
            if not m:
                print('✗ {}/{}: таблицы сокращений нет'.format(lang, name))
                continue
            body = m.group(2)
            cols = 3 if '</td><td>' in body and body.count('</td>') > body.count('<tr>') * 2 else 2
            added = 0
            new_rows = []
            for abbr, full, eng in rows:
                if re.search(r'<tr><td>' + re.escape(abbr) + r'</td>', body):
                    continue
                if cols == 3:
                    new_rows.append('<tr><td>{}</td><td>{}</td><td lang="en">{}</td></tr>'.format(
                        html.escape(abbr), html.escape(full), html.escape(eng)))
                else:
                    new_rows.append('<tr><td>{}</td><td>{}</td></tr>'.format(
                        html.escape(abbr), html.escape(full)))
                added += 1
            if not added:
                continue
            total += added
            print('{}/{}: +{} строк ({} колонки)'.format(lang, name, added, cols))
            if apply:
                t2 = t[:m.end(2)] + '\n' + '\n'.join(new_rows) + '\n' + t[m.end(2):]
                p.write_bytes((t2.replace('\n', '\r\n') if crlf else t2).encode('utf-8'))
    print('итого строк: {}{}'.format(total, '' if apply else ' — пробный прогон'))


if __name__ == '__main__':
    main('--apply' in sys.argv)
