"""ДОБАВЛЕНИЕ ЧЕТЫРЁХ КРАТКОСРОЧНЫХ ПРОГРАММ (по канону).

ЗАЧЕМ. Канон (правило 87): «Блок "Обучение": каталог ровно из 7 программ —
3 долгосрочных и 4 краткосрочных; каждый маленький блок = отдельная дверь
входа в программу». Источник: «каталог обучающих программ, коих сейчас у
нас получается должно быть 7. Почему? Потому что 3 долгосрочных и
4 краткосрочных».

На странице было только 3 программы. Четыре короткие отсутствовали, то есть
блок не давал клиенту четыре из семи входов.

ОТКУДА ВЗЯТЫ ДАННЫЕ. Из реально существующих страниц сайта (ru/telim/), а не
придуманы: психоанализ 864 часа, психодиагностика 864 часа, общая психология
556 часов, юридические основы. Названия и часы сверены с самими файлами.

ЧТО ДЕЛАЕТ СКРИПТ:
  1. добавляет в шаблон раздел «Краткосрочные программы» с четырьмя карточками;
  2. добавляет в данные тексты для них;
  3. пересобирает страницу и показывает результат.

Запуск:
    python _agent/tasks/add_short_programs.py
"""
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))          # .../test/hermes/69
TPL = os.path.join(PROJ, 'templates', 'home.html')
DATA = os.path.join(PROJ, 'content', 'ru.json')

# ── ЧЕТЫРЕ КРАТКОСРОЧНЫЕ ПРОГРАММЫ ───────────────────────────────────────
# hours и адреса сверены с файлами в ru/telim/ сайта.
SHORT = [
    {
        'key': 'psixoanaliz',
        'form': 'Курс',
        'title': 'Психоанализ',
        'gain_pre': 'Даёт язык для работы с бессознательным:',
        'gain_b': 'теория и практика в одном курсе',
        'gain_post': ' — от фрейдовских оснований до современных техник.',
        'facts': ['864 часа', 'направление', 'ведёт Кенан'],
        'href': '/ru/telim/psixoanaliz.html',
    },
    {
        'key': 'psixodiaqnostika',
        'form': 'Курс',
        'title': 'Психодиагностика',
        'gain_pre': 'Даёт инструмент для постановки диагноза:',
        'gain_b': 'методики и их границы',
        'gain_post': ' — что показывает тест, а что приписывают ему зря.',
        'facts': ['864 часа', 'инструменты', 'практика'],
        'href': '/ru/telim/psixodiaqnostika.html',
    },
    {
        'key': 'umumi',
        'form': 'Базовая программа',
        'title': 'Общая психология',
        'gain_pre': 'Даёт основу профессии:',
        'gain_b': 'системное представление о психике',
        'gain_post': ' для тех, кто начинает путь в психологии.',
        'facts': ['556 часов', 'основы', 'с нуля'],
        'href': '/ru/telim/umumi-psixologiya.html',
    },
    {
        'key': 'qanuni',
        'form': 'Для практикующих',
        'title': 'Юридические основы',
        'gain_pre': 'Даёт защиту в работе:',
        'gain_b': 'правовая база деятельности',
        'gain_post': ' — границы ответственности, документы, что можно и чего нельзя.',
        'facts': ['правовая база', 'документы', 'для практики'],
        'href': '/ru/telim/qanuni-esaslar.html',
    },
]


def card_html(c, k):
    """Разметка карточки — ТАКАЯ ЖЕ, как у существующих программ.
    Вид не меняется: новые элементы встают в уже одобренную форму."""
    return '''      <article class="program reveal">
        <span class="program__form">{{%(form)s}}</span>
        <h3 class="program__title">{{%(title)s}}</h3>
        <p class="program__gain">{{%(pre)s}} <b>{{%(b)s}}</b>{{%(post)s}}</p>
        <div class="program__facts">
          <span>{{%(f1)s}}</span><span>{{%(f2)s}}</span><span>{{%(f3)s}}</span>
        </div>
        <div class="program__foot">
          <a class="btn btn--line btn--sm" href="%(href)s">{{%(btn)s}}</a>
        </div>
      </article>
''' % {
        'form': k + '_form', 'title': k + '_title', 'pre': k + '_pre',
        'b': k + '_b', 'post': k + '_post',
        'f1': k + '_f1', 'f2': k + '_f2', 'f3': k + '_f3',
        'btn': k + '_btn', 'href': c['href'],
    }


def main():
    tpl = io.open(TPL, encoding='utf-8').read()

    if 'short-programs' in tpl:
        print('раздел краткосрочных уже есть — ничего не делаю')
        return 0

    data = json.loads(io.open(DATA, encoding='utf-8').read())

    # тексты для новых карточек
    for c in SHORT:
        k = c['key']
        data[k + '_form'] = c['form']
        data[k + '_title'] = c['title']
        data[k + '_pre'] = c['gain_pre']
        data[k + '_b'] = c['gain_b']
        data[k + '_post'] = c['gain_post']
        for i, f in enumerate(c['facts'], 1):
            data[k + '_f%d' % i] = f
        data[k + '_btn'] = 'Программа'

    block = '''
    <div id="short-programs" style="margin-top:var(--space-u8)">
      <div class="section__head" style="align-items:flex-start;text-align:left;margin-bottom:var(--space-u5)">
        <span class="eyebrow">Краткосрочные</span>
        <h3 style="font-family:var(--font-display);font-size:var(--size-step3)">Четыре короткие программы</h3>
        <p class="lead">Не заменяют основное обучение, а закрывают конкретную нехватку:
          направление, инструмент, основу или правовую сторону работы.</p>
      </div>
      <div class="cards grid--4" style="display:grid">
''' + ''.join(card_html(c, c['key']) for c in SHORT) + '''      </div>
    </div>

'''

    # вставляем перед закрытием блока обучения: ищем секцию programs
    m = re.search(r'(<section class="section" id="programs">.*?)(\n  </div>\n</section>)', tpl, re.S)
    if not m:
        print('НЕ НАЙДЕН блок programs — останов')
        return 1

    tpl = tpl[:m.end(1)] + block + tpl[m.end(1):]
    io.open(TPL, 'w', encoding='utf-8', newline='\n').write(tpl)
    io.open(DATA, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(data, ensure_ascii=False, indent=2))

    print('шаблон: добавлен раздел краткосрочных программ')
    print('данные: добавлено %d меток' % (len(SHORT) * 9))

    # пересборка и проверка
    r = subprocess.run([sys.executable, os.path.join(PROJ, '_tools', 'build_pages.py'), 'ru'],
                       capture_output=True, text=True, cwd=PROJ)
    print(r.stdout.strip() or r.stderr.strip())
    return r.returncode


if __name__ == '__main__':
    sys.exit(main())
