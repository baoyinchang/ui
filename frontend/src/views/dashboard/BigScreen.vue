<template>
  <div class="BigScreen-container">
    <h2>Bigscreen</h2>
    <p>此页面正在开发中...</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// 组件逻辑
onMounted(() => {
  console.log('Bigscreen 组件已挂载')
})
</script>

<style scoped>
.BigScreen-container {
  padding: 20px;
}
</style>
