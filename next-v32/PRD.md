# NEXT-V32 — PRD.md

> Product Requirements Document. Что конкретно строим, пошагово.
> Дата: 2026-09-14. Версия: v1.0.

---

## Принцип работы

- Каждый шаг = измеримый результат
- Каждый write → проверка (read / браузер)
- Если не могу проверить визуально — говорю честно
- Не изобретаю серверы / API-прокси / миграции
- Один шаг за раз, не распыляюсь
- Перед массовыми изменениями → эталон на одной странице
- Пользователь дал карт-бланш на качество и решения — действую автономно

---

## Фаза 0 — План и референсы ✅

**Что сделано**:
- [x] Разведка текущего сайта (структура, контент, темы)
- [x] Разведка `next-v32` (что было сделано предыдущим агентом)
- [x] Анализ референсов (jobtop.store, ragimoff.org, Awwwards 2026)
- [x] `DESIGN.md` — фундамент дизайна

**Deliverable**: `DESIGN.md` готов.

---

## Фаза 1 — Дизайн-система (tokens.css)

**Задачи**:
- [ ] Переписать `styles/tokens.css` с полной шкалой (fonts, colors, type-scale, spacing, motion, shadows, radii, layout)
- [ ] Создать `styles/layout.css` — grid, container, breakpoints, mobile-first
- [ ] Создать `styles/components.css` (переписать) — buttons, cards, nav, footer, metric, section
- [ ] Создать `styles/theme.css` — light/dark через `[data-theme]`
- [ ] Создать `styles/sections.css` — manifesto, directions, about, blog grid
- [ ] Создать `styles/books.css` (переписать) — book card с настоящими пропорциями

**Acceptance**:
- Все токены работают в `:root` и `[data-theme="dark"]`
- Тема переключается через `data-theme-toggle`
- Mobile breakpoint: 768px, 1024px

**Время**: ~1 час.

---

## Фаза 2 — Hero (5 слоёв + parallax + scroll-driven)

**Задачи**:
- [ ] Переписать `<section class="hero">` в `az/index.html` — 5 слоёв
- [ ] `styles/hero.css` — стили 5 слоёв, edge-to-edge
- [ ] `scripts/hero-parallax.js` — RAF-based parallax (5 скоростей)
- [ ] Текст манифест в hero с scroll-triggered reveal
- [ ] Метрики с counter-up при scroll (через `scripts/counter.js`)
- [ ] Scroll hint (анимированная стрелка)

**Acceptance**:
- Hero = 100vh, edge-to-edge
- 5 слоёв с разной скоростью работают при scroll
- Метрики считают 23+, 3000+, 300+, 11+ при попадании в viewport
- Текст появляется с stagger (badge → title → subtitle → CTAs → metrics → scroll hint)
- prefers-reduced-motion: parallax и counter отключаются

**Время**: ~2 часа.

---

## Фаза 3 — Секции (editorial layout)

**Задачи**:
- [ ] Manifesto — левая колонка (40%) + правая колонка лестница (60%)
- [ ] 3 направления — alternating full-bleed (Training, Services, B2B), НЕ карточки
- [ ] Профиль Kenan — большой портрет + био
- [ ] Витрина книг — magazine grid 2×2, с hover description
- [ ] Блог — magazine masonry grid
- [ ] CTA — тёмный блок с 3 кнопками
- [ ] Footer — 4 колонки

**Acceptance**:
- Layout не «лендинг из карточек», а editorial storytelling
- Scroll-triggered slide-in для направлений
- Hover на book-card: поднимается, показывает описание
- Все секции дышат (много воздуха, 96px section-y)

**Время**: ~3 часа.

---

## Фаза 4 — Темы light/dark

**Задачи**:
- [ ] Доделать `styles/theme.css` — все компоненты адаптируются под обе темы
- [ ] `scripts/theme.js` (переписать) — плавный transition при переключении
- [ ] Sun/Moon иконка в header — с micro-animation
- [ ] Default: prefers-color-scheme

**Acceptance**:
- Переключение без визуального «прыжка» (transition 220ms)
- Сохраняется в localStorage
- Работает prefers-color-scheme как default

**Время**: ~30 мин.

---

## Фаза 5 — Контент (тексты, 4 языка)

**Задачи**:
- [ ] Переписать ВСЕ тексты в `az/index.html` (без перевёртышей)
- [ ] Перевести `en/index.html` (EN)
- [ ] Перевести `ru/index.html` (RU)
- [ ] Hero heading / subtitle — привлекательные, editorial уровня
- [ ] Manifesto — крупный текст-голос бренда
- [ ] Описания 4 книг — настоящие, не сломанные
- [ ] Мета-описания, SEO-теги

