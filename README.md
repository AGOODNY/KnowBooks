# KnowBooks — 书籍推荐系统

  一个基于 React 和 Vite 的全栈书籍推荐 Web 应用。

  ## 技术栈

  - **前端**：React 18、React Router v6、Vite
  - **样式**：纯 CSS、Poppins + Lora + Inter 字体
  - **状态管理**：React Hooks（useState、useMemo、usePagination）


  ## 功能概览

  ### 用户端页面

  | 页面 | 路由 | 状态 |
  |------|------|------|
  | 营销首页 | `/` | 已完成 |
  | 仪表盘 | `/home` | 已完成 |
  | 搜索与筛选 | `/search` | 已完成 |
  | 书籍详情 | `/book/:id` | 占位 |
  | 上传书籍 | `/upload` | 占位 |
  | 个人中心 | `/profile` | 占位 |
  | 管理后台 | `/admin` | 占位 |
  | 更多推荐 | `/recommend` | 占位 |

  ### 核心模块

  - **智能推荐** — 三种推荐策略切换（为你推荐 / 热门 / 最新）
  - **标签云** — 可点击tag标签，支持分类浏览
  - **搜索与筛选** — 关键词搜索 + 标签/作者/评分筛选 + 分页
  - **书籍卡片** — 可复用卡片组件，三种尺寸（默认 / 小型 / 紧凑型）
  - **响应式布局** — 适配桌面端，支持移动端断点

  ## 本地启动

  ### 环境要求

  - Node.js **18+**
  - npm **9+**

  ### 安装与运行

  ```bash
  # 克隆仓库
  git clone https://github.com/mushroomAAA/Knowbooks.git
  cd Knowbooks

  # 安装依赖
  npm install

  # 启动开发服务器
  npm run dev

  浏览器访问 http://localhost:5173。
  ```

  ### 生产构建
  ```bash
  npm run build
  npm run preview
  ```

  ### 项目结构
  ```bash
  Knowbooks/
  ├── index.html                 # 入口 HTML（引入 Google Fonts）
  ├── package.json
  ├── vite.config.js
  ├── src/
  │   ├── main.jsx               # React 入口 + BrowserRouter
  │   ├── App.jsx                # 路由定义（8 条路由）
  │   ├── styles/
  │   │   └── global.css         # CSS 变量、品牌色彩、全局重置
  │   ├── data/
  │   │   └── mockData.js        # 模拟数据（20 本书、10 个标签）
  │   ├── hooks/
  │   │   └── usePagination.js   # 异步分页钩子（async/await）
  │   ├── components/
  │   │   ├── Navbar.jsx/css     # 全局导航栏
  │   │   ├── SearchBar.jsx/css  # 搜索输入框
  │   │   ├── BookCard.jsx/css   # 书籍卡片（3 种尺寸）
  │   │   ├── TagCloud.jsx/css   # 标签云
  │   │   └── Placeholder.jsx/css # 占位页面
  │   └── pages/
  │       ├── Landing.jsx/css    # 营销首页
  │       ├── Home.jsx/css       # 用户仪表盘
  │       ├── Search.jsx/css     # 搜索结果 + 筛选
  │       ├── BookDetail.jsx     # 占位
  │       ├── Upload.jsx         # 占位
  │       ├── Profile.jsx        # 占位
  │       ├── Admin.jsx          # 占位
  │       └── Recommend.jsx      # 占位
  ```

  ### 模拟数据约定
  ```bash
  开发阶段统一使用以下命名规则：

  ┌──────┬──────────────────┬─────────────────────┐
  │ 类型 │       格式       │        示例         │
  ├──────┼──────────────────┼─────────────────────┤
  │ 书名 │ book_exampleX    │ book_example1       │
  ├──────┼──────────────────┼─────────────────────┤
  │ 作者 │ author_exampleX  │ author_example3     │
  ├──────┼──────────────────┼─────────────────────┤
  │ 简介 │ text_exampleX    │ text_example7       │
  ├──────┼──────────────────┼─────────────────────┤
  │ 标签 │ tag_exampleX     │ tag_example4        │
  ├──────┼──────────────────┼─────────────────────┤
  │ 封面 │ 无（灰色占位图） │ 显示 "Not uploaded" │
  └──────┴──────────────────┴─────────────────────┘

  点赞数、评分、收藏数均为随机生成。
  ```
  

  ### 配色
  ```bash
  ┌───────────────────────┬─────────┬────────────────────────┐
  │         变量          │  色值   │          用途          │
  ├───────────────────────┼─────────┼────────────────────────┤
  │ --color-dark          │ #2d2c28 │ 正文文字               │
  ├───────────────────────┼─────────┼────────────────────────┤
  │ --color-light         │ #fefdfb │ 页面背景               │
  ├───────────────────────┼─────────┼────────────────────────┤
  │ --color-bg-secondary  │ #fcfaf5 │ 区块背景               │
  ├───────────────────────┼─────────┼────────────────────────┤
  │ --color-mid-gray      │ #8c8982 │ 次要文字               │
  ├───────────────────────┼─────────┼────────────────────────┤
  │ --color-light-gray    │ #e8e4db │ 边框、分隔线           │
  ├───────────────────────┼─────────┼────────────────────────┤
  │ --color-accent-orange │ #d9704a │ 主强调色（按钮、高亮） │
  └───────────────────────┴─────────┴────────────────────────┘
  ```

  ### 字体
  ```bash
  - 标题：Poppins（字重 600–800）
  - 正文：Lora（字重 400–500）
  - UI 元素：Inter（字重 400–600）
  ```
  ### API 对接说明
  
  usePagination 钩子已预留后端对接接口：
  ```bash
  // 当前（模拟数据）:
  const fetchFn = (pageNum, pageSize) => {
    const items = filteredBooks.slice(start, start + pageSize)
    return { items, total: filteredBooks.length }
  }

  // 未来（真实 API）:
  const fetchFn = async (pageNum, pageSize) => {
    const res = await fetch(`/api/books?page=${pageNum}&size=${pageSize}&...`)
    return res.json()
  }
  ```
