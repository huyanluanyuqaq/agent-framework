# Workspace Agent Framework

> 一套**通用、可扩展、可复用、可维护**的多项目 Multi-Agent 协作框架。
> 与具体技术栈无关；所有协作状态落盘为文件；任何 AI Agent（Claude / Codex / OpenCode / Hermes / 未来 Agent）均可接入。

---

## 1. 这是什么？

本仓库不是一个软件项目，而是一个 **Agent Workspace Operating Framework**。

它解决一个核心问题：

> 多个 AI Agent 要在多个项目上长期协作，但 Agent 会退出、重启、换模型、换工具，
> 而**协作状态不能丢**。

答案是：**把所有协作状态放进文件系统，用 Git 管理，让文件成为唯一事实来源。**

| 概念 | 含义 |
|------|------|
| **Workspace** | AI Agent 的项目管理与协作环境（本仓库） |
| **Project** | 一个具体的、可独立 Git 管理的软件项目（`projects/` 下） |
| **Task** | 一次协作的最小单元，自包含目录 |
| **Role** | Agent 在任务中扮演的职责 |
| **Workflow** | 角色之间的编排顺序 |
| **Handoff** | Agent 之间通过文件传递的交接记录 |

---

## 2. 架构

三层结构，规则自上而下继承：

```
Workspace 层（跨项目共享，技术栈无关）
        │  规则下传，可被覆盖
        ▼
Project 层（单个软件项目，技术栈相关）
        │  任务实例化
        ▼
Task 层（协作单元，自包含）
```

**规则优先级（双轴模型）：**

- **约束轴**：Security / Safety / System 规则为**受保护规则**，永远生效，任何层不得削弱。
- **特化轴**：非受保护规则按具体性覆盖 —— Workspace → Project → Task → 目录 → 任务上下文。

---

## 3. 目录结构

```
.
├── AGENTS.md                 # Agent 入口协议（先读这个）
├── README.md                 # 本文件（人类可读）
│
├── .agents/                  # Agent 工作规范（跨项目共享）
│   ├── roles/                #   8 个通用角色
│   ├── workflows/            #   5 个工作流
│   ├── rules/                #   5 类通用规则
│   ├── protocols/            #   8 个协作协议
│   └── state/                #   跨项目全局状态
│
├── templates/                # 可复制模板
│   ├── project/              #   项目骨架（新项目的起点）
│   ├── task/TASK.md          #   任务模板
│   ├── handoff/HANDOFF.md    #   交接模板
│   └── adr/ADR.md            #   架构决策记录模板
│
├── projects/                 # 实际项目（每个独立 Git）
│   └── README.md             #   项目清单（Discovery 入口）
│
└── shared/                   # 跨项目共享资源
    ├── scripts/              #   可复用脚本（含 create_project.py）
    ├── tools/                #   可复用工具
    └── knowledge/            #   共享知识（禁止放项目源码）
```

---

## 4. Agent 如何工作

Agent 的工作循环是固定的：

```
读取上下文 → 声明 Role → 执行 → 验证 → 写 Handoff
```

**读取顺序**（详见 `AGENTS.md` §4）：

```
AGENTS.md → 项目 AGENTS.md → 任务 TASK.md → 相关 role/workflow/rules
```

**关键约束：**

- Agent **不依赖聊天上下文**，一切以文件为准。
- Agent 开始前必须**声明 Role**。
- Agent 结束时必须**写 Handoff**（不能只靠聊天交接）。

---

## 5. 如何创建新项目

### 方式 A — 使用脚本（推荐）

```bash
python shared/scripts/create_project.py my-project \
  --description "一句话描述这个项目" \
  --tech-stack "Python, FastAPI, PostgreSQL"
```

脚本会：复制 `templates/project/` → `projects/my-project/`，替换占位符，并可选初始化 Git。

### 方式 B — 手动复制

```bash
cp -r templates/project projects/my-project
# 然后编辑 projects/my-project/AGENTS.md，替换所有 {{...}} 占位符
```

### 方式 C — 接入既有项目

已有一个在开发的项目，想纳入本 Workspace？

**不要复制模板覆盖它。** 按 `.agents/protocols/project-adoption.md` 执行，
核心原则是 **只加不改**：只追加协调层（`AGENTS.md` + `docs/` + `tasks/`），
**不动**源码、测试、构建配置。

```bash
# 先只读检查，产出 Adoption Report，确认方案后再执行
```

### 创建后

1. 编辑 `projects/my-project/AGENTS.md`，填完所有 `{{PLACEHOLDER}}`。
2. 在 `projects/README.md` 登记该项目。
3. 在 `docs/requirements/` 写需求，在 `docs/architecture/` 写架构。
4. 把第一个 Task 放进 `tasks/backlog/`，开始协作。

---

## 6. 如何开始一个 Task

1. 从 `templates/task/TASK.md` 复制，创建：
   `projects/<name>/tasks/backlog/TASK-001-<slug>/TASK.md`
2. 填完 TASK.md 的静态部分（Objective / Scope / Acceptance Criteria / …）。
3. 状态设为 `READY`，分配给某个 Role。
4. 把 Task 目录从 `backlog/` 移到 `active/`，状态设为 `ACTIVE`。
5. 按 Workflow 推进，每次交接写 Handoff。
6. Reviewer 给 PASS 后，移入 `done/`。

---

## 7. Agent 如何协作

