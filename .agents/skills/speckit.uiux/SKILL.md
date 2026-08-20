---
name: speckit.uiux
description: UI/UX Architect - Definition of Design System Anti-Slop, UI Components, Spacing, Typography, Responsive Patterns.
---

## 🎯 Mission
Set up and manage "Pro Max" UI/UX standards for the project, ensuring a premium, professional, unique interface and ABSOLUTELY no "AI slops" (avoid AI's boring default designs).

## 📥 Input
- `.agents/specs/[feature]/spec.md` (contains User Scenarios)
- `.agents/memory/constitution.md` (tech stack constraints)
- Brand guidelines (if any)

## 📋 Protocol

### Phase 0: Brief Inference (Read the Room)
- Analyze projects (SaaS, portfolio, public-sector) to shape vibe.
- Define 3 parameters: `DESIGN_VARIANCE` (1-10), `MOTION_INTENSITY` (1-10), `VISUAL_DENSITY` (1-10).

### Phase 1: Brand Identity & Colors (Anti-Default)
- **Colors**: It is PROHIBITED to use default colors (red, blue, green). It is PROHIBITED to abuse "AI Purple / Blue glow". Use a sophisticated palette like Cold Luxury, Forest, Black & Tan.
- **Typography**: PROHIBITED using `Inter` and Serif as default for anything. Use `Geist` , `Satoshi` , `Cabinet Grotesk` or a sans-serif font of your choice.

### Phase 2: Spacing, Layout & Rhythm
- **Main Layout Protection**: Shared Page Shell (Header/Sidebar/Footer/Main Container) là layout chuẩn cố định toàn bộ website. KHÔNG ĐƯỢC tự ý chỉnh sửa hay làm biến dạng Layout chính khi làm việc ở các trang con. Hạn chế sửa layout chính, khi bắt buộc cần sửa PHẢI HỎI VÀ XÁC NHẬN VỚI USER trước.
- **Mandatory Pre-Flight Check**: Mỗi khi tạo mới hoặc thiết kế bất kỳ trang nào, BẮT BUỘC phải đọc và kiểm tra đối chiếu lại hệ thống khoảng cách (Padding/Margin scale), Grid rhythm (`gap-4`), và Bảng màu sắc Global.
- ALWAYS prefer existing framework/theme classes (`p-4`, `text-lg`,
  `rounded-md`) over arbitrary values so every screen uses the same scale.
- Use `gap-4` as the primary gap. Use `gap-2` only for tightly related controls
  and `gap-6`/`gap-8` only for clear hierarchy boundaries.
- Fixed-pixel values are limited to hairline borders, blur/shadow tuning, and
  very small precision radii. Repeated exceptions become named theme tokens.
- Limit Hero's top padding (max `pt-24` ). Hero maximum 2 subject lines.
- Apply Anti-Center Bias: Avoid boringly centering the Hero.
- Misuse of "eyebrow" (titles in super small caps) is PROHIBITED. Maximum 1 eyebrow per 3 sections.
- Bento Grid must have rhythm, not leave empty cells, diversify the background of the cells (images, subtle gradients, text).

### Phase 3: Core Components Design & i18n Protocol
- **RULE TỐI CAO: Reuse & Separation**:
  - Bắt buộc kiểm tra kỹ xem component có sẵn chưa trước khi tạo mới. Ưu tiên 100% tái sử dụng các khối component quen thuộc có sẵn trong thư mục components.
  - Tuyệt đối không tự ý viết code tạo UI form, card design hoặc các widget phức tạp trực tiếp bên trong các file Page. Phải tách biệt hoàn toàn thành các component độc lập để tái sử dụng.
- **i18n Strict Protocol**:
  - Phân tích và khai báo 100% văn bản vào file JSON dịch (`locales/{lang}/common.json` cho chuỗi dùng chung, `locales/{lang}/{module}.json` cho chuỗi theo module/trang).
  - Sử dụng i18n key đồng bộ tại 100% các thuộc tính UI (`label`, `placeholder`, `dropdown title`, `button text`, `tooltip`, `modal`, `toast`, `table header`, `empty state`).
- **Buttons**: Text does not wrap lines on the desktop. Contrast WCAG AA.
- **Cards**: Limit dark shadows on light backgrounds. Do not nest cards within cards.
- **Forms**: Label on input, do not use placeholder instead of label.

### Phase 4: Rich Aesthetics Directive
- Avoid cheap AI gradients. Use realistic Glassmorphism (backdrop-filter + 1px inner border) if the vibe fits.
- Interactive States & Skeleton Loading:
  - Bắt buộc áp dụng Skeleton Loading 1:1 với cấu trúc thực tế cho mọi component có tải dữ liệu bất đồng bộ. Nghiêm cấm dùng spinner quay tròn generic hoặc text loading thô sơ.
  - Tactile feedback using a built-in utility such as `active:scale-95`.

## 📤 Output
- File: `.agents/knowledge_base/ui_ux_standards.md`
- File: `.agents/specs/[feature]/ui-specs.md` (for each feature)

## 🚫 Guard Rails
- FORBIDDEN: Modifying the main page layout shell without asking and getting explicit user approval.
- MANDATORY: Perform pre-flight check of grid rhythm, padding scale, and color tokens before creating any new page.
- DO NOT use browser default colors.
- DO NOT mix Serif and Sans-serif in the same headline.
- DO NOT use 2 CTAs with the same purpose (same intent) on the same page.
- DO NOT use arbitrary fixed-pixel utilities when an existing class or token
  expresses the same intent.
- DO NOT write form designs or detailed UI blocks directly inside page files.
- MANDATORY: Check and reuse existing components before creating new ones.
- MANDATORY: Apply 1:1 skeleton loading to all asynchronous components.
- MANDATORY: Declare 100% UI texts in separate JSON files per module & common (`locales/{lang}/common.json` & `locales/{lang}/{module}.json`).
- FORBIDDEN: Hardcode string literals in UI or mix languages (English & Vietnamese) on the same interface.
- MANDATORY Mobile-first design priority.

