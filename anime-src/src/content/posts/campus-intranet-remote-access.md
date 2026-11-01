---
title: 高校内网资源在校外怎么用：一次完整的可用性探查
published: 2026-11-01 23:30:00
description: 把学校内网那一堆只能在校内访问的系统，逐个探到校外可用的方法，附死路清单
tags: [网络, 校园网, WebVPN, 踩坑]
category: 技术
draft: false
comment: true
---
前阵子在校外，我想把作业平台上那份实验报告拉下来，结果发现手机上根本进不去。折腾了几个钟头之后，我索性坐下来把这条链路一层层拆开。下面这些记录是按"最有用但最不直觉"排的，不是按我实际踩坑的时间顺序排的——如果你只读一节，读第一节和第二节。

先给一个判定口径，后面所有内容都建立在它上面：目标地址是 `10.x`、`172.16-31.x`、`192.168.x` 这三段私网，就一定得走 WebVPN；是 `*.neuq.edu.cn` 且公网 DNS 能解析出结果的，直接连，别绕。听起来很废话，但实际遇到的第一个坑就是——同一套系统往往同时挂在内网 IP 和学院域名上，入口不同、可用性不同。

## 零、三步打开（附直链）

前提：人在校外，用浏览器操作，不用装客户端。

**第 1 步，登录 WebVPN**：打开 <https://vpn.neuq.edu.cn/>，点「统一认证」，输学号和统一身份认证密码。

**第 2 步，打开作业平台**。登录成功后，在同一浏览器的新标签页里粘这条：

```
https://vpn.neuq.edu.cn/https/77726476706e69737468656265737421f3f444902632265e7b1d98e29d51367b0755/indexcs/simple.jsp
```

会看到 CourseGrading 的登录页（标题写着「东北大学秦皇岛分校-计算机专业课一体化平台」，右下角有版本号）。

**第 3 步，用作业平台的账号登录**。注意这是**另一套账号**，不是刚才的统一认证密码。登进去就有课程列表、作业、提交记录和分数。

完事。作业平台在门户里没有被发布成图标，所以只能这样手输链接——我当初就是卡在这儿，翻遍门户都没找到入口。

### 其它常用入口

**直接点，不用 VPN**（公网就能开）：

| 系统 | 链接 |
|---|---|
| 统一身份认证（改密码、所有系统的总入口） | <https://ids.neuq.edu.cn/authserver/login> |
| 教务系统（学籍、成绩、考试、选课、空闲教室） | <http://jwxt.neuq.edu.cn/eams/homeExt.action> |
| 一网通办（PC 端办事大厅） | <https://eone.neuq.edu.cn/> |
| 学工 / 办事大厅 | <http://ehall.neuq.edu.cn/index.html> |
| 图书馆统一检索 | <http://libopac.neuq.edu.cn/reader/hwthau.php> |
| 智慧东秦（手机端一站式） | <https://superapp.neuq.edu.cn/> |

**必须过 WebVPN**：财务实训、组成原理 / FPGA 云实验、教学云桌面、智慧档案、自助打印这些。它们的链接要自己生成，方法见第二节最后那行命令——把主机名或内网 IP 填进去，它会直接打印完整链接。

### 打不开时看这张表

| 现象 | 原因 | 怎么办 |
|---|---|---|
| 又跳回 `vpn.neuq.edu.cn/login` | 会话过期（几小时） | 重新登录，再粘一次链接 |
| 跳到 `/wengine-vpn/failed`，显示「该网站无法访问」 | 网关连不上那台内网机器 | 不是你的问题，换时间再试 |
| 页面开了但登录后空白、报「系统异常」 | 目标系统自己的会话坏了 | 清该站 cookie 再登一次 |

下面从第一节开始是完整原理：链路怎么走、主机名怎么编码、什么时候会遇到假阳性。不着急用的话，从那儿往下读。

## 一、WebVPN 的登录是四步，不是两步

大多数教程只写到"CAS 登录成功就完事了"，而网瑞达这套网关的真实链路是四段，少一段都白搭：

1. 在 CAS（`https://ids.neuq.edu.cn/authserver/login`）拿到 `ticket=ST-...`；
2. `GET /login?cas_login=true&ticket=...`，这时**不会**给你会话，而是 302 到 `/fingerprint`；
3. `/fingerprint` 是一个 687 字节的 FingerprintJS 页面，作用是让浏览器算出一个设备指纹；
4. 手动 `GET /set-fingerprint?<原参数>&fingerprint=<32位hex>`，然后**再跟一次** `/login?cas_login=true&ticket=...`。

