# 🔍 SEO, GEO & Web Quality Standards

## 📋 Technical SEO Checklist (Required)
- [ ] Each page has a unique `<title>`, max 60 characters
- [ ] Each page has a `<meta description>`, max 160 characters
- [ ] Only one `<h1>` per page, standard heading hierarchy (H1 → H2 → H3)
- [ ] Canonical URL for every page to avoid duplicate content
- [ ] `sitemap.xml` automatically generated and submitted to Google Search Console
- [ ] `robots.txt` correctly configured (does not block CSS/JS)
- [ ] Image: descriptive `alt` text, lazy loading, WebP/AVIF format
- [ ] URL slug: lowercase, hyphens, no accents
- [ ] Mobile-first responsive design

## ⚡ Core Web Vitals & Performance Budget
- [ ] **LCP (Largest Contentful Paint) < 2.5s**: High priority above-fold elements, preload LCP image.
- [ ] **INP (Interaction to Next Paint) < 200ms**: Avoid blocking main thread, split long tasks.
- [ ] **CLS (Cumulative Layout Shift) < 0.1**: Specify dimensions (width/height) or `aspect-ratio` on all media/ads.
- [ ] Total page weight < 1.5 MB, JS < 300 KB (compressed), CSS < 100 KB (compressed), Fonts < 100 KB.

## 🤖 GEO (Generative Engine Optimization)
- [ ] File `llms.txt` at root domain
- [ ] Structured Data (JSON-LD) for Article, Product, FAQ, BreadcrumbList
- [ ] E-E-A-T signals: Author bio, source citations, publish/update dates
- [ ] Content format: short paragraphs, bullet points, numbered lists
- [ ] Fact-density: Each paragraph has ≥1 data point or citation
- [ ] FAQ sections matching "People Also Ask" queries
- [ ] Topic clusters: Internal linking between related posts

## 🛠️ Performance Optimization Techniques

### 1. Instant Navigation (Speculation Rules API)
For multi-page apps, prerender next pages on hover to reduce LCP to ~0ms:
```html
<script type="speculationrules">
{
  "prerender": [{
    "where": { "href_matches": "/*" },
    "eagerness": "moderate"
  }]
}
</script>
```

### 2. Yielding to Scheduler (Reduce INP)
Split long tasks (>50ms) using `scheduler.yield()` to keep the main thread responsive:
```javascript
async function processLargeArray(items) {
  for (let i = 0; i < items.length; i += 100) {
    items.slice(i, i + 100).forEach(expensiveOperation);
    if ('scheduler' in window && 'yield' in scheduler) {
      await scheduler.yield();
    } else {
      await new Promise(r => setTimeout(r, 0)); // Fallback
    }
  }
}
```

### 3. Visual Stability (Reduce CLS)
Always reserve space for dynamic content and images:
```html
<!-- Set aspect-ratio or explicit dimensions -->
<img src="photo.webp" alt="Hero" style="aspect-ratio: 16/9; width: 100%;" />
<div style="min-height: 250px;"> <!-- Ad container -->
  <iframe src="ad-link" height="250"></iframe>
</div>
```

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
```
