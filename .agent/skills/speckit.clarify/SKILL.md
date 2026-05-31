---
name: speckit.clarify
description: Ambiguity Resolver - PhÃ¡t hiá»‡n vÃ  giáº£i quyáº¿t mÆ¡ há»“ trong spec.
role: Clarity Engineer
---

## ðŸŽ¯ Mission
Scan spec.md â†’ phÃ¡t hiá»‡n chá»— mÆ¡ há»“ â†’ há»i developer tá»‘i Ä‘a 3 cÃ¢u â†’ cáº­p nháº­t spec.

## ðŸ“¥ Input
- `.agent/specs/[feature]/spec.md`

## ðŸ“‹ Protocol
1. Scan spec.md tÃ¬m:
   - **Vague language**: "nhanh", "nhiá»u", "dá»… dÃ¹ng", "tÆ°Æ¡ng tá»±", "v.v."
   - **Missing boundaries**: KhÃ´ng rÃµ min/max, pagination limits, file size limits
   - **Undefined error handling**: Khi X fail thÃ¬ sao?
   - **Ambiguous actors**: "User" lÃ  ai? Admin? Guest? Registered?
2. PhÃ¢n loáº¡i má»—i issue:
   - ðŸ”´ **CRITICAL**: áº¢nh hÆ°á»Ÿng kiáº¿n trÃºc, PHáº¢I há»i developer
   - ðŸŸ¡ **IMPORTANT**: NÃªn há»i nhÆ°ng cÃ³ thá»ƒ Ä‘á» xuáº¥t máº·c Ä‘á»‹nh
   - ðŸŸ¢ **MINOR**: Tá»± fix Ä‘Æ°á»£c (VD: thÃªm "tá»‘i Ä‘a 50 items" náº¿u thiáº¿u)
3. Há»i developer Tá»I ÄA 3 cÃ¢u CRITICAL, má»—i cÃ¢u cÃ³ báº£ng options:
   ```
   | Option | MÃ´ táº£ | Impact |
   |--------|-------|--------|
   | A      | ...   | ...    |
   | B      | ...   | ...    |
   | C      | ...   | ...    |
   ```
4. Auto-fix cÃ¡c items ðŸŸ¢ MINOR.
5. Cáº­p nháº­t spec.md vá»›i clarifications â†’ Ä‘Ã¡nh dáº¥u `[CLARIFIED]`.

## ðŸ“¤ Output
- File: Updated `.agent/specs/[feature]/spec.md`

## ðŸš« Guard Rails
- Tá»I ÄA 3 cÃ¢u há»i â€” khÃ´ng há»i quÃ¡ nhiá»u.
- KHÃ”NG thay Ä‘á»•i intent gá»‘c cá»§a spec.

## When to Use
- Sau `@speckit.specify`, khi spec cÃ²n chá»— mÆ¡ há»“ cáº§n lÃ m rÃµ trÆ°á»›c khi plan.
- **KHÃ”NG dÃ¹ng cho**: táº¡o spec má»›i (â†’ `@speckit.specify`), kiá»ƒm tra nháº¥t quÃ¡n spec/plan/tasks (â†’ `@speckit.analyze`).

## Common Rationalizations
| LÃ½ do bao biá»‡n | Sá»± tháº­t |
|---|---|
| "Há»i háº¿t cho cháº¯c" | Há»i quÃ¡ nhiá»u lÃ m náº£n developer. Tá»‘i Ä‘a 3 cÃ¢u CRITICAL. |
| "Tá»± Ä‘oÃ¡n intent cho nhanh" | ÄoÃ¡n sai intent phÃ¡ cáº£ plan. Item CRITICAL pháº£i há»i. |
| "MÆ¡ há»“ nhá» ká»‡ nÃ³" | Vague language gÃ¢y hiá»ƒu lá»‡ch khi implement. Auto-fix MINOR, Ä‘Ã¡nh dáº¥u rÃµ. |
| "Sá»­a luÃ´n cáº£ intent gá»‘c" | Clarify khÃ´ng Ä‘Æ°á»£c Ä‘á»•i Ã½ Ä‘á»‹nh gá»‘c cá»§a spec. Chá»‰ lÃ m rÃµ. |

## Red Flags
- Há»i developer >3 cÃ¢u.
- Thay Ä‘á»•i intent gá»‘c cá»§a spec.
- Bá» qua vague language ("nhanh", "nhiá»u", "dá»… dÃ¹ng").
- Item CRITICAL bá»‹ tá»± Ä‘oÃ¡n thay vÃ¬ há»i.

## Verification
- [ ] ÄÃ£ scan vague language, missing boundaries, undefined error, ambiguous actors.
- [ ] Má»—i issue phÃ¢n loáº¡i CRITICAL/IMPORTANT/MINOR.
- [ ] Há»i â‰¤3 cÃ¢u CRITICAL, má»—i cÃ¢u cÃ³ báº£ng options.
- [ ] MINOR Ä‘Æ°á»£c auto-fix; spec cáº­p nháº­t, Ä‘Ã¡nh dáº¥u `[CLARIFIED]`.
- [ ] Intent gá»‘c giá»¯ nguyÃªn.
