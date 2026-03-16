#!/usr/bin/env python3
"""
文章站点生成脚本

用法：
  python3 generate.py              # 生成 index.html 和更新所有文章的推荐链接
  python3 generate.py --article tavily-config  # 更新指定文章的推荐链接
  python3 generate.py --index-only  # 仅生成 index.html

数据源：articles.json
"""

import json
import os
import argparse
from datetime import datetime
from pathlib import Path

# 配置
ARTICLES_DIR = Path(__file__).parent
DATA_FILE = ARTICLES_DIR / "articles.json"
INDEX_FILE = ARTICLES_DIR / "index.html"

# ============================================
# HTML 模板
# ============================================

INDEX_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_title} - OpenClaw 工具与文章</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        slate: {{
                            850: '#1e293b',
                            900: '#0f172a',
                        }}
                    }},
                    animation: {{
                        'float': 'float 20s infinite linear',
                        'pulse-slow': 'pulse 3s infinite',
                    }},
                    keyframes: {{
                        float: {{
                            '0%, 100%': {{ transform: 'translateY(100vh) translateX(0)', opacity: '0' }},
                            '10%, 90%': {{ opacity: '1' }},
                            '50%': {{ transform: 'translateY(50vh) translateX(50px)' }},
                        }}
                    }}
                }}
            }}
        }}
    </script>
    <style>
        .bg-grid {{
            background-image: 
                linear-gradient(rgba(56, 189, 248, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(56, 189, 248, 0.03) 1px, transparent 1px);
            background-size: 50px 50px;
        }}
        .gradient-text {{
            background: linear-gradient(135deg, #f8fafc 0%, #94a3b8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .glass-card {{
            background: rgba(30, 41, 59, 0.6);
            backdrop-filter: blur(10px);
        }}
        .article-card {{
            transition: all 0.3s ease;
        }}
        .article-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }}
    </style>
