"""test/11 — иллюстрации через DashScope wan2.7-image (бесплатная квота воркспейса irada).
Запуск НА СЕРВЕРЕ 164.68.114.15 (ключ лежит там, не печатается):  python3 gen_art.py  ->  /tmp/r11_art/<имя>.png
Текста на картинках нет: надписи обложек набираются на сайте шрифтом (буква Ə не превращается в квадрат)."""
import json, os, sys, requests

d = json.load(open('/opt/prod/tools/tr_keys.json'))
KEY = d['irada']['key_prefix'] + '.' + d['irada']['key_tail']
BASE = 'https://dashscope-intl.aliyuncs.com/api/v1'
MODEL = os.environ.get('MODEL', 'wan2.7-image')
OUT = '/tmp/r11_art'
os.makedirs(OUT, exist_ok=True)
NEG = 'text, letters, typography, numbers, watermark, logo, signature, frame, border, people, faces, hands, blurry, deformed, cartoon, low quality'
STYLE = (' Premium book cover artwork, vertical composition, deep ink-blue almost black background, old gold and warm ivory light, '
         'fine detail, cinematic soft glow, elegant and expensive, generous empty dark space in the upper third and the lower quarter '
         'for a title, no text, no letters, no words, no numbers, no watermark, no frame.')
ART = {
    'klinik-a': 'A human brain seen in profile, sculpted from thousands of fine luminous golden threads like a map of neural pathways, floating in darkness, a few threads drifting upward like sparks.',
    'klinik-b': 'An antique anatomical engraving of the human brain reinterpreted in gold leaf on dark blue lacquer, delicate gilded lines, a thin golden meridian circle around it like an astrolabe.',
    'klinik-c': 'A translucent crystal human brain lit from within by warm golden light, standing on an invisible surface, soft reflections, dark blue studio background, museum object photography.',
    'phoenix':  'A phoenix bird rising with wide spread wings, drawn from thousands of fine luminous golden threads, a few threads drifting upward like sparks.',
    'guilt':    'A single spherical virus particle with a crown of spikes, drawn from thousands of fine luminous golden threads, cracked open on one side with warm light spilling out.',
    'pandemic': 'A circular labyrinth maze, drawn from thousands of fine luminous golden threads, one brighter thread finding its way out to the edge and drifting upward.',
    'freud':    'A classic psychoanalytic couch with a patterned oriental rug and a round pillow, an empty armchair behind it, all drawn from thousands of fine luminous golden threads.',
}


def generate(prompt, size):
    r = requests.post(BASE + '/services/aigc/multimodal-generation/generation',
                      headers={'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json'},
                      json={'model': MODEL, 'input': {'messages': [{'role': 'user', 'content': [{'text': prompt + STYLE}]}]},
                            'parameters': {'negative_prompt': NEG, 'size': size, 'n': 1, 'prompt_extend': False, 'watermark': False}}, timeout=300)
    j = r.json()
    if r.status_code != 200:
        raise RuntimeError(str(j.get('code')) + ': ' + str(j.get('message'))[:200])
    for c in j['output']['choices'][0]['message']['content']:
        if c.get('image'):
            return c['image']
    raise RuntimeError('no image')


for name in (sys.argv[1:] or list(ART)):
    fn = '%s/%s.png' % (OUT, name)
    if os.path.exists(fn):
        print('есть', name); continue
    err = None
    for size in ('928*1664', '1024*1536', '1024*1024'):
        try:
            url = generate(ART[name], size)
            open(fn, 'wb').write(requests.get(url, timeout=300).content)
            print('готово', name, size); err = None; break
        except Exception as e:
            err = str(e)
            if 'Arrearage' in err or 'FreeTierOnly' in err or 'Unpurchased' in err:   # квота кончилась — стоп, платного не трогаем
                print('СТОП квота:', err); sys.exit(2)
    if err:
        print('ошибка', name, err)
