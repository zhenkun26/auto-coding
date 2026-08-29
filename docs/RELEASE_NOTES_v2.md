# v2.0.0 迭代方案与发布说明

> **状态**：已发布（2026-08-29）。本文同时作为 GitHub Release 正文（`release.yml` 的 `body_path`）。

## v2.0.0 — 更少的过程，更多的证据

auto-coding v1 证明了一件事：AI 编码助手需要风险感知的执行深度和不可造假的验证证据。但它也背上了一个不必要的包袱——把 OpenSpec 当成了内核依赖，要求每个使用者先理解一套规格系统的仪式。

v2 做的是减法。**风险路由和证据纪律留在内核，规格系统降级为可选外挂**：仓库里已有任何规划工作流（OpenSpec、spec-kit、issue 流程）就尊重它，没有就内联规划。仅此一条，不再需要"三选一执行边界"。

### 移除的重量

- **OpenSpec 出内核**：执行边界从"Standalone / OpenSpec-managed / Not yet bounded"三选一简化为一句话——"仓库已有规划工作流则以之为规划权威，否则内联规划"。`[NO_OPENSPEC]` 标记、任务勾选同步协议、sync/archive 收尾建议全部从核心契约中移除。
- **规格系统支持拆为可选伴侣 skill**（`auto-coding-openspec`，单独安装）：OpenSpec 用户的完整工作流不变，其他用户不再为其付出任何上下文成本。
- **仓库自食其果的部分一并清除**：本仓库的 `openspec/` 目录（23 个文件约 1000 行）与 6 个 openspec 辅助 skill 已移除（git 历史可溯），改用 [DECISIONS.md](DECISIONS.md)（ADR）+ GitHub issues + CHANGELOG 记录决策——这也是新默认路径的活示范。
- **词汇瘦身**：L0/L1/L2 自检、R1/R2/R6/R8 冲突裁决、逃逸门等自造概念合并进直白语言与不可协商规则，核心概念压缩到 10 个以内。`SKILL.md` 从 201 行减至 123 行。

### 新增的能力

- **`verify-evidence` 独立小 skill**：四态证据（PASS / FAIL / BLOCKED / NOT_APPLICABLE）与工具链验证纪律单独成件、可自动触发，不必安装整套 auto-coding 也能搭配自己的工作流使用。
- **`/setup-auto-coding` 一次性配置**：选严格度档位（strict / default / light）、主语言与证据阈值，配置写入 AGENTS.md 的 `## auto-coding` 小节——不发明新配置格式，普通文件即状态。
- **`npx skills add zhenkun26/auto-coding` 安装通道**：与 Codex plugin 并行，覆盖 Claude Code 等其他 agent；四个 skill 各自成目录、安装时可勾选，用户拿到的是可自行修改的普通文件。
- **README 定位对比表**：与 spec-kit、OpenSpec、GSD、mattpocock/skills 的生态位差异一页讲清。

### 不变的部分，以及为什么

四态证据纪律、防降级规则（High-risk 永不降档）、六个风险标志、对抗性测试夹具、脚本与 CI 自检——这些是 auto-coding 与"流程接管型"项目的根本区别，v2 一行不动。本仓库的迭代方式（在同一仓库做减法而非另起炉灶）本身就是这套价值观的示范：脚本、测试、打包全部存活，被重写的只有文字层。

### 定位对比

| | spec-kit / OpenSpec / GSD | mattpocock/skills | auto-coding v2 |
|:---|:---|:---|:---|
| 生态位 | 规格驱动开发流程 | 对齐、规划与设计工作流 | 交付保真：风险路由 + 证据纪律 |
| 状态存放在 | 规格目录 / change 目录 | issue tracker、CONTEXT.md、ADR | 仓库本身 + 可选单状态文件 |
| 上手成本 | 需先学习规格仪式 | 低 | 低（默认零过程文件） |
| 适合谁 | 团队需要正式规格 | 日常工程对齐 | 要"验证证据不可造假"的个人与小团队 |

### 迁移指南

