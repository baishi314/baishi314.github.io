export interface Friend { id: string; name: string; url: string; description: string; avatar: string; themeColor: string; }

export const friendsData: Friend[] = [
  {
    id: "github",
    name: "GitHub",
    description: "全世界程序员的家，我的代码也在这里。",
    avatar: "/avatar.svg",
    url: "https://github.com",
    themeColor: "rgba(99, 102, 241, 0.5)",
  },
  {
    id: "bgm",
    name: "Bangumi 番组计划",
    description: "追番记录与评分，看过的动画都在这。",
    avatar: "/avatar.svg",
    url: "https://bgm.tv",
    themeColor: "rgba(236, 72, 153, 0.5)",
  },
  {
    id: "mdn",
    name: "MDN Web Docs",
    description: "写前端时最常查的文档。",
    avatar: "/avatar.svg",
    url: "https://developer.mozilla.org/zh-CN/",
    themeColor: "rgba(56, 189, 248, 0.5)",
  },
];
