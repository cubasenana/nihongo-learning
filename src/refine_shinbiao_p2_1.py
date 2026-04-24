from __future__ import annotations

from pathlib import Path
import re
import unicodedata


ROOT = Path(r"D:\Project\GitHub\nihongo-learning")
STRUCTURED = ROOT / r"resources\新标日\md\structured\初级上册"


def compact_cjk_spaces(text: str) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    text = re.sub(r"(?<=[\u3040-\u30ff\u3400-\u9fff])\s+(?=[\u3040-\u30ff\u3400-\u9fff])", "", text)
    return text.strip()


def normalize_lesson_number(raw: str) -> str:
    text = unicodedata.normalize("NFKC", raw)
    text = text.replace("!", "1").replace("！", "1")
    digits = re.sub(r"\D", "", text)
    return digits or raw.strip()


def replace_first_and_remove_duplicates(text: str, pattern: str, replacement: str) -> str:
    compiled = re.compile(pattern, re.MULTILINE)
    first = True

    def repl(match: re.Match[str]) -> str:
        nonlocal first
        if first:
            first = False
            return replacement
        return ""

    return compiled.sub(repl, text)


def dedupe_exact_line(text: str, target: str) -> str:
    seen = False
    lines: list[str] = []
    for line in text.splitlines():
        if line == target:
            if seen:
                continue
            seen = True
        lines.append(line)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def demote_appendix_subsections(text: str, section_heading: str, next_heading: str | None = None) -> str:
    if section_heading not in text:
        return text

    start = text.index(section_heading) + len(section_heading)
    end = text.index(next_heading, start) if next_heading and next_heading in text[start:] else len(text)
    body = text[start:end]
    body = re.sub(r"(?m)^## 第", "### 第", body)
    return text[:start] + body + text[end:]


def normalize_appendix() -> None:
    path = STRUCTURED / "appendix.md"
    text = path.read_text(encoding="utf-8")

    text = text.replace("第 23课 周末或节假日,有时散步,有时\n买东西", "第 23课 周末或节假日,有时散步,有时买东西")

    text = re.sub(r"(?m)^I\.课文译文\s*$", "## I. 课文译文", text)
    text = re.sub(r"(?m)^♦课文译文的使用符号如下:\s*$", "- 课文译文的使用符号如下：", text)
    text = text.replace("甲/5表示甲乙都可以。", "甲/乙表示甲乙都可以。")
    text = re.sub(r"(?m)^课\s*文\s*译\s*文\s*$", "", text)
    text = re.sub(r"(?m)^课文译文\s*$", "", text)

    text = re.sub(
        r"(?m)^第\s*([!！0-9０-９]+)\s*[课課]\s*(.*)\s*$",
        lambda m: (
            f"## 第{normalize_lesson_number(m.group(1))}课 {compact_cjk_spaces(m.group(2))}"
            if compact_cjk_spaces(m.group(2))
            else f"### 第{normalize_lesson_number(m.group(1))}课"
        ),
        text,
    )
    text = re.sub(
        r"(?m)^[く〈]\s*应用课文\s*[〉>]\s*(.+?)\s*$",
        lambda m: f"## 应用课文：{compact_cjk_spaces(m.group(1))}",
        text,
    )

    text = re.sub(r"(?m)^H\s*\.\s*练习!!参考答案\s*$", "## II. 练习 II 参考答案", text)
    text = re.sub(r"(?m)^・\s*练习!!参考答案的使用符号如下:\s*$", "- 练习 II 参考答案的使用符号如下：", text)
    text = re.sub(r"(?m)^练习!!参考答案\s*$", "", text)

    text = replace_first_and_remove_duplicates(
        text,
        r"^练习[口H!I1]+、模拟试题参考答案\s*$",
        "## III. 练习与模拟试题参考答案",
    )
    text = replace_first_and_remove_duplicates(
        text,
        r"^句型、表达索引\s*$",
        "## IV. 句型、表达索引",
    )

    text = demote_appendix_subsections(text, "## II. 练习 II 参考答案", "## III. 练习与模拟试题参考答案")
    text = demote_appendix_subsections(text, "## III. 练习与模拟试题参考答案", "## IV. 句型、表达索引")
    text = demote_appendix_subsections(text, "## IV. 句型、表达索引")
    text = re.sub(r"(?m)^### 对话 [A-D]\s*$", "", text)

    text = re.sub(r"\n{3,}", "\n\n", text)
    path.write_text(text, encoding="utf-8")


