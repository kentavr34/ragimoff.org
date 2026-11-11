"""ИЗВЛЕЧЕНИЕ ВСЕХ РЕПЛИК ВЛАДЕЛЬЦА ИЗ АРХИВА ЦНС.

ЗАЧЕМ. Владелец (11.11.2026): «вся история сайта, которая вообще не знаю
когда началась, должна быть доступна... вывести главные выводы, ключи,
какие инструменты можно использовать, на что обратить внимание, какие
элементы приветствуются, в чём заключается цель. Вывести из всех диалогов
контекст... и это уже будет ТЗ».

То есть требования нельзя восстанавливать по памяти — они лежат в переписке
и должны быть извлечены из неё дословно.

ОТКУДА. Архив ЦНС: /srv/cns/chats/<проект>/<дата>_<сессия>.jsonl
Формат строки: {project, session_id, date, turns: [{ts, role, text}, ...]}
Берём только role == "user" — это и есть реплики владельца.

Запуск:
    python _agent/cns_dialogs/extract.py
"""
import glob
import io
import json
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))

# Слова, по которым реплика относится к работе над сайтом.
# Список широкий намеренно: лучше взять лишнее и отсеять, чем потерять требование.
KEY = [
    'сайт', 'страниц', 'главн', 'шрифт', 'дизайн', 'блок', 'текст', 'заголов',
    'кнопк', 'меню', 'цвет', 'тем', 'мобильн', 'моушен', 'анимац', 'фото',
    'картинк', 'копирайт', 'цен', 'форм', 'регистрац', 'тренинг', 'консульт',
    'книг', 'обучен', 'program', 'hero', 'герой', 'html', 'css', 'верстк',
    'вёрстк', 'ragimoff', 'рагимов', 'рагимoff', 'шапк', 'подзаголов',
    'структур', 'последовательн', 'требован', 'макет', 'токен', 'стил',
]


def load_users():
    users = []
    for f in glob.glob(os.path.join(HERE, '*', '*.jsonl')):
        try:
            lines = io.open(f, encoding='utf-8', errors='ignore').read().splitlines()
        except Exception:
            continue
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            proj = d.get('project', '?')
            date = d.get('date', '')
            sid = d.get('session_id', '')
            for t in d.get('turns', []):
                if t.get('role') != 'user':
                    continue
                txt = (t.get('text') or '').strip()
                if txt:
                    users.append({'project': proj, 'date': date, 'session': sid, 'text': txt})
    return users


def main():
    users = load_users()
    print('ВСЕГО РЕПЛИК ВЛАДЕЛЬЦА: %d' % len(users))
    for k, v in Counter(u['project'] for u in users).most_common():
        print('  %-12s %d' % (k, v))

    site = [u for u in users if any(k in u['text'].lower() for k in KEY)]
    print()
    print('ОТНОСЯТСЯ К РАБОТЕ НАД САЙТОМ: %d' % len(site))
    print('СИМВОЛОВ В НИХ: %d' % sum(len(u['text']) for u in site))

    for name, data in (('_все_реплики.json', users), ('_реплики_о_сайте.json', site)):
        p = os.path.join(HERE, name)
        io.open(p, 'w', encoding='utf-8', newline='\n').write(
            json.dumps(data, ensure_ascii=False, indent=1))
        print('  сохранено: %s (%d записей)' % (name, len(data)))


if __name__ == '__main__':
    main()
