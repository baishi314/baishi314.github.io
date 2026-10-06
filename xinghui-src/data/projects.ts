// 项目列表

export type Project = {
  id: string;
  name: string;
  description: string;
  icon: string;
  githubUrl: string;
  tags: string[];
};

export const projectsData: Project[] = [
  {
    id: "blog",
    name: "个人博客系统",
    githubUrl: "https://github.com/baishi314/baishi314.github.io",
    description: "你正在看的这个站。三套主题共用一个仓库，静态导出后托管在 GitHub Pages。",
    icon: "🏠",
    tags: ["Next.js", "React", "Tailwind"],
  },
  {
    id: "minecraft",
    name: "Minecraft 生电工具",
    githubUrl: "",
    description: "自己用的红石机器与建筑自动化脚本，主要是懒得手挖。",
    icon: "⛏️",
    tags: ["Python", "Minecraft"],
  },
  {
    id: "notes",
    name: "学习笔记整理",
    githubUrl: "",
    description: "把散在各处的笔记归一整理，顺手放到网上，方便自己随时查。",
    icon: "📝",
    tags: ["笔记", "整理"],
  },
];
