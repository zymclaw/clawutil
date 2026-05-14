# ClawUtil Blog 设计规划 V3（最终版）

> 现代化全栈博客系统 + Arco Design 企业级设计体系
> 创建日期：2026-03-09
> 版本：v3.0
> 状态：已确认，待开发

---

## 📋 项目背景与目标

### 背景
- **已有内容**：4 篇文章 + 1 个 Skill + AI 里程碑时间线
- **现有地址**：https://zymclaw.github.io/clawutil/
- **核心问题**：内容分散、缺乏 CMS、扩展性受限

### 目标
建立一个**现代化的个人 AI 技术博客**，支持：
- 📰 **日更文章**：系统化的内容生产工作流
- 📖 **工具百科**：AI 工具的知识沉淀
- 🆚 **对比评测**：多工具横向对比
- 🎙️ **播客栏目**（后期）
- ✍️ **CMS 后台**：Markdown 编辑器 + 文章管理

---

## 🎯 核心定位

### Slogan
> **「探索 AI 工具的每一天」**
> 个人 AI 工具探索的「日报 + 知识库 + 实验记录」

### 内容范围
| 类别 | 覆盖内容 |
|------|----------|
| AI 大模型 | Claude Code、Gemini、DeepSeek、Kimi、MiniMax、StepFun、豆包、Seedance |
| Agent 框架 | OpenClaw、nanoClaw、Skill 系统等 |
| 内容形态 | 技术文章 + 播客（后期） |

### 更新频率
- **目标**：日更
- **投入**：每天 3 小时

---

## 🏗️ 技术架构

### 技术栈

```
┌─────────────────────────────────────────────────────────────┐
│  前端展示层          Next.js 14 (App Router)               │
│  UI 组件库           @arco-design/web-react (字节出品)      │
│  样式方案            Tailwind CSS + Arco Design Token       │
├─────────────────────────────────────────────────────────────┤
│  CMS 管理后台        Next.js Route Groups (/admin)         │
│  编辑器              @uiw/react-md-editor (分屏预览)        │
├─────────────────────────────────────────────────────────────┤
│  API 层              Next.js Route Handlers                │
├─────────────────────────────────────────────────────────────┤
│  数据层              Prisma ORM + SQLite (开发)             │
│  文件存储            本地 → Vercel Blob (生产)              │
├─────────────────────────────────────────────────────────────┤
│  部署                Vercel (Serverless)                   │
└─────────────────────────────────────────────────────────────┘
```

### 详细依赖

```json
{
  "核心框架": {
    "next": "^14.x",
    "react": "^18.x",
    "typescript": "^5.x"
  },
  "UI 组件": {
    "@arco-design/web-react": "^2.x",
    "@arco-design/theme-line": "latest",
    "tailwindcss": "^3.4.x"
  },
  "编辑器": {
    "@uiw/react-md-editor": "^4.x",
    "react-markdown": "^9.x"
  },
  "数据": {
    "prisma": "^5.x",
    "@prisma/client": "^5.x"
  },
  "工具": {
    "zustand": "^4.x (状态管理)",
    "dayjs": "^1.x (日期)",
    "react-hot-toast": "^2.x (反馈)"
  }
}
```

---

## 🗄️ 数据库设计

### Prisma Schema

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "sqlite"
  url      = env("DATABASE_URL")
}

// 文章表
model Article {
  id          String      @id @default(uuid())
  slug        String      @unique
  title       String
  summary     String?
  content     String      // Markdown
  htmlContent String?     // 编译后 HTML
  
  type        ArticleType @default(DAILY)
  status      Status      @default(DRAFT)
  
  publishDate DateTime?
  createdAt   DateTime    @default(now())
  updatedAt   DateTime    @updatedAt
  
  viewCount   Int         @default(0)
  readTime    Int?
  
  categoryId  String?
  category    Category?   @relation(fields: [categoryId], references: [id])
  tags        Tag[]
  
  coverImage  String?
  metaDesc    String?
  
  @@index([publishDate])
  @@index([status])
  @@index([type])
}

// 分类表
model Category {
  id          String    @id @default(uuid())
  slug        String    @unique
  name        String
  description String?
  icon        String?   // emoji
  color       String?   // 主题色
  sortOrder   Int       @default(0)
  
  articles    Article[]
  
  createdAt   DateTime  @default(now())
  updatedAt   DateTime  @updatedAt
}

