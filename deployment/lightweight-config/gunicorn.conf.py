# Gunicorn轻量化配置 - 适用于蜜罐主机
# 内存占用: ~50-100MB (相比Uvicorn更稳定)
# CPU占用: 低

import multiprocessing
import os

# 服务器配置
bind = "127.0.0.1:8000"
backlog = 512  # 降低backlog以节省内存

# 工作进程配置 - 根据资源情况调整
workers = min(2, multiprocessing.cpu_count())  # 最多2个worker
worker_class = "uvicorn.workers.UvicornWorker"  # 使用异步worker
worker_connections = 100  # 每个worker的连接数
max_requests = 1000  # 防止内存泄漏
max_requests_jitter = 100

# 内存和超时配置
timeout = 30
keepalive = 2
worker_tmp_dir = "/dev/shm"  # 使用内存文件系统

# 日志配置
loglevel = "warning"  # 减少日志输出
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'
accesslog = "/var/log/hsystem/access.log"
errorlog = "/var/log/hsystem/error.log"

# 进程管理
preload_app = True  # 预加载应用以节省内存
daemon = False
pidfile = "/var/run/hsystem/gunicorn.pid"
user = "hsystem"
group = "hsystem"

# 性能优化
worker_tmp_dir = "/dev/shm"
tmp_upload_dir = "/tmp"

# 环境变量
raw_env = [
    "PYTHONPATH=/opt/hsystem/backend",
    "ENVIRONMENT=production"
]

# 钩子函数 - 用于监控和优化
def when_ready(server):
    """服务器启动完成时的回调"""
    server.log.info("H-System EDR Backend Server is ready")

def worker_int(worker):
    """Worker进程中断时的回调"""
    worker.log.info("Worker received INT or QUIT signal")

def pre_fork(server, worker):
    """Fork worker前的回调"""
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_fork(server, worker):
    """Fork worker后的回调"""
    server.log.info("Worker spawned (pid: %s)", worker.pid)
    
    # 设置进程标题
    import setproctitle
    setproctitle.setproctitle(f"hsystem-worker-{worker.age}")

def worker_abort(worker):
    """Worker异常退出时的回调"""
    worker.log.info("Worker received SIGABRT signal")
