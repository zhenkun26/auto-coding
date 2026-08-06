## Context

仓库无服务进程，唯一实质代码为 Python CLI 与检查脚本（见 proposal.md - Why）。Docker/K8s 面向两个诚实用途：CI 验证镜像与只读文档镜像；不虚构业务服务。

## Goals / Non-Goals

**Goals:**
- 消除代码中的静默错误与崩溃路径，向下兼容全部现有调用。
- 交付可构建的容器与可 apply 的 K8s 清单，验收报告可复现。

**Non-Goals:**
- 不编造 HTTP 业务接口或数据库。
- 不把技能包伪装成"交易系统"部署。

## Decisions

**D1: 修复以"收集并上报"替代静默跳过。**
解析失败、IO 失败统一收集为 warnings，不中断主流程（保持 CLI 兼容），但不再无声。裸 `except Exception` 改为精确捕获并上报。

**D2: CLI 参数用显式校验替代裸索引。**
`sys.argv.index(...)+1` 会越界崩溃；改为解析函数：缺失/非法参数输出 usage 并 exit 2；`--source` 目录不存在 exit 2（修复"0 契约=成功"的假通过）。

**D3: 容器默认"验证模式"，可选"文档镜像模式"。**
默认 ENTRYPOINT 跑 pytest + check_repo（CI 用）；`serve` 模式用 `python -m http.server` 只读托管仓库文档（K8s 部署对象）。HEALTHCHECK 面向 serve 模式。

**D4: K8s 清单面向只读文档镜像，占位符明确。**
镜像地址、Secret 值全部使用 `<PLACEHOLDER>` 并在报告中高亮；探针用 HTTP GET `/`。

**D5: 覆盖与并发验证本地可跑。**
coverage.py 测两个模块；并发冒烟用 ThreadPoolExecutor 发起 1000 次 CLI 子进程调用。

## Risks / Trade-offs

- **本环境可能无 Docker daemon** → 构建命令写入报告，本地只做静态校验（YAML 解析）。
- **文档镜像规模膨胀** → `.dockerignore` 排除 .git/ai_pipeline 等，保持 <100MB。
- **并发测试耗时** → 1000 次轻量调用并行，限制在 60s 内。

## Migration Plan

1. 审查证据 → 修复代码 → 补测试 → 覆盖率/并发验证。
2. Dockerfile + /deploy 清单 → 静态校验 YAML。
3. 生成 ACCEPTANCE_REPORT.md → 同步插件副本 → 提交。

## Open Questions

- Docker daemon 与 registry 凭据（报告给出命令，实际构建/推送由用户执行）。
- K8s 集群环境（清单为标准模板，按环境改 Secret）。
