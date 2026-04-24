from __future__ import annotations

import argparse
from collections import OrderedDict
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


TASKS = OrderedDict(
    [
        ("extract", ("pdf_to_markdown.py", "从 PDF 提取整本原始 Markdown")),
        ("pipeline", ("shinbiao_markdown.py", "运行初级上册的主转换流程")),
        ("split", ("split_shinbiao_markdown.py", "按目录拆分 Markdown 章节")),
        ("normalize", ("normalize_shinbiao_markdown.py", "做首轮规则化清洗")),
        ("review", ("build_shinbiao_review_pages.py", "生成或更新回修清单")),
        ("reader-pdf-9-24", ("build_shinbiao_reader_from_pdf.py", "按原 PDF 重建第 9-24 课 reader 草稿")),
        ("reader-repair-spec", ("repair_reader_spec_issues.py", "修复 reader 课稿中的页码锚点和完成度规范问题")),
        ("reader-s3-9-24", ("promote_reader_s3.py", "把第 9-24 课 reader 稿统一提升到 S3 学习版")),
        ("reader-quality-all", ("quality_refine_reader_all.py", "按 READER_SPEC 对第 1-24 课做整册质量修订")),
        ("vitepress-export", ("export_shinbiao_to_vitepress.py", "同步初级上册到 docs/ 目录供 VitePress/GitHub Pages 发布")),
        ("p0-1", ("refine_shinbiao_p0_1.py", "精修第 9-12 课生词表")),
        ("p0-2", ("refine_shinbiao_p0_2.py", "精修第 13-16 课生词表")),
        ("p0-3", ("refine_shinbiao_p0_3.py", "精修第 17-20 课生词表")),
        ("p0-4", ("refine_shinbiao_p0_4.py", "精修第 21-24 课生词表")),
        ("p1-1", ("refine_shinbiao_p1_1.py", "重建入门单元高噪声页")),
        ("p1-2", ("refine_shinbiao_p1_2.py", "清洗 lesson 正文结构")),
        ("p2-1", ("refine_shinbiao_p2_1.py", "整理 N5 模拟题与附录结构")),
        ("vocab-batch", ("refine_shinbiao_vocab_batch.py", "按页图批量精修生词表的辅助脚本")),
    ]
)


def list_tasks() -> None:
    print("Shinbiao Pipeline\n")
    print("用法:")
    print("  python src/main.py list")
    print("  python src/main.py run <task>\n")
    print("可用任务:")
    for name, (script, description) in TASKS.items():
        print(f"  {name:<10} {script:<32} {description}")


def run_task(name: str) -> int:
    script_name, _ = TASKS[name]
    script_path = SRC / script_name
    if not script_path.exists():
        print(f"[missing] {script_path}", file=sys.stderr)
        return 1
    completed = subprocess.run([sys.executable, str(script_path)], cwd=ROOT)
    return completed.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="新标日结构化稿与 VitePress 站点脚本入口")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help="列出可用脚本任务")
    run_parser = subparsers.add_parser("run", help="运行指定任务")
    run_parser.add_argument("task", choices=list(TASKS.keys()), help="任务名")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command in (None, "list"):
        list_tasks()
        return 0

    if args.command == "run":
        return run_task(args.task)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
