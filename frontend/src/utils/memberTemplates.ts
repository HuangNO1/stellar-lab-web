/**
 * 成員描述模板
 * 將模板從國際化文件中移出以避免 Vue i18n 編譯錯誤
 */

export const memberDescriptionTemplates = {
    zh: `## 个人简介

[在此处介绍您的研究背景和学术经历]

## 研究领域

{{research: 机器学习, 深度学习, 计算机视觉, 自然语言处理#10b981}}

## 个人主页

{{github: https://github.com/your-username}}
{{scholar: https://scholar.google.com/citations?user=YOUR_ID}}
{{linkedin: https://linkedin.com/in/your-profile}}
{{researchgate: https://researchgate.net/profile/your-profile}}
{{website: https://your-personal-website.com}}

## 教育背景

- **年份-年份**: 学位, 学校/机构名称
- **年份-年份**: 学位, 学校/机构名称

## 代表性成果

### 实验室论文
{{papers: 1,2,3}}

### 其他论文发表
- [论文标题], [期刊/会议名称], [发表年份]
- [论文标题], [期刊/会议名称], [发表年份]

### 项目经历
- **项目名称**: [项目描述] ([起始年份-结束年份])`,
  zh_TW: `## 個人簡介

[在此處介紹您的研究背景和學術經歷]

## 研究領域

{{research: 機器學習, 深度學習, 計算機視覺, 自然語言處理#10b981}}

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
- **項目名稱**: [項目描述] ([起始年份-結束年份])`,

  en: `## Profile

[Introduce your research background and academic experience here]

## Research Areas

{{research: Machine Learning, Deep Learning, Computer Vision#3b82f6, Natural Language Processing}}

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
- **Project Name**: [Project Description] ([Start Year-End Year])`
};