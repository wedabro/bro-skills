---
name: speckit.checklist
description: Requirements Validator - Táº¡o vÃ  validate checklist tá»« spec.
role: Requirements Auditor
---

## ðŸŽ¯ Mission
TrÃ­ch xuáº¥t má»i functional requirement tá»« spec.md thÃ nh checklist cÃ³ thá»ƒ track Ä‘Æ°á»£c.

## ðŸ“¥ Input
- `.agent/specs/[feature]/spec.md`
- `.agent/specs/[feature]/tasks.md` (náº¿u cÃ³)

## ðŸ“‹ Protocol
1. Äá»c spec.md â†’ trÃ­ch xuáº¥t má»i yÃªu cáº§u (tá»« User Scenarios + Success Criteria).
2. Táº¡o checklist format:
   ```markdown
   ## Functional Requirements
   - [ ] FR01: User cÃ³ thá»ƒ Ä‘Äƒng kÃ½ tÃ i khoáº£n â†’ T003, T004
   - [ ] FR02: User cÃ³ thá»ƒ Ä‘Äƒng nháº­p â†’ T005
   - [x] FR03: User cÃ³ thá»ƒ xem sáº£n pháº©m â†’ T010 âœ…
   ```
3. Náº¿u cÃ³ tasks.md â†’ link má»—i requirement Ä‘áº¿n task IDs.
4. ÄÃ¡nh status: âœ… Met / âŒ Not Met / âš ï¸ Partial.

## ðŸ“¤ Output
- File: `.agent/specs/[feature]/checklist.md`

## ðŸš« Guard Rails
- Má»—i requirement PHáº¢I trÃ­ch dáº«n Ä‘Æ°á»£c tá»« spec.md (khÃ´ng tá»± bá»‹a thÃªm).

## When to Use
- Khi cáº§n trÃ­ch requirement tá»« spec thÃ nh checklist track Ä‘Æ°á»£c, link tá»›i task.
- **KHÃ”NG dÃ¹ng cho**: kiá»ƒm tra nháº¥t quÃ¡n artifact (â†’ `@speckit.analyze`), validate runtime (â†’ `@speckit.validate`).

## Common Rationalizations
| LÃ½ do bao biá»‡n | Sá»± tháº­t |
|---|---|
| "ThÃªm requirement cho Ä‘áº§y Ä‘á»§" | Checklist pháº£i trÃ­ch tá»« spec, khÃ´ng tá»± bá»‹a. |
| "Khá»i link task cho nhanh" | KhÃ´ng link task thÃ¬ khÃ´ng track Ä‘Æ°á»£c tiáº¿n Ä‘á»™. Link task ID. |
| "ÄÃ¡nh Met cho xong" | Status pháº£i pháº£n Ã¡nh thá»±c táº¿: Met/Not Met/Partial. |

## Red Flags
- Requirement khÃ´ng trÃ­ch dáº«n Ä‘Æ°á»£c tá»« spec.md.
- Checklist item thiáº¿u link task ID (khi cÃ³ tasks.md).
- Status Ä‘Ã¡nh dáº¥u khÃ´ng Ä‘Ãºng thá»±c táº¿.

## Verification
- [ ] Má»i requirement trÃ­ch tá»« User Scenarios + Success Criteria.
- [ ] Má»—i item link tá»›i task ID (náº¿u cÃ³ tasks.md).
- [ ] Status Ä‘Ã¡nh Ä‘Ãºng: Met/Not Met/Partial.
- [ ] `checklist.md` khÃ´ng chá»©a requirement tá»± bá»‹a.
