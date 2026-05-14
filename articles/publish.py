#!/usr/bin/env python3
"""
ClawUtil 文章发布工具

用法：
  python3 publish.py new <title>           # 创建新文章
  python3 publish.py edit <id>             # 编辑文章（打开 HTML）
  python3 publish.py preview <id>          # 本地预览
  python3 publish.py check                 # 检查所有文章
  python3 publish.py generate              # 运行 generate.py
  python3 publish.py status                # 查看状态
  python3 publish.py workflow              # 完整工作流（检查+生成+预览）
  python3 publish.py publish <id>          # 发布（git add/commit/push）

示例：
  python3 publish.py new "OpenClaw 新功能体验"
  python3 publish.py workflow
  python3 publish.py publish stock-skill-and-dual-lobster
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# 配置
ARTICLES_DIR = Path(__file__).parent
DATA_FILE = ARTICLES_DIR / "articles.json"
TEMPLATE_DIR = ARTICLES_DIR.parent / "_templates" / "article-template.html"
REPO_DIR = ARTICLES_DIR.parent

def load_data():
    """加载文章数据"""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    """保存文章数据"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_id(title):
    """根据标题生成 ID"""
    import re
    # 移除特殊字符，转小写，空格转连字符
    id_str = re.sub(r'[^\w\s-]', '', title.lower())
    id_str = re.sub(r'[\s]+', '-', id_str)
    return id_str[:50]

def generate_folder_name(date, id_str):
    """生成目录名"""
    return f"{date}-{id_str}"

def cmd_new(title):
    """创建新文章"""
    data = load_data()
    
    # 生成基本信息
    today = datetime.now().strftime("%Y-%m-%d")
    article_id = generate_id(title)
    folder = generate_folder_name(today, article_id)
    
    # 检查是否已存在
    for article in data['articles']:
        if article['id'] == article_id:
            print(f"❌ 文章 ID '{article_id}' 已存在")
            return False
    
    # 创建目录
    article_dir = ARTICLES_DIR / folder
    article_dir.mkdir(parents=True, exist_ok=True)
    
    # 读取模板
    if TEMPLATE_DIR.exists():
        with open(TEMPLATE_DIR, 'r', encoding='utf-8') as f:
            template = f.read()
    else:
        print(f"⚠️  模板文件不存在: {TEMPLATE_DIR}")
        template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}}</title>
    <style>
        /* 在这里添加样式 */
    </style>
</head>
<body>
    <article>
        <h1>{{TITLE}}</h1>
        <p>{{SUBTITLE}}</p>
        <!-- 在这里添加内容 -->
    </article>
</body>
</html>"""
    
    # 替换模板变量
    content = template.replace('{{TITLE}}', title)
    content = content.replace('{{SUBTITLE}}', '')
    content = content.replace('{{DATE}}', today)
    content = content.replace('{{READ_TIME}}', '5分钟')
    
    # 写入文件
    article_file = article_dir / 'article.html'
    with open(article_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 更新 articles.json
    new_article = {
        "id": article_id,
        "title": title,
        "subtitle": "",
        "date": today,
        "readTime": "5分钟",
        "tags": [],
        "category": "日记",
        "folder": folder,
        "file": "article.html",
        "coverImage": None,
        "description": "",
        "published": False
    }
    
    # 插入到文章列表开头
    data['articles'].insert(0, new_article)
    save_data(data)
    
    print(f"""
✅ 文章创建成功！

📁 目录: {folder}
📄 文件: {folder}/article.html
🆔 ID: {article_id}

