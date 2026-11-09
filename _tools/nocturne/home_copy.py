"""Ноктюрн · тексты главной из первого концепта (Кенан 09.11: «в первом демо были хорошие слова» — короче,
без повторов, с позиции психологии клиентского сервиса). Концепт был на русском; AZ и EN — перевод.
Цифра «5–8 сессий» (энурез) из концепта не подтверждена материалами сайта — фраза без цифры."""

SPEC = {
 'az': {'title': 'Sizi eşidən iki mütəxəssis',
        'haqqimda.html': 'RAGIMOFF Psixologiya Məktəbinin təsisçisi, «Klinik Psixiatriya» sorğu kitabının müəllifi.',
        'samira.html': 'Cütlüklər, valideyn və uşaq əlaqəsi, çətin yeniyetmələr. Ailə terapiyası modullarını aparır.'},
 'ru': {'title': 'Двое, кто слышит',
        'haqqimda.html': 'Основатель Школы психологии RAGIMOFF, автор справочника «Клиническая психиатрия».',
        'samira.html': 'Пары, связь родителя с ребёнком, трудные подростки. Ведёт модули семейной терапии.'},
 'en': {'title': 'Two who listen',
        'haqqimda.html': 'Founder of the RAGIMOFF Psychology School, author of the reference book “Clinical Psychiatry”.',
        'samira.html': 'Couples, the parent–child bond, difficult teenagers. Leads the family therapy modules.'},
}
PROG_SUB = {
 'az': 'İnstitut diplomu və ya QR ilə yoxlanılan IPAS sertifikatı. Əyani, onlayn və video dərslər.',
 'ru': 'Диплом института или сертификат IPAS с QR-проверкой. Очно, онлайн и видеоуроки.',
 'en': 'An institute diploma or an IPAS certificate verified by QR code. In person, online and video lessons.',
}
SVC = {
 'az': {'title': 'Nə ilə müraciət edirlər',
        'sub': 'Depressiya, panika, fobiya — xarakter zəifliyi deyil, klinik diaqnozdur. Hər birinin həlli var.',
        'more': 'Ətraflı',
        'cards': ['Münaqişələr valideyn ailəsinin modellərindən başlayır — terapiya onları görünən edir.',
                  'Aqressiya, itaətsizlik, məktəbdən imtina — birlikdə oxumağı öyrəndiyimiz daxili siqnaldır.',
                  'Sinir sisteminin yetişməsi məsələsidir, tərbiyə deyil. Diqqətlə, mərhələ-mərhələ həll olunur.',
                  'Uyğunsuz anda real fizioloji reaksiya. KDT yalançı siqnalı söndürür.',
                  'Problem iradədə deyil. Psixoterapiya tarazlığı bərpa edir.',
                  'Çıxış və qiymətləndirilmə qorxusu xarakter xüsusiyyəti deyil. Ekspozisiya terapiyası ilə həll olunur.']},
 'ru': {'title': 'С чем приходят',
        'sub': 'Депрессия, паника, фобия — не слабость характера, а клинический диагноз. У каждого из них есть решение.',
        'more': 'Подробнее',
        'cards': ['Конфликты берут начало в паттернах родительской семьи — терапия делает их видимыми.',
                  'Агрессия, непослушание, отказ от школы — внутренний сигнал, который учатся читать вместе.',
                  'Вопрос созревания нервной системы, а не воспитания. Решается бережно и поэтапно.',
                  'Реальная физиологическая реакция в неподходящий момент. КПТ отключает ложный сигнал.',
                  'Проблема не в воле. Психотерапия восстанавливает баланс.',
                  'Страх выступлений и оценки — не черта характера. Решается экспозиционной терапией.']},
 'en': {'title': 'What brings people here',
        'sub': 'Depression, panic, phobia are not a weakness of character but a clinical diagnosis. Each has a solution.',
        'more': 'Learn more',
        'cards': ['Conflicts start in patterns from the parents’ family — therapy makes them visible.',
                  'Aggression, disobedience, refusing school — an inner signal we learn to read together.',
                  'A matter of the nervous system maturing, not of upbringing. Solved gently, step by step.',
                  'A real physiological reaction at the wrong moment. CBT switches off the false alarm.',
                  'The problem is not willpower. Psychotherapy restores the balance.',
                  'Fear of speaking and of being judged is not a character trait. Exposure therapy solves it.']},
}
SVC_PAGES = ['aile-terapiyasi.html', 'aile-terapiyasi-usaq.html', 'enurez.html', 'panik-ataklar.html', 'depressiya.html', 'sosial-fobiya.html']
