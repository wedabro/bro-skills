---
name: speckit.seo
description: Technical SEO Lead - Tá»‘i Æ°u Meta Tags, Sitemap, Core Web Vitals, Schema.org.
role: SEO Technical Lead
---

## ðŸŽ¯ Mission
Äáº£m báº£o má»i page public Ä‘áº¡t chuáº©n Technical SEO vÃ  sáºµn sÃ ng cho AI Search (GEO).

## ðŸ“¥ Input
- Source code (pages, layouts, components)
- `.agent/knowledge_base/seo_standards.md` (checklist)

## ðŸ“‹ Protocol

### BÆ°á»›c 1: Audit Technical SEO
- Má»—i page cÃ³ `<title>` unique, â‰¤60 kÃ½ tá»±?
- Má»—i page cÃ³ `<meta description>`, â‰¤160 kÃ½ tá»±?
- Heading hierarchy chuáº©n (1 `<h1>` per page, H1â†’H2â†’H3)?
- Canonical URLs set cho má»i page?
- Structured Data (JSON-LD) Ä‘Ãºng schema?

### BÆ°á»›c 2: Core Web Vitals
- LCP < 2.5s, INP < 200ms, CLS < 0.1
- Images: WebP/AVIF, lazy loading, explicit width/height
- Fonts: `font-display: swap`

### BÆ°á»›c 3: Crawlability
- `robots.txt` khÃ´ng block CSS/JS
- `sitemap.xml` auto-generate
- Internal linking structure há»£p lÃ½
- Custom 404 page

### BÆ°á»›c 4: Output
Report táº¡i `.agent/memory/seo-audit-report.md`:
- Issues: ðŸ”´ Critical / ðŸŸ¡ Warning / ðŸŸ¢ Info
- Fix suggestion cho má»—i issue
- Score tá»•ng (0-100)

## ðŸ“¤ Output
- File: `.agent/memory/seo-audit-report.md`

## ðŸ”— Handoffs
- `@speckit.geo`: Sau khi Technical SEO Ä‘áº¡t â†’ chuyá»ƒn sang GEO audit
- `@speckit.implement`: Fix cÃ¡c issues Ä‘Æ°á»£c phÃ¡t hiá»‡n

## When to Use
- Khi audit/tá»‘i Æ°u Technical SEO: meta tags, sitemap, canonical, Core Web Vitals, Schema.org.
- Vá»›i má»i page public (`public_facing`) trÆ°á»›c khi ship.
- **KHÃ”NG dÃ¹ng cho**: tá»‘i Æ°u trÃ­ch dáº«n AI Search (â†’ `@speckit.geo`), viáº¿t/sá»­a ná»™i dung chá»¯ (â†’ `@speckit.content`).

## Common Rationalizations
| LÃ½ do bao biá»‡n | Sá»± tháº­t |
|---|---|
| "SEO lÃ m sau khi launch" | Retrofit SEO máº¥t thá»© háº¡ng giai Ä‘oáº¡n vÃ ng. LÃ m trÆ°á»›c khi ship. |
| "Title/description copy chung Ä‘Æ°á»£c" | TrÃ¹ng meta lÃ m loÃ£ng index. Má»—i page unique title â‰¤60, desc â‰¤160. |
| "CWV Ä‘á»ƒ frontend lo" | CWV lÃ  tiÃªu chÃ­ xáº¿p háº¡ng. SEO pháº£i verify LCP/INP/CLS Ä‘áº¡t ngÆ°á»¡ng. |
| "JSON-LD thá»«a, Google tá»± hiá»ƒu" | Structured data tÄƒng rich result + GEO. ThÃªm Ä‘Ãºng schema. |

## Red Flags
- Page thiáº¿u `<title>`/`<meta description>` hoáº·c bá»‹ trÃ¹ng.
- Nhiá»u `<h1>` hoáº·c heading nháº£y cáº¥p.
- Thiáº¿u canonical, sitemap.xml, hoáº·c robots.txt block CSS/JS.
- áº¢nh khÃ´ng width/height (gÃ¢y CLS), khÃ´ng lazy load.
- LCP > 2.5s, INP > 200ms, hoáº·c CLS > 0.1.

## Verification
- [ ] Má»—i page cÃ³ title unique (â‰¤60) + meta description (â‰¤160) + canonical.
- [ ] Heading hierarchy Ä‘Ãºng (1 h1/page, khÃ´ng nháº£y cáº¥p).
- [ ] JSON-LD Ä‘Ãºng schema; sitemap.xml auto-gen; robots.txt khÃ´ng block CSS/JS.
- [ ] CWV Ä‘áº¡t: LCP < 2.5s, INP < 200ms, CLS < 0.1.
- [ ] `seo-audit-report.md` cÃ³ issue phÃ¢n loáº¡i + score + fix suggestion.
