<template>
  <div class="data-table">
    <!-- 表格工具栏 -->
    <div v-if="showToolbar" class="table-toolbar">
      <div class="toolbar-left">
        <slot name="toolbar-left">
          <el-button
            v-if="showRefresh"
            type="primary"
            :icon="Refresh"
            @click="handleRefresh"
          >
            刷新
          </el-button>
          <el-button
            v-if="showAdd"
            type="primary"
            :icon="Plus"
            @click="handleAdd"
          >
            新增
          </el-button>
          <el-button
            v-if="showBatchDelete && selectedRows.length > 0"
            type="danger"
            :icon="Delete"
            @click="handleBatchDelete"
          >
            批量删除
          </el-button>
        </slot>
      </div>
      <div class="toolbar-right">
        <slot name="toolbar-right">
          <el-input
            v-if="showSearch"
            v-model="searchKeyword"
            placeholder="搜索..."
            :prefix-icon="Search"
            clearable
            @input="handleSearch"
            style="width: 200px; margin-right: 10px"
          />
          <el-button
            v-if="showExport"
            :icon="Download"
            @click="handleExport"
          >
            导出
          </el-button>
          <el-button
            v-if="showColumnSetting"
            :icon="Setting"
            @click="showColumnDialog = true"
          >
            列设置
          </el-button>
        </slot>
      </div>
    </div>

    <!-- 数据表格 -->
    <el-table
      ref="tableRef"
      v-loading="loading"
      :data="tableData"
      :height="tableHeight"
      :max-height="maxHeight"
      :stripe="stripe"
      :border="border"
      :size="size"
      :fit="fit"
      :show-header="showHeader"
      :highlight-current-row="highlightCurrentRow"
      :row-class-name="rowClassName"
      :row-style="rowStyle"
      :cell-class-name="cellClassName"
      :cell-style="cellStyle"
      :header-row-class-name="headerRowClassName"
      :header-row-style="headerRowStyle"
      :header-cell-class-name="headerCellClassName"
      :header-cell-style="headerCellStyle"
      :row-key="rowKey"
      :empty-text="emptyText"
      :default-expand-all="defaultExpandAll"
      :expand-row-keys="expandRowKeys"
      :default-sort="defaultSort"
      :tooltip-effect="tooltipEffect"
      :show-summary="showSummary"
      :sum-text="sumText"
      :summary-method="summaryMethod"
      :span-method="spanMethod"
      :select-on-indeterminate="selectOnIndeterminate"
      :indent="indent"
      :lazy="lazy"
      :load="load"
      :tree-props="treeProps"
      @select="handleSelect"
      @select-all="handleSelectAll"
      @selection-change="handleSelectionChange"
      @cell-mouse-enter="handleCellMouseEnter"
      @cell-mouse-leave="handleCellMouseLeave"
      @cell-click="handleCellClick"
      @cell-dblclick="handleCellDblclick"
      @row-click="handleRowClick"
      @row-contextmenu="handleRowContextmenu"
      @row-dblclick="handleRowDblclick"
      @header-click="handleHeaderClick"
      @header-contextmenu="handleHeaderContextmenu"
      @sort-change="handleSortChange"
      @filter-change="handleFilterChange"
      @current-change="handleCurrentChange"
      @header-dragend="handleHeaderDragend"
      @expand-change="handleExpandChange"
    >
      <!-- 选择列 -->
      <el-table-column
        v-if="showSelection"
        type="selection"
        width="55"
        :selectable="selectable"
        :reserve-selection="reserveSelection"
      />

      <!-- 序号列 -->
      <el-table-column
        v-if="showIndex"
        type="index"
        label="序号"
        width="60"
        :index="indexMethod"
      />

      <!-- 动态列 -->
      <template v-for="column in visibleColumns" :key="column.prop">
        <el-table-column
          :prop="column.prop"
          :label="column.label"
          :width="column.width"
          :min-width="column.minWidth"
          :fixed="column.fixed"
          :render-header="column.renderHeader"
          :sortable="column.sortable"
          :sort-method="column.sortMethod"
          :sort-by="column.sortBy"
          :sort-orders="column.sortOrders"
          :resizable="column.resizable"
          :formatter="column.formatter"
          :show-overflow-tooltip="column.showOverflowTooltip"
          :align="column.align"
          :header-align="column.headerAlign"
          :class-name="column.className"
          :label-class-name="column.labelClassName"
          :selectable="column.selectable"
          :reserve-selection="column.reserveSelection"
          :filters="column.filters"
          :filter-placement="column.filterPlacement"
          :filter-multiple="column.filterMultiple"
          :filter-method="column.filterMethod"
          :filtered-value="column.filteredValue"
        >
          <template v-if="column.slot" #default="scope">
            <slot :name="column.slot" :row="scope.row" :column="scope.column" :$index="scope.$index" />
          </template>
          <template v-if="column.headerSlot" #header="scope">
            <slot :name="column.headerSlot" :column="scope.column" :$index="scope.$index" />
          </template>
        </el-table-column>
      </template>

      <!-- 操作列 -->
      <el-table-column
        v-if="showActions"
        label="操作"
        :width="actionWidth"
        :min-width="actionMinWidth"
        :fixed="actionFixed"
        :align="actionAlign"
      >
        <template #default="scope">
          <slot name="actions" :row="scope.row" :$index="scope.$index">
            <el-button
              v-if="showEdit"
              type="primary"
              size="small"
              :icon="Edit"
              @click="handleEdit(scope.row, scope.$index)"
            >
              编辑
            </el-button>
            <el-button
              v-if="showDelete"
              type="danger"
              size="small"
              :icon="Delete"
              @click="handleDelete(scope.row, scope.$index)"
            >
              删除
            </el-button>
          </slot>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页组件 -->
    <div v-if="showPagination" class="table-pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="pageSizes"
        :size="paginationSize"
        :disabled="paginationDisabled"
        :hide-on-single-page="hideOnSinglePage"
        :total="total"
        :layout="paginationLayout"
        :prev-text="prevText"
        :next-text="nextText"
        :background="paginationBackground"
        @size-change="handleSizeChange"
        @current-change="handleCurrentPageChange"
        @prev-click="handlePrevClick"
        @next-click="handleNextClick"
      />
    </div>

    <!-- 列设置对话框 -->
    <el-dialog
      v-model="showColumnDialog"
      title="列设置"
      width="400px"
      :close-on-click-modal="false"
    >
      <div class="column-setting">
        <el-checkbox
          v-model="checkAll"
          :indeterminate="isIndeterminate"
          @change="handleCheckAllChange"
        >
          全选
        </el-checkbox>
        <el-divider />
        <el-checkbox-group v-model="checkedColumns" @change="handleCheckedColumnsChange">
          <draggable
            v-model="columnSettings"
            item-key="prop"
            handle=".drag-handle"
            @end="handleColumnDragEnd"
          >
            <template #item="{ element }">
              <div class="column-item">
                <el-icon class="drag-handle"><Rank /></el-icon>
                <el-checkbox :label="element.prop">{{ element.label }}</el-checkbox>
              </div>
            </template>
          </draggable>
        </el-checkbox-group>
      </div>
      <template #footer>
        <el-button @click="showColumnDialog = false">取消</el-button>
        <el-button type="primary" @click="handleColumnSettingConfirm">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Refresh,
  Plus,
  Delete,
  Search,
  Download,
  Setting,
  Edit,
  Rank
} from '@element-plus/icons-vue'
import draggable from 'vuedraggable'
import { debounce } from '@/utils'
import type { TableColumn } from '@/types/global'

