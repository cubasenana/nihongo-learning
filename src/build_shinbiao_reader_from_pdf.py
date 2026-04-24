from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = ROOT / "resources" / "新标日" / "新版标日第二版初级 上册(高清无水印).pdf"
STRUCTURED_DIR = ROOT / "resources" / "新标日" / "md" / "structured" / "初级上册"
READER_DIR = ROOT / "resources" / "新标日" / "md" / "reader" / "初级上册"

# `pdftotext` 的页码与教材正文页码已经对齐，这里不再做额外偏移。
PDF_OFFSET = 0
PAGE_RANGE_RE = re.compile(r"^> Pages:\s*(\d+)-(\d+)\s*$", re.M)

SECTION_HEADINGS = {
    "基本课文": "## 基本课文",
    "语法解释": "## 语法解释",
    "表达及词语讲解": "## 表达及词语讲解",
    "应用课文": "## 应用课文",
    "练习": "## 练习",
    "练习i": "### 练习 I",
    "练习ii": "### 练习 II",
    "单元末": "## 单元末",
}

HEADING_ALIASES = {
    "练习h": "### 练习 II",
    "练习n": "### 练习 II",
    "练习u": "### 练习 II",
}


def find_pdftotext() -> str:
    exe = shutil.which("pdftotext")
    if not exe:
        raise FileNotFoundError("pdftotext not found in PATH")
    return exe


