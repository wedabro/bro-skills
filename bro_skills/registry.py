"""Registry - Defines all Skills and Workflows for bro-skills.
This is the Single Source of Truth for metadata.

Each skill has a `project_types` field:
  - "all" → Applies to all types of projects
  - "web" → Web project only (Public B2C, SaaS B2B, Full-stack)
  - "web_public" → Web Public project only (B2C with end-user)"""

# ============================================================================
# PROJECT TYPES
# ============================================================================
PROJECT_TYPES = {
    "web_public": {
        "label": "Web Public (B2C)",
        "description": "Landing Page, Blog, E-commerce, News — Need SEO + GEO",
        "includes_skills": ["all", "web", "web_public"],
    },
    "web_saas": {
        "label": "Web SaaS (B2B)",
        "description": "Dashboard, Admin Panel, Internal Tool, API Service — Less SEO required",
        "includes_skills": ["all", "web"],
    },
    "mobile_app": {
        "label": "Mobile App",
        "description": "iOS/Android (React Native, Flutter, Swift, Kotlin) — No SEO, use ASO",
        "includes_skills": ["all"],
    },
    "desktop_cli": {
        "label": "Desktop / CLI Tool",
        "description": "Electron, WPF, CLI — No SEO needed",
        "includes_skills": ["all"],
    },
    "fullstack": {
        "label": "Full-stack (Web + API)",
        "description": "Frontend (Web) + Backend (API) — Foundation for Web + Mobile Apps (Need SEO + GEO + DevOps)",
        "includes_skills": ["all", "web", "web_public"],
    },
    "game": {
        "label": "Game Development",
        "description": "Game (Unity/Unreal/Godot/Phaser) — Game loop, ECS, netcode",
        "includes_skills": ["all"],
    },
    "simple_script": {
        "label": "Simple Script / Automation",
        "description": "Small Python/Bash/JS scripts — No Docker, No Next.js",
        "includes_skills": ["all"],
        "use_docker": False,
        "is_soft_rules": True,
    },
    "custom_infra": {
        "label": "Custom Infrastructure",
        "description": "The project has its own infrastructure — Do not force Docker standard 89XX",
        "includes_skills": ["all"],
        "use_docker": False,
        "is_soft_rules": True,
    },
}


