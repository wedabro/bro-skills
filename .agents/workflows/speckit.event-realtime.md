---
description: Realtime & Event-Driven Architecture Workflow
---

# ⚡ Realtime & Event-Driven Pipeline

## Pre-conditions
- Redis / RabbitMQ / Kafka service configured in `.env` and `docker-compose.yml`

## Steps
1. **@speckit.event-realtime** — Channel & Transport Design
   - Choose WebSocket (bidirectional) or SSE (unidirectional streaming).
2. **@speckit.event-realtime** — Multi-node Scaling & Heartbeat
   - Set up Redis Pub/Sub adapter and 30s ping/pong heartbeat.
3. **@speckit.event-realtime** — Transactional Outbox Pattern
   - Implement outbox table schema and asynchronous publisher worker.
4. **@speckit.event-realtime** — Idempotent Consumer & DLQ
   - Enforce message deduplication and dead-letter queue routing.
