# 🎨 UI/UX Standards (Anti-Slop & Premium)

## 🌈 Brand Palette & Color Calibration
- **Anti-Default**: FORBIDDEN to use default browser colors (pure red/blue/green). FORBIDDEN to overuse "AI Purple" gradients.
- **Premium Consumer Ban**: Avoid AI default beige + brass/clay palettes unless explicitly requested. Use alternatives like Cold Luxury (silver-grey + chrome), Forest (deep green + bone), or Black and Tan.
- **1 Accent Rule**: Choose a single Accent color and use it consistently across the entire site.

## 🧭 Systemic Layout & Ownership
- **Shared Page Shell**: Manage the header, sidebar, footer, content container,
  breadcrumbs, page title, and page actions through shared layout components.
  Do not rebuild the shell inside individual pages.
- **Strict Main Layout Protection (Khóa Cứng Layout Chính)**: Shared Page Shell (Header, Sidebar, Footer, Main Container) là layout chuẩn cố định toàn website. TUYỆT ĐỐI KHÔNG tự ý chỉnh sửa hay làm biến dạng Layout chính khi code các trang con. Hạn chế tối đa việc sửa Layout chính. Trong trường hợp đặc biệt cần điều chỉnh Layout chính, BẮT BUỘC PHẢI HỎI VÀ NHẬN ĐƯỢC XÁC NHẬN CỦA USER trước khi sửa.
- **Page-Family Consistency**: Pages with the same purpose must share the same
  content width, horizontal padding, title position, and composition pattern.
- **Single Change Point**: Centralize color, typography, spacing, radius, shadow,
  container width, breakpoints, control height, z-index, and motion in design
  tokens, CSS variables, theme configuration, or typed component variants.
- **Shared Primitives**: Standardize buttons, fields, cards, tables, dialogs,
  drawers, loading states, empty states, and error states. Feature code composes
  these primitives instead of restyling them.


## 🔡 Typography & Font-Size Guidelines (Anti-Slop)
- **Unit Standard**: Always use `rem` units (calculated from browser default root font-size, usually 16px) for scalability.
- **Display Font**: FORBIDDEN to use `Inter` as default for creative headings. Use `Geist`, `Satoshi`, `Cabinet Grotesk`, `Outfit`, or a project-specific font.
- **Serif Discipline**: DO NOT use Serif fonts as default unless brand requires editorial/luxury/vintage styles. Forbidden to mix serif and sans-serif fonts in the same heading.
- **Default/Body Text Size**:
  - **Interactive-Heavy Pages (Interactive/Dashboards/Forms)**: Main body text size should be 14px to 20px (0.875rem - 1.25rem). Prefer 1rem (16px) as the default to optimize information density, button spacing, text inputs, and controls.
  - **Text-Heavy Pages (Content-rich/Articles/Blogs)**: Main body text size should be 18px to 24px (1.125rem - 1.5rem) to ensure readability for long paragraphs. NEVER exceed 24px for body text.
- **Secondary/Sub-text**: Should be roughly 2 font sizes smaller than the body font (e.g., 0.875rem / 14px when Body is 16px; or 0.8125rem - 0.85rem / 13px when Body is 18px) for caption, metadata, and description.
- **Optimal Line Length (Measure)**: For body blocks (especially text-heavy layouts), constrain the text container width so that each line contains **50 to 75 characters** (including spaces). (Under 50 characters causes rapid eye movements; over 75 characters makes it hard to locate the next line).
- **Headings Hierarchy**:
  - **Desktop H1 Size**: Experiment with sizes between 30px and 50px (1.875rem - 3.125rem). H1 headings max 2 lines. Subtext max 20 words.
  - **Font Weight**: Use solid, prominent weights (`font-bold`, `font-extrabold`, or `font-black`).
  - **Font Pairing**: Headers and subheads are ideal places to pair a second font. Ensure logical pairing and strong contrast.
- **Text Inputs & Textareas**: Font size MUST be at least 1rem (16px) to prevent iOS Safari from auto-zooming on focus.
- **Line Height (Leading)**:
  - Standard body text ratio should be 1.5 to 1.7.
  - **Text-Heavy Pages**: Prefer Body 1.125rem (18px) and Line-height 1.6 - 1.7 to minimize eye strain.
  - **Interactive-Heavy Pages**: Prefer Body 1rem (16px) and Line-height 1.5 for compact, high-density layouts.

## 📏 Layout, Spacing & Padding
- **Mandatory Pre-Flight Rule Check (Check Rule Mỗi Khi Tạo Trang)**: Mỗi khi tạo mới hoặc thiết kế bất kỳ trang nào, Agent BẮT BUỘC phải đọc và kiểm tra lại hệ thống khoảng cách (Padding/Margin Scale), hệ thống lưới (Grid Rhythm), và Bảng màu sắc thiết kế Global của dự án để đảm bảo tính nhất quán tuyệt đối.
- **Utility Class Priority**: ALWAYS prefer existing framework/theme classes
  such as `p-4`, `text-lg`, `gap-4`, and `rounded-md`. This shared scale is the
  source of truth for consistent spacing, typography, sizing, and radius.

- **Primary Gap Rhythm**: Use `gap-4` as the default gap for components, grids,
  and ordinary content groups. Use `gap-2` only for tightly related controls
  and `gap-6`/`gap-8` only when a larger hierarchy boundary clearly requires it.
- **Arbitrary Value Ban**: DO NOT use arbitrary fixed-pixel utilities such as
  `p-[18px]`, `text-[17px]`, or `w-[347px]` when an existing class or design
  token can express the intent.
