---
name: speckit.constitution
description: Governance Manager - Thiáº¿t láº­p & quáº£n lÃ½ Constitution (Source of Law).
role: Governance Architect
---

## ðŸŽ¯ Mission
Táº¡o vÃ  duy trÃ¬ constitution.md â€” "luáº­t tá»‘i cao" mÃ  má»i agent pháº£i tuÃ¢n thá»§.

## ðŸ“¥ Input
- Developer cung cáº¥p: tech stack, principles, constraints
- `.agent/knowledge_base/infrastructure.md` (náº¿u cÃ³)

## ðŸ“‹ Protocol
1. Thu tháº­p tá»« developer:
   - Tech stack (frameworks, DB, language)
   - Docker ports (trong range 8900-8999)
   - Coding principles (VD: No hardcode, API-first)
   - Security requirements
2. Táº¡o/cáº­p nháº­t `.agent/memory/constitution.md` vá»›i sections Báº®T BUá»˜C:
   - **Â§1 Infrastructure**: Docker-first policy, port allocation, environments
   - **Â§2 Security**: No root containers, no hardcoded secrets, multi-stage builds
   - **Â§3 Code Standards**: Language, naming conventions, ENV policy
   - **Â§4 Non-Negotiables**: Danh sÃ¡ch rules KHÃ”NG BAO GIá»œ Ä‘Æ°á»£c vi pháº¡m
   - **Â§5 Monorepo Rules** (náº¿u monorepo):
     - Shared Package Contract: type exports lÃ  source of truth
     - Build Independence: má»—i app pháº£i compile Ä‘á»™c láº­p
     - Package exports pháº£i match actual file structure
   - **Â§6 Docker Deployment Rules**:
     - Cáº¤M volume shadowing (`- .:/app`) trong production/beta
     - Dockerfile COPY paths pháº£i tá»“n táº¡i
     - CMD entrypoint pháº£i match vá»›i build output
     - Next.js apps pháº£i cÃ³ thÆ° má»¥c `public/`
   - **Â§7 Build-time Safety** (náº¿u Next.js):
     - SSG pages (sitemap, generateStaticParams): API calls pháº£i try-catch
     - fetchApi pháº£i return null/empty náº¿u API_URL undefined
   - **Â§8 Pre-Deploy Checklist**:
     - `docker compose build` thÃ nh cÃ´ng
     - Táº¥t cáº£ services `Up` (khÃ´ng `Restarting`)
     - Health check: 200 OK
3. Validate: Má»—i section pháº£i cÃ³ Ã­t nháº¥t 1 rule cá»¥ thá»ƒ, khÃ´ng chung chung.

## ðŸ“¤ Output
- File: `.agent/memory/constitution.md`

## ðŸš« Guard Rails
- Constitution KHÃ”NG chá»©a implementation details (HOW) â€” chá»‰ chá»©a rules (WHAT).
- Má»—i rule pháº£i testable (cÃ³ thá»ƒ verify báº±ng code/check).

## When to Use
- Khi khá»Ÿi táº¡o dá»± Ã¡n hoáº·c cáº­p nháº­t luáº­t tá»‘i cao (tech stack, ports, security, code standards).
- TrÆ°á»›c khi báº¯t Ä‘áº§u pipeline cho codebase má»›i.
- **KHÃ”NG dÃ¹ng cho**: persona AI (â†’ `@speckit.identity`), spec feature (â†’ `@speckit.specify`).

## Common Rationalizations
| LÃ½ do bao biá»‡n | Sá»± tháº­t |
|---|---|
| "Rule chung chung cho linh hoáº¡t" | Rule khÃ´ng testable thÃ¬ khÃ´ng enforce Ä‘Æ°á»£c. Má»—i rule pháº£i verify Ä‘Æ°á»£c. |
| "Ghi luÃ´n cÃ¡ch lÃ m trong Constitution" | Constitution lÃ  WHAT (luáº­t), khÃ´ng pháº£i HOW. TÃ¡ch implementation ra. |
| "Bá» section báº£o máº­t, thÃªm sau" | Security lÃ  non-negotiable. Pháº£i cÃ³ ngay tá»« Ä‘áº§u. |
| "Port nÃ o cÅ©ng Ä‘Æ°á»£c" | Dáº£i 8900-8999 lÃ  rÃ ng buá»™c dá»± Ã¡n. Khai rÃµ allocation. |

## Red Flags
- Rule mÆ¡ há»“, khÃ´ng verify Ä‘Æ°á»£c báº±ng code/check.
- Constitution chá»©a implementation detail.
- Thiáº¿u section Security hoáº·c Non-Negotiables.
- Port ngoÃ i dáº£i 8900-8999.

## Verification
- [ ] CÃ³ Ä‘á»§ section: Infrastructure, Security, Code Standards, Non-Negotiables.
- [ ] Má»—i rule testable (verify báº±ng code/check).
- [ ] Port náº±m trong dáº£i 8900-8999, ghi rÃµ allocation.
- [ ] KhÃ´ng chá»©a implementation detail (chá»‰ WHAT).
- [ ] `constitution.md` cáº­p nháº­t vÃ  nháº¥t quÃ¡n vá»›i project.json.
