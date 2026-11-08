"""Ноктюрн · видео для первого экрана главной (scroll-scrub, как на JobTop).

Запуск на 164:  python3 gen_video.py            → /tmp/nocturne_video/still.png, hero.mp4
Шаг 1: кадр wan2.7-image (бесплатная квота, проверено 08.11.2026).
Шаг 2: image-to-video — перебор моделей wan*-i2v; только бесплатная квота:
        Arrearage / FreeTierOnly / Quota → эта модель пропускается, на платное не переходим.
Ключ: /opt/prod/tools/tr_keys.json → irada (значение не печатается).
"""
import json, os, sys, time, urllib.request, urllib.error

BASE = 'https://dashscope-intl.aliyuncs.com/api/v1'
OUT = '/tmp/nocturne_video'
os.makedirs(OUT, exist_ok=True)
_K = json.load(open('/opt/prod/tools/tr_keys.json'))
e = _K[os.environ.get('KEYNAME', 'irada')]
KEY = e if isinstance(e, str) else ((e['key_prefix'] + '.' + e['key_tail']) if 'key_tail' in e else e.get('key', ''))
BASE = os.environ.get('BASE', BASE)

STILL = ('Cinematic photograph, wide 16:9. A quiet private study of a psychotherapist at night. '
         'On a dark walnut desk lies a large old open book with cream pages, a brass desk lamp casts a warm '
         'golden pool of light on the pages, a fountain pen beside it. Behind, tall dark bookshelves full of '
         'leather-bound volumes fade into deep blue-black shadow; a tall window on the right shows a faint '
         'night city with soft bokeh lights. Composition: the book and lamp in the right half of the frame, '
         'the left half dark and calm for text. Palette: ink-black, midnight navy, warm gold. '
         'Shallow depth of field, 35mm film grain, Roger Deakins lighting, ultra detailed, elegant, serene.')
NEG = 'people, person, hands, face, text, letters, watermark, logo, cartoon, illustration, oversaturated, blurry'
MOTION = ('Very slow smooth cinematic dolly-in toward the open book on the desk. The pages of the book gently '
          'turn by themselves one after another, the warm lamp light softly breathes, tiny dust particles float '
          'in the golden light, city lights twinkle in the window. Stable camera, no people, elegant and calm.')
I2V = os.environ.get('I2V', 'wan2.6-i2v,wan2.5-i2v-preview,wan2.2-i2v-plus,wan2.2-i2v-flash,wan2.1-i2v-plus,wan2.1-i2v-turbo').split(',')
STOP = ('Arrearage', 'FreeTierOnly', 'Quota', 'quota', 'Unpurchased', 'AccessDenied', 'Model.NotFound', 'ModelNotFound', 'InvalidParameter', 'not supported', 'does not exist')


def call(url, body=None, headers=None, method=None):
    h = {'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json'}
    h.update(_K.get(os.environ.get('KEYNAME', 'irada') + '_headers') or {})
    h.update(headers or {})
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None, headers=h, method=method)
    try:
        return json.load(urllib.request.urlopen(req, timeout=120))
    except urllib.error.HTTPError as ex:
        return {'_err': ex.code, **json.loads(ex.read().decode() or '{}')}


def still():
    p = os.path.join(OUT, 'still.png')
    url_f = os.path.join(OUT, 'still.url')
    if os.path.exists(url_f) and os.path.exists(p):
        return open(url_f).read().strip()
    r = call(BASE + '/services/aigc/multimodal-generation/generation', {
        'model': 'wan2.7-image',
        'input': {'messages': [{'role': 'user', 'content': [{'text': STILL}]}]},
        'parameters': {'negative_prompt': NEG, 'size': '1664*928', 'n': 1, 'prompt_extend': False, 'watermark': False}})
    try:
        u = [c['image'] for c in r['output']['choices'][0]['message']['content'] if 'image' in c][0]
    except Exception:
        print('STILL FAIL', r.get('code'), r.get('message'))
        sys.exit(1)
    urllib.request.urlretrieve(u, p)
    open(url_f, 'w').write(u)
    print('still ok')
    return u


def video(img_url):
    for m in I2V:
        body = {'model': m, 'input': {'prompt': MOTION, 'negative_prompt': NEG, 'img_url': img_url},
                'parameters': {'resolution': '1080P', 'duration': 5, 'prompt_extend': False, 'watermark': False}}
        r = call(BASE + '/services/aigc/video-generation/video-synthesis', body, {'X-DashScope-Async': 'enable'})
        tid = (r.get('output') or {}).get('task_id')
        if not tid:
            print(m, 'skip:', r.get('code'), str(r.get('message'))[:120])
            continue
        print(m, 'task started')
        for _ in range(120):
            time.sleep(10)
            s = call(BASE + '/tasks/' + tid, method='GET')
            st = (s.get('output') or {}).get('task_status')
            if st == 'SUCCEEDED':
                urllib.request.urlretrieve(s['output']['video_url'], os.path.join(OUT, 'hero.mp4'))
                open(os.path.join(OUT, 'model.txt'), 'w').write(m)
                print(m, 'video ok')
                return True
            if st in ('FAILED', 'CANCELED', 'UNKNOWN'):
                print(m, 'failed:', (s.get('output') or {}).get('code'), str((s.get('output') or {}).get('message'))[:120])
                break
    return False


if __name__ == '__main__':
    u = still()
    if os.environ.get('ONLY_STILL'):
        sys.exit(0)
    sys.exit(0 if video(u) else 2)
