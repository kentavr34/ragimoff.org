# RAGIMOFF.ORG — Dizayn Masterplanı
## Hər dəyişiklikdən ƏVVƏL bu sənədi oxu

---

## I. 2026 Professional Web Design Standartları

### 1. MOBILE-FIRST (Ən vacib qayda)
- Əvvəl mobil (320-480px) dizayn et, sonra desktop
- Touch hədəfləri minimum 44×44px olmalıdır
- Mətn mobilde minimum 16px
- Grid: mobil=1 sütun → tablet=2 sütun → desktop=3-4 sütun
- **YOXLA:** Hər dəyişiklik sonra telefonda bax

### 2. VİZUAL İYERARXİYA
- H1 > H2 > H3 — ölçü fərqi aydın olmalıdır
- CTA düymələri saytda ən görkəmli element olmalıdır
- Hər blokda 1 əsas mesaj, 1 CTA
- **QAYDA:** İstifadəçi 3 saniyədə nə etməli olduğunu anlamalıdır

### 3. TİPOQRAFİYA
- Başlıq: Playfair Display (serif) — emosional, peşəkar
- Mətn: Lato + **Noto Sans** (azərbaycan hərfləri üçün vacib)
- Font stack: `'Lato', 'Noto Sans', 'Segoe UI', Arial Unicode MS, sans-serif`
- **Azərbaycan hərfləri:** ə, ş, ç, ğ, ı, ö, ü — Noto Sans olmadan korlanır
- Minimal font ölçüləri: body=15-16px, small=13px, heading=24px+
- Sətir hündürlüyü: body=1.7-1.85, heading=1.1-1.3

### 4. RƏNGLƏRİN DÜZGÜNlüyü
- Navy: #0d1b3e (əsas)
- Accent: #c8a96e (qızılı — CTA, vurğu)
- White: #ffffff
- Light: #f4f6f9
- Gray: #6b7280
- Kontrast: ağ üzərindəki mətn minimum 4.5:1 nisbət
- **QAYDA:** Rəng paleti dəyişdirilməməlidir

### 5. ŞƏKILLƏR
- Hər şəkil üçün `aspect-ratio` dəyişməz olmalıdır
- `object-fit: cover` + `object-position: top center` — üz kəsilməsin
- Portrait foto (şəxs): aspect-ratio 2/3 və ya 3/4
- Landscape foto: aspect-ratio 16/9 və ya 4/3
- Diplom/sertifikat: hamısı **horizontal** (landscape), eyni aspect-ratio
- **Şəkil faylları:** WebP/AVIF üstündür, JPEG max 200KB
- Alt text hər şəkildə olmalıdır

### 6. LAYOUT VƏ SPACING
- Max genişlik: 1240px (section-inner)
- Section padding: 72px 32px (desktop), 48px 20px (mobil)
- Kartlar arası boşluq: 20-24px
- Elementlər arası minimum boşluq: 8px
- **QAYDA:** Yığışıq görünüş (crowded) qəbul edilmir

### 7. KOMPONENTLƏRİN TUTARLILIĞI
- Bütün kartlar eyni border-radius: 10-12px
- Bütün düymələr eyni height: min 44px
- Bütün section header-lar eyni: tag → h2 → lead paragraph
- Footer bütün səhifələrdə eyni
- Header bütün səhifələrdə eyni

### 8. ANİMASİYA VƏ İNTERAKSİYA
- Hover: 0.2-0.25s ease transition
- Scroll animasiyası: .fi sinfi ilə (artıq var)
- Lightbox: ✕ düyməsi + backdrop click + ESC + ← → klaviatura
- Modal: backdrop click ilə bağlanır

### 9. SÜRƏTLİLİK
- Şəkillər: loading="lazy" (yuxarıdakı hero: loading="eager")
- Şrift: Google Fonts preconnect (artıq var)
- CSS: inline kritik CSS, shared.css ayrı
- Hədəf: 2 saniyədən az yükləmə

### 10. SEO VƏ METAdata
- Hər səhifədə unikal `<title>` (60 simvol max)
- Hər səhifədə `<meta name="description">` (160 simvol max)
- Canonical URL
- Open Graph teqləri (sosial media üçün)

---

## II. Mövcud Saytın Audit Siyahısı

### ✅ Yaxşı olan cəhətlər:
- Rəng paleti professional (navy + gold)
- Playfair Display başlıq fontu uyğundur
- WhatsApp düyməsi var
- Lightbox navigasiya var (← →, ESC)
- shared.css/shared.js modular quruluş
- Scroll animasiyalar (.fi sinfi)

### ❌ Mövcud problemlər (prioritet sıra ilə):

**KRİTİK:**
1. **Hero foto** — photo-portal.jpg (1224×2700) hero-da çox uzun, sıxılır
   - Həll: photo-hero-suit.jpg istifadə et, max-height:280px, object-fit:cover
2. **Noto Sans yüklənmir** — index.html-də Google Fonts-da yoxdur
   - Həll: Fonts link-ə `&family=Noto+Sans:wght@300;400;700` əlavə et
