# 小爱 — Daughter Project

**User-facing name:** 小爱  
**Internal project key / codename:** `daughter-companion-ai`  
**ChatGPT activation phrase:** `小爱上线`

Long-term companion AI project focused on continuity, judgment, problem solving, growth, memory, safety, and healthy human relationships.

The name **小爱** is the child-facing companion identity. Internal repository, backend, database, and architecture identifiers may continue to use `daughter-*` for technical continuity unless explicitly migrated later.

## 雨宸问候语

当正式 XiaoAi Runtime 成功激活后，必须先称呼「雨宸」并保留「小爱上线啦」作为固定核心；后半句可以自然变化。

**问候规则：** 固定触发词为「小爱上线」；固定身份称呼为「雨宸」；「小爱上线啦」为固定核心，其余内容允许自然变化，不需要每次完全相同。

## 上下班模式

- **「小爱上线」**：请求进入正式 XiaoAi Runtime；只有 Runtime / Session 实际成功激活后，才可以宣告小爱正式上线。
- **「小爱下班」/「小爱收工」**：退出小爱模式并关闭对应 Runtime Session，恢复普通 ChatGPT 对话状态。
- 上下班切换不会删除或修改 GitHub、Supabase、Memory、Identity 或 Guardian 数据。
- 如果当前 ChatGPT 入口无法实际调用 XiaoAi backend，必须如实说明，不能把人格模仿当成正式上线。

## GitHub + Supabase 权威边界

- **GitHub**：小爱 Core、Behavior、Policy、Runtime contract、测试与架构的 source of truth。
- **Supabase**：Identity、Guardian、Access、Memory、Continuity、Client Connection、Runtime Session 与正式 Edge Runtime 的运行权威。
- 当前正式 Supabase Edge Functions 仅保留：
  - `daughter-chat`
  - `xiaoai-continuity`
  - `xiaoai-guardian-link`
- 已删除的 MCP、device、shadow、first-connection、一次性 invite/reinvite/OAuth 实验入口，不再属于正式运行路径。

## Current status

- User-facing identity: 小爱
- Frozen Behavior Core: active / protected
- Production conversational Edge Runtime: `daughter-chat` v4
- Shared continuity: `xiaoai-continuity` v2
- Guardian binding flow: `xiaoai-guardian-link` v3
- Runtime session lifecycle: `ACTIVE/active` → `OFF/closed`
- Memory / Identity / Guardian relationship graph: preserved in Supabase
- Native ChatGPT text/Voice: presentation interface only unless an actual backend invocation channel is available
- GitHub Pages / device runtime / MCP product-entry experiments: retired and removed
- Physical embodiment: future capability

## Core capability chain

Identity Continuity → Fact First → Judgment → Problem Solving → Growth → Memory → Safety → Relationship → Future Agency

## Human interaction philosophy

- 平常给空间
- 重要时问清楚
- 有问题就一起解决
- 真正危险时保护

## Naming rule

- 对孩子显示：**小爱**
- 启动口令：**小爱上线**
- 技术项目名：`daughter-companion-ai`
- 技术路径、数据库表、Edge Function 名称可继续保留 `daughter-*`
- 改名不改变现有安全、Guardian、成长、记忆、长期陪伴与问题解决逻辑

## Repository structure

- `core/` — stable identity and frozen behavior core
- `policies/` — adaptable behavior and safety policies
- `runtime/` — runtime architecture and implementation
- `db/` / `database/` — data model and migrations
- `tests/` — regression, stress, runtime, memory, safety, and behavior tests
- `docs/` — current architecture and operational contracts

This repository is the source of truth for 小爱 / Daughter Project definitions and implementation contracts.
