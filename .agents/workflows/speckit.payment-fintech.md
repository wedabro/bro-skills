---
description: Payment Gateway & Idempotent Ledger Workflow
---

# 💳 Payment & FinTech Ledger Pipeline

## Pre-conditions
- Gateway API credentials configured in `.env` (Stripe, ZaloPay, MoMo, VNPay)
- Relational database available for ACID transactions

## Steps
1. **@speckit.payment-fintech** — Money Precision & Schema Setup
   - Use integer minor units or `DECIMAL(18, 4)`. Absolute ban on `float`.
2. **@speckit.payment-fintech** — RFC 8935 Idempotency Key Middleware
   - Implement Redis-backed atomic distributed locks and response caching.
3. **@speckit.payment-fintech** — Raw Body Webhook Signature Verification
   - Verify HMAC SHA-256 signatures with timestamp anti-replay validation.
4. **@speckit.payment-fintech** — Double-Entry Ledger & State Machine
   - Create balanced immutable journal entries ($\sum \text{Debit} = \sum \text{Credit}$).
