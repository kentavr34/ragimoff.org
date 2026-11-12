# Карта файлов новой версии сайта (test/11)

Собирается автоматически: `python _tools/structure_check.py map`. Правила раскладки проверяет тот же страж — файл не на своём месте останавливает публикацию.

## Корень — страницы

| файл | что это |
|---|---|
| `index.html` | главная |
| `program.html` | программа обучения (?p=) |
| `specialist.html` | специалист (?s=) |
| `consult.html` | консультация (?c=) |
| `contact.html` | контакты |
| `corporate.html` | тренинги для компаний |
| `blog.html` | блог |
| `article.html` | статья (?a=) |
| `law.html` | переадресация на блок «Юридические основы» |
| `shop.html` | книжный магазин |
| `book.html` | страница книги (?b=) |
| `read.html` | читалка (?b=&c=) |
| `test.html` | тест для студентов |
| `README.md` | описание проекта |
| `FILE_MAP.md` | карта файлов (собирается этим стражем) |
| `.gitignore` | что не публикуется |
| `404.html` | страница «не найдено»: переводит прежние адреса сайта на новые |
| `CLAUDE.md` | вводная для агента |
| `CNAME` | домен ragimoff.org |
| `.nojekyll` | публиковать как есть |
| `robots.txt` | правила для поисковиков |
| `sitemap.xml` | карта сайта (build_sitemap.py) |
| `sw.js` | снимает сохранённые копии прежнего сайта с устройств |
| `favicon.ico` | значок |
| `app.webmanifest` | описание приложения |
| `site.webmanifest` | описание приложения |
| `browserconfig.xml` | значки для Windows |
| `indexnow_key.txt` | ключ оповещения поисковиков |
| `_lang-switch.js` | нужен странице заказа книг (временно) |
| `apple-touch-icon-120x120.png` | значок |
| `apple-touch-icon-152x152.png` | значок |
| `apple-touch-icon-180x180.png` | значок |
| `apple-touch-icon-76x76.png` | значок |
| `apple-touch-icon.png` | значок |

## Папки

| папка | что лежит |
|---|---|
| `assets/` | оформление и сценарии: css, js, img, hero |
| `data/` | тексты страниц по разделам и языкам |
| `books/` | библиотека: текст книг отдельно от страниц |
| `_tools/` | инструменты сборки и стражи |
| `_agent/` | служебное (не публикуется, кроме lock и archive) |
| `vendor/` | сторонние библиотеки |
| `sketch/` | наброски |
| `payment/` | страницы возврата после оплаты (адреса записаны на сервере оплаты) |
| `test/` | действующий тест: aile.html и его движок quiz.js |
| `app/` | приложение для Android |
| `favicons/` | значки |
| `.well-known/` | подтверждение приложения |
| `.claude/` | настройки агента |

## Тексты страниц — `data/<раздел>/<страница>.<язык>.json`

| раздел | что лежит | страниц × языков |
|---|---|---|
| `data/blog/` | статьи и список блога | 115 файлов (39 страниц) |
| `data/cons/` | страницы консультаций | 30 файлов (10 страниц) |
| `data/page/` | контакты, тренинги | 6 файлов (2 страниц) |
| `data/spec/` | специалисты | 6 файлов (2 страниц) |
| `data/law/` | блок «Юридические основы» | 3 файлов (1 страниц) |
| `data/shop/` | каталог магазина | 3 файлов (1 страниц) |

## Картинки — `assets/img/<раздел>/`

| раздел | что лежит | файлов |
|---|---|---|
| `assets/img/home/` | главная | 3 |
| `assets/img/books/` | обложки книг | 45 |
| `assets/img/specialists/` | портреты и дипломы специалистов | 16 |
| `assets/img/programs/` | обучение: документы института, образцы, фото групп | 30 |
| `assets/img/consult/` | картины героя страниц консультаций | 9 |
| `assets/img/training/` | тренинги для компаний | 1 |
| `assets/img/blog/` | обложки статей по рубрикам | 50 |

В данных картинка записывается как `/images/<раздел>/…` — сценарий подставляет `assets/img/`.

## Библиотека — `books/`

Текст книги хранится один раз и отдельно от страниц. Читает его одна читалка `read.html?b=<книга>&c=<глава>`; новая книга или новый язык — это новая папка с текстом, новых страниц не появляется.

- `books/index.json` — картотека: все книги, языки, число глав и объём.
- `books/<книга>/book.json` — паспорт: названия на языках, сведения, обложка, оглавление.
- `books/<книга>/<язык>/NN.html` — текст главы NN.
- Найти, где что написано: `python _tools/library_find.py <слова> [--book книга] [--lang язык]` — выдаёт книгу, главу и абзац.

