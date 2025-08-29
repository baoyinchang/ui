/**
 * 部署配置文件
 * 支持多环境部署配置
 */

const path = require('path')

// 部署环境配置
const deployConfig = {
  // 开发环境
  development: {
    name: '开发环境',
    host: 'dev.hsystem.com',
    port: 22,
    username: 'deploy',
    password: '', // 建议使用密钥认证
    privateKey: path.resolve(__dirname, '../keys/dev_rsa'),
    remotePath: '/var/www/hsystem-dev',
    localPath: path.resolve(__dirname, 'dist'),
    backup: true,
    backupPath: '/var/backups/hsystem-dev',
    commands: {
      before: [
        'echo "开始部署到开发环境..."',
        'pm2 stop hsystem-dev || true'
      ],
      after: [
        'pm2 start hsystem-dev || pm2 start /var/www/hsystem-dev/ecosystem.config.js',
        'echo "开发环境部署完成"'
      ]
    }
  },

  // 测试环境
  staging: {
    name: '测试环境',
    host: 'staging.hsystem.com',
    port: 22,
    username: 'deploy',
    privateKey: path.resolve(__dirname, '../keys/staging_rsa'),
    remotePath: '/var/www/hsystem-staging',
    localPath: path.resolve(__dirname, 'dist'),
    backup: true,
    backupPath: '/var/backups/hsystem-staging',
    commands: {
      before: [
        'echo "开始部署到测试环境..."',
        'pm2 stop hsystem-staging || true',
        'nginx -t' // 检查nginx配置
      ],
      after: [
        'pm2 start hsystem-staging',
        'nginx -s reload',
        'echo "测试环境部署完成"'
      ]
    }
  },

  // 生产环境
  production: {
    name: '生产环境',
    host: 'prod.hsystem.com',
    port: 22,
    username: 'deploy',
    privateKey: path.resolve(__dirname, '../keys/prod_rsa'),
    remotePath: '/var/www/hsystem-prod',
    localPath: path.resolve(__dirname, 'dist'),
    backup: true,
    backupPath: '/var/backups/hsystem-prod',
    keepBackups: 5, // 保留最近5个备份
    commands: {
      before: [
        'echo "开始部署到生产环境..."',
        'pm2 stop hsystem-prod || true',
        'nginx -t',
        'systemctl status nginx'
      ],
      after: [
        'pm2 start hsystem-prod',
        'nginx -s reload',
        'systemctl reload nginx',
        'echo "生产环境部署完成"',
        'curl -f http://localhost/health || echo "健康检查失败"'
      ]
    },
    // 生产环境额外配置
    confirmDeploy: true, // 部署前需要确认
    rollbackOnError: true, // 出错时自动回滚
    healthCheck: {
      url: 'http://localhost/health',
      timeout: 30000,
      retries: 3
    }
  }
}

// Docker部署配置
const dockerConfig = {
  // Docker镜像配置
  image: {
    name: 'hsystem-edr-frontend',
    tag: process.env.BUILD_VERSION || 'latest',
    registry: 'registry.hsystem.com'
  },

  // 容器配置
  container: {
    name: 'hsystem-frontend',
    ports: ['80:80', '443:443'],
    volumes: [
      '/etc/nginx/conf.d:/etc/nginx/conf.d:ro',
      '/var/log/nginx:/var/log/nginx'
    ],
    environment: {
      NODE_ENV: 'production',
      TZ: 'Asia/Shanghai'
    },
    restart: 'unless-stopped',
    networks: ['hsystem-network']
  },

  // 构建配置
  build: {
    context: '.',
    dockerfile: 'Dockerfile',
    args: {
      NODE_VERSION: '18-alpine',
      BUILD_DATE: new Date().toISOString()
    },
    target: 'production'
  }
}

// Kubernetes部署配置
const k8sConfig = {
  namespace: 'hsystem',
  deployment: {
    name: 'hsystem-frontend',
    replicas: 3,
    image: `${dockerConfig.image.registry}/${dockerConfig.image.name}:${dockerConfig.image.tag}`,
    resources: {
      requests: {
        cpu: '100m',
        memory: '128Mi'
      },
      limits: {
        cpu: '500m',
        memory: '512Mi'
      }
    },
    ports: [
      {
        name: 'http',
        containerPort: 80,
        protocol: 'TCP'
      }
    ],
    env: [
      {
        name: 'NODE_ENV',
        value: 'production'
      },
      {
        name: 'TZ',
        value: 'Asia/Shanghai'
      }
    ]
  },

  service: {
    name: 'hsystem-frontend-service',
    type: 'ClusterIP',
    ports: [
      {
        name: 'http',
        port: 80,
        targetPort: 'http',
        protocol: 'TCP'
      }
    ]
  },

  ingress: {
    name: 'hsystem-frontend-ingress',
    className: 'nginx',
    hosts: [
      {
        host: 'hsystem.com',
        paths: [
          {
            path: '/',
            pathType: 'Prefix'
          }
        ]
      }
    ],
    tls: [
      {
        secretName: 'hsystem-tls',
        hosts: ['hsystem.com']
      }
    ]
  }
}

// CDN配置
const cdnConfig = {
  provider: 'aliyun', // 阿里云CDN
  domain: 'cdn.hsystem.com',
  bucket: 'hsystem-static',
  region: 'oss-cn-hangzhou',
  accessKeyId: process.env.OSS_ACCESS_KEY_ID,
  accessKeySecret: process.env.OSS_ACCESS_KEY_SECRET,
  
  // 上传配置
  upload: {
    include: ['**/*.js', '**/*.css', '**/*.png', '**/*.jpg', '**/*.svg'],
    exclude: ['**/index.html'],
    gzip: true,
    cache: {
      '**/*.js': 'max-age=31536000', // 1年
      '**/*.css': 'max-age=31536000', // 1年
      '**/*.png': 'max-age=2592000', // 30天
      '**/*.jpg': 'max-age=2592000', // 30天
      '**/*.svg': 'max-age=2592000'  // 30天
    }
  },

  // 刷新配置
  refresh: {
    urls: [
      'https://cdn.hsystem.com/',
      'https://cdn.hsystem.com/assets/'
    ],
    dirs: [
      'https://cdn.hsystem.com/assets/'
    ]
  }
}

// 监控配置
const monitorConfig = {
  // 性能监控
  performance: {
    enabled: true,
    endpoint: 'https://monitor.hsystem.com/api/performance',
    sampleRate: 0.1 // 10%采样率
  },

  // 错误监控
  error: {
    enabled: true,
    endpoint: 'https://monitor.hsystem.com/api/errors',
    ignoreErrors: [
      'Script error',
      'Network Error',
      'ChunkLoadError'
    ]
  },

  // 用户行为监控
  behavior: {
    enabled: true,
    endpoint: 'https://monitor.hsystem.com/api/behavior',
    events: ['click', 'scroll', 'resize']
  }
}

module.exports = {
  deployConfig,
  dockerConfig,
  k8sConfig,
  cdnConfig,
  monitorConfig
}
