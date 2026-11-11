/* test/11 — ТЕКСТЫ И ДАННЫЕ главной, три языка. Один источник: страница только рисует то, что здесь.
   Факты — только из КАНОН_ГЛАВНАЯ.md, раздел 12 (часы и цены долгосрочных программ, заголовки блога — с живого сайта ragimoff.org).
   Каждая строка существует один раз: заголовки разделов (eye — пусто, номера не показываем; h — название, sub — одно предложение до 62 знаков) лежат в самих блоках. */

const P = l => '/' + l + '/';                       /* адреса существующих страниц сайта */
const KP = { ru: '/klinik-psixiatriya/ru/', az: '/klinik-psixiatriya/', en: '/klinik-psixiatriya/en/' };
const BK = l => l === 'az' ? '/books/' : '/books/' + l + '/';

export const LINKS = l => {
  const cons = ['panik-ataklar', 'depressiya', 'sosial-fobiya', 'enurez', 'aile-terapiyasi'].map(x => P(l) + 'konsultasiya/' + x + '.html').concat(P(l) + 'konsultasiya/index.html');   /* страницы «тревожные расстройства и ОКР» нет — ведёт на список консультаций */
  return {
    spec: [P(l) + 'mutexessisler/kenan-rehimov.html', P(l) + 'mutexessisler/samire-rehimova.html'],
    /* порядок: Клиническая психиатрия, Фрейд, Эра Феникса, Вирус вины, Шизофрения */
    books: [KP[l] + 'index.html', BK(l)].concat(['phoenix-era', 'virus-viny', 'shizofreniya'].map(b => '/books/' + b + (l === 'az' ? '/' : '/' + l + '/') + 'index.html')),
    prog: ['umumi-psixologiya', 'klinik-psixologiya', 'psixoterapiya-praktikumu', 'psixodiaqnostika', 'qisamuddetli', 'psixoanaliz', 'aile-terapiyasi'].map(x => P(l) + 'telim/' + x + '.html'),
    cons,
    form: P(l) + 'konsultasiya/depressiya.html#registration', corp: P(l) + 'korporativ/index.html', blogAll: P(l) + 'bloq/index.html',
    blog: ['depressiya', 'enurez', 'aile'].map(x => P(l) + 'bloq/' + x + '.html'),
    myths: ['6A70.html#6a70-10-mifler', '6B04.html#6b04-10-mifler', '6B00.html#6b00-10-mifler', '6B20.html#6b20-10-mifler', '6C00.html#6c00-10-mifler'].map(x => KP[l] + x),
    /* подвал: параллельно T[l].foot.cols[i].l */
    foot: [cons, [P(l) + 'telim/index.html', P(l) + 'telim/qisamuddetli.html', P(l) + 'telim/qanuni-esaslar.html'], ['https://wa.me/994702200376', l === 'ru' ? 'https://t.me/doctor_ragimoff' : 'https://t.me/ragimoff', P(l) + 'elaqe/index.html']],
    contact: P(l) + 'elaqe/index.html', law: P(l) + 'telim/qanuni-esaslar.html', wa: 'https://wa.me/994702200376', tg: l === 'ru' ? 'https://t.me/doctor_ragimoff' : 'https://t.me/ragimoff', shop: BK(l),
  };
};

