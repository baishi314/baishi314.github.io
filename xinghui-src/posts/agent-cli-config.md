---
title: "装完还是用不了：配置、通道与防封"
date: "2026-11-03 12:40:00"
description: "命令行 agent 装完还有三件事：拿到一条能用的通道、把配置写对、别把号玩死。有官方订阅的人其实零配置，这份笔记先帮你判断要不要动手。"
cover: "/cover-default.svg"
tags: ["AI", "Agent", "Windows", "工具"]
---
工具装好了，命令也能敲出来，但一用就卡住。结局只有两种：它不认你写的配置，或者第二天号没了。

先分流。有官方订阅的不用配置，看完第一节就走；没有订阅、或者想接国内便宜模型的，从第二节开始。安装步骤见[上一篇](../agent-tools-windows/)。

## 一、有正版订阅：零配置

Codex 是这里最省事的一个：

```powershell
codex
```

第一次运行会问登录方式，选「用 ChatGPT 账号登录」，浏览器弹出页面点确认，回到终端就能进对话界面。全程不碰 `config.toml`，这个文件保持不存在反而是对的。

登录成功后，`%USERPROFILE%\.codex\` 下会多一个 `auth.json`。这个文件就是凭据本身，别复制到第二台机器，附录里那条 `refresh token was already used` 正是它引起的。

Claude Code 同理：

```powershell
claude
```

选登录 Anthropic 账号，浏览器授权，再过一次手机验证，之后 `claude` 直接可用。验证方式：`claude` 里敲 `/status`，账号一栏显示邮箱就对了；显示 API key，说明它读到的是环境变量，不是登录态。

**不要给正版账号加 `ANTHROPIC_BASE_URL`。** 加上它就等于主动声明「我在走中转」，附录里那套识别机制正是从这一条开始启动的。很多号是照着教程「配得更完整」配没的：正版订阅下唯一该存在的凭据，是登录后生成的那个 auth 文件，环境变量越干净越好。

## 二、没有订阅：先拿到通行证

两种通行证的成本结构不一样：一次性号码按次付费，key 按量付费。先想清楚要跑多久，再决定买哪一种。

### 路 A：一次性号码

用 [hero-sms-cn.com](https://hero-sms-cn.com/)（中文站），四步。

1. 注册并充值。起充一两美元，用不完的余额可以留着。
2. 服务名搜 `openai`。不是 `chatgpt`，搜错了会买到一个用不上的号。
3. 选越南或泰国号。单次 0.006 美元起，越南号大约 0.09–2.94 美元，看库存浮动。
4. 20 分钟内收到 6 位码就填进去。没收到会自动退余额，不用去发工单。

号码是一次性的。平台把它卖给别人之后，落在那个号上的验证码就与你无关了，所以收到就立刻填，别攒着。起充金额不高，试错成本比买一个月会员低得多。

三条纪律：

1. 同一个账号最多试两次。
2. 失败就换号，同时换平台。
3. 别连点重试。连续失败三次，账号会被锁成「电话认证次数过多」，之后换任何平台都收不到码。

### 路 B：直接买 key

注册平台、充值、建 key，就这样。key 路线完全不触发手机验证，只验支付，所以前面那些号码的坑一个都不会遇到。代价是按量计费，且能选的模型受平台限制。建 key 时把额度上限设低一点，平台跑路或者 key 泄露，损失封顶。

## 三、要接第三方 API：两张配置卡

两张卡对应两个客户端。填之前先确认手上这条通行证提供的是哪种端点，对不上就别浪费时间改字段，先回附录看协议那一节。

### Codex

**文件在哪**：`%USERPROFILE%\.codex\config.toml`，没有就新建。

**填什么**：

```toml
model = "MODEL_NAME"
model_provider = "relay"

