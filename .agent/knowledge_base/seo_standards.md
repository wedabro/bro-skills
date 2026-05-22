# 🔍 SEO & GEO Standards

## 📋 Technical SEO Checklist (Bắt buộc)
- [ ] Mỗi page có `<title>` unique, tối đa 60 ký tự
- [ ] Mỗi page có `<meta description>`, tối đa 160 ký tự
- [ ] Chỉ 1 `<h1>` per page, heading hierarchy chuẩn (H1 → H2 → H3)
- [ ] Canonical URL cho mọi page để tránh duplicate content
- [ ] `sitemap.xml` tự động generate và submit lên Google Search Console
- [ ] `robots.txt` cấu hình đúng (không block CSS/JS)
- [ ] Image: `alt` text mô tả, lazy loading, format WebP/AVIF
- [ ] URL slug: lowercase, dấu gạch ngang, không dấu tiếng Việt
- [ ] Mobile-first responsive design
- [ ] Core Web Vitals targets: LCP < 2.5s, INP < 200ms, CLS < 0.1

## 🤖 GEO (Generative Engine Optimization)
- [ ] File `llms.txt` tại root domain
- [ ] Structured Data (JSON-LD) cho Article, Product, FAQ, BreadcrumbList
- [ ] E-E-A-T signals: Author bio, nguồn trích dẫn, ngày publish/update
- [ ] Content format: short paragraphs, bullet points, numbered lists
- [ ] Fact-density: Mỗi đoạn văn ≥1 data point hoặc trích dẫn
- [ ] FAQ sections dạng "People Also Ask"
- [ ] Topic clusters: Liên kết nội bộ giữa bài viết cùng chủ đề

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