# ============================================================================
# SKILLS REGISTRY
# ============================================================================
SKILLS_REGISTRY = [
    # --- CORE SKILLS (all project types) ---
    {
        "name": "speckit.identity",
        "role": "Persona Architect",
        "description": "Manage AI personality and behavioral orientation for the project.",
        "project_types": "all",
    },
    {
        "name": "speckit.devops",
        "role": "DevOps Architect",
        "description": "Docker Infrastructure & Security Hardening Specialist — Port ENV-first, range 8900-8999.",
        "project_types": "all",
    },
    {
        "name": "speckit.analyze",
        "description": "Consistency Checker - Analyze consistency between spec, plan, tasks",
        "role": "Consistency Analyst",
        "project_types": "all",
        "depends_on": ["speckit.tasks"],
        "handoffs": [
            {"label": "Fix Issues", "agent": "speckit.implement", "prompt": "Fix the consistency issues found"},
        ],
    },
    {
        "name": "speckit.checker",
        "description": "Static Analysis Aggregator - Run static analysis on the codebase",
        "role": "Static Analyst",
        "project_types": "all",
        "depends_on": ["speckit.implement"],
        "handoffs": [
            {"label": "Fix Issues", "agent": "speckit.implement", "prompt": "Fix static analysis issues"},
        ],
    },
    {
        "name": "speckit.checklist",
        "description": "Requirements Validator - Create and validate checklist from spec",
        "role": "Requirements Auditor",
        "project_types": "all",
        "depends_on": ["speckit.specify"],
        "handoffs": [],
    },
    {
        "name": "speckit.clarify",
        "description": "Ambiguity Resolver - Detect and resolve ambiguity in spec",
        "role": "Clarity Engineer",
        "project_types": "all",
        "depends_on": ["speckit.specify"],
        "handoffs": [
            {"label": "Update Spec", "agent": "speckit.specify", "prompt": "Update spec with clarifications"},
        ],
    },
    {
        "name": "speckit.constitution",
        "description": "Governance Manager - Set up & manage Constitution (Source of Law)",
        "role": "Governance Architect",
        "project_types": "all",
        "depends_on": [],
        "handoffs": [
            {"label": "Build Specification", "agent": "speckit.specify", "prompt": "Implement the feature specification based on the updated constitution"},
        ],
    },
    {
        "name": "speckit.diff",
        "description": "Artifact Comparator - Compares differences between artifacts",
        "role": "Diff Analyst",
        "project_types": "all",
        "depends_on": [],
        "handoffs": [],
    },
    {
        "name": "speckit.implement",
        "description": "Code Builder (Anti-Regression) - Deploy code in tasks with IRONCLAD protocols",
        "role": "Master Builder",
        "project_types": "all",
        "depends_on": ["speckit.tasks"],
        "handoffs": [
            {"label": "Run Tests", "agent": "speckit.tester", "prompt": "Run tests for implemented code"},
            {"label": "Review Code", "agent": "speckit.reviewer", "prompt": "Review the implementation"},
        ],
    },
    {
        "name": "speckit.migrate",
        "description": "Legacy Code Migrator - Convert legacy code to the new standard",
        "role": "Migration Specialist",
        "project_types": "all",
        "depends_on": [],
        "handoffs": [
            {"label": "Create Spec", "agent": "speckit.specify", "prompt": "Create spec from migrated codebase"},
        ],
    },
    {
        "name": "speckit.plan",
        "description": "Technical Planner - Create plan.md from spec (data model, API contracts, research)",
        "role": "System Architect",
        "project_types": "all",
        "depends_on": ["speckit.specify"],
        "handoffs": [
            {"label": "Create Tasks", "agent": "speckit.tasks", "prompt": "Break the plan into tasks"},
            {"label": "Create Checklist", "agent": "speckit.checklist", "prompt": "Create a checklist"},
        ],
    },
    {
        "name": "speckit.quizme",
        "description": "Logic Challenger (Red Team) - Ask critical questions, find edge cases",
        "role": "Red Team Analyst",
        "project_types": "all",
        "depends_on": ["speckit.specify"],
        "handoffs": [],
    },
    {
        "name": "speckit.reviewer",
        "description": "Code Reviewer - Review code according to spec and best practices",
        "role": "Code Reviewer",
        "project_types": "all",
        "depends_on": ["speckit.implement"],
        "handoffs": [
            {"label": "Fix Issues", "agent": "speckit.implement", "prompt": "Fix review issues"},
        ],
    },
    {
        "name": "speckit.specify",
        "description": "Feature Definer - Generates spec.md from natural language description",
        "role": "Domain Scribe",
        "project_types": "all",
        "depends_on": [],
        "handoffs": [
            {"label": "Build Technical Plan", "agent": "speckit.plan", "prompt": "Create a plan for the spec"},
            {"label": "Clarify Requirements", "agent": "speckit.clarify", "prompt": "Clarify specification requirements"},
        ],
    },
    {
        "name": "speckit.status",
        "description": "Progress Dashboard - Displays project progress status",
        "role": "Progress Tracker",
        "project_types": "all",
        "depends_on": ["speckit.tasks"],
        "handoffs": [],
    },
    {
        "name": "speckit.tasks",
        "description": "Task Breaker - Create atomic tasks.md, with dependency order from plan",
        "role": "Execution Strategist",
        "project_types": "all",
        "depends_on": ["speckit.plan"],
        "handoffs": [
            {"label": "Analyze Consistency", "agent": "speckit.analyze", "prompt": "Run consistency analysis"},
            {"label": "Implement", "agent": "speckit.implement", "prompt": "Start the implementation"},
        ],
    },
    {
        "name": "speckit.taskstoissues",
        "description": "Issue Tracker Syncer - Synchronize tasks.md to issue tracker",
        "role": "Issue Syncer",
        "project_types": "all",
        "depends_on": ["speckit.tasks"],
        "handoffs": [],
    },
    {
        "name": "speckit.tester",
        "description": "Test Runner & Coverage - Run tests and report coverage",
        "role": "Test Engineer",
        "project_types": "all",
        "depends_on": ["speckit.implement"],
        "handoffs": [
            {"label": "Fix Failures", "agent": "speckit.implement", "prompt": "Fix test failures"},
        ],
    },
    {
        "name": "speckit.validate",
        "description": "Implementation Validator - Validate implementation vs overall spec",
        "role": "Validation Oracle",
        "project_types": "all",
        "depends_on": ["speckit.implement"],
        "handoffs": [],
    },

    # --- WEB SKILLS (web + web_public projects) ---
    {
        "name": "speckit.seo",
        "description": "Technical SEO - Meta tags, Sitemap, Robots.txt, Canonical, Core Web Vitals, Schema.org",
        "role": "SEO Technical Lead",
        "project_types": "web",
        "depends_on": ["speckit.implement"],
        "handoffs": [
            {"label": "Audit GEO", "agent": "speckit.geo", "prompt": "Run GEO audit on the content"},
            {"label": "Fix Issues", "agent": "speckit.implement", "prompt": "Fix SEO issues found"},
        ],
    },
    {
        "name": "speckit.geo",
        "description": "Generative Engine Optimization - llms.txt, E-E-A-T, FAQ Schema, AI Citation, Topic Authority",
        "role": "GEO Strategist",
        "project_types": "web",
        "depends_on": ["speckit.seo"],
        "handoffs": [
            {"label": "Update Content", "agent": "speckit.content", "prompt": "Optimize content for AI citation"},
        ],
    },
    {
        "name": "speckit.content",
        "description": "Content Architect - Heading H1-H6, Readability, Multimodal (Image Alt, Video), Fact-density",
        "role": "Content Strategist",
        "project_types": "web_public",
        "depends_on": ["speckit.specify"],
        "handoffs": [
            {"label": "SEO Check", "agent": "speckit.seo", "prompt": "Validate SEO compliance of content"},
        ],
    },
    {
        "name": "speckit.uiux",
        "description": "UI/UX Architect - Definition of Design System, UI Components, Spacing, Typography, Responsive Patterns.",
        "role": "UI/UX Architect",
        "project_types": "web",
        "depends_on": ["speckit.specify"],
        "handoffs": [
            {"label": "Update Plan", "agent": "speckit.plan", "prompt": "Integrate UI/UX specs into the technical plan"},
        ],
    },
    {
        "name": "speckit.debug",
        "description": "Systematic Debugger - Diagnose problems, find individual root causes, and recommend fix plans.",
        "role": "Debug Specialist",
        "project_types": "all",
    },
    {
        "name": "speckit.backlog",
        "description": "Backlog Manager - Manage Ideas, Pending Requests and scan TODO/FIXME from codebase.",
        "role": "Product Owner",
        "project_types": "all",
    },
    {
        "name": "speckit.roadmap",
        "description": "Roadmap Strategist - Manage high-level roadmaps (Milestones) and transitions between Phases.",
        "role": "Product Manager",
        "project_types": "all",
    },
    {
        "name": "speckit.map",
        "description": "Codebase Mapper - Automatically analyze project structure, draw dependency diagrams, and write architectural documents.",
        "role": "Software Architect",
        "project_types": "all",
    },
    {
        "name": "speckit.uat",
        "description": "UAT Analyzer - Analyze manual acceptance results and process gaps from the User.",
        "role": "QA Engineer",
        "project_types": "all",
    },
    {
        "name": "speckit.wordpress",
        "description": "WordPress Theme Architect - Expert in developing themes, plugins and optimizing the WordPress ecosystem.",
        "role": "WordPress Expert",
        "project_types": "web",
    },
    {
        "name": "speckit.3d",
        "description": "3D Specialist - 3D modeling, WebGL/Three.js/React Three Fiber, Unity/Unreal Engine 3D integration, shaders, optimization.",
        "role": "3D Architect & Developer",
        "project_types": "builder",
    },

    # ========================================================================
    # MULTI-AGENT BUILDERS (v2 — Attribute-based selection)
    # `project_types: "builder"` → DO NOT select past the old filter tag.
    # Select via attribute resolver (resolve_builder_skills) according to project type +
    # attributes (architecture / platforms / flags).
    # As for speckit.security tag "all" → core, applies to EVERY project.
    # ========================================================================
    {
        "name": "speckit.security",
        "description": "Security Auditor - Audit AppSec theo OWASP, secret scanning, dependency/vuln, threat modeling.",
        "role": "Security Auditor",
        "project_types": "all",
    },
    {
        "name": "speckit.backend",
        "description": "Backend/API Developer - Build API services, business logic, auth, integration.",
        "role": "Backend Engineer",
        "project_types": "builder",
    },
    {
        "name": "speckit.frontend",
        "description": "Frontend Developer - UI components, state management, data fetching, accessibility, performance.",
        "role": "Frontend Engineer",
        "project_types": "builder",
    },
    {
        "name": "speckit.database",
        "description": "Database Architect - Schema, index, migration, query optimization, data integrity.",
        "role": "Database Architect",
        "project_types": "builder",
    },
    {
        "name": "speckit.ios",
        "description": "iOS Developer - Native iOS (Swift/SwiftUI), lifecycle, App Store compliance, Keychain.",
        "role": "iOS Engineer",
        "project_types": "builder",
    },
    {
        "name": "speckit.android",
        "description": "Android Developer - Native Android (Kotlin/Compose), lifecycle, Play Store compliance, Keystore.",
        "role": "Android Engineer",
        "project_types": "builder",
    },
    {
        "name": "speckit.mobile",
        "description": "Mobile Developer - Cross-platform (React Native/Flutter), offline-first, store compliance.",
        "role": "Mobile Engineer",
        "project_types": "builder",
    },
    {
        "name": "speckit.data",
        "description": "Data/ML Engineer - Data pipeline (ETL/ELT), data quality, ML workflow, orchestration.",
        "role": "Data Engineer",
        "project_types": "builder",
    },
    {
        "name": "speckit.gamedev",
        "description": "Game Developer - Engine, gameplay loop, physics, asset pipeline, netcode, performance.",
        "role": "Game Developer",
        "project_types": "builder",
    },
    {
        "name": "k8s-manifest-generator",
        "description": "Create production-ready Kubernetes manifests for Deployments, Services, ConfigMaps, and Secrets.",
        "role": "Kubernetes Architect",
        "project_types": "builder",
    },
    {
        "name": "async-python-patterns",
        "description": "Python asynchronous programming patterns, concurrency, asyncio, and performance optimization.",
        "role": "Async Python Expert",
        "project_types": "builder",
    },
    {
        "name": "backend-architect",
        "description": "Expert backend architect specializing in scalable API design, microservices, and distributed systems.",
        "role": "Backend Architect",
        "project_types": "builder",
    },
    {
        "name": "security-auditor",
        "description": "Security auditor specializing in code auditing, threat modeling, and vulnerability scanning.",
        "role": "Security Auditor",
        "project_types": "builder",
    },
    {
        "name": "full-stack-orchestration-full-stack-feature",
        "description": "Full-stack feature orchestration and coordination patterns.",
        "role": "Orchestration Engineer",
        "project_types": "builder",
    },
    {
        "name": "conductor-implement",
        "description": "Conductor workflow management and structured feature implementation.",
        "role": "Conductor Specialist",
        "project_types": "builder",
    },
    {
        "name": "ponytail",
        "description": "Forces the laziest solution that actually works, simplest, shortest, most minimal. Channels a senior dev who has seen everything: YAGNI, standard library first, native platform features, one line before fifty.",
        "role": "Lazy Senior Developer",
        "project_types": "all",
    },
]


