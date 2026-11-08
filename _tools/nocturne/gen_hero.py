"""Иллюстрации первых экранов «Ноктюрна» через DashScope wan2.7-image (env MODEL), общий адрес dashscope-intl —
тот же способ и ключ, что у обложек книг Фрейда (Freud/tools/site/gen_covers.py).
Запуск НА СЕРВЕРЕ 164.68.114.15 (ключ лежит там, не печатается):
    python3 gen_hero.py            -> /tmp/nocturne_hero/<slug>.png
    python3 gen_hero.py tehsil enurez   (только выбранные)
Готовое уже не перегенерируется. Людей и детей в кадре нет: wan2.5 отклоняет такие темы,
а реальные лица на сайте — только фото специалистов и студентов."""
import json, time, requests, os, sys

d = json.load(open('/opt/prod/tools/tr_keys.json'))
KEY = d['irada']['key_prefix'] + '.' + d['irada']['key_tail']
BASE = os.environ.get('BASE', 'https://dashscope-intl.aliyuncs.com/api/v1')   # воркспейсный адрес irada отвечает 403 Unpurchased
OUT = '/tmp/nocturne_hero'
os.makedirs(OUT, exist_ok=True)

STYLE = ('Museum-quality oil painting, cinematic nocturne, deep ink-blue night palette with warm ivory light '
         'and touches of old gold, soft glow, rich texture, calm and expensive mood, wide composition with '
         'the subject on the right third and quiet dark negative space on the left for a headline, '
         'no people, no faces, no text, no letters, no words, no signature, no watermark, no frame.')
NEG = 'text, letters, typography, watermark, logo, signature, frame, border, people, faces, hands, blurry, deformed'

HERO = {
    # консультации
    'xidmetler':          'A quiet consulting room at night: two deep armchairs facing each other across a low table, a glass of water, a warm brass floor lamp, tall window with the city lights of Baku far below.',
    'aile-terapiyasi':    'Several cups of tea gathered around one round wooden table in a warm home at night, chairs pulled close together, a single pendant lamp lighting them all equally.',
    'aile-terapiyasi-usaq': 'A small wooden house-shaped shelf with toy figures of a family, colored pencils and a child drawing of a sun on the table, soft lamplight in a calm playroom at night.',
    'depressiya':         'A rain-streaked window at night, behind it the first pale gold light of dawn slowly breaking over dark rooftops, a single small plant on the windowsill reaching toward the light.',
    'panik-ataklar':      'A calm dark sea at night under a clearing sky, a slow wave settling on the sand, a lighthouse beam sweeping softly across the water, feeling of breath returning.',
    'sosial-fobiya':      'An empty theatre stage seen from the wings, one soft golden spotlight on the boards, a velvet curtain slightly parted, rows of empty seats fading into the dark.',
    'enurez':             'A child bedroom at night seen from the doorway, a neatly made small bed, a crescent-moon night light glowing, a plush toy bear sitting on the pillow, stars through the window.',
    'valideyn-mektebi':   'Two pairs of shoes, a large pair and a small pair, standing side by side at a doorway, warm hallway light, a coat and a small backpack hanging on hooks.',
    # обучение
    'tehsil':             'A grand old academic library at night, long oak tables with brass reading lamps, open notebooks and a stack of psychology books, gold light on spines of thousands of books.',
    'program-umumi':      'An open notebook with hand-drawn diagrams of the mind, a fountain pen, a vintage brain model of white porcelain on a desk under a warm lamp.',
    'program-klinik':     'A clinician desk at night: a stethoscope, a case file folder, a classic reflex hammer and an anatomical drawing of the brain under a green banker lamp.',
    'program-praktikum':  'A circle of empty wooden chairs in a softly lit studio room at night, one chair turned slightly, tall windows with blue night outside, a sense of a group about to meet.',
    'program-psixoanaliz': 'A psychoanalytic couch covered by a richly patterned oriental rug, a leather armchair behind it, small antique statuettes on a shelf, warm lamp in a dark study.',
    'program-psixodiaqnostika': 'Ten symmetrical ink blot cards spread on a dark desk, a magnifying glass, a pencil and a test booklet, a single warm lamp casting long shadows.',
    'qanunlar':           'A heavy law book open on a desk next to classical scales of justice in old gold, a seal and a fountain pen, deep blue night light from a tall window.',
    # прочее
    'b2b':                'A modern glass office tower at night seen from inside a meeting room, an empty long table with notebooks and water glasses, warm light inside, blue city outside.',
    'blog':               'A writing desk at night by a large window, an open journal, a cup of tea with steam, a stack of letters and a warm lamp, the city lights soft in the distance.',
}


MODEL = os.environ.get('MODEL', 'wan2.7-image')   # qwen-image-3.0-pro на irada: Arrearage (бесплатной квоты нет)
SIZE = os.environ.get('SIZE', '1664*928')


def generate(prompt):
    """qwen-image / wan2.7-image: синхронный multimodal-generation, сразу отдаёт URL картинки."""
    r = requests.post(BASE + '/services/aigc/multimodal-generation/generation',
                      headers={'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json'},
                      json={'model': MODEL,
                            'input': {'messages': [{'role': 'user', 'content': [{'text': prompt + ' ' + STYLE}]}]},
                            'parameters': {'negative_prompt': NEG, 'size': SIZE, 'n': 1, 'prompt_extend': False, 'watermark': False}},
                      timeout=300)
    j = r.json()
    if r.status_code != 200:
        raise RuntimeError(str(j.get('code')) + ': ' + str(j.get('message')))
    for c in j['output']['choices'][0]['message']['content']:
        if c.get('image'):
            return c['image']
    raise RuntimeError('no image in answer')


want = sys.argv[1:] or list(HERO)
ok = 0
for slug in want:
    if os.path.exists(f'{OUT}/{slug}.png'):
        continue
    for attempt in range(2):
        try:
            url = generate(HERO[slug])
            open(f'{OUT}/{slug}.png', 'wb').write(requests.get(url, timeout=120).content)
            print('ok', slug, flush=True); ok += 1
            break
        except Exception as e:
            msg = str(e)
            print('fail', slug, msg, flush=True)
            if any(t in msg for t in ('FreeTierOnly', 'Arrearage', 'Quota', 'Unpurchased', 'invalid_api_key')):
                print('STOP: доступ/квота/оплата — дальше не иду'); sys.exit(2)
            time.sleep(8)
print('done', ok, 'new;', len(os.listdir(OUT)), 'files in', OUT)
