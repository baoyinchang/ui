<template>
  <div
    ref="chartRef"
    class="base-chart"
    :style="{ width: width, height: height }"
    v-loading="loading"
  />
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick, computed } from 'vue'
import * as echarts from 'echarts/core'
import {
  BarChart,
  LineChart,
  PieChart,
  ScatterChart,
  RadarChart,
  MapChart,
  TreeChart,
  TreemapChart,
  GraphChart,
  GaugeChart,
  FunnelChart,
  ParallelChart,
  SankeyChart,
  BoxplotChart,
  CandlestickChart,
  HeatmapChart,
  SunburstChart,
  ThemeRiverChart
} from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  PolarComponent,
  AriaComponent,
  ParallelComponent,
  LegendComponent,
  RadarComponent,
  ToolboxComponent,
  DataZoomComponent,
  VisualMapComponent,
  TimelineComponent,
  CalendarComponent,
  GraphicComponent,
  MarkPointComponent,
  MarkLineComponent,
  MarkAreaComponent,
  BrushComponent,
  DatasetComponent,
  TransformComponent
} from 'echarts/components'
import { LabelLayout, UniversalTransition } from 'echarts/features'
import { CanvasRenderer } from 'echarts/renderers'
import { useAppStore } from '@/store/app'
import { debounce } from '@/utils'

// 注册必要的组件
echarts.use([
  // 图表类型
  BarChart,
  LineChart,
  PieChart,
  ScatterChart,
  RadarChart,
  MapChart,
  TreeChart,
  TreemapChart,
  GraphChart,
  GaugeChart,
  FunnelChart,
  ParallelChart,
  SankeyChart,
  BoxplotChart,
  CandlestickChart,
  HeatmapChart,
  SunburstChart,
  ThemeRiverChart,
  
  // 组件
  TitleComponent,
  TooltipComponent,
  GridComponent,
  PolarComponent,
  AriaComponent,
  ParallelComponent,
  LegendComponent,
  RadarComponent,
  ToolboxComponent,
  DataZoomComponent,
  VisualMapComponent,
  TimelineComponent,
  CalendarComponent,
  GraphicComponent,
  MarkPointComponent,
  MarkLineComponent,
  MarkAreaComponent,
  BrushComponent,
  DatasetComponent,
  TransformComponent,
  
  // 功能
  LabelLayout,
  UniversalTransition,
  
  // 渲染器
  CanvasRenderer
])

// 组件属性
interface Props {
  option: echarts.EChartsOption
  width?: string
  height?: string
  loading?: boolean
  theme?: string
  initOptions?: echarts.EChartsInitOpts
  group?: string
  autoResize?: boolean
  notMerge?: boolean
  replaceMerge?: string | string[]
  lazyUpdate?: boolean
  silent?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  width: '100%',
  height: '400px',
  loading: false,
  theme: '',
  autoResize: true,
  notMerge: false,
  lazyUpdate: false,
  silent: false
})

// 事件定义
const emit = defineEmits([
  'chart-ready',
  'chart-click',
  'chart-dblclick',
  'chart-mousedown',
  'chart-mousemove',
  'chart-mouseup',
  'chart-mouseover',
  'chart-mouseout',
  'chart-globalout',
  'chart-contextmenu',
  'chart-highlight',
  'chart-downplay',
  'chart-selectchanged',
  'chart-legendselectchanged',
  'chart-legendselected',
  'chart-legendunselected',
  'chart-legendselectall',
  'chart-legendinverseselect',
  'chart-legendscroll',
  'chart-datazoom',
  'chart-datarangeselected',
  'chart-timelinechanged',
  'chart-timelineplaychanged',
  'chart-restore',
  'chart-dataviewchanged',
  'chart-magictypechanged',
  'chart-geoselectchanged',
  'chart-geoselected',
  'chart-geounselected',
  'chart-axisareaselected',
  'chart-brush',
  'chart-brushEnd',
  'chart-brushselected',
  'chart-globalcursortaken',
  'chart-rendered',
  'chart-finished'
])

// 响应式数据
const chartRef = ref<HTMLElement>()
const chartInstance = ref<echarts.ECharts>()
const appStore = useAppStore()

// 计算属性
const currentTheme = computed(() => {
  return props.theme || appStore.theme
})

// 初始化图表
const initChart = async () => {
  if (!chartRef.value) return

  await nextTick()

  // 销毁已存在的实例
  if (chartInstance.value) {
    chartInstance.value.dispose()
  }

  // 创建新实例
  chartInstance.value = echarts.init(
    chartRef.value,
    currentTheme.value,
    {
      devicePixelRatio: window.devicePixelRatio,
      renderer: 'canvas',
      useDirtyRect: true,
      ...props.initOptions
    }
  )

  // 设置分组
  if (props.group) {
    chartInstance.value.group = props.group
  }

  // 绑定事件
  bindEvents()

  // 设置配置项
  setOption()

  // 触发就绪事件
  emit('chart-ready', chartInstance.value)
}

