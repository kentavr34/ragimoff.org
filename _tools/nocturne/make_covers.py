#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Обложки книг RAGIMOFF — плоские, лицом, в стиле сайта.

ПОЧЕМУ ПЕРЕПИСАНО.
Первая версия накладывала текст поверх готового 3D-макета книги. Проблема:
на исходниках нарисован корешок с посторонними надписями (на «Клинической
психиатрии» там стоит «VOGUE»), плюс вид под углом. Для обложки в магазине
это неверно: нужен вид ЛИЦОМ, без чужого текста.

ЧТО ДЕЛАЕТ.
1. Берёт исходник и вырезает из него только художественную часть (мозг, феникс,
   кинцуги) — центральную область, обходя корешок.
2. Строит плоскую обложку 1024x1536: фон со свечением цвета книги, искусство
   в мягком круге, типографика, издательская марка.
3. Всё в стиле сайта: Cormorant Garamond, золото на тёмном.

Запуск: python make_covers.py
Пишет:  books/covers/<id>-cover.jpg
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))          # site/_tools/nocturne
SITE = os.path.dirname(os.path.dirname(HERE))               # site
COVERS = os.path.join(SITE, "books", "covers")

W, H = 1024, 1536
GOLD = (201, 169, 97)
GOLD_D = (168, 140, 78)
MILK = (242, 237, 227)
SOFT = (188, 181, 168)
DIM = (138, 133, 124)

F_SERIF_B = "C:/Windows/Fonts/georgiab.ttf"
F_SERIF = "C:/Windows/Fonts/georgia.ttf"
F_SANS_B = "C:/Windows/Fonts/segoeuib.ttf"
F_SANS = "C:/Windows/Fonts/segoeui.ttf"

# Какую область исходника брать под искусство, чтобы не поймать корешок.
ART = {
    "klinik.jpg":   (0.30, 0.10, 0.99, 0.86),
    "pandemic.jpg": (0.24, 0.06, 0.99, 0.90),
    "phoenix.jpg":  (0.18, 0.04, 0.97, 0.94),
    "guilt.jpg":    (0.20, 0.04, 0.99, 0.92),
}

BOOKS = [
    dict(src="klinik.jpg", out="klinik-cover.jpg", accent=(58, 96, 132),
         kicker="DƏRSLİK",
         title=["KLİNİK", "PSİXİATRİYA"],
         sub="DSM-5 · ICD-11 · beynəlxalq protokollar",
         meta="820 səhifə · B5 çap · 4 dil: AZ · RU · EN · TR"),
    dict(src="phoenix.jpg", out="phoenix-cover.jpg", accent=(122, 74, 32),
         kicker="AİLƏ TERAPİYASI",
         title=["FENİKS", "ERASI"],
         sub="Cütlük və ailə münasibətləri üzərində iş",
         meta="3 dil · çap versiyası mövcuddur"),
    dict(src="guilt.jpg", out="guilt-cover.jpg", accent=(120, 46, 38),
         kicker="KBT YANAŞMASI",
         title=["GÜNAHKARLIQ", "VİRUSU"],
         sub="Yanlış təsəvvürlərlə terapevtik iş",
         meta="3 dil · depressiya və narahatlıq"),
    dict(src="pandemic.jpg", out="pandemic-cover.jpg", accent=(96, 84, 58),
         kicker="MAARİFLƏNDİRMƏ",
         title=["ŞİZOFREMİYA", "Cinnət pandemiyası"],
         sub="Xəstəliyi damğadan ayırmaq",
         meta="3 dil · klinik psixiatriya"),
]


def font(path, size):
    for p in (path, F_SERIF_B, F_SERIF, F_SANS_B, F_SANS):
        try:
            if p and os.path.exists(p):
                return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


