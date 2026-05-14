'use client';

import { Card, Button, Table, Tag, Space, Typography, Empty, Input } from '@arco-design/web-react';
import { Plus, Pencil, Trash2, Tag as TagIcon } from 'lucide-react';

const { Title } = Typography;

const categories = [
  { id: '1', name: 'OpenClaw', slug: 'openclaw', icon: '🦞', color: '#165DFF', articleCount: 0 },
  { id: '2', name: 'Claude Code', slug: 'claude-code', icon: '🟣', color: '#D97757', articleCount: 0 },
  { id: '3', name: 'Kimi CLI', slug: 'kimi', icon: '🌙', color: '#00B42A', articleCount: 0 },
];

const tags = [
  { id: '1', name: '教程', articleCount: 0 },
  { id: '2', name: '故障排查', articleCount: 0 },
  { id: '3', name: '对比评测', articleCount: 0 },
];

export default function CategoriesPage() {
  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <Title heading={3} className="!mb-0">分类与标签</Title>
        <Space>
          <Button type="primary" icon={<Plus size={16} />}>
            新建分类
          </Button>
          <Button icon={<TagIcon size={16} />}>
            新建标签
          </Button>
        </Space>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 分类管理 */}
        <Card title="文章分类">
          <Table
            data={categories}
            rowKey="id"
            columns={[
              {
                title: '分类',
                render: (_, record) => (
                  <div className="flex items-center gap-2">
                    <span className="text-xl">{record.icon}</span>
                    <span className="font-medium">{record.name}</span>
                  </div>
                ),
              },
              {
                title: '标识',
                dataIndex: 'slug',
                width: 120,
              },
              {
                title: '文章数',
                dataIndex: 'articleCount',
                width: 80,
                render: (count) => <Tag color="gray">{count}</Tag>,
              },
              {
                title: '操作',
                width: 120,
                render: () => (
                  <Space>
                    <Button type="text" icon={<Pencil size={16} />} size="small" />
                    <Button type="text" status="danger" icon={<Trash2 size={16} />} size="small" />
                  </Space>
                ),
              },
            ]}
          />
        </Card>

        {/* 标签管理 */}
        <Card title="文章标签">
          <div className="mb-4">
            <Input.Search placeholder="搜索标签..." />
          </div>
          <div className="flex flex-wrap gap-2">
            {tags.map((tag) => (
              <Tag key={tag.id} closable className="px-3 py-1">
                {tag.name} ({tag.articleCount})
              </Tag>
            ))}
          </div>
          <Empty className="mt-8" description="点击上方按钮添加新标签" />
        </Card>
      </div>
    </div>
  );
}
