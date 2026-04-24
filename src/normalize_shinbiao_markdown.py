from __future__ import annotations

import argparse
import re
from pathlib import Path


PAGE_RE = re.compile(r"^## Page (\d+)$")
LESSON_TITLE_RE = re.compile(r"^第\s*\d+\s*課")
UNIT_TITLE_RE = re.compile(r"^第\s*\d+\s*单元")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize split Shin Nihongo markdown files into a cleaner structure."
    )
    parser.add_argument("source_dir", type=Path, help="Directory with split markdown files")
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        required=True,
        help="Directory where normalized markdown files will be written",
    )
    parser.add_argument(
        "--book-title",
        help="Title used for the generated index.md. Defaults to the source directory name.",
    )
    return parser.parse_args()


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text).replace("：", "").replace(":", "")


def detect_heading(line: str) -> str | None:
    token = compact(line)
    if not token:
        return None

    if "表达及词语讲解" in token and len(token) <= 12:
        return "## 表达及词语讲解"
    if "语法解释" in token and len(token) <= 10:
        return "## 语法解释"
    if "应用课文" in token and len(token) <= 10:
        return "## 应用课文"
    if "生词表" in token and len(token) <= 12:
        return "## 生词表"
    if ("基本课文" in token or re.fullmatch(r"本.*文", token)) and len(token) <= 12:
        return "## 基本课文"
    if token == "练习":
        return "## 练习"
    if token.startswith("练习"):
        suffix = token[2:]
        if suffix in {"I", "Ⅰ", "1"}:
            return "### 练习 I"
        if suffix in {"II", "Ⅱ", "H", "U", "N", "n", "口"}:
            return "### 练习 II"
    if token in {"A", "B", "C", "D"}:
        return f"### 对话 {token}"

    return None


def push_line(lines: list[str], value: str) -> None:
    if value == "":
        if lines and lines[-1] == "":
            return
    lines.append(value)


def normalize_document(text: str) -> str:
    raw_lines = text.splitlines()
    first_page_index = next(
        (index for index, line in enumerate(raw_lines) if PAGE_RE.match(line.strip())),
        len(raw_lines),
    )

    preamble = [line.rstrip() for line in raw_lines[:first_page_index]]
    content = raw_lines[first_page_index:]
    title_line = next((line for line in preamble if line.startswith("# ")), "#")
    section_title = title_line[2:].strip() if title_line.startswith("# ") else ""

    is_lesson = bool(LESSON_TITLE_RE.match(section_title))
    is_unit = bool(UNIT_TITLE_RE.match(section_title))
    title_token = compact(section_title)

    normalized: list[str] = []
    for line in preamble:
        normalized.append(line)

    if normalized and normalized[-1] != "":
        normalized.append("")

    saw_major_heading = not is_lesson

    for raw_line in content:
        stripped = raw_line.strip()

        page_match = PAGE_RE.match(stripped)
        if page_match:
            push_line(normalized, "")
            push_line(normalized, f"> Page {page_match.group(1)}")
            push_line(normalized, "")
            continue

        if not stripped:
            push_line(normalized, "")
            continue

        if stripped.isdigit():
            continue

        heading = detect_heading(stripped)
        if heading is not None:
            push_line(normalized, "")
            push_line(normalized, heading)
            push_line(normalized, "")
            if heading.startswith("## "):
                saw_major_heading = True
            continue

        token = compact(stripped)

        if not is_unit and UNIT_TITLE_RE.match(stripped):
            continue
        if token == title_token:
            continue
        if stripped in {"第", "課"}:
            continue

        if is_lesson and not saw_major_heading:
            continue

        push_line(normalized, stripped)

    while normalized and normalized[-1] == "":
        normalized.pop()

    return "\n".join(normalized) + "\n"


def read_title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def read_pages_line(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("> Pages:"):
            return line.replace("> ", "", 1).strip()
    return ""


def ordered_source_files(source_dir: Path) -> list[Path]:
    index_path = source_dir / "index.md"
    if not index_path.is_file():
        return sorted(path for path in source_dir.glob("*.md") if path.name != "index.md")

    ordered: list[Path] = []
    for line in index_path.read_text(encoding="utf-8").splitlines():
        match = re.search(r"\(([^)]+\.md)\)", line)
        if not match:
            continue
        file_path = source_dir / match.group(1)
        if file_path.is_file() and file_path.name != "index.md":
            ordered.append(file_path)

    return ordered


def write_index(book_title: str, target_dir: Path, file_paths: list[Path]) -> None:
    lines = [f"# {book_title}", ""]
    for path in file_paths:
        title = read_title(path)
        pages = read_pages_line(path)
        if pages:
            lines.append(f"- [{title}]({path.name}) | {pages}")
        else:
            lines.append(f"- [{title}]({path.name})")
    (target_dir / "index.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    source_dir = args.source_dir.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    source_files = ordered_source_files(source_dir)

    written_files: list[Path] = []
    for source_path in source_files:
        normalized_text = normalize_document(source_path.read_text(encoding="utf-8"))
        target_path = output_dir / source_path.name
        target_path.write_text(normalized_text, encoding="utf-8")
        written_files.append(target_path)

    book_title = args.book_title or source_dir.name
    write_index(book_title, output_dir, written_files)

    print(f"Wrote {len(written_files)} normalized markdown files to {output_dir}")
    print(f"Index: {output_dir / 'index.md'}")


if __name__ == "__main__":
    main()