// 标签表
model Tag {
  id        String    @id @default(uuid())
  name      String    @unique
  color     String?
  articles  Article[]
  
  createdAt DateTime  @default(now())
}

// 里程碑表
model Milestone {
  id          String            @id @default(uuid())
  year        Int
  month       Int?
  day         Int?
  title       String
  description String
  category    MilestoneCategory @default(TECH)
  importance  Int               @default(1)
  link        String?
  
  createdAt   DateTime          @default(now())
}

enum ArticleType {
  DAILY       // 日更文章
  WIKI        // 工具百科
  COMPARE     // 对比评测
  WORKFLOW    // 工作流
  WEEKLY      // 周报
}

enum Status {
  DRAFT
  PUBLISHED
  ARCHIVED
}

enum MilestoneCategory {
  TECH
  PRODUCT
  CULTURE
  RESEARCH
}
```

---

## 📁 项目结构

```
clawutil-v4/
├── 📁 app/                              # Next.js 14 App Router
│   ├── 📄 layout.tsx                    # 根布局 + Arco Provider
│   ├── 📄 page.tsx                      # 首页
│   ├── 📄 globals.css                   # 全局样式
│   │
│   ├── 📁 (blog)/                       # 博客展示路由组
│   │   ├── 📁 daily/
│   │   │   ├── 📄 page.tsx              # 日报列表
│   │   │   └── 📁 [slug]/
│   │   │       └── 📄 page.tsx          # 文章详情
│   │   ├── 📁 wiki/
│   │   │   ├── 📄 page.tsx              # 工具矩阵
│   │   │   └── 📁 [slug]/
│   │   │       └── 📄 page.tsx          # 工具详情
│   │   ├── 📁 compare/
│   │   └── 📁 milestones/
│   │
│   └── 📁 admin/                        # CMS 管理后台
│       ├── 📄 layout.tsx                # 后台布局（左侧导航）
│       ├── 📄 page.tsx                  # Dashboard
│       ├── 📁 articles/
│       │   ├── 📄 page.tsx              # 文章列表
│       │   ├── 📁 new/
│       │   │   └── 📄 page.tsx          # 新建文章
│       │   └── 📁 [id]/
│       │       └── 📄 page.tsx          # 编辑文章
│       ├── 📁 categories/
│       └── 📁 settings/
│
├── 📁 components/
│   ├── 📁 arco/                         # Arco 风格组件
│   │   ├── ArticleCard.tsx
│   │   ├── ArticleList.tsx
│   │   ├── TagCloud.tsx
│   │   └── WikiCard.tsx
│   ├── 📁 editor/                       # 编辑器组件
│   │   ├── MarkdownEditor.tsx
│   │   ├── ArticleForm.tsx
│   │   └── SplitPreview.tsx
│   └── 📁 blog/
│       └── ...
│
├── 📁 lib/
│   ├── 📄 arco-theme.ts                 # Arco 主题配置
│   ├── 📄 db.ts                         # Prisma client
│   └── 📄 utils.ts
│
├── 📁 styles/
│   ├── 📄 globals.css
│   └── 📄 arco-override.css
│
├── 📁 prisma/
│   ├── 📄 schema.prisma
│   └── 📁 migrations/
│
├── 📁 types/
│   └── 📄 index.ts
│
├── 📁 scripts/
│   ├── 📄 seed.ts                       # 初始化数据
│   └── 📄 migrate-from-v2.ts            # 迁移旧文章
│
└── 📄 next.config.js
```

---

## 🎨 设计系统（Arco Design 风格）

### 色彩系统

```typescript
// lib/arco-theme.ts

// 主色：科技蓝 (Arco Blue)
export const colors = {
  primary: {
    1: '#E8F3FF',
    2: '#BEDAFF',
    3: '#94BFFF',
    4: '#6AA1FF',
    5: '#4080FF',  // hover
    6: '#165DFF',  // 主色
    7: '#0E42D2',  // active
    8: '#072CA6',
    9: '#031A79',
    10: '#000D4D',
  },
  
  // 功能色
  success: '#00B42A',   // 绿
  warning: '#FF7D00',   // 橙
  danger: '#F53F3F',    // 红
  
  // 中性色
  gray: {
    1: '#F7F8FA',   // 背景
    2: '#F2F3F5',
    3: '#E5E6EB',   // 边框
    4: '#C9CDD4',
    5: '#A9AEB8',   // 次要文字
    6: '#86909C',
    7: '#6B7785',
    8: '#4E5969',   // 正文
    9: '#272E3B',
    10: '#1D2129',  // 标题/暗黑背景
  }
};