- **OpenSpec 用户**：安装 `auto-coding-openspec` 伴侣 skill（把仓库根的 `auto-coding-openspec/` 复制到 skills 目录），行为与 v1 一致。
- **其他用户**：无需任何迁移。v1 中 OpenSpec 相关指令本来就不会触发。
- **本仓库协作者**：决策记录以 [DECISIONS.md](DECISIONS.md) 为准；历史规格树可通过 git 历史查看（`git log -- openspec/`）。

### 版本策略（自 v2 起生效）

`pyproject.toml` 是唯一版本事实源，插件清单版本由 CI 机械校验一致（见 `scripts/check_repo.py`）。语义化版本对 skill 内容的含义：**MAJOR** = 执行契约或路由行为变化；**MINOR** = 新增 references、脚本或安装通道；**PATCH** = 文字与文档修正。发布时去掉 `-dev` 后缀打 `v*` tag。

---

## v2.0.0 — Less Process, More Evidence

auto-coding v1 proved that AI coding assistants need risk-aware execution depth and unfakeable verification evidence. It also carried an unnecessary burden: OpenSpec as a kernel dependency, asking every user to learn a spec system's ceremony first.

v2 subtracts. **Risk routing and evidence discipline stay in the kernel; spec systems become an optional add-on**: respect whatever planning workflow a repository already has (OpenSpec, spec-kit, an issue flow), otherwise plan inline. One rule replaces the three-way execution boundary.

### Weight removed

- **OpenSpec leaves the kernel**: the execution boundary collapses from "Standalone / OpenSpec-managed / Not yet bounded" to one sentence — "if the repository already has a planning workflow, treat it as planning authority; otherwise plan inline." The `[NO_OPENSPEC]` marker, task-checkbox sync protocol, and sync/archive wrap-up suggestions are all removed from the core contract.
- **Spec support moves to an optional companion skill** (`auto-coding-openspec`, installed separately): OpenSpec users keep their full workflow; everyone else pays zero context cost for it.
- **The repo stops dogfooding the weight**: this repository's `openspec/` tree (23 files, ~1000 lines) and the six openspec helper skills are removed (recoverable from git history) in favor of [DECISIONS.md](DECISIONS.md) (ADRs) + GitHub issues + CHANGELOG — a live demonstration of the new default path.
- **Vocabulary diet**: invented concepts (L0/L1/L2 self-checks, R1/R2/R6/R8 rulings, escape gates) merge into plain language and non-negotiable rules; core concepts compress below 10. `SKILL.md` shrinks from 201 to 123 lines.

### Capabilities added

- **A standalone `verify-evidence` skill**: the four-state evidence discipline (PASS / FAIL / BLOCKED / NOT_APPLICABLE) and toolchain verification, usable with any workflow without installing the whole skill.
- **`/setup-auto-coding` one-time setup**: strictness profile (strict / default / light), primary language, and evidence thresholds written as an `## auto-coding` section into `AGENTS.md` — no new config format; ordinary files are the state.
- **`npx skills add zhenkun26/auto-coding`**: alongside the Codex plugin, covering Claude Code and other agents; all four skills as self-contained, individually pickable directories of ordinary, editable files.
- **A README positioning table**: one page on how this differs from spec-kit, OpenSpec, GSD, and mattpocock/skills.

### What does not change, and why

Four-state evidence, anti-degradation rules (High-risk never downgrades), the six risk flags, adversarial test fixtures, and script/CI self-checks are what separate auto-coding from process-owning frameworks — v2 does not touch them. Iterating inside the same repository rather than starting fresh is itself a demonstration of these values: scripts, tests, and packaging survive intact; only the prose layer is rewritten.

### Migration guide

- **OpenSpec users**: install the `auto-coding-openspec` companion skill (copy `auto-coding-openspec/` from the repo root into your skills directory); behavior matches v1.
- **Everyone else**: no migration needed — the OpenSpec paths never triggered by default in v1.
- **Repository collaborators**: decision records live in [DECISIONS.md](DECISIONS.md); the historical spec tree remains viewable via git history (`git log -- openspec/`).

### Version policy (effective with v2)

`pyproject.toml` is the single version source; the plugin manifest version is mechanically checked for consistency in CI (see `scripts/check_repo.py`). Semver for skill content: **MAJOR** = contract or routing behavior change; **MINOR** = new references, scripts, or install channels; **PATCH** = wording and documentation fixes. Releases drop the `-dev` suffix and tag `v*`.