// 组件属性定义
interface Props {
  // 数据相关
  data?: any[]
  loading?: boolean
  total?: number
  
  // 表格配置
  columns?: TableColumn[]
  height?: string | number
  maxHeight?: string | number
  stripe?: boolean
  border?: boolean
  size?: 'large' | 'default' | 'small'
  fit?: boolean
  showHeader?: boolean
  highlightCurrentRow?: boolean
  rowClassName?: string | ((row: any, index: number) => string)
  rowStyle?: any
  cellClassName?: string | ((row: any, column: any, rowIndex: number, columnIndex: number) => string)
  cellStyle?: any
  headerRowClassName?: string | ((row: any, index: number) => string)
  headerRowStyle?: any
  headerCellClassName?: string | ((row: any, column: any, rowIndex: number, columnIndex: number) => string)
  headerCellStyle?: any
  rowKey?: string | ((row: any) => string)
  emptyText?: string
  defaultExpandAll?: boolean
  expandRowKeys?: any[]
  defaultSort?: { prop: string; order: string }
  tooltipEffect?: 'dark' | 'light'
  showSummary?: boolean
  sumText?: string
  summaryMethod?: (param: { columns: any[]; data: any[] }) => any[]
  spanMethod?: (param: { row: any; column: any; rowIndex: number; columnIndex: number }) => number[] | { rowspan: number; colspan: number }
  selectOnIndeterminate?: boolean
  indent?: number
  lazy?: boolean
  load?: (row: any, treeNode: any, resolve: (data: any[]) => void) => void
  treeProps?: { hasChildren?: string; children?: string }
  
