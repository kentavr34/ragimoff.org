# LightRAG Integration для ragimoff.org

## Статус подключения

✅ **Проект успешно зарегистрирован в LightRAG**

- **API Key**: `chesscoin_rag_secret_2026`
- **Direct URL**: `http://185.203.116.131:9622`
- **Proxy URL**: `https://chesscoin.app/lightrag/`
- **WebUI**: `https://chesscoin.app/rag/`
- **Project ID**: `ragimoff_site_2026`
- **Project Label**: `ragimoff.org`

---

## Использование

### 1. Логирование новой функции

```python
from lightrag_client import RagimoffLightRAGClient

client = RagimoffLightRAGClient()

client.log_feature(
    name='Mobile Menu Fix',
    description='Fixed mobile navigation menu behavior on index.html',
    files=['index.html', 'shared.js']
)
```

### 2. Логирование исправления ошибки

```python
client.log_bugfix(
    issue='Hero section image breaking on mobile',
    fix='Added object-fit: cover and proper aspect-ratio to hero image',
    files=['index.html', 'shared.css']
)
```

### 3. Логирование дизайн-обновления

```python
client.log_design_update(
    update='Unified spacing system to 8px grid',
    components=['shared.css', 'all HTML pages']
)
```

### 4. Проверка соединения

```python
if client.test_connection():
    print("Connected to LightRAG!")
else:
    print("Connection failed")
```

---

## Командная строка

Используйте скрипт `log_changes.py` для быстрого логирования из командной строки:

```bash
# Логировать новую функцию
python log_changes.py feature "Mobile menu fix" --files index.html,shared.js

# Логировать исправление
python log_changes.py bugfix "Fixed hero image on mobile" --files index.html

# Логировать дизайн-обновление
python log_changes.py design "Unified 8px spacing grid"

# Логировать документацию
python log_changes.py docs "Updated DESIGN_MASTERPLAN.md"
```

---

## Просмотр истории

Откройте WebUI для просмотра всех логированных изменений:
**https://chesscoin.app/rag/**

---

## Структура LightRAG

### Endpoint: `/insert/{project_id}`

Для логирования изменений отправляйте POST запрос с формате:

```json
{
  "text": "Описание изменения",
  "nodes": [
    {
      "id": "уникальный_id",
      "label": "Название",
      "type": "тип_узла",
      "properties": {
        "key": "value"
      }
    }
  ],
  "edges": [
    {
      "source": "узел1",
      "target": "узел2",
      "type": "тип_связи"
    }
  ]
}
```

### Headers

```
X-API-Key: chesscoin_rag_secret_2026
Content-Type: application/json
```

---

## Типы изменений (change_type)

- **feature** - новая функция
- **bugfix** - исправление ошибки
- **refactor** - рефакторинг кода
- **design** - дизайн-обновление
- **docs** - обновление документации

---

## Примеры интеграции в рабочий процесс

### После каждого коммита

```bash
# Логировать изменения после git commit
git commit -m "Fix mobile menu"
python log_changes.py feature "Mobile menu fix" --files index.html shared.js
```

### Перед деплоем

```bash
# Логировать готовность к деплою
python log_changes.py feature "Deployment v2.0" --files index.html tehsil.html
```

### Документирование багов

```bash
python log_changes.py bugfix "Hero section responsive" --files index.html shared.css
```

---

## Мониторинг

Все изменения автоматически:
- Отправляются в LightRAG
- Получают уникальный Track ID
- Сохраняются с меткой времени (ISO 8601)
- Связываются с файлами проекта

---

## Альтернативные способы отправки

### cURL

```bash
curl -X POST http://185.203.116.131:9622/insert/ragimoff_site_2026 \
  -H "X-API-Key: chesscoin_rag_secret_2026" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Feature: Mobile menu fix",
    "nodes": [{"id": "change1", "label": "Mobile menu fix"}]
  }'
```

### Python requests

```python
import requests

response = requests.post(
    'http://185.203.116.131:9622/insert/ragimoff_site_2026',
    headers={'X-API-Key': 'chesscoin_rag_secret_2026'},
    json={
        'text': 'Feature: Mobile menu fix',
        'nodes': [{'id': 'change1', 'label': 'Mobile menu fix'}]
    }
)
```

---

## Troubleshooting

### Ошибка: "Invalid token"

- Проверьте, что API Key правильный
- Убедитесь, что используется заголовок `X-API-Key`, а не `Authorization`

### Ошибка: 404 Not Found

- Проверьте URL (должен содержать `/insert/{project_id}`)
- Project ID должен быть `ragimoff_site_2026`

### Ошибка: "Field required: text"

- Обязательно включите поле `text` в тело запроса
- `text` содержит описание изменения

---

## Информация о проекте

- **Название**: ragimoff.org
- **Тип**: Static HTML/CSS/JS website
- **Статус**: Active
- **Деплой**: Netlify
- **Дизайн-система**: Mobile-first, Playfair+Lato, Navy+Gold palette
- **Страницы**: 25+ (блог, услуги, образование, дипломы)

---

Для вопросов или проблем обратитесь к системному администратору.
