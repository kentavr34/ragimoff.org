"""ЭТАЛОН → ШАБЛОН + ДАННЫЕ.

ЗАЧЕМ ЭТОТ ФАЙЛ. Владелец (11.11.2026): «нельзя начинать строить автомобиль,
а потом перестроить его и сделать жилой дом. Тебе задача была дана сделать на
примере одной страницы ПО НОВОЙ ТЕХНОЛОГИИ. А ты мне HTML суёшь».

Суть претензии верна. Было два неверных подхода:
  1. Текст прямо в HTML — правка формулировки требует правки разметки,
     а на трёх языках это три расходящихся файла.
  2. Я переписал разметку и стили «по мотивам» — и потерял вид, который
     владелец уже одобрил. Визуал и технологию нельзя менять по очереди:
     при переносе страницы в шаблон вид обязан остаться ТЕМ ЖЕ.

ПРАВИЛЬНЫЙ ПОДХОД, реализованный здесь: эталон берётся как НЕИЗМЕНЯЕМАЯ
основа. Из него механически вынимаются ТОЛЬКО ТЕКСТЫ и АДРЕСА — они
становятся данными. Разметка и стили остаются ровно теми же.

    эталон index.html  →  _tools/to_template.py  →  templates/home.html (шаблон)
                                                   →  content/ru.json (данные)
    шаблон + данные    →  _tools/build_pages.py  →  index.html  (тот же вид)

КАК РАБОТАЕТ ВЫНЕСЕНИЕ
  Текстовые узлы и атрибуты с адресами заменяются метками вида
  {{section.key}} — плоскими ключами, без вложенных путей. Плоские ключи
  взяты намеренно: вложенные пути в шаблонах читаются плохо, а ошибку в
  них почти невозможно найти глазами.

ГАРАНТИЯ, ЗАШИТАЯ В КОД
  После вынесения скрипт собирает страницу обратно из шаблона и данных и
  сравнивает с эталоном. Расхождение — это ошибка, а не «почти то же самое»:
  именно «почти то же самое» и превратило хороший вид в плохой.

Запуск:
    python _tools/to_template.py
"""
import html
import io
import json
import pathlib
import re
import sys

BASE = pathlib.Path(__file__).resolve().parents[1]
ETALON = BASE / '_agent' / 'etap' / 'index_ETALON_70.html'
TPL = BASE / 'templates' / 'home.html'
DATA = BASE / 'content' / 'ru.json'


# ── ЧТО НЕ ВЫНОСИТЬ В ДАННЫЕ ─────────────────────────────────────────────
# Техническое: не текст для человека, а разметка, ключи, служебные адреса.
KEEP_AS_IS = [
    r'^\s*$',                      # пустые
    r'^[{}();,.\s]+$',             # синтаксис скриптов
    r'^\s*(design|vendor|images|books)/',  # пути к своим файлам
    r'^\s*/',                      # абсолютные пути
    r'^https?://',
    r'^#[a-zA-Z]',                 # якоря
    r'^[a-z-]+$',                  # кодовые слова (dark, light, sepia…)
    r'\.(css|js|webp|jpg|png|svg)$',
    r'^__HIDE_',                   # спрятанные script/style — вернуть как есть
]

# Атрибуты, которые МОГУТ содержать текст для человека.
TEXT_ATTRS = ('alt', 'title', 'aria-label', 'content')


def keep(text):
    """Проверяет, надо ли оставить строку прямо в шаблоне."""
    t = text.strip()
    if not t:
        return True
    for rx in KEEP_AS_IS:
        if re.match(rx, t):
            return True
    # строки без букв вообще (числа, знаки) — не текст для человека
    if not re.search(r'[A-Za-zА-Яа-яƏəĞğŞşÇçÖöÜüİı]', t):
        return True
    return False


def is_text_node(text):
    """Текст между тегами, который стоит вынести."""
    t = text.strip()
    if not t or keep(t):
        return False
    # внутри <script> и <style> не трогаем — это код, а не текст
    return True


