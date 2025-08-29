<template>
  <template v-for="route in routes" :key="route.path">
    <!-- 无子菜单的普通菜单项 -->
    <el-menu-item
      v-if="!route.children || route.children.length === 0"
      :index="getFullPath(route)"
      v-show="!route.meta?.hideInMenu && hasPermission(route.meta?.permission)"
    >
      <el-icon v-if="route.meta?.icon">
        <component :is="route.meta.icon" />
      </el-icon>
      <template #title>{{ route.meta?.title }}</template>
    </el-menu-item>
    
    <!-- 有子菜单的菜单组 -->
    <el-sub-menu
      v-else-if="route.children && route.children.length > 0 && hasPermission(route.meta?.permission)"
      :index="getFullPath(route)"
    >
      <template #title>
        <el-icon v-if="route.meta?.icon">
          <component :is="route.meta.icon" />
        </el-icon>
        <span>{{ route.meta?.title }}</span>
      </template>
      
      <!-- 递归渲染子菜单 -->
      <MenuTree 
        :routes="route.children" 
        :parent-path="getFullPath(route)"
        :has-permission="hasPermission"
      />
    </el-sub-menu>
  </template>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { RouteRecordRaw } from 'vue-router'

// 定义props
interface Props {
  routes: RouteRecordRaw[]
  parentPath?: string
  hasPermission: (permission?: string) => boolean
}

const props = withDefaults(defineProps<Props>(), {
  parentPath: ''
})

// 获取完整路径
const getFullPath = (route: RouteRecordRaw): string => {
  if (route.path.startsWith('/')) {
    // 绝对路径
    return route.path
  } else {
    // 相对路径，需要拼接父路径
    const parentPath = props.parentPath.endsWith('/') 
      ? props.parentPath.slice(0, -1) 
      : props.parentPath
    return `${parentPath}/${route.path}`
  }
}
</script>

<style scoped>
/* 菜单样式可以在这里自定义 */
</style>
