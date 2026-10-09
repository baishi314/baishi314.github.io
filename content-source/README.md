# 写文章 / 改内容 —— 使用说明

三套站点（极简笔记 / 二次元小屋 / 星辉小屋）的内容**只有一份源**，就在这个
`content-source/` 目录里。改这里，跑一次同步脚本，三个站一起变。

---

## 一、写新文章（最常用）

**双击项目根目录的 `发布.bat`**，然后按提示填：

```
标题: 我的第一篇技术笔记
日期时间 [2026-10-09 10:30:00]:        ← 直接回车用当前时间
标签（多个用逗号隔开，可留空）: Python, 笔记
分类（单个词，可留空）: 学习
摘要（一句话，可留空）: 记录一下踩的坑
要置顶吗 (y/n) [n]:                    ← 回车 = 不置顶
封面图地址（可留空用默认图）:            ← 回车 = 用默认图
英文短名（用 - 连接，如 my-first-post）: python-notes
```

填完后会**自动打开记事本**，在里面写正文（普通 Markdown 就行），
**保存 + 关掉记事本**，回到黑窗口按回车。

接下来它会自动：同步三站 → 本地构建检查 → 提交 → 推送。

**约 2 分钟后**，三个站都会有这篇文章：

- https://baishi314.github.io/minimal/
- https://baishi314.github.io/anime/
- https://baishi314.github.io/xinghui/

---

## 二、为什么要填「英文短名」

文章的文件名会变成网址，比如 `pipeline-test` 对应：

```
https://baishi314.github.io/minimal/posts/pipeline-test/
```

中文标题不能直接当文件名 —— Next.js 会把中文做 URL 编码后再去找文件，
直接构建失败。所以文件名统一用英文，**标题照旧写中文，不影响显示**。

---

## 三、改已有文章

直接编辑 `content-source/posts/` 里的 `.md` 文件，然后双击 `发布.bat`
（它会问你想不想新建 —— 直接回车跳过那一步的方法见下），或者手动：

```bash
python content-source/sync-content.py
git add -A && git commit -m "更新文章" && git push
```

想删文章：把 `content-source/posts/` 里对应的 `.md` 删掉，再同步一次，
三站会一起消失。

---

## 四、改「关于我 / 资源导航 / 项目 / 友链」

这些不是 Markdown，是 JSON，在 `content-source/` 下：

| 文件 | 管什么 |
|---|---|
| `profile.json` | 关于我：自我介绍、技能栈、联系方式 |
| `projects.json` | 项目作品列表 |
| `resources.json` | 资源导航（置顶那篇的全部链接） |

改完跑一次 `python content-source/sync-content.py` 就行。

> `profile.json` 里的技能栈是 `[["分类名", ["技能1", "技能2"]], ...]`，
> `resources.json` 里的链接是 `["名称", "一句话说明", "网址", "链接文字"]`。

---

## 五、文章能用的字段

写在 `.md` 文件最顶上，两个 `---` 之间：

```yaml
---
title: "文章标题"              # 必填
date: 2026-10-09 15:30:00      # 必填，按这个排序
tags: ["标签1", "标签2"]        # 可空
category: "日常"                # 可空
summary: "一句话摘要"           # 可空，显示在列表页
pinned: false                  # true = 置顶
draft: false                   # true = 不发布
cover: ""                      # 封面图，空着用默认图
---
```

**注意**：统一写 `summary` / `date` / `tags` 就行，不用管各站的差异 ——
极简站要的 `summary`、二次元站要的 `published`、`description`，
同步脚本会自动转换。

---

## 六、本地预览（发布前想看效果）

双击 `预览.bat`，选 1 / 2 / 3 选一个站，会自动打开浏览器预览。

**只同步 + 本地构建，不会推送**，随便试。

---

## 七、出问题了怎么办

**发布失败 / 文章没出现**：
1. 打开 https://github.com/baishi314/baishi314.github.io/actions
2. 看最近一条 `Build and Deploy Sites` 是不是红的
3. 红的就点进去，找报错那一步

**提交了但想撤销**：
```bash
git log --oneline -5          # 找到要回退到的那条
git revert <那条的哈希>       # 生成一个反向提交（安全，不改历史）
git push
```

**同步脚本报错**：多半是 JSON 格式写错了（少个逗号、多个逗号）。
把报错信息发我，或者用在线 JSON 校验器检查。

---

## 八、文件清单

```
content-source/
├── posts/               ← 你写的文章都放这
│   ├── hello-writing.md     示例（可以删）
│   ├── hello-world.md       开站文（按主题微调）
│   └── resources.md         置顶资源导航
├── profile.json         ← 关于我
├── projects.json        ← 项目作品
├── resources.json       ← 资源导航的链接数据
├── newpost.py           ← 新建文章向导
└── sync-content.py      ← 同步脚本（核心）

发布.bat                 ← 双击发布
预览.bat                 ← 双击本地预览
```

---

## 九、几个约定

- **别手改生成出来的文件**：`minimal-src/`、`anime-src/src/content/`、
  `xinghui-src/posts/` 里的内容会被同步脚本**覆盖**。要改就改
  `content-source/` 里的源。
- 唯一例外：`anime-src/src/config/*`、`xinghui-src/siteConfig.ts` 这类
  站点配置不在同步范围内，可以直接改。
- `resources.md` / `hello-world.md` / `welcome.md` 这三篇由脚本按主题
  生成，**不要放进 `content-source/posts/`**（同名会被忽略）。
