## 1. 对抗性审查证据

- [x] 1.1 输出代码文件清单与各维度扫描结果（异常、参数、编码、密钥、绝对路径）

## 2. 代码修复

- [x] 2.1 `_contract_check.py`：解析/IO 失败收集上报，消除裸 except
- [x] 2.2 `_contract_check.py`：CLI 参数校验（缺失/非法/--source 不存在 → 快速失败 + usage）
- [x] 2.3 `check_repo.py`：非 UTF-8 读取不崩溃、无 frontmatter 不崩溃

## 3. 测试与验收

- [x] 3.1 新增测试：解析失败上报、CLI 边界、check_repo 功能
- [x] 3.2 1000 并发 CLI 冒烟测试通过
- [x] 3.3 覆盖率 ≥80% 验证通过（实测 88%）

## 4. 容器与部署

- [x] 4.1 Dockerfile（多阶段、非 root、HEALTHCHECK、cache mount）+ .dockerignore
- [x] 4.2 /deploy K8s 清单（Deployment+PDB/Service/ConfigMap/Secret/Ingress/HPA/探针），YAML 静态校验

## 5. 报告与提交

- [x] 5.1 docs/ACCEPTANCE_REPORT.md 综合报告（六节齐全）
- [x] 5.2 同步插件包副本 + 全量验证 + git 提交
