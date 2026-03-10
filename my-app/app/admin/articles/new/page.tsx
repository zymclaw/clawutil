'use client';

import { useState } from 'react';
import { 
  Card, 
  Button, 
  Input, 
  Select, 
  Typography, 
  Space, 
  InputTag,
  Message,
  Grid,
  Tabs
} from '@arco-design/web-react';
import { Save, Eye, Send } from 'lucide-react';
import MDEditor from '@uiw/react-md-editor';
import { ArticleTypeLabels, type ArticleType, type Status } from '@/types';
import { calculateReadTime } from '@/lib/utils';

const { Title } = Typography;
const { Row, Col } = Grid;
const TabPane = Tabs.TabPane;

const typeOptions = Object.entries(ArticleTypeLabels).map(([value, label]) => ({
  value,
  label,
}));

const statusOptions = [
  { value: 'DRAFT', label: '草稿' },
  { value: 'PUBLISHED', label: '立即发布' },
];

export default function NewArticlePage() {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('# 开始写作...\n\n');
  const [type, setType] = useState<ArticleType>('DAILY');
  const [tags, setTags] = useState<string[]>([]);
  const [status, setStatus] = useState<Status>('DRAFT');
  const [saving, setSaving] = useState(false);

  const readTime = calculateReadTime(content);
  const wordCount = content.length;

  const handleSave = async () => {
    if (!title.trim()) {
      Message.warning('请输入文章标题');
      return;
    }

    setSaving(true);
    
    // MVP 阶段先模拟保存
    setTimeout(() => {
      Message.success(`文章已保存为${status === 'PUBLISHED' ? '并发布' : '草稿'}`);
      setSaving(false);
    }, 1000);
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <Title heading={3} className="!mb-0">新建文章</Title>
        <Space>
          <Button icon={<Eye size={16} />}>预览</Button>
          <Button 
            type="primary" 
            icon={<Save size={16} />} 
            loading={saving}
            onClick={handleSave}
          >
            保存
          </Button>
        </Space>
      </div>

      <Row gutter={16}>
        <Col xs={24} lg={16}>
          <Card className="mb-4">
            <Input
              placeholder="输入文章标题..."
              size="large"
              value={title}
              onChange={setTitle}
              className="!text-xl !font-semibold !mb-4"
              style={{ border: 'none', padding: 0, background: 'transparent' }}
            />

            <Tabs defaultActiveTab="edit">
              <TabPane key="edit" title="编辑">
                <div style={{ height: 'calc(100vh - 400px)', minHeight: 400 }}>
                  <MDEditor
                    value={content}
                    onChange={(val) => setContent(val || '')}
                    height="100%"
                    preview="edit"
                  />
                </div>
              </TabPane>
              <TabPane key="split" title="分屏预览">
                <div style={{ height: 'calc(100vh - 400px)', minHeight: 400 }}>
                  <MDEditor
                    value={content}
                    onChange={(val) => setContent(val || '')}
                    height="100%"
                    preview="live"
                  />
                </div>
              </TabPane>
              <TabPane key="preview" title="预览">
                <div 
                  className="markdown-body p-6 bg-white rounded"
                  style={{ height: 'calc(100vh - 400px)', minHeight: 400, overflow: 'auto' }}
                >
                  <MDEditor.Markdown source={content} />
                </div>
              </TabPane>
            </Tabs>
          </Card>

          <div className="flex items-center justify-between text-sm text-gray-500">
            <span>💡 提示：支持从飞书、Notion、Word 直接粘贴富文本</span>
            <span>{wordCount.toLocaleString()} 字 · 预计 {readTime} 分钟阅读</span>
          </div>
        </Col>

        <Col xs={24} lg={8}>
          <Space direction="vertical" className="w-full" size="medium">
            <Card title="发布设置">
              <Space direction="vertical" className="w-full">
                <div>
                  <div className="text-sm text-gray-600 mb-2">文章类型</div>
                  <Select
                    value={type}
                    onChange={setType}
                    options={typeOptions}
                    className="w-full"
                  />
                </div>

                <div>
                  <div className="text-sm text-gray-600 mb-2">标签</div>
                  <InputTag
                    value={tags}
                    onChange={setTags}
                    placeholder="添加标签，按回车确认"
                    className="w-full"
                  />
                </div>

                <div>
                  <div className="text-sm text-gray-600 mb-2">发布状态</div>
                  <Select
                    value={status}
                    onChange={setStatus}
                    options={statusOptions}
                    className="w-full"
                  />
                </div>

                <Button 
                  type="primary" 
                  long 
                  icon={<Send size={16} />}
                  loading={saving}
                  onClick={handleSave}
                >
                  {status === 'PUBLISHED' ? '立即发布' : '保存草稿'}
                </Button>
              </Space>
            </Card>

            <Card title="封面图片">
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-500 transition-colors cursor-pointer">
                <div className="text-4xl mb-2">🖼️</div>
                <div className="text-gray-500">点击或拖拽上传封面</div>
                <div className="text-xs text-gray-400 mt-1">支持 JPG、PNG 格式</div>
              </div>
            </Card>

            <Card title="文章信息">
              <Space direction="vertical" className="w-full text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-500">字数</span>
                  <span>{wordCount.toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">预计阅读</span>
                  <span>{readTime} 分钟</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">状态</span>
                  <span>{status === 'DRAFT' ? '草稿' : '已发布'}</span>
                </div>
              </Space>
            </Card>
          </Space>
        </Col>
      </Row>
    </div>
  );
}
