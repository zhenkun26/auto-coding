# auto-coding — 风险感知的 AI 编码交付 skill

🌐 语言 / Language：[简体中文](README.md) · [English](README-EN.md)

一套面向 AI 编码助手的**风险感知交付 skill**：按不确定性与操作风险分流执行深度，按需规划、最小改动、用项目自有工具链验证、凭证据交付。

## 它是什么

auto-coding 帮助编码智能体在修改代码时：先识别风险与约束，再以与任务相称的深度规划、实现、验证并交付结果。它由一套在 vibe coding 中反复踩坑后沉淀的并联开发体系（OpenSpec 规划 + Pipeline 执行 + Ponytail 代码最小化 + grill-me 决策追问）重构而来——保留全部实战机制，换上更克制的骨架：

- **主文件只留合同**：`SKILL.md` 约 160 行，细节全部下放到 12 份按需读取的 references；
- **默认零过程文件**：不再产出 TASK_PLAN / LOCATE_MAP / RUN_LOG 等十几个流水线文件，只有长任务才使用单一状态文件；
- **授权边界前置**：初始化规格系统、安装依赖、提交、部署、迁移、删除都需要显式授权。

## 核心理念

不是所有改动都应走相同的重型流水线。本 skill 根据不确定性、影响范围和操作风险选择执行深度：**风险优先于改动大小**——即使只有一行代码，鉴权和金额逻辑也属于 High-risk。

它强调最小且完整的改动：优先复用现有实现、标准库和已安装依赖（复用 > stdlib > 已装依赖 > 新代码），避免无关重构、流程文件膨胀和未经授权的副作用。验证证据严格区分 `PASS` / `FAIL` / `BLOCKED` / `NOT_APPLICABLE`，`BLOCKED` 永不当 `PASS`。

## 三条执行路径

| 路径 | 适用情况 | 最低执行深度 |
|:---|:---|:---|
| **Fast** | 单文件、明确、低风险、易回滚 | 定位、最小修改、L0/L1 自检 |
| **Standard** | 多文件行为、接口变化或明显不确定性 | 简短计划、调用方感知实现、静态检查与测试 |
| **High-risk** | FINANCE / AUTH / MIGRATION / STATE_MACHINE / EXTERNAL_API / ENV_OPS，或并发、破坏性行为 | 书面不变量与回滚策略、分步实现、风险专项验证 |

Greenfield/brownfield 不影响路由等级，只影响规划与定位深度（greenfield 无既有代码可定位，直接创建）。

## 工作方式

1. 读取仓库规则、CI 与当前工作区状态；可用 `scripts/detect_project.py` 只读探测项目形态。
2. 选择 Fast / Standard / High-risk 路由。
3. 按路由深度规划；≥3 个未决设计决策时执行决策追问（decision-grilling）。
4. 沿复用梯子实现，每个任务执行 L0（导入）→ L1（行为断言）→ L2（契约比对）三层自检，带层级类型检查点与逃逸门检测。
5. 用项目已有命令验证；缺失工具按 adaptive 规则处理（有配置无工具→中断提示；无配置→降级为替代证据并如实标注）。
6. 汇报改动、验证证据、逃逸门、假设与后续动作；提交、规格 sync/archive 仅作为建议，需授权后执行。

冲突裁决（需求存在性以规格为准、代码复用以复用为准、规格缺陷回滚报缺陷、任务清单以事实为准）详见 [references/conflict-rulings.md](references/conflict-rulings.md)。

## 安全边界

本 skill 不会自动：

- 初始化 OpenSpec 或其他规格系统
- 安装依赖
- 提交、推送、发布或部署
- 删除文件、执行数据迁移或修改远程服务
- 把无法执行的验证说成通过

这些操作需要用户明确授权。无法运行的验证标记为 `BLOCKED`，并与替代证据分开说明。

## 持续沉淀与断点恢复

- **默认无沉淀**。唯一的常驻产物是 `ai_pipeline/ERROR_MEMORY.md`，且仅在发生自愈、逃逸门或 Critical 失败时追加（见 [references/sedimentation.md](references/sedimentation.md)）。
- **断点恢复**：仅长任务/易中断任务使用单一状态文件 `ai_pipeline/state.json`，由 `scripts/manage_state.py` 原子化读写（见 [references/recovery.md](references/recovery.md)）。下次调用时如实打印断点并询问 resume 或 restart。

## 目录结构

