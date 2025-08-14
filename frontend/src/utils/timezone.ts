/**
 * 時區處理工具函數
 * 統一處理前端時間顯示和格式化
 */

import { useI18n } from 'vue-i18n';

/**
 * 解析 UTC 時間字符串並轉換為 Date 對象
 * @param utcTimeString - UTC 時間字符串 (ISO 格式)
 * @returns Date 對象
 */
export function parseUTCTime(utcTimeString: string): Date {
  // 確保時間字符串以 Z 結尾表示 UTC
  let isoString = utcTimeString;
  if (!isoString.endsWith('Z') && !isoString.includes('+') && !isoString.includes('-', 10)) {
    isoString += 'Z';
  }
  return new Date(isoString);
}

/**
 * 格式化時間為本地時間字符串
 * @param utcTimeString - UTC 時間字符串
 * @param locale - 語言環境 ('zh' | 'en')
 * @param options - 格式化選項
 * @returns 格式化的時間字符串
 */
export function formatDateTime(
  utcTimeString: string, 
  locale: 'zh' | 'en' = 'zh',
  options?: Intl.DateTimeFormatOptions
): string {
  const date = parseUTCTime(utcTimeString);
  
  const defaultOptions: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: locale === 'en'
  };
  
  const formatOptions = { ...defaultOptions, ...options };
  const localeString = locale === 'zh' ? 'zh-CN' : 'en-US';
  
  return date.toLocaleString(localeString, formatOptions);
}

/**
 * 格式化時間為相對時間（多久前）
 * @param utcTimeString - UTC 時間字符串
 * @param t - i18n 翻譯函數
 * @returns 相對時間字符串
 */
export function formatRelativeTime(utcTimeString: string, t: (key: string) => string): string {
  const date = parseUTCTime(utcTimeString);
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  
  const minutes = Math.floor(diff / (1000 * 60));
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);
  const months = Math.floor(days / 30);
  const years = Math.floor(days / 365);

  if (years > 0) {
    return `${years}${t('admin.quickAction.timeFormat.yearsAgo')}`;
  } else if (months > 0) {
    return `${months}${t('admin.quickAction.timeFormat.monthsAgo')}`;
  } else if (days > 0) {
    return `${days}${t('admin.quickAction.timeFormat.daysAgo')}`;
  } else if (hours > 0) {
    return `${hours}${t('admin.quickAction.timeFormat.hoursAgo')}`;
  } else if (minutes > 0) {
    return `${minutes}${t('admin.quickAction.timeFormat.minutesAgo')}`;
  } else {
    return t('admin.quickAction.timeFormat.justNow');
  }
}

/**
 * 格式化時間為簡短相對時間（用於列表顯示）
 * @param utcTimeString - UTC 時間字符串
 * @param t - i18n 翻譯函數
 * @returns 簡短相對時間字符串
 */
export function formatShortRelativeTime(utcTimeString: string, t: (key: string) => string): string {
  const date = parseUTCTime(utcTimeString);
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  
  const minutes = Math.floor(diff / (1000 * 60));
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (days > 0) {
    return `${days}${t('admin.quickAction.timeFormat.daysAgo')}`;
  } else if (hours > 0) {
    return `${hours}${t('admin.quickAction.timeFormat.hoursAgo')}`;
  } else if (minutes > 0) {
    return `${minutes}${t('admin.quickAction.timeFormat.shortMinutesAgo')}`;
  } else {
    return t('admin.quickAction.timeFormat.now');
  }
}

/**
 * 獲取當前時區信息
 * @returns 時區信息對象
 */
export function getCurrentTimezone(): { 
  name: string; 
  offset: string; 
  offsetMinutes: number 
} {
  const date = new Date();
  const offsetMinutes = -date.getTimezoneOffset();
  const offsetHours = Math.floor(Math.abs(offsetMinutes) / 60);
  const offsetMins = Math.abs(offsetMinutes) % 60;
  const offsetSign = offsetMinutes >= 0 ? '+' : '-';
  
  return {
    name: Intl.DateTimeFormat().resolvedOptions().timeZone,
    offset: `UTC${offsetSign}${offsetHours.toString().padStart(2, '0')}:${offsetMins.toString().padStart(2, '0')}`,
    offsetMinutes
  };
}

/**
 * Vue 組合式函數：提供統一的時間格式化功能
 */
export function useTimeFormatter() {
  const { locale, t } = useI18n();
  
  const getCurrentLocale = (): 'zh' | 'en' => {
    return locale.value as 'zh' | 'en';
  };
  
  return {
    formatDateTime: (utcTimeString: string, options?: Intl.DateTimeFormatOptions) => 
      formatDateTime(utcTimeString, getCurrentLocale(), options),
    formatRelativeTime: (utcTimeString: string) => 
      formatRelativeTime(utcTimeString, t),
    formatShortRelativeTime: (utcTimeString: string) => 
      formatShortRelativeTime(utcTimeString, t),
    parseUTCTime,
    getCurrentTimezone,
    getCurrentLocale
  };
}