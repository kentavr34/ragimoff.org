"""СБОРКА СТРАНИЦЫ ИЗ ШАБЛОНА И ДАННЫХ.

ТЕХНОЛОГИЯ, КОТОРУЮ ЭТОТ ФАЙЛ РЕАЛИЗУЕТ (требование владельца 11.11.2026):
    шаблон (разметка + стили) + данные (тексты) → страница

Владелец: «нельзя начинать строить автомобиль, а потом перестроить его
и сделать жилой дом... Тебе задача была дана сделать на примере одной
страницы по новой технологии. А ты мне HTML суёшь».

Здесь эти две задачи РАЗДЕЛЕНЫ так, чтобы больше не смешиваться:
    templates/home.html   — ВИД. Правится, только если меняем вид.
    content/<язык>.json   — СЛОВА. Правится всегда, когда меняем текст.
    build_pages.py        — связывает одно с другим и ничего больше.

ЧТО ЭТОТ СБОРЩИК НЕ ДЕЛАЕТ (и это важно). Он НЕ строит разметку и НЕ
описывает блоки. Прежний вариант делал именно так — генерировал HTML
из описаний блоков, и вид получался «по мотивам»: карточки, шапка и
герой вышли хуже одобренного эталона. Тогда и была испорчена работа,
которую владелец оценил на 70%.

ГЛАВНАЯ ГАРАНТИЯ. Шаблон получен из одобренного эталона механически
(_tools/to_template.py), и сборка из него совпадает с эталоном БАЙТ В БАЙТ.
Значит перенос страницы в технологию НЕ ИЗМЕНИЛ ВИД.

ПРОВЕРКИ, ВСТРОЕННЫЕ В СБОРКУ (не отдельным шагом):
  1. Незаполненная метка останавливает сборку: пустое место на странице
     хуже остановленной сборки.
  2. Данные, которые шаблон не использует, выводятся предупреждением:
     это признак, что текст поправили, а он никуда не попал.

Запуск:
    python _tools/build_pages.py            # все языки, для которых есть данные
    python _tools/build_pages.py ru         # только русский
"""
import html
import io
import json
import pathlib
import re
import sys

BASE = pathlib.Path(__file__).resolve().parents[1]
TPL_DIR = BASE / 'templates'
CONTENT = BASE / 'content'
LANGS = ['ru', 'az', 'en']

MARK = re.compile(r'\{\{([A-Za-z0-9_]+)\}\}')


def load_data(lang):
    """Данные языка — единственный источник текста на странице."""
    f = CONTENT / ('%s.json' % lang)
    if not f.is_file():
        return None
    return json.loads(io.open(f, encoding='utf-8').read())


def render(tpl, data, lang):
    used = set()
    missing = []

    def sub(m):
        k = m.group(1)
        used.add(k)
        if k not in data:
            missing.append(k)
            return m.group(0)
        # экранируем: угловые скобки в тексте не сломают разметку
        return html.escape(str(data[k]), quote=True)

    out = MARK.sub(sub, tpl)

    if missing:
        raise SystemExit(
            'ОСТАНОВ: в шаблоне есть метки, которых нет в данных %s.json:\n  %s\n'
            'Добавьте их в файл текста — страница с пустыми местами не собирается.'
            % (lang, '\n  '.join(sorted(set(missing))[:20])))
    return out, used


def build(lang):
    data = load_data(lang)
    if data is None:
        print('  %-3s  данных нет — пропускаю' % lang)
        return None

    tpl_file = TPL_DIR / 'home.html'
    if not tpl_file.is_file():
        raise SystemExit('НЕТ ШАБЛОНА: %s' % tpl_file)
    tpl = io.open(tpl_file, encoding='utf-8').read()

    out, used = render(tpl, data, lang)

    # язык документа берётся из данных, а не остаётся русским
    if lang != 'ru':
        out = re.sub(r'<html lang="[a-z]+"', '<html lang="%s"' % lang, out, count=1)

    # РАССИНХРОН: текст в данных, который шаблон не использует — значит
    # правка никуда не попала. Это надо видеть, а не выяснять на сайте.
    extra = [k for k in data if k not in used and not k.startswith('_')]
    if extra:
        print('  ⚠ %s: не использовано меток: %d — этот текст на страницу не попадёт'
              % (lang, len(extra)))
        for k in sorted(extra)[:5]:
            print('       %s = %s' % (k, str(data[k])[:55]))

    dest = BASE / ('index.html' if lang == 'ru' else '%s/index.html' % lang)
    dest.parent.mkdir(parents=True, exist_ok=True)

    # ── ПУТИ К ФАЙЛАМ ДЛЯ СТРАНИЦ В ПОДПАПКАХ ─────────────────────────
    # НАЙДЕНО 11.11.2026: азербайджанская и английская страницы собирались
    # с теми же относительными путями, что и русская, но лежат в ПОДПАПКЕ
    # (az/index.html, en/index.html). Ссылки вида `design/base.css`
    # указывали на `az/design/base.css`, которого нет, — и обе страницы
    # оставались БЕЗ ОФОРМЛЕНИЯ. Никакой ошибки при этом не возникало:
    # браузер просто не находил стили. Нашёл критик — 17 «битых ссылок»,
    # то есть не ложное срабатывание, а настоящая потеря вида.
    #
    # ЧТО ДЕЛАЕМ: для страниц в подпапке относительные пути поднимаются
    # на уровень выше (`../`). Абсолютные пути (/images/..., /books/...)
    # не трогаем — они указывают на корень ДОМЕНА и от папки не зависят.
    if lang != 'ru':
        out = re.sub(r'(["\'(])(design/|vendor/)', r'\1../\2', out)

    io.open(dest, 'w', encoding='utf-8', newline='\n').write(out)
    return dest, len(used)


def main():
    langs = sys.argv[1:] or LANGS
    print('СБОРКА: шаблон + данные → страница')
    print('  вид    : templates/home.html')
    print('  слова  : content/<язык>.json')
    print()
    done = 0
    for lg in langs:
        r = build(lg)
        if r:
            dest, n = r
            done += 1
            print('  ✅ %-3s  %-22s меток заполнено: %d' % (lg, dest.relative_to(BASE), n))
    if not done:
        print('  ничего не собрано: нет файлов данных')
        return 1
    print('\nготово')
    return 0


if __name__ == '__main__':
    sys.exit(main())