def normalize_mock_test() -> None:
    path = STRUCTURED / "mock-test-n5.md"
    text = path.read_text(encoding="utf-8")

    text = re.sub(r"(?m)^模拟试题\s*$", "", text)
    text = re.sub(r"(?m)^注意事项\s*$", "## 注意事项", text, count=1)
    text = re.sub(r"(?m)^解答用紙\s*$", "## 解答用紙", text, count=1)
    text = re.sub(r"(?m)^•げんごちしき（もじ・ごい）\s*$", "### げんごちしき（もじ・ごい）", text)
    text = re.sub(r"(?m)^•げんごちしき（ぶんぽう）[•・]どっかい\s*$", "### げんごちしき（ぶんぽう）・どっかい", text)
    text = re.sub(r"(?m)^•ちょうかい\s*$", "### ちょうかい", text)
    text = re.sub(r"(?m)^言語知識（文字・語彙）\s*$", "## 言語知識（文字・語彙）", text)
    text = re.sub(r"(?m)^言語知識\s*（文法）[•・]読解\s*$", "## 言語知識（文法）・読解", text)
    text = re.sub(r"(?m)^聴解スクリプト\s*$", "## 聴解スクリプト", text)
    text = re.sub(
        r"(?m)^•言語知識\s*（文字[•・]語彙）\s*$",
        "## 参考答案（OCR 噪声较高）\n\n### 言語知識（文字・語彙）",
        text,
        count=1,
    )
    text = re.sub(r"(?m)^•言語知識（文法）\s*$", "### 言語知識（文法）", text)

    if "## ちょうかい" not in text:
        text = text.replace("> Page 330", "## ちょうかい\n\n> Page 330", 1)

    text = re.sub(r"\n{3,}", "\n\n", text)
    path.write_text(text, encoding="utf-8")


def update_todo() -> None:
    path = STRUCTURED / "TODO.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("- [ ] `P2-1` 整理 `N5` 模拟题与附录结构", "- [x] `P2-1` 整理 `N5` 模拟题与附录结构")
    text = text.replace("- 当前执行中：`P2-1`", "- 当前执行中：`P2-2`")
    path.write_text(text, encoding="utf-8")


def update_review_pages() -> None:
    path = STRUCTURED / "review-pages.md"
    text = path.read_text(encoding="utf-8")
    lesson_line = "- [lesson-01.md](./lesson-01.md) 到 [lesson-24.md](./lesson-24.md)：正文结构已完成一轮规则化清洗，已统一 `基本课文 / 语法解释 / 练习 / 单元末 / 场景对话` 等核心标题。"
    mock_line = "- [mock-test-n5.md](./mock-test-n5.md) 与 [appendix.md](./appendix.md)：已完成一轮结构化收尾，补齐 `N5` 模拟题、附录、答案区和索引区的主标题。"
    text = text.replace(
        "- [mock-test-n5.md](./mock-test-n5.md) 与 [appendix.md](./appendix.md)：适合作为 `P2-1` 的收尾清洗对象。\n- [src](../../../src)：适合作为 `P2-2` 的脚本入口整理与说明文档补充对象。",
        "- [src](../../../src)：适合作为 `P2-2` 的脚本入口整理与说明文档补充对象。"
    )
    text = text.replace(
        "- [lesson-01.md](./lesson-01.md) 到 [lesson-24.md](./lesson-24.md)：正文结构已完成一轮规则化清洗，已统一 `基本课文 / 语法解释 / 练习 / 单元末 / 场景对话` 等核心标题。\n- [lesson-01.md](./lesson-01.md) 到 [lesson-24.md](./lesson-24.md)：正文结构已完成一轮规则化清洗，已统一 `基本课文 / 语法解释 / 练习 / 单元末 / 场景对话` 等核心标题。",
        "- [lesson-01.md](./lesson-01.md) 到 [lesson-24.md](./lesson-24.md)：正文结构已完成一轮规则化清洗，已统一 `基本课文 / 语法解释 / 练习 / 单元末 / 场景对话` 等核心标题。"
    )
    text = text.replace(
        "- [第24課 李さんは もう すぐ 来ると 思います](./lesson-24.md)：`Page 308` 生词表已结合原 PDF 页图完成首轮精修。",
        "- [第24課 李さんは もう すぐ 来ると 思います](./lesson-24.md)：`Page 308` 生词表已结合原 PDF 页图完成首轮精修。\n- [mock-test-n5.md](./mock-test-n5.md) 与 [appendix.md](./appendix.md)：已完成一轮结构化收尾，补齐 `N5` 模拟题、附录、答案区和索引区的主标题。"
    )
    text = text.replace(
        "- 下一阶段建议顺序是：正文高噪声结构 -> `N5` 模拟题与附录 -> 脚本入口与说明文档。",
        "- 下一阶段建议顺序是：脚本入口与说明文档 -> 决定是否让 `resources/` 退出 `.gitignore` -> 按需做零散页人工复核。"
    )
    text = dedupe_exact_line(text, lesson_line)
    text = dedupe_exact_line(text, mock_line)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    normalize_appendix()
    normalize_mock_test()
    update_todo()
    update_review_pages()


if __name__ == "__main__":
    main()