  // 功能开关
  showToolbar?: boolean
  showRefresh?: boolean
  showAdd?: boolean
  showBatchDelete?: boolean
  showSearch?: boolean
  showExport?: boolean
  showColumnSetting?: boolean
  showSelection?: boolean
  showIndex?: boolean
  showActions?: boolean
  showEdit?: boolean
  showDelete?: boolean
  showPagination?: boolean
  
  // 选择相关
  selectable?: (row: any, index: number) => boolean
  reserveSelection?: boolean
  
  // 序号相关
  indexMethod?: (index: number) => number
  
  // 操作列配置
  actionWidth?: string | number
  actionMinWidth?: string | number
  actionFixed?: boolean | 'left' | 'right'
  actionAlign?: 'left' | 'center' | 'right'
  
  // 分页配置
  currentPage?: number
  pageSize?: number
  pageSizes?: number[]
  paginationSize?: 'large' | 'default' | 'small'
  paginationDisabled?: boolean
  hideOnSinglePage?: boolean
  paginationLayout?: string
  prevText?: string
  nextText?: string
  paginationBackground?: boolean
}

// 默认属性值
const props = withDefaults(defineProps<Props>(), {
  data: () => [],
  loading: false,
  total: 0,
  columns: () => [],
  stripe: true,
  border: true,
  size: 'default',
  fit: true,
  showHeader: true,
  highlightCurrentRow: true,
  emptyText: '暂无数据',
  defaultExpandAll: false,
  tooltipEffect: 'dark',
  showSummary: false,
  sumText: '合计',
  selectOnIndeterminate: true,
  indent: 16,
  lazy: false,
  showToolbar: true,
  showRefresh: true,
  showAdd: true,
  showBatchDelete: true,
  showSearch: true,
  showExport: true,
  showColumnSetting: true,
  showSelection: false,
  showIndex: true,
  showActions: true,
  showEdit: true,
  showDelete: true,
  showPagination: true,
  reserveSelection: false,
  actionWidth: 150,
  actionAlign: 'center',
  actionFixed: 'right',
  currentPage: 1,
  pageSize: 20,
  pageSizes: () => [10, 20, 50, 100],
  paginationSize: 'default',
  paginationDisabled: false,
  hideOnSinglePage: false,
  paginationLayout: 'total, sizes, prev, pager, next, jumper',
  paginationBackground: true
})

// 事件定义
const emit = defineEmits([
  'refresh',
  'add',
  'edit',
  'delete',
  'batch-delete',
  'export',
  'search',
  'selection-change',
  'sort-change',
  'filter-change',
  'size-change',
  'current-change',
  'page-change'
])

// 响应式数据
const tableRef = ref()
const searchKeyword = ref('')
const selectedRows = ref<any[]>([])
const showColumnDialog = ref(false)
const columnSettings = ref<TableColumn[]>([])
const checkedColumns = ref<string[]>([])
const checkAll = ref(true)
const isIndeterminate = ref(false)

// 计算属性
const tableData = computed(() => props.data)
const tableHeight = computed(() => props.height)
const visibleColumns = computed(() => {
  if (checkedColumns.value.length === 0) {
    return props.columns
  }
  return columnSettings.value.filter(col => checkedColumns.value.includes(col.prop))
})

// 初始化列设置
const initColumnSettings = () => {
  columnSettings.value = [...props.columns]
  checkedColumns.value = props.columns.map(col => col.prop)
}

// 搜索处理（防抖）
const handleSearch = debounce((value: string) => {
  emit('search', value)
}, 300)

// 事件处理函数
const handleRefresh = () => {
  emit('refresh')
}

const handleAdd = () => {
  emit('add')
}

const handleEdit = (row: any, index: number) => {
  emit('edit', row, index)
}

const handleDelete = (row: any, index: number) => {
  ElMessageBox.confirm('确定要删除这条记录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    emit('delete', row, index)
  }).catch(() => {
    // 用户取消删除
  })
}

