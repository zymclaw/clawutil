import type { Metadata } from 'next';
import '@arco-design/web-react/dist/css/arco.css';
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
      <head>
        <style dangerouslySetInnerHTML={{
          __html: `
            /* Arco Design Button Alignment Fix */
            .arco-btn {
              display: inline-flex !important;
              align-items: center !important;
              justify-content: center !important;
              gap: 6px !important;
            }
            .arco-btn svg,
            .arco-btn .lucide {
              flex-shrink: 0 !important;
              width: 16px !important;
              height: 16px !important;
            }
            /* Arco Card Radius */
            .arco-card {
              border-radius: 8px !important;
            }
            /* Arco Layout Background */
            .arco-layout {
              background: #f7f8fa !important;
            }
          `
        }} />
      </head>
      <body>{children}</body>
    </html>
  );
}