```
├── SKILL.md                     # 总控：核心契约、路由、工作流、资源地图
├── references/                  # 按需读取的 12 份参考
│   ├── routing.md               #   Fast/Standard/High-risk 分流与风险标志
│   ├── planning.md              #   按比例的规划、原子拆解、决策追问
│   ├── implementation.md        #   复用梯子、定位法、L0/L1/L2 自检、逃逸门
│   ├── verification.md          #   静态/运行时闸门、阈值单一事实源
│   ├── risk-controls.md         #   六个风险标志的不可降级控制
│   ├── adaptive.md              #   工具链自适应与降级规则
│   ├── conflict-rulings.md      #   R1/R2/R6/R8 冲突裁决
│   ├── sedimentation.md         #   ERROR_MEMORY / TECH_NOTES（可选）
│   ├── recovery.md              #   跨会话断点恢复
│   ├── openspec.md              #   已有 OpenSpec 工作流的消费与收尾
│   └── toolchain-python.md / toolchain-typescript.md
├── scripts/
│   ├── detect_project.py        # 只读项目探测（语言/CI/规格系统/greenfield）
│   ├── manage_state.py          # 原子化单一状态文件
│   ├── check_python_contracts.py# Python 结构契约检查（AST + Gherkin 回退）
│   ├── state_schema.json        # 状态文件参考 schema
│   ├── check_repo.py            # 仓库机械检查（链接/许可/双语 README 一致性）
│   └── sync_plugin_skills.sh    # 插件包同步（单一事实源为仓库根）
├── plugins/auto-coding/         # Codex plugin 包
├── tests/                       # pytest 测试套件
└── openspec/                    # 本仓库自身的规格（dogfooding）
```

## 安装

发布形态为 Codex plugin + marketplace，仓库内 marketplace 位于 `.agents/plugins/marketplace.json`。

```bash
# 从 GitHub 安装
codex plugin marketplace add zhenkun26/auto-coding
codex plugin add auto-coding@auto-coding

# 本地开发安装
codex plugin marketplace add /path/to/this/repo
codex plugin add auto-coding@auto-coding

# 更新 / 卸载
codex plugin marketplace upgrade
codex plugin remove auto-coding@auto-coding
```

修改技能内容后，发布前运行 `bash scripts/sync_plugin_skills.sh` 重新同步插件包。

## 使用

```
Use $auto-coding to implement this change with risk-aware routing and verification.
```

或直接描述任务，由 skill 自己完成路由。已有 OpenSpec 的仓库可以直接交接变更目录：`按 auto-coding 实现 openspec/changes/<name>/`。

## 环境约束

| 依赖 | 必需？ | 缺失时 |
|:---|:---|:---|
| bash（POSIX sh） | 必需 | 无降级——bash 是执行环境 |
| git | 提交时必需 | 代码已写但未提交，如实标注 |
| Python 3.10+ | 契约检查/检测脚本 | 契约检查降级为人工 L2 清单 |
| mypy / ruff / pytest | Python 模板 | 有配置无工具→安装提示并中断；无配置→`BLOCKED` + 替代证据 |
| tsc / eslint / jest | TS 模板 | 同上 |
| OpenSpec CLI | 可选 | 全程 `[NO_OPENSPEC]` 内联规划，不自动初始化 |

## 质量保障

- 三层自检（L0/L1/L2）+ 硬性闸门：类型检查 Critical（失败中断+回滚）、lint Standard（自愈 ≤3 轮）、覆盖率默认行 ≥80% / 分支 ≥70%。
- 层级类型检查点：每完成一个拓扑层对所有已写文件全量类型检查，捕获跨文件类型错误。
- 逃逸门检测：以 `Any` / `# type: ignore` / `cast()` 保命的自愈记为 `[ESCAPE_HATCH]` 质量债，交付时如实列出。
- 自动化契约检查：AST 比对规格签名与实际代码，命名空间感知（`ClassName.method`），空契约不误报通过。
- 仓库自检：pytest 测试套件 + markdown 链接完整性 + 许可头扫描 + 中英 README 结构一致性，全部在 CI 中运行（`.github/workflows/ci.yml`）。

## 第三方组件与许可

MIT License。复用梯子（reuse ladder）改写自 Ponytail（MIT）；历史版本曾捆绑 OpenSpec 技能与 grill-me。详见 [THIRD_PARTY.md](THIRD_PARTY.md) 与 [CHANGELOG.md](CHANGELOG.md)。
