"""ЧЕТЫРЕ ФОРМЫ РЕГИСТРАЦИИ НА СТРАНИЦУ (по канону).

ЗАЧЕМ. Канон, правило 65: «Форма регистрации — на обучение отдельная, на
индивидуальный тренинг отдельная, на консультации отдельная, бизнес-тренинг
отдельная». На странице не было НИ ОДНОЙ: стояли только якоря на блоки.

ПРАВИЛА, КОТОРЫЕ ЗДЕСЬ СОБЛЮДЕНЫ:
  · Формы уходят в существующий контур (api.ragimoff.org/api/training-reg),
    админку и Telegram-бот не трогаем — канон, правило 69.
  · Индивидуальный тренинг: минимум 20 часов, от 2000 AZN за одного
    специалиста и 3000, если ведут оба (канон, правило 70).
  · Консультация: цена зависит от числа участников и формата.
  · Кнопки живые: состояние отправки, результат, запасной путь в WhatsApp
    (канон, правило 110 — «запрещены дохлые кнопки регистрации»).

ЧТО ДЕЛАЕТ СКРИПТ:
  1. добавляет разметку блока регистрации в шаблон;
  2. добавляет тексты в данные;
  3. подключает forms.css и forms.js;
  4. собирает страницу.

Запуск:
    python _agent/tasks/add_forms.py
"""
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
TPL = os.path.join(PROJ, 'templates', 'home.html')
DATA = os.path.join(PROJ, 'content', 'ru.json')

BLOCK = '''
<!-- ═══════════ РЕГИСТРАЦИЯ: ЧЕТЫРЕ ФОРМЫ (канон, правило 65) ═══════════ -->
<section class="section section--lined" id="registration">
  <div class="wrap">
    <div class="section__head reveal">
      <span class="eyebrow">Регистрация</span>
      <h2>Записаться</h2>
      <p class="lead">Четыре направления — четыре отдельные формы. Заполните ту,
        которая вам нужна: заявка попадает к специалисту напрямую.</p>
    </div>

    <div class="reg reveal" data-req="Заполните выделенные поля" data-sending="Отправляем…"
         data-ok="Заявка принята. Мы свяжемся с вами."
         data-err="Не удалось отправить заявку.">

      <div class="reg__tabs" role="tablist" aria-label="Направление">
        <button class="reg__tab" type="button" data-tab="training" role="tab" aria-selected="true">
          Обучение<small>Получить диплом или сертификат</small>
        </button>
        <button class="reg__tab" type="button" data-tab="individual" role="tab" aria-selected="false">
          Индивидуальный тренинг<small>Личная работа со специалистом</small>
        </button>
        <button class="reg__tab" type="button" data-tab="consult" role="tab" aria-selected="false">
          Консультация<small>Один или вдвоём, онлайн или очно</small>
        </button>
        <button class="reg__tab" type="button" data-tab="b2b" role="tab" aria-selected="false">
          Для организаций<small>Тренинг для команды</small>
        </button>
      </div>

      <!-- 1. ОБУЧЕНИЕ -->
      <div class="reg__panel is-on" data-panel="training">
        <form class="reg__form" id="regTraining" novalidate>
          <label class="reg__field">
            <span class="reg__label">Имя</span>
            <input class="reg__input" type="text" name="fname" autocomplete="given-name">
          </label>
          <label class="reg__field">
            <span class="reg__label">Телефон</span>
            <input class="reg__input" type="tel" name="phone" autocomplete="tel" placeholder="+994 __ ___ __ __">
          </label>
          <label class="reg__field reg__field--wide">
            <span class="reg__label">Программа</span>
            <select class="reg__select" name="program">
              <option value="">Выберите программу</option>
              <option>Клиническая психология — диплом ДПО, 2392 часа</option>
              <option>Практикум по психотерапии — 864 часа</option>
              <option>Системная семейная терапия</option>
              <option>Психоанализ — 864 часа</option>
              <option>Психодиагностика — 864 часа</option>
              <option>Общая психология — 556 часов</option>
              <option>Юридические основы деятельности</option>
            </select>
          </label>
          <label class="reg__field reg__field--wide">
            <span class="reg__label">Вопрос, если есть</span>
            <textarea class="reg__textarea" name="question"></textarea>
          </label>
          <div class="reg__row">
            <span class="reg__note">Стоимость программ установлена. Порядок оплаты
              и начало занятий подтвердит специалист.</span>
            <button class="btn btn--gold" type="submit">Отправить заявку</button>
          </div>
          <div class="reg__msg" hidden></div>
        </form>
      </div>

      <!-- 2. ИНДИВИДУАЛЬНЫЙ ТРЕНИНГ -->
      <div class="reg__panel" data-panel="individual">
        <form class="reg__form" id="regIndividual" novalidate>
          <label class="reg__field">
            <span class="reg__label">Имя</span>
            <input class="reg__input" type="text" name="fname" autocomplete="given-name">
          </label>
          <label class="reg__field">
            <span class="reg__label">Телефон</span>
            <input class="reg__input" type="tel" name="phone" autocomplete="tel">
          </label>
          <label class="reg__field">
            <span class="reg__label">Часов занятий</span>
            <input class="reg__input" type="text" name="hours" placeholder="минимум 20">
          </label>
          <label class="reg__field">
            <span class="reg__label">Тема</span>
            <input class="reg__input" type="text" name="topic">
          </label>
          <div class="reg__field reg__field--wide">
            <span class="reg__label">Кто ведёт</span>
            <div class="reg__row" style="gap:18px">
              <label><input type="radio" name="who" value="kenan" checked> Кенан Рагимов</label>
              <label><input type="radio" name="who" value="samira"> Самира Рагимова</label>
              <label><input type="radio" name="who" value="both"> Оба специалиста</label>
            </div>
          </div>
          <div class="reg__price">от 2000 AZN за одного специалиста · 3000 AZN, если ведут оба</div>
          <div class="reg__row">
            <span class="reg__note">Минимум 20 часов. При добавлении человека цена
              на одного снижается, общая — растёт.</span>
            <button class="btn btn--gold" type="submit">Отправить заявку</button>
          </div>
          <div class="reg__msg" hidden></div>
        </form>
      </div>

      <!-- 3. КОНСУЛЬТАЦИЯ -->
      <div class="reg__panel" data-panel="consult">
        <form class="reg__form" id="regConsult" novalidate>
          <label class="reg__field">
            <span class="reg__label">Имя</span>
            <input class="reg__input" type="text" name="fname" autocomplete="given-name">
          </label>
          <label class="reg__field">
            <span class="reg__label">Телефон</span>
            <input class="reg__input" type="tel" name="phone" autocomplete="tel">
          </label>
          <div class="reg__field reg__field--wide">
            <span class="reg__label">Кто участвует</span>
            <div class="reg__row" style="gap:18px">
              <label><input type="radio" name="who" value="one" checked> Один человек</label>
              <label><input type="radio" name="who" value="both"> Вдвоём</label>
            </div>
          </div>
          <div class="reg__field reg__field--wide">
            <span class="reg__label">Формат</span>
            <div class="reg__row" style="gap:18px">
              <label><input type="radio" name="format" value="online" checked> Онлайн</label>
              <label><input type="radio" name="format" value="offline"> Очно</label>
            </div>
          </div>
          <label class="reg__field reg__field--wide">
            <span class="reg__label">С чем обращаетесь</span>
            <input class="reg__input" type="text" name="topic">
          </label>
          <div class="reg__price">онлайн 100 AZN · очно 150 AZN · вдвоём онлайн 150 AZN · вдвоём очно 200 AZN</div>
          <div class="reg__row">
            <span class="reg__note">Продолжительность — час. Точное время
              согласует специалист после заявки.</span>
            <button class="btn btn--gold" type="submit">Записаться</button>
          </div>
          <div class="reg__msg" hidden></div>
        </form>
      </div>

      <!-- 4. ДЛЯ ОРГАНИЗАЦИЙ -->
      <div class="reg__panel" data-panel="b2b">
        <form class="reg__form" id="regB2b" novalidate>
          <label class="reg__field">
            <span class="reg__label">Имя</span>
            <input class="reg__input" type="text" name="fname" autocomplete="name">
          </label>
          <label class="reg__field">
            <span class="reg__label">Телефон</span>
            <input class="reg__input" type="tel" name="phone" autocomplete="tel">
          </label>
          <label class="reg__field">
            <span class="reg__label">Организация</span>
            <input class="reg__input" type="text" name="company">
          </label>
          <label class="reg__field">
            <span class="reg__label">Участников</span>
            <input class="reg__input" type="text" name="count">
          </label>
          <label class="reg__field reg__field--wide">
            <span class="reg__label">Задача</span>
            <textarea class="reg__textarea" name="goal"></textarea>
          </label>
          <div class="reg__row">
            <span class="reg__note">Заявка без оплаты: сначала уточняем задачу
              и объём, потом предлагаем программу.</span>
            <button class="btn btn--gold" type="submit">Отправить заявку</button>
          </div>
          <div class="reg__msg" hidden></div>
        </form>
      </div>

    </div>
  </div>
</section>
'''


