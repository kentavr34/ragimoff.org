# DESIGN-SCHEMES.md — карта структуры и дизайна next-v32

> Источник истины для структуры, навигации и контента страниц.
> Каждая страница — одна сущность, один CSS-файл (`styles/pages/{name}.css`).

---

## 1. Бизнес-сущности Kenan Rəhimov (RAGIMOFF)

| Сущность | Описание | URL (AZ) |
|---|---|---|
| **Kənan** | Главный психолог, IPAS Ambassador, основатель | haqqimda.html |
| **Samirə** | Семейный терапевт, супруга | samira.html |
| **Təhsil** | 3 программы обучения | tehsil.html |
| **Xidmətlər** | 6 направлений консультаций | xidmetler.html |
| **Kitablar** | 4 книги | books.html |
| **Ailə Terapiyası** | Семейная терапия Samirə | aile-terapiyasi.html |
| **B2B** | Корпоративные услуги | b2b.html |
| **Blog** | Статьи | blog.html |
| **Əlaqə** | Контакты | (в шапке/подвале) |

---

## 2. Главное меню (единое для всех 4 языков)

| Ключ | AZ | RU | EN | TR | Ссылка |
|---|---|---|---|---|---|
| `home` | Ana | Главная | Home | Ana | index.html |
| `tehsil` | Təhsil | Обучение | Training | Eğitim | tehsil.html |
| `xidmetler` | Xidmətlər | Услуги | Services | Hizmetler | xidmetler.html |
| `kitablar` | Kitablar | Книги | Books | Kitaplar | books.html |
| `aile` | Ailə | Семейная | Family | Aile | aile-terapiyasi.html |
| `b2b` | B2B | B2B | B2B | B2B | b2b.html |
| `blog` | Blog | Блог | Blog | Blog | blog.html |
| `haqqimda` | Haqqımda | Обо мне | About | Hakkımda | haqqimda.html |

> ⚠️ НЕ добавлять в основное меню: samira.html (это «дочка» haqqimda), books/ (дочка kitablar), program-*.html (дочки tehsil). Они — подразделы.

---

## 3. Дизайн-схемы (4 главных шаблона)

### 3.1. HOME (index.html)

**Назначение:** продать себя за 8 секунд + направить в нужный раздел.

**Структура (по убыванию приоритета):**

| # | Секция | CSS-класс | Контент | Источник |
|---|---|---|---|---|
| 1 | **Hero** | `.hero` | IPAS Ambassador · BAPPs · ADA<br>Заголовок + подзаголовок<br>2 CTA: Zəng et / Kitablarımız<br>Метрики 23+ / 3000+ / 300+ / 11 | `haqqimda.html` |
| 2 | **Manifesto** | `.manifesto` | Quote: "Sənədlər, həmkarlar, faktlar — sübuta dayalı siqnal."<br>Лестница из 3 шагов | новый |
| 3 | **Partners** | `.partners-section` | Full-bleed фото Kenan + Samirə<br>2 "+" cursor с bio-panels | `samira.html` + `haqqimda.html` |
| 4 | **Directions (3 направления)** | `.directions` | Təhsil, Xidmətlər, B2B — alternating full-bleed | копия `az/index.html` |
| 5 | **About Kenan** | `.about` | Портрет + bio + бейджи IPAS/BAPPs/ADA | `haqqimda.html` |
| 6 | **Books (4 книги)** | `.books-gallery` | Phoenix, Guilt, Pandemic, Clinical | `books.html` |
| 7 | **Blog (превью 3 статьи)** | `.blog-grid` | 3 свежие статьи | `blog.html` |
| 8 | **CTA** | `.cta-section` | Тёмный блок: +994 70 220 03 76 / WhatsApp / Telegram | footer |

---

### 3.2. TƏHSIL (tehsil.html)

**Назначение:** продать 3 программы обучения.

**Структура:**

