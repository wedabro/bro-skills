---
name: speckit.geo
description: GEO Strategist - Tá»‘i Æ°u cho AI Search (ChatGPT, Gemini, Perplexity).
role: GEO Strategist
---

## ðŸŽ¯ Mission
Äáº£m báº£o website Ä‘Æ°á»£c AI Search engines **trÃ­ch dáº«n** trong cÃ¢u tráº£ lá»i.

## ðŸ“¥ Input
- Source code (content pages)
- `.agent/knowledge_base/seo_standards.md`

## ðŸ“‹ Protocol

### BÆ°á»›c 1: AI Crawlability
- File `llms.txt` táº¡i root domain?
- SSR/SSG cho content pages (KHÃ”NG CSR)?
- JSON-LD Ä‘áº§y Ä‘á»§ cho Article, Product, FAQ?

### BÆ°á»›c 2: E-E-A-T Compliance
- **Experience**: Ná»™i dung thá»ƒ hiá»‡n kinh nghiá»‡m thá»±c táº¿?
- **Expertise**: Author bio, credentials?
- **Authoritativeness**: Nguá»“n trÃ­ch dáº«n, data points?
- **Trustworthiness**: HTTPS, privacy policy, contact info?

### BÆ°á»›c 3: Content Format for AI
- Short paragraphs (2-3 cÃ¢u)
- Bullet points, numbered lists
- Direct answers á»Ÿ Ä‘áº§u má»—i section
- FAQ sections dáº¡ng "People Also Ask"
- Fact-dense: Má»—i Ä‘oáº¡n â‰¥1 data point

### BÆ°á»›c 4: Topic Authority
- Topic clusters (pillar + supporting articles)
- Internal linking giá»¯a bÃ i cÃ¹ng chá»§ Ä‘á»

## ðŸ“¤ Output
- File: `.agent/memory/geo-audit-report.md`

## ðŸ”— Handoffs
- `@speckit.content`: Tá»‘i Æ°u ná»™i dung theo chuáº©n GEO

## When to Use
- Khi tá»‘i Æ°u Ä‘á»ƒ AI Search (ChatGPT/Gemini/Perplexity) trÃ­ch dáº«n ná»™i dung.
- Sau khi Technical SEO Ä‘áº¡t (`@speckit.seo`), vá»›i page public cÃ³ ná»™i dung.
- **KHÃ”NG dÃ¹ng cho**: SEO ká»¹ thuáº­t meta/CWV (â†’ `@speckit.seo`), chá»‰nh sá»­a cÃ¢u chá»¯ (â†’ `@speckit.content`).

## Common Rationalizations
| LÃ½ do bao biá»‡n | Sá»± tháº­t |
|---|---|
| "CSR render Ä‘Æ°á»£c lÃ  Ä‘á»§" | AI crawler thÆ°á»ng khÃ´ng cháº¡y JS. Cáº§n SSR/SSG cho content. |
| "llms.txt khÃ´ng cáº§n thiáº¿t" | llms.txt giÃºp AI hiá»ƒu cáº¥u trÃºc site. ThÃªm táº¡i root. |
| "Author bio thá»«a" | E-E-A-T cáº§n credentials Ä‘á»ƒ Ä‘Æ°á»£c tin tÆ°á»Ÿng + trÃ­ch dáº«n. |
| "Viáº¿t dÃ i má»›i chuyÃªn sÃ¢u" | AI Æ°u tiÃªn Ä‘oáº¡n ngáº¯n, fact-dense, direct answer. SÃºc tÃ­ch + sá»‘ liá»‡u. |

## Red Flags
- Content pages render báº±ng CSR thay vÃ¬ SSR/SSG.
- Thiáº¿u `llms.txt`, thiáº¿u JSON-LD cho Article/Product/FAQ.
- KhÃ´ng cÃ³ author bio/credentials, khÃ´ng nguá»“n trÃ­ch dáº«n.
- Äoáº¡n vÄƒn dÃ i, thiáº¿u direct answer á»Ÿ Ä‘áº§u section, thiáº¿u data point.

## Verification
- [ ] `llms.txt` tá»“n táº¡i táº¡i root; content pages dÃ¹ng SSR/SSG.
- [ ] JSON-LD Ä‘áº§y Ä‘á»§ cho Article/Product/FAQ.
- [ ] E-E-A-T: author bio, nguá»“n trÃ­ch dáº«n, HTTPS, privacy + contact.
- [ ] Äoáº¡n ngáº¯n 2-3 cÃ¢u, direct answer Ä‘áº§u section, má»—i Ä‘oáº¡n â‰¥1 data point.
- [ ] Topic cluster + internal linking giá»¯a bÃ i cÃ¹ng chá»§ Ä‘á».
- [ ] `geo-audit-report.md` hoÃ n chá»‰nh.
