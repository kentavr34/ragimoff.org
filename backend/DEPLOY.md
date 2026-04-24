# Apps Script Deploy — 2 минуты

## Шаг 1. Открыть редактор
1. Откройте [таблицу](https://docs.google.com/spreadsheets/d/1ucYNu6mjcDzUE1g4rVIQi__56qUhaMjcG9r0JorV2rI/edit)
2. Верхнее меню → **Extensions → Apps Script**
3. В открывшемся редакторе удалите всё в `Code.gs`
4. Вставьте содержимое `backend/apps-script.gs`
5. Ctrl+S (сохранить), название проекта: `RAGIMOFF Backend`

## Шаг 2. Deploy как Web App
1. Справа вверху → кнопка **Deploy → New deployment**
2. Шестерёнка ⚙️ слева → выбрать **Web app**
3. Заполнить:
   - Description: `ragimoff-backend-v1`
   - Execute as: **Me (ваш email)**
   - Who has access: **Anyone**
4. Кнопка **Deploy**
5. Первый раз попросит авторизацию → Advanced → Go to (unsafe) → Allow
6. Скопируйте **Web app URL** (заканчивается на `/exec`)

## Шаг 3. Отдайте мне URL
Пришлите сюда URL вида:
```
https://script.google.com/macros/s/AKfyc.../exec
```

Дальше я сам:
- подключу обе формы сайта (регистрация + отзывы)
- протестирую через preview
- закоммичу

## Проверка без сайта (опционально)
Откройте URL в браузере — должно показать:
```json
{"ok":true,"service":"ragimoff-backend"}
```
