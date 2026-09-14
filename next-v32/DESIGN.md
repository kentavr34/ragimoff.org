# NEXT-V32 — DESIGN.md

> Фундамент дизайна. Все решения по стилю, типографике, цвету, композиции и анимации — здесь.
> Дата создания: 2026-09-14. Версия: v1.0.

---

## 1. Цель

Полностью рабочий статический сайт в `D:/Документы/ragimoff/next-v32/`, который:

- **Лучше текущего сайта во всём**, в первую очередь в дизайне
- 3 языка сайта: az / ru / en
- 4 языка книги «Клиническая Психиатрия»: az / ru / en / tr
- Общая галерея книг — витрина для онлайн-покупок (4 книги × 4 языка описания)
- Переключатель светлой / тёмной темы
- Scroll-анимации в hero главной страницы и на главных страницах разделов
- **НЕ** на страницах книг внутри книжного магазина (там — спокойно, для чтения)
- Мобильная адаптация
- Деплой на `ragimoff.org/next-v32/` через GitHub Pages

**Текущий сайт (D:/Документы/ragimoff/) — НЕ ТРОГАТЬ**. Админка, формы, Telegram-бот остаются на старом.

## 2. Аудитория

- AZ: психолог-профессионал, ищущий лицензированное обучение / практику
- TR/RU: иммигранты в TR ищущие понятную информацию о психологической помощи
- EN: международные партнёры (IPAS, BAPPs, ADA), представители академии
- Конечные клиенты: семьи, пары, родители — ищут профессиональную помощь

Все сегменты требуют **доверия и серьёзности**. Это не развлекательный сайт — это визитная карточка клиники.

## 3. Референсы и что из них берём

### 3.1. jobtop.store

**Берём:**
- Плотный минимализм, чистая типографика, много воздуха
- Манифест-блок — крупный текст-манифест как «голос бренда»
- Карточки-метрики с крупными цифрами
- Лестница доверия (шаги подтверждения) — левая колонка + правая колонка
- Editorial-стиль, читается как серьёзное издание

### 3.2. ragimoff.org (текущий)

**Сохраняем:**
- Тёмный hero с золотым акцентом — это фирменный цвет Kenan
- Золотой #D4A843 — основной accent (тёплый, аристократичный)
- Структура секций: 3 направления → профиль Kenan → книги → блог → CTA
- Метрики 23+ / 3000+ / 300+ / 11+ — мощный социальный сигнал
- Структура книг: Phoenix Era, Guilt Virus, Pandemic of Madness, Clinical Psychiatry

**Что улучшаем:**
- Hero — с 1-слойного на 5-слойный parallax
- Карточки книг — с CSS-градиентов на реальные обложки
- Тексты книг — с перевёрнутых описаний на настоящие
- Анимации — с базовых hover на scroll-driven storytelling

### 3.3. Awwwards SOTD 2026 (дополнительно)

**Берём паттерны:**
- **Porsche Motorsport scrollytelling** — единый непрерывный мир, не «лендинг из секций»
- **Active Theory** — 3D / canvas для hero (но мы пока без 3D, через CSS + parallax)
- **Locomotive Cinema** — typography-led, smooth scroll
- **Hon Tran 3P rule** — Art Direction + Directed Motion + Performance
- **Hon Tran «Hostage Hero»** — pinned scroll-scrubbed hero

**Используем техники:**
- 5-слойный parallax в hero (bg → atmosphere → floor → action → text)
- GSAP ScrollTrigger через CDN (для scroll-driven)
- Lenis smooth scroll через CDN
- IntersectionObserver как fallback для prefers-reduced-motion

## 4. Дизайн-система (фундамент)

### 4.1. Шрифты (Pentagram правило: max 3 шрифта)

```
Display (заголовки, hero, манифест):
  Cormorant Garamond — serif, элегантный, editorial
  weights: 400 / 500 / 600 / 700
  italic: для акцентов в манифесте

Body (текст, навигация, описания):
  Inter — sans-serif, читабельный, современный
  weights: 300 / 400 / 500 / 600 / 700

Mono (только для метрик / ISBN / дат):
  JetBrains Mono — моноширинный, технический акцент
  weights: 400 / 700
```

