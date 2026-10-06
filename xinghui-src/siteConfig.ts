// siteConfig.ts - 全站控制中心

export const siteConfig = {
  // 1. 站点标题与博主信息
  title: "baishi314 \u306e小窝",
  faviconUrl: "/favicon.svg",
  authorName: "baishi314",
  bio: "写代码、看动画、偶尔打游戏的一个人。",

  navTitle: "baishi314",

  navSuffix: " \u306e ",
  navAfter: "小窝",

  // 2. 头像
  avatarUrl: "/avatar.svg",

  // 3. 背景
  useGradient: true,
  themeColors: ["#a18cd1", "#fbc2eb", "#a1c4fd", "#c2e9fb"],
  bgImages: [],

  // 4. 文章默认封面
  defaultPostCover: "/cover-default.svg",

  // 5. 首页照片墙预览图
  photoWallImage: "/cover-default.svg",

  // 音乐播放列表（网易云歌曲 ID，前端直连 Meting API）
  cloudMusicIds: ["3438968283", "1809646618", "3361076230"],

  social: {
    github: "https://github.com/baishi314",
    gitee: "",
    google: "",
    email: "baishi3142396@163.com",
    qq: "",
    wechat: "",
  },
  counts: {
    photos: 0,
  },
  chatterTitle: "云端杂谈",
  chatterDescription: "代码、动画与生活的碎片记录",

  // 全局背景弹幕
  danmakuList: ["在干嘛呢？", "有蛋壳吗？", "前方高能反应！", "代码写完了吗", "今天背单词了吗？", "Hello World", "写算法中", "睡大觉中", "到底在干嘛？"],

  // 评论区：Giscus（无需后端）。填入仓库与讨论区 ID 后即可启用
  giscusConfig: {
    repo: "",
    repoId: "",
    category: "Announcements",
    categoryId: "",
  },

  buildDate: "2026-10-05T00:00:00",
  footerBadges: [
    { name: "Next.js", color: "text-sky-500", svg: "<path d=\"M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z\"/>" },
    { name: "React", color: "text-cyan-400", svg: "<path d=\"M12 22.6l-9.8-5.6V5.6L12 0l9.8 5.6v11.4l-9.8 5.6zm-8.2-6.5l8.2 4.7 8.2-4.7V7.5L12 2.8 3.8 7.5v8.6z\"/>" },
    { name: "Tailwind", color: "text-teal-400", svg: "<path d=\"M12.001,4.8c-3.2,0-5.2,1.6-6,4.8c1.2-1.6,2.6-2.2,4.2-1.8c0.913,0.228,1.565,0.89,2.288,1.624C13.666,10.618,15.027,12,18.001,12 c3.2,0,5.2-1.6,6-4.8c-1.2,1.6-2.6,2.2-4.2,1.8c-0.913-0.228-1.565-0.89-2.288-1.624C16.337,6.182,14.976,4.8,12.001,4.8z M6.001,12c-3.2,0-5.2,1.6-6,4.8c1.2-1.6,2.6-2.2,4.2-1.8c0.913,0.228,1.565,0.89,2.288,1.624c1.177,1.194,2.538,2.576,5.512,2.576 c3.2,0,5.2-1.6,6-4.8c-1.2,1.6-2.6,2.2-4.2,1.8c-0.913-0.228-1.565-0.89-2.288-1.624C10.337,13.382,8.976,12,6.001,12z\"/>" },
  ],

  friendLinkApplyFormat: "\u540d\u79f0\uff1abaishi314 \u306e\u5c0f\u7a9d\n\u7b80\u4ecb\uff1a\u5199\u4ee3\u7801\u3001\u770b\u52a8\u753b\u3001\u5076\u5c14\u6253\u6e38\u620f\n\u94fe\u63a5\uff1ahttps://baishi314.github.io/xinghui/\n\u5934\u50cf\uff1ahttps://baishi314.github.io/xinghui/avatar.svg",

  enableLevelSystem: true,
};

export default siteConfig;
