# Ragimoff.org Project Bible

## 1. Typography and font policy
- Primary body font: **Inter** across the entire site.
- Use a single font family for all pages where possible to keep the visual system consistent and premium.
- Fallback stack must preserve Azerbaijani letter support: `'Inter', 'Segoe UI', 'Arial Unicode MS', sans-serif`.
- Avoid mixing serif and sans-serif families on the same page.
- Only fonts with accurate Azerbaijani diacritic rendering may be used in headings and body text.

## 2. Typography scale
- Base text: **16px**.
- Paragraph / body: **1rem** with line-height **1.75**.
- Lead text: **1.25rem**.
- Headings:
  - H1: **3.5rem** / **56px** maximum.
  - H2: **2.8125rem** / **45px** maximum.
  - H3: **1.875rem** / **30px**.
  - H4: **1.5625rem** / **25px**.
- Keep headings letter-spacing subtle: **-0.02em** to **0em**.
- Use a maximum line length of **70ch** for readable paragraphs.

## 3. Layout and spacing
- Maintain an **8px grid system** with spacing variables: 8, 16, 24, 32, 40, 48, 56, 64.
- All sections should use consistent padding and margins from the shared spacing scale.
- Use equal-height content panels for side-by-side sections where applicable.
- Keep major content blocks **symmetrical**: left/right columns, cards, feature grids.
- Preserve breathing room around text blocks, especially hero sections and cards.

## 4. Navigation and buttons
- Navigation labels: uppercase, medium weight, and at least **0.875rem** for legibility.
- CTA buttons should be at least **48px high** with generous horizontal padding.
- Use premium accent states consistently: gold accent for primary actions and deep navy for dark CTA states.
- Maintain a visual hierarchy between text links, secondary buttons, and primary buttons.

## 5. Certificate and gallery presentation
- Use consistent grid sizing for certificates and proof images: **auto-fit** with minimum card width of **280px**.
- Images in certificate/gallery cards must share the same **aspect ratio** and border style.
- Each certificate card should include a compact label block with a small title and supporting detail.
- Avoid mixed gallery layouts with different widths or unbalanced rows.
- Do not reuse the same photo more than once on a single page; each page should feel visually fresh and unique.

## 6. Accessibility and contrast
- Text color should be high contrast on backgrounds: avoid low-contrast grey text for body copy.
- Use dark text on white/light backgrounds and light text on dark/navy backgrounds.
- Buttons and interactive elements must be easily clickable on mobile.
- Keep link and button spacing large enough for thumb targets.

## 7. Design rule enforcement
- All typography choices and layout rules are part of the project bible.
- Global styles for `body`, `button`, `input`, `textarea`, `select`, and `a` must inherit the approved font stack.
- Any new page or section must follow this file before adding custom overrides.
- Document deviations in the project bible when a local exception is necessary.

## 8. LightRAG project metadata
- Tag updates using `design` or `docs` changes in LightRAG.
- Keep the project history linked to file changes and the rule set.
- Save major design-system decisions as discrete logged entries to preserve development history.
