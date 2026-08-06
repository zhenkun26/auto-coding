## Context

上一个 change（productize-auto-coding）已实现 v0.1.0 并提交，但尚未走 Phase D；仓库仍有可清理的重复源与文档漂移（见 proposal.md - Why）。推送 GitHub 前需通过发布闸门；实际推送等待用户提供远端 URL。

## Goals / Non-Goals

**Goals:**
- 推送前所有可机械验证的闸门通过：规划归档、单一技能源、README 结构一致、插件可安装。
- 每个清理项都有可复现的检查，避免再次漂移。

**Non-Goals:**
- 不实际推送 GitHub（等用户 remote URL）。
- 不做中英 README 全量逐句翻译——只保证结构与实质性内容一致，接受详略差异。
- 不重建历史验证矩阵。

## Decisions

**D1: 删除 `openspec/commands/opsx/`，README 使用示例改为 `$openspec-*` 技能调用。**
Codex 只加载 `.codex/skills` 与 `openspec/skills` 形态，旧命令目录是 Claude 时代的遗留双副本，必然漂移。备选（保留并标注 legacy）被否决：仍保留漂移源。删除后 CHANGELOG 提供迁移说明。

**D2: README 对齐采用"结构一致性检查 + 实质差异修正"。**
在 `check_repo.py` 增加中英 README 标题结构对比；人工修正实质性内容差异。全量翻译工作量大、收益低，不在本次范围。

**D3: 本地安装验证走 marketplace 流程，验证后卸载。**
`codex plugin marketplace add` + `codex plugin add auto-coding@auto-coding` 确认技能加载，随后 remove 恢复环境。若本机配置写入被限制，降级为结构化校验并标注 `[SKIP_LOCAL_INSTALL]`。

**D4: Phase D 在本 change 内执行。**
`openspec sync` + `openspec archive` 处理 productize-auto-coding，产出主 specs 与归档目录，随本 change 一并提交。

## Risks / Trade-offs

- **删除 opsx 影响依赖旧命令的用户** → CHANGELOG 迁移说明；本产品定位 Codex，技能调用是唯一支持方式。
- **本地安装验证污染本机 Codex 配置** → 验证后卸载并给出恢复命令。
- **README 结构检查可能误报（如 EN 独有的小节）** → 检查允许明确的例外清单，合并且保留一致性收益。

## Migration Plan

1. 先做 Phase D（sync/archive），再删 opsx 并改 README 引用。
2. 加 README 结构检查，修正标题差异。
3. 本地安装验证（可降级）。
4. CHANGELOG 收口 + 全量验证 + 提交；推送留待用户提供 remote URL。

## Open Questions

- GitHub 仓库 URL（推送时提供）。
- LICENSE 署名与 grill-me 出处沿用 productize-auto-coding 的开放项，不阻塞本次实现。
