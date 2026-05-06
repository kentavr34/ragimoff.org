# RAGIMOFF — Architecture & Development Guide

Многоязычный статический сайт (AZ / RU / EN) на чистом HTML + CSS + JS.
Хостинг: **GitHub Pages**, домен `ragimoff.org` (см. `CNAME`).
Деплой: `git push` в ветку `main`.

> Эта документация — для будущих агентов и разработчиков. Прочитай её ПЕРЕД любыми правками.

---

## Quick start

```bash
# Локальная разработка (любой статический сервер)
python -m http.server 5500

# После правки _partials/* или _i18n.json — обязательно:
python build.py

# Только одна страница
python build.py haqqimda.html
python build.py ru/blog.html

# Dry-run (что изменится, без записи)
python build.py --check

# Watch-режим (автопересборка при изменении партиалов)
python build.py --watch
```

---

## Критические правила

1. **`index.html` (корневой, AZ) — ЭТАЛОН.** НЕ менять без явного разрешения автора.
   `build.py` намеренно его пропускает (`SKIP_FILES`).
2. **`klinik-psixiatriya/`** — отдельная структура (книга), не трогать.
   `build.py` пропускает её через `SKIP_DIRS`.
3. **Перед массовыми правками** — создавай git tag-бэкап:
   ```bash
   git tag backup-before-<что-меняешь>
   git push --tags
   ```
4. **Никогда не push без коммита** — пользователь должен видеть изменения.
5. **Не редактируй блоки между `<!-- BEGIN: NAME -->` и `<!-- END: NAME -->` руками.**
   Они полностью перезаписываются при следующем `python build.py`.
   Правь шаблон в `_partials/NAME.html` или строки в `_i18n.json`.

---

## Файловая структура

```
sayt2/
├── index.html             ← AZ главная (ЭТАЛОН, не трогать)
├── *.html                 ← AZ страницы (~56 шт)
├── ru/*.html              ← RU переводы (~54 шт)
├── en/*.html              ← EN переводы (~53 шт)
├── klinik-psixiatriya/    ← отдельная книга (не трогать)
│
├── _partials/             ← шаблоны компонентов
│   ├── header.html
│   ├── mobile-nav.html
│   ├── footer.html
│   ├── hero-search.html
│   └── kitab-modal.html
├── _i18n.json             ← словарь переводов (az/ru/en)
├── build.py               ← рендерер
├── components.js          ← runtime injection (dev fallback, опционально)
│
├── gtc.css                ← основные стили
├── gtc-dark.css           ← dark theme overrides (Binance-inspired palette)
├── shared.js              ← общий JS (toggleMenu, toggleSubMenu, lang redirect)
├── js-hero-fit.js         ← binary-search font-fitting для page-hero-x
├── images/                ← статика
├── data/                  ← поисковый индекс и пр.
├── backend/               ← серверная часть (отдельно)
└── CNAME                  ← домен GitHub Pages
```

---

## Компонентная система

### Зачем
Раньше шапка / меню / подвал жили отдельной копией в каждом из ~160 HTML-файлов.
Любое изменение (например, новая ссылка в подменю) требовало править 160 мест.
Теперь — **одно место**: `_partials/header.html` + `_i18n.json`.

### Как это работает

В исходном HTML каждый компонент представлен парой:

```html
<!-- @include header -->
<!-- BEGIN: header (auto-generated, do not edit by hand) -->
<header class="site-header">
  ... сгенерированный HTML с правильным языком и активной вкладкой ...
</header>
<!-- END: header -->
```

* **`<!-- @include NAME -->`** — директива (ставится один раз вручную, потом не трогать).
* **`<!-- BEGIN: NAME -->...<!-- END: NAME -->`** — авто-генерируется `build.py`.
  Содержимое полностью перезаписывается при каждой пересборке.

Этот подход (рендер в исходник) выбран сознательно:
* GitHub Pages отдаёт готовый HTML — без JS-инъекций, без задержек, без проблем с SEO.
* Diff в git показывает реальные правки (видно, что именно поменялось в шапке).
* Не нужно поднимать build-сервер / dist-папку.

### Поддерживаемые компоненты

