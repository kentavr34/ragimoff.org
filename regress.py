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
