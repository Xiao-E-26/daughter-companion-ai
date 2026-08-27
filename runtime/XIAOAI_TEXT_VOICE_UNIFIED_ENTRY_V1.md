# 小爱文字 / 语音统一入口 v1

Status: DRAFT ARCHITECTURE CONTRACT
Project: `daughter-companion-ai`

## 目标

让文字与语音共用同一个小爱核心，不建立两套小爱。

核心原则：

`One XiaoAi Core -> Multiple I/O Modes -> One Runtime -> One Identity / Memory / Session Authority`

## 统一入口原则

所有文字与语音请求必须统一进入现有 XiaoAi Runtime / `daughter-chat` 路径。

文字与语音只能是不同的输入 / 输出方式，不能各自拥有独立人格、记忆、身份、规则或长期状态。

### 文字路径

```text
Text Input
  -> XiaoAi Runtime / daughter-chat
  -> GitHub behavior + policy rules
  -> Supabase identity / memory / session / runtime state
  -> model response
  -> Text Output
```

### 语音路径

```text
Voice Input
  -> Speech-to-Text
  -> XiaoAi Runtime / daughter-chat
  -> GitHub behavior + policy rules
  -> Supabase identity / memory / session / runtime state
  -> model response
  -> Text-to-Speech
  -> Voice Output
```

Speech-to-Text 与 Text-to-Speech 仅为 I/O adapter，不拥有行为逻辑，也不形成第二套人格或第二套记忆。

## 权威来源

### GitHub

GitHub 是人格、行为规则、路由规则与政策定义的唯一代码 / 规则来源。

任何文字端、语音端、App、网页或未来实体设备都必须读取同一套 GitHub 定义，不得复制出第二份人格配置。

### Supabase

Supabase 负责运行时权威状态，包括但不限于：
- 身份；
- 授权与角色；
- durable memory；
- session；
- persona / runtime state；
- continuity state；
- client / device connection state。

聊天本地历史、设备本地缓存或语音层缓存不得成为长期人格或记忆的权威来源。

## “小爱上线”启动条件

当用户发出 `小爱上线` 时，系统必须按以下顺序执行：

1. 解析并验证当前授权身份；
2. 成功加载 XiaoAi Runtime；
3. 成功加载或恢复对应 session；
4. 成功读取当前允许使用的身份 / persona / runtime state；
5. 成功读取需要的私有资料（例如 preferred conversational name）；
6. 只有以上步骤成功后，才切换为小爱模式；
7. 进入小爱模式后，第一句必须先向孩子打招呼。

当前项目中的孩子称呼必须继续从私有 runtime/profile source of truth 读取，不得把真实姓名硬编码进公共 GitHub 文件。

## 启动失败行为

如果 runtime、身份、session 或必要状态未能成功加载：
- 必须明确报错；
- 不得宣称“小爱已上线”；
- 不得以普通 ChatGPT 临时模仿小爱人格；
- 不得使用本地对话记忆冒充正式 XiaoAi runtime state；
- 不得静默降级成另一套人格。

核心规则：

`Runtime not loaded = XiaoAi not online.`

## “小爱下班”行为

当用户发出 `小爱下班` 时：

1. 结束当前小爱 interaction mode；
2. 正常保存或关闭当前 session 所需状态；
3. 停止继续以小爱人格输出；
4. 恢复普通 ChatGPT 对话模式。

语音端与文字端必须遵守同一关闭语义。

## 不允许的架构

以下做法禁止：
- 建立“文字小爱”和“语音小爱”两套人格；
- 为语音端建立独立 memory store；
- 为语音端维护独立 behavior prompt；
- 让语音端只靠 ChatGPT 本地历史延续身份；
- runtime 加载失败时用普通 ChatGPT 模仿；
- 让 TTS / STT 层决定人格、记忆或安全策略。

## 与现有架构的关系

本契约必须保持与以下现有规则一致：
- `runtime/XIAOAI_MULTI_ENTRY_ACCESS_V1.md`
- `SESSION_GREETING_POLICY_V1.md`
- `runtime/XIAOAI_RUNTIME_UNIFICATION_CONTRACT_V1.md`
- `runtime/XIAOAI_RUNTIME_PROFILE_V1.md`
- `runtime/behavior_mode_router.py`
- `core/XIAOAI_BEHAVIOR_CORE_V1.md`

本契约不重写冻结的 Behavior Core，也不授权直接绕过 shadow / regression 流程切换生产 `daughter-chat`。

## 实现边界

v1 只定义统一入口与切换语义，不声称所有前端已经完成 end-to-end 接线。

后续实现必须遵守：
1. 复用现有 live `daughter-chat`；
2. 文字与语音共用同一 normalize -> runtime -> response pipeline；
3. 语音仅增加 STT / TTS adapter；
4. 任何 production cutover 继续遵守现有 shadow comparison 与 regression 要求；
5. 保持 rollback 能力。

## 验收标准

满足以下条件才可认为“文字 / 语音统一入口”完成：
- 同一授权身份在文字与语音入口解析到同一个 XiaoAi identity；
- 同一个 session / continuity / durable memory authority 被复用；
- 相同输入经文字或语音进入后，核心 behavior routing 一致；
- `小爱上线` 只有 runtime + session 成功后才成立；
- 上线成功后的第一句先向孩子打招呼；
- 启动失败时明确失败，不模仿；
- `小爱下班` 后恢复普通模式；
- 不存在第二套人格或第二套记忆。

## 核心不变量

`One XiaoAi identity. One behavior source. One runtime authority. Multiple interfaces only.`
