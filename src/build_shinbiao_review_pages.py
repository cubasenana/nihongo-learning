from __future__ import annotations

import argparse
import re
from pathlib import Path


PAGE_RE = re.compile(r"^> Page (\d+)$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a review-pages markdown for noisy Shin Nihongo pages."
    )
    parser.add_argument("structured_dir", type=Path, help="Structured markdown directory")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        required=True,
        help="Output markdown path",
    )
    return parser.parse_args()


def find_vocab_page(path: Path) -> int | None:
    current_page: int | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        page_match = PAGE_RE.match(line.strip())
        if page_match:
            current_page = int(page_match.group(1))
            continue
        if line.strip() == "## 生词表":
            return current_page
    return None


def lesson_paths(structured_dir: Path) -> list[Path]:
    return sorted(structured_dir.glob("lesson-*.md"))


def lesson_title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def build_report(structured_dir: Path) -> str:
    lines = [
        "# Review Pages",
        "",
        "## 优先处理",
        "",
        f"- [入门单元](./01-intro-unit.md)：`Page 25-28` 为假名笔顺/书写表，图表密集，OCR 噪声高。",
        f"- [入门单元](./01-intro-unit.md)：`Page 30-31` 为声调类型与符号图示页，字符和标记失真明显。",
        f"- [入门单元](./01-intro-unit.md)：`Page 34-37` 为发音对比和口型/舌位说明，建议结合原 PDF 复核。",
        "",
        "## 生词表页",
        "",
        "以下页面都是双栏词表、注音和词类标记混排，最适合后续做逐课精修。",
        "",
    ]

    for path in lesson_paths(structured_dir):
        vocab_page = find_vocab_page(path)
        if vocab_page is None:
            continue
        title = lesson_title(path)
        lines.append(
            f"- [{title}](./{path.name})：`Page {vocab_page}`，生词表双栏混排，建议人工校对词头、词类与中文释义。"
        )

    lines.extend(
        [
            "",
            "## 说明",
            "",
            "- 这份清单只标记高价值回修页，不代表其他页面已经完全无噪声。",
            "- 如果后续继续清理，建议顺序是：`入门单元` -> `第1-4课生词表` -> 其余各课生词表。",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    structured_dir = args.structured_dir.expanduser().resolve()
    output_path = args.output.expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_report(structured_dir), encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