| Компонент       | Файл шаблона                        | Где используется                    |
|-----------------|-------------------------------------|--------------------------------------|
| `header`        | `_partials/header.html`             | Все страницы (десктоп шапка)         |
| `mobile-nav`    | `_partials/mobile-nav.html`         | Все страницы (мобильное меню)        |
| `footer`        | `_partials/footer.html`             | Все страницы                         |
| `hero-search`   | `_partials/hero-search.html`        | Hero-секции с поисковиком           |
| `kitab-modal`   | `_partials/kitab-modal.html`        | Все страницы (модалка заказа книги) |

### Подстановка переменных

В шаблонах используется синтаксис `{{var_name}}`. Источник значений:

1. **`_i18n.json`** — все строки (метки навигации, плейсхолдеры, надписи).
   Раздел выбирается автоматически по пути файла:
   * `/` (корень) → `az`
   * `/ru/...`    → `ru`
   * `/en/...`    → `en`
2. **Авто-вычисляемые** (в `build.py`):
   * `{{lang_switches}}`, `{{mobile_lang_switches}}` — переключатели языка
     с правильными относительными путями.
   * `{{cls_home}}`, `{{cls_tehsil}}`, `{{cls_xidmetler}}`, `{{cls_b2b}}`, `{{cls_blog}}` —
     добавляют `class="nav-active"` соответствующей вкладке.
     Активная вкладка определяется по basename файла (см. `ACTIVE_MAP` в `build.py`).
3. **Параметры директивы** — например:
   ```html
   <!-- @include hero-search placeholder="Тема, услуга..." -->
   ```
   Перебивают значения из i18n.

---

## Команды build.py

```bash
python build.py                  # рендер всех страниц (idempotent)
python build.py --check          # dry-run; код возврата 2 если есть что менять (для CI)
python build.py --watch          # рестарт при изменении _partials/ или _i18n.json
python build.py haqqimda.html    # одна страница
python build.py ru/blog.html     # одна страница в подпапке
python build.py --migrate        # legacy: превратить старые сырые блоки в @include
                                 #         (безопасно повторно — пропускает уже сделанное)
```

Что НЕ делает `build.py`:
* Не трогает `index.html` (корневой), `template.html`, `klinik-psixiatriya/`, `backend/`.
* Не модифицирует страницы БЕЗ директив `<!-- @include ... -->` —
  если хочешь оставить страницу полностью ручной, просто не ставь маркер.

---

## Common operations

### Изменить надпись в навигации
1. Открой `_i18n.json`.
2. Поменяй нужный ключ (`home`, `education`, `consultation` и т.д.) во всех трёх языках.
3. `python build.py`
4. Проверь diff, закоммить.

### Добавить ссылку в подменю
1. Открой `_partials/header.html` и `_partials/mobile-nav.html`.
2. Добавь `<li><a href="...">{{новый_ключ}}</a></li>` (или `<a>` для mobile).
3. Добавь `новый_ключ` в `_i18n.json` для AZ/RU/EN.
4. `python build.py`

### Добавить ссылку в footer
1. Открой `_partials/footer.html`.
2. Добавь `<li>` в нужную колонку.
3. Если нужны переводы — добавь ключ в `_i18n.json`.
4. `python build.py`

### Создать новую страницу
1. Скопируй похожую существующую (например `enurez.html` → `panik-2.html`).
2. Поменяй контент между `<!-- END: header -->` и `<!-- @include footer -->`.
3. Поменяй `<title>`, `<meta description>`, `<meta og:*>`.
4. Создай аналоги в `ru/` и `en/`.
5. Если новая страница должна подсвечиваться в навигации — добавь её
   в `ACTIVE_MAP` в `build.py`.
6. `python build.py`

### Добавить новый язык (например, `tr`)
1. Создай папку `tr/` и копии страниц туда.
2. Добавь раздел `"tr": { ... }` в `_i18n.json` со всеми ключами.
3. В `build.py`:
   * Добавь `"tr": "tr"` в `LANG_DIRS`.
   * В функции `lang_switches()` расширь список языков и подкорректируй пути.
4. `python build.py`

### Добавить новый компонент (например, `breadcrumb`)
1. Создай `_partials/breadcrumb.html` с шаблоном (используй `{{var}}`).
2. Добавь нужные ключи в `_i18n.json`.
3. На странице, где он нужен, поставь `<!-- @include breadcrumb -->`.
4. `python build.py` — `BEGIN/END` блок появится автоматически.

---

## Page Hero System (`.page-hero-x`)

Стиль шапки внутренних страниц. Реализовано в `gtc.css` + `js-hero-fit.js`.

