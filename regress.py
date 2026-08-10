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
 ],
 'tr': [
    'Işıklı ADA', 'heyecanım tabancayla', 'farklılaşma diploması', 'KTTD',
    'Kənan Rəhimov', 'internatür', 'Kaynağa özgü belirteçler', 'PTSB',
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
