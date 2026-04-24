# AI 接口

这里放的是给抓取器、脚本和 AI 用的直读入口，不走网页排版层。

当前已开放：

- 新标日初级上册原文镜像：`/nihongo-learning/ai/shinbiao/elementary-book-1/`
- 浏览安全索引：`/nihongo-learning/ai/shinbiao/elementary-book-1/`
- 原文索引：`/nihongo-learning/ai/shinbiao/elementary-book-1/raw/index.md`
- 机器清单：`/nihongo-learning/ai/shinbiao/elementary-book-1/manifest.json`
- 单课浏览模式：`/nihongo-learning/ai/shinbiao/elementary-book-1/lesson-05/`
- 单课原始 MD：`/nihongo-learning/ai/shinbiao/elementary-book-1/raw/lesson-05.md`

## 设计原则

- 每课保留一份源 Markdown 镜像
- 每课额外生成一份带 `utf-8` 元信息的浏览安全页
- 站点网页继续走 `VitePress` 渲染版
- AI 入口优先保证稳定、纯文本、可抓取
- 若某课存在 `reader/` 覆盖稿，则 AI 入口默认也返回该覆盖稿

## 现在怎么用

1. 人类阅读：继续看 `/shinbiao/elementary-book-1/lesson-xx`
2. 浏览器 / 通用 Web Fetch：优先请求 `/ai/shinbiao/elementary-book-1/lesson-xx/`
3. AI / 脚本抓取原始 Markdown：请求 `/ai/shinbiao/elementary-book-1/raw/lesson-xx.md`
4. 批量发现：先读 `manifest.json`，再按 `viewPath` 或 `rawPath` 选择抓取
