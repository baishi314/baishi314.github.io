# 星辉小屋（xinghui）

baishi314 个人站的第三套主题，面板式首页 + 在线音乐 + 猫猫助手。

## 来源

风格移植自开源项目 [XinghuisamaBlogs](https://github.com/heiehiehi/XinghuisamaBlogs)
（原作者 XingHuiSama，授权协议 CC BY-NC 4.0）。
感谢原作者的设计。

## 本仓库做了什么

原项目靠 Vercel 服务端跑 API，这里改成**纯静态**，能直接托管 GitHub Pages：

| 原实现 | 改成 |
| --- | --- |
| `output: 'export'` 被注释 | 启用静态导出，删除全部 5 个 API 路由 |
| AI 猫助手（Gemini） | 本地词库匹配（Key 放前端会泄露） |
| 和风天气 API（需 Key） | wttr.in 免 Key 接口 |
| 网易云音乐后端代理 | 前端直连 Meting 镜像 |
| Gitalk（需服务端代理） | Giscus（无后端） |
| `next/font/google` | 系统字体栈（避免构建期联网） |

另外新增 `lib/asset.ts` 的 `withBase()`，支持 `/xinghui` 子路径部署。

## 本地开发

```bash
pnpm install
pnpm dev            # 开发预览

# 静态构建（产物在 out/）
BASE_PATH=/xinghui pnpm build
```

## 目录

- `posts/` 文章（Markdown，带 frontmatter）
- `chatters/` 杂谈
- `moments/` 说说
- `data/` 项目 / 友链 / 相册
- `siteConfig.ts` 全站配置
- `app/about/about.md` 关于我
