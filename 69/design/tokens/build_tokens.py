#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_tokens.py — ГЕНЕРАТОР ТОКЕНОВ: tokens.json → tokens.generated.css
========================================================================
Концепт 69. Принцип: значения задаются ТОЛЬКО в tokens.json.
Этот файл — единственное место, где они превращаются в CSS.

Запуск:
    python design/tokens/build_tokens.py

Результат:
    design/tokens/tokens.generated.css   — НЕ РЕДАКТИРОВАТЬ ВРУЧНУЮ

Что делает:
  1. Читает tokens.json
  2. Разворачивает ссылки вида {color.raw.night-0} в реальные значения
  3. Пишет CSS-переменные: цвет → --color-*, шрифт → --font-*,
     размер → --size-*, отступ → --space-*, и так далее
  4. Пишет темы (dark / light / sepia) — переопределение семантических ролей
  5. Адаптив: объекты {desktop, tablet, mobile} → медиа-запросы
  6. Проверяет полноту: нет ли ссылок на несуществующие токены
"""
import json, os, re, sys, io

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "tokens.json")
OUT = os.path.join(HERE, "tokens.generated.css")

# группы, которые превращаются в CSS-переменные, и их префикс
GROUPS = {
    "color": "color",
    "font": "font",
    "size": "size",
    "space": "space",
    "layout": "layout",
    "radius": "radius",
    "shadow": "shadow",
    "motion": "motion",
    "hero": "hero",
    "z": "z",
}

BREAK_TABLET = 768
BREAK_MOBILE = 560


def load():
    with io.open(SRC, encoding="utf-8") as f:
        return json.load(f)


def flatten(node, prefix="", out=None, sources=None):
    """Развернуть дерево в плоский словарь путь -> значение."""
    if out is None:
        out = {}
    if sources is None:
        sources = set()
    for k, v in node.items():
        if k.startswith("$"):
            continue
        path = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            # адаптивный объект?
            if set(v.keys()) <= {"desktop", "tablet", "mobile"} and v:
                out[path] = v
            else:
                flatten(v, path, out, sources)
        else:
            out[path] = v
    return out


def build_index(data):
    """Индекс всех значений: путь -> значение (для разворачивания ссылок)."""
    idx = {}
    def walk(node, prefix=""):
        for k, v in node.items():
            if k.startswith("$"):
                continue
            path = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict) and not (set(v.keys()) <= {"desktop", "tablet", "mobile"}):
                walk(v, path)
            else:
                idx[path] = v
    walk(data)
    return idx


REF = re.compile(r"\{([^}]+)\}")


def resolve(value, idx, seen=None):
    """Развернуть {ссылки}. Бросает ошибку на несуществующую ссылку."""
    if seen is None:
        seen = set()
    if not isinstance(value, str):
        return value

    def sub(m):
        key = m.group(1).strip()
        if key in seen:
            raise ValueError(f"циклическая ссылка: {key}")
        if key not in idx:
            raise ValueError(f"ссылка на несуществующий токен: {{{key}}}")
        v = idx[key]
        if isinstance(v, dict):
            raise ValueError(f"ссылка ведёт на группу, а не значение: {{{key}}}")
        return str(resolve(v, idx, seen | {key}))
    return REF.sub(sub, value)


def css_name(group, path):
    """путь токена -> имя CSS-переменной.
    color.semantic.bg -> --color-bg  (служебное слово 'semantic' убирается:
    компоненты ссылаются на роль, а не на слой)."""
    body = path.replace(".", "-")
    body = body.replace("-raw-", "-").replace("semantic-", "")
    return f"--{body}"


# ── СТОРОЖ КОНТРАСТА ────────────────────────────────────────────────────
# ПРИЧИНА: при первом прогоне системы служебные роли (text-faint,
# accent-soft) в светлой и сепия-темах дали 4.17:1 и 3.18:1 — ниже порога
# AA 4.5:1. На глаз это не видно, а читаемость страдает.
# РЕШЕНИЕ: проверка встроена в сборку. Сборка падает, если роль просела —
# подобрать цвет «примерно» больше нельзя.
AA_TEXT = 4.5      # обычный текст
AA_LARGE = 3.0     # крупный текст (18.66px+ bold / 24px+)


def _rgb(c):
    """'#RRGGBB' / '#RGB' / 'rgba(...)' -> (r,g,b)."""
    c = c.strip()
    if c.startswith("#"):
        h = c[1:]
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    nums = re.findall(r"[\d.]+", c)
    return tuple(int(float(x)) for x in nums[:3]) if nums else (0, 0, 0)


def _lum(c):
    def ch(v):
        v = v / 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (_rgb(c))
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def _ratio(fg, bg):
    l1, l2 = _lum(fg), _lum(bg)
    hi, lo = (l1, l2) if l1 > l2 else (l2, l1)
    return (hi + 0.05) / (lo + 0.05)


ROLES_CHECKED = [
    "text", "text-strong", "text-muted", "text-faint",
    "accent", "accent-soft", "on-accent",
]


def check_contrast(themes):
    """themes: {"dark": {роль: цвет, ...}, ...}. Возвращает список проблем."""
    problems = []
    report = []
    for tname, roles in themes.items():
        bg = roles.get("bg")
        if not bg:
            continue
        for role in ROLES_CHECKED:
            fg = roles.get(role)
            if not fg:
                continue
            # on-accent проверяется на фоне акцента, а не страницы
            base = roles.get("accent", bg) if role == "on-accent" else bg
            if not base.startswith("#"):
                continue   # прозрачные не считаем
            r = _ratio(fg, base)
            mark = "ok" if r >= AA_TEXT else ("только крупный" if r >= AA_LARGE else "ПРОВАЛ")
            report.append(f"    {tname:6} {role:13} {fg:9} {r:5.2f}:1  {mark}")
            if r < AA_TEXT and role != "on-accent":
                problems.append(f"{tname}: --color-{role} контраст {r:.2f}:1 < {AA_TEXT} (AA)")
    return problems, report


def main():
    data = load()
    idx = build_index(data)

    errors = []
    root_vars = []      # обычные
    tablet_vars = []    # переопределения на планшете
    mobile_vars = []    # на телефоне

    for group in GROUPS:
        node = data.get(group)
        if not isinstance(node, dict):
            continue
        # для цвета берём ТОЛЬКО semantic (raw — служебный)
        if group == "color":
            node = {"semantic": node.get("semantic", {})}
        flat = flatten(node, prefix=group)
        for path, val in flat.items():
            name = css_name(group, path)
            if isinstance(val, dict):
                # адаптивный
                if "desktop" in val:
                    try:
                        root_vars.append((name, resolve(val["desktop"], idx)))
                    except ValueError as e:
                        errors.append(f"{path}: {e}")
                if "tablet" in val:
                    try:
                        tablet_vars.append((name, resolve(val["tablet"], idx)))
                    except ValueError as e:
                        errors.append(f"{path}: {e}")
                if "mobile" in val:
                    try:
                        mobile_vars.append((name, resolve(val["mobile"], idx)))
                    except ValueError as e:
                        errors.append(f"{path}: {e}")
            else:
                try:
                    root_vars.append((name, resolve(val, idx)))
                except ValueError as e:
                    errors.append(f"{path}: {e}")

    if errors:
        print("ОШИБКИ В ТОКЕНАХ:")
        for e in errors:
            print("  ✗", e)
        sys.exit(1)

    # ── ТЕМЫ: определения (из них и проверка контраста, и генерация CSS) ──
    light_roles = {
        "bg": "#F7F4EE",
        "bg-elevated": "#FFFDF8",
        "surface": "#EFEAE0",
        "surface-glass": "rgba(26,26,30,.04)",
        "text": "#1A1A1E",
        "text-strong": "#0B0B0F",
        "text-muted": "#4A4741",
        "text-faint": "#6E695F",
        "border": "rgba(26,26,30,.14)",
        "border-strong": "rgba(26,26,30,.26)",
        "accent": "#8A6A22",
        "accent-soft": "#7D5F1C",
        "on-accent": "#FFFDF8",
        "link": "#8A6A22",
        "link-hover": "#6B5017",
        "focus-ring": "#8A6A22",
        "shadow-color": "rgba(60,50,20,.18)",
        "overlay": "rgba(247,244,238,.97)",
    }
    sepia_roles = {
        "bg": "#F2E8D5",
        "bg-elevated": "#F8F1E3",
        "surface": "#E9DCC3",
        "surface-glass": "rgba(43,36,25,.05)",
        "text": "#2B2419",
        "text-strong": "#191308",
        "text-muted": "#544736",
        "text-faint": "#6B5D48",
        "border": "rgba(43,36,25,.16)",
        "border-strong": "rgba(43,36,25,.3)",
        "accent": "#7A5A1E",
        "accent-soft": "#855F14",
        "on-accent": "#F8F1E3",
        "link": "#7A5A1E",
        "link-hover": "#5C4314",
        "focus-ring": "#7A5A1E",
        "shadow-color": "rgba(43,36,25,.2)",
        "overlay": "rgba(242,232,213,.97)",
    }

    # ── ПРОВЕРКА КОНТРАСТА (все три темы) ───────────────────────────────
    themes_for_check = {}
    dark_roles = {}
    for n, v in root_vars:
        if n.startswith("--color-") and isinstance(v, str) and v.startswith("#"):
            dark_roles[n.replace("--color-", "")] = v
    themes_for_check["dark"] = dark_roles
    for name, block in (("light", light_roles), ("sepia", sepia_roles)):
        themes_for_check[name] = dict(dark_roles)
        themes_for_check[name].update(block)

    cproblems, creport = check_contrast(themes_for_check)
    print("КОНТРАСТ (порог AA = 4.5:1):")
    for line in creport:
        print(line)
    if cproblems:
        print()
        print("ПРОВАЛ КОНТРАСТА — сборка остановлена:")
        for p in cproblems:
            print("  ✗", p)
        print("  Подобрать цвет заново. Порог не понижать.")
        sys.exit(2)
    print("    все роли проходят AA ✓")
    print()

    L = []
    L.append("/* ═══════════════════════════════════════════════════════════════════")
    L.append("   RAGIMOFF · СГЕНЕРИРОВАННЫЕ ТОКЕНЫ — НЕ РЕДАКТИРОВАТЬ ВРУЧНУЮ")
    L.append("   Источник: design/tokens/tokens.json")
    L.append("   Сборка:   python design/tokens/build_tokens.py")
    L.append("   ═══════════════════════════════════════════════════════════════════ */")
    L.append("")
    L.append(":root, [data-theme=\"dark\"] {")
    for n, v in root_vars:
        L.append(f"  {n}: {v};")
    L.append("}")
    L.append("")

    L.append("/* ── СВЕТЛАЯ ТЕМА: переопределяются только семантические роли ── */")
    L.append("[data-theme=\"light\"] {")
    for k, v in light_roles.items():
        L.append(f"  --color-{k}: {v};")
    L.append("}")
    L.append("")

    L.append("/* ── СЕПИЯ: тема читалки ── */")
    L.append("[data-theme=\"sepia\"] {")
    for k, v in sepia_roles.items():
        L.append(f"  --color-{k}: {v};")
    L.append("}")
    L.append("")

    if tablet_vars:
        L.append(f"/* ── ПЛАНШЕТ (≤{BREAK_TABLET}px) ── */")
        L.append(f"@media (max-width: {BREAK_TABLET}px) {{")
        L.append("  :root {")
        for n, v in tablet_vars:
            L.append(f"    {n}: {v};")
        L.append("  }")
        L.append("}")
        L.append("")

    if mobile_vars:
        L.append(f"/* ── ТЕЛЕФОН (≤{BREAK_MOBILE}px) ── */")
        L.append(f"@media (max-width: {BREAK_MOBILE}px) {{")
        L.append("  :root {")
        for n, v in mobile_vars:
            L.append(f"    {n}: {v};")
        L.append("  }")
        L.append("}")
        L.append("")

    text = "\n".join(L)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    print(f"OK: {OUT}")
    print(f"    переменных: {len(root_vars)}")
    print(f"    планшетных переопределений: {len(tablet_vars)}")
    print(f"    телефонных переопределений: {len(mobile_vars)}")
    print(f"    строк: {len(L)}")

    # контроль: вывести список групп переменных
    seen = {}
    for n, _ in root_vars:
        g = n.strip("-").split("-")[0]
        seen[g] = seen.get(g, 0) + 1
    print("    по группам: " + ", ".join(f"{k} {v}" for k, v in sorted(seen.items())))


if __name__ == "__main__":
    main()
