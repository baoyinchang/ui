// 全局图标注册插件
import type { App } from 'vue'
import { elementPlusIcons } from '@/components/icons/ElementPlusIcons'

// 图标注册插件
export function setupIcons(app: App) {
  // 注册所有 Element Plus 图标为全局组件
  Object.entries(elementPlusIcons).forEach(([name, component]) => {
    app.component(name, component)
  })
  
  console.log(`✅ 已注册 ${Object.keys(elementPlusIcons).length} 个图标组件`)
}

// 默认导出
export default setupIcons