# ============================================================================
# WORKFLOWS REGISTRY
# ============================================================================
WORKFLOWS_REGISTRY = [
    {
        "command": "00-speckit.all",
        "description": "Full Pipeline (Specify → Clarify → Plan → Tasks → Analyze)",
        "skills": ["speckit.specify", "speckit.clarify", "speckit.plan", "speckit.tasks", "speckit.analyze"],
    },
    {
        "command": "01-speckit.constitution",
        "description": "Establish/update Constitution (Source of Law)",
        "skills": ["speckit.constitution"],
    },
    {
        "command": "speckit.identity",
        "description": "Create/update Master Identity for AI Agent",
        "skills": ["speckit.identity"],
    },
    {
        "command": "speckit.devops",
        "description": "Docker Infrastructure & Port Allocation (ENV-first)",
        "skills": ["speckit.devops"],
    },
    {
        "command": "02-speckit.specify",
        "description": "Create Feature Specification (spec.md)",
        "skills": ["speckit.specify"],
    },
    {
        "command": "03-speckit.clarify",
        "description": "Resolve ambiguity in Specification",
        "skills": ["speckit.clarify"],
    },
    {
        "command": "04-speckit.plan",
        "description": "Create Technical Plan (plan.md)",
        "skills": ["speckit.plan"],
    },
    {
        "command": "05-speckit.tasks",
        "description": "Create Task Breakdown (tasks.md)",
        "skills": ["speckit.tasks"],
    },
    {
        "command": "06-speckit.analyze",
        "description": "Analyze consistency between artifacts",
        "skills": ["speckit.analyze"],
    },
    {
        "command": "07-speckit.implement",
        "description": "Deploy code according to tasks (Anti-Regression)",
        "skills": ["speckit.implement"],
    },
    {
        "command": "08-speckit.checker",
        "description": "Run Static Analysis",
        "skills": ["speckit.checker"],
    },
    {
        "command": "09-speckit.tester",
        "description": "Run Tests & Coverage",
        "skills": ["speckit.tester"],
    },
    {
        "command": "10-speckit.reviewer",
        "description": "Code Review",
        "skills": ["speckit.reviewer"],
    },
    {
        "command": "11-speckit.validate",
        "description": "Validate Implementation vs Spec",
        "skills": ["speckit.validate"],
    },
    {
        "command": "12-speckit.seo",
        "description": "Technical SEO Audit & Optimization",
        "skills": ["speckit.seo"],
        "project_types": "web",
    },
    {
        "command": "13-speckit.geo",
        "description": "GEO - Optimized for AI Search (ChatGPT, Gemini, Perplexity)",
        "skills": ["speckit.geo"],
        "project_types": "web",
    },
    {
        "command": "speckit.prepare",
        "description": "Prep Pipeline (Specify → Clarify → Plan → Tasks → Analyze)",
        "skills": ["speckit.specify", "speckit.clarify", "speckit.plan", "speckit.tasks", "speckit.analyze"],
    },
    {
        "command": "util-speckit.checklist",
        "description": "Create/validate Requirements Checklist",
        "skills": ["speckit.checklist"],
    },
    {
        "command": "util-speckit.content",
        "description": "Content Strategy & Readability Audit",
        "skills": ["speckit.content"],
        "project_types": "web_public",
    },
    {
        "command": "util-speckit.diff",
        "description": "Compare Artifacts (Spec vs Implementation)",
        "skills": ["speckit.diff"],
    },
    {
        "command": "util-speckit.migrate",
        "description": "Migrate Legacy Code",
        "skills": ["speckit.migrate"],
    },
    {
        "command": "util-speckit.quizme",
        "description": "Red Team - Ask critical questions to find edge cases",
        "skills": ["speckit.quizme"],
    },
    {
        "command": "util-speckit.status",
        "description": "Display Progress Dashboard",
        "skills": ["speckit.status"],
    },
    {
        "command": "util-speckit.uiux",
        "description": "Set up/update UI/UX Design System & Standards",
        "skills": ["speckit.uiux"],
        "project_types": "web",
    },
    {
        "command": "util-speckit.taskstoissues",
        "description": "Sync tasks.md → Issue Tracker",
        "skills": ["speckit.taskstoissues"],
    },
    {
        "command": "speckit.debug",
        "description": "Systematic Debugging",
        "skills": ["speckit.debug"],
    },
    {
        "command": "speckit.backlog",
        "description": "Managing Ideas (Backlog) and scanning technical debt (TODO/FIXME)",
        "skills": ["speckit.backlog"],
    },
    {
        "command": "speckit.roadmap",
        "description": "Manage high-level roadmaps (Milestones) and transitions between Phases",
        "skills": ["speckit.roadmap"],
    },
    {
        "command": "speckit.map",
        "description": "Draw the architecture map and dependency diagram of the Codebase",
        "skills": ["speckit.map"],
    },
    {
        "command": "speckit.uat",
        "description": "UAT Analyzer - Analyze manual acceptance results and process gaps from the User.",
        "skills": ["speckit.uat"],
    },
    {
        "command": "speckit.wordpress",
        "description": "WordPress Theme & Plugin Development Workflow",
        "skills": ["speckit.wordpress"],
        "project_types": "web",
    },
    {
        "command": "speckit.orchestrate",
        "description": "Multi-Agent Orchestration - Select & coordinate agents by project_type + attributes",
        "skills": ["speckit.specify", "speckit.plan", "speckit.tasks", "speckit.implement"],
    },
    {
        "command": "speckit.gamedev",
        "description": "Game Development Pipeline - Engine setup, game loop, performance, asset pipeline",
        "skills": ["speckit.gamedev", "speckit.uiux"],
    },
    {
        "command": "speckit.3d",
        "description": "3D Modeling, Web 3D & Game 3D Workflow",
        "skills": ["speckit.3d"],
    },
    {
        "command": "full-stack-orchestration-full-stack-feature",
        "description": "Full-Stack Feature Orchestration Workflow",
        "skills": ["full-stack-orchestration-full-stack-feature"],
    },
    {
        "command": "conductor-implement",
        "description": "Conductor Feature Implementation Workflow",
        "skills": ["conductor-implement"],
    },
]