```html
<section class="page-hero-x" data-theme="dark"
  style="background-image:url('PATH');"
  aria-labelledby="page-h1">
  <div class="page-hero-x-inner">
    <span class="ph-badge">КАТЕГОРИЯ</span>
    <h1 class="ph-h1" id="page-h1">
      <span class="ph-h1-w1">Слово1</span>
      <span class="ph-h1-w2">Слово2</span>
    </h1>
    <p class="ph-sub">
      <span class="ph-sub-mob">мобильная строка 1</span>
      <span class="ph-sub-mob">мобильная строка 2</span>
      <span class="ph-sub-mob">мобильная строка 3</span>
      <span class="ph-sub-desk">десктоп строка 1</span>
      <span class="ph-sub-desk">десктоп строка 2</span>
    </p>
    <!-- @include hero-search -->
  </div>
</section>
```

**Правила:**
* Все 3 строки (H1 + 2 десктоп-сабтайтла) выравниваются по ширине поисковика (620 px) через binary-search font-fitting.
* На мобайле — 3 строки сабтайтла, центрированы. **Подзаголовок ≤ 2 строк на десктопе, обе одинаковой длины.** Если получилось 3+ строк — переписать.
* Background-image — опционально.

---

## Дизайн-система

### Палитра (`gtc-dark.css`)
* `--bnb-bg: #0B0E11` — фон
* `--bnb-surface: #1E2026` — карточки
* `--bnb-gold: #E6B44A` — акцент
* `--bnb-text: #EAECEF` — основной текст

### Hero на главной (index.html)
* Фото `kenan-removebg-preview.png`: `height: 380px`, `object-fit: cover`, прижато к низу полоски.

### Footer Address
* 2 строки с `<br/>`.
* Кликабельный, открывает Google Maps.
* Свой золотой border + hover.

---

## История версий и бэкапы

```bash
# Список бэкап-тегов
git tag -l 'backup-*'

# Откатиться на бэкап
git checkout backup-before-components-system

# Сравнить с бэкапом
git diff backup-before-components-system -- '*.html'
```

Текущий бэкап перед внедрением компонентной системы:
**`backup-before-components-system`** (запушен в origin).

---

## TODO / Known issues

* [ ] Ru/En страницы пока используют `KİTABIN SİFARİŞİ` модалку
      (общий компонент). Если решите вернуть `ЗАПИСЬ` → `tehsil.html#registration` —
      пропишите в `_partials/header.html` условный блок (через {{var}}).
* [ ] `klinik-psixiatriya/` — отдельная подсистема, своя шапка / навигация.
      Не интегрирована (по дизайну).

---

## English summary (for AI agents)

This is a multilingual static site (AZ / RU / EN) hosted on GitHub Pages
under `ragimoff.org`.

**Component system.** Header, mobile nav, footer, hero-search and kitab-modal
live in `_partials/*.html` with `{{variable}}` placeholders. Strings are in
`_i18n.json` (sections `az`, `ru`, `en`). The renderer is `build.py` (Python 3).

**How rendering works.** Source HTML files contain pairs:

```html
<!-- @include NAME -->
<!-- BEGIN: NAME (auto-generated, do not edit by hand) -->
... rendered HTML ...
<!-- END: NAME -->
```

`build.py` walks all `.html` files (skipping `index.html`,
`klinik-psixiatriya/`, `backend/`, `template.html`), detects the language
from the path (`/`, `/ru/`, `/en/`), determines the active nav tab from the
filename (`ACTIVE_MAP`), then rewrites every `BEGIN/END` block in place.

After editing any partial or i18n string, ALWAYS run `python build.py` and
commit the resulting changes.

**Critical:** `index.html` (root, AZ) is the design etalon and is never
touched by the build. The `klinik-psixiatriya/` book has its own structure
and is also excluded.

**Page hero system.** `.page-hero-x` uses binary-search font-fitting
(`js-hero-fit.js`) so badge / H1 / subtitle / search bar all align to the
search bar width (620px desktop). Mobile shows 3 subtitle lines, desktop
shows 2 (equal length).

**To add a language:** add a section in `_i18n.json`, extend `LANG_DIRS` and
`lang_switches()` in `build.py`, create the language directory with HTML files.

**To add a component:** create `_partials/NAME.html`, place
`<!-- @include NAME -->` markers on pages, run `python build.py`.
