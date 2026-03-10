# ClawUtil 博客设计方案

> 设计日期：2026-03-08
> 状态：待继续完善
> 明日继续点：确认内容深度、首月聚焦工具、平台优先级

---

## 一、核心定位

**从**：OpenClaw 工具分享  
**升级为**：「AI 工具全栈实验室」

**Slogan**：个人 AI 工具探索的「日报 + 知识库 + 实验记录」

**目标**：
- 日更（每天投入 3 小时）
- 覆盖国内外主流 AI 工具（OpenClaw、Claude Code、Kimi、DeepSeek、Gemini、MiniMax、StepFun、豆包、Seedance 等）
- 后期加入播客栏目
- 多平台分发（微信、小红书、CSDN、知乎），最终变现流量
- 技术栈：纯 HTML + Tailwind CSS（GitHub Pages）
- 品牌：保留 ClawUtil

---

## 二、网站架构（纯 HTML 版）

```
clawutil/
├── index.html                    # 首页：今日更新 + 热点工具 + 最新播客
├── about.html                    # 关于：个人介绍 + 时间线 + 联系方式
│
├── 📁 daily/                     # 【核心】日更内容（按日期）
│   ├── 2026/
│   │   ├── 03/
│   │   │   ├── 2026-03-08.html   # 今日探索
│   │   │   └── ...
│   │   └── 04/
│   └── index.html                # 日报归档页
│
├── 📁 tools/                     # 【知识库】工具百科（按工具分类）
│   ├── index.html                # 工具导航页（矩阵对比）
│   ├── openclaw/
│   │   ├── index.html            # OpenClaw 总览
│   │   ├── setup.html            # 部署指南
│   │   ├── skills.html           # Skill 开发
│   │   └── troubleshooting.html  # 故障排查
│   ├── claude-code/
│   ├── kimi-cli/
│   ├── deepseek/
│   ├── gemini/
│   ├── minimax/
│   ├── stepfun/
│   ├── doubao/
│   ├── seedance/
│   └── frameworks/               # Agent 框架
│       ├── nanoclaw.html
│       └── skill-system.html
│
├── 📁 compare/                   # 【对比评测】多工具横向对比
│   ├── coding-assistants.html    # 代码助手对比
│   ├── image-generation.html     # 生图工具对比
│   └── video-generation.html     # 视频工具对比
│
├── 📁 workflows/                 # 【实战】工作流组合方案
│   ├── index.html
│   ├── openclaw-kimi.html
│   └── claude-cursor.html
│
├── 📁 podcast/                   # 【播客】（后期）
│   ├── index.html
│   ├── 2026-03-08-ep01.html
│   └── feed.xml
│
├── 📁 assets/
│   ├── css/
│   ├── js/
│   └── images/
│
└── 📁 _templates/                # 【辅助】HTML 模板
    ├── daily-template.html
    ├── tool-template.html
    └── podcast-template.html
```

### 标签体系（双标签）
- **工具标签**：`claude-code`, `kimi`, `openclaw`, `seedance`...
- **类型标签**：`tutorial`, `troubleshoot`, `compare`, `news`, `workflow`

---

## 三、日更内容规划

### 周内容日历

| 星期 | 主题 | 内容形式 | 预计耗时 | 产出 |
|------|------|---------|---------|------|
| **周一** | 🔧 工具深潜 | 深度体验一个新功能/工具 | 3h | 1 篇深度文章 (1500-2000字) |
| **周二** | ⚡ 实战速记 | 记录当天解决问题的过程 | 1.5h | 1 篇短文/速查 (500-800字) |
| **周三** | 🆚 对比评测 | 两个工具对比测试 | 3h | 1 篇对比文章 + 对比表格 |
| **周四** | 🔗 工作流组合 | 多个工具组合使用方案 | 2.5h | 1 个工作流指南 |
| **周五** | 📰 周报汇总 | 本周AI圈新闻+个人收获 | 2h | 1 期 Newsletter |
| **周六** | 🎙️ 播客录制 | （后期）录制+剪辑 | 3h | 1 期播客 |
| **周日** | 📝 知识整理 | 整理本周内容进 Wiki | 2h | 更新工具百科页 |

### 每日 3 小时分配

```
Hour 1: 探索与实验
  └── 实际使用工具，解决问题，记录过程
  └── 截图、录屏、记笔记

Hour 2: 内容创作
  └── 用 OpenClaw 辅助整理思路
  └── 撰写文章初稿（Markdown/HTML）

Hour 3: 打磨与分发
  └── 排版、配图、代码高亮
  └── 发布到主站
  └── （可选）改编分发到其他平台
```

### 效率技巧

1. **模板化**：每种内容类型有固定模板，直接填空
2. **OpenClaw 辅助**：
   - 用 `/skill:blog-assistant` 生成文章大纲
   - 用 AI 把口语化记录整理成文章
3. **素材积累**：平时用 OpenClaw 的 memory 随时记录，写的时候直接调用
4. **批量处理**：一次拍摄/制作多天的配图

---

## 四、多平台分发策略

### 平台适配矩阵