export const T = {
  /* ───────────────────────────── РУССКИЙ ───────────────────────────── */
  ru: {
    nav: { spec: 'Специалисты', books: 'Книги', edu: 'Обучение', cons: 'Консультации', corp: 'Тренинги', enl: 'Просвещение', blog: 'Блог', contact: 'Контакты', cta: 'Записаться', law: 'Правовые основы' },
    hero: { school: 'Школа психологии', q: 'Doctor Ragimoff', scroll: 'Листайте вниз', b: ['Консультации', 'Обучение', 'Книги', 'Тренинги'] },
    belt: ['Психотерапия', 'Обучение психологов', 'Книги', 'Супервизия', 'Семейная терапия', 'Тренинги'],
    spec: { eye: '', h: 'Специалисты', sub: 'Подробнее о каждом — на личной странице.', more: 'Подробнее',
      mentors: 'Кенан Рагимов учился в Институте имени Бехтерева в 2001–2003 годах у профессоров Бориса Дмитриевича Карвасарского и Виктора Давыдовича Вида.',
      p: [{ n: 'Кенан Рагимов', r: 'Психотерапевт', f: ['Врач-психотерапевт с 2003 года, Санкт-Петербург', 'Амбассадор Международной психотерапевтической ассоциации с 2022 года', 'Автор учебников и книг по психотерапии'] },
          { n: 'Самира Рагимова', r: 'Психолог', f: ['Клинический психолог', 'Семейный терапевт', 'Автор книги «Эра Феникса»'] }] },
    books: { eye: '', h: 'Книги', sub: 'Учебник, авторские книги и Фрейд на азербайджанском.', read: 'Читать бесплатно', order: 'Заказать печатную книгу',
      b: [{ k: 'Учебник', t: 'Клиническая психиатрия', a: 'Кенан Рагимов', f: ['МКБ-10, МКБ-11 и DSM-5 собраны в одной книге.', '820 печатных страниц формата B5 — для учёбы и для работы с пациентами.', 'Читать можно на азербайджанском, русском, английском и турецком.'] },
          { k: 'Впервые на азербайджанском', t: 'Зигмунд Фрейд', a: 'Перевод на азербайджанский', f: ['В издание вошли 22 книги Фрейда.', 'Перевод сделан с немецкого оригинала.', 'Читать бесплатно: откройте и сверьте перевод сами.'] },
          { k: 'Методология психотерапии', t: 'Эра Феникса', a: 'Самира Рагимова, соавтор — Кенан Рагимов', f: ['Книга о пути к осознанным взаимоотношениям.', 'Двенадцать моделей взаимоотношений — от «Лилит» до «Феникса».', 'В конце — диагностический тест, игровая практика и колода «Феникс».'] },
          { k: 'Просвещение', t: 'Вирус вины', a: 'Кенан Рагимов', f: ['Книга о том, как освободиться от чувства вины.', 'Три части: диагноз, источники вины и путь к выздоровлению.', 'В приложении — тесты для самопроверки и рекомендуемая литература.'] },
          { k: 'Просвещение', t: 'Шизофрения. Пандемия безумия', a: 'Кенан Рагимов', f: ['История шизофрении: от неолитических хирургов до наших дней.', 'Крепелин и Блейлер, малярия, инсулин, лоботомия: как менялись диагноз и лечение.', 'В приложении — как распознать настоящего специалиста.'] }],
      next: 'Скоро среди наших книг — «Общая психотерапия»: том на русском уже готов.',
      lib: 'В течение 2027 года библиотека пополнится профессиональной литературой.' },
    edu: { eye: '', h: 'Обучение', sub: 'Семь программ с дипломом или международным сертификатом.', more: 'Подробнее',
      p: [{ t: 'Общая психология', d: 'Диплом Института ДПО Санкт-Петербурга', m: ['1\u00A0556 часов', '1 год: 6 + 6 месяцев'], price: 'от 200 AZN в месяц' },
          { t: 'Клиническая психология', d: 'Диплом Института ДПО Санкт-Петербурга', m: ['1\u00A0528 часов', '1 год: 6 + 6 месяцев'], price: 'от 300 AZN в месяц' },
          { t: 'Практикум по психотерапии', d: 'Международный сертификат', m: ['864 часа', '1 год — практика'], price: 'от 175 AZN в месяц' },
          { t: 'Психодиагностика', d: 'Международный сертификат', m: ['3 месяца + 6 месяцев супервизии', '800 AZN при предоплате'], price: '300 AZN в месяц' },
          { t: 'Когнитивно-поведенческая терапия', d: 'Международный сертификат', m: ['3 месяца + 6 месяцев супервизии', '800 AZN при предоплате'], price: '300 AZN в месяц' },
          { t: 'Психоанализ', d: 'Международный сертификат', m: ['3 месяца + 6 месяцев супервизии', '800 AZN при предоплате'], price: '300 AZN в месяц' },
          { t: 'Семейная терапия', d: 'Международный сертификат', m: ['3 месяца + 6 месяцев супервизии', '800 AZN при предоплате'], price: '300 AZN в месяц' }] },
    cons: { eye: '', h: 'Консультации', sub: 'Выберите тему или напишите свою.', cta: 'Записаться на консультацию', wa: 'Написать в WhatsApp',
      who: 'Вы выбираете, к кому записаться: к Кенану Рагимову, к Самире Рагимовой или к обоим.',
      other: ['Другая тема', 'Напишите в WhatsApp, что вас беспокоит, — подскажем, к кому записаться.'], note: 'После регистрации вы перейдёте в платёжную систему. Оплатив, отправьте чек в WhatsApp на +994 70 220 03 76 — мы подтвердим время.',
      t: [['Панические атаки', 'Приступ реален: тело отвечает страхом там, где опасности нет.'],
          ['Депрессия', 'Не слабость воли, а состояние, с которым работает психотерапия.'],
          ['Социальная фобия', 'Страх выступлений и чужой оценки — не черта характера.'],
          ['Ночной энурез', 'За годы практики — более 1\u00A0000 пациентов: 250 в 2025 году, более 100 — в этом году.'],
          ['Семейная терапия', 'Работаем с парами и с детско-родительскими отношениями.'],
          ['Тревожные расстройства и ОКР', 'У тревоги и навязчивостей есть чёткие критерии диагноза и лечение.']] },
    corp: { eye: '', h: 'Тренинги', sub: 'Для компаний, команд и корпоративных мероприятий.', lead: 'Школа HR работает с 2008 года и подготовила более 2\u00A0000 человек.', cta: 'Заказать тренинг',
      clientsH: 'Среди клиентов и событий:', clients: ['MG', 'Unibank', 'DNS Computers', 'Business Party by Ragimoff'], n: [],
      t: ['Управление персоналом', 'Лидерство', 'Командная работа', 'Коммуникации и продажи'] },
    enl: { eye: '', h: 'Просвещение', sub: 'Пять заблуждений о психических расстройствах и их лечении.', flip: 'Что на самом деле', back: 'Миф', more: 'Читать в учебнике',
      m: [['Депрессия', '«Антидепрессанты меняют личность человека»', 'Антидепрессанты уменьшают симптомы, но не меняют личность. Если человек «не чувствует себя собой», это побочный эффект: врач меняет препарат или снижает дозу.'],
          ['Социальная тревога', '«Социальная тревога — обычная застенчивость, лечения не требует»', 'Социальное тревожное расстройство мешает учёбе и работе, повышает риск депрессии и употребления алкоголя. Это медицинское состояние, а не просто застенчивость.'],
          ['Тревожные расстройства', '«Генерализованную тревогу лечат только релаксацией или йогой»', 'Релаксация и йога дают лишь умеренный вспомогательный эффект. При средней и тяжёлой степени нужны когнитивно-поведенческая терапия, лекарства или то и другое вместе.'],
          ['ОКР', '«ОКР — просто черта характера, связанная с чистоплотностью»', 'ОКР вызывает тревогу и нарушает повседневную жизнь. Диагноз ставят по клиническим критериям, а не по чертам характера.'],
          ['Ночной энурез', '«Наказание или оскорбления исправят ребёнка»', 'Наказание противопоказано: оно снижает самооценку и повышает риск депрессии. Лучше работает положительное подкрепление.']] },
    blog: { eye: '', h: 'Блог', sub: '', all: 'Все статьи', p: [['Депрессия', 'Чем депрессия отличается от грусти?'], ['Ночной энурез', 'Ребёнок мочится в постель ночью — 5 ложных убеждений'], ['Семейные отношения', '5 принципов разрешения семейных конфликтов']] },
    tg: { h: 'Новые материалы — в Telegram', sub: 'Подписывайтесь на наш канал.', cta: 'Перейти в канал' },
    a11y: { title: 'Doctor Ragimoff — Школа психологии', menu: 'Меню', theme: 'Тема', night: 'Ночь', paper: 'Бумага', sepia: 'Сепия', lang: 'Язык' },
    foot: {
      cols: [{ h: 'Терапия', l: ['Панические атаки', 'Депрессия', 'Социальная фобия', 'Ночной энурез', 'Семейная терапия', 'Тревожные расстройства и ОКР'] },
             { h: 'Образование', l: ['Долгосрочные программы', 'Краткосрочные программы', 'Правовые основы'] },
             { h: 'Контакты', l: ['WhatsApp +994 70 220 03 76', 'Telegram', 'Баку, Джафар Джаббарлы 40, Caspian Business Center, 9 этаж'] }],
      copy: ['© 2026 Doctor Ragimoff.', 'Все права защищены.'] },
  },

  /* ───────────────────────────── AZƏRBAYCAN ───────────────────────────── */
  az: {
    nav: { spec: 'Mütəxəssislər', books: 'Kitablar', edu: 'Təhsil', cons: 'Konsultasiyalar', corp: 'Təlimlər', enl: 'Maarifləndirmə', blog: 'Bloq', contact: 'Əlaqə', cta: 'Qəbula yazılın', law: 'Hüquqi əsaslar' },
    hero: { school: 'Psixologiya Məktəbi', q: 'Doctor Ragimoff', scroll: 'Sürüşdürün', b: ['Konsultasiyalar', 'Təhsil', 'Kitablar', 'Təlimlər'] },
    belt: ['Psixoterapiya', 'Psixoloqların təhsili', 'Kitablar', 'Superviziya', 'Ailə terapiyası', 'Təlimlər'],
    spec: { eye: '', h: 'Mütəxəssislər', sub: 'Hər biri haqqında ətraflı — öz səhifəsində.', more: 'Ətraflı',
      mentors: 'Kənan Rəhimov 2001–2003-cü illərdə Bexterev adına İnstitutda professorlar Boris Dmitriyeviç Karvasarski və Viktor Davidoviç Viddən dərs alıb.',
      p: [{ n: 'Kənan Rəhimov', r: 'Psixoterapevt', f: ['2003-cü ildən Sankt-Peterburqda həkim-psixoterapevt', '2022-ci ildən Beynəlxalq Psixoterapevtik Assosiasiyanın səfiri', 'Psixoterapiya üzrə dərsliklərin və kitabların müəllifi'] },
          { n: 'Samirə Rəhimova', r: 'Psixoloq', f: ['Klinik psixoloq', 'Ailə terapevti', '«Feniks erası» kitabının müəllifi'] }] },
    books: { eye: '', h: 'Kitablar', sub: 'Dərslik, müəllif kitabları və Azərbaycan dilində Freyd.', read: 'Pulsuz oxuyun', order: 'Çap nüsxəsini sifariş edin',
      b: [{ k: 'Dərslik', t: 'Klinik Psixiatriya', a: 'Kənan Rəhimov', f: ['XBT-10, XBT-11 və DSM-5 bir kitabda toplanıb.', 'B5 formatında 820 çap səhifəsi: həm öyrənmək, həm praktik iş üçün.', 'Azərbaycan, rus, ingilis və türk dillərində oxumaq olar.'] },
          { k: 'Azərbaycan dilində ilk dəfə', t: 'Ziqmund Freyd', a: 'Azərbaycan dilinə tərcümə', f: ['Nəşrə Freydin 22 kitabı daxildir.', 'Tərcümə alman dilindəki orijinaldan edilib.', 'Pulsuz oxumaq olar: açın və tərcüməni özünüz yoxlayın.'] },
          { k: 'Psixoterapiya metodologiyası', t: 'Feniks erası', a: 'Samirə Rəhimova, həmmüəllif — Kənan Rəhimov', f: ['Şüurlu münasibətlərə aparan yol haqqında kitab.', 'On iki münasibət modeli — «Lilit»dən «Feniks»ə qədər.', 'Sonda diaqnostik test, oyun praktikası və «Feniks» dəsti var.'] },
          { k: 'Maarifləndirmə', t: 'Günahkarlıq virusu', a: 'Kənan Rəhimov', f: ['Günahkarlıq hissindən azad olmaq haqqında kitab.', 'Üç hissə: diaqnoz, günahkarlığın mənbələri və sağalma yolu.', 'Əlavədə özünü yoxlama testləri və tövsiyə olunan ədəbiyyat var.'] },
          { k: 'Maarifləndirmə', t: 'Şizofreniya. Cinnət pandemiyası', a: 'Kənan Rəhimov', f: ['Şizofreniyanın tarixi: neolit cərrahlarından bu günə qədər.', 'Kraepelin və Bleyler, malyariya, insulin, lobotomiya: diaqnoz və müalicə necə dəyişib.', 'Əlavədə mütəxəssisi necə ayırd etməyin yolları göstərilir.'] }],
      next: '«Ümumi psixoterapiya» tezliklə kitablarımız sırasında olacaq: rus dilində cild artıq hazırdır.',
      lib: '2027-ci il ərzində kitabxana peşəkar ədəbiyyatla zənginləşəcək.' },
    edu: { eye: '', h: 'Təhsil', sub: 'Diplom və ya beynəlxalq sertifikatla yeddi proqram.', more: 'Ətraflı',
      p: [{ t: 'Ümumi psixologiya', d: 'Sankt-Peterburq Əlavə Təhsil İnstitutunun diplomu', m: ['1\u00A0556 saat', '1 il: 6 + 6 ay'], price: 'ayda 200 AZN-dən' },
          { t: 'Klinik psixologiya', d: 'Sankt-Peterburq Əlavə Təhsil İnstitutunun diplomu', m: ['1\u00A0528 saat', '1 il: 6 + 6 ay'], price: 'ayda 300 AZN-dən' },
          { t: 'Psixoterapiya praktikumu', d: 'Beynəlxalq sertifikat', m: ['864 saat', '1 il — praktika'], price: 'ayda 175 AZN-dən' },
          { t: 'Psixodiaqnostika', d: 'Beynəlxalq sertifikat', m: ['3 ay + 6 ay superviziya', 'əvvəlcədən ödənişdə 800 AZN'], price: 'ayda 300 AZN' },
          { t: 'Koqnitiv-davranış terapiyası', d: 'Beynəlxalq sertifikat', m: ['3 ay + 6 ay superviziya', 'əvvəlcədən ödənişdə 800 AZN'], price: 'ayda 300 AZN' },
          { t: 'Psixoanaliz', d: 'Beynəlxalq sertifikat', m: ['3 ay + 6 ay superviziya', 'əvvəlcədən ödənişdə 800 AZN'], price: 'ayda 300 AZN' },
          { t: 'Ailə terapiyası', d: 'Beynəlxalq sertifikat', m: ['3 ay + 6 ay superviziya', 'əvvəlcədən ödənişdə 800 AZN'], price: 'ayda 300 AZN' }] },
    cons: { eye: '', h: 'Konsultasiyalar', sub: 'Mövzunu seçin və ya öz mövzunuzu yazın.', cta: 'Konsultasiyaya yazılın', wa: 'WhatsApp-da yazın',
      who: 'Qəbulu Kənan Rəhimov, Samirə Rəhimova və ya hər iki mütəxəssis birlikdə aparır — seçim sizindir.',
      other: ['Başqa mövzu', 'Sizi nə narahat edir — WhatsApp-da yazın, hansı mütəxəssisin uyğun olduğunu deyərik.'], note: 'Qeydiyyatdan sonra ödəniş sisteminə keçəcəksiniz. Ödənişdən sonra qəbzi +994 70 220 03 76 nömrəsinə WhatsApp ilə göndərin — görüş vaxtını təsdiqləyəcəyik.',
      t: [['Panik tutmaları', 'Tutma real hadisədir: bədən təhlükə olmayan yerdə qorxu ilə cavab verir.'],
          ['Depressiya', 'İradə zəifliyi deyil, psixoterapiya ilə müalicə olunan vəziyyətdir.'],
          ['Sosial fobiya', 'İctimai çıxış və başqalarının qiymətləndirməsi qorxusu xarakter xüsusiyyəti deyil.'],
          ['Gecə enurezi', 'Təcrübə illərində 1\u00A0000-dən çox pasiyent, 2025-ci ildə 250, bu il isə 100-dən çox.'],
          ['Ailə terapiyası', 'Cütlüklərlə və valideyn–uşaq münasibətləri ilə işləyirik.'],
          ['Təşviş pozuntuları və OKP', 'Təşviş və obsessiyaların aydın diaqnostik meyarları və müalicəsi var.']] },
    corp: { eye: '', h: 'Təlimlər', sub: 'Şirkətlər, komandalar və korporativ tədbirlər üçün.', lead: 'HR məktəbi 2008-ci ildən fəaliyyət göstərir və 2\u00A0000-dən çox nəfər hazırlayıb.', cta: 'Təlim sifariş edin',
      clientsH: 'Müştərilər və tədbirlər:', clients: ['MG', 'Unibank', 'DNS Computers', 'Business Party by Ragimoff'], n: [],
      t: ['Heyətin idarə olunması', 'Liderlik', 'Komanda işi', 'Ünsiyyət və satış'] },
    enl: { eye: '', h: 'Maarifləndirmə', sub: 'Psixi pozuntular və müalicə haqqında beş yanlış təsəvvür.', flip: 'Əslində necədir', back: 'Mif', more: 'Dərslikdə oxuyun',
      m: [['Depressiya', '«Antidepressant şəxsiyyəti dəyişdirir»', 'Antidepressantlar simptomları azaldır, şəxsiyyəti dəyişmir. İnsan «özümü hiss etmirəm» deyirsə, bu yan təsirdir: həkim preparatı dəyişir və ya dozanı azaldır.'],
          ['Sosial təşviş', '«Sosial təşviş adi utancaqlıqdır, müalicə tələb etmir»', 'Sosial təşviş pozuntusu təhsilə və işə mane olur, depressiya və alkoqol istifadəsi riskini artırır. Bu, sadəcə utancaqlıq deyil, tibbi vəziyyətdir.'],
          ['Təşviş pozuntuları', '«Ümumiləşmiş təşvişi yalnız relaksasiya və ya yoga sağaldır»', 'Relaksasiya və yoga yalnız mülayim köməkçi təsir göstərir. Orta və ağır halda koqnitiv-davranış terapiyası, dərmanlar və ya hər ikisi lazımdır.'],
          ['OKP', '«OKP sadəcə təmizkarlıqla bağlı xarakter xüsusiyyətidir»', 'OKP təşviş doğurur və gündəlik həyatı pozur. Diaqnoz xarakter xüsusiyyətlərinə görə deyil, klinik meyarlarla qoyulur.'],
          ['Gecə enurezi', '«Cəza və ya təhqir uşağı düzəldər»', 'Cəza əks-göstərişdir: özünə qiyməti azaldır, depressiya riskini artırır. Müsbət gücləndirmə daha yaxşı işləyir.']] },
    blog: { eye: '', h: 'Bloq', sub: '', all: 'Bütün məqalələr', p: [['Depressiya', 'Depressiya kədərdən necə fərqlənir?'], ['Gecə enurezi', 'Uşağınız gecələr yatağı isladırsa — 5 yanlış inanc'], ['Ailə münasibətləri', 'Ailə münaqişəsini həll etmənin 5 prinsipi']] },
    tg: { h: 'Yeni materiallar — Telegram-da', sub: 'Kanalımıza abunə olun.', cta: 'Kanala keçin' },
    a11y: { title: 'Doctor Ragimoff — Psixologiya Məktəbi', menu: 'Menyu', theme: 'Rəng mövzusu', night: 'Gecə', paper: 'Kağız', sepia: 'Sepiya', lang: 'Dil' },
    foot: {
      cols: [{ h: 'Terapiya', l: ['Panik tutmaları', 'Depressiya', 'Sosial fobiya', 'Gecə enurezi', 'Ailə terapiyası', 'Təşviş pozuntuları və OKP'] },
             { h: 'Təhsil', l: ['Uzunmüddətli proqramlar', 'Qısamüddətli proqramlar', 'Hüquqi əsaslar'] },
             { h: 'Əlaqə', l: ['WhatsApp +994 70 220 03 76', 'Telegram', 'Bakı, Cəfər Cabbarlı küçəsi 40, Caspian Business Center, 9-cu mərtəbə'] }],
      copy: ['© 2026 Doctor Ragimoff.', 'Bütün hüquqlar qorunur.'] },
  },

  /* ───────────────────────────── ENGLISH ───────────────────────────── */
  en: {
    nav: { spec: 'Specialists', books: 'Books', edu: 'Education', cons: 'Consultations', corp: 'Training', enl: 'Psychoeducation', blog: 'Blog', contact: 'Contact', cta: 'Book a visit', law: 'Legal basis' },
    hero: { school: 'School of Psychology', q: 'Doctor Ragimoff', scroll: 'Scroll down', b: ['Consultations', 'Education', 'Books', 'Training'] },
    belt: ['Psychotherapy', 'Training for psychologists', 'Books', 'Supervision', 'Family therapy', 'Training'],
    spec: { eye: '', h: 'Specialists', sub: 'More about each is on their own page.', more: 'Learn more',
      mentors: 'Kenan Ragimov studied at the Bekhterev Institute in 2001–2003 under Professors Boris Dmitrievich Karvasarsky and Viktor Davydovich Vid.',
      p: [{ n: 'Kenan Ragimov', r: 'Psychotherapist', f: ['Medical doctor and psychotherapist since 2003, Saint Petersburg', 'Ambassador of the International Psychotherapy Association since 2022', 'Author of textbooks and books on psychotherapy'] },
          { n: 'Samira Ragimova', r: 'Psychologist', f: ['Clinical psychologist', 'Family therapist', 'Author of the book “Phoenix Era”'] }] },
    books: { eye: '', h: 'Books', sub: 'Textbook, books by Kenan and Samira, Freud in Azerbaijani.', read: 'Read for free', order: 'Order a printed copy',
      b: [{ k: 'Textbook', t: 'Clinical Psychiatry', a: 'Kenan Ragimov', f: ['ICD-10, ICD-11 and DSM-5 are brought together in one book.', '820 printed pages in B5 format, for study and for work with patients.', 'You can read it in Azerbaijani, Russian, English and Turkish.'] },
          { k: 'First in Azerbaijani', t: 'Sigmund Freud', a: 'Azerbaijani translation', f: ['The edition includes 22 books by Freud.', 'The translation was made from the German original.', 'Free to read: open a volume and judge the translation for yourself.'] },
          { k: 'Psychotherapy methodology', t: 'Phoenix Era', a: 'Samira Ragimova, co-author Kenan Ragimov', f: ['A book on the path to conscious relationships.', 'Twelve relationship models, from “Lilith” to “Phoenix”.', 'At the end: a diagnostic test, game-based practice and the “Phoenix” deck.'] },
          { k: 'Psychoeducation', t: 'The Guilt Virus', a: 'Kenan Ragimov', f: ['A book on how to free yourself from guilt.', 'Three parts: the diagnosis, the sources of guilt and the way to recovery.', 'The appendix has self-assessment tests and recommended reading.'] },
          { k: 'Psychoeducation', t: 'Schizophrenia. A Pandemic of Madness', a: 'Kenan Ragimov', f: ['The history of schizophrenia, from Neolithic surgeons to the present day.', 'Kraepelin and Bleuler, malaria, insulin, lobotomy: how diagnosis and treatment changed.', 'The appendix explains how to recognise a true specialist.'] }],
      next: 'Coming soon among our books: “General Psychotherapy”. The Russian volume is already finished.',
      lib: 'Throughout 2027 the library will grow with professional literature.' },
    edu: { eye: '', h: 'Education', sub: 'Seven programmes: diploma or international certificate.', more: 'Learn more',
      p: [{ t: 'General psychology', d: 'Diploma of the Institute of Continuing Professional Education, Saint Petersburg', m: ['1,556 hours', '1 year: 6 + 6 months'], price: 'from 200 AZN a month' },
          { t: 'Clinical psychology', d: 'Diploma of the Institute of Continuing Professional Education, Saint Petersburg', m: ['1,528 hours', '1 year: 6 + 6 months'], price: 'from 300 AZN a month' },
          { t: 'Psychotherapy practicum', d: 'International certificate', m: ['864 hours', '1 year — practice'], price: 'from 175 AZN a month' },
          { t: 'Psychodiagnostics', d: 'International certificate', m: ['3 months + 6 months of supervision', '800 AZN if prepaid'], price: '300 AZN a month' },
          { t: 'Cognitive behavioural therapy', d: 'International certificate', m: ['3 months + 6 months of supervision', '800 AZN if prepaid'], price: '300 AZN a month' },
          { t: 'Psychoanalysis', d: 'International certificate', m: ['3 months + 6 months of supervision', '800 AZN if prepaid'], price: '300 AZN a month' },
          { t: 'Family therapy', d: 'International certificate', m: ['3 months + 6 months of supervision', '800 AZN if prepaid'], price: '300 AZN a month' }] },
    cons: { eye: '', h: 'Consultations', sub: 'Choose a topic or write your own.', cta: 'Book a consultation', wa: 'Message on WhatsApp',
      who: 'You choose whom to see: Kenan Ragimov, Samira Ragimova or both.',
      other: ['Another topic', 'Tell us on WhatsApp what is troubling you, and we will suggest whom to see.'], note: 'After you register, you will be taken to the payment page. Once you have paid, send the receipt via WhatsApp to +994 70 220 03 76 and we will confirm the time.',
      t: [['Panic attacks', 'The attack is real: the body answers with fear where there is no danger.'],
          ['Depression', 'Not a weakness of will but a condition that psychotherapy treats.'],
          ['Social phobia', 'Fear of speaking and of being judged is not a character trait.'],
          ['Nocturnal enuresis', 'More than 1,000 patients over the years of practice, 250 in 2025, more than 100 this year.'],
          ['Family therapy', 'We work with couples and with parent–child relationships.'],
          ['Anxiety disorders and OCD', 'Anxiety and obsessions have clear diagnostic criteria and treatment.']] },
    corp: { eye: '', h: 'Training', sub: 'For companies, teams and corporate events.', lead: 'The HR School has worked since 2008 and has trained more than 2,000 people.', cta: 'Request a training',
      clientsH: 'Clients and events include:', clients: ['MG', 'Unibank', 'DNS Computers', 'Business Party by Ragimoff'], n: [],
      t: ['People management', 'Leadership', 'Teamwork', 'Communication and sales'] },
    enl: { eye: '', h: 'Psychoeducation', sub: 'Five misconceptions about mental disorders and treatment.', flip: 'What is true', back: 'The myth', more: 'Read in the textbook',
      m: [['Depression', '“Antidepressants change a person’s personality”', 'Antidepressants reduce symptoms but do not change personality. If someone “no longer feels like themselves”, it is a side effect: the doctor changes the drug or lowers the dose.'],
          ['Social anxiety', '“Social anxiety is ordinary shyness and needs no treatment”', 'Social anxiety disorder interferes with study and work and raises the risk of depression and alcohol use. It is a medical condition, not just shyness.'],
          ['Anxiety disorders', '“Generalised anxiety is treated only by relaxation or yoga”', 'Relaxation and yoga have only a moderate supporting effect. In moderate to severe cases, cognitive behavioural therapy, medication or both are needed.'],
          ['OCD', '“OCD is just a character trait about cleanliness”', 'OCD causes distress and disrupts daily life. It is diagnosed by clinical criteria, not by character traits.'],
          ['Nocturnal enuresis', '“Punishment or insults will correct the child”', 'Punishment is contraindicated: it lowers self-esteem and raises the risk of depression. Positive reinforcement works better.']] },
    blog: { eye: '', h: 'Blog', sub: '', all: 'All articles', p: [['Depression', 'How does depression differ from sadness?'], ['Nocturnal enuresis', 'When a child wets the bed at night: 5 false beliefs'], ['Family relationships', '5 principles of resolving family conflicts']] },
    tg: { h: 'New materials are on Telegram', sub: 'Subscribe to our channel (in Azerbaijani).', cta: 'Open the channel' },
    a11y: { title: 'Doctor Ragimoff — School of Psychology', menu: 'Menu', theme: 'Theme', night: 'Night', paper: 'Paper', sepia: 'Sepia', lang: 'Language' },
    foot: {
      cols: [{ h: 'Therapy', l: ['Panic attacks', 'Depression', 'Social phobia', 'Nocturnal enuresis', 'Family therapy', 'Anxiety disorders and OCD'] },
             { h: 'Education', l: ['Long-term programmes', 'Short-term programmes', 'Legal basis'] },
             { h: 'Contact', l: ['WhatsApp +994 70 220 03 76', 'Telegram', 'Baku, Jafar Jabbarly 40, Caspian Business Center, 9th floor'] }],
      copy: ['© 2026 Doctor Ragimoff.', 'All rights reserved.'] },
  },
};

