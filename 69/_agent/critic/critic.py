"""АГЕНТ-КРИТИК: ПРОВЕРКА РАБОТЫ ПРОТИВ КАНОНА.

ЗАЧЕМ. Владелец (11.11.2026): «Вам нужно сделать критика... который будет
каждый шаг, каждую работу проверять, каждый элемент сайта. Ты делаешь
элемент сайта, сдаёшь, он проверяет и сразу показывает ошибки, которые
надо исправить... Этот критик не должен тебя допускать, чтобы ты сдавал
работу незавершённой. И доделывал до тех пор, пока у критика не закончатся
замечания. Пока по всем пунктам, которые будут созданы из всех моих реплик».

И главная причина, по которой он понадобился: «вы просто не умеете свои
задачи, свои работы проверять. Не проверяете. Тяп-ляп сделали — и бросаете
вперёд, типа готово, проверяйте. А я в качестве редактора должен постоянно
проверять и находить ошибки, злиться».

То есть критик существует ровно для одного: чтобы владелец БОЛЬШЕ НЕ БЫЛ
РЕДАКТОРОМ. Проверка идёт до сдачи, а не после.

ВАЖНО ПРО ПРИРОДУ КРИТИКА. Он проверяет ФАКТЫ на странице, а не мнения о
них: наличие элемента, размер, цвет, контраст, число строк, положение в
кадре, битые ссылки, видимость при отключённом движении. Всё, что можно
измерить прибором, измеряется прибором. Замечание без замера — это мнение,
и оно не принимается как основание для правки.

ПРАВО РЕШЕНИЯ. Владелец: «Всё равно оставить право выбора, что делать тебе.
Почему? Потому что он может выдавать техническую ошибку... А ты смотришь и
принимаешь решение. Но объясняешь. Это диалог». Поэтому у критика есть
второй режим: он выносит замечание, а исполнитель может его ОТКЛОНИТЬ,
обязательно с обоснованием. Отклонение без обоснования не допускается —
это и есть «тяп-ляп».

Запуск:
    python _agent/critic/critic.py                 # полная проверка страницы
    python _agent/critic/critic.py --json          # вывод машинно-читаемо
"""
import argparse
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# ПРИЧИНА ПРАВКИ: было PROJ = dirname(HERE), то есть папка _agent вместо
# папки проекта. Критик из-за этого «не находил» ни страницу, ни канон.
# Проверять надо на два уровня выше: _agent/critic → _agent → test/69.
PROJ = os.path.dirname(os.path.dirname(HERE))     # .../test/69
CANON = os.path.join(PROJ, '_agent', 'canon')

# ── УРОВНИ ЗАМЕЧАНИЙ ─────────────────────────────────────────────────────
BLOCK = 'БЛОК'      # нельзя сдавать: нарушение канона или технический дефект
WARN = 'ВНИМАНИЕ'   # нужно объяснить: либо принять, либо обосновать отказ
NOTE = 'ЗАМЕТКА'    # к сведению, решения не требует


class Report:
    def __init__(self):
        self.items = []

    def add(self, level, rule, detail, where='', quote=''):
        self.items.append({'level': level, 'rule': rule, 'detail': detail,
                           'where': where, 'quote': quote})

    def count(self, level):
        return sum(1 for i in self.items if i['level'] == level)


# ── ПРОВЕРКИ HTML ────────────────────────────────────────────────────────

