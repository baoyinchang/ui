<template>
  <div class="asset-detail">
    <el-row :gutter="20">
      <!-- 基本信息卡片 -->
      <el-col :span="16">
        <el-card title="基本信息">
          <el-descriptions column="1" border>
            <el-descriptions-item label="资产名称">{{ asset.name }}</el-descriptions-item>
            <el-descriptions-item label="资产类型">
              <StatusTag 
                :value="asset.asset_type" 
                type="custom" 
                :custom-mapping="assetTypeMapping" 
              />
            </el-descriptions-item>
            <el-descriptions-item label="IP地址">{{ asset.ip_address }}</el-descriptions-item>
            <el-descriptions-item label="MAC地址">{{ asset.mac_address || '-' }}</el-descriptions-item>
            <el-descriptions-item label="操作系统">{{ asset.os_version || '-' }}</el-descriptions-item>
            <el-descriptions-item label="状态">
              <StatusTag :value="asset.status" type="asset-status" show-dot />
            </el-descriptions-item>
            <el-descriptions-item label="风险评分">
              <el-progress
                :percentage="asset.risk_score"
                :color="getRiskColor(asset.risk_score)"
                :show-text="false"
                :stroke-width="6"
                style="width: 100px; display: inline-block; margin-right: 8px"
              />
              {{ asset.risk_score }}%
            </el-descriptions-item>
            <el-descriptions-item label="最后活跃时间">{{ formatTime(asset.last_seen) }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>

      <!-- 操作卡片 -->
      <el-col :span="8">
        <el-card title="操作">
          <div class="action-buttons">
            <el-button type="primary" :icon="Edit" @click="handleEdit">编辑资产</el-button>
            <el-button type="success" :icon="Refresh" @click="handleRescan">重新扫描</el-button>
            <el-button type="warning" :icon="Download" @click="handleExport">导出信息</el-button>
            <el-button type="danger" :icon="Delete" @click="handleDelete" v-if="!asset.is_honeypot">删除资产</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 编辑表单对话框 -->
    <el-dialog v-model="showEditDialog" title="编辑资产" width="600px">
      <el-form ref="editFormRef" :model="editForm" :rules="editRules" label-width="100px">
        <el-form-item label="资产名称" prop="name">
          <el-input v-model="editForm.name" />
        </el-form-item>
        <el-form-item label="资产类型" prop="asset_type">
          <el-select v-model="editForm.asset_type">
            <el-option 
              v-for="(label, key) in ASSET_TYPE_LABELS" 
              :key="key" 
              :label="label" 
              :value="key" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="editForm.status">
            <el-option label="正常" value="normal" />
            <el-option label="警告" value="warning" />
            <el-option label="危险" value="danger" />
            <el-option label="离线" value="offline" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="editForm.description" type="textarea" rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSaveEdit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Edit, Refresh, Download, Delete } from '@element-plus/icons-vue'
import StatusTag from '@/components/common/StatusTag.vue'
import { assetsApi } from '@/api'
import { formatTime, ASSET_TYPE_LABELS } from '@/utils'
import type { Asset } from '@/types/api'
import type { UpdateAssetRequest } from '@/types/api'

// 接收父组件传入的资产数据
const props = defineProps<{
  asset: Asset
}>()

// 暴露事件
const emit = defineEmits<{
  (e: 'update'): void
  (e: 'close'): void
}>()

// 状态管理
const showEditDialog = ref(false)
const editFormRef = ref()
const editForm = reactive<UpdateAssetRequest>({
  name: '',
  asset_type: '',
  status: '',
  description: ''
})

// 验证规则
const editRules = {
  name: [{ required: true, message: '请输入资产名称', trigger: 'blur' }],
  asset_type: [{ required: true, message: '请选择资产类型', trigger: 'change' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

// 资产类型映射
const assetTypeMapping = computed(() => {
  const mapping: Record<string, { text: string }> = {}
  Object.entries(ASSET_TYPE_LABELS).forEach(([key, value]) => {
    mapping[key] = { text: value }
  })
  return mapping
})

// 初始化表单数据
onMounted(() => {
  Object.assign(editForm, props.asset)
})

// 风险颜色计算
const getRiskColor = (score: number) => {
  if (score < 30) return '#52c41a'
  if (score < 70) return '#faad14'
  return '#f5222d'
}

// 编辑资产
const handleEdit = () => {
  Object.assign(editForm, props.asset)
  showEditDialog.value = true
}

// 保存编辑
const handleSaveEdit = async () => {
  try {
    await editFormRef.value.validate()
    await assetsApi.updateAsset(props.asset.id, editForm)
    ElMessage.success('更新成功')
    showEditDialog.value = false
    emit('update')
  } catch (error) {
    console.error('更新失败:', error)
  }
}

// 重新扫描
const handleRescan = async () => {
  try {
    await assetsApi.rescanAsset(props.asset.id)
    ElMessage.success('扫描任务已提交')
    emit('update')
  } catch (error) {
    console.error('扫描失败:', error)
  }
}

// 导出信息
const handleExport = async () => {
  try {
    await assetsApi.exportAsset(props.asset.id)
    ElMessage.success('导出成功')
  } catch (error) {
    console.error('导出失败:', error)
  }
}

// 删除资产
const handleDelete = async () => {
  try {
    await ElMessageBox.confirm('确定要删除该资产吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await assetsApi.deleteAsset(props.asset.id)
    ElMessage.success('删除成功')
    emit('close')
    emit('update')
  } catch (error) {
    // 取消删除不做处理
  }
}
</script>

<style scoped>
.asset-detail {
  padding: 16px 0;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.el-progress {
  vertical-align: middle;
}
</style>