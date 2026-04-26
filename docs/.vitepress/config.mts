import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Nihongo Learning',
  description: '新标日学习站点实验版',
  lang: 'zh-CN',
  base: '/nihongo-learning/',
  lastUpdated: true,
  cleanUrls: true,
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '新标日', link: '/shinbiao/' },
      { text: '初级上册', link: '/shinbiao/elementary-book-1/' }
    ],
    search: {
      provider: 'local'
    },
    outline: {
      level: [2, 3],
      label: '本页目录'
    },
    docFooter: {
      prev: '上一页',
      next: '下一页'
    },
    sidebarMenuLabel: '页面导航',
    returnToTopLabel: '回到顶部',
    darkModeSwitchLabel: '外观',
    lightModeSwitchTitle: '切换到浅色模式',
    darkModeSwitchTitle: '切换到深色模式',
    sidebar: {
      '/shinbiao/': [
        {
          text: '新标日',
          items: [
            { text: '总览', link: '/shinbiao/' },
            { text: '初级上册', link: '/shinbiao/elementary-book-1/' }
          ]
        }
      ],
      '/shinbiao/elementary-book-1/': [
        {
          text: '入门与前置',
          collapsed: false,
          items: [
            { text: '总览', link: '/shinbiao/elementary-book-1/' },
            { text: '前置资料', link: '/shinbiao/elementary-book-1/00-frontmatter' },
            { text: '入门单元', link: '/shinbiao/elementary-book-1/01-intro-unit' }
          ]
        },
        {
          text: '第 1 单元',
          collapsed: true,
          items: [
            { text: '单元概览', link: '/shinbiao/elementary-book-1/unit-01-overview' },
            { text: '第 1 课', link: '/shinbiao/elementary-book-1/lesson-01' },
            { text: '第 2 课', link: '/shinbiao/elementary-book-1/lesson-02' },
            { text: '第 3 课', link: '/shinbiao/elementary-book-1/lesson-03' },
            { text: '第 4 课', link: '/shinbiao/elementary-book-1/lesson-04' }
          ]
        },
        {
          text: '第 2 单元',
          collapsed: true,
          items: [
            { text: '单元概览', link: '/shinbiao/elementary-book-1/unit-02-overview' },
            { text: '第 5 课', link: '/shinbiao/elementary-book-1/lesson-05' },
            { text: '第 6 课', link: '/shinbiao/elementary-book-1/lesson-06' },
            { text: '第 7 课', link: '/shinbiao/elementary-book-1/lesson-07' },
            { text: '第 8 课', link: '/shinbiao/elementary-book-1/lesson-08' }
          ]
        },
        {
          text: '第 3 单元',
          collapsed: true,
          items: [
            { text: '单元概览', link: '/shinbiao/elementary-book-1/unit-03-overview' },
            { text: '第 9 课', link: '/shinbiao/elementary-book-1/lesson-09' },
            { text: '第 10 课', link: '/shinbiao/elementary-book-1/lesson-10' },
            { text: '第 11 课', link: '/shinbiao/elementary-book-1/lesson-11' },
            { text: '第 12 课', link: '/shinbiao/elementary-book-1/lesson-12' }
          ]
        },
        {
          text: '第 4 单元',
          collapsed: true,
          items: [
            { text: '单元概览', link: '/shinbiao/elementary-book-1/unit-04-overview' },
            { text: '第 13 课', link: '/shinbiao/elementary-book-1/lesson-13' },
            { text: '第 14 课', link: '/shinbiao/elementary-book-1/lesson-14' },
            { text: '第 15 课', link: '/shinbiao/elementary-book-1/lesson-15' },
            { text: '第 16 课', link: '/shinbiao/elementary-book-1/lesson-16' }
          ]
        },
        {
          text: '第 5 单元',
          collapsed: true,
          items: [
            { text: '单元概览', link: '/shinbiao/elementary-book-1/unit-05-overview' },
            { text: '第 17 课', link: '/shinbiao/elementary-book-1/lesson-17' },
            { text: '第 18 课', link: '/shinbiao/elementary-book-1/lesson-18' },
            { text: '第 19 课', link: '/shinbiao/elementary-book-1/lesson-19' },
            { text: '第 20 课', link: '/shinbiao/elementary-book-1/lesson-20' }
          ]
        },
        {
          text: '第 6 单元',
          collapsed: true,
          items: [
            { text: '单元概览', link: '/shinbiao/elementary-book-1/unit-06-overview' },
            { text: '第 21 课', link: '/shinbiao/elementary-book-1/lesson-21' },
            { text: '第 22 课', link: '/shinbiao/elementary-book-1/lesson-22' },
            { text: '第 23 课', link: '/shinbiao/elementary-book-1/lesson-23' },
            { text: '第 24 课', link: '/shinbiao/elementary-book-1/lesson-24' }
          ]
        },
        {
          text: '附加内容',
          collapsed: true,
          items: [
            { text: 'N5 模拟题', link: '/shinbiao/elementary-book-1/mock-test-n5' },
            { text: '附录', link: '/shinbiao/elementary-book-1/appendix' }
          ]
        }
      ]
    }
  }
})
