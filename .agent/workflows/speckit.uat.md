---
description: UAT Analyzer - Phân tích kết quả nghiệm thu thủ công và xử lý các khoảng cách (gaps) từ User.
---

# /speckit.uat

Sử dụng skill `speckit.uat` để kiểm chứng kết quả với người dùng.

## Các bước thực hiện:

1. **Tiếp nhận phản hồi**: User chạy thử app và báo lỗi/thiếu sót.
2. **Ghi nhận Gap**: Lưu vào `.agent/verification/[phase]-UAT.md`.
3. **Phân tích nguyên nhân**: So sánh với Spec.md để tìm ra điểm chưa khớp.
4. **Sinh Fix-Plan**: Tạo danh sách tasks mới để vá các lỗ hổng (Gaps).
5. **Đưa vào Implementation**: Chuyển tasks mới cho `speckit.implement`.
