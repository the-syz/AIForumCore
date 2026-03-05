# Docker 和 Redis 安装配置指南

## 一、Docker 安装

### 1.1 Windows 系统安装 Docker Desktop

#### 步骤 1：下载 Docker Desktop

1. 访问官网下载页面：https://www.docker.com/products/docker-desktop
2. 点击 "Download for Windows" 按钮下载安装包
3. 或者使用直接下载链接（可能需要登录）：
   - https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe

#### 步骤 2：安装 Docker Desktop

1. 双击下载的 `Docker Desktop Installer.exe`
2. 按照安装向导进行安装：
   - 接受许可协议
   - 选择安装路径（默认即可）
   - 勾选 "Use WSL 2 instead of Hyper-V"（推荐）
   - 点击 "OK" 开始安装
3. 等待安装完成，可能需要重启电脑

#### 步骤 3：验证安装

打开 PowerShell 或 CMD，运行以下命令：

```powershell
# 检查 Docker 版本
docker --version

# 检查 Docker Compose 版本
docker-compose --version

# 运行测试容器
docker run hello-world
```

如果看到 "Hello from Docker!" 的欢迎信息，说明安装成功。

#### 步骤 4：配置 Docker

1. 打开 Docker Desktop 应用
2. 点击设置（Settings）图标
3. 推荐配置：
   - **General**: 勾选 "Start Docker Desktop when you log in"
   - **Resources**: 
     - CPUs: 至少 2 核
     - Memory: 至少 4GB
     - Disk: 至少 20GB
   - **Docker Engine**: 可以配置镜像加速（见下文）

#### 步骤 5：配置镜像加速（推荐）

由于国内网络原因，建议配置镜像加速：

1. 打开 Docker Desktop 设置
2. 选择 "Docker Engine"
3. 在 JSON 配置中添加：

```json
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com"
  ]
}
```

4. 点击 "Apply & Restart"

---

## 二、Redis 安装

### 2.1 使用 Docker 安装 Redis（推荐）

这是最简单的方式，无需单独安装 Redis：

```powershell
# 拉取 Redis 镜像
docker pull redis:6

# 运行 Redis 容器
docker run -d --name redis -p 6379:6379 redis:6

# 验证 Redis 是否运行
docker ps

# 测试 Redis 连接
docker exec -it redis redis-cli ping
```

如果返回 `PONG`，说明 Redis 运行正常。

#### 持久化配置（可选）

```powershell
# 创建本地目录用于持久化
mkdir f:\AIForumCore\redis-data

# 运行带持久化的 Redis
docker run -d --name redis \
  -p 6379:6379 \
  -v f:\AIForumCore\redis-data:/data \
  redis:6 redis-server --appendonly yes
```

### 2.2 Windows 本地安装 Redis（备选）

#### 步骤 1：下载 Redis

1. 访问：https://github.com/microsoftarchive/redis/releases
2. 下载 `Redis-x64-xxx.msi` 安装包
3. 或者下载 ZIP 版本解压使用

#### 步骤 2：安装 Redis

**MSI 安装方式：**
1. 双击 MSI 文件
2. 按照向导安装
3. 勾选 "Add to PATH"

**ZIP 解压方式：**
1. 解压到 `C:\Redis` 目录
2. 将 `C:\Redis` 添加到系统环境变量 PATH

#### 步骤 3：启动 Redis

```powershell
# 启动 Redis 服务
redis-server.exe

# 或者作为 Windows 服务安装
redis-server.exe --service-install
redis-server.exe --service-start
```

#### 步骤 4：验证安装

```powershell
# 连接 Redis
redis-cli.exe

# 测试
127.0.0.1:6379> ping
PONG

# 退出
127.0.0.1:6379> exit
```

---

## 三、Docker Compose 配置（项目使用）

在你的项目根目录创建 `docker-compose.yml` 文件：