**Hero heading варианты** (для обсуждения, склоняюсь к первому):
- AZ: «23 il — insanları eşidir, həyatları dəyişdirir»
- RU: «23 года — слышим людей, меняем жизни»
- EN: «23 years — listening to people, changing lives»
- TR: «23 yıl — insanları dinliyor, hayatları değiştiriyor»

**Manifesto текст** (пример):
- AZ: «Rezumelərə deyil, sənədlərə və həmkarların təsdiqinə inanırıq. Burada psixoloqu yalnız kağız deyil — sənədlər, həmkarlar və faktlar müəyyən edir. Sənin sözün, kollektiv təsdiqlə — etibarlı siqnal.»
- RU: «Мы верим не резюме, а документам и подтверждению коллег. Психолога здесь определяют не бумаги — а документы, коллеги и факты. Ваше слово, подкреплённое коллективной проверкой — надёжный сигнал.»
- EN: «We believe in documents and peer confirmation, not resumes. Here, a psychologist is defined not by a paper — but by documents, colleagues, and facts. Your word, backed by collective verification — a reliable signal.»

**Acceptance**:
- Все тексты — привлекательные, без перевёртышей
- Каждый язык — идиоматичный (не машинный перевод)
- 4 описания книг — настоящие

**Время**: ~2 часа.

---

## Фаза 6 — Анимации (GSAP ScrollTrigger + Lenis)

**Задачи**:
- [ ] `scripts/main.js` — init Lenis smooth scroll
- [ ] `scripts/scroll-anim.js` — GSAP ScrollTrigger для всех секций
- [ ] Hero parallax через RAF (НЕ GSAP — для перформанса)
- [ ] Counter-up для метрик через GSAP
- [ ] Slide-in для направлений
- [ ] Fade-in для manifesto, books, blog

**Acceptance**:
- Scroll smooth через Lenis
- ScrollTrigger работает на всех секциях
- Counter-up плавный (не дёрганый)
- prefers-reduced-motion: всё отключается

**Время**: ~2 часа.

---

## Фаза 7 — Полировка

**Задачи**:
- [ ] Mobile adaptation (320px — 1920px)
- [ ] Touch-friendly кнопки (min 44×44)
- [ ] Lazy-load для изображений
- [ ] Lighthouse Performance ≥ 90
- [ ] Lighthouse SEO = 100
- [ ] Lighthouse Accessibility ≥ 95
- [ ] Meta tags, Open Graph, Twitter cards
- [ ] Sitemap.xml, robots.txt
- [ ] 404.html
- [ ] GitHub Pages deploy

**Acceptance**:
- На мобиле hero = визуал без текста, текст под ним
- Lighthouse ≥ 90 / 100 / 95
- Сайт загружается < 1.5s на 3G
- Деплой работает на `ragimoff.org/next-v32/`

**Время**: ~1 час.

---

## Фаза 8 — Расширение (другие страницы)

**Только после Фазы 7**:
- [ ] `az/tehsil.html` (Образование)
- [ ] `az/xidmetler.html` (Услуги)
- [ ] `az/b2b.html`
- [ ] `az/blog.html` + 5 blog-страниц
- [ ] `az/haqqimda.html`
- [ ] `az/books/index.html` (витрина)
- [ ] `az/books/{phoenix-era, guilt-virus, pandemic-madness, clinical-psychiatry}.html`
- [ ] `az/klinik-psixiatriya/` — специальная страница-учебник

**Копирование EN/RU/TR**:
- [ ] После AZ готов — копировать структуру, переводить

**Время**: ~4 часа.

---

## Открытые вопросы для Kenan (по возможности — НЕ блокирую работу)

1. **Обложки книг**: использовать текущие CSS-градиенты или попробовать AI-сгенерировать? (Если есть рабочие API-ключи от Дашскопе — буду пробовать)
2. **Фото Kenan**: использовать `https://ragimoff.org/images/kenan/kenan-removebg-preview.png` или нужна другая версия?
4. **Предложение по цене книг**: оставить в манатах или добавить пересчёт в USD/EUR/RUB?

---

## Текущий статус

**Сделано**:
- DESIGN.md (v1.0)
- PRD.md (этот файл)
- Разведка завершена

**В работе**: Фаза 1 — Дизайн-система.

**Готово к старту**: Фаза 0 завершена.