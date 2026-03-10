'use client';

import { Card, Button, Table, Tag, Space, Typography, Empty } from '@arco-design/web-react';
import { Plus, Pencil, Trash2, Eye } from 'lucide-react';
import Link from 'next/link';
import { ArticleTypeLabels, StatusLabels, ArticleTypeColors, type Article } from '@/types';

const { Title } = Typography;

// MVP 阶段空数据
const articles: Article[] = [];

const columns = [
  {
    title: '标题',
    dataIndex: 'title',
    render: (title: string, record: Article) => (
      <div>
        <div className="font-medium">{title}</div>
        <div className="text-xs text-gray-500 mt-1">
          {record.summary ? record.summary.slice(0, 50) + '...' : '暂无摘要'}
        </div>
      </div>
    ),
  },
  {
    title: '类型',
    dataIndex: 'type',
    width: 100,
    render: (type: string) => (
      <Tag color={ArticleTypeColors[type as keyof typeof ArticleTypeColors]}>
        {ArticleTypeLabels[type as keyof typeof ArticleTypeLabels]}
      </Tag>
    ),
  },
  {
    title: '状态',
    dataIndex: 'status',
    width: 100,
    render: (status: string) => {
      const colorMap: Record<string, string> = {
        DRAFT: 'gray',
        PUBLISHED: 'green',
        ARCHIVED: 'orange',
      };
      return (
        <Tag color={colorMap[status]}>
          {StatusLabels[status as keyof typeof StatusLabels]}
        </Tag>
      );
    },
  },
  {
    title: '发布时间',
    dataIndex: 'publishDate',
    width: 180,
    render: (date: Date | null) => date ? new Date(date).toLocaleString('zh-CN') : '-',
  },
  {
    title: '阅读量',
    dataIndex: 'viewCount',
    width: 100,
    render: (count: number) => count.toLocaleString(),
  },
  {
    title: '操作',
    width: 200,
    render: (_: unknown, record: Article) => (
      <Space>
        <Button type="text" icon={<Eye size={16} />} size="small">
          预览
        </Button>
        <Link href={`/admin/articles/${record.id}`}>
          <Button type="text" icon={<Pencil size={16} />} size="small">
            编辑
          </Button>
        </Link>
        <Button type="text" status="danger" icon={<Trash2 size={16} />} size="small">
          删除
        </Button>
      </Space>
    ),
  },
];

export default function ArticlesPage() {
  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <Title heading={3} className="!mb-0">文章管理</Title>
        <Link href="/admin/articles/new">
          <Button type="primary" icon={<Plus size={16} />}>
            新建文章
          </Button>
        </Link>
      </div>

      <Card>
        {articles.length === 0 ? (
          <Empty
            icon={<div className="text-6xl">📝</div>}
            description={
              <div className="text-center">
                <div className="text-lg mb-2">还没有文章</div>
                <div className="text-gray-500 mb-4">开始创作你的第一篇技术文章吧！</div>
                <Link href="/admin/articles/new">
                  <Button type="primary" icon={<Plus size={16} />}>
                    新建文章
                  </Button>
                </Link>
              </div>
            }
          />
        ) : (
          <Table
            columns={columns}
            data={articles}
            rowKey="id"
            pagination={{
              total: articles.length,
              pageSize: 10,
            }}
          />
        )}
      </Card>
    </div>
  );
}
