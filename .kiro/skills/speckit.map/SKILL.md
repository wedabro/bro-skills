---
name: speckit.map
description: Codebase Mapper - Tá»± Ä‘á»™ng phÃ¢n tÃ­ch cáº¥u trÃºc dá»± Ã¡n, váº½ biá»ƒu Ä‘á»“ phá»¥ thuá»™c vÃ  viáº¿t tÃ i liá»‡u kiáº¿n trÃºc.
role: Technical Lead
---

## ðŸŽ¯ Mission
GiÃºp Agent vÃ  User nhanh chÃ³ng hiá»ƒu Ä‘Æ°á»£c toÃ n bá»™ "báº£n Ä‘á»“" cá»§a codebase, Ä‘áº·c biá»‡t lÃ  cÃ¡c dá»± Ã¡n cÅ© (Brownfield) hoáº·c dá»± Ã¡n phá»©c táº¡p.

## ðŸ“‹ Protocol

### Phase 1: Structure Discovery (QuÃ©t cáº¥u trÃºc)
- QuÃ©t toÃ n bá»™ thÆ° má»¥c báº±ng lá»‡nh `tree` hoáº·c `ls -R`.
- XÃ¡c Ä‘á»‹nh cÃ¡c Tech Stack cá»‘t lÃµi (frameworks, databases, libraries).

### Phase 2: Dependency Mapping (SÆ¡ Ä‘á»“ phá»¥ thuá»™c)
- PhÃ¢n tÃ­ch cÃ¡c lá»‡nh `import` hoáº·c `require` Ä‘á»ƒ tÃ¬m sá»± phá»¥ thuá»™c giá»¯a cÃ¡c modules.
- LÆ°u káº¿t quáº£ vÃ o `.agent/codebase/STRUCTURE.md`.

### Phase 3: Integration Inventory (Danh má»¥c tÃ­ch há»£p)
- Liá»‡t kÃª cÃ¡c service bÃªn thá»© 3 (API bÃªn ngoÃ i, DB connection).
- LÆ°u vÃ o `.agent/codebase/INTEGRATIONS.md`.

## ðŸ“¤ Output Artifacts
- `.agent/codebase/ARCHITECTURE.md`: Tá»•ng quan kiáº¿n trÃºc.
- `.agent/codebase/CONVENTIONS.md`: CÃ¡c quy Æ°á»›c code Ä‘ang sá»­ dá»¥ng.

## ðŸš« Guard Rails
- KHÃ”NG Ä‘á»c ná»™i dung táº¥t cáº£ cÃ¡c file cÃ¹ng lÃºc Ä‘á»ƒ trÃ¡nh trÃ n context. Æ¯u tiÃªn Ä‘á»c header vÃ  exports.
- PHáº¢I cáº­p nháº­t láº¡i báº£n Ä‘á»“ sau má»—i Ä‘á»£t refactor lá»›n.

## When to Use
- Khi cáº§n hiá»ƒu nhanh cáº¥u trÃºc codebase (Ä‘áº·c biá»‡t brownfield/dá»± Ã¡n phá»©c táº¡p).
- TrÆ°á»›c khi sá»­a lá»›n hoáº·c onboard tÃ­nh nÄƒng vÃ o codebase láº¡.
- **KHÃ”NG dÃ¹ng cho**: cháº©n Ä‘oÃ¡n lá»—i cá»¥ thá»ƒ (â†’ `@speckit.debug`), thiáº¿t káº¿ feature má»›i (â†’ `@speckit.plan`).

## Common Rationalizations
| LÃ½ do bao biá»‡n | Sá»± tháº­t |
|---|---|
| "Äá»c háº¿t file cho cháº¯c" | Äá»c táº¥t cáº£ trÃ n context. Æ¯u tiÃªn header + exports. |
| "Map 1 láº§n lÃ  Ä‘á»§" | Refactor lá»›n lÃ m map lá»—i thá»i. Cáº­p nháº­t sau má»—i Ä‘á»£t refactor. |
| "Khá»i ghi tÃ i liá»‡u, nhá»› trong Ä‘áº§u" | Context bay sau compaction. LÆ°u artifact ARCHITECTURE/CONVENTIONS. |
| "Bá» qua integration ngoÃ i" | Service bÃªn thá»© 3 lÃ  Ä‘iá»ƒm rá»§i ro. Pháº£i inventory. |

## Red Flags
- Äá»c toÃ n bá»™ file cÃ¹ng lÃºc gÃ¢y trÃ n context.
- KhÃ´ng cáº­p nháº­t map sau refactor lá»›n.
- Thiáº¿u artifact ARCHITECTURE.md/CONVENTIONS.md.
- Bá» sÃ³t integration/service bÃªn ngoÃ i.

## Verification
- [ ] ÄÃ£ quÃ©t structure + xÃ¡c Ä‘á»‹nh tech stack cá»‘t lÃµi.
- [ ] Dependency map giá»¯a modules Ä‘Æ°á»£c ghi láº¡i.
- [ ] Integration bÃªn thá»© 3 Ä‘Æ°á»£c inventory.
- [ ] CÃ³ artifact ARCHITECTURE.md + CONVENTIONS.md.
- [ ] Map cáº­p nháº­t sau refactor lá»›n (náº¿u cÃ³).
