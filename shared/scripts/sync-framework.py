#!/usr/bin/env python3
"""sync-framework.py — 把中央公共规范同步到项目（本地层，零权限）。

设计目标（对应任务书 §6.3）：
  1. 可手动触发（CLI）
  2. 可指定全部项目 / 单个项目
  3. 可指定规范版本（git tag）
  4. 同步前检查目标仓库
  5. 同步后创建独立分支
  6. 每个项目一个独立分支与提交
  7. PR 标题/描述说明公共规范更新
  8. 失败时输出清晰错误并非零退出
  9. 可重复执行、可回滚
 10. 默认不推送、不合并（推送与开 PR 需显式 --push）

用法：
  python shared/scripts/sync-framework.py --list
  python shared/scripts/sync-framework.py --project shadcn-admin [--dry-run]
  python shared/scripts/sync-framework.py --all [--version 2.0.0]
  python shared/scripts/sync-framework.py --project <name> --push

安全约束：
  - 永不直接推送到项目主分支
  - 永不自动合并 PR
  - 目标仓库工作区必须干净（除非 --allow-dirty）
  - 只写入 `.agent-framework/**` 与 `framework-version.json`
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

FRAMEWORK_ROOT = Path(__file__).resolve().parent.parent.parent
WORKSPACE_ROOT = FRAMEWORK_ROOT.parent
PROJECTS_DIR = WORKSPACE_ROOT / "projects"

# 同步范围（任务书 6.2）。审计脚本必须同步 —— 门禁若各项目持一份副本就会漂移，
# 而漂移的门禁等于没有门禁（PR #43 的教训：F10 丢失正源于此）。
SYNC_SCRIPTS = ["audit-project.py"]


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and proc.returncode != 0:
        raise RuntimeError(
            f"命令失败 ({proc.returncode}): {' '.join(cmd)}\n"
            f"  stdout: {proc.stdout.strip()}\n  stderr: {proc.stderr.strip()}"
        )
    return proc


def git(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return run(["git", "-c", "safe.directory=*", *args], cwd=cwd, check=check)


def fail(msg: str) -> None:
    print(f"[ERROR] {msg}", file=sys.stderr)
    sys.exit(1)


def load_version() -> dict:
    vf = FRAMEWORK_ROOT / "framework-version.json"
    if not vf.is_file():
        fail(f"找不到 {vf}")
    return json.loads(vf.read_text(encoding="utf-8"))


def discover_projects() -> list[str]:
    if not PROJECTS_DIR.is_dir():
        fail(f"找不到 projects 目录：{PROJECTS_DIR}")
    return sorted(
        p.name for p in PROJECTS_DIR.iterdir()
        if p.is_dir() and (p / ".git").is_dir()
    )


def sync_one(project_name: str, version: str, dry_run: bool, allow_dirty: bool, push: bool) -> bool:
    project = PROJECTS_DIR / project_name
    print(f"\n=== {project_name} ===")

    if not (project / ".git").is_dir():
        print("  [SKIP] 不是 Git 仓库")
        return False

    branch = git(project, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    if branch != "main":
        print(f"  [FAIL] 当前分支 {branch} != main，请先切回")
        return False

    # 工作区检查只对「会写入」的路径生效；dry-run 不落盘，无需干净工作区。
    if not dry_run:
        if not allow_dirty:
            dirty = git(project, "status", "--porcelain", check=False).stdout.strip()
            if dirty:
                print(f"  [FAIL] 工作区不干净，拒绝同步（保护未提交工作）：\n{dirty}")
                return False
        else:
            print("  [WARN] --allow-dirty：跳过工作区检查")

    src_dir = FRAMEWORK_ROOT / ".agents"
    dst_dir = project / ".agent-framework"
    files = sorted(p for p in src_dir.iterdir() if p.is_file() and p.suffix == ".md")
    if not files:
        print(f"  [FAIL] 源规范目录为空：{src_dir}")
        return False

    script_src = FRAMEWORK_ROOT / "shared" / "scripts"
    scripts = [script_src / s for s in SYNC_SCRIPTS if (script_src / s).is_file()]
    if not scripts:
        print(f"  [FAIL] 审计脚本缺失：{script_src}/{SYNC_SCRIPTS}")
        return False

    print(f"  将同步 {len(files)} 个规范文件 -> .agent-framework/；"
          f"{len(scripts)} 个脚本 -> shared/scripts/")
    if dry_run:
        for f in files:
            print(f"    [dry-run] {f.name}")
        for s in scripts:
            print(f"    [dry-run] shared/scripts/{s.name}")
        print("  [dry-run] 不写入、不提交")
        return True

    dst_dir.mkdir(exist_ok=True)
    for f in files:
        shutil.copy2(f, dst_dir / f.name)

    dst_scripts = project / "shared" / "scripts"
    dst_scripts.mkdir(parents=True, exist_ok=True)
    for s in scripts:
        shutil.copy2(s, dst_scripts / s.name)

    vf = project / "framework-version.json"
    payload = {
        "framework": "agent-framework",
        "version": version,
        "source": "huyanluanyuqaq/agent-framework",
        "lastSyncedAt": date.today().isoformat(),
    }
    vf.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    branch_name = f"chore/framework-sync-{version}"
    if git(project, "rev-parse", "--verify", branch_name, check=False).returncode == 0:
        print(f"  [WARN] 分支 {branch_name} 已存在，将复用")
        git(project, "checkout", branch_name)
    else:
        git(project, "checkout", "-b", branch_name)

    git(project, "add", ".agent-framework", "framework-version.json", "shared/scripts")
    staged = git(project, "diff", "--cached", "--name-only").stdout.strip()
    if not staged:
        print("  [OK] 无差异，已是最新版本")
        git(project, "checkout", "main")
        return True

    msg = (
        f"chore(framework): sync agent-framework v{version}\n\n"
        f"同步公共规范到 .agent-framework/（{len(files)} 个文件）与 shared/scripts/（{len(scripts)} 个脚本）。\n"
        f"版本来源：huyanluanyuqaq/agent-framework v{version}\n\n"
        f"Changed files:\n" + "\n".join(f"- {line}" for line in staged.splitlines())
    )
    git(project, "commit", "-m", msg)
    print(f"  [OK] 已提交到分支 {branch_name}")

    if push:
        try:
            git(project, "push", "-u", "origin", branch_name)
            print(f"  [OK] 已推送 {branch_name}")
            pr = run(
                ["gh", "pr", "create", "--base", "main", "--head", branch_name,
                 "--title", f"chore(framework): sync agent-framework v{version}",
                 "--body",
                 "## 公共规范同步\n\n"
                 f"- 框架：agent-framework\n- 版本：v{version}\n"
                 f"- 同步文件：`.agent-framework/**`（{len(files)} 个）、`shared/scripts/audit-project.py`\n"
                 "- 版本文件：`framework-version.json`\n\n"
                 "未覆盖：`AGENTS.md` / `README.md` / 项目技术配置 / 业务代码 / 项目专属 CI"],
                cwd=project, check=False,
            )
            if pr.returncode == 0:
                print(f"  [OK] PR 已创建：{pr.stdout.strip()}")
            else:
                print(f"  [WARN] 推送成功但 PR 创建失败（可手动创建）：{pr.stderr.strip()}")
        except Exception as exc:  # noqa: BLE001
            print(f"  [WARN] 推送失败（本地提交仍保留）：{exc}")
    else:
        print("  [INFO] 未推送。手动执行：")
        print(f"         cd {project}")
        print(f"         git push -u origin {branch_name}")

    git(project, "checkout", "main")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="同步中央公共规范到项目")
    ap.add_argument("--list", action="store_true", help="列出可同步的项目")
    ap.add_argument("--project", help="指定单个项目")
    ap.add_argument("--all", action="store_true", help="同步全部项目")
    ap.add_argument("--version", help="指定规范版本（默认取 framework-version.json）")
    ap.add_argument("--dry-run", action="store_true", help="只预览，不写入")
    ap.add_argument("--allow-dirty", action="store_true", help="允许目标仓库工作区不干净")
    ap.add_argument("--push", action="store_true", help="推送分支并尝试创建 PR")
    args = ap.parse_args()

    meta = load_version()
    version = args.version or meta["version"]

    if args.list:
        print("可同步的项目：")
        for name in discover_projects():
            print(f"  - {name}")
        return 0

    if not args.project and not args.all:
        ap.error("必须指定 --project <name> 或 --all（或用 --list 查看）")

    available = discover_projects()
    targets = available if args.all else [args.project]
    unknown = [t for t in targets if t not in available]
    if unknown:
        fail(f"未知项目：{unknown}。可用：{available}")

    print(f"中央规范版本：v{version}")
    print(f"目标项目：{targets}")
    print(f"模式：{'dry-run' if args.dry_run else 'apply'}{' + push' if args.push else ''}")

    ok = [t for t in targets if sync_one(t, version, args.dry_run, args.allow_dirty, args.push)]
    bad = [t for t in targets if t not in ok]

    print("\n===== 汇总 =====")
    print(f"  成功：{len(ok)}/{len(targets)}  {ok}")
    if bad:
        print(f"  失败：{len(bad)}  {bad}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