def main():
    tpl = io.open(TPL, encoding='utf-8').read()
    if 'id="registration"' in tpl:
        print('блок регистрации уже есть — ничего не делаю')
        return 0

    # ставим блок сразу после консультаций: клиент только что прочитал,
    # с чем приходят, и здесь же может записаться
    m = re.search(r'(<section class="section[^"]*" id="services">.*?\n</section>\n)', tpl, re.S)
    if not m:
        print('НЕ НАЙДЕН блок services — останов')
        return 1
    tpl = tpl[:m.end(1)] + BLOCK + tpl[m.end(1):]

    # подключаем стили и скрипт формы
    if 'forms.css' not in tpl:
        tpl = tpl.replace('<link rel="stylesheet" href="design/components/blocks.css">',
                          '<link rel="stylesheet" href="design/components/blocks.css">\n'
                          '<link rel="stylesheet" href="design/components/forms.css">')
    if 'forms.js' not in tpl:
        tpl = tpl.replace('</body>', '<script src="design/components/forms.js"></script>\n</body>')

    io.open(TPL, 'w', encoding='utf-8', newline='\n').write(tpl)

    data = json.loads(io.open(DATA, encoding='utf-8').read())
    # текстов внутри блока нет — он весь из разметки, поэтому данные не трогаем
    print('шаблон: добавлен блок регистрации с четырьмя формами')
    print('  подключено: forms.css, forms.js')

    r = subprocess.run([sys.executable, os.path.join(PROJ, '_tools', 'build_pages.py'), 'ru'],
                       capture_output=True, text=True, cwd=PROJ)
    print(r.stdout.strip() or r.stderr.strip())
    return r.returncode


if __name__ == '__main__':
    sys.exit(main())
