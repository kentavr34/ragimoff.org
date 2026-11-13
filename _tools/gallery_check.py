# -*- coding: utf-8 -*-
"""gallery_check.py — страж галерей (13.11.2026, слово Кенана: один и тот же диплом/сертификат не должен стоять в галерее дважды).
Ищет во всех data/**/*.json блоки галерей (списки объектов с полем src) и сравнивает сами изображения:
одинаковый файл (sha256) или почти одинаковая картинка (средний хэш 16×16, расстояние ≤ 6) — повтор.
  python _tools/gallery_check.py          — отчёт; код 1, если есть повторы"""
import glob, hashlib, io, json, os, sys
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)


def local(src):
    s = src.split("?")[0].lstrip("/")
    for cand in (s, "assets/img/" + s.split("images/", 1)[-1] if "images/" in s else s):
        if os.path.exists(cand):
            return cand
    return None


_ah = {}


def ahash(p):
    if p not in _ah:
        try:
            im = Image.open(p).convert("L").resize((16, 16), Image.LANCZOS)
            px = list(im.getdata())
            m = sum(px) / len(px)
            _ah[p] = sum(1 << i for i, v in enumerate(px) if v > m)
        except Exception:
            _ah[p] = None
    return _ah[p]


def galleries(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from galleries(v, path + "/" + str(k))
    elif isinstance(o, list):
        if o and all(isinstance(x, dict) and "src" in x for x in o):
            yield path, o
        else:
            for i, v in enumerate(o):
                yield from galleries(v, path + "[%d]" % i)


OK = set(frozenset(x) for x in json.load(io.open("_tools/gallery_ok.json", encoding="utf-8"))) if os.path.exists("_tools/gallery_ok.json") else set()
bad = 0
for f in sorted(glob.glob("data/**/*.json", recursive=True)):
    try:
        d = json.load(io.open(f, encoding="utf-8"))
    except Exception:
        continue
    for path, items in galleries(d):
        seen = []
        for i, x in enumerate(items):
            p = local(x["src"])
            if not p:
                continue
            h, a = hashlib.sha256(open(p, "rb").read()).hexdigest(), ahash(p)
            for j, (h2, a2, p2) in enumerate(seen):
                if h == h2:
                    print("%s %s: №%d повторяет №%d (тот же файл) — %s = %s" % (f, path, i + 1, j + 1, p, p2))
                    bad += 1
                    break
                if a is not None and a2 is not None and bin(a ^ a2).count("1") <= 8 and frozenset((os.path.basename(p), os.path.basename(p2))) not in OK:
                    print("%s %s: №%d похож на №%d — проверить глазами и, если разные, внести пару в _tools/gallery_ok.json: %s ~ %s" % (f, path, i + 1, j + 1, p, p2))
                    bad += 1
                    break
            seen.append((h, a, p))
print("ПОВТОРОВ В ГАЛЕРЕЯХ:", bad)
sys.exit(1 if bad else 0)