**标准三 Agent 模型：**

```
Requirement → Architect → Design → Developer → Implementation
                                                     │
                                                     ▼
                                                  Reviewer
                                                     │
                                          ┌──────────┴──────────┐
                                        PASS                  FAIL
                                          │                     │
                                        DONE            CHANGES_REQUESTED
                                                                │
                                                          back to Developer
```

**架构变更回流：** Developer 若发现设计不可行 → 回到 Architect。

**并行协作的冲突解决**（不引入复杂锁）：

| 机制 | 作用 |
|------|------|
| Task Ownership | 一个 Task 同时只有一个 Owner |
| File Scope | Task 声明允许改动的路径，避免重叠 |
| Git Branch | 一个 Task 一个分支 |
| Status | 通过 TASK.md 状态表达占用 |

---

## 8. 如何使用 Roles

角色定义在 `.agents/roles/`。每个角色文件包含：
Purpose / Responsibilities / Inputs / Outputs / Allowed Actions /
Forbidden Actions / Workflow / Completion Criteria / Handoff Requirements。

**8 个角色：** Architect、Developer、Reviewer、Tester、DevOps、Researcher、Product、Security。

**用法：** Agent 在 Handoff 和 TASK.md 中声明当前 Role，并遵守该角色的权限边界。

**Role ≠ Agent：** 角色是"帽子"，不是"进程"。一个 Agent 可以依次扮演多个角色，
只有「实现者 ≠ 批准者」这条不可兼任。可用 Agent 数量少于角色数量时的分配方案
（角色家族 · 2 Agent 最小配置 · 1 Agent 降级）见 `.agents/protocols/role-assignment.md`。

---

## 9. 如何使用 Workflows

工作流定义在 `.agents/workflows/`：

| Workflow | 流程 |
|----------|------|
| **Feature** | Requirement → Design → Implementation → Test → Review → Done |
| **Bugfix** | Reproduce → Diagnose → Fix → Regression Test → Review → Done |
| **Refactor** | Analyze → Plan → Refactor → Test → Review |
| **Research** | Question → Research → Evidence → Analysis → Recommendation |
| **Release** | Prepare → Verify → Build → Deploy → Observe → Record |

**用法：** Task 在 `TASK.md` 中声明 `Workflow: feature`，Agent 按该工作流的阶段推进。

---

## 10. Handoff 如何工作

Handoff 是**文件**，不是聊天消息。位置：

```
projects/<name>/tasks/<state>/<task-id>/handoffs/HANDOFF-<seq>-<from>-to-<to>.md
```

**为什么放在 Task 内？** Handoff 是 Task 作用域的产物，应与 Task 同生命周期 ——
Task 归档时，其全部交接历史一并归档，且 Git 友好。

**必填字段：** From / To / Task / Current State / Completed Work / Changed Files /
Tests / Known Issues / Remaining Work / Assumptions / Risks / Next Action。

模板：`templates/handoff/HANDOFF.md`。

---

## 11. Task 状态如何工作

**物理目录（4 个）：**

```
tasks/backlog/  →  tasks/active/  →  tasks/review/  →  tasks/done/
```

**逻辑状态**（记录在 `TASK.md` 的 `Status` 字段）：

```
BACKLOG → READY → ACTIVE → REVIEW → DONE
                    ▲         │
                    │         ├─→ CHANGES_REQUESTED ─┐
                    │         └─→ TEST_FAILED ────────┤
                    │                                 │
                    └─────────────────────────────────┘
ACTIVE ─→ BLOCKED ─→ (解除后回 ACTIVE)
ACTIVE ─→ REQUIREMENT_CHANGED ─→ 回 DESIGN
```

**设计取舍：** 不把每个状态做成目录（避免目录爆炸）。目录只表达粗粒度阶段，
细粒度状态由 `TASK.md` 承载。

---

## 12. 如何维护本框架

| 场景 | 做法 |
|------|------|
| 新增角色 | 在 `.agents/roles/` 加文件，并在 `AGENTS.md` §5 登记 |
| 新增工作流 | 在 `.agents/workflows/` 加文件，并在 `AGENTS.md` §6 登记 |
| 修改通用规则 | 直接改 `.agents/rules/*.md`（注意 security.md 为受保护规则） |
| 改进项目模板 | 改 `templates/project/`，已存在的项目**不自动同步** |
| 规则冲突 | 按 `.agents/protocols/rule-precedence.md` 裁决 |

**维护原则：**

- 单一事实来源 —— 规则只定义一处。
- 保持精简 —— 不为"看起来专业"而增加目录或文件。
- 保持技术栈无关 —— Workspace 层不出现任何具体技术。

---

## 13. 支持哪些 Agent

框架与 Agent 实现无关。任何能够**读写文件**的 Agent 均可接入：

Claude · Codex · OpenCode · Hermes · 以及未来任何 Agent。

**接入方式：** 让 Agent 先读 `AGENTS.md`，然后按协议工作即可。
不需要任何专有 SDK 或运行时。

---

## 14. 设计原则速查

```
Inspect First → Understand → Design → Explain → Implement → Validate → Report
```

- 文件即状态，聊天不作数
- 受保护规则不可削弱
- 最小改动，不做顺带重构
- 项目可脱离 Workspace 独立运行
- 简单 / 显式 / 基于文件 / Git 友好 / 人类可读

---

*版本：1.0*
