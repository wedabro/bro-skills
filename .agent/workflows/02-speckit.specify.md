---
description: Tạo Feature Specification (spec.md)
---

# 📝 Feature Specification

## Pre-conditions
- `.agent/memory/constitution.md` tồn tại

## Steps

1. Developer mô tả feature bằng ngôn ngữ tự nhiên
2. **@speckit.specify** — Parse mô tả → tạo spec.md chuẩn hóa
3. Review output: spec.md phải có Overview, User Scenarios, Requirements, Success Criteria

## Success Criteria
- ✅ spec.md có ≥1 User Scenario
- ✅ Mỗi scenario có Actor + Action + Value
- ✅ Success Criteria là testable
