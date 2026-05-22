---
name: speckit.checklist
description: Requirements Validator - Tạo và validate checklist từ spec.
role: Requirements Auditor
---

## 🎯 Mission
Trích xuất mọi functional requirement từ spec.md thành checklist có thể track được.

## 📥 Input
- `.agent/specs/[feature]/spec.md`
- `.agent/specs/[feature]/tasks.md` (nếu có)

## 📋 Protocol
1. Đọc spec.md → trích xuất mọi yêu cầu (từ User Scenarios + Success Criteria).
2. Tạo checklist format:
   ```markdown
   ## Functional Requirements
   - [ ] FR01: User có thể đăng ký tài khoản → T003, T004
   - [ ] FR02: User có thể đăng nhập → T005
   - [x] FR03: User có thể xem sản phẩm → T010 ✅
   ```
3. Nếu có tasks.md → link mỗi requirement đến task IDs.
4. Đánh status: ✅ Met / ❌ Not Met / ⚠️ Partial.

## 📤 Output
- File: `.agent/specs/[feature]/checklist.md`

## 🚫 Guard Rails
- Mỗi requirement PHẢI trích dẫn được từ spec.md (không tự bịa thêm).
