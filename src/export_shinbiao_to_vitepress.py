from __future__ import annotations

from dataclasses import dataclass
import html
import json
from pathlib import Path
import re
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "resources" / "新标日" / "md" / "structured" / "初级上册"
READER_DIR = ROOT / "resources" / "新标日" / "md" / "reader" / "初级上册"
DOCS_DIR = ROOT / "docs"
BOOK_DIR = DOCS_DIR / "shinbiao" / "elementary-book-1"
READER_ASSET_DIR = READER_DIR / "assets"
BOOK_ASSET_DIR = BOOK_DIR / "assets"
PUBLIC_DIR = DOCS_DIR / "public"
AI_ROOT_DIR = PUBLIC_DIR / "ai" / "shinbiao" / "elementary-book-1"
AI_RAW_DIR = AI_ROOT_DIR / "raw"

SITE_BASE = "/nihongo-learning"
BOOK_ROUTE = "/shinbiao/elementary-book-1"
AI_BOOK_ROUTE = "/ai/shinbiao/elementary-book-1"
AI_RAW_ROUTE = f"{AI_BOOK_ROUTE}/raw"

INDEX_ENTRY_RE = re.compile(r"^- \[(.+?)\]\((.+?\.md)\)(?: \| (.+))?$")
PAGE_RANGE_RE = re.compile(r"^> Pages:\s*(.+)$", re.MULTILINE)
PAGE_RE = re.compile(r"^> Page\s+(\d+)\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
SAFE_INLINE_HTML_RE = re.compile(r"</?(ruby|rt|rp)\b[^>]*>")
ASSET_LINK_RE = re.compile(r"(!\[[^\]]*\]\()(\./assets/[^)]+)(\))")
NUMBER_RE = re.compile(r"\d+")

SKIP_FILES = {"index.md", "review-pages.md", "TODO.md", "READER_SPEC.md"}


@dataclass(frozen=True)
class Entry:
    title: str
    filename: str
    pages: str | None

    @property
    def html_path(self) -> str:
        return f"{SITE_BASE}{BOOK_ROUTE}/{self.filename.removesuffix('.md')}"

    @property
    def raw_path(self) -> str:
        return f"{SITE_BASE}{AI_RAW_ROUTE}/{self.filename}"

    @property
    def view_path(self) -> str:
        return f"{SITE_BASE}{AI_BOOK_ROUTE}/{self.filename.removesuffix('.md')}/"


def natural_sort_key(value: str) -> tuple[object, ...]:
    parts: list[object] = []
    last = 0
    for match in NUMBER_RE.finditer(value):
        if match.start() > last:
            parts.append(value[last:match.start()].lower())
        parts.append(int(match.group(0)))
        last = match.end()
    if last < len(value):
        parts.append(value[last:].lower())
    return tuple(parts)


def read_source_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def extract_pages(text: str) -> str | None:
    match = PAGE_RANGE_RE.search(text)
    if match:
        return match.group(1).strip()
    return None


def derive_title(path: Path) -> str:
    text = read_source_text(path)
    match = HEADING_RE.search(text)
    if match:
        return match.group(1).strip()
    return path.stem


def load_entries() -> list[Entry]:
    entries: list[Entry] = []
    seen: set[str] = set()
    index_path = SOURCE_DIR / "index.md"

    for line in index_path.read_text(encoding="utf-8").splitlines():
        match = INDEX_ENTRY_RE.match(line.strip())
        if not match:
            continue
        title, filename, pages = match.groups()
        if filename in SKIP_FILES:
            continue
        entries.append(Entry(title=title, filename=filename, pages=pages))
        seen.add(filename)

    for path in sorted(READER_DIR.glob("*.md"), key=lambda item: natural_sort_key(item.name)):
        if path.name in SKIP_FILES or path.name in seen:
            continue
        text = read_source_text(path)
        entries.append(
            Entry(
                title=derive_title(path),
                filename=path.name,
                pages=extract_pages(text),
            )
        )

    return entries


def resolve_source_path(filename: str) -> Path:
    reader_path = READER_DIR / filename
    if reader_path.exists():
        return reader_path
    return SOURCE_DIR / filename


def source_layer_for(filename: str) -> str:
    return "reader" if (READER_DIR / filename).exists() else "structured"


def escape_preserving_safe_html(raw_line: str) -> str:
    parts: list[str] = []
    last = 0

    for match in SAFE_INLINE_HTML_RE.finditer(raw_line):
        parts.append(html.escape(raw_line[last:match.start()]))
        parts.append(match.group(0))
        last = match.end()

    parts.append(html.escape(raw_line[last:]))
    return "".join(parts)


def transform_content(text: str) -> str:
    lines: list[str] = []

    for raw_line in text.splitlines():
        range_match = PAGE_RANGE_RE.match(raw_line)
        if range_match:
            lines.append(f'<div class="page-range">Pages: {html.escape(range_match.group(1))}</div>')
            continue

        page_match = PAGE_RE.match(raw_line)
        if page_match:
            page_number = page_match.group(1)
            lines.append(f'<div class="page-marker" data-page="{page_number}">Page {page_number}</div>')
            continue

        if raw_line.lstrip().startswith("> "):
            lines.append(raw_line)
            continue

        # VitePress 会把裸露的 < / > 当作 HTML 片段解析。
        # 这里统一转义正文里的 OCR 噪声，避免单页因为少数字符直接炸掉整站构建。
        # 对 reader 稿里明确允许的少量内联 HTML（如 ruby）保留原样。
        lines.append(escape_preserving_safe_html(raw_line))

    text = "\n".join(lines)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip() + "\n"


def normalize_raw_markdown(text: str) -> str:
    def replace_asset_link(match: re.Match[str]) -> str:
        asset_path = match.group(2).removeprefix("./")
        return f"{match.group(1)}{SITE_BASE}{BOOK_ROUTE}/{asset_path}{match.group(3)}"

    normalized = ASSET_LINK_RE.sub(replace_asset_link, text)
    return normalized.strip() + "\n"


def write_utf8_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def sync_pages(entries: list[Entry]) -> None:
    if BOOK_DIR.exists():
        for path in BOOK_DIR.glob("*.md"):
            path.unlink()
    BOOK_DIR.mkdir(parents=True, exist_ok=True)

    for entry in entries:
        source_path = resolve_source_path(entry.filename)
        target_path = BOOK_DIR / entry.filename
        target_path.write_text(
            transform_content(read_source_text(source_path)),
            encoding="utf-8",
        )


def sync_assets() -> None:
    if BOOK_ASSET_DIR.exists():
        shutil.rmtree(BOOK_ASSET_DIR)

    if READER_ASSET_DIR.exists():
        shutil.copytree(READER_ASSET_DIR, BOOK_ASSET_DIR)
    else:
        BOOK_ASSET_DIR.mkdir(parents=True, exist_ok=True)


def ai_index_lines(entries: list[Entry]) -> list[str]:
    lines = [
        "# 新标日初级上册 AI 原文接口",
        "",
        "推荐给浏览器和通用 Web Fetch 的入口是 `viewPath`。",
        "需要保留原始 Markdown 字节流时，再使用 `rawPath`。",
        "",
        f"manifest.json: {SITE_BASE}{AI_BOOK_ROUTE}/manifest.json",
        f"raw index: {SITE_BASE}{AI_RAW_ROUTE}/index.md",
        "",
    ]

    for entry in entries:
        lines.extend(
            [
                f"- {entry.title}",
                f"  view: {entry.view_path}",
                f"  raw: {entry.raw_path}",
                f"  html: {entry.html_path}",
            ]
        )

    lines.append("")
    return lines


def render_ai_root_index(entries: list[Entry]) -> str:
    items = []
    for entry in entries:
        items.append(
            "<li>"
            f"<a href=\"{entry.view_path}\">{html.escape(entry.title)}</a>"
            f"<div class=\"links\">view: <a href=\"{entry.view_path}\">{html.escape(entry.view_path)}</a></div>"
            f"<div class=\"links\">raw: <a href=\"{entry.raw_path}\">{html.escape(entry.raw_path)}</a></div>"
            f"<div class=\"links\">html: <a href=\"{entry.html_path}\">{html.escape(entry.html_path)}</a></div>"
            "</li>"
        )

    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="zh-CN">',
            "<head>",
            '  <meta charset="utf-8">',
            '  <meta name="viewport" content="width=device-width, initial-scale=1">',
            "  <title>新标日初级上册 AI 原文接口</title>",
            "  <style>",
            "    body { margin: 0; font-family: ui-monospace, SFMono-Regular, Consolas, monospace; background: #fafaf9; color: #18181b; }",
            "    main { max-width: 960px; margin: 0 auto; padding: 24px 20px 48px; }",
            "    h1 { margin-top: 0; font-size: 28px; }",
            "    p { line-height: 1.7; }",
            "    ul { padding-left: 20px; }",
            "    li { margin-bottom: 18px; }",
            "    .links { margin-top: 4px; color: #52525b; font-size: 14px; }",
            "    a { color: #0f766e; text-decoration: none; }",
            "    a:hover { text-decoration: underline; }",
            "    code { background: #f4f4f5; padding: 2px 6px; border-radius: 6px; }",
            "  </style>",
            "</head>",
            "<body>",
            "<main>",
            "  <h1>新标日初级上册 AI 原文接口</h1>",
            "  <p>这里提供两类入口：<code>view</code> 用于浏览器和通用 Web Fetch，<code>raw</code> 保留原始 Markdown 镜像。</p>",
            f"  <p><a href=\"{SITE_BASE}{AI_BOOK_ROUTE}/manifest.json\">manifest.json</a> | <a href=\"{SITE_BASE}{AI_RAW_ROUTE}/index.md\">raw index.md</a></p>",
            "  <ul>",
            *[f"    {item}" for item in items],
            "  </ul>",
            "</main>",
            "</body>",
            "</html>",
            "",
        ]
    )


