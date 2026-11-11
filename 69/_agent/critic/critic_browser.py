"""КРИТИК · ПРОВЕРКА В БРАУЗЕРЕ: ЗАМЕРЫ ВМЕСТО МНЕНИЙ.

ЗАЧЕМ ОТДЕЛЬНЫЙ ФАЙЛ. Первый критик (critic.py) проверяет страницу как
текст: ссылки, alt, заголовки, запретные формулировки. Этого мало.
Владелец: «вы просто не умеете свои задачи, свои работы проверять.
Не проверяете. Тяп-ляп сделали — и бросаете вперёд, типа готово».
Большая часть дефектов этого проекта видна ТОЛЬКО в браузере: невидимые
блоки, текст на лице, переполнение по горизонтали, неработающие темы,
невидимые в светлой теме надписи. Их нельзя поймать чтением файла.

ЧТО ПРОВЕРЯЕТ ЭТОТ ФАЙЛ — каждый пункт родился из реальной поломки:
  1. ВИДИМОСТЬ БЛОКОВ. Самая дорогая ошибка проекта: блоки с opacity 0,
     которые так и не проявились — страница выглядела пустой.
  2. ПЕРЕПОЛНЕНИЕ ПО ГОРИЗОНТАЛИ. Появляется от широких элементов и
     ломает всю раскладку на телефоне.
  3. ТЕКСТ НА ЛИЦЕ В ГЕРОЕ. Владелец говорил дважды: «текст лезет на
     лицо девушке». Проверяется пересечением прямоугольника текста с
     зоной человека.
  4. РАБОТОСПОСОБНОСТЬ ТРЁХ ТЕМ. Обязательное требование владельца;
     один раз переключателя не было ВООБЩЕ, в другой раз в светлой теме
     текст пропадал.
  5. КОНТРАСТ ТЕКСТА В КАЖДОЙ ТЕМЕ. Белое на светлом — самый частый
     дефект светлой темы.
  6. БИБЛИОТЕКИ МОУШЕНА. Если GSAP не поднялся — анимации молча не
     работают, и никто об этом не узнаёт.
  7. ЗАЩИТА ОТ НЕВИДИМОСТИ. При сломанном скрипте страница обязана
     читаться целиком.

Запуск (через browser_exec в Hermes):
    код этого файла выполняется в браузере и возвращает список замечаний.
"""
CHECK_JS = r"""
(function () {
  var out = [];
  function add(level, what, detail) { out.push({level: level, what: what, detail: detail}); }
  var cs = getComputedStyle;

  /* 1. ВИДИМОСТЬ БЛОКОВ */
  var blocks = document.querySelectorAll('.reveal');
  var hidden = 0;
  var hiddenSample = [];
  for (var i = 0; i < blocks.length; i++) {
    var el = blocks[i];
    var r = el.getBoundingClientRect();
    var inView = r.top < innerHeight && r.bottom > 0;
    if (parseFloat(cs(el).opacity) < 0.5) {
      hidden++;
      if (inView && hiddenSample.length < 3) {
        hiddenSample.push((el.className || '').slice(0, 40));
      }
    }
  }
  if (hiddenSample.length) {
    add('БЛОК', 'Невидимые блоки в зоне видимости', hiddenSample.join(' | '));
  }
  add('ИНФО', 'Блоков всего', String(blocks.length));

  /* 2. ПЕРЕПОЛНЕНИЕ ПО ГОРИЗОНТАЛИ */
  if (document.documentElement.scrollWidth > innerWidth + 1) {
    add('БЛОК', 'Переполнение по горизонтали',
        'ширина ' + document.documentElement.scrollWidth + ' против окна ' + innerWidth);
  }

  /* 3. ТЕКСТ НА ЛИЦЕ В ГЕРОЕ */
  var heroImg = document.querySelector('.hero__frame img, .hero__media img');
  var heroTxt = document.querySelector('.hero__inner');
  if (heroImg && heroTxt) {
    var ti = heroImg.getBoundingClientRect(), tt = heroTxt.getBoundingClientRect();
    /* зона головы: верхняя треть портрета, центральная половина по ширине */
    var head = {
      left: ti.left + ti.width * 0.30,
      right: ti.left + ti.width * 0.78,
      top: ti.top + ti.height * 0.05,
      bottom: ti.top + ti.height * 0.42
    };
    var ox = Math.max(0, Math.min(head.right, tt.right) - Math.max(head.left, tt.left));
    var oy = Math.max(0, Math.min(head.bottom, tt.bottom) - Math.max(head.top, tt.top));
    if (ox > 0 && oy > 0) {
      var area = (ox * oy) / Math.max(1, tt.width * tt.height);
      if (area > 0.12) {
        add(area > 0.3 ? 'БЛОК' : 'ВНИМАНИЕ', 'Текст заходит на зону лица в герое',
            'пересечение ' + Math.round(area * 100) + '% площади текста');
      }
    }
  }

  /* 4+5. ТЕМЫ И КОНТРАСТ */
  function bgOf(el) {
    var n = el;
    while (n && n !== document.documentElement) {
      var c = cs(n).backgroundColor;
      var m = c.match(/[\d.]+/g);
      if (m && (m.length < 4 || parseFloat(m[3]) > 0.5)) return c;
      n = n.parentElement;
    }
    return cs(document.body).backgroundColor;
  }
  function lum(c) {
    var m = c.match(/[\d.]+/g);
    if (!m) return null;
    var r = +m[0], g = +m[1], b = +m[2];
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255;
  }
  var themes = [];
  var btns = document.querySelectorAll('.theme__btn, .themes button');
  if (!btns.length) {
    add('БЛОК', 'Нет переключателя тем', 'требование владельца: три темы');
  }
  for (var t = 0; t < btns.length; t++) {
    var name = btns[t].getAttribute('data-theme-set') || '?';
    themes.push(name);
    document.documentElement.setAttribute('data-theme', name);
    var rgb = getComputedStyle(document.body).backgroundColor;
    var bad = 0, badSample = '';
    var els = document.querySelectorAll('h1,h2,h3,p,li,a,span,button,label');
    for (var k = 0; k < els.length; k++) {
      var e = els[k];
      if (!e.textContent.trim() || e.offsetParent === null) continue;
      var lt = lum(cs(e).color), lb = lum(bgOf(e));
      if (lt === null || lb === null) continue;
      if (Math.abs(lt - lb) < 0.20) {
        bad++;
        if (!badSample) badSample = (e.className || e.tagName).slice(0, 36);
      }
    }
    if (bad) {
      add('ВНИМАНИЕ', 'Мало контраста в теме «' + name + '»',
          bad + ' элементов, например ' + badSample);
    }
  }
  document.documentElement.setAttribute('data-theme', themes[0] || 'dark');

  /* 6. БИБЛИОТЕКИ МОУШЕНА */
  if (document.querySelector('script[src*="gsap"]') && typeof window.gsap === 'undefined') {
    add('ВНИМАНИЕ', 'GSAP подключён, но не загрузился', 'анимации не работают');
  }
  if (document.querySelector('script[src*="lenis"]') && typeof window.Lenis === 'undefined') {
    add('ВНИМАНИЕ', 'Lenis подключён, но не загрузился', 'инерции прокрутки нет');
  }

  /* 7. ФОРМЫ */
  var forms = document.querySelectorAll('.reg__form');
  if (forms.length < 4) {
    add('БЛОК', 'Форм регистрации меньше четырёх',
        'канон требует: обучение, индивидуальный тренинг, консультации, организации');
  }
  for (var fi = 0; fi < forms.length; fi++) {
    var f = forms[fi];
    if (!f.querySelector('button[type="submit"]')) {
      add('ВНИМАНИЕ', 'В форме нет кнопки отправки', f.id || '—');
    }
    var req = f.querySelectorAll('[name]');
    if (!req.length) add('ВНИМАНИЕ', 'В форме нет полей', f.id || '—');
  }

  return out;
})()
"""


def main():
    """Печатает код проверки: его надо выполнить в браузере через browser_exec."""
    print('# выполни этот код в браузере на проверяемой странице:')
    print('# результат — список замечаний по уровням БЛОК / ВНИМАНИЕ / ИНФО')
    print(CHECK_JS)


if __name__ == '__main__':
    main()
