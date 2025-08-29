module.exports = {
  // 基础配置
  printWidth: 100,
  tabWidth: 2,
  useTabs: false,
  semi: false,
  singleQuote: true,
  quoteProps: 'as-needed',
  jsxSingleQuote: true,
  trailingComma: 'none',
  bracketSpacing: true,
  bracketSameLine: false,
  arrowParens: 'avoid',
  rangeStart: 0,
  rangeEnd: Infinity,
  requirePragma: false,
  insertPragma: false,
  proseWrap: 'preserve',
  htmlWhitespaceSensitivity: 'css',
  vueIndentScriptAndStyle: false,
  endOfLine: 'lf',
  embeddedLanguageFormatting: 'auto',
  singleAttributePerLine: false,

  // 覆盖特定文件类型的配置
  overrides: [
    {
      files: '*.vue',
      options: {
        parser: 'vue',
        printWidth: 120,
        singleAttributePerLine: true
      }
    },
    {
      files: ['*.json', '*.jsonc'],
      options: {
        parser: 'json',
        printWidth: 120,
        trailingComma: 'none'
      }
    },
    {
      files: '*.md',
      options: {
        parser: 'markdown',
        printWidth: 80,
        proseWrap: 'always',
        singleQuote: false
      }
    },
    {
      files: '*.yaml',
      options: {
        parser: 'yaml',
        printWidth: 120,
        singleQuote: false
      }
    },
    {
      files: '*.yml',
      options: {
        parser: 'yaml',
        printWidth: 120,
        singleQuote: false
      }
    },
    {
      files: ['*.css', '*.scss', '*.less'],
      options: {
        parser: 'css',
        printWidth: 120,
        singleQuote: false
      }
    },
    {
      files: '*.html',
      options: {
        parser: 'html',
        printWidth: 120,
        htmlWhitespaceSensitivity: 'ignore'
      }
    }
  ]
}
