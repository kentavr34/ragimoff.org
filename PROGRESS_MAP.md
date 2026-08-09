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
| 6A00 | İNTELLEKTUAL İNKİŞAF POZUNTUSU | 39 | ✓✓✓✓ |
| 6A01 | İNKİŞAF NİTQ VƏ DİL POZUNTULARI | 37 | ✓✓✓✓ |
| 6A02 | AUTİZM SPEKTRİ POZUNTUSU (ASP) | 43 | ✓✓✓✓ |
| 6A03 | SPESİFİK ÖYRƏNMƏ POZUNTUSU | 37 | ✓✓✓✓ |
| 6A04 | HƏRƏKƏT KOORDİNASİYASININ İNKİŞAFI POZUNTUSU | 32 | ✓✓✓✓ |
| 6A05 | DİQQƏT DEFİSİTİ VƏ HİPERAKTİVLİK POZUNTUSU (DDHP) | 43 | ✓✓✓✓ |
| 6A06 | STEREOTİPİK HƏRƏKƏT POZUNTUSU | 38 | ✓✓✓✓ |
| 6A20 | ŞİZOFRENİYA | 49 | ✓✓✓✓ |
| 6A21 | ŞİZOAFFEKTİV POZUNTU | 38 | ✓✓✓✓ |
| 6A22 | ŞİZOTİPİK POZUNTU | 41 | ✓✓✓✓ |
| 6A23 | KƏSKİN VƏ KEÇİCİ PSİXOTİK POZUNTU | 39 | ✓✓✓✓ |
| 6A24 | SAYIQLAMA POZUNTUSU | 41 | ✓✓✓✓ |
| 6A25 | İLKİN PSİXOTİK POZUNTULARIN SİMPTOMATİK TƏZAHÜRLƏRİ | 34 | ✓✓✓✓ |
| 6A40 | BAŞQA BİR PSİXİ POZUNTU İLƏ ƏLAQƏLİ KATATONİYA | 35 | ✓✓✓✓ |
| 6A60 | BİPOLYAR POZUNTU TİP I | 41 | ✓✓✓✓ |
| 6A61 | BİPOLYAR POZUNTU TİP II | 38 | ✓✓✓✓ |
| 6A62 | SİKLOTİMİK POZUNTU | 36 | ✓✓✓✓ |
| 6A70 | TƏK EPİZODLU DEPRESİV POZUNTU | 44 | ✓✓✓✓ |
| 6A71 | TƏKRARLANAN DEPRESİV POZUNTU | 38 | ✓✓✓✓ |
| 6A72 | DİSTİMİK POZUNTU | 39 | ✓✓✓✓ |
| 6B00 | GENERALİZƏ OLUNMUŞ NARAHATLIQ POZUNTUSU (GAD) | 41 | ✓✓✓✓ |
| 6B01 | PANİK POZUNTU | 40 | ✓✓✓✓ |
| 6B02 | AQORAFOBİYA | 36 | ✓✓✓✓ |
| 6B03 | SPESİFİK FOBİYA | 40 | ✓✓✓✓ |
| 6B04 | SOSİAL NARAHATLIQ POZUNTUSU | 35 | ✓✓✓✓ |
| 6B05 | AYRILMA NARAHATLIĞI POZUNTUSU | 38 | ✓✓✓✓ |
| 6B06 | SELEKTİV MUTİZM | 34 | ✓✓✓✓ |
| 6B20 | OBSESSİV-KOMPULSİV POZUNTU (OKP) | 36 | ✓✓✓✓ |
| 6B21 | BƏDƏN DİSMORFİK POZUNTUSU (BDD) | 37 | ✓✓✓✓ |
| 6B22 | BƏDƏNİN QOXUSU POZUNTUSU | 35 | ✓✓✓✓ |
| 6B23 | HİPOXONDRİYA | 36 | ✓✓✓✓ |
| 6B24 | TOPLAMA POZUNTUSU | 39 | ✓✓✓✓ |
| 6B25 | BƏDƏNƏ YÖNƏLMİŞ TƏKRAR DAVRANIŞLAR POZUNTUSU | 39 | ✓✓✓✓ |
| 6B40 | POSTTRAVMATİK STRESS POZUNTUSU (PTSP) | 44 | ✓✓✓✓ |
| 6B41 | KOMPLEKS POSTTRAVMATİK STRESS POZUNTUSU (KPTSP) | 40 | ✓✓✓✓ |
| 6B42 | UZANMIŞ YAS POZUNTUSU | 40 | ✓✓✓✓ |
| 6B43 | ADAPTASİYA POZUNTUSU | 37 | ✓✓✓✓ |
| 6B44 | REAKTİV BAĞLANMA POZUNTUSU | 43 | ✓✓✓✓ |
| 6B45 | SOSİAL QATILMA MƏHDUDLAŞMASI POZUNTUSU | 37 | ✓✓✓✓ |
| 6B60 | DİSSOSİATİV NEVROLOJİ SİMPTOM POZUNTUSU | 41 | ✓✓✓✓ |
| 6B61 | DİSSOSİATİV AMNEZİYA | 35 | ✓✓✓✓ |
| 6B64 | DİSSOSİATİV İDENTİFİKASİYA POZUNTUSU (DİP) | 45 | ✓✓✓✓ |
| 6B65 | PARSİAL DİSSOSİATİV İDENTİFİKASİYA POZUNTUSU | 28 | ✓✓✓✓ |
| 6B66 | DEPERSONALİZASİYA-DEREALİZASİYA POZUNTUSU | 27 | ✓✓✓✓ |
| 6B80 | SİNİR ANOREKSİYASI | 40 | ✓✓✓✓ |
| 6B81 | SİNİR BULİMİYASI | 38 | ✓✓✓✓ |
| 6B82 | AŞIRI QİDALANMA POZUNTUSU | 38 | ✓✓✓✓ |
| 6B83 | QAÇINAN-MƏHDUDLAŞDIRICI QİDA QƏBULU POZUNTUSU | 39 | ✓✓✓✓ |
| 6B84 | PİKA | 40 | ✓✓✓✓ |
| 6B85 | RUMİNASİYA-REQURGİTASİYA POZUNTUSU | 39 | ✓✓✓✓ |
| 6C00 | ENUREZ | 38 | ✓✓✓✓ |
| 6C01 | ENKOPREZ | 39 | ✓✓✓✓ |
| 6C20 | BƏDƏN DİSSTRESİ POZUNTUSU | 37 | ✓✓✓✓ |
| 6C40 | ALKOQOL QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 44 | ✓✓✓✓ |
| 6C41 | KANNABİNOİDLƏRİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 41 | ✓✓✓✓ |
| 6C43 | OPİOİDLƏRİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 35 | ✓✓✓✓ |
| 6C44 | SAKİTLƏŞDİRİCİ, HİPNOTİK VƏ YA ANKSİYOLİTİKLƏRİN QƏB | 35 | ✓✓✓✓ |
| 6C45 | KOKAİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 38 | ✓✓✓✓ |
| 6C46 | AMFETAMİN, METAMFETAMİN VƏ YA MEKATİNON DA DAXİL OLM | 39 | ✓✓✓✓ |
| 6C49 | HALÜSİNOGENLƏRİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 30 | ✓✓✓✓ |
| 6C4A | NİKOTİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 27 | ✓✓✓✓ |
| 6C50 | QUMAR OYNAMA POZUNTUSU | 38 | ✓✓✓✓ |
| 6C51 | OYUN OYNAMA POZUNTUSU | 12 | ✓✓✓✓ |
| 6C70 | PYROMANİYA | 33 | ✓✓✓✓ |
| 6C71 | KLEPTOMANİYA | 36 | ✓✓✓✓ |
| 6C72 | KOMPULSİV CİNSİ DAVRANIŞ POZUNTUSU | 32 | ✓✓✓✓ |
| 6C73 | ARALIQ PARTLAYICI POZUNTU | 39 | ✓✓✓✓ |
| 6C90 | MÜXALİF-İNADKAR POZUNTU (ODD) | 43 | ✓✓✓✓ |
| 6C91 | DAVRANIŞ POZUNTUSU | 42 | ✓✓✓✓ |
| 6D10 | ŞƏXSİYYƏT POZUNTUSU | 39 | ✓✓✓✓ |
| 6D11 | QABARIQ ŞƏXSİYYƏT XÜSUSİYYƏTLƏRİ VƏ YA REAKSİYALARI | 38 | ✓✓✓✓ |
| 6D30 | EKSHİBİSİONİSTİK POZUNTU | 33 | ✓✓✓✓ |
| 6D31 | VOYEURİSTİK POZUNTU | 33 | ✓✓✓✓ |
| 6D32 | PEDOFİLİK POZUNTU | 39 | ✓✓✓✓ |
| 6D33 | MƏCBURİ CİNSİ SADİZM POZUNTUSU | 35 | ✓✓✓✓ |
| 6D34 | FROTTERİSTİK POZUNTU | 33 | ✓✓✓✓ |
| 6D50 | ÖZÜNƏ TƏTBİQ EDİLƏN SAXTA POZUNTU | 38 | ✓✓✓✓ |
| 6D51 | BAŞQASINA TƏTBİQ EDİLƏN SAXTA POZUNTU | 37 | ✓✓✓✓ |
| 6D70 | DELİRİUM | 36 | ✓✓✓✓ |
| 6D71 | YÜNGÜL NEYROKOQNİTİV POZUNTU | 35 | ✓✓✓✓ |
| 6D72 | AMNESTİK POZUNTU | 37 | ✓✓✓✓ |
| 6D80 | ALZHEİMER XƏSTƏLİYİ NƏTİCƏSİNDƏ DEMENSİYA | 34 | ✓✓✓✓ |
| 6D81 | SEREBROVASKULYAR XƏSTƏLİK NƏTİCƏSİNDƏ DEMENSİYA | 34 | ✓✓✓✓ |
| 6D82 | LEVİ CİSİMCİKLƏRİ XƏSTƏLİYİ NƏTİCƏSİNDƏ DEMENSİYA | 34 | ✓✓✓✓ |
| 6D83 | FRONTOTEMPORAL DEMENSİYA (FTD) | 33 | ✓✓✓✓ |
| 6E20 | HAMİLƏLİK, DOĞUŞ VƏ YA ZAHILIQ DÖVRÜ İLƏ ƏLAQƏLİ PSİ | 43 | ✓✓✓✓ |
| 6E21 | HAMİLƏLİK, DOĞUŞ VƏ YA ZAHILIQ DÖVRÜ İLƏ ƏLAQƏLİ PSİ | 38 | ✓✓✓✓ |
| 6E40 | BAŞQA YERDƏ TƏSNİF EDİLƏN POZUNTULARA VƏ YA XƏSTƏLİK | 35 | ✓✓✓✓ |
| 6E61 | İKİNCİLİ PSİXOTİK SİNDROM | 26 | ✓✓✓✓ |
| 6E62 | İKİNCİLİ ƏHVAL-RUHİYYƏ SİNDROMU | 39 | ✓✓✓✓ |
| 6E63 | İKİNCİLİ TƏŞVİŞ SİNDROMU | 26 | ✓✓✓✓ |
| 7A00 | XRONİKİ İNSOMNİYA | 35 | ✓✓✓✓ |
| 7A20 | NARKOLEPSİYA | 36 | ✓✓✓✓ |
| 7A21 | İDİOPATİK HİPERSOMNİYA | 25 | ✓✓✓✓ |
| 7A41 | OBSTRUKTİV YUXU APNOESİ | 24 | ✓✓✓✓ |
| 7A60 | GECİKMİŞ TİPLİ YUXU-OYANIQLIQ FAZALARIN POZUNTUSU | 28 | ✓✓✓✓ |
| 8A05 | İLKİN TİKLƏR VƏ YA TİK POZUNTULARI | 34 | ✓✓✓✓ |
| GA34 | PREMENSTRUAL DİSFORİK POZUNTU (PMDD) | 29 | ✓✓✓✓ |
| HA00 | HİPOAKTİV CİNSİ İSTƏK DİSFUNKSİYASI | 36 | ✓✓✓✓ |
| HA01 | KİŞİ EREKTİL DİSFUNKSİYASI | 39 | ✓✓✓✓ |
| HA02 | ANORQAZMİYA | 35 | ✓✓✓✓ |
| HA03 | KİŞİLƏRDƏ ERKƏN EYAKULYASİYA | 37 | ✓✓✓✓ |
| HA20 | AĞRILI PENETRASİYA CİNSƏL POZUNTUSU | 26 | ✓✓✓✓ |
| HA40 | CİNSİ DİSFUNKSİYALARDA VƏ CİNSİ AĞRI POZUNTULARINDA  | 24 | ✓✓✓✓ |

Столбец «Языки» — порядок az · ru · en · tr.
