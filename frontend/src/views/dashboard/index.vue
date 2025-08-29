<template>
  <!-- 直接使用SecurityOverview组件 -->
  <SecurityOverview />
</template>

<script setup lang="ts">
import SecurityOverview from './SecurityOverview.vue'
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: 500;
  color: #303133;
  margin: 0;
}

.page-actions {
  display: flex;
  gap: 12px;
}

.page-content {
  min-height: 400px;
}

.content-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}
</style>
