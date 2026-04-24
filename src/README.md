# Shinbiao Markdown Scripts

这套脚本用于把 `resources/新标日` 下的《新版中日交流标准日本语 初级上册》从 PDF 转成可维护的 Markdown，并逐步做结构化精修，再同步到 `VitePress` 站点。

## 建议入口

优先用统一入口查看或执行任务：

```powershell
python src/main.py list
python src/main.py run p2-1
python src/main.py run reader-pdf-9-24
python src/main.py run reader-repair-spec
python src/main.py run reader-s3-9-24
python src/main.py run reader-quality-all
python src/main.py run vitepress-export
npm run docs:clean
npm run docs:export
npm run docs:dev
```

## 推荐顺序

1. `extract` / `pipeline`
   抽取 PDF 文字层，生成最初的整本 Markdown。
2. `split` / `normalize`
   按课拆分，并做首轮标题、段落、对话结构清洗。
3. `review`
   生成回修清单，确认高价值页。
4. `reader-pdf-9-24`
   直接按原 PDF 页码重建第 `9-24` 课 `reader` 草稿，拉直正文主干并复用已精修生词表。
5. `reader-repair-spec`
   修复 `reader` 课稿中的页码范围、逐页锚点和缺失的完成度状态行，使其重新对齐 `READER_SPEC` 的 `M0 / S1-S3` 要求。
6. `reader-s3-9-24`
   把第 `9-24` 课 `reader` 稿统一提升到 `S3` 学习版，补齐更密的 `ruby` 并收口完成度说明；脚本会先校验 `Pages / Page / 图像策略 / 关键模块` 是否齐全，避免半成品被误盖章成 `S3`。
7. `reader-quality-all`
   按 `READER_SPEC` 对第 `1-24` 课做整册质量修订：统一课题注音、修正明显错误的 `ruby`、替换临时占位说明，并补齐练习题的网页学习版保真边界说明。
8. `p0-*`
   按批次精修第 `9-24` 课生词表。
9. `p1-*`
   清洗入门单元和正文高噪声结构。
10. `p2-1`
   收尾 `mock-test-n5.md` 与 `appendix.md`。
11. `vitepress-export`
   把当前结构化稿同步到 `docs/` 目录，供 `VitePress` / `GitHub Pages` 使用；如果 `reader/` 下存在同名页面，会优先使用人类精修稿覆盖。同时会额外生成 `docs/public/ai/...` 下的两层 AI 产物：`view/` 负责浏览器与通用 Web Fetch，`raw/` 保留原始 Markdown 镜像和 `manifest.json`。

## 脚本索引

| 任务 | 脚本 | 说明 |
| --- | --- | --- |
| `extract` | `pdf_to_markdown.py` | 直接从 PDF 提取整本文字层 |
| `pipeline` | `shinbiao_markdown.py` | 初级上册主转换流程 |
| `split` | `split_shinbiao_markdown.py` | 按课拆分 Markdown |
| `normalize` | `normalize_shinbiao_markdown.py` | 做首轮规则化清洗 |
| `review` | `build_shinbiao_review_pages.py` | 生成或更新 `review-pages.md` |
| `reader-pdf-9-24` | `build_shinbiao_reader_from_pdf.py` | 按原 PDF 批量重建第 `9-24` 课 `reader` 草稿 |
| `reader-repair-spec` | `repair_reader_spec_issues.py` | 回填 `reader` 页码锚点与完成度状态，重新对齐 `READER_SPEC` |
| `reader-s3-9-24` | `promote_reader_s3.py` | 把第 `9-24` 课 `reader` 稿统一提升到 `S3` 学习版 |
| `reader-quality-all` | `quality_refine_reader_all.py` | 按 `READER_SPEC` 对第 `1-24` 课做整册质量修订 |
| `vitepress-export` | `export_shinbiao_to_vitepress.py` | 同步初级上册到 `docs/` 目录 |
| `p0-1` ~ `p0-4` | `refine_shinbiao_p0_*.py` | 分批精修第 `9-24` 课生词表 |
| `p1-1` | `refine_shinbiao_p1_1.py` | 重建入门单元高噪声页 |
| `p1-2` | `refine_shinbiao_p1_2.py` | 清洗正文高噪声结构 |
| `p2-1` | `refine_shinbiao_p2_1.py` | 整理 `N5` 模拟题与附录结构 |
| `vocab-batch` | `refine_shinbiao_vocab_batch.py` | 生词表批量精修辅助脚本 |

## 注意事项

- 多数脚本当前仍写死了仓库根路径：`D:\Project\GitHub\nihongo-learning`。
- 生词表精修脚本依赖页图校对；若要重新渲染 PDF 页面，建议保证 `Poppler` 可用。
- `resources/` 默认仍按大目录忽略，但 `resources/新标日/md/structured/初级上册/` 与 `resources/新标日/md/reader/初级上册/` 已显式解除忽略，便于版本化源稿。
- 当前已将 `resources/新标日/md/structured/初级上册/` 与 `resources/新标日/md/reader/初级上册/` 重新纳入版本控制，便于 CI 从源稿重建站点。
- 对 GitHub Pages 来说，当前 workflow 会先运行 `vitepress-export` 再构建；本地预览前如果你更新了源稿，仍建议先手动跑一次 `npm run docs:export`。
- `vitepress-export` 现在会同步三层产物：网页阅读版在 `docs/shinbiao/...`，AI 浏览安全页在 `docs/public/ai/.../<lesson>/index.html`，原始 Markdown 镜像在 `docs/public/ai/.../raw/...`。
- 切换站点壳或怀疑缓存污染时，可以先跑一次 `npm run docs:clean` 再重建。
- 当前站点壳以 `docs/.vitepress/` 为唯一真源，运行时不再保留旧兼容层。
- 当前内容层分为两层：`structured/` 是机器清洗稿，`reader/` 是人类可读覆盖稿。
- `reader/初级上册/READER_SPEC.md` 是当前的修课规范入口，定义了 `M0-M7` 模块和 `S1-S3` 完成等级。
- 当前产物更偏“个人学习 / 检索 / 二次加工版”，不是出版社级排版复刻版。

## 后续建议

1. 如果要长期维护这套 Markdown，建议单独决定是否让 `resources/` 退出 `.gitignore`。
2. 如果要继续提高可读性，优先回看 `01-intro-unit.md` 里的笔顺图、声调图，以及少量 OCR 残留页。
3. 如果后面要进一步利用 `VitePress` 的原生能力，再考虑补专用主题组件、鉴权路由和更细粒度的 AI 数据接口。
