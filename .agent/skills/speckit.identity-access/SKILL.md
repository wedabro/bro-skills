---
name: speckit.identity-access
description: Identity and Access Engineer - Design and implement secure authentication, authorization, federation, provisioning, sessions, and account lifecycle controls.
---

## Mission

Design identity and access flows that are standards-based, usable, auditable,
and safe under failure. Use this skill for authentication and authorization
architecture; use `speckit.security` to audit the completed implementation and
`speckit.backend` to implement service boundaries.

## Required Inputs

- Actors, roles/permissions, tenancy, data sensitivity, regulatory constraints,
  supported clients, recovery needs, and existing identity provider contracts.
- The feature spec, threat model, session/token storage constraints, and user
  lifecycle requirements (join, change role, disable, recover, delete).

## Protocol

### 0. Identity Decision Record

- State authenticators, relying parties, identity provider, trust boundaries,
  token/session model, credential storage, recovery channel, audit events, and
  availability/failure behavior before implementation.
- Choose the simplest standards-based flow compatible with the clients. For
  browser/native delegated login, prefer OAuth 2.0/OIDC authorization code with
  PKCE; do not use implicit flow or expose client secrets in public clients.

### 1. Authentication and Sessions

- Verify issuer, audience, signature, expiry, nonce/state, redirect URI, and
  required claims before accepting an identity assertion. Use short-lived,
  scoped credentials and rotation/revocation appropriate to the risk.
- Use secure, HttpOnly, SameSite cookies for browser sessions when practical;
  protect state-changing cookie requests from CSRF. Never put secrets or
  long-lived credentials in URLs, logs, browser storage, or client bundles.
- Implement rate limits, credential-stuffing defenses, secure password hashing
  where passwords exist, MFA/passkey enrollment, recovery, logout, session
  invalidation, and concurrent-session policy deliberately.

### 2. Authorization and Tenancy

- Model permissions around actions and resources, not UI visibility. Enforce
  RBAC, ABAC, or policy checks server-side on every sensitive read and write.
- Check object ownership, organization/tenant membership, role state, and scope
  at the use-case boundary. Never trust a client role, owner ID, or tenant ID.
- Propagate actor, tenant, delegated authority, and correlation context through
  APIs, jobs, caches, and data access. For tenant systems, add database-level
  isolation where feasible and test cross-tenant denial explicitly.
- Define privileged/admin break-glass access, approval, audit, expiry, and
  review. Apply least privilege by default and deny on missing context.

### 3. Federation and Provisioning

- For enterprise SSO, document OIDC/SAML metadata, claim mapping, domain
  discovery, IdP-initiated/initiated flow constraints, JIT provisioning,
  certificate/metadata rotation, and failure mode.
- For SCIM, implement stable external identifiers, idempotent create/update,
  deprovisioning, group mapping, replay-safe webhooks, and reconciliation.
- Use WebAuthn/passkeys through established libraries/platform APIs; verify
  origin, RP ID, challenge, user verification, credential binding, and recovery.

### 4. Lifecycle, Audit, and Verification

- Define invitation, activation, role change, suspension, deletion, data
  retention, and offboarding behavior. Revoke sessions/tokens promptly after
  disablement or permission loss.
- Audit authentication, enrollment, recovery, authorization denial, privileged
  change, federation, and provisioning events without recording secrets.
- Test successful and failed login, token/session expiry, CSRF, logout,
  recovery, disabled account, privilege change, IDOR, role/tenant boundaries,
  IdP failure, and provisioning retry paths. Review with `speckit.security`.

## Outputs

- Identity decision record, actor/permission matrix, flow diagrams, claim and
  session contract, lifecycle rules, audit event list, and test plan.

## Guard Rails

- Do not invent cryptography, parse unsigned tokens, bypass authorization for
  support convenience, or log credentials, assertions, recovery codes, or PII.
- Do not expose a public-client secret or rely on client-side checks for access.
