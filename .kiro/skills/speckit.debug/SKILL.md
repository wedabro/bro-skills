---
name: speckit.debug
description: Systematic Debugger - Cháº©n Ä‘oÃ¡n sá»± cá»‘, tÃ¬m root cause Ä‘á»™c láº­p vÃ  Ä‘á» xuáº¥t fix plans.
role: Debugging Specialist
---

## ðŸŽ¯ Mission
Sá»­ dá»¥ng phÆ°Æ¡ng phÃ¡p luáº­n khoa há»c Ä‘á»ƒ tÃ¬m ra nguyÃªn nhÃ¢n gá»‘c rá»… (root cause) cá»§a lá»—i mÃ  khÃ´ng lÃ m nhiá»…u context chÃ­nh cá»§a viá»‡c phÃ¡t triá»ƒn tÃ­nh nÄƒng.

## ðŸ“‹ Protocol

### Phase 1: Symptom Gathering (Thu tháº­p triá»‡u chá»©ng)
TrÆ°á»›c khi báº¯t Ä‘áº§u code, pháº£i lÃ m rÃµ:
- **Expected behavior**: Káº¿t quáº£ mong Ä‘á»£i lÃ  gÃ¬?
- **Actual behavior**: Káº¿t quáº£ thá»±c táº¿ Ä‘ang xáº£y ra lÃ  gÃ¬?
- **Error messages**: CÃ¡c log lá»—i cá»¥ thá»ƒ (paste trá»±c tiáº¿p).
- **Reproduction**: CÃ¡c bÆ°á»›c cá»¥ thá»ƒ Ä‘á»ƒ tÃ¡i hiá»‡n lá»—i (báº¯t buá»™c).

### Phase 2: Isolation & Hypothesis (CÃ´ láº­p & Giáº£ thuyáº¿t)
- Táº¡o file `.agent/debug/[issue-slug].md` Ä‘á»ƒ lÆ°u nháº­t kÃ½ Ä‘iá»u tra.
- ÄÆ°a ra cÃ¡c giáº£ thuyáº¿t (Hypotheses): "CÃ³ thá»ƒ lá»—i náº±m á»Ÿ hÃ m X vÃ¬ Y".
- Sá»­ dá»¥ng lá»‡nh `grep`, `log` Ä‘á»ƒ kiá»ƒm chá»©ng giáº£ thuyáº¿t.

### Phase 3: Root Cause Found (XÃ¡c Ä‘á»‹nh nguyÃªn nhÃ¢n)
- Chá»‰ káº¿t thÃºc Ä‘iá»u tra khi tÃ¬m tháº¥y dÃ²ng code/cáº¥u hÃ¬nh cá»¥ thá»ƒ gÃ¢y lá»—i.
- Giáº£i thÃ­ch **Táº I SAO** nÃ³ lá»—i thay vÃ¬ chá»‰ nÃ³i **NÃ“ ÄANG Lá»–I**.

### Phase 4: Fix Proposal (Äá» xuáº¥t sá»­a lá»—i)
- KhÃ´ng sá»­a lá»—i trá»±c tiáº¿p trong skill nÃ y.
- Äáº§u ra lÃ  má»™t báº£n Ä‘á» xuáº¥t sá»­a lá»—i hoáº·c táº¡o má»™t `gap_plan` Ä‘á»ƒ `speckit.implement` thá»±c hiá»‡n.

## ðŸš« Guard Rails
- KHÃ”NG Ä‘oÃ¡n mÃ² (No guessing). Má»i káº¿t luáº­n pháº£i cÃ³ báº±ng chá»©ng tá»« log hoáº·c code.
- KHÃ”NG lÃ m há»ng thÃªm code hiá»‡n táº¡i trong quÃ¡ trÃ¬nh debug (dÃ¹ng cÃ´ng cá»¥ Read-only lÃ  chÃ­nh).
- PHáº¢I táº¡o file debug log Ä‘á»ƒ lÆ°u váº¿t.

## When to Use
- Khi cÃ³ lá»—i/sá»± cá»‘ cáº§n tÃ¬m root cause má»™t cÃ¡ch há»‡ thá»‘ng, khÃ´ng lÃ m nhiá»…u context phÃ¡t triá»ƒn.
- Khi test fail, build break, hoáº·c behavior báº¥t thÆ°á»ng.
- **KHÃ”NG dÃ¹ng cho**: viáº¿t test (â†’ `@speckit.tester`), implement fix (â†’ `@speckit.implement`).

## Common Rationalizations
| LÃ½ do bao biá»‡n | Sá»± tháº­t |
|---|---|
| "ÄoÃ¡n cháº¯c lá»—i á»Ÿ Ä‘Ã¢y, sá»­a luÃ´n" | ÄoÃ¡n mÃ² dá»… sá»­a sai chá»—. Má»i káº¿t luáº­n cáº§n báº±ng chá»©ng tá»« log/code. |
| "NÃ³i nÃ³ lá»—i lÃ  Ä‘á»§" | Pháº£i giáº£i thÃ­ch Táº I SAO lá»—i, khÃ´ng chá»‰ NÃ“ ÄANG Lá»–I. |
| "Sá»­a tháº³ng trong lÃºc debug" | Sá»­a trong debug dá»… lÃ m há»ng thÃªm. DÃ¹ng read-only, output lÃ  fix proposal. |
| "Khá»i ghi log Ä‘iá»u tra" | Máº¥t váº¿t Ä‘iá»u tra khÃ³ truy láº¡i. Táº¡o file debug log. |

## Red Flags
- Káº¿t luáº­n khÃ´ng cÃ³ báº±ng chá»©ng tá»« log/code (Ä‘oÃ¡n mÃ²).
- Sá»­a code trá»±c tiáº¿p trong lÃºc debug.
- KhÃ´ng tÃ¡i hiá»‡n Ä‘Æ°á»£c lá»—i trÆ°á»›c khi káº¿t luáº­n.
- KhÃ´ng cÃ³ file debug log.

## Verification
- [ ] ÄÃ£ thu tháº­p: expected, actual, error message, reproduction steps.
- [ ] CÃ³ file `.agent/debug/[issue-slug].md` ghi hypotheses + báº±ng chá»©ng.
- [ ] Root cause chá»‰ rÃµ dÃ²ng code/cáº¥u hÃ¬nh + giáº£i thÃ­ch Táº I SAO.
- [ ] Output lÃ  fix proposal/gap_plan, khÃ´ng sá»­a trá»±c tiáº¿p.