下一步：
1. 编辑文章内容: open articles/{folder}/article.html
2. 更新 articles.json 中的元数据（tags, description 等）
3. 预览: python3 publish.py preview {article_id}
4. 发布: 编辑 articles.json 设置 published: true，然后 git push
""")
    return True

def cmd_preview(article_id):
    """本地预览文章"""
    data = load_data()
    
    for article in data['articles']:
        if article['id'] == article_id:
            folder = article['folder']
            file = article['file']
            article_path = ARTICLES_DIR / folder / file
            
            if article_path.exists():
                print(f"📖 打开预览: {article_path}")
                subprocess.run(['open', str(article_path)])
                return True
            else:
                print(f"❌ 文章文件不存在: {article_path}")
                return False
    
    print(f"❌ 未找到文章: {article_id}")
    return False

def cmd_check():
    """检查所有文章"""
    data = load_data()
    issues = []
    
    print("🔍 检查文章状态...\n")
    
    for article in data['articles']:
        folder = article['folder']
        file = article['file']
        article_path = ARTICLES_DIR / folder / file
        
        issues_per_article = []
        
        # 检查文件是否存在
        if not article_path.exists():
            issues_per_article.append(f"文件不存在: {article_path}")
        
        # 检查 </style> 标签数量
        if article_path.exists():
            with open(article_path, 'r', encoding='utf-8') as f:
                content = f.read()
                style_count = content.count('</style>')
                if style_count > 1:
                    issues_per_article.append(f"有 {style_count} 个 </style> 标签（应为 1 个）")
                
                # 检查是否有 CSS 暴露在 </style> 后面（但在 <body> 前）
                if style_count >= 1:
                    parts = content.split('</style>')
                    if len(parts) >= 2:
                        # 取 </style> 和 </head> 之间的内容
                        after_style = parts[1]
                        # 只检查 </head> 之前的部分
                        if '</head>' in after_style:
                            head_part = after_style.split('</head>')[0]
                            if '.rec-' in head_part or '推荐文章轮播' in head_part:
                                issues_per_article.append("CSS 暴露在 </style> 后面")
        
        # 检查必填字段
        required_fields = ['title', 'date', 'folder', 'file']
        for field in required_fields:
            if not article.get(field):
                issues_per_article.append(f"缺少必填字段: {field}")
        
        status = "❌" if issues_per_article else "✅"
        pub_status = "🟢 已发布" if article.get('published') else "🟡 草稿"
        
        print(f"{status} {article['title'][:30]:<30} {pub_status}")
        
        if issues_per_article:
            for issue in issues_per_article:
                print(f"   └─ {issue}")
            issues.extend(issues_per_article)
    
    print(f"\n{'='*50}")
    if issues:
        print(f"❌ 发现 {len(issues)} 个问题，请修复后再发布")
        return False
    else:
        print("✅ 所有文章检查通过")
        return True

def cmd_generate():
    """运行 generate.py"""
    print("🔄 运行 generate.py...")
    result = subprocess.run(['python3', 'generate.py'], cwd=ARTICLES_DIR)
    return result.returncode == 0

def cmd_status():
    """查看状态"""
    data = load_data()
    
    print("📊 文章统计\n")
    print(f"总文章数: {len(data['articles'])}")
    print(f"已发布: {sum(1 for a in data['articles'] if a.get('published'))}")
    print(f"草稿: {sum(1 for a in data['articles'] if not a.get('published'))}")
    
    print("\n📋 最近文章:")
    for article in data['articles'][:5]:
        pub = "🟢" if article.get('published') else "🟡"
        print(f"  {pub} {article['date']} - {article['title'][:40]}")

def cmd_edit(article_id):
    """编辑文章"""
    data = load_data()
    
    for article in data['articles']:
        if article['id'] == article_id:
            folder = article['folder']
            file = article['file']
            article_path = ARTICLES_DIR / folder / file
            json_path = DATA_FILE
            
            print(f"📝 打开编辑:")
            print(f"   文章: {article_path}")
            print(f"   元数据: {json_path}")
            
            # 打开 HTML 文件
            subprocess.run(['open', str(article_path)])
            # 打开 JSON 文件
            subprocess.run(['open', '-a', 'TextEdit', str(json_path)])
            return True
    
    print(f"❌ 未找到文章: {article_id}")
    return False

def cmd_workflow():
    """完整工作流：检查 + 生成 + 预览最新文章"""
    print("🔄 执行完整工作流...\n")
    
    # 1. 检查
    print("【1/3】检查文章格式...")
    if not cmd_check():
        print("\n❌ 检查未通过，请修复后再继续")
        return False
    
    # 2. 生成
    print("\n【2/3】生成首页和推荐链接...")
    if not cmd_generate():
        print("\n❌ 生成失败")
        return False
    
    # 3. 预览最新文章
    print("\n【3/3】打开最新文章预览...")
    data = load_data()
    if data['articles']:
        latest = data['articles'][0]
        print(f"\n📖 最新文章: {latest['title']}")
        print(f"   ID: {latest['id']}")
        print(f"   日期: {latest['date']}")
        cmd_preview(latest['id'])
    
    print("\n" + "="*50)
    print("✅ 工作流完成！")
    print("\n下一步：")
    print("1. 检查预览效果")
    print("2. 确认无误后回复「可以发布」")
    print("3. 执行: python3 publish.py publish <文章ID>")
    return True

def cmd_publish(article_id):
    """发布到 GitHub"""
    data = load_data()
    
    for article in data['articles']:
        if article['id'] == article_id:
            title = article['title']
            folder = article['folder']
            
            print(f"🚀 发布文章: {title}\n")
            
            # 检查是否有未提交的更改
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                    cwd=REPO_DIR, capture_output=True, text=True)
            
            if not result.stdout.strip():
                print("⚠️  没有需要提交的更改")
                return False
            
            # git add
            print("📦 添加文件...")
            subprocess.run(['git', 'add', '.'], cwd=REPO_DIR)
            
            # git commit
            commit_msg = f"docs: 发布文章「{title}」"
            print(f"📝 提交: {commit_msg}")
            subprocess.run(['git', 'commit', '-m', commit_msg], cwd=REPO_DIR)
            
            # git push
            print("🚀 推送到 GitHub...")
            result = subprocess.run(['git', 'push'], cwd=REPO_DIR)
            
            if result.returncode == 0:
                print("\n✅ 发布成功！")
                print(f"📖 在线地址: https://zymclaw.github.io/clawutil/articles/{folder}/article.html")
                return True
            else:
                print("\n❌ 推送失败")
                return False
    
    print(f"❌ 未找到文章: {article_id}")
    return False

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'new':
        if len(sys.argv) < 3:
            print("用法: python3 publish.py new <title>")
            sys.exit(1)
        title = ' '.join(sys.argv[2:])
        cmd_new(title)
    
    elif cmd == 'edit':
        if len(sys.argv) < 3:
            print("用法: python3 publish.py edit <id>")
            sys.exit(1)
        cmd_edit(sys.argv[2])
    
    elif cmd == 'preview':
        if len(sys.argv) < 3:
            print("用法: python3 publish.py preview <id>")
            sys.exit(1)
        cmd_preview(sys.argv[2])
    
    elif cmd == 'check':
        cmd_check()
    
    elif cmd == 'generate':
        cmd_generate()
    
    elif cmd == 'status':
        cmd_status()
    
    elif cmd == 'workflow':
        cmd_workflow()
    
    elif cmd == 'publish':
        if len(sys.argv) < 3:
            print("用法: python3 publish.py publish <id>")
            sys.exit(1)
        cmd_publish(sys.argv[2])
    
    else:
        print(f"未知命令: {cmd}")
        print(__doc__)
        sys.exit(1)

if __name__ == '__main__':
    main()
