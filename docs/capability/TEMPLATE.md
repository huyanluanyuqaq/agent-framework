# 平台 / 环境能力记录（模板）

> **本文件记录"实际能做什么"，不是"规范要求什么"。**
> 每条断言必须附**实测命令与实测输出**。未实测的一律写「未实测」。
>
> **引用前必须重测。** 平台设置、token、身份、仓库可见性都属于**可变事实**，
> 会随时间漂移。本文件 §8 是漂移记录区。

---

## 1. 仓库属性

| 项 | 值 | 实测命令 | 实测日期 |
|---|---|---|---|
| 仓库 | `owner/repo` | `gh api repos/owner/repo --jq .full_name` | |
| 可见性 | public / private | `gh api repos/owner/repo --jq .private` | |
| 默认分支 | | `gh api repos/owner/repo --jq .default_branch` | |
| Issues 启用 | | `gh api repos/owner/repo --jq .has_issues` | |

## 2. 分支保护

| 项 | 值 | 实测命令 |
|---|---|---|
| 是否存在保护 | | `gh api repos/owner/repo/branches/main/protection` |
| 必需 PR | | 同上，`.required_pull_request_requests` |
| 必需检查 | | 同上，`.required_status_checks.contexts` |
| 禁止强制推送 | | 同上，`.allow_force_pushes.enabled` |
| 禁止删除分支 | | 同上，`.allow_deletions.enabled` |
| 是否允许管理员绕过 | | 同上，`.enforce_admins.enabled` |
| 规则集（rulesets） | | `gh api repos/owner/repo/rulesets` |

> ⚠️ **CODEOWNERS 不能单独提供独立审查。** 它只自动请求审查者，
> 不创建独立身份、不启用审批、不阻止合并。

## 3. 身份与凭据

| 项 | 值 | 实测命令 |
|---|---|---|
| Git 身份（SSH/HTTPS） | | `ssh -T git@github.com` 或 `git remote -v` |
| `gh` 身份 | | `gh api user --jq .login` |
| token scopes | | `gh api -i user` 看 `x-oauth-scopes` |
| 是否可开 PR | | `gh pr create --help`（需 `repo` scope） |
| 是否可触发工作流 | | `gh api -i user` 看是否含 `workflow` scope |

> ⚠️ `gh auth status` 可能误报 token 无效（沙箱内无法读取凭据管理器时）。
> **以 `gh api user` 与 `gh api rate_limit` 的实测结果为准。**

## 4. 必须如实披露的限制

> 本节写"平台不强制、只能靠制度"的事项。**不得把文档中的禁止事项
> 描述为平台已强制。**

| # | 限制 | 说明 |
|---|---|---|
| 1 | 独立审查 | 若只有一个 GitHub 身份，平台审计记录无法区分 Coordinator 与 Developer，<br>「独立审查为流程约定，平台不强制」 |
| 2 | 检查时序 | 若某检查仅在合并后触发，它**不构成门禁** |
| 3 | 管理员绕过 | 若 `enforce_admins=false`，所有者可绕过全部保护 |

## 5. 本地环境约束

| 项 | 值 | 实测命令 |
|---|---|---|
| SSH(22) 可达 | | `ssh -T git@github.com` |
| HTTPS(443) 可达 | | `git ls-remote --heads <https-url>` |
| `gh` 可联网 | | `gh api rate_limit` |
| Git dubious ownership | | `git status`（报错即存在） |
| NTFS ACL Deny | | `(Get-Acl <path>).Access` |

## 6. 已实证的门禁行为（阳性/阴性对照）

| 编号 | 断言 | 实证方式 | 结论 |
|---|---|---|---|
| V1 | 直推默认分支被拒 | 探针分支推送 | |
| V2 | 必需检查失败时合并被阻止 | 探针 PR + `PUT /pulls/N/merge` | |
| V3 | 必需检查全绿时可正常合并 | 阳性对照 PR | |

## 7. 待办 / 已知缺口

| # | 缺口 | 影响 | 需要的操作 |
|---|---|---|---|

## 8. 漂移记录区

> 每次重测发现与上文不一致时，在此登记：**旧值 → 新值 → 原因 → 日期**。

| 日期 | 条目 | 旧值 | 新值 | 原因 |
|---|---|---|---|---|
