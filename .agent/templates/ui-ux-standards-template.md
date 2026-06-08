# 🎨 UI/UX Standards (Anti-Slop & Premium)

## 🌈 Brand Palette & Color Calibration
- **Anti-Default**: CẤM dùng các màu mặc định của trình duyệt (red/blue/green nguyên bản). CẤM lạm dụng "AI Purple" gradient.
- **Premium Consumer Ban**: Tránh dùng palette kem/be + đồng/đất sét (beige + brass/clay) mặc định của AI trừ khi brief yêu cầu rõ. Sử dụng các palette thay thế như Cold Luxury (silver-grey + chrome), Forest (deep green + bone), hoặc Black and Tan.
- **Quy tắc 1 Accent**: Chọn 1 màu nhấn (Accent) duy nhất và dùng nhất quán trên toàn bộ trang.

## 🔡 Typography (Anti-Slop)
- **Display Font**: CẤM dùng `Inter` làm mặc định cho các heading sáng tạo. Hãy dùng `Geist`, `Satoshi`, `Cabinet Grotesk`, `Outfit` hoặc một font phù hợp dự án.
- **Serif Discipline**: KHÔNG dùng font có chân (Serif) làm mặc định trừ khi brand yêu cầu phong cách editorial/luxury/vintage. Cấm mix chữ có chân và không chân trong cùng 1 tiêu đề.
- **Hierarchy**: Tiêu đề H1 tối đa 2 dòng. Phụ đề (subtext) tối đa 20 từ.

## 📏 Layout & Rhythm
- **Hero Section**: Hạn chế top padding (max `pt-24` trên desktop).
- **Anti-Center Bias**: Tránh căn giữa Hero một cách nhàm chán nếu không phải là trang manifesto. Ưu tiên bố cục Split Screen hoặc Asymmetric.
- **Eyebrow Restraint**: CẤM lạm dụng "eyebrow" (tiêu đề nhỏ in hoa phía trên) ở mọi section. Tối đa 1 eyebrow trên mỗi 3 sections.
- **Bento Grid**: Lưới Bento phải có nhịp điệu. Số lượng ô bằng đúng số lượng content. Không để ô trống. Cần đa dạng hoá cell (ảnh thực tế, gradient, chữ).
- **Zigzag Ban**: Tối đa 2 section liên tiếp dùng layout "trái-ảnh phải-chữ" đảo ngược (zigzag).

## 🧱 Core Components (Atomic) & Accessibility
- **Buttons (CTAs)**:
  - CẤM text trên button bị rớt dòng (wrap text) trên desktop. Label button tối đa 3 từ (ví dụ: `Get Started`).
  - CẤM 2 CTA có cùng mục đích (cùng intent) xuất hiện trên cùng một trang (chỉ chọn 1 label).
  - Tỉ lệ tương phản WCAG AA tối thiểu 4.5:1 (Không dùng chữ trắng trên nền xám nhạt).
- **Interactive UI States**:
  - Skeletal loaders cho dữ liệu loading (không dùng spinner chung chung).
  - Tactile Feedback: Thêm `-translate-y-[1px]` hoặc `scale-[0.98]` khi `:active` để tạo cảm giác bấm vật lý.
- **Images**: BẮT BUỘC có hình ảnh thật (từ image gen tool, unsplash, picsum). CẤM dùng các `div` fake screenshot.

## ✨ Micro-animations
- Sử dụng `framer-motion` hoặc `gsap` có chủ đích.
- Motion phải hỗ trợ `prefers-reduced-motion`.
- CẤM lặp marquee (chữ chạy ngang) quá 1 lần trên 1 trang.
