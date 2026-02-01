#!/usr/bin/env python3
"""
质量评分计算脚本模板

功能：计算五维度质量评分

Usage:
    python3 calculate_score.py --version v1.0.0 --output result.json

Arguments:
    --version VERSION   版本号（必需）
    --output PATH       输出路径（默认 ./out/quality_score.json）
    --detailed          输出详细分析
    --help              显示帮助

Exit Codes:
    0 - 成功
    1 - 参数错误
    2 - 依赖错误
    3 - 评分未达标（总分 < 3.0）

Author: ArchPilot Core Framework
Date: 2026-02-01
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


# ============ 配置常量 ============

# 评分权重
SCORE_WEIGHTS = {
    "D1": 0.20,  # 文档完整性
    "D2": 0.15,  # 追溯关系
    "D3": 0.30,  # 功能实现
    "D4": 0.25,  # 测试验证
    "D5": 0.10   # 代码质量
}

# 评分阈值
GRADE_THRESHOLDS = {
    "excellent": 4.5,
    "good": 4.0,
    "pass": 3.0,
    "fail": 0
}

# 层级目录
LAYER_DIRECTORIES = {
    "L1": "L1_Requirements",
    "L2": "L2_Architecture",
    "L3": "L3_DetailDesign",
    "L4": "L4_Implementation",
    "L5": "L5_Verification"
}


# ============ 评分计算函数 ============

def calculate_d1_score(project_root: str) -> dict:
    """计算 D1: 文档完整性评分"""
    score = 5.0
    deductions = []
    details = []

    # 检查各层级文档
    for layer, directory in LAYER_DIRECTORIES.items():
        if layer in ["L1", "L2", "L3"]:  # D1 只检查设计文档
            dir_path = Path(project_root) / directory
            if not dir_path.exists():
                score -= 1.0
                deductions.append(f"{layer} directory not found")
            else:
                doc_count = len(list(dir_path.glob("*.md")))
                details.append(f"{layer}: {doc_count} documents")
                if doc_count == 0:
                    score -= 0.5
                    deductions.append(f"{layer} has no documents")

    # 检查治理文档
    governance_dir = Path(project_root) / "Governance"
    if not governance_dir.exists():
        score -= 0.5
        deductions.append("Governance directory not found")

    score = max(1.0, min(5.0, score))

    return {
        "dimension": "D1",
        "name": "文档完整性",
        "score": round(score, 2),
        "weight": SCORE_WEIGHTS["D1"],
        "weighted_score": round(score * SCORE_WEIGHTS["D1"], 3),
        "details": details,
        "deductions": deductions
    }


def calculate_d2_score(project_root: str) -> dict:
    """计算 D2: 追溯关系评分"""
    # 简化实现：检查文档是否包含追溯字段
    score = 5.0
    deductions = []
    details = []

    total_docs = 0
    docs_with_trace = 0

    for layer, directory in LAYER_DIRECTORIES.items():
        dir_path = Path(project_root) / directory
        if dir_path.exists():
            for md_file in dir_path.glob("*.md"):
                if md_file.name not in ["README.md", "INDEX.md"]:
                    total_docs += 1
                    content = md_file.read_text(encoding='utf-8')
                    if "traces_from:" in content or "traces_to:" in content:
                        docs_with_trace += 1

    if total_docs > 0:
        trace_ratio = docs_with_trace / total_docs
        details.append(f"Documents with trace: {docs_with_trace}/{total_docs}")

        if trace_ratio < 0.5:
            score = 2.0
            deductions.append(f"Less than 50% documents have trace info")
        elif trace_ratio < 0.7:
            score = 3.0
            deductions.append(f"Less than 70% documents have trace info")
        elif trace_ratio < 0.9:
            score = 4.0
            deductions.append(f"Less than 90% documents have trace info")
    else:
        score = 1.0
        deductions.append("No documents found")

    return {
        "dimension": "D2",
        "name": "追溯关系",
        "score": round(score, 2),
        "weight": SCORE_WEIGHTS["D2"],
        "weighted_score": round(score * SCORE_WEIGHTS["D2"], 3),
        "details": details,
        "deductions": deductions
    }


def calculate_d3_score(project_root: str) -> dict:
    """计算 D3: 功能实现评分"""
    score = 5.0
    deductions = []
    details = []

    l4_dir = Path(project_root) / LAYER_DIRECTORIES["L4"]
    if not l4_dir.exists():
        score = 1.0
        deductions.append("L4 Implementation directory not found")
    else:
        # 统计实现文件
        code_files = list(l4_dir.rglob("*.cpp")) + \
                     list(l4_dir.rglob("*.py")) + \
                     list(l4_dir.rglob("*.js")) + \
                     list(l4_dir.rglob("*.ts"))

        details.append(f"Code files found: {len(code_files)}")

        if len(code_files) == 0:
            score = 2.0
            deductions.append("No code files found")
        elif len(code_files) < 5:
            score = 3.5
            deductions.append("Limited code files")

    return {
        "dimension": "D3",
        "name": "功能实现",
        "score": round(score, 2),
        "weight": SCORE_WEIGHTS["D3"],
        "weighted_score": round(score * SCORE_WEIGHTS["D3"], 3),
        "details": details,
        "deductions": deductions
    }


def calculate_d4_score(project_root: str) -> dict:
    """计算 D4: 测试验证评分"""
    score = 5.0
    deductions = []
    details = []

    l5_dir = Path(project_root) / LAYER_DIRECTORIES["L5"]
    if not l5_dir.exists():
        score = 1.0
        deductions.append("L5 Verification directory not found")
    else:
        test_files = list(l5_dir.rglob("TC_*.md")) + \
                     list(l5_dir.rglob("test_*.py")) + \
                     list(l5_dir.rglob("*_test.cpp"))

        details.append(f"Test files found: {len(test_files)}")

        if len(test_files) == 0:
            score = 2.0
            deductions.append("No test files found")
        elif len(test_files) < 3:
            score = 3.0
            deductions.append("Limited test coverage")

    return {
        "dimension": "D4",
        "name": "测试验证",
        "score": round(score, 2),
        "weight": SCORE_WEIGHTS["D4"],
        "weighted_score": round(score * SCORE_WEIGHTS["D4"], 3),
        "details": details,
        "deductions": deductions
    }


def calculate_d5_score(project_root: str) -> dict:
    """计算 D5: 代码质量评分"""
    # 简化实现：基于基本检查
    score = 4.0  # 默认良好
    deductions = []
    details = []

    details.append("Basic code quality check (simplified)")
    details.append("Full static analysis requires external tools")

    return {
        "dimension": "D5",
        "name": "代码质量",
        "score": round(score, 2),
        "weight": SCORE_WEIGHTS["D5"],
        "weighted_score": round(score * SCORE_WEIGHTS["D5"], 3),
        "details": details,
        "deductions": deductions
    }


def determine_grade(total_score: float) -> tuple:
    """确定质量评级"""
    if total_score >= GRADE_THRESHOLDS["excellent"]:
        return "优秀", "Excellent", "≥4.5"
    elif total_score >= GRADE_THRESHOLDS["good"]:
        return "良好", "Good", "≥4.0 且 <4.5"
    elif total_score >= GRADE_THRESHOLDS["pass"]:
        return "及格", "Pass", "≥3.0 且 <4.0"
    else:
        return "不及格", "Fail", "<3.0"


def determine_recommendation(total_score: float, grade: str) -> str:
    """确定发布建议"""
    if grade == "优秀":
        return "✅ 推荐正式发布"
    elif grade == "良好":
        return "✅ 可以正式发布"
    elif grade == "及格":
        return "⚠️ 有条件发布（仅限 Beta/RC）"
    else:
        return "❌ 禁止发布"


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='计算五维度质量评分',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--version', required=True,
                        help='版本号')
    parser.add_argument('--output', default='./out/quality_score.json',
                        help='输出路径')
    parser.add_argument('--detailed', action='store_true',
                        help='输出详细分析')
    parser.add_argument('--project-root', default='.',
                        help='项目根目录')
    return parser.parse_args()


def main():
    """主函数"""
    args = parse_args()

    # 计算各维度评分
    d1 = calculate_d1_score(args.project_root)
    d2 = calculate_d2_score(args.project_root)
    d3 = calculate_d3_score(args.project_root)
    d4 = calculate_d4_score(args.project_root)
    d5 = calculate_d5_score(args.project_root)

    dimensions = [d1, d2, d3, d4, d5]

    # 计算加权总分
    total_score = sum(d["weighted_score"] for d in dimensions)
    total_score = round(total_score, 2)

    # 确定评级和建议
    grade_cn, grade_en, grade_range = determine_grade(total_score)
    recommendation = determine_recommendation(total_score, grade_cn)

    # 确定状态
    status = "success" if total_score >= 3.0 else "failure"

    # 构建输出
    output = {
        "script": "calculate_score",
        "version": args.version,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": status,
        "project_root": os.path.abspath(args.project_root),
        "total_score": total_score,
        "max_score": 5.0,
        "grade": {
            "chinese": grade_cn,
            "english": grade_en,
            "range": grade_range
        },
        "recommendation": recommendation,
        "dimensions": {
            "D1": d1,
            "D2": d2,
            "D3": d3,
            "D4": d4,
            "D5": d5
        },
        "weights": SCORE_WEIGHTS,
        "thresholds": GRADE_THRESHOLDS
    }

    # 输出结果
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    # 打印摘要
    print(f"Quality Score Calculation - {args.version}")
    print("=" * 50)
    for d in dimensions:
        print(f"  {d['dimension']}: {d['score']}/5.0 (weighted: {d['weighted_score']})")
    print("-" * 50)
    print(f"  Total Score: {total_score}/5.0")
    print(f"  Grade: {grade_cn} ({grade_en})")
    print(f"  Recommendation: {recommendation}")
    print("=" * 50)
    print(f"Results written to: {output_path}")

    # 返回退出码
    if status == "failure":
        return 3
    return 0


if __name__ == '__main__':
    sys.exit(main())

