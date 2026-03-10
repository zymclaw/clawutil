import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  console.log('开始初始化数据...');

  // 创建分类
  const categories = [
    { name: 'OpenClaw', slug: 'openclaw', icon: '🦞', color: '#165DFF', description: 'AI 助手与 Agent 框架' },
    { name: 'Claude Code', slug: 'claude-code', icon: '🟣', color: '#D97757', description: 'Anthropic 的 AI 编程助手' },
    { name: 'Kimi CLI', slug: 'kimi', icon: '🌙', color: '#00B42A', description: '月之暗面的 AI 助手' },
  ];

  for (const category of categories) {
    await prisma.category.upsert({
      where: { slug: category.slug },
      update: {},
      create: category,
    });
  }
  console.log('✅ 分类创建完成');

  // 创建示例文章
  const articles = [
    {
      title: 'ClawUtil 博客系统正式发布',
      slug: 'clawutil-v1-release',
      content: `# ClawUtil 博客系统正式发布

## 介绍

这是一个现代化的个人 AI 技术博客系统，基于 Next.js + Arco Design 构建。

## 特性

- 📝 Markdown 编辑器
- 🎨 多主题支持
- 📱 响应式设计
- ⚡ 高性能

## 开始使用

访问后台管理页面开始创作：

\`\`\`
/admin
\`\`\`

## 技术栈

- Next.js 14
- TypeScript
- Arco Design
- Prisma
- SQLite
`,
      summary: 'ClawUtil 博客系统正式发布，基于 Next.js + Arco Design 构建的现代化个人博客',
      type: 'DAILY',
      status: 'PUBLISHED',
      readTime: 3,
      tags: ['公告', 'ClawUtil'],
    },
  ];

  for (const article of articles) {
    const { tags, ...articleData } = article;
    
    await prisma.article.upsert({
      where: { slug: article.slug },
      update: {},
      create: {
        ...articleData,
        publishDate: new Date(),
        tags: {
          connectOrCreate: tags.map((tag: string) => ({
            where: { name: tag },
            create: { name: tag },
          })),
        },
      },
    });
  }
  console.log('✅ 示例文章创建完成');

  console.log('初始化完成！');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