# ============================================================================
# MULTI-AGENT ATTRIBUTE-BASED SELECTION (v2)
# ============================================================================
# active_builders = BASE_BUILDERS_BY_TYPE[type]
#                 + MODIFIERS.architecture[arch]
#                 + MODIFIERS.platforms[p...]
#                 + MODIFIERS.flags[f...]
# The Orchestrator coordinates these builders according to the Task Tag (@agent:).
# ----------------------------------------------------------------------------

# Default Builder according to project_type
BASE_BUILDERS_BY_TYPE = {
    "web_public":   ["speckit.frontend", "speckit.uiux"],
    "web_saas":     ["speckit.frontend", "speckit.backend", "speckit.database", "speckit.uiux"],
    "fullstack":    ["speckit.frontend", "speckit.backend", "speckit.database", "speckit.uiux"],
    "mobile_app":   [],  # decided by platforms
    "game":         ["speckit.gamedev"],
    "desktop_cli":  ["speckit.frontend"],
    "simple_script": [],
    "custom_infra": [],
}

# Modifiers: project properties → add builder
MODIFIERS = {
    "architecture": {
        "monolith": [],
        "microservice": ["speckit.devops", "speckit.database", "speckit.backend"],
        "serverless": ["speckit.devops", "speckit.backend"],
    },
    "platforms": {
        "web": ["speckit.frontend", "speckit.uiux"],
        "ios": ["speckit.ios"],
        "android": ["speckit.android"],
        "cross_platform": ["speckit.mobile"],
        "desktop": ["speckit.frontend"],
    },
    "flags": {
        "public_facing": ["speckit.seo", "speckit.geo", "speckit.content"],
        "has_backend": ["speckit.backend", "speckit.database"],
        "has_persistence": ["speckit.database"],
        "containerized": ["speckit.devops"],
        "multiplayer": ["speckit.backend", "speckit.devops"],
        "has_pii": ["speckit.security", "speckit.database"],
        "ml": ["speckit.data"],
        "3d": ["speckit.3d"],
    },
}

