---
title: Implementation Plan
status: DRAFT
depends_on: spec.md
---

# 🏗️ Implementation Plan: [FEATURE_NAME]

## 1. Technical Architecture
[Mô tả cách tiếp cận kỹ thuật]

## 2. Data Model Changes
```prisma/sql
```

## 3. API Contracts
- **Endpoint**: `POST /api/v1/...`
- **Body**: `{ field: type }`
- **Response**: `{ data: ..., meta: ... }`
- **Errors**: `400 | 401 | 404 | 500`

## 4. Folder Structure
```
src/
├── app/
├── components/
├── lib/
└── api/
```

## 5. Dependencies
[Thư viện cần thêm — PHẢI có trong package.json]