def main():
    if not ETALON.is_file():
        print('НЕТ ЭТАЛОНА: %s' % ETALON)
        return 1

    src = io.open(ETALON, encoding='utf-8').read()
    data = {}
    n = [0]

    def key(prefix):
        n[0] += 1
        return '%s_%02d' % (prefix, n[0])

    # ── 1. Вырезаем <script> и <style> целиком: там код и данные темы,
    #      их вынесение сломало бы переключатель оформления ──────────────
    placeholders = {}

    def hide(m):
        tag = m.group(1)
        k = '__HIDE_%s_%d__' % (tag, len(placeholders))
        placeholders[k] = m.group(0)
        return k

    work = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', hide, src, flags=re.S | re.I)

    # ── 2. Атрибуты с текстом (alt, title, aria-label) ──────────────────
    def attr_sub(m):
        name, val = m.group(1), m.group(2)
        if keep(val) or len(val.strip()) < 2:
            return m.group(0)
        k = key('txt')
        data[k] = html.unescape(val)
        return '%s="{{%s}}"' % (name, k)

    work = re.sub(r'\b(%s)="([^"]*)"' % '|'.join(TEXT_ATTRS), attr_sub, work, flags=re.I)

    # ── 3. Текстовые узлы между тегами ─────────────────────────────────
    #     Идём по частям, разрезанным тегами: то, что не тег — кандидат.
    parts = re.split(r'(<[^>]+>)', work)
    out = []
    for part in parts:
        if part.startswith('<') and part.endswith('>'):
            out.append(part)
            continue
        # текст с сохранением ведущих и хвостовых пробелов (для ритма вёрстки)
        m = re.match(r'^(\s*)(.*?)(\s*)$', part, flags=re.S)
        if not m:
            out.append(part)
            continue
        pre, core, post = m.group(1), m.group(2), m.group(3)
        if is_text_node(core):
            k = key('txt')
            data[k] = html.unescape(core)
            out.append('%s{{%s}}%s' % (pre, k, post))
        else:
            out.append(part)
    work = ''.join(out)

    # ── 4. Возвращаем скрипты и стили на место ─────────────────────────
    for k, v in placeholders.items():
        work = work.replace(k, v)

    TPL.parent.mkdir(parents=True, exist_ok=True)
    io.open(TPL, 'w', encoding='utf-8', newline='\n').write(work)

    # тексты сохраняем отдельно: это заготовка для content/ru.json
    TEXTS = BASE / 'content' / '_взято_из_эталона.json'
    TEXTS.parent.mkdir(parents=True, exist_ok=True)
    io.open(TEXTS, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(data, ensure_ascii=False, indent=2))

    print('шаблон: %s (%d меток)' % (TPL.relative_to(BASE), n[0]))
    print('тексты: %s' % TEXTS.relative_to(BASE))

    # ── 5. ПРОВЕРКА ОБРАТНОЙ СБОРКИ ────────────────────────────────────
    # Собираем страницу из шаблона и данных и сверяем с эталоном.
    # Совпадение = при переносе в шаблон вид не изменился.
    def put(text, key_):
        return re.sub(r'\{\{%s\}\}' % re.escape(key_), lambda _m: html.escape(data[key_], quote=True), text)

    back = work
    for k in data:
        back = put(back, k)

    if back == src:
        print('\n✅ СБОРКА ИЗ ШАБЛОНА СОВПАДАЕТ С ЭТАЛОНОМ БАЙТ В БАЙТ.')
        print('   Вид не изменился: разметка и стили те же, тексты теперь в данных.')
        return 0

    # если не совпало — показываем ПЕРВОЕ расхождение, а не «что-то не то»
    lim = min(len(back), len(src))
    pos = next((i for i in range(lim) if back[i] != src[i]), lim)
    print('\n❌ РАСХОЖДЕНИЕ с эталоном на символе %d' % pos)
    print('   эталон : %r' % src[max(0, pos - 60):pos + 60])
    print('   собрано: %r' % back[max(0, pos - 60):pos + 60])
    print('   длины: эталон %d, собрано %d' % (len(src), len(back)))
    return 1


if __name__ == '__main__':
    sys.exit(main())
