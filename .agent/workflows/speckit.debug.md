---
description: Chẩn đoán và sửa lỗi hệ thống chuyên sâu (Systematic Debugging)
---

# /speckit.debug

Sử dụng skill `speckit.debug` để điều tra nguyên nhân gốc rễ của sự cố.

## Các bước thực hiện:

1. **Thu thập triệu chứng**: Yêu cầu người dùng cung cấp Expected/Actual behavior và Error logs.
2. **Khởi tạo Debug Log**: Tạo file `.agent/debug/[issue].md` để ghi chép.
3. **Phân tích Code**: Sử dụng `grep` và `read` để cô lập vùng nghi ngờ.
4. **Giả thuyết & Kiểm chứng**: Đưa ra các giả thuyết và kiểm tra bằng log/code.
5. **Kết luận Root Cause**: Xác định nguyên nhân và đề xuất fix plan.

// turbo
6. Sử dụng `speckit.implement` để thực hiện bản vá nếu user đồng ý.
