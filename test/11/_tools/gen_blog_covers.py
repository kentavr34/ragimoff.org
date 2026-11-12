"""test/11 — обложки статей блога и картины героя новых страниц через DashScope wan2.7-image
(бесплатная квота воркспейса irada; при исчерпании квоты — стоп, платное не трогаем).
Запуск НА СЕРВЕРЕ 164.68.114.15 (ключ лежит там, не печатается):  python3 gen_blog_covers.py [имя ...]  ->  /tmp/r11_blog/<имя>.png
Единый стиль сайта: предмет, сотканный из золотых нитей света на тёмно-синем фоне; людей, лиц и надписей нет."""
import json, os, sys, requests

d = json.load(open('/opt/prod/tools/tr_keys.json'))
KEY = d['irada']['key_prefix'] + '.' + d['irada']['key_tail']
BASE = 'https://dashscope-intl.aliyuncs.com/api/v1'
MODEL = os.environ.get('MODEL', 'wan2.7-image')
OUT = '/tmp/r11_blog'
os.makedirs(OUT, exist_ok=True)
NEG = 'text, letters, typography, numbers, watermark, logo, signature, frame, border, people, faces, portrait, blurry, deformed, cartoon, low quality, photo of a person'
STYLE = (' The subject is drawn from thousands of fine luminous golden threads of light, a few threads drifting upward like sparks. '
         'Wide horizontal editorial illustration, deep ink-blue almost black background, old gold and warm ivory light, fine detail, '
         'cinematic soft glow, calm, elegant and expensive, the subject placed slightly right of centre with generous dark empty space around it, '
         'no text, no letters, no words, no numbers, no watermark, no frame, no people.')
ART = {
    'depressiya-protokol': 'A bare winter tree on the left side gradually turning into the same tree in full leaf on the right side, one continuous branch joining them.',
    'enurez-protokol': 'A child bed with a soft pillow and a folded blanket, a crescent moon and three small stars above it, a tiny bedside alarm device with a thin cable resting on the blanket.',
    'enurez-3': 'A small bedwetting alarm: a flat moisture sensor connected by a thin cable to a little round sounder with tiny sound waves, lying beside folded child pyjamas, a crescent moon above.',
    'enurez-4': 'A bedside table with a glass of water, a small medicine bottle and three tablets next to it, a crescent moon in the dark window behind.',
    'enurez-5': 'A night-light lamp glowing beside a child bed, a teddy bear sitting on the pillow, a calendar page with small stars marked on it hanging on the wall.',
    'panik-2': 'A human brain seen in profile with a small almond-shaped amygdala glowing much brighter deep inside it, fine pulses of light running from it along neural pathways.',
    'panik-4': 'A staircase of seven wide steps rising out of darkness toward an open doorway filled with warm light.',
    'psixolog-olmaq-2': 'A path that forks into two roads at a wooden signpost with two blank arrow boards pointing in different directions, both roads leading toward a distant horizon.',
    'psixolog-olmaq-4': 'A large old lantern lighting a smaller lantern beside it, the flame passing between them, an open notebook lying in front.',
    'sosial-fobiya-3': 'An empty oval standing mirror in a quiet room reflecting a soft warm glow, a single chair in front of it.',
    'tesvis-pozuntulari': 'A tangled knot of threads on the left slowly unravelling into one calm straight line that runs to the right edge.',
    'okp': 'A door lock with a key in it surrounded by perfectly concentric repeating circles like ripples, a row of identical keys aligned with exact spacing below.',
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
    for size in ('1664*928', '1536*1024'):
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
