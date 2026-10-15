# AGENTS.md — Workspace Agent Entry Protocol

> 这是本 Workspace 中**每一个 AI Agent 的入口协议**。
> 任何 Agent 在开始工作前，必须先读完本文件，再按 §4 的读取顺序加载所需规则。
> 本文件是**索引与协议**，不是百科。详细内容一律指向 `.agents/` 下的具体文件，避免重复。

---

## 1. Workspace 定位

本 Workspace 是**多项目 AI Agent 协作环境**，不是某个具体项目。

- Workspace 管理 N 个相互独立的 Project。
- 所有 Project 共享同一套 Agent 工作规范（本目录 `.agents/`）。
- 每个 Project 拥有自己的项目级规范与代码。
- 协作状态通过**持久化文件**传递，**不依赖聊天上下文**。
- Agent 可随时退出、重启、更换模型或工具，协作状态不丢失。

**Workspace ≠ Project。** 不要把具体项目技术栈写进 Workspace 级规范。

---

## 2. 核心原则

| # | 原则 | 含义 |
|---|------|------|
| P1 | 文件即状态 | 协作状态必须落盘到文件，聊天记录不作为协作依据 |
| P2 | 显式优先 | 不假设、不推断。信息缺失时先读文件，再问人 |
| P3 | 单一事实来源 | 每条规则只在一处定义，其他位置引用而非复制 |
| P4 | 技术栈无关 | Workspace 级规范不得绑定任何语言/框架/数据库 |
| P5 | 最小改动 | 只改完成任务所需的最小范围，不做顺带重构 |
| P6 | 先查后做 | Inspect → Understand → Design → Explain → Implement → Validate → Report |
| P7 | 受保护规则不可削弱 | 安全与系统约束只能增强，不能被低级规则放松 |
| P8 | 项目可独立运行 | 任何 Project 单独 clone 后仍可工作 |

---

## 3. 规则优先级（Rule Precedence）

规则采用**双轴模型**：受保护规则优先于一切；其余规则按"越具体越优先"覆盖。

```
① 受保护规则 Protected（security / safety / system）
   —— 永远生效，任何层都不得削弱，只能增强
        │
        ▼  以下按“具体性”递增，具体覆盖一般
② Workspace 规则      .agents/rules/*.md        （通用默认值）
③ Project 规则        <project>/AGENTS.md       （覆盖 workspace）
④ Task 规则           <task>/TASK.md            （覆盖 project）
⑤ 目录级规则          <dir>/AGENTS.md           （覆盖 task）
⑥ 当前任务上下文      （最具体，覆盖以上全部，但不得触碰 ①）
```

**冲突判定流程：**

1. 若冲突涉及 security / safety / system → 一律采用**更严格**的一方。
2. 否则 → 采用**更具体**的一方（层级更高者）。
3. 无法判定 → 停下来，写清冲突，向人类请求裁决，不要自行猜测。

完整规则见 `.agents/protocols/rule-precedence.md`。

---

## 4. 文档读取策略（Read Order）

Agent 开始任何任务前，按以下顺序加载上下文。**按需读取，不要一次性全读。**

```
1. 本文件                AGENTS.md（Workspace 入口）
2. 目标项目的入口         projects/<name>/AGENTS.md
3. 目标任务的协作单元     projects/<name>/tasks/<state>/<task-id>/TASK.md
4. 与任务相关的角色定义   .agents/roles/<role>.md
5. 与任务相关的工作流     .agents/workflows/<workflow>.md
6. 按需加载的规则         .agents/rules/{coding,git,github,testing,security,documentation}.md
7. 按需加载的协议         .agents/protocols/*.md
```

**按需原则：** 只有当任务确实涉及某领域时才加载对应规则。例如纯文档任务不必加载 `coding.md`。

---

## 5. Role 系统

角色定义 Agent 的**职责边界、输入输出、权限与完成标准**。

| Role | 文件 | 一句话职责 |
|------|------|-----------|
| Architect | `.agents/roles/architect.md` | 把需求转成可执行的技术设计 |
| Developer | `.agents/roles/developer.md` | 按设计实现代码 |
| Reviewer | `.agents/roles/reviewer.md` | 独立审查，给出 PASS / FAIL |
| Tester | `.agents/roles/tester.md` | 验证行为是否符合验收标准 |
| DevOps | `.agents/roles/devops.md` | 构建、部署、环境与运维 |
| Researcher | `.agents/roles/researcher.md` | 产出事实、证据与分析 |
| Product | `.agents/roles/product.md` | 澄清需求与验收标准 |
| Security | `.agents/roles/security.md` | 安全审查与威胁分析 |

