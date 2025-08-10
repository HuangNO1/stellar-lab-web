import { ref, onMounted } from 'vue';
import { labApi } from '@/services/api';
import type { Lab } from '@/types/api';

/**
 * 實驗室數據 Hook
 */
export function useLab() {
  const lab = ref<Lab | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const fetchLab = async () => {
    try {
      loading.value = true;
      error.value = null;
      const response = await labApi.getLab();
      if (response.code === 0) {
        lab.value = response.data;
      } else {
        error.value = response.message;
      }
    } catch (err) {
      console.error('Failed to fetch lab data:', err);
      error.value = '獲取實驗室數據失敗';
    } finally {
      loading.value = false;
    }
  };

  return {
    lab,
    loading,
    error,
    fetchLab
  };
}

/**
 * 自動獲取實驗室數據的 Hook
 */
export function useLabWithAutoFetch() {
  const labData = useLab();
  
  onMounted(() => {
    labData.fetchLab();
  });
  
  return labData;
}