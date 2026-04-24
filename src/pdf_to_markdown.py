from __future__ import annotations

import argparse
import re
from pathlib import Path

from pypdf import PdfReader


PAGE_NUMBER_RE = re.compile(r"^(?:\d+|[IVXLCDM]+)$")
SPACE_RE = re.compile(r"[ \t\u3000]+")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a PDF with an embedded text layer into Markdown."
    )
    parser.add_argument("pdf", type=Path, help="Source PDF path")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output Markdown path. Defaults to the PDF name with a .md suffix.",
    )
    parser.add_argument(
        "--title",
        help="Optional Markdown title. Defaults to the PDF stem.",
    )
    parser.add_argument(
        "--start-page",
        type=int,
        default=1,
        help="1-based first page to export",
    )
    parser.add_argument(
        "--end-page",
        type=int,
        help="1-based last page to export. Defaults to the end of the PDF.",
    )
    return parser.parse_args()


def normalize_line(line: str) -> str:
    line = line.replace("\x00", " ").replace("\u00a0", " ")
    line = SPACE_RE.sub(" ", line)
    return line.strip()


def clean_page_lines(text: str) -> list[str]:
    raw_lines = text.splitlines()
    lines: list[str] = []

    for index, raw_line in enumerate(raw_lines):
        line = normalize_line(raw_line)
        if not line:
            if lines and lines[-1] != "":
                lines.append("")
            continue

        is_last_content_line = index == len(raw_lines) - 1
        if is_last_content_line and PAGE_NUMBER_RE.fullmatch(line):
            continue

        lines.append(line)

    while lines and lines[-1] == "":
        lines.pop()

    return lines


def render_markdown(
    pdf_path: Path,
    title: str,
    reader: PdfReader,
    start_page: int,
    end_page: int,
) -> str:
    parts = [
        f"# {title}",
        "",
        f"> Source PDF: `{pdf_path.name}`",
        "> Conversion: embedded text extraction via `pypdf`",
        "> Notes: page boundaries are preserved; complex tables, ruby text, and layout may need manual cleanup.",
        "",
    ]

    for page_number in range(start_page, end_page + 1):
        page = reader.pages[page_number - 1]
        text = page.extract_text() or ""
        lines = clean_page_lines(text)

        parts.append(f"## Page {page_number}")
        parts.append("")

        if lines:
            parts.extend(lines)
        else:
            parts.append("[[no extractable text]]")

        parts.append("")

    return "\n".join(parts).strip() + "\n"


def main() -> None:
    args = parse_args()
    pdf_path = args.pdf.expanduser().resolve()
    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    output_path = args.output.expanduser().resolve() if args.output else pdf_path.with_suffix(".md")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    reader = PdfReader(str(pdf_path))
    total_pages = len(reader.pages)

    start_page = max(1, args.start_page)
    end_page = args.end_page or total_pages
    end_page = min(end_page, total_pages)

    if start_page > end_page:
        raise ValueError(
            f"Invalid page range: start_page={start_page}, end_page={end_page}, total_pages={total_pages}"
        )

    title = args.title or pdf_path.stem
    markdown = render_markdown(pdf_path, title, reader, start_page, end_page)
    output_path.write_text(markdown, encoding="utf-8")

    print(f"Wrote {output_path}")
    print(f"Pages: {start_page}-{end_page} / {total_pages}")


if __name__ == "__main__":
    main()
