<template>
  <div class="index-container">
    <h2>Index</h2>
    <p>此页面正在开发中...</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// 组件逻辑
onMounted(() => {
  console.log('Index 组件已挂载')
})
</script>

<style scoped>
.index-container {
  padding: 20px;
}
</style>
