---
title: "🔗 常用资源导航"
date: 2026-10-09
draft: false
tags: ["资源", "导航"]
categories: ["导航"]
summary: "141 个亲测能打开的网站，每个都用一句话说清「是干什么的」，点一下就能进。"
ShowToc: true
TocOpen: true
weight: 1
pin: true
---

> **这篇会一直置顶。** 找不到东西的时候，先来这里翻。
> 每一条都是**实际点开验证过**的，挂了就换掉。按「想干什么」分好类了——**想学什么就直接点哪个**。

---

## 📚 编程 & 计算机

| 网站 | 是什么 | 直接进 |
|---|---|---|
| **东秦计科人生存手册** | 学长写的新生避坑指南：Git 怎么用、Vim 怎么入门、算法从哪开始、保研怎么准备，还有龙芯实验室的招新介绍。新生强烈建议先翻一遍 | [manual.shettydev.com](https://manual.shettydev.com/loongson/) |
| **菜鸟教程** | 查语法用的总入口：C、C++、Java、Python、SQL、HTML、JS 都有例子，还能在线跑一段试试。写代码时突然想不起某个语法怎么写，来这搜最快 | [runoob.com](https://www.runoob.com/) |
| **CS 自学指南** | 国内最出名的计算机自学路线图，把 MIT、伯克利、CMU 的公开课按难度排好了。不知道从哪学起，从这一本开始 | [csdiy.wiki](https://csdiy.wiki/) |
| **CS 61A** | 伯克利最经典的程序设计入门课官网，有全套讲义和作业。想体验国外名校计算机第一课，做这个 | [cs61a.org](https://cs61a.org/) |
| **你缺计** | 写给非计算机专业的计算机通识课，讲原理不讲八股。文科生也能看懂的那类 | [criwits.top](https://www.criwits.top/missing/) |
| **Ac-Wiki** | 大学生经验百科，学习、科研、竞赛、升学的问题基本都有人写过答案 | [ac-wiki.org](https://ac-wiki.org/) |
| **Missing Semester** | MIT 开的「你大学不会教但一定要会」的课：命令行、编辑器、调试、版本控制、数据整理。全程干货、不废话，刚学编程时看完能少走很多弯路 | [missing.csail.mit.edu](https://missing.csail.mit.edu/) |
| **Crash Course 计算机科学** | 8 小时把计算机科学全貌讲一遍的科普视频：计算机怎么来的、内部怎么运作、有哪些核心思想。开学前想对专业有个整体印象，看这个 | [去 B 站看](https://www.bilibili.com/video/BV1EW411u7th) |
| **Linux 101** | 中国科大学生写的 Linux 入门讲义，从装系统、命令行讲到服务器运维。想在 Linux 上正经学点东西，这本来路很清楚 | [lug.ustc.edu.cn](https://101.lug.ustc.edu.cn/) |

---

## 🤖 AI 学习

| 网站 | 是什么 | 直接进 |
|---|---|---|
| **从零开始的 AI 学习** | 帝国理工计算机博士做的 AI 科普系列，先讲「AI 这三年发生了什么」，再讲「为什么你写不好提示词」。不炒概念、不卖课，从生活例子讲起，20 分钟能看完 | [看第 1 集](https://www.bilibili.com/video/BV1TDGT6vEqC/) |
| **为什么你写不好提示词** | 同一个需求换个说法，AI 输出天差地别。这集用一个小实验演示提示词的威力，把 Agent、Harness 这些唬人新词拨开，只讲最该先掌握的提示词 | [看这集](https://www.bilibili.com/video/BV1VrGu6JEqk/) |
| **PyTorch 官方教程** | 深度学习框架 PyTorch 的官方教程集：从张量、自动求导讲到训练一个完整网络，每篇都能直接跑。装完框架第一站就来这 | [pytorch.org](https://pytorch.org/tutorials/) |
| **动手学深度学习** | 李沐等人写的开源书，中文免费，讲完理论立刻给可运行的代码，还配了视频课。不想只抄代码的话，从这本打底 | [zh.d2l.ai](https://zh.d2l.ai/) |

---

## 🤖 AI Agent 工具

### 终端 Agent（在命令行里干活）

| 网站 | 是什么 | 直接进 |
|---|---|---|
| **Claude Code** | Anthropic 官方的终端 agent：在项目目录里敲 claude，它能读整个代码库、直接改文件、跑命令自查。Windows 原生支持，装完先配 key | [claude.com](https://claude.com/product/claude-code) |
| **Codex CLI** | OpenAI 官方命令行 agent，Rust 写的，启动比 Node 版快一截，支持沙箱执行和「先给方案再动手」。装法 npm i -g @openai/codex | [GitHub](https://github.com/openai/codex) |
| **Gemini CLI** | Google 的终端 agent，用 Google 账号登录就有很大的免费额度，个人写代码基本不花钱。开源，可自己改 | [GitHub](https://github.com/google-gemini/gemini-cli) |
| **Qwen Code** | 阿里通义的终端 agent，从 Gemini CLI 分叉改的，直接接通义千问模型，国内网络不用翻墙。装法 npm i -g @qwen-code/qwen-code | [GitHub](https://github.com/QwenLM/qwen-code) |
| **Aider** | 最老牌的结对编程工具之一：你改一处、它跟着补全，每次改动自动 git commit，改坏了直接回滚。几乎任何模型都能接，包括本地 Ollama | [aider.chat](https://aider.chat/) |
| **OpenCode** | 开源终端 agent，TUI 界面，模型随便换（OpenAI 兼容的都行），不绑定厂商。Windows 上 npm i -g opencode-ai 就能跑 | [opencode.ai](https://opencode.ai/) |
| **Crush** | Charm 团队（做 glow、lazygit 那批人）出的终端 agent，界面好看、Go 写的、启动快。嫌别家终端界面丑的可以试它 | [GitHub](https://github.com/charmbracelet/crush) |
| **Continue CLI** | 开源的 IDE 插件加命令行，最大特点是能完全接本地模型，代码不出本机。公司不让把代码传到云端时用它 | [continue.dev](https://continue.dev/) |

### 编辑器 / IDE 里用

| 网站 | 是什么 | 直接进 |
|---|---|---|
| **Cursor** | 把 AI 直接做进编辑器：能读整个项目、按一句话改多个文件，比在网页里贴代码顺手。免费版够上手，学生认证有优惠 | [cursor.com](https://cursor.com/) |
| **Cline** | VS Code 里的 agent 插件，装完侧边栏点一下就开始改文件，每一步想干什么都先弹出来问你同不同意。新手看着它干活学得最快 | [cline.bot](https://cline.bot/) |
| **Roo Code** | Cline 的多模式版本：写代码、做架构、调试各一套提示词，长任务不容易跑偏。也是 VS Code 插件，免费开源 | [roocode.com](https://roocode.com/) |

### 在自己电脑上跑模型

| 网站 | 是什么 | 直接进 |
|---|---|---|
| **Ollama** | 一条 ollama run qwen3:8b 就在本机跑起开源模型，还能开 OpenAI 兼容端口让上面那些 agent 接它当后端，一分钱不花 | [ollama.com](https://ollama.com/) |
| **LM Studio** | 图形界面的本地模型客户端：搜模型、下载、聊天、开兼容 API 全在窗口里点。不想碰命令行的话比 Ollama 省事 | [lmstudio.ai](https://lmstudio.ai/) |

### MCP 协议 & 自己写 Agent

| 网站 | 是什么 | 直接进 |
|---|---|---|
| **MCP 官方文档** | 让 AI 接上你的文件、数据库、浏览器的那套通用协议。Claude Code、Codex、Cline 现在都支持，想给 agent 加能力先看这 | [modelcontextprotocol.io](https://modelcontextprotocol.io/) |
| **awesome-mcp-servers** | 社区整理的 MCP 服务器大全，按用途分好类：连 GitHub、查数据库、控浏览器、读本地文件。想让 agent 干某件事，先来这搜有没有现成的 | [GitHub](https://github.com/punkpeye/awesome-mcp-servers) |
| **Pydantic AI** | Python 的 agent 框架，写法跟普通异步函数几乎一样，但会校验模型返回的结构。自己动手写 agent，从这入门最不容易被抽象层绕晕 | [ai.pydantic.dev](https://ai.pydantic.dev/) |
| **AutoGen** | 微软的多 agent 框架：几个 agent 各干一块、互相讨论，最后拼出结果。想做「一个写代码、一个审代码」这种组合来看它 | [GitHub](https://github.com/microsoft/autogen) |

### Windows 一键装

| 网站 | 是什么 | 直接进 |
|---|---|---|
| **AI Agent 一键安装器** | 上面这些命令行工具在 Windows 上要一个个配 Node、Python、环境变量，很折腾。这个 bat 双击就有菜单：自动装 Node/pnpm/uv，批量装各组 CLI，写 API 环境变量，清掉失效代理。附配套教程 | [下载 .bat](https://github.com/baishi314/baishi314.github.io/raw/main/tools/install-agent-cli.bat) |

---

## 💻 编程语言

### C 语言

| 网站 | 是什么 | 直接进 |
|---|---|---|
| **菜鸟教程 C 语言** | 查语法用的网站，从变量、循环到指针都有例子。不用通读，写代码时忘了什么查什么 | [runoob.com](https://www.runoob.com/cprogramming/c-tutorial.html) |
| **C 语言中文网** | 比菜鸟更细的 C 语言教程，二十多万字，配合课程查漏补缺正合适。免费看，有广告 | [biancheng.net](https://c.biancheng.net/c/) |
| **翁恺《C 语言程序设计》** | 浙江大学翁恺老师的名课，讲得清楚、节奏舒服，很多人大学第一门编程课就看这个 | [去 MOOC 搜课名](https://www.icourse163.org/) |
| **PTA 程序设计平台** | 很多学校的程序实验就是在这里交的。题目偏基础，适合边上课边刷 | [pintia.cn](https://pintia.cn/) |

### C++

| 网站 | 是什么 | 直接进 |
|---|---|---|
| **菜鸟教程 C++** | C++ 入门，重点讲清楚类和对象——这是从 C 跨到 C++ 最难的一步 | [runoob.com](https://www.runoob.com/cplusplus/cpp-tutorial.html) |
| **cplusplus.com** | 英文的 C++ 教程和标准库手册，写 C++ 时查某个容器、某个函数怎么用，最权威 | [cplusplus.com](https://cplusplus.com/) |
| **C++ 中文网** | C++ 专题式教程，按知识点一块块讲，适合配合课程复习 | [biancheng.net](https://c.biancheng.net/cplus/) |
| **黑马程序员 C++** | B 站 4700 万播放的 C++ 课，从语法一路讲到能做项目。零基础跟着敲完基本能独立写东西 | [去 B 站看](https://www.bilibili.com/video/BV1et411b73Z/) |

### C++ · STL 与算法竞赛

| 网站 | 是什么 | 直接进 |
|---|---|---|
| **算法竞赛常用 STL** | 武汉理工 ACM 集训队的新生课，2 小时把 vector、map、set、queue、stack 这些刷题常用的容器过一遍。收藏数是点赞数的两倍，很多人当手册反复翻。语法学完、开始刷题时看这个 | [去 B 站看](https://www.bilibili.com/video/BV1L8411y7th/) |
| **C++ 标准库速查** | STL 全部容器的官方参考页：每个容器有哪些成员函数、复杂度多少，写得最全。写代码时忘了某个函数怎么用，来这查 | [cplusplus.com](https://cplusplus.com/reference/stl/) |
| **STL 基础教程** | 从 vector、string 开始一步步讲容器怎么用，配合代码演示。刚开始接触 STL、还没到刷题阶段的话，先看这个打底 | [runoob.com](https://www.runoob.com/cplusplus/cpp-stl-tutorial.html) |

### Java

| 网站 | 是什么 | 直接进 |
|---|---|---|
| **廖雪峰 Java 教程** | 中文 Java 教程里最系统的之一，免费、能从头读到尾。适合零基础按顺序啃 | [liaoxuefeng.com](https://liaoxuefeng.com/books/java/introduction/index.html) |
| **Java 官方文档** | Oracle 官方 API 文档。写 Java 时遇到不认识的类，来这查官方定义 | [docs.oracle.com](https://docs.oracle.com/en/java/) |
| **黑马程序员 Java** | 2700 万播放的 Java 入门课，讲到集合、IO、多线程，还带着做力扣题 | [去 B 站看](https://www.bilibili.com/video/BV17F411T7Ao/) |
| **尚硅谷 Java** | 另一个主流 Java 入门课，章节划分清晰，适合想按部就班学的人 | [去 B 站看](https://www.bilibili.com/video/BV1YT4y1H7YM/) |

### Python

| 网站 | 是什么 | 直接进 |
|---|---|---|
| **廖雪峰 Python 教程** | Python 教程，从基础语法讲到常用库，内容免费。很多人第一门语言就学的这个 | [liaoxuefeng.com](https://liaoxuefeng.com/books/python/introduction/index.html) |
| **Python 官方中文文档** | Python 官方文档的中文版。查标准库、查某个函数，官方说了算 | [docs.python.org](https://docs.python.org/zh-cn/3/) |
| **黑马程序员 Python** | 2500 万播放，8 天从零基础到会写完整项目。想快速上手 Python 看这套 | [去 B 站看](https://www.bilibili.com/video/BV1qW4y1a7fU/) |
| **尚硅谷 Python** | Python 入门课，节奏稍慢、讲得更细，适合完全没接触过编程的 | [去 B 站看](https://www.bilibili.com/video/BV1eZ421b7ag/) |

---

## 🧮 算法 & 刷题

| 网站 | 是什么 | 直接进 |
|---|---|---|
| **Hello 算法** | GitHub 13 万星的开源算法教程，用图和动画讲数据结构。免费、中文、可以当教科书用 | [hello-algo.com](https://www.hello-algo.com/) |
| **OI Wiki** | 算法竞赛的知识百科：从并查集、线段树到网络流，每个知识点都有原理推导和可运行的模板代码。覆盖 OI 和 ACM 两类竞赛，是打算法竞赛最全的中文资料库。刷题遇到不会的算法，先来这查 | [oi-wiki.org](https://oi-wiki.org/) |
| **VisuAlgo** | 把排序、树、图这些算法做成动画，能一步步看着它跑。学数据结构时看不懂文字，来看这个 | [visualgo.net](https://visualgo.net/) |
| **浙大数据结构** | 浙江大学的《数据结构》国家精品课，MOOC 上口碑很好，考研党常用 | [去 MOOC 搜课名](https://www.icourse163.org/) |
| **王道数据结构** | 3097 万播放，考研 408 数据结构的事实标准。考研就用这套 | [去 B 站看](https://www.bilibili.com/video/BV1b7411N798/) |
| **洛谷** | 中文算法竞赛刷题站，题解质量高、有梯度。零基础刷算法从这里开始 | [luogu.com.cn](https://www.luogu.com.cn/) |
| **南阳理工 OJ** | 南阳理工学院的校内评测站，对新生最友好：自带按专题排好的「萌新入门题单」，从顺序结构、分支循环一路排到二分、搜索，不用自己规划路线 | [acm.nyist.edu.cn](https://acm.nyist.edu.cn/) |
| **杭电 OJ** | 杭州电子科技大学的老牌 ACM 训练站，2005 年开到现在。74 卷约 7400 题，中文题面多；1000 号起是经典入门区，1089–1096 专门练 A+B 的八种输入格式 | [acm.hdu.edu.cn](https://acm.hdu.edu.cn/) |
| **北大 POJ** | 北京大学的在线评测系统，题从 1000 编起、分 31 卷，题面以英文为主。动态规划和搜索的入门名题很多出自这里，地址是 http，浏览器可能提示不安全 | [poj.org](http://poj.org/problemlist) |
| **力扣 LeetCode** | 面试算法题主战场，题目按数组、链表、树、动态规划分好专题。找工作必刷 | [leetcode.cn](https://leetcode.cn/) |
| **Codeforces** | 全球最大的算法竞赛平台，有定期比赛和全球排名。想打竞赛来这练手速和思维 | [codeforces.com](https://codeforces.com/) |
| **牛客网** | 校招社招求职平台，笔试真题、面经、内推都在这里。大厂笔试的题基本能搜到 | [nowcoder.com](https://www.nowcoder.com/) |
| **Nand2Tetris** | 从一根导线（Nand 门）开始，一路做出逻辑门、CPU、汇编器、虚拟机，最后在你自己造的计算机上跑俄罗斯方块。想搞懂「计算机到底怎么运作」，这门课最直观 | [nand2tetris.org](https://www.nand2tetris.org/) |
| **李春葆《数据结构教程》第 6 版** | 清华大学出版社的教材，微课视频加题库版（C 语言描述）。不少学校的数据结构课就按它讲，配着上课进度翻最省事 | [清华社](https://www.tup.tsinghua.edu.cn/booksCenter/book_09395501.html) |
| **数据结构基础（贺利坚）** | 高校老师录的课，明确按李春葆那本的顺序讲，配套代码和练习都有。课上没听明白时用它补 | [看第 1 集](https://www.bilibili.com/video/BV1pf4y1Z7nf/) |

---

## 🏆 竞赛

| 网站 | 是什么 | 直接进 |
|---|---|---|
| **全国大学生数学建模竞赛** | 高教社杯，每年 9 月，三人一队、三天三夜。官网发历年赛题和获奖名单，通知都以这为准；学校一般先搞校内选拔 | [cmathc.org.cn](https://www.cmathc.org.cn/) |
| **美国大学生数学建模竞赛（美赛）** | 每年 2 月，MCM/ICM 连考四天。题目全英文、获奖面相对宽，对保研和简历有实打实的加分，队里最好有人专管英文摘要 | [comap.com](https://www.comap.com/contests/mcm-icm) |
| **CCPC 中国大学生程序设计竞赛** | 国内自己的 ICPC 体系，分站赛加总决赛，题风接近 ICPC。想往简历上写算法竞赛经历，从 CCPC 网络赛开始报名最现实 | [ccpc.io](https://ccpc.io/) |
| **ICPC 国际大学生程序设计竞赛** | 全球最硬的编程竞赛，三人一队一台电脑。校队选拔从校内赛起步，ACM 集训队练的就是它 | [icpc.global](https://icpc.global/) |
| **RoboMaster 机甲大师赛** | 大疆办的机器人对抗赛：自己造步兵、英雄、工程机器人上场打。偏机械、电控、视觉三个方向，跟 ACM 是两套技能树 | [robomaster.com](https://www.robomaster.com/) |
| **蓝桥杯** | 个人赛，分省赛和国赛，题目偏算法加填空。含金量不如 ACM，但准备周期短、拿奖概率高，大一先拿张奖状不亏 | [lanqiao.cn](https://www.lanqiao.cn/) |

---

## ⚙️ 开发工具

| 网站 | 是什么 | 直接进 |
|---|---|---|
| **Git 官方手册** | Git 官方参考文档，查某个命令的参数、查 push/pull 的区别，权威 | [git-scm.com](https://git-scm.com/docs) |
| **廖雪峰 Git 教程** | 中文 Git 教程里讲得最清楚的一本，按操作流程走一遍就懂版本控制了 | [liaoxuefeng.com](https://liaoxuefeng.com/books/git/introduction/index.html) |
| **黑马程序员 Git** | 144 万播放，从建仓库到多人协作完整讲一遍。团队开发前先看这个 | [去 B 站看](https://www.bilibili.com/video/BV1MU4y1Y7h5/) |
| **GitHub** | 全世界的代码都在这里。看开源项目怎么写、把自己代码存上去都用它。（部分校园网访问不稳，可先用下面的 Gitee） | [github.com](https://github.com/) |
| **Gitee 码云** | 国内的代码托管平台，访问快、不需要科学上网。GitHub 打不开时用这个 | [gitee.com](https://gitee.com/) |
| **菜鸟教程 Linux** | Linux 入门，讲文件系统、常用命令和权限。第一次用 Linux 从这开始 | [runoob.com](https://www.runoob.com/linux/linux-tutorial.html) |
| **Linux 命令搜索引擎** | 780 个 Linux 命令的用法和参数，按命令名搜，比翻 man 手册方便 | [wangchujiang.com](https://wangchujiang.com/linux-command/) |
| **man7 官方手册** | Linux 官方 man 手册在线版。要看最权威的系统调用说明，来这 | [man7.org](https://man7.org/linux/man-pages/) |
| **开源中国** | 国内最大的开源技术社区，技术资讯、开源项目、博客都有 | [oschina.net](https://www.oschina.net/) |
| **黑马程序员 Linux** | 789 万播放，从装系统到部署环境的完整 Linux 课，运维入门常用 | [去 B 站看](https://www.bilibili.com/video/BV1n84y1i7td/) |
| **尚硅谷 Linux** | 277 万播放的 Linux 教程，命令讲得很细，适合想打牢基础 | [去 B 站看](https://www.bilibili.com/video/BV1dW411M7xL/) |
| **菜鸟教程 MySQL** | SQL 基础教程，讲建表、增删改查和常用语法。数据库入门第一站 | [runoob.com](https://www.runoob.com/mysql/mysql-tutorial.html) |
| **SQLBolt** | 在网页上边学边写 SQL，每课都有练习，写完立刻知道对不对。学 SQL 最快的方式 | [sqlbolt.com](https://sqlbolt.com/) |
| **黑马程序员 MySQL** | 1343 万播放，从装 MySQL 讲到索引优化，数据库课里最全的一套 | [去 B 站看](https://www.bilibili.com/video/BV1Kr4y1i7ru/) |
| **尚硅谷 MySQL** | 5 天上手 MySQL，节奏快，适合赶时间快速入门 | [去 B 站看](https://www.bilibili.com/video/BV1Cm421373b/) |
| **VS Code** | 最流行的代码编辑器，装插件后 C、Python、前端都能写。免费、轻量 | [code.visualstudio.com](https://code.visualstudio.com/) |
| **IntelliJ IDEA** | 写 Java 的御用工具，代码补全和调试特别强。社区版免费够用 | [jetbrains.com](https://www.jetbrains.com/idea/) |

---

## 🧰 开发神器

| 网站 | 是什么 | 直接进 |
|---|---|---|
| **Compiler Explorer** | 你写的 C/C++ 代码到底变成了什么？这个网站左边写代码、右边实时显示编译出的汇编，还能换编译器对比。搞不懂指针、循环优化、函数调用开销时，看一眼就明白了 | [godbolt.org](https://godbolt.org/) |
| **explainshell** | 把一长串看不懂的 Linux 命令粘进去，它逐段告诉你每个参数是什么意思。别人给的命令不敢直接跑？先来这拆开看看 | [explainshell.com](https://explainshell.com/) |
| **Learn Git Branching** | 用动画和小关卡把 git 的 merge、rebase、分支玩明白，全程在网页上点，不怕搞坏自己的仓库。看完文字教程还是一头雾水的，来这动手过几关 | [网页版](https://learngitbranching.js.org/?locale=zh_CN) |
| **Regex101** | 正则表达式在线调试器：边写边高亮匹配结果，右侧逐字符解释你的表达式在干什么，还给出每种语言的等价写法。写正则靠猜是行不通的，用这个 | [regex101.com](https://regex101.com/) |
| **Excalidraw** | 手绘风格的在线画图工具，画出来的示意图自带草稿感、很适合放进课程报告和 PPT。不用装软件、不用注册，打开就能画 | [excalidraw.com](https://excalidraw.com/) |
| **draw.io** | 画流程图、UML 图、架构图的老牌免费工具，模板多、导出格式全，还能直接存到网盘或 GitHub。实验报告里要画图基本靠它 | [diagrams.net](https://app.diagrams.net/) |
| **github1s** | 在网页上直接以 VS Code 的界面打开任意 GitHub 仓库，能跳转定义、看文件树。想读别人的源码，又懒得 clone 到本地时用这个 | [github1s.com](https://github1s.com/) |
| **Bootlin 源码阅读** | Linux 内核源码在线阅读，最狠的是交叉引用：点任意函数、结构体都能跳到定义处。想看看操作系统底层到底怎么写的，从这翻 | [bootlin.com](https://elixir.bootlin.com/linux/latest/source) |
| **HelloGitHub** | 每月一期推荐 GitHub 上好玩又适合上手的开源项目，会讲清楚这个项目是干嘛的。想找练手项目但不知道从哪翻起，看两期就有感觉了 | [hellogithub.com](https://hellogithub.com/) |
| **CS 视频课程合集** | 一个人整理的「全世界计算机课程视频」清单，按方向分好类，从操作系统到编译原理都有。想看视频课但不知道有哪些可选的，来这挑 | [GitHub](https://github.com/Developer-Y/cs-video-courses) |
| **提问的智慧** | 写代码卡住时怎么问才能得到回答？这篇经典文章讲透了：先自己查、把问题描述清楚、给出你试过什么。看完再提问，得到答案的概率会高很多 | [GitHub](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/main/README-zh_CN.md) |
| **命令行的艺术** | GitHub 十万星的开源教程，把 Linux 命令行里真正好用的技巧一条条列出来。不用从头读，随手翻几条用进日常，效率就不一样了 | [GitHub](https://github.com/jlevy/the-art-of-command-line/blob/master/README-zh.md) |
| **keybr** | 在线练盲打，会根据你的薄弱字母动态出题，不知不觉就把指法练顺了。打字总要看键盘的可以每天来十分钟 | [keybr.com](https://www.keybr.com/) |
| **SQLZoo** | 把 SQL 分成一个个小练习，边读题边在网页里写查询，立刻能看到结果对不对。学 SQL 光看语法记不住，动手写才记得牢 | [sqlzoo.net](https://sqlzoo.net/wiki/SQL_Tutorial) |

---

## 🎓 课程 & 考试

| 网站 | 是什么 | 直接进 |
|---|---|---|
| **中国大学 MOOC** | 国内高校的免费公开课，从高数、线代到专业课都有。找课在搜索框里搜课程名 | [icourse163.org](https://www.icourse163.org/) |
| **高数（B 站）** | 220 万播放的高数上册精讲，函数极限这块讲得尤其清楚，适合预习和补课 | [去 B 站看](https://www.bilibili.com/video/BV1xhmnYFEir) |
| **3Blue1Brown** | 用动画讲数学的顶流频道，线性代数、微积分、神经网络都有成系列的讲解。课本上看不懂的「这到底在干嘛」，他能给你画出来 | [3blue1brown.com](https://www.3blue1brown.com/) |
| **四六级单词课** | 刘晓艳四级单词精讲，25 天带背一遍，317 万播放。四六级词汇量不够的看这个 | [去 B 站看](https://www.bilibili.com/video/BV1ZzUYByEKi/) |
| **四六级刷题** | 在线刷四六级真题，做完直接看解析和错题统计 | [examcrafts.com](https://examcrafts.com/cet4) |
| **蓝桥杯** | 蓝桥杯官方平台，报名、模拟赛、历年真题都在这。计算机专业性价比很高的竞赛 | [lanqiao.cn](https://www.lanqiao.cn/) |
| **计算机三级（NCRE）** | 全国计算机等级考试官网。三级分网络技术、数据库技术、信息安全技术、嵌入式系统开发技术四个方向，大纲和报名时间都以这为准；不用一级级往上考，可以直接报三级 | [neea.edu.cn](https://ncre.neea.edu.cn/) |

---

## 📑 论文 & 学术检索

| 网站 | 是什么 | 直接进 |
|---|---|---|
| **谷歌学术** | 搜论文第一站：看被引次数、找免费 PDF、顺着引用链往前翻。国内直连不稳，得挂代理 | [scholar.google.com](https://scholar.google.com/) |
| **dblp** | 计算机领域的论文书目库，按作者、会议、年份查，结果干净、不掺无关内容。查「这个方向有哪些顶会」「某人发过什么」用它最准 | [dblp.org](https://dblp.org/) |
| **arXiv** | 预印本服务器：论文没正式发表就先挂这，cs.LG、cs.CL 每天都有新的。追最新进展看它，但没有同行评审，结论得自己掂量 | [arxiv.org](https://arxiv.org/) |
| **Semantic Scholar** | AI 加持的学术搜索：自动抽要点、标引用关系。谷歌学术打不开时，有些场景它反而更好用 | [semanticscholar.org](https://www.semanticscholar.org/) |
| **Connected Papers** | 输入一篇论文，自动画出同领域的引用关系图，点越近关系越紧。入门一个新方向时，五分钟摸清这群人在讨论什么 | [connectedpapers.com](https://www.connectedpapers.com/) |

---

## 🪟 Windows 效率工具

| 网站 | 是什么 | 直接进 |
|---|---|---|
| **Pogget** | Windows 上的桌面文件收纳盒：把散在各个盘里的常用文件拖进盒子，在桌面点开就能用——不搬文件、只建连接，不占额外空间，用完随时清空。还能拆分出多个盒子当抽屉用，磁力访问窗会在「打开/保存」对话框旁边自动吸附，选文件不用一层层翻目录。完全免费 | [pogget.vilinko.com](https://pogget.vilinko.com/) |
| **Lertaro** | Everything 和 Listary 的现代替代品：直接解析 NTFS 的 MFT 表，开机就建好全盘索引，敲几个字秒出结果；再靠 USN 日志实时盯着文件变动，刚存的文件立刻能搜到。C# WPF 写的界面干净，支持插件和自定义搜索范围。开源在 GitHub，去 Releases 页下最新版 | [下载页](https://github.com/Lertaro/Lertaro/releases) |

---

## ⌨️ 输入法 & 文本

| 网站 | 是什么 | 直接进 |
|---|---|---|
| **Rime 官网** | 中州韵输入法引擎的官方站。Windows 的小狼毫、macOS 的鼠须管、Linux 的 ibus-rime 都是它的前端，想搞清 Rime 是什么、为什么值得折腾，先看这里 | [rime.im](https://rime.im/) |
| **小狼毫 Weasel** | Windows 上的 Rime 前端，装完就有全拼/双拼可用。词库、皮肤、方案切换全在本机文件里改，改坏了随时能回滚 | [rime/weasel](https://github.com/rime/weasel) |
| **雾凇拼音 rime-ice** | 最省心的中文方案：词库全、常用词准、配置项开箱即用。不加任何自定义就已经能日常用，是我现在的默认方案 | [iDvel/rime-ice](https://github.com/iDvel/rime-ice) |
| **万象拼音 rime-wanxiang** | 带语法模型的整句方案，连打长句一次上屏；支持首字母简码，打单个字母就出高频候选。想榨干整句准确率就上这个 | [amzxyz/rime-wanxiang](https://github.com/amzxyz/rime-wanxiang) |
| **雾凇拼音 Wiki** | 词库怎么挂、import_tables 怎么写、部署报错怎么修，配置卡住了先翻这里，比翻 issues 快 | [rime-ice wiki](https://github.com/iDvel/rime-ice/wiki) |
| **白霜拼音 rime-frost** | 另一个词库向方案，词频和简码的取舍与雾凇不同。可以拿来对比手感，也可以只借它的词库 | [gaboolic/rime-frost](https://github.com/gaboolic/rime-frost) |
| **Rime 定制指南** | 官方 wiki，*.custom.yaml 补丁机制、schema 结构、lua 扩展全在这。Rime 里所有「为什么必须这么写」的答案 | [rime/home wiki](https://github.com/rime/home/wiki) |
| **東風破 plum** | 官方方案/词库包管理器，一条命令装全套方案和词库，懒得手动拷文件就用它 | [rime/plum](https://github.com/rime/plum) |
| **鼠须管 Squirrel** | macOS 上的 Rime 前端。配置结构和 Windows 完全通用，换平台不用重新学一遍 | [rime/squirrel](https://github.com/rime/squirrel) |
| **ibus-rime** | Linux 上的 Rime 前端（ibus 框架），双系统或服务器党用这个，同一套配置文件直接搬过去 | [rime/ibus-rime](https://github.com/rime/ibus-rime) |

---

## 🛠️ 好用的工具

| 网站 | 是什么 | 直接进 |
|---|---|---|
| **LabEx** | 在浏览器里练 Linux，不用装虚拟机也不怕搞坏电脑。边学边敲命令 | [labex.io](https://labex.io/zh/learn) |
| **打字鸭** | 免费练打字和盲打的网站，有指法教学和打字游戏。打字慢的可以每天练十分钟 | [daziya.com](https://daziya.com/) |
| **AiPPT** | 输入主题自动生成 PPT 初稿，再自己改。赶汇报、赶作业的时候很省时间 | [aippt.cn](https://www.aippt.cn/) |
| **Office 工具集** | 一堆办公小工具的合集，PDF 转换、文档处理之类的都有，不用装软件 | [abcdoffice.com](https://www.abcdoffice.com/zh-cn/) |
| **picDone** | 在线修图，抠图、压缩、加字、拼图十秒出结果，免费不要登录 | [picdone.com](https://picdone.com/zh/) |
| **易简历** | 在线做简历，选模板填内容直接导出 PDF 或 Word，免费 | [toolxx.cn](https://toolxx.cn/) |
| **触手 AI** | 国内的 AI 绘画平台，文字生成图片、图生图都能做，有免费额度 | [chushou.art](https://www.chushou.art/) |
| **TieZ** | macOS 上的剪贴板管理器，有点东西：复制过的文字、富文本、图片、文件路径全自动进历史，多色标签分类加全局搜索，随手就能捞回来；Tauri 2 + Rust 写的原生应用，占内存小，有毛玻璃 / 书页 / 便利贴 / 3D 等八套主题，平时贴边自动隐藏不挡事。跨设备用 WebDAV 或 MQTT 同步，验证码能直接推到当前那台设备，同一个局域网也能互传文件。只发 macOS 版，去 Releases 下 dmg | [GitHub](https://github.com/jimuzhe/tiez-clipboard) |

---

## 🌐 网络 & 魔法

| 网站 | 是什么 | 直接进 |
|---|---|---|
| **魔法区（免费魔法合集）** | 蓝奏云上的免费魔法（科学上网工具）合集，安卓端为主、偶尔更新 PC 端，作者会持续往里补还能用的。连不上的先换节点；提示失效就是真失效了，等更新 | [zdfxdk.lanzouq.com](https://zdfxdk.lanzouq.com/s/mfrjq) |

---

## 📖 找书 & 资料

| 网站 | 是什么 | 直接进 |
|---|---|---|
| **古登堡计划** | 7 万本公版电子书免费下载，英文经典文学基本都有。完全合法、无反爬、打开就能下 | [gutenberg.org](https://www.gutenberg.org/) |
| **arXiv** | 预印本论文库，计算机、物理、数学的论文基本第一时间发在这。查最前沿的研究看这里 | [arxiv.org](https://arxiv.org/) |
| **知网** | 中文学术论文检索，毕业论文、课程报告找参考文献主要靠它。校内网络一般免费用 | [cnki.net](https://www.cnki.net/) |
| **国家统计局** | 官方统计数据，写报告、做分析要找权威数据时来这，免费 | [stats.gov.cn](https://www.stats.gov.cn/) |

---

## 🎬 放松一下

| 网站 | 是什么 | 直接进 |
|---|---|---|
| **大明王朝 1566 解说** | 豆瓣 9.8 分的国剧天花板，34 万字解说全剧，4568 万播放。看剧太慢就听解说 | [去 B 站看](https://www.bilibili.com/video/BV1Ue4y1w7bk/) |
| **Bangumi 番组计划** | 中文动画数据库，看过的番能打分记录，找番时按评分排序很好用。（个别网络下打不开，可换流量） | [bgm.tv](https://bgm.tv/) |

---

**最后更新：2026-10-28** · 全部 141 条链接已实测可用
