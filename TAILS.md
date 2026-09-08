# Хвосты — 2026-09-05 (список на завтра)

Задачи, где нужно решение Кенана или внешнее действие (публикация, доступы, ключи, внешние API).
Основной GEO-проход локально завершён, эти пункты его не блокируют. Возвращаемся отдельной сессией.

## 1. Публикация GEO-набора на прод
Коммит + push ветки `main` (remote: `github.com/kentavr34/ragimoff.org.git`).
В наборе ~178 файлов: обновлённые HTML всех трёх деревьев (AZ-корень / ru / en) со схемами
Schema.org (MedicalCondition, Article/BlogPosting, HowTo, Organisation, FAQPage),
`robots.txt` (ИИ-краулеры открыты), `geo_optimize.py`, `indexnow_submit.py`,
`indexnow_key.txt`, `llms.txt` (корень / en / ru).
Прод = GitHub Pages: страница станет публичной сразу после push.
В набор уже включены правки этой сессии: снят `noindex` с `ru/samira.html` и `en/samira.html`
(страница семейного терапевта индексируется во всех трёх языках; корень был снят ранее в Wave 1.4).

## 2. IndexNow — ✅ ЗАКРЫТО 2026-09-08
- Деплой выполнен (`2b1b9df`), ключ открылся: `https://ragimoff.org/indexnow_key.txt` → HTTP 200.
- `indexnow_submit.py` повторно запущен 2026-09-08: **api.indexnow.org 200, Bing 200, Yandex 200** —
  верификация пройдена, 403 `SiteVerificationNotCompleted` ушёл. WebSub (Google hub, Superfeedr) — 204 по всем URL.

## 3. Google Indexing API
- Не настроен (нет сервис-аккаунта в Google Cloud / Search Console).
- Решение: создавать аккаунт и пушить обновления через API, или положиться на sitemap + llms.txt + естественный обход.
- Решается после п.1–2.

## 4. Sitemap-пинги устарели — ✅ ЗАКРЫТО 2026-09-08
- Подтверждено прогоном: Google ping 404 (deprecated, googleblog 2023-06), Bing ping 410 Gone, Яндекс 200.
- Google/Bing убраны из `indexnow_submit.py` (остался только Яндекс); Google/Bing индексируют
  через sitemap + IndexNow (п.2 закрыт).

## 5. Review/Rating schema
- В `geo_optimize.py` тип Review для страниц услуг не добавлялся (xidmetler, программы и т.д.).
- Не блокирует деплой; расширить скрипт (тип `Review` + `aggregateRating`, без выдуманных цифр — только реальные) и прогнать.

## 6. Разобрать оставшиеся файлы (dev-артефакты)
- ✅ 2026-09-08 (Wave 1.6): `deploy-temp/`, `deploy-temp2`, `_wip_backup_20260906/` удалены — содержимое сломанного батча 06.09 доступно в `git stash@{0}`; страж `_hero_check.py` закоммичен.
- `rebuild_site_search_index.py`, `temp_index.html`, `temp_shared.js`, `check_samira.py`, `.commit_msg` — решить: влить / удалить / в `.gitignore`.
- `standardize_az.py`, `standardize_ru.py`, `standardize_en.py`, `geo_out.txt` — артефакты сессии 06.09, остались незакоммиченными: влить или удалить.
- ⚠️ `template.html` и `ru/template.html` **отслеживаются git и попадут на прод** при деплое (заголовок «Səhifə | RAGIMOFF», без JSON-LD). Решение: удалить из репо или добавить в `.gitignore` (проверено: в sitemap их нет, но на GitHub Pages они опубликуются).
- `gp.html` / `wc.html` — справочные копии (CBASP-мануал и др.), уже в `.gitignore` (коммит `a7eaa8c`) — НЕ трогать, не публикуются.

## 7. Реестры `archive/config`
- Просмотрены полностью: `pass.txt` (13 211 байт) и `api.txt` (28 180 байт) — других файлов-креденшалов в папке нет, есть только бэкапы/выгрузки.
- Состав и статусы зафиксированы; значения секретов никуда не выносились и в log не попадали.
- Отдельных решений на сегодня не требуется. При следующей работе с ключами — сверяться с этими двумя файлами как с источником истины.

## 8. Доводка SEO (не блокирует деплой)
- **og:locale / og:image / og:title / og:desc — готово на 100% живых страниц.** Аудит с order-agnostic регексом (порядок `property`/`content` не важен): lang 172/172, title 171/172, desc 170/172, canon 170/172, hreflang 165/172, og:locale 168/172, og:title 169/172, og:desc 169/172, og:image 167/172, jsonld 168/172. Все недостающие — только dev-артефакты (gp/wc/template/temp_index, см. п.6) или эталонный корень.
- `geo_optimize.py` получил функцию `normalize_og()`: добавляет недостающие `og:locale` (по `html lang`: az_AZ/ru_RU/en_US) и `og:image` (дефолтный), **кроме** эталонного корневого `index.html` (хард-правило). Прогон идемпотентен (0 изменений на повторном).
- Осталось по эталонному корню (только с разрешения владельца): `hreflang`-блок (3 линка по образцу `ru/index.html`) и `og:image` для `index.html`.
- Оставшиеся ISSUES аудита легитимны: `blog-klinik-psixiatriya.html` и `klinik-psixiatriya.html` одноязычны, `gp.html`/`wc.html` в `.gitignore`, `ru/template.html` — см. п.6.

## Порядок на завтра
1 → 2 (деплой + IndexNow) → затем 3–5 по готовности решений; п.6 — вместе с п.1.