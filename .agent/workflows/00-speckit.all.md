---
description: Full Pipeline (Specify → Clarify → Plan → Tasks → Analyze)
---

# 🚀 Full Pipeline

## Steps

1. **@speckit.map** — (NẾU dự án cũ) Quét cấu trúc và hiểu codebase hiện tại.
   - Output: `.agent/codebase/` docs.

2. **@speckit.specify** — Tạo spec.md từ mô tả feature.
   - Output: `.agent/specs/[feature]/spec.md`.

3. **@speckit.clarify** — Giải quyết mơ hồ và chốt User Scenarios.

4. **@speckit.roadmap** — Cập nhật `.agent/ROADMAP.md` với Phase/Milestone mới.

5. **@speckit.plan** — Tạo kiến trúc (Goal-Backward).
   - Output: plan.md, must_haves.

6. **@speckit.tasks** — Breakdown thành atomic tasks (Task Anatomy).
   - Output: tasks.md.

7. **@speckit.analyze** — Kiểm tra tính nhất quán 360 độ.

## Success Criteria
- ✅ spec.md, plan.md, tasks.md tồn tại và nhất quán
- ✅ Không vi phạm Constitution
