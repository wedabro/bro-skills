---
description: Triển khai code theo tasks (Anti-Regression)
---

# 🛠️ Implementation

## Pre-conditions
- tasks.md tồn tại với tasks chưa complete
- plan.md tồn tại (kiến trúc)
- constitution.md tồn tại (rules)

## Steps

Cho MỖI task `- [ ]` trong tasks.md (theo thứ tự):

1. **@speckit.implement** — Thực thi IRONCLAD Protocols:
   - P1: Blast Radius Analysis → đánh giá risk
   - P2: Strategy Selection → inline edit hoặc Strangler Pattern
   - P3: TDD → repro script fail → code → pass
   - P4: Context Anchoring → re-read constitution mỗi 3 tasks
   - P5: **Build Gate** → chạy `tsc --noEmit` hoặc `docker compose build`
     - Nếu thêm/sửa component props → grep tất cả callers
     - Nếu thêm/sửa type interface → grep tất cả usage
     - Nếu đổi file structure → verify Dockerfile COPY paths
   - P6: **Deviation Rules** → Tự động sửa lỗi/thêm validate/fix blockers phát sinh ngoài plan.
2. Mark `- [X]` khi task pass **VÀ build gate pass**
3. Repeat cho task tiếp theo

## Success Criteria
- ✅ Mọi tasks marked `[X]`
- ✅ Docker build pass
- ✅ Không regression trên tasks đã complete
- ✅ Mọi build gates pass