| книга (папка) | название | языки | глав | знаков, тыс. |
|---|---|---|---|---|
| `freud-afaziya` | Afaziyaların dərk edilməsinə dair | az | 4 | 330 |
| `freud-aforizmlar` | Aforizmlər | az | 12 | 34 |
| `freud-fliesse-mektublari` | Psixoanalizin başlanğıcından: Flissə məktublar | az | 119 | 766 |
| `freud-gw01` | Histeriyadan psixoanalizə | az | 15 | 1043 |
| `freud-gw02` | Yuxuların yozumu | az | 11 | 1315 |
| `freud-gw04` | Gündəlik həyatın psixopatologiyası | az | 12 | 522 |
| `freud-gw05` | Cinsəllik nəzəriyyəsi və Dora halı | az | 6 | 535 |
| `freud-gw06` | Zarafat və onun şüursuzla əlaqəsi | az | 7 | 431 |
| `freud-gw07` | Fantaziya, uşaqlıq və məcburiyyət | az | 16 | 699 |
| `freud-gw08` | Leonardo, Şreber və müalicənin texnikası | az | 25 | 721 |
| `freud-gw09` | Totem və tabu | az | 5 | 335 |
| `freud-gw10` | Narsisizm, şüursuz və matəm | az | 28 | 705 |
| `freud-gw11` | Psixoanalizə giriş mühazirələri | az | 28 | 846 |
| `freud-gw12` | Qorxulu, «Uşağı döyürlər» və uşaq nevrozu | az | 15 | 507 |
| `freud-gw13` | Həzz prinsipinin o tayında | az | 24 | 674 |
| `freud-gw14` | Din, mədəniyyət və təşviş | az | 34 | 897 |
| `freud-gw15` | Psixoanalizə giriş: yeni mühazirələr | az | 8 | 340 |
| `freud-gw16` | Musa adamı və monoteist din | az | 16 | 443 |
| `freud-gw17` | Psixoanalizin xülasəsi | az | 15 | 241 |
| `freud-koka-afaziya` | Koka və afaziya: psixoanalizdən əvvəlki əsərlər | az | 11 | 429 |
| `freud-kokain` | Koka haqqında | az | 7 | 100 |
| `freud-referatlar-1884-1885` | Referatlar | az | 2 | 151 |
| `freud-resenziyalar-1887-1910` | Resenziyalar | az | 11 | 48 |
| `freud-sehnede-psixopatik-personajlar` | Səhnədə psixopatik personajlar | az | 1 | 12 |
| `freud-sevgi-mektublari` | Sevgi məktubları | az | 56 | 227 |
| `freud-sossur-on-sozu` | R. de Sossürün kitabına ön söz | az | 1 | 3 |
| `freud-usaq-iflici` | İnfantil serebral iflic | az | 11 | 803 |
| `freud-yung-mektublari` | Freyd–Yunq məktubları | az | 366 | 966 |
| `freud-zweig-mektublari` | Freyd–Tsveyq məktubları | az | 79 | 86 |
| `klinik-psixiatriya` | Клиническая психиатрия | az ru en tr | 137/137/137/137 | 1334/1349/1251/1201 |
| `phoenix-era` | Эра Феникса | az ru en | 22/22/22 | 313/307/340 |
| `shizofreniya` | Шизофрения. Пандемия безумия | az ru en | 36/36/36 | 507/499/518 |
| `virus-viny` | Вирус вины | az ru en | 29/29/29 | 346/320/335 |

## Сценарии и стили — `assets/`

| файл | назначение |
|---|---|
| `assets/js\blocks.js` | test/11 — блоки внутренних страниц: один набор на специалистов, консультации, контакты, тренинги, право, блог. |
| `assets/js\chrome.js` | test/11 — общая «рама» внутренних страниц: шапка, меню, тема, язык, соцсети, подвал. Тексты — из content.js, стили — из site.css. |
| `assets/js\content.js` | test/11 — ТЕКСТЫ И ДАННЫЕ главной, три языка. Один источник: страница только рисует то, что здесь. |
| `assets/js\light.js` | Живой свет: тёмная комната с лампой (ночь) или дневной свет на бумаге (бумага, сепия). |
| `assets/js\page-program.js` | test/11 — страница программы обучения: один шаблон на все программы. Данные — programs.js, подписи — content.js (T[l].pp), форма — reg.js. |
| `assets/js\page-shop.js` | test/11 — прототип книжного магазина (shop.html) и страницы книги (book.html?b=<id>). |
| `assets/js\page-test.js` | test/11 — страница теста: рама сайта (шапка, меню, темы, подвал). Сам тест ведёт прежний сценарий /test/quiz.js. |
| `assets/js\page.js` | test/11 — внутренняя страница из блоков: один сценарий на специалистов, консультации, контакты, тренинги, право, блог и статью. |
| `assets/js\programs.js` | Данные семи образовательных программ (ru / az / en). |
| `assets/js\reader.js` | test/11 — единая читалка библиотеки: read.html?b=<книга>&c=<глава>. |
| `assets/js\reg.js` | test/11 — единая форма записи: сначала «на что», дальше поля меняются. Всё, что можно, выбирается нажатием и уже выбрано по умолчанию. |
| `assets/js\shop-order.js` | Позиции корзины: название и цена каждой книги, как на странице заказа /books/ (собирает _tools/patch_shop_1112b.py). |
| `assets/js\site.js` | test/11 — главная: отрисовка из content.js, герой на кадрах, лента программ, книги в объёме, мифы, меню. |
| `assets/js\totop.js` | test/11 — кнопка «наверх»: одна на все страницы (главная и внутренние). Появляется после первого экрана, стоит над кнопкой WhatsApp. |
| `assets/css\site.css` | test/11 — ГЛАВНАЯ. Единое управление: токены и три темы в начале файла; все блоки читают только эти переменные. |

