---
name: design-taste-frontend
description: Implement premium new frontend landing pages, portfolios, editorial sites, and marketing pages without generic AI styling. Use for code-producing web UI work, including responsive layout, typography, assets, and motion. Do not use for broad redesign audits of existing products, image-only concepts, mobile-app screens, dashboards, data tables, or image-first reconstruction; use the dedicated skill instead.
---

# Design Taste Frontend

Ship polished frontend code that fits the brief and the existing project. Treat every rule as contextual, not as a style preset.

## Scope and precedence

- Use `image-to-code` when an existing reference image must be reconstructed or the task explicitly requires an image-first workflow.
- Use `imagegen-frontend-web` when the deliverable is design imagery only.
- Use `redesign-existing-projects` when auditing and broadly upgrading an existing interface is the primary task.
- Use this skill for new builds and focused frontend implementation work.
- Preserve the project's framework, design system, conventions, and working behavior unless the user requests a migration.

## Workflow

1. Inspect the brief, repository, existing UI, assets, dependencies, and responsive behavior.
2. State one short design read: page kind, audience, visual direction, and implementation foundation.
3. Choose a restrained system for type, color, spacing, radius, imagery, and motion. Reuse existing tokens and installed packages first.
4. Implement the smallest coherent change that covers the whole page or requested surface.
5. Verify desktop and mobile layout, interaction states, reduced motion, contrast, overflow, and build/tests.

Ask one clarifying question only when two materially different design directions remain plausible. Otherwise infer and proceed.

## Non-negotiables

- Avoid templated defaults: purple glow, centered dark-mesh hero, repeated three-card rows, excessive glass, and uniform section rhythms.
- Keep one visual language per page: one palette, one radius system, one icon family, and consistent type hierarchy.
- Use cards only when grouping or elevation carries meaning. Prefer spacing, dividers, and composition otherwise.
- Give each section a distinct job and vary layout families; never repeat split-image rows more than twice consecutively.
- Keep the hero visible on a small laptop: concise headline, short supporting copy, and primary CTA above the fold.
- Use real or generated visual assets when imagery matters. Do not fake product screenshots with decorative divs.
- Use factual copy. Label sample data and never invent precise metrics, specifications, awards, or customer claims.
- Implement loading, empty, error, hover, focus, and active states when the surface requires them.
- Use CSS Grid for structural layouts and explicit mobile fallbacks for every multi-column section.
- Respect `prefers-reduced-motion`; add motion only when it communicates hierarchy, story, feedback, or state.
- Check installed dependencies before importing. Prefer native CSS and the existing stack over new packages.
- Audit visible copy, CTA contrast, focus states, navigation wrapping, overflow, and image alt text before finishing.

## Detailed reference

Do not load the full guide for routine component work. Read only the relevant portion of [references/full-guide.md](references/full-guide.md) when the task needs one of these deeper protocols:

- Design-system selection or install commands: search `BRIEF → DESIGN SYSTEM MAP` or `Appendix A`.
- Typography, palette, layout, assets, or content rules: search `DESIGN ENGINEERING DIRECTIVES`.
- GSAP sticky stacks or horizontal scroll: search `CONTEXT-AWARE PROACTIVITY`.
- Dark mode and accessibility constraints: search `PERFORMANCE & ACCESSIBILITY` or `DARK MODE PROTOCOL`.
- Redesign preservation decisions: search `REDESIGN PROTOCOL`.
- Final comprehensive audit: search `FINAL PRE-FLIGHT CHECK`.

Use `rg -n "<heading or phrase>" references/full-guide.md` to locate the needed section instead of reading the entire file.
