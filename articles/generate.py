#!/usr/bin/env python3
"""
文章站点生成脚本

用法：
  python3 generate.py              # 生成 index.html 和更新所有文章的推荐链接
  python3 generate.py --article tavily-config  # 更新指定文章的推荐链接

数据源：articles.json
"""

import json
import os
from datetime import datetime
from pathlib import Path

# 配置
ARTICLES_DIR = Path(__file__).parent
DATA_FILE = ARTICLES_DIR / "articles.json"
INDEX_TEMPLATE = ARTICLES_DIR / "templates" / "index.html"
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

def load_data():
    """加载文章数据"""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_tag_html(tags, category):
    """生成标签 HTML"""
    colors = {
        "配置指南": "from-blue-500/20 to-cyan-500/20 text-blue-400 border-blue-500/30",
        "故障排查": "from-cyan-500/20 to-emerald-500/20 text-cyan-400 border-cyan-500/30",
        "技术教程": "from-purple-500/20 to-pink-500/20 text-purple-400 border-purple-500/30",
    }
    
    html = f'<span class="bg-gradient-to-r {colors.get(category, "from-slate-500/20 to-slate-500/20 text-slate-400 border-slate-500/30")} px-3 py-1 rounded-full text-xs font-semibold border">\n'
    html += f'                                    {category}\n'
    html += f'                                </span>\n'
    
    for tag in tags[:1]:  # 只显示第一个 tag
        html += f'                                <span class="bg-gradient-to-r from-emerald-500/20 to-teal-500/20 text-emerald-400 border border-emerald-500/30 px-3 py-1 rounded-full text-xs font-semibold">\n'
        html += f'                                    {tag}\n'
        html += f'                                </span>\n'
    
    return html

def generate_article_card(article, has_image=False):
    """生成文章卡片 HTML"""
    tags_html = generate_tag_html(article['tags'], article['category'])
    
    date = article['date'].split('-')[1] + '-' + article['date'].split('-')[2]  # MM-DD
    date_display = article['date'][5:]  # YYYY-MM-DD -> MM-DD
    
    if has_image and article.get('coverImage'):
        card_class = ""
        flex_class = " flex-1"
        cover_image = f'<div class="md:w-64 md:flex-shrink-0">\n                            <img src="{article["folder"]}/{article["coverImage"]}" alt="{article["title"]}" class="w-full h-48 md:h-full object-cover">\n                        </div>'
        author_span = ""
    else:
        card_class = "p-6"
        flex_class = ""
        cover_image = ""
        author_span = '<span class="flex items-center gap-1">\n                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>\n                                        龙虾\n                                    </span>'
    
    return ARTICLE_LINK_TEMPLATE.format(
        folder=article['folder'],
        file=article['file'],
        title=article['title'],
        description=article['description'],
        date=article['date'],
        readTime=article['readTime'] + '阅读',
        tags=tags_html,
        card_class=card_class,
        flex_class=flex_class,
        cover_image=cover_image,
        author_span=author_span
    )

def generate_recommendations(current_id, articles):
    """生成推荐文章列表"""
    html = """        <section class="recommendations">
            <h3>📖 更多文章</h3>
            <ul>
"""
    for article in articles:
        if article['id'] != current_id and article.get('published', True):
            html += f'                <li><a href="../{article["folder"]}/{article["file"]}">{article["title"]}</a></li>\n'
    
    if html.count('<li>') == 1:  # 只有标题
        html += '                <li>暂无更多文章</li>\n'
    
    html += """            </ul>
        </section>"""
    return html

def update_article_recommendations(article, all_articles):
    """更新单篇文章的推荐链接"""
    article_path = ARTICLES_DIR / article['folder'] / article['file']
    if not article_path.exists():
        print(f"⚠️ 文章文件不存在: {article_path}")
        return False
    
    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找并替换推荐区域
    start_marker = '<section class="recommendations">'
    end_marker = '</section>'
    
    start = content.find(start_marker)
    end = content.find(end_marker, start) + len(end_marker)
    
    if start == -1:
        print(f"⚠️ 未找到推荐区域: {article_path}")
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
    
    new_footer = f"""    <footer>
        <p>© {datetime.now().year} {site['title']} | <a href="{site['github']}" style="color: var(--primary-color);">GitHub</a></p>
        <p style="margin-top: 10px;">本文由 OpenClaw AI 助手「{site['author']}」创作</p>
    </footer>"""
    
    new_content = content[:start] + new_footer + content[end:]
    
    with open(article_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    """主函数"""
    print("🦞 文章站点生成器")
    print("=" * 50)
    
    data = load_data()
    site = data['site']
    articles = data['articles']
    
    # 按日期排序（最新在前）
    articles.sort(key=lambda x: x['date'], reverse=True)
    
    print(f"\n📚 共 {len(articles)} 篇文章")
    
    # 更新所有文章的推荐链接和页脚
    print("\n📝 更新文章内容...")
    for article in articles:
        if article.get('published', True):
            update_article_recommendations(article, articles)
            update_article_footer(article, site)
    
    print("\n✅ 完成！")
    print("\n💡 提示:")
    print("   - 修改 articles.json 添加/编辑文章信息")
    print("   - 运行 python3 generate.py 更新所有页面")

if __name__ == '__main__':
    main()
