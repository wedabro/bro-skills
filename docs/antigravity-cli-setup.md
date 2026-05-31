# Using bro-skills with Antigravity CLI

> Google's agentic coding CLI (formerly Gemini CLI) is now **Antigravity CLI**. This guide replaces the old Gemini CLI setup.

## Setup

### Option 1: Install as Skills (Recommended)

Antigravity CLI auto-discovers `SKILL.md` files in `.antigravity/skills/` (or `.agents/skills/`). Each skill activates on demand when it matches your task.

```bash
# Init the full .agent/ structure first
bro-skills init --target /path/to/project

# Or install skills directly into the workspace skill dir
antigravity skills install /path/to/bro-skills/.agent/skills/
```

- Workspace-scoped skills go into `.antigravity/skills/`.
- User-level skills go into `~/.antigravity/skills/`.

Verify with:

```
/skills list
```

Antigravity CLI injects skill names and descriptions into the prompt automatically. When it recognizes a matching task, it asks permission to activate the skill before loading its full instructions.

### Option 2: AGENTS.md (Persistent Context)

For rules you want always loaded as persistent project context (rather than on-demand activation), use the repo's `AGENTS.md`. Antigravity CLI reads `AGENTS.md` from the project root on every session.

```markdown
# Project Instructions

@.agent/skills/speckit.implement/SKILL.md
@.agent/skills/speckit.reviewer/SKILL.md
```

> **Skills vs AGENTS.md:** Skills are on-demand expertise that activate only when relevant, keeping your context window clean. `AGENTS.md` provides persistent context loaded for every prompt. Use skills for phase-specific workflows and `AGENTS.md` for always-on project conventions.

## Recommended Configuration

### Always-On (AGENTS.md)

Add these as persistent context for every session:

- `speckit.implement` — Build in small verifiable slices (IRONCLAD protocols)
- `speckit.reviewer` — Five-axis review before merge

### On-Demand (Skills)

Install these so they activate only when relevant:

- `speckit.specify` — Activates when starting a new feature
- `speckit.plan` — Activates when designing architecture
- `speckit.tester` — Activates when writing tests or fixing bugs
- `speckit.security` — Activates during security reviews
- `speckit.frontend` / `speckit.backend` — Activate for domain work

## Advanced Configuration

### MCP Integration

Many skills leverage [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) tools. Configure MCP servers in your Antigravity CLI config (`~/.antigravity/config.json` or workspace `.antigravity/mcp.json`).

### Session Hooks

Antigravity CLI supports session lifecycle hooks. Configure a `SessionStart` hook to remind the agent of available skills or load a meta-skill at the start of each session.

### Explicit Context Loading

Load any skill into the current session with the `@` symbol:

```markdown
Use the @.agent/skills/speckit.tester/SKILL.md skill to implement this fix.
```

## Workflows (Slash Commands)

The repo ships workflows under `.agent/workflows/` mapped to the SDD lifecycle. Run from the project root:

| Command | What it does |
|---------|--------------|
| `/01-speckit.constitution` | Establish project law (tech stack, principles) |
| `/02-speckit.specify` | Write a structured spec before code |
| `/03-speckit.clarify` | Resolve ambiguity in the spec |
| `/04-speckit.plan` | Break work into architecture + contracts |
| `/05-speckit.tasks` | Atomic task breakdown (15-Minute Rule) |
| `/07-speckit.implement` | Implement with IRONCLAD protocols |
| `/00-speckit.all` | Full prep pipeline in one command |

## Usage Tips

1. **Prefer skills over AGENTS.md** — Skills activate on demand and keep your context window focused. Only put skills in `AGENTS.md` if you want them always loaded.
2. **Skill descriptions matter** — Each `SKILL.md` has a `description` field that tells the agent when to activate it. Descriptions in this repo state both *what* the skill does and *when* to trigger it.
3. **Respond in Vietnamese** — Per the project constitution, the agent communicates with developers in Vietnamese.
4. **Combine with knowledge base** — Reference `.agent/knowledge_base/` files for project-specific standards.
