# auto-coding — 对抗性生产级审查与部署验收报告

> **历史文档**：本报告记录的是 v0.1.0 的验收结果。v0.2.0 已移除 Docker/K8s 容器化与 pipeline 目录结构，文中提及的 `deploy/`、`Dockerfile`、`pipeline/` 等路径均已不存在，仅作历史存档。

> 报告日期：2026-08-06 · 版本：v0.1.0
>
> **诚实声明**：本仓库是 AI 编码技能包（文档 + 轻量 CLI 工具），**不是业务服务**，没有 HTTP 业务接口、数据库或网络依赖。因此本报告的"金融级"审查聚焦于代码真实存在的风险面（异常处理、参数边界、编码、并发调用），Docker/K8s 面向两个诚实用途：**CI 验证镜像**（默认）与**只读文档镜像**（serve 模式）。任何未来的业务服务需另行设计与审查。

---

## 1. 项目概述

### 技术栈

| 组件 | 技术 |
|:---|:---|
| 核心工具 | Python 3.12（`pipeline/_contract_check.py`，312→340 行） |
| 仓库检查 | Python（`scripts/check_repo.py`） |
| 同步脚本 | POSIX sh（`scripts/sync_plugin_skills.sh`） |
| 测试 | pytest 36 用例 + coverage 88% |
| 容器 | Docker 多阶段（python:3.12-alpine，目标 <100MB） |
| 部署 | Kubernetes manifests（/deploy，8 个资源） |

### 架构

```text
仓库（单一事实源）
  ├── pipeline/_contract_check.py   ── L2 契约结构校验（AST + Gherkin 回退）
  ├── scripts/check_repo.py         ── 链接完整性 / license / README 结构
  ├── scripts/sync_plugin_skills.sh ── 插件包同步
  └── tests/                        ── 36 用例（含 1000 并发冒烟）
        │
        ▼
  Docker 镜像（两种模式）
  ├── MODE=validate  → pytest + check_repo（CI 用，一次性退出）
  └── MODE=serve     → python -m http.server :8000（只读文档镜像，K8s 用）
        │
        ▼
  Kubernetes（/deploy）：Deployment 3 副本 + PDB + Service + Ingress + HPA
```

---

## 2. 对抗性审查报告

### 审查范围与方法

逐文件扫描：所有 `.py` / `.sh` / `.json` / `.yaml`；维度：逻辑黑洞与竞态、性能、OWASP、配置与环境幻觉、日志可观测性。以下为**全部真实发现**，无虚构项。

### 发现清单（按严重度）

| # | 级别 | 位置 | 问题 | 攻击/影响案例 | 状态 |
|:--|:---|:---|:---|:---|:---|
| 1 | [P1] | `_contract_check.py:207`（旧 204） | 裸 `except Exception: continue` | 读取权限/编码错误被静默吞掉，契约检查假性通过 | ✅ 已修复 |
| 2 | [P1] | `_contract_check.py:121`（旧 118） | `except SyntaxError: continue` 静默跳过解析失败 | 含语法错误的文件不报错，MISSING 契约不可见 | ✅ 已修复 |
| 3 | [P1] | `_contract_check.py` `__main__` | `sys.argv.index("--spec")+1` 越界；`--source` 不存在时"0 契约=成功"假通过 | 参数缺失直接 traceback；错误目录静默返回成功 | ✅ 已修复 |
| 4 | [P1] | `_contract_check.py` 全部文件读取 | `open(..., encoding="utf-8")` 严格解码 | 非 UTF-8 spec/源码触发 UnicodeDecodeError 崩溃 | ✅ 已修复 |
| 5 | [P2] | `scripts/check_repo.py` | `split("---", 2)[1]` 对无 frontmatter 的 SKILL.md 抛 IndexError；`read_text` 严格解码 | 一个坏文件让整个 CI 检查崩溃 | ✅ 已修复 |
| 6 | [P2] | `_contract_check.py` 正则解析 | 签名正则可能误匹配正文 | 假阳性契约失败（文档化限制，不改语义） | ⏸ 已知限制 |
| 7 | [P2] | `_contract_check.py` 文件读取 | 无大小上限 | 超大文件内存放大（CLI 场景低危） | ⏸ 已知限制 |
| 8 | [P3] | `sync_plugin_skills.sh` | 依赖 `rsync`/`rm` | 缺 rsync 时脚本失败（`set -euo pipefail` 已快速失败） | ⏸ 环境约束已文档化 |

