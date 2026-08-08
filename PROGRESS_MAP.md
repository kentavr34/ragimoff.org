# Карта состояния книги «Klinik Psixiatriya»

Карточек: **112** × 4 языка. Файл генерируется `progress_map.py` из фактического состояния, не из памяти.

## Что закрыто по всей книге

Проверяется автоматически, `python checkup.py` — девять проверок:

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
| наличие источников | чисто |

Шапки и структура разделов собираются из `_codes_canon.json`; обе сборки идемпотентны — повторный прогон не меняет ни байта. Это и есть доказательство, что данные и страницы совпадают.

## Сверка содержания по блокам

Сплошная сверка — это чтение всех одиннадцати разделов карточки на четырёх языках с проверкой утверждений по первоисточникам. Автоматические проверки её не заменяют: они не видят «Шкалу насилия» вместо «Шкалы тяжести» — такое находится только чтением.

| Блок | Карточек | Состояние |
|---|---|---|
| 6A | 21 | сверен полностью — 3 отчёта, 121 правка |
| 6B | 30 | сверен полностью — 4 отчёта, 418 правок |
| 6C | 21 | сверен полностью — 2 отчёта, 21 карточка |
| 6D | 16 | сверен полностью — 6D81 и 6D83 дочитаны отдельно |
| 6E | 7 | сверен полностью |
| 7A | 7 | сверен полностью |
| 8A | 1 | сверен полностью |
| GA | 1 | сверен полностью |
| HA | 8 | сверен полностью |

## Карточки

