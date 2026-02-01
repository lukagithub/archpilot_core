# 开发检查清单

**文档版本**: v1.0.0  
**最后更新**: 2026-02-01  
**适用范围**: 采用五层文档驱动开发（L1-L5）的项目

> 本文档定义了 L1-L5 层级一致性检查的标准、方法和评估准则。

---

## 1. 概述

### 1.1 目的

- 建立统一的 L1-L5 层级一致性检查标准
- 确保需求、设计、实现、验证的完整追溯链
- 提供可量化的质量评估方法
- 规范检查流程和问题处理机制

### 1.2 权威来源

> **参考**: L1-L5 层级职责、目录与前缀请参考 `ARCHITECTURE_DEFINITION.md`；术语写法遵循 `GLOSSARY.md`。

---

## 2. 文档完整性检查

### 2.1 文档存在性规则

**规则编号**: R-DOC-001  
**规则等级**: ✅ MUST

**检查内容**:
- [ ] 每个 L1 需求有对应的文档文件
- [ ] 每个 L2 架构有对应的文档文件
- [ ] 每个 L3 设计有对应的文档文件
- [ ] 每个 L5 测试有对应的测试文件

**检查方法**:
```bash
# 统计各层级文档数量
find L1_Requirements/ -name "FR_*.md" | wc -l
find L2_Architecture/ -name "SA_*.md" | wc -l
find L3_DetailDesign/ -name "DD_*.md" | wc -l
find L5_Verification/ -name "TC-*" | wc -l
```

**通过标准**:
- 所有计划内文档 100% 存在
- 文档内容结构完整

---

### 2.2 命名规范检查

**规则编号**: R-NAME-001  
**规则等级**: ✅ MUST

**检查内容**:
- [ ] 100% 文件前缀符合 `rules_naming.md`
- [ ] 术语使用符合 `GLOSSARY.md`
- [ ] 无命名冲突

**检查方法**:
```bash
python3 scripts/check_naming.py --layer L1 --strict
python3 scripts/check_naming.py --layer L2 --strict
python3 scripts/check_naming.py --layer L3 --strict
python3 scripts/check_naming.py --layer L5 --strict
```

---

### 2.3 目录结构检查

**规则编号**: R-STRUCT-001  
**规则等级**: ✅ MUST

**标准目录结构**:
```
project_root/
├── Governance/              # 治理文档
├── L1_Requirements/         # L1 需求层
├── L2_Architecture/         # L2 架构层
├── L3_DetailDesign/         # L3 设计层
├── L4_Implementation/       # L4 实现层
└── L5_Verification/         # L5 验证层
```

**检查内容**:
- [ ] 目录结构符合标准
- [ ] 无文件放置在错误位置

---

## 3. 追溯性检查

### 3.1 垂直追溯性规则

**规则编号**: R-TRACE-001  
**规则等级**: ✅ MUST

**追溯链模型**:
```
L1 (需求) 
  ↓ traces_to
L2 (架构)
  ↓ traces_to  
L3 (设计)
  ↓ traces_to
L4 (代码)
  ↓ verified_by
L5 (测试)
```

**检查内容**:
- [ ] 每个 L2 文档追溯到至少一个 L1 文档
- [ ] 每个 L3 文档追溯到至少一个 L2 文档
- [ ] 每个 L4 实现追溯到至少一个 L3 文档
- [ ] 每个 L5 测试追溯到至少一个 L1 文档

**元数据格式**:
```yaml
---
id: FR_core_001
layer: L1
traces_from: []              # 上游来源
traces_to: [SA_core_001]     # 下游实现
---
```

**检查方法**:
```bash
python3 scripts/validate_trace.py --full-chain
python3 scripts/validate_trace.py --from L1 --to L5
```

---

### 3.2 水平关联性规则

**规则编号**: R-TRACE-002  
**规则等级**: ⚠️ SHOULD

**检查内容**:
- [ ] 相关需求之间有 `related` 关联
- [ ] 接口文档双向引用

---

### 3.3 追溯完整度评估

| 完整度 | 标准 | 评级 |
|--------|------|------|
| 100% | 所有层级追溯完整 | 优秀 |
| ≥90% | 核心追溯完整 | 良好 |
| ≥70% | 主要追溯存在 | 及格 |
| <70% | 追溯缺失严重 | 不及格 |

---

## 4. 元数据检查

### 4.1 必需字段检查

