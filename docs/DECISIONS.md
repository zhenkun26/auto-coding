# auto-coding 技术决策记录

> 本文件只记录影响 skill 结构、验证边界和发布方式的取舍。依据 README、CHANGELOG、git 历史和验收报告；历史验收报告中已经移除的 v0.1.0 容器路径不视为当前架构。

## 索引

| ID | 决策 | 状态 | 证据 |
|---|---|---|---|
| ADR-AC-001 | 单一风险感知 skill + 按需 references | accepted | CHANGELOG 0.2.0、README |
| ADR-AC-002 | Fast/Standard/High-risk 三档路由 | accepted | CHANGELOG 0.2.0、README |
| ADR-AC-003 | 证据状态使用 PASS/FAIL/BLOCKED/NOT_APPLICABLE | accepted | README、验收报告 |
| ADR-AC-004 | 根仓库为 skill 单一事实源，插件包由同步脚本生成 | accepted | CHANGELOG、`sync_plugin_skills.sh` |
| ADR-AC-005 | pyproject 为唯一版本事实源，CI 机械校验插件清单一致 | accepted | `check_repo.check_version_consistency`、CHANGELOG |
| ADR-AC-006 | 四层记忆模型 + 证据时效规则应对运行中遗忘 | accepted | `docs/MEMORY_STRATEGY.md`、`references/recovery.md`、`references/sedimentation.md` |
| ADR-AC-007 | OpenSpec 降级为可选伴侣 skill，核心契约一刀切通用规则 | accepted | CHANGELOG、`auto-coding-openspec/`、`verify-evidence/` |
| ADR-AC-008 | 仓库级配置写入 AGENTS.md 的 `## auto-coding` 小节，不发明新配置格式 | accepted | `setup-auto-coding/`、CHANGELOG 2.0.0 |

## ADR-AC-001：单一风险感知 skill + 按需 references

- **背景**：旧结构包含多个流程目录和大量过程文件；需要保留机制但降低入口复杂度。
- **候选方案**：继续维护多个子 skill；把全部内容塞进一个超长主文件；主文件保留契约、细节拆到按需读取的 references。
- **选择**：一个约 180 行的 `SKILL.md` 负责契约、路由、工作流和资源地图，细节进入 12 个 references。
- **放弃**：默认生成 TASK_PLAN、RUN_LOG 等大量过程文件；继续保留重复流程入口。
- **验证**：CHANGELOG 记录目录重构和 OpenSpec 归档；README 记录当前目录结构与按需读取方式。
- **改判条件**：references 之间出现无法定位的强耦合，或使用者需要跨多个文件才能完成基本路由判断。

## ADR-AC-002：Fast/Standard/High-risk 三档路由

- **背景**：改动规模不能单独代表风险；鉴权、迁移、状态机和外部 API 即使只改一行也需要更深验证。
- **候选方案**：所有任务走同一重流程；按文件数量路由；按不确定性、影响范围和风险标志路由。
- **选择**：Fast、Standard、High-risk 三档；FINANCE/AUTH/MIGRATION/STATE_MACHINE/EXTERNAL_API/ENV_OPS 直接提升到 High-risk。
- **放弃**：C0/C1a/C1b/C2 旧分级和只按文件数量决定深度。
- **验证**：README 与 CHANGELOG 记录当前路由与名称统一。
- **改判条件**：新增风险域无法映射现有六类，或真实任务统计显示某一档无法给出稳定验证边界。

## ADR-AC-003：验证证据使用四态，而不是把阻塞当通过

- **背景**：工具缺失、环境不可用和 prompt 级规则不能被写成“通过”。
- **候选方案**：仅 PASS/FAIL；缺环境时静默跳过；使用 PASS/FAIL/BLOCKED/NOT_APPLICABLE 并分开报告替代证据。
- **选择**：四态证据，并要求 `BLOCKED` 不得转写为 `PASS`。
- **放弃**：用 `[SKIP_*]` 或估计值填充未执行验证。
- **验证**：README 安全边界和验收报告“验证边界声明”均明确区分机器可验证层与依赖执行者自律层。
- **改判条件**：建立了可客观度量当前 prompt 级规则的自动评测后，再增加新的证据状态或收紧门槛。

## ADR-AC-004：根仓库为单一事实源，插件包由同步脚本生成

- **背景**：发布包必须和仓库根目录的 skill 内容一致，手工复制会产生漂移。
- **候选方案**：根目录与插件包分别维护；发布时人工复制；通过 `scripts/sync_plugin_skills.sh` 从根目录同步并在 CI 检查 diff。
- **选择**：根目录为事实源，插件目录是生成/同步产物；CI 重新同步并阻断漂移。
- **放弃**：双份手工编辑和默认自动提交。
- **验证**：CHANGELOG 记录同步脚本与 CI drift check；验收报告记录插件官方校验通过。
- **改判条件**：插件发布格式需要与根目录完全不同，且能建立有版本锁定的生成过程。

## ADR-AC-005：pyproject 为唯一版本事实源，CI 机械校验插件清单一致

