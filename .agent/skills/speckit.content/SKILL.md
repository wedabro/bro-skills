---
name: speckit.content
description: Content Architect - Heading Structure, Readability, Multimodal, Fact-density.
role: Content Strategist
---

## ðŸŽ¯ Mission
Äáº£m báº£o ná»™i dung website Ä‘áº¡t chuáº©n cho cáº£ ngÆ°á»i Ä‘á»c VÃ€ AI search engines.

## ðŸ“¥ Input
- Content pages (bÃ i viáº¿t, sáº£n pháº©m, landing pages)
- `.agent/knowledge_base/seo_standards.md`

## ðŸ“‹ Protocol

### BÆ°á»›c 1: Heading Structure
- Má»—i page chá»‰ 1 `<h1>` duy nháº¥t
- Hierarchy: H1â†’H2â†’H3 (khÃ´ng nháº£y cáº¥p)
- Heading mÃ´ táº£ ná»™i dung section cá»¥ thá»ƒ

### BÆ°á»›c 2: Readability
- Äoáº¡n vÄƒn: Tá»‘i Ä‘a 3-4 cÃ¢u
- Bullet points thay cho Ä‘oáº¡n dÃ i
- Highlight key terms (bold/italic)

### BÆ°á»›c 3: Multimodal Content
- Image: `alt` text mÃ´ táº£ chi tiáº¿t
- Video: Transcript hoáº·c description
- Tables: Responsive, cÃ³ caption

### BÆ°á»›c 4: Fact-density
- Má»—i section â‰¥1 statistic/data point
- TrÃ­ch dáº«n nguá»“n khi Ä‘Æ°a claims
- Quotes tá»« experts khi phÃ¹ há»£p

## ðŸ“¤ Output
- File: `.agent/memory/content-guidelines.md`

## ðŸ”— Handoffs
- `@speckit.seo`: Validate SEO compliance sau khi optimize

## When to Use
- Khi viáº¿t/biÃªn táº­p ná»™i dung: heading structure, readability, multimodal, fact-density.
- Cho bÃ i viáº¿t, trang sáº£n pháº©m, landing page trÆ°á»›c khi publish.
- **KHÃ”NG dÃ¹ng cho**: SEO ká»¹ thuáº­t (â†’ `@speckit.seo`), tá»‘i Æ°u AI Search (â†’ `@speckit.geo`).

## Common Rationalizations
| LÃ½ do bao biá»‡n | Sá»± tháº­t |
|---|---|
| "Viáº¿t liá»n máº¡ch cho tá»± nhiÃªn" | Äoáº¡n dÃ i khÃ³ Ä‘á»c + khÃ³ cho AI trÃ­ch. TÃ¡ch 3-4 cÃ¢u, dÃ¹ng bullet. |
| "Alt text Ä‘iá»n sau" | Thiáº¿u alt lÃ m máº¥t a11y + image SEO. Viáº¿t alt mÃ´ táº£ ngay. |
| "Claim ai cÅ©ng biáº¿t, khá»i nguá»“n" | Claim khÃ´ng nguá»“n giáº£m Ä‘á»™ tin. Má»—i claim cáº§n data/nguá»“n. |
| "Heading Ä‘áº·t sao cÅ©ng Ä‘Æ°á»£c" | Heading lá»™n xá»™n phÃ¡ cáº¥u trÃºc Ä‘á»c + crawl. 1 h1, khÃ´ng nháº£y cáº¥p. |

## Red Flags
- Nhiá»u h1 hoáº·c heading nháº£y cáº¥p; heading mÆ¡ há»“.
- Äoáº¡n vÄƒn dÃ i, khÃ´ng bullet, khÃ´ng highlight key term.
- áº¢nh thiáº¿u alt, video thiáº¿u transcript, table thiáº¿u caption.
- Section khÃ´ng cÃ³ statistic/data point hoáº·c claim khÃ´ng nguá»“n.

## Verification
- [ ] Má»—i page 1 h1; hierarchy H1â†’H2â†’H3 khÃ´ng nháº£y cáº¥p; heading mÃ´ táº£ rÃµ.
- [ ] Äoáº¡n â‰¤3-4 cÃ¢u; dÃ¹ng bullet; key term Ä‘Æ°á»£c highlight.
- [ ] áº¢nh cÃ³ alt mÃ´ táº£; video cÃ³ transcript; table responsive + caption.
- [ ] Má»—i section â‰¥1 data point; claim cÃ³ nguá»“n trÃ­ch dáº«n.
- [ ] `content-guidelines.md` cáº­p nháº­t.
