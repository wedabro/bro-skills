---
name: speckit.taskstoissues
description: Issue Tracker Syncer - Äá»“ng bá»™ tasks.md sang issue tracker.
role: Issue Syncer
---

## ðŸŽ¯ Mission
Parse tasks.md â†’ táº¡o issues sáºµn sÃ ng import vÃ o GitHub/GitLab/Jira.

## ðŸ“¥ Input
- `.agent/specs/[feature]/tasks.md`

## ðŸ“‹ Protocol
1. Parse má»—i task â†’ extract: ID, title, description, phase, user story link.
2. Map sang issue format:
   ```markdown
   **Title**: T003 - Implement user registration API
   **Labels**: phase-2, us-1, backend
   **Description**:
   - File: `src/api/auth.ts`
   - Depends on: T002
   - Acceptance: User can register with email/password
   ```
3. Group issues theo Phase â†’ táº¡o Milestones.
4. Output file `.agent/memory/issues-export.md`.

## ðŸ“¤ Output
- File: `.agent/memory/issues-export.md`

## ðŸš« Guard Rails
- KHÃ”NG táº¡o issue trÃªn remote â€” chá»‰ generate file export.

## When to Use
- Khi cáº§n chuyá»ƒn tasks.md thÃ nh file export issue (GitHub/GitLab/Jira).
- **KHÃ”NG dÃ¹ng cho**: chia task (â†’ `@speckit.tasks`), táº¡o issue trá»±c tiáº¿p trÃªn remote.

## Common Rationalizations
| LÃ½ do bao biá»‡n | Sá»± tháº­t |
|---|---|
| "Táº¡o issue tháº³ng trÃªn remote cho nhanh" | Skill chá»‰ generate file export, khÃ´ng táº¡o issue remote. |
| "Khá»i link dependency/user story" | Thiáº¿u link lÃ m máº¥t ngá»¯ cáº£nh. Map Ä‘á»§ phase/label/dependency. |

## Red Flags
- Táº¡o issue trá»±c tiáº¿p trÃªn remote tracker.
- Issue thiáº¿u label/phase/dependency/acceptance.

## Verification
- [ ] Má»—i task map sang issue: ID, title, description, label, dependency, acceptance.
- [ ] Issue group theo Phase â†’ Milestone.
- [ ] Output `issues-export.md`; khÃ´ng táº¡o issue remote.
