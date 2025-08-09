declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

// Vue 3 module exports fix
declare module 'vue' {
  export * from '@vue/runtime-dom'
  export * from '@vue/runtime-core'
  export * from '@vue/reactivity'
  export * from '@vue/shared'
  
  // Explicit exports for commonly used functions
  export const ref: typeof import('@vue/reactivity').ref
  export const computed: typeof import('@vue/reactivity').computed
  export const reactive: typeof import('@vue/reactivity').reactive
  export const readonly: typeof import('@vue/reactivity').readonly
  export const watch: typeof import('@vue/runtime-core').watch
  export const watchEffect: typeof import('@vue/runtime-core').watchEffect
  export const onMounted: typeof import('@vue/runtime-core').onMounted
  export const onUnmounted: typeof import('@vue/runtime-core').onUnmounted
  export const onUpdated: typeof import('@vue/runtime-core').onUpdated
  export const onBeforeMount: typeof import('@vue/runtime-core').onBeforeMount
  export const onBeforeUnmount: typeof import('@vue/runtime-core').onBeforeUnmount
  export const onBeforeUpdate: typeof import('@vue/runtime-core').onBeforeUpdate
}