- **Fixed-Pixel Exceptions**: Fixed `px` values are allowed only for hairline
  borders such as `border-[1px]`, blur/shadow tuning, or very small radii that
  require pixel-level sharpness. If the same exception appears more than once,
  promote it to a named theme token or reusable class.
- **4-Point Spacing Scale**: Stay on the framework scale (`p-1`, `p-2`, `p-3`,
  `p-4`, `p-5`, `p-6`, `p-8`, `p-10`, `p-12`, `p-16`). Keep equivalent values
  on the shared 4px rhythm; do not invent page-local spacing.
- **Hero Section**: Limit top padding (max `pt-24` on desktop).
- **Anti-Center Bias**: Avoid boring centered Hero layout unless it's a manifesto page. Prefer Split Screen or Asymmetric layouts.
- **Eyebrow Restraint**: FORBIDDEN to overuse "eyebrow" headings. Max 1 eyebrow per 3 sections.
- **Bento Grid**: Bento grids must have rhythm. Number of cells must match content. No empty cells. Diversify cells (real images, gradients, text).
- **Zigzag Ban**: Max 2 consecutive sections using alternating image-text (zigzag) layouts.
- **Core Padding Guidelines**:
  - **Buttons (CTAs)**: Vertical padding of 0.5rem (8px), horizontal padding of 1rem (16px).
  - **Page Containers**: Prefer `px-4 md:px-6 lg:px-8`.
  - **Cards & Small Containers**: Prefer `p-4`, increasing to `p-6` only when the
    component hierarchy or viewport needs more room.
  - **Form Fields**: Use `gap-4`; use `gap-2` for icon-label or helper-text pairs.
  - **Page Sections/Containers**: Vertical padding (py) should be generous, ranging from 2rem (32px) to 4rem (64px) to let layouts breathe.

## 📱 Responsive System
- Design mobile-first and use the project's established `sm`, `md`, `lg`, `xl`,
  and `2xl` breakpoints. Add a breakpoint only when content demonstrates a
  reusable need.
- Let shared layout and component primitives own their responsive behavior.
  Avoid page-specific breakpoint patches for behavior already owned upstream.

## 🔢 Minimize Font-size Variations (Consistency First)
- **Max 4 Font Sizes**: Limit font variations on a single page to a maximum of 4 sizes:
  1. **Header Size**: Main headings (H1) and subheaders (H2, H3).
  2. **Default/Body Size**: Standard body text, and interactive controls (textboxes, dropdowns, buttons, navigation menus). Keep these strictly uniform.
  3. **Secondary Size**: ~2px smaller than default (usually 0.875rem / 14px). Used for secondary descriptions, captions, metadata, or supporting info.
  4. **Tertiary/Label/Wildcard Size**: Smallest size (usually 0.75rem - 0.8rem / 12px - 13px) for capitalized labels, tags, or deep hierarchical items to balance visual weight.
- **Strict Consistency**: Default to uniformity. Do not introduce arbitrary font sizes.

## 🧱 Core Components (Atomic) & Accessibility
- **RULE TỐI CAO: Reuse First & Page Cleanliness**:
  - Bắt buộc kiểm tra kỹ hệ thống component có sẵn trước khi tạo mới. Nếu đã có component tương tự, PHẢI sử dụng lại hoặc mở rộng qua props/variants thay vì tự ý tạo mới hoặc nhân bản code.
  - TUYỆT ĐỐI KHÔNG tự ý viết code tạo UI form, card design, hoặc các khối giao diện chi tiết trực tiếp bên trong các file Page (ví dụ `page.tsx`, `index.html`, v.v.). Page chỉ đóng vai trò làm layout container kết nối, truyền props, quản lý high-level state và fetching dữ liệu. Mọi form, card, widget phải được tách biệt hoàn toàn thành các component con độc lập trong thư mục components.
- **Forms**: Use a shared field contract for label, control, helper text, error,
  required, disabled, read-only, success, and loading states.
- **Tables**: Use a shared table/data-table primitive for loading, empty state,
  pagination, sorting, filtering, row actions, selection, responsiveness, and
  data formatting as applicable.
- **Dialogs & Drawers**: Use shared shell/header/content/footer primitives.
  Centralize overlay, width, padding, radius, and motion.
- **Buttons (CTAs)**:
  - FORBIDDEN to wrap button text on desktop. Button labels max 3 words (e.g., `Get Started`).
  - FORBIDDEN to have 2 CTAs with the same intent on the same page (choose only one label).
  - Minimum WCAG AA contrast ratio 4.5:1 (Do not use white text on light grey background).
- **Interactive UI States & Skeleton Loading**:
  - BẮT BUỘC áp dụng **Skeleton Loading** cho tất cả các component có tải dữ liệu bất đồng bộ (async API call). Nghiêm cấm dùng spinner quay tròn generic hoặc text loading thô sơ cho toàn bộ vùng nội dung lớn.
  - Thiết kế của Skeleton Loader phải khớp 1:1 với kích thước, bo góc, cấu trúc phân cấp và layout của component thực tế khi hiển thị dữ liệu xong nhằm tránh hiện tượng giật lắc bố cục (layout shift).
  - Tactile Feedback: Use built-in utilities such as `active:translate-y-px`
    or `active:scale-95` for physical button feedback.
- **Images**: REQUIRED to have real images (from image gen tools, Unsplash, Picsum). FORBIDDEN to use div fake screenshots.

## ✨ Micro-animations
- Use `framer-motion` or `gsap` intentionally.
- Animations must respect `prefers-reduced-motion`.
- FORBIDDEN to repeat marquee texts more than once per page.
