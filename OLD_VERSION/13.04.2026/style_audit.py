import re
from pathlib import Path

ALLOWED_FONTS = [
    "Inter",
    "Segoe UI",
    "Arial Unicode MS",
    "sans-serif",
]

FONT_IMPORT_PATTERN = re.compile(r"fonts\.googleapis\.com/css2\?family=([^&\"]+)")
FONT_FAMILY_PATTERN = re.compile(r"font-family\s*:\s*([^;]+);")
STYLE_ATTR_PATTERN = re.compile(r"style\s*=\s*\"([^\"]*)\"")
SPACING_PATTERN = re.compile(r"(?:margin|padding)(?:-(?:top|right|bottom|left))?\s*:\s*([^;]+);")
PX_VALUE_PATTERN = re.compile(r"(-?\d+(?:\.\d+)?)px")

html_files = list(Path('.').glob('*.html')) + list(Path('ru').glob('*.html'))
css_files = [Path('shared.css')]

issues = []


def parse_font_families(value):
    parts = [p.strip().strip('"\'') for p in value.split(',')]
    return parts


def is_allowed_family(families):
    for family in families:
        if family in ALLOWED_FONTS:
            return True
    return False


def check_font_family_declaration(line, location):
    value = line.strip()
    families = parse_font_families(value)
    if not any(f in ALLOWED_FONTS for f in families):
        return f"Invalid font-family '{value}' at {location}"
    # also ensure only allowed fonts appear
    bad = [f for f in families if f not in ALLOWED_FONTS]
    if bad:
        return f"Disallowed font family values {bad} at {location}"
    return None


def check_spacing_values(value, location):
    errors = []
    for match in PX_VALUE_PATTERN.finditer(value):
        val = float(match.group(1))
        if abs(val) % 8 != 0:
            errors.append(f"Non-8px spacing {val}px at {location}")
    return errors


def analyze_file(path, text):
    path_issues = []
    for m in FONT_IMPORT_PATTERN.finditer(text):
        imported = m.group(1)
        if 'Inter' not in imported:
            path_issues.append(f"Font import contains non-Inter family: {imported}")
    for m in FONT_FAMILY_PATTERN.finditer(text):
        declaration = m.group(1)
        location = f"{path}:font-family declaration"
        families = parse_font_families(declaration)
        if not any(f in ALLOWED_FONTS for f in families):
            path_issues.append(f"Invalid font-family '{declaration}'")
        bad = [f for f in families if f not in ALLOWED_FONTS]
        if bad:
            path_issues.append(f"Disallowed font family values {bad} in '{declaration}'")
    for style_match in STYLE_ATTR_PATTERN.finditer(text):
        style_value = style_match.group(1)
        for m in re.finditer(r"font-family\s*:\s*([^;]+);", style_value):
            declaration = m.group(1)
            families = parse_font_families(declaration)
            if not any(f in ALLOWED_FONTS for f in families):
                path_issues.append(f"Invalid inline font-family '{declaration}'")
            bad = [f for f in families if f not in ALLOWED_FONTS]
            if bad:
                path_issues.append(f"Disallowed inline font family values {bad} in '{declaration}'")
        for m in SPACING_PATTERN.finditer(style_value):
            spacing_value = m.group(1)
            path_issues.extend(check_spacing_values(spacing_value, f"{path} inline style"))
    return path_issues


def main():
    all_issues = {}
    for path in html_files + css_files:
        text = path.read_text(encoding='utf-8', errors='ignore')
        file_issues = analyze_file(path, text)
        if file_issues:
            all_issues[str(path)] = file_issues

    if not all_issues:
        print('PASS: No style violations found in font-family or spacing checks.')
        return

    print('STYLE AUDIT REPORT')
    print('==================\n')
    for path, file_issues in all_issues.items():
        print(f'{path}:')
        for issue in file_issues:
            print(f'  - {issue}')
        print('')

if __name__ == '__main__':
    main()
