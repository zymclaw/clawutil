import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'ClawUtil - 探索 AI 工具的每一天',
  description: '个人 AI 技术博客，记录 OpenClaw、Claude Code、Kimi 等工具的使用经验',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
