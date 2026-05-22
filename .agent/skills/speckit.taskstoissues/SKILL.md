---
name: speckit.taskstoissues
description: Issue Tracker Syncer - Đồng bộ tasks.md sang issue tracker.
role: Issue Syncer
---

## 🎯 Mission
Parse tasks.md → tạo issues sẵn sàng import vào GitHub/GitLab/Jira.

## 📥 Input
- `.agent/specs/[feature]/tasks.md`

## 📋 Protocol
1. Parse mỗi task → extract: ID, title, description, phase, user story link.
2. Map sang issue format:
   ```markdown
   **Title**: T003 - Implement user registration API
   **Labels**: phase-2, us-1, backend
   **Description**:
   - File: `src/api/auth.ts`
   - Depends on: T002
   - Acceptance: User can register with email/password
   ```
3. Group issues theo Phase → tạo Milestones.
4. Output file `.agent/memory/issues-export.md`.

## 📤 Output
- File: `.agent/memory/issues-export.md`

## 🚫 Guard Rails
- KHÔNG tạo issue trên remote — chỉ generate file export.
