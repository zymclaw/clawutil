export interface Article {
  id: string;
  slug: string;
  title: string;
  summary: string | null;
  content: string;
  htmlContent: string | null;
  type: ArticleType;
  status: Status;
  publishDate: Date | null;
  createdAt: Date;
  updatedAt: Date;
  viewCount: number;
  readTime: number | null;
  categoryId: string | null;
  category: Category | null;
  tags: Tag[];
  coverImage: string | null;
  metaDesc: string | null;
}

export interface Category {
  id: string;
  slug: string;
  name: string;
  description: string | null;
  icon: string | null;
  color: string | null;
  sortOrder: number;
  articles: Article[];
  createdAt: Date;
  updatedAt: Date;
}

export interface Tag {
  id: string;
  name: string;
  color: string | null;
  articles: Article[];
  createdAt: Date;
}

export type ArticleType = 'DAILY' | 'WIKI' | 'COMPARE' | 'WORKFLOW' | 'WEEKLY';
export type Status = 'DRAFT' | 'PUBLISHED' | 'ARCHIVED';

export const ArticleTypeLabels: Record<ArticleType, string> = {
  DAILY: '日报',
  WIKI: '百科',
  COMPARE: '对比',
  WORKFLOW: '工作流',
  WEEKLY: '周报',
};

export const ArticleTypeColors: Record<ArticleType, string> = {
  DAILY: '#165DFF',
  WIKI: '#00B42A',
  COMPARE: '#FF7D00',
  WORKFLOW: '#722ED1',
  WEEKLY: '#F5319D',
};

export const StatusLabels: Record<Status, string> = {
  DRAFT: '草稿',
  PUBLISHED: '已发布',
  ARCHIVED: '归档',
};
