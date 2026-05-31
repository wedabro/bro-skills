---
name: speckit.validate
description: Implementation Validator - Validate implementation vs spec tá»•ng thá»ƒ.
role: Validation Oracle
---

## ðŸŽ¯ Mission
Kiá»ƒm tra TOÃ€N Bá»˜ implementation cÃ³ Ä‘Ã¡p á»©ng spec.md hay khÃ´ng â€” final gate trÆ°á»›c deploy.

## ðŸ“¥ Input
- Táº¥t cáº£ artifacts: spec.md, plan.md, tasks.md
- Source code (implementation)
- `.agent/memory/constitution.md`

## ðŸ“‹ Protocol
1. **Tasks Completion**: Má»i task trong tasks.md Ä‘Ã£ `[X]`?
2. **Success Criteria**: Má»i SC trong spec.md Ä‘Ã£ Ä‘áº¡t?
3. **Build Verification** (PHáº¢I cháº¡y actual command):
   ```bash
   docker compose -f docker-compose.beta.yml build 2>&1 | tail -n 100
   ```
   Náº¿u fail â†’ âŒ BLOCKED
4. **Runtime Verification** (PHáº¢I cháº¡y actual command):
   ```bash
   docker compose -f docker-compose.beta.yml up -d
   sleep 15
   docker compose -f docker-compose.beta.yml ps
   ```
   - Táº¥t cáº£ services pháº£i `Up` (KHÃ”NG `Restarting`)
   - Náº¿u `Restarting` â†’ cháº¡y `docker compose logs <service>` â†’ âŒ BLOCKED
5. **Health Check** (PHáº¢I cháº¡y actual command):
   ```bash
   curl -s http://localhost:<web_port> | head -c 200
   curl -s http://localhost:<api_port>/health
   ```
   Táº¥t cáº£ pháº£i tráº£ vá» 200
6. **Constitution Check**: KhÃ´ng vi pháº¡m rules nÃ o?
7. **Final Verdict**:
   ```
   ðŸ VALIDATION REPORT
   â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
   Tasks:        15/15 âœ…
   TS Build:     PASS âœ…
   Runtime:      PASS âœ… (all services Up)
   Health:       PASS âœ… (all 200)
   Constitution: PASS âœ…
   â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
   VERDICT: âœ… READY FOR DEPLOY
   ```

## ðŸ“¤ Output
- File: `.agent/memory/validation-report.md`
- Verdict: âœ… PASS hoáº·c âŒ FAIL (kÃ¨m danh sÃ¡ch blockers)

## ðŸš« Guard Rails
- KHÃ”NG approve náº¿u cÃ²n task chÆ°a complete.
- KHÃ”NG approve náº¿u build fail.
- KHÃ”NG approve náº¿u báº¥t ká»³ service nÃ o `Restarting`.
- PHáº¢I cháº¡y actual commands â€” khÃ´ng chá»‰ Ä‘á»c code.

## When to Use
- Final gate trÆ°á»›c deploy: kiá»ƒm tra toÃ n bá»™ implementation Ä‘Ã¡p á»©ng spec + build + runtime + health.
- **KHÃ”NG dÃ¹ng cho**: kiá»ƒm tra nháº¥t quÃ¡n artifact (â†’ `@speckit.analyze`), review code (â†’ `@speckit.reviewer`).

## Common Rationalizations
| LÃ½ do bao biá»‡n | Sá»± tháº­t |
|---|---|
| "Äá»c code tháº¥y Ä‘Ãºng lÃ  pass" | Äá»c code â‰  cháº¡y Ä‘Æ°á»£c. Pháº£i cháº¡y actual build/runtime/health command. |
| "CÃ²n 1 task chÆ°a xong nhÆ°ng nhá»" | Task chÆ°a `[X]` = chÆ°a hoÃ n thÃ nh. KhÃ´ng approve. |
| "Service Restarting cháº¯c tá»± á»•n" | Restarting = lá»—i runtime. BLOCKED cho tá»›i khi Up. |
| "Health check sau deploy kiá»ƒm" | Health fail sau deploy = downtime. Verify trÆ°á»›c. |

## Red Flags
- Approve khi cÃ²n task chÆ°a `[X]` hoáº·c build fail.
- CÃ³ service á»Ÿ tráº¡ng thÃ¡i `Restarting`.
- Chá»‰ Ä‘á»c code mÃ  khÃ´ng cháº¡y command thá»±c táº¿.
- Health endpoint khÃ´ng tráº£ 200.

## Verification
- [ ] Má»i task `[X]`; má»i Success Criteria Ä‘áº¡t.
- [ ] Build command cháº¡y thá»±c táº¿ PASS.
- [ ] Táº¥t cáº£ service `Up` (khÃ´ng `Restarting`).
- [ ] Health check tráº£ 200 cho web + api.
- [ ] Constitution pass; verdict ghi rÃµ trong `validation-report.md`.
