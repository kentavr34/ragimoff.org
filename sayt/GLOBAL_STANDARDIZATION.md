# Ragimoff Portal: Global Standardization Rollout

## ШАБЛОН: index.html — НЕПРИКОСНОВЕНЕН
> Дата фиксации: 2026-04-14. Страница завершена и утверждена как эталон.
> **Запрещено менять стили, структуру секций и компоненты index.html без явного разрешения автора.**

---

## Архитектура шаблона (index.html)

### Порядок секций
1. `<header>` — фиксированный, navy фон, логотип + nav + CTA
2. `<nav class="mobile-nav">` — мобильное меню
3. `.hub-hero` — Hero: сетка `1fr 360px`, фото 342×400px
4. `.stats-strip` — полоса статистики (4 показателя)
5. `.eco-section` — 3 eco-карточки (3 направления)
6. `.about-sec` — О специалисте: таймлайн + фото + галерея дипломов
7. `#services .svc-mini` — 6 карточек услуг + кнопка "Bütün Xidmətlər"
8. `<footer>` — 4 колонки: бренд / тerapiya / təhsil / əlaqə
9. `.wa-float` — WhatsApp плавающая кнопка

---

## Цветовые токены (из shared.css :root — единственный источник правды)

| Токен | Значение | Назначение |
|---|---|---|
| `--navy` | `#061826` | Фон hero, header, footer, тёмные панели |
| `--blue` | `#0a2540` | Вторичный тёмный фон |
| `--accent` | `#b59b72` | Золото — акцент, кнопки, метки |
| `--gold` | `#d4af37` | Hover-состояние кнопок |
| `--light` | `#f8f9fa` | Светлый фон секций |
| `--white` | `#ffffff` | Фон карточек, текст на тёмном |
| `--text` | `#061826` | Основной текст |
| `--gray` | `#4a5568` | Вторичный текст, описания |
| `--border` | `#e2e8f0` | Границы |

---

## Типографика (Major Third ×1.25)

| Токен | px | Назначение |
|---|---|---|
| `--text-xs` | 12px | Метки, eco-label, footer-heading |
| `--text-sm` | 14px | Карточки body, nav links |
| `--text-base` | 16px | Основной текст |
| `--text-lg` | 18px | Карточки h4 |
| `--text-xl` | 20px | Подзаголовки, about-lead |
| `--text-2xl` | 25px | h4 в панелях |
| `--text-3xl` | 30px | h3 |
| `--text-4xl` | 36px | Section h2 |
| `--text-5xl` | 45px | Hero h2 |
| `--text-6xl` | 56px | Page h1 (один на странице) |

Шрифты: **Inter** (заголовки) + **Manrope** (body)

---

## Ритм секций (строгий стандарт)

```
[Метка .tag-premium]   margin-bottom: 25px  ← Premium Master Gap
[Заголовок h2]         margin-bottom: 16px  ← Title density
[Подзаголовок .eco-subtitle] margin-bottom: 55px ← Master Gap to content
[Контент / сетка]
```

- Отступ сверху секции: **55px** (Master Gutter)
- Горизонтальный padding всех секций: **55px** (Master Gutter)
- На мобиле (≤768px): padding **24px**

---

## Компоненты шаблона

### `.tag-premium` (метка секции)
```css
border: 1px solid rgba(181,155,114,0.4);
background: rgba(181,155,114,0.06);
color: var(--accent);
font-size: var(--text-xs);
font-weight: 700;
padding: 8px 16px;
border-radius: 0 !important;
text-transform: uppercase;
letter-spacing: 0.1em;
margin-bottom: 25px; /* СТАНДАРТ */
```
Вариант `.tag-premium.dark-text` — для светлых секций (navy цвет текста).

### `.eco-card` (карточка направления)
- `border-top: 4px solid var(--navy)` в обычном состоянии
- `border-top: 4px solid var(--accent)` + `::before scaleX(1)` для `.gold-border`
- hover: `translateY(-8px)`, акцентная верхняя полоса
- Структура: `.eco-label` → `h3` → `p` → `.eco-link`

### `.svc-card` (карточка услуги)
- Белый фон, `border: 1px solid var(--border)`
- hover: accent border + `translateY(-4px)`
- `.svc-card-active` — выделенная карточка (золотой фон)
- Структура: `.eco-label` → `h4` → `p`

