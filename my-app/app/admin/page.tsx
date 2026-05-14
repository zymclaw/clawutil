'use client';

import { Card, Statistic, Button, Typography, Grid, Space, Tag } from '@arco-design/web-react';
import {
  Plus,
  ArrowRight,
} from 'lucide-react';
import Link from 'next/link';

const { Title, Paragraph } = Typography;
const { Row, Col } = Grid;

export default function AdminDashboard() {
  // MVP 阶段显示模拟数据
  const stats = {
    articles: 0,
    views: 0,
    tags: 0,
    drafts: 0,
  };

  return (
    <div>
      <div className="mb-8">
        <Title heading={3} className="!mb-2">欢迎回来 👋</Title>
        <Paragraph className="text-gray-500">
          这是你的个人 AI 技术博客管理后台，开始创作吧！
        </Paragraph>
      </div>

      {/* Stats Cards */}
      <Row gutter={16} className="mb-8">
        <Col xs={24} sm={12} lg={6} className="mb-4">
          <Card>
            <Statistic
              title="文章总数"
              value={stats.articles}
              suffix="篇"
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6} className="mb-4">
          <Card>
            <Statistic
              title="总阅读量"
              value={stats.views}
              suffix="次"
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6} className="mb-4">
          <Card>
            <Statistic
              title="标签"
              value={stats.tags}
              suffix="个"
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6} className="mb-4">
          <Card>
            <Statistic
              title="草稿箱"
              value={stats.drafts}
              suffix="篇"
            />
          </Card>
        </Col>
      </Row>

      {/* Quick Actions */}
      <Row gutter={16} className="mb-8">
        <Col xs={24} lg={12} className="mb-4">
          <Card
            title="快速开始"
            extra={
              <Link href="/admin/articles/new">
                <Button type="primary" icon={<Plus size={16} />}>
                  新建文章
                </Button>
              </Link>
            }
          >
            <Space direction="vertical" className="w-full">
              <div className="flex items-center justify-between py-3 border-b border-gray-100">
                <div>
                  <div className="font-medium">创建新文章</div>
                  <div className="text-sm text-gray-500">开始撰写你的技术文章</div>
                </div>
                <Link href="/admin/articles/new">
                  <Button type="text" icon={<ArrowRight size={16} />} />
                </Link>
              </div>
              <div className="flex items-center justify-between py-3 border-b border-gray-100">
                <div>
                  <div className="font-medium">管理文章</div>
                  <div className="text-sm text-gray-500">查看、编辑和发布文章</div>
                </div>
                <Link href="/admin/articles">
                  <Button type="text" icon={<ArrowRight size={16} />} />
                </Link>
              </div>
              <div className="flex items-center justify-between py-3">
                <div>
                  <div className="font-medium">设置分类</div>
                  <div className="text-sm text-gray-500">管理文章分类和标签</div>
                </div>
                <Link href="/admin/categories">
                  <Button type="text" icon={<ArrowRight size={16} />} />
                </Link>
              </div>
            </Space>
          </Card>
        </Col>

        <Col xs={24} lg={12} className="mb-4">
          <Card title="内容日历">
            <div className="text-center py-8">
              <div className="text-4xl mb-4">📅</div>
              <Paragraph className="text-gray-500">
                内容日历功能开发中...
              </Paragraph>
              <Tag color="arcoblue">MVP v2</Tag>
            </div>
          </Card>
        </Col>
      </Row>

      {/* Recent Articles */}
      <Card
        title="最近文章"
        extra={
          <Link href="/admin/articles">
            <Button type="text">查看全部</Button>
          </Link>
        }
      >
        <div className="text-center py-12">
          <div className="text-6xl mb-4">📝</div>
          <Title heading={5} className="!mb-2">还没有文章</Title>
          <Paragraph className="text-gray-500 mb-4">
            开始创作你的第一篇技术文章吧！
          </Paragraph>
          <Link href="/admin/articles/new">
            <Button type="primary" size="large" icon={<Plus size={18} />}>
              立即创建
            </Button>
          </Link>
        </div>
      </Card>
    </div>
  );
}
