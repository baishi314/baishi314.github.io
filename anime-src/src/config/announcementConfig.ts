import type { AnnouncementConfig } from "../types/announcementConfig";

export const announcementConfig: AnnouncementConfig = {
	// 公告标题，留空则走i18n默认标题
	title: "",

	// 公告内容
	content: "这里是「二次元小屋」，风格大厅里的一个版本。想看别的风格可以回大厅。",

	// 是否允许用户关闭公告
	closable: true,

	link: {
		// 启用链接
		enable: true,
		// 链接文本
		text: "返回大厅",
		// 链接 URL
		url: "https://baishi314.github.io/",
		// 内部链接
		external: true,
	},
};
