# MOTION-GUIDE.md — руководство по motion.dev для начинающего девелопера

> Motion (бывший Framer Motion) — production-grade библиотека анимаций для React, JavaScript и Vue.
> **Сайт:** https://motion.dev · **Лицензия:** MIT (бесплатно)
> **Размер:** до 90% меньше GSAP · **Поддержка:** Chrome, Safari, Firefox, Edge

---

## 0. Установка

### React (npm)
```bash
npm install motion
```
```js
import { motion } from "motion/react";
```

### Vanilla JavaScript (CDN, без сборки)
```html
<script src="https://cdn.jsdelivr.net/npm/motion@11.18.0/dist/motion.js"></script>
```
```js
const { animate, scroll, inView, stagger } = window.Motion;
```

> Для next-v32 (vanilla HTML, без билда) используем **CDN-вариант** через `<script>`.

---

## 1. Пять базовых концепций (запомни это)

| # | Концепция | Что делает | Пример |
|---|---|---|---|
| 1 | **Animate** | Анимирует CSS-значение | `animate(el, { opacity: 1 }, { duration: 0.6 })` |
| 2 | **Spring** | Реалистичная физика пружины | `animate(el, { x: 100 }, { type: "spring", stiffness: 300 })` |
| 3 | **InView** | Триггер при попадании в viewport | `inView(el, () => animate(el, ...))` |
| 4 | **Scroll** | Привязка к scroll-позиции | `scroll(animate(el, { y: [0, 100] }))` |
| 5 | **Hover / Press** | Интерактивные жесты | CSS-псевдоклассы + JS-обработчики |

---

## 2. ТОП-20 самых эффектных элементов

> Каждый элемент: **назначение · ресурсы · код · проверка**

---

### #1. Fade-In при скролле (базовый reveal)

**Назначение:** блок появляется с opacity 0→1 при попадании в viewport. Самый частый паттерн.

**Ресурсы:** Motion (CDN), один CSS-класс.

**Код (vanilla JS):**
```html
<div class="reveal" style="opacity: 0; transform: translateY(30px);">...</div>

<script>
  inView('.reveal', (el) => {
    animate(el, { opacity: 1, y: 0 }, { duration: 0.6, easing: 'ease-out' });
  }, { margin: '-10% 0px' });
</script>
```

**Проверка:** скролл вниз → блоки появляются один за другим.

---

### #2. Stagger — каскадное появление дочерних элементов

**Назначение:** список/grid, где элементы появляются один за другим (каскад).

**Код:**
```html
<ul class="stagger">
  <li>Пункт 1</li><li>Пункт 2</li><li>Пункт 3</li>
</ul>

<script>
  inView('.stagger', (el) => {
    animate(el.querySelectorAll('li'), 
      { opacity: 1, y: 0 },
      { delay: stagger(0.08), duration: 0.5 }
    );
  });
</script>
```

**Проверка:** при появлении секции элементы появляются с задержкой 80мс между ними.

---

### #3. Scroll-Progress Bar (индикатор прогресса чтения)

**Назначение:** тонкая полоска сверху/сбоку страницы, показывает глубину скролла.

**Код:**
```js
const bar = document.querySelector('.progress-bar');
scroll(
  animate(bar, { scaleX: [0, 1] }, { ease: 'linear' }),
  { target: document.documentElement }
);
// CSS: .progress-bar { position: fixed; top: 0; left: 0; right: 0; height: 3px; background: gold; transform-origin: 0 50%; transform: scaleX(0); }
```

**Проверка:** скролл → полоска растёт слева направо.

---

### #4. Magnetic Button (притяжение к курсору)

**Назначение:** кнопка слегка "притягивается" к курсору при наведении (Awwwards-приём).

**Код:**
```js
document.querySelectorAll('.btn--magnetic').forEach(btn => {
  btn.addEventListener('mousemove', (e) => {
    const r = btn.getBoundingClientRect();
    const x = (e.clientX - r.left - r.width / 2) * 0.3;
    const y = (e.clientY - r.top - r.height / 2) * 0.3;
    animate(btn, { x, y }, { duration: 0.4, type: 'spring', stiffness: 200 });
  });
  btn.addEventListener('mouseleave', () => {
    animate(btn, { x: 0, y: 0 }, { type: 'spring', stiffness: 200 });
  });
});
```

**Проверка:** наведи курсор на кнопку → она слегка двигается за ним.

---

### #5. Ken-Burns Slow Zoom (для hero-фото)