Загрузка: Google Fonts CDN с `preconnect` (уже есть).

### 4.2. Палитра

**Light theme** (основная — тёплая, paper-like):
```css
--bg-canvas:        #F5F3EF;  /* основной фон — тёплый бежевый */
--bg-surface:       #FFFFFF;  /* карточки, hover */
--bg-surface-2:     #FAF7F1;  /* второстепенный */
--ink-primary:      #1A1A2E;  /* основной текст — глубокий тёмно-синий */
--ink-secondary:    #6B6B7B;  /* второстепенный текст */
--ink-muted:        #9A9AAA;  /* captions */
--accent-gold:      #B8860B;  /* основной золотой (DarkGoldenrod) */
--accent-gold-hot:  #D4A843;  /* hover / hero */
--accent-gold-soft: #F3E8C8;  /* фон для золотых карточек */
--border:           #E8E4DD;  /* границы, тонкие линии */
--border-strong:    #D4CFC4;
--success:          #10a37f;
--warn:             #F5A623;
--danger:           #EF4146;
```

**Dark theme** (hero и акценты):
```css
--bg-canvas:        #0D0D12;  /* основной тёмный */
--bg-surface:       #1A1A24;  /* карточки */
--bg-surface-2:     #111118;  /* глубже */
--ink-primary:      #E8E4DD;  /* светлый текст */
--ink-secondary:    #B0B0BA;  /* второстепенный */
--ink-muted:        #76767A;
--accent-gold:      #D4A843;  /* золотой — основной в тёмной */
--accent-gold-hot:  #F5E6B8;  /* hover */
--accent-gold-soft: #2A2518;  /* тёмный золотой фон */
--border:           #2A2A35;
```

**Почему тёплый бежевый + золотой**: психология, доверие, человечность. Холодный синий = корпоративный, generic. Тёплый бежевый = бумага, книга, мастерская. Золотой = премиальность, медицина (латинская «aurum»), экспертиза.

### 4.3. Шкала типов (модулярная, 1.333 ratio на 18px)

```css
--fs-xs:    0.694rem;  /* 12.5px — captions */
--fs-sm:    0.833rem;  /* 15px   — small body */
--fs-base:  1rem;      /* 18px   — body */
--fs-md:    1.333rem;  /* 24px   — large body */
--fs-lg:    1.777rem;  /* 32px   — small heading */
--fs-xl:    2.369rem;  /* 42.6px — h3 */
--fs-2xl:   3.157rem;  /* 56.8px — h2 */
--fs-3xl:   4.209rem;  /* 75.8px — h1 */
--fs-4xl:   5.61rem;   /* 101px  — hero display */
--fs-5xl:   7.48rem;   /* 134px  — hero statement */
```

Line heights:
```css
--lh-display:  0.86;   /* hero headings */
--lh-heading:  1.05;   /* h2, h3 */
--lh-body:     1.55;   /* body */
--lh-tight:    1.2;    /* captions */
```

### 4.4. Spacing (4px doubling, Pentagram)

```css
--sp-1: 4px;
--sp-2: 8px;
--sp-3: 16px;
--sp-4: 24px;
--sp-5: 48px;
--sp-6: 96px;
--sp-7: 144px;
--sp-8: 192px;
--section-y: 96px;
--container-gutter: 48px;
```

### 4.5. Motion (OpenAI Design System)

```css
--motion-instant: 100ms;
--motion-fast:    150ms;   /* hovers */
--motion-base:    220ms;   /* transitions */
--motion-slow:    360ms;   /* entrances */
--motion-deliberate: 520ms; /* hero elements */
--ease-standard:  cubic-bezier(0.16, 1, 0.3, 1);
--ease-emphasis:  cubic-bezier(0.7, 0, 0.3, 1);
--ease-exit:      cubic-bezier(0.7, 0, 0.84, 0);
```

### 4.6. Layout