3. **Hero grid 1fr 360px** — 1280px ekranda sağ sütun sıxılır
   - Həll: `grid-template-columns: 1.4fr 1fr` istifadə et
4. **Ümumi CSS/JS dublikatları** — bəzi səhifələrdə (xüsusən `index.html`) shared-lə eyni funksiyalar və stillər yenidən yazılıb
   - Risk: mobil menyu və scroll animasiyalar səhifələr arasında fərqli işləyə bilər
   - Həll: mümkün olduqca “ümumi davranış” `shared.css`/`shared.js`-də saxlanılsın, səhifələr isə yalnız unikallığı əlavə etsin
5. **Mobil menyu standartı fərqlidir** — bir çox səhifədə `.mobile-nav.open`, `index.html`-də isə `.mobile-nav.show` (inline CSS/JS ilə)
   - Risk: gələcək dəyişikliklərdə bir səhifə düzələr, digəri pozular
   - Həll: 1 standart seç (tövsiyə: `.open`) və bütün səhifələrdə eynilə saxla
6. **`shared.js` vs inline script** — `index.html`-də `toggleMenu/closeMenu/IntersectionObserver/submitBooking` kimi adlar təkrar var
   - Risk: hansı versiyanın işlədiyi səhifədən asılıdır (override olur)
   - Həll: funksiyaları ya `shared.js`-də saxla, ya da unikallara ad ver (`homeToggleMenu` və s.)

**ORTA:**
4. **Diplom şəkilləri** — bəzilər hələ portrait görünür ekranda (CSS aspect-ratio məsələsi)
   - Həll: `.dip-card img { aspect-ratio: 4/3; object-fit: cover; }`
5. **tehsil.html başlığı** — "İki yol: Sənəd və Bacarıq" 2 sətirə düşür
   - Həll: font-size azalt, white-space: nowrap əvəzinə container genişlət
6. **3.html law accordion** — klikləndikdə yuxarı aparır
   - Həll: `<a href="#" onclick="...">` → `<button onclick="...">` et
7. **Otuzyvlar** — 10-cu rəy silinib amma CSS rev-grid hələ 3-sütun deklarasiyası yoxdur

**KIÇIK:**
8. Haqqımda foto — `photo-portal-crop.jpg` 480×640 — qəbuledilebilir
9. Bəzi səhifələrdə `href="#"` — scroll-to-top edir
10. Mobil: hamburger menyu z-index 100, lightbox z-index 900 — OK

---

## III. Hər Dəyişiklik Üçün Checklist

Hər kodlama sessiyasından ƏVVƏL:
- [ ] Bu masterplanı oxu
- [ ] Həll etdiyin problemi bu siyahıdan tap
- [ ] Dəyişikliyi etmədən əvvəl faylı aç və konteksti anla (xüsusən: `shared.css`, `shared.js`, `index.html`)
- [ ] Eyni davranışın iki yerdə (shared + inline) təkrar yazılmadığını yoxla

Hər kodlama sessiyasından SONRA:
- [ ] Mobil menyu bütün səhifələrdə eyni qaydada açılıb-bağlanır?
- [ ] Scroll animasiyalar bütün səhifələrdə eyni qaydada işləyir?
- [ ] Hero foto düzgün proporsiyadadır?
- [ ] Azərbaycan hərfləri düzgün görünür? (Noto Sans aktivdir?)
- [ ] Bütün linklar işləyir?
- [ ] Mobil görünüş düzgündür? (media queries var?)
- [ ] Şəkillər loading="lazy" var?

---

## IV. Fayl Strukturu

```
ragimoff/
├── index.html          — Əsas səhifə
├── haqqimda.html       — Haqqında + diplomlar
├── tehsil.html         — Təhsil (2 tab)
├── 3.html              — Klinik Psixologiya landing
├── 5.html              — Praktikum landing
├── proqram.html        — Tam tədris proqramı (YENİ)
├── qanunlar.html       — Qanuni əsaslar
├── blog.html           — Blog
├── aile-terapiyasi.html
├── aile-terapiyasi-usaq.html
├── enurez.html
├── panik-ataklar.html
├── depressiya.html
├── sosial-fobiya.html
├── cert/index.html     — Sertifikat yoxlama (YENİ)
├── data/certs.json     — Sertifikat bazası (YENİ)
├── shared.css          — Ümumi stillər
├── shared.js           — Ümumi JS
├── images/             — Bütün şəkillər
│   ├── photo-hero-suit.jpg    — Hero üçün (480×640)
│   ├── photo-portal-crop.jpg  — Haqqımda üçün (480×640)
│   ├── diplomas/              — 13 diplom (hamısı landscape)
│   ├── cert/                  — Sertifikat nümunələri
│   └── institute/             — SPb IDPO sənədləri
└── DESIGN_MASTERPLAN.md — Bu fayl
```

---

*Son yenilənmə: 22 Mart 2026*
*Hər dəyişiklikdən əvvəl oxu. Heç vaxt unuma.*