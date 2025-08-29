#!/usr/bin/env node

/**
 * 前端代码检查脚本
 * 检查语法错误、类型错误、导入问题等
 */

const fs = require('fs')
const path = require('path')
const { execSync } = require('child_process')

class FrontendChecker {
  constructor() {
    this.issues = []
    this.frontendDir = path.resolve(__dirname, '../frontend')
  }

  logIssue(level, component, message) {
    this.issues.push({ level, component, message })
  }

  checkFileExists(filePath, description) {
    const fullPath = path.join(this.frontendDir, filePath)
    if (fs.existsSync(fullPath)) {
      console.log(`✅ ${description}`)
      return true
    } else {
      this.logIssue('ERROR', 'Files', `${description} 不存在: ${filePath}`)
      return false
    }
  }

  checkPackageJson() {
    console.log('\n📦 检查 package.json...')
    
    const packagePath = path.join(this.frontendDir, 'package.json')
    if (!fs.existsSync(packagePath)) {
      this.logIssue('ERROR', 'Package', 'package.json 不存在')
      return false
    }

    try {
      const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf8'))
      
      // 检查必要的依赖
      const requiredDeps = [
        'vue',
        'vue-router',
        'pinia',
        'element-plus',
        'axios',
        'echarts'
      ]

      const missingDeps = requiredDeps.filter(dep => 
        !packageJson.dependencies?.[dep] && !packageJson.devDependencies?.[dep]
      )

      if (missingDeps.length > 0) {
        this.logIssue('ERROR', 'Dependencies', `缺少依赖: ${missingDeps.join(', ')}`)
      } else {
        console.log('✅ 核心依赖完整')
      }

      // 检查脚本
      const requiredScripts = ['dev', 'build', 'preview']
      const missingScripts = requiredScripts.filter(script => 
        !packageJson.scripts?.[script]
      )

      if (missingScripts.length > 0) {
        this.logIssue('WARNING', 'Scripts', `缺少脚本: ${missingScripts.join(', ')}`)
      } else {
        console.log('✅ 构建脚本完整')
      }

      return true
    } catch (error) {
      this.logIssue('ERROR', 'Package', `package.json 解析失败: ${error.message}`)
      return false
    }
  }

  checkConfigFiles() {
    console.log('\n⚙️ 检查配置文件...')
    
    const configFiles = [
      { path: 'vite.config.ts', desc: 'Vite配置文件' },
      { path: 'tsconfig.json', desc: 'TypeScript配置文件' },
      { path: '.eslintrc.cjs', desc: 'ESLint配置文件' },
      { path: '.prettierrc.cjs', desc: 'Prettier配置文件' },
      { path: '.env.development', desc: '开发环境配置' }
    ]

    let allExist = true
    configFiles.forEach(file => {
      if (!this.checkFileExists(file.path, file.desc)) {
        allExist = false
      }
    })

    return allExist
  }

  checkSourceStructure() {
    console.log('\n📁 检查源码结构...')
    
    const requiredDirs = [
      { path: 'src', desc: '源码目录' },
      { path: 'src/components', desc: '组件目录' },
      { path: 'src/views', desc: '页面目录' },
      { path: 'src/api', desc: 'API目录' },
      { path: 'src/utils', desc: '工具函数目录' },
      { path: 'src/types', desc: '类型定义目录' },
      { path: 'src/stores', desc: '状态管理目录' },
      { path: 'src/router', desc: '路由目录' },
      { path: 'src/styles', desc: '样式目录' }
    ]

    let allExist = true
    requiredDirs.forEach(dir => {
      const fullPath = path.join(this.frontendDir, dir.path)
      if (fs.existsSync(fullPath) && fs.statSync(fullPath).isDirectory()) {
        console.log(`✅ ${dir.desc}`)
      } else {
        this.logIssue('ERROR', 'Structure', `${dir.desc} 不存在: ${dir.path}`)
        allExist = false
      }
    })

    return allExist
  }

  checkImportPaths() {
    console.log('\n🔗 检查导入路径...')
    
    // 检查关键文件的导入
    const keyFiles = [
      'src/main.ts',
      'src/App.vue',
      'src/router/index.ts',
      'src/api/request.ts'
    ]

    keyFiles.forEach(file => {
      const fullPath = path.join(this.frontendDir, file)
      if (fs.existsSync(fullPath)) {
        try {
          const content = fs.readFileSync(fullPath, 'utf8')
          
          // 检查是否有明显的导入错误
          const importLines = content.split('\n').filter(line => 
            line.trim().startsWith('import') || line.trim().startsWith('from')
          )

          // 简单检查：查找可能的路径问题
          const suspiciousImports = importLines.filter(line => 
            line.includes('../../../') || // 过深的相对路径
            line.includes('undefined') ||  // 未定义的导入
            line.includes('null')         // 空导入
          )

          if (suspiciousImports.length > 0) {
            this.logIssue('WARNING', 'Imports', `${file} 可能存在导入问题`)
          }

        } catch (error) {
          this.logIssue('WARNING', 'Imports', `无法读取文件: ${file}`)
        }
      }
    })

    console.log('✅ 导入路径检查完成')
  }