**Назначение:** фоновое фото медленно зумится при скролле, давая кинематографический эффект.

**Код:**
```js
const hero = document.querySelector('.hero-bg-img');
inView(hero, () => {
  scroll(animate(hero, { scale: [1, 1.15] }, { ease: 'linear' }));
});
// CSS: .hero-bg-img { transform: scale(1); will-change: transform; }
```

**Проверка:** при скролле фото медленно увеличивается.

---

### #6. Counter-Up (числа с 0 до N при появлении)

**Назначение:** метрики (23+ лет, 3000+ клиентов) анимируются от 0 к финальному значению.

**Код:**
```js
document.querySelectorAll('[data-counter]').forEach(el => {
  const target = parseInt(el.dataset.counter);
  inView(el, () => {
    animate(0, target, {
      duration: 1.4,
      ease: 'easeOut',
      onUpdate: (v) => { el.textContent = Math.round(v); }
    });
  }, { once: true });
});
```

**Проверка:** при появлении число "крутится" от 0 до 23.

---

### #7. Parallax Image Layer (многослойный параллакс)

**Назначение:** при скролле фоновый слой движется медленнее, чем контент — эффект глубины.

**Код:**
```js
document.querySelectorAll('[data-parallax]').forEach(layer => {
  const speed = parseFloat(layer.dataset.parallax); // 0.2, 0.4
  scroll(
    animate(layer, { y: [0, -window.innerHeight * speed] }, { ease: 'linear' }),
    { target: layer.closest('section') }
  );
});
```

**Проверка:** скролл → фоновые слои двигаются с разной скоростью.

---

### #8. Smooth Scroll (Lenis-style без зависимостей)

**Назначение:** плавная прокрутка вместо "прыжков".

**Код:**
```js
// Альтернатива Lenis через Motion
scroll(animate(window, { scrollY: [0, document.body.scrollHeight] }, {
  ease: 'linear'
}), { target: window });
```

> Для next-v32 уже подключён **Lenis** через CDN (см. `scripts/scroll-anim.js`).

---

### #9. Text Scramble / Glitch Reveal (наведение)

**Назначение:** при наведении текст "перетасовывается" случайными символами, потом возвращается.

**Код:**
```js
function scrambleText(el) {
  const original = el.textContent;
  const chars = '!@#$%^&*()_+-=[]{}|;:,.<>?';
  let frame = 0;
  const interval = setInterval(() => {
    el.textContent = original.split('').map((c, i) => {
      if (i < frame) return original[i];
      if (c === ' ') return ' ';
      return chars[Math.floor(Math.random() * chars.length)];
    }).join('');
    frame++;
    if (frame >= original.length) clearInterval(interval);
  }, 30);
}

document.querySelectorAll('.scramble').forEach(el => {
  el.addEventListener('mouseenter', () => scrambleText(el));
});
```

**Проверка:** наведи на заголовок → буквы хаотично меняются на 0.5 сек, потом возвращаются.

---

### #10. Magnetic Image Follow (фото следует за курсором)

**Назначение:** в hero-секции фото Kenan плавно движется за курсором мыши.

**Код:**
```js
const portrait = document.querySelector('.hero-portrait');
document.addEventListener('mousemove', (e) => {
  const r = portrait.getBoundingClientRect();
  const x = ((e.clientX - r.left) / window.innerWidth - 0.5) * 30;
  const y = ((e.clientY - r.top) / window.innerHeight - 0.5) * 30;
  animate(portrait, { x, y }, { duration: 0.8, type: 'spring', stiffness: 80 });
});
```

**Проверка:** двигай мышь → Kenan слегка следит за курсором.

---

### #11. Hamburger → X menu transition

**Назначение:** плавная трансформация гамбургера в крестик при открытии меню.

**Код:**
```js
const btn = document.querySelector('.menu-toggle');
const spans = btn.querySelectorAll('span');
btn.addEventListener('click', () => {
  const open = btn.classList.toggle('open');
  animate(spans[0], { y: open ? 6 : 0, rotate: open ? 45 : 0 });
  animate(spans[1], { opacity: open ? 0 : 1 });
  animate(spans[2], { y: open ? -6 : 0, rotate: open ? -45 : 0 });
});
```

**Проверка:** клик → три полоски превращаются в X с плавной анимацией.

---

### #12. Drag-to-Reorder (сортировка карточек)

**Назначение:** карточки книг или услуг можно перетаскивать мышью.

