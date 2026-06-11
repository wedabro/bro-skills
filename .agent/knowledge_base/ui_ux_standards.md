# 🎨 UI/UX Standards (Anti-Slop & Premium)

## 🌈 Brand Palette & Color Calibration
- **Anti-Default**: PROHIBITED using browser default colors (original red/blue/green). Misuse of the "AI Purple" gradient is PROHIBITED.
- **Premium Consumer Ban**: Avoid using AI's default cream/beige + bronze/clay palette unless the brief specifically requires it. Use alternative palettes like Cold Luxury (silver-grey + chrome), Forest (deep green + bone), or Black and Tan.
- **1 Accent Rule**: Choose a single accent color (Accent) and use it consistently across the entire page.

## 🔡 Typography (Anti-Slop)
- **Display Font**: PROHIBITED using `Inter` as default for creative headings. Use `Geist` , `Satoshi` , `Cabinet Grotesk` , `Outfit` or a font suitable for the project.
- **Serif Discipline**: DO NOT use serif fonts as default unless the brand requires editorial/luxury/vintage style. It is forbidden to mix serif and sans serif text in the same title.
- **Hierarchy**: H1 title maximum 2 lines. Subtitles (subtext) maximum 20 words.

## 📏 Layout & Rhythm
- **Hero Section**: Limit top padding (max `pt-24` on desktop).
- **Anti-Center Bias**: Avoid boringly centering Hero if it is not a manifesto page. Prioritize Split Screen or Asymmetric layout.
- **Eyebrow Restraint**: PROHIBITED abuse of "eyebrow" (small capital title above) in all sections. Maximum 1 eyebrow per 3 sections.
- **Bento Grid**: The Bento Grid must have rhythm. The number of cells equals the exact amount of content. Do not leave blank cells. Need to diversify cells (realistic images, gradients, text).
- **Zigzag Ban**: Maximum 2 consecutive sections use a reversed "left-image-right-text" layout (zigzag).

## 🧱 Core Components (Atomic) & Accessibility
- **Buttons (CTAs)**:
  - It is PROHIBITED to have wrapped text on the button on the desktop. Label button maximum 3 words (for example: `Get Started` ).
  - 2 CTAs with the same purpose (same intent) are PROHIBITED from appearing on the same page (select only 1 label).
  - Minimum WCAG AA contrast ratio 4.5:1 (No white text on light gray background).
- **Interactive UI States**:
  - Skeletal loaders for loading data (don't use generic spinners).
  - Tactile Feedback: Add `-translate-y-[1px]` or `scale-[0.98]` when `:active` to create a physical click feeling.
- **Images**: REQUIRED real images (from image gen tool, unsplash, picsum). It is PROHIBITED to use `div` fake screenshots.

## ✨ Micro-animations
- Use `framer-motion` or `gsap` intentionally.
- Motion must support `prefers-reduced-motion` .
- It is PROHIBITED to repeat marquee (horizontal text) more than once on a page.
