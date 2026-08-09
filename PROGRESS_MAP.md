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
| 6A00 | İNTELLEKTUAL İNKİŞAF POZUNTUSU | 36 | ✓✓✓✓ |
| 6A01 | İNKİŞAF NİTQ VƏ DİL POZUNTULARI | 32 | ✓✓✓✓ |
| 6A02 | AUTİZM SPEKTRİ POZUNTUSU (ASP) | 40 | ✓✓✓✓ |
| 6A03 | SPESİFİK ÖYRƏNMƏ POZUNTUSU | 35 | ✓✓✓✓ |
| 6A04 | HƏRƏKƏT KOORDİNASİYASININ İNKİŞAFI POZUNTUSU | 31 | ✓✓✓✓ |
| 6A05 | DİQQƏT DEFİSİTİ VƏ HİPERAKTİVLİK POZUNTUSU (DDHP) | 39 | ✓✓✓✓ |
| 6A06 | STEREOTİPİK HƏRƏKƏT POZUNTUSU | 36 | ✓✓✓✓ |
| 6A20 | ŞİZOFRENİYA | 43 | ✓✓✓✓ |
| 6A21 | ŞİZOAFFEKTİV POZUNTU | 36 | ✓✓✓✓ |
| 6A22 | ŞİZOTİPİK POZUNTU | 37 | ✓✓✓✓ |
| 6A23 | KƏSKİN VƏ KEÇİCİ PSİXOTİK POZUNTU | 36 | ✓✓✓✓ |
| 6A24 | SAYIQLAMA POZUNTUSU | 37 | ✓✓✓✓ |
| 6A25 | İLKİN PSİXOTİK POZUNTULARIN SİMPTOMATİK TƏZAHÜRLƏRİ | 33 | ✓✓✓✓ |
| 6A40 | BAŞQA BİR PSİXİ POZUNTU İLƏ ƏLAQƏLİ KATATONİYA | 33 | ✓✓✓✓ |
| 6A60 | BİPOLYAR POZUNTU TİP I | 39 | ✓✓✓✓ |
| 6A61 | BİPOLYAR POZUNTU TİP II | 36 | ✓✓✓✓ |
| 6A62 | SİKLOTİMİK POZUNTU | 33 | ✓✓✓✓ |
| 6A70 | TƏK EPİZODLU DEPRESİV POZUNTU | 41 | ✓✓✓✓ |
| 6A71 | TƏKRARLANAN DEPRESİV POZUNTU | 35 | ✓✓✓✓ |
| 6A72 | DİSTİMİK POZUNTU | 37 | ✓✓✓✓ |
| 6B00 | GENERALİZƏ OLUNMUŞ NARAHATLIQ POZUNTUSU (GAD) | 38 | ✓✓✓✓ |
| 6B01 | PANİK POZUNTU | 37 | ✓✓✓✓ |
| 6B02 | AQORAFOBİYA | 34 | ✓✓✓✓ |
| 6B03 | SPESİFİK FOBİYA | 37 | ✓✓✓✓ |
| 6B04 | SOSİAL NARAHATLIQ POZUNTUSU | 33 | ✓✓✓✓ |
| 6B05 | AYRILMA NARAHATLIĞI POZUNTUSU | 36 | ✓✓✓✓ |
| 6B06 | SELEKTİV MUTİZM | 33 | ✓✓✓✓ |
| 6B20 | OBSESSİV-KOMPULSİV POZUNTU (OKP) | 34 | ✓✓✓✓ |
| 6B21 | BƏDƏN DİSMORFİK POZUNTUSU (BDD) | 34 | ✓✓✓✓ |
| 6B22 | BƏDƏNİN QOXUSU POZUNTUSU | 35 | ✓✓✓✓ |
| 6B23 | HİPOXONDRİYA | 33 | ✓✓✓✓ |
| 6B24 | TOPLAMA POZUNTUSU | 37 | ✓✓✓✓ |
| 6B25 | BƏDƏNƏ YÖNƏLMİŞ TƏKRAR DAVRANIŞLAR POZUNTUSU | 37 | ✓✓✓✓ |
| 6B40 | POSTTRAVMATİK STRESS POZUNTUSU (PTSP) | 42 | ✓✓✓✓ |
| 6B41 | KOMPLEKS POSTTRAVMATİK STRESS POZUNTUSU (KPTSP) | 37 | ✓✓✓✓ |
| 6B42 | UZANMIŞ YAS POZUNTUSU | 37 | ✓✓✓✓ |
| 6B43 | ADAPTASİYA POZUNTUSU | 36 | ✓✓✓✓ |
| 6B44 | REAKTİV BAĞLANMA POZUNTUSU | 41 | ✓✓✓✓ |
| 6B45 | SOSİAL QATILMA MƏHDUDLAŞMASI POZUNTUSU | 35 | ✓✓✓✓ |
| 6B60 | DİSSOSİATİV NEVROLOJİ SİMPTOM POZUNTUSU | 38 | ✓✓✓✓ |
| 6B61 | DİSSOSİATİV AMNEZİYA | 33 | ✓✓✓✓ |
| 6B64 | DİSSOSİATİV İDENTİFİKASİYA POZUNTUSU (DİP) | 40 | ✓✓✓✓ |
| 6B65 | PARSİAL DİSSOSİATİV İDENTİFİKASİYA POZUNTUSU | 25 | ✓✓✓✓ |
| 6B66 | DEPERSONALİZASİYA-DEREALİZASİYA POZUNTUSU | 24 | ✓✓✓✓ |
| 6B80 | SİNİR ANOREKSİYASI | 37 | ✓✓✓✓ |
| 6B81 | SİNİR BULİMİYASI | 35 | ✓✓✓✓ |
| 6B82 | AŞIRI QİDALANMA POZUNTUSU | 33 | ✓✓✓✓ |
| 6B83 | QAÇINAN-MƏHDUDLAŞDIRICI QİDA QƏBULU POZUNTUSU | 35 | ✓✓✓✓ |
| 6B84 | PİKA | 35 | ✓✓✓✓ |
| 6B85 | RUMİNASİYA-REQURGİTASİYA POZUNTUSU | 35 | ✓✓✓✓ |
| 6C00 | ENUREZ | 35 | ✓✓✓✓ |
| 6C01 | ENKOPREZ | 36 | ✓✓✓✓ |
| 6C20 | BƏDƏN DİSSTRESİ POZUNTUSU | 35 | ✓✓✓✓ |
| 6C40 | ALKOQOL QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 42 | ✓✓✓✓ |
| 6C41 | KANNABİNOİDLƏRİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 39 | ✓✓✓✓ |
| 6C43 | OPİOİDLƏRİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 34 | ✓✓✓✓ |
| 6C44 | SAKİTLƏŞDİRİCİ, HİPNOTİK VƏ YA ANKSİYOLİTİKLƏRİN QƏB | 35 | ✓✓✓✓ |
| 6C45 | KOKAİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 35 | ✓✓✓✓ |
| 6C46 | AMFETAMİN, METAMFETAMİN VƏ YA MEKATİNON DA DAXİL OLM | 36 | ✓✓✓✓ |
| 6C49 | HALÜSİNOGENLƏRİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 28 | ✓✓✓✓ |
| 6C4A | NİKOTİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 24 | ✓✓✓✓ |
| 6C50 | QUMAR OYNAMA POZUNTUSU | 36 | ✓✓✓✓ |
| 6C51 | OYUN OYNAMA POZUNTUSU | 11 | ✓✓✓✓ |
| 6C70 | PYROMANİYA | 32 | ✓✓✓✓ |
| 6C71 | KLEPTOMANİYA | 34 | ✓✓✓✓ |
| 6C72 | KOMPULSİV CİNSİ DAVRANIŞ POZUNTUSU | 30 | ✓✓✓✓ |
| 6C73 | ARALIQ PARTLAYICI POZUNTU | 36 | ✓✓✓✓ |
| 6C90 | MÜXALİF-İNADKAR POZUNTU (ODD) | 41 | ✓✓✓✓ |
| 6C91 | DAVRANIŞ POZUNTUSU | 40 | ✓✓✓✓ |
| 6D10 | ŞƏXSİYYƏT POZUNTUSU | 38 | ✓✓✓✓ |
| 6D11 | QABARIQ ŞƏXSİYYƏT XÜSUSİYYƏTLƏRİ VƏ YA REAKSİYALARI | 36 | ✓✓✓✓ |
| 6D30 | EKSHİBİSİONİSTİK POZUNTU | 32 | ✓✓✓✓ |
| 6D31 | VOYEURİSTİK POZUNTU | 33 | ✓✓✓✓ |
| 6D32 | PEDOFİLİK POZUNTU | 36 | ✓✓✓✓ |
| 6D33 | MƏCBURİ CİNSİ SADİZM POZUNTUSU | 33 | ✓✓✓✓ |
| 6D34 | FROTTERİSTİK POZUNTU | 33 | ✓✓✓✓ |
| 6D50 | ÖZÜNƏ TƏTBİQ EDİLƏN SAXTA POZUNTU | 35 | ✓✓✓✓ |
| 6D51 | BAŞQASINA TƏTBİQ EDİLƏN SAXTA POZUNTU | 34 | ✓✓✓✓ |
| 6D70 | DELİRİUM | 34 | ✓✓✓✓ |
| 6D71 | YÜNGÜL NEYROKOQNİTİV POZUNTU | 33 | ✓✓✓✓ |
| 6D72 | AMNESTİK POZUNTU | 34 | ✓✓✓✓ |
| 6D80 | ALZHEİMER XƏSTƏLİYİ NƏTİCƏSİNDƏ DEMENSİYA | 31 | ✓✓✓✓ |
| 6D81 | SEREBROVASKULYAR XƏSTƏLİK NƏTİCƏSİNDƏ DEMENSİYA | 31 | ✓✓✓✓ |
| 6D82 | LEVİ CİSİMCİKLƏRİ XƏSTƏLİYİ NƏTİCƏSİNDƏ DEMENSİYA | 32 | ✓✓✓✓ |
| 6D83 | FRONTOTEMPORAL DEMENSİYA (FTD) | 31 | ✓✓✓✓ |
| 6E20 | HAMİLƏLİK, DOĞUŞ VƏ YA ZAHILIQ DÖVRÜ İLƏ ƏLAQƏLİ PSİ | 38 | ✓✓✓✓ |
| 6E21 | HAMİLƏLİK, DOĞUŞ VƏ YA ZAHILIQ DÖVRÜ İLƏ ƏLAQƏLİ PSİ | 34 | ✓✓✓✓ |
| 6E40 | BAŞQA YERDƏ TƏSNİF EDİLƏN POZUNTULARA VƏ YA XƏSTƏLİK | 31 | ✓✓✓✓ |
| 6E61 | İKİNCİLİ PSİXOTİK SİNDROM | 25 | ✓✓✓✓ |
| 6E62 | İKİNCİLİ ƏHVAL-RUHİYYƏ SİNDROMU | 35 | ✓✓✓✓ |
| 6E63 | İKİNCİLİ TƏŞVİŞ SİNDROMU | 23 | ✓✓✓✓ |
| 7A00 | XRONİKİ İNSOMNİYA | 32 | ✓✓✓✓ |
| 7A20 | NARKOLEPSİYA | 33 | ✓✓✓✓ |
| 7A21 | İDİOPATİK HİPERSOMNİYA | 23 | ✓✓✓✓ |
| 7A41 | OBSTRUKTİV YUXU APNOESİ | 22 | ✓✓✓✓ |
| 7A60 | GECİKMİŞ TİPLİ YUXU-OYANIQLIQ FAZALARIN POZUNTUSU | 27 | ✓✓✓✓ |
| 8A05 | İLKİN TİKLƏR VƏ YA TİK POZUNTULARI | 30 | ✓✓✓✓ |
| GA34 | PREMENSTRUAL DİSFORİK POZUNTU (PMDD) | 26 | ✓✓✓✓ |
| HA00 | HİPOAKTİV CİNSİ İSTƏK DİSFUNKSİYASI | 33 | ✓✓✓✓ |
| HA01 | KİŞİ EREKTİL DİSFUNKSİYASI | 34 | ✓✓✓✓ |
| HA02 | ANORQAZMİYA | 33 | ✓✓✓✓ |
| HA03 | KİŞİLƏRDƏ ERKƏN EYAKULYASİYA | 35 | ✓✓✓✓ |
| HA20 | AĞRILI PENETRASİYA CİNSƏL POZUNTUSU | 23 | ✓✓✓✓ |
| HA40 | CİNSİ DİSFUNKSİYALARDA VƏ CİNSİ AĞRI POZUNTULARINDA  | 22 | ✓✓✓✓ |

Столбец «Языки» — порядок az · ru · en · tr.
