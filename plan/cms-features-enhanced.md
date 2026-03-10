# ClawUtil CMS 功能增强设计

> 借鉴 Raphael Publish 的现代化编辑器功能
> 整合日期：2026-03-10

---

## 🎯 核心借鉴点

### 从 Raphael Publish 提取的精华功能

| 功能 | Raphael 实现 | 我们的适配 |
|------|-------------|-----------|
| **智能粘贴** | 飞书/Notion/Word 富文本自动转 Markdown | ✅ 直接借鉴 |
| **截图粘贴** | Ctrl+V 图片转 Base64 插入 | ✅ 直接借鉴 |
| **多设备预览** | 手机/平板/桌面三视图 | ✅ 适配为响应式预览 |
| **滚动同步** | 编辑区↔预览区双向同步 | ✅ 直接借鉴 |
| **多主题** | 30+ 套排版主题 | ✅ 简化为 5-8 套 |
| **微信兼容** | 外链图片转 Base64 | ✅ 改为通用导出优化 |
| **导出功能** | PDF/HTML 导出 | ✅ 直接借鉴 |
| **字数统计** | 实时字数显示 | ✅ 直接借鉴 |

---

## ✨ 增强版 CMS 功能设计

### 1. 智能编辑器 (Smart Editor)

```typescript
interface SmartEditorFeatures {
  // 1. 智能粘贴
  smartPaste: {
    enabled: true;
    sources: ['feishu', 'notion', 'word', 'web'];
    conversion: 'html-to-markdown'; // 使用 turndown
    imageHandling: 'base64-inline'; // 图片转为 base64
  };
  
  // 2. 截图粘贴
  screenshotPaste: {
    enabled: true;
    shortcut: 'Ctrl/Cmd + V';
    output: '![图片](data:image/png;base64,...)'
  };
  
  // 3. 拖拽上传
  dragDrop: {
    enabled: true;
    target: 'editor-area';
    output: 'markdown-image';
  };
}
```

**实现参考**：
```typescript
// lib/smartPaste.ts
import TurndownService from 'turndown';
import { gfm } from 'turndown-plugin-gfm';

const turndownService = new TurndownService({
  headingStyle: 'atx',
  bulletListMarker: '-',
  codeBlockStyle: 'fenced',
  fence: '```',
  emDelimiter: '*',
  strongDelimiter: '**',
  linkStyle: 'inlined'
});

turndownService.use(gfm);

export function handleSmartPaste(
  e: ClipboardEvent,
  callback: (markdown: string) => void
) {
  const clipboardData = e.clipboardData;
  if (!clipboardData) return;
  
  const htmlData = clipboardData.getData('text/html');
  const textData = clipboardData.getData('text/plain');
  const imageFiles = Array.from(clipboardData.items || [])
    .filter(item => item.kind === 'file' && item.type.startsWith('image/'))
    .map(item => item.getAsFile())
    .filter(Boolean);
  
  // 优先处理图片粘贴
  if (imageFiles.length > 0) {
    e.preventDefault();
    handleImagePaste(imageFiles, callback);
    return;
  }
  
  // 处理富文本粘贴
  if (htmlData && htmlData.trim() !== '') {
    e.preventDefault();
    const markdown = turndownService.turndown(htmlData);
    callback(cleanupMarkdown(markdown));
  }
}
```

---

### 2. 多设备预览系统

```typescript
interface PreviewSystem {
  // 视图模式
  devices: [
    { id: 'mobile', name: '手机', width: 375, height: 812 },
    { id: 'tablet', name: '平板', width: 768, height: 1024 },
    { id: 'pc', name: '桌面', width: '100%', height: 'auto' }
  ];
  
  // 设备框架
  deviceFrame: {
    mobile: 'iphone-frame',   // 带刘海/圆角
    tablet: 'ipad-frame',     // 平板边框
    pc: 'none'                // 无边框
  };
  
