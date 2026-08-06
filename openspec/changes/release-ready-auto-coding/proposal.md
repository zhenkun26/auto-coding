## Why

productize-auto-coding 已交付 v0.1.0 基线并提交，但发布到 GitHub 前仍有阻塞项：上一 change 未走 Phase D（sync/archive）、中英 README 存在内容漂移、opsx 旧命令与 skills 双份拷贝、插件未做过本地安装验证。按用户要求：全部实现完成前不推送 GitHub。

## What Changes

- **BREAKING**: 移除 `openspec/commands/opsx/` 旧命令目录（Codex 产品以 `openspec/skills/` 为唯一技能源，README 使用示例同步改为 `$openspec-*` 技能调用）。
- 完成 `productize-auto-coding` 的 Phase D：delta specs 合并进主 specs、归档 change。
- 中英 README 内容对齐：以机械检查（标题结构一致性）收口，修正实质性内容差异，接受措辞详略差异。
- 发布前本地安装验证：通过 marketplace 实际安装插件并确认技能加载，验证后卸载。
- 补充 CHANGELOG 收口与最终提交；推送 GitHub 留待用户提供远端 URL 后执行。

## Capabilities

### New Capabilities
- `release-readiness`: 仓库在推送前满足发布闸门——规划归档、插件可安装验证、文档结构一致、旧命令清理。

### Modified Capabilities

（无现有 specs 需要修改）

## Impact

- 目录：删除 `openspec/commands/opsx/`；`openspec/specs/` 新增三个主 spec（plugin-distribution / legal-compliance / content-consistency）；`openspec/changes/productize-auto-coding/` 移至 archive。
- 文档：README.md / README-EN.md（使用示例、目录结构）、CHANGELOG.md。
- 验证设施：`scripts/check_repo.py` 增加 README 标题结构一致性检查。
- 本机 Codex 环境：临时安装/卸载 auto-coding 插件（验证用）。
