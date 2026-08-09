# Карта состояния книги «Klinik Psixiatriya»

Карточек: **104** × 4 языка. Файл генерируется `progress_map.py` из фактического состояния, не из памяти.

## Что закрыто по всей книге

Проверяется автоматически, `python checkup.py` — одиннадцать проверок:

| Ось | Состояние |
|---|---|
| полнота четырёх языков | чисто |
| структурная параллельность | чисто |
| целостность навигации | чисто |
| три классификации в шапке | чисто |
| канон азербайджанского | чисто |
| межъязыковое загрязнение | чисто |
| известные ложные друзья | чисто |
| типографика | чисто |
| разделитель после </strong> | чисто |
| турецкое правило процента | чисто |
| наличие источников | чисто |

Шапки и структура разделов собираются из `_codes_canon.json`; обе сборки идемпотентны — повторный прогон не меняет ни байта. Это и есть доказательство, что данные и страницы совпадают.

## Сверка содержания по блокам

Сплошная сверка — это чтение всех одиннадцати разделов карточки на четырёх языках с проверкой утверждений по первоисточникам. Автоматические проверки её не заменяют: они не видят «Шкалу насилия» вместо «Шкалы тяжести» — такое находится только чтением.

| Блок | Карточек | Состояние |
|---|---|---|
| 6A | 20 | сверен полностью — 3 отчёта, 121 правка |
| 6B | 30 | сверен полностью — 4 отчёта, 418 правок |
| 6C | 19 | сверен полностью — 2 отчёта, 21 карточка |
| 6D | 16 | сверен полностью — 6D81 и 6D83 дочитаны отдельно |
| 6E | 6 | сверен полностью |
| 7A | 5 | сверен полностью |
| 8A | 1 | сверен полностью |
| GA | 1 | сверен полностью |
| HA | 6 | сверен полностью |

## Карточки

