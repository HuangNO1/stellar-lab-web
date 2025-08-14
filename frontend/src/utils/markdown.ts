/**
 * Markdown配置工具
 * 統一配置所有markdown渲染器，包含數學公式支持
 */

import katex from 'katex';
import 'katex/dist/katex.min.css';

// 定义 markdown-it 相关类型
interface MarkdownIt {
  inline: {
    ruler: {
      before(name: string, ruleName: string, rule: (state: StateInline, silent: boolean) => boolean): void;
    };
  };
  block: {
    ruler: {
      before(name: string, ruleName: string, rule: (state: StateBlock, start: number, end: number, silent: boolean) => boolean): void;
    };
  };
  renderer: {
    rules: Record<string, (tokens: Token[], idx: number, options?: unknown, env?: unknown, renderer?: unknown) => string>;
  };
}

interface StateInline {
  pos: number;
  posMax: number;
  src: string;
  push(type: string, tag: string, nesting: number): Token;
}

interface StateBlock {
  bMarks: number[];
  eMarks: number[];
  tShift: number[];
  sCount: number[];
  blkIndent: number;
  src: string;
  line: number;
  getLines(begin: number, end: number, indent: number, keepLastLF: boolean): string;
  push(type: string, tag: string, nesting: number): Token;
}

interface Token {
  markup: string;
  content: string;
  block?: boolean;
  attrGet(name: string): string | null;
  attrSet(name: string, value: string): void;
}

interface MarkdownPlugin {
  plugin: (md: MarkdownIt) => void;
}

interface RendererFunction {
  (tokens: Token[], idx: number, options?: unknown, env?: unknown, renderer?: unknown): string;
}

/**
 * 創建支持數學公式的markdown插件 (使用KaTeX)
 * 使用正確的 markdown-it 插件模式
 */
export const createMathPlugin = (): MarkdownPlugin => {
  return {
    plugin: (md: MarkdownIt) => {
      // 添加inline math規則
      md.inline.ruler.before('escape', 'math_inline', (state: StateInline, silent: boolean) => {
        const start = state.pos;
        const marker = state.src.charCodeAt(start);
        
        // 檢查是否以 $ 開始
        if (marker !== 0x24 /* $ */) {
          return false;
        }
        
        // 檢查是否是 $$ (display math)
        if (state.src.charCodeAt(start + 1) === 0x24) {
          return false;
        }
        
        let pos = start + 1;
        let found = false;
        
        // 查找結束的 $
        while (pos < state.posMax) {
          const char = state.src.charCodeAt(pos);
          
          if (char === 0x24 /* $ */) {
            found = true;
            break;
          }
          
          if (char === 0x0A /* \n */) {
            break;
          }
          
          pos++;
        }
        
        if (!found || pos === start + 1) {
          return false;
        }
        
        const content = state.src.slice(start + 1, pos);
        
        if (!silent) {
          const token = state.push('math_inline', 'math', 0);
          token.markup = '$';
          token.content = content;
        }
        
        state.pos = pos + 1;
        return true;
      });
      
      // 添加block math規則
      md.block.ruler.before('fence', 'math_block', (state: StateBlock, start: number, end: number, silent: boolean) => {
        const pos = state.bMarks[start] + state.tShift[start];
        const max = state.eMarks[start];
        
        if (pos + 2 > max) {
          return false;
        }
        
        const marker = state.src.slice(pos, pos + 2);
        if (marker !== '$$') {
          return false;
        }
        
        let nextLine = start + 1;
        let found = false;
        
        while (nextLine < end) {
          const linePos = state.bMarks[nextLine] + state.tShift[nextLine];
          const lineMax = state.eMarks[nextLine];
          
          if (linePos < lineMax && state.sCount[nextLine] < state.blkIndent) {
            break;
          }
          
          if (state.src.slice(linePos, linePos + 2) === '$$') {
            found = true;
            break;
          }
          
          nextLine++;
        }
        
        if (!found) {
          return false;
        }
        
        const content = state.getLines(start + 1, nextLine, 0, false).trim();
        
        if (!silent) {
          const token = state.push('math_block', 'div', 0);
          token.block = true;
          token.content = content;
          token.markup = '$$';
        }
        
        state.line = nextLine + 1;
        return true;
      });
      
      // 渲染inline math
      md.renderer.rules.math_inline = (tokens: Token[], idx: number) => {
        const token = tokens[idx];
        try {
          const rendered = katex.renderToString(token.content, {
            displayMode: false,
            throwOnError: false,
            errorColor: '#cc0000',
            strict: false
          });
          return `<span class="math-inline">${rendered}</span>`;
        } catch (error) {
          console.warn('KaTeX inline render error:', error);
          return `<span class="math-inline math-error">$${token.content}$</span>`;
        }
      };
      
      // 渲染block math
      md.renderer.rules.math_block = (tokens: Token[], idx: number) => {
        const token = tokens[idx];
        try {
          const rendered = katex.renderToString(token.content, {
            displayMode: true,
            throwOnError: false,
            errorColor: '#cc0000',
            strict: false
          });
          return `<div class="math-display">${rendered}</div>`;
        } catch (error) {
          console.warn('KaTeX block render error:', error);
          return `<div class="math-display math-error">$$${token.content}$$</div>`;
        }
      };
    }
  };
};

/**
 * 創建鏈接處理插件
 * 為外部鏈接添加target="_blank"和安全屬性
 */
export const createLinkPlugin = (): MarkdownPlugin => {
  return {
    plugin: (md: MarkdownIt) => {
      // 修改鏈接渲染規則
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const defaultRender: RendererFunction = md.renderer.rules.link_open || function(tokens: Token[], idx: number, _options?: unknown, _env?: unknown, _renderer?: unknown) {
        // 如果沒有預設渲染函數，提供一個基本實現
        const token = tokens[idx];
        let attrs = '';
        if (token.attrGet) {
          // 這裡簡化處理，實際實現會更複雜
          const href = token.attrGet('href');
          if (href) attrs += ` href="${href}"`;
        }
        return `<a${attrs}>`;
      };

      md.renderer.rules.link_open = function (tokens: Token[], idx: number, options?: unknown, env?: unknown, renderer?: unknown) {
        const token = tokens[idx];
        const href = token.attrGet('href');
        
        // 檢查是否為外部鏈接
        if (href && (href.startsWith('http://') || href.startsWith('https://') || href.startsWith('//') || href.includes('://'))) {
          // 為外部鏈接添加安全屬性
          token.attrSet('target', '_blank');
          token.attrSet('rel', 'noopener noreferrer');
        }
        
        return defaultRender(tokens, idx, options, env, renderer);
      };
    }
  };
};

/**
 * 創建完整的markdown插件配置
 * 包含數學公式和鏈接處理
 */
export const createMarkdownPlugins = (): MarkdownPlugin[] => {
  return [
    createMathPlugin(),
    createLinkPlugin()
  ];
};