| Код | Название (az) | Правок | Языки |
|---|---|---|---|
| 6A00 | İNTELLEKTUAL İNKİŞAF POZUNTUSU | 28 | ✓✓✓✓ |
| 6A01 | İNKİŞAF NİTQ VƏ DİL POZUNTULARI | 25 | ✓✓✓✓ |
| 6A02 | AUTİZM SPEKTRİ POZUNTUSU (ASP) | 30 | ✓✓✓✓ |
| 6A03 | SPESİFİK ÖYRƏNMƏ POZUNTUSU | 28 | ✓✓✓✓ |
| 6A04 | HƏRƏKƏT KOORDİNASİYASININ İNKİŞAFI POZUNTUSU | 26 | ✓✓✓✓ |
| 6A05 | DİQQƏT DEFİSİTİ VƏ HİPERAKTİVLİK POZUNTUSU (DDHP) | 31 | ✓✓✓✓ |
| 6A06 | STEREOTİPİK HƏRƏKƏT POZUNTUSU | 29 | ✓✓✓✓ |
| 6A07 | TİKLİ POZUNTULAR (TOURETTE SİNDROMU) | 10 | ✓✓✓✓ |
| 6A20 | ŞİZOFRENİYA | 34 | ✓✓✓✓ |
| 6A21 | ŞİZOAFFEKTİV POZUNTU | 31 | ✓✓✓✓ |
| 6A22 | ŞİZOTİPİK POZUNTU | 28 | ✓✓✓✓ |
| 6A23 | KƏSKİN VƏ KEÇİCİ PSİXOTİK POZUNTU | 29 | ✓✓✓✓ |
| 6A24 | SAYIQLAMA POZUNTUSU | 28 | ✓✓✓✓ |
| 6A25 | İLKİN PSİXOTİK POZUNTULARIN SİMPTOMATİK TƏZAHÜRLƏRİ | 25 | ✓✓✓✓ |
| 6A40 | BAŞQA BİR PSİXİ POZUNTU İLƏ ƏLAQƏLİ KATATONİYA | 26 | ✓✓✓✓ |
| 6A60 | BİPOLYAR POZUNTU TİP I | 29 | ✓✓✓✓ |
| 6A61 | BİPOLYAR POZUNTU TİP II | 29 | ✓✓✓✓ |
| 6A62 | SİKLOTİMİK POZUNTU | 26 | ✓✓✓✓ |
| 6A70 | TƏK EPİZODLU DEPRESİV POZUNTU | 32 | ✓✓✓✓ |
| 6A71 | TƏKRARLANAN DEPRESİV POZUNTU | 28 | ✓✓✓✓ |
| 6A72 | DİSTİMİK POZUNTU | 31 | ✓✓✓✓ |
| 6B00 | GENERALİZƏ OLUNMUŞ NARAHATLIQ POZUNTUSU (GAD) | 30 | ✓✓✓✓ |
| 6B01 | PANİK POZUNTU | 29 | ✓✓✓✓ |
| 6B02 | AQORAFOBİYA | 28 | ✓✓✓✓ |
| 6B03 | SPESİFİK FOBİYA | 28 | ✓✓✓✓ |
| 6B04 | SOSİAL NARAHATLIQ POZUNTUSU | 26 | ✓✓✓✓ |
| 6B05 | AYRILMA NARAHATLIĞI POZUNTUSU | 28 | ✓✓✓✓ |
| 6B06 | SELEKTİV MUTİZM | 27 | ✓✓✓✓ |
| 6B20 | OBSESSİV-KOMPULSİV POZUNTU (OKP) | 28 | ✓✓✓✓ |
| 6B21 | BƏDƏN DİSMORFİK POZUNTUSU (BDD) | 27 | ✓✓✓✓ |
| 6B22 | BƏDƏNİN QOXUSU POZUNTUSU | 27 | ✓✓✓✓ |
| 6B23 | HİPOXONDRİYA | 26 | ✓✓✓✓ |
| 6B24 | TOPLAMA POZUNTUSU | 28 | ✓✓✓✓ |
| 6B25 | BƏDƏNƏ YÖNƏLMİŞ TƏKRAR DAVRANIŞLAR POZUNTUSU | 29 | ✓✓✓✓ |
| 6B40 | POSTTRAVMATİK STRESS POZUNTUSU (PTSP) | 32 | ✓✓✓✓ |
| 6B41 | KOMPLEKS POSTTRAVMATİK STRESS POZUNTUSU (KPTSP) | 27 | ✓✓✓✓ |
| 6B42 | UZANMIŞ YAS POZUNTUSU | 29 | ✓✓✓✓ |
| 6B43 | ADAPTASİYA POZUNTUSU | 28 | ✓✓✓✓ |
| 6B44 | REAKTİV BAĞLANMA POZUNTUSU | 30 | ✓✓✓✓ |
| 6B45 | SOSİAL QATILMA MƏHDUDLAŞMASI POZUNTUSU | 26 | ✓✓✓✓ |
| 6B60 | DİSSOSİATİV NEVROLOJİ SİMPTOM POZUNTUSU | 29 | ✓✓✓✓ |
| 6B61 | DİSSOSİATİV AMNEZİYA | 27 | ✓✓✓✓ |
| 6B64 | DİSSOSİATİV İDENTİFİKASİYA POZUNTUSU (DİP) | 30 | ✓✓✓✓ |
| 6B65 | PARSİAL DİSSOSİATİV İDENTİFİKASİYA POZUNTUSU | 17 | ✓✓✓✓ |
| 6B66 | DEPERSONALİZASİYA-DEREALİZASİYA POZUNTUSU | 17 | ✓✓✓✓ |
| 6B80 | SİNİR ANOREKSİYASI | 27 | ✓✓✓✓ |
| 6B81 | SİNİR BULİMİYASI | 27 | ✓✓✓✓ |
| 6B82 | AŞIRI QİDALANMA POZUNTUSU | 26 | ✓✓✓✓ |
| 6B83 | QAÇINAN-MƏHDUDLAŞDIRICI QİDA QƏBULU POZUNTUSU | 28 | ✓✓✓✓ |
| 6B84 | PİKA | 28 | ✓✓✓✓ |
| 6B85 | RUMİNASİYA-REQURGİTASİYA POZUNTUSU | 29 | ✓✓✓✓ |
| 6C00 | ENUREZ | 28 | ✓✓✓✓ |
| 6C01 | ENKOPREZ | 28 | ✓✓✓✓ |
| 6C20 | BƏDƏN DİSSTRESİ POZUNTUSU | 27 | ✓✓✓✓ |
| 6C40 | ALKOQOL QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 31 | ✓✓✓✓ |
| 6C41 | KANNABİNOİDLƏRİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 32 | ✓✓✓✓ |
| 6C42 | KANNABİS İSTİFADƏSİ POZUNTULARI | 13 | ✓✓✓✓ |
| 6C43 | OPİOİDLƏRİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 28 | ✓✓✓✓ |
| 6C44 | SAKİTLƏŞDİRİCİ, HİPNOTİK VƏ YA ANKSİYOLİTİKLƏRİN QƏB | 28 | ✓✓✓✓ |
| 6C45 | KOKAİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 27 | ✓✓✓✓ |
| 6C46 | AMFETAMİN, METAMFETAMİN VƏ YA MEKATİNON DA DAXİL OLM | 29 | ✓✓✓✓ |
| 6C47 | NİKOTİN İSTİFADƏSİ POZUNTULARI | 12 | ✓✓✓✓ |
| 6C49 | HALÜSİNOGENLƏRİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 20 | ✓✓✓✓ |
| 6C4A | NİKOTİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 17 | ✓✓✓✓ |
| 6C50 | QUMAR OYNAMA POZUNTUSU | 30 | ✓✓✓✓ |
| 6C51 | OYUN OYNAMA POZUNTUSU | 3 | ✓✓✓✓ |
| 6C70 | PYROMANİYA | 26 | ✓✓✓✓ |
| 6C71 | KLEPTOMANİYA | 27 | ✓✓✓✓ |
| 6C72 | KOMPULSİV CİNSİ DAVRANIŞ POZUNTUSU | 25 | ✓✓✓✓ |
| 6C73 | ARALIQ PARTLAYICI POZUNTU | 29 | ✓✓✓✓ |
| 6C90 | MÜXALİF-İNADKAR POZUNTU (ODD) | 31 | ✓✓✓✓ |
| 6C91 | DAVRANIŞ POZUNTUSU | 30 | ✓✓✓✓ |
| 6D10 | ŞƏXSİYYƏT POZUNTUSU | 29 | ✓✓✓✓ |
| 6D11 | QABARIQ ŞƏXSİYYƏT XÜSUSİYYƏTLƏRİ VƏ YA REAKSİYALARI | 28 | ✓✓✓✓ |
| 6D30 | EKSHİBİSİONİSTİK POZUNTU | 25 | ✓✓✓✓ |
| 6D31 | VOYEURİSTİK POZUNTU | 26 | ✓✓✓✓ |
| 6D32 | PEDOFİLİK POZUNTU | 29 | ✓✓✓✓ |
| 6D33 | MƏCBURİ CİNSİ SADİZM POZUNTUSU | 26 | ✓✓✓✓ |
| 6D34 | FROTTERİSTİK POZUNTU | 25 | ✓✓✓✓ |
| 6D50 | ÖZÜNƏ TƏTBİQ EDİLƏN SAXTA POZUNTU | 27 | ✓✓✓✓ |
| 6D51 | BAŞQASINA TƏTBİQ EDİLƏN SAXTA POZUNTU | 26 | ✓✓✓✓ |
| 6D70 | DELİRİUM | 29 | ✓✓✓✓ |
| 6D71 | YÜNGÜL NEYROKOQNİTİV POZUNTU | 26 | ✓✓✓✓ |
| 6D72 | AMNESTİK POZUNTU | 28 | ✓✓✓✓ |
| 6D80 | ALZHEİMER XƏSTƏLİYİ NƏTİCƏSİNDƏ DEMENSİYA | 26 | ✓✓✓✓ |
| 6D81 | SEREBROVASKULYAR XƏSTƏLİK NƏTİCƏSİNDƏ DEMENSİYA | 25 | ✓✓✓✓ |
| 6D82 | LEVİ CİSİMCİKLƏRİ XƏSTƏLİYİ NƏTİCƏSİNDƏ DEMENSİYA | 26 | ✓✓✓✓ |
| 6D83 | FRONTOTEMPORAL DEMENSİYA (FTD) | 25 | ✓✓✓✓ |
| 6E20 | HAMİLƏLİK, DOĞUŞ VƏ YA ZAHILIQ DÖVRÜ İLƏ ƏLAQƏLİ PSİ | 31 | ✓✓✓✓ |
| 6E21 | HAMİLƏLİK, DOĞUŞ VƏ YA ZAHILIQ DÖVRÜ İLƏ ƏLAQƏLİ PSİ | 29 | ✓✓✓✓ |
| 6E40 | BAŞQA YERDƏ TƏSNİF EDİLƏN POZUNTULARA VƏ YA XƏSTƏLİK | 25 | ✓✓✓✓ |
| 6E60 | İKİNCİLİ PSİXOTİK SİNDROM | 11 | ✓✓✓✓ |
| 6E61 | İKİNCİLİ PSİXOTİK SİNDROM | 20 | ✓✓✓✓ |
| 6E62 | İKİNCİLİ ƏHVAL-RUHİYYƏ SİNDROMU | 29 | ✓✓✓✓ |
| 6E63 | İKİNCİLİ TƏŞVİŞ SİNDROMU | 16 | ✓✓✓✓ |
| 7A00 | XRONİKİ İNSOMNİYA | 27 | ✓✓✓✓ |
| 7A20 | NARKOLEPSİYA | 28 | ✓✓✓✓ |
| 7A21 | İDİOPATİK HİPERSOMNİYA | 19 | ✓✓✓✓ |
| 7A40 | SİRKADİAN RİTM YUXU-OYANMA POZUNTULARI | 12 | ✓✓✓✓ |
| 7A41 | OBSTRUKTİV YUXU APNOESİ | 17 | ✓✓✓✓ |
| 7A60 | GECİKMİŞ TİPLİ YUXU-OYANIQLIQ FAZALARIN POZUNTUSU | 21 | ✓✓✓✓ |
| 7A80 | NARKOLEPSİYA | 13 | ✓✓✓✓ |
| 8A05 | İLKİN TİKLƏR VƏ YA TİK POZUNTULARI | 21 | ✓✓✓✓ |
| GA34 | PREMENSTRUAL DİSFORİK POZUNTU (PMDD) | 18 | ✓✓✓✓ |
| HA00 | HİPOAKTİV CİNSİ İSTƏK DİSFUNKSİYASI | 26 | ✓✓✓✓ |
| HA01 | KİŞİ EREKTİL DİSFUNKSİYASI | 28 | ✓✓✓✓ |
| HA02 | ANORQAZMİYA | 27 | ✓✓✓✓ |
| HA03 | KİŞİLƏRDƏ ERKƏN EYAKULYASİYA | 29 | ✓✓✓✓ |
| HA04 | GENİTO-PELVİK AĞRI / PENETRASİYA POZUNTUSU (VAGİNİSM | 12 | ✓✓✓✓ |
| HA05 | DİGƏR XƏSTƏLİK VƏ POZUNTU İLƏ ƏLAQƏLİ CİNSİ DİSFUNKS | 13 | ✓✓✓✓ |
| HA20 | AĞRILI PENETRASİYA CİNSƏL POZUNTUSU | 17 | ✓✓✓✓ |
| HA40 | CİNSİ DİSFUNKSİYALARDA VƏ CİNSİ AĞRI POZUNTULARINDA  | 17 | ✓✓✓✓ |

Столбец «Языки» — порядок az · ru · en · tr.
