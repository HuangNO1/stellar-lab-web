/**
 * 成員描述模板
 * 將模板從國際化文件中移出以避免 Vue i18n 編譯錯誤
 */

export const memberDescriptionTemplates = {
  zh: `## 個人簡介

[在此處介紹您的研究背景和學術經歷]

## 研究領域

{{research: 機器學習, 深度學習, 計算機視覺, 自然語言處理}}

## 個人主頁

{{github: https://github.com/your-username}}
{{scholar: https://scholar.google.com/citations?user=YOUR_ID}}
{{linkedin: https://linkedin.com/in/your-profile}}
{{researchgate: https://researchgate.net/profile/your-profile}}
{{website: https://your-personal-website.com}}

## 教育背景

- **年份-年份**: 學位, 學校/機構名稱
- **年份-年份**: 學位, 學校/機構名稱

## 代表性成果

### 實驗室論文
{{papers: 1,2,3}}

### 其他論文發表
- [論文標題], [期刊/會議名稱], [發表年份]
- [論文標題], [期刊/會議名稱], [發表年份]

### 項目經歷
- **項目名稱**: [項目描述] ([起始年份-結束年份])

---

### 📝 Markdown 語法說明：

**🏷️ 研究領域標籤**：
\`{{research: 領域1, 領域2, 領域3}}\`
- 自動循環顯示不同顏色（藍色、資訊藍、綠色、橙色、紅色）
- 支持自定義顏色：\`{{research: 機器學習#3b82f6, 深度學習#8b5cf6, 計算機視覺#10b981}}\`
- 自定義顏色格式：領域名#六位HEX顏色碼（如 #ff0000 代表紅色）
- 支持容器背景色：\`{{research: 機器學習, 深度學習[bg:#f0f9ff]}}\`
- 背景色格式：在標籤組最後添加 [bg:#六位HEX顏色碼]

**🔗 個人主頁連結**：
- \`{{github: https://github.com/username}}\` - GitHub 頁面（灰色）
- \`{{scholar: https://scholar.google.com/citations?user=ID}}\` - Google Scholar（藍色）
- \`{{linkedin: https://linkedin.com/in/profile}}\` - LinkedIn（藍色）
- \`{{researchgate: https://researchgate.net/profile/name}}\` - ResearchGate（綠色）
- \`{{website: https://your-site.com}}\` - 個人網站（主色調）
- \`{{任意標籤名: https://連結地址}}\` - 通用連結（如 \`{{個人博客: https://blog.example.com}}\`）

**📚 論文列表**：
\`{{papers: 1,2,3}}\`
- 填入實驗室論文的ID編號（以逗號分隔）

## 榮譽獎項

- [獎項名稱], [頒發機構], [獲獎年份]

## 聯繫方式

- **郵箱**: [您的郵箱]`,

  en: `## Profile

[Introduce your research background and academic experience here]

## Research Areas

{{research: Machine Learning, Deep Learning, Computer Vision, Natural Language Processing}}

## Homepage

{{github: https://github.com/your-username}}
{{scholar: https://scholar.google.com/citations?user=YOUR_ID}}
{{linkedin: https://linkedin.com/in/your-profile}}
{{researchgate: https://researchgate.net/profile/your-profile}}
{{website: https://your-personal-website.com}}

## Education

- **Year-Year**: Degree, Institution Name
- **Year-Year**: Degree, Institution Name

## Representative Achievements

### Lab Publications
{{papers: 1,2,3}}

### Other Publications
- [Paper Title], [Journal/Conference Name], [Publication Year]
- [Paper Title], [Journal/Conference Name], [Publication Year]

### Project Experience
- **Project Name**: [Project Description] ([Start Year-End Year])

---

### 📝 Markdown Syntax Guide:

**🏷️ Research Area Tags**:
\`{{research: Area1, Area2, Area3}}\`
- Automatically cycles through different colors (blue, info blue, green, orange, red)
- Supports custom colors: \`{{research: Machine Learning#3b82f6, Deep Learning#8b5cf6, Computer Vision#10b981}}\`
- Custom color format: AreaName#6-digit HEX color code (e.g., #ff0000 for red)
- Supports container background: \`{{research: Machine Learning, Deep Learning[bg:#f0f9ff]}}\`
- Background format: Add [bg:#6-digit HEX color code] at the end of tag list

**🔗 Homepage Links**:
- \`{{github: https://github.com/username}}\` - GitHub page (default gray)
- \`{{scholar: https://scholar.google.com/citations?user=ID}}\` - Google Scholar (info blue)
- \`{{linkedin: https://linkedin.com/in/profile}}\` - LinkedIn (primary blue)
- \`{{researchgate: https://researchgate.net/profile/name}}\` - ResearchGate (success green)
- \`{{website: https://your-site.com}}\` - Personal website (primary theme)
- \`{{any-label: https://your-link.com}}\` - Generic link (e.g., \`{{personal-blog: https://blog.example.com}}\`)

**📚 Paper Lists**:
\`{{papers: 1,2,3}}\`
- Enter lab paper ID numbers (comma-separated)

## Honors & Awards

- [Award Name], [Awarding Institution], [Year]

## Contact

- **Email**: [Your Email]`
};