// 本文件由 content-source/sync-content.py 自动生成，请勿手改

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
    id: "study-script",
    name: "学习通类人刷课工程",
    githubUrl: "",
    description: "基于 Chrome profile + 类人鼠标键盘 + 截图视觉识别，推进课程视频与测验闭环，严格规避风控。",
    icon: "🎯",
    tags: ["Python", "自动化", "图像识别"],
  },
  {
    id: "auto-framework",
    name: "auto-framework",
    githubUrl: "",
    description: "通用自动化框架，178+ 测试通过，打包为 8MB 单文件 exe，免 Python 运行时即可运行。",
    icon: "⚙️",
    tags: ["Node.js", "PyInstaller", "单文件"],
  },
  {
    id: "html-tools",
    name: "单文件 HTML 教具系列",
    githubUrl: "",
    description: "空间向量 / 平面向量 / 复数 / 二次函数 / 抛体运动实验室，零依赖双击即开，深色主题自适应。",
    icon: "📐",
    tags: ["HTML", "交互可视化", "教学"],
  },
  {
    id: "science-anim",
    name: "理科动画短视频框架",
    githubUrl: "",
    description: "science-anim-studio：结构化生成理科教学短视频脚本与画面，降低内容制作门槛。",
    icon: "🎬",
    tags: ["内容生成", "教学"],
  },
  {
    id: "dsh",
    name: "DeepSeek Harness 本地套件",
    githubUrl: "",
    description: "本地 Web GUI 调用 deepseek-v4-pro，配套多模型中转与批量 AI 编程任务统一调度。",
    icon: "🤖",
    tags: ["本地 AI", "Web GUI", "Agent"],
  },
  {
    id: "mc-gen",
    name: "Minecraft 生电机械生成器",
    githubUrl: "",
    description: "「赤石科技」系列：用 Python 脚本按 LSB-first 位打包直接生成 .litematic 投影，把红石机械做成可一键贴的雕像式结构。",
    icon: "⛏️",
    tags: ["Python", "Litematica", "生电"],
  },
  {
    id: "office-auto",
    name: "Office / 演示自动化",
    githubUrl: "",
    description: "基于 WPS COM 的文档批处理链路：docx 转 PDF、PPT 导 PNG、OOXML 手改与校验，把排版活交给脚本。",
    icon: "📊",
    tags: ["WPS COM", "OOXML", "自动化"],
  },
];
