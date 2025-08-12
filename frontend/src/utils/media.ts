/**
 * 媒體文件相關工具函數
 */

/**
 * 獲取媒體文件的完整URL
 * @param path 媒體文件路徑 (如: "/media/lab_logo/logo.png" 或 "lab_logo/logo.png")
 * @returns 完整的URL地址
 */
export const getMediaUrl = (path: string): string => {
  if (!path) return '';
  
  // 如果已經是完整URL，直接返回
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path;
  }
  
  // 根據API.md，媒體文件通過 /api/media/serve/{file_path} 獲取
  const baseUrl = process.env.VUE_APP_API_BASE_URL || 'http://127.0.0.1:8000/api';
  
  // 移除路徑開頭的 /media/ 前綴（如果存在）
  const cleanPath = path.startsWith('/media/') ? path.substring(7) : path;
  
  return `${baseUrl}/media/serve/${cleanPath}`;
};

/**
 * 獲取媒體文件資訊的URL
 * @param path 媒體文件路徑
 * @returns 文件資訊URL
 */
export const getMediaInfoUrl = (path: string): string => {
  if (!path) return '';
  
  const baseUrl = process.env.VUE_APP_API_BASE_URL || 'http://127.0.0.1:8000/api';
  const cleanPath = path.startsWith('/media/') ? path.substring(7) : path;
  
  return `${baseUrl}/media/info/${cleanPath}`;
};

/**
 * 上傳媒體文件的URL
 * @returns 上傳接口URL
 */
export const getMediaUploadUrl = (): string => {
  const baseUrl = process.env.VUE_APP_API_BASE_URL || 'http://127.0.0.1:8000/api';
  return `${baseUrl}/media/upload`;
};

/**
 * 獲取實驗室Logo URL
 * @param logoPath Logo路徑
 * @returns Logo URL，如果沒有則返回空字符串
 */
export const getLabLogoUrl = (logoPath?: string): string => {
  return logoPath ? getMediaUrl(logoPath) : '';
};

/**
 * 獲取輪播圖URL列表
 * @param carousel1 輪播圖1路徑
 * @param carousel2 輪播圖2路徑
 * @param carousel3 輪播圖3路徑
 * @param carousel4 輪播圖4路徑
 * @returns 有效的輪播圖URL數組
 */
export const getCarouselUrls = (
  carousel1?: string,
  carousel2?: string,
  carousel3?: string,
  carousel4?: string
): string[] => {
  const urls: string[] = [];
  
  if (carousel1) urls.push(getMediaUrl(carousel1));
  if (carousel2) urls.push(getMediaUrl(carousel2));
  if (carousel3) urls.push(getMediaUrl(carousel3));
  if (carousel4) urls.push(getMediaUrl(carousel4));
  
  return urls;
};

/**
 * 獲取所有有效輪播圖URL列表
 * @param carousel1 輪播圖1路徑
 * @param carousel2 輪播圖2路徑
 * @param carousel3 輪播圖3路徑
 * @param carousel4 輪播圖4路徑
 * @returns 有效的輪播圖URL數組
 */
export const getValidCarouselUrls = (
  carousel1?: string,
  carousel2?: string,
  carousel3?: string,
  carousel4?: string
): string[] => {
  const urls: string[] = [];
  
  if (carousel1) urls.push(getMediaUrl(carousel1));
  if (carousel2) urls.push(getMediaUrl(carousel2));
  if (carousel3) urls.push(getMediaUrl(carousel3));
  if (carousel4) urls.push(getMediaUrl(carousel4));
  
  return urls;
};

/**
 * 獲取預設輪播圖URL列表
 * @returns 預設輪播圖URL數組
 */
export const getDefaultCarouselUrls = (): string[] => {
  return [
    'https://naive-ui.oss-cn-beijing.aliyuncs.com/carousel-img/carousel1.jpeg',
    'https://naive-ui.oss-cn-beijing.aliyuncs.com/carousel-img/carousel2.jpeg'
  ];
};

/**
 * 獲取成員頭像URL
 * @param avatarPath 頭像路徑
 * @returns 頭像URL，如果沒有則返回默認頭像
 */
export const getMemberAvatarUrl = (avatarPath?: string): string => {
  return avatarPath ? getMediaUrl(avatarPath) : '/default-avatar.png';
};

/**
 * 獲取論文文件URL
 * @param filePath 文件路徑
 * @returns 文件URL
 */
export const getPaperFileUrl = (filePath?: string): string => {
  return filePath ? getMediaUrl(filePath) : '';
};

/**
 * 檢查是否有有效的輪播圖
 * @param carousel1 輪播圖1路徑
 * @param carousel2 輪播圖2路徑
 * @param carousel3 輪播圖3路徑
 * @param carousel4 輪播圖4路徑
 * @returns 是否有任何有效的輪播圖
 */
export const hasCarouselImages = (
  carousel1?: string,
  carousel2?: string,
  carousel3?: string,
  carousel4?: string
): boolean => {
  return !!(carousel1 || carousel2 || carousel3 || carousel4);
};

/**
 * 檢查文件是否為圖片
 * @param path 文件路徑或文件名
 * @returns 是否為圖片文件
 */
export const isImageFile = (path: string): boolean => {
  if (!path) return false;
  const imageExtensions = /\.(jpg|jpeg|png|gif|webp|svg)$/i;
  return imageExtensions.test(path);
};

/**
 * 檢查文件是否為PDF
 * @param path 文件路徑或文件名
 * @returns 是否為PDF文件
 */
export const isPdfFile = (path: string): boolean => {
  if (!path) return false;
  return /\.pdf$/i.test(path);
};

/**
 * 獲取文件類型根據文件擴展名
 * @param path 文件路徑或文件名
 * @returns 文件類型（image, pdf, other）
 */
export const getFileType = (path: string): 'image' | 'pdf' | 'other' => {
  if (!path) return 'other';
  
  if (isImageFile(path)) return 'image';
  if (isPdfFile(path)) return 'pdf';
  return 'other';
};

/**
 * 格式化文件大小
 * @param bytes 字節數
 * @returns 格式化後的文件大小字串
 */
export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B';
  
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

/**
 * 根據API文檔定義的媒體文件類型
 */
export type MediaFileType = 'lab_logo' | 'member_avatar' | 'paper' | 'other';

/**
 * 根據文件路徑推斷媒體文件類型
 * @param path 文件路徑
 * @returns 媒體文件類型
 */
export const inferMediaType = (path: string): MediaFileType => {
  if (!path) return 'other';
  
  if (path.includes('lab_logo')) return 'lab_logo';
  if (path.includes('member_avatar')) return 'member_avatar';
  if (path.includes('paper')) return 'paper';
  
  return 'other';
};