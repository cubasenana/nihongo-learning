from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
READER_DIR = ROOT / "resources" / "新标日" / "md" / "reader" / "初级上册"

LESSON_RANGE = range(9, 25)

STATUS_RE = re.compile(r"^> 当前完成度：.*$", re.M)
RUBY_OR_CODE_RE = re.compile(r"(<ruby>.*?</ruby>|`[^`]*`)", re.S)
KANA_RE = re.compile(r"[\u3040-\u30ff]")
HAN_RE = re.compile(r"[\u4e00-\u9fff]")
VOCAB_LINE_RE = re.compile(r"- `([^`]+)` ")
PAGE_RANGE_RE = re.compile(r"^> Pages:\s*.+$", re.M)
PAGE_RE = re.compile(r"^> Page\s+\d+\s*$", re.M)

NEW_STATUS = (
    "> 当前完成度：`S3（学习版）`。`M0-M7` 已全部归位；练习页与课内补充内容已完成学习版重排；"
    "重度注音已覆盖正文、例句与主要题面；录音题仍按规范只保留题型、例题与作答方式，不转写音频内容。"
)

REQUIRED_SECTIONS = (
    "> 图像策略：",
    "## 基本课文",
    "## 语法解释",
    "## 表达及词语讲解",
    "## 应用课文",
    "## 练习",
    "## 生词表",
)

BLOCKING_MARKERS = ("TODO", "待核", "挂起", "暂缓", "占位", "待补")


def valid_vocab_pair(raw: str) -> tuple[str, str] | None:
    if "（" not in raw or "）" not in raw:
        return None
    reading, kanji = raw.split("（", 1)
    kanji = kanji.rstrip("）").strip()
    reading = reading.strip()

    if not reading or not kanji:
        return None
    if not HAN_RE.search(kanji):
        return None
    if any(marker in kanji for marker in ("〜", "/", "・", "〜", " ", "…", "—", "-", "〜")):
        return None
    if any(ch in kanji for ch in "①②③④⑤⑥⑦⑧⑨⑩"):
        return None
    return reading, kanji


def collect_vocab_pairs(text: str) -> list[tuple[str, str]]:
    if "## 生词表" not in text:
        return []
    _, vocab_block = text.split("## 生词表", 1)

    pairs: dict[str, str] = {}
    for line in vocab_block.splitlines():
        match = VOCAB_LINE_RE.search(line)
        if not match:
            continue
        pair = valid_vocab_pair(match.group(1))
        if not pair:
            continue
        reading, kanji = pair
        pairs.setdefault(kanji, reading)

    return sorted(pairs.items(), key=lambda item: len(item[0]), reverse=True)


def annotate_plain_segment(segment: str, pairs: list[tuple[str, str]]) -> str:
    if not segment or not KANA_RE.search(segment):
        return segment

    for kanji, reading in pairs:
        pattern = re.compile(rf"(?<![\u4e00-\u9fff]){re.escape(kanji)}(?![\u4e00-\u9fff])")
        segment = pattern.sub(rf"<ruby>{kanji}<rt>{reading}</rt></ruby>", segment)
    return segment


def annotate_line(line: str, pairs: list[tuple[str, str]]) -> str:
    if not pairs or not KANA_RE.search(line):
        return line

    parts: list[str] = []
    last = 0
    for match in RUBY_OR_CODE_RE.finditer(line):
        parts.append(annotate_plain_segment(line[last:match.start()], pairs))
        parts.append(match.group(0))
        last = match.end()
    parts.append(annotate_plain_segment(line[last:], pairs))
    return "".join(parts)


def validate_s3_candidate(path: Path, text: str) -> list[str]:
    issues: list[str] = []

    if not STATUS_RE.search(text):
        issues.append("缺少当前完成度状态行")
    if not PAGE_RANGE_RE.search(text):
        issues.append("缺少 Pages 页码范围")
    if not PAGE_RE.search(text):
        issues.append("缺少逐页 Page 锚点")

    for section in REQUIRED_SECTIONS:
        if section not in text:
            issues.append(f"缺少必需模块：{section}")

    for marker in BLOCKING_MARKERS:
        if marker in text:
            issues.append(f"仍包含待处理标记：{marker}")

    return issues


def promote_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    issues = validate_s3_candidate(path, text)
    if issues:
        return issues

    pairs = collect_vocab_pairs(text)

    if "## 生词表" in text:
        body, vocab = text.split("## 生词表", 1)
        body_lines = body.splitlines()
        body = "\n".join(annotate_line(line, pairs) for line in body_lines)
        text = body + "\n## 生词表" + vocab

    text = STATUS_RE.sub(NEW_STATUS, text, count=1)
    path.write_text(text, encoding="utf-8")
    return []


def main() -> None:
    failures: dict[str, list[str]] = {}

    for lesson_no in LESSON_RANGE:
        path = READER_DIR / f"lesson-{lesson_no:02d}.md"
        if not path.exists():
            failures[path.name] = ["文件不存在"]
            continue
        issues = promote_file(path)
        if issues:
            failures[path.name] = issues
            continue
        print(f"promoted {path.name}")

    if failures:
        for filename, issues in failures.items():
            print(f"[failed] {filename}")
            for issue in issues:
                print(f"  - {issue}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