[model_providers.relay]
name = "Relay"
base_url = "https://RELAY_HOST/v1"
env_key = "RELAY_API_KEY"
wire_api = "responses"
```

key 本身不写进这个文件，只写变量名：

```powershell
setx RELAY_API_KEY "sk-XXXXXXXX"
```

`base_url` 必须带 `/v1`；`env_key` 只能填环境变量名，直接填 `sk-` 开头那串会报 401。`wire_api` 现在只剩 `responses` 一个合法值，老教程里的 `chat` 已经不被接受，写上会直接报解析失败。

**怎么确认**：关掉终端重开，敲 `codex`，发一句「1+1」，能回话就通了。启动时报 `missing env var RELAY_API_KEY`，说明 `setx` 之后没重开窗口，当前进程拿的还是旧环境。

### Claude Code

**文件在哪**：`%USERPROFILE%\.claude\settings.json`。

**填什么**：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-XXXXXXXX",
    "ANTHROPIC_BASE_URL": "https://RELAY_HOST",
    "ANTHROPIC_MODEL": "MODEL_NAME",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "SMALL_MODEL",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "MODEL_NAME",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "BIG_MODEL"
  }
}
```

这里的 `ANTHROPIC_BASE_URL` 填到中转方给你的那一层：通常就是域名根，也可能带 `/anthropic` 这样的路径前缀，但**不要再自己叠 `/v1`**，和 Codex 那张卡正好相反。三个模型变量填中转接口里列出来的名字，不是 Claude 官方那几个。JSON 不接受注释，也不接受单引号，从教程里抄的时候把中文标点一并换掉。

**怎么确认**：`claude` 里敲 `/status`，看 Base URL 是不是你写的那个、token 前几位对不对。

补一句：`settings.json` 的 `env` 优先级高于系统环境变量，两边都设会互相覆盖。这是「我明明改了却不生效」的头号原因，改完只留一边。

**CC Switch**：不想手写 JSON 就装它，图形界面填 key，它替你写上面两个文件。

## 四、出错了看这里

按报错原文查，一处改完重开进程再试，别一次改三处。查不到就照附录的五格顺序排。

| 报错原文 | 真因 | 改哪一处 |
|---|---|---|
| `'claude' 不是内部或外部命令` | PATH 没刷新 | 关掉终端重开 |
| `401 invalid api key` | key 错，或 base_url 没带 `/v1` | 换 key，补 `/v1` |
| `404 not found` | 协议不对，中转只给 chat completions | 换支持 responses 的中转 |
| `unsupported_country_region_territory` | 节点在香港或大陆 | 换出口节点，重开进程 |
| `refresh token was already used` | 同一 auth.json 多机共用 | 只留一台，其余删文件重登 |
| `Unexpected token } in JSON` | JSON 少一个英文逗号 | 用校验器过一遍 |
| `expected newline, found ...` | TOML 段落头或引号写错 | 查 `[model_providers.x]` 那一行 |
| 项目级 `.codex/config.toml` 不生效 | 项目级忽略 model_providers | 改写用户级 |
| `ECONNREFUSED 127.0.0.1:7890` | 旧代理残留 | 清掉 `HTTPS_PROXY` |
| `UNABLE_TO_VERIFY_LEAF_SIGNATURE` | 代理做了 TLS 拦截 | 设 `NODE_EXTRA_CA_CERTS` |
| `os error 10013` | 1455 端口被占 | 改用 `codex login --device-auth` |
| `电话认证次数过多` | 该账号已锁 | 换账号，别在这号上继续 |

---

## 附录

### 五个格

| 格 | Codex | Claude Code |
|---|---|---|
| 客户端 | `codex` CLI | `claude` CLI |
| 认证 | `auth.json`，或 `env_key` 指向的变量 | `settings.json` 的 `env` 块，或 OAuth 文件 |
| 端点 | `base_url`，末尾带 `/v1` | `ANTHROPIC_BASE_URL`，只到域名根 |
| 协议 | `/v1/responses` | `/v1/messages` |
| 模型名 | `model` 字段 | `ANTHROPIC_MODEL` 与三个 DEFAULT 变量 |

九成的报错，是这五格里有一格没对上。客户端版本、认证方式、端点、协议、模型名，缺一格就是 401 或 404，而报错文案往往只提最后一个。

