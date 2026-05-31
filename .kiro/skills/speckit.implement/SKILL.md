---
name: speckit.implement
description: Code Builder (Anti-Regression) - Triá»ƒn khai code theo tasks vá»›i IRONCLAD protocols.
role: Master Builder
---

## ðŸŽ¯ Mission
Implement code theo tasks.md, tuÃ¢n thá»§ 5 IRONCLAD Protocols, zero regression.

## ðŸ“¥ Input
- `.agent/specs/[feature]/tasks.md` (danh sÃ¡ch tasks)
- `.agent/specs/[feature]/plan.md` (kiáº¿n trÃºc)
- `.agent/memory/constitution.md` (rules)

## ðŸ“‹ Protocol â€” Cho Má»–I task chÆ°a complete:

### Protocol 1: Blast Radius Analysis
- List Táº¤T Cáº¢ files bá»‹ áº£nh hÆ°á»Ÿng bá»Ÿi task.
- Rate: ðŸŸ¢ LOW (1-2 files) / ðŸŸ¡ MED (3 files) / ðŸ”´ HIGH (>3 files)
- Náº¿u HIGH â†’ BÃO developer trÆ°á»›c khi code.

### Protocol 2: Strategy Selection
- ðŸŸ¢ LOW risk â†’ Sá»­a trá»±c tiáº¿p (inline edit)
- ðŸ”´ HIGH risk â†’ **Strangler Pattern**: Táº¡o file má»›i â†’ migrate â†’ xÃ³a file cÅ©

### Protocol 3: TDD (Reproduction First)
- Táº¡o script `repro_task_[ID].sh` chá»©ng minh bug/feature TRÆ¯á»šC khi code.
- Cháº¡y â†’ pháº£i FAIL â†’ Implement fix â†’ Cháº¡y láº¡i â†’ pháº£i PASS.

### Protocol 4: Context Anchoring
- Má»—i 3 tasks â†’ re-read `constitution.md` + project structure.
- Äáº£m báº£o khÃ´ng drift khá»i architecture.

### Protocol 5: Post-Implementation Build Gate â­
**SAU Má»–I TASK**, cháº¡y kiá»ƒm tra compile:
1. **TypeScript Check**:
   ```bash
   docker compose exec <service> npx tsc --noEmit
   # Hoáº·c:
   docker compose build 2>&1 | tail -n 50
   ```
2. **Interface Contract Check**:
   - Náº¿u task THÃŠM/Sá»¬A props vÃ o component â†’ grep Táº¤T Cáº¢ nÆ¡i gá»i component Ä‘Ã³.
   - Náº¿u task THÃŠM/Sá»¬A type interface â†’ grep Táº¤T Cáº¢ nÆ¡i dÃ¹ng type Ä‘Ã³.
   ```bash
   grep -rn "ComponentName" apps/*/src/ --include="*.tsx"
   ```
3. **Dockerfile Path Check** (náº¿u task liÃªn quan):
   - Náº¿u task táº¡o/xÃ³a/di chuyá»ƒn file â†’ verify Dockerfile COPY paths váº«n há»£p lá»‡.
   - Náº¿u task Ä‘á»•i `output` config (standalone, etc.) â†’ verify runner CMD path.

Náº¿u build gate FAIL â†’ fix ngay TRÆ¯á»šC KHI chuyá»ƒn task tiáº¿p theo.

### Protocol 5.5: Commit Gate â­ (Báº®T BUá»˜C)
**SAU KHI build gate PASS cho Má»–I task**, Báº®T BUá»˜C commit ngay:
1. Stage cÃ¡c file cá»§a task (chá»‰ file liÃªn quan, KHÃ”NG `git add .` bá»«a bÃ£i):
   ```bash
   git add <file1> <file2>
   ```
2. Commit theo format chuáº©n (imperative, tiáº¿ng Anh):
   ```bash
   git commit -m "feat(T001): [description]"
   ```
3. Má»—i task = 1 atomic commit (1 task chá»‰ giáº£i quyáº¿t 1 váº¥n Ä‘á»).

Quy táº¯c:
- KHÃ”NG chuyá»ƒn task tiáº¿p theo náº¿u task hiá»‡n táº¡i chÆ°a Ä‘Æ°á»£c commit.
- KHÃ”NG gá»™p nhiá»u task vÃ o 1 commit.
- Type theo loáº¡i thay Ä‘á»•i: `feat` / `fix` / `refactor` / `chore` / `test` / `docs`.
- Breaking change â†’ thÃªm `!` sau scope hoáº·c `BREAKING CHANGE:` á»Ÿ footer.

