# ClawUtil Blog 技术架构 v3.0

> 现代化全栈博客系统设计方案
> 技术栈：TypeScript + Next.js + Prisma + SQLite

---

## 一、技术选型

### 1.1 核心架构

```
┌─────────────────────────────────────────────────────────────┐
│                      ClawUtil Blog v3                        │
├─────────────────────────────────────────────────────────────┤
│  前端 (Next.js 14 App Router)                                │
│  ├── 📱 博客展示端 (/app/)                                   │
│  │   ├── 首页、文章列表、文章详情                            │
│  │   ├── 工具百科、对比评测                                  │
│  │   └── 里程碑时间线                                        │
│  │                                                           │
│  └── ⚙️ CMS 管理端 (/app/admin/)                             │
│      ├── 文章编辑器 (Markdown + 实时预览)                    │
│      ├── 文章管理 (CRUD)                                     │
│      ├── 分类/标签管理                                       │
│      └── 数据统计                                            │
├─────────────────────────────────────────────────────────────┤
│  API 层 (Next.js API Routes)                                 │
│  ├── /api/articles - 文章 CRUD                               │
│  ├── /api/categories - 分类管理                              │
│  ├── /api/tags - 标签管理                                    │
│  └── /api/auth - 简单认证（可选）                            │
├─────────────────────────────────────────────────────────────┤
│  数据层 (Prisma ORM + SQLite)                                │
│  ├── Article - 文章                                          │
│  ├── Category - 分类                                         │
│  ├── Tag - 标签                                              │
│  └── Milestone - 里程碑                                      │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 技术栈详情

| 层级 | 技术 | 版本 | 用途 |
|------|------|------|------|
| **框架** | Next.js | 14+ | React 全栈框架，App Router |
| **语言** | TypeScript | 5+ | 类型安全 |
| **样式** | Tailwind CSS | 3.4+ | 原子化 CSS |
| **组件** | shadcn/ui | latest | UI 组件库 |
| **ORM** | Prisma | 5+ | 数据库 ORM |
| **数据库** | SQLite | - | 本地文件数据库 |
| **编辑器** | react-markdown + MDEditor | - | Markdown 编辑 |
| **部署** | Vercel / 自有服务器 | - | 静态/动态部署 |

---

## 二、数据库设计

### 2.1 Schema (Prisma)

```prisma
// prisma/schema.prisma

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "sqlite"
  url      = env("DATABASE_URL")
}

// 文章表
model Article {
  id          String   @id @default(uuid())
  slug        String   @unique // URL 友好的标识，如 "claude-code-plan-mode"
  title       String
  summary     String?  // 摘要
  content     String   // Markdown 内容
  htmlContent String?  // 编译后的 HTML（可选，加速渲染）
  
  // 元数据
  type        ArticleType @default(DAILY) // 文章类型
  status      Status      @default(DRAFT) // 发布状态
  
  // 时间
  publishDate DateTime?   // 发布日期
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  
  // 阅读数据
  viewCount   Int @default(0)
  readTime    Int? // 预计阅读时间（分钟）
  
  // 关联
  categoryId  String?
  category    Category? @relation(fields: [categoryId], references: [id])
  tags        Tag[]
  
  // SEO
  coverImage  String? // 封面图 URL
  metaDesc    String? // SEO 描述
  
  @@index([publishDate])
  @@index([status])
  @@index([type])
}

// 分类表（工具百科用）
model Category {
  id          String @id @default(uuid())
  slug        String @unique
  name        String // 如 "OpenClaw"
  description String?
  icon        String? // emoji 或图标 URL
  color       String? // 主题色
  sortOrder   Int @default(0)
  
  articles    Article[]
  
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
}

// 标签表
model Tag {
  id        String @id @default(uuid())
  name      String @unique
  color     String? // 标签颜色
  articles  Article[]
  
  createdAt DateTime @default(now())
}

// 里程碑表
model Milestone {
  id          String @id @default(uuid())
  year        Int
  month       Int?
  day         Int?
  title       String
  description String
  category    MilestoneCategory @default(TECH)
  importance  Int @default(1) // 1-5，重要性
  link        String? // 相关链接
  
  createdAt   DateTime @default(now())
}

