---
name: image-to-code
description: "Build or reconstruct a visually important website through an image-first workflow: generate or inspect section references, analyze them, then implement matching responsive code. Use when the user supplies a website image to reproduce or explicitly wants a visual-first web build. Do not use for ordinary frontend edits, image-only deliverables, mobile apps, or brand boards."
---

# Image to Code

Treat the design image as an implementation specification, then ship working code that matches its hierarchy, rhythm, assets, and responsive intent.

## Precedence

- Use this skill as the single orchestrator for image-first web implementation.
- Invoke image generation as an internal step when references are missing; do not independently run a second competing web-design workflow.
- Use `design-taste-frontend` instead for normal code-first frontend work.
- Use `imagegen-frontend-web` alone when the user wants images but no code.

## Workflow

1. Inspect the repository, runtime, existing design system, routes, assets, and supplied images.
2. Determine the section list and identify which sections lack a readable reference.
3. Generate fresh, standalone section images only where needed. Prefer large section-specific references over a tiny full-page board.
4. Analyze each reference for layout, type, spacing, color, surfaces, imagery, components, and responsive behavior.
5. Implement with the existing stack, matching the reference before introducing stylistic reinterpretation.
6. Compare the rendered page against the reference and correct the largest visual deltas first.
7. Verify responsive behavior, interactions, reduced motion, accessibility, and build/tests.

## Non-negotiables

- Do not crop old images to manufacture missing section references.
- Keep the hero readable and visible on a small laptop; do not let decorative art bury copy or CTAs.
- Recreate hierarchy and spacing, not just colors and border radii.
- Avoid nested cards, micro-UI clutter, fake screenshots, and placeholder rectangles.
- Use real/generated assets at the correct aspect ratio and preserve focal points responsively.
- Extract repeated values into existing tokens or a small coherent token set; avoid one-off magic values everywhere.
- Preserve functionality and project conventions while improving visual fidelity.
- Do not claim fidelity without inspecting the rendered result at representative desktop and mobile sizes.

## Detailed reference

Read only the relevant section of [references/full-guide.md](references/full-guide.md):

- Deciding when to generate references: search `MANDATORY IMAGE-FIRST RULE` or `WHEN TO TRIGGER`.
- Section-image strategy: search `CODEX-SPECIFIC SECTION IMAGE` or `SECTION IMAGE GENERATION`.
- Visual analysis: search `DEEP IMAGE ANALYSIS REQUIREMENT`.
- Hero, responsive first view, and box reduction: search the corresponding heading.
- Extracting text, type, spacing, components, and color: search `EXTRACTION RULE`.
- Fidelity and missing details: search `ANTI-DRIFT` or `MISSING DETAIL RESOLUTION`.
- Final verification: search `CLARITY CHECK`.

Use `rg -n "<heading>" references/full-guide.md`; read the full guide only for a large, ambiguous reconstruction requiring the complete protocol.