// 设置图表配置
const setOption = () => {
  if (!chartInstance.value || !props.option) return

  chartInstance.value.setOption(
    props.option,
    {
      notMerge: props.notMerge,
      replaceMerge: props.replaceMerge,
      lazyUpdate: props.lazyUpdate,
      silent: props.silent
    }
  )
}

// 绑定事件
const bindEvents = () => {
  if (!chartInstance.value) return

  const events = [
    'click', 'dblclick', 'mousedown', 'mousemove', 'mouseup',
    'mouseover', 'mouseout', 'globalout', 'contextmenu',
    'highlight', 'downplay', 'selectchanged', 'legendselectchanged',
    'legendselected', 'legendunselected', 'legendselectall',
    'legendinverseselect', 'legendscroll', 'datazoom',
    'datarangeselected', 'timelinechanged', 'timelineplaychanged',
    'restore', 'dataviewchanged', 'magictypechanged',
    'geoselectchanged', 'geoselected', 'geounselected',
    'axisareaselected', 'brush', 'brushEnd', 'brushselected',
    'globalcursortaken', 'rendered', 'finished'
  ]

  events.forEach(event => {
    chartInstance.value?.on(event, (params: any) => {
      emit(`chart-${event}` as any, params)
    })
  })
}

// 调整图表大小
const resize = debounce(() => {
  chartInstance.value?.resize()
}, 100)

// 监听窗口大小变化
const handleResize = () => {
  if (props.autoResize) {
    resize()
  }
}

// 公开方法
const getChart = () => chartInstance.value

const setChartOption = (option: echarts.EChartsOption, opts?: echarts.SetOptionOpts) => {
  if (!chartInstance.value) return
  chartInstance.value.setOption(option, opts)
}

const getWidth = () => chartInstance.value?.getWidth()

const getHeight = () => chartInstance.value?.getHeight()

const getDom = () => chartInstance.value?.getDom()

const getOption = () => chartInstance.value?.getOption()

const resizeChart = (opts?: echarts.ResizeOpts) => {
  chartInstance.value?.resize(opts)
}

const dispatchAction = (payload: echarts.Payload) => {
  chartInstance.value?.dispatchAction(payload)
}

const on = (eventName: string, handler: echarts.EventCallback<any>) => {
  chartInstance.value?.on(eventName, handler)
}

const off = (eventName: string, handler?: echarts.EventCallback<any>) => {
  chartInstance.value?.off(eventName, handler)
}

const convertToPixel = (finder: echarts.ConvertFinder, value: string | number | Date) => {
  return chartInstance.value?.convertToPixel(finder, value)
}

const convertFromPixel = (finder: echarts.ConvertFinder, value: number[]) => {
  return chartInstance.value?.convertFromPixel(finder, value)
}

const containPixel = (finder: echarts.ConvertFinder, value: number[]) => {
  return chartInstance.value?.containPixel(finder, value)
}

const showLoading = (type?: string, opts?: echarts.LoadingOpts) => {
  chartInstance.value?.showLoading(type, opts)
}

const hideLoading = () => {
  chartInstance.value?.hideLoading()
}

const getDataURL = (opts?: echarts.GetDataURLOpts) => {
  return chartInstance.value?.getDataURL(opts)
}

const getConnectedDataURL = (opts?: echarts.GetConnectedDataURLOpts) => {
  return chartInstance.value?.getConnectedDataURL(opts)
}

const appendData = (opts: echarts.AppendDataOpts) => {
  chartInstance.value?.appendData(opts)
}

const clear = () => {
  chartInstance.value?.clear()
}

const isDisposed = () => {
  return chartInstance.value?.isDisposed()
}

const dispose = () => {
  chartInstance.value?.dispose()
}

// 暴露方法
defineExpose({
  getChart,
  setOption: setChartOption,
  getWidth,
  getHeight,
  getDom,
  getOption,
  resize: resizeChart,
  dispatchAction,
  on,
  off,
  convertToPixel,
  convertFromPixel,
  containPixel,
  showLoading,
  hideLoading,
  getDataURL,
  getConnectedDataURL,
  appendData,
  clear,
  isDisposed,
  dispose
})

// 监听器
watch(() => props.option, () => {
  setOption()
}, { deep: true })

watch(() => props.loading, (loading) => {
  if (!chartInstance.value) return
  
  if (loading) {
    chartInstance.value.showLoading('default', {
      text: '加载中...',
      color: '#409eff',
      textColor: '#000',
      maskColor: 'rgba(255, 255, 255, 0.8)',
      zlevel: 0,
      fontSize: 12,
      showSpinner: true,
      spinnerRadius: 10,
      lineWidth: 5
    })
  } else {
    chartInstance.value.hideLoading()
  }
})

watch(currentTheme, () => {
  // 主题变化时重新初始化图表
  initChart()
})

// 生命周期
onMounted(() => {
  initChart()
  
  if (props.autoResize) {
    window.addEventListener('resize', handleResize)
  }
})

onUnmounted(() => {
  if (props.autoResize) {
    window.removeEventListener('resize', handleResize)
  }
  
  if (chartInstance.value) {
    chartInstance.value.dispose()
  }
})
</script>

<style scoped lang="scss">
.base-chart {
  min-height: 200px;
}
</style>