| Код | Название (az) | Правок | Языки |
|---|---|---|---|
| 6A00 | İNTELLEKTUAL İNKİŞAF POZUNTUSU | 40 | ✓✓✓✓ |
| 6A01 | İNKİŞAF NİTQ VƏ DİL POZUNTULARI | 38 | ✓✓✓✓ |
| 6A02 | AUTİZM SPEKTRİ POZUNTUSU (ASP) | 44 | ✓✓✓✓ |
| 6A03 | SPESİFİK ÖYRƏNMƏ POZUNTUSU | 38 | ✓✓✓✓ |
| 6A04 | HƏRƏKƏT KOORDİNASİYASININ İNKİŞAFI POZUNTUSU | 33 | ✓✓✓✓ |
| 6A05 | DİQQƏT DEFİSİTİ VƏ HİPERAKTİVLİK POZUNTUSU (DDHP) | 44 | ✓✓✓✓ |
| 6A06 | STEREOTİPİK HƏRƏKƏT POZUNTUSU | 39 | ✓✓✓✓ |
| 6A20 | ŞİZOFRENİYA | 50 | ✓✓✓✓ |
| 6A21 | ŞİZOAFFEKTİV POZUNTU | 39 | ✓✓✓✓ |
| 6A22 | ŞİZOTİPİK POZUNTU | 42 | ✓✓✓✓ |
| 6A23 | KƏSKİN VƏ KEÇİCİ PSİXOTİK POZUNTU | 40 | ✓✓✓✓ |
| 6A24 | SAYIQLAMA POZUNTUSU | 42 | ✓✓✓✓ |
| 6A25 | İLKİN PSİXOTİK POZUNTULARIN SİMPTOMATİK TƏZAHÜRLƏRİ | 35 | ✓✓✓✓ |
| 6A40 | BAŞQA BİR PSİXİ POZUNTU İLƏ ƏLAQƏLİ KATATONİYA | 36 | ✓✓✓✓ |
| 6A60 | BİPOLYAR POZUNTU TİP I | 42 | ✓✓✓✓ |
| 6A61 | BİPOLYAR POZUNTU TİP II | 39 | ✓✓✓✓ |
| 6A62 | SİKLOTİMİK POZUNTU | 37 | ✓✓✓✓ |
| 6A70 | TƏK EPİZODLU DEPRESİV POZUNTU | 45 | ✓✓✓✓ |
| 6A71 | TƏKRARLANAN DEPRESİV POZUNTU | 39 | ✓✓✓✓ |
| 6A72 | DİSTİMİK POZUNTU | 40 | ✓✓✓✓ |
| 6B00 | GENERALİZƏ OLUNMUŞ NARAHATLIQ POZUNTUSU (GAD) | 42 | ✓✓✓✓ |
| 6B01 | PANİK POZUNTU | 41 | ✓✓✓✓ |
| 6B02 | AQORAFOBİYA | 37 | ✓✓✓✓ |
| 6B03 | SPESİFİK FOBİYA | 41 | ✓✓✓✓ |
| 6B04 | SOSİAL NARAHATLIQ POZUNTUSU | 36 | ✓✓✓✓ |
| 6B05 | AYRILMA NARAHATLIĞI POZUNTUSU | 39 | ✓✓✓✓ |
| 6B06 | SELEKTİV MUTİZM | 35 | ✓✓✓✓ |
| 6B20 | OBSESSİV-KOMPULSİV POZUNTU (OKP) | 37 | ✓✓✓✓ |
| 6B21 | BƏDƏN DİSMORFİK POZUNTUSU (BDD) | 38 | ✓✓✓✓ |
| 6B22 | BƏDƏNİN QOXUSU POZUNTUSU | 36 | ✓✓✓✓ |
| 6B23 | HİPOXONDRİYA | 37 | ✓✓✓✓ |
| 6B24 | TOPLAMA POZUNTUSU | 40 | ✓✓✓✓ |
| 6B25 | BƏDƏNƏ YÖNƏLMİŞ TƏKRAR DAVRANIŞLAR POZUNTUSU | 40 | ✓✓✓✓ |
| 6B40 | POSTTRAVMATİK STRESS POZUNTUSU (PTSP) | 45 | ✓✓✓✓ |
| 6B41 | KOMPLEKS POSTTRAVMATİK STRESS POZUNTUSU (KPTSP) | 41 | ✓✓✓✓ |
| 6B42 | UZANMIŞ YAS POZUNTUSU | 41 | ✓✓✓✓ |
| 6B43 | ADAPTASİYA POZUNTUSU | 38 | ✓✓✓✓ |
| 6B44 | REAKTİV BAĞLANMA POZUNTUSU | 44 | ✓✓✓✓ |
| 6B45 | SOSİAL QATILMA MƏHDUDLAŞMASI POZUNTUSU | 38 | ✓✓✓✓ |
| 6B60 | DİSSOSİATİV NEVROLOJİ SİMPTOM POZUNTUSU | 42 | ✓✓✓✓ |
| 6B61 | DİSSOSİATİV AMNEZİYA | 36 | ✓✓✓✓ |
| 6B64 | DİSSOSİATİV İDENTİFİKASİYA POZUNTUSU (DİP) | 46 | ✓✓✓✓ |
| 6B65 | PARSİAL DİSSOSİATİV İDENTİFİKASİYA POZUNTUSU | 29 | ✓✓✓✓ |
| 6B66 | DEPERSONALİZASİYA-DEREALİZASİYA POZUNTUSU | 28 | ✓✓✓✓ |
| 6B80 | SİNİR ANOREKSİYASI | 41 | ✓✓✓✓ |
| 6B81 | SİNİR BULİMİYASI | 39 | ✓✓✓✓ |
| 6B82 | AŞIRI QİDALANMA POZUNTUSU | 39 | ✓✓✓✓ |
| 6B83 | QAÇINAN-MƏHDUDLAŞDIRICI QİDA QƏBULU POZUNTUSU | 40 | ✓✓✓✓ |
| 6B84 | PİKA | 41 | ✓✓✓✓ |
| 6B85 | RUMİNASİYA-REQURGİTASİYA POZUNTUSU | 40 | ✓✓✓✓ |
| 6C00 | ENUREZ | 39 | ✓✓✓✓ |
| 6C01 | ENKOPREZ | 40 | ✓✓✓✓ |
| 6C20 | BƏDƏN DİSSTRESİ POZUNTUSU | 38 | ✓✓✓✓ |
| 6C40 | ALKOQOL QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 45 | ✓✓✓✓ |
| 6C41 | KANNABİNOİDLƏRİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 42 | ✓✓✓✓ |
| 6C43 | OPİOİDLƏRİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 36 | ✓✓✓✓ |
| 6C44 | SAKİTLƏŞDİRİCİ, HİPNOTİK VƏ YA ANKSİYOLİTİKLƏRİN QƏB | 36 | ✓✓✓✓ |
| 6C45 | KOKAİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 39 | ✓✓✓✓ |
| 6C46 | AMFETAMİN, METAMFETAMİN VƏ YA MEKATİNON DA DAXİL OLM | 40 | ✓✓✓✓ |
| 6C49 | HALÜSİNOGENLƏRİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 31 | ✓✓✓✓ |
| 6C4A | NİKOTİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 28 | ✓✓✓✓ |
| 6C50 | QUMAR OYNAMA POZUNTUSU | 39 | ✓✓✓✓ |
| 6C51 | OYUN OYNAMA POZUNTUSU | 13 | ✓✓✓✓ |
| 6C70 | PYROMANİYA | 34 | ✓✓✓✓ |
| 6C71 | KLEPTOMANİYA | 37 | ✓✓✓✓ |
| 6C72 | KOMPULSİV CİNSİ DAVRANIŞ POZUNTUSU | 33 | ✓✓✓✓ |
| 6C73 | ARALIQ PARTLAYICI POZUNTU | 40 | ✓✓✓✓ |
| 6C90 | MÜXALİF-İNADKAR POZUNTU (ODD) | 44 | ✓✓✓✓ |
| 6C91 | DAVRANIŞ POZUNTUSU | 43 | ✓✓✓✓ |
| 6D10 | ŞƏXSİYYƏT POZUNTUSU | 40 | ✓✓✓✓ |
| 6D11 | QABARIQ ŞƏXSİYYƏT XÜSUSİYYƏTLƏRİ VƏ YA REAKSİYALARI | 39 | ✓✓✓✓ |
| 6D30 | EKSHİBİSİONİSTİK POZUNTU | 34 | ✓✓✓✓ |
| 6D31 | VOYEURİSTİK POZUNTU | 34 | ✓✓✓✓ |
| 6D32 | PEDOFİLİK POZUNTU | 40 | ✓✓✓✓ |
| 6D33 | MƏCBURİ CİNSİ SADİZM POZUNTUSU | 36 | ✓✓✓✓ |
| 6D34 | FROTTERİSTİK POZUNTU | 34 | ✓✓✓✓ |
| 6D50 | ÖZÜNƏ TƏTBİQ EDİLƏN SAXTA POZUNTU | 39 | ✓✓✓✓ |
| 6D51 | BAŞQASINA TƏTBİQ EDİLƏN SAXTA POZUNTU | 38 | ✓✓✓✓ |
| 6D70 | DELİRİUM | 37 | ✓✓✓✓ |
| 6D71 | YÜNGÜL NEYROKOQNİTİV POZUNTU | 36 | ✓✓✓✓ |
| 6D72 | AMNESTİK POZUNTU | 38 | ✓✓✓✓ |
| 6D80 | ALZHEİMER XƏSTƏLİYİ NƏTİCƏSİNDƏ DEMENSİYA | 35 | ✓✓✓✓ |
| 6D81 | SEREBROVASKULYAR XƏSTƏLİK NƏTİCƏSİNDƏ DEMENSİYA | 35 | ✓✓✓✓ |
| 6D82 | LEVİ CİSİMCİKLƏRİ XƏSTƏLİYİ NƏTİCƏSİNDƏ DEMENSİYA | 35 | ✓✓✓✓ |
| 6D83 | FRONTOTEMPORAL DEMENSİYA (FTD) | 34 | ✓✓✓✓ |
| 6E20 | HAMİLƏLİK, DOĞUŞ VƏ YA ZAHILIQ DÖVRÜ İLƏ ƏLAQƏLİ PSİ | 44 | ✓✓✓✓ |
| 6E21 | HAMİLƏLİK, DOĞUŞ VƏ YA ZAHILIQ DÖVRÜ İLƏ ƏLAQƏLİ PSİ | 39 | ✓✓✓✓ |
| 6E40 | BAŞQA YERDƏ TƏSNİF EDİLƏN POZUNTULARA VƏ YA XƏSTƏLİK | 36 | ✓✓✓✓ |
| 6E61 | İKİNCİLİ PSİXOTİK SİNDROM | 27 | ✓✓✓✓ |
| 6E62 | İKİNCİLİ ƏHVAL-RUHİYYƏ SİNDROMU | 40 | ✓✓✓✓ |
| 6E63 | İKİNCİLİ TƏŞVİŞ SİNDROMU | 27 | ✓✓✓✓ |
| 7A00 | XRONİKİ İNSOMNİYA | 36 | ✓✓✓✓ |
| 7A20 | NARKOLEPSİYA | 37 | ✓✓✓✓ |
| 7A21 | İDİOPATİK HİPERSOMNİYA | 26 | ✓✓✓✓ |
| 7A41 | OBSTRUKTİV YUXU APNOESİ | 25 | ✓✓✓✓ |
| 7A60 | GECİKMİŞ TİPLİ YUXU-OYANIQLIQ FAZALARIN POZUNTUSU | 29 | ✓✓✓✓ |
| 8A05 | İLKİN TİKLƏR VƏ YA TİK POZUNTULARI | 35 | ✓✓✓✓ |
| GA34 | PREMENSTRUAL DİSFORİK POZUNTU (PMDD) | 30 | ✓✓✓✓ |
| HA00 | HİPOAKTİV CİNSİ İSTƏK DİSFUNKSİYASI | 37 | ✓✓✓✓ |
| HA01 | KİŞİ EREKTİL DİSFUNKSİYASI | 40 | ✓✓✓✓ |
| HA02 | ANORQAZMİYA | 36 | ✓✓✓✓ |
| HA03 | KİŞİLƏRDƏ ERKƏN EYAKULYASİYA | 38 | ✓✓✓✓ |
| HA20 | AĞRILI PENETRASİYA CİNSƏL POZUNTUSU | 27 | ✓✓✓✓ |
| HA40 | CİNSİ DİSFUNKSİYALARDA VƏ CİNSİ AĞRI POZUNTULARINDA  | 25 | ✓✓✓✓ |

Столбец «Языки» — порядок az · ru · en · tr.
