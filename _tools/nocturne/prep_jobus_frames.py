"""Кадры видео JobTop (D:/Projects/Jobus/platform/public/hero-a.mp4, 240 кадров) → первый экран главной Ноктюрна.
Обрезка значка генератора (правый нижний угол), увеличение, резкость, контраст/цвет.
d/: 1600×900 (десктоп), m/: 1000×1000 квадрат вокруг героини (телефон). Берётся каждый 1.5-й кадр → 160 кадров.
Источник кадров: _assets/nocturne_video/jobus_src/s%03d.jpg (ffmpeg -q:v 2)."""
import pathlib
from PIL import Image, ImageEnhance, ImageFilter
A = pathlib.Path(__file__).resolve().parents[3] / '_assets' / 'nocturne_video'
SRC, OUT = A / 'jobus_src', A / 'jobus_frames'
N = 160
for sub in ('d', 'm'):
    (OUT / sub).mkdir(parents=True, exist_ok=True)
for k in range(N):
    i = 1 + round(k * 239 / (N - 1))
    im = Image.open(SRC / ('s%03d.jpg' % i)).convert('RGB').crop((0, 0, 1160, 652))
    im = ImageEnhance.Contrast(im).enhance(1.07)
    im = ImageEnhance.Color(im).enhance(1.08)
    im = ImageEnhance.Brightness(im).enhance(1.04)
    d = im.resize((1600, 900), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.4, percent=60, threshold=2))
    d.save(OUT / 'd' / ('f%03d.webp' % k), 'WEBP', quality=72, method=5)
    m = im.crop((345, 0, 997, 652)).resize((1000, 1000), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.4, percent=60, threshold=2))
    m.save(OUT / 'm' / ('f%03d.webp' % k), 'WEBP', quality=68, method=5)
print('ok', N)
