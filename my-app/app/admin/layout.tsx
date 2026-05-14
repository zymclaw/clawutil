'use client';

import { Layout, Menu, Button, Space, Avatar, Typography } from '@arco-design/web-react';
import {
  LayoutDashboard,
  FileText,
  Tag,
  Settings,
  Menu as MenuIcon,
  X,
  Home,
} from 'lucide-react';
import Link from 'next/link';
import { useState } from 'react';

const { Sider, Header, Content } = Layout;
const { Title } = Typography;

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [collapsed, setCollapsed] = useState(false);

  const menuItems = [
    {
      key: '/admin',
      icon: <LayoutDashboard size={18} />,
      title: '概览',
    },
    {
      key: '/admin/articles',
      icon: <FileText size={18} />,
      title: '文章管理',
    },
    {
      key: '/admin/categories',
      icon: <Tag size={18} />,
      title: '分类标签',
    },
    {
      key: '/admin/settings',
      icon: <Settings size={18} />,
      title: '系统设置',
    },
  ];

  return (
    <Layout className="min-h-screen">
      <Sider
        trigger={null}
        collapsible
        collapsed={collapsed}
        breakpoint="lg"
        className="bg-white shadow-md"
        style={{ position: 'fixed', height: '100vh', left: 0, top: 0, zIndex: 100 }}
      >
        <div className="h-16 flex items-center justify-center border-b border-gray-100">
          <Link href="/" className="flex items-center gap-2">
            <span className="text-2xl">🦞</span>
            {!collapsed && <Title heading={6} className="!mb-0">ClawUtil</Title>}
          </Link>
        </div>
        
        <Menu
          defaultSelectedKeys={['/admin']}
          style={{ width: '100%' }}
          className="border-r-0"
        >
          {menuItems.map((item) => (
            <Menu.Item key={item.key}>
              <Link href={item.key} className="flex items-center gap-2">
                {item.icon}
                {!collapsed && <span>{item.title}</span>}
              </Link>
            </Menu.Item>
          ))}
        </Menu>
      </Sider>

      <Layout style={{ marginLeft: collapsed ? 80 : 200, transition: 'all 0.2s' }}>
        <Header className="bg-white shadow-sm sticky top-0 z-50 px-6 flex items-center justify-between">
          <Space>
            <Button
              type="text"
              icon={collapsed ? <MenuIcon size={18} /> : <X size={18} />}
              onClick={() => setCollapsed(!collapsed)}
            />
            <Link href="/">
              <Button type="text" icon={<Home size={18} />}>
                返回首页
              </Button>
            </Link>
          </Space>
          
          <Space>
            <span className="text-gray-500">zym</span>
            <Avatar size={32}>Z</Avatar>
          </Space>
        </Header>

        <Content className="p-6 bg-gray-50 min-h-[calc(100vh-64px)]">
          {children}
        </Content>
      </Layout>
    </Layout>
  );
}
