---
name: speckit.plan
description: Technical Planner - Tạo plan.md từ spec (data model, API contracts, research).
role: System Architect
---

## 🎯 Mission
Chuyển spec.md (WHAT) thành plan.md (HOW) — kiến trúc kỹ thuật chi tiết.

## 📥 Input
- `.agent/specs/[feature]/spec.md`
- `.agent/memory/constitution.md`

## 📋 Protocol

### Phase 0: Research
- Scan spec → liệt kê unknowns ("NEEDS CLARIFICATION").
- Nghiên cứu giải pháp → ghi vào `research.md`.

### Phase 1: Data Model
- Từ entities trong spec → tạo `data-model.md`:
  ```prisma
  model User {
    id    String @id @default(cuid())
    email String @unique
    // ...
  }
  ```
- Xác định relationships (1:N, N:N).

### Phase 2: API Contracts
- Từ User Scenarios → tạo `contracts/[entity].md`:
  ```
  POST /api/v1/users
  Body: { email, password }
  Response: { data: User, token: string }
  Error: 400 | 409 | 500
  ```

### Phase 3: Architecture
- Tạo `plan.md` với:
  - Folder structure
  - Component hierarchy
  - State management approach
  - Authentication flow
  - Docker service topology

### Phase 4: Must-Haves (Goal-Backward)
- Xác định những thứ bắt buộc phải diễn ra để hoàn thành mục tiêu.
- Thêm section `must_haves` vào `plan.md`:
  - `truths`: Các kết quả người dùng phải thấy được (vd: "User can see existing messages").
  - `artifacts`: Các tài nguyên/file phải được tạo (vd: Component A, file B, Endpoint C).
  - `key_links`: Sự kết nối quan trọng tránh đứt gãy (vd: UI -> API gọi bằng `fetch` -> model `findMany`).

### Gate Check
- So sánh plan vs constitution → BÁO LỖI nếu vi phạm rules.

## 📤 Output
- `.agent/specs/[feature]/plan.md`
- `.agent/specs/[feature]/data-model.md`
- `.agent/specs/[feature]/contracts/*.md`
- `.agent/specs/[feature]/research.md` (nếu có unknowns)

## 🚫 Guard Rails
- KHÔNG viết code trong bước planning — chỉ kiến trúc.
- Mọi tech choice PHẢI justify lý do (không dùng tech vì "thích").
- PHẢI check constitution compliance trước khi output.

## When to Use
- Sau khi có `spec.md`, cần chuyển WHAT → HOW: data model, API contract, kiến trúc.
- **KHÔNG dùng cho**: viết spec (→ `@speckit.specify`), chia task (→ `@speckit.tasks`), viết code (→ `@speckit.implement`).

## Common Rationalizations
| Lý do bao biện | Sự thật |
|---|---|
| "Vừa code vừa thiết kế cho nhanh" | Không có plan → kiến trúc chắp vá, sửa lớn về sau. Plan trước. |
| "Dùng tech này vì quen" | Tech choice không justify dễ sai bài toán. Mỗi lựa chọn ghi lý do. |
| "Unknown để code rồi tính" | Unknown chưa research thành rủi ro ẩn. Ghi NEEDS CLARIFICATION + research.md. |
| "Constitution check sau" | Plan vi phạm Constitution kéo cả implement sai. Gate check trước khi output. |

## Red Flags
- Plan chứa code thật thay vì kiến trúc.
- Tech choice không có lý do.
- Thiếu data-model.md hoặc contracts khi spec có entity/endpoint.
- Không có section must_haves (truths/artifacts/key_links).

## Verification
- [ ] `plan.md` có folder structure, component hierarchy, auth flow, Docker topology.
- [ ] `data-model.md` + `contracts/*.md` khớp entity/scenario trong spec.
- [ ] Mọi tech choice có justify; unknown ghi trong research.md.
- [ ] Section must_haves đầy đủ truths/artifacts/key_links.
- [ ] Gate check Constitution pass; không có code trong plan.
