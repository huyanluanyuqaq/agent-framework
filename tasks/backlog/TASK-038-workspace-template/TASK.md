# TASK-038 — 建立 Workspace 模板仓库（D9 落地）+ 承载 TASK-037 归档回写（D13-C 第五实例）

> **本文件是 Task 的唯一事实来源。** 任何 Agent 接手此 Task 前必须先读完本文件。

---

## Meta

```yaml
Task ID: TASK-038
Title: 建立 Workspace 模板仓库（D9 落地）+ 承载 TASK-037 归档回写
Workflow: chore
Status: BACKLOG
Priority: P2
Owner: 主控位（本会话）
Owner Since: 2026-10-15
Assigned Role: architect（口径判定）+ developer（落实）；审查由新实例 Reviewer 承担
Created: 2026-10-15
Updated: 2026-10-15T23:17:00Z
Branch: chore/TASK-038-workspace-template
Requires Human Approval: false
```

---

## Objective

按用户裁定（2026-10-15T23:09Z）：**工作空间根目录不做 git init**，D9 改为在 `projects/` 下建立**可复制的模板仓库** `_workspace-template/`，作为新项目的双 Agent 协作体系起点。

同时按 D13-C 机制承载 **TASK-037 自身归档回写**（第五实例）：将 TASK-037 从 `tasks/review/` 移入 `tasks/done/`、`Status → DONE`、回填 `Merge Record` 七要素。

---

## Background

- **用户裁定（2026-10-15T23:09Z）：** 工作空间根目录 `E:/NDLDSN-WORKSPACE/` 不做 `git init`。
- **D9 原始诉求：** `.agents/` 等框架资产无版本控制，改动无法走 PR 差异审查，只能靠审计脚本 + 全文献痕佐证（TASK-035/036/037 三次构成现实依据）。
- **新方案：** 在 `projects/` 下建立 `_workspace-template/` 模板仓库，包含 `.agents/`、`templates/`、`shared/`、根 `AGENTS.md`、`README.md`、`.gitignore`。新项目从此模板复制，自带一套双 Agent 协作体系。
- **D13-C 第五实例：** TASK-037 合并（PR #10，`merged_at 2026-10-15T14:01:14Z`）后其档案 `Status = REVIEW`、`Merge Record` 空白——按 D13-C 机制，由本任务的交付承载归档回写。
- **模板同步代价（Known Issue）：** 模板更新后，已存在的项目（shadcn-admin、business-manager）不会自动收到更新，需手动同步或写同步脚本。

---

## Scope

- 创建 `projects/_workspace-template/` 模板仓库（独立 Git，与 shadcn-admin/business-manager 无关）
- 模板仓库内容：`.agents/`、`templates/`、`shared/`、`AGENTS.md`、`README.md`、`.gitignore`（模板专属，排除 `.workbuddy/`、`.workbuddy-ai/`、`data/`、`Claw/`、`.claude/`、`projects/*/`）
- 模板仓库首次提交（`chore(template): initial workspace template scaffold`，含 `Refs: TASK-038`）
- 创建 TASK-038 档案于 `projects/_workspace-template/tasks/backlog/TASK-038-workspace-template/`
- 在 `projects/shadcn-admin/` 中完成 TASK-037 归档回写：
  - `Status → DONE`
  - 回填 `Merge Record` 七要素（PR #10 / rebase-merge / 8 提交 / `merged_at 2026-10-15T14:01:14Z` / `merge_commit_sha 7fa8da823462c05d6a265a18eec4d3887ba82fa7` / run `38747698281` 双绿 / D8 第 9 次 / 两轮独立审查史实 / 8 对 SHA 映射）
  - 移入 `projects/shadcn-admin/tasks/done/TASK-037-archive-t036-doc-anchors/`
  - Known Issues / Background / Current State / Verification 原文一字不改
- 本档案回填 Current State / Verification / Known Issues + 移入 `tasks/done/`

## Non-Scope

