import re
import os

path = r'C:\Users\SAM\Desktop\Antigravity_Workspace\ragimoff\tehsil.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Emojis to remove or replace
emojis_to_remove = ['📄', '🧠', '⚖️', '📋', '🏛️', '📹', '🎥', '🏢', '💬', '🇦🇿', '💰', '🌍', '🎁']
for e in emojis_to_remove:
    text = text.replace(e, '')

# Update the "Bolnaya tochka"
old_intro = '<p class="fade-in">Bu proqram psixologiya sahəsində <strong>dövlət tərəfindən tanınan</strong> əlavə ixtisas diplomu almaq istəyənlər üçün hazırlanmışdır. Siz həm peşəkar bacarıq, həm də rəsmi sənəd alırsınız.</p>'
new_intro = '<p class="fade-in">Başqa sahə üzrə ali təhsiliniz var, amma psixoloq olmaq istəyirsiniz? Yenidən 4 il bakalavr oxumağa ehtiyac yoxdur. Azərbaycan qanunvericiliyi qısa və rəsmi yol təklif edir — Əlavə Peşə Təhsili (DPO). Siz 1 il ərzində həm peşəkar bacarıq, həm də rəsmi sənəd alırsınız.</p>'
text = text.replace(old_intro, new_intro)

# Update the DPO Legal structure (Cabinet Ministers NO 163)
old_highlight = '<p>Azərbaycanda psixoloji xidmət göstərməyin qanuni əsası <strong>Sənəd</strong>dir (rəsmi diplom). Ancaq pasiyentə kömək etmək üçün <strong>Sənət</strong> lazımdır (real bacarıq). Bu proqramda siz ikisini birdən alırsınız.</p>'
new_highlight = '<p><strong>Niyə məhz 1 il?</strong> Nazirlər Kabinetinin 163 nömrəli qərarına əsasən (Bənd 3.1.1), yeni peşəyə yiyələnmək üçün yenidənhazırlanma təhsili 1 tədris ili çəkir. Beləliklə, siz qısa müddətdə rəsmi ixtisas alırsınız.</p>'
text = text.replace(old_highlight, new_highlight)

# Remove "Dövlət tanınan diplom (SPb DPO)" from Pricing list
old_pf = '<li><span class="pf-dot">✦</span>Dövlət tanınan diplom (SPb DPO)</li>'
new_pf = '<li><span class="pf-dot">✦</span>Rəsmi DPO Diplomu (Klinik psixoloq)</li>'
text = text.replace(old_pf, new_pf)

# Remove "Sankt-Peterburq Əlavə Peşə Təhsili İnstitutunun Diplomu" from doc-list
old_doc1 = '<li><span class="doc-check">✦</span>Sankt-Peterburq Əlavə Peşə Təhsili İnstitutunun Diplomu — "Klinik Psixoloq" kvalifikasiyası</li>'
new_doc1 = '<li><span class="doc-check">✦</span>Rəsmi DPO Diplomu — "Klinik psixoloq" kvalifikasiyası (Rusiya Federasiyası FRDO reyestrinə daxil edilir)</li>'
text = text.replace(old_doc1, new_doc1)

# Add successful centers in Praktikum
old_praktikum_hero_p = '<p>Yaxşı psixoloq heç vaxt işsiz qalmır. Çünki həyatın ən mürəkkəb problemlərini həll edə bilən insan həmişə tələb olunur. Praktikum sizə məhz bu bacarığı verir.</p>'
new_praktikum_hero_p = '<p>Yaxşı psixoloq heç vaxt işsiz qalmır. Praktikum nəzəriyyə deyil, birbaşa müştəri cəlb etmək, müalicə aparmaq və qazanc əldə etmək üçün vasitədir. Tələbələrimiz tam hazırlıq keçdikdən sonra öz psixoloji mərkəzlərini açır və sahəvi rəhbər olurlar. Nəticə öz sözünü deyir.</p>'
text = text.replace(old_praktikum_hero_p, new_praktikum_hero_p)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("tehsil.html updated")
