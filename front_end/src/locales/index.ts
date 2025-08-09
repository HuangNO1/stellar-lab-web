import { createI18n } from 'vue-i18n'
import Cookies from 'js-cookie'
import zh from './zh'
import en from './en'

// Get language from cookie or default to Chinese
const getDefaultLanguage = (): string => {
  const savedLanguage = Cookies.get('language')
  if (savedLanguage && ['zh', 'en'].includes(savedLanguage)) {
    return savedLanguage
  }
  // Browser language detection
  const browserLanguage = navigator.language.toLowerCase()
  if (browserLanguage.includes('zh')) {
    return 'zh'
  }
  return 'en'
}

// Set language to cookie
export const setLanguage = (language: string): void => {
  Cookies.set('language', language, { expires: 365 }) // Save for 1 year
}

// Theme utilities
export const getTheme = (): string => {
  const savedTheme = Cookies.get('theme')
  if (savedTheme && ['light', 'dark'].includes(savedTheme)) {
    return savedTheme
  }
  // Default to light theme
  return 'light'
}

export const setTheme = (theme: string): void => {
  Cookies.set('theme', theme, { expires: 365 }) // Save for 1 year
}

// Create i18n instance
const i18n = createI18n({
  locale: getDefaultLanguage(),
  fallbackLocale: 'zh', // Fallback to Chinese
  messages: {
    zh,
    en
  },
  legacy: false, // Use Composition API mode
  globalInjection: true // Enable global $t function
})

export default i18n