/* ── материалы владельца (живой сайт и досье со старого сайта): документы, фильм, ролики ── */
const MEDIA = {
  ru: { proofs: ['Диплом о профессиональной переподготовке — образец', 'Международный сертификат — образец', 'Группа «Школы психологии» с преподавателем'],
        film: { id: 'rb68nHEF9-o', t: 'Драма Сабины', d: 'Экранизация реального случая. 31 минута.', cta: 'Смотреть фильм' },
        vids: [['Unibank — командный тренинг', '1JMEVec4F1c'], ['Business Party by Ragimoff', 'kEk6B3kNEoE']],
        more: 'Более 3\u00A0000 человек прошли тренинги лично у Кенана Рагимова.' },
  az: { proofs: ['Peşə yenidənhazırlığı haqqında diplom — nümunə', 'Beynəlxalq sertifikat — nümunə', '«Psixologiya Məktəbi»nin qrupu müəllimlə birlikdə'],
        film: { id: 'rb68nHEF9-o', t: 'Səbinənin draması', d: 'Real hadisə əsasında çəkilmiş film. 31 dəqiqə.', cta: 'Filmə baxın' },
        vids: [['Unibank — komanda təlimi', '1JMEVec4F1c'], ['Business Party by Ragimoff', 'kEk6B3kNEoE']],
        more: 'Kənan Rəhimovun şəxsən keçirdiyi təlimlərdə 3\u00A0000-dən çox insan iştirak edib.' },
  en: { proofs: ['Diploma of professional retraining — sample', 'International certificate — sample', 'A School of Psychology group with their teacher'],
        film: { id: 'rb68nHEF9-o', t: 'Sabina’s drama', d: 'A screen adaptation of a real case. 31 minutes.', cta: 'Watch the film' },
        vids: [['Unibank — team training', '1JMEVec4F1c'], ['Business Party by Ragimoff', 'kEk6B3kNEoE']],
        more: 'More than 3,000 people have attended trainings that Kenan Ragimov led in person.' },
};
for (const l of Object.keys(MEDIA)) { const m = MEDIA[l]; T[l].edu.proofs = m.proofs; T[l].cons.film = m.film; T[l].corp.vids = m.vids; T[l].corp.lead = T[l].corp.lead + ' ' + m.more; }