enum ArticleType {
  DAILY       // 日更文章
  WIKI        // 工具百科
  COMPARE     // 对比评测
  WORKFLOW    // 工作流
  WEEKLY      // 周报
}

enum Status {
  DRAFT       // 草稿
  PUBLISHED   // 已发布
  ARCHIVED    // 归档
}

enum MilestoneCategory {
  TECH        // 技术突破
  PRODUCT     // 产品发布
  CULTURE     // 文化影响
  RESEARCH    // 研究论文
}
```

---

## 三、项目结构

```
clawutil-blog/
├── 📁 app/                          # Next.js 14 App Router
│   ├── 📄 layout.tsx                # 根布局
│   ├── 📄 page.tsx                  # 博客首页
│   ├── 📄 globals.css               # 全局样式
│   │
│   ├── 📁 (blog)/                   # 博客展示路由组
│   │   ├── 📁 daily/                # 日报模块
│   │   │   ├── 📄 page.tsx          # 日报列表
│   │   │   └── 📁 [slug]/           # 文章详情
│   │   │       └── 📄 page.tsx
│   │   ├── 📁 wiki/                 # 工具百科
│   │   │   ├── 📄 page.tsx          # 工具矩阵
│   │   │   └── 📁 [slug]/           # 工具详情
│   │   │       └── 📄 page.tsx
│   │   ├── 📁 compare/              # 对比评测
│   │   ├── 📁 milestones/           # 里程碑
│   │   └── 📁 tags/                 # 标签聚合
│   │
│   └── 📁 admin/                    # CMS 管理后台
│       ├── 📄 layout.tsx            # 管理端布局
│       ├── 📄 page.tsx              # 管理首页/Dashboard
│       ├── 📁 articles/             # 文章管理
│       │   ├── 📄 page.tsx          # 文章列表
│       │   ├── 📁 new/              # 新建文章
│       │   │   └── 📄 page.tsx
│       │   └── 📁 [id]/             # 编辑文章
│       │       └── 📄 page.tsx
│       ├── 📁 categories/           # 分类管理
│       └── 📁 settings/             # 系统设置
│
├── 📁 components/                   # 组件
│   ├── 📁 ui/                       # shadcn/ui 组件
│   ├── 📁 blog/                     # 博客组件
│   │   ├── ArticleCard.tsx
│   │   ├── ArticleList.tsx
│   │   ├── TagCloud.tsx
│   │   └── WikiCard.tsx
│   ├── 📁 editor/                   # 编辑器组件
│   │   ├── MarkdownEditor.tsx       # Markdown 编辑器
│   │   └── ArticleForm.tsx          # 文章表单
│   └── 📁 admin/                    # 管理端组件
│       ├── AdminNav.tsx
│       ├── DashboardStats.tsx
│       └── DataTable.tsx
│
├── 📁 lib/                          # 工具库
│   ├── 📄 db.ts                     # Prisma 客户端
│   ├── 📄 api.ts                    # API 封装
│   ├── 📄 utils.ts                  # 通用工具
│   └── 📄 markdown.ts               # Markdown 处理
│
├── 📁 prisma/
│   ├── 📄 schema.prisma             # 数据库 schema
│   └── 📁 migrations/               # 数据库迁移
│
├── 📁 types/                        # TypeScript 类型
│   └── 📄 index.ts
│
├── 📁 public/                       # 静态资源
│   ├── 📁 uploads/                  # 上传文件
│   └── 📁 images/
│
├── 📁 scripts/                      # 脚本
│   ├── 📄 seed.ts                   # 初始化数据
│   └── 📄 migrate-md.ts             # 迁移现有 Markdown
│
├── 📄 next.config.js
├── 📄 tailwind.config.ts
├── 📄 tsconfig.json
├── 📄 package.json
└── 📄 .env                          # 环境变量
```

---

## 四、核心功能设计

### 4.1 CMS 文章编辑器

```typescript
// 功能特性：
// 1. 分屏预览：左侧编辑，右侧实时预览
// 2. Markdown 支持：标准语法 + GitHub Flavored Markdown
// 3. 元数据编辑：标题、分类、标签、发布时间、封面图
// 4. 自动保存：本地草稿 + 服务器保存
// 5. 文章模板：快速创建日更/百科/对比文章
// 6. 图片上传：拖拽上传，自动保存到 public/uploads

