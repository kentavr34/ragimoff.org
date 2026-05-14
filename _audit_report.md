# AUDIT REPORT — KLINIK_PSIXIATRIYA_13.docx + chapters-v2

**Дата:** 2026-05-14
**Источники проверки:**
- МКБ-11 РФ 2022 (`_supplements/ICD-11_RU_2022_reference.pdf`, 454 стр.)
- 994 grammar bible (`C:\Users\SAM\Desktop\994\grammar_bibles\az.md`)
- WHO ICD-11 stable 2024-01 (онлайн)

## 1. ИСТОЧНИК СИНЕГО ЦВЕТА (HARDCODED ROOT)

Текст не голубой в самих параграфах. Голубой приходит из:

| Источник | Значение | Где |
|---|---|---|
| `theme1.xml` accent1 | `#4F81BD` | определение темы документа |
| `styles.xml` Heading5-9 | `w:themeColor="accent1" w:val="4F81BD"` | стили, унаследованные от Office шаблона |
| `styles.xml` Hyperlink | (тоже attached, но фикс работает) | — |

**Причина:** мой код `s.font.color.rgb = RGBColor(0,0,0)` через python-docx **НЕ снимает атрибут `w:themeColor`**. Word при рендере отдаёт приоритет `themeColor` над `val`. Нужна прямая правка XML — удалить `w:themeColor` со всех heading-стилей в `styles.xml` + перекрасить `accent1` в `theme1.xml` на `000000`.

## 2. ТЕРМИНОЛОГИЯ — ПРОБЛЕМЫ

Проверены 103 disorder-h1 заголовка.

### A. Чистые англоязычные транслитерации (фиксить)

| Код | Сейчас | Должно быть | Источник нормы |
|---|---|---|---|
| HA01 | `PREMATURE EJAKULYASİYA (PE)` | `TEZBİR (ERKƏN) EJAKULYASİYA (PE)` | "Premature" — англ., azerb. = tezbir / erkən |
| 6B45 | `DİSİNHİBE SOSİAL CƏLBEDİCİLİK POZUNTUSU` | `DEZİNHİBİSİYALI SOSİAL CƏLBEDİCİLİK POZUNTUSU` | "Disinhibe" — англ. транслит, лат. = dezinhibisiya |
| 6B22 | `İY REFERANS POZUNTUSU` | `PATOLOJİ BƏDƏN QOXUSU POZUNTUSU` (с (ORS) в скобках) | "İy referans" — калька "olfactory reference"; РФ: «Патологическая озабоченность собственным запахом» |

### B. Латинизмы — оставить (per 994 grammar bible §«Заимствования»)

«Психиатрические/медицинские термины часто латинизмы: şizofreniya, bipolyar pozuntu, paranoya, hallüsinasiya, depressiya. Не пытаться "перевести" в тюркский корень — это профессиональная лексика.»

Поэтому остаются БЕЗ изменений:
- ŞİZOFRENİYA, ŞİZOAFFEKTİV, ŞİZOTİPİK
- BİPOLYAR, SİKLETİMİK, DİSTİMİK
- KATATONİYA, AQORAFOBİYA, ANORGASMİYA
- DEPERSONALİZASİYA-DEREALİZASİYA
- KLEPTOMANİYA, PYROMANİYA, PEDOFİLİK
- DELİRİUM, FRONTOTEMPORAL, DEMENSİYA
- POSTNATAL, ADAPTASİYA, NARKOLEPSİYA
- EREKTİL DİSFUNKSİYA, HİPERSOMNİYA

### C. Уже правильно (после моих fix-ов 1-4)

- ✅ 6B80 SİNİR ANOREKSİYASI
- ✅ 6B81 SİNİR BULİMİYASI
- ✅ 6A71 TƏKRARLANAN DEPRESİV POZUNTU
- ✅ 6C20 BƏDƏN DİSSTRES POZUNTUSU
- ✅ 6C91 MÜXALİF-İNADKAR POZUNTU
- ✅ Mədəniyyət (вместо Kültür)
- ✅ kultura (вместо kültür лаб.)

## 3. КОДЫ vs СОДЕРЖАНИЕ — потенциальные сдвиги

PDF МКБ-11 РФ показал расхождения. Возможные проблемы (требуют проверки против WHO Browser):

| Код | У нас | РФ ICD-11 | WHO ICD-11 (2024) |
|---|---|---|---|
| 6A73 | PREMENSTRUAL DİSFORİK | Mixed depressive+anxiety | **PMDD = GA34.41**, 6A73 = Mixed dep-anx → ОШИБКА КОДА |
| 6B41 | POSTTRAVMATİK STRES | Reactive Attachment | **6B41 = RAD**, PTSD = 6B43 → ОШИБКА |
| 6B43 | UZANMIŞ YAS | PTSD | **6B43 = PTSD**, Prolonged grief = 6B45 → ОШИБКА |
| 6B44 | REAKTİV BAĞLANMA | Complex PTSD | **6B44 = cPTSD**, RAD = 6B41 → ОШИБКА |
| 6B45 | DİSİNHİBE SOSİAL | Prolonged grief | **6B45 = Prolonged grief**, Disinhibited = 6B42 → ОШИБКА |

**⚠ВНИМАНИЕ:** содержимое глав 6B41-6B45 написано правильно по темам (PTSD имеет содержание PTSD), но **ICD-коды у этих расстройств перепутаны**. Требуется переименовать файлы `_supplements/chapters-v2/` и переинжектировать главы.

## 4. РЕКОМЕНДАЦИИ — В ОДНОМ БАТЧЕ

### Минимум (срочно):
1. **Починить синий цвет:** прямая правка `styles.xml` + `theme1.xml` в `build_book.py` (не через python-docx)
2. **HA01:** PREMATURE → TEZBİR (ERKƏN)
3. **6B45 (текущее «disinhibe»):** → DEZİNHİBİSİYALI
4. **6B22 İY REFERANS:** → PATOLOJİ BƏDƏN QOXUSU POZUNTUSU

### Содержимое (требует подтверждения):
5. **Свопы кодов 6B41-6B45** — переименовать файлы и проверить содержимое:
   - 6B41 должен быть Reactive Attachment Disorder (сейчас у нас 6B44)
   - 6B42 должен быть Disinhibited Social Engagement (сейчас у нас 6B45)
   - 6B43 должен быть PTSD (сейчас у нас 6B41)
   - 6B44 должен быть Complex PTSD (сейчас у нас 6B42)
   - 6B45 должен быть Prolonged Grief (сейчас у нас 6B43)
6. **6A73:** должен быть Mixed depressive-anxiety disorder (PMDD выкинуть, она в GA34.41)

## 5. ПОСЛЕ ВСЕХ ФИКСОВ — одна сборка

`KLINIK_PSIXIATRIYA_14.docx` будет финальной версией после применения пп. 1-4 + (опционально) пп. 5-6.