**Код:**
```js
import { Reorder } from "motion/react";

<Reorder.Group values={items} onReorder={setItems}>
  {items.map(item => (
    <Reorder.Item key={item} value={item} className="book-card" whileDrag={{ scale: 1.05 }}>
      <BookCard item={item} />
    </Reorder.Item>
  ))}
</Reorder.Group>
```

**Проверка:** потяни карточку — другие плавно перераспределяются.

---

### #13. Modal/Dialog with AnimatePresence

**Назначение:** модальное окно появляется с плавным scale + fade, при закрытии — обратно.

**Код (React):**
```js
<AnimatePresence>
  {isOpen && (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.2 }}
    >
      <Modal />
    </motion.div>
  )}
</AnimatePresence>
```

**Проверка:** модалка открывается с плавным scale, закрывается обратно.

---

### #14. Number Flip (как на цифровых часах)

**Назначение:** число переворачивается, как страница календаря, при изменении.

**Код:**
```js
animate(0, 100, {
  duration: 2,
  onUpdate: (v) => {
    el.textContent = Math.floor(v);
    el.style.transform = `rotateX(${(v % 1) * 360}deg)`;
  }
});
```

**Проверка:** число прокручивается в 3D-эффекте.

---

### #15. Toast/Notification Stack (стопка уведомлений)

**Назначение:** уведомления появляются снизу, складываются стопкой, исчезают по очереди.

**Код:**
```js
function toast(msg) {
  const el = document.createElement('div');
  el.className = 'toast';
  el.textContent = msg;
  document.getElementById('toast-stack').appendChild(el);
  animate(el, { y: 0, opacity: 1, scale: 1 }, { type: 'spring', stiffness: 300 });
  setTimeout(() => {
    animate(el, { opacity: 0, x: 100 }, { duration: 0.3 }).then(() => el.remove());
  }, 3000);
}
```

**Проверка:** вызывай `toast('Привет!')` — уведомление появится справа снизу.

---

### #16. Tilt-3D Card (карточка наклоняется за мышью)

**Назначение:** карточка книги/услуги наклоняется в 3D в направлении курсора.

**Код:**
```js
document.querySelectorAll('.tilt-card').forEach(card => {
  card.addEventListener('mousemove', (e) => {
    const r = card.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width - 0.5;
    const y = (e.clientY - r.top) / r.height - 0.5;
    animate(card, {
      rotateY: x * 15,
      rotateX: -y * 15,
      transformPerspective: 1000
    }, { duration: 0.3 });
  });
  card.addEventListener('mouseleave', () => {
    animate(card, { rotateY: 0, rotateX: 0 }, { duration: 0.5 });
  });
});
```

**Проверка:** наведи на карточку → 3D-наклон за мышью.

---

### #17. SVG Path Drawing (анимация контура)

**Назначение:** рисует SVG-путь как "ручкой" (от 0% до 100%) при появлении.

**Код:**
```js
const path = document.querySelector('.signature path');
const length = path.getTotalLength();
path.style.strokeDasharray = length;
path.style.strokeDashoffset = length;
inView(path, () => {
  animate(path, { strokeDashoffset: 0 }, { duration: 2, ease: 'easeInOut' });
});
```

**Проверка:** при скролле подпись Kenan "пишется" автоматически.

---

### #18. Carousel with Snap (лента с snap-scroll)

**Назначение:** горизонтальная лента карточек с привязкой к ближайшей.

**Код:**
```js
import { useScroll, useTransform } from "motion/react";

const scrollX = useScroll().scrollX;
const x = useTransform(scrollX, (v) => -v * 0.5);
// Привязать transform: translateX(x) к ленте
```

> Альтернативный вариант: CSS `scroll-snap-type: x mandatory;` + `scroll-snap-align: start;` — без JS.

---

### #19. Spring Physics Toggle (toggle с пружиной)

**Назначение:** toggle-кнопка с пружинной анимацией — красиво "пружинит" при клике.

**Код:**
```js
const toggle = document.querySelector('.toggle');
let isOn = false;
toggle.addEventListener('click', () => {
  isOn = !isOn;
  animate(toggle, {
    backgroundColor: isOn ? '#10a37f' : '#1a1a2e',
    scale: [1, 0.9, 1.05, 1]  // ключевые кадры пружины
  }, { duration: 0.4, ease: 'easeOut' });
});
```

**Проверка:** клик → toggle "сжимается" и "отскакивает" пружиной.

---

### #20. View Transition API (переходы между страницами)

