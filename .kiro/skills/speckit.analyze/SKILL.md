---
name: speckit.analyze
description: Consistency Checker - PhÃ¢n tÃ­ch tÃ­nh nháº¥t quÃ¡n giá»¯a spec, plan, tasks.
role: Consistency Analyst
---

## ðŸŽ¯ Mission
Äáº£m báº£o spec.md, plan.md, tasks.md khÃ´ng mÃ¢u thuáº«n vÃ  phá»§ háº¿t requirements.

## ðŸ“¥ Input
- `.agent/specs/[feature]/spec.md`
- `.agent/specs/[feature]/plan.md`
- `.agent/specs/[feature]/tasks.md`

## ðŸ“‹ Protocol
1. **Coverage Check**: Má»—i User Scenario trong spec â†’ pháº£i cÃ³ task(s) trong tasks.md.
2. **Conflict Check**: Plan nÃ³i dÃ¹ng tech A nhÆ°ng tasks láº¡i reference tech B â†’ BÃO Lá»–I.
3. **Constitution Check**: So plan.md vá»›i constitution.md â†’ phÃ¡t hiá»‡n violations.
4. **Completeness Check**: Má»—i data model trong plan â†’ pháº£i cÃ³ task táº¡o model + migration.
5. **Output báº£ng Gap Analysis**:
   ```
   | Spec Requirement | Plan Section | Task ID | Status |
   |------------------|-------------|---------|--------|
   | User login       | Auth flow   | T005    | âœ… OK  |
   | Payment          | -           | -       | âŒ GAP |
   ```
6. TÃ­nh Coverage Score: `(matched / total) Ã— 100%`.

## ðŸ“¤ Output
- Console: Gap Analysis table + Coverage Score
- File: `.agent/memory/analyze-report.md`

## ðŸš« Guard Rails
- CHá»ˆ bÃ¡o cÃ¡o â€” KHÃ”NG tá»± Ã½ sá»­a artifacts.
- Má»—i gap pháº£i chá»‰ rÃµ artifact nÃ o thiáº¿u.

## When to Use
- Sau khi cÃ³ spec + plan + tasks, cáº§n kiá»ƒm tra nháº¥t quÃ¡n vÃ  Ä‘á»™ phá»§ requirement.
- TrÆ°á»›c khi `@speckit.implement` báº¯t Ä‘áº§u code.
- **KHÃ”NG dÃ¹ng cho**: validate implementation Ä‘Ã£ code (â†’ `@speckit.validate`), lÃ m rÃµ spec (â†’ `@speckit.clarify`).

## Common Rationalizations
| LÃ½ do bao biá»‡n | Sá»± tháº­t |
|---|---|
| "Spec vá»›i plan cháº¯c khá»›p rá»“i" | Drift Ã¢m tháº§m ráº¥t phá»• biáº¿n. Coverage check tá»«ng scenario. |
| "Tá»± sá»­a gap luÃ´n cho nhanh" | Analyze chá»‰ bÃ¡o cÃ¡o, khÃ´ng sá»­a artifact. Sá»­a thuá»™c agent chá»§. |
| "Gap nhá» bá» qua" | Gap = requirement khÃ´ng Ä‘Æ°á»£c implement. Chá»‰ rÃµ artifact thiáº¿u. |
| "Khá»i check Constitution á»Ÿ bÆ°á»›c nÃ y" | Plan vi pháº¡m Constitution kÃ©o cáº£ pipeline sai. Pháº£i check. |

## Red Flags
- User Scenario khÃ´ng map tá»›i task nÃ o.
- Plan dÃ¹ng tech A nhÆ°ng tasks reference tech B.
- Data model trong plan thiáº¿u task táº¡o model/migration.
- Tá»± sá»­a artifact thay vÃ¬ bÃ¡o cÃ¡o.

## Verification
- [ ] Má»—i User Scenario map tá»›i â‰¥1 task.
- [ ] KhÃ´ng cÃ³ conflict tech giá»¯a plan vÃ  tasks.
- [ ] Má»—i data model cÃ³ task táº¡o + migration.
- [ ] Gap Analysis table + Coverage Score xuáº¥t ra `analyze-report.md`.
- [ ] Chá»‰ bÃ¡o cÃ¡o, khÃ´ng sá»­a artifact.
