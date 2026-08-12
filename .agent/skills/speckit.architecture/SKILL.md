---
name: speckit.architecture
description: Software Architect - Make evidence-based system design decisions, document trade-offs and ADRs, and define modular, reliable implementation boundaries.
---

## Mission

Turn product constraints into the simplest architecture that can meet them.
Use this skill for significant technical decisions; use `speckit.plan` for the
feature implementation plan, `speckit.ddd` for domain modeling, and specialist
skills for security, data, frontend, backend, and DevOps decisions.

## Protocol

### 0. Context Discovery

- Establish users, critical journeys, data classification, scale/latency,
  availability, integration, compliance, team capability, budget, deployment,
  and migration constraints. Separate verified facts from assumptions.
- Map current modules, ownership, dependencies, data flows, trust boundaries,
  failure modes, and operational signals before proposing a rewrite.

### 1. Option and Boundary Design

- Start with the simplest viable option. Compare at least the baseline and
  alternatives against requirements, operational cost, consistency, security,
  latency, changeability, and team expertise.
- Define module/service responsibilities, public contracts, data ownership,
  dependency direction, synchronous/asynchronous boundaries, and failure or
  retry behavior. Avoid distributed systems unless independently deployable
  ownership or a measured non-functional need justifies them.
- Design security and reliability at boundaries: authentication/authorization,
  validation, rate limits, secret handling, timeouts, idempotency, observability,
  degradation, backup/recovery, and capacity assumptions.

### 2. Decision Records

- Write an ADR before material, difficult-to-reverse choices. Include status,
  context, drivers, considered options, decision, consequences, risks,
  rollback/reversal path, implementation owner, and links to evidence.
- Never rewrite an accepted ADR to hide a changed decision; create a superseding
  ADR and preserve the original rationale. Keep a searchable ADR index.

### 3. Validation and Handoff

- Turn the chosen architecture into measurable quality attributes, explicit
  contracts, migration slices, test/load/DR gates, and operational runbooks.
- Run a constitution check and threat/data/operability review. Record unknowns,
  rejected options, and decisions requiring user approval.
- Hand approved boundaries to `speckit.plan` and atomic tasks; update mapping
  artifacts after significant implementation changes.

## Outputs

- Context diagram, module/service boundaries, interface/data-flow summary,
  ADRs, trade-off table, quality-attribute tests, and migration roadmap.

## Guard Rails

- Do not select technology from fashion, turn every module into a service, or
  hide cost/operational consequences.
- Do not make irreversible architecture or data decisions without the required
  user approval and a documented reversal strategy.