// 内容类型色
export const typeColors = {
  daily: { light: '#E8F3FF', main: '#165DFF', text: '#165DFF' },    // 蓝
  wiki: { light: '#E8FFEA', main: '#00B42A', text: '#00B42A' },     // 绿
  compare: { light: '#FFF7E8', main: '#FF7D00', text: '#FF7D00' },  // 橙
  workflow: { light: '#F5E8FF', main: '#722ED1', text: '#722ED1' }, // 紫
  weekly: { light: '#FFE8F1', main: '#F5319D', text: '#F5319D' },   // 粉
};
```

### 字体规范

```typescript
export const typography = {
  sizes: {
    h1: '36px',      // 页面大标题
    h2: '28px',      // 区块标题
    h3: '20px',      // 卡片标题
    body: '14px',    // 正文（主字号）
    small: '12px',   // 辅助文字
  },
  lineHeight: 1.4,
  lineHeightLoose: 1.6,  // 文章正文
  weight: {
    light: 300,
    regular: 400,
    medium: 500,
    semibold: 600,
  }
};
```

### 阴影层级

```typescript
export const shadows = {
  1: '0 2px 5px rgba(0, 0, 0, 0.08)',   // 卡片默认
  2: '0 4px 10px rgba(0, 0, 0, 0.1)',   // 卡片hover
  3: '0 8px 20px rgba(0, 0, 0, 0.12)',  // 下拉菜单
  4: '0 12px 30px rgba(0, 0, 0, 0.16)', // 模态框
};
```

### 圆角

```typescript
export const borderRadius = {
  small: '2px',     // 标签
  medium: '4px',    // 按钮、输入框
  large: '8px',     // 卡片
  xlarge: '12px',   // 大卡片
};
```

---

## 📰 内容生产体系

### 周内容日历

| 星期 | 主题 | 内容类型 | 预计耗时 | 产出 |
|------|------|----------|----------|------|
| **周一** | 🔧 工具深潜 | DAILY | 3h | 1 篇深度文章 (1500-2000字) |
| **周二** | ⚡ 实战速记 | DAILY | 1.5h | 1 篇短文/速查 (500-800字) |
| **周三** | 🆚 对比评测 | COMPARE | 3h | 1 篇对比文章 + 表格 |
| **周四** | 🔗 工作流组合 | WORKFLOW | 2.5h | 1 个工作流指南 |
| **周五** | 📰 周报汇总 | WEEKLY | 2h | 1 期 Newsletter |
| **周六** | 📝 知识整理 | WIKI | 2h | 更新工具百科页 |
| **周日** | 🎯 规划 | - | 1h | 下周选题规划 |

### 每日 3 小时分配

```
Hour 1: 探索与实验
  └── 实际使用工具，解决问题，记录过程
  └── 截图、录屏、记笔记

Hour 2: 内容创作
  └── 用 OpenClaw 辅助整理思路
  └── 在 CMS 中撰写文章

Hour 3: 打磨与发布
  └── 排版、配图、标签设置
  └── 发布到主站
  └── (可选) 分发到其他平台
```

---

## 🛠️ CMS 功能设计

### 文章编辑器

```typescript
interface EditorFeatures {
  // 编辑模式
  mode: 'split' | 'edit' | 'preview';
  
  // 分屏预览
  splitView: {
    left: 'markdown',   // 左侧编辑
    right: 'preview',   // 右侧实时预览
  };
  
  // 工具栏
  toolbar: [
    'heading',
    'bold', 'italic', 'strikethrough',
    'quote', 'code', 'codeBlock',
    'link', 'image', 'table',
    'ul', 'ol', 'checkbox'
  ];
  
  // 快捷插入模板
  templates: {
    '日更模板': dailyTemplate,
    '百科模板': wikiTemplate,
    '对比表格': compareTableTemplate,
    '信息框': infoBoxTemplate,
  };
  
