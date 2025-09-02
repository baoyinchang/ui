<template>
  <div class="asset-import">
    <el-upload
      class="upload-area"
      action="#"
      :auto-upload="false"
      :on-change="handleFileChange"
      :show-file-list="false"
      accept=".xlsx,.xls,.csv"
    >
      <el-card class="upload-card" :border="false">
        <div class="upload-icon">
          <el-icon><Upload /></el-icon>
        </div>
        <div class="upload-text">
          <p class="title">拖放文件到此处或点击上传</p>
          <p class="hint">支持 .xlsx, .xls, .csv 格式，最大 10MB</p>
          <el-button type="primary" class="upload-btn">选择文件</el-button>
        </div>
      </el-card>
    </el-upload>

    <template v-if="uploadFile">
      <el-card class="file-info" :border="false">
        <div class="file-header">
          <el-icon><Document /></el-icon>
          <span class="file-name">{{ uploadFile.name }}</span>
          <el-button 
            type="text" 
            size="small" 
            :icon="Delete" 
            class="remove-btn"
            @click="clearFile"
          />
        </div>
        <el-divider />
        <div class="import-options">
          <el-form :model="importOptions">
            <el-form-item label="重复处理">
              <el-radio-group v-model="importOptions.duplicateStrategy">
                <el-radio label="skip">跳过重复</el-radio>
                <el-radio label="update">更新重复</el-radio>
                <el-radio label="ignore">忽略重复</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="导入后操作">
              <el-checkbox v-model="importOptions.autoScan">自动扫描导入的资产</el-checkbox>
            </el-form-item>
          </el-form>
        </div>
      </el-card>

      <div class="import-actions">
        <el-button @click="$emit('cancel')">取消</el-button>
        <el-button type="primary" @click="handleImport">确认导入</el-button>
      </div>
    </template>

    <el-card class="template-card" :border="false">
      <div class="template-info">
        <p>如需批量导入，可下载模板填写后上传</p>
        <el-button 
          type="success" 
          :icon="Download" 
          @click="downloadTemplate"
        >
          下载模板
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage, ElLoading } from 'element-plus'
import { Upload, Document, Delete, Download } from '@element-plus/icons-vue'
import { assetsApi } from '@/api'

// 上传文件状态
const uploadFile = ref<File | null>(null)

// 导入选项
const importOptions = reactive({
  duplicateStrategy: 'skip', // skip:跳过 update:更新 ignore:忽略
  autoScan: true
})

// 处理文件选择
const handleFileChange = (uploadFile: any) => {
  // 验证文件大小
  if (uploadFile.size > 10 * 1024 * 1024) {
    ElMessage.error('文件大小不能超过10MB')
    return
  }
  uploadFile.value = uploadFile.raw
}

// 清除选中文件
const clearFile = () => {
  uploadFile.value = null
}

// 下载模板
const downloadTemplate = async () => {
  try {
    await assetsApi.downloadImportTemplate()
    ElMessage.success('模板下载成功')
  } catch (error) {
    console.error('模板下载失败:', error)
    ElMessage.error('模板下载失败')
  }
}

// 处理导入
const handleImport = async () => {
  if (!uploadFile.value) return

  const loading = ElLoading.service({
    lock: true,
    text: '正在导入...',
    background: 'rgba(0, 0, 0, 0.7)'
  })

  try {
    const formData = new FormData()
    formData.append('file', uploadFile.value)
    formData.append('duplicate_strategy', importOptions.duplicateStrategy)
    formData.append('auto_scan', importOptions.autoScan ? '1' : '0')

    await assetsApi.batchImportAssets(formData)
    ElMessage.success('导入成功')
    uploadFile.value = null
    loading.close()
    $emit('success')
  } catch (error) {
    console.error('导入失败:', error)
    ElMessage.error('导入失败')
    loading.close()
  }
}
</script>

<style scoped>
.asset-import {
  padding: 10px 0;
}

.upload-area {
  margin-bottom: 20px;
}

.upload-card {
  text-align: center;
  padding: 30px 0;
  border: 2px dashed #ccc;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.upload-card:hover {
  border-color: #409eff;
}

.upload-icon {
  font-size: 48px;
  color: #409eff;
  margin-bottom: 16px;
}

.upload-text .title {
  font-size: 16px;
  margin-bottom: 8px;
}

.upload-text .hint {
  color: #666;
  margin-bottom: 16px;
}

.file-info {
  margin-bottom: 20px;
  border: 1px solid #ebeef5;
}

.file-header {
  display: flex;
  align-items: center;
  padding: 12px 0;
}

.file-header .el-icon {
  margin-right: 8px;
  color: #409eff;
}

.file-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.remove-btn {
  color: #f5222d;
}

.import-options {
  padding: 10px 0;
}

.import-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-bottom: 20px;
}

.template-card {
  padding: 15px;
  background-color: #f5f7fa;
}

.template-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.template-info p {
  margin: 0;
  color: #666;
}
</style>