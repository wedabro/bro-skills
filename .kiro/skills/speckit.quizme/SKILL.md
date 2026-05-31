---
name: speckit.quizme
description: Logic Challenger (Red Team) - Äáº·t cÃ¢u há»i pháº£n biá»‡n, tÃ¬m edge cases.
role: Red Team Analyst
---

## ðŸŽ¯ Mission
Challenge spec + plan báº±ng cÃ¢u há»i edge-case, tÃ¬m lá»— há»•ng logic trÆ°á»›c khi implement.

## ðŸ“¥ Input
- `.agent/specs/[feature]/spec.md`
- `.agent/specs/[feature]/plan.md`

## ðŸ“‹ Protocol
1. Äá»c spec + plan â†’ tÃ¬m assumptions áº©n (implicit assumptions).
2. Sinh Tá»I ÄA 5 cÃ¢u há»i edge-case, má»—i cÃ¢u thuá»™c 1 category:
   - **Boundary**: "Náº¿u user nháº­p 0 sáº£n pháº©m thÃ¬ sao?"
   - **Concurrency**: "Náº¿u 2 ngÆ°á»i cÃ¹ng mua sáº£n pháº©m cuá»‘i cÃ¹ng?"
   - **Failure**: "Náº¿u payment gateway timeout?"
   - **Security**: "Náº¿u user sá»­a price trong request?"
   - **Scale**: "Náº¿u cÃ³ 100K products, performance ra sao?"
3. Vá»›i má»—i cÃ¢u há»i â†’ Ä‘á» xuáº¥t giáº£i phÃ¡p náº¿u developer confirm Ä‘Ã³ lÃ  váº¥n Ä‘á».
4. Interactive: Chá» developer tráº£ lá»i â†’ quyáº¿t Ä‘á»‹nh cáº§n update spec khÃ´ng.

## ðŸ“¤ Output
- Console: Interactive Q&A session
- File: `.agent/memory/quizme-findings.md` (náº¿u phÃ¡t hiá»‡n issues)

## ðŸš« Guard Rails
- Tá»I ÄA 5 cÃ¢u há»i â€” khÃ´ng overwhelm developer.
- CÃ¢u há»i pháº£i THá»°C Táº¾, khÃ´ng há»i edge case quÃ¡ xa vá»i.

## When to Use
- Khi cáº§n challenge spec/plan báº±ng cÃ¢u há»i edge-case trÆ°á»›c khi implement (red team).
- **KHÃ”NG dÃ¹ng cho**: lÃ m rÃµ mÆ¡ há»“ thÆ°á»ng (â†’ `@speckit.clarify`), debug lá»—i runtime (â†’ `@speckit.debug`).

## Common Rationalizations
| LÃ½ do bao biá»‡n | Sá»± tháº­t |
|---|---|
| "Spec rÃµ rá»“i, khá»i challenge" | Assumption áº©n lÃ  nguá»“n bug lá»›n nháº¥t. LuÃ´n red-team trÆ°á»›c implement. |
| "Há»i tháº­t nhiá»u cho ká»¹" | QuÃ¡ nhiá»u cÃ¢u lÃ m náº£n. Tá»‘i Ä‘a 5 cÃ¢u thá»±c táº¿. |
| "Edge case láº¡ cÅ©ng há»i cho cháº¯c" | Edge xa vá»i gÃ¢y nhiá»…u. Chá»‰ há»i case thá»±c táº¿. |

## Red Flags
- Bá» qua viá»‡c tÃ¬m implicit assumptions.
- Há»i >5 cÃ¢u hoáº·c cÃ¢u há»i xa rá»i thá»±c táº¿.
- KhÃ´ng Ä‘á» xuáº¥t giáº£i phÃ¡p cho má»—i váº¥n Ä‘á» tÃ¬m ra.

## Verification
- [ ] ÄÃ£ tÃ¬m implicit assumptions trong spec/plan.
- [ ] Sinh â‰¤5 cÃ¢u edge-case theo category (boundary/concurrency/failure/security/scale).
- [ ] Má»—i cÃ¢u kÃ¨m Ä‘á» xuáº¥t giáº£i phÃ¡p.
- [ ] Findings ghi vÃ o `quizme-findings.md` (náº¿u cÃ³ issue).