def extract_pdf_text(start_book_page: int, end_book_page: int) -> str:
    pdftotext = find_pdftotext()
    start_pdf_page = start_book_page + PDF_OFFSET
    end_pdf_page = end_book_page + PDF_OFFSET
    result = subprocess.run(
        [pdftotext, "-layout", "-f", str(start_pdf_page), "-l", str(end_pdf_page), str(PDF_PATH), "-"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )
    return result.stdout


def load_lesson_page_range(lesson_no: int) -> tuple[int, int]:
    path = STRUCTURED_DIR / f"lesson-{lesson_no:02d}.md"
    text = path.read_text(encoding="utf-8")
    match = PAGE_RANGE_RE.search(text)
    if not match:
        raise ValueError(f"missing page range in {path}")
    return int(match.group(1)), int(match.group(2))


def compact_spaces(text: str) -> str:
    previous = None
    while previous != text:
        previous = text
        text = re.sub(r"(?<=[\u3040-\u30ff\u4e00-\u9fffA-Za-z0-9])\s+(?=[\u3040-\u30ff\u4e00-\u9fffA-Za-z0-9])", "", text)
    text = re.sub(r"\s+([，。！？：；）】》、])", r"\1", text)
    text = re.sub(r"([（【《])\s+", r"\1", text)
    return text.strip()


def normalize_heading(line: str) -> str | None:
    key = re.sub(r"\s+", "", line).lower()
    if key in SECTION_HEADINGS:
        return SECTION_HEADINGS[key]
    if key in HEADING_ALIASES:
        return HEADING_ALIASES[key]
    if len(key) <= 5 and "本" in key and "文" in key:
        return "## 基本课文"
    return None


def is_noise_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if re.fullmatch(r"\d{1,3}", stripped):
        return True
    if re.match(r"^第\s*\d+\s*单元", stripped):
        return True
    if re.match(r"^第\s*\d+\s*課", stripped):
        return True
    if re.match(r"^目录$", stripped):
        return True
    if len(stripped) <= 12 and re.search(r"[\^_＝~…|<>]", stripped):
        return True
    if re.search(r"[^\w\s\u3040-\u30ff\u4e00-\u9fff（）()：:，。,．！？!?\-・/％%①②③④⑤⑥⑦⑧⑨⑩△▲▼▽□■○●◆★☆…『』「」【】《》“”‘’]", stripped):
        bad_chars = re.findall(r"[^\w\s\u3040-\u30ff\u4e00-\u9fff（）()：:，。,．！？!?\-・/％%①②③④⑤⑥⑦⑧⑨⑩△▲▼▽□■○●◆★☆…『』「」【】《》“”‘’]", stripped)
        if bad_chars and len(bad_chars) / max(len(stripped), 1) >= 0.12:
            return True
        # Short OCR-garbage lines are usually more harmful than helpful.
        return len(stripped) <= 16
    return False


def normalize_line(line: str) -> str:
    line = line.replace("：", ":")
    line = re.sub(r"\s+", " ", line.strip())
    line = re.sub(r"^(甲|乙)\s*:\s*", r"\1：", line)
    line = re.sub(r"^(李|森|小野|長島|吉田|店員)\s*:\s*", r"\1：", line)
    line = compact_spaces(line)
    line = line.replace("甲:", "甲：").replace("乙:", "乙：").replace("李:", "李：").replace("小野:", "小野：").replace("森:", "森：").replace("長島:", "長島：")
    return line


def title_fragments(title: str, lesson_no: int) -> set[str]:
    plain = title.removeprefix("#").strip()
    pieces = {part.strip() for part in plain.split() if part.strip()}
    pieces.discard(f"第{lesson_no}課")
    pieces.update({f"第{lesson_no}", "第", "課", "第課"})
    return pieces


def postprocess_reader_text(text: str) -> str:
    text = re.sub(
        r"(?m)^(甲\s*[：:].+)\n### 对话 ([ABCDＡＢＣＤ])\n\n?(乙\s*[：:].+)",
        r"### 对话 \2\n\n\1\n\3",
        text,
    )
    text = re.sub(r"(?m)^(乙\s*[：:].+)\n### 对话 ([ABCDＡＢＣＤ])$", r"### 对话 \2\n\n\1", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def page_footer(lines: list[str]) -> int | None:
    for raw in reversed(lines[-8:]):
        match = re.fullmatch(r"(\d{1,3})", raw.strip())
        if match:
            return int(match.group(1))
    return None


def extract_structured_vocab_tail(lesson_no: int) -> str:
    path = STRUCTURED_DIR / f"lesson-{lesson_no:02d}.md"
    text = path.read_text(encoding="utf-8")
    marker = "## 生词表"
    idx = text.find(marker)
    if idx < 0:
        return ""
    tail = text[idx:]
    stop_match = re.search(r"^> Page \d+\s*$|^# 第", tail[len(marker):], re.M)
    if stop_match:
        tail = tail[: len(marker) + stop_match.start()]
    return tail.strip()


def build_reader_markdown(lesson_no: int) -> str:
    structured_path = STRUCTURED_DIR / f"lesson-{lesson_no:02d}.md"
    structured_text = structured_path.read_text(encoding="utf-8")
    title = structured_text.splitlines()[0].strip()
    skip_title_fragments = title_fragments(title, lesson_no)
    title_compact = re.sub(r"\s+", "", title.removeprefix("#").replace(f"第{lesson_no}課", "").strip())
    start_page, end_page = load_lesson_page_range(lesson_no)
    raw_pdf = extract_pdf_text(start_page, end_page)
    vocab_tail = extract_structured_vocab_tail(lesson_no)

    out_lines: list[str] = [
        title,
        "",
        f"> Pages: {start_page}-{end_page}",
        "",
        "> 完成等级：`S1`（主干可读草稿）",
        "> 说明：本稿已按原 PDF 重新拉直主内容，后续继续按 `READER_SPEC.md` 提升到 `S2/S3`。",
        "> 图像策略：本轮优先先拉直正文；需要保留参考图的页面后续单独补图。",
        "",
    ]

    stop_pdf_after_vocab = False
    current_section = ""
    pages = raw_pdf.split("\f")
    fallback_page = start_page

    for page_text in pages:
        if stop_pdf_after_vocab:
            break

        raw_lines = [line.rstrip() for line in page_text.splitlines()]
        footer = page_footer(raw_lines)
        page_no = footer or fallback_page
        fallback_page += 1

        cleaned_page_lines: list[str] = []
        for raw in raw_lines:
            if not raw.strip():
                cleaned_page_lines.append("")
                continue
            if is_noise_line(raw):
                continue
            line = normalize_line(raw)
            if not line:
                continue
            if footer == start_page and not current_section:
                compact = re.sub(r"\s+", "", line)
                if line in skip_title_fragments:
                    continue
                if compact and compact != title_compact and compact in title_compact:
                    continue
                if line.startswith("第") and len(line) <= 6:
                    continue
                if re.fullmatch(r"[■□◆◇○●▲△_=\-~…]+", line):
                    continue
            heading = normalize_heading(line)
            if heading:
                if heading == "## 生词表":
                    stop_pdf_after_vocab = True
                    break
                if heading != current_section:
                    if cleaned_page_lines and cleaned_page_lines[-1] != "":
                        cleaned_page_lines.append("")
                    cleaned_page_lines.append(heading)
                    cleaned_page_lines.append("")
                    current_section = heading
                continue
            if re.fullmatch(r"[ABCDＡＢＣＤ]", line):
                cleaned_page_lines.append(f"### 对话 {line}")
                cleaned_page_lines.append("")
                continue
            cleaned_page_lines.append(line)

        while cleaned_page_lines and cleaned_page_lines[0] == "":
            cleaned_page_lines.pop(0)
        while cleaned_page_lines and cleaned_page_lines[-1] == "":
            cleaned_page_lines.pop()
        out_lines.append(f"> Page {page_no}")
        out_lines.append("")
        if not cleaned_page_lines:
            out_lines.append("> 本页内容已并入相邻页面重排，保留原书页码锚点。")
            out_lines.append("")
            continue

        if page_no == start_page and not current_section:
            out_lines.append("## 基本课文")
            out_lines.append("")
            current_section = "## 基本课文"
        out_lines.extend(cleaned_page_lines)
        out_lines.append("")

    if vocab_tail:
        out_lines.append(vocab_tail)
        out_lines.append("")

    # Final light cleanup.
    text = "\n".join(out_lines)
    text = postprocess_reader_text(text)
    return text.rstrip() + "\n"


def main() -> None:
    READER_DIR.mkdir(parents=True, exist_ok=True)
    for lesson_no in range(9, 25):
        target = READER_DIR / f"lesson-{lesson_no:02d}.md"
        target.write_text(build_reader_markdown(lesson_no), encoding="utf-8")
        print(f"built {target.name}")


if __name__ == "__main__":
    main()