只有最后这次跟跳才会下发会话 cookie（`wengine_vpn_ticket...`）。我在这上面浪费的时间最久：拿到 ticket、走完 1~3，然后就以为登录完成了，接着所有请求都被 302 弹回登录页，看起来像是"权限不足"，其实只是 cookie 根本没发下来。

另一个小坑：判断当前会话有没有登录，不要在首页 HTML 里翻 `window.__NUXT__`。未登录状态下那个对象里 `canVisitConnection:false` 是个兜底默认值，看着像是没有权限，但它不代表服务端判断。要判权限就打 `GET /user/info`，看它返回什么。

```bash
# 判断会话是否有效（不要看首页 HTML）
curl -s -b cookies.txt https://vpn.neuq.edu.cn/user/info
```

这套链路最坑的地方在于**它不报错**。每一步都是 302，看上去顺理成章，但只要漏掉最后那次 `/login`，拿到的会话就进不去任何内网路径，表现是请求被一路弹回登录页。我一度以为是自己构造的编码错了，把编码反解验证了三遍才回过头发现症结在前一步。教训是：**登录链路里任何一步"看起来成功了"都不算成功，只有真正取到内网资源才算。**

验编码有没有算对，有个不用登内网的办法：把 `encHost()` 的结果反解一遍，看是不是等于原主机名。AES-CFB 是对称流模式，用同一个 key/iv 再跑一次就能还原：

```js
function decHost(code) {
  const hex = code.replace(/^77726476706e69737468656265737421/, '');
  const d = crypto.createDecipheriv('aes-128-cfb', KEY, KEY);
  return Buffer.concat([d.update(Buffer.from(hex, 'hex')), d.final()]).toString('utf8');
}
```

反解对不上，说明你输进去的明文就不是主机名——常见于把带端口的 `host:port` 整串塞进了加密函数。端口不进加密，端口在协议段里。

## 二、内网主机名是这样编码的

这是整篇文章最硬的一条。WebVPN 的转发路径长这样：

```
https://vpn.neuq.edu.cn/http/<编码>/<路径>
```

`<编码>` 不是 base64，也不是 URL 编码，而是：

```
<编码> = "77726476706e69737468656265737421" + hex(AES-128-CFB(key=iv="wrdvpnisthebest!", 明文=主机名))
```

前面那串 28 位十六进制，解出来恰好是 ASCII 的 `wrdvpnisthebest!`——也就是 key 本身。知道这一点之后就不用再猜算法了，直接自己算：

```js
const crypto = require('crypto');
const KEY = Buffer.from('wrdvpnisthebest!', 'utf8');
const PREFIX = '77726476706e69737468656265737421';

function encHost(host) {
  const c = crypto.createCipheriv('aes-128-cfb', KEY, KEY);
  const out = Buffer.concat([c.update(Buffer.from(host, 'utf8')), c.final()]);
  return PREFIX + out.toString('hex');
}

// 用法：https://vpn.neuq.edu.cn/http/<encHost('内网主机')>/<路径>
console.log(encHost('<内网主机>'));
```

端口写在协议段里：`/http-<内网端口>/<编码>/`，标准 HTTPS 端口可以省略成 `/https/`。

这条规则的价值在于：它意味着你**不局限于门户清单里发布过的那些应用**。任何一台内网 HTTP/HTTPS 主机，只要你知道主机名且能连通，就能构造出访问路径。端口扫描做不到的事，靠一个主机名就够了——前提是你得知道主机名。

## 三、它能做什么，不能做什么

实测出来的能力边界，比想象中窄：

| 能力 | 结果 |
|---|---|
| 代理任意内网 HTTP/HTTPS 主机 | 可以，不限门户清单 |
| ICMP（ping） | 没有 |
| UDP | 没有 |
| 标准 CONNECT 隧道 | 没有 |
| 当系统代理用 | 不行 |
| 连 MySQL / Redis / SMB / 游戏 | 不行 |
| `/proxy.pac` | 返回 200，但 0 字节 |
| 网页版 SSH / RDP 堡垒机 | 没有（`showMenuBastion:false`） |

所以它是一个"HTTP 应用层的转发器"，不是 VPN。想拿它当全局代理跑其它协议，方向从一开始就错了。

## 四、必须走 WebVPN 才有用的东西

按有用程度排：