| # | Секция | CSS-класс | Контент | Источник |
|---|---|---|---|---|
| 1 | **Page Hero** | `.page-hero` | Eyebrow: Təhsil<br>Заголовок: "Klinik psixologiya üzrə peşəkar təhsil"<br>Subtitle + 4 stat (3 proqram / 27 ay / 300+ / 11 sertifikat) | новый |
| 2 | **3 Programs** | `.programs-grid` | 3 карточки с featured (Klinik):<br>01 — Ümumi Psixologiya (9 ay)<br>02 — Klinik Psixologiya (12 ay) — featured<br>03 — Klinik Praktikum (6 ay) | `tehsil.html` |
| 3 | **Process (4 шага)** | `.process-steps` | 01 Müraciət → 02 Test və müsahibə → 03 Təhsil → 04 Sertifikat | новый |
| 4 | **Audience (3 типа)** | `.audience-grid` | Məzun / Peşəkarı dəyişmək / Biliklərini artırmaq | новый |
| 5 | **CTA** | `.cta-section` | İlkin konsultasiya — zəng et | footer |

---

### 3.3. KITABLAR (books.html)

**Назначение:** продать 4 книги + дать превью.

**Структура:**

| # | Секция | CSS-класс | Контент | Источник |
|---|---|---|---|---|
| 1 | **Library Hero** | `.books-hero` | Eyebrow: Kitabxana<br>Заголовок: "Klinik təcrübə — çapa çevrilmiş."<br>4 stat (4 kitab / 1208 səhifə / 3000+ ekspertiza) | новый |
| 2 | **Featured Book** | `.featured-book` | Обложка + название + 5 преимуществ + цена + 2 кнопки | `books.html` |
| 3 | **Catalog (4 книги)** | `.books-gallery` | Все 4 книги: Phoenix, Guilt, Pandemic, Clinical | `books.html` |
| 4 | **Library About** | `.library-about` | "Niyə bu kitablar" — editorial manifesto | `books.html` |
| 5 | **CTA (заказ)** | `.cta-section` | Çatdırılma + zəng | footer |

> Каждая книга → отдельная страница `books/{slug}.html` с TOC, sample, author bio.

---

### 3.4. XİDMƏTLƏR (xidmetler.html)

**Назначение:** описать 6 типов консультаций + конверсия.

**Структура:**

| # | Секция | CSS-класс | Контент | Источник |
|---|---|---|---|---|
| 1 | **Services Hero** | `.page-hero` | Eyebrow: Xidmətlər<br>Заголовок: "Klinik protokollar — Azərbaycan dilində."<br>4 stat (6 istiqamət / 3000+ hal / 23 il / 95% müsbət) | новый |
| 2 | **6 Services** | `.services-grid` | 6 карточек с иконками:<br>Depressiya, Panik ataklar, Sosial fobiya, Ailə terapiyası, Uşaq, Travma | `xidmetler.html` |
| 3 | **Process (4 шага)** | `.process-steps` | 01 İlk müraciət → 02 İlk konsultasiya (60 dəq) → 03 Müalicə planı → 04 Müntəzəm seanslar | `xidmetler.html` |
| 4 | **CTA** | `.cta-section` | İlk konsultasiya — zəng | footer |

---

## 4. CSS-архитектура (модульная)

```
styles/
├── tokens.css       # ВСЕ CSS-переменные (цвета, шрифты, размеры, тени, motion)
├── layout.css       # grid, container, breakpoints
├── components.css   # header, .btn, .card, .metric, .nav-link
├── hero.css         # только .hero (используется на index)
├── animations.css   # .reveal, .stagger, scroll-triggered утилиты
├── sections.css     # ОБЩИЕ секции (manifesto, process, audience, cta)
├── books.css        # стили для book-карточек и detail
└── pages/
    ├── home.css         # partners-section, directions, about
    ├── education.css    # programs-grid, hero
    ├── books.css        # (уже есть) — оставить как есть
    ├── services.css     # services-grid
    ├── blog.css         # blog-article
    ├── about.css        # bio-hero, timeline
    ├── family.css       # aile-terapiyasi стили
    ├── contact.css      # form-styling
    └── b2b.css          # corporate стили
```

> **Правило:** одна страница = один CSS-файл в `pages/`. Если стиль используется на 2+ страницах — выносить в `sections.css` или `components.css`.

---