# Only resolve builder skills that actually exist in the registry
_BUILDER_SKILL_NAMES = {
    s["name"] for s in SKILLS_REGISTRY
    if s.get("project_types") == "builder"
}


def resolve_builder_skills(project_type, attributes=None):
    """Resolve builder skill list by project_type + attributes.

    attributes = {
        "architecture": "monolith" | "microservices" | "serverless",
        "platforms": ["web", "ios", "android", "cross_platform", "desktop"],
        "flags": ["public_facing", "has_backend", ...]
    }
    Returns a list of skill names (duplicates removed, only builder skills that exist)."""
    selected = []
    selected.extend(BASE_BUILDERS_BY_TYPE.get(project_type, []))

    attrs = attributes or {}

    arch = attrs.get("architecture")
    if arch:
        selected.extend(MODIFIERS["architecture"].get(arch, []))

    for p in attrs.get("platforms", []) or []:
        selected.extend(MODIFIERS["platforms"].get(p, []))

    for f in attrs.get("flags", []) or []:
        selected.extend(MODIFIERS["flags"].get(f, []))

    # Same type, keep order; Just keep the skill builder alive in the registry
    seen = set()
    result = []
    for name in selected:
        if name in _BUILDER_SKILL_NAMES and name not in seen:
            seen.add(name)
            result.append(name)
    return result