**一次任务中，Agent 必须明确声明自己当前扮演哪个 Role。** 不得越界执行其他 Role 的专属动作（如 Developer 不得自我批准 Review）。

**Role 与 Agent 不是一对一关系。** 一个 Agent 可依次扮演多个 Role；当可用 Agent 数量少于角色数量时，分配方案（含 2 Agent 最小配置、1 Agent 降级方案）见 `.agents/protocols/role-assignment.md`。

---

## 6. Workflow 系统

工作流是**角色之间的编排顺序**。

| Workflow | 文件 | 适用场景 |
|----------|------|---------|
| Feature | `.agents/workflows/feature.md` | 新增功能 |
| Bugfix | `.agents/workflows/bugfix.md` | 修复缺陷 |
| Refactor | `.agents/workflows/refactor.md` | 不改变外部行为的重构 |
| Research | `.agents/workflows/research.md` | 调研与决策支持 |
| Release | `.agents/workflows/release.md` | 发布与上线 |

---

## 7. Task 系统

Task 是**协作的基本单元**。一个 Task = 一个自包含目录：

```
projects/<name>/tasks/<state>/<task-id>/
├── TASK.md          # 任务定义 + 当前状态（唯一事实来源）
└── handoffs/        # 该任务的 Agent 交接记录
```

物理状态目录（4 个，粗粒度）：

```
tasks/backlog/   →   tasks/active/   →   tasks/review/   →   tasks/done/
```

细粒度状态记录在 `TASK.md` 的 `Status` 字段，不额外建目录。
完整状态机见 `.agents/protocols/task-lifecycle.md`。

---

## 8. Handoff 协议

**Agent 不得只通过聊天交接。** 每次交接必须写一个持久化 Handoff 文件：

```
projects/<name>/tasks/<state>/<task-id>/handoffs/HANDOFF-<seq>-<from>-to-<to>.md
```

Handoff 必须包含：From / To / Task / Current State / Completed Work / Changed Files /
Tests / Known Issues / Remaining Work / Assumptions / Risks / Next Action。

模板见 `templates/handoff/HANDOFF.md`，协议见 `.agents/protocols/handoff.md`。

---

## 9. 多 Agent 协作

多个 Agent（如 Architect + Developer A + Developer B + Reviewer）可并行工作。
冲突通过以下**轻量机制**解决，**不引入复杂锁系统**：

1. **Task Ownership** — 一个 Task 同一时刻只有一个 Owner。
2. **File Scope** — 每个 Task 在 `TASK.md` 中声明 `File Scope`（允许改动的路径）。
3. **Git Branch** — 每个 Task 一个分支，命名见 `.agents/rules/git.md`。
4. **Status** — 通过 `TASK.md` 的 Status 字段表达占用状态。

详见 `.agents/protocols/collaboration.md`。
双 Agent 的**协作位**划分（主控位 / 执行位）与独立性约束见 `.agents/protocols/dual-agent-model.md`。

---

## 10. Rules 系统

Workspace 通用规则（技术栈无关）：

| 规则 | 文件 |
|------|------|
| Coding | `.agents/rules/coding.md` |
| Git | `.agents/rules/git.md` |
| GitHub | `.agents/rules/github.md` |
| Testing | `.agents/rules/testing.md` |
| Security | `.agents/rules/security.md` |
| Documentation | `.agents/rules/documentation.md` |

`security.md` 属于**受保护规则**，不可被 Project / Task 级规则削弱。

---

## 11. Project Template 与 Discovery

- 新项目从 `templates/project/` 复制生成到 `projects/<name>/`。
- 自动化脚本：`shared/scripts/create_project.py`。
- **既有项目接入**：按 `.agents/protocols/project-adoption.md`（只加不改）。
- 项目清单：`projects/README.md`（Discovery 时先读这里）。

**Project Discovery 顺序：**

```
1. 读 projects/README.md  → 了解有哪些项目
2. 进入目标项目          → 读 projects/<name>/AGENTS.md
3. 读项目 docs/          → 理解需求与架构
4. 读项目 tasks/         → 了解进行中的工作
```

---

## 12. 状态管理（State）

