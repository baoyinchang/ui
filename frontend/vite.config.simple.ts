import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import type { UserConfig, ConfigEnv } from 'vite'

// 简化的Vite配置 - 只包含必需的插件
export default defineConfig(({ command, mode }: ConfigEnv): UserConfig => {
  const root = process.cwd()
  const env = loadEnv(mode, root)
  const isBuild = command === 'build'

  return {
    root,
    base: env.VITE_PUBLIC_PATH || '/',

    plugins: [
      // Vue支持
      vue({
        script: {
          defineModel: true,
          propsDestructure: true
        }
      }),

      // 自动导入
      AutoImport({
        imports: [
          'vue',
          'vue-router',
          'pinia',
          {
            'element-plus': [
              'ElMessage',
              'ElMessageBox',
              'ElNotification',
              'ElLoading'
            ]
          }
        ],
        resolvers: [ElementPlusResolver()],
        dts: true,
        eslintrc: {
          enabled: true,
          filepath: './.eslintrc-auto-import.json',
          globalsPropValue: true
        }
      }),

      // 组件自动导入
      Components({
        resolvers: [ElementPlusResolver()],
        dts: true
      })
    ],

    // 路径别名
    resolve: {
      alias: {
        '@': resolve(__dirname, 'src'),
        '~': resolve(__dirname, 'src'),
        'vue': 'vue/dist/vue.esm-bundler.js'
      }
    },

    // CSS配置
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: `@import "@/assets/css/variables.scss";`
        }
      }
    },

    // 开发服务器配置
    server: {
      host: '0.0.0.0',
      port: Number(env.VITE_DEV_PORT) || 3000,
      open: env.VITE_DEV_OPEN === 'true',
      cors: true,
      proxy: {
        '/api': {
          target: env.VITE_API_BASE_URL || 'http://localhost:8000',
          changeOrigin: true,
          // 不重写路径，保持 /api 前缀
        }
      }
    },

    // 构建配置
    build: {
      target: 'es2015',
      outDir: 'dist',
      assetsDir: 'assets',
      sourcemap: env.VITE_BUILD_SOURCEMAP === 'true',
      minify: 'terser',
      terserOptions: {
        compress: {
          drop_console: env.VITE_BUILD_DROP_CONSOLE === 'true',
          drop_debugger: true
        }
      },
      rollupOptions: {
        output: {
          chunkFileNames: 'assets/js/[name]-[hash].js',
          entryFileNames: 'assets/js/[name]-[hash].js',
          assetFileNames: 'assets/[ext]/[name]-[hash].[ext]',
          manualChunks: {
            vue: ['vue', 'vue-router', 'pinia'],
            elementPlus: ['element-plus'],
            echarts: ['echarts', 'vue-echarts']
          }
        }
      },
      chunkSizeWarningLimit: 1000
    },

    // 优化配置
    optimizeDeps: {
      include: [
        'vue',
        'vue-router',
        'pinia',
        'element-plus',
        'axios',
        'echarts',
        'vue-echarts'
      ]
    },

    // 定义全局变量
    define: {
      __VUE_OPTIONS_API__: true,
      __VUE_PROD_DEVTOOLS__: false
    }
  }
})
