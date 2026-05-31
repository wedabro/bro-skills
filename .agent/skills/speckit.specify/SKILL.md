---
name: speckit.specify
description: Feature Definer - Táº¡o spec.md tá»« mÃ´ táº£ ngÃ´n ngá»¯ tá»± nhiÃªn.
role: Domain Scribe
---

## ðŸŽ¯ Mission
Chuyá»ƒn mÃ´ táº£ ngÃ´n ngá»¯ tá»± nhiÃªn â†’ spec.md chuáº©n hÃ³a (WHAT, khÃ´ng pháº£i HOW).

## ðŸ“¥ Input
- MÃ´ táº£ feature tá»« developer (text tá»± do)
- `.agent/memory/constitution.md` (constraints)

## ðŸ“‹ Protocol
1. Äá»c mÃ´ táº£ â†’ trÃ­ch xuáº¥t:
   - **Actors**: Ai tÆ°Æ¡ng tÃ¡c? (User, Admin, System, Guest)
   - **Actions**: LÃ m gÃ¬? (CRUD, search, filter, export)
   - **Data**: Dá»¯ liá»‡u gÃ¬? (entities, fields, relationships)
   - **Constraints**: Giá»›i háº¡n gÃ¬? (auth, permissions, limits)
2. Táº¡o `.agent/specs/[feature]/spec.md` vá»›i format Báº®T BUá»˜C:
   ```markdown
   ---
   title: [Feature Name]
   status: DRAFT
   version: 1.0.0
   created: [date]
   ---
   ## 1. Overview
   [1-2 cÃ¢u mÃ´ táº£]

   ## 2. User Scenarios
   - **US1**: As a [actor], I want to [action], so that [value].
   - **US2**: ...

   ## 3. Functional Requirements
   - FR01: [requirement cá»¥ thá»ƒ, measurable]

   ## 4. Non-Functional Requirements
   - NFR01: Response time < 2s

   ## 5. Success Criteria
   - [ ] SC01: [testable criterion]
   ```
3. Má»—i User Scenario PHáº¢I cÃ³: Actor + Action + Value.
4. Má»—i Functional Requirement PHáº¢I measurable (cÃ³ sá»‘ liá»‡u cá»¥ thá»ƒ).

## ðŸ“¤ Output
- File: `.agent/specs/[feature]/spec.md`

## ðŸš« Guard Rails
- KHÃ”NG viáº¿t implementation details (HOW) â€” chá»‰ mÃ´ táº£ WHAT.
- KHÃ”NG dÃ¹ng technical jargon trong User Scenarios (business language).
- KHÃ”NG bá» qua error cases â€” má»—i action pháº£i cÃ³ "khi tháº¥t báº¡i thÃ¬ sao?"

## When to Use
- Khi cÃ³ mÃ´ táº£ feature dáº¡ng ngÃ´n ngá»¯ tá»± nhiÃªn, cáº§n chuyá»ƒn thÃ nh spec.md chuáº©n (WHAT).
- BÆ°á»›c Ä‘áº§u pipeline, trÆ°á»›c `@speckit.clarify` vÃ  `@speckit.plan`.
- **KHÃ”NG dÃ¹ng cho**: thiáº¿t káº¿ ká»¹ thuáº­t/HOW (â†’ `@speckit.plan`), chia task (â†’ `@speckit.tasks`).

## Common Rationalizations
| LÃ½ do bao biá»‡n | Sá»± tháº­t |
|---|---|
| "Viáº¿t luÃ´n cÃ¡ch lÃ m cho rÃµ" | Spec láº«n HOW khÃ³a cá»©ng giáº£i phÃ¡p sá»›m. Chá»‰ mÃ´ táº£ WHAT. |
| "Requirement Ä‘á»‹nh tÃ­nh lÃ  Ä‘á»§" | "Nhanh/nhiá»u" khÃ´ng verify Ä‘Æ°á»£c. FR pháº£i measurable, cÃ³ sá»‘ liá»‡u. |
| "Error case tÃ­nh sau" | Bá» qua tháº¥t báº¡i táº¡o lá»— há»•ng spec. Má»—i action cÃ³ nhÃ¡nh tháº¥t báº¡i. |
| "User chung chung Ä‘Æ°á»£c" | KhÃ´ng rÃµ actor gÃ¢y sai phÃ¢n quyá»n. Äá»‹nh danh rÃµ actor. |

## Red Flags
- Spec chá»©a chi tiáº¿t implementation (tÃªn hÃ m, framework cá»¥ thá»ƒ).
- Functional requirement khÃ´ng Ä‘o Ä‘Æ°á»£c.
- User Scenario thiáº¿u Actor/Action/Value.
- KhÃ´ng cÃ³ error case cho action.

## Verification
- [ ] spec.md cÃ³ Ä‘á»§ Overview, User Scenarios, FR, NFR, Success Criteria.
- [ ] Má»—i User Scenario cÃ³ Actor + Action + Value.
- [ ] Má»—i FR measurable; má»—i action cÃ³ nhÃ¡nh tháº¥t báº¡i.
- [ ] KhÃ´ng chá»©a implementation detail; ngÃ´n ngá»¯ business.