- **背景**：pyproject.toml（0.2.1）与插件清单 plugin.json（0.2.0）已经出现版本漂移；发布依赖 `v*` tag，两处版本不一致会污染发布。
- **候选方案**：两处手工同步；发布前人工核对；pyproject 作为唯一事实源并由 `check_repo.check_version_consistency` 机械校验清单一致。
- **选择**：pyproject 为唯一事实源；插件清单必须与其相等，漂移即 CI 失败。开发期版本号带 `-dev` 后缀，发布时去掉后缀打 `v*` tag。语义化版本对 skill 内容的含义：MAJOR = 契约或路由行为变化，MINOR = 新增 references/脚本/安装通道，PATCH = 文字与文档修正。
- **放弃**：双处手工维护版本号与人工核对。
- **验证**：`check_repo.py` 输出包含版本一致性检查；`tests/test_check_repo.py` 覆盖漂移、一致、缺失清单三个分支。
- **改判条件**：插件生态要求插件清单使用独立版本号或引入版本锁文件。

## ADR-AC-006：四层记忆模型 + 证据时效规则应对运行中遗忘

- **背景**：长任务与跨会话执行中，会话压缩或中断会让模型凭"印象"继续，把上一会话的推断当成已验证事实；跨会话接手时新实例读不到旧实例的计划与证据。OpenSpec 降级为可选外挂后（v2 方向），其 change 目录不再默认承担计划状态职责。
- **候选方案**：依赖聊天历史与模型记忆；全程强制生成过程文件；分层记忆——仓库本身为默认记忆（L0），ERROR_MEMORY 沉淀跨任务教训（L1），单一原子 state 文件承载长任务断点（L2），结构化交接报告面向人（L3），并配合反遗忘规则。
- **选择**：四层记忆模型 + 五条反遗忘规则。最核心的是证据时效：恢复会话后，上一会话的一切 PASS 视为未验证，必须按当前路由重跑关键闸门；其次是单一状态源、恢复协议（resume/restart 判据）与沉淀压缩上限。
- **放弃**：把聊天记录当作权威记忆；用更多过程文件替代分层判断。
- **验证**：`docs/MEMORY_STRATEGY.md` 为设计文档；`references/recovery.md`（证据时效、resume/restart 判据）与 `references/sedimentation.md`（压缩上限）承载操作细则；SKILL.md 常驻状态契约包含证据重验要求。
- **改判条件**：出现可客观度量的跨会话记忆评测后，可收紧或调整四层模型的触发条件。

## ADR-AC-007：OpenSpec 降级为可选伴侣 skill，核心契约一刀切通用规则

- **背景**：v1 将 OpenSpec 当作内核依赖——SKILL.md 与 references 中出现 38 次，工作流第一步要求三选一执行边界，而 95% 的目标用户不使用 OpenSpec，为其付出纯上下文成本；本仓库自身也因 dogfooding 承担 23 个规格文件的维护税。竞品调研（mattpocock/skills 等）表明"小而组合、不接管流程"是更受欢迎的形态。
- **候选方案**：保持内核耦合；换用另一套规格系统；降级为可选伴侣 skill，核心契约改为一条通用规则（仓库已有规划工作流则以之为规划权威，否则内联规划）。
- **选择**：降级方案。`references/openspec.md` 升格为根目录伴侣 skill `auto-coding-openspec/`（单独安装，不进默认插件包）；三选一执行边界、`[NO_OPENSPEC]` 标记、任务勾选与 sync/archive 协议从核心契约移除；本仓库 `openspec/` 目录与 `.codex/skills/openspec-*` 删除（git 历史可溯），决策记录以 DECISIONS.md 为准。同时进行词汇瘦身：L0/L1/L2 → 三遍自检（导入/行为/契约），R1/R2/R6/R8 裁决并入正文，`conflict-rulings.md` 删除；四态证据纪律独立为 `verify-evidence/` skill 随插件分发。
- **放弃**：内核级 OpenSpec 协议与自造编号术语体系；引入新规格系统替代 OpenSpec 的方案（只是把重量换名字）。
- **验证**：SKILL.md 无 OpenSpec 专属协议；`check_repo.py` 全绿（链接/许可/README 结构/工具链路由）；pytest 套件通过；插件包同步后含 `auto-coding` 与 `verify-evidence` 两个 skill。
- **改判条件**：多数用户反馈需要内置规格系统，或出现被广泛采用的轻量规格标准可直接内联。

## ADR-AC-008：仓库级配置写入 AGENTS.md 的 `## auto-coding` 小节，不发明新配置格式

- **背景**：不同用户需要不同执行深度（严格度、主语言、证据阈值），v1 没有配置面；v2 的方向是"状态放在普通文件里"（对齐 mattpocock/skills 的 issue tracker / CONTEXT.md 哲学），因此不应引入 `.auto-coding.json` 之类的新配置系统。
- **候选方案**：新增 JSON/TOML 配置文件；环境变量；把配置写入仓库指令文件（AGENTS.md）的专用小节。
- **选择**：AGENTS.md 的 `## auto-coding` 小节。`/setup-auto-coding` 一次性引导生成（严格度 strict / default / light、主语言、证据阈值、授权备注），核心 skill 在工作流第 1 步读仓库指令时自然读到，零额外机制。风险标志在所有档位下均强制升级 High-risk——档位只调仪式感，不调安全性。
- **放弃**：新配置文件格式与机器校验（无对应消费方，纯增重）。
- **验证**：`setup-auto-coding/SKILL.md` 提供引导与模板；AGENTS.md 已是核心工作流第 1 步的必读项。
- **改判条件**：出现需要机器读取配置的场景（如 CI 强制档位），再评估独立配置文件。
