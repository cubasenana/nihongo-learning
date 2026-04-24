from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(r"D:\Project\GitHub\nihongo-learning")
STRUCTURED = ROOT / r"resources\新标日\md\structured\初级上册"


def compact_cjk_spaces(text: str) -> str:
    text = re.sub(r"^[A-Za-z]+", "", text.strip())
    text = re.sub(r"(?<=[\u3040-\u30ff\u3400-\u9fff])\s+(?=[\u3040-\u30ff\u3400-\u9fff])", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_scene_heading(match: re.Match[str]) -> str:
    raw_title = compact_cjk_spaces(match.group(1) or "")
    if raw_title:
        return f"### 场景对话：{raw_title}"
    return "### 场景对话"


def insert_basic_heading(text: str) -> str:
    if "## 基本课文" in text:
        return text
    updated, count = re.subn(
        r"(^> Page \d+\s*$\n+)(?=### 对话 [A-D])",
        r"\1## 基本课文\n\n",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if count:
        return updated
    return text


def dedupe_grammar_headings(text: str) -> str:
    seen = False
    lines: list[str] = []
    for line in text.splitlines():
        if line.strip() == "## 语法解释":
            if seen:
                continue
            seen = True
        lines.append(line)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def normalize_lesson(path: Path) -> None:
    text = path.read_text(encoding="utf-8")

    text = insert_basic_heading(text)
    text = re.sub(r"(?m)^(?:##\s*)?语法解,释\s*$", "## 语法解释", text)
    text = re.sub(r"(?m)^元\s*$", "", text)
    text = re.sub(r"(?m)^(?:■)?实用.?$", "", text)
    text = re.sub(r"(?m)^场景对话\s*(.*)$", normalize_scene_heading, text)
    text = re.sub(r"(?m)^单元末\s*$", "## 单元末", text)
    text = dedupe_grammar_headings(text)

    if path.name == "lesson-20.md":
        text = text.replace("死五供\nr ヽ词语\n之 泉 」\nL\n", "### 词语之泉\n\n")
        text = text.replace("死ゑ供\nヽ\\日 本\n", "### 日本的时令景物与传统活动\n\n")

    if path.name == "lesson-16.md":
        text = re.sub(r"(?m)^有关疾病的词语\s*$", "### 有关疾病的词语", text)

    if path.name == "lesson-08.md":
        text = re.sub(r"(?m)^食べ物\s*$", "### 食べ物", text)

    path.write_text(text, encoding="utf-8")


def update_todo() -> None:
    path = STRUCTURED / "TODO.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("- [ ] `P1-2` 清洗正文高噪声结构：对话标签、标题、断行、专栏段落", "- [x] `P1-2` 清洗正文高噪声结构：对话标签、标题、断行、专栏段落")
    text = text.replace("- 当前执行中：`P1-2`", "- 当前执行中：`P2-1`")
    path.write_text(text, encoding="utf-8")


def update_review_pages() -> None:
    path = STRUCTURED / "review-pages.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "- [lesson-01.md](./lesson-01.md) 到 [lesson-24.md](./lesson-24.md)：集中清洗对话标签、标题错位、专栏段落断行，以及个别页内双栏错序问题。\n- [mock-test-n5.md](./mock-test-n5.md) 与 [appendix.md](./appendix.md)：适合作为 `P2-1` 的收尾清洗对象。",
        "- [mock-test-n5.md](./mock-test-n5.md) 与 [appendix.md](./appendix.md)：适合作为 `P2-1` 的收尾清洗对象。\n- [src](../../../src)：适合作为 `P2-2` 的脚本入口整理与说明文档补充对象。"
    )
    text = text.replace(
        "- [入门单元](./01-intro-unit.md)：`Page 25-28 / 30-31 / 34-37` 已完成结构化重建；笔顺图和声调图的具体图形细节仍建议回看原 PDF。",
        "- [入门单元](./01-intro-unit.md)：`Page 25-28 / 30-31 / 34-37` 已完成结构化重建；笔顺图和声调图的具体图形细节仍建议回看原 PDF。\n- [lesson-01.md](./lesson-01.md) 到 [lesson-24.md](./lesson-24.md)：正文结构已完成一轮规则化清洗，已统一 `基本课文 / 语法解释 / 练习 / 单元末 / 场景对话` 等核心标题。"
    )
    path.write_text(text, encoding="utf-8")


def main() -> None:
    for path in sorted(STRUCTURED.glob("lesson-*.md")):
        normalize_lesson(path)
    update_review_pages()
    update_todo()


if __name__ == "__main__":
    main()
