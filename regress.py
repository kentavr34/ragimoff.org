# -*- coding: utf-8 -*-
"""
regress.py — сторож: дефекты, которые уже исправлены, не должны вернуться.

Каждая строка ниже когда-то стояла в книге и была найдена сплошным чтением
азербайджанского мастера и трёх переводов. Список нужен затем, чтобы
пересборка, массовая замена или новая правка не воскресили их незаметно.

    python regress.py          # 0 — чисто; иначе список воскресших
"""
from __future__ import annotations
import re, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
BOOK = ROOT / 'klinik-psixiatriya'
DIRS = {'az': BOOK, 'ru': BOOK / 'ru', 'en': BOOK / 'en', 'tr': BOOK / 'tr'}

# язык → строки, которых больше быть не должно
GONE = {
 'az': [
    # очередь 1 §8 глава 14 — ОВР был привязан к чужому коду, 2026-08-15
    '(ODD, XBT-11 <span class="icd">6C91</span>)',
    # очередь 1 §8 глава 13 — английские обломки в мастере, 2026-08-15
    'ood stabilizator', 'Group support (S-Anon',
    # канон первичного звена — «birinci tibbi yardım» (Кенан 2026-08-15);
    # «ilk tibbi yardım» это первая помощь, другое понятие
    'ilkin tibbi yardım', 'birinci yardım səviyyəsində',
    # очередь 1 §8 глава 12 — NG219 и MacArthur, 2026-08-15
    'NICE CG52, NG219', 'mortalitet və HIV transmissiyasını əhəmiyyətli azaldır (MacArthur',
    # очередь 1 §8 глава 11 — 6C20, 2026-08-15
    'səviyyəsində integrate care', 'Birinci yardım səviyyəsində KDT',
    # очередь 1 §8 глава 10 — обломки в 6C01, 2026-08-15
    'aylıq-illik dozada', 'enemadan üstündür (tövsiyə edilmir',
    # очередь 1 §8 глава 09 — CBT-E, рефидинг, лиздексамфетамин, 2026-08-15
    '40 seans 20 həftə', 'Başlanğıc 20 kkal/kq/gün', 'günlük 30–70 mq',
    # очередь 1 §8 глава 08 — «сопротивление» вместо «совладания», 2026-08-15
    'müqavimət (coping)',
    # очередь 1 §8 глава 07 — обломки текста, 2026-08-15
    'göstərənnu', '+ ya da pre-trauma',
    # очередь 1 §8 глава 06 — Foa 2005, Crerand, Tolin, 2026-08-13
    'ERP + SSRİ</strong> — orta-ağır OKP-də monoterapiyadan üstün',
    'Plast Reconstr Surg 2010', 'Depress Anxiety 2015 RKİ',
    # очередь 1 §8 глава 05 — FDA, APA, Wolitzky-Taylor, 2026-08-13
    'esitalopram, paroksetin — FDA',
    'APA Clinical Practice Guideline for the Treatment of Anxiety Disorders',
    'ekspozisiya farmakoterapiyadan üstün',
    # очередь 1 §8 главы 03–04 — Cipriani 2018, FDA, Miklowitz, 2026-08-13
    'Tepevtik səviyyə', 'Miklowitz D.J. Am J Psychiatry 2003',
    'reboxetin uyğunlaşmada (acceptability) ən yüksək',
    'kvetiapin (FDA təsdiqi), lurasidon',
    # очередь 1 §8 глава 02 — Leucht 2012, FDA, Health Affairs, 2026-08-13
    '5 dəfə artırır (Leucht', 'Lancet Psychiatry 2016;3(2):158–169',
    'FDA tərəfindən şizoaffektiv pozuntu üçün xüsusi təsdiq edilmişdir',
    # очередь 1 §8 глава 01 — сверка с FDA и PubMed, 2026-08-12
    'FDA 5–17 yaşlı RAS', 'Cortese 2018 meta-analiz İD fonunda effektivliyi təsdiqləyir',
    'Tourette sindromunda 6–17 yaş', '<td>100–400 mq/gün</td><td>FDA 2021; uşaqlar və yetkinlər',
    # §N «О книге» обещала несуществующую структуру, 2026-08-12
    'Tarixi konsepsiyalar', 'Bölmə 4-ə baxın (KTTD',
    '<li><strong>Monitorinq</strong> — Bölmə 9.</li>',
    'Klinik formalar</strong> (lazım olduqda)',
    # §M вставка вместо названия классификации и метки таблиц, 2026-08-12
    'Tələblər for WHO', 'The development of the WHO, 2019',
    'Reed GM, , Reed GM', 'qüvvəyə minmə 2022 — XBT-11:',
    '(ODD, WHO, 2019, qüvvəyə minmə 2022',
    '<td lang="en">ŞİZOFRENİYA SPEKTRİ', '<td lang="ru">KATATONİYA',
    '<span lang="en">First MB</span>', '<span lang="en">Swanson JM</span>',
    # §H2 вводные страницы, 2026-08-12
    '«– OKP üçün).»>ERP',
    # §H часть 2 — вводные страницы, 2026-08-12
    '«Düzəliş et» düyməsi var', 'Düzəlt düyməsinə basaraq',
    '103 pozuntu', 'AACE, APA, NICE',
    # §H справочные страницы и навигация, 2026-08-12
    # §G главы 7, 8, 16, 17, 2026-08-12
    'HA40.Z', 'HA40 Sexual dysfunction associated with disorder',
    # §F 6B80, 2026-08-12
    'XBT-11 — paralel; «atypical sinir anoreksiyası»',
    # §E коды против ICD-11 MMS, 2026-08-12
    'Statistics. 8A05 Primary tics', 'ICD-11. 7A21 Hypersomnolence',
    'ICD-11. 7A60 Circadian', 'ICD-11. GA34 Premenstrual',
    'ICD-11. HA01 Erectile', 'ICD-11. HA02 Anorgasmia', 'ICD-11. HA03 Early',
    '<span class="icd">8A05</span>', '<span class="icd">GA34</span>',
    '<span class="icd">HA01</span>', '<span class="icd">HA02</span>',
    '<span class="icd">HA03</span>', '<span class="icd">7A21</span>',
    '<span class="icd">7A60</span>',
    # §11 «Источники», 2026-08-12
    'Coccaro E.F. et al. tədqiqatları',
    # обломки слов
    'həyətəm', 'rağın', 'qıdaşma', 'qıdaşdırma', 'yaşıq,', 'parmaq qılığı',
    'sıxılı', 'tezliyi artım', 'qıçtı', 'çiknə', 'weksloid', 'qaz-zəkam',
    'kütəbə', 'əkstərkib', 'ƏKSTƏRKİBDIR', 'amestik', 'rectisivism',
    'mekatinon', 'deliriya', 'hiperarausal', 'simulyasiya-dən',
    'əlilli qayğı göstərənda', 'formasıilə',
    # турецкие формы вместо азербайджанских
    'geç ', 'kategoriya', 'Patlayıcı', 'bunaması', 'Tetikleyicilər',
    'sxizofreniya', 'Yatak baxımı', 'utuş',
    # английский внутри азербайджанской прозы
    'subthreshold', 'Reality testing', 'premenarchal',
    'manik-depresiv insanity', 'performans-only', 'inkapasitə', 'nutrisional',
    'gain motivasiyası', '<td>Malingering</td>', 'gum çeynəmə',
    'World Health Organization tərəfindən', 'atypical cinsi maraq',
    'Other Specified Parafiliya', 'qulluqçu', 'İşıqlandırılmış',
    'Aclı qlükoza', 'Maximum uzunluq', 'Kənar məqsəd', 'episodic harmful use',
    # незакрытые конструкции
    'kimi rəsmiyyət', '» rəsmiyyət', 'Recurrent rəsmiyyət', 'YOXdur',
    'AYRI kateqoriya', 'Fiziki təmkin',
    # фактические
    '1830-cu illərdə Pinel', 'Kraft-Ebing', 'hippokampotomiya',
    'qabaqlanan mortalite', 'Kahlbaum, Kraft-Ebing',
    # служебные пометки редактора
    'dəqiq şəkildə təkrarlanmalıdır', 'Source-whitelist bodies',
    'to be completed from the indexed record',
    # §10 «Мифы»: сплошное чтение 104 карточек
    'magic təfəkkür', 'supersitsiyalar', '«günah ifa edən övlad»',
    'mitozda T21 nondisjunction', 'qıtlığa nəzarətli', 'qabaqlanan səbəb',
    'ön-qabaqlanan', 'komada-dır', 'underdiagnosed sindromdur',
    'psixoloji break-down', 'kötukdür', 'illüzionukdur',
    'Yatak yatma', 'məşgəliyyat təhlükəsizliyi', 'reality testing pozulmuş',
    'ruhani uyanış', 'duhalıq', 'dühalıq',
    'sürətli sikllaşma', 'klinik utility', 'kontrindikasiyadır',
    'Underdiagnosis', 'overdiagnosis-dan', 'General Medical Council məlumatlandırması',
    'YOXDUR', 'MÜTLƏQDİR', 'HƏR İKİ',
    # §7–§9 «Обследование · Лечение · Прогноз»
    'böy,', 'çocluqluq', 'interocaeptiv',
    'psixoeducation', 'psikoeducational', 'Specifik',
    'psixoedukation', 'hospitalize', 'Phase-oriented (üç fazalı)',
    'self-harm', 'Pillə 2: guided self-help',
    'housebound', 'wait-list', 'Lisdexamfetamine',
    'D-cycloserine', 'Diaphragmatic breathing', 'Nutrisional',
    'sodium oxybate', 'Wakefulness-promoting', 'diphenhydramine',
    'felaket', 'kardiyak', 'İnteqrə ',
    'psixosocial', 'multidisiplinarlı', 'öz-öz idarə',
    'BİRİNCİ SIRA', 'yatak öncəsi', 'yulduz çartı',
    'obscene', 'serotonergic', 'stroke,',
    'Koksu yağı', 'alternative izah', 'magic',
    '1-bir-bir',
    # справочные страницы: список сокращений и глоссарий
    'skrinninq', 'skrining',
    'Atipik (İkinci Nəsil) Antipsixotiklər', '<td>MDP</td>',
    'ARFİD', 'Huzursuz Bacaq',
    'Tip Iı', 'Oppositional Defiant Disorder (6C91)',
    'Early/Premature Ejaculation (HA01)', 'Avoidant/Restrictive Food Intake Disorder (6B85)',
    '6B64–6B6Z', '6C91–6C9Z',
    '6E61–6E6Z', 'HA01–HA0Z',
    # контрольная вычитка 2026-08-10, §1–§6
    'motorin və nitq', 'məktəb adheziyası', 'ümbrella',
    'yaşa qədər tutur', 'aşağı, mülayim, ağır, dərin', 'hipotetik təxəyyül',
    'az-aşkarlanma', '\x08Severity bölgüsü', 'Severity bölgüsü',
    'DSÖ', 'Qarşısıalan', 'Vilson xəstəliyi',
    'valideyndə müalicəsiz', 'Valideyndə valproat', 'dementiya',
    # контрольная вычитка 2026-08-10, партии 3–5
    'ekstra-eqo', 'hipersəs', 'məhkəmə edən səs',
    '\x08vaaq\x08', 'Hüzursuzluq', 'bulantı',
    'overprotection', 'neurotizm', 'noradrenergic',
    'separation anxiety tarixçəsi', 'irritabəl bağırsaq', 'meydan, çay',
    'qıdaş', '«acne»', 'hipervigilance',
    'asanlıqla startle', 'Self-organization', 'Self-Organization',
    'delayed onset',
    # контрольная вычитка 2026-08-10, партия 6
    'gizlin', '\x08dieta\x08', 'hyperphagia',
    'çatışmazlığılar', 'nutritional supplement', 'Krohn',
    'Qidalı dəyəri', 'Gain motivasiyası', 'post-prandial',
    'gastroparesis', 'over-aktiv', 'urinary infection',
    'holding maneuvers', 'kemping', 'motility tədqiqat',
    # контрольная вычитка §1–§6: карточки 6C51–HA40
    'nevroinkişaf', 'klinisist', '«imkansız»', 'neglect', 'sexual abuse',
    'İnsight', 'komplex', 'Münxauzen', 'tutmalar, apnoea', 'overanxious',
    'Separation test', 'superimposed on demensiya', 'UNDERDIAGNOSED',
    'göstəricilər-dan', 'intensive care', 'X-ray', '-1 to -2',
    'pasiyent əksinə', 'yalan ola bilər', 'induksiyalı və ya yalan',
    'plakatlar', 'tangllar', 'dudaq-yutma', 'identifikasiya itkisi',
    'hava çirkliliyi', 'urinary', 'saxlamamazlıq', 'hiperlipidemia',
    'Hipoperfusiya', 'abulia', 'çətirini', 'ribot qanunu',
    'uyumsuzluq', 'Klein-Levin', 'hiperinsomniya', 'İskandinaviya',
    'dezoryentasiya', 'Respirator effort', 'iş çəkənlər', 'clock gen',
    'zəbtsiz', 'Histaminergic', 'ehkalaliya', 'bazal ganglia',
    'qəzəbli partlayış', 'tikler', 'somatic urge', 'məktəbdə tutma',
    'yetişkinlik', 'mediadan kopya', 'labilliyə', 'ovariy', 'süpressiya',
    # «urologic» стоит с уточнением: подстрока входит в neurological,
    # «Pelvic» — в официальное имя DSM Genito-Pelvic, «carbohydrate» —
    # в лабораторный термин carbohydrate-deficient transferrin.
    'Serotonergic', 'carbohydrate ehtiyacı', 'polikistik over', 'Pelvic ağrı',
    'Sosial-kulturel', 'göstərilərkən', 'neyrogenic', 'Erektion',
    'erektion', 'Orgazm', 'delayed eyakulyasiya', 'bilgi çatışmazlığı',
    'və urologic', 'algı pozulması', 'Stranger danger', 'pelvik döşəmə',
    'Deep dispareunia', 'qadağa təhsil', 'cərrahiyyə yara',
    'kannabis xronik', 'xroniki böyrək', 'reflektor tensiyası',
    # второй проход: английские вставки в аз. прозе вне скобок и кавычек
    # «habit selection» осталось как пояснение в скобках при аз. термине —
    # сторожим только форму без перевода.
    # фактчекинг по CDDR ВОЗ 2026-08-11: сроки XBT-11 не равны DSM-5-TR
    'Tezlik: ən azı həftədə 1 dəfə, ≥ 3 ay.', 'XBT-11 — paralel; «atypical bulimia',
    'regurgitasiyası ≥ 1 ay',
    # аз. орфография: «distres», двойное s только в английских именах
    'Distress və ya münasibət', 'distress dözümlülüyü', 'Onkoloji distress',
    # порча от lang_tags: срез слева + остаток по длине
    'Lang Disord</span>sord',
    'gestasion', 'İnternal modelling', 'habit selection və', 'inflamasion',
    'peer setting', 'toplama-də', 'anorexia-', 'fostering', 'preskripsion',
    # орфографические решения владельца 2026-08-10 (fix_orthography.py):
    # азербайджанский пишет двойное s, apnoe и -ergik
    'DEPRESİV', 'Depresiv', 'depresiv', 'depresiya', 'Depresiya',
    'antidepresant', 'Antidepresant', 'apnesi', 'apneda', 'hipopnesi',
    'erjik', 'KEÇİRTMƏ',
    # аз. «stress» с двойным s; «cPTSP» — форма без своего языка,
    # карточка 6B41 сама озаглавлена KPTSP. Пробел в начале обязателен:
    # без него строка ловит законное «distresi», «Disstresi», «distresini».
    'cPTSP', ' stresli', ' stresor', ' stresin', ' stresə', ' stresi',
 ],
 'ru': [
    # очередь 1 §8 глава 14 — ОВР был привязан к чужому коду, 2026-08-15
    '(ОВР, МКБ-11 <span class="icd">6C91</span>)',
    # очередь 1 §8 глава 12 — NG219 и MacArthur, 2026-08-15
    'NICE CG52, NG219', 'снижает смертность и передачу ВИЧ (MacArthur',
    # очередь 1 §8 глава 11 — 6C20, 2026-08-15
    'на уровне первой помощи',
    # очередь 1 §8 глава 10 — обломки в 6C01, 2026-08-15
    'ежемесячно-годовой дозе', 'предпочтительнее клизмы (не рекомендуется',
    # очередь 1 §8 глава 09 — CBT-E, рефидинг, лиздексамфетамин, 2026-08-15
    '40 сеансов за 20 недель', 'Начальная доза 20 ккал/кг/сут', '30–70 мг ежедневно',
    # очередь 1 §8 глава 07 — обломки текста, 2026-08-15
    'проверочного поведения ухаживающего лица', '+ или пре-травматическое',
    # очередь 1 §8 глава 06 — Foa 2005, Crerand, Tolin, 2026-08-13
    'ЭРП + СИОЗС</strong> — превосходит монотерапию',
    'Plast Reconstr Surg 2010', 'Depress Anxiety 2015 РКИ',
    # очередь 1 §8 глава 05 — FDA, APA, Wolitzky-Taylor, 2026-08-13
    'эсциталопрам, пароксетин — FDA',
    'APA Clinical Practice Guideline for the Treatment of Anxiety Disorders',
    'экспозиция превосходит фармакотерапию',
    # очередь 1 §8 главы 03–04 — Cipriani 2018, FDA, Miklowitz, 2026-08-13
    'Miklowitz D.J. Am J Psychiatry 2003',
    'ребоксетин имеют наивысшую приемлемость',
    'кветиапин (одобрение FDA), луразидон',
    # очередь 1 §8 глава 02 — Leucht 2012, FDA, Health Affairs, 2026-08-13
    'в 5 раз (Leucht', 'Lancet Psychiatry 2016;3(2):158–169',
    'специально одобрены FDA для шизоаффективного расстройства',
    # очередь 1 §8 глава 01 — сверка с FDA и PubMed, 2026-08-12
    'при РАС у 5–17 лет', 'Cortese 2018 подтверждает эффективность на фоне ИР',
    'Туретта в возрасте 6–17 лет', '<td>100–400 мг/сут</td><td>FDA 2021; дети и взрослые',
    # §N «О книге» обещала несуществующую структуру, 2026-08-12
    'исторических концепций', 'Исторические концепции',
    'см. раздел 4 (сравнение CDDR',
    '<li><strong>Мониторинг</strong> — Раздел 9.</li>',
    # §M вставка вместо названия классификации и метки таблиц, 2026-08-12
    'требования for WHO', 'Разработка ВОЗ, 2019 г.',
    'вступление в силу 2022 — МКБ-11:', '(ОВР, ВОЗ, 2019, вступление',
    '</strong> Указывает на вероятность', '(КОДТ)',
    '<td lang="az">РАССТРОЙСТВА', '<td lang="en">ТРЕВОЖНЫЕ',
    '<span lang="en">Popov Yu</span>', '<span lang="en">Hyman SE</span>',
    '<span lang="en">Kessler RC</span>', '<td lang="ru">Anorexia Nervosa',
    # §H2 вводные страницы, 2026-08-12
    '<strong>Из 11 разделов</strong>', 'с <strong>Где это уместно</strong>',
    '<strong>из международных правил</strong>', 'Наиболее основные скрининговые',
    'очень распространено', 'патологического сюжета',
    'приблизительно-конкретный план', 'Для ОКР: ЭРП',
    # §H часть 2 — вводные страницы, 2026-08-12
    'кнопка «Исправить»', 'нажав кнопку',
    '103 расстройства', '103 нарушения', 'AACE, APA, NICE',
    # §H справочные страницы и навигация, 2026-08-12
    'Полное название на азербайджанском языке',
    'ПАРЦИАЛЬНОЕ ДИССОЦИАТИВНОЕ ИД',
    # §G главы 7, 8, 16, 17, 2026-08-12
    'HA40.Z', 'HA40 Sexual dysfunction associated with disorder',
    'циркадный ритм не нарушен', 'приступы в школе',
    'модификация при БДР', 'нарастание симптомов</strong> нет',
    'Не менее <strong>1 год</strong>',
    # §F 6B80, 2026-08-12
    'МКБ-11 — параллельно; «атипичная нервная анорексия»',
    # §E коды против ICD-11 MMS, 2026-08-12
    'Statistics. 8A05 Primary tics', 'ICD-11. 7A21 Hypersomnolence',
    'ICD-11. 7A60 Circadian', 'ICD-11. GA34 Premenstrual',
    'ICD-11. HA01 Erectile', 'ICD-11. HA02 Anorgasmia', 'ICD-11. HA03 Early',
    '<span class="icd">8A05</span>', '<span class="icd">GA34</span>',
    '<span class="icd">HA01</span>', '<span class="icd">HA02</span>',
    '<span class="icd">HA03</span>', '<span class="icd">7A21</span>',
    '<span class="icd">7A60</span>',
    # §11 «Источники», 2026-08-12
    'Исследования Coccaro E.F.',
    # §8 «Лечение», 2026-08-12
    'ССР, КПТ, комбинация', 'Manual Taper</span>l Taper', 'Ахэи',
    'Адаптация Y-BOCS для БДР', 'диагноза — Ston (Stone J.)',
    'реберсинг — <strong>опасный</strong>', '(при <span lang="en">ID/ASD</span>)',
    '<strong>Налоксон</strong> — ВМ/ВН', 'Сравнение КПТ + циталопрам',
    'управление непредвиденными обстоятельствами', 'Менеджмент непредвиденных обстоятельств',
    'менеджмента непредвиденных обстоятельств',
    'Терапия с использованием непредвиденных обстоятельств',
    '<th>нарушение</th>', '<th>запись</th>', '<th>Преиму</th>', '<th>Экспрессия</th>',
    'монотерапия антидепрессантами.</td>', 'дополнительный компонент.</li>',
    'Кардиальная КДТ', 'если КБИТ недоступна', '<tr><td>Clonidine</td>',
    'Sodium Oxybate</span> (Xyrem/Xywav)', 'питолизант', 'Тазимелтеон',
    'лёгкая-умеренная ОСА', 'ответа на СИПАП', 'гипогонадизме ТРТ',
    'У женщин постменопаузальный', 'тревоге по поводу производительности',
    'запланированные дневные грезы', 'Roessner V. et al. <span lang="en">Eur Child Adolesc Psychiatry</span> 2011) показали',
    'одобрены только при нарколепсии', 'ВРЕДНЫ;', 'стимуляторы СНИЖАЮТ',
    'рисперидон ПРОТИВОПОКАЗАНЫ', 'мета-анализ). <a href="https://www.nice.org.uk/guidance/cg178"',
    'Освещенный ADA', 'мой двор топят палками', 'завершил(а)', 'В.Д. Видин',
    'Затяжное Расстройство Печали', 'Затяжное расстройство траура',
    'Обсессивно-Компульсивное Расстройство', 'Электросудорожная Терапия',
    'СИОЗС Высокая Доза', 'Психологическое Обследование', 'Одиночество + гнев',
    'Источники', 'КТТД', 'гиппокампотомии', 'Kraft-Ebing',
    'Source-whitelist bodies', 'to be completed from the indexed record',
    'ПРИЛОЖЕНИЕ В', 'ПРИЛОЖЕНИЕ Б', 'сонная одурь', 'Шкала насилия',
    # §10 «Мифы»: сплошное чтение 104 карточек
    'при митозе', 'постельный режим или круглосуточное', 'воспроизводить точно',
    'гиподиагностика', 'ИР НЕТ',
    # §7–§9 «Обследование · Лечение · Прогноз»
    'ПЕРВАЯ ЛИНИЯ', 'ОБЯЗАТЕЛЬНЫ.', 'housebound',
    'Lisdexamfetamine',
    # справочные страницы: список сокращений и глоссарий
    'Атипичные (второго поколения) антипсихотики', '6B64–6B6Z',
    'HA01–HA0Z',
    # контрольная вычитка §1–§6: карточки 6C51–HA40
    'противоречат пациенту', 'лгать на собеседовании', 'индуцированное или ложное',
    'Separation test', 'UNDERDIAGNOSED', 'седация, отмена',
    'потеря идентификации', 'губы-глотание', 'походка, urinary',
    # числовая сверка и сверка абзацев 2026-08-11
    'КПТСР', '1830-х годах Пинель', 'DBT против CBT при пограничном',
    'Параллельное развитие с 6D30',
    # вычитка русского, партии 1–2
    'был оставлен международным научным', 'а также адаптивное поведение — это',
    'под кодом <strong>четыре подтипа</strong> кодируется',
    '(DLD)</strong> заменён на.', '— Редкое тяжёлое речевое',
    'в связи базальные ганглии', 'идентичности <strong>вмешивается',
    'excessive acquisition</strong> с;', 'классификация под;',
    'представляет стандартные протоколы для.', 'ДИП',
    # вычитка русского, партия 3: инверсия «оставлен» и спутанные корни
    'оставлены в современной клинической', 'впоследствии оставлен.',
    'были оставлены из-за отсутствия', 'избегание, прыжки, игры с мячом',
    'Не терять необходимые вещи', 'Побеги или лазание',
    'играть в спокойные занятия',
    # вычитка русского, партия 4: карточка 6A20
    '6A20</span> с кодом располагается', 'кодируется отдельно от него',
    '— Термин «шизофрении»', '<strong>Отменено</strong> (клиническая',
    'подход</strong> Применен', 'по сравнению с основными изменениями',
    'в течение течения', 'BMC Med 2004 meta-analiz',
    'и <strong>редкие варианты числа копий',
    'возраст начала с 7 лет.', '<strong>До 12</strong> повышено',
    # партия 5: 6A21, 6A22 — азербайджанское причастие развернули так, что
    # сказуемое осталось висеть после придаточного
    'дополнительно <strong>При котором', 'расстройством</strong> захватывает',
    'совпадение</strong> Высокая генетическая', '</strong> — Впервые ввел',
    '</strong> — Шизоаффективное расстройство как', '</strong> — Подспецификации типа',
    'эпизода</strong> является клиническим', '(психотическая категория). <span',
    '(Cluster A). <strong>и</strong>', '</strong> — Концепция «латентной',
    '</strong> — Термин «шизотип»', '</strong> — Шизотипическое расстройство',
    '</strong> — Датские исследования',
    # партия 7: 6A62, 6A70, 6A71, 6A40 и добор «ё»
    '<strong>subthreshold</strong> хроническое', 'рекуррентное, формальность',
    'Гиппократ</strong> — Термин «меланхолия», IV', 'GABA-ергической',
    'запрещен ', 'нелеченый', 'нелеченая', 'нелеченых', 'раздраженного кишечника',
    'напряженная', 'искаженными',
    # партия 16: сокращения сведены к формам мастера (FTD, AChEI, PPD, PPP)
    'ЛВД', 'бвЛВД', 'АХЭИ', 'ИАХЭ', 'ППД', 'истории ППР', 'большинство ППР', 'Миф 1: «ППР',
    'Миф 5: «ППР', 'анамнезе ППП', 'Миф 1: «ППП',
    # партия 15: аз. сокращение ДДГП в русском тексте (в книге СДВГ 562 раза)
    'ДДГП', 'лоботомия“—', 'переживания“—', '„привык“—', '„5 стадий“—', 'возврат“—',
    # партия 14: одно расстройство шестью именами; ДТЛ; согласование
    'фактитивного расстройства', 'Фактитивное расстройство', 'фактитивное расстройство',
    'Фактициозное расстройство', 'фактициозное расстройство', 'Фактитное расстройство',
    'Симулятивное расстройство', 'симулятивного расстройства', '(?)ДТЛ',
    'сексуальная возбуждение', 'Является предотвратимой причиной смертности',
    # партия 13: 6C20 — сказуемое в конце
    'дистресса</strong> устанавливается (основное',
    # партия 12: незакрытая скобка и код DSM в 6B22 (мастер даёт F42.8)
    'DSM-5-TR: F65.2 — стойкое', 'Movement Disorder</span> — нейроонтогенетическое',
    'DSM-5-TR: F42.2 (специфицированное',
    # партия 11: «идентификация» вместо «идентичность» (структура личности)
    'нарушение идентификации', 'новую идентификацию', 'Множественные идентификации',
    'Различные идентификации', '«идентификациями», «альтерами»', 'Каждая идентификация',
    'недоминантные идентификации', 'Не-доминантные идентификации',
    'Доминантная идентификация', 'доминантной идентификации',
    'к себе (идентификация, самооценка', '«DIP-NOS»',
    # партия 10: имя синдрома — Willi Kleine и Max Levin
    'Клейна-Левина', 'Клейне-Левина',
    # партия 9: сокращения сведены к латинским, как в мастере
    'ОКР, ДТД', 'при БДД', 'для БДД', 'признак БДД', 'с БДД)', 'кПТСР',
    '(РРП) тип', 'не к РРП', 'самого РАД', '«РАД —', 'что и РП,', 'от РАД, ДСЭД',
    'при ДСЭД', 'РАД и ДСЭД', 'РП, ДРСП', 'переход в РП', 'риск РП/АСРЛ',
    'гиперарузал', 'как формальность', 'Illness Anxiety Disorder</strong> (F45.22)',
    'убежденностью пациента', 'клиническим отчетам',
    'ипохондрия — спектр ОКР</strong> включён внутрь',
    'консультативно- liaison',
    # партия 8: 6A06, 6A20, 6B20–6B23
    '<p>нарушение <strong>две формы', '<p><strong>клозапин</strong>',
    'накопительство, ДТР', 'аутизм, ДТР', '(ТДР; МКБ-11', 'эффективны при ДТР',
    'ОКР и ДТР', 'ОКР, ДТР,', '<p>обсессивно-компульсивное расстройство',
    # утечки с азербайджанского и фамилии кириллицей вместо латиницы книги
    '2009 icmal', 'lupus paneli', 'ikiz meta-analiz', 'network meta-analiz',
    'Amiloid hipotezi', 'СДВГ + tik', 'Эскироль', 'Кальбаум', 'Крафт-Эбинг',
    'Акискаль', 'Ост Л.Г', 'Линдеманн Э.', 'Липовски З.', 'Ортона С.Т.',
    'Ливингстон Г.', 'Бинсвангер О.',
    # ALL-CAPS, испорченный первой версией fix_yo.py
    # партия 6: заглавная посреди фразы, 57 мест (prosecheck.py)
    'Термин «идиотия» разграничивал', 'подтипы <strong>Расстройство аутистического',
    'Связь ОТСУТСТВУЕТ', 'дислексией <strong>Не является', 'явно преобладает',
    'вмешательство</strong> Комбинация', 'недель</strong> В течение',
    'недели</strong> Количество подтверждений', 'нарушение</strong> Требует',
    'уже <strong>Не является подтипом', 'Нейролептический Злокачественный Синдром',
    'один <strong>Маниакальный эпизод', '<p>Рекуррентное депрессивное расстройство (МКБ-11: <span class="icd">6A70',
    'от рекуррентного депрессивного расстройства (6A70)',
    'один</strong> Наблюдается большой', 'Однако <strong>Синдром отмены',
    'однако <strong>Долгосрочная', 'отдельно</strong> Перенесено',
    'доза</strong> Требуется', 'и Экскориация (L98.1)',
    '(интрузивные) <strong>Избегание', 'отделяясь</strong> Перенесено',
    '(DSO)</strong> Добавляется', 'особенности»</strong> Устанавливается',
    'булимии <strong>Противопоказан', 'Ступенчатая Пищевая', 'Ступенчатое Возвращение',
    'Ступенчатая Помощь', 'Пролонгированная Экспозиция', 'Терапия Коммуникации',
    'линия</strong> Для возраста', 'одновременно <strong>Жестокое',
    'также <strong>Является категорией', 'рефрактерности <strong>Кветиапин',
    'или Биполярное расстройство I типа', 'Вторичный Психотический Синдром',
    'Вторичный Аффективный Синдром', 'Вторичный Синдром Тревоги', 'Остаточной Тревоге',
    'Обструктивное Апноэ Сна', 'Начало <strong>До 18', 'Раздела III',
    'на Тип I', 'и Тип II', 'концепция Типа I', 'сохранении Типа II',
    'с Типом I', 'на Тип I.', 'при Типе II', 'пациенты Типа II',
    '<strong>Тип 1</strong> (с катаплексией', 'и <strong>Тип 2</strong> (без',
    'Питолизант и Солриамфетол', 'Амфетамин Edeleano L. (1887) синтез',
    'Лёгкое НЕЙРОКОГНИТИВНОЕ', 'РАССТРОЙСТВА Приёма ПИЩИ',
    'Koccaro', 'Бине и Симон', 'Шнейдер (1959)', 'Кэндес Ньюмейкер',
    'Эскироль (1838)', 'Акискаль —',
 ],
 'en': [
    # очередь 1 §8 глава 14 — ОВР был привязан к чужому коду, 2026-08-15
    '(ODD, ICD-11 <span class="icd">6C91</span>)',
    # очередь 1 §8 глава 12 — NG219 и MacArthur, 2026-08-15
    'NICE CG52, NG219', 'reduces mortality and HIV transmission (MacArthur',
    # очередь 1 §8 глава 11 — 6C20, 2026-08-15
    'integrate care at the primary care level', 'once comprehensive examination',
    # очередь 1 §8 глава 10 — обломки в 6C01, 2026-08-15
    'monthly-yearly dose', 'oral superior to enema (not recommended',
    # очередь 1 §8 глава 09 — CBT-E, рефидинг, лиздексамфетамин, 2026-08-15
    '40 sessions over 20 weeks', 'Initial 20 kcal/kg/day', 'daily 30–70 mg',
    # очередь 1 §8 глава 07 — обломки текста, 2026-08-15
    '+ or pre-trauma phase 1',
    # очередь 1 §8 глава 06 — Foa 2005, Crerand, Tolin, 2026-08-13
    'ERP + SSRI</strong> — superior to monotherapy',
    'Plast Reconstr Surg 2010', 'Depress Anxiety 2015 RCT',
    # очередь 1 §8 глава 05 — FDA, APA, Wolitzky-Taylor, 2026-08-13
    'escitalopram, paroxetine — FDA',
    'APA Clinical Practice Guideline for the Treatment of Anxiety Disorders',
    'exposure superior to pharmacotherapy',
    # очередь 1 §8 главы 03–04 — Cipriani 2018, FDA, Miklowitz, 2026-08-13
    'Miklowitz D.J. Am J Psychiatry 2003',
    'reboxetine highest in acceptability',
    'quetiapine (FDA approved), lurasidone',
    # очередь 1 §8 глава 02 — Leucht 2012, FDA, Health Affairs, 2026-08-13
    'relapse risk 5-fold (Leucht', 'Lancet Psychiatry 2016;3(2):158–169',
    'specifically approved by the FDA for schizoaffective disorder',
    # очередь 1 §8 глава 01 — сверка с FDA и PubMed, 2026-08-12
    'irritability in ASD aged 5–17', 'confirms efficacy against a background of IDD',
    'Tourette syndrome, ages 6–17', '<td>100–400 mg/day</td><td>FDA 2021; children and adults',
    # §N «О книге» обещала несуществующую структуру, 2026-08-12
    'Historical concepts', 'see Section 4 (CDDR',
    '<li><strong>Monitoring</strong> — Section 9.</li>',
    # §M вставка вместо названия классификации и метки таблиц, 2026-08-12
    'implementation提议', 'The development of the WHO, 2019',
    'Guidelines for WHO, 2019', 'Disorders (CDDG).</strong> Geneva',
    '(ODD, WHO, 2019, implementation', '</strong> Indicates possibility',
    '<td lang="ru">CATATONIA', '<td lang="ru">PERSONALITY DISORDERS',
    '<td lang="ru">Anorexia Nervosa',
    # §H2 вводные страницы, 2026-08-12
    '<strong>From 11 sections</strong>', 'in appropriate context</strong> Integrated',
    'Medication names both', '<strong>In Appendix B</strong> Most used',
    'terminology systematized in', 'ERP essential for OCD',
    '<strong>Pharmacotherapy</strong> In many cases', 'definitive minimal effective dose',
    'medication</strong> It requires caution', '<strong>Somatic presentation</strong> Widespread',
    'Stigma and isolation', 'avoid pathological subject', 'approximate-definite plan',
    'Assessment structured using scales like', 'Treatment plan <strong>Should cover',
    'Individuals at school/workplace', '<strong>High emotional load</strong> It is a profession',
    # §H часть 2 — вводные страницы, 2026-08-12
    '“Edit” button', 'by pressing the button', '103 disorders',
    'AACE, APA, NICE', 'context</strong> verilir', '(CBT + ICD-10',
    # §H справочные страницы и навигация, 2026-08-12
    'Full name in Azerbaijani', 'ADHD</td><td>Opioid Use Disorder',
    'Bipolyar II Pozuntu', 'Bipolyar I Pozuntu', 'Major Depressiv Pozuntu',
    'high-functioning ASP', 'rituals in ASP', 'in RAS patients',
    'Urgent ASP diagnostic', 'Detailed ASP clinical',
    'DISSOCIATIVE IDENTIFICA',
    # §G главы 7, 8, 16, 17, 2026-08-12
    'HA40.Z', 'HA40 Sexual dysfunction associated with disorder',
    'core insomnia', '<strong>1 il</strong>', 'seizure at school',
    'modification in MDD', '(finasterid ', 'During pelvic or urologic examination',
    'Of another psychiatric disorder (MDD, panic, dysthymic)',
    'HA03.0</span> Premature ejaculation',
    # §F 6B80, 2026-08-12
    'atypical nervous anorexia',
    # §E коды против ICD-11 MMS, 2026-08-12
    'Statistics. 8A05 Primary tics', 'ICD-11. 7A21 Hypersomnolence',
    'ICD-11. 7A60 Circadian', 'ICD-11. GA34 Premenstrual',
    'ICD-11. HA01 Erectile', 'ICD-11. HA02 Anorgasmia', 'ICD-11. HA03 Early',
    '<span class="icd">8A05</span>', '<span class="icd">GA34</span>',
    '<span class="icd">HA01</span>', '<span class="icd">HA02</span>',
    '<span class="icd">HA03</span>', '<span class="icd">7A21</span>',
    '<span class="icd">7A60</span>',
    # §11 «Источники» и навигация, 2026-08-12
    'Studies by Coccaro', 'DEPRESIVE', '← µ=',
    # §8 «Лечение», 2026-08-12
    'version of ADHD', 'based on ASD at early age', 'intended in self-harm striking',
    'based on ergotherapy', 'the base for influencing core symptoms',
    'evidence in ASD is weak/specific', 'DHDD symptoms', 'predominant in adults.',
    'Initiation of titration in children;</td>', "(patient's) psychiatric treatment",
    'is MANDatory', '<th>recording</th>', '<th>Prevalence</th>', '<th>Expression</th>',
    'monotherapy.</td>', 'rapid cycling; severe.', '2–5 il', 'Inner restlessness, akathisia',
    'weak effect on EPS, tardive dyskinesia and negative symptoms',
    'contributes to negative symptoms and EPS reduction',
    'Historically, erotomania and somatic delusions were considered predominant',
    'can be a trigger for decompensation under stress', 'Typical antipsychotic 3–6 months',
    'cannabis withdrawal, alcohol dependence concurrent treatment',
    'tryramine crisis', 'Second-third order', 'Treatment Guidelines” list',
    'Genu reduction', 'CDT for depersonalization', 'Alternativ; sluggish response',
    'RCTs — CBT gold standard', 'Anticonvulsants for PNES. <strong>',
    'Stable service and fostering', 'Consistent service environment',
    'MANTRA, SSCM adult alternatives', 'the evidence-based approach.',
    'diagnostic residual nature', 'medication exists.</strong>;',
    'Treatment methodologies”', 'Hoarding Questionnaire-Revised',
    'SSRI/SNRI induced cataplexy', 'Low Mandibular Advancement Device',
    'Downward dosage', 'circadian discrepancy', 'modification in BPS',
    'Postmenopausal in women', 'Orientation masturbation training',
    'Pastore A. RI 2014', 'CBT-I is non-responsive', 'microbrain hemorrhage',
    'planned daydreaming', 'Second-order:', 'Third row:', 'tetrabenazin off-label',
    'The patient is separated from the primary caregiver',
    'Soft confrontation</strong> (“non-confrontational approach”',
    'PRECIPITATES OR WORSENS', 'are HARMFUL;', 'Prigerson (H.G. Prigerson)',
    'Foa (E.B. Foa)', 'LaFrance (W.C. LaFrance)', 'Hirshfeld',
    '(CBTp / CBTp —', 'Rapid cycling</strong> Stop antidepressant',
    'Parent training programs first-line</strong> For ages',
    'Illuminated ADA', 'in the yard with a...', 'clinical ordinate',
    'Reflects modification', 'RAGIMOFF Professional Psychology School</strong> founder',
    'loneliness + stubbornness', 'Loneliness + stubbornness', 'KTTD', 'CBTD',
    'hippocampotomy', 'Kraft-Ebing', 'Source-whitelist bodies',
    'to be completed from the indexed record', 'SAMHSA TYPE', 'Soviet Union +',
    'EXTRAORDINARY', 'Violence scale', 'Antidepressant reduces symptoms, does not',
    # §10 «Мифы»: сплошное чтение 104 карточек
    'nondisjunction in mitosis', 'Bed rest or 24/7', 'occupational safety is challenging',
    'should be reproduced exactly', 'problem than.', 'there is NO association',
    # §7–§9 «Обследование · Лечение · Прогноз»
    'FIRST LINE',
    # справочные страницы: список сокращений и глоссарий
    'Atypical (Second Generation) Antipsychotics', 'patient (not ‘patient’)',
    '6B64–6B6Z', '"kod-cell">6A70</td><td>Bipolyar I',
    # контрольная вычитка §1–§6: карточки 6C51–HA40
    '‘impossible’ or atypical', 'contradict patient', 'may lie in interview',
    'UNDERDIAGNOSED', 'loss of identification', 'lip-swallowing',
    '(gait, urinary, cognitive)', 'Impairment umbrella.',
    # фактчекинг по CDDR ВОЗ 2026-08-11
    'Frequency: at least once weekly, ≥ 3 months.',
    'behaviour</strong>(in the conceptual',
    # вычитка английского, партия 2
    'conscious function</strong> differs from.', 'Under classification;',
    'presents standard protocols for it.', 'acquisition</strong> with;',
    '(AUD structure); ICD-11 — parallel',
    'regurgitation of swallowed food ≥ 1 month',
    # числовая сверка 2026-08-11
    'relapse rates of 50–80%', '(2,8%)', '15,2 / 100', '3,9–9,6 / 100',
    # сверка абзацев 2026-08-11: отозванное утверждение уцелело в переводах
    'In the 1830s, Pinel', 'Comparison of self-help internet-based',
    # вычитка английского, партия 3
    'Avoid sitting in places that require', 'Inability to work.',
    'Answer a question that has not been completed',
    'Amphetamine synthesis by Edeleano',
    'Clinical diagnosis. <strong>not based', 'In ICD-11 classification <span',
    'Tics typically <strong>premonitory urge</strong> (preceded',
    # партия 13: определения §1 английского дерева
    'Manic episode</strong> — It is characterized', 'major depressive</strong> Characterized by episodes',
    "history <strong>only one</strong> A major depressive",
    'mental acts) characterized by the disorder', '(DSO)</strong> Added:',
    'non-dominant identifications', '<strong>Without compensatory behaviors</strong>',
    'Pathological Body Odor Disturbance (BOD)', '<p>Repeated depressive disorder',
    'DSM-5-TR — separate diagnosis.', 'characteristic domains</strong> has been modeled',
    'as categorical diagnosis <strong>has been abolished', 'hallucinations) characterized neuropsychiatric',
    '<span class="icd">HA20</span>DSM-5-TR',
    'Specific Learning Disorder — a neurodevelopmental',
    'Coordination Disorder, DCD — a neurodevelopmental',
    'Stereotypic Movement Disorder — characterized',
    'DSM-5-TR: F98.21 — characterized', 'F52.32 in men — persistent',
    'DSM-5-TR: F42.2 specified within OCD', 'Klein-Levin', 'Illness Anxiety Disorder</strong> (F45.22)', 'two forms</strong>classified',
    '<p><strong>clozapine</strong>', '<strong>qualifier</strong>s:', '<strong>Hippokrat</strong>',
    # партия 4: 6A21, 6A22
    'additionally <strong>Continuation of psychotic',
    'affective disorder</strong> On one hand', 'overlap</strong> high genetic',
    'not met.</strong> Clinical condition.',
    '(psychotic category) <span', '(Cluster A) <strong>and</strong>',
 ],
 'tr': [
    # очередь 1 §8 глава 14 — ОВР был привязан к чужому коду, 2026-08-15
    '(ODD, ICD-11 <span class="icd">6C91</span>)',
    # очередь 1 §8 глава 12 — NG219 и MacArthur, 2026-08-15
    'NICE CG52, NG219', 'mortalite ve HIV transmisyonunu anlamlı ölçüde azaltır (MacArthur',
    # очередь 1 §8 глава 10 — обломки в 6C01, 2026-08-15
    'aylık-yıllık dozda', 'oral lavmandan üstündür (önerilmez',
    # очередь 1 §8 глава 09 — CBT-E, рефидинг, лиздексамфетамин, 2026-08-15
    '40 seans 20 hafta', 'Başlangıç 20 kkal/kg/gün', 'günlük 30–70 mg',
    # очередь 1 §8 глава 07 — обломки текста, 2026-08-15
    '+ ya da travma öncesi faz 1',
    # очередь 1 §8 глава 06 — Foa 2005, Crerand, Tolin, 2026-08-13
    'ERP + SSRI</strong> — orta-ağır OKB',
    'Plast Reconstr Surg 2010', 'Depress Anxiety 2015 RKÇ',
    # очередь 1 §8 глава 05 — FDA, APA, Wolitzky-Taylor, 2026-08-13
    'essitalopram, paroksetin — FDA',
    'APA Clinical Practice Guideline for the Treatment of Anxiety Disorders',
    'maruz bırakma farmakoterapiden üstün',
    # очередь 1 §8 главы 03–04 — Cipriani 2018, FDA, Miklowitz, 2026-08-13
    'Miklowitz D.J. Am J Psychiatry 2003',
    'reboksetin uyumda (acceptability) en yüksek',
    'ketiapin (FDA onayı), lurasidon',
    # очередь 1 §8 глава 02 — Leucht 2012, FDA, Health Affairs, 2026-08-13
    '5 kat artırır (Leucht', 'Lancet Psychiatry 2016;3(2):158–169',
    'FDA tarafından şizoaffektif bozukluk için özel olarak onaylanmıştır',
    # очередь 1 §8 глава 01 — сверка с FDA и PubMed, 2026-08-12
    "FDA 5–17 yaşlı OSB'de", 'Cortese 2018 meta-analiz İD fonunda etkililiği doğruluyor',
    'Tourette sendromunda 6–17 yaş', '<td>100–400 mg/gün</td><td>FDA 2021; çocuklar ve yetişkinler',
    # §N «О книге» обещала несуществующую структуру, 2026-08-12
    'Tarihsel kavramlar', "Bölüm 4'e bakın (CDDR",
    '<li><strong>İzleme</strong> — Bölüm 9.</li>',
    # §M вставка вместо названия классификации и метки таблиц, 2026-08-12
    'Kriterleri for WHO', "WHO'nun geliştirdiği, 2019",
    'Reed GM, , Reed GM', 'yürürlüğe giriş 2022 — ICD-11:',
    '(ODD, WHO, 2019, yürürlük 2022', '</strong> Olasılığını gösterir',
    '<td lang="en">ŞİZOFRENİ SPEKTRUMU', '<td lang="ru">KATATONİ<',
    '<td lang="ru">Anorexia Nervosa',
    # §H2 вводные страницы, 2026-08-12
    'OKB için). ERP', '<strong>Farmakoterapi</strong> Çoğu durumda',
    '<strong>Somatik sunum</strong> Çok', 'patolojik örgü olmaması',
    '<strong>C-SSRS</strong> Şeklinde', "Ek B'de</strong> En sık",
    # §H часть 2 — вводные страницы, 2026-08-12
    '“Düzelt” düğmesi var', 'Düzelt düğmesine basarak',
    '103 bozukluk', 'AACE, APA, NICE',
    # §H справочные страницы и навигация, 2026-08-12
    'Azerbaycan dili tam adı',
    # §G главы 7, 8, 16, 17, 2026-08-12
    'HA40.Z', 'HA40 Sexual dysfunction associated with disorder',
    '<strong>1 il</strong>', 'okulda tutma', "MDB'de modifikasyon",
    'bozukluklarında. <strong>önerilmez',
    # §F 6B80, 2026-08-12
    'ICD-11 — paralel; “atipik anoreksiya nervoza”',
    # §E коды против ICD-11 MMS, 2026-08-12
    'Statistics. 8A05 Primary tics', 'ICD-11. 7A21 Hypersomnolence',
    'ICD-11. 7A60 Circadian', 'ICD-11. GA34 Premenstrual',
    'ICD-11. HA01 Erectile', 'ICD-11. HA02 Anorgasmia', 'ICD-11. HA03 Early',
    '<span class="icd">8A05</span>', '<span class="icd">GA34</span>',
    '<span class="icd">HA01</span>', '<span class="icd">HA02</span>',
    '<span class="icd">HA03</span>', '<span class="icd">7A21</span>',
    '<span class="icd">7A60</span>',
    'KOMPULSİF CİNSEL TOPLUM KARŞITI DAVRANIM',
    # §11 «Источники», 2026-08-12
    'Coccaro E.F. et al. çalışmaları',
    # §8 «Лечение», 2026-08-12
    'Stimulant + Davranış Bozukluğu', 'OSB temelinde erken yaşta',
    "TDA'nın klasik formunu", 'stimulant veya non-stimulant + CBT',
    'Erişkin DEHB için CBT (', 'lisdexamfetamine veya atomoksetin',
    'Vebster-Stratton', 'Nann (Nunn R.G.)', 'CBT + sitalopram karşılaştırma',
    'yasal belge.  — Akademik', 'müdahale.  — 3 aşamalı çerçeve',
    'GWAS (Demontis D. et al.  poligen', 'süre, zaman</strong>',
    'genç, ergen</strong>', 'karışma, müdahale etme', '<th>ihlal</th>',
    'Psikoz için Bilişsel-Davranışçı Terapi (Psikoz için',
    '2–5 il', '<th>Aralığa</th>', 'rişoşet psikozu', '<th>Talimat</th>',
    'ayrıca belirti yok', 'Reyn (Raine A.)', 'Miklovits', 'hızlı döngü riski; eklenmiştir.',
    'Lorazepam çağrı testi', 'BDT, KİPT', 'BDT / KİT', 'tranylcypromine',
    'Tedavi metodikaları”', 'Kluatr (Cloitre M.)', 'Kendal (Kendall P.C.)',
    'Barret (Barrett P.M.)', 'Libovits', 'MÖT (Maruz Bırakma',
    "OKB'de gözlemlenene yanıt", 'Psikolojik destek:</strong> azaltılması',
    '8.2 Anti-agonist', 'Nikotin Replasman Tedavisi.</strong>',
    'farmakoterapi + davranışsal üstün', 'Tibbi stabilizasyon',
    'lisdexamfetamine ÇİA', 'Ston (Stone J.)', 'Smayk (Smyke A.T.)',
    'Refrakter: imipramine', 'Sodium Oxybate</span> (Xyrem/Xywav)',
    "2009 ÇÇÇ", "SSRI; ATB'de", 'Scared Straight etkisiz',
    'önerilmez.</strong>;', 'HBT taraması', 'Anti-amyloid antikorlar',
    'BDT, KİT (özellikle peripartum', 'planlı gündüz rüyaları',
    '<li><strong>sıra:</strong>', '<strong>basamak:</strong> penil protez',
    'α-blokatorla ehtiyat', 'premotor his', 'premontör', '<tr><td>Clonidine</td>',
    "(BPD'de modifikasyon)", 'Mayndfulnes', 'menstrüasyon başladığında',
    'sirkadiyen farkına', 'tek başına ekstakomb', 'KPTSS', 'karmaşık DDHB',
    'Işıklı ADA', 'heyecanım tabancayla', 'farklılaşma diploması', 'KTTD',
    'strömgren', 'önlenebilir mortalite nedenidir', 'kontrol kaybı hissi). <strong>kompansatuvar',
    '(önlenen tik veya gerilim)', 'bağımlılık, kaynaklı psikotik', 'yaratması veya yalan söylemesi', 'Bozukluk (IED; ICD-11)', 'kısıtlılık (CATALISE).',
    'DSM-5-TR: F42.2 OKB spektrumu', 'Klein-Levin', 'olarak resmiyet.', 'Bozukluk” resmiyet;', 'Recurrent resmiyet.',
    'olarak resmiyet (komorbid', 'Şeklinde resmiyet', 'resmiyeti.', "DSM-III'ten resmiyet", 'iki formu</strong>ile', '<p>ihlal <strong>', '<p><strong>klozapin</strong>',
    'yönetimi</strong>neye', 'alanı</strong>nin', '<strong>Manik epizod</strong>la', 'rehberi</strong>dır', '<strong>Hippokrat</strong>', 'Kənan Rəhimov', 'internatür', 'Kaynağa özgü belirteçler', 'PTSB',
    'Toksikoloji skrining', 'kontenjan yönetimi', 'hipokampotomi',
    'Kraft-Ebing', 'Source-whitelist bodies', 'Stepwise inme',
    # §10 «Мифы»: сплошное чтение 104 карточек
    'mitozda T21', 'Yatak istirahati', 'underdiagnosed sendromdur',
    'birebir korunmalıdır', 'bilgilendirmesi', 'overdiagnosis',
    'ilişki YOKTUR',
    # §7–§9 «Обследование · Лечение · Прогноз»
    'housebound', 'self-harm',
    'Wakefulness-promoting', 'obscene',
    # справочные страницы: список сокращений и глоссарий
    'Atipik (İkinci Kuşak) Antipsikotikler', 'ARFİD',
    '6B64–6B6Z', 'hasta (not ',
    # контрольная вычитка §1–§6: карточки 6C51–HA40
    'hastanın aksini gösteriyor', 'yalan söylüyor olabilir',
    '(indüklenmiş veya yalan)', 'overanxious', 'superimposed on demans',
    'UNDERDIAGNOSED', 'identifikasyon kaybı', 'dudak-yutma',
    '(yürüyüş, üriner, kognitif)', 'akciğer X-ray', 'Abdominal X-ray',
    # второй проход: аз. «skrininq» вместо турецкого «tarama»
    'skrining',
    # орфографические решения владельца 2026-08-10: турецкий держит -erjik,
    # азербайджанское -ergik сюда попадать не должно. «depressiv» не сторожим:
    # подстрока входит в английское «depressive» из имён DSM и источников.
    'ergik', 'cPTSP', 'KOMPLEKS POSTTRAVMATİK',
    # фактчекинг по CDDR ВОЗ 2026-08-11
    'Sıklık: en az haftada 1 kez, ≥ 3 ay<', 'regürjitasyonu ≥ 1 ay',
    # вычитка турецкого, партия 1
    "Lawa's Law", 'davranış</strong>da (kavramsal', 'DİB',
    '(AUD yapısı); ICD-11 — paralel',
    # числовая сверка 2026-08-11
    '%0,5–6 (geniş aralık', '%75 hastada', 'J Clin Psychiatry 2006',
    # сверка абзацев 2026-08-11
    "1830'larda Pinel", '6D30 eksibisyonizmle paralel gelişim',
    # вычитка турецкого, партия 3: kaçma (бегство) вместо koşma (бег)
    'yerlerde kaçma veya tırmanma',
 ],
}
# Ложные срабатывания, снятые после разбора:
#   «parmaq» — входит в aparmaq («проводить»), нужна граница слова;
#   «executive control network» — устоявшееся английское имя нейросети;
#   «DEYİL» капслоком — авторский приём выделения отрицания; переведён
#   в <strong>deyil</strong>, то есть выделение сохранено, регистр приведён
#   к типографской норме.
SKIP = {}


def main() -> int:
    bad = []
    for lg, needles in GONE.items():
        d = DIRS[lg]
        for fp in sorted(d.glob('*.html')):
            m = re.search(r'<main[\s\S]*?</main>', fp.read_text(encoding='utf-8', errors='ignore'), re.I)
            if not m:
                continue
            body = m.group(0)
            for n in needles:
                if n in SKIP and fp.stem in SKIP[n]:
                    continue
                if n == 'Источники':          # законный заголовок §11
                    continue
                c = body.count(n)
                if c:
                    bad.append(f'{lg}/{fp.stem}: «{n}» ×{c}')
    if bad:
        print(f'ВЕРНУЛИСЬ дефекты: {len(bad)}')
        for b in bad:
            print('  ', b)
        return 1
    total = sum(len(v) for v in GONE.values())
    print(f'чисто: ни один из {total} исправленных дефектов не вернулся '
          f'(az {len(GONE["az"])}, ru {len(GONE["ru"])}, en {len(GONE["en"])}, tr {len(GONE["tr"])})')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