interface EditorFeatures {
  // 编辑模式
  mode: 'split' | 'edit' | 'preview'
  
  // 工具栏
  toolbar: [
    'heading', 'bold', 'italic', 'quote',
    'link', 'image', 'code', 'table',
    'ul', 'ol', 'todo'
  ]
  
  // 快捷插入
  snippets: {
    '日更模板': dailyTemplate,
    '百科模板': wikiTemplate,
    '对比表格': compareTable,
    '信息框': infoBox,
    '代码块': codeBlock
  }
}
```

### 4.2 API 设计 (RESTful)

```typescript
// 文章 API
GET    /api/articles              // 列表（支持分页、筛选、搜索）
POST   /api/articles              // 创建
GET    /api/articles/[id]         // 详情
PUT    /api/articles/[id]         // 更新
DELETE /api/articles/[id]         // 删除

// 分类 API
GET    /api/categories            // 全部分类
POST   /api/categories            // 创建分类

// 标签 API
GET    /api/tags                  // 热门标签
POST   /api/articles/[id]/tags    // 关联标签

// 文件上传
POST   /api/upload                // 图片上传
```

---

## 五、部署方案

### 5.1 方案 A：Vercel 托管（推荐）

```
优点：
- 自动 CI/CD
- 全球 CDN
- Serverless 函数
- 免费额度充足

限制：
- SQLite 需要特殊处理（使用 Vercel Postgres 或 Neon）
- 文件上传需要 S3 兼容存储

配置：
- 数据库：Vercel Postgres (PostgreSQL) 或 Neon
- 文件存储：Cloudflare R2 / AWS S3
- 部署：GitHub → Vercel 自动部署
```

### 5.2 方案 B：自有服务器

```
适用场景：
- 希望完全控制数据
- 已有服务器资源

配置：
- 服务器：任意 VPS (2C2G 起步)
- 数据库：SQLite (简单) 或 PostgreSQL
- 部署：Docker + Docker Compose
- 反向代理：Nginx / Caddy
```

---

## 六、迁移策略

### 6.1 现有内容迁移

```typescript
// 步骤 1: 提取现有文章元数据
// 从现有 HTML 中提取：
// - 标题
// - 日期
// - 摘要
// - 内容（需要清理 HTML → Markdown）

// 步骤 2: 转换格式
// 使用 turndown 将 HTML 转为 Markdown

// 步骤 3: 导入数据库
// 运行 seed 脚本自动导入
```

### 6.2 渐进式迁移

```
Phase 1: 新系统开发（并行运行）
  └── 现有站点保持不变
  └── 新系统开发 + 内容导入
  
Phase 2: 切换 DNS（可选）
  └── 新系统部署到子域名：beta.zymclaw.github.io
  └── 测试验证
  
Phase 3: 完全切换
  └── 主域名指向新系统
  └── 旧站点作为备份
```

---

## 七、开发计划

### Week 1: 基础架构
- [ ] 初始化 Next.js 项目 + TypeScript
- [ ] 配置 Tailwind + shadcn/ui
- [ ] 设计 Prisma Schema
- [ ] 搭建基础页面结构

### Week 2: CMS 开发
- [ ] 文章 CRUD API
- [ ] Markdown 编辑器
- [ ] 文章管理界面
- [ ] 分类/标签管理

### Week 3: 博客前端
- [ ] 首页设计
- [ ] 文章列表/详情
- [ ] 工具百科
- [ ] 标签系统

### Week 4: 数据迁移 & 部署
- [ ] 迁移现有 4 篇文章
- [ ] 里程碑数据导入
- [ ] Vercel 部署配置
- [ ] 域名切换

---

## 八、技术亮点

1. **TypeScript 全栈**：前后端统一类型安全
2. **App Router**：Next.js 14 最新特性，支持 SSR/SSG/ISR
3. **自研 CMS**：定制化编辑器，完美适配个人工作流
4. **数据库优先**：Prisma ORM，类型安全的数据库操作
5. **现代化 UI**：shadcn/ui + Tailwind，快速构建美观界面
6. **内容模板**：支持日更/百科/对比多种文章模板
