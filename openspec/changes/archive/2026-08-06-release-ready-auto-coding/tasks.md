## 1. 规划收尾（Phase D）

- [x] 1.1 运行 `openspec sync productize-auto-coding`：delta specs 合并进 `openspec/specs/`
- [x] 1.2 运行 `openspec archive productize-auto-coding`：change 归档到 `openspec/changes/archive/`

## 2. 单一技能源

- [x] 2.1 删除 `openspec/commands/opsx/` 旧命令目录
- [x] 2.2 README.md / README-EN.md 的使用示例与目录树改为 `$openspec-*` 技能调用，不再引用 `commands/opsx`

## 3. README 中英结构一致性

- [x] 3.1 `scripts/check_repo.py` 增加中英 README 标题结构对比检查
- [x] 3.2 对齐 README.md 与 README-EN.md 章节标题并修正实质性内容差异

## 4. 本地安装验证

- [x] 4.1 通过 marketplace 本地安装 auto-coding 插件并确认技能加载
- [x] 4.2 验证后卸载插件与 marketplace，恢复本机环境

## 5. 收口

- [x] 5.1 CHANGELOG.md 更新 0.1.0 条目（opsx 清理、安装验证、README 对齐）
- [x] 5.2 全量验证（openspec validate / pytest / check_repo / plugin validate）并 git 提交
- [x] 5.3 输出推送指引（等待用户提供 GitHub remote URL）