def art_panel(src_path, box):
    """Вырезает художественную часть, приводит к квадрату, мягкий круглый край."""
    im = Image.open(src_path).convert("RGB")
    w, h = im.size
    x0, y0, x1, y1 = box
    im = im.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1)))
    side = min(im.size)
    im = im.crop(((im.width - side) // 2, (im.height - side) // 2,
                  (im.width - side) // 2 + side, (im.height - side) // 2 + side))
    im = im.resize((760, 760), Image.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = ImageEnhance.Color(im).enhance(1.05)
    mask = Image.new("L", (760, 760), 0)
    ImageDraw.Draw(mask).ellipse((4, 4, 756, 756), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(28))
    return im, mask


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def make(b):
    src = os.path.join(COVERS, b["src"])
    if not os.path.exists(src):
        print(f"  нет файла: {src}")
        return

    # фон с мягким свечением цвета книги
    canvas = Image.new("RGB", (W, H), (7, 9, 14))
    glow = Image.new("RGB", (W, H), (7, 9, 14))
    gd = ImageDraw.Draw(glow)
    ax, ay, az = b["accent"]
    for i in range(26, 0, -1):
        t = i / 26
        r = int(430 * t)
        col = (int(ax * (1 - t) * .55), int(ay * (1 - t) * .55), int(az * (1 - t) * .55))
        gd.ellipse((W // 2 - r, int(H * 0.44) - r, W // 2 + r, int(H * 0.44) + r), fill=col)
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    canvas = Image.blend(canvas, glow, 0.55)

    art, mask = art_panel(src, ART.get(b["src"], (0.2, 0.05, 0.99, 0.95)))
    canvas.paste(art, ((W - 760) // 2, 258), mask)

    d = ImageDraw.Draw(canvas)

    # рамка
    d.rectangle((56, 56, W - 57, H - 57), outline=(52, 48, 42), width=2)
    d.rectangle((66, 66, W - 67, H - 67), outline=(30, 28, 25), width=1)

    # рубрика
    f_kick = font(F_SANS_B, 25)
    kw = d.textlength(b["kicker"], font=f_kick)
    d.text(((W - kw) / 2, 104), b["kicker"], font=f_kick, fill=GOLD)
    d.line([((W - 90) / 2, 148), ((W + 90) / 2, 148)], fill=GOLD_D, width=2)

    # автор
    f_auth = font(F_SERIF, 44)
    aw = d.textlength("KƏNAN RƏHİMOV", font=f_auth)
    d.text(((W - aw) / 2, 176), "KƏNAN RƏHİMOV", font=f_auth, fill=MILK)

    # название
    y = 1048
    for i, line in enumerate(b["title"]):
        size = 96 if i == 0 else 64
        f = font(F_SERIF_B, size)
        while d.textlength(line, font=f) > W - 150 and size > 40:
            size -= 3
            f = font(F_SERIF_B, size)
        lw = d.textlength(line, font=f)
        d.text(((W - lw) / 2, y), line, font=f, fill=MILK)
        y += int(size * 1.02)

    y += 22
    d.line([((W - 150) / 2, y), ((W + 150) / 2, y)], fill=GOLD, width=2)
    y += 26

    f_sub = font(F_SANS, 30)
    for line in wrap(d, b["sub"], f_sub, W - 220):
        lw = d.textlength(line, font=f_sub)
        d.text(((W - lw) / 2, y), line, font=f_sub, fill=SOFT)
        y += 40

    # марка
    f_brand = font(F_SANS_B, 36)
    bw = d.textlength("RAGIMOFF", font=f_brand)
    d.text(((W - bw) / 2 - 5, H - 156), "RAGIMOFF", font=f_brand, fill=MILK)
    d.text(((W + bw) / 2 + 2, H - 156), ".", font=f_brand, fill=GOLD)

    f_meta = font(F_SANS, 24)
    mw = d.textlength(b["meta"], font=f_meta)
    d.text(((W - mw) / 2, H - 104), b["meta"], font=f_meta, fill=DIM)

    out = os.path.join(COVERS, b["out"])
    canvas.save(out, "JPEG", quality=93, optimize=True, progressive=True)
    print(f"  {b['out']:24s} {os.path.getsize(out):>8,} байт")


if __name__ == "__main__":
    print("источник:", COVERS)
    for b in BOOKS:
        make(b)
    print("готово")
