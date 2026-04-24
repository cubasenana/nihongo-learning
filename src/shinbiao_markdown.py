from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path


PAGE_SPLIT_RE = re.compile(r"^## Page (\d+)\n\n", re.M)
SPACE_RE = re.compile(r"\s+")
FILLER_RE = re.compile(r"[.。•…■·\-]+")
CJK_RE = re.compile(r"[\u3400-\u9fff\u3040-\u30ff]")


@dataclass(frozen=True)
class Page:
    number: int
    text: str

    @property
    def lines(self) -> list[str]:
        return self.text.splitlines()

    @property
    def first_nonempty_line(self) -> str:
        for line in self.lines:
            stripped = line.strip()
            if stripped:
                return stripped
        return ""


@dataclass(frozen=True)
class TocEntry:
    kind: str
    number: int | None
    title: str
    logical_page: int


@dataclass
class Section:
    slug: str
    title: str
    kind: str
    start_page: int
    end_page: int = 0


def load_pages(markdown_path: Path) -> list[Page]:
    text = markdown_path.read_text(encoding="utf-8")
    parts = PAGE_SPLIT_RE.split(text)
    pages: list[Page] = []

    for index in range(1, len(parts), 2):
        number = int(parts[index])
        page_text = parts[index + 1].strip()
        pages.append(Page(number=number, text=page_text))

    return pages


def pages_by_number(pages: list[Page]) -> dict[int, Page]:
    return {page.number: page for page in pages}


def collapse_spaces(text: str) -> str:
    return SPACE_RE.sub(" ", text).strip()


def normalize_toc_line(line: str) -> str:
    stripped = line.strip()
    if not stripped:
        return ""

    stripped = FILLER_RE.sub(" ", stripped)
    stripped = stripped.replace("•", " ")
    stripped = stripped.replace("■", " ")
    return collapse_spaces(stripped)


def parse_toc_entries(pages: list[Page]) -> list[TocEntry]:
    page_map = pages_by_number(pages)
    entries: list[TocEntry] = []

    lesson_re = re.compile(r"^第\s*(\d+)\s*課\s*(.*?)\s+(\d{2,3})$")
    unit_re = re.compile(r"^第\s*(\d+)\s*单元\s*(.*?)\s+(\d{2,3})$")

    for toc_page in (15, 16, 17):
        page = page_map.get(toc_page)
        if page is None:
            continue

        for raw_line in page.lines:
            line = normalize_toc_line(raw_line)
            if not line:
                continue

            lesson_match = lesson_re.match(line)
            if lesson_match:
                number = int(lesson_match.group(1))
                title = clean_title(lesson_match.group(2))
                logical_page = int(lesson_match.group(3))
                entries.append(
                    TocEntry(
                        kind="lesson",
                        number=number,
                        title=f"第{number}課 {title}",
                        logical_page=logical_page,
                    )
                )
                continue

            unit_match = unit_re.match(line)
            if unit_match:
                number = int(unit_match.group(1))
                title = clean_title(unit_match.group(2))
                logical_page = int(unit_match.group(3))
                entries.append(
                    TocEntry(
                        kind="unit",
                        number=number,
                        title=f"第{number}单元 {title}",
                        logical_page=logical_page,
                    )
                )
                continue

            if "日本语能力测试N5模拟试题" in line:
                page_match = re.search(r"(\d{2,3})$", line)
                if page_match:
                    entries.append(
                        TocEntry(
                            kind="mock-test",
                            number=None,
                            title="日本语能力测试 N5 模拟试题",
                            logical_page=int(page_match.group(1)),
                        )
                    )

    return entries


def clean_title(title: str) -> str:
    cleaned = collapse_spaces(title)
    cleaned = cleaned.strip(" /'\"")
    cleaned = cleaned.replace("  ", " ")
    return cleaned


def guess_unit_title(page: Page, fallback: str) -> str:
    for raw_line in page.lines[:10]:
        line = collapse_spaces(raw_line)
        if not line:
            continue
        if line.isdigit():
            continue
        if "課" in line:
            continue
        if not CJK_RE.search(line):
            continue
        if len(line) > 24:
            continue
        return clean_title(line)
    return fallback


