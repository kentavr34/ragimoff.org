/* Данные семи образовательных программ (ru / az / en).
   Источник: живые страницы site/{ru,az,en}/telim/*.html; правила владельца от 11.11.2026
   (краткие программы: 3 мес. + 6 мес. групповой супервизии, 300 AZN/мес. или 800 AZN при предоплате;
   даты начала не указываются). */

/* ---------- Общие блоки для «Общей» и «Клинической» психологии (страница «Юридические основы») ---------- */

const FAQ_RU = [
  ['Нужна ли нострификация диплома?', 'Нет. Диплом о дополнительном профессиональном образовании (ДПО) даёт законное право работать в Азербайджане без процедуры подтверждения (нострификации) в Министерстве образования. Приступать к деятельности можно сразу после получения диплома.'],
  ['Кто выдаёт диплом?', 'Санкт-Петербургский институт дополнительного профессионального образования для психологов и психотерапевтов — учебное заведение, лицензированное Министерством образования России. Кенан Рагимов — преподаватель института и его официальный представитель в Азербайджане.'],
  ['Как проверить диплом и лицензию?', 'Номер диплома проверяется в российском федеральном реестре (ФИС ФРДО), лицензия института — на сайте Рособрнадзора. Имя «Рагимов Кенан Ровшанович» можно найти в списке преподавателей на сайте института.'],
  ['Даёт ли диплом право называться психологом и оказывать психологическую помощь?', 'Да. По Закону Азербайджанской Республики «О психологической помощи» (ст. 1.0.2 и 3.2) психологом признаётся и тот, кто получил специальность психолога в форме дополнительного образования; слова «психолог», «психотерапия» и другие допускается использовать лицам, имеющим право оказывать психологическую помощь.'],
  ['Признаётся ли дополнительное образование официальным?', 'Да. Статья 24 Закона Азербайджанской Республики «Об образовании» признаёт дополнительное образование официальной формой образования. Диплом Санкт-Петербургского института относится именно к этой категории.'],
  ['Можно ли получить диплом психолога, если высшее образование по другой специальности?', 'Да. Согласно Постановлению Кабинета Министров АР № 163 (п. 3.1.1), переподготовка — форма дополнительного образования, позволяющая освоить новую профессию. Лицо с высшим образованием по другой специальности может пройти переподготовку по психологии и получить диплом психолога.'],
  ['Где могут работать выпускники?', 'По Соглашению между Россией и Азербайджаном в сфере образования (Закон АР № 455-IIQ от 13 мая 2003 г.) диплом Санкт-Петербургского института официально признан в Азербайджане. При соответствии требованиям работодателя выпускники могут работать как в государственных, так и в частных учреждениях.']
];

const FAQ_AZ = [
  ['Diplomun nostrifikasiyasına ehtiyac varmı?', 'Xeyr. Əlavə Təhsil diplomu Azərbaycan Respublikasında təsdiqlənmə (nostrifikasiya) prosedurundan keçmədən işləməyə qanuni hüquq verir. Diplomu aldıqdan dərhal sonra fəaliyyətə başlaya bilərsiniz.'],
  ['Diplomu kim verir?', 'Sankt-Peterburq Əlavə Təhsil İnstitutu — Rusiya Təhsil Nazirliyi tərəfindən lisenziyalanmış rəsmi təhsil müəssisəsi. Kənan Rəhimov institutun müəllimi və Azərbaycandakı rəsmi nümayəndəsidir.'],
  ['Diplomu və lisenziyanı necə yoxlamaq olar?', 'Diplomun nömrəsi Rusiyanın federal reyestrində (FİS FRDO), institutun lisenziyası isə Rosobrnadzor saytında yoxlanıla bilər. «Рагимов Кенан Ровшанович» adını institutun saytında müəllimlər siyahısında tapa bilərsiniz.'],
  ['Diplom «psixoloq» adlanmaq və psixoloji yardım göstərmək hüququ verirmi?', 'Bəli. «Psixoloji yardım haqqında» Azərbaycan Respublikası Qanununa (maddə 1.0.2 və 3.2) əsasən psixoloq ixtisasını əlavə təhsil formasında əldə edən şəxs də psixoloq sayılır; «psixoloq», «psixoterapiya» və digər sözlərdən psixoloji yardım göstərmək hüququ olan şəxslər istifadə edə bilər.'],
  ['Əlavə təhsil rəsmi təhsil formasıdırmı?', 'Bəli. «Təhsil haqqında» Azərbaycan Respublikası Qanununun 24-cü maddəsi əlavə təhsili rəsmi təhsil forması kimi tanıyır. Sankt-Peterburq İnstitutunun diplomu məhz bu kateqoriyaya aiddir.'],
  ['Başqa ixtisas üzrə ali təhsilim varsa, psixoloq diplomu ala bilərəmmi?', 'Bəli. Nazirlər Kabinetinin 163 nömrəli Qərarına (bənd 3.1.1) əsasən yenidənhazırlanma yeni peşə və ixtisasa yiyələnməyə imkan verən əlavə təhsil formasıdır. Başqa ixtisaslı ali təhsilə malik şəxs psixologiya üzrə yenidənhazırlanma keçərək psixoloq diplomu ala bilər.'],
  ['Məzunlar harada işləyə bilər?', 'Rusiya ilə Azərbaycan arasında təhsil sahəsindəki Sazişə (AR Qanunu № 455-IIQ, 13 may 2003) əsasən Sankt-Peterburq İnstitutunun diplomu Azərbaycanda rəsmi tanınan sənəddir. İşə qəbul edən tərəfin tələblərinə uyğun olduqda məzunlar həm dövlət, həm də özəl müəssisələrdə fəaliyyət göstərə bilər.']
];

const FAQ_EN = [
  ['Is nostrification of the diploma required?', 'No. A diploma of additional professional education (CPD) gives the legal right to work in the Republic of Azerbaijan without a confirmation procedure (nostrification) by the Ministry of Education. You may begin practice immediately after receiving the diploma.'],
  ['Who issues the diploma?', 'The St Petersburg Institute of Additional Professional Education for Psychologists and Psychotherapists, an official educational institution licensed by the Russian Ministry of Education. Kenan Ragimov is an instructor at the institute and its official representative in Azerbaijan.'],
  ['How can the diploma and licence be verified?', 'The diploma number can be checked in the Russian federal register (FIS FRDO) and the institute’s licence on the Rosobrnadzor website. The name “Ragimov Kenan Rovshanovich” can be found in the faculty list on the institute’s website.'],
  ['Does the diploma give the right to use the title “psychologist” and provide psychological assistance?', 'Yes. Under the Law of the Republic of Azerbaijan “On Psychological Assistance” (Articles 1.0.2 and 3.2), a person who has acquired the specialty of psychologist through additional education is also a psychologist; the words “psychologist”, “psychotherapy” and others may be used by persons entitled to provide psychological assistance.'],
  ['Is additional education recognised as official?', 'Yes. Article 24 of the Law of the Republic of Azerbaijan “On Education” recognises additional education as an official form of education. The diploma of the St Petersburg Institute falls precisely within this category.'],
  ['Can I get a psychologist’s diploma if my degree is in another field?', 'Yes. Under Decree No. 163 of the Cabinet of Ministers (clause 3.1.1), retraining is a form of additional education that allows a person to master a new profession. A person with a higher education in another speciality may undergo retraining in psychology and receive a full psychologist’s diploma.'],
  ['Where can graduates work?', 'Under the Education Agreement between Russia and Azerbaijan (Law of the Republic of Azerbaijan No. 455-IIQ, 13 May 2003), the diploma of the St Petersburg Institute is an officially recognised document in Azerbaijan. Provided they meet employer requirements, graduates may work in both public and private institutions.']
];

/* ---------- Программы ---------- */

