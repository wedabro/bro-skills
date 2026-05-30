---
description: Game Development Pipeline - Engine setup, game loop, performance, asset pipeline
---

# 🎮 Game Development

## Pre-conditions
- `project.json.project_type` = `game`
- Engine target đã xác định (Unity/Unreal/Godot/Phaser/PixiJS/custom)

## Steps

1. **@speckit.gamedev** — Engine & Project Setup
   - Xác định engine, cấu trúc thư mục, Docker env (web game) hoặc CI build (native)

2. **@speckit.gamedev** — Core Architecture
   - Game loop (fixed/variable timestep), ECS/Component, State Machine, Event Bus

3. **@speckit.gamedev** — Performance Budget
   - Frame budget (16.6ms@60fps), object pooling, profiling

4. **@speckit.uiux** — HUD & Menu
   - UI states (Menu/Pause/GameOver), responsive HUD

5. **@speckit.gamedev** — Asset Pipeline + Netcode (nếu multiplayer)
   - Atlas/LOD, naming convention, server-authoritative netcode

6. **@speckit.tester** — Game logic tests + playtest checklist

## Success Criteria
- ✅ Game loop ổn định, đạt frame budget
- ✅ Không hard-code balance/asset/URL (dùng config/ENV)
- ✅ Object pooling cho hot objects
- ✅ Multiplayer (nếu có): server validate
