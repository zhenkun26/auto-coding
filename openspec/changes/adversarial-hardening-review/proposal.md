## Why

仓库即将对外发布，需要对唯一实质代码（`pipeline/_contract_check.py`、`scripts/check_repo.py`）做一次对抗性生产级审查与加固，并补齐容器化与部署清单。审查以"金融级"标准进行，但诚实适配仓库实际形态：无服务、无网络依赖，重点放在异常处理、参数边界、编码健壮性与并发调用。

## What Changes

- 修复 `_contract_check.py`：消除 `except Exception` 裸吞与静默跳过；CLI 参数缺失/非法时快速失败；`--source` 不存在时不得静默通过；文件读取编码安全。
- 修复 `check_repo.py`：非 UTF-8 文件不崩溃。
- 新增测试：解析失败上报、CLI 边界、check_repo 功能、1000 次并发调用冒烟；覆盖率 ≥80%。
- 新增生产级 Dockerfile（多阶段、<100MB、非 root、HEALTHCHECK、构建缓存）与 `/deploy` K8s 清单（Deployment+PDB、Service、ConfigMap、Secret 占位、Ingress、HPA、HTTP 探针）。
- 交付综合验收报告 `docs/ACCEPTANCE_REPORT.md`。

## Capabilities

### New Capabilities
- `hardening`: 代码错误不静默、CLI 失败快速暴露、测试覆盖 ≥80%、1000 并发调用无错、容器与 K8s 清单可用。

### Modified Capabilities

（无现有 specs 需要修改）

## Impact

- `pipeline/_contract_check.py`、`scripts/check_repo.py`、`tests/`。
- 新增：`Dockerfile`、`.dockerignore`、`/deploy/*.yaml`、`docs/ACCEPTANCE_REPORT.md`。
- 插件包内 `_contract_check.py` 副本需同步（`scripts/sync_plugin_skills.sh`）。
