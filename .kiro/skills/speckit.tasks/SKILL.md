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

## When to Use
- Sau khi có `plan.md`, cần breakdown thành tasks atomic có thứ tự dependency.
- **KHÔNG dùng cho**: thiết kế kiến trúc (→ `@speckit.plan`), thực thi task (→ `@speckit.implement`).

## Common Rationalizations
| Lý do bao biện | Sự thật |
|---|---|
| "Gộp nhiều việc vào 1 task cho gọn" | Task lớn khó verify + rollback. Giữ ≤15 phút, ≤3 files. |
| "Verify để khi implement tính" | Task không có lệnh verify thì không biết khi nào xong. Mỗi task có Verify tự động. |
| "Thứ tự task không quan trọng" | Sai thứ tự dependency gây block. Foundation ở Phase 2, task phụ thuộc đặt sau. |
| "File path ghi chung chung" | Task thiếu path cụ thể dễ làm sai chỗ. Luôn ghi đường dẫn rõ. |

## Red Flags
- Task >3 files hoặc >15 phút.
- Task thiếu 1 trong 4 phần: Files / Action / Verify / Done.
- Task không có file path cụ thể; Action mơ hồ.
- Task phụ thuộc đặt trước task nó cần.

## Verification
- [ ] Mọi task ≤15 phút, ảnh hưởng ≤3 files.
- [ ] Mỗi task đủ 4 phần (Files/Action/Verify/Done) với Verify là lệnh tự động.
- [ ] Phase structure đúng: Setup → Foundation → mỗi User Story 1 phase → Polish.
- [ ] Dependency hợp lệ: task phụ thuộc đặt sau; không trùng lặp.
- [ ] `tasks.md` link task ↔ User Scenario.
