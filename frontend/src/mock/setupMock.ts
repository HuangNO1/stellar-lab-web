import Mock from 'mockjs'
import mockApi from './index'

// 環境變量控制 mock 開關
export const IS_MOCK = 
  (typeof import.meta !== 'undefined' && import.meta.env?.VITE_USE_MOCK === 'true') || 
  (typeof import.meta !== 'undefined' && import.meta.env?.DEV)

// Mock 服務設置
export function setupProdMockServer() {
  if (IS_MOCK) {
    console.log('[Mock] 正在設置 MockJS...')
    
    try {
      // 設置 Mock 延遲時間（避免調用 Mock.setup）
      // Mock.setup({
      //   timeout: '300-600'
      // })
      
      // 遍歷並註冊所有的 mock 接口
      mockApi.forEach(api => {
        Mock.mock(new RegExp(api.url), api.method, api.response)
        console.log(`[Mock] 註冊 ${api.method.toUpperCase()} ${api.url}`)
      })
      
      console.log('[Mock] MockJS 設置完成')
    } catch (error) {
      console.warn('[Mock] Mock setup error:', error)
    }
  } else {
    console.log('[Mock] MockJS 已禁用')
  }
}