### `.stats-strip` (полоса статистики)
- Фон: `var(--navy)`, border top/bottom: `rgba(181,155,114,0.15)`
- 4 колонки: цифра (accent, 2.25rem, Inter 800) + метка (белый 45%, 0.7rem)
- Разделители: `1px solid rgba(181,155,114,0.15)`

### `.gallery-1` + `.gallery-band` (галерея дипломов)
- `.gallery-band`: navy полоса на `100vw`, full-bleed
- Слайды: transparent фон, без рамок
- `object-fit: contain` — дипломы отображаются целиком
- 3 активных слайда видны, остальные — узкие полоски справа
- Клик → lightbox через `openGalleryStage()` из shared.js

### Кнопки
| Класс | Состояние | Hover |
|---|---|---|
| `.btn-primary` | accent bg, navy text | gold bg |
| `.btn-outline` | transparent, accent border | accent bg 15% |
| `.btn-navy` | navy bg, white text | blue bg |
| `.nav-cta` | accent bg, navy text | gold bg |

### Header
- `position: fixed`, height: 96px, blur(20px)
- Логотип: `RAGIMOFF.` + `Psixologiya Məktəbi`
- Nav: Ana Səhifə / Təhsil / Korporativ / Blog / QEYDİYYAT (CTA)
- Мобильный toggle: `toggleMenu()` → `.mobile-nav.open`

### Footer (4 колонки: `2fr 1fr 1fr 1fr`, gap 64px)
- Колонка 1 (бренд): логотип + описание + соцсети (TG/FB/IG/YT)
- Колонка 2 (Terapiya): Ailə / Enurez / Panik / Depressiya / Sosial Fobiya
- Колонка 3 (Təhsil): Ümumi Psixologiya / Klinik DPO / Praktikum / Blog / YouTube
- Колонка 4 (Əlaqə): телефон / email / WhatsApp / Telegram / Instagram

---

## Правила для всех остальных страниц

1. **Копировать `<header>` и `<footer>` из index.html без изменений**
2. **Не переопределять** `.tag-premium`, `.btn-*`, `.eco-card`, `.svc-card` глобально
3. Страничные стили — только в `<style>` внутри `<head>` страницы
4. Все spacing через `var(--space-X)`, не px напрямую
5. `border-radius: 0 !important` везде — скругления запрещены
6. Без emoji в контенте и коде

---

## Статус страниц

| Страница | Статус | Приоритет |
|---|---|---|
| `index.html` | ШАБЛОН — завершён 2026-04-14 | — |
| `haqqimda.html` | В работе | 1 |
| `tehsil.html` | Требует переработки контента | 2 |
| `qanunlar.html` | Связана с tehsil.html | 2 |
| `xidmetler.html` | Требует наполнения | 3 |
| `aile-terapiyasi.html` | Добавить блок блога | 4 |
| `aile-terapiyasi-usaq.html` | Добавить блок блога | 4 |
| `depressiya.html` | Добавить блок блога | 4 |
| `enurez.html` | Добавить блок блога | 4 |
| `panik-ataklar.html` | Добавить блок блога | 4 |
| `sosial-fobiya.html` | Добавить блок блога | 4 |
| `b2b.html` | Направления + форма | 5 |
| `blog.html` + посты | Проверить единообразие | 6 |

---

## Что хранится в shared.css (трогать осторожно)

- `:root {}` — все CSS-токены
- `header`, `.logo-*`, `nav.desktop-nav`, `.mobile-nav` — навигация
- `.btn`, `.btn-primary`, `.btn-outline`, `.btn-navy`, `.btn-wa` — кнопки
- `.eco-card`, `.eco-label`, `.eco-link` — карточки направлений
- `.svc-card`, `.svc-card-active` — карточки услуг
- `.about-inner`, `.about-img-wrap`, `.timeline-list` — блок "О специалисте"
- `.gallery-1`, `.gallery-1-stage`, `.stage-nav` — галерея + lightbox
- `.card-premium` — универсальная премиум-карточка
- `footer`, `.footer-grid`, `.footer-links` — футер
- `.wa-float` — WhatsApp кнопка
- `.modal-overlay` — модальные окна
- `.fi` — fade-in анимация при скролле

## Что хранится в shared.js (трогать осторожно)

- `toggleMenu()` / `closeMenu()` — мобильное меню
- `initGalleryOne(id)` — инициализация галереи слайдов
- `openGalleryStage(src, collection)` — lightbox для дипломов
- `navigateStage(dir)` / `closeGalleryStage()` — навигация lightbox
- `DOMContentLoaded` — авто-инициализация галерей и аккордеонов
