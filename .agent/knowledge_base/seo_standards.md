# 🔍 SEO ​​& GEO Standards

## 📋 Technical SEO Checklist (Required)
- [ ] Each page has `<title>` unique, maximum 60 characters
- [ ] Each page has `<meta description>` , maximum 160 characters
- [ ] Only 1 `<h1>` per page, standard heading hierarchy (H1 → H2 → H3)
- [ ] Canonical URL for every page to avoid duplicate content
- [ ] `sitemap.xml` automatically generates and submits to Google Search Console
- [ ] `robots.txt` correct configuration (no CSS/JS blocking)
- [ ] Image: `alt` text description, lazy loading, format WebP/AVIF
- [ ] URL slug: lowercase, dash, no Vietnamese accents
- [ ] Mobile-first responsive design
- [ ] Core Web Vitals targets: LCP < 2.5s, INP < 200ms, CLS < 0.1

## 🤖 GEO (Generative Engine Optimization)
- [ ] File `llms.txt` at root domain
- [ ] Structured Data (JSON-LD) for Article, Product, FAQ, BreadcrumbList
- [ ] E-E-A-T signals: Author bio, source, publication/update date
- [ ] Content format: short paragraphs, bullet points, numbered lists
- [ ] Fact-density: Each paragraph has ≥1 data point or quote
- [ ] FAQ sections as "People Also Ask"
- [ ] Topic clusters: Internal links between articles on the same topic

## 📊 Schema.org (JSON-LD Templates)

### Article
```json
{"@context":"https://schema.org","@type":"Article","headline":"...","author":{"@type":"Person","name":"..."},"datePublished":"...","image":"..."}
```

### Product
```json
{"@context":"https://schema.org","@type":"Product","name":"...","image":"...","offers":{"@type":"Offer","price":"...","priceCurrency":"VND"}}
```

### FAQ
```json
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"...","acceptedAnswer":{"@type":"Answer","text":"..."}}]}
```json
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"...","acceptedAnswer":{"@type":"Answer","text":"..."}}]}
```
