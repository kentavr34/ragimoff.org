# -*- coding: utf-8 -*-
"""Новые обложки статей и картины героя (владелец 12.11.2026, п. 11): картинки из gen_blog_covers.py
переводятся в webp и подставляются в данные. Старые файлы обложек не удаляются.
Запуск: python apply_covers.py <папка с png>   (повторный запуск ничего не меняет)."""
import io, os, sys, json, glob
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
SRC = sys.argv[1]
HERO = ("tesvis-pozuntulari", "okp")
for png in sorted(glob.glob(os.path.join(SRC, "*.png"))):
    slug = os.path.basename(png)[:-4]
    im = Image.open(png).convert("RGB")
    im.thumbnail((1440, 1440))
    if slug in HERO:
        rel = "consult/%s.webp" % slug
        os.makedirs("assets/img/consult", exist_ok=True)
        im.save("assets/img/" + rel, "WEBP", quality=84)
        for fn in glob.glob("data/cons/%s.*.json" % slug):
            d = json.load(io.open(fn, encoding="utf-8"))
            if d.get("img") != "/images/" + rel:
                d["img"] = "/images/" + rel
                json.dump(d, io.open(fn, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
                print("герой:", fn)
        continue
    old = None
    for l in ("ru", "az", "en"):
        fn = "data/blog/index.%s.json" % l
        d = json.load(io.open(fn, encoding="utf-8"))
        ch = False
        for it in d["items"] + ([d["featured"]] if isinstance(d.get("featured"), dict) else []):
            if it.get("slug") == slug:
                old = old or it.get("cover")
                rel = os.path.dirname(old)[len("/images/"):] + "/%s-art.webp" % slug
                if it.get("cover") != "/images/" + rel:
                    it["cover"] = "/images/" + rel
                    ch = True
        if ch:
            json.dump(d, io.open(fn, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
            print("список:", fn, slug)
    if not old:
        print("НЕТ в списке блога:", slug)
        continue
    rel = os.path.dirname(old)[len("/images/"):] + "/%s-art.webp" % slug
    im.save("assets/img/" + rel, "WEBP", quality=84)
    for fn in glob.glob("data/blog/%s.*.json" % slug):
        d = json.load(io.open(fn, encoding="utf-8"))
        if d.get("img") != "/images/" + rel:
            d["img"] = "/images/" + rel
            json.dump(d, io.open(fn, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
            print("статья:", fn)
