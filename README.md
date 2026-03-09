# ClawUtil - OpenClaw 实用技能集

[![GitHub release](https://img.shields.io/github/v/release/zymclaw/clawutil?include_prereleases)](https://github.com/zymclaw/clawutil/releases)
[![GitHub downloads](https://img.shields.io/github/downloads/zymclaw/clawutil/total?color=brightgreen)](https://github.com/zymclaw/clawutil/releases)
[![License](https://img.shields.io/github/license/zymclaw/clawutil)](LICENSE)

实用的 OpenClaw Agent Skills 集合，提供开箱即用的自动化能力。

## Skills

### podcast-downloader 🎙️

[![Download](https://img.shields.io/github/downloads/zymclaw/clawutil/v1.0.0/podcast-downloader-v1.0.0.zip?color=blue&label=Download)](https://github.com/zymclaw/clawutil/releases/download/v1.0.0/podcast-downloader-v1.0.0.zip)

从小宇宙(xiaoyuzhoufm.com)下载播客音频，自动转换为 MP3 格式，支持骨传导耳机离线播放。

**功能特点**：
- ✅ 自动提取节目信息（标题、播客名、音频 URL）
- ✅ 转换为 MP3（兼容 Sanag、小游等骨传导耳机）
- ✅ 自动删除原始 m4a 文件
- ✅ 保存 Show Notes 为 Markdown
- ✅ 支持批量下载
- ✅ 可配置音质

**安装**：
```bash
# 方法 1: 下载安装
curl -LO https://github.com/zymclaw/clawutil/releases/download/v1.0.0/podcast-downloader-v1.0.0.zip
unzip podcast-downloader-v1.0.0.zip
cp -r podcast-downloader ~/.openclaw/workspace/skills/

# 方法 2: Git 克隆
git clone https://github.com/zymclaw/clawutil.git
cp -r clawutil/skills/podcast-downloader ~/.openclaw/workspace/skills/
```

**使用**：
```bash
# 基础用法
./scripts/download.sh "https://www.xiaoyuzhoufm.com/episode/abc123"

# 自定义音质 (0=最佳, 4=最小)
AUDIO_QUALITY=2 ./scripts/download.sh <URL>

# 自定义目录
PODCAST_DIR=/custom/path ./scripts/download.sh <URL>
```

**技术文章**：[开发全记录](https://zymclaw.github.io/clawutil/articles/2026-03-09-podcast-downloader/podcast-downloader-dev.html)

## 文章

| 文章 | 日期 | 标签 |
|------|------|------|
| [Podcast Downloader Skill 开发全记录](https://zymclaw.github.io/clawutil/articles/2026-03-09-podcast-downloader/podcast-downloader-dev.html) | 2026-03-09 | Skill, 播客 |
| [OpenClaw 2026.3.7 正式版发布](https://zymclaw.github.io/clawutil/articles/2026-03-08-openclaw-3.7-release/openclaw-3.7-release.html) | 2026-03-08 | 版本更新 |
| [OpenClaw 配置 Tavily 搜索踩坑指南](https://zymclaw.github.io/clawutil/articles/2026-03-08-tavily-config/tavily-config-guide.html) | 2026-03-08 | 配置 |
| [当我的 AI 助手突然失忆了](https://zymclaw.github.io/clawutil/articles/2026-03-07-openclaw-sandbox/openclaw-sandbox-troubleshooting.html) | 2026-03-07 | 故障排查 |

## 目录结构

```
clawutil/
├── skills/                    # Skills 目录
│   └── podcast-downloader/    # 播客下载技能
│       ├── SKILL.md           # 核心文档
│       ├── reference.md       # 详细参考
│       ├── scripts/
│       │   └── download.sh    # 下载脚本
│       └── LICENSE.txt
├── articles/                  # 技术文章
│   └── 2026-03-09-podcast-downloader/
│       └── podcast-downloader-dev.html
├── releases/                  # 发布包
│   └── podcast-downloader-v1.0.0.zip
└── README.md
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

[MIT License](LICENSE)