### 不适用项（明确标注，未虚构）

- **竞态/Check-Then-Act**：无共享状态、无服务进程——CLI 单进程幂等。
- **分布式事务/Saga**：无事务与补偿需求。
- **N+1 / HTTP 超时雪崩**：无数据库、无出站 HTTP 客户端。
- **SQL/NoSQL/命令注入**：无 SQL；无 `shell=True`/`os.system`。
- **越权**：无用户体系与数据访问。
- **密钥硬编码**：全仓库扫描为零（仅文档示例 `{"token": "..."}`）。
- **绝对路径依赖**：代码中为零（脚本均以 `BASH_SOURCE`/`__file__` 定位）。
- **敏感日志/TraceId**：无日志输出敏感数据；无分布式链路，TraceId 不适用。

### 修复前后对比（关键 diff）

`except Exception: continue` → 精确捕获并上报：

```diff
-            except Exception:
-                continue
+            except (OSError, UnicodeDecodeError) as exc:
+                record_diagnostic(f"read error ({fpath}): {exc}")
+                continue
```

CLI 参数越界崩溃 → 显式解析 + 快速失败：

```diff
-    spec_path = sys.argv[sys.argv.index("--spec") + 1] if "--spec" in sys.argv else ""
-    src_dir = sys.argv[sys.argv.index("--source") + 1] if "--source" in sys.argv else "src/"
+    spec_path, src_dir = parse_cli_args(sys.argv[1:])
+    if not spec_path:
+        print("Usage: ...")
+        return 1
+    return run_cli(spec_path, src_dir)
```

`__main__` 内联逻辑 → 可测的 `main()/run_cli()` 入口（CLI 行为不变），使 CLI 路径进入覆盖率。

---

## 3. 本地构建与镜像发布指南

```bash
# 构建（多阶段，runner 目标 <100MB）
docker build --target runner -t <YOUR_REGISTRY>/auto-coding:v0.1.0 .

# 本地验证模式（CI 用，跑完退出）
docker run --rm <YOUR_REGISTRY>/auto-coding:v0.1.0

# 本地文档镜像模式（K8s 同款）
docker run --rm -p 8000:8000 -e MODE=serve <YOUR_REGISTRY>/auto-coding:v0.1.0
curl -s http://127.0.0.1:8000/ | head

# 推送（需先 docker login <YOUR_REGISTRY>）
docker push <YOUR_REGISTRY>/auto-coding:v0.1.0
```

镜像大小验收：`docker images <YOUR_REGISTRY>/auto-coding` 应 < 100MB（alpine 基底 + pytest 依赖）。

---

## 4. K8s 一键部署指南

### 应用顺序

```bash
kubectl apply -f deploy/00-namespace.yaml
kubectl apply -f deploy/01-configmap.yaml
kubectl apply -f deploy/02-secret.yaml
kubectl apply -f deploy/03-deployment.yaml
kubectl apply -f deploy/04-pdb.yaml
kubectl apply -f deploy/05-service.yaml
kubectl apply -f deploy/06-ingress.yaml
kubectl apply -f deploy/07-hpa.yaml
```

### 修改 Secrets 与占位符（高亮）

`deploy/03-deployment.yaml` 中 **`image: <YOUR_REGISTRY>/auto-coding:v0.1.0`** 必须替换为你的镜像地址；`deploy/06-ingress.yaml` 中 **`auto-coding.example.com`** 必须替换为你的域名。

Secret 当前为占位符（`deploy/02-secret.yaml`）：

