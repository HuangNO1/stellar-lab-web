import { ComponentCustomProperties } from 'vue'

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $t: (key: string, ...args: any[]) => string
    $tc: (key: string, choice?: number, values?: any) => string
    $te: (key: string) => boolean
    $d: (value: number | Date, ...args: any[]) => string
    $n: (value: number, ...args: any[]) => string
  }
}