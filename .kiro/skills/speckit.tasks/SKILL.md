---
name: speckit.tasks
description: Task Breaker - Táº¡o tasks.md atomic, cÃ³ thá»© tá»± dependency tá»« plan.
role: Execution Strategist
---

## ðŸŽ¯ Mission
Chuyá»ƒn plan.md thÃ nh danh sÃ¡ch tasks atomic, cÃ³ thá»© tá»± dependency, má»—i task â‰¤15 phÃºt.

## ðŸ“¥ Input
- `.agent/specs/[feature]/plan.md`
- `.agent/specs/[feature]/spec.md`

## ðŸ“‹ Protocol
1. Äá»c plan.md â†’ breakdown má»—i component thÃ nh atomic tasks.
2. Format giáº£i pháº«u Báº®T BUá»˜C cho má»—i task (4 thÃ nh pháº§n):
   ```markdown
   - [ ] T001 [P] TiÃªu Ä‘á» task
     - Files: ÄÆ°á»ng dáº«n cÃ¡c file bá»‹ áº£nh hÆ°á»Ÿng
     - Action: Lá»‡nh thá»±c thi chi tiáº¿t, rÃµ rÃ ng (cáº¥m mÆ¡ há»“)
     - Verify: Lá»‡nh kiá»ƒm chá»©ng Tá»° Äá»˜NG (báº¯t buá»™c, vÃ­ dá»¥: `npm test`, `curl`)
     - Done: TiÃªu chÃ­ nghiá»‡m thu cá»¥ thá»ƒ
   ```
   - `[P]`: Priority (blocking task)
   - `[US1]`: Link Ä‘áº¿n User Scenario
3. Phase Structure Báº®T BUá»˜C:
   - **Phase 1: Setup** â€” Project init, configs, boilerplate
   - **Phase 2: Foundation** â€” DB, auth, shared utilities (blocking)
   - **Phase 3+**: Má»—i User Story = 1 phase (theo priority tá»« spec)
   - **Final Phase: Polish** â€” Error handling, optimization, cleanup
4. Dependency Rules:
   - Task phá»¥ thuá»™c task khÃ¡c â†’ pháº£i Ä‘áº·t SAU.
   - Foundation tasks luÃ´n á»Ÿ Phase 2.
5. **15-Minute Rule**: Má»—i task â‰¤ 15 phÃºt, áº£nh hÆ°á»Ÿng â‰¤ 3 files.

## ðŸ“¤ Output
- File: `.agent/specs/[feature]/tasks.md`

## ðŸš« Guard Rails
- KHÃ”NG táº¡o task quÃ¡ lá»›n (>3 files hoáº·c >15 phÃºt).
- KHÃ”NG táº¡o task trÃ¹ng láº·p.
- Má»—i task PHáº¢I cÃ³ file path cá»¥ thá»ƒ.

## When to Use
- Sau khi cÃ³ `plan.md`, cáº§n breakdown thÃ nh tasks atomic cÃ³ thá»© tá»± dependency.
- **KHÃ”NG dÃ¹ng cho**: thiáº¿t káº¿ kiáº¿n trÃºc (â†’ `@speckit.plan`), thá»±c thi task (â†’ `@speckit.implement`).

## Common Rationalizations
| LÃ½ do bao biá»‡n | Sá»± tháº­t |
|---|---|
| "Gá»™p nhiá»u viá»‡c vÃ o 1 task cho gá»n" | Task lá»›n khÃ³ verify + rollback. Giá»¯ â‰¤15 phÃºt, â‰¤3 files. |
| "Verify Ä‘á»ƒ khi implement tÃ­nh" | Task khÃ´ng cÃ³ lá»‡nh verify thÃ¬ khÃ´ng biáº¿t khi nÃ o xong. Má»—i task cÃ³ Verify tá»± Ä‘á»™ng. |
| "Thá»© tá»± task khÃ´ng quan trá»ng" | Sai thá»© tá»± dependency gÃ¢y block. Foundation á»Ÿ Phase 2, task phá»¥ thuá»™c Ä‘áº·t sau. |
| "File path ghi chung chung" | Task thiáº¿u path cá»¥ thá»ƒ dá»… lÃ m sai chá»—. LuÃ´n ghi Ä‘Æ°á»ng dáº«n rÃµ. |

## Red Flags
- Task >3 files hoáº·c >15 phÃºt.
- Task thiáº¿u 1 trong 4 pháº§n: Files / Action / Verify / Done.
- Task khÃ´ng cÃ³ file path cá»¥ thá»ƒ; Action mÆ¡ há»“.
- Task phá»¥ thuá»™c Ä‘áº·t trÆ°á»›c task nÃ³ cáº§n.

## Verification
- [ ] Má»i task â‰¤15 phÃºt, áº£nh hÆ°á»Ÿng â‰¤3 files.
- [ ] Má»—i task Ä‘á»§ 4 pháº§n (Files/Action/Verify/Done) vá»›i Verify lÃ  lá»‡nh tá»± Ä‘á»™ng.
- [ ] Phase structure Ä‘Ãºng: Setup â†’ Foundation â†’ má»—i User Story 1 phase â†’ Polish.
- [ ] Dependency há»£p lá»‡: task phá»¥ thuá»™c Ä‘áº·t sau; khÃ´ng trÃ¹ng láº·p.
- [ ] `tasks.md` link task â†” User Scenario.
