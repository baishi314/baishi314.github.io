// 子路径部署时给本地静态资源（以 "/" 开头且非 "//"）补上 basePath；外部 http(s) 链接原样返回
const BP = process.env.NEXT_PUBLIC_BASE_PATH || '';

export function withBase(src?: string | null): string {
  if (!src) return '';
  if (/^(https?:)?\/\//i.test(src) || src.startsWith('data:')) return src;
  if (!src.startsWith('/')) return src;
  if (BP && src.startsWith(BP + '/')) return src;
  return BP + src;
}
