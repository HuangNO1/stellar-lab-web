/* eslint-disable */
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

declare module 'vue3-markdown-it' {
  import { DefineComponent } from 'vue'
  const MarkdownIt: DefineComponent<{
    source?: string
    plugins?: any[]
    breaks?: boolean
    linkify?: boolean
    typographer?: boolean
    html?: boolean
    xhtmlOut?: boolean
    langPrefix?: string
    quotes?: string
    highlight?: (str: string, lang: string) => string
  }, {}, any>
  export default MarkdownIt
}