  // 滚动同步
  scrollSync: {
    enabled: boolean;
    bidirectional: true; // 双向同步
    smooth: true;
  };
}
```

**界面设计**：
```
┌─────────────────────────────────────────────────────────────┐
│  📱 手机   📱 平板   💻 桌面      [同步滚动 🔗]              │
├──────────────────────────┬──────────────────────────────────┤
│                          │                                  │
│  # 文章标题              │   ┌─────────────────────────┐    │
│                          │   │  📱 iPhone 15 Pro       │    │
│  正文内容...             │   │  ┌───────────────────┐  │    │
│                          │   │  │                   │  │    │
│  - 列表项                │   │  │  文章标题         │  │    │
│  - 列表项                │   │  │                   │  │    │
│                          │   │  │  正文内容...      │  │    │
│  ![图片](...)            │   │  │                   │  │    │
│                          │   │  │  - 列表项         │  │    │
│                          │   │  │  - 列表项         │  │    │
│                          │   │  │                   │  │    │
│                          │   │  └───────────────────┘  │    │
│                          │   └─────────────────────────┘    │
│                          │                                  │
├──────────────────────────┴──────────────────────────────────┤
│  1,234 字                                                  │
└─────────────────────────────────────────────────────────────┘
```

---

### 3. 主题排版系统

借鉴 Raphael 的主题系统，但精简适配博客场景：

```typescript
interface ThemeSystem {
  // 博客专用主题（5-8套）
  themes: [
    {
      id: 'minimal',
      name: '极简白',
      description: '纯净阅读体验',
      styles: {
        container: 'background: #fff; color: #333;',
        h1: 'font-size: 28px; font-weight: 600; color: #1a1a1a;',
        h2: 'font-size: 22px; font-weight: 600; color: #2a2a2a;',
        p: 'font-size: 16px; line-height: 1.8; color: #333;',
        code: 'background: #f5f5f5; padding: 2px 6px; border-radius: 4px;',
        blockquote: 'border-left: 4px solid #165DFF; padding-left: 16px; color: #666;',
        link: 'color: #165DFF; text-decoration: none;',
        img: 'max-width: 100%; border-radius: 8px;'
      }
    },
    {
      id: 'claude',
      name: 'Claude 燕麦',
      description: '温暖舒适的阅读感',
      styles: { /* Claude 风格 */ }
    },
    {
      id: 'dark',
      name: '深色模式',
      description: '护眼暗色主题',
      styles: { /* 深色模式 */ }
    },
    {
      id: 'notion',
      name: 'Notion 风',
      description: '熟悉的效率感',
      styles: { /* Notion 风格 */ }
    },
    {
      id: 'github',
      name: 'GitHub',
      description: '开发者友好',
      styles: { /* GitHub 风格 */ }
    }
  ];
}
```

**主题切换 UI**：
```
┌────────────────────────────────────────────────────────┐
│  排版风格                                              │
│  [极简白] [Claude] [深色] [Notion] [更多 ▼]           │
└────────────────────────────────────────────────────────┘
```

---

### 4. 增强工具栏

```typescript
interface EnhancedToolbar {
  // 基础编辑
  basic: ['heading', 'bold', 'italic', 'strikethrough', 'divider'];
  
  // 插入
  insert: ['link', 'image', 'table', 'code', 'codeBlock', 'blockquote', 'divider'];
  
  // 列表
  list: ['unordered', 'ordered', 'task'];
  
  // 高级
  advanced: [
    'formula',      // LaTeX 公式
    'mermaid',      // 流程图
    'callout',      // 信息框
    'toggle',       // 折叠块
    'divider'
  ];
  
  // 快捷模板
  templates: {
    'daily': '日更文章模板',
    'wiki': '工具百科模板',
    'compare': '对比评测模板',
    'weekly': '周报模板'
  };
}
```

**工具栏设计**：
```
┌─────────────────────────────────────────────────────────────────┐
│  H  B  I  S        [链接] [图片] [表格] [代码] [引用]          │
│  ─────────────────────────────────────────────────────────────  │
│  •  1.  ☑        [公式] [流程图] [信息框] [模板 ▼]            │
└─────────────────────────────────────────────────────────────────┘
```

---

### 5. 导出与分享系统

```typescript
interface ExportSystem {
  // 导出格式
  formats: [
    {
      id: 'markdown',
      name: 'Markdown',
      ext: '.md',
      icon: '📝'
    },
    {
      id: 'html',
      name: 'HTML',
      ext: '.html',
      icon: '🌐',
      options: {
        standalone: true,  // 包含完整样式
        minify: false
      }
    },
    {
      id: 'pdf',
      name: 'PDF',
      ext: '.pdf',
      icon: '📄',
      options: {
        format: 'A4',
        margin: { top: 20, right: 20, bottom: 20, left: 20 }
      }
    },
    {
      id: 'wechat',
      name: '公众号',
      ext: null,
      icon: '💬',
      // 特殊处理：外链图片转 Base64
      preprocessing: 'image-to-base64'
    }
  ];
  
