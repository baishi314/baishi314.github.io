export interface Photo { url: string; caption?: string; }
export interface Album { id: string; title: string; description: string; cover: string; date: string; photos: Photo[]; }

// 相册暂空，后续放上自己拍的照片
export const albums: Album[] = [];