def check_html(page, r):
    """Страница как файл: структура, ссылки, обязательные элементы."""
    h = io.open(page, encoding='utf-8', errors='ignore').read()

    # 1. Ссылки и картинки.
    #    ВАЖНОЕ РАЗЛИЧИЕ, из-за которого первая версия критика давала
    #    десятки ложных срабатываний: пути вида /images/... — АБСОЛЮТНЫЕ
    #    ОТ КОРНЯ САЙТА, и на живом адресе работают (корень домена = папка
    #    site). Критик же запускается из ЛОКАЛЬНОЙ папки версии, и путь к
    #    корню сайта приходится вычислять.
    #
    #    ПРИЧИНА ВТОРОЙ ПРАВКИ: после переноса версий в test/hermes/69
    #    корень сайта оказался дальше, чем предполагал простой расчёт, и
    #    критик снова «нашёл» 40 битых ссылок. Поэтому корень теперь
    #    ИЩЕТСЯ по признаку: папка, содержащая index.html сайта и каталог
    #    images. Так проверка не сломается при следующем переносе.
    def find_site_root(start):
        d = start
        for _ in range(6):
            if os.path.isdir(os.path.join(d, 'images')) and \
               os.path.isdir(os.path.join(d, 'books')):
                return d
            parent = os.path.dirname(d)
            if parent == d:
                break
            d = parent
        return os.path.dirname(os.path.dirname(PROJ))   # запасной вариант

    SITE_ROOT = find_site_root(os.path.dirname(page))
    base = os.path.dirname(page)

    missing = []
    for m in re.finditer(r'(?:href|src)="([^"]+)"', h):
        url = m.group(1).strip()
        if not url or url.startswith(('http', 'mailto:', 'tel:', 'data:', '#')):
            continue
        clean = url.split('?')[0].split('#')[0]
        if not clean:
            continue
        if clean.startswith('/'):
            target = os.path.normpath(os.path.join(SITE_ROOT, clean.lstrip('/')))
        else:
            target = os.path.normpath(os.path.join(base, clean))
        if not (os.path.isfile(target) or os.path.isdir(target)):
            missing.append(url)

    # Одинаковые отсутствующие адреса показываем ОДИН раз: список из
    # пятидесяти повторов одной ссылки читать невозможно.
    for url in sorted(set(missing)):
        n = missing.count(url)
        r.add(BLOCK, 'Битая ссылка' + (' (×%d)' % n if n > 1 else ''), url, 'страница')

    # 2. Картинки без alt — доступность и запрет владельца на «пустые» места
    for m in re.finditer(r'<img\b[^>]*>', h, re.I):
        tag = m.group(0)
        if 'alt=' not in tag.lower():
            r.add(WARN, 'Картинка без alt', tag[:90], 'страница')

    # 3. Обязательные вещи канона
    if not re.search(r'<html[^>]*\blang=', h):
        r.add(BLOCK, 'Не указан язык документа', '<html lang>', 'начало файла')
    if '<h1' not in h:
        r.add(BLOCK, 'На странице нет главного заголовка h1', '<h1>')
    if h.count('<h1') > 1:
        r.add(WARN, 'Больше одного h1', 'найдено: %d' % h.count('<h1'))

    return h


def check_texts(page, r):
    """Тексты: длина заголовков, запретные формулировки, дубли."""
    h = io.open(page, encoding='utf-8', errors='ignore').read()

    # Заголовки: владелец неоднократно требовал, чтобы заголовок не разваливался
    # на много строк. Точную ширину даёт замер в браузере, здесь — длина текста.
    for m in re.finditer(r'<h2[^>]*>(.*?)</h2>', h, re.S | re.I):
        t = re.sub(r'<[^>]+>', ' ', m.group(1))
        t = re.sub(r'\s+', ' ', t).strip()
        if len(t) > 70:
            r.add(WARN, 'Длинный заголовок h2 (%d знаков)' % len(t),
                  t[:80], 'вероятно развалится на 3 строки')

    # Запрещённые формулировки (из канона: самохвальба, слово «доказательство»)
    banned = [
        (r'\bдоказательств', 'Слово «доказательство» — владелец запретил прямо'),
        (r'\bнаш[аи]?\s+уникальн', 'Самохвальба: «наша уникальная»'),
        (r'\bлучш(ий|ая|ее)\s+в\s+мире\b', 'Самохвальба: «лучший в мире» без подтверждения'),
        (r'\bмы\s+гордимся\b', 'Самохвальба: «мы гордимся»'),
    ]
    body = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', h, flags=re.S | re.I)
    for rx, why in banned:
        for m in re.finditer(rx, body, re.I):
            frag = body[max(0, m.start() - 60):m.end() + 60]
            frag = re.sub(r'\s+', ' ', frag)
            r.add(WARN, why, frag, 'текст')

    # Дубли абзацев: владелец отдельно ругал повторы
    paras = re.findall(r'<p[^>]*>(.*?)</p>', body, re.S | re.I)
    seen = {}
    for p in paras:
        t = re.sub(r'<[^>]+>', ' ', p)
        t = re.sub(r'\s+', ' ', t).strip()
        if len(t) < 40:
            continue
        if t in seen:
            r.add(BLOCK, 'Дублирующийся абзац', t[:80], 'повтор текста')
        seen[t] = True


