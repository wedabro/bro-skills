# bro-skills Rules for bro-skills

Dá»± Ã¡n: bro-skills

## 1. PHÃP Lá»†NH Tá»I CAO
- TuÃ¢n thá»§ nghiÃªm ngáº·t file `.agent/memory/constitution.md`.
- Docker-First: Má»i hoáº¡t Ä‘á»™ng code vÃ  cháº¡y app pháº£i diá»…n ra trong container. KHÃ”NG cháº¡y node/python trÃªn host.
- Ports: Chá»‰ sá»­ dá»¥ng dáº£i port 8900-8999.

## 2. bro-skills PROTOCOL
- Má»i task pháº£i Ä‘i qua quy trÃ¬nh: Specify â†’ Plan â†’ Tasks â†’ Implement.
- Sá»­ dá»¥ng Workflows trong `.agent/workflows/` vÃ  Skills trong `.agent/skills/`.

## 3. NGÃ”N NGá»® & CODE
- Pháº£n há»“i developer hoÃ n toÃ n báº±ng Tiáº¿ng Viá»‡t.
- 15-Minute Rule: Má»—i task pháº£i atomic, â‰¤ 15 phÃºt, áº£nh hÆ°á»Ÿng â‰¤ 3 files.
- PowerShell 5.1+, ngÄƒn cÃ¡ch lá»‡nh báº±ng dáº¥u `;` (KHÃ”NG dÃ¹ng `&&`).
- KHÃ”NG hard-code URLs, Tokens, Keys. DÃ¹ng ENV vars (`.env`).

## 4. AN TOÃ€N
- KHÃ”NG cháº¡y `docker compose down -v` trÃªn Production.
- Táº¡o script tá»± Ä‘á»™ng (`.agent/scripts/`) cho lá»—i láº·p láº¡i.
- Kiá»ƒm tra logs ngay khi lá»—i: `docker compose logs -f <service>`.


