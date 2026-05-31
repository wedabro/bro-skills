---
name: speckit.diff
description: Artifact Comparator - So sÃ¡nh sá»± khÃ¡c biá»‡t giá»¯a cÃ¡c artifacts.
role: Diff Analyst
---

## ðŸŽ¯ Mission
So sÃ¡nh 2 versions cá»§a artifact â†’ highlight thay Ä‘á»•i â†’ Ä‘Ã¡nh giÃ¡ impact.

## ðŸ“¥ Input
- 2 files hoáº·c 2 versions cáº§n so sÃ¡nh (spec, plan, tasks, code)

## ðŸ“‹ Protocol
1. Äá»c cáº£ 2 versions.
2. So sÃ¡nh section-by-section:
   - âž• **Added**: Sections/requirements má»›i
   - âž– **Removed**: Sections/requirements bá»‹ xÃ³a
   - âœï¸ **Changed**: Sections cÃ³ ná»™i dung thay Ä‘á»•i
3. Impact Analysis: Má»—i thay Ä‘á»•i áº£nh hÆ°á»Ÿng artifact nÃ o downstream?
   - VD: ThÃªm field trong spec â†’ cáº§n update plan â†’ cáº§n thÃªm tasks
4. Output báº£ng tÃ³m táº¯t.

## ðŸ“¤ Output
- Console: Diff summary table
- File: `.agent/memory/diff-report.md` (náº¿u cáº§n lÆ°u)

## ðŸš« Guard Rails
- CHá»ˆ so sÃ¡nh vÃ  bÃ¡o cÃ¡o â€” KHÃ”NG tá»± Ã½ sá»­a artifacts.

## When to Use
- Khi so sÃ¡nh 2 version cá»§a artifact (spec/plan/tasks/code) vÃ  Ä‘Ã¡nh giÃ¡ impact downstream.
- **KHÃ”NG dÃ¹ng cho**: kiá»ƒm tra nháº¥t quÃ¡n toÃ n bá»™ (â†’ `@speckit.analyze`), review code (â†’ `@speckit.reviewer`).

## Common Rationalizations
| LÃ½ do bao biá»‡n | Sá»± tháº­t |
|---|---|
| "Liá»‡t kÃª thay Ä‘á»•i lÃ  Ä‘á»§" | Thiáº¿u impact analysis thÃ¬ khÃ´ng biáº¿t pháº£i sá»­a gÃ¬ tiáº¿p. |
| "Sá»­a luÃ´n artifact downstream" | Diff chá»‰ so sÃ¡nh + bÃ¡o cÃ¡o, khÃ´ng tá»± sá»­a. |
| "Bá» qua thay Ä‘á»•i nhá»" | Thay Ä‘á»•i nhá» cÃ³ thá»ƒ lan downstream. Ghi nháº­n Ä‘á»§ Added/Removed/Changed. |

## Red Flags
- Tá»± sá»­a artifact thay vÃ¬ bÃ¡o cÃ¡o.
- Thiáº¿u impact analysis cho thay Ä‘á»•i.
- Bá» sÃ³t Added/Removed/Changed.

## Verification
- [ ] So sÃ¡nh section-by-section: Added/Removed/Changed.
- [ ] Má»—i thay Ä‘á»•i cÃ³ impact analysis downstream.
- [ ] Output diff summary table; chá»‰ bÃ¡o cÃ¡o, khÃ´ng sá»­a.