```css
--max-w:          1680px;
--container-max:  1280px;     /* основной контент */
--container-narrow: 880px;    /* текст манифеста */
--nav-h:          72px;
--rail:           56px;
```

### 4.7. Border radius

```css
--radius-sm: 4px;
--radius-md: 8px;
--radius-lg: 12px;
--radius-xl: 20px;
--radius-2xl: 28px;
--radius-pill: 999px;
```

### 4.8. Shadows

```css
--shadow-sm: 0 1px 3px rgba(26,26,46,0.06);
--shadow-md: 0 4px 12px rgba(26,26,46,0.08);
--shadow-lg: 0 16px 48px rgba(26,26,46,0.12);
--shadow-glow: 0 0 32px rgba(212,168,67,0.18);  /* золотое свечение для CTA */
```

## 5. Композиция Hero (5 слоёв, edge-to-edge)

```
.hero [100vh, edge-to-edge, no border]
├── hero-layer-bg       [parallax 0.12]  — фото Kenan (портрет)
├── hero-layer-atmos    [parallax 0.28]  — золотые частицы (canvas)
├── hero-layer-floor    [parallax 0.42]  — градиент снизу
├── hero-layer-action   [parallax 0.62]  — текст манифест
└── hero-layer-fg        [parallax 0.88]  — CTA, метрики, scroll hint
```

**Текст в hero**:
- Eyebrow: «IPAS Ambassador · BAPPs · ADA» (золотой, uppercase, letter-spacing 0.12em)
- Heading: «23 il — insanları eşidirir, həyatları dəyişdirir» (короман гарамонд, 134px)
- Subheading: «Klinik psixologiya, təhsil və B2B» (inter, 32px)
- CTA: 2 кнопки (Call, Books)
- Metrics row: 23+ / 3000+ / 300+ / 11+ (с counting animation при scroll)
- Scroll hint: анимированная стрелка вниз (только в light theme, в dark — без)

## 6. Композиция секций (editorial, не лендинг)

### 6.1. Манифест (Manifesto)
- Левая колонка (40%): eyebrow + крупный текст-манифест (50–80 слов)
- Правая колонка (60%): лестница доверия (3 шага, вертикально)
- Разделитель — тонкая золотая линия

### 6.2. 3 направления (Training / Services / B2B)
- НЕ карточки в ряд. Чередующиеся full-bleed секции:
  - Чётные: текст слева + изображение справа
  - Нечётные: изображение слева + текст справа
- Scroll-triggered slide-in (slide-left / slide-right)

### 6.3. Профиль Kenan
- Большой портрет слева (Kenan-removebg-preview.png с обработкой)
- Справа: имя, достижения, список, CTA
- Под портретом — бейджи (IPAS, BAPPs, ADA)

### 6.4. Витрина книг
- **Без реальных обложек** (или с AI-сгенерированными, если ключи заработают)
- 4 книги, magazine grid (2×2)
- Каждая карточка: обложка + название + категория + цена + кнопка
- Hover: поднимается, показывает описание

### 6.5. Блог (magazine grid)
- 3 карточки, masonry-style
- Каждая: миниатюра + тег + заголовок + дата + excerpt

### 6.6. CTA (контакты)
- Тёмный фон, золотой акцент
- 3 кнопки: телефон, Telegram, WhatsApp
- Цитата / manifesto финал

### 6.7. Footer
- 4 колонки: лого + контакты / Training / Services / Books
- Copyright + языковой переключатель

## 7. Анимации (12 Disney principles + GSAP)

| Принцип | Где применяем |
|---|---|
| Squash & Stretch | Hero scale-in при загрузке (h1 чуть-чуть сжимается-разжимается) |
| Anticipation | CTA-кнопки — slight pull-back перед hover |
| Staging | Hero — 5 слоёв с разной скоростью |
| Follow Through | Метрики — counter не замирает, digits слегка покачиваются |
| Slow In / Slow Out | Все переходы — ease-curve, не linear |
| Arc | Scroll-driven элементы по дуге (не по прямой) |
| Secondary Action | Counter-up метрик при scroll |
| Timing | Hero stagger: badge → title → subtitle → CTAs → metrics → scroll hint |
| Exaggeration | Hover на book-card: scale 1.03, shadow deeper |
| Appeal | Editorial layout с большим воздухом |
| Drawing | Scroll-pinned hero — текст появляется как-будто рисуется |
| Personality | Kenan portrait с лёгким subtle hover-эффектом |