### Protocol 6: Deviation Rules (Xá»­ lÃ½ sai lá»‡ch)
Náº¾U phÃ¡t hiá»‡n lá»—i phÃ¡t sinh ngoÃ i plan trong quÃ¡ trÃ¬nh code, tá»± Ä‘á»™ng xá»­ lÃ½:
- **Rule 1 (Auto-fix bugs):** Tá»± sá»­a lá»—i logic, cÃº phÃ¡p do task gÃ¢y ra.
- **Rule 2 (Auto-add missing):** Tá»± thÃªm error handling, validation náº¿u bá»‹ thiáº¿u.
- **Rule 3 (Auto-fix blockers):** Tá»± cÃ i thÆ° viá»‡n thiáº¿u, sá»­a lá»—i import.
- **Rule 4 (Ask human):** Dá»ªNG vÃ  há»i user náº¿u thay Ä‘á»•i Kiáº¿n trÃºc (thÃªm/Ä‘á»•i DB, Framework, core architecture).

### Completion (Self-Check Protocol)
- Báº¯t buá»™c cháº¡y kiá»ƒm tra file Ä‘Ã£ tá»“n táº¡i vÃ  lá»‡nh `Verify` pass 100%.
- ÄÃ¡nh `- [X] T001 ...` trong tasks.md khi task pass **VÃ€ build gate pass VÃ€ Ä‘Ã£ commit**.
- Commit message format: `feat(T001): [description]`
- **Commit lÃ  Báº®T BUá»˜C** â€” task chÆ°a commit = task chÆ°a hoÃ n thÃ nh.

## ðŸ“¤ Output
- Code files (theo plan.md paths)
- Updated `tasks.md` (checkboxes)

## ðŸš« Guard Rails
- KHÃ”NG import thÆ° viá»‡n khÃ´ng cÃ³ trong `package.json` / `pyproject.toml`.
- KHÃ”NG sá»­a quÃ¡ 3 files trong 1 task mÃ  khÃ´ng há»i.
- KHÃ”NG bá» qua TDD step â€” pháº£i cÃ³ repro script.
- KHÃ”NG hard-code URLs, tokens, keys, default text.
- KHÃ”NG tick task [X] náº¿u chÆ°a qua build gate. â­
- KHÃ”NG tick task [X] náº¿u chÆ°a commit. â­

## When to Use
- Khi thá»±c thi cÃ¡c task trong `tasks.md` thÃ nh code, theo IRONCLAD protocols.
- **KHÃ”NG dÃ¹ng cho**: chia task (â†’ `@speckit.tasks`), viáº¿t test riÃªng (â†’ `@speckit.tester`), review (â†’ `@speckit.reviewer`).

## Common Rationalizations
| LÃ½ do bao biá»‡n | Sá»± tháº­t |
|---|---|
| "Build gate sau cá»¥m task cháº¡y 1 láº§n" | Lá»—i gá»™p láº¡i khÃ³ truy nguá»“n. Build gate sau Má»–I task. |
| "Commit gá»™p cuá»‘i cho gá»n" | Máº¥t tÃ­nh atomic + khÃ³ revert. Má»—i task = 1 commit. |
| "Bá» repro script, fix tháº³ng cho nhanh" | KhÃ´ng repro thÃ¬ khÃ´ng chá»©ng minh Ä‘Ã£ fix. TDD reproduction first. |
| "Äá»•i DB/framework luÃ´n cho tiá»‡n" | Thay Ä‘á»•i kiáº¿n trÃºc cáº§n human approve (Rule 4). Dá»«ng vÃ  há»i. |
| "Import lib nÃ y tiá»‡n, thÃªm vÃ o" | Lib ngoÃ i manifest = rá»§i ro/hallucination. Chá»‰ dÃ¹ng lib cÃ³ trong package.json/pyproject. |

## Red Flags
- Tick task `[X]` khi chÆ°a qua build gate hoáº·c chÆ°a commit.
- Sá»­a >3 files trong 1 task mÃ  khÃ´ng há»i.
- KhÃ´ng cÃ³ repro script trÆ°á»›c khi fix.
- Hard-code URL/token/key/default text.
- Import thÆ° viá»‡n khÃ´ng cÃ³ trong manifest.

## Verification
- [ ] Má»—i task qua build gate (tsc/build pass) trÆ°á»›c khi chuyá»ƒn task káº¿.
- [ ] Má»—i task = 1 atomic commit (Conventional Commits, tiáº¿ng Anh).
- [ ] CÃ³ repro script FAILâ†’PASS cho bug/feature.
- [ ] Lá»‡nh `Verify` cá»§a task pass 100%; checkbox `[X]` cáº­p nháº­t trong tasks.md.
- [ ] KhÃ´ng hard-code secret; khÃ´ng import lib ngoÃ i manifest.
- [ ] Thay Ä‘á»•i kiáº¿n trÃºc (náº¿u cÃ³) Ä‘Ã£ Ä‘Æ°á»£c human approve.
