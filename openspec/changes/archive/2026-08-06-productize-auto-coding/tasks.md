## 1. 合规基线

- [x] 1.1 创建根目录 LICENSE（MIT，版权 "auto-coding contributors"，可在推送前改署名）
- [x] 1.2 创建 THIRD_PARTY.md：ponytail（MIT, DietrichGebert）、OpenSpec skills（MIT, Fission-AI）、grill-me（标注"需确认原创性"）
- [x] 1.3 顶层 SKILL.md、grill-me、pipeline 的 frontmatter 补 `license: MIT`

## 2. 命名统一与一致性修正

- [x] 2.1 README.md / README-EN.md 标题与正文统一为 auto-coding（sb_coding 仅作历史名首次出现）
- [x] 2.2 pipeline/SKILL.md 标题 "5-stage" → "6-stage"，与 frontmatter 与 README 一致
- [x] 2.3 修正 SKILL.md C1b 路由矛盾：正文与路由表统一（≤5 文件跳过节点2/3，>5 文件按 greenfield/brownfield 深度运行）
- [x] 2.4 重命名 pipeline/simulator_verify → pipeline/runtime_verify，更新 frontmatter name、ADAPTIVE.md 引用、README 目录树（中英）
- [x] 2.5 SKILL.md Phase 0 bootstrap 改为 `openspec init --tools codex`（移除 claude/.claude 导向）

## 3. 验证声明修正

- [x] 3.1 README.md 质量保障段：改写"10 套件/148 测试/ps1 脚本"为历史验证记录（资产未随仓库发布），删除 ps1 文件引用
- [x] 3.2 README-EN.md Quality assurance 段做同等修正，与中文版同步

## 4. Codex plugin 打包

- [x] 4.1 用 plugin-creator 脚手架生成 .codex-plugin/plugin.json（id=auto-coding, version=0.1.0, skills 清单）
- [x] 4.2 生成 marketplace 条目与安装文档（README 增补 install/update/uninstall 章节）

## 5. 测试与 CI

- [x] 5.1 tests/ 为 pipeline/_contract_check.py 补 pytest（happy path / edge / error），跑通
- [x] 5.2 新增 .github/workflows/ci.yml：pytest + markdown 链接检查 + frontmatter license 扫描

## 6. 版本与收尾

- [x] 6.1 创建 CHANGELOG.md（0.1.0，含重命名迁移说明）
- [x] 6.2 机械验证：simulator 零命中、5-stage 零命中、claude 零命中、sb_coding 仅历史引用、openspec validate 通过、测试通过
- [x] 6.3 git 提交（按功能分组），输出推送指引