## Инструменты — `_tools/`

| файл | назначение |
|---|---|
| `_tools\apply_covers.py` | Новые обложки статей и картины героя (владелец 12.11.2026, п. 11): картинки из gen_blog_covers.py |
| `_tools\build_blog.py` | Блог → данные test/11: статьи <lang>/bloq/*.html → data/blog/<slug>.<lang>.json, список → data/blog/index.<lang>.json. |
| `_tools\build_book_print.py` | Книга сайта из печатной версии (12.11.2026): текст библиотеки собирается из свёрстанного Word папки Print — |
| `_tools\build_klinik.py` | Книга «Клиническая психиатрия» -> библиотека новой системы (12.11.2026). |
| `_tools\build_law.py` | Блок «Юридические основы деятельности» для страниц «Общая психология» и «Клиническая психология». |
| `_tools\build_library.py` | Библиотека книг новой системы: текст хранится отдельно от страницы (решение владельца 12.11.2026). |
| `_tools\build_library_legacy.py` | Библиотека: работы Фрейда вне серии, которые лежат в прежнем формате читалки (страницы глав с <main class="site-main">): |
| `_tools\build_shop.py` | Каталог для прототипа книжного магазина (test/11/shop.html, book.html). |
| `_tools\build_sitemap.py` | Карта сайта sitemap.xml: все страницы новой системы. Запуск из корня сайта: python _tools/build_sitemap.py |
| `_tools\clean_data.py` | Чистка данных внутренних страниц: в строках остаются только strong, em, b, i, a, br, sup, sub. Статьи блога (prose) не трогаются. |
| `_tools\collect_images.py` | Картинки внутренних страниц: всё, на что ссылаются data/**/*.json (/images/…), копируется в assets/img/site/ — новая версия не зависит от старых папок. |
| `_tools\css_collide.py` | Страж столкновения имён в стилях (урок 12.11.2026: правило «.posts» для страницы блога переопределило |
| `_tools\css_scale.py` | Отступы — только из шкалы. Режимы: |
| `_tools\form_check.py` | Проверка формы записи на всех видах страниц БЕЗ создания заявок: сетевой вызов в браузере подменён, |
| `_tools\gen_art.py` | test/11 — иллюстрации через DashScope wan2.7-image (бесплатная квота воркспейса irada). |
| `_tools\gen_blog_covers.py` | test/11 — обложки статей блога и картины героя новых страниц через DashScope wan2.7-image |
| `_tools\libcommon.py` | Общее для сборщиков библиотеки: единый вид паспорта книги (book.json). |
| `_tools\library_find.py` | Поиск по библиотеке: в какой книге, в какой главе и в каком абзаце написано (как по картотеке). |
| `_tools\make_covers.py` | test/11 — сборка обложек: рисунок (_agent/art/<книга>.png) → кадр 2:3 → надписи шрифтом (cover.html) → assets/img/book-<книга>-<язык>.jpg |
| `_tools\make_shells.py` | Оболочки внутренних страниц: рама (шапка, подвал, окно просмотра, кнопка WhatsApp) берётся из program.html — один источник. |
| `_tools\merge_books.py` | Комплектация коротких работ Фрейда в книги (слово владельца 13.11.2026: короче 100 страниц отдельной книгой не продаём). |
| `_tools\pages_check.py` | Автоматическая проверка ВСЕХ внутренних страниц test/11 (Chrome без окна). |
| `_tools\parity_check.py` | Сверка языков: у каждой страницы на ru / az / en должен быть один и тот же состав — |
| `_tools\reg_test.py` | Проверка формы записи на живой странице: одна тестовая заявка на консультацию (имя TEST), до оплаты не доходит. |
| `_tools\reorg_images.py` | Раскладка картинок по разделам сайта «как в библиотеке» (решение владельца 12.11.2026). |
| `_tools\round.py` | Круг проверки главной по канону: замеры во всех сочетаниях (язык × тема × окно) и снимки блоков для критиков. |
| `_tools\sentence_case.py` | Заголовки как предложения (решение владельца 12.11.2026, п. 10: «исправить как полагается с точки зрения |
| `_tools\sentence_case_js.py` | Заголовки как предложения в текстах программ (assets/js/programs.js): названия модулей, блоков, документов. |
| `_tools\stamp.py` | Номер версии к стилям и скриптам — чтобы телефон не показывал старые файлы. Запуск из корня сайта перед публикацией: python _tools/stamp.py |
| `_tools\structure_check.py` | Страж структуры файлов и карта файлов проекта (требование владельца 12.11.2026: «как в библиотеке — |
| `_tools\verify_data.py` | Сторож дословности: каждая строка текста в data/<kind>/<slug>.<lang>.json должна быть в исходной странице (поле src). |

Скрипты `patch_*.py` — разовые правки с датой в имени; они сохранены как журнал изменений и повторно ничего не меняют.
