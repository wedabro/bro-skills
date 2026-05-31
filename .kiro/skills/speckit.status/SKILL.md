---
name: speckit.status
description: Progress Dashboard - Hiá»ƒn thá»‹ tráº¡ng thÃ¡i tiáº¿n Ä‘á»™ project.
role: Progress Tracker
---

## ðŸŽ¯ Mission
Parse tasks.md â†’ tÃ­nh tiáº¿n Ä‘á»™ â†’ hiá»ƒn thá»‹ dashboard trá»±c quan.

## ðŸ“¥ Input
- `.agent/specs/[feature]/tasks.md`

## ðŸ“‹ Protocol
1. Parse tasks.md â†’ Ä‘áº¿m checkboxes:
   - `- [X]` = completed
   - `- [ ]` = pending
2. NhÃ³m theo Phase â†’ tÃ­nh % má»—i phase.
3. Output dashboard:
   ```
   ðŸ“Š Progress Dashboard: [Feature Name]
   â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
   Phase 1: Setup        â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ 100% (4/4)
   Phase 2: Foundation   â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘  50% (3/6)
   Phase 3: User Auth    â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘   0% (0/5)
   â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
   Total:                â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘  47% (7/15)
   ```
4. List tasks Ä‘ang pending (tiáº¿p theo cáº§n lÃ m).

## ðŸ“¤ Output
- Console: Dashboard visualization

## ðŸš« Guard Rails
- KHÃ”NG thay Ä‘á»•i tasks.md â€” chá»‰ Ä‘á»c vÃ  bÃ¡o cÃ¡o.

## When to Use
- Khi cáº§n dashboard tiáº¿n Ä‘á»™ tá»« tasks.md (% theo phase, task pending káº¿ tiáº¿p).
- **KHÃ”NG dÃ¹ng cho**: lá»™ trÃ¬nh cáº¥p cao (â†’ `@speckit.roadmap`), validate hoÃ n thÃ nh (â†’ `@speckit.validate`).

## Common Rationalizations
| LÃ½ do bao biá»‡n | Sá»± tháº­t |
|---|---|
| "Tick luÃ´n task gáº§n xong cho Ä‘áº¹p sá»‘" | Status chá»‰ Ä‘á»c, khÃ´ng sá»­a tasks.md. Pháº£n Ã¡nh Ä‘Ãºng checkbox thá»±c táº¿. |
| "BÃ¡o % tá»•ng lÃ  Ä‘á»§" | Thiáº¿u breakdown theo phase khÃ³ tháº¥y bottleneck. TÃ­nh % má»—i phase. |

## Red Flags
- Thay Ä‘á»•i tasks.md thay vÃ¬ chá»‰ Ä‘á»c.
- Chá»‰ bÃ¡o % tá»•ng, khÃ´ng breakdown theo phase.
- KhÃ´ng list task pending káº¿ tiáº¿p.

## Verification
- [ ] Parse Ä‘Ãºng `[X]`/`[ ]` tá»« tasks.md.
- [ ] TÃ­nh % má»—i phase + tá»•ng.
- [ ] List task pending káº¿ tiáº¿p.
- [ ] KhÃ´ng chá»‰nh sá»­a tasks.md.
