## Why

sb_coding 已从个人技能仓库成长为方法论完整但"不可发布"的状态：无许可、无打包形态、命名不一致、README 宣称的验证矩阵无法复现。目标是把本项目迭代成可上 GitHub、可一键安装的 Codex Skill 产品，并在此过程中用体系自身完成 dogfooding。

## What Changes

- **BREAKING**: 产品统一命名为 `auto-coding`（顶层 SKILL.md frontmatter 已是该名，README、plugin 元数据、目录说明全部对齐；仓库对外沿用原 sb_coding 语义作为历史名）。
- 新增 MIT LICENSE 与 THIRD_PARTY.md（ponytail / openspec 第三方许可与来源声明）。
- 新增 Codex plugin 形态：`.codex-plugin/plugin.json` + marketplace 条目，支持一键安装与版本更新。
- 修正内容一致性硬伤：C1b 路由矛盾、pipeline 5-stage/6-stage 命名、`simulator_verify` 改名 `runtime_verify`、Phase 0 `openspec init --tools claude` 改为 codex。
- 修正 README 验证声明：移除/改写不可复现的"10 套件/148 测试/ps1 脚本"表述，改为诚实记录当前验证状态。
- 为 `pipeline/_contract_check.py` 补充单元测试，并新增 CHANGELOG 与基础 CI。

## Capabilities

### New Capabilities
- `plugin-distribution`: auto-coding 以 Codex plugin + marketplace 形式发布，包含 plugin.json、版本号与 CHANGELOG，用户可一键安装。
- `legal-compliance`: 仓库以 MIT 许可发布，第三方组件（ponytail、openspec）保留来源与许可声明。
- `content-consistency`: 产品命名、复杂度路由、阶段编号、组件命名在所有文档间一致；验证声明可复现。

### Modified Capabilities

（无现有 specs 需要修改）

## Impact

- 全仓库 Markdown 文档（SKILL.md、README.md、README-EN.md、pipeline/、adaptive/、self_verify/）。
- 目录结构：`pipeline/simulator_verify/` → `pipeline/runtime_verify/`。
- 新增文件：LICENSE、THIRD_PARTY.md、CHANGELOG.md、`.codex-plugin/plugin.json`、marketplace 条目、`tests/`、`.github/workflows/`。
- 本变更同时作为体系自身的第一个 C2 dogfooding 案例。