| 系统 | 说明 |
|---|---|
| 作业平台 CourseGrading 8.2.0 | 学生登录字段 `stid` / `pwd` / `captchaCode`，验证码图在 `/cgjiaoyan`（130×48 GIF）。密码要按 `base64(AES-128-ECB(PKCS7(密码), key="Client8Sess!06ID"))` 提交，直接发明文必然失败。同一套系统有两个入口：内网 IP 和学院域名 `ccelab.neuq.edu.cn`（公网 DNS 查不到，只在网关侧解析） |
| 财务实训平台 | 网中网财务决策平台高级版 v4.2.0；用友分析云（Yonyou Analytics） |
| 组成原理 / 龙芯 FPGA 云实验平台 | Loongson FPGA Cloud，`/upload` → `/signin`。有开放注册表单，但我没注册 |
| 教学云桌面 | OpenStack/KVM 底座的 VDI，前端是 `ng-app` 组件式。`/v1/node/status`、`/api/flavors` 这类 GET 不需要鉴权就能读到宿主机 CPU 型号和 7 种虚拟机规格；改机器的接口全部要登录 |
| 自助打印 / 文件真伪验证 | 正脉高校自助服务系统，公网也可达（部署在学校公网段），但功能要校内身份 |
| 智慧档案 | 校内 Tomcat 上的档案系统 |

除了作业平台我给了现成链接，上表其它系统都得自己生成那串编码。一条命令搞定，把主机名换成你要的即可（Node.js，不需要装包）：

```bash
node -e "const c=require('crypto'),K=Buffer.from('wrdvpnisthebest!');const h=process.argv[1];const x=c.createCipheriv('aes-128-cfb',K,K);console.log('https://vpn.neuq.edu.cn/https/77726476706e69737468656265737421'+Buffer.concat([x.update(Buffer.from(h)),x.final()]).toString('hex')+'/')" 主机名或内网IP
```

它会把完整链接打印出来，粘到已登录 WebVPN 的浏览器地址栏就行。注意 http 站点要把 `/https/` 换成 `/http/`，非默认端口写成 `/http-端口号/`。

FPGA 云平台那个注册表单我盯着看了很久，最后没提交。理由很简单：注册会在校内留下一个自造账号，属于"制造痕迹"，不是"读取信息"。这条线我自己划了。

## 五、前置知识：学校有两套完全不同的认证体系

这一点不搞清楚，后面全是白试。

**统一身份认证 CAS**：`https://ids.neuq.edu.cn/authserver/login`，金智 wisedu 那套。登录表单里会带一个随机的 `pwdDefaultEncryptSalt`，前端用 AES-128-CBC 加密密码，明文是"64 位随机串 + 密码"，IV 随机生成，服务端并不校验 IV，提交字段名是 `passwordEncrypt`。

关键结论：**直接发明文密码会被判"用户名或密码有误"，这是假失败。** 你会以为是密码错了，其实是加密层没走。

**WebVPN 本地账号库**（网瑞达）：`https://vpn.neuq.edu.cn/do-login`，`auth_type=local`，密码明文提交。这套库和统一认证**不是一套口令**。拿统一认证的密码在这里试，会返回「[local]:用户名或密码错误；还剩4次机会」。本地库只有 5 次机会——所以不要在这里盲试，试满就锁了。

**第三个客户端 EasyConnect**（深信服 SSL VPN）：服务器地址 `https://vpn2.neuq.edu.cn`，验证码强制（`g_bRndImg 1`）。我试过绕开网页端的验证码，直接打 `POST /por/login_psw.csp?encrypt=1`（密码做 RSA PKCS#1 后转小写 hex，这个接口确实不要验证码），返回的是 `Invalid username or password!`。

结论：**它的本地账号库里没有统一认证的账号。** 对只有统一认证账号的人来说，这条路是死的。我在这上面耗掉了一个多小时，写在这里省后来人的时间。

## 六、公网直连的那一批

这些不需要 VPN，公网直接访问：

- 智慧东秦 `superapp.neuq.edu.cn`（移动端一站式）
- 教务系统 `jwxt.neuq.edu.cn/eams/`
- 一网通办 `eone.neuq.edu.cn`
- 学工 ehall
- 图书馆统一检索 `libopac.neuq.edu.cn`（超星新一代）
- 学校主页、信息化办

先直连试一遍，连不上再挂 VPN——反过来做是浪费。

## 七、CAS 白名单是个坑

直接拿这几个地址去 CAS 登录，会返回一坨 10428 字节的页面：「应用未注册，不允许使用认证服务来认证您访问的目标应用」。

```
https://eone.neuq.edu.cn/
https://jwxt.neuq.edu.cn/eams/homeExt.action
https://libopac.neuq.edu.cn/
```

但教务其实**是能登的**——关键在于走对入口：