## 5. Тексты (ИСПОЛЬЗОВАТЬ РЕАЛЬНЫЕ, не придумывать)

### Hero (index.html)
- Eyebrow: **IPAS Ambassador · BAPPs · ADA** (из haqqimda.html)
- Заголовок: новый (editorial) — `"23 il — insanları eşidirir, həyatları dəyişdirir."`
- Subtitle: новый (editorial) — `"Sənədlər, həmkarlar, faktlar — sübuta dayalı siqnal."`
- Метрики: **23+** (illik təcrübə), **3000+** (uğurlu hal), **300+** (yetişdirilmiş mütəxəssis), **11** (sertifikat)

### Manifesto
- Eyebrow: `Manifesto`
- Pull-quote: новый (editorial) — `"Sənədlər, həmkarlar, faktlar — sübuta dayalı siqnal."`
- Body: редакционный текст

### Partners
- Eyebrow: `Müəssis`
- Heading: `"klinik həyat yoldaşı"` (реально, Samirə)
- **Kenan bio** (реально из haqqimda.html): `"23 illik klinik təcrübəyə malik həkim-psixiatr, psixoterapevt və psixologiya müəllimi."`
- **Samirə bio** (реально из samira.html): `"Klinik psixoloq və ailə terapevti. Ailə terapiyası, çətin yeniyetmələrlə iş və təşviş pozuntuları üzrə ixtisaslaşma."`

### About
- Всё из haqqimda.html

### Books
- Всё из books.html (Phoenix, Guilt, Pandemic, Clinical Psychiatry)

### Təhsil (tehsil.html)
- Всё из tehsil.html + 3 program страницы

### Xidmətlər (xidmetler.html)
- Всё из xidmetler.html + 4 детальные страницы (depressiya, enurez, panik-ataklar, sosial-fobiya)

### Ailə Terapiyası
- Всё из samira.html и aile-terapiyasi.html

### B2B
- Всё из b2b.html

### Blog
- Список + detail страницы из `blog/*.html`

---

## 6. Сайтмап (sitemap.xml будущего)

```
/
├── /[lang]/          ← AZ / RU / EN / TR (auto-detect по IP)
│   ├── index.html           ← Главная
│   ├── tehsil.html          ← 3 программы
│   │   ├── program-umumi.html
│   │   ├── program-klinik.html
│   │   └── program-praktikum.html
│   ├── xidmetler.html       ← 6 услуг
│   │   ├── depressiya.html
│   │   ├── enurez.html
│   │   ├── panik-ataklar.html
│   │   └── sosial-fobiya.html
│   ├── books.html           ← 4 книги
│   │   ├── phoenix-era.html
│   │   ├── guilt-virus.html
│   │   ├── pandemic-madness.html
│   │   └── clinical-psychiatry.html
│   ├── aile-terapiyasi.html  ← Samirə
│   │   └── aile-terapiyasi-usaq.html
│   ├── b2b.html
│   ├── blog.html
│   │   └── blog-{topic}.html  (40+)
│   └── haqqimda.html         ← Kenan bio
```

---

## 7. Что НЕ делать (anti-patterns)

- ❌ Плодить одинаковые копии текста в 4 языках через ручной find-replace
- ❌ Изобретать текст (Samirə, "Mina", выдуманные имена)
- ❌ Использовать скриншоты с других сайтов (lunchlinepartners)
- ❌ Создавать новые HTML-структуры для header/footer — только через CSS
- ❌ Hover-эффекты translateY/scale (Wix-look)
- ❌ Hover-анимация, которая выглядит как 2015 (translucent glow, scale-up)
- ❌ Создавать 30+ одинаковых страниц когда хватит 5-7 эталонных

---

## 8. Следующие шаги

1. ✅ DESIGN-SCHEMES.md (этот файл)
2. ⬜ Создать `styles/pages/{home,education,books,services,blog,about,family,contact,b2b}.css`
3. ⬜ Рефакторинг — переместить page-specific стили в pages/
4. ⬜ Создать эталоны (3-4 страницы) на основе этого документа
5. ⬜ Сайтмап (sitemap.xml)
6. ⬜ Деплой на `ragimoff.org/next-v32/`