## 8. Технический стек

- **Статика**: HTML5 + CSS3 + vanilla JS (ES2020)
- **Без билда**: никаких webpack/vite/next
- **CDN libs**:
  - GSAP 3.13+ (gsap.com) — `https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js`
  - ScrollTrigger — `https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/ScrollTrigger.min.js`
  - Lenis — `https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js`
- **Шрифты**: Google Fonts CDN (preconnect)
- **Изображения**: оптимизированный WebP, lazy-load
- **Деплой**: GitHub Pages → `ragimoff.org/next-v32/`

## 9. Структура файлов

```
next-v32/
├── index.html               # языковой селектор
├── DESIGN.md                # этот файл
├── PRD.md                   # задачи
├── styles/
│   ├── tokens.css           # CSS variables (новая полная версия)
│   ├── layout.css           # grid, container, breakpoints
│   ├── components.css       # buttons, cards, nav
│   ├── hero.css             # 5-слойный hero
│   ├── sections.css         # manifesto, directions, books, blog
│   ├── books.css            # book card gallery
│   ├── theme.css            # light/dark switching
│   └── animations.css       # scroll-triggered + hover
├── scripts/
│   ├── theme.js             # localStorage + data-theme
│   ├── hero-parallax.js     # RAF-based 5-layer parallax
│   ├── scroll-anim.js       # GSAP ScrollTrigger + Lenis init
│   ├── counter.js           # number counter-up on scroll
│   └── main.js              # navigation, mobile menu
├── partials/                # shared HTML (header, footer) — для копирования
│   ├── header.html
│   └── footer.html
├── images/
│   ├── kenan/               # portrait
│   ├── books/               # 4 обложки (или generated)
│   ├── blog/                # 3 миниатюры
│   └── ui/                  # icons, ornaments
├── az/                      # 3 языка сайта
│   ├── index.html
│   ├── haqqimda.html
│   ├── tehsil.html
│   ├── xidmetler.html
│   ├── b2b.html
│   ├── blog.html
│   ├── books/
│   │   ├── index.html       # витрина
│   │   ├── phoenix-era.html
│   │   ├── guilt-virus.html
│   │   ├── pandemic-madness.html
│   │   └── clinical-psychiatry.html
│   └── ... (другие blog-страницы)
├── ru/
├── en/
├── tr/                      # только книга Clinical Psychiatry
└── klinik-psixiatriya/      # 4 языка книги (отдельная страница-учебник)
    ├── az/
    ├── ru/
    ├── en/
    └── tr/
```

## 10. Acceptance criteria

Сайт считается готовым когда:

- [ ] Токены модульные (1.333 ratio на type, 4px doubling на spacing)
- [ ] Hero 50–70% whitespace (negative space)
- [ ] Hero заполняет edge-to-edge (нет border, нет card)
- [ ] 5 слоёв движутся с разной скоростью
- [ ] Метрики считаются вверх при scroll
- [ ] Scroll-driven анимации через GSAP ScrollTrigger (или CSS view-timeline)
- [ ] Lenis smooth scroll работает
- [ ] Light/dark тема переключается плавно (transition)
- [ ] Тема сохраняется в localStorage
- [ ] Mobile-first: hero = визуал без текста, текст снизу
- [ ] Все тексты без перевёртышей и на правильных языках
- [ ] Реальные обложки книг (или качественные AI-сгенерированные)
- [ ] prefers-reduced-motion: анимации отключаются
- [ ] Lighthouse Performance ≥ 90
- [ ] Lighthouse SEO = 100
- [ ] Lighthouse Accessibility ≥ 95
- [ ] GitHub Pages деплой: `ragimoff.org/next-v32/` отдаёт 200