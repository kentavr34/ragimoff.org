#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_klinik_melumat_fill.py — наполнение melumat.html (4 языка) как «главной
страницы дополнительных данных» книги «Klinik Psixiatriya».

Страница была пустой (<div class="bk-read"> без содержимого) и с чужим
подзаголовком от страницы главы. Скрипт:
  * меняет подзаголовок на честный (раздел дополнительных данных);
  * вписывает три блока ссылок-строк по каркасу книги (h2 + ul/li):
      1) свои четыре подстраницы раздела (словарь, приложения A–E, шкалы,
         итоговые рекомендации),
      2) онлайн-тесты, которые реально есть на сайте,
      3) дополнительные материалы сайта.
Ссылки только на существующие страницы; ничего не выдумывается.
Запуск: python _tools/_klinik_melumat_fill.py [--apply]
"""
from __future__ import annotations
import sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent / "klinik-psixiatriya"
APPLY = "--apply" in sys.argv

SUB_OLD = {
    "": "Bu fəsildəki pozuntular — hər biri ayrıca səhifə:",
    "ru": "Расстройства этой главы — каждое на отдельной странице:",
    "en": "Disorders in this chapter — each on a separate page:",
    "tr": "Bu bölümdeki bozukluklar — her biri ayrı sayfa:",
}
SUB_NEW = {
    "": "Bölmənin səhifələri və saytdakı əlavə materiallar — bir yerdə:",
    "ru": "Страницы раздела и дополнительные материалы сайта — в одном месте:",
    "en": "Section pages and further materials on the site — in one place:",
    "tr": "Bölümün sayfaları ve sitedeki ek materyaller — bir arada:",
}
BLOCKS = {
    "": """<h2 id="bolmenin-sehifeleri">Bölmənin səhifələri</h2>
<ul>
<li><a href="abbreviatur.html">Terminoloji lüğət</a> — abbreviaturalar və klinik terminlər, üç dildə qarşılıqları ilə.</li>
<li><a href="elave-acde.html">Əlavələr A–E</a> — monitorinq və müayinə standartları, praktik protokollar.</li>
<li><a href="elave-skalalar.html">Əlavə B — Şkalalar</a> — skrininq şkalaları: M-CHAT-R, AQ-10, ASRS, SNAP-IV.</li>
<li><a href="yekun.html">Yekun tövsiyələr</a> — kitabın fəsillərindən çıxan əsas klinik dərslər.</li>
</ul>

<h2 id="onlayn-testler">Onlayn testlər</h2>
<ul>
<li><a href="/books/phoenix-era/test/">Münasibət modellərinin xəritəsi</a> — «Feniks Erası» kitabı üzrə onlayn test.</li>
<li><a href="/books/virus-viny/22-1-ci-bolme-ozunu-yoxlama-testleri.html">Özünü yoxlama testləri</a> — «Günahkarlıq Virusu» kitabının test bölməsi.</li>
</ul>

<h2 id="saytda-elave-materiallar">Saytda əlavə materiallar</h2>
<ul>
<li><a href="/blog-klinik-psixiatriya.html">Klinik Psixiatriya — XBT-11 rəhbərliyi</a> — kitab haqqında bloq yazısı.</li>
<li><a href="/klinik-psixiatriya.html">Kitabın sifarişi</a> — çap nüsxəsinin sifariş səhifəsi.</li>
<li><a href="/books/">Kitablar</a> — saytdakı bütün kitablar.</li>
</ul>""",
    "ru": """<h2 id="stranicy-razdela">Страницы раздела</h2>
<ul>
<li><a href="abbreviatur.html">Терминологический словарь</a> — сокращения и клинические термины, в том числе на трёх языках.</li>
<li><a href="elave-acde.html">Приложения A–E</a> — стандарты мониторинга и обследования, практические протоколы.</li>
<li><a href="elave-skalalar.html">Приложение B — Шкалы</a> — скрининговые шкалы: M-CHAT-R, AQ-10, ASRS, SNAP-IV.</li>
<li><a href="yekun.html">Заключительные рекомендации</a> — главные клинические уроки книги.</li>
</ul>

<h2 id="onlajn-testy">Онлайн-тесты</h2>
<ul>
<li><a href="/books/phoenix-era/test/ru/">Карта моделей взаимоотношений</a> — онлайн-тест по книге «Эра Феникса».</li>
<li><a href="/books/virus-viny/ru/22-glava-22.html">Тесты для самопроверки</a> — тестовый раздел книги «Вирус вины».</li>
</ul>