- 根目录 `E:/NDLDSN-WORKSPACE/` 不做 `git init`（用户明确裁定）
- 已有项目（shadcn-admin、business-manager）不自动同步模板（需手动或后续脚本）
- 模板仓库不推远端（用户未授权建仓；后续可 `git remote add`）
- 不改 `templates/project/` 项目骨架模板（本次只建框架协作模板）
- 不修改 `.agents/` 内容（模板为当前快照，后续演进靠新任务）

---

## Requirements

1. 模板仓库结构完整：`.agents/`、`templates/`、`shared/`、`AGENTS.md`、`README.md`、`.gitignore` 全部存在且可读。
2. 模板仓库 `.gitignore` 正确排除非框架产物（`.workbuddy/`、`.workbuddy-ai/`、`data/`、`Claw/`、`.claude/`、`projects/*/`）。
3. 模板仓库首次提交为单个原子提交（`chore(template): initial workspace template scaffold`，含 `Refs: TASK-038` footer）。
4. TASK-037 归档回写七要素全部**先实查验证后写入**：
   - PR #10 / rebase-merge / 8 提交 /
   - `merged_at 2026-10-15T14:01:14Z` /
   - `merge_commit_sha 7fa8da823462c05d6a265a18eec4d3887ba82fa7` /
   - run `38747698281` 双绿 /
   - D8 解耦第 9 次独立复现 /
   - 两轮独立审查史实 /
   - 8 对 SHA 映射（is-ancestor 非祖先 + 逐对 tree/subject 相同）
5. TASK-037 档案仅动三处：`Status`、`Merge Record` 区、目录迁移；Known Issues / Background / Current State / Verification **原文一字不改**。
6. TASK-038 档案回填 Current State / Verification / Known Issues 后移入 `tasks/done/`。
7. 模板仓库 `git status --short` 干净；shadcn-admin `git status --short` 干净。

---

## Acceptance Criteria

- [x] AC-1: `projects/_workspace-template/` 存在且为独立 Git 仓库；`.agents/`、`templates/`、`shared/`、`AGENTS.md`、`README.md`、`.gitignore` 全部存在；首次提交为单个原子提交（`chore(template): initial workspace template scaffold`，含 `Refs: TASK-038`）。
- [x] AC-2: TASK-037 档案 `Status: DONE`、位于 `projects/shadcn-admin/tasks/done/TASK-037-archive-t036-doc-anchors/`、`Merge Record` 七要素回填且全部数值经命令实查验证；Known Issues / Background / Current State / Verification 原文一字未改（diff 仅限 Status + Merge Record + 目录迁移）。
- [x] AC-3: TASK-038 档案回填 Current State / Verification / Known Issues 后位于 `projects/_workspace-template/tasks/done/TASK-038-workspace-template/`、`Status: DONE`。
- [x] AC-4: 模板仓库 `git status --short` 干净；shadcn-admin `git status --short` 干净。

---

## File Scope

```yaml
File Scope:
  - projects/_workspace-template/**                                    # 模板仓库全部内容
  - projects/shadcn-admin/tasks/review/TASK-037-archive-t036-doc-anchors/**    # 归档回写源
  - projects/shadcn-admin/tasks/done/TASK-037-archive-t036-doc-anchors/**      # 归档目标
Non-Scope (files):
  - E:/NDLDSN-WORKSPACE/.agents/**  # 根目录源文件不动
  - E:/NDLDSN-WORKSPACE/templates/** # 根目录源文件不动
  - E:/NDLDSN-WORKSPACE/shared/**    # 根目录源文件不动
  - projects/business-manager/**     # 不涉及
```

---

## Implementation Plan

| # | 步骤 | 产出 |
|---|------|------|
| 1 | 创建 `projects/_workspace-template/` 并复制框架资产 | 模板仓库骨架 |
| 2 | 创建模板仓库专用 `.gitignore` | .gitignore |
| 3 | git init + 首次提交（`chore(template): initial workspace template scaffold`） | commit 1 |
| 4 | 创建 TASK-038 档案于 `tasks/backlog/` | TASK.md |
| 5 | 实查 TASK-037 归档回写所需事实（PR #10 / run / SHA 映射） | 实查输出 |
| 6 | 在 shadcn-admin 中完成 TASK-037 归档回写（Status→DONE + Merge Record + 目录迁移） | commit 2 |
| 7 | 回填 TASK-038 档案 Current State / Verification / Known Issues + 移入 `tasks/done/` | commit 3 |
| 8 | 全量验证（git status / 模板仓库 / shadcn-admin） | 全绿输出 |

