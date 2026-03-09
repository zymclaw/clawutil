# Podcast Downloader Skill

小宇宙播客下载工具，自动转换为 MP3 格式。

## 安装

```bash
# 方法 1: 克隆仓库
git clone https://github.com/zymclaw/clawutil.git
cp -r clawutil/skills/podcast-downloader ~/.openclaw/workspace/skills/

# 方法 2: 直接下载
curl -LO https://raw.githubusercontent.com/zymclaw/clawutil/main/skills/podcast-downloader/SKILL.md
# ... 下载其他文件
```

## 使用

```bash
# 基础用法
./scripts/download.sh "https://www.xiaoyuzhoufm.com/episode/abc123"

# 自定义音质
AUDIO_QUALITY=2 ./scripts/download.sh <URL>

# 自定义目录
PODCAST_DIR=/custom/path ./scripts/download.sh <URL>
```

## 下载统计

查看 GitHub Releases 或直接使用 GitHub API 追踪。

## 技术文章

[Podcast Downloader Skill 开发全记录](../../articles/2026-03-09-podcast-downloader/podcast-downloader-dev.html)
