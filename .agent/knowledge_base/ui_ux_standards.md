# 🎨 UI/UX Standards & Anti-Slop Guidelines (Pro Max)

Tài liệu này định nghĩa tiêu chuẩn thiết kế premium, có hồn, chống lại các khuôn mẫu thiết kế AI mặc định ("AI slop") cho dự án.

---

## 1. 🎛️ THE THREE DIALS (Bộ Ba Cấu Hình Giao Diện)
Mọi trang thiết kế phải định cấu hình bộ ba dial từ 1 đến 10 dựa trên "Design Read":

* **`DESIGN_VARIANCE`** (1 = Đối xứng hoàn hảo | 10 = Nghệ thuật bất đối xứng)
* **`MOTION_INTENSITY`** (1 = Tĩnh hoàn toàn | 10 = Chuyển động vật lý cinematic)
* **`VISUAL_DENSITY`** (1 = Thoáng đãng như triển lãm | 10 = Bảng điều khiển dày đặc dữ liệu)

### Cấu hình mặc định cho các loại trang (Dial Inference):
* **SaaS/B2B Landing**: `7 / 6 / 4`
* **Creative/Agency Landing**: `9 / 8 / 3`
* **Designer/Creative Portfolio**: `8 / 7 / 3`
* **Developer Portfolio**: `6 / 5 / 4`
* **Editorial / Blog**: `6 / 4 / 3`

---

## 2. 🌈 PALETTE COLOR CALIBRATION (Bảng Màu Đẳng Cấp)
**CẤM MẶC ĐỊNH**: Cấm sử dụng màu tím gradient AI-slop phát sáng (`AI-purple`) hoặc màu generic của trình duyệt. Cấm mặc định sử dụng palette beige/brass/espresso sáo rỗng cho các dòng sản phẩm cao cấp (DTC premium consumer).
Hãy xoay tua hoặc chọn một trong các palette sau:

* **Cold Luxury (Lạnh lùng sang trọng)**: Silver-grey + Chrome/Smoke accents + Dark charcoal text.
* **Forest (Rừng sâu hoang dã)**: Deep forest green (`#0f2e1e`) + Bone (`#f4f1ea`) background + Amber accent.
* **Cobalt + Cream (Cổ điển nổi bật)**: Saturated cobalt blue (`#0047ab`) làm accent duy nhất chống lại nền cream nhẹ hoặc xám trung tính.
* **Terracotta + Slate (Ấm áp tương phản)**: Warm terracotta rust (`#c86446`) đối thoại cùng Slate grey (`#334155`).
* **Monochrome Pop**: Nền đen/trắng tinh khiết (`#000000`/`#ffffff`) + 1 màu accent bão hòa cực mạnh (Emerald, Hot Pink, Electric Blue).

*Quy tắc nhất quán màu*: Một khi đã chọn tone màu cho trang, phải đồng bộ toàn trang. Nút CTA, tag, border, và focus ring phải dùng chung một họ màu accent đã khóa.

---

## 3. 🔡 TYPOGRAPHY PAIRINGS (Cặp Phông Chữ Thiết Kế)
**CẤM MẶC ĐỊNH**: Không sử dụng font `Inter` cho tiêu đề trang lớn trừ khi có yêu cầu cụ thể cho trang thương mại/dịch vụ công. Cấm sử dụng font display serif (`Fraunces` hay `Instrument Serif`) làm phông display mặc định cho mọi dự án sáng tạo.

### Cặp font đề xuất (Chọn 1 cặp cho cả trang):
* **Geist Family (Modern & Tech)**: `Geist Sans` + `Geist Mono`
* **Satoshi + JetBrains (Dev-focus)**: `Satoshi` + `JetBrains Mono`
* **Cabinet Grotesk + Inter (Sleek Display)**: `Cabinet Grotesk` (tiêu đề) + `Inter` (nội dung)
* **Neue Montreal + Mono**: `PP Neue Montreal` (tiêu đề) + `IBM Plex Mono` (nội dung)

### Quy tắc Typography:
* **Display/Headlines**: `text-4xl md:text-6xl tracking-tighter leading-[1.1] font-bold`.
* **Descender Clearance**: Nếu tiêu đề dùng chữ nghiêng (*italic*) và chứa ký tự thò dưới (`y, g, j, p, q`), bắt buộc dùng `leading-[1.1]` trở lên kèm padding-bottom để tránh bị cắt chữ.
* **Body**: `text-base text-gray-600 dark:text-gray-400 leading-relaxed max-w-[65ch]`.

---

