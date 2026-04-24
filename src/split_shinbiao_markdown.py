from __future__ import annotations

import argparse
from pathlib import Path

from shinbiao_markdown import build_sections, load_pages, pages_by_number, render_index, render_section


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Split a raw Shin Nihongo markdown export into section files."
    )
    parser.add_argument("source", type=Path, help="Whole-book markdown path")
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        required=True,
        help="Directory where split markdown files will be written",
    )
    parser.add_argument(
        "--book-title",
        help="Title used for the generated index.md. Defaults to the source stem.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_path = args.source.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    pages = load_pages(source_path)
    page_map = pages_by_number(pages)
    sections = build_sections(pages)

    for section in sections:
        target_path = output_dir / f"{section.slug}.md"
        target_path.write_text(render_section(section, page_map), encoding="utf-8")

    book_title = args.book_title or source_path.stem
    (output_dir / "index.md").write_text(render_index(book_title, sections), encoding="utf-8")

    print(f"Wrote {len(sections)} section files to {output_dir}")
    print(f"Index: {output_dir / 'index.md'}")


if __name__ == "__main__":
    main()