const handleBatchDelete = () => {
  if (selectedRows.value.length === 0) {
    ElMessage.warning('请先选择要删除的记录')
    return
  }
  
  ElMessageBox.confirm(`确定要删除选中的 ${selectedRows.value.length} 条记录吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    emit('batch-delete', selectedRows.value)
  }).catch(() => {
    // 用户取消删除
  })
}

const handleExport = () => {
  emit('export')
}

const handleSelectionChange = (selection: any[]) => {
  selectedRows.value = selection
  emit('selection-change', selection)
}

const handleSortChange = (sort: any) => {
  emit('sort-change', sort)
}

const handleFilterChange = (filters: any) => {
  emit('filter-change', filters)
}

const handleSizeChange = (size: number) => {
  emit('size-change', size)
}

const handleCurrentPageChange = (page: number) => {
  emit('current-change', page)
  emit('page-change', { page, size: props.pageSize })
}

// 列设置相关
const handleCheckAllChange = (val: boolean) => {
  checkedColumns.value = val ? columnSettings.value.map(col => col.prop) : []
  isIndeterminate.value = false
}

const handleCheckedColumnsChange = (value: string[]) => {
  const checkedCount = value.length
  checkAll.value = checkedCount === columnSettings.value.length
  isIndeterminate.value = checkedCount > 0 && checkedCount < columnSettings.value.length
}

const handleColumnDragEnd = () => {
  // 拖拽结束后更新列顺序
}

const handleColumnSettingConfirm = () => {
  showColumnDialog.value = false
  ElMessage.success('列设置已保存')
}

// 表格事件处理（透传）
const handleSelect = (selection: any[], row: any) => {
  // 透传事件
}

const handleSelectAll = (selection: any[]) => {
  // 透传事件
}

const handleCellMouseEnter = (row: any, column: any, cell: any, event: Event) => {
  // 透传事件
}

const handleCellMouseLeave = (row: any, column: any, cell: any, event: Event) => {
  // 透传事件
}

const handleCellClick = (row: any, column: any, cell: any, event: Event) => {
  // 透传事件
}

const handleCellDblclick = (row: any, column: any, cell: any, event: Event) => {
  // 透传事件
}

const handleRowClick = (row: any, column: any, event: Event) => {
  // 透传事件
}

const handleRowContextmenu = (row: any, column: any, event: Event) => {
  // 透传事件
}

const handleRowDblclick = (row: any, column: any, event: Event) => {
  // 透传事件
}

const handleHeaderClick = (column: any, event: Event) => {
  // 透传事件
}

const handleHeaderContextmenu = (column: any, event: Event) => {
  // 透传事件
}

const handleCurrentChange = (currentRow: any, oldCurrentRow: any) => {
  // 透传事件
}

const handleHeaderDragend = (newWidth: number, oldWidth: number, column: any, event: Event) => {
  // 透传事件
}

const handleExpandChange = (row: any, expandedRows: any[]) => {
  // 透传事件
}

const handlePrevClick = (currentPage: number) => {
  // 透传事件
}

const handleNextClick = (currentPage: number) => {
  // 透传事件
}

// 公开方法
const clearSelection = () => {
  tableRef.value?.clearSelection()
}

const toggleRowSelection = (row: any, selected?: boolean) => {
  tableRef.value?.toggleRowSelection(row, selected)
}

const toggleAllSelection = () => {
  tableRef.value?.toggleAllSelection()
}

const toggleRowExpansion = (row: any, expanded?: boolean) => {
  tableRef.value?.toggleRowExpansion(row, expanded)
}

const setCurrentRow = (row: any) => {
  tableRef.value?.setCurrentRow(row)
}

const clearSort = () => {
  tableRef.value?.clearSort()
}

const clearFilter = (columnKeys?: string[]) => {
  tableRef.value?.clearFilter(columnKeys)
}

const doLayout = () => {
  tableRef.value?.doLayout()
}

const sort = (prop: string, order: string) => {
  tableRef.value?.sort(prop, order)
}

// 暴露方法给父组件
defineExpose({
  clearSelection,
  toggleRowSelection,
  toggleAllSelection,
  toggleRowExpansion,
  setCurrentRow,
  clearSort,
  clearFilter,
  doLayout,
  sort
})

// 监听列变化
watch(() => props.columns, () => {
  initColumnSettings()
}, { immediate: true })

// 组件挂载
onMounted(() => {
  initColumnSettings()
})
</script>

<style scoped lang="scss">
.data-table {
  .table-toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    padding: 16px;
    background: var(--el-bg-color-page);
    border-radius: 4px;

    .toolbar-left {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .toolbar-right {
      display: flex;
      align-items: center;
      gap: 8px;
    }
  }

  .table-pagination {
    display: flex;
    justify-content: flex-end;
    margin-top: 16px;
    padding: 16px 0;
  }

  .column-setting {
    .column-item {
      display: flex;
      align-items: center;
      padding: 8px 0;
      cursor: move;

      .drag-handle {
        margin-right: 8px;
        cursor: grab;
        color: var(--el-text-color-secondary);

        &:active {
          cursor: grabbing;
        }
      }
    }
  }
}
</style>