```bash
# 先打一次 http 的入口，让它自己 302 到 CAS
curl -s -i "http://jwxt.neuq.edu.cn/eams/homeExt.action" | grep -i location
```

它会 302 到 CAS，并把**带 `;jsessionid=...` 的完整 service 串**放进 `service` 参数里。而 CAS 的白名单比的是**完整 service 串**，包含 `;jsessionid=` 那一截。所以你自己手写一个"干净"的 service 反而匹配不上——删掉 jsessionid 就等于把自己从白名单里踢出去。

已注册的几个（可以直接用 CAS 跳）：`superapp.neuq.edu.cn`、`newcas.neuq.edu.cn/cas/login`、`ehall.neuq.edu.cn/index.html`。

## 八、智慧东秦的微服务：鉴权头不是 Bearer

从智慧东秦前端 bundle 里抠出 8 个后端服务：`message-service`、`transaction`（路径前缀 `/ttc/`）、`authx-service`、`form-design`、`formflow`、`newcas`、`eone`、`superapp`。

鉴权头不是常见的 `Authorization: Bearer <token>`，而是 **`X-Id-Token`**；它的值不是整段 JWT，而是从 CAS 回跳 URL 里那段 JWT 的 payload 里取出来的 `idToken` 字段。用错写法，所有接口统一返回：

```json
{"code":401,"message":"token信息不存在"}
```

能用的读接口举例：

```bash
# 本人身份与院系
curl -s -H "X-Id-Token: $ID_TOKEN" \
  https://authx-service.neuq.edu.cn/personal/api/v1/personal/me/user

# 待办列表 —— 只接受 GET
curl -s -H "X-Id-Token: $ID_TOKEN" \
  "https://transaction.neuq.edu.cn/ttc/api/ttc/center-list/getToDoList?pageNum=1&pageSize=20"
```

`getToDoList` 用 POST 会返回 `Request method 'POST' not supported`，这个报错很容易被误读成"接口不存在"。另外还有 `getToDoListCountNew`、`getNewsCount` 两个计数接口。

chunk 是怎么找到的：bundle 里 `jsonpScriptSrc(chunkId)` 返回 `static/js/<name>.<hash>.js`，用正则 `"([A-Za-z0-9\-~]+)":"([0-9a-f]{8})"` 从映射表里抽出 149 条 chunk→hash，筛出 44 个页面 chunk 下载下来，一共抽出 309 条接口路径。这个方法对所有 webpack 打包的前端都通用。

顺带一个观察：一网通办的 `portal-api` 在报错时会回显下游服务的内部地址，泄露过 Docker 服务名和内部端口。具体值我就不写了，但这个现象本身值得记——错误处理没做好，等于把内网拓扑结构送出去。

## 九、教务系统能读到什么（只读）

`homeExt!submenus.action` 下面挂了 28 个菜单。实际可用的：

学籍信息、我的考试、我的成绩、公共课表查询、空闲教室查询、教材查看、收费学分核对、量化评教、创新学分申请、退课申请、校外考试报名记录、培养方案完成情况。转专业、大类分流、推免、辅修、缓考、毕业论文这六个入口存在，但当前未开放。

退课申请的扣费规则写在页面里：第 1 学时前退课扣 50%，第 3 学时前 75%，第 5 学时前 100%，之后不允许退，最低扣 5。这条规则平时没人注意，真要退课时才发现。

**死路警告**：「我的课表」入口 `courseTableForStd.action` 本身返回 200，看起来是通的，但课表格子是由 `courseTableForStd!courseTable.action` 渲染的，那个端点 500，异常是 `java.lang.NullPointerException`，容器是 `Apache Tomcat/7.0.109`，原因是模板缺失。`myPlan.action` 同样 500。所以个人课表是拿不到的，只能退而求其次走「公共课表查询」按班级/专业查。

**空闲教室查询**是实测可用的，但字段要求很怪：

```bash
curl -s -X POST "http://jwxt.neuq.edu.cn/eams/classroom/apply/free!search.action" \
  -d "cycleTime.cycleCount=1" \
  -d "cycleTime.cycleType=1" \
  -d "cycleTime.dateBegin=<日期>" \
  -d "cycleTime.dateEnd=<日期>" \
  -d "roomApplyTimeType=1" \
  -d "timeBegin=<节次起>" \
  -d "timeEnd=<节次止>"
```

少任何一个字段，请求会被静默弹回登录页——不是报错，是弹回登录页，所以看起来像会话过期。另外返回列表里的「容量」字段大量为 0，因为后台没维护这个字段，不要拿它做筛选。

