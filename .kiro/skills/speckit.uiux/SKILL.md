---
name: speckit.uiux
description: UI/UX Architect - Äá»‹nh nghÄ©a Design System, UI Components, Spacing, Typography, Responsive Patterns.
role: UI/UX Architect
---

## ðŸŽ¯ Mission
Thiáº¿t láº­p vÃ  quáº£n lÃ½ tiÃªu chuáº©n UI/UX "Pro Max" cho dá»± Ã¡n, Ä‘áº£m báº£o giao diá»‡n premium, chuyÃªn nghiá»‡p vÃ  nháº¥t quÃ¡n.

## ðŸ“¥ Input
- `.agent/specs/[feature]/spec.md` (chá»©a User Scenarios)
- `.agent/memory/constitution.md` (tech stack constraints)
- Brand guidelines (logo, mÃ u sáº¯c tá»« developer)

## ðŸ“‹ Protocol

### Phase 1: Brand Identity & Colors
- Äá»‹nh nghÄ©a báº£ng mÃ u (Primary, Secondary, Accent, State Colors).
- Äá»‹nh nghÄ©a Typography (Font families, Font sizes cho Heading/Body).
- **TrÃ¡nh mÃ u generic** (red, blue, green nguyÃªn báº£n). DÃ¹ng HSL hoáº·c palette bÃ i báº£n.

### Phase 2: Spacing & Layout
- Äá»‹nh nghÄ©a Container max-width (7xl, 1280px, v.v.).
- Spacing system (Padding/Margin chuáº©n: 4, 8, 16, 24, 32px).
- Responsive Grid system cho Mobile/Tablet/Desktop.

### Phase 3: Core Components Design
- **Buttons**: CÃ¡c tráº¡ng thÃ¡i default, hover, active, disabled.
- **Cards**: Shadow, border-radius, hover transitions.
- **Forms**: Input styles, error states, focus rings.
- **Badges/Tags**: Tráº¡ng thÃ¡i Sale, Hot, New, v.v.

### Phase 4: Rich Aesthetics Directive
- Sá»­ dá»¥ng Glassmorphism, Vibrancy, Gradients náº¿u phÃ¹ há»£p.
- Äá»‹nh nghÄ©a Micro-animations (framer-motion, CSS transitions).

## ðŸ“¤ Output
- File: `.agent/knowledge_base/ui_ux_standards.md`
- File: `.agent/specs/[feature]/ui-specs.md` (cho tá»«ng tÃ­nh nÄƒng)

## ðŸš« Guard Rails
- KHÃ”NG sá»­ dá»¥ng mÃ u máº·c Ä‘á»‹nh cá»§a trÃ¬nh duyá»‡t.
- KHÃ”NG thiáº¿t káº¿ quÃ¡ phá»©c táº¡p gÃ¢y cháº­m performance.
- PHáº¢I Æ°u tiÃªn Mobile-first design.

## When to Use
- Khi thiáº¿t láº­p/cáº­p nháº­t Design System: color, typography, spacing, component spec.
- TrÆ°á»›c khi `@speckit.frontend` code UI cho tÃ­nh nÄƒng má»›i.
- **KHÃ”NG dÃ¹ng cho**: implement component thÃ nh code (â†’ `@speckit.frontend`), ná»™i dung chá»¯ (â†’ `@speckit.content`).

## Common Rationalizations
| LÃ½ do bao biá»‡n | Sá»± tháº­t |
|---|---|
| "DÃ¹ng mÃ u máº·c Ä‘á»‹nh trÃ¬nh duyá»‡t cho nhanh" | MÃ u generic lÃ m UI ráº» tiá»n, thiáº¿u nháº­n diá»‡n. DÃ¹ng palette HSL bÃ i báº£n. |
| "Spacing tÃ¹y chá»—, miá»…n Ä‘áº¹p lÃ  Ä‘Æ°á»£c" | Spacing tÃ¹y tiá»‡n gÃ¢y rá»‘i thá»‹ giÃ¡c. DÃ¹ng scale chuáº©n (4/8/16/24/32). |
| "Component states Ä‘á»ƒ frontend tá»± lo" | Thiáº¿u spec hover/active/disabled gÃ¢y UI khÃ´ng nháº¥t quÃ¡n. Äá»‹nh nghÄ©a Ä‘á»§. |
| "Mobile tÃ­nh sau, desktop trÆ°á»›c" | Mobile-first Ã©p Æ°u tiÃªn ná»™i dung cá»‘t lÃµi. Thiáº¿t káº¿ responsive tá»« Ä‘áº§u. |

## Red Flags
- DÃ¹ng mÃ u nguyÃªn báº£n (red/blue/green) thay vÃ¬ palette.
- Spacing khÃ´ng theo scale thá»‘ng nháº¥t.
- Component thiáº¿u Ä‘á»‹nh nghÄ©a Ä‘á»§ tráº¡ng thÃ¡i (hover/active/disabled/focus).
- Hiá»‡u á»©ng náº·ng lÃ m cháº­m render.
- Thiáº¿t káº¿ desktop-only, bá» qua mobile.

## Verification
- [ ] `ui_ux_standards.md` cÃ³ Ä‘á»§ color palette + typography + spacing scale.
- [ ] Core component (button/card/form/badge) cÃ³ spec Ä‘á»§ tráº¡ng thÃ¡i + focus ring.
- [ ] Responsive breakpoint Ä‘á»‹nh nghÄ©a rÃµ (mobile/tablet/desktop), mobile-first.
- [ ] Contrast mÃ u Ä‘áº¡t WCAG AA.
- [ ] CÃ³ `ui-specs.md` cho tÃ­nh nÄƒng Ä‘ang lÃ m.