/* ── OWNER_1111B: слова владельца 11.11 (вечер) — руководители, «Наши книги», частые заблуждения, галерея, короткие названия ── */
const OWN = {
  ru: {
    lead: { h: 'Квалификация', items: [['2001–2003', 'Кенан Рагимов получил образование по психотерапии в Институте имени В. М. Бехтерева.'], ['Руководитель', 'Профессор Б. Д. Карвасарский — главный психотерапевт Министерства здравоохранения Российской Федерации до 2012 года.'], ['Руководитель', 'Профессор В. Д. Вид — первый в странах СНГ психоаналитик, официально дипломированный Международной психоаналитической ассоциацией.'], ['С 2003 года', 'Сотрудничает с Институтом имени Б. Д. Карвасарского и Санкт-Петербургским институтом дополнительного профессионального образования: преподаёт и входит в аттестационную комиссию.']] },
    booksH: 'Наши книги', booksSub: 'Книги наших специалистов и переводы учебников.',
    enlSub: 'Частые заблуждения на пути к квалифицированной помощи.',
    myth: 'Миф', go: 'Подробнее', kpt: 'КПТ', galBtn: 'Фотогалерея',
    gal: [['diploma', 'Диплом о профессиональной переподготовке — образец'], ['cert', 'Международный сертификат — образец'], ['group', 'Группа «Школы психологии» с преподавателем'],
          ['supplement', 'Приложение к диплому: дисциплины и часы'], ['cert-family', 'Международный сертификат по семейной терапии — образец'], ['meeting', 'Кенан Рагимов на встрече с группой'], ['outdoor', 'Группа слушателей']] },
  az: {
    lead: { h: 'Kvalifikasiya', items: [['2001–2003', 'Kənan Rəhimov V. M. Bexterev adına İnstitutda psixoterapiya üzrə təhsil alıb.'], ['Rəhbəri', 'Professor B. D. Karvasarski — 2012-ci ilədək Rusiya Federasiyası Səhiyyə Nazirliyinin baş psixoterapevti.'], ['Rəhbəri', 'Professor V. D. Vid — MDB ölkələrində Beynəlxalq Psixoanaliz Assosiasiyasının rəsmi diplomunu almış ilk psixoanalitik.'], ['2003-cü ildən', 'B. D. Karvasarski adına İnstitut və Sankt-Peterburq Əlavə Təhsil İnstitutu ilə əməkdaşlıq edir, tədris aparır və attestasiya komissiyasının üzvüdür.']] },
    booksH: 'Kitablarımız', booksSub: 'Mütəxəssislərimizin kitabları və dərslik tərcümələri.',
    enlSub: 'İxtisaslı köməyə mane olan ən çox yayılmış yanlış təsəvvürlər.',
    myth: 'Mif', go: 'Ətraflı', kpt: 'KDT', galBtn: 'Fotoqalereya',
    gal: [['diploma', 'Peşə yenidənhazırlığı haqqında diplom — nümunə'], ['cert', 'Beynəlxalq sertifikat — nümunə'], ['group', '«Psixologiya Məktəbi»nin qrupu müəllimlə birlikdə'],
          ['supplement', 'Diploma əlavə: fənlər və saatlar'], ['cert-family', 'Ailə terapiyası üzrə beynəlxalq sertifikat — nümunə'], ['meeting', 'Kənan Rəhimov qrupla görüşdə'], ['outdoor', 'Dinləyicilər qrupu']] },
  en: {
    lead: { h: 'Qualifications', items: [['2001–2003', 'Kenan Ragimov trained in psychotherapy at the V. M. Bekhterev Institute.'], ['Supervisor', 'Professor B. D. Karvasarsky — chief psychotherapist of the Ministry of Health of the Russian Federation until 2012.'], ['Supervisor', 'Professor V. D. Vid — the first psychoanalyst in the CIS countries officially certified by the International Psychoanalytical Association.'], ['Since 2003', 'He works with the B. D. Karvasarsky Institute and the Saint Petersburg Institute of Continuing Professional Education: he teaches and sits on the attestation commission.']] },
    booksH: 'Our books', booksSub: 'Books by our specialists and translated textbooks.',
    enlSub: 'Common misconceptions on the way to qualified help.',
    myth: 'Myth', go: 'Read more', kpt: 'CBT', galBtn: 'Photo gallery',
    gal: [['diploma', 'Diploma of professional retraining — sample'], ['cert', 'International certificate — sample'], ['group', 'A School of Psychology group with their teacher'],
          ['supplement', 'Diploma supplement: subjects and hours'], ['cert-family', 'International certificate in family therapy — sample'], ['meeting', 'Kenan Ragimov at a meeting with a group'], ['outdoor', 'A group of students']] },
};
for (const l of Object.keys(OWN)) { const o = OWN[l], t = T[l];
  t.spec.lead = o.lead; t.books.h = o.booksH; t.books.sub = o.booksSub; t.enl.sub = o.enlSub; t.enl.myth = o.myth; t.enl.go = o.go; t.edu.gal = o.gal; t.edu.galBtn = o.galBtn;
  t.edu.p[4].t = o.kpt;                                   /* короткое название — в одну строку на карточке */
  if (t.a11y) Object.assign(t.a11y, l === 'ru' ? { prev: 'Назад', next: 'Вперёд', close: 'Закрыть' } : l === 'az' ? { prev: 'Geri', next: 'İrəli', close: 'Bağla' } : { prev: 'Previous', next: 'Next', close: 'Close' });
}

