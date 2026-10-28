---
title: "我把输入法换成了 Rime：雾凇 + 万象双方案，附踩坑全记录"
date: 2026-10-27
draft: false
tags: ["Rime", "输入法", "Windows", "工具", "折腾记录"]
categories: ["折腾记录"]
summary: "程序员天天在打字，输入法却常年是最将就的那个。这份记录是小狼毫 + 雾凇拼音 + 万象拼音的完整落地过程：三套词库怎么挂、单字母候选怎么开、部署顺序错一步就卡十分钟，以及一次让主力方案\"彻底死亡\"的词库乱序事故。"
---
输入法大概是程序员电脑上最不该将就、却最常被将就的软件。搜狗装完先弹三个广告，微软拼音的词库里没有 `std::vector`，打到一半要切出去搜英文变量名——这些零碎的摩擦加起来，一天几十次。

换成 [Rime](https://rime.im/)（Windows 前端叫**小狼毫 Weasel**）之后，这些摩擦一次性消失：词库是自己的、候选是自己排的、全程不联网。代价是它**什么都不给你配好**，一切靠 YAML。

这篇是我这台机器上实际在跑的一套配置的完整记录，不是教程搬运。**下面是能直接照抄的参数，加上踩过的坑。**

## 一、先说我最后跑成什么样

一句话结论：

> 雾凇拼音（全拼主干）与万象拼音（整句最强）**共存**，默认进雾凇，`F4` / `Ctrl+\`` 随时切换。

环境：

| 项 | 值 |
|---|---|
| 前端 | 小狼毫 Weasel **0.17.4**（librime **1.13.1**） |
| 用户目录 | `C:\Rime`（改注册表 `HKCU\Software\Rime\Weasel\RimeUserDir` 重定向，不是默认的 `%APPDATA%\Rime`） |
| 皮肤 | `weasel.custom.yaml` → `style/color_scheme: dark_temple`（暗堂，深色） |
| 方案切换 | `F4` 或 `Ctrl+\``（反引号）唤出方案选单 |

用户目录挪出 `%APPDATA%` 这件事值一提：Rime 的词典编译产物加上腾讯大词库能吃到几百 MB，塞在 AppData 里既不好备份也不好用 git 管。挪到 `C:\Rime` 之后它就是一个干净的、可以整体打包的文件夹。

## 二、为什么让两套方案共存

Rime 的 `default.yaml` 里有个 `schema_list`，**列表顺序 = 默认优先级**。我现在是这么排的：

| 顺序 | schema | 说明 |
|---|---|---|
| 1（默认） | `rime_ice` | 雾凇拼音（全拼），主用 |
| 2 | `wanxiang` | 万象拼音（整句模型最强） |
| 3 | `wanxiang_english` | 万象英文 / 中英混输 |
| 4 | `t9` | 中文九键（依赖 rime_ice，**勿删**） |
| 5–11 | `double_pinyin` 系列 | 自然码 / 智能ABC / 微软 / 搜狗 / 小鹤 / 紫光 / 拼音加加 双拼 |

这俩不是一个替代另一个，是**分工**：

- **雾凇拼音**（[iDvel/rime-ice](https://github.com/iDvel/rime-ice)）胜在词库全、惯用词准、开箱即用的配置项多。日常敲中文、敲注释、敲文档，它是最稳的。
- **万象拼音**（[amzxyz/rime-wanxiang](https://github.com/amzxyz/rime-wanxiang)）带一个 `wanxiang-lts-zh-hans.gram` 语法模型，整句连打的上限更高。写长句、写口语化的东西时切过去，一次上屏一整句。

多方案共存唯一要注意的是：**别删 `t9`**。中文九键是挂在 `rime_ice` 上的，删了会连带影响雾凇的加载。

## 三、目录结构与三个领域词库（重点）

```
C:\Rime\
├─ default.yaml / default.custom.yaml   # 方案列表、全局键位、标点、快捷键
├─ weasel.yaml / weasel.custom.yaml     # 前端皮肤/外观（暗堂）
├─ rime_ice.*                           # 雾凇 schema + 词库
├─ wanxiang.* + wanxiang_*.schema.yaml  # 万象家族（主/简码/英文/混合/反查/九键）
├─ wanxiang-lts-zh-hans.gram            # 万象语法模型（整句核心）
├─ cn_dicts/                            # 雾凇基础词库，含 tencent 大词库（~120MB，编译慢）
├─ domain_dicts/                        # 用户领域词库（3 个，见下）
├─ lua/                                 # 万象 lua 脚本（custom_phrase 等）
├─ build/                               # 编译产物 *.bin（部署时重建，删了无害）
└─ *.userdb                             # 用户词典（个人调频，勿删）
```

**这才是这次配置真正的价值所在：三个自己挂上去的领域词库。** 它们通过 `rime_ice.dict.yaml` 的 `import_tables` 挂进主词库：

- `domain_dicts/selected.jisuanjicihuidaquan` — **计算机词汇大全**
- `domain_dicts/selected.kaifadashenzhuanyongciku` — **开发大神专用词库**
- `domain_dicts/selected.kaomoji` — 颜文字（拼音触发，混入普通候选）

第一、二个就是"程序员特调"的核心：变量命名习惯、常见 API、框架名、编译报错里的词，都在候选里。打 `huancun` 第一个就是「缓存」，打 `yichang` 直接出「异常」，不用在"亿昌/宜昌"里挑。

第三个是颜文字，用 `km` 前缀触发，混在普通候选里：

```
kmbang → (★ω★)
kmao   → (>▽<)
```

**但这个词库就是把我坑死的那一个**，见第六节。

## 四、键盘手感：这些键位值得改

配置里我保留了这几处，都是"改完再也回不去"的：

- **以词定字**：`[` 取首字、`]` 取末字。打完一个词只想要其中一个字时，不用退格重打。
- **中英切换**：左 `Shift` = 上屏当前编码并切英文；`CapsLock` = 清掉未上屏内容切英文。分工清楚，不会打了半句英文全丢。
- **翻页**：`-` / `=` 上/下页（不再是 `,` `.`，跟 Vim、less 一致）。
- **光标移动**：`Tab` / `Shift+Tab` 在已输入的拼音之间移动光标，改错中间一个字母不用全删。
- **符号/字形切换**：`Ctrl+Shift+3` 中英标点；`Ctrl+Shift+4` 简繁。
- **单字母候选（万象）**：`wanxiang.schema.yaml` 主翻译器 `enable_completion: true` + `wanxiang_algebra.yaml` 的首字母简码规则
  `abbrev/^([qwrtypsdfghjklzxcbnm]).+$/$1/`
  → 打单个 `l` 就出「了 / 来 / 里…」候选。

- **AI 模块（可选，我没开）**：配置里带了个 `ai_enhance.lua`，能接本地服务（`127.0.0.1:3080`）或硅基流动，输入 `/ai 提示` 触发。**实时候选有延迟**，挂全局会让每次打字都等网络，我的建议是只用它离线生成词库/短语，别全局挂。

## 五、部署流程：顺序搞错会卡十几分钟

Rime 改完词库/配置**必须重新部署**才生效。而部署这一步有个坑：`WeaselServer` 和 `WeaselDeployer` 会抢词典锁，直接点部署可能卡 10 分钟以上。

正确顺序：

1. **先结束进程**

   ```powershell
   Stop-Process -Name "WeaselServer","WeaselDeployer" -Force
   ```

2. **再部署**（二选一）

   - 命令行独立编译：

     ```powershell
     "C:\Program Files\Rime\weasel-0.17.4\WeaselDeployer.exe" /deploy
     ```

     含 tencent 大词库时约 **10–30 分钟**，期间输入法不可用。

   - 或者托盘右键「重新部署」——让 Server 在后台自己建，更稳定，**日常推荐这个**。

3. **命令行部署后要手动重启 Server**：启动 `WeaselServer.exe`。

4. **校验**：看 `C:\Rime\build\rime_ice.table.bin` 的时间戳是不是本次部署的时刻。不是就说明没真编译。

## 六、踩坑记录（这一节最值钱）

### 坑 1：一个词库没排序，整个方案"死"了

症状：雾凇打不出任何中文，颜文字也失效。而且**不是报错弹窗**，是静默降级——输入法看着在，就是不出字。

根因链条是这样的：

```
kaomoji 词库追加内容未按码排序
  → 该词典标了 sort: origin，乱序即违约
  → 编译报 table.cc:271 invalid metadata
  → rime_ice 整个 schema 加载失败
```

一个 300 行的颜文字词库，把主力全拼方案整死，而且死得毫无提示。修复：

1. 词库按编码重新排序（乱序条目归零）
2. 删掉损坏的 `build/*.bin`
3. 完整重新部署

2026-10-23 修完，日志是 `9 success, 0 failure`，`rime_ice.table.bin` 重建到 60MB。

**教训**：`sort: origin` 的词典，拼音码必须严格有序。手写词库时按码排好再存，别指望 Rime 帮你排。

### 坑 2：万象单字母 `l` 不出候选

一度以为是配置错了。实际上配置本来就支持（`enable_completion` + 简码规则都在），**是默认方案（雾凇）已经死了**，输入法状态错乱，导致看起来像万象的问题。

雾凇复活之后，一切正常。**排查顺序应该是：先确认默认方案是活的，再怀疑具体方案配置。**

### 坑 3：万象"变慢"

同理。之前默认进的是死的雾凇，每次打字都得先手动切到万象，主观上就是"卡"。修好默认方案后不再需要切。

### 坑 4：一条无害但烦人的警告

```
lua/wanxiang/custom_phrase.lua:206
attempt to call a nil value (method 'disconnect')
```

librime 1.13.1 里没有 `disconnect` 方法，析构时报警告。**不影响功能、不影响速度**，可以用 `pcall` 包一层消掉（非紧急，我一直没管）。

会看日志的人应该都会发现：Rime 的坑几乎全是**"配置合法但不合约定"**导致的静默失败，没有异常栈可看。所以每次改完，一定要跑下面的验证清单。

## 七、日常维护与备份

- 改词库/配置 → **必须重新部署**，否则等于没改。
- **备份**：Rime 没有官方云同步。多机一致的两种做法：
  - `mklink /D` 软链到 OneDrive / 坚果云；
  - 用 git 管 `C:\Rime`，**忽略 `build/` 与 `*.userdb`**（这俩能占掉绝大部分体积，且都是可重建/个人化的）。
- **加新词库**：只动 `import_tables` 和 `domain_dicts/`，别去改 `default.yaml` 的全局段落。
- **快速验证清单**（每次部署完打一遍，30 秒）：

  1. 雾凇（默认）打 `nihao` → 出「你好」等中文
  2. 切万象打单字母 `l` → 出「了 / 来 / 里…」候选
  3. 打 `kmbang` → 出颜文字

  三条都过，才算这次部署成功了。

## 八、如果你也想抄这套

最小路径：

1. 装 [小狼毫](https://github.com/rime/weasel)（或用 [東風破 plum](https://github.com/rime/plum) 一键装方案）
2. 上 [雾凇拼音](https://github.com/iDvel/rime-ice) 打底，按它的 wiki 配 `default.custom.yaml`
3. 想要整句更强，再加 [万象拼音](https://github.com/amzxyz/rime-wanxiang)，把 `wanxiang` 排进 `schema_list` 第 2 位
4. 把 `import_tables` 指向你自己的 `domain_dicts/`——**这一步才是把它变成"你的"输入法的关键**
5. 严格走第五节的部署顺序，每次都跑验证清单

---

配置能跑通就别手痒乱改全局文件。Rime 的失败模式不是崩给你看，是安静地不出字。**改一处，验三条。**

> 相关资源我整理在站内那篇置顶的「🔗 常用资源导航」的 **⌨️ 输入法 & 文本** 一节里了：各平台前端、词库方案、定制文档，都是点开能用的。
