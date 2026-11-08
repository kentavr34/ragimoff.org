"""Видео первого экрана → кадры для покадровой прокрутки.
  python cut_frames.py <hero.mp4> [N=96]  → D:/Projects/Ragimoff/_assets/nocturne_video/frames/f000.jpg …
После этого build.py сам положит кадры в images/hero-home/ и включит их на главной (data-frames)."""
import subprocess, sys, pathlib, shutil
src = pathlib.Path(sys.argv[1]).resolve()
n = int(sys.argv[2]) if len(sys.argv) > 2 else 96
out = pathlib.Path(__file__).resolve().parents[3] / '_assets' / 'nocturne_video' / 'frames'
if out.exists():
    shutil.move(str(out), str(out.with_name('frames_old')))   # не удаляем: прежние кадры — в frames_old
out.mkdir(parents=True)
dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(src)]).decode().strip())
subprocess.check_call(['ffmpeg', '-v', 'error', '-i', str(src), '-vf', 'fps=%.4f,scale=1920:-2' % (n / dur), '-q:v', '3', str(out / 'f%03d.jpg'), '-start_number', '0'])
print(len(list(out.glob('*.jpg'))), 'frames →', out)
