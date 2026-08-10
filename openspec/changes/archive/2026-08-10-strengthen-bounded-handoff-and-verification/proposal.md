## Why

`auto-coding` 已具备风险路由、最小实现和证据化交付，但当前任务拆分仍以“单文件”为主要原子性标准，OpenSpec task 会在实现后立即勾选，验证流程也缺少对默认值、调用方覆盖、非法输入、失败清理和兼容路径的统一相邻检查。这些规则容易让一个完整结果被机械拆碎，或让“代码已写”“局部测试已过”过早升级为已完成。

## What Changes

- 将 Standard/High-risk 的任务边界从“单文件/单函数”调整为“单一结果、单一主要风险边界、独立验收门”，允许实现、测试和必要契约同步构成一个最小完整改动。
- 区分 standalone 与 OpenSpec-managed 执行；OpenSpec 是规划权威，执行者不得静默扩展或修正规格边界，也不得仅凭实现完成更新验收状态。
- 为契约或行为修复增加相邻路径检查：默认输入、调用方覆盖、缺失/非法输入、失败清理和兼容行为。
- 固化证据生成顺序：实现、定向回归、相邻检查、相关全量门禁、原始结果、交付报告/状态。
- 对 High-risk、外部副作用和跨会话交接增加按需 pre-code rehearsal，并在连续修复引入实质回归时触发停止补丁和根因复审。
- 删除验证失败时自动执行 `git checkout` 的规则，保留失败现场并避免覆盖用户或任务前已有修改。
- 让仓库/CI 已声明的验证阈值优先；默认覆盖率与轮次限制作为无项目规则时的指导，不冒充通用通过标准。
- 补齐 Go/Rust 工具链 reference 与探测测试闭环，不引入新的常驻 phase/STATUS/STEP 文档体系。

## Capabilities

### New Capabilities

- `bounded-delivery`: 定义结果导向的任务边界、OpenSpec-managed 交接、相邻路径验证、修复熔断和证据顺序。

### Modified Capabilities

（无）

## Impact

- 主契约：`SKILL.md`。
- 规划与执行规则：`references/planning.md`、`references/implementation.md`、`references/openspec.md`。
- 验证与高风险控制：`references/verification.md`、`references/risk-controls.md`、相关 toolchain references。
- 探测与验证：`scripts/detect_project.py`、`tests/test_detect_project.py`，以及必要的仓库一致性测试。
- 发布副本：实现完成后需通过现有同步脚本更新 `plugins/auto-coding/`，但本 change 不引入第二套 skill 或状态文件。