def render_ai_view(entry: Entry, raw_text: str) -> str:
    source_layer = source_layer_for(entry.filename)
    page_meta = html.escape(entry.pages) if entry.pages else "未标页码"
    escaped_text = html.escape(raw_text)

    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="zh-CN">',
            "<head>",
            '  <meta charset="utf-8">',
            '  <meta name="viewport" content="width=device-width, initial-scale=1">',
            f"  <title>{html.escape(entry.title)} | AI 原文镜像</title>",
            "  <style>",
            "    body { margin: 0; font-family: ui-monospace, SFMono-Regular, Consolas, monospace; background: #ffffff; color: #111827; }",
            "    main { max-width: 1080px; margin: 0 auto; padding: 24px 20px 48px; }",
            "    h1 { margin-top: 0; font-size: 26px; }",
            "    .meta { color: #4b5563; line-height: 1.7; margin-bottom: 20px; }",
            "    .meta a { color: #0f766e; text-decoration: none; }",
            "    .meta a:hover { text-decoration: underline; }",
            "    pre { white-space: pre-wrap; word-break: break-word; overflow-wrap: anywhere; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 18px; line-height: 1.65; font-size: 14px; }",
            "    code { background: #f4f4f5; padding: 2px 6px; border-radius: 6px; }",
            "  </style>",
            "</head>",
            "<body>",
            "<main>",
            f"  <h1>{html.escape(entry.title)} | AI 原文镜像</h1>",
            "  <div class=\"meta\">",
            f"    <div>pages: <code>{page_meta}</code></div>",
            f"    <div>source layer: <code>{html.escape(source_layer)}</code></div>",
            f"    <div>raw markdown: <a href=\"{entry.raw_path}\">{html.escape(entry.raw_path)}</a></div>",
            f"    <div>lesson html: <a href=\"{entry.html_path}\">{html.escape(entry.html_path)}</a></div>",
            "  </div>",
            f"  <pre>{escaped_text}</pre>",
            "</main>",
            "</body>",
            "</html>",
            "",
        ]
    )