/* ── ТИПОГРАФИКА (ru): неразрывный пробел после коротких предлогов и союзов, перед тире, в числах и в телефоне ── */
const NB = '\u00A0';
const ruTypo = x => {
  const w = '(?:в|во|к|ко|с|со|у|о|об|от|на|по|за|из|и|а|но|не|ни|до|для|при|над|под|без|или|да|же|бы|ли)';
  const re = new RegExp('(^|[\\s\u00A0«(])(' + w + ')[ ]+(?=\\S)', 'gi');
  return x.replace(re, '$1$2' + NB).replace(re, '$1$2' + NB)
    .replace(/ — /g, NB + '— ')
    .replace(/(\d) (?=(?:год|лет|мес|час|AZN|страниц|человек|этаж|минут))/g, '$1' + NB)
    .replace(/\+994 70 220 03 76/g, '+994' + NB + '70' + NB + '220' + NB + '03' + NB + '76');
};
const ruWalk = o => { for (const k of Object.keys(o)) { const v = o[k]; if (typeof v === 'string') o[k] = ruTypo(v); else if (v && typeof v === 'object') ruWalk(v); } };
ruWalk(T.ru);

/* ── BOOK_SOON: «Общая психотерапия» — тем же шаблоном; кнопка пока ведёт на главную страницу книг (слово владельца 11.11) ── */
const SOON = {
  ru: { k: 'Скоро', t: 'Общая психотерапия', a: 'Кенан Рагимов', f: ['Том на русском языке уже готов.', 'Азербайджанское издание готовится.', 'Скоро книга появится среди наших книг.'] },
  az: { k: 'Tezliklə', t: 'Ümumi psixoterapiya', a: 'Kənan Rəhimov', f: ['Rus dilində cild artıq hazırdır.', 'Azərbaycan dilində nəşr hazırlanır.', 'Tezliklə kitablarımızın sırasında olacaq.'] },
  en: { k: 'Coming soon', t: 'General psychotherapy', a: 'Kenan Ragimov', f: ['The volume in Russian is ready.', 'The Azerbaijani edition is in preparation.', 'It will soon join our books.'] },
};
for (const l of Object.keys(SOON)) T[l].books.soon = SOON[l];

