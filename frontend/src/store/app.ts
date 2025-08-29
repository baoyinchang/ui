import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  // 侧边栏状态
  const sidebarCollapsed = ref(false)
  
  // 主题设置
  const theme = ref<'light' | 'dark'>('light')
  
  // 语言设置
  const locale = ref('zh-CN')
  
  // 页面加载状态
  const pageLoading = ref(false)
  
  // 面包屑导航
  const breadcrumbs = ref<Array<{ title: string; path?: string }>>([])
  
  // 当前页面标题
  const pageTitle = ref('')
  
  // 切换侧边栏
  const toggleSidebar = () => {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }
  
  // 设置侧边栏状态
  const setSidebarCollapsed = (collapsed: boolean) => {
    sidebarCollapsed.value = collapsed
  }
  
  // 切换主题
  const toggleTheme = () => {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
  }
  
  // 设置主题
  const setTheme = (newTheme: 'light' | 'dark') => {
    theme.value = newTheme
  }
  
  // 设置语言
  const setLocale = (newLocale: string) => {
    locale.value = newLocale
  }
  
  // 设置页面加载状态
  const setPageLoading = (loading: boolean) => {
    pageLoading.value = loading
  }
  
  // 设置面包屑
  const setBreadcrumbs = (crumbs: Array<{ title: string; path?: string }>) => {
    breadcrumbs.value = crumbs
  }
  
  // 设置页面标题
  const setPageTitle = (title: string) => {
    pageTitle.value = title
    document.title = title ? `${title} - H-System EDR平台` : 'H-System EDR平台'
  }
  
  return {
    // 状态
    sidebarCollapsed,
    theme,
    locale,
    pageLoading,
    breadcrumbs,
    pageTitle,
    
    // 方法
    toggleSidebar,
    setSidebarCollapsed,
    toggleTheme,
    setTheme,
    setLocale,
    setPageLoading,
    setBreadcrumbs,
    setPageTitle
  }
}, {
  persist: {
    key: 'hsystem-app',
    storage: localStorage,
    paths: ['sidebarCollapsed', 'theme', 'locale']
  }
})
