/**
 * 去除文本中的 markdown 格式，返回純文本
 * @param text - 包含 markdown 格式的文本
 * @returns 純文本
 */
export function stripMarkdown(text: string): string {
  if (!text) return '';
  
  return text
    // 移除標題格式 (# ## ### 等)
    .replace(/^#{1,6}\s+/gm, '')
    // 移除粗體格式 (**text** 或 __text__)
    .replace(/\*\*(.*?)\*\*/g, '$1')
    .replace(/__(.*?)__/g, '$1')
    // 移除斜體格式 (*text* 或 _text_)
    .replace(/\*(.*?)\*/g, '$1')
    .replace(/_(.*?)_/g, '$1')
    // 移除刪除線格式 (~~text~~)
    .replace(/~~(.*?)~~/g, '$1')
    // 移除行內代碼格式 (`code`)
    .replace(/`(.*?)`/g, '$1')
    // 移除鏈接格式 [text](url)
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
    // 移除圖片格式 ![alt](url)
    .replace(/!\[([^\]]*)\]\([^)]*\)/g, '$1')
    // 移除代碼塊格式
    .replace(/```[\s\S]*?```/g, '')
    .replace(/```.*$/gm, '')
    // 移除引用格式 (> text)
    .replace(/^>\s+/gm, '')
    // 移除列表格式 (- item 或 * item 或 + item)
    .replace(/^[\s]*[-*+]\s+/gm, '')
    // 移除有序列表格式 (1. item)
    .replace(/^\d+\.\s+/gm, '')
    // 移除多餘的空行和空白字符
    .replace(/\n{2,}/g, '\n')
    .replace(/^\s+|\s+$/g, '')
    // 移除 HTML 標籤
    .replace(/<[^>]*>/g, '');
}