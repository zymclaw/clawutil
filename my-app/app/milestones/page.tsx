'use client';

import { useState } from 'react';
import { Layout, Button, Typography, Space, Spin, Message } from '@arco-design/web-react';
import { 
  ArrowLeft, 
  ExternalLink, 
  RefreshCw,
  Maximize2,
  Minimize2
} from 'lucide-react';
import Link from 'next/link';

const { Header, Content } = Layout;
const { Title, Text } = Typography;

export default function MilestonesPage() {
  const [loading, setLoading] = useState(true);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [key, setKey] = useState(0); // 用于刷新 iframe

  const handleRefresh = () => {
    setLoading(true);
    setKey(prev => prev + 1);
    Message.success('页面已刷新');
  };

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen();
      setIsFullscreen(true);
    } else {
      document.exitFullscreen();
      setIsFullscreen(false);
    }
  };

  return (
    <Layout className="min-h-screen bg-gray-50">
      {/* 顶部导航栏 */}
      <Header className="bg-white shadow-sm sticky top-0 z-50 h-16">
        <div className="max-w-full mx-auto px-4 h-full flex items-center justify-between">
          <Space>
            <Link href="/">
              <Button type="text" icon={<ArrowLeft size={18} />}>
                返回首页
              </Button>
            </Link>
            <div className="h-6 w-px bg-gray-200 mx-2" />
            <span className="text-2xl">🦞</span>
            <Title heading={5} className="!mb-0 hidden sm:block">ClawUtil</Title>
          </Space>

          <Space>
            <Text type="secondary" className="hidden md:block">
              AI 发展里程碑时间线
            </Text>
            <div className="h-6 w-px bg-gray-200 mx-2" />
            <Button 
              type="text" 
              icon={<RefreshCw size={16} />}
              onClick={handleRefresh}
            >
              刷新
            </Button>
            <Button 
              type="text" 
              icon={isFullscreen ? <Minimize2 size={16} /> : <Maximize2 size={16} />}
              onClick={toggleFullscreen}
            >
              {isFullscreen ? '退出全屏' : '全屏'}
            </Button>
            <a 
              href="/clawutil/milestones/index.html" 
              target="_blank" 
              rel="noopener noreferrer"
            >
              <Button type="text" icon={<ExternalLink size={16} />}>
                新窗口打开
              </Button>
            </a>
          </Space>
        </div>
      </Header>

      {/* iframe 容器 */}
      <Content className="relative p-0">
        {loading && (
          <div className="absolute inset-0 flex flex-col items-center justify-center bg-white z-10">
            <Spin size={40} />
            <Text className="mt-4 text-gray-500">正在加载里程碑...</Text>
          </div>
        )}
        
        <iframe
          key={key}
          src="/clawutil/milestones/index.html"
          className="w-full border-0"
          style={{ 
            height: 'calc(100vh - 64px)',
            display: loading ? 'none' : 'block'
          }}
          onLoad={() => setLoading(false)}
          allow="fullscreen"
          title="AI 发展里程碑时间线"
        />
      </Content>
    </Layout>
  );
}
