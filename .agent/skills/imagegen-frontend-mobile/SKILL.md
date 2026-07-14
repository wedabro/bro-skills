---
name: imagegen-frontend-mobile
description: Generate premium app-native mobile screen images and coherent multi-screen flows for iOS, Android, or cross-platform products. Use when the deliverable is mobile UI imagery, screen concepts, or phone-mockup presentations. Produce images only; do not write app code, website sections, or brand-guideline boards.
---

# Mobile App Image Direction

Generate readable, internally consistent mobile screens that feel native to the requested platform and product category.

## Output contract

- Generate enough standalone screens to show the requested flow; one image must not pretend to cover several unreadable screens.
- Default to a subtle premium phone frame unless the user asks for frameless screens.
- Keep the app UI, not the device mockup, as the visual focus.
- Generate fresh screens for missing states; never crop prior images into new deliverables.
- Return images only. Do not write code.

## Workflow

1. Determine platform mode, audience, primary job, navigation model, and exact flow.
2. Define a design bible: palette, type scale, spacing, icon style, imagery, surface treatment, and signature component.
3. Map the minimum complete screen sequence, including important success, empty, error, or permission states.
4. Generate screens in flow order while preserving navigation, tokens, copy tone, and component behavior.
5. Check safe areas, tap-target plausibility, text size, state continuity, platform conventions, and mockup framing.

## Non-negotiables

- Design for a phone viewport first; do not shrink a desktop dashboard into a handset.
- Keep primary actions reachable and hierarchy obvious at a glance.
- Use platform conventions intentionally: iOS, Android, or a consistent cross-platform neutral language.
- Avoid excessive cards, pills, floating glass, tiny labels, fake metrics, and decorative gradients.
- Keep one navigation model across the flow unless a state explicitly changes it.
- Use images and texture when they support the product; never sacrifice text readability.
- Use one coherent icon family and consistent component geometry.
- Keep onboarding concise and show product value before asking for unnecessary permissions.

## Detailed reference

Read only the relevant section of [references/full-guide.md](references/full-guide.md):

- Platform conventions: search `PLATFORM MODE RULE`.
- Screen count and flow planning: search `GENERATE ENOUGH SCREENS` or `LOGICAL FLOW RULE`.
- Mockup and safe-area details: search `DEVICE MOCKUP FRAME` or `SAFE AREA`.
- Navigation, iconography, texture, palette, or typography: search the matching heading.
- Product-category guidance: search `CATEGORY-SPECIFIC BIAS`.
- Regeneration and final checks: search `REGENERATION RULE` or `QUALITY CHECK`.

Use `rg -n "<heading>" references/full-guide.md`; avoid loading the complete guide for a small, well-specified flow.
