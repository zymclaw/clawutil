/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  distDir: 'dist',
  basePath: '/clawutil',
  assetPrefix: '/clawutil',
  images: {
    unoptimized: true,
  },
  trailingSlash: true,
  transpilePackages: ['@arco-design/web-react'],
};

export default nextConfig;