| 平台 | 内容特点 | ClawUtil 原文适配方式 |
|------|---------|---------------------|
| **微信公众号** | 长文、可排版、封面图重要 | 直接发，优化头图和摘要 |
| **小红书** | 短图文、表情、重点突出 | 提取 3-5 个要点，做成图文卡片 |
| **CSDN** | 技术代码、SEO友好 | 保持原样，优化标题关键词 |
| **知乎** | 问答形式、深度分析 | 改编成"如何评价/使用 XXX" |
| **Twitter/X** | 短文本、线程(thread) | 提取核心观点，做成 thread |

### 分发工作流

```
ClawUtil 主站（GitHub Pages）
        │
        ├── 长文 → 微信公众号 / CSDN / 知乎（全文）
        │
        ├── 要点提取 → 小红书图文（3-5页）
        │
        └── 核心观点 → Twitter Thread / 知乎回答
```

---

## 五、播客规划（后期）

**栏目名**：「ClawUtil Radio」或「AI 工具漫谈」

| 栏目 | 说明 | 时长 | 频率 |
|------|------|------|------|
| **周一速览** | 回顾本周探索的工具亮点 | 10-15min | 每周一 |
| **深度对谈** | 与开发者/重度用户对话 | 30-45min | 每月 2 期 |
| **新手导航** | 针对特定工具的入门指南 | 20min | 按需 |

**技术方案**：
- 托管：Anchor.fm / 小宇宙（免费）
- 嵌入：用 `<iframe>` 嵌入到网站
- RSS：手动维护 `podcast/feed.xml`

---

## 六、纯 HTML 技术优化

### 模板系统

创建基础模板，每次复制填空：

- `_templates/daily-template.html` - 日更文章模板
- `_templates/tool-template.html` - 工具百科模板
- `_templates/podcast-template.html` - 播客页面模板

### OpenClaw Skill 建议

```bash
# 快速创建日报
/skill:new-daily "2026-03-09" "claude-code" "Claude Code 的 Plan 模式体验"

# 生成多平台版本
/skill:cross-platform "文章路径" "小红书|知乎|公众号"
```

### GitHub Actions 自动化

- 自动生成文章列表
- 自动生成 RSS
- 自动部署

---

## 七、内容矩阵示例（未来一周）

| 日期 | 主题 | 标题示例 | 平台分发 |
|------|------|---------|---------|
| Mon | 工具深潜 | 《Claude Code Plan 模式深度体验：比Cursor更适合规划？》 | 全文→公众号/CSDN/知乎 |
| Tue | 实战速记 | 《Kimi CLI 的 `/flow` 命令速查》 | 小红书图文+知乎想法 |
| Wed | 对比评测 | 《Claude Code vs Kimi CLI：代码场景谁更强？》 | 对比表→小红书+全文→公众号 |
| Thu | 工作流 | 《我的 OpenClaw + Kimi 双AI工作流》 | 图文→小红书+长文→公众号 |
| Fri | 周报 | 《AI工具周报#1：Claude Plan模式、Seedance 2.0、Kimi WebUI》 | Newsletter→全平台 |
| Sat | 播客 | （首期筹备） | - |
| Sun | 整理 | 更新 Wiki：Kimi CLI 百科页 | - |

---

## 八、待确认决策（明日继续）

### 8.1 日报详细程度

| 选项 | 说明 | 日更压力 |
|------|------|---------|
| A. 探索笔记 | 记录当天探索过程，较随意，像实验记录 | ⭐⭐ 低 |
| B. 微型教程 | 解决一个具体问题，有步骤可复现 | ⭐⭐⭐ 中 |
| C. 完整文章 | 结构完整的长文（如现有 Sandbox 文章） | ⭐⭐⭐⭐⭐ 高 |

**当前倾向**：A+B 混合，周五周报再汇总成 C

### 8.2 首月聚焦工具

推荐首月聚焦 **2-3 个工具** 建立深度：
- **OpenClaw**（核心优势）
- **Claude Code**（新晋热门，Plan 模式有话题性）
- **Kimi CLI**（国产代表，与 OpenClaw 可联动）

一个月后逐步加入 DeepSeek、Seedance 等。

### 8.3 多平台优先级

建议分阶段：
1. **第1月**：专注建设主站（ClawUtil），积累 20+ 篇内容
2. **第2月**：开通公众号，同步主站内容
3. **第3月**：加入小红书（需要额外做图）
4. **第4月+**：知乎、CSDN、播客

### 8.4 其他待讨论

- [ ] 是否保留现有首页设计，还是重新设计博客门户首页？
- [ ] 现有两篇文章如何融入新结构？
- [ ] 是否需要评论区（Gitalk/Utterances）？
- [ ] 是否需要访问统计（Google Analytics/Plausible）？
- [ ] 域名：保持 `zymclaw.github.io/clawutil` 还是考虑独立域名？

---

## 九、明日继续要点

1. 确认日报详细程度（A/B/C）
2. 确认首月聚焦工具（是否 OpenClaw+Claude Code+Kimi CLI）
3. 确认平台启动顺序
4. 确定首页设计方向
5. 制定第一周的详细内容计划

---

## 十、参考资源

- 现有文章：
  - `/articles/2026-03-07-openclaw-sandbox/` - Sandbox 故障排查实录
  - `/articles/2026-03-08-tavily-config/` - Tavily 配置指南
- 设计文档：本文档