def detect_page_offset(pages: list[Page], toc_entries: list[TocEntry]) -> int:
    mock_entry = next((entry for entry in toc_entries if entry.kind == "mock-test"), None)
    if mock_entry is not None:
        for page in pages:
            if page.first_nonempty_line == "日本语能力测试N5模拟试题":
                return page.number - mock_entry.logical_page

    raise ValueError("Unable to determine the logical-to-physical page offset.")


def detect_intro_start(pages: list[Page]) -> int:
    for page in pages:
        if page.first_nonempty_line == "入门单元":
            return page.number
    raise ValueError("Unable to locate the start of the intro unit.")


def detect_appendix_start(pages: list[Page]) -> int:
    for page in pages:
        if page.first_nonempty_line == "附录":
            return page.number
    raise ValueError("Unable to locate the appendix.")


def build_sections(pages: list[Page]) -> list[Section]:
    toc_entries = parse_toc_entries(pages)
    if not toc_entries:
        raise ValueError("No TOC entries were parsed from the source markdown.")

    page_map = pages_by_number(pages)
    page_offset = detect_page_offset(pages, toc_entries)
    intro_start = detect_intro_start(pages)
    appendix_start = detect_appendix_start(pages)
    max_page = max(page.number for page in pages)

    sections: list[Section] = [
        Section(slug="00-frontmatter", title="前置资料", kind="frontmatter", start_page=1),
        Section(slug="01-intro-unit", title="入门单元", kind="intro-unit", start_page=intro_start),
    ]

    for entry in toc_entries:
        physical_page = entry.logical_page + page_offset

        if entry.kind == "unit":
            assert entry.number is not None
            page = page_map.get(physical_page)
            title = entry.title
            if page is not None:
                guessed = guess_unit_title(page, entry.title)
                title = f"第{entry.number}单元 {guessed}"
            sections.append(
                Section(
                    slug=f"unit-{entry.number:02d}-overview",
                    title=f"{title} 概览",
                    kind="unit",
                    start_page=physical_page,
                )
            )
        elif entry.kind == "lesson":
            assert entry.number is not None
            sections.append(
                Section(
                    slug=f"lesson-{entry.number:02d}",
                    title=entry.title,
                    kind="lesson",
                    start_page=physical_page,
                )
            )
        elif entry.kind == "mock-test":
            sections.append(
                Section(
                    slug="mock-test-n5",
                    title=entry.title,
                    kind="mock-test",
                    start_page=physical_page,
                )
            )

    sections.append(
        Section(
            slug="appendix",
            title="附录",
            kind="appendix",
            start_page=appendix_start,
        )
    )

    sections.sort(key=lambda section: section.start_page)

    unique_sections: list[Section] = []
    seen_starts: set[int] = set()
    for section in sections:
        if section.start_page in seen_starts:
            continue
        seen_starts.add(section.start_page)
        unique_sections.append(section)

    for index, section in enumerate(unique_sections):
        next_start = max_page + 1
        if index + 1 < len(unique_sections):
            next_start = unique_sections[index + 1].start_page
        section.end_page = next_start - 1

    return unique_sections


def render_section(section: Section, page_map: dict[int, Page]) -> str:
    lines = [
        f"# {section.title}",
        "",
        f"> Pages: {section.start_page}-{section.end_page}",
        "",
    ]

    for page_number in range(section.start_page, section.end_page + 1):
        page = page_map.get(page_number)
        if page is None:
            continue
        lines.append(f"## Page {page_number}")
        lines.append("")
        lines.extend(page.lines)
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_index(book_title: str, sections: list[Section]) -> str:
    lines = [f"# {book_title}", ""]
    for section in sections:
        lines.append(f"- [{section.title}]({section.slug}.md)")
        lines.append(f"  Pages: `{section.start_page}-{section.end_page}`")
    return "\n".join(lines).rstrip() + "\n"