## 4. 📐 LAYOUT DISCIPLINE (Quy Tắc Bố Cục Chặt Chẽ)
* **Hero Viewport Stability**: Hero section PHẢI nằm gọn trong khung nhìn đầu tiên. Headline tối đa 2 dòng, subtext tối đa 20 từ (3-4 dòng). CTAs phải hiển thị rõ ràng mà không cần cuộn trang.
* **Hero Top Padding Cap**: Khoảng cách trên cùng của Hero tối đa `pt-24` (desktop) để tránh nội dung bị trôi xuống dưới.
* **Zigzag Alternation Cap**: Tối đa 2 section liên tiếp có bố cục đổi bên trái/phải (`left-image + right-text` rồi đổi ngược). Section thứ 3 phải chuyển sang bento grid, full-width hoặc vertical stack.
* **Eyebrow Restraint**: Uppercase wide-tracking labels (eyebrow) phía trên tiêu đề section chỉ được dùng tối đa **1 lần trên mỗi 3 sections**.
* **Split-Header Ban**: Bố cục "tiêu đề lớn bên trái + một đoạn giải thích nhỏ bên phải" bị cấm dùng làm mặc định. Hãy xếp chồng chúng theo chiều dọc.
* **Bento Cell Count & Rhythm**: Bento grid phải có số ô bằng đúng số lượng nội dung thực tế (không để ô trống). Tối thiểu 2-3 ô trong lưới bento phải có nền khác biệt (ảnh, background màu ấm, pattern) để tạo nhịp điệu trực quan.

---

## 5. 🧱 INTERACTIVE COMPONENTS (Tương Tác & Khung Giao Diện)
* **Shape Consistency**: Đồng bộ bo góc toàn trang. Nếu chọn bo góc tròn mềm (radius 12-16px), toàn bộ card và input phải bo góc mềm. Nút bấm có thể dùng dạng full-pill nhưng phải tuân theo quy tắc nhất quán.
* **Button Contrast Check**: Chữ trên nút CTA phải đạt độ tương phản tối thiểu WCAG AA (4.5:1). Cấm nút trắng chữ trắng, hoặc nút viền mờ tối màu chữ mờ.
* **CTA Button Wrap Ban**: Chữ trên nút bấm CTA chính chỉ được nằm trên 1 dòng duy nhất ở màn hình desktop. Nhãn nút tối đa 3 từ.
* **No Duplicate CTA Intent**: Cấm đặt 2 nút bấm có cùng mục đích (nhưng viết nhãn khác nhau) trên cùng một trang (ví dụ: vừa có "Get in touch" vừa có "Let's talk"). Chọn 1 nhãn thống nhất.
* **Form Contrast**: Ô nhập liệu (inputs), focus ring, và placeholder phải hiển thị rõ ràng trên nền section. Placeholder không được thay thế nhãn input (`label` luôn nằm trên `input`).

---

## 6. ✨ MOTION & PERFORMANCE (Chuyển Động & Hiệu Năng)
* **Bắt buộc Reduced Motion**: Mọi animation kích hoạt khi `MOTION_INTENSITY > 3` phải kiểm tra `prefers-reduced-motion` và hạ cấp xuống giao diện tĩnh tương ứng.
* **Spring Physics**: Chuyển động hover/active phải sử dụng spring physics (`type: "spring", stiffness: 100, damping: 20`) thay vì linear hay ease-in-out thông thường.
* **Cấm Scroll Listener Thủ Công**: Cấm lắng nghe sự kiện `window.addEventListener("scroll")` và tính toán tọa độ cuộn thủ công trong React State. Hãy dùng `GSAP ScrollTrigger` hoặc `motion/react` `useScroll` để tối ưu hóa hiệu năng render.
* **Hardware Acceleration**: Chỉ animate các thuộc tính `transform` và `opacity`. Không animate `top`, `left`, `width`, `height`.

---

## 7. 📸 VISUAL ASSET STRATEGY (Chiến Lược Tài Nguyên Trực Quan)
* **No Div-based Screenshots**: Cấm tự vẽ mockup giao diện/màn hình bằng các thẻ `div` giả lập. Hãy dùng ảnh thật, screenshot thật hoặc component mini thực tế hoạt động được.
* **Logo Wall Wall-Only**: Logo wall đối tác chỉ chứa logo (dùng Simple Icons SVG chất lượng cao). Cấm thêm text giải thích lĩnh vực dưới mỗi logo.
* **Spring-loaded Placeholder**: Khi không có ảnh thật, dùng picsum với seed mô tả cụ thể: `https://picsum.photos/seed/{descriptive-seed}/{w}/{h}`.
