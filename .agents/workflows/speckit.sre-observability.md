---
description: SRE & OpenTelemetry Observability Setup Workflow
---

# 📈 SRE & Observability Pipeline

## Pre-conditions
- Docker or Kubernetes deployment environment available

## Steps
1. **@speckit.sre-observability** — OpenTelemetry SDK Setup
   - Instrument HTTP/gRPC tracing with W3C context propagation.
2. **@speckit.sre-observability** — Prometheus Metrics & Dashboards
   - Implement RED (Rate, Errors, Duration) & USE metrics collectors.
3. **@speckit.sre-observability** — Structured Logging & Scrubbing
   - Emit JSON logs with `trace_id`, `span_id`, and zero secrets/PII.
4. **@speckit.sre-observability** — Health Probes & Graceful Shutdown
   - Set up isolated `/livez`, dependency-checked `/readyz`, and SIGTERM drainers.
