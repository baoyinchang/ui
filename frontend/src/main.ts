import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import pinia from './store'

// Element Plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'

// 样式
import './styles/index.scss'

// NProgress样式
import 'nprogress/nprogress.css'

const app = createApp(App)

// 注册Element Plus图标（只注册常用的）
import {
  ArrowDown,
  ArrowLeft,
  ArrowRight,
  ArrowUp,
  Bell,
  Check,
  CircleCheck,
  CircleClose,
  Clock,
  Collection,
  Connection,
  DataAnalysis,
  DataBoard,
  Delete,
  Document,
  DocumentAdd,
  DocumentDelete,
  Download,
  Edit,
  FolderOpened,
  FullScreen,
  HomeFilled,
  InfoFilled,
  Key,
  Lock,
  Message,
  Monitor,
  More,
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
  View,
  Warning
} from '@element-plus/icons-vue'

// 注册图标组件
const icons = {
  ArrowDown,
  ArrowLeft,
  ArrowRight,
  ArrowUp,
  Bell,
  Check,
  CircleCheck,
  CircleClose,
  Clock,
  Collection,
  Connection,
  DataAnalysis,
  DataBoard,
  Delete,
  Document,
  DocumentAdd,
  DocumentDelete,
  Download,
  Edit,
  FolderOpened,
  FullScreen,
  HomeFilled,
  InfoFilled,
  Key,
  Lock,
  Message,
  Monitor,
  More,
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
  View,
  Warning
}

// 注册所有图标
Object.entries(icons).forEach(([key, component]) => {
  app.component(key, component)
})

app.use(pinia)
app.use(router)
app.use(ElementPlus)

app.mount('#app')