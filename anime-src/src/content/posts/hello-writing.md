---
title: 示例：你可以这样写文章
published: 2026-10-08 10:00:00
description: 这行摘要会同步到三站，极简站叫 summary，另两站叫 description，你不用管。
tags: [示例, 说明]
category: 日常
draft: false
comment: true
---
## 写文章的规矩只有一条

**在 `content-source/posts/` 里放一个 `.md` 文件就行。**

三套站点的 frontmatter 差异（`date` / `published`、`summary` / `description`、
`tags` + `categories` / 只 `tags`）由同步脚本自动处理，你不用记。

---

## 顶部那几个字段

| 字段 | 必填 | 说明 |
|---|---|---|
| `title` | 是 | 文章标题 |
| `date` | 是 | 写成 `2026-10-08 10:00:00` 就会按当天排序 |
| `tags` | 否 | 标签，数组，如 `["Python", "笔记"]` |
| `category` | 否 | 分类，单个词，如 `"日常"` |
| `summary` | 否 | 一句话摘要，会显示在文章列表里 |
| `pinned` | 否 | 填 `true` 就置顶 |
| `draft` | 否 | 填 `true` 就不发布（草稿） |
| `cover` | 否 | 封面图地址，留空用默认图 |

---

## 正文就是普通 Markdown

### 支持表格

| 语言 | 用途 |
|---|---|
| Python | 脚本、自动化 |
| JavaScript | 前端 |
| Java | 课程 |

### 支持代码块

```python
def hello(name: str) -> str:
    return f"你好，{name}"
```

### 支持引用、列表、链接

> 引用会长这样。

- 有序列表
- 无序列表
- [超链接](https://baishi314.github.io/)

---

## 写完怎么发布

双击项目根目录的 **`发布.bat`**，按提示输入标题就行。

它会自动：建文件 → 同步三站 → 本地构建检查 → 提交 → 推送。

大约 2 分钟后，三套站点的首页都会出现这篇文章。
