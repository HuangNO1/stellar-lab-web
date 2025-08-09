/// <reference types="vite/client" />

declare interface ImportMetaEnv {
  readonly VITE_USE_MOCK: string
  readonly VITE_API_BASE_URL: string
  readonly VITE_NODE_ENV: string
}

declare interface ImportMeta {
  readonly env: ImportMetaEnv
}

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $router: import('vue-router').Router
    $route: import('vue-router').RouteLocationNormalizedLoaded
  }
}