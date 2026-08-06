## Context

当前仓库是方法论完整的技能包，但缺少可发布形态（见 proposal.md - Why）。约束：仅面向 Codex、MIT 许可、产品名 auto-coding、以 plugin + marketplace 发布。仓库内容全部为 Markdown 文档 + 一个 312 行 Python 契约检查脚本，无运行时依赖。

## Goals / Non-Goals

**Goals:**
- 一次性完成"可发布基线"：许可、打包、命名、一致性、可验证性。
- 所有修正可被 grep/测试机械验证，避免再次漂移。

**Non-Goals:**
- 不改动方法论本身（复杂度分流、阈值、节点设计保持现状，只修正描述矛盾）。
- 不重建"10 套件/148 测试"验证矩阵（作者手上没有原始资产），只诚实标注历史状态。
- 不实际创建 GitHub 远端仓库或执行 marketplace 发布（需要用户提供仓库 URL）。

## Decisions

**D1: 产品名采用 `auto-coding`，`sb_coding` 降级为历史引用。**
用户已选 auto-coding 且顶层 SKILL.md frontmatter 已是该名，改名成本最低；README 标题、plugin.json、CHANGELOG 全部统一，正文首次出现时标注"原名 sb_coding"。备选（保留 sb_coding）被否决。

**D2: 插件打包为单 plugin + 多 skills。**
`.codex-plugin/plugin.json` 声明 `auto-coding` plugin，bundled skills 覆盖：入口 auto-coding（顶层 SKILL.md）、grill-me、pipeline、ponytail（含 exported 子技能）、openspec 六技能。self_verify 与 adaptive 是 pipeline 技能的参考文档，不作为独立技能打包。manifest 具体 schema 由 plugin-creator 技能脚手架生成后核对。

**D3: `simulator_verify` 重命名为 `runtime_verify`。**
目录、frontmatter name、ADAPTIVE.md 引用、README 目录树三处同步；这是 Node 6 运行时验证组件，旧名有误导性。备选（保留旧名）会持续误导新用户。

**D4: 验证声明改为"可复现承诺"。**
README QA 段改写为两层：仓库内可复现的（L0/L1/L2 协议、_contract_check.py、新增 pytest）与历史验证记录（标注"原验证资产未随仓库发布，待重建"）。ps1 脚本引用删除。

**D5: 一致性修正全部以机械检查收口。**
每个修正项对应一个 grep 断言（如 `grep -rn 'simulator' .` 应零命中、`grep -c '5-stage' pipeline/SKILL.md` 应为 0），保证文档间不再次漂移。

**D6: 测试与 CI 从"宣称"变为"随仓库"。**
`tests/` 为 `_contract_check.py` 提供 pytest 覆盖（happy path / edge / error）；`.github/workflows/ci.yml` 跑 pytest + markdown 链接检查 + frontmatter 扫描。

## Risks / Trade-offs

- **重命名破坏用户工作流** → CHANGELOG 与 README 加迁移说明：旧 `simulator_verify` 引用在 0.1.0 起失效。
- **marketplace 发布依赖远端仓库** → 本变更只交付 manifest 与安装文档；实际 publish 命令留待推送后执行。
- **grill-me 出处不明** → THIRD_PARTY.md 中标注"需维护者确认原创性"；若确认改编自第三方，发布前必须补充来源与许可。
- **README 中英再漂移** → 本变更同步修改两份 README 的受影响章节；长期用 CI 的章节结构对比（可选）控制。

## Migration Plan

1. 先做一致性修正与改名（单文件、可验证），再做合规与文档改写。
2. plugin 脚手架与 manifest 在内容稳定后生成。
3. 测试 + CI 最后落地，跑通后统一提交。
4. 推送至用户仓库后：创建 marketplace 发布、打 v0.1.0 tag、CHANGELOG 收口。

## Open Questions

- 用户 GitHub 仓库名与 URL（marketplace 条目需要）。
- LICENSE 版权人署名：默认 "auto-coding contributors"，用户可在推送前改为个人名。
