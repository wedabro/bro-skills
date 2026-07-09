
---
name: speckit.taskstoissues
description: Issue Tracker Syncer - Synchronize tasks.md to issue tracker.
role: Issue Syncer
---

## 🎯 Mission
Parse tasks.md → create issues ready to import into GitHub/GitLab/Jira.

## 📥 Input
- `.agent/specs/[feature]/tasks.md`

## 📋 Protocol
1. Parse each task → extract: ID, title, description, phase, user story link.
2. Map sang issue format:
   ```markdown
   **Title**: T003 - Implement user registration API
   **Labels**: phase-2, us-1, backend
   **Description**:
   - File: `src/api/auth.ts`
   - Depends on: T002
   - Acceptance: User can register with email/password
   ```
3. Group issues by Phase → create Milestones.
4. Output file `.agent/memory/issues-export.md`.

## 📤 Output
- File: `.agent/memory/issues-export.md`

## 🚫 Guard Rails
- DO NOT create an issue on the remote — just generate an export file.
