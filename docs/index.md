# Nihongo Learning

这是一个先在 `GitHub Pages` 上落地、后续可直接迁移到自有服务器的日语学习站点实验版。

当前策略很明确：

- `docs/` 放可发布、可跟踪的人类阅读版内容
- `resources/` 继续保留本地精修产物和中间层
- `VitePress` 负责阅读体验、导航和全文搜索
- 导出链路与构建链路都以 `VitePress` 为唯一站点壳，不再保留旧兼容层
- 后续如果迁移到轻量云服务器，只需要继续 `npm run docs:build` 并托管静态产物

## 当前入口

- [AI 接口](ai/index.md)
- [新标日总览](shinbiao/index.md)
- [初级上册总览](shinbiao/elementary-book-1/index.md)

## 现在这版的定位

- 目标是“可随时阅读、可继续迭代”的教材站点
- 不是像素级复刻纸书
- 优先保留学习价值、阅读连续性和可搜索性
- 同时保留一条给 AI / 脚本直读的原文 Markdown 镜像出口