</head>
<body class="bg-gradient-to-br from-slate-900 to-slate-800 text-slate-200 min-h-screen relative overflow-x-hidden">

    <!-- 背景网格 -->
    <div class="fixed inset-0 bg-grid pointer-events-none z-0"></div>
    
    <!-- 浮动粒子 -->
    <div id="particles" class="fixed inset-0 pointer-events-none z-10 overflow-hidden"></div>

    <!-- 主内容 -->
    <main class="relative z-20 max-w-5xl mx-auto px-6 py-12">
        
        <!-- 头部 -->
        <header class="text-center mb-16">
            <div class="flex justify-center items-center gap-4 mb-6">
                <span class="text-6xl">🦞</span>
                <div class="text-left">
                    <h1 class="text-4xl md:text-5xl font-extrabold gradient-text">{site_title}</h1>
                    <p class="text-slate-400">{site_subtitle}</p>
                </div>
            </div>
            
            <p class="text-xl text-slate-400 max-w-2xl mx-auto">
                OpenClaw AI 助手的实战经验、故障排查指南、工具脚本与最佳实践
            </p>
            
            <div class="flex justify-center gap-6 mt-8 text-sm">
                <a href="{github_url}" class="flex items-center gap-2 text-slate-400 hover:text-cyan-400 transition-colors">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                    GitHub
                </a>
                <a href="https://openclaw.ai" class="flex items-center gap-2 text-slate-400 hover:text-cyan-400 transition-colors">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/></svg>
                    OpenClaw
                </a>
                <a href="https://clawhub.ai" class="flex items-center gap-2 text-slate-400 hover:text-cyan-400 transition-colors">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
                    ClawHub
                </a>
            </div>
        </header>

        <!-- 文章列表 -->
        <section class="mb-12">
            <div class="flex items-center gap-3 mb-8">
                <span class="w-1 h-8 bg-gradient-to-b from-cyan-400 to-emerald-500 rounded-full"></span>
                <h2 class="text-2xl font-bold text-white">📝 技术文章</h2>
            </div>
            
            <div class="grid gap-6">
{article_cards}
                <!-- 占位卡片 - 即将发布 -->
                <div class="article-card glass-card border border-slate-700/50 rounded-2xl p-6 opacity-50">
                    <div class="flex items-center gap-2 mb-3">
                        <span class="bg-slate-700 text-slate-400 px-3 py-1 rounded-full text-xs font-semibold">
                            即将发布
                        </span>
                    </div>
                    <h3 class="text-xl font-bold text-slate-400 mb-2">
                        更多精彩文章正在路上...
                    </h3>
                    <p class="text-slate-500">
                        敬请期待更多 OpenClaw 实战教程、工具脚本和最佳实践分享
                    </p>
                </div>
            </div>
        </section>

        <!-- 分类标签 -->
        <section class="mb-12">
            <div class="flex items-center gap-3 mb-6">
                <span class="w-1 h-8 bg-gradient-to-b from-cyan-400 to-emerald-500 rounded-full"></span>
                <h2 class="text-2xl font-bold text-white">🏷️ 分类标签</h2>
            </div>
            
            <div class="flex flex-wrap gap-3">
{category_tags}
            </div>
        </section>

        <!-- 快速链接 -->
        <section class="mb-12">
            <div class="flex items-center gap-3 mb-6">
                <span class="w-1 h-8 bg-gradient-to-b from-cyan-400 to-emerald-500 rounded-full"></span>
                <h2 class="text-2xl font-bold text-white">🔗 快速链接</h2>
            </div>
            
            <div class="grid md:grid-cols-3 gap-4">
                <a href="https://openclaw.ai" class="glass-card border border-slate-700/50 rounded-xl p-5 hover:border-cyan-500/50 transition-all group">
                    <div class="flex items-center gap-3 mb-2">
                        <span class="text-2xl">🦞</span>
                        <h3 class="font-bold text-white group-hover:text-cyan-400 transition-colors">OpenClaw 官网</h3>
                    </div>
                    <p class="text-slate-400 text-sm">打造你的 AI 私人助理</p>
                </a>
                
                <a href="https://clawhub.ai" class="glass-card border border-slate-700/50 rounded-xl p-5 hover:border-emerald-500/50 transition-all group">
                    <div class="flex items-center gap-3 mb-2">
                        <span class="text-2xl">🏪</span>
                        <h3 class="font-bold text-white group-hover:text-emerald-400 transition-colors">ClawHub 技能市场</h3>
                    </div>
                    <p class="text-slate-400 text-sm">发现和分享 AI 技能</p>
                </a>
                
                <a href="https://docs.openclaw.ai" class="glass-card border border-slate-700/50 rounded-xl p-5 hover:border-purple-500/50 transition-all group">
                    <div class="flex items-center gap-3 mb-2">
                        <span class="text-2xl">📚</span>
                        <h3 class="font-bold text-white group-hover:text-purple-400 transition-colors">OpenClaw 文档</h3>
                    </div>
                    <p class="text-slate-400 text-sm">完整的使用指南和 API 文档</p>
                </a>
            </div>
        </section>

        <!-- 页脚 -->
        <footer class="text-center text-slate-500 pt-8 border-t border-slate-800">
            <p>© {year} {site_title}. 保留所有权利。</p>
            <p class="mt-2 text-sm">The lobster grows stronger. 🦞</p>
            <div class="flex justify-center gap-6 mt-6">
                <a href="{github_url}" class="hover:text-cyan-400 transition-colors">GitHub</a>
                <a href="https://openclaw.ai" class="hover:text-cyan-400 transition-colors">OpenClaw</a>
                <a href="https://clawhub.ai" class="hover:text-cyan-400 transition-colors">ClawHub</a>
            </div>
        </footer>
    </main>

    <script>
        // 生成背景粒子
        const particlesContainer = document.getElementById('particles');
        for (let i = 0; i < 30; i++) {{
            const particle = document.createElement('div');
            particle.className = 'absolute w-1 h-1 bg-cyan-400/40 rounded-full animate-float';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 20 + 's';
            particle.style.animationDuration = (15 + Math.random() * 10) + 's';
            particlesContainer.appendChild(particle);
        }}
    </script>