  checkTypeScript() {
    console.log('\n🔍 检查 TypeScript 配置...')
    
    try {
      // 检查 tsconfig.json
      const tsconfigPath = path.join(this.frontendDir, 'tsconfig.json')
      if (fs.existsSync(tsconfigPath)) {
        const tsconfig = JSON.parse(fs.readFileSync(tsconfigPath, 'utf8'))
        
        // 检查关键配置
        const compilerOptions = tsconfig.compilerOptions || {}
        
        if (!compilerOptions.strict) {
          this.logIssue('WARNING', 'TypeScript', '建议启用严格模式')
        }

        if (!compilerOptions.paths || !compilerOptions.paths['@/*']) {
          this.logIssue('WARNING', 'TypeScript', '缺少路径映射配置')
        }

        console.log('✅ TypeScript 配置检查完成')
      }
    } catch (error) {
      this.logIssue('ERROR', 'TypeScript', `TypeScript 配置检查失败: ${error.message}`)
    }
  }

  checkEnvironmentFiles() {
    console.log('\n🌍 检查环境配置...')
    
    const envFiles = [
      '.env.development',
      '.env.production'
    ]

    envFiles.forEach(file => {
      const fullPath = path.join(this.frontendDir, file)
      if (fs.existsSync(fullPath)) {
        try {
          const content = fs.readFileSync(fullPath, 'utf8')
          
          // 检查必要的环境变量
          const requiredVars = [
            'VITE_API_BASE_URL',
            'VITE_APP_TITLE'
          ]

          const missingVars = requiredVars.filter(varName => 
            !content.includes(varName)
          )

          if (missingVars.length > 0) {
            this.logIssue('WARNING', 'Environment', 
              `${file} 缺少环境变量: ${missingVars.join(', ')}`)
          } else {
            console.log(`✅ ${file} 配置完整`)
          }

        } catch (error) {
          this.logIssue('ERROR', 'Environment', `读取 ${file} 失败: ${error.message}`)
        }
      }
    })
  }

  generateReport() {
    console.log('\n' + '='.repeat(60))
    console.log('🔍 前端代码检查报告')
    console.log('='.repeat(60))

    if (this.issues.length === 0) {
      console.log('✅ 所有检查项目都通过了！')
      return
    }

    // 按级别分组
    const errors = this.issues.filter(issue => issue.level === 'ERROR')
    const warnings = this.issues.filter(issue => issue.level === 'WARNING')
    const infos = this.issues.filter(issue => issue.level === 'INFO')

    if (errors.length > 0) {
      console.log(`\n❌ 严重问题 (${errors.length}个):`)
      errors.forEach(issue => {
        console.log(`   [${issue.component}] ${issue.message}`)
      })
    }

    if (warnings.length > 0) {
      console.log(`\n⚠️  警告 (${warnings.length}个):`)
      warnings.forEach(issue => {
        console.log(`   [${issue.component}] ${issue.message}`)
      })
    }

    if (infos.length > 0) {
      console.log(`\n💡 信息 (${infos.length}个):`)
      infos.forEach(issue => {
        console.log(`   [${issue.component}] ${issue.message}`)
      })
    }

    console.log(`\n总计: ${errors.length}个错误, ${warnings.length}个警告, ${infos.length}个信息`)

    // 修复建议
    if (errors.length > 0 || warnings.length > 0) {
      console.log('\n🔧 修复建议:')
      console.log('1. 运行 npm install 安装依赖')
      console.log('2. 检查配置文件是否完整')
      console.log('3. 确认源码结构正确')
      console.log('4. 修复导入路径问题')
      console.log('5. 完善环境变量配置')
    }
  }

  runAllChecks() {
    console.log('🚀 开始前端代码检查...\n')

    // 运行所有检查
    this.checkPackageJson()
    this.checkConfigFiles()
    this.checkSourceStructure()
    this.checkImportPaths()
    this.checkTypeScript()
    this.checkEnvironmentFiles()

    // 生成报告
    this.generateReport()

    // 返回是否有严重错误
    const hasErrors = this.issues.some(issue => issue.level === 'ERROR')
    return !hasErrors
  }
}

function main() {
  const checker = new FrontendChecker()
  const success = checker.runAllChecks()

  if (success) {
    console.log('\n🎉 前端代码检查完成，没有发现严重问题！')
    process.exit(0)
  } else {
    console.log('\n💥 发现严重问题，请修复后重试！')
    process.exit(1)
  }
}

if (require.main === module) {
  main()
}
