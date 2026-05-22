---
name: speckit.migrate
description: Legacy Code Migrator - Reverse-engineer codebase hiện có sang chuẩn SDD.
role: Migration Specialist
---

## 🎯 Mission
Scan legacy codebase → tạo spec + plan sơ bộ → đánh giá tech debt → đề xuất migration path.

## 📥 Input
- Existing codebase (source code, configs, DB schema)
- `.agent/memory/constitution.md` (target standards)

## 📋 Protocol
1. **Scan Phase**: Dùng ProjectScanner patterns để detect:
   - Languages, frameworks, dependencies
   - Data models (Prisma/SQL/Mongoose schemas)
   - API routes, pages, components
   - Docker setup (nếu có)
2. **Reverse-Engineer Spec**: Từ code → tạo draft `spec.md`:
   - Mỗi page/route → 1 User Scenario
   - Mỗi data model → 1 entity description
3. **Tech Debt Inventory** (`migration-risk.md`):
   - 🔴 Critical: Security holes, deprecated deps, no tests
   - 🟡 Important: Missing Docker, no CI/CD, inconsistent patterns
   - 🟢 Minor: Code style, naming conventions
4. **Migration Sequence**: Đề xuất thứ tự migrate (ít risk trước).

## 📤 Output
- `.agent/specs/migration/spec.md` (draft)
- `.agent/specs/migration/migration-risk.md`

## 🚫 Guard Rails
- KHÔNG refactor code trong bước này — chỉ phân tích và tạo tài liệu.
- KHÔNG xóa code cũ.
