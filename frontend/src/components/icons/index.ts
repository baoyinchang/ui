// 图标组件导出
export { default as Dashboard } from './Dashboard.vue'
export { default as Alert } from './Alert.vue'
export { default as User } from './User.vue'
export { default as Setting } from './Setting.vue'
export { default as Document } from './Document.vue'
export { default as Search } from './Search.vue'
export { default as Shield } from './Shield.vue'
export { default as Desktop } from './Desktop.vue'
export { default as Crosshairs } from './Crosshairs.vue'
export { default as Refresh } from './Refresh.vue'
export { default as ArrowDown } from './ArrowDown.vue'
export { default as SwitchButton } from './SwitchButton.vue'
export { default as FullScreen } from './FullScreen.vue'
export { default as Fold } from './Fold.vue'
export { default as Expand } from './Expand.vue'

// 图标映射
export const iconMap = {
  Dashboard: () => import('./Dashboard.vue'),
  Alert: () => import('./Alert.vue'),
  User: () => import('./User.vue'),
  Setting: () => import('./Setting.vue'),
  Document: () => import('./Document.vue'),
  Search: () => import('./Search.vue'),
  Shield: () => import('./Shield.vue'),
  Desktop: () => import('./Desktop.vue'),
  Crosshairs: () => import('./Crosshairs.vue'),
  Refresh: () => import('./Refresh.vue'),
  ArrowDown: () => import('./ArrowDown.vue'),
  SwitchButton: () => import('./SwitchButton.vue'),
  FullScreen: () => import('./FullScreen.vue'),
  Fold: () => import('./Fold.vue'),
  Expand: () => import('./Expand.vue'),
}
