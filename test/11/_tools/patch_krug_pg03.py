# -*- coding: utf-8 -*-
"""Правки по третьему кругу критика внутренних страниц (12.11.2026). Повторный запуск ничего не меняет.
 1. Энурез: третья линия названа по сути (обследование), препарат — по назначению эндокринолога; герой «без единого медикамента» больше не спорит со схемой.
 2. Главная: цифры по энурезу как у владельца (более 1 000; в 2025 году более 250, из них более 100 бесплатно).
 3. Лицензия института: по скану её выдало министерство образования Кировской области — формулировка «лицензировано Министерством образования России» заменена на проверяемую.
 4. IPAS: на печати сертификата — International Psychotherapy Association; расшифровка приведена к этому виду.
 5. Подпись сертификата по семейной терапии; опечатка lazimdir; «Амбассадор IPAS» вместо «Посол»."""
import io, os, sys, json, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
N = [0]


def sub(fn, pairs):
    s = io.open(fn, encoding="utf-8").read()
    o = s
    for a, b in pairs:
        s = s.replace(a, b)
    if s != o:
        io.open(fn, "w", encoding="utf-8", newline="\n").write(s)
        N[0] += 1
        print("изменён", fn)


# 1. энурез
sub("data/cons/enurez.ru.json", [("Комбинация: аларм-терапия + медикаменты", "Если поведенческая терапия не помогла — дополнительное обследование"),
                                 ("избыточном объёме жидкости возможно назначение десмопрессина или его аналогов", "избыточном объёме жидкости эндокринолог может назначить десмопрессин или его аналоги")])
sub("data/cons/enurez.az.json", [("Kombinasiya: Alarm terapiya + dərmanlar", "Davranış terapiyası kömək etmədikdə — əlavə müayinə"),
                                 ("endokrinoloji müayinə ilə sübut olduqdan sonra desmopressin və ya digər analoqları təyin edilə bilər", "endokrinoloji müayinə ilə sübut olduqdan sonra endokrinoloq desmopressin və ya onun analoqlarını təyin edə bilər")])
sub("data/cons/enurez.en.json", [("Combination: Alarm therapy + medication", "If behavioural therapy has not helped — further assessment"),
                                 ("desmopressin or its analogues may be prescribed", "an endocrinologist may prescribe desmopressin or its analogues")])

# 2. главная: цифры по энурезу
sub("assets/js/content.js", [
    ("'За годы практики — более 1\\u00A0000 пациентов: 250 в 2025 году, более 100 — в этом году.'", "'За 23 года — более 1\\u00A0000 детей; в 2025 году — более 250, из них более 100 бесплатно.'"),
    ("'Təcrübə illərində 1\\u00A0000-dən çox pasiyent, 2025-ci ildə 250, bu il isə 100-dən çox.'", "'23 ildə 1\\u00A0000-dən çox uşaq; 2025-ci ildə 250-dən çox, onlardan 100-dən çoxu ödənişsiz.'"),
    ("'More than 1,000 patients over the years of practice, 250 in 2025, more than 100 this year.'", "'More than 1,000 children in 23 years; over 250 in 2025, more than 100 of them free of charge.'")])

# 3–4. лицензия и IPAS в общих вопросах программ
sub("assets/js/programs.js", [
    ("— учебное заведение, лицензированное Министерством образования России.", "— учебное заведение с бессрочной государственной лицензией на образовательную деятельность."),
    ("— Rusiya Təhsil Nazirliyi tərəfindən lisenziyalanmış rəsmi təhsil müəssisəsi.", "— təhsil fəaliyyəti üzrə müddətsiz dövlət lisenziyası olan rəsmi təhsil müəssisəsi."),
    (", an official educational institution licensed by the Russian Ministry of Education.", ", an official educational institution holding a permanent state licence for educational activity."),
    ("International Psychotherapy Accreditation Society (IPAS)", "International Psychotherapy Association (IPAS)")])
for fn in glob.glob("data/*/*.json"):
    sub(fn, [("International Psychotherapy Accreditation Society", "International Psychotherapy Association"), ("lazimdir", "lazımdır"),
             ("Посол IPAS", "Амбассадор IPAS"), ("посол IPAS", "амбассадор IPAS")])
# 5. подпись сертификата (на нём: Couples Counselling in Family Therapy)
for fn in glob.glob("_agent/archive/law_page/law.*.json") + glob.glob("data/*/*.json"):
    sub(fn, [("Сертификат IPAS — Общая психология", "Сертификат IPAS — Семейная терапия"), ("IPAS Sertifikatı — Ümumi Psixologiya", "IPAS sertifikatı — Ailə terapiyası"),
             ("IPAS sertifikatı — Ümumi Psixologiya", "IPAS sertifikatı — Ailə terapiyası"), ("IPAS Certificate — General Psychology", "IPAS certificate — Family therapy"),
             ("IPAS certificate — General Psychology", "IPAS certificate — Family therapy")])
print("файлов изменено:", N[0])
