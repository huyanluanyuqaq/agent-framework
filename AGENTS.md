# AGENTS.md — agent-framework（中央公共规范仓）

> **这是所有项目共享的 Agent 规范的唯一维护源。**
> 任何项目不得在本仓之外另行定义公共规范；项目级规则一律写在项目自己的 `AGENTS.md` 中。

---

## 1. 定位

本仓库维护**跨项目通用**的 Agent 规范：

| 内容 | 位置 |
|---|---|
| 通用规范（7 篇） | `.agents/` |
| 新项目模板 | `templates/project/` |
| 可复用脚本 | `shared/scripts/` |
| 共享资源 | `shared/` |
| 框架决策记录 | `docs/decisions/` |
| 历史归档 | `docs/archive/` |

**本仓不包含任何具体项目的技术栈、业务逻辑、目录结构或特殊要求。**

---

## 2. 规范文件（7 篇）

| 文件 | 职责 |
|---|---|
| `collaboration.md` | 三角色、任务分级（S/M/L）、拆分规则、并行机制、轻量交接 |
| `git.md` | 分支、提交、合并、冲突、回滚、工作区保护 |
| `github.md` | PR、检查、合并、平台配置、禁止操作 |
| `quality.md` | 代码质量、测试、安全、文档 |
| `rule-precedence.md` | 受保护规则清单 + 优先级裁决算法 |
| `permissions.md` | 三角色权限矩阵与通用权限原则 |
| `change-safety.md` | 🔴 高风险操作强制流程（受保护） |

**Agent 读取顺序：** 先读本文件 → 按任务需要读上表对应文件。
涉及安全/删除/生产/破坏性 Git 时，**必须**读 `change-safety.md`。

---

## 3. 受保护规则

以下规则**只能被增强，不能被任何项目或任务规则削弱**：

| 规则 | 位置 |
|---|---|
| 安全约束 | `quality.md` §三 |
| Git 禁止操作 | `git.md` §6 |
| 测试禁止事项 | `quality.md` §二 §5 |
| 职责分离（实现者 ≠ 批准者） | `permissions.md` §3 P3 |
| 不可自我提权 | `permissions.md` §3 P5 |
| 高风险操作流程 | `change-safety.md` |
| GitHub 侧对应禁止项 | `github.md` §6 |

冲突裁决算法见 `rule-precedence.md` §4。

---

## 4. 维护原则

1. **单一事实来源** —— 一条规则只在一处定义，其他位置引用而非复制。
2. **技术栈无关** —— 不把任何项目的技术选型写进公共规范。
3. **最小改动** —— 只改必要范围，不做顺带重构。
4. **先查后做** —— Inspect → Understand → Design → Explain → Implement → Validate → Report。
5. **不追求模块化而过度拆分文档。**

---

## 5. 版本管理与发布

### 版本号

`framework-version.json` 是唯一版本源，采用语义化版本：

| 级别 | 含义 |
|---|---|
| **MAJOR** | 不兼容变更（删除/重命名规范文件、改变受保护规则） |
| **MINOR** | 新增兼容规则或能力 |
| **PATCH** | 修复与小幅调整 |

### 发布流程

```
1. 修改 .agents/ 或 templates/
2. 更新 framework-version.json 的 version 与 changelog
3. 提交并推送 main
4. 打 tag：v<version>
5. 触发同步：见 `shared/scripts/sync-framework.py` 或 .github/workflows/sync-framework.yml
```

### 项目侧版本记录

每个项目根目录有 `framework-version.json`，记录 `version` / `source` / `lastSyncedAt`。

**同步范围仅限 `.agent-framework/**`。** 项目的 `AGENTS.md`、`README.md`、技术配置、
业务代码、项目专属 CI **永不被自动覆盖**。

---

## 6. 同步机制

| 层 | 入口 | 权限需求 |
|---|---|---|
| **本地** | `shared/scripts/sync-framework.py` | 无（零权限，立即可用） |
| **平台** | `.github/workflows/sync-framework.yml` | Fine-grained PAT（仓库 Secret） |

同步行为：每个目标项目建独立分支 → 更新 `.agent-framework/` 与版本文件 → 开一个 PR。
**不自动合并，不直推主分支。**

回滚：把项目分支指向旧版本重新跑一次同步，产生新 PR，**不 force push**。

---

## 7. 目录结构

```
agent-framework/
├── AGENTS.md                  ← 本文件
├── framework-version.json     ← 唯一版本源
├── README.md
├── .agents/                   ← 7 篇公共规范（同步到项目 .agent-framework/）
├── templates/project/         ← 新项目模板
├── shared/scripts/            ← sync-framework.py / audit_framework.py / create_project.py
├── shared/                    ← 跨项目共享资源
├── docs/
│   ├── decisions/             ← 框架 ADR
│   ├── capability/            ← 平台/环境能力记录模板
│   └── archive/               ← 历史设计文档
└── .github/workflows/
    └── sync-framework.yml     ← 平台同步（需 PAT）
```