def get_skills_for_project_type(project_type, attributes=None):
    """Filter skills appropriate to project type.

    Consists of 2 parts:
      1. Tag-based (legacy): skills have project_types in includes_skills (all/web/web_public).
         Builder skills (project_types == "builder") are removed from this branch.
      2. Attribute-based (v2): builder skills resolve by project_type + attributes."""
    if project_type not in PROJECT_TYPES:
        return SKILLS_REGISTRY  # fallback: return all

    type_info = PROJECT_TYPES[project_type]
    allowed = type_info["includes_skills"]

    # 1. Tag-based core/web skills (NOT includes builder)
    tagged = [
        s for s in SKILLS_REGISTRY
        if s.get("project_types", "all") in allowed
        and s.get("project_types") != "builder"
    ]

    # 2. Attribute-based builder skills
    builder_names = resolve_builder_skills(project_type, attributes)
    builders = [s for s in SKILLS_REGISTRY if s["name"] in builder_names]

    # Merge, keep registry order, eliminate duplicates
    seen = set()
    result = []
    for s in tagged + builders:
        if s["name"] not in seen:
            seen.add(s["name"])
            result.append(s)
    return result


def get_project_type_info(project_type):
    """Get the metadata of the project type."""
    return PROJECT_TYPES.get(project_type, {
        "label": "Unknown",
        "use_docker": True,
        "is_soft_rules": False
    })


def get_workflows_for_project_type(project_type):
    """Filter workflows by project type."""
    if project_type not in PROJECT_TYPES:
        return WORKFLOWS_REGISTRY

    allowed = PROJECT_TYPES[project_type]["includes_skills"]
    return [w for w in WORKFLOWS_REGISTRY if w.get("project_types", "all") in allowed]

