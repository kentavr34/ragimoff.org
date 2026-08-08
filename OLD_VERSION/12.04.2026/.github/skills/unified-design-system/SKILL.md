---
name: unified-design-system
description: '**WORKFLOW SKILL** — Single source of truth for all design, typography, spacing, and animation rules. USE FOR: enforcing consistency across all files, validating changes, and generating compliant CSS/HTML. INVOKES: file system tools, semantic search, LightRAG logging.'
---

# Unified Design System

## Core Principles

1. **Typography**
   - Primary font: `Inter` (fallback: `'Inter', 'Segoe UI', 'Arial Unicode MS', sans-serif`)
   - Base size: `18px` (1.125rem)
   - Scale (Major Third 1.25): `18px → 22.5px → 28px → 35px → 44px → 55px`
   - Line height: `body: 1.75`, `headings: 1.1–1.2`
   - `text-wrap: balance` for all multi-line headings

2. **Spacing System (8px Grid)**
   - CSS variables: `--space-1: 8px`, `--space-2: 16px`, `--space-3: 24px`, `--space-4: 32px`, `--space-5: 40px`, `--space-6: 48px`, `--space-7: 56px`, `--space-8: 64px`, `--space-9: 72px`, `--space-10: 80px`, `--space-11: 96px`, `--space-12: 128px`
   - Hero sections: `padding: var(--space-9) var(--space-4) var(--space-8)` (72px 32px 64px)
   - Standard sections: `padding: var(--space-11) var(--space-4)` (96px 32px)

3. **Colors & Borders**
   - Navy: `#061826`
   - Accent (gold): `#b59b72`
   - Light: `#f8f9fa`
   - Border: `1px solid rgba(0,0,0,0.08)`
   - Shadow: `0 24px 64px rgba(6,24,38,0.08)`

4. **Animations & Transitions**
   - Hover: `0.25s ease`
   - Scroll animations: `.fi` class (already implemented)
   - All transitions must use `var(--space-X)` for timing consistency

5. **Images & Layout**
   - Hero: `photo-hero-suit.jpg`, `object-fit: cover`, `max-height: 280px`
   - Galleries: `aspect-ratio: 16/9`, `object-fit: cover`
   - Max width: `1240px`
   - Mobile-first: `360px`, `640px`, `768px`, `1100px` breakpoints

## Workflow Enforcement

1. **Before any change**: Validate against this document
2. **During implementation**: Use only CSS variables and approved values
3. **After implementation**: Log to LightRAG with `change_type: design`
4. **Testing**: Verify on mobile (360px), tablet (768px), desktop (1280px)

## Audit Checklist (McKinsey Standard)

- [ ] No inline styles (except critical hero)
- [ ] No duplicate `style` attributes
- [ ] All padding/margin use `var(--space-X)`
- [ ] All headings use `text-wrap: balance`
- [ ] All images have `loading="lazy"` (hero: `eager`)
- [ ] All links use gold accent color
- [ ] No blue `#007bff` links on dark backgrounds
- [ ] All galleries use `aspect-ratio: 16/9`
- [ ] All text lines ≤ 75 characters
- [ ] All CTAs have `min-height: 44px`

## Integration

- **LightRAG logging**: Use `log_design_update()` from `lightrag_client.py`
- **CLI**: `python log_changes.py design "Unified system applied"`
- **Files affected**: `shared.css`, `shared.js`, all `*.html`

## Version
- **Date**: 2026-04-12
- **Author**: Ragimoff Design Team