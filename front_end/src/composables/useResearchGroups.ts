import { ref, onMounted } from 'vue';
import { researchGroupApi } from '@/services/api';
import type { ResearchGroup, ResearchGroupQueryParams } from '@/types/api';

/**
 * 課題組數據 Hook
 */
export function useResearchGroups() {
  const researchGroups = ref<ResearchGroup[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const total = ref(0);
  const currentPage = ref(1);

  const fetchResearchGroups = async (params?: ResearchGroupQueryParams) => {
    try {
      loading.value = true;
      error.value = null;
      const response = await researchGroupApi.getResearchGroups(params);
      if (response.code === 0) {
        researchGroups.value = response.data.items;
        total.value = response.data.total;
        currentPage.value = response.data.page;
      } else {
        error.value = response.message;
      }
    } catch (err) {
      console.error('Failed to fetch research groups:', err);
      error.value = '獲取課題組數據失敗';
      // 如果 API 請求失敗，使用本地數據作為後備
      try {
        const { researchGroups: fallbackData } = await import('@/Model/researchGroup');
        // 類型轉換，將本地數據轉換為 API 類型
        researchGroups.value = fallbackData.map(group => ({
          ...group,
          research_group_desc_zh: group.research_group_desc_zh || '',
          research_group_desc_en: group.research_group_desc_en || '',
          mem_id: group.mem_id || undefined,
          leader: group.leader
        })) as ResearchGroup[];
        total.value = fallbackData.length;
      } catch (importErr) {
        console.error('Failed to import fallback data:', importErr);
      }
    } finally {
      loading.value = false;
    }
  };

  const getResearchGroup = async (groupId: number) => {
    try {
      const response = await researchGroupApi.getResearchGroup(groupId);
      if (response.code === 0) {
        return response.data;
      } else {
        throw new Error(response.message);
      }
    } catch (err) {
      console.error('Failed to fetch research group:', err);
      throw err;
    }
  };

  const createResearchGroup = async (data: Partial<ResearchGroup>) => {
    try {
      const response = await researchGroupApi.createResearchGroup(data);
      if (response.code === 0) {
        // 重新獲取列表
        await fetchResearchGroups();
        return response.data;
      } else {
        throw new Error(response.message);
      }
    } catch (err) {
      console.error('Failed to create research group:', err);
      throw err;
    }
  };

  const updateResearchGroup = async (groupId: number, data: Partial<ResearchGroup>) => {
    try {
      const response = await researchGroupApi.updateResearchGroup(groupId, data);
      if (response.code === 0) {
        // 重新獲取列表
        await fetchResearchGroups();
        return response.data;
      } else {
        throw new Error(response.message);
      }
    } catch (err) {
      console.error('Failed to update research group:', err);
      throw err;
    }
  };

  const deleteResearchGroup = async (groupId: number) => {
    try {
      const response = await researchGroupApi.deleteResearchGroup(groupId);
      if (response.code === 0) {
        // 重新獲取列表
        await fetchResearchGroups();
      } else {
        throw new Error(response.message);
      }
    } catch (err) {
      console.error('Failed to delete research group:', err);
      throw err;
    }
  };

  return {
    researchGroups,
    loading,
    error,
    total,
    currentPage,
    fetchResearchGroups,
    getResearchGroup,
    createResearchGroup,
    updateResearchGroup,
    deleteResearchGroup
  };
}

/**
 * 自動獲取課題組數據的 Hook
 */
export function useResearchGroupsWithAutoFetch(params?: ResearchGroupQueryParams) {
  const researchGroupData = useResearchGroups();
  
  onMounted(() => {
    researchGroupData.fetchResearchGroups(params);
  });
  
  return researchGroupData;
}