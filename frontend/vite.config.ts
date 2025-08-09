import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { viteMockServe } from 'vite-plugin-mock'
import { resolve } from 'path'

export default defineConfig(({ mode, command }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const useMock = env.VITE_USE_MOCK === 'true'
  
  return {
    plugins: [
      vue(),
      ...(useMock && command === 'serve' ? [viteMockServe({
        mockPath: 'src/mock',
        localEnabled: true,
        prodEnabled: false,
        logger: true,
      })] : []),
    ],
    resolve: {
      alias: {
        '@': resolve(__dirname, 'src'),
      },
    },
    server: {
      port: 3000,
      ...(useMock ? {} : {
        proxy: {
          '/api': {
            target: 'http://localhost:8000',
            changeOrigin: true,
          },
        },
      }),
    },
  }
})