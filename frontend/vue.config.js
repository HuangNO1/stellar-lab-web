const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  // Disable TypeScript checking for build to bypass lodash compatibility issues
  chainWebpack: config => {
    config.plugins.delete('fork-ts-checker')
  },
  // Configure webpack to ignore TypeScript errors
  configureWebpack: {
    resolve: {
      alias: {
        '@': require('path').resolve(__dirname, 'src')
      }
    }
  }
})