</body>
</html>'''

# 文章卡片模板（有封面图）
ARTICLE_CARD_WITH_IMAGE = '''                <a href="{folder}/{file}" class="article-card glass-card border border-slate-700/50 rounded-2xl overflow-hidden block">
                    <div class="md:flex">
                        <div class="md:w-64 md:flex-shrink-0">
                            <img src="{folder}/{cover_image}" alt="{title}" class="w-full h-48 md:h-full object-cover">
                        </div>
                        <div class="p-6 flex-1">
                            <div class="flex items-center gap-2 mb-3">
{tags}
                            </div>
                            <h3 class="text-xl font-bold text-white mb-2 hover:text-cyan-400 transition-colors">
                                {title}
                            </h3>
                            <p class="text-slate-400 mb-4 line-clamp-2">
                                {description}
                            </p>
                            <div class="flex items-center justify-between text-sm text-slate-500">
                                <div class="flex items-center gap-4">
                                    <span class="flex items-center gap-1">
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                                        {date}
                                    </span>
                                    <span class="flex items-center gap-1">
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                                        {read_time}
                                    </span>
                                </div>
                                <span class="text-cyan-400 hover:underline">阅读全文 →</span>
                            </div>
                        </div>
                    </div>
                </a>'''

# 文章卡片模板（无封面图）
ARTICLE_CARD_NO_IMAGE = '''                <a href="{folder}/{file}" class="article-card glass-card border border-slate-700/50 rounded-2xl overflow-hidden block">
                    <div class="p-6">
                        <div class="flex items-center gap-2 mb-3">
{tags}
                        </div>
                        <h3 class="text-xl font-bold text-white mb-2 hover:text-cyan-400 transition-colors">
                            {title}
                        </h3>
                        <p class="text-slate-400 mb-4 line-clamp-2">
                            {description}
                        </p>
                        <div class="flex items-center justify-between text-sm text-slate-500">
                            <div class="flex items-center gap-4">
                                <span class="flex items-center gap-1">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                                    {date}
                                </span>
                                <span class="flex items-center gap-1">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                                    {read_time}
                                </span>
                                <span class="flex items-center gap-1">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
                                    {author}
                                </span>
                            </div>
                            <span class="text-cyan-400 hover:underline">阅读全文 →</span>
                        </div>
                    </div>
                </a>'''

# ============================================
# 导航栏模板（自动注入）
# ============================================

NAVBAR_CSS = '''
        /* 导航栏 */
        .nav-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 0;
            margin-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
        }

        .nav-bar .logo {
            display: flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
            color: var(--text-color);
            font-weight: 600;
            font-size: 1.1rem;
        }

        .nav-bar .logo:hover {
            color: var(--primary-color);
        }

        .nav-bar .back-link {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 8px 16px;
            background: var(--card-bg);
            color: var(--text-color);
            text-decoration: none;
            border-radius: 8px;
            font-size: 0.9rem;
            transition: all 0.2s ease;
            border: 1px solid var(--border-color);
        }

        .nav-bar .back-link:hover {
            background: var(--primary-color);
            border-color: var(--primary-color);
            transform: translateX(-3px);
        }

        /* 推荐文章轮播 */
        .recommendations {
            margin-top: 50px;
            padding: 25px;
            background: var(--card-bg);
            border-radius: 12px;
            border: 1px solid var(--border-color);
        }
        
        .rec-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .rec-header h3 {
            margin: 0;
            font-size: 1.2rem;
        }
        
        .rec-counter {
            font-size: 0.85rem;
            color: var(--text-muted);
        }
        
        .rec-carousel-wrapper {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .rec-carousel {
            flex: 1;
            overflow: hidden;
        }
        
        .rec-track {
            display: flex;
            transition: transform 0.3s ease;
        }
        
        .rec-card {
            flex: 0 0 calc(33.333% - 12px);
            margin-right: 18px;
            background: rgba(30, 41, 59, 0.5);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            transition: all 0.2s ease;
        }
        
        .rec-card:hover {
            border-color: var(--primary-color);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15);
        }
        
        .rec-card-link {
            display: block;
            padding: 16px;
            text-decoration: none;
        }
        
        .rec-card-title {
            color: var(--text-color);
            font-weight: 600;
            font-size: 0.95rem;
            margin-bottom: 8px;
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        
        .rec-card-desc {
            color: var(--text-muted);
            font-size: 0.8rem;
            margin-bottom: 10px;
            line-height: 1.5;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        
        .rec-card-date {
            color: var(--text-muted);
            font-size: 0.75rem;
        }
        
        .rec-nav {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            border: 1px solid var(--border-color);
            background: var(--card-bg);
            color: var(--text-color);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
            transition: all 0.2s ease;
            flex-shrink: 0;
        }
        
        .rec-nav:hover {
            background: var(--primary-color);
            border-color: var(--primary-color);
        }
        
        .no-articles {
            color: var(--text-muted);
            text-align: center;
            padding: 20px;
        }
        
        @media (max-width: 768px) {
            .rec-card {
                flex: 0 0 100%;
                margin-right: 0;
            }
            
            .rec-carousel-wrapper {
                flex-direction: column;
            }
            
            .rec-nav {
                align-self: center;
            }
        }
'''

NAVBAR_HTML = '''    <nav class="nav-bar">
        <a href="../index.html" class="logo">🦞 ClawUtil</a>
        <a href="../index.html" class="back-link">← 返回列表</a>
    </nav>
'''

# 文章内页推荐链接模板
ARTICLE_LINK_TEMPLATE = """                <a href="{folder}/{file}" class="article-card glass-card border border-slate-700/50 rounded-2xl overflow-hidden block">
                    <div class="{card_class}">
                        {cover_image}
                        <div class="p-6{flex_class}">
                            <div class="flex items-center gap-2 mb-3">
                                {tags}
                            </div>
                            <h3 class="text-xl font-bold text-white mb-2 hover:text-cyan-400 transition-colors">
                                {title}
                            </h3>
                            <p class="text-slate-400 mb-4 line-clamp-2">
                                {description}
                            </p>
                            <div class="flex items-center justify-between text-sm text-slate-500">
                                <div class="flex items-center gap-4">
                                    <span class="flex items-center gap-1">
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                                        {date}
                                    </span>
                                    <span class="flex items-center gap-1">
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                                        {readTime}
                                    </span>
                                    {author_span}
                                </div>
                                <span class="text-cyan-400 hover:underline">阅读全文 →</span>
                            </div>
                        </div>
                    </div>
                </a>"""

# ============================================
# 工具函数
# ============================================

def load_data():
    """加载文章数据"""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_category_color(category):
    """获取分类对应的颜色"""
    colors = {
        "配置指南": "from-blue-500/20 to-cyan-500/20 text-blue-400 border-blue-500/30",
        "故障排查": "from-cyan-500/20 to-emerald-500/20 text-cyan-400 border-cyan-500/30",
        "技术教程": "from-purple-500/20 to-pink-500/20 text-purple-400 border-purple-500/30",
        "最佳实践": "from-orange-500/20 to-amber-500/20 text-orange-400 border-orange-500/30",
        "工具脚本": "from-emerald-500/20 to-teal-500/20 text-emerald-400 border-emerald-500/30",
    }
    return colors.get(category, "from-slate-500/20 to-slate-500/20 text-slate-400 border-slate-500/30")

def get_tag_color(tag):
    """获取标签对应的颜色"""
    colors = [
        "border-cyan-500/30 text-cyan-400 hover:bg-cyan-500/10",
        "border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/10",
        "border-purple-500/30 text-purple-400 hover:bg-purple-500/10",
        "border-pink-500/30 text-pink-400 hover:bg-pink-500/10",
        "border-orange-500/30 text-orange-400 hover:bg-orange-500/10",
        "border-blue-500/30 text-blue-400 hover:bg-blue-500/10",
        "border-amber-500/30 text-amber-400 hover:bg-amber-500/10",
    ]
    # 使用 hash 来确保同一标签颜色一致
    idx = hash(tag) % len(colors)
    return colors[idx]

def generate_tag_html(tags, category):
    """生成标签 HTML"""
    html = f'                                <span class="bg-gradient-to-r {get_category_color(category)} px-3 py-1 rounded-full text-xs font-semibold border">\n'
    html += f'                                    {category}\n'
    html += f'                                </span>\n'
    
    for tag in tags[:1]:  # 只显示第一个 tag
        html += f'                                <span class="bg-gradient-to-r from-emerald-500/20 to-teal-500/20 text-emerald-400 border border-emerald-500/30 px-3 py-1 rounded-full text-xs font-semibold">\n'
        html += f'                                    {tag}\n'
        html += f'                                </span>\n'
    
    return html

def generate_article_card(article, site):
    """生成文章卡片 HTML"""
    tags_html = generate_tag_html(article['tags'], article['category'])
    
    if article.get('coverImage'):
        # 有封面图的卡片
        return ARTICLE_CARD_WITH_IMAGE.format(
            folder=article['folder'],
            file=article['file'],
            title=article['title'],
            description=article['description'],
            date=article['date'],
            read_time=article['readTime'] + ' 阅读',
            tags=tags_html,
            cover_image=article['coverImage']
        )
    else:
        # 无封面图的卡片
        return ARTICLE_CARD_NO_IMAGE.format(
            folder=article['folder'],
            file=article['file'],
            title=article['title'],
            description=article['description'],
            date=article['date'],
            read_time=article['readTime'] + ' 阅读',
            tags=tags_html,
            author=site['author']
        )

def generate_category_tags(articles):
    """生成分类标签 HTML"""
    # 收集所有标签
    all_tags = set()
    all_categories = set()
    
    for article in articles:
        if article.get('published', True):
            all_categories.add(article['category'])
            for tag in article.get('tags', []):
                all_tags.add(tag)
    
    html_lines = []
    
    # 分类颜色映射（用于标签展示）
    category_tag_colors = {
        "配置指南": "border-blue-500/30 text-blue-400 hover:bg-blue-500/10",
        "故障排查": "border-cyan-500/30 text-cyan-400 hover:bg-cyan-500/10",
        "技术教程": "border-purple-500/30 text-purple-400 hover:bg-purple-500/10",
        "最佳实践": "border-orange-500/30 text-orange-400 hover:bg-orange-500/10",
        "工具脚本": "border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/10",
    }
    
    # 先添加分类
    for category in sorted(all_categories):
        color = category_tag_colors.get(category, "border-slate-500/30 text-slate-400 hover:bg-slate-500/10")
        html_lines.append(f'                <span class="glass-card {color} px-4 py-2 rounded-full text-sm cursor-pointer transition-all">')
        html_lines.append(f'                    # {category}')
        html_lines.append('                </span>')
    
    # 再添加标签
    for tag in sorted(all_tags):
        tag_color = get_tag_color(tag)
        html_lines.append(f'                <span class="glass-card {tag_color} px-4 py-2 rounded-full text-sm cursor-pointer transition-all">')
        html_lines.append(f'                    # {tag}')
        html_lines.append('                </span>')
    
    return '\n'.join(html_lines)

def generate_index_html(data):
    """生成 index.html"""
    site = data['site']
    articles = data['articles']
    
    # 按日期排序（最新在前）
    articles_sorted = sorted(articles, key=lambda x: x['date'], reverse=True)
    
    # 只处理已发布的文章
    published_articles = [a for a in articles_sorted if a.get('published', True)]
    
    # 生成文章卡片
    article_cards = []
    for article in published_articles:
        article_cards.append(generate_article_card(article, site))
    
    # 生成分类标签
    category_tags = generate_category_tags(published_articles)
    
    # 填充模板
    html = INDEX_TEMPLATE.format(
        site_title=site['title'],
        site_subtitle=site['subtitle'],
        github_url=site['github'],
        year=datetime.now().year,
        article_cards='\n'.join(article_cards),
        category_tags=category_tags
    )
    
    return html

def generate_recommendations(current_id, articles, per_page=3):
    """生成推荐文章列表（卡片轮播形式）
    
    Args:
        current_id: 当前文章ID（不显示）
        articles: 所有文章列表
        per_page: 每页显示多少篇（默认3篇）
    """
    # 过滤出已发布的文章（排除当前文章）
    published = [a for a in articles if a['id'] != current_id and a.get('published', True)]
    
    if not published:
        return """        <section class="recommendations">
            <h3>📖 更多文章</h3>
            <p class="no-articles">暂无更多文章</p>
        </section>"""
    
    # 生成卡片 HTML
    cards_html = ""
    for article in published:
        title = article.get('title', '未命名')
        desc = article.get('description', '') or article.get('subtitle', '')
        if len(desc) > 60:
            desc = desc[:60] + '...'
        date = article.get('date', '')
        folder = article.get('folder', '')
        file = article.get('file', 'article.html')
        
        cards_html += f'''
                <div class="rec-card">
                    <a href="../{folder}/{file}" class="rec-card-link">
                        <div class="rec-card-title">{title}</div>
                        <div class="rec-card-desc">{desc}</div>
                        <div class="rec-card-date">{date}</div>
                    </a>
                </div>'''
    
    # 是否需要分页
    total = len(published)
    need_pagination = total > per_page
    
    html = f'''        <section class="recommendations">
            <div class="rec-header">
                <h3>📖 更多文章</h3>
                {f'<span class="rec-counter"><span id="recPage">1</span>/{(total + per_page - 1) // per_page}</span>' if need_pagination else ''}
            </div>
            <div class="rec-carousel-wrapper">
                <button class="rec-nav rec-prev" onclick="recNavigate(-1)"{' style="visibility:hidden"' if not need_pagination else ''}>❮</button>
                <div class="rec-carousel">
                    <div class="rec-track" id="recTrack">
{cards_html}
                    </div>
                </div>
                <button class="rec-nav rec-next" onclick="recNavigate(1)"{' style="visibility:hidden"' if not need_pagination else ''}>❯</button>
            </div>
            <script>
            (function() {{
                let page = 0;
                const perPage = {per_page};
                const total = {total};
                const pages = Math.ceil(total / perPage);
                const track = document.getElementById('recTrack');
                const pageEl = document.getElementById('recPage');
                const prevBtn = document.querySelector('.rec-prev');
                const nextBtn = document.querySelector('.rec-next');
                
                function updateCarousel() {{
                    const offset = -page * 100;
                    track.style.transform = 'translateX(' + offset + '%)';
                    if (pageEl) pageEl.textContent = page + 1;
                    if (prevBtn) prevBtn.style.visibility = page === 0 ? 'hidden' : 'visible';
                    if (nextBtn) nextBtn.style.visibility = page >= pages - 1 ? 'hidden' : 'visible';
                }}
                
                window.recNavigate = function(dir) {{
                    page = Math.max(0, Math.min(pages - 1, page + dir));
                    updateCarousel();
                }};
                
                updateCarousel();
            }})();
            </script>
        </section>'''
    
    return html

def update_article_recommendations(article, all_articles):
    """更新单篇文章的推荐链接"""
    article_path = ARTICLES_DIR / article['folder'] / article['file']
    if not article_path.exists():
        print(f"⚠️  文章文件不存在: {article_path}")
        return False
    
    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 删除旧的 .recommendations 样式（如果存在）
    import re
    old_css_pattern = r'\s*/\* 推荐阅读 \*/\s*\.recommendations \{[^}]*\}\s*\.recommendations h3 \{[^}]*\}\s*\.recommendations ul \{[^}]*\}\s*\.recommendations li \{[^}]*\}\s*\.recommendations li:last-child \{[^}]*\}\s*\.recommendations a \{[^}]*\}\s*\.recommendations a:hover \{[^}]*\}'
    content = re.sub(old_css_pattern, '', content)
    
    # 查找并替换推荐区域
    start_marker = '<section class="recommendations">'
    end_marker = '</section>'
    
    start = content.find(start_marker)
    end = content.find(end_marker, start) + len(end_marker)
    
    if start == -1:
        print(f"⚠️  未找到推荐区域: {article_path}")
        return False
    
    new_recommendations = generate_recommendations(article['id'], all_articles)
    new_content = content[:start] + new_recommendations + content[end:]
    
    with open(article_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ 更新推荐链接: {article['title']}")
    return True

def update_article_footer(article, site):
    """更新文章页脚"""
    article_path = ARTICLES_DIR / article['folder'] / article['file']
    if not article_path.exists():
        return False
    
    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新页脚
    old_footer_start = '<footer>'
    old_footer_end = '</footer>'
    
    start = content.find(old_footer_start)
    end = content.find(old_footer_end, start) + len(old_footer_end)
    
    if start == -1:
        return False
    
    # 从 2026-03-14 开始，Thea 有了名字，署名改为 Thea（Athena）
    # 之前的文章继续用"龙虾"署名
    if article['date'] >= '2026-03-14':
        author = 'Thea（Athena）— Jeff 的超级 AI 助理 🧠'
    else:
        author = f'OpenClaw AI 助手「{site["author"]}」'
    
    new_footer = f"""    <footer>
        <p>© {datetime.now().year} {site['title']} | <a href="{site['github']}" style="color: var(--primary-color);">GitHub</a></p>
        <p style="margin-top: 10px;">本文由 {author}创作</p>
    </footer>"""
    
    new_content = content[:start] + new_footer + content[end:]
    
    with open(article_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def inject_navbar(article):
    """自动注入导航栏（如果不存在）"""
    article_path = ARTICLES_DIR / article['folder'] / article['file']
    if not article_path.exists():
        return False
    
    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已有导航栏（检查 <nav 元素，而不是 CSS class）
    if '<nav class="nav-bar">' in content or '<nav class="nav-bar"':
        return False  # 已有导航栏，跳过
    
    # 注入 CSS（在 </style> 前）
    if '</style>' in content:
        content = content.replace('</style>', NAVBAR_CSS + '\n    </style>')
    
    # 注入 HTML（在 <body> 后，<header> 前）
    if '<body>' in content and '<header>' in content:
        content = content.replace('<body>\n    <header>', '<body>\n' + NAVBAR_HTML + '\n    <header>')
    
    with open(article_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 注入导航栏: {article['title']}")
    return True

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='文章站点生成器')
    parser.add_argument('--article', '-a', help='只更新指定文章的推荐链接')
    parser.add_argument('--index-only', '-i', action='store_true', help='只生成 index.html')
    args = parser.parse_args()
    
    print("🦞 ClawUtil 文章站点生成器")
    print("=" * 50)
    
    data = load_data()
    site = data['site']
    articles = data['articles']
    
    # 按日期排序（最新在前）
    articles.sort(key=lambda x: x['date'], reverse=True)
    
    published_count = sum(1 for a in articles if a.get('published', True))
    print(f"\n📚 共 {len(articles)} 篇文章，{published_count} 篇已发布")
    
    # 生成 index.html
    print("\n📄 生成 index.html...")
    html_content = generate_index_html(data)
    
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 已生成: {INDEX_FILE}")
    
    if args.index_only:
        print("\n✅ 完成！（仅生成 index.html）")
        return
    
    # 更新文章推荐链接
    if args.article:
        # 只更新指定文章
        article = next((a for a in articles if a['id'] == args.article), None)
        if article:
            print(f"\n📝 更新文章: {article['title']}")
            inject_navbar(article)  # 自动注入导航栏
            update_article_recommendations(article, articles)
            update_article_footer(article, site)
        else:
            print(f"⚠️  未找到文章: {args.article}")
    else:
        # 更新所有文章
        print("\n📝 更新文章内容...")
        for article in articles:
            if article.get('published', True):
                inject_navbar(article)  # 自动注入导航栏
                update_article_recommendations(article, articles)
                update_article_footer(article, site)
    
    print("\n✅ 完成！")
    print("\n💡 提示:")
    print("   - 修改 articles.json 添加/编辑文章信息")
    print("   - 运行 python3 generate.py 更新所有页面")
    print("   - 运行 python3 generate.py --article <id> 更新指定文章")
    print("   - 运行 python3 generate.py --index-only 仅生成首页")

if __name__ == '__main__':
    main()
