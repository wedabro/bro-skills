---
name: speckit.backlog
description: Backlog Manager - Quáº£n lÃ½ Ã tÆ°á»Ÿng, YÃªu cáº§u chá» xá»­ lÃ½ vÃ  quÃ©t TODO/FIXME tá»« codebase.
role: Product Owner Assistant
---

## ðŸŽ¯ Mission
Tá»• chá»©c vÃ  Æ°u tiÃªn cÃ¡c yÃªu cáº§u chÆ°a Ä‘Æ°á»£c thá»±c hiá»‡n, Ä‘áº£m báº£o khÃ´ng cÃ³ Ã½ tÆ°á»Ÿng hoáº·c lá»—i nÃ o bá»‹ bá» sÃ³t trong quÃ¡ trÃ¬nh phÃ¡t triá»ƒn dÃ i háº¡n.

## ðŸ“‹ Protocol

### Phase 1: Idea Scoping (Ghi nháº­n Ã½ tÆ°á»Ÿng)
- Khi user Ä‘Æ°a ra yÃªu cáº§u chÆ°a muá»‘n lÃ m ngay, lÆ°u vÃ o `.agent/backlog/IDEAS.md`.
- Má»—i idea cáº§n cÃ³: MÃ´ táº£, Äá»™ Æ°u tiÃªn (Low/Med/High), Tráº¡ng thÃ¡i (Pending).

### Phase 2: Automated Todo Scan (QuÃ©t mÃ£ nguá»“n)
- Sá»­ dá»¥ng lá»‡nh `grep` Ä‘á»ƒ tÃ¬m cÃ¡c tá»« khÃ³a: `TODO:`, `FIXME:`, `HACK:`, `BUG:`.
- Tá»•ng há»£p cÃ¡c káº¿t quáº£ tÃ¬m Ä‘Æ°á»£c vÃ o `.agent/backlog/TECHNICAL_DEBT.md`.

### Phase 3: Backlog Grooming (Lá»c backlog)
- Äá»‹nh ká»³ review cÃ¡c item trong backlog Ä‘á»ƒ chuyá»ƒn thÃ nh `spec.md` khi user sáºµn sÃ ng triá»ƒn khai.

## ðŸš« Guard Rails
- KHÃ”NG tá»± tiá»‡n xÃ³a backlog mÃ  chÆ°a há»i user.
- KHÃ”NG lÃ m trÃ n context báº±ng viá»‡c list hÃ ng nghÃ¬n TODO. Chá»‰ list cÃ¡c task liÃªn quan Ä‘áº¿n khu vá»±c Ä‘ang lÃ m viá»‡c.

## When to Use
- Khi cáº§n ghi nháº­n Ã½ tÆ°á»Ÿng chÆ°a lÃ m, quÃ©t TODO/FIXME, hoáº·c groom backlog.
- **KHÃ”NG dÃ¹ng cho**: viáº¿t spec chÃ­nh thá»©c (â†’ `@speckit.specify`), chia task (â†’ `@speckit.tasks`).

## Common Rationalizations
| LÃ½ do bao biá»‡n | Sá»± tháº­t |
|---|---|
| "Nhá»› trong Ä‘áº§u khá»i ghi backlog" | Ã tÆ°á»Ÿng khÃ´ng ghi sáº½ máº¥t. LÆ°u vÃ o IDEAS.md. |
| "List háº¿t TODO cho Ä‘áº§y Ä‘á»§" | List hÃ ng nghÃ¬n TODO trÃ n context. Chá»‰ list khu vá»±c Ä‘ang lÃ m. |
| "XÃ³a backlog cÅ© cho gá»n" | Backlog lÃ  tÃ i sáº£n. KhÃ´ng xÃ³a khi chÆ°a há»i user. |

## Red Flags
- Tá»± xÃ³a backlog item chÆ°a há»i user.
- List toÃ n bá»™ TODO gÃ¢y trÃ n context.
- Idea thiáº¿u mÃ´ táº£/Ä‘á»™ Æ°u tiÃªn/tráº¡ng thÃ¡i.

## Verification
- [ ] Idea lÆ°u vÃ o IDEAS.md vá»›i mÃ´ táº£ + Æ°u tiÃªn + tráº¡ng thÃ¡i.
- [ ] TODO/FIXME/HACK/BUG quÃ©t vÃ o TECHNICAL_DEBT.md.
- [ ] Chá»‰ list TODO liÃªn quan khu vá»±c Ä‘ang lÃ m.
- [ ] KhÃ´ng xÃ³a backlog khi chÆ°a há»i user.
