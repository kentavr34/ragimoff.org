"""test/11 — сборка обложек: рисунок (_agent/art/<книга>.png) → кадр 2:3 → надписи шрифтом (cover.html) → assets/img/book-<книга>-<язык>.jpg
Запуск: python make_covers.py   (нужен локальный сервер из корня site на порту PORT и Chrome; снимает shot.py)."""
import os, subprocess, sys, pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
ART = ROOT / '_agent' / 'art'
OUT = ROOT / 'assets' / 'img'
PORT = os.environ.get('PORT', '8812')
SHOT = os.environ.get('SHOT', str(pathlib.Path(os.environ.get('TEMP', '.')) / 'shot.py'))
SRC = {'klinik': ('klinik-a.png', .42, 1.0), 'phoenix': ('phoenix.png', 0, .70), 'guilt': ('guilt.png', .42, 1.0),
       'pandemic': ('pandemic.png', .30, 1.0), 'freud': ('freud.png', .40, 1.0), 'therapy': ('therapy.png', .55, 1.0)}     # файл, доля сдвига сверху, используемая доля высоты

for book, (fn, off, keep) in SRC.items():
    im = Image.open(ART / fn).convert('RGB')
    w, h = im.size
    if keep < 1:                                   # у рисунка внизу мусорная «надпись» модели — берём только верх и доливаем фоном
        top = im.crop((0, 0, w, round(h * keep))).resize((800, round(h * keep * 800 / w)), Image.LANCZOS)
        bg = Image.new('RGB', (800, 1200), top.getpixel((10, top.height - 4)))
        bg.paste(top, (0, 0)); im2 = bg
    else:
        ch = round(w * 1.5); y = round((h - ch) * off)
        im2 = im.crop((0, y, w, y + ch)).resize((800, 1200), Image.LANCZOS)
    im2.save(ART / ('art-%s.jpg' % book), quality=90)

tmp = pathlib.Path(os.environ.get('TEMP', '.'))
for book in SRC:
    for lang in ('az', 'ru', 'en'):
        env = dict(os.environ, NOMOB='1', WAIT='7')          # ждём загрузки расширенных наборов шрифта (Ə, İ, Ş, Ğ)
        pref = str(tmp / ('cov_%s_%s' % (book, lang)))
        subprocess.run([sys.executable, SHOT, 'http://127.0.0.1:%s/test/11/_agent/art/cover.html?b=%s&l=%s' % (PORT, book, lang), '800', '1200', pref, '0'],
                       env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        Image.open(pref + '_0.jpg').resize((640, 960), Image.LANCZOS).save(OUT / ('book-%s-%s.jpg' % (book, lang)), quality=88)
        print('готово', book, lang)