**Назначение:** плавные переходы при переходе между страницами (как в Next.js).

**Код (vanilla JS):**
```js
// На странице, с которой уходим:
document.addEventListener('click', (e) => {
  const link = e.target.closest('a[href]');
  if (!link || link.target === '_blank' || link.origin !== location.origin) return;
  e.preventDefault();
  const transition = document.startViewTransition(() => {
    location.href = link.href;
  });
});

// В CSS:
::view-transition-old(root) { animation: fade-out 0.3s; }
::view-transition-new(root) { animation: fade-in 0.3s; }
@keyframes fade-out { to { opacity: 0; } }
@keyframes fade-in { from { opacity: 0; } }
```

**Проверка:** клик по ссылке → страница плавно перетекает.

---

## 3. Сводная таблица эффектов

| # | Эффект | Сложность | Файл / где использовать | WOW-эффект |
|---|---|---|---|---|
| 1 | Fade-in reveal | Низкая | Любой блок | ⭐⭐ |
| 2 | Stagger | Низкая | Списки, гриды | ⭐⭐ |
| 3 | Scroll progress bar | Низкая | `<body>` overlay | ⭐⭐ |
| 4 | Magnetic button | Средняя | CTA-кнопки | ⭐⭐⭐ |
| 5 | Ken-Burns | Средняя | Hero-фото | ⭐⭐⭐ |
| 6 | Counter-up | Средняя | Метрики | ⭐⭐ |
| 7 | Parallax layers | Средняя | Hero, разделы | ⭐⭐⭐ |
| 8 | Smooth scroll | Средняя | Глобально | ⭐⭐ |
| 9 | Text scramble | Высокая | Заголовки | ⭐⭐⭐ |
| 10 | Magnetic image | Средняя | Hero-фото | ⭐⭐⭐ |
| 11 | Hamburger → X | Низкая | Меню | ⭐⭐ |
| 12 | Drag-to-reorder | Высокая | Списки | ⭐⭐⭐ |
| 13 | Modal AnimatePresence | Средняя | Формы, попапы | ⭐⭐⭐ |
| 14 | Number flip | Средняя | Метрики, цены | ⭐⭐⭐ |
| 15 | Toast stack | Высокая | Уведомления | ⭐⭐ |
| 16 | Tilt-3D card | Средняя | Карточки | ⭐⭐⭐ |
| 17 | SVG path draw | Низкая | Подписи, иконки | ⭐⭐⭐ |
| 18 | Carousel snap | Средняя | Книги, услуги | ⭐⭐ |
| 19 | Spring toggle | Низкая | Theme, language | ⭐⭐ |
| 20 | View transition | Высокая | Cross-page | ⭐⭐⭐⭐ |

---

## 4. Производительность (60 FPS)

**Золотые правила:**
- ✅ `transform` + `opacity` — анимировать ТОЛЬКО эти свойства (GPU)
- ✅ `will-change: transform, opacity` — добавить в CSS
- ❌ НЕ анимировать `width`, `height`, `top`, `left`, `margin`, `padding` (вызывает reflow)
- ✅ Использовать `transform: translate3d(0, 0, 0)` для включения GPU
- ✅ Проверять DevTools → Performance → 60 FPS target

---

## 5. Доступность (a11y)

```js
// Всегда уважай prefers-reduced-motion
const motion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  ? { duration: 0 }
  : { duration: 0.6 };

animate(el, { opacity: 1 }, motion);
```

---

## 6. Подключение в next-v32 (vanilla JS через CDN)

**`index.html`** или в конце `<body>` главных страниц:
```html
<script src="https://cdn.jsdelivr.net/npm/motion@11.18.0/dist/motion.js"></script>
<script>
  const { animate, scroll, inView, stagger } = Motion;
  // ... примеры выше
</script>
```

---

## 7. Документация и ресурсы

- 📚 **Docs:** https://motion.dev/docs
- 🎯 **Examples:** https://motion.dev/examples
- 🎨 **UI Library:** https://motion.dev/ui
- 📰 **Magazine:** https://motion.dev/magazine
- 💻 **GitHub:** https://github.com/motiondivision/motion
- 🎓 **Tutorial Book:** https://book.motion.dev
- 🤖 **AI Kit:** https://motion.dev/ai-kit (для AI-агентов, которые генерируют код с Motion)

---

**Создано:** 2026-09-14
**Версия Motion:** 11.18.0
**Лицензия:** MIT (бесплатно для коммерческого использования)
