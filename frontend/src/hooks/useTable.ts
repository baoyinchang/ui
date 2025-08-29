/**
 * 表格相关的Hook
 */

import { ref, reactive, computed } from 'vue'
import type { Ref } from 'vue'

export interface TableConfig {
  pageSize?: number
  showPagination?: boolean
  showSelection?: boolean
}

export interface PaginationData {
  current: number
  pageSize: number
  total: number
}

export function useTable<T = any>(config: TableConfig = {}) {
  const {
    pageSize = 20,
    showPagination = true,
    showSelection = false
  } = config
  
  // 表格数据
  const tableData: Ref<T[]> = ref([])
  const loading = ref(false)
  const selectedRows: Ref<T[]> = ref([])
  
  // 分页数据
  const pagination = reactive<PaginationData>({
    current: 1,
    pageSize,
    total: 0
  })
  
  // 搜索条件
  const searchForm = ref({})
  
  // 计算属性
  const hasSelection = computed(() => selectedRows.value.length > 0)
  const selectedCount = computed(() => selectedRows.value.length)
  
  /**
   * 设置表格数据
   */
  const setTableData = (data: T[], total?: number) => {
    tableData.value = data
    if (total !== undefined) {
      pagination.total = total
    }
  }
  
  /**
   * 清空表格数据
   */
  const clearTableData = () => {
    tableData.value = []
    pagination.total = 0
  }
  
  /**
   * 处理选择变化
   */
  const handleSelectionChange = (selection: T[]) => {
    selectedRows.value = selection
  }
  
  /**
   * 清空选择
   */
  const clearSelection = () => {
    selectedRows.value = []
  }
  
  /**
   * 处理页码变化
   */
  const handleCurrentChange = (page: number) => {
    pagination.current = page
  }
  
  /**
   * 处理页大小变化
   */
  const handleSizeChange = (size: number) => {
    pagination.pageSize = size
    pagination.current = 1
  }
  
  /**
   * 重置分页
   */
  const resetPagination = () => {
    pagination.current = 1
    pagination.total = 0
  }
  
  /**
   * 刷新表格
   */
  const refresh = () => {
    // 触发数据重新加载的逻辑
    // 具体实现由使用方提供
  }
  
  /**
   * 重置搜索条件
   */
  const resetSearch = () => {
    searchForm.value = {}
    resetPagination()
  }
  
  return {
    // 数据
    tableData,
    loading,
    selectedRows,
    pagination,
    searchForm,
    
    // 计算属性
    hasSelection,
    selectedCount,
    
    // 方法
    setTableData,
    clearTableData,
    handleSelectionChange,
    clearSelection,
    handleCurrentChange,
    handleSizeChange,
    resetPagination,
    refresh,
    resetSearch
  }
}