def check_canon_files(r):
    """Сам канон: на месте ли, подтверждены ли цитаты."""
    files = ['otvet_ВИД.md', 'otvet_ТЕКСТЫ.md', 'otvet_СТРУКТУРА.md',
             'otvet_ОШИБКИ_И_ПРОЦЕСС.md', 'otvet_ТЕХНОЛОГИЯ.md']
    for f in files:
        p = os.path.join(CANON, f)
        if not os.path.isfile(p):
            r.add(BLOCK, 'Раздел канона отсутствует', f, 'папка canon')
        elif os.path.getsize(p) < 2000:
            r.add(WARN, 'Подозрительно малый раздел канона', f,
                  '%d байт' % os.path.getsize(p))


def check_css_balance(r):
    """БАЛАНС ФИГУРНЫХ СКОБОК В СТИЛЯХ.

    ЗАЧЕМ ОТДЕЛЬНАЯ ПРОВЕРКА. Найдено 11.11.2026: в hero.css стоял
    медиа-запрос без закрывающей скобки. Файл выглядел ЦЕЛЫМ, ошибок
    в консоли не было, но браузер молча отбрасывал все 200 строк стилей
    после места ошибки — включая цвета текста героя.

    ЧТО ЭТО ЗНАЧИЛО ДЛЯ ВЛАДЕЛЬЦА: «в светлой теме буквы не видны
    на некоторых местах». Он видел следствие, а причина была в одной
    пропущенной скобке за 80 строк до конца файла.

    Это самый коварный класс дефектов в проекте: ни синтаксическая
    проверка, ни глаз, ни консоль браузера его не показывают. Показывает
    только подсчёт скобок — поэтому он теперь обязателен.
    """
    import glob
    import re as _re
    for f in sorted(glob.glob(os.path.join(PROJ, 'design', '**', '*.css'), recursive=True)):
        try:
            s = io.open(f, encoding='utf-8').read()
        except Exception:
            continue
        # комментарии исключаем: их содержимое — текст, а не код
        clean = _re.sub(r'/\*.*?\*/', '', s, flags=_re.S)
        o, c = clean.count('{'), clean.count('}')
        if o != c:
            r.add(BLOCK, 'Нарушен баланс скобок в стилях',
                  '%s: открывающих %d, закрывающих %d' % (os.path.basename(f), o, c),
                  'браузер молча отбросит часть правил')


def main():
    ap = argparse.ArgumentParser(description='Проверка страницы против канона')
    ap.add_argument('--page', default=os.path.join(PROJ, 'index.html'),
                    help='проверяемая страница')
    ap.add_argument('--json', action='store_true', help='вывод машинно-читаемо')
    a = ap.parse_args()

    r = Report()
    check_canon_files(r)
    check_css_balance(r)
    if os.path.isfile(a.page):
        check_html(a.page, r)
        check_texts(a.page, r)
    else:
        r.add(BLOCK, 'Страница не найдена', a.page)

    if a.json:
        print(json.dumps(r.items, ensure_ascii=False, indent=2))
        return 1 if r.count(BLOCK) else 0

    print('=' * 72)
    print('КРИТИК: проверка против канона')
    print('страница: %s' % a.page)
    print('=' * 72)
    print()

    if not r.items:
        print('Замечаний нет. Работа может быть сдана.')
        return 0

    for level in (BLOCK, WARN, NOTE):
        items = [i for i in r.items if i['level'] == level]
        if not items:
            continue
        print('── %s (%d)' % (level, len(items)))
        for i in items:
            print('   • %s' % i['rule'])
            if i['detail']:
                print('     %s' % i['detail'][:150])
            if i['where']:
                print('     место: %s' % i['where'])
        print()

    print('=' * 72)
    print('ИТОГ: блокирующих %d, на объяснение %d'
          % (r.count(BLOCK), r.count(WARN)))
    print()
    if r.count(BLOCK):
        print('РАБОТА НЕ МОЖЕТ БЫТЬ СДАНА: есть блокирующие замечания.')
        print('Правило владельца: критик не пропускает незавершённую работу,')
        print('и правки идут до тех пор, пока замечания не закончатся.')
        return 1
    print('Блокирующих замечаний нет. Замечания уровня «внимание» нужно либо')
    print('исправить, либо отклонить с обоснованием — молча пропускать нельзя.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
