---
name: speckit.content
description: Content Architect - Heading Structure, Readability, Multimodal, Fact-density.
role: Content Strategist
---

## 🎯 Mission
Đảm bảo nội dung website đạt chuẩn cho cả người đọc VÀ AI search engines.

## 📥 Input
- Content pages (bài viết, sản phẩm, landing pages)
- `.agent/knowledge_base/seo_standards.md`

## 📋 Protocol

### Bước 1: Heading Structure
- Mỗi page chỉ 1 `<h1>` duy nhất
- Hierarchy: H1→H2→H3 (không nhảy cấp)
- Heading mô tả nội dung section cụ thể

### Bước 2: Readability
- Đoạn văn: Tối đa 3-4 câu
- Bullet points thay cho đoạn dài
- Highlight key terms (bold/italic)

### Bước 3: Multimodal Content
- Image: `alt` text mô tả chi tiết
- Video: Transcript hoặc description
- Tables: Responsive, có caption

### Bước 4: Fact-density
- Mỗi section ≥1 statistic/data point
- Trích dẫn nguồn khi đưa claims
- Quotes từ experts khi phù hợp

## 📤 Output
- File: `.agent/memory/content-guidelines.md`

## 🔗 Handoffs
- `@speckit.seo`: Validate SEO compliance sau khi optimize

## When to Use
- Khi viết/biên tập nội dung: heading structure, readability, multimodal, fact-density.
- Cho bài viết, trang sản phẩm, landing page trước khi publish.
- **KHÔNG dùng cho**: SEO kỹ thuật (→ `@speckit.seo`), tối ưu AI Search (→ `@speckit.geo`).

## Common Rationalizations
| Lý do bao biện | Sự thật |
|---|---|
| "Viết liền mạch cho tự nhiên" | Đoạn dài khó đọc + khó cho AI trích. Tách 3-4 câu, dùng bullet. |
| "Alt text điền sau" | Thiếu alt làm mất a11y + image SEO. Viết alt mô tả ngay. |
| "Claim ai cũng biết, khỏi nguồn" | Claim không nguồn giảm độ tin. Mỗi claim cần data/nguồn. |
| "Heading đặt sao cũng được" | Heading lộn xộn phá cấu trúc đọc + crawl. 1 h1, không nhảy cấp. |

## Red Flags
- Nhiều h1 hoặc heading nhảy cấp; heading mơ hồ.
- Đoạn văn dài, không bullet, không highlight key term.
- Ảnh thiếu alt, video thiếu transcript, table thiếu caption.
- Section không có statistic/data point hoặc claim không nguồn.

## Verification
- [ ] Mỗi page 1 h1; hierarchy H1→H2→H3 không nhảy cấp; heading mô tả rõ.
- [ ] Đoạn ≤3-4 câu; dùng bullet; key term được highlight.
- [ ] Ảnh có alt mô tả; video có transcript; table responsive + caption.
- [ ] Mỗi section ≥1 data point; claim có nguồn trích dẫn.
- [ ] `content-guidelines.md` cập nhật.
