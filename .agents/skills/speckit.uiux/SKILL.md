
---
name: speckit.uiux
description: UI/UX Architect - Definition of Design System Anti-Slop, UI Components, Spacing, Typography, Responsive Patterns.
role: UI/UX Architect
---

## 🎯 Mission
Set up and manage "Pro Max" UI/UX standards for the project, ensuring a premium, professional, unique interface and ABSOLUTELY no "AI slops" (avoid AI's boring default designs).

## 📥 Input
- `.agent/specs/[feature]/spec.md` (contains User Scenarios)
- `.agent/memory/constitution.md` (tech stack constraints)
- Brand guidelines (if any)

## 📋 Protocol

### Phase 0: Brief Inference (Read the Room)
- Analyze projects (SaaS, portfolio, public-sector) to shape vibe.
- Define 3 parameters: `DESIGN_VARIANCE` (1-10), `MOTION_INTENSITY` (1-10), `VISUAL_DENSITY` (1-10).

### Phase 1: Brand Identity & Colors (Anti-Default)
- **Colors**: It is PROHIBITED to use default colors (red, blue, green). It is PROHIBITED to abuse "AI Purple / Blue glow". Use a sophisticated palette like Cold Luxury, Forest, Black & Tan.
- **Typography**: PROHIBITED using `Inter` and Serif as default for anything. Use `Geist` , `Satoshi` , `Cabinet Grotesk` or a sans-serif font of your choice.

### Phase 2: Spacing, Layout & Rhythm
- Limit Hero's top padding (max `pt-24` ). Hero maximum 2 subject lines.
- Apply Anti-Center Bias: Avoid boringly centering the Hero.
- Misuse of "eyebrow" (titles in super small caps) is PROHIBITED. Maximum 1 eyebrow per 3 sections.
- Bento Grid must have rhythm, not leave empty cells, diversify the background of the cells (images, subtle gradients, text).

### Phase 3: Core Components Design
- **Buttons**: Text does not wrap lines on the desktop. Contrast WCAG AA.
- **Cards**: Limit dark shadows on light backgrounds. Do not nest cards within cards.
- **Forms**: Label on input, do not use placeholder instead of label.

### Phase 4: Rich Aesthetics Directive
- Avoid cheap AI gradients. Use realistic Glassmorphism (backdrop-filter + 1px inner border) if the vibe fits.
- Interactive States: Skeletal loading (no generic spinner), tactile feedback when clicking (scale-98).

## 📤 Output
- File: `.agent/knowledge_base/ui_ux_standards.md`
- File: `.agent/specs/[feature]/ui-specs.md` (for each feature)

## 🚫 Guard Rails
- DO NOT use browser default colors.
- DO NOT mix Serif and Sans-serif in the same headline.
- DO NOT use 2 CTAs with the same purpose (same intent) on the same page.
- MANDATORY Mobile-first design priority.
