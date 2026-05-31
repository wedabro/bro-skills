---
name: speckit.plan
description: Technical Planner - Táº¡o plan.md tá»« spec (data model, API contracts, research).
role: System Architect
---

## ðŸŽ¯ Mission
Chuyá»ƒn spec.md (WHAT) thÃ nh plan.md (HOW) â€” kiáº¿n trÃºc ká»¹ thuáº­t chi tiáº¿t.

## ðŸ“¥ Input
- `.agent/specs/[feature]/spec.md`
- `.agent/memory/constitution.md`

## ðŸ“‹ Protocol

### Phase 0: Research
- Scan spec â†’ liá»‡t kÃª unknowns ("NEEDS CLARIFICATION").
- NghiÃªn cá»©u giáº£i phÃ¡p â†’ ghi vÃ o `research.md`.

### Phase 1: Data Model
- Tá»« entities trong spec â†’ táº¡o `data-model.md`:
  ```prisma
  model User {
    id    String @id @default(cuid())
    email String @unique
    // ...
  }
  ```
- XÃ¡c Ä‘á»‹nh relationships (1:N, N:N).

### Phase 2: API Contracts
- Tá»« User Scenarios â†’ táº¡o `contracts/[entity].md`:
  ```
  POST /api/v1/users
  Body: { email, password }
  Response: { data: User, token: string }
  Error: 400 | 409 | 500
  ```

### Phase 3: Architecture
- Táº¡o `plan.md` vá»›i:
  - Folder structure
  - Component hierarchy
  - State management approach
  - Authentication flow
  - Docker service topology

### Phase 4: Must-Haves (Goal-Backward)
- XÃ¡c Ä‘á»‹nh nhá»¯ng thá»© báº¯t buá»™c pháº£i diá»…n ra Ä‘á»ƒ hoÃ n thÃ nh má»¥c tiÃªu.
- ThÃªm section `must_haves` vÃ o `plan.md`:
  - `truths`: CÃ¡c káº¿t quáº£ ngÆ°á»i dÃ¹ng pháº£i tháº¥y Ä‘Æ°á»£c (vd: "User can see existing messages").
  - `artifacts`: CÃ¡c tÃ i nguyÃªn/file pháº£i Ä‘Æ°á»£c táº¡o (vd: Component A, file B, Endpoint C).
  - `key_links`: Sá»± káº¿t ná»‘i quan trá»ng trÃ¡nh Ä‘á»©t gÃ£y (vd: UI -> API gá»i báº±ng `fetch` -> model `findMany`).

### Gate Check
- So sÃ¡nh plan vs constitution â†’ BÃO Lá»–I náº¿u vi pháº¡m rules.

## ðŸ“¤ Output
- `.agent/specs/[feature]/plan.md`
- `.agent/specs/[feature]/data-model.md`
- `.agent/specs/[feature]/contracts/*.md`
- `.agent/specs/[feature]/research.md` (náº¿u cÃ³ unknowns)

## ðŸš« Guard Rails
- KHÃ”NG viáº¿t code trong bÆ°á»›c planning â€” chá»‰ kiáº¿n trÃºc.
- Má»i tech choice PHáº¢I justify lÃ½ do (khÃ´ng dÃ¹ng tech vÃ¬ "thÃ­ch").
- PHáº¢I check constitution compliance trÆ°á»›c khi output.

## When to Use
- Sau khi cÃ³ `spec.md`, cáº§n chuyá»ƒn WHAT â†’ HOW: data model, API contract, kiáº¿n trÃºc.
- **KHÃ”NG dÃ¹ng cho**: viáº¿t spec (â†’ `@speckit.specify`), chia task (â†’ `@speckit.tasks`), viáº¿t code (â†’ `@speckit.implement`).

## Common Rationalizations
| LÃ½ do bao biá»‡n | Sá»± tháº­t |
|---|---|
| "Vá»«a code vá»«a thiáº¿t káº¿ cho nhanh" | KhÃ´ng cÃ³ plan â†’ kiáº¿n trÃºc cháº¯p vÃ¡, sá»­a lá»›n vá» sau. Plan trÆ°á»›c. |
| "DÃ¹ng tech nÃ y vÃ¬ quen" | Tech choice khÃ´ng justify dá»… sai bÃ i toÃ¡n. Má»—i lá»±a chá»n ghi lÃ½ do. |
| "Unknown Ä‘á»ƒ code rá»“i tÃ­nh" | Unknown chÆ°a research thÃ nh rá»§i ro áº©n. Ghi NEEDS CLARIFICATION + research.md. |
| "Constitution check sau" | Plan vi pháº¡m Constitution kÃ©o cáº£ implement sai. Gate check trÆ°á»›c khi output. |

## Red Flags
- Plan chá»©a code tháº­t thay vÃ¬ kiáº¿n trÃºc.
- Tech choice khÃ´ng cÃ³ lÃ½ do.
- Thiáº¿u data-model.md hoáº·c contracts khi spec cÃ³ entity/endpoint.
- KhÃ´ng cÃ³ section must_haves (truths/artifacts/key_links).

## Verification
- [ ] `plan.md` cÃ³ folder structure, component hierarchy, auth flow, Docker topology.
- [ ] `data-model.md` + `contracts/*.md` khá»›p entity/scenario trong spec.
- [ ] Má»i tech choice cÃ³ justify; unknown ghi trong research.md.
- [ ] Section must_haves Ä‘áº§y Ä‘á»§ truths/artifacts/key_links.
- [ ] Gate check Constitution pass; khÃ´ng cÃ³ code trong plan.