```bash
# 用你的真实值重新生成 base64 后替换
printf '<YOUR_DB_PASSWORD>' | base64   # → 替换 DB_PASSWORD 的值
printf '<YOUR_API_KEY>' | base64       # → 替换 API_KEY 的值
kubectl apply -f deploy/02-secret.yaml
kubectl rollout restart deployment/auto-coding -n auto-coding
```

### 部署后检查

```bash
kubectl get pods,svc,hpa,pdb -n auto-coding
kubectl rollout status deployment/auto-coding -n auto-coding
```

---

## 5. 验收测试结果

### 本地全量验收（已实测）

```text
pytest:                     36 passed（4.65s）
覆盖率（工具模块）:          88%  （_contract_check.py 89% / check_repo.py 86%）
1000 并发 CLI 冒烟:          1000/1000 退出码 0
openspec validate:          adversarial-hardening-review valid
check_repo.py:              links / licenses / README structure OK
插件官方校验:                plugins/auto-coding valid
deploy/*.yaml 静态校验:      8/8 资源解析通过
```

### 关键命令（可复现）

```bash
# 单元测试 + 覆盖率
python -m pytest tests/ -q
coverage run -m pytest tests/ -q && coverage report --include='pipeline/_contract_check.py,scripts/check_repo.py'

# 1000 并发冒烟（测试套件内置）
python -m pytest tests/test_contract_check.py::test_should_pass_1000_concurrent_invocations -q

# 契约检查 CLI 边界（缺失参数应快速失败）
python pipeline/_contract_check.py --spec            # exit 1 + usage
python pipeline/_contract_check.py --spec nope.md --source ./ --source 不存在目录

# 文档镜像压测示例（serve 模式 + 并发请求）
hey -n 10000 -c 100 http://127.0.0.1:8000/   # 或 ab -n 10000 -c 100 ...
```

> 说明："1000 并发请求"在无服务形态下以 **1000 次并发 CLI 调用** 等价验收；文档镜像的 HTTP 压测命令如上，实测数据以你的运行环境为准。

---

## 6. 回滚预案

### 镜像/应用回滚（K8s）

```bash
# 回滚到上一个 Deployment revision
kubectl rollout undo deployment/auto-coding -n auto-coding

# 回滚到指定 revision（先查历史）
kubectl rollout history deployment/auto-coding -n auto-coding
kubectl rollout undo deployment/auto-coding -n auto-coding --to-revision=<N>
```

### 代码回滚（Git）

```bash
# 撤销最后一次提交（保留工作区改动）或硬回退到稳定提交
git revert HEAD
# 或
git reset --hard <STABLE_COMMIT>
```

### 配置回滚

```bash
# 回滚 Secret/ConfigMap 后重启工作负载
kubectl apply -f deploy/02-secret.yaml
kubectl rollout restart deployment/auto-coding -n auto-coding
```

### 应急开关

- 文档镜像仅只读，无写入面，数据丢失风险为零；异常时直接缩容：`kubectl scale deployment auto-coding -n auto-coding --replicas=0`。
- PDB 保证滚动更新/节点维护期间至少 2 副本可用。

---

## 验证边界声明（2026-08-07 补充）

本项目的机制分两层，可验证性不同，如实声明如下：

- **有机器验证的一层**：工具脚本（探测、契约检查、状态管理）的确定性行为由 `tests/fixtures/adversarial/` 陷阱场景 + `tests/test_adversarial_fixtures.py` 断言覆盖——契约不匹配必须 FAIL、缺返回注解不得假性 PASS、散文中的伪签名必须被忽略、空 `tests/` 目录不得当作 pytest 已配置、损坏状态文件必须大声报错。这些断言在 CI 中每次运行。
- **仍依赖执行者自律的一层**：风险路由分级、逃逸门如实上报、`BLOCKED` 不报 `PASS` 等 prompt 级规则，作用于 agent 行为，目前没有客观度量手段能证明 agent 始终遵守。这是 prompt 工程类项目的固有边界，本项目不声称已解决。