```yaml
version: '3.8'

services:
  # MySQL 数据库
  db:
    image: mysql:8.0
    container_name: aiforum-mysql
    environment:
      MYSQL_ROOT_PASSWORD: your_password
      MYSQL_DATABASE: aiforum
      MYSQL_USER: aiforum
      MYSQL_PASSWORD: your_password
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"
    command: --default-authentication-plugin=mysql_native_password

  # Redis 缓存
  redis:
    image: redis:6
    container_name: aiforum-redis
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes

  # 后端服务
  backend:
    build: ./backend
    container_name: aiforum-backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql+pymysql://aiforum:your_password@db:3306/aiforum
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=your-secret-key-here
      - ZHIPU_API_KEY_1=your-api-key-1
      - ZHIPU_API_KEY_2=your-api-key-2
      - ZHIPU_API_KEY_3=your-api-key-3
      - ZHIPU_API_KEY_4=your-api-key-4
      - ZHIPU_API_KEY_5=your-api-key-5
    depends_on:
      - db
      - redis
    volumes:
      - ./uploads:/app/uploads

  # 前端服务
  frontend:
    build: ./frontend
    container_name: aiforum-frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  mysql_data:
  redis_data:
```

---

## 四、常用 Docker 命令

```powershell
# 查看运行中的容器
docker ps

# 查看所有容器（包括停止的）
docker ps -a

# 启动容器
docker start 容器名

# 停止容器
docker stop 容器名

# 重启容器
docker restart 容器名

# 删除容器
docker rm 容器名

# 查看容器日志
docker logs 容器名

# 进入容器内部
docker exec -it 容器名 /bin/bash

# 使用 Docker Compose 启动所有服务
docker-compose up -d

# 停止所有服务
docker-compose down

# 查看服务状态
docker-compose ps

# 查看服务日志
docker-compose logs -f

# 重新构建并启动
docker-compose up -d --build
```

---

## 五、常见问题解决

### 5.1 Docker 启动失败

**问题**：Docker Desktop 无法启动，提示 "WSL 2 installation is incomplete"

**解决**：
```powershell
# 安装 WSL 2
wsl --install

# 或者手动下载 Linux 内核更新包
# https://docs.microsoft.com/windows/wsl/wsl2-kernel
```

### 5.2 端口被占用

**问题**：Redis 启动失败，提示端口 6379 被占用

**解决**：
```powershell
# 查找占用端口的进程
netstat -ano | findstr :6379

# 结束进程（将 <PID> 替换为实际的进程ID）
taskkill /PID <PID> /F
```

### 5.3 内存不足

**问题**：Docker 运行缓慢或容器崩溃

**解决**：
1. 打开 Docker Desktop 设置
2. 增加 Resources -> Memory 到 4GB 或更高
3. 重启 Docker Desktop

### 5.4 防火墙阻止

**问题**：无法连接到 Redis 或 MySQL

**解决**：
1. 打开 Windows 防火墙设置
2. 添加允许规则：
   - 端口 6379 (Redis)
   - 端口 3306 (MySQL)
   - 端口 8000 (后端)
   - 端口 80 (前端)

---

## 六、验证安装

创建一个测试脚本来验证环境：

```powershell
# test-environment.ps1

Write-Host "=== 环境检查 ===" -ForegroundColor Green

# 检查 Docker
Write-Host "`n检查 Docker..." -ForegroundColor Yellow
docker --version
docker-compose --version

# 检查 Redis (Docker 方式)
Write-Host "`n检查 Redis (Docker)..." -ForegroundColor Yellow
docker run --rm redis:6 redis-server --version

# 检查端口
Write-Host "`n检查端口占用..." -ForegroundColor Yellow
$ports = @(6379, 3306, 8000, 80)
foreach ($port in $ports) {
    $result = netstat -ano | findstr ":$port"
    if ($result) {
        Write-Host "端口 $port 已被占用" -ForegroundColor Red
    } else {
        Write-Host "端口 $port 可用" -ForegroundColor Green
    }
}

Write-Host "`n=== 检查完成 ===" -ForegroundColor Green
```

运行测试脚本：
```powershell
.\test-environment.ps1
```

---

## 七、下一步

安装完成后，你可以：

1. **启动基础服务**：
   ```powershell
   docker-compose up -d db redis
   ```

2. **验证连接**：
   ```powershell
   # 测试 Redis
   docker exec -it aiforum-redis redis-cli ping
   
   # 测试 MySQL
   docker exec -it aiforum-mysql mysql -u aiforum -p
   ```

3. **开始开发**：
   - 后端开发环境已准备就绪
   - 前端开发环境已准备就绪
   - 数据库和缓存服务已运行

如有问题，请查看 Docker 和 Redis 的官方文档：
- Docker: https://docs.docker.com/
- Redis: https://redis.io/documentation
