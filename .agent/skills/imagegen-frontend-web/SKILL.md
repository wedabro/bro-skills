---
name: imagegen-frontend-web
description: Generate premium horizontal website design-reference images for landing pages, marketing sites, and product pages. Use when the requested deliverable is web design imagery or when an image-first implementation workflow needs upstream section concepts. Produce images only, one standalone image per page section; do not write frontend code or mobile-app screens.
---

# Frontend Web Image Direction

Create a coherent set of implementation-ready website section images, not a compressed mood board.

## Output contract

- Generate one separate horizontal image for every requested section.
- Never combine multiple sections into one tall board or tiny overview.
- Keep one palette, typography system, material language, and narrative spine across the set.
- Make each image large enough to inspect and recreate accurately.
- Generate fresh section images; do not crop earlier outputs to simulate missing views.
- Return images only. Do not write code.

## Workflow

1. Infer audience, conversion goal, section list, brand constraints, and required visual tone.
2. Define a compact design bible: palette, type character, imagery, surfaces, grid, CTA language, and recurring motif.
3. Assign each section a distinct composition and purpose before generating.
4. Generate sections individually in narrative order while carrying the same design bible forward.
5. Check legibility, realistic content density, CTA clarity, cross-section consistency, and composition variety.

## Composition rules

- Keep the hero clean and readable; match headline scale to copy length and leave the main CTA visible.
- Vary composition anchors: centered, split, off-grid, full-bleed, product-led, editorial, or data-led as the story requires.
- Do not repeat left-text/right-image layouts throughout the page.
- Use real visual hierarchy instead of filling every section with cards, badges, pills, or KPI tiles.
- Avoid generic AI-purple gradients, empty glass panels, fake dashboards, placeholder copy, and decorative noise.
- Use background imagery, texture, typography, and negative space intentionally; not every section needs a container.
- Keep all visible text short, plausible, and comfortably readable at the output resolution.

## Detailed reference

Read only the relevant section of [references/full-guide.md](references/full-guide.md):

- Variation system and composition choices: search `COMBINATORIAL VARIATION ENGINE`.
- Hero constraints: search `HERO MINIMALISM RULES`.
- Section counting and sizing: search `IMAGE COUNT & PAGE SLICING`.
- Anti-slop, type, density, and material rules: search the corresponding heading.
- Standard page packs or examples: search `DEFAULT SITE PACKS` or `EXAMPLE INTERPRETATIONS`.

Use `rg -n "<heading>" references/full-guide.md`; do not load the full guide unless the brief genuinely needs the complete art-direction system.