**规则编号**: R-META-001  
**规则等级**: ✅ MUST

**必需字段**:
| 字段 | L1 | L2 | L3 | L4 | L5 |
|------|----|----|----|----|-----|
| id | ✅ | ✅ | ✅ | ⭕ | ✅ |
| layer | ✅ | ✅ | ✅ | ⭕ | ✅ |
| status | ✅ | ✅ | ✅ | ⭕ | ✅ |
| version | ✅ | ✅ | ✅ | ⭕ | ✅ |
| traces_from | ✅ | ✅ | ✅ | ⭕ | ✅ |
| traces_to | ✅ | ✅ | ✅ | ⭕ | ⭕ |

**检查方法**:
```bash
python3 scripts/extract_metadata.py --validate
```

---

### 4.2 状态一致性检查

**规则编号**: R-META-002  
**规则等级**: ⚠️ SHOULD

**检查内容**:
- [ ] `status` 值为有效状态（draft/review/approved/deprecated）
- [ ] deprecated 文档的下游不应有 approved 文档
- [ ] approved 文档的上游应全部 approved

---

## 5. 代码追溯检查

### 5.1 代码注释追溯

**规则编号**: R-CODE-001  
**规则等级**: ⚠️ SHOULD

**检查内容**:
- [ ] 核心代码文件包含 `@requirement` 注释
- [ ] 核心代码文件包含 `@design` 注释
- [ ] 注释中的 ID 存在于对应层级

**检查方法**:
```bash
# 搜索追溯注释
grep -r "@requirement" L4_Implementation/
grep -r "@design" L4_Implementation/
```

---

### 5.2 代码覆盖度

**规则编号**: R-CODE-002  
**规则等级**: ⚠️ SHOULD

**检查内容**:
- [ ] 每个 L3 设计有对应的 L4 实现
- [ ] L4 实现覆盖 L3 设计的主要功能点

---

## 6. 测试验证检查

### 6.1 测试覆盖检查

**规则编号**: R-TEST-001  
**规则等级**: ✅ MUST

**检查内容**:
- [ ] 每个 L1 需求有对应的 L5 测试
- [ ] 测试用例 `traces_from` 正确引用 L1 文档
- [ ] 关键功能有集成测试覆盖

---

### 6.2 测试执行检查

**规则编号**: R-TEST-002  
**规则等级**: ✅ MUST

**检查内容**:
- [ ] 所有测试用例已执行
- [ ] 测试执行报告包含必需字段
- [ ] 失败的测试有分析和处理

---

## 7. 发布前检查清单

### 7.1 完整检查清单

#### 文档完整性
- [ ] L1 需求文档完整
- [ ] L2 架构文档完整
- [ ] L3 设计文档完整
- [ ] L5 测试文档完整

#### 命名规范
- [ ] 所有文件命名符合规范
- [ ] 无命名冲突

#### 追溯关系
- [ ] L1→L2 追溯完整
- [ ] L2→L3 追溯完整
- [ ] L3→L4 追溯完整
- [ ] L4→L5 追溯完整
- [ ] L5→L1 闭环完整

#### 元数据
- [ ] 所有文档包含必需字段
- [ ] 状态一致性正确

#### 代码质量
- [ ] 代码包含追溯注释
- [ ] 无严重静态分析问题

#### 测试验证
- [ ] 所有测试用例通过
- [ ] 测试覆盖率达标

---

## 8. 问题处理流程

### 8.1 问题分级

| 级别 | 描述 | 处理时限 | 是否阻断发布 |
|------|------|----------|--------------|
| 严重 | 追溯链断裂、核心文档缺失 | 立即 | ✅ 是 |
| 重要 | 元数据不完整、命名不规范 | 24小时 | ⚠️ 视情况 |
| 一般 | 格式问题、可选字段缺失 | 下个版本 | ❌ 否 |

### 8.2 问题处理流程

```
1. 发现问题
   ↓
2. 评估级别
   ↓
3. 分配责任人
   ↓
4. 修复问题
   ↓
5. 验证修复
   ↓
6. 关闭问题
```

---

## 9. 关联文档

- `ARCHITECTURE_DEFINITION.md` - 架构权威定义
- `GLOSSARY.md` - 术语标准表
- `rules/rules_naming.md` - 命名规范
- `rules/rules_coding.md` - 编码规范
- `rules/rules_testcases.md` - 测试用例规范
- `release_checklist.md` - 发布检查清单