  // 自动保存
  autoSave: {
    enabled: true,
    interval: 30000,  // 30秒
  };
}
```

### 元数据编辑

```typescript
interface ArticleMeta {
  title: string;           // 文章标题
  slug: string;            // URL 标识
  summary: string;         // 摘要（自动生成或手动编辑）
  type: ArticleType;       // 文章类型
  category: Category;      // 所属分类
  tags: Tag[];             // 标签
  coverImage?: string;     // 封面图
  publishDate?: Date;      // 发布时间
  status: Status;          // 发布状态
}
```

---

## 🚀 开发路线图

### Week 1: 基础架构（3.10-3.16）
- [ ] 初始化 Next.js + TypeScript 项目
- [ ] 安装配置 Arco Design + Tailwind
- [ ] 设计 Prisma Schema
- [ ] 初始化数据库
- [ ] 搭建基础布局组件

### Week 2: CMS 开发（3.17-3.23）
- [ ] Dashboard 页面（统计卡片）
- [ ] 文章列表（Arco Table + 分页）
- [ ] Markdown 分屏编辑器
- [ ] 文章 CRUD API
- [ ] 自动保存功能

### Week 3: 博客前端（3.24-3.30）
- [ ] 首页设计（Hero + 卡片 + 标签云）
- [ ] 日报列表/详情页
- [ ] 工具百科矩阵页
- [ ] 标签系统
- [ ] 暗黑模式支持

### Week 4: 数据迁移 & 部署（3.31-4.6）
- [ ] 迁移现有 4 篇文章
- [ ] 里程碑数据导入
- [ ] 移动端适配
- [ ] Vercel 部署配置
- [ ] 域名切换

---

## 📊 多平台分发策略

### 平台优先级

```
Phase 1 (第1月): 专注建设主站，积累 20+ 篇内容
    ↓
Phase 2 (第2月): 开通微信公众号，同步主站内容
    ↓
Phase 3 (第3月): 加入小红书（图文版）
    ↓
Phase 4 (第4月+): 知乎、CSDN、播客
```

### 平台适配

| 平台 | 内容特点 | 适配方式 |
|------|----------|----------|
| 微信公众号 | 长文、可排版 | 直接发布，优化头图 |
| 小红书 | 短图文、重点突出 | 提取 3-5 个要点，做图文卡片 |
| CSDN | 技术代码、SEO | 保持原样，优化标题关键词 |
| 知乎 | 问答形式 | 改编成"如何评价 XXX" |

---

## 🔐 待确认决策

### 已确认 ✅
- [x] 技术栈：Next.js + TypeScript + Arco Design
- [x] 数据库：SQLite（开发）→ PostgreSQL（生产）
- [x] 部署：Vercel
- [x] 首月聚焦工具：OpenClaw + Claude Code + Kimi CLI
- [x] 内容类型：日报 + 百科 + 对比

### 待决策 ❓
- [ ] 是否保留现有里程碑页面的独立 React 实现？
- [ ] 是否需要简单的认证（如密码保护 CMS）？
- [ ] 图片存储：本地 → Vercel Blob / Cloudflare R2？
- [ ] 是否添加评论系统（Giscus）？
- [ ] 是否需要访问统计（Vercel Analytics）？

---

## 📚 参考资源

### 设计参考
- Arco Design：https://arco.design
- Arco React 组件：https://arco.design/react/components
- Arco 色彩系统：https://arco.design/react/docs/palette

### 技术参考
- Next.js 14：https://nextjs.org/docs
- Prisma：https://www.prisma.io/docs
- MD Editor：https://github.com/uiwjs/react-md-editor

### 现有资源
- 当前站点：https://zymclaw.github.io/clawutil/
- GitHub 仓库：https://github.com/zymclaw/clawutil
- 现有文章：4 篇（待迁移）

---

## 📝 变更日志

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v1.0 | 2026-03-08 | 初始设计方案（纯 HTML） |
| v2.0 | 2026-03-08 | 优化内容结构和周计划 |
| v3.0 | 2026-03-09 | 升级为 Next.js + TypeScript + Arco Design 全栈方案 |

---

## 💾 文档存储位置

- 本文件：`/git-repos/clawutil/DESIGN-PLAN-v3-final.md`
- 历史版本：`/git-repos/clawutil/DESIGN-PLAN.md` (v2)
- 记忆系统：`/git-repos/clawutil/.kimi/memory.json` (待创建)
