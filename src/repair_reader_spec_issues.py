from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
READER_DIR = ROOT / "resources" / "新标日" / "md" / "reader" / "初级上册"
STRUCTURED_DIR = ROOT / "resources" / "新标日" / "md" / "structured" / "初级上册"

PAGES_RE = re.compile(r"^> Pages:\s*(\d+)-(\d+)\s*$", re.M)
PAGE_RE = re.compile(r"^> Page\s+(\d+)\s*$", re.M)
STATUS_RE = re.compile(r"^> 当前完成度：.*$", re.M)

PAGE_PLACEHOLDER = "> 本页内容已并入相邻页面重排，当前保留原书页码锚点。"

STATUS_BY_LESSON = {
    5: "> 当前完成度：`S3（学习版）`。`M0-M7` 已全部归位；练习页已完成学习版重排；时间表达与应用课文保持高保真阅读体验；录音题仍只保留题型、例题与作答方式，不转写音频内容。",
    6: "> 当前完成度：`S3（学习版）`。`M0-M7` 已全部归位；练习页与路线图场景已完成学习版重排；关键路线图保留参考图；录音题仍只保留题型、例题与作答方式，不转写音频内容。",
    7: "> 当前完成度：`S3（学习版）`。`M0-M7` 已全部归位；练习页与动作图示页已完成学习版重排；关键动作图示保留参考图；录音题仍只保留题型、例题与作答方式，不转写音频内容。",
    8: "> 当前完成度：`S3（学习版）`。`M0-M7` 已全部归位；练习页与补充专题已完成学习版重排；词汇图示页和街头标识页保留参考图；录音题仍只保留题型、例题与作答方式，不转写音频内容。",
}


@dataclass
class PageBlock:
    page_no: int
    lines: list[str]

    @property
    def first_heading(self) -> str | None:
        for line in self.lines:
            if line.startswith("## ") or line.startswith("### "):
                return line.strip()
        return None


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_page_blocks(text: str) -> tuple[str, list[PageBlock]]:
    matches = list(PAGE_RE.finditer(text))
    if not matches:
        return text.rstrip() + "\n", []

    prelude = text[: matches[0].start()].rstrip() + "\n"
    blocks: list[PageBlock] = []

    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        raw_lines = text[start:end].strip("\n").splitlines()
        blocks.append(PageBlock(page_no=int(match.group(1)), lines=raw_lines))

    return prelude, blocks


def load_structured_page_info(lesson_no: int) -> tuple[tuple[int, int], list[PageBlock]]:
    path = STRUCTURED_DIR / f"lesson-{lesson_no:02d}.md"
    text = read_text(path)
    range_match = PAGES_RE.search(text)
    if not range_match:
        raise ValueError(f"missing page range in {path}")
    prelude, blocks = parse_page_blocks(text)
    del prelude
    return (int(range_match.group(1)), int(range_match.group(2))), blocks


def sync_page_range(text: str, start: int, end: int) -> str:
    new_line = f"> Pages: {start}-{end}"
    if PAGES_RE.search(text):
        return PAGES_RE.sub(new_line, text, count=1)
    return text


def ensure_status_line(lesson_no: int, text: str) -> str:
    status_line = STATUS_BY_LESSON[lesson_no]
    if STATUS_RE.search(text):
        return STATUS_RE.sub(status_line, text, count=1)

    anchor = "> 图像策略："
    if anchor not in text:
        raise ValueError(f"missing image strategy line in lesson-{lesson_no:02d}")

    head, tail = text.split(anchor, 1)
    first_line, _, rest = tail.partition("\n")
    insertion = f"{anchor}{first_line}\n\n{status_line}\n"
    return head + insertion + rest


def build_repaired_blocks(reader_blocks: list[PageBlock], structured_blocks: list[PageBlock]) -> list[str]:
    expected_pages = [block.page_no for block in structured_blocks]
    structured_headings = {block.page_no: block.first_heading for block in structured_blocks}

    assigned: dict[int, list[str]] = {}
    cursor = 0
    last_assigned_page: int | None = None

    for block in reader_blocks:
        heading = block.first_heading
        target_index: int | None = None

        if heading is not None:
            for index in range(cursor, len(expected_pages)):
                page_no = expected_pages[index]
                if structured_headings.get(page_no) == heading:
                    target_index = index
                    break

        if target_index is None:
            target_index = cursor

        if target_index >= len(expected_pages):
            if last_assigned_page is None:
                continue
            assigned.setdefault(last_assigned_page, []).extend([""] + block.lines)
            continue

        page_no = expected_pages[target_index]
        cursor = target_index + 1
        last_assigned_page = page_no
        assigned[page_no] = block.lines

    output: list[str] = []
    for page_no in expected_pages:
        output.append(f"> Page {page_no}")
        output.append("")
        lines = assigned.get(page_no)
        if lines:
            output.extend(lines)
        else:
            output.append(PAGE_PLACEHOLDER)
        output.append("")

    return output


def repair_lesson_pages(lesson_no: int) -> None:
    path = READER_DIR / f"lesson-{lesson_no:02d}.md"
    text = read_text(path)
    page_range, structured_blocks = load_structured_page_info(lesson_no)
    text = sync_page_range(text, *page_range)
    prelude, reader_blocks = parse_page_blocks(text)

    rebuilt = [prelude.rstrip(), ""]
    rebuilt.extend(build_repaired_blocks(reader_blocks, structured_blocks))
    path.write_text("\n".join(line for line in rebuilt if line is not None).rstrip() + "\n", encoding="utf-8")


def repair_status_lines() -> None:
    for lesson_no in range(5, 9):
        path = READER_DIR / f"lesson-{lesson_no:02d}.md"
        text = read_text(path)
        text = ensure_status_line(lesson_no, text)
        path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    repair_status_lines()
    for lesson_no in range(9, 25):
        repair_lesson_pages(lesson_no)
        print(f"repaired lesson-{lesson_no:02d}.md")


if __name__ == "__main__":
    main()