/* ── REG_FORM: единая форма записи — подписи на трёх языках ── */
const REG = {
  ru: { eye: '', h: 'Запись', sub: 'Выберите, на что записаться, — остальное в несколько нажатий.',
    kinds: [['consult', 'Консультация'], ['edu', 'Обучение'], ['ind', 'Индивидуальная подготовка'], ['b2b', 'Для компании']],
    f: { fname: 'Имя', lname: 'Фамилия', phone: 'Телефон', company: 'Компания', other: 'Ваша тема', id: 'Удостоверение личности — фото или скан', dip: 'Диплом о высшем образовании — если есть' },
    who: { l: 'Специалист', o: [['kenan', 'Кенан Рагимов'], ['samira', 'Самира Рагимова'], ['both', 'Оба специалиста']] }, fmt: { l: 'Формат', o: [['online', 'Онлайн'], ['offline', 'Очно']] },
    topic: 'Тема', topicOther: 'Другая тема', prog: 'Программа', hours: { l: 'Количество часов', min: 'минимум 20' },
    b2b: { topic: 'Тематика', other: 'Другое', free: 'Заявка без оплаты', goal: { l: 'Цель', o: ['Развитие команды', 'Подготовка руководителей', 'Рост продаж', 'Стресс и выгорание', 'Корпоративное мероприятие'] },
      count: { l: 'Участников', o: ['до 10', '10–20', '20–50', 'более 50'] }, lang: { l: 'Язык', o: ['Азербайджанский', 'Русский', 'Английский'] }, place: { l: 'Где', o: ['В вашем офисе', 'Онлайн', 'Выездной формат'] } },
    price: 'Стоимость', perHour: 'за встречу, 1 час', noteB2b: 'Оплаты на этом шаге нет: с вами свяжется наш специалист.',
    send: { consult: 'Записаться и перейти к оплате', edu: 'Отправить заявку', ind: 'Записаться и перейти к оплате', b2b: 'Отправить заявку' },
    pay: { now: 'Оплатить сейчас', inst: 'В рассрочку (банк)' }, req: 'Заполните выделенные поля.', sending: 'Отправляем…', ok: 'Заявка принята. Мы свяжемся с вами.', err: 'Не удалось отправить заявку. Напишите нам в' },
  az: { eye: '', h: 'Qeydiyyat', sub: 'Nəyə yazılmaq istədiyinizi seçin — qalanı bir neçə toxunuşla.',
    kinds: [['consult', 'Konsultasiya'], ['edu', 'Təhsil'], ['ind', 'Fərdi hazırlıq'], ['b2b', 'Şirkət üçün']],
    f: { fname: 'Ad', lname: 'Soyad', phone: 'Telefon', company: 'Şirkət', other: 'Sizin mövzunuz', id: 'Şəxsiyyət vəsiqəsi — foto və ya skan', dip: 'Ali təhsil haqqında diplom — varsa' },
    who: { l: 'Mütəxəssis', o: [['kenan', 'Kənan Rəhimov'], ['samira', 'Samirə Rəhimova'], ['both', 'Hər iki mütəxəssis']] }, fmt: { l: 'Format', o: [['online', 'Onlayn'], ['offline', 'Əyani']] },
    topic: 'Mövzu', topicOther: 'Başqa mövzu', prog: 'Proqram', hours: { l: 'Saatların sayı', min: 'ən azı 20' },
    b2b: { topic: 'Mövzu', other: 'Digər', free: 'Ödənişsiz müraciət', goal: { l: 'Məqsəd', o: ['Komandanın inkişafı', 'Rəhbərlərin hazırlanması', 'Satışların artırılması', 'Stress və tükənmə', 'Korporativ tədbir'] },
      count: { l: 'İştirakçı sayı', o: ['10-a qədər', '10–20', '20–50', '50-dən çox'] }, lang: { l: 'Dil', o: ['Azərbaycan dili', 'Rus dili', 'İngilis dili'] }, place: { l: 'Harada', o: ['Sizin ofisdə', 'Onlayn', 'Səyyar format'] } },
    price: 'Qiymət', perHour: 'bir görüş, 1 saat', noteB2b: 'Bu mərhələdə ödəniş yoxdur: mütəxəssisimiz sizinlə əlaqə saxlayacaq.',
    send: { consult: 'Yazılın və ödənişə keçin', edu: 'Müraciəti göndərin', ind: 'Yazılın və ödənişə keçin', b2b: 'Müraciəti göndərin' },
    pay: { now: 'İndi ödəyin', inst: 'Hissə-hissə (bank)' }, req: 'İşarələnmiş xanaları doldurun.', sending: 'Göndərilir…', ok: 'Müraciətiniz qəbul edildi. Sizinlə əlaqə saxlayacağıq.', err: 'Müraciəti göndərmək mümkün olmadı. Bizə yazın:' },
  en: { eye: '', h: 'Booking', sub: 'Choose what you are booking — the rest takes a few taps.',
    kinds: [['consult', 'Consultation'], ['edu', 'Education'], ['ind', 'Individual training'], ['b2b', 'For a company']],
    f: { fname: 'First name', lname: 'Last name', phone: 'Phone', company: 'Company', other: 'Your topic', id: 'Identity document — photo or scan', dip: 'Higher-education diploma — if you have one' },
    who: { l: 'Specialist', o: [['kenan', 'Kenan Ragimov'], ['samira', 'Samira Ragimova'], ['both', 'Both specialists']] }, fmt: { l: 'Format', o: [['online', 'Online'], ['offline', 'In person']] },
    topic: 'Topic', topicOther: 'Another topic', prog: 'Programme', hours: { l: 'Number of hours', min: '20 minimum' },
    b2b: { topic: 'Subject', other: 'Other', free: 'Request without payment', goal: { l: 'Goal', o: ['Team development', 'Training managers', 'Sales growth', 'Stress and burnout', 'Corporate event'] },
      count: { l: 'Participants', o: ['up to 10', '10–20', '20–50', 'more than 50'] }, lang: { l: 'Language', o: ['Azerbaijani', 'Russian', 'English'] }, place: { l: 'Where', o: ['At your office', 'Online', 'Off-site'] } },
    price: 'Price', perHour: 'per session, 1 hour', noteB2b: 'No payment at this step: our specialist will contact you.',
    send: { consult: 'Book and go to payment', edu: 'Send the request', ind: 'Book and go to payment', b2b: 'Send the request' },
    pay: { now: 'Pay now', inst: 'In instalments (bank)' }, req: 'Please fill in the highlighted fields.', sending: 'Sending…', ok: 'Your request has been received. We will contact you.', err: 'The request could not be sent. Write to us on' },
};
for (const l of Object.keys(REG)) T[l].reg = REG[l];