  // 分享
  share: {
    copyLink: true,
    generateQR: true,
    social: ['twitter', 'weibo', 'wechat']
  };
}
```

---

### 6. 实时协作与统计

```typescript
interface EditorStats {
  // 基础统计
  basic: {
    charCount: number;      // 字符数
    wordCount: number;      // 词数（中文按字）
    readTime: number;       // 预计阅读时间（分钟）
    paragraphCount: number; // 段落数
  };
  
  // 详细统计
  detailed: {
    headingCount: number;   // 标题数
    imageCount: number;     // 图片数
    linkCount: number;      // 链接数
    codeBlockCount: number; // 代码块数
  };
  
  // 历史
  history: {
    lastSaved: Date;
    saveCount: number;
    versions: Version[];
  };
}
```

**底部状态栏**：
```
┌─────────────────────────────────────────────────────────────────┐
│  💾 自动保存于 14:32        1,234 字 · 5 分钟阅读 · 3 张图片    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎨 CMS 界面布局（最终版）

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🦞 ClawUtil  CMS                                        zym  [退出]       │
├──────────┬──────────────────────────────────────────────────────────────────┤
│          │  📝 文章管理 / 新建文章                                          │
│  📊 概览  ├──────────────────────────────────────────────────────────────────┤
│  📝 文章  │                                                                    │
│  🏷️ 分类  │  ┌─────────────────────────────────────────────────────────┐   │
│  ⚙️ 设置  │  │  标题                                                     │   │
│          │  │  [输入文章标题...]                                        │   │
│          │  └─────────────────────────────────────────────────────────┘   │
│          │                                                                    │
│          │  分类: [日报 ▼]  标签: [OpenClaw ▼] [Claude ▼] [+添加]         │
│          │                                                                    │
│          │  排版: [极简白] [Claude] [深色] [Notion] [GitHub]              │
│          │                                                                    │
│          │  ┌───────────────────────┬──────────────────────────┐          │
│          │  │  Markdown             │  预览                    │          │
│          │  │                       │                          │          │
│          │  │  # 标题               │   ┌──────────────────┐   │          │
│          │  │                       │   │                  │   │          │
│          │  │  正文...              │   │  渲染效果         │   │          │
│          │  │                       │   │                  │   │          │
│          │  │  ![图](...)           │   │  同步滚动         │   │          │
│          │  │                       │   │                  │   │          │
│          │  └───────────────────────┴──────────────────────────┘          │
│          │                                                                    │
│          │  📱 手机  📱 平板  💻 桌面    [同步滚动 🔗]                      │
│          │                                                                    │
│          │  封面: [上传/拖拽图片]  发布: [立即 ▼]  时间: [日期时间]         │
│          │                                                                    │
│          │  ┌─────────────────────────────────────────────────────────┐   │
│          │  │  💡 提示：支持从飞书、Notion、Word 直接粘贴             │   │
│          │  │      支持截图 Ctrl+V 直接插入图片                        │   │
│          │  └─────────────────────────────────────────────────────────┘   │
│          │                                                                    │
│          │           [保存草稿] [预览] [导出 ▼] [立即发布]                │
│          │                                                                    │
│          │  💾 自动保存于 14:32    1,234 字 · 5 分钟 · 3 张图片          │
│          │                                                                    │
└──────────┴──────────────────────────────────────────────────────────────────┘
```

---

## 📋 功能优先级

### P0 - 核心功能（必须有）
- [ ] Markdown 编辑器
- [ ] 实时预览
- [ ] 文章 CRUD
- [ ] 分类/标签管理
- [ ] 自动保存

### P1 - 增强体验（Raphael 借鉴）
- [ ] **智能粘贴**（富文本转 Markdown）
- [ ] **截图粘贴**（Ctrl+V 图片）
- [ ] **多设备预览**（手机/平板/桌面）
- [ ] **滚动同步**
- [ ] **主题切换**（5套主题）
- [ ] **字数统计**

### P2 - 高级功能（后续迭代）
- [ ] 导出 PDF/HTML
- [ ] 公众号一键复制
- [ ] 版本历史
- [ ] 协同编辑
- [ ] 快捷键系统

---

## 🔗 参考资源

- **Raphael Publish**: https://github.com/zymclaw/raphael-publish
- **核心技术**: 
  - turndown (HTML to Markdown)
  - react-markdown (Markdown 渲染)
  - html2pdf.js (PDF 导出)
  - framer-motion (动画)
