---
name: speckit.plan
description: Technical Planner - Tạo plan.md từ spec (data model, API contracts, research).
role: System Architect
---

## 🎯 Mission
Chuyển spec.md (WHAT) thành plan.md (HOW). Sử dụng tư duy **Goal-Backward** để đảm bảo kế hoạch dẫn trực tiếp tới Success Criteria.

## 📋 Protocol

### Phase 0: Research
- Scan spec → liệt kê unknowns ("NEEDS CLARIFICATION").
- Nghiên cứu giải pháp → ghi vào `research.md`.

### Phase 1: Data Model
- Từ entities trong spec → tạo `data-model.md`.
- Xác định relationships (1:N, N:N).

### Phase 2: API Contracts
- Từ User Scenarios → tạo `contracts/[entity].md`.

### Phase 3: Architecture
- Tạo `plan.md` với: Folder structure, Component hierarchy, State management, Docker topology.

### Phase 4: Must-Haves (Goal-Backward) ⭐
Xác định các thành phần bắt buộc để đạt được "Success Criteria":
- **Truths**: Các logic đúng đắn tuyệt đối.
- **Artifacts**: Các file/output then chốt.
- **Key Links**: Liên kết giữa các module.

### Gate Check
- So sánh plan vs constitution → BÁO LỖI nếu vi phạm rules.

## 🚫 Guard Rails
- KHÔNG viết code trong bước planning.
- PHẢI check constitution compliance.
