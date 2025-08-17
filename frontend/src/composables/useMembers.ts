import { ref, onMounted, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { memberApi } from '@/services/api';
import type { Member, MemberQueryParams } from '@/types/api';
import { getMemberAvatarUrl } from '@/utils/media';

/**
 * 成員數據 Hook
 */
export function useMembers() {
  const { t, locale } = useI18n();
  const members = ref<Member[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const total = ref(0);
  const currentPage = ref(1);

  const fetchMembers = async (params?: MemberQueryParams) => {
    try {
      loading.value = true;
      error.value = null;
      const response = await memberApi.getMembers(params);
      if (response.code === 0) {
        members.value = response.data.items;
        total.value = response.data.total;
        currentPage.value = response.data.page || 1;
      } else {
        error.value = response.message;
      }
    } catch (err) {
      console.error('Failed to fetch members:', err);
      error.value = t('common.fetchError');
      // 設置為空數組而不是使用本地數據
      members.value = [];
      total.value = 0;
    } finally {
      loading.value = false;
    }
  };

  const getMember = async (memberId: number) => {
    try {
      const response = await memberApi.getMember(memberId);
      if (response.code === 0) {
        return response.data;
      } else {
        throw new Error(response.message);
      }
    } catch (err) {
      console.error('Failed to fetch member:', err);
      throw err;
    }
  };

  // 按成員類型分組
  const groupedMembers = computed(() => {
    const groups = {
      teachers: [] as Member[], // 教師
      phd: [] as Member[],      // 博士生
      master: [] as Member[],   // 碩士生
      undergraduate: [] as Member[], // 本科生
      alumni: [] as Member[],   // 校友（已畢業的學生）
      others: [] as Member[]    // 其他
    };

    members.value.forEach(member => {
      if (member.mem_type === 0) {
        // 教師
        groups.teachers.push(member);
      } else if (member.mem_type === 1) {
        // 學生 - 根據 student_type 和 destination 判斷
        if (member.destination_zh || member.destination_en) {
          // 有去向信息的是校友
          groups.alumni.push(member);
        } else {
          // 根據學生類型分組
          switch (member.student_type) {
            case 0:
              groups.phd.push(member);
              break;
            case 1:
              groups.master.push(member);
              break;
            case 2:
              groups.undergraduate.push(member);
              break;
            default:
              groups.others.push(member);
          }
        }
      } else if (member.mem_type === 2) {
        // 校友
        groups.alumni.push(member);
      } else {
        // 其他類型
        groups.others.push(member);
      }
    });

    // 為每個分組排序
    const sortMembers = (memberList: Member[]) => {
      return memberList.sort((a, b) => {
        // 教師按職務類型排序：教授(0) > 副教授(1) > 講師(2) > 助理研究員(3) > 博士後(4)
        if (a.mem_type === 0 && b.mem_type === 0) {
          const jobOrder = [0, 1, 2, 3, 4]; // 正確的職務排序
          const aOrder = jobOrder.indexOf(a.job_type ?? 4);
          const bOrder = jobOrder.indexOf(b.job_type ?? 4);
          if (aOrder !== bOrder) {
            return aOrder - bOrder;
          }
          // 同職務類型按姓名排序
          const aName = locale.value === 'zh' ? a.mem_name_zh : a.mem_name_en;
          const bName = locale.value === 'zh' ? b.mem_name_zh : b.mem_name_en;
          return (aName || '').localeCompare(bName || '');
        }
        
        // 學生按年級排序（高年級在前），同年級按姓名排序
        if (a.mem_type === 1 && b.mem_type === 1) {
          const aGrade = a.student_grade ?? 0;
          const bGrade = b.student_grade ?? 0;
          if (aGrade !== bGrade) {
            return bGrade - aGrade; // 高年級在前
          }
          // 同年級按姓名排序
          const aName = locale.value === 'zh' ? a.mem_name_zh : a.mem_name_en;
          const bName = locale.value === 'zh' ? b.mem_name_zh : b.mem_name_en;
          return (aName || '').localeCompare(bName || '');
        }
        
        // 校友排序：先按畢業年份（近年優先），再按身份類型，最後按姓名
        if (a.mem_type === 2 && b.mem_type === 2) {
          // 先按畢業年份排序（近年畢業的在前）
          const aYear = a.graduation_year ?? 0;
          const bYear = b.graduation_year ?? 0;
          if (aYear !== bYear) {
            return bYear - aYear; // 近年畢業的在前
          }
          
          // 同年畢業按身份類型排序：博士(0) > 碩士(1) > 本科(2) > 教師(3) > 其他(4)
          const identityOrder = [0, 1, 2, 3, 4];
          const aIdentity = identityOrder.indexOf(a.alumni_identity ?? 4);
          const bIdentity = identityOrder.indexOf(b.alumni_identity ?? 4);
          if (aIdentity !== bIdentity) {
            return aIdentity - bIdentity;
          }
          
          // 同身份按姓名排序
          const aName = locale.value === 'zh' ? a.mem_name_zh : a.mem_name_en;
          const bName = locale.value === 'zh' ? b.mem_name_zh : b.mem_name_en;
          return (aName || '').localeCompare(bName || '');
        }
        
        // 其他按姓名排序
        const aName = locale.value === 'zh' ? a.mem_name_zh : a.mem_name_en;
        const bName = locale.value === 'zh' ? b.mem_name_zh : b.mem_name_en;
        return (aName || '').localeCompare(bName || '');
      });
    };

    return {
      teachers: sortMembers(groups.teachers),
      phd: sortMembers(groups.phd),
      master: sortMembers(groups.master),
      undergraduate: sortMembers(groups.undergraduate),
      alumni: sortMembers(groups.alumni),
      others: sortMembers(groups.others)
    };
  });

  // 獲取成員頭像URL
  const getMemberAvatar = (member: Member) => {
    return getMemberAvatarUrl(member.mem_avatar_path);
  };

  // 獲取成員職位描述
  const getMemberPosition = (member: Member) => {
    if (member.mem_type === 0) {
      // 教師
      const jobTypeKeys = ['professor', 'associateProfessor', 'lecturer', 'assistantProfessor', 'postdoc'];
      const jobTypeKey = jobTypeKeys[member.job_type || 4];
      return t(`members.positions.${jobTypeKey}`);
    } else if (member.mem_type === 1) {
      // 學生
      if (member.destination_zh || member.destination_en) {
        // 有去向信息的學生視為校友 - 顯示去向
        const destination = locale.value === 'zh' ? member.destination_zh : member.destination_en;
        return destination || t('members.positions.alumni');
      } else {
        // 在校學生
        const studentTypeKeys = ['phdStudent', 'masterStudent', 'undergraduate'];
        const studentTypeKey = studentTypeKeys[member.student_type || 0];
        const type = t(`members.positions.${studentTypeKey}`);
        if (member.student_grade) {
          const grade = locale.value === 'zh' ? 
            `${member.student_grade}${t('members.positions.year')}` :
            `${t('members.positions.year')} ${member.student_grade}`;
          return `${type} ${grade}`;
        }
        return type;
      }
    } else if (member.mem_type === 2) {
      // 校友 - 顯示身份、畢業年份和去向
      let position = '';
      
      // 身份類型
      if (member.alumni_identity !== undefined) {
        const identityKeys = ['phdGraduate', 'masterGraduate', 'undergraduateGraduate', 'faculty', 'other'];
        const identityKey = identityKeys[member.alumni_identity] || 'other';
        position = t(`members.positions.${identityKey}`);
      }
      
      // 畢業年份
      if (member.graduation_year) {
        const year = locale.value === 'zh' ? 
          `${member.graduation_year}${t('members.positions.graduateYear')}` :
          `${member.graduation_year} ${t('members.positions.graduate')}`;
        position = position ? `${position} (${year})` : year;
      }
      
      // 去向信息
      if (member.destination_zh || member.destination_en) {
        const destination = locale.value === 'zh' ? member.destination_zh : member.destination_en;
        if (destination) {
          position = position ? `${position} - ${destination}` : destination;
        }
      }
      
      return position || t('members.positions.alumni');
    } else {
      // 其他
      return t('members.positions.other');
    }
  };

  return {
    members,
    loading,
    error,
    total,
    currentPage,
    groupedMembers,
    fetchMembers,
    getMember,
    getMemberAvatar,
    getMemberPosition
  };
}

/**
 * 自動獲取成員數據的 Hook（默認獲取所有數據）
 */
export function useMembersWithAutoFetch(params?: MemberQueryParams) {
  const memberData = useMembers();
  
  onMounted(() => {
    // 默認使用 all=true 獲取所有數據，並按名稱排序
    const queryParams = params || { all: 'true', sort_by: 'name', order: 'asc' };
    memberData.fetchMembers(queryParams);
  });
  
  return memberData;
}