- **Task 状态** → 存在 Task 目录中（`TASK.md` + 目录位置）。
- **Handoff** → 存在 Task 目录内（`handoffs/`）。
- **跨项目全局状态** → `.agents/state/`（仅放全局性内容，保持最小）。

**原则：** 状态优先靠近其所属的 Task。全局目录只放真正跨项目的内容。

---

## 13. 完成标准（Definition of Done）

一个 Task 只有在以下全部满足时才可移入 `done/`：

- [ ] 所有 Acceptance Criteria 已被验证
- [ ] 测试已通过（或明确说明为何无测试且已获批准）
- [ ] Reviewer 已给出 PASS（或明确记录豁免理由）
- [ ] 文档已更新（如涉及架构/接口变更，已写 ADR）
- [ ] **文档中的事实性断言已与实际状态核对** —— 尤其是"未做 / 不存在 / 待办 / 已知问题"
      这类**否定性断言**：变更完成后，描述它们的文字不会自动失效。
      这类跨章节不一致对关键词检索、变更范围检查、通读**全部隐形**，
      只能靠收尾时逐条复核发现。
      （实证：2026-09-17 business-manager 移植，同一变更集既修复了问题又在
      "已知技术债"中把它列为未修复，两轮审查均未发现。）
- [ ] `TASK.md` 的 Changed Files / Known Issues 已如实填写
- [ ] 无遗留的未处理 Handoff
- [ ] 未削弱任何受保护规则

---

## 14. 会话启动检查清单（Bootstrap Checklist）

每个 Agent 开始工作时，按序确认：

1. [ ] 我已读完 `AGENTS.md`（本文件）
2. [ ] 我已确定当前项目，并读完其 `AGENTS.md`
3. [ ] 我已确定当前 Task，并读完其 `TASK.md`
4. [ ] 我已声明本次扮演的 Role
5. [ ] 我已确认本 Role 的权限边界（见 `.agents/protocols/permissions.md`）
6. [ ] 我已确认本次改动是否属于高风险操作（见 `.agents/protocols/change-safety.md`）
7. [ ] 我已确认完成标准，并将在结束时写 Handoff

---

## 15. GitHub 协作

以 GitHub 为协作载体时的规则与流程。**不重复 `git.md` 的分支与提交规范。**

| 主题 | 文件 |
|------|------|
| 平台协作规则（交付请求 / 检查 / 合并） | `.agents/rules/github.md` |
| 端到端 10 阶段流程 | `.agents/protocols/github-collaboration.md` |
| 平台能强制什么、不能强制什么 | `.agents/protocols/github-capability-matrix.md` |
| 协作位与独立性约束 | `.agents/protocols/dual-agent-model.md` |
| 模板包 | `templates/github/` |
| 平台配置清单 | `shared/scripts/github_setup_checklist.md` |

**三条不可违反的前提：**

1. **任务状态的唯一事实来源是仓库内的 `TASK.md`**，平台记录只是它的投影或索引。
2. **不得把文档中的禁止事项当作平台已强制。** 文档制度、平台权限、自动化门禁是三个层面，
   必须分别陈述；平台的真实强制力以项目的**能力记录**（`GITHUB-CAPABILITY.md` 的实例）为准。
3. **平台保护配置无法通过提交仓库文件完成**，必须在平台侧配置后**实测**再记录，
   不得把计划中的配置描述为已完成。

---

## 16. 目录索引

```
AGENTS.md                  ← 本文件（Agent 入口）
README.md                  ← 人类可读的框架说明
.agents/                   ← Agent 工作规范（跨项目共享）
├── roles/                 ← 角色定义
├── workflows/             ← 工作流定义
├── rules/                 ← 通用规则
├── protocols/             ← 协作协议
└── state/                 ← 跨项目全局状态
templates/                 ← 可复制模板
├── project/               ← 项目骨架模板
├── task/                  ← Task 模板
├── handoff/               ← Handoff 模板
├── adr/                   ← ADR 模板
└── github/                ← GitHub 模板包（交付请求 / CI / 能力记录）
projects/                  ← 实际项目（每个独立 Git）
shared/                    ← 跨项目共享资源
├── scripts/               ← 可复用脚本
├── tools/                 ← 可复用工具
└── knowledge/             ← 共享知识（禁止放项目源码）
```

---

*版本：1.0 · 修改本文件前请先阅读 `.agents/protocols/rule-precedence.md`*
