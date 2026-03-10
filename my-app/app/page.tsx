'use client';

import { Button, Card, Layout, Typography, Space, Statistic, Grid } from '@arco-design/web-react';
import { 
  Pencil, 
  Rocket,
  Github,
} from 'lucide-react';
import Link from 'next/link';

const { Header, Content, Footer } = Layout;
const { Title, Paragraph } = Typography;
const { Row, Col } = Grid;

export default function Home() {
  return (
    <Layout className="min-h-screen bg-gray-50">
      {/* Header */}
      <Header className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-2xl">🦞</span>
            <div>
              <Title heading={5} className="!mb-0 !text-gray-900">ClawUtil</Title>
              <span className="text-xs text-gray-500">探索 AI 工具的每一天</span>
            </div>
          </div>
          
          <Space>
            <Link href="/admin">
              <Button type="primary" icon={<Pencil size={16} />}>
                写文章
              </Button>
            </Link>
          </Space>
        </div>
      </Header>

      {/* Hero Section */}
      <Content className="flex-1">
        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 py-20">
          <div className="max-w-4xl mx-auto px-6 text-center">
            <Title heading={1} className="!text-4xl md:!text-5xl !mb-6 !text-gray-900">
              探索 AI 工具的每一天
            </Title>
            <Paragraph className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
              个人 AI 技术博客，记录 OpenClaw、Claude Code、Kimi 等工具的使用经验、故障排查与最佳实践
            </Paragraph>
            <Space size="large">
              <Link href="/admin">
                <Button type="primary" size="large" icon={<Rocket size={18} />}>
                  开始写作
                </Button>
              </Link>
              <Button size="large" icon={<Github size={18} />}>
                查看源码
              </Button>
            </Space>
          </div>
        </div>

        {/* Stats */}
        <div className="max-w-6xl mx-auto px-6 -mt-10">
          <Row gutter={16}>
            <Col xs={12} md={6}>
              <Card className="text-center shadow-sm">
                <Statistic
                  title="文章"
                  value={0}
                  suffix="篇"
                />
              </Card>
            </Col>
            <Col xs={12} md={6}>
              <Card className="text-center shadow-sm">
                <Statistic
                  title="工具百科"
                  value={0}
                  suffix="个"
                />
              </Card>
            </Col>
            <Col xs={12} md={6}>
              <Card className="text-center shadow-sm">
                <Statistic
                  title="对比评测"
                  value={0}
                  suffix="篇"
                />
              </Card>
            </Col>
            <Col xs={12} md={6}>
              <Card className="text-center shadow-sm">
                <Statistic
                  title="今日更新"
                  value="待开始"
                />
              </Card>
            </Col>
          </Row>
        </div>

        {/* Quick Access */}
        <div className="max-w-6xl mx-auto px-6 py-16">
          <Title heading={3} className="!mb-8 text-center">快速入口</Title>
          <Row gutter={16}>
            <Col xs={24} md={6} className="mb-4">
              <Link href="/articles/">
                <Card 
                  className="h-full hover:shadow-md transition-shadow cursor-pointer"
                  title={
                    <Space>
                      <span className="text-2xl">📰</span>
                      <span>日报文章</span>
                    </Space>
                  }
                >
                  <Paragraph className="text-gray-600">
                    日更技术文章，记录 AI 工具的使用心得与实战经验
                  </Paragraph>
                </Card>
              </Link>
            </Col>
            <Col xs={24} md={6} className="mb-4">
              <Card 
                className="h-full hover:shadow-md transition-shadow cursor-pointer"
                title={
                  <Space>
                    <span className="text-2xl">📖</span>
                    <span>工具百科</span>
                  </Space>
                }
              >
                <Paragraph className="text-gray-600">
                  OpenClaw、Claude Code、Kimi 等工具的完整使用指南
                </Paragraph>
              </Card>
            </Col>
            <Col xs={24} md={6} className="mb-4">
              <Card 
                className="h-full hover:shadow-md transition-shadow cursor-pointer"
                title={
                  <Space>
                    <span className="text-2xl">🆚</span>
                    <span>对比评测</span>
                  </Space>
                }
              >
                <Paragraph className="text-gray-600">
                  多工具横向对比，帮你选择最适合的 AI 助手
                </Paragraph>
              </Card>
            </Col>
            <Col xs={24} md={6} className="mb-4">
              <Link href="/milestones/">
                <Card 
                  className="h-full hover:shadow-md transition-shadow cursor-pointer border-orange-200"
                  title={
                    <Space>
                      <span className="text-2xl">🔥</span>
                      <span className="text-orange-600">AI 里程碑</span>
                    </Space>
                  }
                >
                  <Paragraph className="text-gray-600">
                    从 Transformer 到认知革命，AI 发展重大事件时间线
                  </Paragraph>
                </Card>
              </Link>
            </Col>
          </Row>
        </div>

        {/* Tech Stack */}
        <div className="bg-white py-16">
          <div className="max-w-4xl mx-auto px-6 text-center">
            <Title heading={4} className="!mb-6">技术栈</Title>
            <Space wrap size="large">
              <span className="px-4 py-2 bg-gray-100 rounded-full">Next.js 14</span>
              <span className="px-4 py-2 bg-gray-100 rounded-full">TypeScript</span>
              <span className="px-4 py-2 bg-gray-100 rounded-full">Arco Design</span>
              <span className="px-4 py-2 bg-gray-100 rounded-full">Prisma</span>
              <span className="px-4 py-2 bg-gray-100 rounded-full">SQLite</span>
            </Space>
          </div>
        </div>
      </Content>

      {/* Footer */}
      <Footer className="bg-gray-900 text-white py-8">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <Paragraph className="text-gray-400">
            © 2026 ClawUtil · Made with 🦞 by zClaw
          </Paragraph>
        </div>
      </Footer>
    </Layout>
  );
}
