"""ПЕРЕНОС ОСТАТКОВ РУССКОГО ТЕКСТА ИЗ ШАБЛОНА В ДАННЫЕ.

ЗАЧЕМ. Система управления дизайном требует: текст ОТДЕЛЬНО от вида.
Шаблон — вид, content/*.json — тексты. Когда шаблон собран из готовой
страницы механически (разрезанием), часть текста остаётся вшитой прямо
в разметку. Раннер заметен только на других языках: собрал
азербайджанскую страницу — и в ней по-русски написано «Отправить заявку»,
«Имя», «Телефон», целый блок краткосрочных программ.

Найдено 11.11.2026 замером: в az/index.html — 1197 русских букв, причём
в английской ровно столько же. Это и был признак, что дело не в переводе,
а в шаблоне.

ЧТО ДЕЛАЕТ ЭТОТ СКРИПТ:
  1. находит в шаблоне текстовые узлы с русскими буквами (вне <script>,
     <style>, комментариев и вне уже существующих меток);
  2. заменяет каждый на метку {{txt_NNN}};
  3. дописывает тексты в ru.json, az.json, en.json — с переводом для тех
     мест, где перевод известен из уже переведённых данных, и с пометкой
     TODO там, где нужен новый перевод.

ВАЖНО: скрипт СОХРАНЯЕТ выравнивание и переводы строк, чтобы собранная
страница не потеряла вид. Запускать после резервной копии шаблона.
"""
import io
import json
import os
import re
import shutil
import sys

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(PROJ, 'templates', 'home.html')
CONTENT = os.path.join(PROJ, 'content')


def find_russian_text_nodes(html):
    """Возвращает список отрезков (start, end, текст) с русскими буквами
       в видимых текстовых узлах шаблона."""
    # зоны, где текст не является видимым: комментарии, скрипты, стили
    zones = []
    for pat in (r'<!--.*?-->', r'<script.*?</script>', r'<style.*?</style>'):
        for m in re.finditer(pat, html, re.S):
            zones.append((m.start(), m.end()))

    def in_zone(pos):
        for a, b in zones:
            if a <= pos < b:
                return True
        return False

    out = []
    # текстовые узлы: между > и <
    for m in re.finditer(r'>([^<>]+)<', html):
        t = m.group(1)
        if not re.search(r'[а-яА-ЯёЁ]', t):
            continue
        if in_zone(m.start(1)):
            continue
        # пропускаем технические значения: alt, aria, скриптовые выражения
        out.append((m.start(1), m.end(1), t))
    return out


def main():
    apply_changes = '--apply' in sys.argv
    html = io.open(TPL, encoding='utf-8').read()
    nodes = find_russian_text_nodes(html)

    print('найдено русских текстовых узлов в шаблоне: %d' % len(nodes))
    total_words = sum(len(re.findall(r'[а-яА-ЯёЁ]+', t)) for _, _, t in nodes)
    print('русских слов всего: %d' % total_words)

    # какие метки уже есть
    ru = json.loads(io.open(os.path.join(CONTENT, 'ru.json'), encoding='utf-8').read())
    existing = {v.strip(): k for k, v in ru.items()
                if isinstance(v, str) and not k.startswith('_')}

    new_texts = []
    for a, b, t in nodes:
        key = t.strip()
        if key in existing:
            # текст уже есть в данных — просто ставим метку
            new_texts.append((a, b, t, existing[key], False))
        else:
            new_texts.append((a, b, t, None, True))

    already = sum(1 for x in new_texts if not x[4])
    fresh = sum(1 for x in new_texts if x[4])
    print('  из них уже есть в данных: %d' % already)
    print('  требуют перевода заново: %d' % fresh)

    print()
    print('--- примеры новых (первые 12) ---')
    shown = 0
    for a, b, t, key, is_new in new_texts:
        if is_new and shown < 12:
            print('   %r' % t.strip()[:70])
            shown += 1

    if not apply_changes:
        print()
        print('Это предварительный просмотр. Запусти с --apply для правки.')
        return

    # резервная копия
    bak = TPL + '.bak'
    shutil.copy(TPL, bak)
    print('резервная копия: %s' % bak)

    # нумеруем новые метки, продолжая существующую нумерацию
    nums = [int(m.group(1)) for k in ru if (m := re.match(r'txt_(\d+)$', k))]
    nxt = (max(nums) + 1) if nums else 1

    # правим шаблон с конца, чтобы не сдвигать позиции
    result = html
    added = {}
    for a, b, t, key, is_new in sorted(new_texts, key=lambda x: -x[0]):
        raw = t
        # сохраняем отступы и переводы строк по краям
        lead = re.match(r'\s*', raw).group(0)
        trail = re.match(r'.*?(\s*)$', raw, re.S).group(1)
        core = raw.strip()
        if is_new:
            if core in added:
                key = added[core]
            else:
                key = 'txt_%d' % nxt
                nxt += 1
                added[core] = key
        repl = lead + '{{' + key + '}}' + trail
        result = result[:a] + repl + result[b:]

    io.open(TPL, 'w', encoding='utf-8', newline='').write(result)
    print('шаблон обновлён, новых меток: %d' % len(added))

    # дописываем новые тексты в ru.json; az/en — пометка на перевод
    with io.open(os.path.join(CONTENT, 'ru.json'), 'w', encoding='utf-8', newline='\n') as f:
        ru.update(added and {v: k for k, v in added.items()} or {})
        json.dump(ru, f, ensure_ascii=False, indent=1)
    print('ru.json дополнен')

    for lang in ('az', 'en'):
        p = os.path.join(CONTENT, '%s.json' % lang)
        if not os.path.isfile(p):
            continue
        d = json.loads(io.open(p, encoding='utf-8').read())
        for core, key in added.items():
            d.setdefault(key, '')  # заполнить переводом позже
        with io.open(p, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        print('%s.json: добавлено пустых меток %d (нужен перевод)' % (lang, len(added)))


if __name__ == '__main__':
    main()