def sync_ai_sources(entries: list[Entry]) -> None:
    if AI_ROOT_DIR.exists():
        shutil.rmtree(AI_ROOT_DIR)
    AI_RAW_DIR.mkdir(parents=True, exist_ok=True)

    manifest = {
        "book": "新标日初级上册",
        "sourcePriority": ["reader", "structured"],
        "baseUrl": f"{SITE_BASE}{AI_BOOK_ROUTE}/",
        "rawBaseUrl": f"{SITE_BASE}{AI_RAW_ROUTE}/",
        "pages": [
            {
                "title": entry.title,
                "filename": entry.filename,
                "pages": entry.pages,
                "viewPath": entry.view_path,
                "rawPath": entry.raw_path,
                "htmlPath": entry.html_path,
                "sourceLayer": source_layer_for(entry.filename),
            }
            for entry in entries
        ],
    }

    for entry in entries:
        source_path = resolve_source_path(entry.filename)
        raw_text = normalize_raw_markdown(read_source_text(source_path))
        write_utf8_text(AI_RAW_DIR / entry.filename, raw_text)
        write_utf8_text(
            AI_ROOT_DIR / entry.filename.removesuffix(".md") / "index.html",
            render_ai_view(entry, raw_text),
        )

    write_utf8_text(AI_RAW_DIR / "index.md", "\n".join(ai_index_lines(entries)))
    write_utf8_text(AI_ROOT_DIR / "index.html", render_ai_root_index(entries))
    write_utf8_text(
        AI_ROOT_DIR / "manifest.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )


def book_index_lines(entries: list[Entry]) -> list[str]:
    lines = [
        "# 新标日初级上册",
        "",
        "这是一份面向网页阅读的《新版中日交流标准日本语 初级上册》实验版导出。",
        "",
        "- 文字优先，尽量不依赖截图拼接",
        "- 页码保留为阅读锚点，版面不做纸书级复刻",
        "- 当前内容来自本地结构化稿同步，若存在 reader 覆盖稿则优先使用",
        "",
        "## AI 原文接口",
        "",
        f"- AI 原文浏览页：`{SITE_BASE}{AI_BOOK_ROUTE}/lesson-xx/`",
        f"- AI 源 MD 目录：`{SITE_BASE}{AI_RAW_ROUTE}/index.md`",
        f"- AI Manifest JSON：`{SITE_BASE}{AI_BOOK_ROUTE}/manifest.json`",
        f"- 原始 Markdown 路径模式：`{SITE_BASE}{AI_RAW_ROUTE}/lesson-xx.md`",
        "",
        "## 入门与前置",
        "",
    ]

    current_unit = ""
    in_prelude = True

    for entry in entries:
        label = f"- [{entry.title}]({entry.filename})"
        if entry.pages:
            label += f" | {entry.pages}"

        if entry.filename in {"00-frontmatter.md", "01-intro-unit.md"}:
            lines.append(label)
            continue

        if in_prelude:
            lines.extend(["", "## 课程目录", ""])
            in_prelude = False

        if entry.filename.startswith("unit-"):
            current_unit = entry.title.replace(" 概览", "")
            lines.extend(["", f"## {current_unit}", "", label])
            continue

        if entry.filename in {"mock-test-n5.md", "appendix.md"}:
            if current_unit != "附加内容":
                current_unit = "附加内容"
                lines.extend(["", "## 附加内容", ""])
            lines.append(label)
            continue

        lines.append(label)

    lines.append("")
    return lines


def write_book_index(entries: list[Entry]) -> None:
    (BOOK_DIR / "index.md").write_text("\n".join(book_index_lines(entries)), encoding="utf-8")


def main() -> None:
    entries = load_entries()
    sync_pages(entries)
    sync_assets()
    sync_ai_sources(entries)
    write_book_index(entries)
    print(f"Exported {len(entries)} pages to {BOOK_DIR} and AI artifacts to {AI_ROOT_DIR}")


if __name__ == "__main__":
    main()
