---
name: speckit.tasks
description: Task Breaker - Tạo tasks.md atomic, có thứ tự dependency từ plan.
role: Execution Strategist
---

## 🎯 Mission
Chuyển plan.md thành danh sách tasks atomic, có thứ tự dependency, mỗi task ≤15 phút.

## 📥 Input
- `.agent/specs/[feature]/plan.md`
- `.agent/specs/[feature]/spec.md`

## 📋 Protocol
1. Đọc plan.md → breakdown mỗi component thành atomic tasks.
2. Format giải phẫu BẮT BUỘC cho mỗi task (4 thành phần):
   ```markdown
   - [ ] T001 [P] Tiêu đề task
     - Files: Đường dẫn các file bị ảnh hưởng
     - Action: Lệnh thực thi chi tiết, rõ ràng (cấm mơ hồ)
     - Verify: Lệnh kiểm chứng TỰ ĐỘNG (bắt buộc, ví dụ: `npm test`, `curl`)
     - Done: Tiêu chí nghiệm thu cụ thể
   ```
   - `[P]`: Priority (blocking task)
   - `[US1]`: Link đến User Scenario
3. Phase Structure BẮT BUỘC:
   - **Phase 1: Setup** — Project init, configs, boilerplate
   - **Phase 2: Foundation** — DB, auth, shared utilities (blocking)
   - **Phase 3+**: Mỗi User Story = 1 phase (theo priority từ spec)
   - **Final Phase: Polish** — Error handling, optimization, cleanup
4. Dependency Rules:
   - Task phụ thuộc task khác → phải đặt SAU.
   - Foundation tasks luôn ở Phase 2.
5. **15-Minute Rule**: Mỗi task ≤ 15 phút, ảnh hưởng ≤ 3 files.

## 📤 Output
- File: `.agent/specs/[feature]/tasks.md`

## 🚫 Guard Rails
- KHÔNG tạo task quá lớn (>3 files hoặc >15 phút).
- KHÔNG tạo task trùng lặp.
- Mỗi task PHẢI có file path cụ thể.
