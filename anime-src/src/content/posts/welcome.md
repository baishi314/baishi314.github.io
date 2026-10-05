---
title: 欢迎来到二次元小屋
published: 2026-10-05
description: 这个版本的博客用了 Firefly 主题，记录一下怎么搭起来的。
tags: [Astro, 博客]
category: 折腾记录
draft: false
---

这是「风格大厅」里的第二个版本，用的是开源的 **Firefly** 主题。

## 为什么是它

看了一圈静态博客主题，最后选了 Firefly：

- **Astro 构建** —— 输出纯静态，GitHub Pages 能直接托管
- **中文原生** —— 文档、界面都是中文，出问题搜得到答案
- **功能齐** —— 搜索、评论、目录、代码高亮、看板娘都自带

## 怎么部署的

关键是子路径部署。这套主题默认部署在域名根目录，但我的站点结构是：

```
baishi314.github.io/          ← 风格大厅
baishi314.github.io/minimal/  ← PaperMod 版本
baishi314.github.io/anime/    ← 这个版本
```

所以要改配置里的 `base`：

```js
// astro.config.mjs
base: process.env.BASE_PATH || "/",
```

构建时传环境变量：

```bash
BASE_PATH=/anime/ pnpm build
```

## 还会加别的吗

可能会。多一套风格就多一套维护成本，先把这两套跑稳再说。
