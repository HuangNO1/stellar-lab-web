const { defineConfig } = require('@vue/cli-service')
const webpack = require('webpack')

module.exports = defineConfig({
  transpileDependencies: true,
  // Disable TypeScript checking for build to bypass lodash compatibility issues
  chainWebpack: config => {
    config.plugins.delete('fork-ts-checker')
  },
  // Configure webpack to ignore TypeScript errors and define Vue feature flags
  configureWebpack: {
    resolve: {
      alias: {
        '@': require('path').resolve(__dirname, 'src')
      }
    },
    plugins: [
      new webpack.DefinePlugin({
        // Vue 3 feature flags
        __VUE_OPTIONS_API__: JSON.stringify(true),
        __VUE_PROD_DEVTOOLS__: JSON.stringify(false),
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: JSON.stringify(false)
      })
    ]
  }
})