## 十、内网资产清点的几个观察

这一节只讲现象和方法，不写地址。

内网大致存在三类主机：操作系统默认页（IIS 欢迎页、nginx 测试页）、教学业务系统、以及基础设施管理面（三台 vSphere 管理界面、一台教学云桌面控制台）。

最值得记下的一台，跑的是 **Apache Tomcat 6.0.35**（2011 年就停止维护了）。它的管理台 `/manager/html` 从公网侧就能访问到，返回 401 基本认证框；`OPTIONS /` 返回 `Allow: GET, HEAD, POST, PUT, DELETE, OPTIONS`。老版本 + 开放管理台，这是教科书级的组合。**我只发了 GET 看到 401 就停手了**，没有尝试任何凭据。看到 401 就该知道边界在哪。

方法上有两件事值得说：

第一，WebVPN 网关会把所有响应的 `Server` 头抹成空，直接看指纹是看不到的。但 302 响应体里仍然会泄露 nginx 版本——这是个被动侧信道，比主动探测安全得多。

第二，网关对连不上的目标有两种表现：302 跳到 `/wengine-vpn/failed`，或者 15 秒超时。**同一台主机两次探测结果会相反。** 所以"超时"绝对不能当作"主机不存在"的证据，只能当作"这次没连上"。这条判据我一开始搞错了，做了一堆错误的排除。

## 十一、怎么判断一个 200 是真的

这次探查里，骗过我的"成功"比明确的失败多得多。总结三条判据，按可靠性排：

**第一，看响应体长度有没有变化。** 同一个接口，未授权时回一个固定长度的落地页，授权后回 JSON，长度差一个数量级。只记状态码不记长度，等于什么都没记。

**第二，看 Content-Type。** nginx 回落 `index.html` 的时候照样回 200，但它回的是 `text/html`，而你要的是 `application/json`。智慧东秦的 `/api/*` 让我在这上面绕了很久——每个路径都 200，每个都"成功"，其实全是同一个首页。

**第三，看有没有结构性内容。** 一网通办的 CMS 接口就是个反例：栏目列表真的返回了 6 个栏目，字段齐全、结构正确，然后内容列表全是空数组。这时候 200 是真的，数据是假的，两者得分开记。

把这三条落成一张表，每次探测记四列：路径、状态码、长度、Content-Type。事后回看，假阳性一眼就能挑出来。

## 十二、死路清单

按浪费时间的多少排序：

- EasyConnect 客户端 —— 本地账号库里没有统一认证账号
- 深信服 Web 登录接口 —— 同上，返回 `Invalid username or password!`
- ehall 办事大厅 JSON API —— 旧版金智 amp2 服务端渲染，`/new/publicapp/*` 全 404
- 教务「我的课表」—— 模板缺失导致 500，不是权限问题
- 教务旧版成绩/考试入口 —— 403
- 图书馆 CAS 登录 —— 不在白名单
- 智慧东秦 `/api/*` —— nginx 回落 index.html，返回 200 但内容是首页，全是假阳性
- 微服务 Swagger / Actuator —— 8 个服务全部未暴露
- 一网通办 CMS 内容接口 —— 6 个栏目确实存在，但内容列表全为空

最后那条特别容易骗人：栏目存在、接口有响应、就是没数据，你会反复怀疑是参数写错了，其实人家就是空的。

## 十三、边界

这一节写清楚哪些事我做了、哪些没做，以及为什么。

**做了的**：只读探测。GET / OPTIONS、读公开的前端 JS、调不需要鉴权的读接口、用我自己的账号读我自己的数据。仅此而已。

**没做的，以及为什么**：

不做口令爆破。WebVPN 本地库 5 次机会，教务和 CAS 也都有锁定策略，爆破除了把账号锁死没有任何收益。

不提交 `/manager/html`。看到 401 就够了，那个认证框背后是别人的运维责任范围，不是我的读取权限。

不发 PUT、不上传文件。`OPTIONS` 说允许 PUT，和"我应该发一个 PUT"是两件事，中间隔着一条我清楚的位置。

不枚举验证码和查询码。那个"文件真伪验证"页面，输学号加验证码就能查到别人的学历信息——穷举它等于批量泄露他人个人信息。这不是技术难度问题，是做不做的问题。

不越权读他人数据。所有带 ID 的接口，我只用自己的 ID 测通就停。

最后一条实操建议：网关按会话限流，大约 0.8 请求/秒。扫段之前先把节奏调下来，否则你会在第 20 个请求之后开始收到一堆看起来像"主机不存在"的超时——而那只是限流，不是网络事实。
