"""
Registry - Định nghĩa tất cả Skills và Workflows cho bro-agent.
Đây là nguồn sự thật duy nhất (Single Source of Truth) cho metadata.

Mỗi skill có trường `project_types`:
  - "all"       → Áp dụng cho mọi loại dự án
  - "web"       → Chỉ dự án Web (Public B2C, SaaS B2B, Full-stack)
  - "web_public" → Chỉ dự án Web Public (B2C có end-user)
"""

# ============================================================================
# PROJECT TYPES
# ============================================================================
PROJECT_TYPES = {
    "web_public": {
        "label": "Web Public (B2C)",
        "description": "Blog, E-commerce, Landing Page, News — Cần SEO + GEO",
        "includes_skills": ["all", "web", "web_public"],
    },
    "web_saas": {
        "label": "Web SaaS (B2B)",
        "description": "Dashboard, Admin Panel, API Service — SEO cho Landing/Blog",
        "includes_skills": ["all", "web"],
    },
    "mobile_app": {
        "label": "Mobile App",
        "description": "iOS/Android — Không cần SEO, dùng ASO",
        "includes_skills": ["all"],
    },
    "desktop_cli": {
        "label": "Desktop / CLI Tool",
        "description": "Electron, WPF, CLI — Không cần SEO",
        "includes_skills": ["all"],
    },
    "fullstack": {
        "label": "Full-stack (Web + API)",
        "description": "Frontend Public + Backend API — Cần SEO + GEO + DevOps",
        "includes_skills": ["all", "web", "web_public"],
    },
    "simple_script": {
        "label": "Simple Script / Automation",
        "description": "Python/Bash/JS scripts nhỏ — Không Docker, Không Next.js",
        "includes_skills": ["all"],
        "use_docker": False,
        "is_soft_rules": True,
    },
    "custom_infra": {
        "label": "Custom Infrastructure",
        "description": "Dự án có hạ tầng riêng — Không ép Docker chuẩn 89XX",
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
        "description": "Quản lý nhân cách và định hướng hành vi của AI cho dự án.",
        "project_types": "all",
    },
    {
        "name": "speckit.devops",
        "role": "DevOps Architect",
        "description": "Chuyên gia hạ tầng Docker & Security Hardening — Port ENV-first, dải 8900-8999.",
        "project_types": "all",
    },
    {
        "name": "speckit.analyze",
        "description": "Consistency Checker - Phân tích tính nhất quán giữa spec, plan, tasks",
        "role": "Consistency Analyst",
        "project_types": "all",
        "depends_on": ["speckit.tasks"],
        "handoffs": [
            {"label": "Fix Issues", "agent": "speckit.implement", "prompt": "Fix the consistency issues found"},
        ],
    },
    {
        "name": "speckit.checker",
        "description": "Static Analysis Aggregator - Chạy static analysis trên codebase",
        "role": "Static Analyst",
        "project_types": "all",
        "depends_on": ["speckit.implement"],
        "handoffs": [
            {"label": "Fix Issues", "agent": "speckit.implement", "prompt": "Fix static analysis issues"},
        ],
    },
    {
        "name": "speckit.checklist",
        "description": "Requirements Validator - Tạo và validate checklist từ spec",
        "role": "Requirements Auditor",
        "project_types": "all",
        "depends_on": ["speckit.specify"],
        "handoffs": [],
    },
    {
        "name": "speckit.clarify",
        "description": "Ambiguity Resolver - Phát hiện và giải quyết mơ hồ trong spec",
        "role": "Clarity Engineer",
        "project_types": "all",
        "depends_on": ["speckit.specify"],
        "handoffs": [
            {"label": "Update Spec", "agent": "speckit.specify", "prompt": "Update spec with clarifications"},
        ],
    },
    {
        "name": "speckit.constitution",
        "description": "Governance Manager - Thiết lập & quản lý Constitution (Source of Law)",
        "role": "Governance Architect",
        "project_types": "all",
        "depends_on": [],
        "handoffs": [
            {"label": "Build Specification", "agent": "speckit.specify", "prompt": "Implement the feature specification based on the updated constitution"},
        ],
    },
    {
        "name": "speckit.diff",
        "description": "Artifact Comparator - So sánh sự khác biệt giữa các artifacts",
        "role": "Diff Analyst",
        "project_types": "all",
        "depends_on": [],
        "handoffs": [],
    },
    {
        "name": "speckit.implement",
        "description": "Code Builder (Anti-Regression) - Triển khai code theo tasks với IRONCLAD protocols",
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
        "description": "Legacy Code Migrator - Chuyển đổi legacy code sang chuẩn mới",
        "role": "Migration Specialist",
        "project_types": "all",
        "depends_on": [],
        "handoffs": [
            {"label": "Create Spec", "agent": "speckit.specify", "prompt": "Create spec from migrated codebase"},
        ],
    },
    {
        "name": "speckit.plan",
        "description": "Technical Planner - Tạo plan.md từ spec (data model, API contracts, research)",
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
        "description": "Logic Challenger (Red Team) - Đặt câu hỏi phản biện, tìm edge cases",
        "role": "Red Team Analyst",
        "project_types": "all",
        "depends_on": ["speckit.specify"],
        "handoffs": [],
    },
    {
        "name": "speckit.reviewer",
        "description": "Code Reviewer - Review code theo spec và best practices",
        "role": "Code Reviewer",
        "project_types": "all",
        "depends_on": ["speckit.implement"],
        "handoffs": [
            {"label": "Fix Issues", "agent": "speckit.implement", "prompt": "Fix review issues"},
        ],
    },
    {
        "name": "speckit.specify",
        "description": "Feature Definer - Tạo spec.md từ mô tả ngôn ngữ tự nhiên",
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
        "description": "Progress Dashboard - Hiển thị trạng thái tiến độ project",
        "role": "Progress Tracker",
        "project_types": "all",
        "depends_on": ["speckit.tasks"],
        "handoffs": [],
    },
    {
        "name": "speckit.tasks",
        "description": "Task Breaker - Tạo tasks.md atomic, có thứ tự dependency từ plan",
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
        "description": "Issue Tracker Syncer - Đồng bộ tasks.md sang issue tracker",
        "role": "Issue Syncer",
        "project_types": "all",
        "depends_on": ["speckit.tasks"],
        "handoffs": [],
    },
    {
        "name": "speckit.tester",
        "description": "Test Runner & Coverage - Chạy tests và báo cáo coverage",
        "role": "Test Engineer",
        "project_types": "all",
        "depends_on": ["speckit.implement"],
        "handoffs": [
            {"label": "Fix Failures", "agent": "speckit.implement", "prompt": "Fix test failures"},
        ],
    },
    {
        "name": "speckit.validate",
        "description": "Implementation Validator - Validate implementation vs spec tổng thể",
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
        "description": "UI/UX Architect - Định nghĩa Design System, UI Components, Spacing, Typography, Responsive Patterns.",
        "role": "UI/UX Architect",
        "project_types": "web",
        "depends_on": ["speckit.specify"],
        "handoffs": [
            {"label": "Update Plan", "agent": "speckit.plan", "prompt": "Integrate UI/UX specs into the technical plan"},
        ],
    },
    {
        "name": "speckit.debug",
        "description": "Systematic Debugger - Chẩn đoán sự cố, tìm root cause độc lập và đề xuất fix plans.",
        "role": "Debug Specialist",
        "project_types": "all",
    },
    {
        "name": "speckit.backlog",
        "description": "Backlog Manager - Quản lý Ý tưởng, Yêu cầu chờ xử lý và quét TODO/FIXME từ codebase.",
        "role": "Product Owner",
        "project_types": "all",
    },
    {
        "name": "speckit.roadmap",
        "description": "Roadmap Strategist - Quản lý lộ trình cấp cao (Milestones) và chuyển giao giữa các Phase.",
        "role": "Product Manager",
        "project_types": "all",
    },
    {
        "name": "speckit.map",
        "description": "Codebase Mapper - Tự động phân tích cấu trúc dự án, vẽ biểu đồ phụ thuộc và viết tài liệu kiến trúc.",
        "role": "Software Architect",
        "project_types": "all",
    },
    {
        "name": "speckit.uat",
        "description": "UAT Analyzer - Phân tích kết quả nghiệm thu thủ công và xử lý các khoảng cách (gaps) từ User.",
        "role": "QA Engineer",
        "project_types": "all",
    },
    {
        "name": "speckit.wordpress",
        "description": "WordPress Theme Architect - Chuyên gia phát triển theme, plugin và tối ưu hóa ecosystem WordPress.",
        "role": "WordPress Expert",
        "project_types": "web",
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
        "description": "Thiết lập/cập nhật Constitution (Source of Law)",
        "skills": ["speckit.constitution"],
    },
    {
        "command": "speckit.identity",
        "description": "Tạo/cập nhật Master Identity cho AI Agent",
        "skills": ["speckit.identity"],
    },
    {
        "command": "speckit.devops",
        "description": "Docker Infrastructure & Port Allocation (ENV-first)",
        "skills": ["speckit.devops"],
    },
    {
        "command": "02-speckit.specify",
        "description": "Tạo Feature Specification (spec.md)",
        "skills": ["speckit.specify"],
    },
    {
        "command": "03-speckit.clarify",
        "description": "Giải quyết mơ hồ trong Specification",
        "skills": ["speckit.clarify"],
    },
    {
        "command": "04-speckit.plan",
        "description": "Tạo Technical Plan (plan.md)",
        "skills": ["speckit.plan"],
    },
    {
        "command": "05-speckit.tasks",
        "description": "Tạo Task Breakdown (tasks.md)",
        "skills": ["speckit.tasks"],
    },
    {
        "command": "06-speckit.analyze",
        "description": "Phân tích tính nhất quán giữa artifacts",
        "skills": ["speckit.analyze"],
    },
    {
        "command": "07-speckit.implement",
        "description": "Triển khai code theo tasks (Anti-Regression)",
        "skills": ["speckit.implement"],
    },
    {
        "command": "08-speckit.checker",
        "description": "Chạy Static Analysis",
        "skills": ["speckit.checker"],
    },
    {
        "command": "09-speckit.tester",
        "description": "Chạy Tests & Coverage",
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
        "description": "GEO - Tối ưu cho AI Search (ChatGPT, Gemini, Perplexity)",
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
        "description": "Tạo/validate Requirements Checklist",
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
        "description": "So sánh Artifacts (Spec vs Implementation)",
        "skills": ["speckit.diff"],
    },
    {
        "command": "util-speckit.migrate",
        "description": "Migrate Legacy Code",
        "skills": ["speckit.migrate"],
    },
    {
        "command": "util-speckit.quizme",
        "description": "Red Team - Đặt câu hỏi phản biện tìm edge cases",
        "skills": ["speckit.quizme"],
    },
    {
        "command": "util-speckit.status",
        "description": "Hiển thị Progress Dashboard",
        "skills": ["speckit.status"],
    },
    {
        "command": "util-speckit.uiux",
        "description": "Thiết lập/cập nhật UI/UX Design System & Standards",
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
        "description": "Chẩn đoán và sửa lỗi hệ thống chuyên sâu (Systematic Debugging)",
        "skills": ["speckit.debug"],
    },
    {
        "command": "speckit.backlog",
        "description": "Quản lý Ý tưởng (Backlog) và quét nợ kỹ thuật (TODO/FIXME)",
        "skills": ["speckit.backlog"],
    },
    {
        "command": "speckit.roadmap",
        "description": "Quản lý lộ trình cấp cao (Milestones) và chuyển giao giữa các Phase",
        "skills": ["speckit.roadmap"],
    },
    {
        "command": "speckit.map",
        "description": "Vẽ bản đồ kiến trúc và sơ đồ phụ thuộc của Codebase",
        "skills": ["speckit.map"],
    },
    {
        "command": "speckit.uat",
        "description": "UAT Analyzer - Phân tích kết quả nghiệm thu thủ công và xử lý các khoảng cách (gaps) từ User.",
        "skills": ["speckit.uat"],
    },
    {
        "command": "speckit.wordpress",
        "description": "WordPress Theme & Plugin Development Workflow",
        "skills": ["speckit.wordpress"],
        "project_types": "web",
    },
]


def get_skills_for_project_type(project_type):
    """Lọc skills phù hợp với loại dự án."""
    if project_type not in PROJECT_TYPES:
        return SKILLS_REGISTRY  # fallback: trả về tất cả

    type_info = PROJECT_TYPES[project_type]
    allowed = type_info["includes_skills"]
    return [s for s in SKILLS_REGISTRY if s.get("project_types", "all") in allowed]


def get_project_type_info(project_type):
    """Lấy metadata của project type."""
    return PROJECT_TYPES.get(project_type, {
        "label": "Unknown",
        "use_docker": True,
        "is_soft_rules": False
    })


def get_workflows_for_project_type(project_type):
    """Lọc workflows phù hợp với loại dự án."""
    if project_type not in PROJECT_TYPES:
        return WORKFLOWS_REGISTRY

    allowed = PROJECT_TYPES[project_type]["includes_skills"]
    return [w for w in WORKFLOWS_REGISTRY if w.get("project_types", "all") in allowed]

