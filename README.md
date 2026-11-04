# agent-framework — 中央公共规范仓

**所有项目共享的 Agent 规范的唯一维护源。**

- 仓库：`git@github.com:huyanluanyuqaq/agent-framework.git`
- 当前版本：见 [`framework-version.json`](framework-version.json)
- Agent 入口：[`AGENTS.md`](AGENTS.md)

---

## 这个仓库是什么

一套**技术栈无关**的 Agent 协作规范，配套项目模板、同步机制与审计脚本。
它不包含任何具体项目的技术栈、业务逻辑或目录结构。

## 目录

```
agent-framework/
├── AGENTS.md                  Agent 入口（规范定位 / 阅读指引 / 维护原则 / 版本发布）
├── framework-version.json     唯一版本源（semver + changelog）
├── README.md                  本文件
├── .agents/                   7 篇公共规范
│   ├── collaboration.md       三角色、任务分级 S/M/L、拆分、并行、轻量交接
│   ├── git.md                 分支、提交、合并、冲突、回滚
│   ├── github.md              PR、检查、合并、平台配置
│   ├── quality.md             代码质量、测试、安全、文档
│   ├── rule-precedence.md     受保护规则 + 优先级裁决
│   ├── permissions.md         三角色权限矩阵
│   └── change-safety.md       高风险操作强制流程（受保护）
├── templates/project/         新项目模板（含 .agent-framework/ + CI + 版本文件）
├── shared/scripts/
│   ├── sync-framework.py      公共规范同步到项目（零权限）
│   ├── audit-project.py       项目级框架合规审计
│   ├── audit_framework.py     框架自检
│   ├── create_project.py      从模板建项目
│   ├── create_from_template.py 从本仓建项目并接入 GitHub
│   └── github_setup_checklist.md
├── docs/
│   ├── decisions/             框架 ADR
│   ├── capability/            平台/环境能力记录模板
│   └── archive/               历史设计文档
└── .github/workflows/         平台同步工作流
```

## 快速开始

**新建项目：**

```bash
python shared/scripts/create_from_template.py my-project \
    --github-user huyanluanyuqaq --repo my-project
```

**把规范同步到已有项目：**

```bash
python shared/scripts/sync-framework.py --project shadcn-admin --dry-run
python shared/scripts/sync-framework.py --project shadcn-admin
```

**审计项目合规性：**

```bash
python shared/scripts/audit-project.py
```

## 版本与发布

`framework-version.json` 是唯一版本源。发布流程：

1. 修改 `.agents/` 或 `templates/project/`
2. 更新 `framework-version.json`（version + changelog）
3. 提交推送 `main`，打 tag `v<version>`
4. 运行同步脚本把规范分发到各项目

同步范围**仅限** `.agent-framework/**` 与 `framework-version.json`。
项目的 `AGENTS.md`、`README.md`、技术配置、业务代码、项目专属 CI **永不被覆盖**。

## 设计原则

1. **单一事实来源** —— 规范只在这里定义一份，项目内是只读副本。
2. **技术栈无关** —— 不把任何项目的选型写进公共规范。
3. **最小改动** —— 只改必要范围。
4. **受保护规则只能增强，不能削弱。**
5. **不追求模块化而过度拆分文档。**
