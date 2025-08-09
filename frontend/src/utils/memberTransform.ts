import type { Member } from '@/types'

// 職稱映射
const JOB_TITLES = {
  0: { zh: '教授', en: 'Professor' },
  1: { zh: '副教授', en: 'Associate Professor' },
  2: { zh: '講師', en: 'Lecturer' },
  3: { zh: '助理研究員', en: 'Assistant Researcher' },
  4: { zh: '博士後', en: 'Postdoc' }
}

const STUDENT_TYPES = {
  0: { zh: '博士生', en: 'Doctoral Student' },
  1: { zh: '碩士生', en: 'Master Student' },
  2: { zh: '大學生', en: 'Undergraduate' }
}

const MEMBER_TYPES = {
  0: 'teacher' as const,
  1: 'student' as const,
  2: 'alumni' as const
}

const GRADE_MAP = {
  1: 'year1',
  2: 'year2',
  3: 'year3',
  4: 'year4',
  5: 'year5'
}

/**
 * 轉換後端Member數據為前端可用格式
 * @param member 後端Member數據
 * @param locale 當前語言 'zh-CN' | 'en-US'
 * @returns 包含計算屬性的Member對象
 */
export function transformMember(member: Omit<Member, 'id' | 'name' | 'job_title' | 'bio' | 'member_type' | 'avatar_url' | 'grade'>, locale: string = 'zh-CN'): Member {
  const isZh = locale === 'zh-CN'
  
  // 計算 id 屬性
  const id = member.mem_id
  
  // 計算name屬性
  const name = isZh 
    ? (member.mem_name_zh || member.mem_name_en || `成員${member.mem_id}`)
    : (member.mem_name_en || member.mem_name_zh || `Member ${member.mem_id}`)
  
  // 計算job_title屬性
  let job_title: string | undefined
  if (member.mem_type === 0 && member.job_type !== undefined) {
    // 教師
    const jobInfo = JOB_TITLES[member.job_type as keyof typeof JOB_TITLES]
    job_title = jobInfo ? (isZh ? jobInfo.zh : jobInfo.en) : undefined
  } else if (member.mem_type === 1 && member.student_type !== undefined) {
    // 學生
    const studentInfo = STUDENT_TYPES[member.student_type as keyof typeof STUDENT_TYPES]
    job_title = studentInfo ? (isZh ? studentInfo.zh : studentInfo.en) : undefined
  }
  
  // 計算bio屬性
  const bio = isZh 
    ? member.mem_desc_zh 
    : member.mem_desc_en
  
  // 計算member_type屬性
  const member_type = MEMBER_TYPES[member.mem_type as keyof typeof MEMBER_TYPES]
  
  // 計算avatar_url屬性
  const avatar_url = member.mem_avatar_path ? `/api/media${member.mem_avatar_path}` : undefined
  
  // 計算grade屬性
  const grade = member.student_grade ? GRADE_MAP[member.student_grade as keyof typeof GRADE_MAP] : undefined
  
  return {
    ...member,
    id,
    name,
    job_title,
    bio,
    member_type,
    avatar_url,
    grade
  }
}

/**
 * 批量轉換成員列表
 */
export function transformMembers(members: Omit<Member, 'id' | 'name' | 'job_title' | 'bio' | 'member_type' | 'avatar_url' | 'grade'>[], locale: string = 'zh-CN'): Member[] {
  return members.map(member => transformMember(member, locale))
}