export const PROGRAMS = {
  order: ['general', 'clinical', 'practicum', 'psychodiagnostics', 'cbt', 'psychoanalysis', 'family'],
  items: {

    /* ===================================================== 1. ОБЩАЯ ПСИХОЛОГИЯ */
    general: {
      kind: 'long',
      reg: 0,
      sample: 'diploma',
      ru: {
        title: 'Общая психология',
        lead: 'Программа разработана для тех, кто начинает с нуля: она сочетает теоретические знания с практическими навыками — от теорий личности до проведения реальных сессий. Право на психологическое консультирование по законодательству Азербайджанской Республики.',
        forWhom: [
          'Начинающие в психологии — предыдущее образование не требуется',
          'Те, кто хочет заниматься саморазвитием',
          'Работники сферы HR, образования, здравоохранения',
          'Те, кто хочет сменить профессию на психолога',
          'Готовящиеся к программе «Клиническая психология»'
        ],
        teachers: [['Кенан Рагимов', 'ведёт программу; 23 года клинической практики, международная квалификация, амбассадор IPAS']],
        facts: [
          ['Длительность', '1 год (6+6 мес.)'],
          ['Объём', '1 556 академических часов, 22 дисциплины'],
          ['Формат', 'Онлайн + офлайн'],
          ['Начало', 'Запись открыта'],
          ['Документ', 'Диплом о профессиональной переподготовке (ДПО), Санкт-Петербургский институт ДПО']
        ],
        includes: [
          'Практикум по психотерапии входит в программу',
          'Видеоуроки д-ра Рагимова по каждой дисциплине и список рекомендованной литературы',
          'Индивидуальный клинический супервизор для каждого слушателя',
          'Возможность принимать пациентов на базе центра RAGIMOFF'
        ],
        program: [
          { t: 'Блок I — Основы психологии', items: ['Общая психология · 72 ч.', 'История психологии · 80 ч.', 'Методологические основы психологии · 80 ч.', 'Социальная психология · 80 ч.'] },
          { t: 'Блок II — Прикладная психология', items: ['Педагогическая психология · 80 ч.', 'Психология развития · 80 ч.', 'Психология развития — расширенный курс · 88 ч.', 'Семейная психология · 72 ч.', 'Стресс и психологическая устойчивость · 80 ч.', 'Конфликтология · 80 ч.', 'Организационная психология · 88 ч.'] },
          { t: 'Блок III — Клинико-терапевтический блок', items: ['Введение в клиническую психологию · 72 ч.', 'Основы нейропсихологии · 80 ч.', 'Психологическое консультирование · 88 ч.', 'Когнитивно-поведенческая терапия (КПТ) · 88 ч.', 'Гештальт-терапия · 88 ч.', 'Аналитическая психология · 80 ч.'] },
          { t: 'Блок IV — Профессиональное развитие', items: ['Психологическая этика и профессиональные стандарты · 80 ч.', 'Построение собственной психологической практики · 56 ч.'] },
          { t: 'Блок V — Итоговая аттестация', items: ['Промежуточная аттестация · 2 ч.', 'Выпускная работа · 40 ч.', 'Итоговый экзамен · 2 ч.'] }
        ],
        doc: {
          t: 'Диплом о профессиональной переподготовке (ДПО)',
          d: 'Диплом выдаёт Санкт-Петербургский институт дополнительного профессионального образования для психологов и психотерапевтов; программа профессиональной переподготовки утверждена руководством института. Сведения о дипломе вносятся в государственный реестр ФИС ФРДО, диплом не требует нострификации, и работодатель может проверить его через реестр.'
        },
        price: {
          rows: [['Полная стоимость', '210 тыс. руб.'], ['При полной оплате (−10%)', '190 тыс. руб.'], ['Рассрочка 12 мес.', '18 тыс. руб./мес.'], ['Рассрочка 24 мес.', '10 тыс. руб./мес.']],
          note: 'Рассрочка до 24 месяцев — от 10 тыс. руб./мес.'
        },
        faq: [...FAQ_RU, ['Нужно ли предыдущее образование по психологии?', 'Нет. Для программы «Общая психология» предыдущее образование по психологии не требуется: подать заявку может любой совершеннолетний человек, интересующийся психологией.']]
      },
      az: {
        title: 'Ümumi Psixologiya',
        lead: 'Proqram psixologiyaya sıfırdan başlayanlar üçün nəzərdə tutulmuşdur: nəzəri biliklər praktik bacarıqlarla birləşir — şəxsiyyət nəzəriyyələrindən real seans keçirməyə qədər. AR qanunvericiliyinə uyğun psixoloji konsultasiya hüququ.',
        forWhom: [
          'Psixologiyaya yeni başlayanlar — əvvəlki təhsil tələb olunmur',
          'Özünü inkişaf etdirmək istəyənlər',
          'HR, təhsil, sağlamlıq sektorunda çalışanlar',
          'Psixologiya peşəsinə keçmək istəyənlər',
          'Klinik psixologiya proqramına hazırlananlar'
        ],
        teachers: [['Kənan Rəhimov', 'proqramı aparır; 23 illik klinik təcrübə, beynəlxalq kvalifikasiya, IPAS Ambassador']],
        facts: [
          ['Müddət', '1 il (6+6 ay)'],
          ['Həcm', '1 556 akademik saat, 22 fənn'],
          ['Format', 'Onlayn + oflayn'],
          ['Başlanğıc', 'Qeydiyyat açıqdır'],
          ['Sənəd', 'Peşə yenidənhazırlanması üzrə Əlavə Təhsil Diplomu, Sankt-Peterburq Əlavə Təhsil İnstitutu']
        ],
        includes: [
          'Psixoterapiya Praktikumu proqrama daxildir',
          'Hər fənn üzrə Dr. Rəhimovun video dərsləri və tövsiyə olunan ədəbiyyat siyahısı',
          'Hər tələbəyə fərdi klinik supervisor təyin edilir',
          'RAGIMOFF mərkəzində öz pasiyentlərini qəbul etmək imkanı'
        ],
        program: [
          { t: 'Blok I — Psixologiyanın Əsasları', items: ['Ümumi psixologiya · 72 saat', 'Psixologiya tarixi · 80 saat', 'Psixologiyanın metodoloji əsasları · 80 saat', 'Sosial psixologiya · 80 saat'] },
          { t: 'Blok II — Tətbiqi Psixologiya', items: ['Pedaqoji psixologiya · 80 saat', 'İnkişaf psixologiyası · 80 saat', 'İnkişaf psixologiyası — genişləndirilmiş kurs · 88 saat', 'Ailə psixologiyası · 72 saat', 'Stress və psixoloji dözümlülük · 80 saat', 'Konfliktologiya · 80 saat', 'Təşkilati psixologiya · 88 saat'] },
          { t: 'Blok III — Klinik-Terapevtik Blok', items: ['Klinik psixologiyaya giriş · 72 saat', 'Neyropsixologiya əsasları · 80 saat', 'Psixoloji konsultasiya · 88 saat', 'Koqnitiv-davranış terapiyası (KDT) · 88 saat', 'Gəştalt terapiyası · 88 saat', 'Analitik psixologiya · 80 saat'] },
          { t: 'Blok IV — Peşəkar İnkişaf', items: ['Psixoloji etika və peşəkar standartlar · 80 saat', 'Öz psixoloji praktikanı qurmaq · 56 saat'] },
          { t: 'Blok V — Yekun Attestasiya', items: ['Aralıq attestasiya · 2 saat', 'Buraxılış işi · 40 saat', 'Yekun test imtahanı · 2 saat'] }
        ],
        doc: {
          t: 'Peşə yenidənhazırlanması üzrə Əlavə Təhsil Diplomu',
          d: 'Diplomu Sankt-Peterburq Əlavə Təhsil İnstitutu verir; peşəkar yenidənhazırlanma proqramı institutun rəhbərliyi tərəfindən təsdiq edilib. Diplom haqqında məlumat FİS FRDO dövlət reyestrinə daxil edilir, nostrifikasiya tələb olunmur, işəgötürən diplomu reyestr vasitəsilə yoxlaya bilər.'
        },
        price: {
          rows: [['Tam qiymət', '4 200 AZN'], ['Öncədən ödənişdə (−400 AZN)', '3 800 AZN'], ['Taksit 12 ay', '350 AZN/ay'], ['Taksit 24 ay', '200 AZN/ay']],
          note: '24 aya qədər taksit imkanı — aylıq minimum 200 AZN.'
        },
        faq: [...FAQ_AZ, ['Əvvəlki psixologiya təhsili tələb olunurmu?', 'Xeyr. «Ümumi Psixologiya» proqramı üçün əvvəlki psixologiya təhsili tələb olunmur: psixologiyaya maraq göstərən hər bir yetkin şəxs müraciət edə bilər.']]
      },
      en: {
        title: 'General Psychology',
        lead: 'The programme is designed for those starting from scratch: it combines theoretical knowledge with practical skills, from personality theories to conducting real sessions. The right to practise psychological counselling under the law of the Republic of Azerbaijan.',
        forWhom: [
          'Beginners in psychology — no prior education required',
          'Those who wish to pursue personal development',
          'HR, education, and healthcare professionals',
          'Those looking to change careers and become a psychologist',
          'Those preparing for the Clinical Psychology programme'
        ],
        teachers: [['Kenan Ragimov', 'leads the programme; 23 years of clinical practice, international qualification, IPAS Ambassador']],
        facts: [
          ['Duration', '1 year (6+6 months)'],
          ['Volume', '1,556 academic hours, 22 disciplines'],
          ['Format', 'Online + offline'],
          ['Start', 'Enrolment is open'],
          ['Document', 'Diploma of professional retraining (CPD), St Petersburg Institute of Additional Professional Education']
        ],
        includes: [
          'The Psychotherapy Practicum is included in the programme',
          'Dr Ragimov’s video lessons for every discipline and a list of recommended literature',
          'Each student is assigned a personal clinical supervisor',
          'The option to see clients at the RAGIMOFF centre'
        ],
        program: [
          { t: 'Block I — Psychology Fundamentals', items: ['General Psychology · 72 hrs', 'History of Psychology · 80 hrs', 'Methodological Foundations of Psychology · 80 hrs', 'Social Psychology · 80 hrs'] },
          { t: 'Block II — Applied Psychology', items: ['Educational Psychology · 80 hrs', 'Developmental Psychology · 80 hrs', 'Developmental Psychology — Advanced Course · 88 hrs', 'Family Psychology · 72 hrs', 'Stress and Psychological Resilience · 80 hrs', 'Conflict Resolution · 80 hrs', 'Organisational Psychology · 88 hrs'] },
          { t: 'Block III — Clinical & Therapeutic Block', items: ['Introduction to Clinical Psychology · 72 hrs', 'Foundations of Neuropsychology · 80 hrs', 'Psychological Counselling · 88 hrs', 'Cognitive Behavioural Therapy (CBT) · 88 hrs', 'Gestalt Therapy · 88 hrs', 'Analytical Psychology · 80 hrs'] },
          { t: 'Block IV — Professional Development', items: ['Psychology Ethics and Professional Standards · 80 hrs', 'Building Your Own Psychology Practice · 56 hrs'] },
          { t: 'Block V — Final Assessment', items: ['Mid-Term Assessment · 2 hrs', 'Graduation Thesis · 40 hrs', 'Final Examination · 2 hrs'] }
        ],
        doc: {
          t: 'Diploma of professional retraining (CPD)',
          d: 'The diploma is issued by the St Petersburg Institute of Additional Professional Education for Psychologists and Psychotherapists; the professional retraining programme is approved by the institute’s management. The diploma is entered in the state register FIS FRDO, requires no nostrification and can be checked by an employer through the register.'
        },
        price: {
          rows: [['Full price', '$2,500'], ['Full payment (−10%)', '$2,250'], ['12-month instalment', '$210/mo.'], ['24-month instalment', '$120/mo.']],
          note: 'Instalment plan up to 24 months — from $120/mo.'
        },
        faq: [...FAQ_EN, ['Is a previous psychology education required?', 'No. The General Psychology programme does not require any previous psychology education: any adult interested in psychology may apply.']]
      }
    },

    /* ===================================================== 2. КЛИНИЧЕСКАЯ ПСИХОЛОГИЯ */
    clinical: {
      kind: 'long',
      reg: 1,
      sample: 'diploma',
      ru: {
        title: 'Клиническая психология (ДПО)',
        lead: 'Программа охватывает диагностику психических расстройств по DSM-5 и ICD-11, основные психотерапевтические подходы (КПТ, элементы EMDR) и реальную клиническую практику. Предназначена для специалистов, уже работающих в своей области или планирующих начать.',
        forWhom: [
          'Специалисты с дипломом о высшем образовании (любое направление)',
          'Прошедшие программу общей психологии',
          'Желающие работать в клиниках и больницах',
          'Желающие стать психотерапевтом',
          'Планирующие открыть собственный психологический центр'
        ],
        teachers: [['Кенан Рагимов', 'ведёт программу; 23 года клинической практики, международная квалификация, амбассадор IPAS']],
        facts: [
          ['Длительность', '1 год (6+6 мес.)'],
          ['Объём', '1 528 академических часов, 23 дисциплины'],
          ['Формат', 'Онлайн + офлайн'],
          ['Начало', 'Запись открыта'],
          ['Документ', 'Диплом о профессиональной переподготовке (ДПО), Санкт-Петербургский институт ДПО, + международный сертификат IPAS']
        ],
        includes: [
          'Программа «Общая психология» входит в программу',
          'Практикум по психотерапии входит в программу',
          'Международный сертификат IPAS/BPA — параллельно с дипломом ДПО',
          'Видеоуроки д-ра Рагимова по каждой дисциплине и еженедельная живая практика',
          'Разбор реальных клинических случаев под супервизией'
        ],
        program: [
          { t: 'Блок I — Неврологические и физиологические основы', items: ['Анатомия центральной нервной системы · 52 ч.', 'Физиология центральной нервной системы · 47 ч.', 'Психофизиология · 48 ч.', 'Нейропсихология · 56 ч.'] },
          { t: 'Блок II — Теоретические основы клинической психологии', items: ['Патопсихология · 53 ч.', 'Введение в клиническую психологию · 47 ч.', 'Психосоматика и телесная психология · 94 ч.', 'Психотерапия: теория и практика · 66 ч.', 'Дифференциальная психология · 47 ч.', 'Теории личности в клинической психологии · 11 ч.', 'Психодиагностика · 67 ч.', 'Основы психологического консультирования · 30 ч.', 'Нарушения психологического развития · 104 ч.', 'Клиническая психология в геронтологии · 63 ч.', 'Девиантология · 50 ч.'] },
          { t: 'Блок III — Дополнительные клинические модули', items: ['Основы психиатрии · 100 ч.', 'Кризисная психология (ПТСР) · 80 ч.', 'Психология зависимостей · 63 ч.'] },
          { t: 'Блок IV — Практикум', items: ['Практикум по нейропсихологии · 112 ч.', 'Практикум по патопсихологии · 161 ч.', 'Практикум по психодиагностике · 105 ч.', 'Практикум по детской клинической психологии · 60 ч.'] },
          { t: 'Блок V — Итоговая аттестация', items: ['Итоговый междисциплинарный экзамен · 12 ч.'] }
        ],
        doc: {
          t: 'Диплом о профессиональной переподготовке (ДПО) + сертификат IPAS',
          d: 'Диплом выдаёт Санкт-Петербургский институт дополнительного профессионального образования для психологов и психотерапевтов; сведения о дипломе вносятся в государственный реестр ФИС ФРДО, нострификация не требуется. Параллельно выдаётся международный сертификат IPAS/BPA с проверкой по QR-коду, действительный и за пределами Азербайджана.'
        },
        price: {
          rows: [['Полная стоимость', '330 тыс. руб.'], ['При полной оплате (−10%)', '300 тыс. руб.'], ['Рассрочка 12 мес.', '28 тыс. руб./мес.'], ['Рассрочка 24 мес.', '15 тыс. руб./мес.']],
          note: 'Минимальный ежемесячный платёж — 15 тыс. руб. Оплата банковским переводом или через СБП.'
        },
        faq: [...FAQ_RU, ['Нужно ли высшее образование?', 'Да. Для программы «Клиническая психология» требуется диплом о высшем образовании (любое направление; предпочтение — психология, медицина, педагогика и социальная работа).']]
      },
      az: {
        title: 'Klinik Psixologiya (Əlavə Təhsil)',
        lead: 'Proqram DSM-5 və ICD-11 üzrə psixi pozuntuların diaqnostikasını, əsas psixoterapevtik yanaşmaları (KDT, EMDR elementləri) və real klinik praktikanı əhatə edir. Öz sahəsində aktiv çalışan ya çalışmağı planlaşdıran mütəxəssislər üçün nəzərdə tutulmuşdur.',
        forWhom: [
          'Ali təhsil diplomu olan mütəxəssislər (istənilən sahə)',
          'Ümumi psixologiya proqramını tamamlayanlar',
          'Klinikalarda, xəstəxanalarda çalışmaq istəyənlər',
          'Psixoterapevt olmaq istəyənlər',
          'Öz psixologiya mərkəzini açmağı planlaşdıranlar'
        ],
        teachers: [['Kənan Rəhimov', 'proqramı aparır; 23 illik klinik təcrübə, beynəlxalq kvalifikasiya, IPAS Ambassador']],
        facts: [
          ['Müddət', '1 il (6+6 ay)'],
          ['Həcm', '1 528 akademik saat, 23 fənn'],
          ['Format', 'Onlayn + oflayn'],
          ['Başlanğıc', 'Qeydiyyat açıqdır'],
          ['Sənəd', 'Peşə yenidənhazırlanması üzrə Əlavə Təhsil Diplomu, Sankt-Peterburq Əlavə Təhsil İnstitutu, + beynəlxalq IPAS sertifikatı']
        ],
        includes: [
          'Ümumi Psixologiya proqramı bu proqrama daxildir',
          'Psixoterapiya Praktikumu proqrama daxildir',
          'Beynəlxalq IPAS/BPA sertifikatı — Əlavə Təhsil diplomu ilə paralel',
          'Hər fənn üzrə Dr. Rəhimovun video dərsləri və həftəlik canlı praktika',
          'Real klinik keyslərin supervisor nəzarəti altında analizi'
        ],
        program: [
          { t: 'Blok I — Neyroloji və Fiziologiya Əsasları', items: ['Mərkəzi sinir sisteminin anatomiyası · 52 saat', 'Mərkəzi sinir sisteminin fiziologiyası · 47 saat', 'Psixofiziologiya · 48 saat', 'Neyropsixologiya · 56 saat'] },
          { t: 'Blok II — Klinik Psixologiyanın Nəzəri Əsasları', items: ['Patopsixologiya · 53 saat', 'Klinik psixologiyaya giriş · 47 saat', 'Psixosomatika və bədən psixologiyası · 94 saat', 'Psixoterapiya: nəzəriyyə və praktika · 66 saat', 'Diferensial psixologiya · 47 saat', 'Klinik psixologiyada şəxsiyyət nəzəriyyələri · 11 saat', 'Psixodiaqnostika · 67 saat', 'Psixoloji konsultasiyanın əsasları · 30 saat', 'Psixoloji inkişaf pozuntuları · 104 saat', 'Gerontologiyada klinik psixologiya · 63 saat', 'Deviantologiya · 50 saat'] },
          { t: 'Blok III — Əlavə Klinik Modullar', items: ['Psixiatriyanın əsasları · 100 saat', 'Böhran psixologiyası (PTSS) · 80 saat', 'Asılılıq psixologiyası · 63 saat'] },
          { t: 'Blok IV — Praktikum', items: ['Neyropsixologiya praktikumu · 112 saat', 'Patopsixologiya praktikumu · 161 saat', 'Psixodiaqnostika praktikumu · 105 saat', 'Uşaq klinik psixologiyası praktikumu · 60 saat'] },
          { t: 'Blok V — Yekun Attestasiya', items: ['Yekun fənlərarası imtahan · 12 saat'] }
        ],
        doc: {
          t: 'Peşə yenidənhazırlanması üzrə Əlavə Təhsil Diplomu + IPAS sertifikatı',
          d: 'Diplomu Sankt-Peterburq Əlavə Təhsil İnstitutu verir; diplom haqqında məlumat FİS FRDO dövlət reyestrinə daxil edilir, nostrifikasiya tələb olunmur. Paralel olaraq QR kodla yoxlanıla bilən, Azərbaycandan kənarda da keçərli olan beynəlxalq IPAS/BPA sertifikatı verilir.'
        },
        price: {
          rows: [['Tam qiymət', '6 600 AZN'], ['Öncədən ödənişdə (−600 AZN)', '6 000 AZN'], ['Taksit 12 ay', '550 AZN/ay'], ['Taksit 24 ay', '300 AZN/ay']],
          note: '24 aya qədər taksit imkanı — aylıq minimum 300 AZN.'
        },
        faq: [...FAQ_AZ, ['Ali təhsil tələb olunurmu?', 'Bəli. «Klinik Psixologiya» proqramı üçün ali təhsil diplomu tələb olunur (istənilən sahə; psixologiya, tibb, pedaqogika və sosial iş sahələrinə üstünlük verilir).']]
      },
      en: {
        title: 'Clinical Psychology (CPD)',
        lead: 'The programme covers the diagnosis of mental disorders using DSM-5 and ICD-11, core psychotherapeutic approaches (CBT, elements of EMDR) and real clinical practice. It is designed for professionals already working in their field or planning to start.',
        forWhom: [
          'Holders of a higher education degree (any field)',
          'Those who have completed the General Psychology programme',
          'Those wishing to work in clinics and hospitals',
          'Those wishing to become a psychotherapist',
          'Those planning to open their own psychology centre'
        ],
        teachers: [['Kenan Ragimov', 'leads the programme; 23 years of clinical practice, international qualification, IPAS Ambassador']],
        facts: [
          ['Duration', '1 year (6+6 months)'],
          ['Volume', '1,528 academic hours, 23 disciplines'],
          ['Format', 'Online + offline'],
          ['Start', 'Enrolment is open'],
          ['Document', 'Diploma of professional retraining (CPD), St Petersburg Institute of Additional Professional Education, + international IPAS certificate']
        ],
        includes: [
          'The General Psychology programme is included',
          'The Psychotherapy Practicum is included in the programme',
          'International IPAS/BPA certificate — alongside the CPD diploma',
          'Dr Ragimov’s video lessons for every discipline and weekly live practice',
          'Real clinical case analysis under supervision'
        ],
        program: [
          { t: 'Block I — Neurological & Physiological Foundations', items: ['Anatomy of the Central Nervous System · 52 hrs', 'Physiology of the Central Nervous System · 47 hrs', 'Psychophysiology · 48 hrs', 'Neuropsychology · 56 hrs'] },
          { t: 'Block II — Theoretical Foundations of Clinical Psychology', items: ['Pathopsychology · 53 hrs', 'Introduction to Clinical Psychology · 47 hrs', 'Psychosomatics and Body-Oriented Psychology · 94 hrs', 'Psychotherapy: Theory and Practice · 66 hrs', 'Differential Psychology · 47 hrs', 'Personality Theories in Clinical Psychology · 11 hrs', 'Psychodiagnostics · 67 hrs', 'Foundations of Psychological Counselling · 30 hrs', 'Psychological Developmental Disorders · 104 hrs', 'Clinical Psychology in Gerontology · 63 hrs', 'Deviantology · 50 hrs'] },
          { t: 'Block III — Additional Clinical Modules', items: ['Fundamentals of Psychiatry · 100 hrs', 'Crisis Psychology (PTSD) · 80 hrs', 'Psychology of Addictions · 63 hrs'] },
          { t: 'Block IV — Practicum', items: ['Neuropsychology Practicum · 112 hrs', 'Pathopsychology Practicum · 161 hrs', 'Psychodiagnostics Practicum · 105 hrs', 'Child Clinical Psychology Practicum · 60 hrs'] },
          { t: 'Block V — Final Assessment', items: ['Final Interdisciplinary Examination · 12 hrs'] }
        ],
        doc: {
          t: 'Diploma of professional retraining (CPD) + IPAS certificate',
          d: 'The diploma is issued by the St Petersburg Institute of Additional Professional Education for Psychologists and Psychotherapists; it is entered in the state register FIS FRDO and requires no nostrification. An international IPAS/BPA certificate, verifiable by QR code and valid outside Azerbaijan, is issued alongside it.'
        },
        price: {
          rows: [['Full price', '$3,900'], ['Full payment (−10%)', '$3,550'], ['12-month instalment', '$330/mo.'], ['24-month instalment', '$180/mo.']],
          note: 'Payment by bank transfer or SWIFT.'
        },
        faq: [...FAQ_EN, ['Is a higher education degree required?', 'Yes. The Clinical Psychology programme requires a higher education diploma (any field; preference is given to graduates in psychology, medicine, education and social work).']]
      }
    },

    /* ===================================================== 3. ПРАКТИКУМ ПО ПСИХОТЕРАПИИ */
    practicum: {
      kind: 'long',
      reg: 2,
      sample: 'cert',
      ru: {
        title: 'Практикум по психотерапии',
        lead: 'Для специалистов, прошедших базовый курс психологии: теория сведена к минимуму, практика — к максимуму. 12 месяцев по 72 часа — 36 часов живых сессий (ролевые игры, разбор случаев, консилиум) и 36 часов видеозаписей.',
        forWhom: [
          'Имеющие высшее образование в области психологии (приветствуется)',
          'Имеющие дополнительное образование по психологии (институт или другой аккредитованный центр)',
          'Работающие в смежных с психологией областях и нуждающиеся в совершенствовании по психотерапии',
          'Занимающиеся официальным коучингом и желающие работать в этой сфере',
          'Желающие повысить профессиональные знания и навыки в области ментального здоровья'
        ],
        teachers: [['Кенан Рагимов', 'живая демонстрация реальных сессий, супервизия, итоговая аттестация']],
        facts: [
          ['Длительность', '12 месяцев'],
          ['Объём', '864 часа: 72 ч. в месяц (36 живых + 36 видео); супервизия — 2 индивидуальные сессии в месяц'],
          ['Формат', 'Онлайн + офлайн; группы до 8 человек'],
          ['Начало', 'Запись открыта'],
          ['Документ', 'Международный сертификат IPAS/BPA (проверка по QR-коду)']
        ],
        includes: [
          'Входит в программы «Общая психология» и «Клиническая психология»; можно пройти и отдельно — с выдачей сертификата',
          '2 индивидуальные сессии супервизии ежемесячно в течение года',
          'Видеоархив: более 300 занятий и более 100 записей реальных сессий',
          'Закрытая Telegram-группа практикума'
        ],
        program: [
          { t: 'I квартал', items: ['Месяц 1 — Первичная оценка и сбор анамнеза · 72 ч.', 'Месяц 2 — Психодиагностика: практика тестовых батарей · 72 ч.', 'Месяц 3 — Первая сессия при расстройствах адаптации · 72 ч.'] },
          { t: 'II квартал', items: ['Месяц 4 — Работа с депрессией и нарушениями настроения · 72 ч.', 'Месяц 5 — Тревога и панические атаки: техники экспозиции · 72 ч.', 'Месяц 6 — Травма: этап стабилизации · 72 ч.'] },
          { t: 'III квартал', items: ['Месяц 7 — Семейная динамика: системный подход · 72 ч.', 'Месяц 8 — Детская психология: нарушения развития · 72 ч.', 'Месяц 9 — Расстройства личности: долгосрочная работа · 72 ч.'] },
          { t: 'IV квартал', items: ['Месяц 10 — Психосоматика: работа с телом · 72 ч.', 'Месяц 11 — Супервизия: разбор сложных случаев · 72 ч.', 'Месяц 12 — Итоговая аттестация: анализ реального случая · 72 ч.'] },
          { t: 'Форматы практики', items: ['Ролевые игры — участники по очереди играют психолога и пациента, супервизор даёт обратную связь в реальном времени', 'Разбор случаев — групповое обсуждение реальных (анонимизированных) клинических случаев', 'Консилиум — мультидисциплинарное обсуждение сложных случаев с позиций психиатра, психолога, психотерапевта', 'Видеоархив — доступ к более чем 100 записям реальных сессий', 'Итоговая аттестация — 30-минутная работа над реальным случаем перед комиссией: анамнез, диагноз, план лечения, прогноз'] }
        ],
        doc: {
          t: 'Международный сертификат IPAS/BPA',
          d: 'Сертификат International Psychotherapy Accreditation Society (IPAS) и BPA выдаётся успешно прошедшим итоговую аттестацию. Подлинность проверяется по QR-коду на сертификате или на сайте ассоциации (intpas.com).'
        },
        price: {
          rows: [['Полная стоимость', '180 тыс. руб.'], ['При полной оплате (−20%)', '150 тыс. руб.'], ['Рассрочка 12 мес.', '15 тыс. руб./мес.'], ['Рассрочка 24 мес.', '9 тыс. руб./мес.']],
          note: 'Оплата банковским переводом или через СБП.'
        },
        faq: []
      },
      az: {
        title: 'Psixoterapiya Praktikumu',
        lead: 'Psixologiya əsas kursunu tamamlamış mütəxəssislər üçün: nəzəriyyə minimuma endirilir, praktika maksimuma çıxarılır. 12 ay, hər ay 72 saat — 36 saat canlı seans (rol oyunları, keys müzakirəsi, konsilium) və 36 saat video yazıları.',
        forWhom: [
          'Əsas ali təhsili psixologiya sahəsində olanlar (üstünlük verilir)',
          'Psixologiya Əlavə Təhsili olanlar (İnstitut və ya digər akkreditasiya olunmuş mərkəz)',
          'Psixologiya sahəsinə yaxın sahələrdə çalışan və psixoterapiya üzrə təkmilləşmə ehtiyacı olanlar',
          'Rəsmi kouçinq sahəsi ilə məşğul olan və bu sahədə fəaliyyət göstərmək istəyən şəxslər',
          'Mental sağlamlıq sahəsində peşəkar bilik və bacarıqlarını artırmaq istəyən şəxslər'
        ],
        teachers: [['Kənan Rəhimov', 'real seansların canlı nümayişi, superviziya, yekun attestasiya']],
        facts: [
          ['Müddət', '12 ay'],
          ['Həcm', '864 saat: ayda 72 saat (36 canlı + 36 video); superviziya — ayda 2 fərdi sessiya'],
          ['Format', 'Onlayn + oflayn; maksimum 8 nəfərlik qruplar'],
          ['Başlanğıc', 'Qeydiyyat açıqdır'],
          ['Sənəd', 'Beynəlxalq IPAS/BPA sertifikatı (QR kodla yoxlanılır)']
        ],
        includes: [
          '«Ümumi Psixologiya» və «Klinik Psixologiya» proqramlarına daxildir; ayrıca da keçmək olar — sertifikatla',
          '1 il boyunca aylıq 2 fərdi superviziya sessiyası',
          'Video arxiv: 300-dən çox dərs və 100+ real seans yazısı',
          'Praktikumun qapalı Telegram qrupu'
        ],
        program: [
          { t: 'I rüb', items: ['Ay 1 — İlkin qiymətləndirmə və anamnez toplama · 72 saat', 'Ay 2 — Psixodiaqnostika: test batareyası praktikası · 72 saat', 'Ay 3 — Uyğunlaşma pozuntularında ilk seans · 72 saat'] },
          { t: 'II rüb', items: ['Ay 4 — Depressiya və əhval pozuntularında iş · 72 saat', 'Ay 5 — Narahatlıq və panik ataklar: ekspozisiya texnikaları · 72 saat', 'Ay 6 — Travma: stabilizasiya mərhələsi · 72 saat'] },
          { t: 'III rüb', items: ['Ay 7 — Ailə dinamikası: sistem yanaşması · 72 saat', 'Ay 8 — Uşaq psixologiyası: inkişaf pozuntuları · 72 saat', 'Ay 9 — Şəxsiyyət pozuntuları: uzunmüddətli iş · 72 saat'] },
          { t: 'IV rüb', items: ['Ay 10 — Psixosomatika: bədən ilə iş · 72 saat', 'Ay 11 — Superviziya: mürəkkəb keyslərin müzakirəsi · 72 saat', 'Ay 12 — Yekun attestasiya: real keys təhlili · 72 saat'] },
          { t: 'Praktika formatları', items: ['Rol oyunları — iştirakçılar növbəli olaraq psixoloq və pasiyent rollarını oynayır, supervizor canlı feedback verir', 'Keys müzakirəsi — həqiqi (anonimləşdirilmiş) klinik keyslərin qrup şəklində müzakirəsi', 'Konsilium — mürəkkəb keyslərin psixiatr, psixoloq və psixoterapevt nöqteyi-nəzərindən multidisiplinar müzakirəsi', 'Video arxiv — 100+ real seans yazısına çıxış', 'Yekun attestasiya — komissiya qarşısında real keys üzərində 30 dəqiqəlik iş: anamnez, diaqnoz, müalicə planı, proqnoz'] }
        ],
        doc: {
          t: 'Beynəlxalq IPAS/BPA sertifikatı',
          d: 'International Psychotherapy Accreditation Society (IPAS) və BPA sertifikatı yekun attestasiyadan uğurla keçənlərə verilir. Sertifikatın həqiqiliyini üzərindəki QR-kodla və ya assosiasiyanın saytında (intpas.com) yoxlamaq olar.'
        },
        price: {
          rows: [['Tam qiymət', '3 600 AZN'], ['Öncədən ödənişdə (−600 AZN)', '3 000 AZN'], ['Taksit 12 ay', '300 AZN/ay'], ['Taksit 24 ay', '175 AZN/ay']],
          note: '24 aya qədər taksit imkanı — aylıq minimum 175 AZN.'
        },
        faq: []
      },
      en: {
        title: 'Psychotherapy Practicum',
        lead: 'For professionals who have completed a foundational psychology course: theory is kept to a minimum, practice is maximised. 12 months at 72 hours per month — 36 hours of live sessions (role-plays, case analysis, case conferences) and 36 hours of video recordings.',
        forWhom: [
          'Those with a basic higher education in psychology (preferred)',
          'Those with additional education in psychology (an institute or another accredited centre)',
          'Those working in fields close to psychology who need to improve in psychotherapy',
          'Those engaged in official coaching who want to work in this field',
          'Those who want to deepen professional knowledge and skills in mental health'
        ],
        teachers: [['Kenan Ragimov', 'live demonstration of real sessions, supervision, final assessment']],
        facts: [
          ['Duration', '12 months'],
          ['Volume', '864 hours: 72 hrs per month (36 live + 36 video); supervision — 2 individual sessions per month'],
          ['Format', 'Online + offline; groups of up to 8 participants'],
          ['Start', 'Enrolment is open'],
          ['Document', 'International IPAS/BPA certificate (verified by QR code)']
        ],
        includes: [
          'Included in the General Psychology and Clinical Psychology programmes; can also be taken separately, with a certificate',
          '2 individual supervision sessions per month throughout the year',
          'Video archive: over 300 lessons and over 100 recordings of real sessions',
          'A closed Telegram group for the practicum'
        ],
        program: [
          { t: 'Q1', items: ['Month 1 — Initial Assessment and History Taking · 72 hrs', 'Month 2 — Psychodiagnostics: Test Battery Practice · 72 hrs', 'Month 3 — First Session in Adjustment Disorders · 72 hrs'] },
          { t: 'Q2', items: ['Month 4 — Working with Depression and Mood Disorders · 72 hrs', 'Month 5 — Anxiety and Panic Attacks: Exposure Techniques · 72 hrs', 'Month 6 — Trauma: Stabilisation Phase · 72 hrs'] },
          { t: 'Q3', items: ['Month 7 — Family Dynamics: Systems Approach · 72 hrs', 'Month 8 — Child Psychology: Developmental Disorders · 72 hrs', 'Month 9 — Personality Disorders: Long-Term Work · 72 hrs'] },
          { t: 'Q4', items: ['Month 10 — Psychosomatics: Body-Oriented Work · 72 hrs', 'Month 11 — Supervision: Complex Case Analysis · 72 hrs', 'Month 12 — Final Assessment: Real Case Analysis · 72 hrs'] },
          { t: 'Practice formats', items: ['Role-plays — participants take turns as psychologist and client, the supervisor gives real-time feedback', 'Case analysis — group discussion of real (anonymised) clinical cases', 'Case conference — multidisciplinary discussion of complex cases from the perspectives of a psychiatrist, psychologist and psychotherapist', 'Video archive — access to over 100 recordings of real sessions', 'Final assessment — a 30-minute real case presentation before a panel: history, diagnosis, treatment plan, prognosis'] }
        ],
        doc: {
          t: 'International IPAS/BPA certificate',
          d: 'The IPAS (International Psychotherapy Accreditation Society) and BPA certificate is issued to those who pass the final assessment. Its authenticity can be verified online via the QR code on it or on the association’s website (intpas.com).'
        },
        price: {
          rows: [['Full price', '$2,150'], ['Full payment (−20%)', '$1,800'], ['12-month instalment', '$180/mo.'], ['24-month instalment', '$110/mo.']],
          note: 'Payment by bank transfer or SWIFT.'
        },
        faq: []
      }
    },

    /* ===================================================== 4. ПСИХОДИАГНОСТИКА */
    psychodiagnostics: {
      kind: 'short',
      reg: 3,
      sample: 'cert',
      ru: {
        title: 'Психодиагностика',
        lead: 'Психические функции и их измерение, психопатология, диагностика по МКБ-11 / МКБ-10 / DSM-5 — обоснование диагноза. Основной источник — справочник Кенана Рагимова «Клиническая психиатрия» на четырёх языках (азербайджанский, русский, английский, турецкий).',
        forWhom: [
          'Психологи, психотерапевты, врачи и педагоги',
          'Студенты психологических факультетов и начинающие специалисты',
          'Высшее образование не требуется; у тех, у кого есть психологическое образование, открыты более широкие возможности',
          'Запись в группу — количество мест ограничено'
        ],
        teachers: [['Кенан Рагимов', 'преподаватель и руководитель программы']],
        facts: [
          ['Длительность', '3 месяца обучения + 6 месяцев групповой супервизии'],
          ['Объём', 'Обучение: 2 раза в неделю × 2 часа; супервизия: 1 раз в неделю, 6 месяцев'],
          ['Формат', 'Очно или онлайн; видеозаписи занятий — без ограничений'],
          ['Начало', 'Запись открыта'],
          ['Документ', 'Международный сертификат IPAS']
        ],
        includes: [
          'Справочник «Клиническая психиатрия» — основной источник программы (последние международные диагностические критерии)',
          'Видеозаписи занятий — просмотр без ограничений',
          'Небольшие группы — индивидуальное внимание каждому участнику',
          'Аттестация по завершении программы'
        ],
        program: [
          { t: '1-й месяц — Общая психология', items: ['Понятие о психических функциях; различные психические функции и методы их измерения'] },
          { t: '2-й месяц — Психопатология', items: ['Психопатологические симптомы — нарушения внимания, памяти и других функций; клинические синдромы'] },
          { t: '3-й месяц — Диагностика по МКБ', items: ['На основе учебника «Клиническая психиатрия»: разделы, симптомы, обоснование диагноза, методы диагностики и подтверждения, рекомендуемая терапия'] },
          { t: 'Супервизия — 6 месяцев', items: ['В группе, 1 раз в неделю, на собственном клиническом материале участников'] }
        ],
        doc: {
          t: 'Сертификат Международной психотерапевтической ассоциации (IPAS)',
          d: 'Программу проводит RAGIMOFF; успешно завершившие обучение получают сертификат International Psychotherapy Association. Подлинность сертификата можно проверить по QR-коду на нём или на сайте ассоциации (intpas.com).'
        },
        price: {
          rows: [['Помесячно', '300 AZN × 3 месяца'], ['Единовременно (3 месяца обучения + 6 месяцев супервизии)', '800 AZN']],
          note: ''
        },
        faq: []
      },
      az: {
        title: 'Psixodiaqnostika',
        lead: 'Psixi funksiyalar və onların ölçülməsi, psixopatologiya, XBT-11 / XBT-10 / DSM-5 üzrə diaqnostika — diaqnozun əsaslandırılması. Proqramın əsas mənbəyi — Kənan Rəhimovun «Klinik Psixiatriya» sorğu kitabı: dörd dildə (Azərbaycan, rus, ingilis, türk).',
        forWhom: [
          'Psixoloqlar, psixoterapevtlər, həkimlər və pedaqoqlar',
          'Psixologiya tələbələri və yeni başlayan mütəxəssislər',
          'Ali təhsil tələb olunmur; psixologiya təhsili olanlar üçün daha geniş imkanlar açılır',
          'Qrupda iştirak üçün qeydiyyat — yerlərin sayı məhduddur'
        ],
        teachers: [['Kənan Rəhimov', 'tədrisçi və proqram rəhbəri']],
        facts: [
          ['Müddət', '3 ay təlim + 6 ay qrupda superviziya'],
          ['Həcm', 'Təlim: həftədə 2 dəfə × 2 saat; superviziya: həftədə 1 dəfə, 6 ay'],
          ['Format', 'Əyani və ya onlayn; dərs videoyazılarına limitsiz baxış'],
          ['Başlanğıc', 'Qeydiyyat açıqdır'],
          ['Sənəd', 'Beynəlxalq IPAS sertifikatı']
        ],
        includes: [
          '«Klinik Psixiatriya» sorğu kitabı — proqramın əsas mənbəyi (ən son beynəlxalq diaqnostik meyarlar)',
          'Dərslərin videoyazılarına limitsiz baxış',
          'Kiçik qruplar — hər iştirakçıya fərdi diqqət',
          'Proqramın sonunda attestasiya'
        ],
        program: [
          { t: '1-ci ay — Ümumi psixologiya', items: ['Psixi funksiyalar anlayışı; müxtəlif psixi funksiyalar və onların ölçülmə metodları'] },
          { t: '2-ci ay — Psixopatologiya', items: ['Psixopatoloji simptomlar — diqqət, yaddaş və digər funksiyaların pozuntuları; klinik sindromlar'] },
          { t: '3-cü ay — XBT üzrə diaqnostika', items: ['«Klinik Psixiatriya» dərsliyi əsasında: bölmələr, simptomlar, diaqnozun əsaslandırılması, diaqnostika və təsdiq metodları, tövsiyə olunan terapiya'] },
          { t: 'Superviziya — 6 ay', items: ['Qrupda, həftədə 1 dəfə, iştirakçıların öz klinik materialı ilə'] }
        ],
        doc: {
          t: 'Beynəlxalq Psixoterapiya Assosiasiyasının (IPAS) sertifikatı',
          d: 'Proqramı RAGIMOFF keçirir; uğurla bitirən iştirakçılar International Psychotherapy Association sertifikatını alır. Sertifikatın həqiqiliyini üzərindəki QR-kodla və ya assosiasiyanın saytında (intpas.com) yoxlamaq olar.'
        },
        price: {
          rows: [['Aylıq ödəniş', '300 AZN × 3 ay'], ['Birdəfəlik ödəniş (3 ay təhsil + 6 ay superviziya)', '800 AZN']],
          note: ''
        },
        faq: []
      },
      en: {
        title: 'Psychodiagnostics',
        lead: 'Mental functions and how they are measured, psychopathology, and diagnosis under ICD-11 / ICD-10 / DSM-5 — justifying a diagnosis. The main source is Kenan Ragimov’s reference book “Clinical Psychiatry”, in four languages (Azerbaijani, Russian, English, Turkish).',
        forWhom: [
          'Psychologists, psychotherapists, doctors and educators',
          'Psychology students and early-career specialists',
          'Higher education is not required; those with a background in psychology have wider opportunities',
          'Enrolment in the group — places are limited'
        ],
        teachers: [['Kenan Ragimov', 'tutor and head of the programme']],
        facts: [
          ['Duration', '3 months of training + 6 months of group supervision'],
          ['Volume', 'Classes: twice a week × 2 hours; supervision: weekly, 6 months'],
          ['Format', 'In person or online; class recordings available without limit'],
          ['Start', 'Enrolment is open'],
          ['Document', 'International IPAS certificate']
        ],
        includes: [
          'The reference book “Clinical Psychiatry” — the programme’s main source (the latest international diagnostic criteria)',
          'Unlimited viewing of class video recordings',
          'Small groups — individual attention for every participant',
          'Attestation at the end of the programme'
        ],
        program: [
          { t: 'Month 1 — General psychology', items: ['The concept of mental functions; the different mental functions and how they are measured'] },
          { t: 'Month 2 — Psychopathology', items: ['Psychopathological symptoms — disorders of attention, memory and other functions; clinical syndromes'] },
          { t: 'Month 3 — Diagnosis by ICD', items: ['Based on the textbook “Clinical Psychiatry”: chapters, symptoms, justifying the diagnosis, methods of diagnosis and confirmation, recommended therapy'] },
          { t: 'Supervision — 6 months', items: ['In a group, once a week, based on the participants’ own clinical material'] }
        ],
        doc: {
          t: 'Certificate of the International Psychotherapy Association (IPAS)',
          d: 'The programme is run by RAGIMOFF; graduates receive a certificate of the International Psychotherapy Association. Its authenticity can be checked with the QR code on it or on the association’s website (intpas.com).'
        },
        price: {
          rows: [['Monthly', '300 AZN × 3 months'], ['Paid at once (3 months of training + 6 months of supervision)', '800 AZN']],
          note: ''
        },
        faq: []
      }
    },

    /* ===================================================== 5. КОГНИТИВНО-ПОВЕДЕНЧЕСКАЯ ТЕРАПИЯ
       Отдельной страницы нет — только карточка на странице «Краткосрочные тренинги» (qisamuddetli.html). */
    cbt: {
      kind: 'short',
      reg: 4,
      sample: 'cert',
      ru: {
        title: 'Когнитивно-поведенческая терапия (КПТ)',
        lead: 'Основы когнитивно-поведенческой терапии и практическое применение.',
        forWhom: [],
        teachers: [['Кенан Рагимов', 'ведёт программу']],
        facts: [
          ['Длительность', '3 месяца обучения + 6 месяцев групповой супервизии'],
          ['Объём', 'Супервизия: 1 раз в неделю, 6 месяцев'],
          ['Формат', ''],
          ['Начало', 'Запись открыта'],
          ['Документ', 'Международный сертификат']
        ],
        includes: [],
        program: [],
        doc: { t: 'Международный сертификат', d: '' },
        price: {
          rows: [['Помесячно', '300 AZN × 3 месяца'], ['Единовременно (3 месяца обучения + 6 месяцев супервизии)', '800 AZN']],
          note: ''
        },
        faq: []
      },
      az: {
        title: 'Koqnitiv-davranış terapiyası (KDT)',
        lead: 'Koqnitiv-davranış terapiyasının əsasları və praktik tətbiqi.',
        forWhom: [],
        teachers: [['Kənan Rəhimov', 'proqramı aparır']],
        facts: [
          ['Müddət', '3 ay təlim + 6 ay qrupda superviziya'],
          ['Həcm', 'Superviziya: həftədə 1 dəfə, 6 ay'],
          ['Format', ''],
          ['Başlanğıc', 'Qeydiyyat açıqdır'],
          ['Sənəd', 'Beynəlxalq sertifikat']
        ],
        includes: [],
        program: [],
        doc: { t: 'Beynəlxalq sertifikat', d: '' },
        price: {
          rows: [['Aylıq ödəniş', '300 AZN × 3 ay'], ['Birdəfəlik ödəniş (3 ay təhsil + 6 ay superviziya)', '800 AZN']],
          note: ''
        },
        faq: []
      },
      en: {
        title: 'Cognitive Behavioural Therapy (CBT)',
        lead: 'Foundations of cognitive behavioural therapy and its practical use.',
        forWhom: [],
        teachers: [['Kenan Ragimov', 'leads the programme']],
        facts: [
          ['Duration', '3 months of training + 6 months of group supervision'],
          ['Volume', 'Supervision: weekly, 6 months'],
          ['Format', ''],
          ['Start', 'Enrolment is open'],
          ['Document', 'International certificate']
        ],
        includes: [],
        program: [],
        doc: { t: 'International certificate', d: '' },
        price: {
          rows: [['Monthly', '300 AZN × 3 months'], ['Paid at once (3 months of training + 6 months of supervision)', '800 AZN']],
          note: ''
        },
        faq: []
      }
    },

    /* ===================================================== 6. ПСИХОАНАЛИЗ */
    psychoanalysis: {
      kind: 'short',
      reg: 5,
      sample: 'cert',
      ru: {
        title: 'Психоанализ',
        lead: 'Теоретический курс по наследию Зигмунда Фрейда и 6 месяцев клинической супервизии. В теоретической части изучается понятийный аппарат психоанализа: бессознательное, сопротивление, толкование сновидений, оговорки, защитные механизмы, детская сексуальность, перенос и контрперенос.',
        forWhom: [
          'Психологи, психотерапевты, врачи и педагоги',
          'Студенты психологических факультетов и начинающие специалисты',
          'Готовые работать с текстами Фрейда',
          'Высшее образование не требуется; у тех, у кого есть психологическое образование, открыты более широкие возможности'
        ],
        teachers: [['Кенан Рагимов', 'преподаватель и руководитель программы; автор проекта перевода наследия Фрейда на азербайджанский язык']],
        facts: [
          ['Длительность', '3 месяца теории + 6 месяцев групповой супервизии'],
          ['Объём', '48 часов теории + 24 сессии супервизии'],
          ['Формат', 'Очно или онлайн; видеозаписи занятий — без ограничений'],
          ['Начало', 'Запись открыта'],
          ['Документ', 'Международный сертификат IPAS']
        ],
        includes: [
          'Бонус: все 24 книги Зигмунда Фрейда впервые в Азербайджане переведены с оригинального немецкого языка на азербайджанский и будут доступны студентам программы',
          'Видеозаписи занятий — просмотр без ограничений',
          'Небольшие группы — индивидуальное внимание каждому участнику',
          'Аттестация по завершении программы'
        ],
        program: [
          { t: 'Модуль 1 — Теория · 3 месяца (2×2 часа в неделю)', items: ['Бессознательное, топическая модель психического аппарата, сопротивление · 16 ч.', 'Толкование сновидений, оговорки, символ и язык · 16 ч.', 'Защитные механизмы, детская сексуальность, перенос и контрперенос · 16 ч.'] },
          { t: 'Модуль 2 — Супервизия · 6 месяцев (1 раз в неделю)', items: ['Еженедельные супервизионные сессии на собственном клиническом материале (материал анонимизируется, разбор — в группе) · 24 сессии'] }
        ],
        doc: {
          t: 'Сертификат Международной психотерапевтической ассоциации (IPAS)',
          d: 'Программу проводит RAGIMOFF; успешно завершившие обучение получают сертификат International Psychotherapy Association. Подлинность сертификата можно проверить по QR-коду на нём или на сайте ассоциации (intpas.com).'
        },
        price: {
          rows: [['Помесячно', '300 AZN × 3 месяца'], ['Единовременно (3 месяца обучения + 6 месяцев супервизии)', '800 AZN']],
          note: ''
        },
        faq: []
      },
      az: {
        title: 'Psixoanaliz',
        lead: 'Ziqmund Freydin irsi üzərində qurulmuş nəzəri kurs və 6 aylıq klinik superviziya. Nəzəri hissədə psixoanalizin anlayış aparatı öyrənilir: şüursuzluq, müqavimət, yuxuların yozumu, sürüşmələr, müdafiə mexanizmləri, uşaq cinsi inkişafı, transfer və əks-transfer.',
        forWhom: [
          'Psixoloqlar, psixoterapevtlər, həkimlər və pedaqoqlar',
          'Psixologiya tələbələri və yeni başlayan mütəxəssislər',
          'Freyd mətnləri ilə işləməyə hazır olanlar',
          'Ali təhsil tələb olunmur; psixologiya təhsili olanlar üçün daha geniş imkanlar açılır'
        ],
        teachers: [['Kənan Rəhimov', 'tədrisçi və proqram rəhbəri; Freyd irsinin Azərbaycan dilinə tərcüməsi layihəsinin müəllifi']],
        facts: [
          ['Müddət', '3 ay nəzəriyyə + 6 ay qrupda superviziya'],
          ['Həcm', '48 saat nəzəriyyə + 24 superviziya sessiyası'],
          ['Format', 'Əyani və ya onlayn; dərs videoyazılarına limitsiz baxış'],
          ['Başlanğıc', 'Qeydiyyat açıqdır'],
          ['Sənəd', 'Beynəlxalq IPAS sertifikatı']
        ],
        includes: [
          'Bonus: Ziqmund Freydin 24 kitabı Azərbaycanda ilk dəfə orijinal alman dilindən Azərbaycan dilinə tərcümə edilib və proqramın tələbələri üçün əlçatan olacaq',
          'Dərslərin videoyazılarına limitsiz baxış',
          'Kiçik qruplar — hər iştirakçıya fərdi diqqət',
          'Proqramın sonunda attestasiya'
        ],
        program: [
          { t: 'Modul 1 — Nəzəriyyə · 3 ay (həftədə 2×2 saat)', items: ['Şüursuzluq, psixi aparatın topik modeli, müqavimət anlayışı · 16 saat', 'Yuxuların yozumu, sürüşmələr, simvol və dil · 16 saat', 'Müdafiə mexanizmləri, uşaq cinsi inkişafı, transfer və əks-transfer · 16 saat'] },
          { t: 'Modul 2 — Superviziya · 6 ay (həftədə 1 dəfə)', items: ['İştirakçıların öz klinik materialı ilə həftəlik superviziya sessiyaları (material anonimləşdirilir, müzakirə qrupda aparılır) · 24 sessiya'] }
        ],
        doc: {
          t: 'Beynəlxalq Psixoterapiya Assosiasiyasının (IPAS) sertifikatı',
          d: 'Proqramı RAGIMOFF keçirir; uğurla bitirən iştirakçılar International Psychotherapy Association sertifikatını alır. Sertifikatın həqiqiliyini üzərindəki QR-kodla və ya assosiasiyanın saytında (intpas.com) yoxlamaq olar.'
        },
        price: {
          rows: [['Aylıq ödəniş', '300 AZN × 3 ay'], ['Birdəfəlik ödəniş (3 ay təhsil + 6 ay superviziya)', '800 AZN']],
          note: ''
        },
        faq: []
      },
      en: {
        title: 'Psychoanalysis',
        lead: 'A theory course based on Sigmund Freud’s legacy and six months of clinical supervision. The theoretical part covers the conceptual apparatus of psychoanalysis: the unconscious, resistance, dream interpretation, slips of the tongue, defence mechanisms, infantile sexuality, transference and countertransference.',
        forWhom: [
          'Psychologists, psychotherapists, doctors and educators',
          'Psychology students and early-career specialists',
          'Those ready to work with Freud’s texts',
          'Higher education is not required; those with a background in psychology have wider opportunities'
        ],
        teachers: [['Kenan Ragimov', 'tutor and head of the programme; author of the project translating Freud’s legacy into Azerbaijani']],
        facts: [
          ['Duration', '3 months of theory + 6 months of group supervision'],
          ['Volume', '48 hours of theory + 24 supervision sessions'],
          ['Format', 'In person or online; class recordings available without limit'],
          ['Start', 'Enrolment is open'],
          ['Document', 'International IPAS certificate']
        ],
        includes: [
          'Bonus: all 24 books by Sigmund Freud, translated from the original German into Azerbaijani for the first time in Azerbaijan, will be available to the students of this programme',
          'Unlimited viewing of class video recordings',
          'Small groups — individual attention for every participant',
          'Attestation at the end of the programme'
        ],
        program: [
          { t: 'Module 1 — Theory · 3 months (2×2 hours weekly)', items: ['The unconscious, the topographical model of the mind, resistance · 16 hrs', 'Dream interpretation, slips, symbol and language · 16 hrs', 'Defence mechanisms, infantile sexuality, transference and countertransference · 16 hrs'] },
          { t: 'Module 2 — Supervision · 6 months (once a week)', items: ['Weekly supervision sessions based on the participant’s own clinical material (material is anonymised and discussed in the group) · 24 sessions'] }
        ],
        doc: {
          t: 'Certificate of the International Psychotherapy Association (IPAS)',
          d: 'The programme is run by RAGIMOFF; graduates receive a certificate of the International Psychotherapy Association. Its authenticity can be checked with the QR code on it or on the association’s website (intpas.com).'
        },
        price: {
          rows: [['Monthly', '300 AZN × 3 months'], ['Paid at once (3 months of training + 6 months of supervision)', '800 AZN']],
          note: ''
        },
        faq: []
      }
    },

    /* ===================================================== 7. СЕМЕЙНАЯ ТЕРАПИЯ */
    family: {
      kind: 'short',
      reg: 6,
      sample: 'cert',
      ru: {
        title: 'Семейная терапия',
        lead: 'Отношения в паре, связь родителя с ребёнком и работа с трудными подростками — терапия и обучение. Два модуля: «Терапия пары» и «Отношения родителя и ребёнка».',
        forWhom: [
          'Психологи и школьные психологи',
          'Педагоги и коучи',
          'Студенты',
          'Родители',
          'Высшее образование не требуется'
        ],
        teachers: [['Самира Рагимова', 'ведёт тренинг: отношения в паре, связь родителя с ребёнком, трудные подростки']],
        facts: [
          ['Длительность', '3 месяца обучения + 6 месяцев групповой супервизии'],
          ['Объём', 'Каждый модуль: 48 часов обучения (2 раза в неделю по 2 часа) и 48 часов супервизии (раз в неделю); 16 занятий в модуле'],
          ['Формат', 'Очно или онлайн (цена одинакова); вторник и четверг, 14:00–16:00'],
          ['Начало', 'Запись открыта'],
          ['Документ', 'Сертификат IPAS (в конце курса — экзамен)']
        ],
        includes: [
          'Видеозаписи занятий — можно заранее посмотреть урок каждого преподавателя',
          'Супервизия 6 месяцев, раз в неделю',
          'Экзамен и сертификат Международной ассоциации психотерапии в конце курса'
        ],
        program: [
          { t: 'Модуль 1 — Терапия пары (отношения мужчины и женщины)', items: ['Выявление дисгармонии в семейной системе — диагностика', 'Первичный приём в терапии пары', 'Разбор конфликтной ситуации', 'Генограмма — жизненный цикл семьи', 'Определение ролей в семейной системе и напряжённые границы', 'Психодрама — психотерапевтические техники в модели семьи', 'Неписаные правила — распределение обязанностей и цена их нарушения', 'Выявление паттернов в отношениях', 'Применение методов классических и современных школ семейной терапии', 'Круг задач, которые решает системная семейная терапия', 'Удовлетворение личных потребностей и свобода выбора', 'Методы коммуникации (теория Г. Бейтсона)', 'Психотерапевтические приёмы в семейных отношениях и разбор случаев', 'Работа в критический период (измена, насилие, подход на пороге развода)', 'Разбор отношений с человеком, страдающим зависимостью (алкоголь, наркотики, игра и др.)', 'Поддерживающий этап в семейной терапии'] },
          { t: 'Модуль 2 — Отношения родителя и ребёнка (семейная терапия для родителей)', items: ['Этапы психофизиологического развития ребёнка', 'Критические моменты этапов развития', 'Диагностика по признакам в семейной терапии', 'Функциональные нарушения внутри семьи', 'Системный разбор семейных историй', 'Построение модели общения с ребёнком', 'Выходы из напряжённых отношений, коррекция родительских методов воспитания', 'Модели поведения детей в проблемных семьях', 'Невротические и поведенческие нарушения у детей', 'Игровая терапия — коррекция модели поведения', 'Агрессивное поведение у детей — модель наказания', 'Детские страхи и практические выходы', 'Проблемы отставания в учёбе', 'Регуляция психики детей в неполной семье', 'Методы полового воспитания в семье', 'Управление семейными отношениями с человеком с особым заболеванием или ограничением поведения'] }
        ],
        doc: {
          t: 'Сертификат Международной психотерапевтической ассоциации (IPAS)',
          d: 'Программу проводит RAGIMOFF; успешно завершившие обучение получают сертификат International Psychotherapy Association. Подлинность сертификата можно проверить по QR-коду на нём или на сайте ассоциации (intpas.com).'
        },
        price: {
          rows: [['Помесячно', '300 AZN × 3 месяца'], ['Единовременно (3 месяца обучения + 6 месяцев супервизии)', '800 AZN']],
          note: 'Цена одинакова очно и онлайн.'
        },
        faq: []
      },
      az: {
        title: 'Ailə terapiyası',
        lead: 'Kişi-qadın münasibətləri, valideyn-övlad bağı və çətin yeniyetmələrlə iş — terapiya və təlim. İki modul: «Cütlük Terapiyası» və «Valideyn-Övlad Münasibətləri».',
        forWhom: [
          'Psixoloqlar və məktəb psixoloqları',
          'Müəllimlər və koçlar',
          'Tələbələr',
          'Valideynlər',
          'Ali təhsil tələb olunmur'
        ],
        teachers: [['Samirə Rəhimova', 'təlimi aparır: kişi-qadın münasibətləri, valideyn-övlad bağı, çətin yeniyetmələrlə iş']],
        facts: [
          ['Müddət', '3 ay təlim + 6 ay qrupda superviziya'],
          ['Həcm', 'Hər modul: 48 saat tədris (həftədə 2 dəfə, hər dərs 2 saat) və 48 saat superviziya (həftədə 1 dəfə); modulda 16 dərs'],
          ['Format', 'Əyani və ya onlayn (qiymət eynidir); çərşənbə axşamı və cümə axşamı, saat 14:00–16:00'],
          ['Başlanğıc', 'Qeydiyyat açıqdır'],
          ['Sənəd', 'IPAS sertifikatı (kursun sonunda imtahan)']
        ],
        includes: [
          'Təlimin video yazıları — hər iki təlimatçının dərsinə əvvəlcədən baxa bilərsiniz',
          '6 ay superviziya, həftədə 1 dəfə',
          'Kursun sonunda imtahan və Beynəlxalq Psixoterapiya Assosiasiyasının sertifikatı'
        ],
        program: [
          { t: 'Modul 1 — Cütlük Terapiyası (kişi-qadın münasibətləri)', items: ['Ailə sistemində disharmoniyanın müəyyən edilməsi — diaqnostika', 'Cütlük terapiyasında ilkin qəbul', 'Münaqişəli vəziyyətin təhlili', 'Genoqramma — ailənin həyat dövrü', 'Ailə sistemində rolların müəyyən olunması və gərgin sərhədlər', 'Psixodrama — ailə modelində psixoterapevtik texnikalar', 'Yazılmayan qaydalar — öhdəliklərin paylaşılması və pozulduqda cəzası', 'Münasibətlərdə patternlərin müəyyən olunması', 'Ailə terapiyasında klassik və müasir məktəblərinin metodların tətbiqi', 'Sistemli Ailə Terapiyasının həll etdiyi problemlər dairəsi', 'Şəxsi ehtiyacların ödənilməsi və seçim azadlığı', 'Kommunikasiya metodları (Q. Beytson nəzəriyyəsi)', 'Ailə münasibətlərində psixoterapevtik üsullar və hazır keyslər', 'Kritik dönəmdə iş prosesi (xəyanət, təcavüz, boşanma ərəfəsində psixoterapevtik yanaşma)', 'Asılılığın müxtəlif formalarından (alkoqol, narkotik, qumar və s.) əziyyət çəkənlə münasibətin təhlili', 'Ailə terapiyasında dəstəkləyici mərhələ'] },
          { t: 'Modul 2 — Valideyn-Övlad Münasibətləri (valideynlər üçün ailə terapiyası)', items: ['Uşağın psixo-fizioloji inkişaf mərhələləri', 'İnkişaf mərhələlərində kritik məqamlar', 'Ailə terapiyasında əlamətlərə görə diaqnostika', 'Ailə daxilində funksional pozuntular', 'Ailə əhvalatlarının sistemli təhlil prosesi', 'Uşaqla ünsiyyət modelinin qurulması', 'Gərgin münasibətlərdən çıxış yolları, valideynlərin tərbiyə metodlarının korreksiyası', 'Problemli ailələrdə uşaqların davranış modelləri', 'Uşaqlarda nevrotik və davranış pozuntuları', 'Oyun terapiyası — davranış modelinin korreksiyası', 'Uşaqlarda aqressiv davranışlar — cəza modeli', 'Uşaqlarda qorxular və praktiki çıxış yolları', 'Tədris və təhsildən geridə qalma problemləri', 'Natamam ailədə uşaqların psixikasının tənzimlənməsi', 'Ailədə cinsi tərbiyə metodları', 'Xüsusi xəstəlik və ya davranış məhdudiyyəti olan insanlarla ailə münasibətlərinin idarə olunması'] }
        ],
        doc: {
          t: 'Beynəlxalq Psixoterapiya Assosiasiyasının (IPAS) sertifikatı',
          d: 'Proqramı RAGIMOFF keçirir; uğurla bitirən iştirakçılar International Psychotherapy Association sertifikatını alır. Sertifikatın həqiqiliyini üzərindəki QR-kodla və ya assosiasiyanın saytında (intpas.com) yoxlamaq olar.'
        },
        price: {
          rows: [['Aylıq ödəniş', '300 AZN × 3 ay'], ['Birdəfəlik ödəniş (3 ay təhsil + 6 ay superviziya)', '800 AZN']],
          note: 'Əyani və onlayn üçün qiymət eynidir.'
        },
        faq: []
      },
      en: {
        title: 'Family therapy',
        lead: 'Couple relationships, the parent-child bond and work with difficult adolescents — therapy and training. Two modules: “Couple Therapy” and “Parent-Child Relationships”.',
        forWhom: [
          'Psychologists and school psychologists',
          'Teachers and coaches',
          'Students',
          'Parents',
          'A degree is not required'
        ],
        teachers: [['Samira Ragimova', 'leads the training: couple relationships, the parent-child bond, difficult adolescents']],
        facts: [
          ['Duration', '3 months of training + 6 months of group supervision'],
          ['Volume', 'Each module: 48 hours of classes (twice a week, 2 hours each) and 48 hours of supervision (once a week); 16 lessons per module'],
          ['Format', 'In person or online (same price); Tuesday and Thursday, 14:00–16:00'],
          ['Start', 'Enrolment is open'],
          ['Document', 'IPAS certificate (the course ends with an exam)']
        ],
        includes: [
          'Video recordings of the training — you can watch a class by each trainer in advance',
          '6 months of supervision, once a week',
          'An exam and a certificate from the International Psychotherapy Association at the end of the course'
        ],
        program: [
          { t: 'Module 1 — Couple Therapy (man-woman relationships)', items: ['Identifying disharmony in the family system — assessment', 'The intake session in couple therapy', 'Analysis of the conflict situation', 'The genogram — the family life cycle', 'Defining roles in the family system and strained boundaries', 'Psychodrama — psychotherapeutic techniques in the family model', 'Unwritten rules — sharing obligations and the cost of breaking them', 'Identifying patterns in the relationship', 'Applying methods from classical and contemporary schools of family therapy', 'The range of problems systemic family therapy addresses', 'Meeting personal needs and freedom of choice', 'Methods of communication (G. Bateson’s theory)', 'Psychotherapeutic techniques in family relationships and worked cases', 'Work in a critical period (infidelity, abuse, the approach on the verge of divorce)', 'Analysing the relationship with a person suffering from addiction (alcohol, drugs, gambling and so on)', 'The supportive stage in family therapy'] },
          { t: 'Module 2 — Parent-Child Relationships (family therapy for parents)', items: ['Stages of a child’s psychophysiological development', 'Critical points in the stages of development', 'Symptom-based assessment in family therapy', 'Functional disorders within the family', 'Systemic analysis of family stories', 'Building a model of communication with the child', 'Ways out of strained relationships, correcting parental methods', 'Children’s behaviour patterns in troubled families', 'Neurotic and behavioural disorders in children', 'Play therapy — correcting the behaviour model', 'Aggressive behaviour in children — the punishment model', 'Children’s fears and practical ways out', 'Problems of falling behind in schooling', 'Regulating a child’s psyche in a single-parent family', 'Methods of sex education in the family', 'Managing family relationships with a person who has a specific illness or behavioural limitation'] }
        ],
        doc: {
          t: 'Certificate of the International Psychotherapy Association (IPAS)',
          d: 'The programme is run by RAGIMOFF; graduates receive a certificate of the International Psychotherapy Association. Its authenticity can be checked with the QR code on it or on the association’s website (intpas.com).'
        },
        price: {
          rows: [['Monthly', '300 AZN × 3 months'], ['Paid at once (3 months of training + 6 months of supervision)', '800 AZN']],
          note: 'The price is the same in person and online.'
        },
        faq: []
      }
    }
  }
};
