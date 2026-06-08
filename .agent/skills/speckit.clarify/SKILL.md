---
name: speckit.clarify
description: Ambiguity Resolver - Phát hiện và giải quyết mơ hồ trong spec.
role: Clarity Engineer
---

## 🎯 Mission
Scan spec.md → phát hiện chỗ mơ hồ → hỏi developer tối đa 3 câu → cập nhật spec.

## 📥 Input
- `.agent/specs/[feature]/spec.md`

## 📋 Protocol
1. Scan spec.md tìm:
   - **Vague language**: "nhanh", "nhiều", "dễ dùng", "tương tự", "v.v."
   - **Missing boundaries**: Không rõ min/max, pagination limits, file size limits
   - **Undefined error handling**: Khi X fail thì sao?
   - **Ambiguous actors**: "User" là ai? Admin? Guest? Registered?
2. Phân loại mỗi issue:
   - 🔴 **CRITICAL**: Ảnh hưởng kiến trúc, PHẢI hỏi developer
   - 🟡 **IMPORTANT**: Nên hỏi nhưng có thể đề xuất mặc định
   - 🟢 **MINOR**: Tự fix được (VD: thêm "tối đa 50 items" nếu thiếu)
3. Hỏi developer TỐI ĐA 3 câu CRITICAL, mỗi câu có bảng options:
   ```
   | Option | Mô tả | Impact |
   |--------|-------|--------|
   | A      | ...   | ...    |
   | B      | ...   | ...    |
   | C      | ...   | ...    |
   ```
4. Auto-fix các items 🟢 MINOR.
5. Cập nhật spec.md với clarifications → đánh dấu `[CLARIFIED]`.

## 📤 Output
- File: Updated `.agent/specs/[feature]/spec.md`

## 🚫 Guard Rails
- TỐI ĐA 3 câu hỏi — không hỏi quá nhiều.
- KHÔNG thay đổi intent gốc của spec.
