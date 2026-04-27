# -*- coding: utf-8 -*-
"""
Phase 1 infrastructure for Russian version.
- Copies all HTML files from root to /ru/
- In AZ files: removes 'Русская версия' footer link, adds AZ|RU toggle in nav
- In RU files: rewrites paths (relative ../ for shared assets), adds RU|AZ toggle, lang="ru"
- UI strings (nav labels, footer labels, common buttons) translated to Russian via dictionary
- Body content of RU pages remains AZ until manual translation phases
"""
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RU = ROOT / "ru"
RU.mkdir(exist_ok=True)

HTML_FILES = sorted([p.name for p in ROOT.glob("*.html")])

# UI translations: AZ → RU (applied only in /ru/ files)
UI_TRANSLATIONS = {
    # Nav items
    "Ana Səhifə": "Главная",
    "Haqqımda": "Обо мне",
    "Təhsil": "Обучение",
    "Ümumi Psixologiya": "Общая психология",
    "Klinik Psixologiya DPO": "Клиническая психология ДПО",
    "Psixoterapiya Praktikumu": "Практикум по психотерапии",
    "Qanuni Əsaslar": "Юридические основы",
    "Konsultasiya": "Консультация",
    "Ailə Terapiyası": "Семейная терапия",
    "Aile-Uşaq Terapiyası": "Детско-родительская терапия",
    "Depressiya": "Депрессия",
    "Panik Ataklar": "Панические атаки",
    "Sosial Fobiya": "Социофобия",
    "Gecə Enurezi": "Ночной энурез",
    "Korporativ": "Корпоративное",
    "Blog": "Блог",
    "Bloq": "Блог",
    "QEYDİYYAT": "ЗАПИСЬ",
    "Qeydiyyat": "Запись",
    "Mobil menyu": "Мобильное меню",

    # Footer columns
    "Terapiya": "Терапия",
    "Psixologiya Bloqu": "Психология (блог)",
    "YouTube Dərslər": "Уроки на YouTube",
    "Əlaqə": "Контакты",

    # Misc UI
    "Psixologiya Məktəbi": "Школа психологии",
    "Bağla": "Закрыть",
    "Əvvəlki": "Предыдущий",
    "Növbəti": "Следующий",
    "© 2026 RAGIMOFF Peşəkar Psixologiya Məktəbi. Peşəkar Nüfuzun Ünvanı.": "© 2026 RAGIMOFF — Профессиональная школа психологии. Адрес профессиональной репутации.",
    "Kənan Rəhimov — Həkim-Psixiatr, Psixoterapevt. 23 il klinik təcrübə. Bakı, Azərbaycan.": "Кенан Рагимов — Врач-психиатр, психотерапевт. 23 года клинической практики. Баку, Азербайджан.",

    # CTA buttons
    "WhatsApp ilə Yazın": "Написать в WhatsApp",
    "Daha Ətraflı": "Подробнее",
    "Bütün Xidmətlər": "Все услуги",
    "Digər Məqalələr": "Другие статьи",
    "Məqaləni oxu": "Читать статью",
    "Oxu": "Читать",
    "Ən Yeni Məqalə": "Самая новая статья",
}

LANG_TOGGLE_AZ = (
    '<a href="ru/{ru_path}" class="lang-switch" aria-label="Русская версия">RU</a>'
    '<a href="{az_path}" class="lang-switch lang-active" aria-label="Azərbaycanca">AZ</a>'
)
LANG_TOGGLE_RU = (
    '<a href="../{az_path}" class="lang-switch" aria-label="Azərbaycan dili">AZ</a>'
    '<a href="{ru_path}" class="lang-switch lang-active" aria-label="Русский">RU</a>'
)

LANG_TOGGLE_MOBILE_AZ = '<a href="ru/{ru_path}" class="mobile-lang">Русская версия</a>'
LANG_TOGGLE_MOBILE_RU = '<a href="../{az_path}" class="mobile-lang">Azərbaycan dili</a>'


def remove_russian_link(html: str) -> str:
    """Remove the 'Русская версия' link in footer-bottom of AZ files."""
    pattern = re.compile(
        r'\s*<a href="https://www\.psychotherapyru\.com"[^>]*>Русская версия</a>',
        re.IGNORECASE,
    )
    return pattern.sub("", html)


def inject_lang_toggle_az(html: str, filename: str) -> str:
    """Insert AZ|RU toggle into desktop-nav and mobile-nav for AZ file."""
    toggle = LANG_TOGGLE_AZ.format(ru_path=filename, az_path=filename)
    # Insert before the QEYDİYYAT/CTA link in desktop-nav
    html = re.sub(
        r'(<a href="tehsil\.html#registration" class="nav-cta"[^>]*>QEYDİYYAT</a>)',
        toggle + r"\n          \1",
        html,
        count=1,
    )
    # Mobile nav: before the registration button
    mobile = LANG_TOGGLE_MOBILE_AZ.format(ru_path=filename)
    html = re.sub(
        r'(<a href="tehsil\.html#registration" class="btn btn-fill"[^>]*>QEYDİYYAT</a>)',
        mobile + r"\n      \1",
        html,
        count=1,
    )
    return html


def inject_lang_toggle_ru(html: str, filename: str) -> str:
    """Insert RU|AZ toggle into RU file."""
    toggle = LANG_TOGGLE_RU.format(az_path=filename, ru_path=filename)
    html = re.sub(
        r'(<a href="tehsil\.html#registration" class="nav-cta"[^>]*>[^<]*</a>)',
        toggle + r"\n          \1",
        html,
        count=1,
    )
    mobile = LANG_TOGGLE_MOBILE_RU.format(az_path=filename)
    html = re.sub(
        r'(<a href="tehsil\.html#registration" class="btn btn-fill"[^>]*>[^<]*</a>)',
        mobile + r"\n      \1",
        html,
        count=1,
    )
    return html


def fix_ru_paths(html: str) -> str:
    """In RU files: shared assets (gtc.css, shared.js, images/) need ../ prefix."""
    html = html.replace('href="gtc.css"', 'href="../gtc.css"')
    html = html.replace('src="shared.js"', 'src="../shared.js"')
    html = re.sub(r'src="images/', 'src="../images/', html)
    html = re.sub(r"url\('images/", "url('../images/", html)
    html = re.sub(r'url\("images/', 'url("../images/', html)
    return html


def translate_ui(html: str) -> str:
    """Apply UI dictionary translations (only in /ru/ files)."""
    # Sort keys by length desc to avoid partial replacements
    for az, ru in sorted(UI_TRANSLATIONS.items(), key=lambda kv: -len(kv[0])):
        html = html.replace(az, ru)
    # html lang="az" → lang="ru"
    html = html.replace('<html lang="az">', '<html lang="ru">')
    return html


def process():
    for filename in HTML_FILES:
        src = ROOT / filename
        html = src.read_text(encoding="utf-8")

        # AZ version: clean + inject toggle
        az_html = remove_russian_link(html)
        az_html = inject_lang_toggle_az(az_html, filename)
        src.write_text(az_html, encoding="utf-8")

        # RU version: fix paths + inject toggle + UI translation
        ru_html = fix_ru_paths(html)
        ru_html = remove_russian_link(ru_html)
        ru_html = inject_lang_toggle_ru(ru_html, filename)
        ru_html = translate_ui(ru_html)
        (RU / filename).write_text(ru_html, encoding="utf-8")
        print(f"OK  {filename}")


if __name__ == "__main__":
    process()
    print(f"\nTotal: {len(HTML_FILES)} files processed (AZ + RU).")
