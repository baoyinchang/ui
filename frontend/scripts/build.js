#!/usr/bin/env node

/**
 * 构建脚本
 * 提供构建优化和分析功能
 */

const { execSync } = require('child_process')
const fs = require('fs')
const path = require('path')
const chalk = require('chalk')

// 构建配置
const BUILD_CONFIG = {
  // 构建模式
  modes: {
    development: 'development',
    production: 'production',
    staging: 'staging'
  },
  
  // 构建选项
  options: {
    analyze: false,
    sourcemap: false,
    minify: true,
    gzip: true,
    report: false
  }
}

/**
 * 打印横幅
 */
function printBanner() {
  console.log(chalk.cyan(`
╔══════════════════════════════════════╗
║        H-System EDR 构建工具         ║
╚══════════════════════════════════════╝
  `))
}

/**
 * 打印帮助信息
 */
function printHelp() {
  console.log(chalk.yellow(`
使用方法:
  node scripts/build.js [options]

选项:
  --mode <mode>     构建模式 (development|production|staging)
  --analyze         启用构建分析
  --sourcemap       生成源码映射
  --no-minify       禁用代码压缩
  --no-gzip         禁用Gzip压缩
  --report          生成构建报告
  --help            显示帮助信息

示例:
  node scripts/build.js --mode production --analyze
  node scripts/build.js --mode development --sourcemap
  `))
}

/**
 * 解析命令行参数
 */
function parseArgs() {
  const args = process.argv.slice(2)
  const config = { ...BUILD_CONFIG.options }
  let mode = BUILD_CONFIG.modes.production

  for (let i = 0; i < args.length; i++) {
    const arg = args[i]
    
    switch (arg) {
      case '--help':
      case '-h':
        printHelp()
        process.exit(0)
        break
        
      case '--mode':
        mode = args[++i]
        if (!Object.values(BUILD_CONFIG.modes).includes(mode)) {
          console.error(chalk.red(`错误: 无效的构建模式 "${mode}"`))
          process.exit(1)
        }
        break
        
      case '--analyze':
        config.analyze = true
        break
        
      case '--sourcemap':
        config.sourcemap = true
        break
        
      case '--no-minify':
        config.minify = false
        break
        
      case '--no-gzip':
        config.gzip = false
        break
        
      case '--report':
        config.report = true
        break
        
      default:
        if (arg.startsWith('--')) {
          console.error(chalk.red(`错误: 未知选项 "${arg}"`))
          process.exit(1)
        }
    }
  }

  return { mode, config }
}

/**
 * 设置环境变量
 */
function setEnvironment(mode, config) {
  process.env.NODE_ENV = mode
  process.env.VITE_BUILD_SOURCEMAP = config.sourcemap ? 'true' : 'false'
  process.env.VITE_BUILD_DROP_CONSOLE = mode === 'production' ? 'true' : 'false'
  
  if (config.analyze) {
    process.env.ANALYZE = 'true'
  }
}

/**
 * 清理构建目录
 */
function cleanBuildDir() {
  const distPath = path.resolve(__dirname, '../dist')
  
  if (fs.existsSync(distPath)) {
    console.log(chalk.yellow('清理构建目录...'))
    fs.rmSync(distPath, { recursive: true, force: true })
    console.log(chalk.green('✅ 构建目录已清理'))
  }
}

/**
 * 执行构建
 */
function runBuild(mode) {
  console.log(chalk.blue(`🚀 开始构建 (${mode} 模式)...`))
  
  const startTime = Date.now()
  
  try {
    execSync('npm run build', {
      stdio: 'inherit',
      cwd: path.resolve(__dirname, '..')
    })
    
    const endTime = Date.now()
    const duration = ((endTime - startTime) / 1000).toFixed(2)
    
    console.log(chalk.green(`✅ 构建完成! 耗时: ${duration}s`))
    
    return true
  } catch (error) {
    console.error(chalk.red('❌ 构建失败:'))
    console.error(error.message)
    return false
  }
}

/**
 * 生成构建报告
 */
function generateReport() {
  const distPath = path.resolve(__dirname, '../dist')
  
  if (!fs.existsSync(distPath)) {
    console.error(chalk.red('错误: 构建目录不存在'))
    return
  }
  
  console.log(chalk.blue('📊 生成构建报告...'))
  
  // 计算文件大小
  function getFileSize(filePath) {
    const stats = fs.statSync(filePath)
    return stats.size
  }
  
  // 格式化文件大小
  function formatSize(bytes) {
    const sizes = ['B', 'KB', 'MB', 'GB']
    if (bytes === 0) return '0 B'
    const i = Math.floor(Math.log(bytes) / Math.log(1024))
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i]
  }
  
  // 扫描文件
  function scanDirectory(dir, files = []) {
    const items = fs.readdirSync(dir)
    
    for (const item of items) {
      const fullPath = path.join(dir, item)
      const stat = fs.statSync(fullPath)
      
      if (stat.isDirectory()) {
        scanDirectory(fullPath, files)
      } else {
        const relativePath = path.relative(distPath, fullPath)
        files.push({
          path: relativePath,
          size: stat.size,
          formattedSize: formatSize(stat.size)
        })
      }
    }
    
    return files
  }
  
  const files = scanDirectory(distPath)
  const totalSize = files.reduce((sum, file) => sum + file.size, 0)
  
  // 按大小排序
  files.sort((a, b) => b.size - a.size)
  
  console.log(chalk.cyan('\n📁 构建文件统计:'))
  console.log(chalk.gray('─'.repeat(60)))
  
  files.slice(0, 10).forEach(file => {
    console.log(`${file.formattedSize.padStart(8)} ${file.path}`)
  })
  
  if (files.length > 10) {
    console.log(chalk.gray(`... 还有 ${files.length - 10} 个文件`))
  }
  
  console.log(chalk.gray('─'.repeat(60)))
  console.log(chalk.green(`总大小: ${formatSize(totalSize)}`))
  console.log(chalk.green(`文件数: ${files.length}`))
  
  // 保存报告到文件
  const report = {
    buildTime: new Date().toISOString(),
    totalSize,
    totalFiles: files.length,
    files: files.map(f => ({
      path: f.path,
      size: f.size
    }))
  }
  
  const reportPath = path.join(distPath, 'build-report.json')
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2))
  
  console.log(chalk.blue(`📄 构建报告已保存: ${reportPath}`))
}

/**
 * 主函数
 */
function main() {
  printBanner()
  
  const { mode, config } = parseArgs()
  
  console.log(chalk.blue(`构建模式: ${mode}`))
  console.log(chalk.blue(`构建选项: ${JSON.stringify(config, null, 2)}`))
  
  // 设置环境
  setEnvironment(mode, config)
  
  // 清理构建目录
  cleanBuildDir()
  
  // 执行构建
  const success = runBuild(mode)
  
  if (!success) {
    process.exit(1)
  }
  
  // 生成报告
  if (config.report) {
    generateReport()
  }
  
  console.log(chalk.green('\n🎉 构建流程完成!'))
}

// 运行主函数
if (require.main === module) {
  main()
}

module.exports = {
  BUILD_CONFIG,
  parseArgs,
  setEnvironment,
  cleanBuildDir,
  runBuild,
  generateReport
}
