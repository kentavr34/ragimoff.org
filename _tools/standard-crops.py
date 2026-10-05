#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""standard-crops.py — вырезки «до/после» для двух дефектов владельца
(aile-terapiyasi: абзац цены → кнопка; карточки → блок KOMANDA).

Координаты берутся из JSON обхода (standard-audit.js): для каждого состояния
— свои, потому что высота страницы меняется.

    python _tools/standard-crops.py --before-json J --after-json J \
        --before-png P --after-png P --page aile-terapiyasi.html --out DIR
"""
import argparse, json, os, sys
from PIL import Image, ImageDraw, ImageFont


def load_blocks(path, page):
    data = json.load(open(path, encoding='utf-8'))
    for p in data:
        if p.get('file') == page and not p.get('error'):
            return p
    return None


def rects(p, w):
    """Прямоугольники обеих проблем (y0, y1) по состоянию страницы."""
    blocks = p['blocks']
    out = {}
    # 1) карточки → следующий блок: низ контента блока N .. первый контент N+1
    for i in range(len(blocks) - 1):
        a, b = blocks[i], blocks[i + 1]
        if a['badgeText'] and b['badgeText'] and (b['top'] + b['gapTop']) - (a['bot'] - a['gapBot']) > 100:
            y0 = int(a['bot'] - a['gapBot'] - 90)
            y1 = int(b['top'] + b['gapTop'] + 150)
            out['blockgap'] = (max(0, y0), min(int(b['bot']), y1))
            out['blockgap_badge'] = b['badgeText']
            break
    # 2) абзац → кнопка: ищем BTN-GAP-подобную пару: последняя кнопка блока TƏLİM
    btns = p.get('btns') or []
    cand = [b for b in btns if b['gap'] < 34]
    if cand:
        # координаты кнопки в обходе не пишутся — берём секцию ТƏLİM/TRAINING/ПРОГРАММА
        # (там стоит абзац цены и кнопка «о тренере»): конец её контента
        for blk in blocks:
            badge = (blk.get('badgeText') or '')
            if badge and badge.upper() in ('TƏLİM', 'ОБУЧЕНИЕ', 'TRAINING'):
                y1 = int(blk['bot'] - blk['gapBot'] + 30)
                y0 = y1 - 330
                out['btngap'] = (max(0, y0), y1)
                break
    return out


def crop(im, box):
    y0, y1 = box
    return im.crop((0, y0, im.width, min(y1, im.height)))


def label(im, text):
    im = im.convert('RGB')
    d = ImageDraw.Draw(im, 'RGBA')
    try:
        f = ImageFont.truetype('arial.ttf', 22)
    except Exception:
        f = ImageFont.load_default()
    d.rectangle([0, 0, 260, 34], fill=(0, 0, 0, 190))
    d.text((10, 6), text, fill=(255, 255, 255), font=f)
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--before-json'); ap.add_argument('--after-json')
    ap.add_argument('--before-png'); ap.add_argument('--after-png')
    ap.add_argument('--page', default='aile-terapiyasi.html')
    ap.add_argument('--out', default='.')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    bj = load_blocks(a.before_json, a.page); aj = load_blocks(a.after_json, a.page)
    if not bj or not aj:
        print('нет данных по', a.page); return 1
    rb = rects(bj, bj.get('w')); ra = rects(aj, aj.get('w'))
    if 'blockgap' not in ra and 'blockgap' in rb:
        badge = rb.get('blockgap_badge')
        for blk in aj['blocks']:
            if badge and blk.get('badgeText') == badge:
                y = int(blk['top'] + blk['gapTop'])
                ra['blockgap'] = (max(0, y - 210), y + 130)
                break
    bim = Image.open(a.before_png); aim = Image.open(a.after_png)
    made = []
    for key, name in (('blockgap', 'карточки-блок'), ('btngap', 'абзац-кнопка')):
        if key not in rb or key not in ra:
            print('нет прямоугольника', key, key in rb, key in ra); continue
        cb = label(crop(bim, rb[key]), 'ДО')
        ca = label(crop(aim, ra[key]), 'ПОСЛЕ')
        h = max(cb.height, ca.height)
        canvas = Image.new('RGB', (cb.width + ca.width + 24, h), (7, 9, 14))
        canvas.paste(cb, (0, 0)); canvas.paste(ca, (cb.width + 24, 0))
        p = os.path.join(a.out, 'crop-' + key + '-' + a.page.replace('/', '_').replace('.html', '') + '.png')
        canvas.save(p)
        made.append(p)
    print('\n'.join(made))
    return 0


if __name__ == '__main__':
    sys.exit(main())
