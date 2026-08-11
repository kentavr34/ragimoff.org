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
    'Işıklı ADA', 'heyecanım tabancayla', 'farklılaşma diploması', 'KTTD',
    'strömgren', 'kontrol kaybı hissi). <strong>kompansatuvar',
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
