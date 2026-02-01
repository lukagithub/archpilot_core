# ArchPilot Core 脚本模板说明

本目录提供自动化脚本的模板，用于实现治理规则中定义的自动化检查功能。

---

## 脚本清单

| 脚本 | 用途 | 级别 |
|------|------|------|
| `check_naming.py` | 命名规范检查 | ⚠️ SHOULD |
| `validate_trace.py` | 追溯关系验证 | ⚠️ SHOULD |
| `calculate_score.py` | 质量评分计算 | ✅ MUST |

---

## 脚本规范

所有脚本必须遵循 `Governance/rules/rules_scripts.md` 定义的规范：

### 通用要求

1. 支持 `--help` 参数
2. 使用标准参数格式（`--version`, `--output`）
3. 输出 JSON 或 Markdown 格式
4. 使用标准退出码

### 输出格式

**JSON 输出必需字段**：
```json
{
  "script": "脚本名称",
  "timestamp": "ISO 8601 时间戳",
  "status": "success|failure|warning",
  "result": {}
}
```

### 退出码

| 退出码 | 含义 |
|--------|------|
| 0 | 成功 |
| 1 | 参数错误 |
| 2 | 依赖错误 |
| 3 | 业务校验失败 |
| 4 | 外部系统错误 |

---

## 使用示例

### 命名检查

```bash
python3 check_naming.py \
  --layer L1 \
  --strict \
  --output build/reports/naming_check.json
```

### 追溯验证

```bash
python3 validate_trace.py \
  --full-chain \
  --output build/reports/trace_validation.json
```

### 质量评分

```bash
python3 calculate_score.py \
  --version v1.0.0 \
  --output build/reports/quality_score.json
```

---

## 定制化

这些脚本为模板，需要根据具体项目进行定制：

1. 修改目录路径常量
2. 调整检查规则
3. 适配项目特定的命名规范
4. 配置评分权重

---

## 相关文档

- [脚本执行规范](../Governance/rules/rules_scripts.md)
- [命名规范](../Governance/rules/rules_naming.md)
- [发布规则](../Governance/rules/rules_release.md)

