# Using bro-skills with Kiro IDE & CLI

> Kiro stores skills under `.kiro/skills/` (project-level) or `~/.kiro/skills/` (global). Kiro also reads `AGENTS.md`, supports steering files, agent hooks, and MCP. See the [Kiro docs](https://kiro.dev/docs/skills/).

## Setup

### Option 1: Install as Skills (Recommended)

Kiro auto-discovers `SKILL.md` files in `.kiro/skills/`. Each skill activates on demand when its `description` matches your task.

```bash
# Init the full .agent/ structure
bro-skills init --target /path/to/project

# Mirror skills into the Kiro skill dir
# (this repo already ships .kiro/skills/ in sync with .agent/skills/)
```

- **Project-level**: `.kiro/skills/<skill-name>/SKILL.md`
- **Global**: `~/.kiro/skills/<skill-name>/SKILL.md`

Each skill needs valid frontmatter (`name` + `description`) so Kiro can discover it:

```yaml
---
name: speckit.specify
description: Feature Definer - Tạo spec.md từ mô tả ngôn ngữ tự nhiên.
role: Domain Scribe
---
```

### Option 2: AGENTS.md + Steering (Persistent Context)

Kiro reads `AGENTS.md` from the project root and steering files from `.kiro/steering/*.md`.

- **AGENTS.md** — always-on project rules (this repo ships one with the bro-skills protocol).
- **Steering** — scoped guidance. Front-matter controls inclusion:
  - `inclusion: always` (default) — loaded every session
  - `inclusion: fileMatch` + `fileMatchPattern: 'README*'` — loaded when a matching file is in context
  - `inclusion: manual` — loaded only when referenced via `#` in chat

> **Skills vs Steering:** Skills are on-demand expertise that activate only when relevant. Steering/AGENTS.md provide persistent context. Use skills for phase-specific workflows and steering for always-on conventions.

## Agent Hooks

Kiro can trigger agent actions automatically on IDE events. This repo ships hooks under `.kiro/hooks/*.kiro.hook` that map the SDD pipeline to manual triggers, plus an auto-commit hook.

| Hook | Trigger | Action |
|------|---------|--------|
| Speckit: Constitution | userTriggered | Run `/01-speckit.constitution` |
| Speckit: Specify | userTriggered | Run `/02-speckit.specify` |
| Speckit: Plan | userTriggered | Run `/04-speckit.plan` |
| Speckit: Tasks | userTriggered | Run `/05-speckit.tasks` |
| Speckit: Implement | userTriggered | Run `/07-speckit.implement` (commits each task) |
| Speckit: Full Pipeline | userTriggered | Run the full `00-speckit.all` pipeline |
| Speckit: Auto Commit | postTaskExecution | Atomic git commit when a task completes |

Hook file schema (`.kiro/hooks/<id>.kiro.hook`):

```json
{
  "enabled": true,
  "name": "Speckit: Specify",
  "description": "Tạo spec.md từ mô tả feature",
  "version": "1",
  "when": { "type": "userTriggered" },
  "then": {
    "type": "askAgent",
    "prompt": "Đọc và thực thi `.agent/workflows/02-speckit.specify.md`..."
  }
}
```

Manage hooks via the **Agent Hooks** section in the Kiro explorer, or the command palette → "Open Kiro Hook UI".

## MCP Integration

Configure MCP servers per workspace at `.kiro/settings/mcp.json` or globally at `~/.kiro/settings/mcp.json`. This repo ships a `codegraph` server:

```json
{
  "mcpServers": {
    "codegraph": {
      "type": "stdio",
      "command": "codegraph",
      "args": ["serve", "--mcp"]
    }
  }
}
```

Reconnect servers from the MCP Server view in the Kiro feature panel after editing config — no restart required.

## Recommended Configuration

### Always-On (AGENTS.md / steering)

- bro-skills protocol (Specify → Plan → Tasks → Implement)
- Docker-First + port range 8900-8999
- Respond to developers in Vietnamese

### On-Demand (Skills)

- `speckit.specify`, `speckit.plan`, `speckit.tasks`, `speckit.implement` — core pipeline
- `speckit.security`, `speckit.reviewer`, `speckit.tester`, `speckit.validate` — quality gates
- `speckit.frontend`, `speckit.backend`, `speckit.database`, `speckit.uiux` — fullstack domain

## Usage Tips

1. **Keep `.agent/skills/` and `.kiro/skills/` in sync** — this repo mirrors both; if you edit one, update the other.
2. **Skill descriptions matter** — the `description` field drives auto-discovery. State both *what* and *when*.
3. **Use hooks for the pipeline** — trigger Speckit workflows from the Agent Hooks panel instead of typing commands.
4. **Auto-commit on task done** — the postTaskExecution hook keeps commits atomic (one task = one commit).