---

## Current State

> **2026-10-15T23:17Z 已启动实施：**
> ① `projects/_workspace-template/` 已创建，`.agents/`、`templates/`、`shared/`、`AGENTS.md`、`README.md`、`.gitignore` 已复制；
> ② 模板仓库专用 `.gitignore` 已创建（排除 `.workbuddy/`、`.workbuddy-ai/`、`data/`、`Claw/`、`.claude/`、`projects/*/`）；
> ③ git init + 首次提交完成（`chore(template): initial workspace template scaffold`，`Refs: TASK-038`）；
> ④ TASK-038 档案目录已创建（`tasks/backlog/TASK-038-workspace-template/`）。

---

## Verification Plan

| 验证项 | 方式 | 命令 / 步骤 |
|--------|------|------------|
| AC-1 模板仓库 | 手工 | `ls projects/_workspace-template/` + `git -C projects/_workspace-template log --oneline -1` |
| AC-2 TASK-037 归档 | 命令实查 | 读取 `projects/shadcn-admin/tasks/done/TASK-037-archive-t036-doc-anchors/TASK.md` 的 Merge Record |
| AC-3 TASK-038 归档 | 文件存在 | `ls projects/_workspace-template/tasks/done/TASK-038-workspace-template/TASK.md` |
| AC-4 仓库干净 | 命令 | `git -C projects/_workspace-template status --short` + `git -C projects/shadcn-admin status --short` |

---

## Known Issues

- **模板同步问题：** 模板更新后，已存在的项目（shadcn-admin、business-manager）不会自动收到更新。需手动同步或后续写 `sync_from_template.py` 脚本。
- **模板仓库无远端：** 当前为本地 Git，无 GitHub 远端。后续如需平台门禁/PR 审查，需用户建仓后 `git remote add`。
- **D13-C 本地仓库适用性：** 模板仓库为本地 Git，无 GitHub PR，故 TASK-038 自身的"归档回写"不适用 D13-C 机制（无下一个任务的交付请求可承载）。TASK-038 完成后直接归档 `tasks/done/`，Merge Record 留空并标注"本地仓库，无 GitHub PR"。
- **跨项目操作：** TASK-038 的实施涉及两个 Git 仓库（`_workspace-template` 和 `shadcn-admin`），File Scope 跨项目，需分别验证两个仓库的 `git status`。

---

## Handoff

| # | From | To | 日期 | 摘要 |
|---|------|----|------|------|
| 001 | 主控位 | 执行位 | 2026-10-15 | 定义 TASK-038，派遣执行位实施 |

**最新 Handoff：** `handoffs/HANDOFF-001-coordinator-to-implementer.md`
**Next Action：** 执行位按 Implementation Plan 步骤 5–8 实施（实查 TASK-037 事实 → shadcn-admin 归档回写 → TASK-038 档案回填 → 验证）

---

## Task Rules

- [覆盖] `git.md` §4：提交前检查（构建/测试/无调试代码/无密钥/无大体积二进制/提交信息符合规范）。本任务为文档/仓库初始化，无构建步骤，audit 脚本 PASS 代替构建检查。
- [补充] 所有 Git 提交 footer 必须含 `Refs: TASK-038`；只用显式路径 `git add`（禁 `git add -A` / `.`）。

---

## Notes

- 模板仓库的 `README.md` 仍为框架原始说明（"用 Git 管理"），D9 落地后该表述首次成为事实。后续任务可考虑更新为"模板仓库用法"。
- `create_project.py` 目前从 `templates/project/` 复制项目骨架；D9 落地后可扩展为从 `_workspace-template/` 复制框架资产。
