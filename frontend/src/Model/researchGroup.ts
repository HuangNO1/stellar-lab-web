export interface Leader {
  mem_id: number;
  mem_name_zh: string;
  mem_name_en: string;
}

export interface ResearchGroup {
  research_group_id: number;
  lab_id: number;
  research_group_name_zh: string;
  research_group_name_en: string;
  research_group_desc_zh: string;
  research_group_desc_en: string;
  mem_id: number;
  enable: number;
  leader: Leader;
}

export const researchGroups: ResearchGroup[] = [
  {
    research_group_id: 1,
    lab_id: 1,
    research_group_name_zh: "人工智慧研究組",
    research_group_name_en: "Artificial Intelligence Research Group",
    research_group_desc_zh: "專注於機器學習和深度學習技術研究",
    research_group_desc_en: "Focus on machine learning and deep learning research",
    mem_id: 1,
    enable: 1,
    leader: {
      mem_id: 1,
      mem_name_zh: "李教授",
      mem_name_en: "Prof. Li"
    }
  },
  {
    research_group_id: 2,
    lab_id: 1,
    research_group_name_zh: "計算機視覺研究組",
    research_group_name_en: "Computer Vision Research Group",
    research_group_desc_zh: "專注於圖像處理、目標檢測和視覺識別技術研究",
    research_group_desc_en: "Focus on image processing, object detection, and visual recognition technologies",
    mem_id: 2,
    enable: 1,
    leader: {
      mem_id: 2,
      mem_name_zh: "王教授",
      mem_name_en: "Prof. Wang"
    }
  },
  {
    research_group_id: 3,
    lab_id: 1,
    research_group_name_zh: "自然語言處理研究組",
    research_group_name_en: "Natural Language Processing Research Group",
    research_group_desc_zh: "專注於語言模型、文本分析和對話系統研究",
    research_group_desc_en: "Focus on language models, text analysis, and conversational systems",
    mem_id: 3,
    enable: 1,
    leader: {
      mem_id: 3,
      mem_name_zh: "張教授",
      mem_name_en: "Prof. Zhang"
    }
  },
  {
    research_group_id: 4,
    lab_id: 1,
    research_group_name_zh: "機器人學研究組",
    research_group_name_en: "Robotics Research Group",
    research_group_desc_zh: "專注於智能機器人、運動控制和人機交互研究",
    research_group_desc_en: "Focus on intelligent robotics, motion control, and human-robot interaction",
    mem_id: 4,
    enable: 1,
    leader: {
      mem_id: 4,
      mem_name_zh: "劉教授",
      mem_name_en: "Prof. Liu"
    }
  }
];