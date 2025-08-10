/**
 * 媒體文件相關工具函數
 */

/**
 * 獲取媒體文件的完整URL
 * @param path 媒體文件路徑
 * @returns 完整的URL地址
 */
export const getMediaUrl = (path: string): string => {
  if (!path) return '';
  
  // 如果已經是完整URL，直接返回
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path;
  }
  
  // 否則拼接API基礎URL
  const baseUrl = process.env.VUE_APP_API_BASE_URL?.replace('/api', '') || 'http://127.0.0.1:8000';
  return `${baseUrl}${path}`;
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