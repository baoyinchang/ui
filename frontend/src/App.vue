<template>
  <div id="app" :class="{ 'dark-theme': appStore.theme === 'dark' }">
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAppStore } from '@/store/app'
import { useUserStore } from '@/store/user'

const appStore = useAppStore()
const userStore = useUserStore()

onMounted(() => {
  // 应用主题
  document.documentElement.setAttribute('data-theme', appStore.theme)

  // 如果有token，尝试刷新用户信息
  if (userStore.token) {
    userStore.refreshUserInfo().catch(() => {
      // 刷新失败，可能token已过期
      console.warn('用户信息刷新失败，可能需要重新登录')
    })
  }
})

// 监听主题变化
appStore.$subscribe((mutation, state) => {
  if (mutation.events?.key === 'theme') {
    document.documentElement.setAttribute('data-theme', state.theme)
  }
})
</script>

<style lang="scss">
#app {
  height: 100%;
  transition: all 0.3s ease;
}

// 暗色主题
.dark-theme {
  background-color: #1a1a1a;
  color: #ffffff;
}

// 全局滚动条样式
* {
  scrollbar-width: thin;
  scrollbar-color: #c1c1c1 #f1f1f1;
}

*::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

*::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

*::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

*::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

// 暗色主题下的滚动条
.dark-theme {
  * {
    scrollbar-color: #4a4a4a #2a2a2a;
  }

  *::-webkit-scrollbar-track {
    background: #2a2a2a;
  }

  *::-webkit-scrollbar-thumb {
    background: #4a4a4a;
  }

  *::-webkit-scrollbar-thumb:hover {
    background: #5a5a5a;
  }
}
</style>