/**
 * Markdown配置工具
 * 統一配置所有markdown渲染器，包含數學公式支持
 */

import katex from 'katex';
import 'katex/dist/katex.min.css';

/**
 * 創建支持數學公式的markdown插件 (使用KaTeX)
 * 使用正確的 markdown-it 插件模式
 */
export const createMathPlugin = () => {
  return {
    plugin: (md: any) => {
      // 添加inline math規則
      md.inline.ruler.before('escape', 'math_inline', (state: any, silent: boolean) => {
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
      md.block.ruler.before('fence', 'math_block', (state: any, start: number, end: number, silent: boolean) => {
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
      md.renderer.rules.math_inline = (tokens: any[], idx: number) => {
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
      md.renderer.rules.math_block = (tokens: any[], idx: number) => {
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
export const createLinkPlugin = () => {
  return {
    plugin: (md: any) => {
      // 修改鏈接渲染規則
      const defaultRender = md.renderer.rules.link_open || function(tokens: any[], idx: number, options: any, env: any, renderer: any) {
        return renderer.renderToken(tokens, idx, options);
      };

      md.renderer.rules.link_open = function (tokens: any[], idx: number, options: any, env: any, renderer: any) {
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
export const createMarkdownPlugins = () => {
  return [
    createMathPlugin(),
    createLinkPlugin()
  ];
};