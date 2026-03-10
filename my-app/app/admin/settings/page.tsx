'use client';

import { Card, Form, Input, Button, Switch, Typography, Message, Tabs } from '@arco-design/web-react';
import { Save, User, Globe, Bell } from 'lucide-react';

const { Title } = Typography;
const TabPane = Tabs.TabPane;

export default function SettingsPage() {
  const [form] = Form.useForm();

  const handleSave = () => {
    Message.success('设置已保存');
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <Title heading={3} className="!mb-0">系统设置</Title>
        <Button type="primary" icon={<Save size={16} />} onClick={handleSave}>
          保存设置
        </Button>
      </div>

      <Tabs defaultActiveTab="basic">
        <TabPane key="basic" title={<span><User size={14} className="inline mr-1" /> 基本信息</span>}>
          <Card className="max-w-2xl">
            <Form form={form} layout="vertical">
              <Form.Item label="博客名称" field="siteName" initialValue="ClawUtil">
                <Input placeholder="输入博客名称" />
              </Form.Item>
              
              <Form.Item label="博客描述" field="siteDesc" initialValue="探索 AI 工具的每一天">
                <Input.TextArea placeholder="输入博客描述" rows={3} />
              </Form.Item>
              
              <Form.Item label="作者名称" field="author" initialValue="zym">
                <Input placeholder="输入作者名称" />
              </Form.Item>
              
              <Form.Item label="GitHub 链接" field="github" initialValue="https://github.com/zymclaw">
                <Input placeholder="输入 GitHub 链接" />
              </Form.Item>
            </Form>
          </Card>
        </TabPane>

        <TabPane key="seo" title={<span><Globe size={14} className="inline mr-1" /> SEO 设置</span>}>
          <Card className="max-w-2xl">
            <Form layout="vertical">
              <Form.Item label="网站标题后缀" field="titleSuffix" initialValue="| ClawUtil">
                <Input placeholder="输入标题后缀" />
              </Form.Item>
              
              <Form.Item label="SEO 关键词" field="keywords" initialValue="AI, OpenClaw, Claude, Kimi">
                <Input placeholder="输入关键词，用逗号分隔" />
              </Form.Item>
              
              <Form.Item label="网站图标 URL" field="favicon">
                <Input placeholder="输入 favicon URL" />
              </Form.Item>
            </Form>
          </Card>
        </TabPane>

        <TabPane key="features" title={<span><Bell size={14} className="inline mr-1" /> 功能开关</span>}>
          <Card className="max-w-2xl">
            <div className="space-y-6">
              <div className="flex items-center justify-between py-4 border-b border-gray-100">
                <div>
                  <div className="font-medium">文章评论</div>
                  <div className="text-sm text-gray-500">允许读者在文章下方发表评论</div>
                </div>
                <Switch />
              </div>
              
              <div className="flex items-center justify-between py-4 border-b border-gray-100">
                <div>
                  <div className="font-medium">文章统计</div>
                  <div className="text-sm text-gray-500">显示文章阅读量和点赞数</div>
                </div>
                <Switch defaultChecked />
              </div>
              
              <div className="flex items-center justify-between py-4 border-b border-gray-100">
                <div>
                  <div className="font-medium">RSS 订阅</div>
                  <div className="text-sm text-gray-500">开启 RSS 订阅功能</div>
                </div>
                <Switch defaultChecked />
              </div>
              
              <div className="flex items-center justify-between py-4">
                <div>
                  <div className="font-medium">暗黑模式</div>
                  <div className="text-sm text-gray-500">允许用户切换暗黑模式</div>
                </div>
                <Switch />
              </div>
            </div>
          </Card>
        </TabPane>
      </Tabs>
    </div>
  );
}