<h2 id="materialy-na-sajte">Дополнительные материалы на сайте</h2>
<ul>
<li><a href="/blog-klinik-psixiatriya.html">Klinik Psixiatriya — руководство по МКБ-11</a> — статья в блоге о книге (AZ).</li>
<li><a href="/klinik-psixiatriya.html">Заказ книги</a> — страница заказа печатного экземпляра (AZ).</li>
<li><a href="/books/ru/">Книги</a> — все книги сайта.</li>
</ul>""",
    "en": """<h2 id="section-pages">Section pages</h2>
<ul>
<li><a href="abbreviatur.html">Glossary of terms</a> — abbreviations and clinical terms, including three-language equivalents.</li>
<li><a href="elave-acde.html">Appendices A–E</a> — monitoring and examination standards, practical protocols.</li>
<li><a href="elave-skalalar.html">Appendix B — Scales</a> — screening scales: M-CHAT-R, AQ-10, ASRS, SNAP-IV.</li>
<li><a href="yekun.html">Final recommendations</a> — the key clinical lessons of the book.</li>
</ul>

<h2 id="online-tests">Online tests</h2>
<ul>
<li><a href="/books/phoenix-era/test/">Relationship models map</a> — online test based on the book “Phoenix Era” (AZ).</li>
<li><a href="/books/virus-viny/en/22-part-1-self-assessment-tests.html">Self-assessment tests</a> — the test section of the book “The Guilt Virus”.</li>
</ul>

<h2 id="more-on-the-site">More on the site</h2>
<ul>
<li><a href="/blog-klinik-psixiatriya.html">Klinik Psixiatriya — ICD-11 guide</a> — blog article about the book (AZ).</li>
<li><a href="/klinik-psixiatriya.html">Book order</a> — order page for the printed copy (AZ).</li>
<li><a href="/books/en/">Books</a> — all books on the site.</li>
</ul>""",
    "tr": """<h2 id="bolum-sayfalari">Bölümün sayfaları</h2>
<ul>
<li><a href="abbreviatur.html">Terim sözlüğü</a> — kısaltmalar ve klinik terimler, üç dildeki karşılıklarıyla.</li>
<li><a href="elave-acde.html">Ekler A–E</a> — izlem ve muayene standartları, pratik protokoller.</li>
<li><a href="elave-skalalar.html">Ek B — Ölçekler</a> — tarama ölçekleri: M-CHAT-R, AQ-10, ASRS, SNAP-IV.</li>
<li><a href="yekun.html">Son öneriler</a> — kitabın temel klinik dersleri.</li>
</ul>

<h2 id="cevrimici-testler">Çevrimiçi testler</h2>
<ul>
<li><a href="/books/phoenix-era/test/">Münasibət modellərinin xəritəsi</a> — «Feniks Erası» kitabına göre çevrimiçi test (AZ).</li>
<li><a href="/books/virus-viny/22-1-ci-bolme-ozunu-yoxlama-testleri.html">Özünü yoxlama testləri</a> — «Günahkarlıq Virusu» kitabının test bölümü (AZ).</li>
</ul>

<h2 id="sitede-ek-materyaller">Sitede ek materyaller</h2>
<ul>
<li><a href="/blog-klinik-psixiatriya.html">Klinik Psixiatriya — XBT-11 rəhbərliyi</a> — kitap hakkında blog yazısı (AZ).</li>
<li><a href="/klinik-psixiatriya.html">Kitabın sifarişi</a> — basılı nüsha sipariş sayfası (AZ).</li>
<li><a href="/books/">Kitablar</a> — sitedeki tüm kitaplar (AZ).</li>
</ul>""",
}
EMPTY_READ = '      <div class="bk-read">\n      </div>'


def main():
    for lang, block in BLOCKS.items():
        p = (ROOT / lang if lang else ROOT) / "melumat.html"
        t = p.read_text(encoding="utf-8")
        assert SUB_OLD[lang] in t, f"{p}: не найден старый подзаголовок"
        assert EMPTY_READ in t, f"{p}: не найден пустой bk-read"
        if APPLY:
            t = t.replace(SUB_OLD[lang], SUB_NEW[lang])
            t = t.replace(EMPTY_READ, '      <div class="bk-read">\n' + block + '\n      </div>')
            p.write_text(t, encoding="utf-8")
        print(f"{lang or 'az':>2}: {p.name} — подзаголовок + {block.count('<li>')} ссылок")
    print("ПРИМЕНЕНО." if APPLY else "СУХОЙ ПРОГОН.")


if __name__ == "__main__":
    main()
