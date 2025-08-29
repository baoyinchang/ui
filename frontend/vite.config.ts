import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import { createHtmlPlugin } from 'vite-plugin-html'
import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'
import { visualizer } from 'rollup-plugin-visualizer'
import vueJsx from '@vitejs/plugin-vue-jsx'
import { compression } from 'vite-plugin-compression2'
import type { UserConfig, ConfigEnv } from 'vite'

// https://vitejs.dev/config/
export default defineConfig(({ command, mode }: ConfigEnv): UserConfig => {
  const root = process.cwd()
  const env = loadEnv(mode, root)
  const isBuild = command === 'build'
  const isDev = mode === 'development'
  const isProd = mode === 'production'

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

      // JSX支持
      vueJsx(),

      // 自动导入
      AutoImport({
        resolvers: [ElementPlusResolver()],
        imports: [
          'vue',
          'vue-router',
          'pinia',
          '@vueuse/core'
        ],
        dts: 'src/types/auto-imports.d.ts',
        eslintrc: {
          enabled: true,
          filepath: './.eslintrc-auto-import.json',
          globalsPropValue: true
        }
      }),

      // 组件自动导入
      Components({
        resolvers: [ElementPlusResolver()],
        dts: 'src/types/components.d.ts',
        dirs: ['src/components'],
        extensions: ['vue', 'tsx'],
        include: [/\.vue$/, /\.vue\?vue/, /\.tsx$/]
      }),

      // HTML模板处理
      createHtmlPlugin({
        inject: {
          data: {
            title: env.VITE_APP_TITLE || 'H-System EDR平台',
            description: env.VITE_APP_DESCRIPTION || '蜜罐安全管理系统'
          }
        },
        minify: isBuild
      }),

      // SVG图标
      createSvgIconsPlugin({
        iconDirs: [resolve(root, 'src/assets/icons')],
        symbolId: 'icon-[dir]-[name]',
        svgoOptions: {
          plugins: [
            {
              name: 'removeAttrs',
              params: {
                attrs: ['class', 'data-name', 'fill', 'stroke']
              }
            }
          ]
        }
      }),

      // Gzip压缩
      isBuild && compression({
        algorithm: 'gzip',
        exclude: [/\.(br)$/, /\.(gz)$/]
      }),

      // 构建分析
      process.env.ANALYZE && visualizer({
        filename: 'dist/stats.html',
        open: true,
        gzipSize: true,
        brotliSize: true
      })
    ].filter(Boolean),
    resolve: {
      alias: {
        '@': resolve(root, 'src'),
        '~': resolve(root, 'src'),
        '#': resolve(root, 'types')
      }
    },

    css: {
      preprocessorOptions: {
        scss: {
          additionalData: `
            @use "@/styles/variables.scss" as *;
            @use "@/styles/mixins.scss" as *;
          `,
          charset: false
        }
      },
      postcss: {
        plugins: [
          {
            postcssPlugin: 'internal:charset-removal',
            AtRule: {
              charset: (atRule) => {
                if (atRule.name === 'charset') {
                  atRule.remove()
                }
              }
            }
          }
        ]
      }
    },

    server: {
      host: '0.0.0.0',
      port: Number(env.VITE_DEV_PORT) || 3000,
      open: env.VITE_DEV_OPEN === 'true',
      cors: true,
      proxy: env.VITE_DEV_PROXY === 'true' ? {
        '/api': {
          target: env.VITE_API_BASE_URL || 'http://localhost:8000',
          changeOrigin: true,
          // 不重写路径，保持 /api 前缀
          configure: (proxy) => {
            proxy.on('error', (err, req, res) => {
              console.log('proxy error', err)
            })
            proxy.on('proxyReq', (proxyReq, req) => {
              console.log('Sending Request:', req.method, req.url)
            })
            proxy.on('proxyRes', (proxyRes, req) => {
              console.log('Received Response:', proxyRes.statusCode, req.url)
            })
          }
        }
      } : undefined
    },

    build: {
      target: 'es2015',
      outDir: 'dist',
      assetsDir: 'assets',
      sourcemap: env.VITE_BUILD_SOURCEMAP === 'true',
      minify: 'terser',
      terserOptions: {
        compress: {
          drop_console: env.VITE_BUILD_DROP_CONSOLE === 'true',
          drop_debugger: true,
          pure_funcs: ['console.log']
        },
        format: {
          comments: false
        }
      },
      rollupOptions: {
        output: {
          chunkFileNames: 'assets/js/[name]-[hash].js',
          entryFileNames: 'assets/js/[name]-[hash].js',
          assetFileNames: (assetInfo) => {
            const info = assetInfo.name?.split('.') || []
            let extType = info[info.length - 1]

            if (/\.(mp4|webm|ogg|mp3|wav|flac|aac)(\?.*)?$/i.test(assetInfo.name || '')) {
              extType = 'media'
            } else if (/\.(png|jpe?g|gif|svg)(\?.*)?$/i.test(assetInfo.name || '')) {
              extType = 'images'
            } else if (/\.(woff2?|eot|ttf|otf)(\?.*)?$/i.test(assetInfo.name || '')) {
              extType = 'fonts'
            }

            return `assets/${extType}/[name]-[hash].[ext]`
          },
          manualChunks: {
            'vue-vendor': ['vue', 'vue-router', 'pinia'],
            'element-plus': ['element-plus'],
            'echarts': ['echarts'],
            'utils': ['axios', 'dayjs', 'lodash-es']
          }
        }
      },
      reportCompressedSize: false,
      chunkSizeWarningLimit: 1000
    },

    optimizeDeps: {
      include: [
        'vue',
        'vue-router',
        'pinia',
        'axios',
        'element-plus/es',
        'element-plus/es/components/message/style/css',
        'element-plus/es/components/message-box/style/css',
        'element-plus/es/components/notification/style/css',
        'element-plus/es/components/loading/style/css',
        '@element-plus/icons-vue',
        'echarts/core',
        'echarts/charts',
        'echarts/components',
        'echarts/renderers',
        'dayjs',
        'dayjs/plugin/relativeTime',
        'dayjs/plugin/utc',
        'dayjs/plugin/timezone'
      ],
      exclude: ['@iconify/json']
    },

    define: {
      __APP_INFO__: JSON.stringify({
        pkg: {
          name: 'h-system-edr',
          version: '1.0.0'
        },
        lastBuildTime: JSON.stringify(new Date())
      })
    }
  }
})