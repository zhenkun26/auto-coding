# auto-coding 技术决策记录

> 本文件只记录影响 skill 结构、验证边界和发布方式的取舍。依据 README、CHANGELOG、OpenSpec 和验收报告；历史验收报告中已经移除的 v0.1.0 容器路径不视为当前架构。

## 索引

| ID | 决策 | 状态 | 证据 |
|---|---|---|---|
| ADR-AC-001 | 单一风险感知 skill + 按需 references | accepted | CHANGELOG 0.2.0、README |
| ADR-AC-002 | Fast/Standard/High-risk 三档路由 | accepted | CHANGELOG 0.2.0、README |
| ADR-AC-003 | 证据状态使用 PASS/FAIL/BLOCKED/NOT_APPLICABLE | accepted | README、验收报告 |
| ADR-AC-004 | 根仓库为 skill 单一事实源，插件包由同步脚本生成 | accepted | CHANGELOG、`sync_plugin_skills.sh` |

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
- **验证**：README、CHANGELOG 和 OpenSpec content-consistency/release-readiness 记录当前路由与名称统一。
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