客户端那一栏指的不是名字，是版本。Codex 切到 responses 是后面几个版本才做的，老版本只发 chat completions，配置照抄也会 404。认证那一栏差别最大：Codex 读 `auth.json` 或环境变量，Claude Code 先读 `settings.json` 的 `env`，再读系统环境变量，最后才轮到 OAuth 文件，三层里任意一层有值都会盖住下面。模型名这一格最容易被跳过：同一个中转的同一个端点，模型名写错回来的往往不是「模型不存在」，而是 404，和端点不存在长得完全一样。

排错按这个顺序走，别跳：

1. 重开进程。环境变量和配置文件都是启动时读的。
2. 看配置能不能解析。JSON 和 TOML 的手写错误比逻辑错误多得多。
3. `/status` 看 Base URL，确认程序读到的就是你以为的那个值。
4. `curl` 端点，看回 401 还是 404。401 是认证问题，404 是路径或协议问题，两者方向完全不同。加 `-i` 只看状态码，别看响应体，响应体经常是一段 HTML 错误页，越看越乱。
5. 对模型名。中转常常只认某几个字符串，写错就回 404，看起来像端点问题。

### 协议为什么不能通用

三家说的不是一种话：

- Codex 只认 `/v1/responses`；
- Claude Code 只认 `/v1/messages`；
- 市面上中转大半只提供 `/v1/chat/completions`。

这就是「配置全对但一直 404」的唯一原因。请求发出去了，路径对，key 也对，但对面没有这个接口，于是回 404，和路径写错的表现一模一样。

两种协议的结构本身也不一样。responses 是「输入项列表 + 输出项列表」，messages 是「role 数组 + content 数组」，字段层层嵌套。所以不是换个路径就能对上，这才是中转只抄 chat completions 的原因：它最简单，也最早被抄烂。

两条解法。一是在前面加一层桥接，把 responses 或 messages 翻译成 chat completions，多一个进程，多一处延迟和故障点。桥接的典型做法是本地起个 `127.0.0.1` 的服务改写请求体，再把流式事件翻译回去；能跑，但工具调用和 reasoning 这类字段在翻译里会丢，长任务跑到一半容易断。二是换一家直接支持 responses 的中转，配置不用改一个字，这是更省事的做法。

判断方法很简单：`curl` 一下 `https://RELAY_HOST/v1/responses`，不带 key 也行。回 401 说明接口存在，只是没认证；回 404 说明这家根本没有这个端点。不想开终端也行，翻中转的文档，里面没有 `responses` 这个词就是没有。

### 封号是怎么判的

四层，由粗到细。判定不是一条规则一票否决，而是几层证据叠加：单条可疑未必封，三五条凑齐基本就没了。

1. **系统时区**。`Asia/Shanghai`、`Asia/Urumqi` 直接被标记，不需要任何行为证据。这个值在「设置 → 时间和语言」里，改它不影响 IP，只会立刻和出口对不上，所以要么一开始就设成出口所在地，要么别动。
2. **`ANTHROPIC_BASE_URL`**。只要不是官方域名，就等于自己声明在走网关。
3. **内置域名与关键词黑名单**。中转域名、常见代理域名、提示词里的敏感词，命中即记。
4. **Unicode 隐写**。提示词里日期的分隔符、引号会被换成不同码位，不同码位分别对应「命中中国时区」「命中域名名单」「命中 AI 相关关键词」。服务端扫一眼字符就知道，不需要额外发请求，也不需要读内容。这种差异肉眼看不出来，两个引号复制到编辑器里长得一模一样。

封号邮件里的图片是追踪像素。打开邮件那一刻，客户端会去拉那张图，真实 IP 就回传了。邮件客户端默认加载远程图片，网页版尤其如此，关掉自动加载，或者只看纯文本。

三条永远有效的做法：

- 出口固定不跳。线路换得比人还勤，比一直用一条更显眼。
- 时区、语言、IP 三者一致。系统时区写上海、浏览器语言是英语、IP 在洛杉矶，这三条凑在一起本身就是结论。
- 能走 key 就别登账号。key 被封只损失余额，账号被封会连历史对话一起没。key 单独建、单独记，别和账号密码放一个文件里。

这两年封禁量大、申诉成功率很低，所以预防优先。真被封了，换号重来的成本，远低于写申诉信的时间。
