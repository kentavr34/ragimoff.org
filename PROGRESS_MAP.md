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
| 6C | 21 | сверка идёт |
| 6D | 16 | сверка идёт |
| 6E | 7 | сверка идёт |
| 7A | 7 | сверка идёт |
| 8A | 1 | сверка идёт |
| GA | 1 | сверка идёт |
| HA | 8 | сверка идёт |

## Карточки

| Код | Название (az) | Правок | Языки |
|---|---|---|---|
| 6A00 | İNTELLEKTUAL İNKİŞAF POZUNTUSU | 28 | ✓✓✓✓ |
| 6A01 | İNKİŞAF NİTQ VƏ DİL POZUNTULARI | 25 | ✓✓✓✓ |
| 6A02 | AUTİZM SPEKTRİ POZUNTUSU (ASP) | 30 | ✓✓✓✓ |
| 6A03 | SPESİFİK ÖYRƏNMƏ POZUNTUSU | 28 | ✓✓✓✓ |
| 6A04 | HƏRƏKƏT KOORDİNASİYASININ İNKİŞAFI POZUNTUSU | 26 | ✓✓✓✓ |
| 6A05 | DİQQƏT DEFİSİTİ VƏ HİPERAKTİVLİK POZUNTUSU (DDHP) | 30 | ✓✓✓✓ |
| 6A06 | STEREOTİPİK HƏRƏKƏT POZUNTUSU | 28 | ✓✓✓✓ |
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
| 6B21 | BƏDƏN DİSMORFİK POZUNTUSU (BDD) | 26 | ✓✓✓✓ |
| 6B22 | BƏDƏNİN QOXUSU POZUNTUSU | 27 | ✓✓✓✓ |
| 6B23 | HİPOXONDRİYA | 26 | ✓✓✓✓ |
| 6B24 | TOPLAMA POZUNTUSU | 28 | ✓✓✓✓ |
| 6B25 | BƏDƏNƏ YÖNƏLMİŞ TƏKRAR DAVRANIŞLAR POZUNTUSU | 28 | ✓✓✓✓ |
| 6B40 | POSTTRAVMATİK STRESS POZUNTUSU (PTSP) | 32 | ✓✓✓✓ |
| 6B41 | KOMPLEKS POSTTRAVMATİK STRESS POZUNTUSU (KPTSP) | 27 | ✓✓✓✓ |
| 6B42 | UZANMIŞ YAS POZUNTUSU | 29 | ✓✓✓✓ |
| 6B43 | ADAPTASİYA POZUNTUSU | 28 | ✓✓✓✓ |
| 6B44 | REAKTİV BAĞLANMA POZUNTUSU | 30 | ✓✓✓✓ |
| 6B45 | SOSİAL QATILMA MƏHDUDLAŞMASI POZUNTUSU | 26 | ✓✓✓✓ |
| 6B60 | DİSSOSİATİV NEVROLOJİ SİMPTOM POZUNTUSU | 29 | ✓✓✓✓ |
| 6B61 | DİSSOSİATİV AMNEZİYA | 26 | ✓✓✓✓ |
| 6B64 | DİSSOSİATİV İDENTİFİKASİYA POZUNTUSU (DİP) | 30 | ✓✓✓✓ |
| 6B65 | PARSİAL DİSSOSİATİV İDENTİFİKASİYA POZUNTUSU | 17 | ✓✓✓✓ |
| 6B66 | DEPERSONALİZASİYA-DEREALİZASİYA POZUNTUSU | 17 | ✓✓✓✓ |
| 6B80 | SİNİR ANOREKSİYASI | 27 | ✓✓✓✓ |
| 6B81 | SİNİR BULİMİYASI | 27 | ✓✓✓✓ |
| 6B82 | AŞIRI QİDALANMA POZUNTUSU | 26 | ✓✓✓✓ |
| 6B83 | QAÇINAN-MƏHDUDLAŞDIRICI QİDA QƏBULU POZUNTUSU | 28 | ✓✓✓✓ |
| 6B84 | PİKA | 28 | ✓✓✓✓ |
| 6B85 | RUMİNASİYA-REQURGİTASİYA POZUNTUSU | 29 | ✓✓✓✓ |
| 6C00 | ENUREZ | 26 | ✓✓✓✓ |
| 6C01 | ENKOPREZ | 27 | ✓✓✓✓ |
| 6C20 | BƏDƏN DİSSTRESİ POZUNTUSU | 26 | ✓✓✓✓ |
| 6C40 | ALKOQOL QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 29 | ✓✓✓✓ |
| 6C41 | KANNABİNOİDLƏRİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 30 | ✓✓✓✓ |
| 6C42 | KANNABİS İSTİFADƏSİ POZUNTULARI | 11 | ✓✓✓✓ |
| 6C43 | OPİOİDLƏRİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 27 | ✓✓✓✓ |
| 6C44 | SAKİTLƏŞDİRİCİ, HİPNOTİK VƏ YA ANKSİYOLİTİKLƏRİN QƏB | 27 | ✓✓✓✓ |
| 6C45 | KOKAİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 26 | ✓✓✓✓ |
| 6C46 | AMFETAMİN, METAMFETAMİN VƏ YA MEKATİNON DA DAXİL OLM | 28 | ✓✓✓✓ |
| 6C47 | NİKOTİN İSTİFADƏSİ POZUNTULARI | 11 | ✓✓✓✓ |
| 6C49 | HALÜSİNOGENLƏRİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 19 | ✓✓✓✓ |
| 6C4A | NİKOTİN QƏBULUNDAN QAYNAQLANAN POZUNTULAR | 16 | ✓✓✓✓ |
| 6C50 | QUMAR OYNAMA POZUNTUSU | 29 | ✓✓✓✓ |
| 6C51 | OYUN OYNAMA POZUNTUSU | 3 | ✓✓✓✓ |
| 6C70 | PYROMANİYA | 26 | ✓✓✓✓ |
| 6C71 | KLEPTOMANİYA | 26 | ✓✓✓✓ |
| 6C72 | KOMPULSİV CİNSİ DAVRANIŞ POZUNTUSU | 24 | ✓✓✓✓ |
| 6C73 | ARALIQ PARTLAYICI POZUNTU | 28 | ✓✓✓✓ |
| 6C90 | MÜXALİF-İNADKAR POZUNTU (ODD) | 30 | ✓✓✓✓ |
| 6C91 | DAVRANIŞ POZUNTUSU | 29 | ✓✓✓✓ |
| 6D10 | ŞƏXSİYYƏT POZUNTUSU | 28 | ✓✓✓✓ |
| 6D11 | QABARIQ ŞƏXSİYYƏT XÜSUSİYYƏTLƏRİ VƏ YA REAKSİYALARI | 27 | ✓✓✓✓ |
| 6D30 | EKSHİBİSİONİSTİK POZUNTU | 24 | ✓✓✓✓ |
| 6D31 | VOYEURİSTİK POZUNTU | 25 | ✓✓✓✓ |
| 6D32 | PEDOFİLİK POZUNTU | 28 | ✓✓✓✓ |
| 6D33 | MƏCBURİ CİNSİ SADİZM POZUNTUSU | 25 | ✓✓✓✓ |
| 6D34 | FROTTERİSTİK POZUNTU | 24 | ✓✓✓✓ |
| 6D50 | ÖZÜNƏ TƏTBİQ EDİLƏN SAXTA POZUNTU | 26 | ✓✓✓✓ |
| 6D51 | BAŞQASINA TƏTBİQ EDİLƏN SAXTA POZUNTU | 25 | ✓✓✓✓ |
| 6D70 | DELİRİUM | 28 | ✓✓✓✓ |
| 6D71 | YÜNGÜL NEYROKOQNİTİV POZUNTU | 25 | ✓✓✓✓ |
| 6D72 | AMNESTİK POZUNTU | 27 | ✓✓✓✓ |
| 6D80 | ALZHEİMER XƏSTƏLİYİ NƏTİCƏSİNDƏ DEMENSİYA | 25 | ✓✓✓✓ |
| 6D81 | SEREBROVASKULYAR XƏSTƏLİK NƏTİCƏSİNDƏ DEMENSİYA | 25 | ✓✓✓✓ |
| 6D82 | LEVİ CİSİMCİKLƏRİ XƏSTƏLİYİ NƏTİCƏSİNDƏ DEMENSİYA | 25 | ✓✓✓✓ |
| 6D83 | FRONTOTEMPORAL DEMENSİYA (FTD) | 24 | ✓✓✓✓ |
| 6E20 | HAMİLƏLİK, DOĞUŞ VƏ YA ZAHILIQ DÖVRÜ İLƏ ƏLAQƏLİ PSİ | 31 | ✓✓✓✓ |
| 6E21 | HAMİLƏLİK, DOĞUŞ VƏ YA ZAHILIQ DÖVRÜ İLƏ ƏLAQƏLİ PSİ | 28 | ✓✓✓✓ |
| 6E40 | BAŞQA YERDƏ TƏSNİF EDİLƏN POZUNTULARA VƏ YA XƏSTƏLİK | 25 | ✓✓✓✓ |
| 6E60 | İKİNCİLİ PSİXOTİK SİNDROM | 11 | ✓✓✓✓ |
| 6E61 | İKİNCİ DƏRƏCƏLİ PSİXOTİK SİNDROM | 19 | ✓✓✓✓ |
| 6E62 | İKİNCİ DƏRƏCƏLİ ƏHVAL-RUHİYYƏ SİNDROMU | 28 | ✓✓✓✓ |
| 6E63 | İKİNCİ DƏRƏCƏLİ TƏŞVİŞ SİNDROMU | 15 | ✓✓✓✓ |
| 7A00 | XRONİKİ İNSOMNİYA | 26 | ✓✓✓✓ |
| 7A20 | NARKOLEPSİYA | 27 | ✓✓✓✓ |
| 7A21 | İDİOPATİK HİPERSOMNİYA | 18 | ✓✓✓✓ |
| 7A40 | SİRKADİAN RİTM YUXU-OYANMA POZUNTULARI | 12 | ✓✓✓✓ |
| 7A41 | OBSTRUKTİV YUXU APNOESİ | 16 | ✓✓✓✓ |
| 7A60 | GECİKMİŞ TİPLİ YUXU-OYANIQLIQ FAZALARIN POZUNTUSU | 21 | ✓✓✓✓ |
| 7A80 | NARKOLEPSİYA | 12 | ✓✓✓✓ |
| 8A05 | İLKİN TİKLƏR VƏ YA TİK POZUNTULARI | 20 | ✓✓✓✓ |
| GA34 | PREMENSTRUAL DİSFORİK POZUNTU (PMDD) | 17 | ✓✓✓✓ |
| HA00 | HİPOAKTİV CİNSİ İSTƏK DİSFUNKSİYASI | 26 | ✓✓✓✓ |
| HA01 | KİŞİ EREKTİL DİSFUNKSİYASI | 28 | ✓✓✓✓ |
| HA02 | ANORQAZMİYA | 27 | ✓✓✓✓ |
| HA03 | KİŞİLƏRDƏ ERKƏN EYAKULYASİYA | 28 | ✓✓✓✓ |
| HA04 | GENİTO-PELVİK AĞRI / PENETRASİYA POZUNTUSU (VAGİNİSM | 12 | ✓✓✓✓ |
| HA05 | DİGƏR XƏSTƏLİK VƏ POZUNTU İLƏ ƏLAQƏLİ CİNSİ DİSFUNKS | 13 | ✓✓✓✓ |
| HA20 | AĞRILI PENETRASİYA CİNSƏL POZUNTUSU | 17 | ✓✓✓✓ |
| HA40 | CİNSİ DİSFUNKSİYALARDA VƏ CİNSİ AĞRI POZUNTULARINDA  | 17 | ✓✓✓✓ |

Столбец «Языки» — порядок az · ru · en · tr.
