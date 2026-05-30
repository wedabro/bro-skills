# 🤖 bro-skills Configuration (ASF 3.3)

> **Project**: bro-skills
> **Type**: Full-stack (Web + API)
> **Generated**: 2026-02-23

## 🏗️ Architecture

- `.agent/identity/`: Định nghĩa Persona & Soul của AI.
- `.agent/knowledge_base/`: Kho tri thức về Business, Data, API, SEO.
- `.agent/skills/`: Các kỹ năng AI chuyên biệt (@mentions).
- `.agent/workflows/`: Các quy trình tự động hóa (/commands).
- `.agent/memory/`: Project Constitution (Luật dự án).
- `.agent/agents/`: Multi-Agent registry & orchestrator.

## 🧭 Multi-Agent System (v2 — Attribute-based)

Tập agent được chọn **động** theo `project_type` + `attributes` (không phải 1 type phẳng).
Cùng loại dự án nhưng thuộc tính khác → bộ agent khác.

### Công thức
```
active = core_agents
       + base_by_type[project_type]
       + modifiers.architecture[architecture]
       + modifiers.platforms[platform...]
       + modifiers.flags[flag...]
       → unique() (loại trùng)
```

### Khai báo trong `project.json`
```json
{
  "project_type": "fullstack",
  "attributes": {
    "architecture": "monolith",        // monolith | microservice | serverless
    "platforms": ["web"],              // web | ios | android | cross_platform | desktop
    "flags": ["public_facing", "has_backend", "has_persistence", "containerized"]
  }
}
```
Flags hỗ trợ: `public_facing`, `has_backend`, `has_persistence`, `containerized`, `multiplayer`, `has_pii`, `ml`.

### Core Agents (mọi dự án)
constitution · identity · specify · clarify · plan · tasks · analyze · implement · tester · reviewer · validate · **security** · debug · map

### Base theo `project_type`
| project_type | Base agents |
|---|---|
| `fullstack` | frontend · backend · database · uiux |
| `web_public` | frontend · uiux |
| `api_service` | backend · database |
| `wordpress` | wordpress |
| `game` | gamedev |
| `mobile` | _(rỗng — quyết định bởi `platforms`)_ |
| `data_pipeline` | data · database |

### Modifiers (thuộc tính → thêm agent)
| Thuộc tính | Giá trị | Thêm agent |
|---|---|---|
| architecture | `microservice` | devops · database · backend |
| architecture | `serverless` | devops · backend |
| platforms | `web` | frontend · uiux |
| platforms | `ios` | **ios** (Swift native) |
| platforms | `android` | **android** (Kotlin native) |
| platforms | `cross_platform` | **mobile** (RN/Flutter) |
| platforms | `desktop` | frontend |
| flags | `public_facing` | seo · geo · content |
| flags | `has_backend` | backend · database |
| flags | `has_persistence` | database |
| flags | `containerized` | devops |
| flags | `multiplayer` | backend · devops |
| flags | `has_pii` | security · database |
| flags | `ml` | data |

### Ví dụ resolved
| Dự án | Attributes | Agent kích hoạt (ngoài core) |
|---|---|---|
| Webapp công khai | `web_public`, `platforms:[web]`, `public_facing` | frontend · uiux · seo · geo · content — **KHÔNG iOS/Android** |
| Microservice API | `api_service`, `architecture:microservice`, `has_pii` | backend · database · **devops** |
| Mobile chỉ iOS | `mobile`, `platforms:[ios]`, `has_backend` | **ios** · backend · database |
| Mobile iOS + Android | `mobile`, `platforms:[ios,android]` | **ios** · **android** |
| Mobile cross-platform | `mobile`, `platforms:[cross_platform]` | **mobile** (1 codebase) |
| Game multiplayer | `game`, `multiplayer` | gamedev · backend · devops |
| Data + ML | `data_pipeline`, `ml` | data · database |

## 👥 Danh mục Agent chuyên biệt

**Builder (theo domain)**
- `@speckit.frontend` — Frontend (components, state, a11y, web-vitals)
- `@speckit.backend` — Backend/API (REST/GraphQL, authz, business logic)
- `@speckit.database` — Database Architect (schema, index, migration)
- `@speckit.ios` — iOS native (Swift/SwiftUI, Keychain, App Store)
- `@speckit.android` — Android native (Kotlin/Compose, Keystore, Play Store)
- `@speckit.mobile` — Mobile cross-platform (RN/Flutter, offline-first)
- `@speckit.gamedev` — Game (loop, ECS, perf budget, netcode)
- `@speckit.data` — Data/ML Engineer (ETL/ELT, data quality)
- `@speckit.wordpress` — WordPress (theme/plugin, hardening)

**Infra & Security**
- `@speckit.devops` — Docker, CI/CD, port ENV-first (8900-8999)
- `@speckit.security` — Audit OWASP, secret scan, dependency CVE _(core, mọi dự án)_

**Design & Content**
- `@speckit.uiux` — Design System, components, responsive
- `@speckit.seo` — Technical SEO (meta, sitemap, CWV)
- `@speckit.geo` — AI Search (llms.txt, E-E-A-T, Schema.org)
- `@speckit.content` — Content (heading, readability, fact-density)

## 🚀 Quick Start
1. `/01-speckit.constitution` — thiết lập luật dự án.
2. Khai báo `attributes` trong `.agent/project.json`.
3. `/speckit.orchestrate` — kích hoạt multi-agent theo `project_type` + `attributes`.
4. `@speckit.identity` — tinh chỉnh Persona của AI.
5. `/02-speckit.specify` — bắt đầu tính năng mới.
