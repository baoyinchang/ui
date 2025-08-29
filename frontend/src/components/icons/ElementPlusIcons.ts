// Element Plus 图标导入和映射
// 解决图标缺失问题

// 从 @element-plus/icons-vue 导入所有需要的图标
import {
  // 基础图标
  ArrowDown,
  ArrowLeft,
  Bell,
  Check,
  CircleCheck,
  CircleClose,
  CircleFilled,
  Clock,
  Collection,
  Connection,
  DataAnalysis,
  DataBoard,
  DocumentAdd,
  DocumentDelete,
  Download,
  FolderOpened,
  FullScreen,
  HomeFilled,
  InfoFilled,
  Key,
  Lock,
  Message,
  Monitor,
  Plus,
  Promotion,
  Rank,
  Refresh,
  RefreshLeft,
  Search,
  Setting,
  SwitchButton,
  TrendCharts,
  Upload,
  User,
  Warning,
  
  // 自定义需要的图标
  Shield,
  Document,
  Desktop,
  
} from '@element-plus/icons-vue'

// 图标映射对象
export const elementPlusIcons = {
  // 基础操作图标
  ArrowDown,
  ArrowLeft,
  Bell,
  Check,
  CircleCheck,
  CircleClose,
  CircleFilled,
  Clock,
  Collection,
  Connection,
  DataAnalysis,
  DataBoard,
  DocumentAdd,
  DocumentDelete,
  Download,
  FolderOpened,
  FullScreen,
  HomeFilled,
  InfoFilled,
  Key,
  Lock,
  Message,
  Monitor,
  Plus,
  Promotion,
  Rank,
  Refresh,
  RefreshLeft,
  Search,
  Setting,
  SwitchButton,
  TrendCharts,
  Upload,
  User,
  Warning,
  
  // 业务相关图标
  Shield,
  Document,
  Desktop,
  
  // 别名映射（解决命名不一致问题）
  Alert: Bell,
  Asset: Desktop,
  Dashboard: DataBoard,
  Crosshairs: Search,
}

// 图标名称数组
export const iconNames = Object.keys(elementPlusIcons)

// 获取图标组件的辅助函数
export function getIcon(name: string) {
  return elementPlusIcons[name as keyof typeof elementPlusIcons] || null
}

// 检查图标是否存在
export function hasIcon(name: string): boolean {
  return name in elementPlusIcons
}

// 获取所有可用图标名称
export function getAllIconNames(): string[] {
  return iconNames
}

// 默认导出
export default elementPlusIcons
