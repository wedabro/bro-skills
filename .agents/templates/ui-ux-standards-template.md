# 🎨 UI/UX Standards (Anti-Slop & Premium)

## 🌈 Brand Palette & Color Calibration
- **Anti-Default**: FORBIDDEN to use default browser colors (pure red/blue/green). FORBIDDEN to overuse "AI Purple" gradients.
- **Premium Consumer Ban**: Avoid AI default beige + brass/clay palettes unless explicitly requested. Use alternatives like Cold Luxury (silver-grey + chrome), Forest (deep green + bone), or Black and Tan.
- **1 Accent Rule**: Choose a single Accent color and use it consistently across the entire site.

## 🔡 Typography (Anti-Slop)
- **Display Font**: FORBIDDEN to use `Inter` as default for creative headings. Use `Geist`, `Satoshi`, `Cabinet Grotesk`, `Outfit`, or a project-specific font.
- **Serif Discipline**: DO NOT use Serif fonts as default unless brand requires editorial/luxury/vintage styles. Forbidden to mix serif and sans-serif fonts in the same heading.
- **Hierarchy**: H1 headings max 2 lines. Subtext max 20 words.

## 📏 Layout & Rhythm
- **Hero Section**: Limit top padding (max `pt-24` on desktop).
- **Anti-Center Bias**: Avoid boring centered Hero layout unless it's a manifesto page. Prefer Split Screen or Asymmetric layouts.
- **Eyebrow Restraint**: FORBIDDEN to overuse "eyebrow" headings. Max 1 eyebrow per 3 sections.
- **Bento Grid**: Bento grids must have rhythm. Number of cells must match content. No empty cells. Diversify cells (real images, gradients, text).
- **Zigzag Ban**: Max 2 consecutive sections using alternating image-text (zigzag) layouts.

## 🧱 Core Components (Atomic) & Accessibility
- **Buttons (CTAs)**:
  - FORBIDDEN to wrap button text on desktop. Button labels max 3 words (e.g., `Get Started`).
  - FORBIDDEN to have 2 CTAs with the same intent on the same page (choose only one label).
  - Minimum WCAG AA contrast ratio 4.5:1 (Do not use white text on light grey background).
- **Interactive UI States**:
  - Skeletal loaders for loading states (do not use generic spinners).
  - Tactile Feedback: Add `-translate-y-[1px]` or `scale-[0.98]` on `:active` states for a physical button feel.
- **Images**: REQUIRED to have real images (from image gen tools, Unsplash, Picsum). FORBIDDEN to use div fake screenshots.

## ✨ Micro-animations
- Use `framer-motion` or `gsap` intentionally.
- Animations must respect `prefers-reduced-motion`.
- FORBIDDEN to repeat marquee texts more than once per page.
