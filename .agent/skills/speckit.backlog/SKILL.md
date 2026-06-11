---
name: speckit.backlog
description: Backlog Manager - Manage Ideas, Pending Requests and scan TODO/FIXME from codebase.
role: Product Owner Assistant
---

## 🎯 Mission
Organize and prioritize unfulfilled requirements, ensuring no ideas or bugs are missed during long-term development.

## 📋 Protocol

### Phase 1: Idea Scoping (Idea recording)
- When a user makes a request that they don't want to do right away, save it to `.agent/backlog/IDEAS.md` .
- Each idea needs: Description, Priority (Low/Med/High), Status (Pending).

### Phase 2: Automated Todo Scan (Scan source code)
- Use the command `grep` to find the keywords: `TODO:` , `FIXME:` , `HACK:` , `BUG:` .
- Summarize the results found into `.agent/backlog/TECHNICAL_DEBT.md` .

### Phase 3: Backlog Grooming (Backlog filtering)
- Periodically review items in the backlog to convert to `spec.md` when the user is ready to deploy.

## 🚫 Guard Rails
- DO NOT arbitrarily delete the backlog without asking the user.
- DO NOT overflow the context by listing thousands of TODOs. Only list tasks related to the area you are working on.
