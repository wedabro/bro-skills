---
name: speckit.map
description: Codebase Mapper - Tự động phân tích cấu trúc dự án, vẽ biểu đồ phụ thuộc và viết tài liệu kiến trúc.
role: Technical Lead
---

## 🎯 Mission
Giúp Agent và User nhanh chóng hiểu được toàn bộ "bản đồ" của codebase, đặc biệt là các dự án cũ (Brownfield) hoặc dự án phức tạp.

## 📋 Protocol

### Phase 1: Structure Discovery (Quét cấu trúc)
- Quét toàn bộ thư mục bằng lệnh `tree` hoặc `ls -R`.
- Xác định các Tech Stack cốt lõi (frameworks, databases, libraries).

### Phase 2: Dependency Mapping (Sơ đồ phụ thuộc)
- Phân tích các lệnh `import` hoặc `require` để tìm sự phụ thuộc giữa các modules.
- Lưu kết quả vào `.agent/codebase/STRUCTURE.md`.

### Phase 3: Integration Inventory (Danh mục tích hợp)
- Liệt kê các service bên thứ 3 (API bên ngoài, DB connection).
- Lưu vào `.agent/codebase/INTEGRATIONS.md`.

## 📤 Output Artifacts
- `.agent/codebase/ARCHITECTURE.md`: Tổng quan kiến trúc.
- `.agent/codebase/CONVENTIONS.md`: Các quy ước code đang sử dụng.

## 🚫 Guard Rails
- KHÔNG đọc nội dung tất cả các file cùng lúc để tránh tràn context. Ưu tiên đọc header và exports.
- PHẢI cập nhật lại bản đồ sau mỗi đợt refactor lớn.
