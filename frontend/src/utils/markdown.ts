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
 * 創建研究領域TAG插件
 * 支持 {{research: 機器學習, 深度學習, 計算機視覺}} 語法
 */
export const createResearchTagPlugin = (): MarkdownPlugin => {
  return {
    plugin: (md: MarkdownIt) => {
      // 添加研究領域TAG規則
      md.inline.ruler.before('escape', 'research_tag', (state: StateInline, silent: boolean) => {
        const start = state.pos;
        const marker = state.src.slice(start, start + 12); // "{{research:"
        
        // 檢查是否以 {{research: 開始
        if (marker !== '{{research:') {
          return false;
        }
        
        let pos = start + 12;
        let found = false;
        
        // 查找結束的 }}
        while (pos < state.posMax - 1) {
          if (state.src.slice(pos, pos + 2) === '}}') {
            found = true;
            break;
          }
          pos++;
        }
        
        if (!found) {
          return false;
        }
        
        const content = state.src.slice(start + 12, pos).trim();
        
        if (!silent) {
          const token = state.push('research_tag', 'div', 0);
          token.markup = '{{research:}}';
          token.content = content;
        }
        
        state.pos = pos + 2;
        return true;
      });
      
      // 渲染研究領域TAG
      md.renderer.rules.research_tag = (tokens: Token[], idx: number) => {
        const token = tokens[idx];
        
        // 檢查是否包含背景色語法: areas[bg:#ffffff]
        let backgroundColor = null;
        let content = token.content;
        const backgroundMatch = content.match(/^(.*?)\[bg:#([0-9a-fA-F]{6})\]$/);
        if (backgroundMatch) {
          backgroundColor = `#${backgroundMatch[2]}`;
          content = backgroundMatch[1];
        }
        
        const areas = content.split(',').map(area => area.trim()).filter(area => area);
        
        if (areas.length === 0) {
          return '';
        }
        
        // 颜色循环：蓝色、资讯蓝、绿色、橙色、红色
        const colors = ['#1890ff', '#13c2c2', '#52c41a', '#fa8c16', '#f5222d'];
        
        const tags = areas.map((area, index) => {
          // 检查是否包含自定义颜色语法：文本#颜色
          const colorMatch = area.match(/^(.+?)#([0-9a-fA-F]{6})$/);
          if (colorMatch) {
            const text = colorMatch[1].trim();
            const color = `#${colorMatch[2]}`;
            // 计算文字颜色
            const textColor = getContrastColor(color);
            return `<span class="research-tag" style="background-color: ${color}; color: ${textColor}; border-color: ${color};">${text}</span>`;
          } else {
            // 使用循环颜色
            const color = colors[index % colors.length];
            return `<span class="research-tag" style="background-color: ${color}; border-color: ${color};">${area}</span>`;
          }
        }).join('');
        
        // 根據是否有自定義背景色設置樣式
        const containerStyle = backgroundColor 
          ? `style="--research-tags-bg: ${backgroundColor}; --research-tags-border: ${backgroundColor};"` 
          : '';
        
        return `<div class="research-tags-container" ${containerStyle}>
          <span class="research-tags-label">研究領域：</span>
          <div class="research-tags">${tags}</div>
        </div>`;
      };
    }
  };
};

// 计算对比色
function getContrastColor(hexColor: string): string {
  // 移除#号
  const hex = hexColor.replace('#', '');
  
  // 转换为RGB
  const r = parseInt(hex.substr(0, 2), 16);
  const g = parseInt(hex.substr(2, 2), 16);
  const b = parseInt(hex.substr(4, 2), 16);
  
  // 计算亮度 (使用相对亮度公式)
  const brightness = (r * 299 + g * 587 + b * 114) / 1000;
  
  // 如果背景较亮使用深色文字，否则使用浅色文字
  return brightness > 128 ? '#000000' : '#ffffff';
}

/**
 * 創建個人主頁URL TAG插件
 * 支持 {{homepage: https://example.com}} 語法
 */
export const createHomepageTagPlugin = (): MarkdownPlugin => {
  return {
    plugin: (md: MarkdownIt) => {
      // 添加個人主頁TAG規則
      md.inline.ruler.before('escape', 'homepage_tag', (state: StateInline, silent: boolean) => {
        const start = state.pos;
        const marker = state.src.slice(start, start + 12); // "{{homepage:"
        
        // 檢查是否以 {{homepage: 開始
        if (marker !== '{{homepage:') {
          return false;
        }
        
        let pos = start + 12;
        let found = false;
        
        // 查找結束的 }}
        while (pos < state.posMax - 1) {
          if (state.src.slice(pos, pos + 2) === '}}') {
            found = true;
            break;
          }
          pos++;
        }
        
        if (!found) {
          return false;
        }
        
        const content = state.src.slice(start + 12, pos).trim();
        
        if (!silent) {
          const token = state.push('homepage_tag', 'div', 0);
          token.markup = '{{homepage:}}';
          token.content = content;
        }
        
        state.pos = pos + 2;
        return true;
      });
      
      // 渲染個人主頁TAG
      md.renderer.rules.homepage_tag = (tokens: Token[], idx: number) => {
        const token = tokens[idx];
        const url = token.content.trim();
        
        if (!url) {
          return '';
        }
        
        // 驗證URL格式
        let validUrl = url;
        if (!url.startsWith('http://') && !url.startsWith('https://')) {
          validUrl = `https://${url}`;
        }
        
        return `<div class="homepage-container">
          <span class="homepage-label">個人主頁：</span>
          <a href="${validUrl}" target="_blank" rel="noopener noreferrer" class="homepage-link">
            <svg class="homepage-icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
            </svg>
            <span class="homepage-text">訪問個人主頁</span>
            <svg class="homepage-external-icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M19 19H5V5h7V3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2v-7h-2v7zM14 3v2h3.59l-9.83 9.83 1.41 1.41L19 6.41V10h2V3h-7z"/>
            </svg>
          </a>
        </div>`;
      };
    }
  };
};

/**
 * 創建論文列表TAG插件
 * 支持 {{papers: 1,2,3}} 語法
 */
export const createPapersTagPlugin = (): MarkdownPlugin => {
  return {
    plugin: (md: MarkdownIt) => {
      // 添加論文列表TAG規則
      md.inline.ruler.before('escape', 'papers_tag', (state: StateInline, silent: boolean) => {
        const start = state.pos;
        const marker = state.src.slice(start, start + 10); // "{{papers:"
        
        // 檢查是否以 {{papers: 開始
        if (marker !== '{{papers:') {
          return false;
        }
        
        let pos = start + 10;
        let found = false;
        
        // 查找結束的 }}
        while (pos < state.posMax - 1) {
          if (state.src.slice(pos, pos + 2) === '}}') {
            found = true;
            break;
          }
          pos++;
        }
        
        if (!found) {
          return false;
        }
        
        const content = state.src.slice(start + 10, pos).trim();
        
        if (!silent) {
          const token = state.push('papers_tag', 'div', 0);
          token.markup = '{{papers:}}';
          token.content = content;
        }
        
        state.pos = pos + 2;
        return true;
      });
      
      // 渲染論文列表TAG
      md.renderer.rules.papers_tag = (tokens: Token[], idx: number) => {
        const token = tokens[idx];
        const paperIds = token.content.split(',').map(id => id.trim()).filter(id => id && !isNaN(Number(id)));
        
        if (paperIds.length === 0) {
          return '';
        }
        
        return `<div class="papers-list-container" data-paper-ids="${paperIds.join(',')}">
          <span class="papers-list-label">相關論文：</span>
          <div class="papers-list-loading">
            <div class="loading-spinner"></div>
            <span>載入論文資訊中...</span>
          </div>
        </div>`;
      };
    }
  };
};
/**
 * 創建完整的markdown插件配置
 * 包含數學公式、鏈接處理和部分TAG插件
 * research TAG 由 MarkdownRenderer.vue 處理
 */
export const createMarkdownPlugins = (): MarkdownPlugin[] => {
  return [
    createMathPlugin(),
    createLinkPlugin(),
    // createResearchTagPlugin(), // 暂时禁用，由 MarkdownRenderer.vue 处理
    createHomepageTagPlugin(),
    createPapersTagPlugin()
  ];
};