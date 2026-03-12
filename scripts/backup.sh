#!/bin/bash

# ============================================================
# AIForum 数据备份脚本
# 用途：自动备份MySQL数据库和上传文件
# 使用：./backup.sh
# 定时任务：每天凌晨2点执行
#   crontab -e
#   0 2 * * * /opt/aiforum/scripts/backup.sh >> /var/log/aiforum_backup.log 2>&1
# ============================================================

set -e

# ==================== 配置区域 ====================

# 备份目录
BACKUP_DIR="/opt/backup/aiforum"

# 项目目录
PROJECT_DIR="/opt/aiforum"

# 环境变量文件
ENV_FILE="${PROJECT_DIR}/.env.prod"

# 保留天数
RETENTION_DAYS=7

# 日期时间戳
DATE=$(date +%Y%m%d_%H%M%S)
DATE_ONLY=$(date +%Y%m%d)

# 日志文件
LOG_FILE="/var/log/aiforum_backup.log"

# ==================== 函数定义 ====================

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

error_exit() {
    log "错误: $1"
    exit 1
}

# 从.env文件读取变量
read_env_var() {
    local var_name=$1
    local var_value=$(grep "^${var_name}=" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2-)
    echo "$var_value"
}

# 检查命令是否存在
check_command() {
    if ! command -v "$1" &> /dev/null; then
        error_exit "命令 $1 未找到，请先安装"
    fi
}

# 清理旧备份
cleanup_old_backups() {
    log "清理 ${RETENTION_DAYS} 天前的旧备份..."
    find "$BACKUP_DIR" -name "*.sql.gz" -mtime +${RETENTION_DAYS} -type f -delete 2>/dev/null || true
    find "$BACKUP_DIR" -name "*.tar.gz" -mtime +${RETENTION_DAYS} -type f -delete 2>/dev/null || true
    log "旧备份清理完成"
}

# ==================== 主程序 ====================

log "=========================================="
log "AIForum 数据备份开始"
log "=========================================="

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 读取数据库配置
MYSQL_ROOT_PASSWORD=$(read_env_var "MYSQL_ROOT_PASSWORD")
MYSQL_USER=$(read_env_var "MYSQL_USER")
MYSQL_PASSWORD=$(read_env_var "MYSQL_PASSWORD")

if [ -z "$MYSQL_ROOT_PASSWORD" ]; then
    error_exit "无法读取MYSQL_ROOT_PASSWORD，请检查.env.prod文件"
fi

# ==================== 备份MySQL数据库 ====================

log "开始备份MySQL数据库..."

DB_BACKUP_FILE="${BACKUP_DIR}/db_backup_${DATE}.sql"

# 使用docker exec在容器内执行mysqldump
docker exec aiforum-mysql mysqldump \
    -u root \
    -p"${MYSQL_ROOT_PASSWORD}" \
    --single-transaction \
    --routines \
    --triggers \
    --events \
    aiforum > "$DB_BACKUP_FILE" 2>/dev/null

if [ $? -eq 0 ] && [ -s "$DB_BACKUP_FILE" ]; then
    # 压缩备份文件
    gzip "$DB_BACKUP_FILE"
    DB_BACKUP_SIZE=$(du -h "${DB_BACKUP_FILE}.gz" | cut -f1)
    log "数据库备份成功: ${DB_BACKUP_FILE}.gz (${DB_BACKUP_SIZE})"
else
    rm -f "$DB_BACKUP_FILE"
    log "警告: 数据库备份失败，跳过"
fi

# ==================== 备份上传文件 ====================

log "开始备份上传文件..."

UPLOADS_DIR="${PROJECT_DIR}/uploads"
UPLOADS_BACKUP_FILE="${BACKUP_DIR}/uploads_backup_${DATE}.tar.gz"

if [ -d "$UPLOADS_DIR" ]; then
    # 检查是否有文件需要备份
    FILE_COUNT=$(find "$UPLOADS_DIR" -type f | wc -l)
    
    if [ "$FILE_COUNT" -gt 0 ]; then
        tar -czf "$UPLOADS_BACKUP_FILE" -C "$PROJECT_DIR" uploads/ 2>/dev/null
        
        if [ $? -eq 0 ]; then
            UPLOADS_BACKUP_SIZE=$(du -h "$UPLOADS_BACKUP_FILE" | cut -f1)
            log "文件备份成功: ${UPLOADS_BACKUP_FILE} (${UPLOADS_BACKUP_SIZE})"
        else
            rm -f "$UPLOADS_BACKUP_FILE"
            log "警告: 文件备份失败"
        fi
    else
        log "上传目录为空，跳过文件备份"
    fi
else
    log "警告: 上传目录不存在，跳过文件备份"
fi

# ==================== 备份向量数据库 ====================

log "开始备份向量数据库..."

VECTOR_DIR="${PROJECT_DIR}/backend/data"
VECTOR_BACKUP_FILE="${BACKUP_DIR}/vector_backup_${DATE}.tar.gz"

if [ -d "$VECTOR_DIR" ]; then
    # 检查是否有向量索引文件
    if ls ${VECTOR_DIR}/*.faiss 1> /dev/null 2>&1; then
        tar -czf "$VECTOR_BACKUP_FILE" -C "${PROJECT_DIR}/backend" data/ 2>/dev/null
        
        if [ $? -eq 0 ]; then
            VECTOR_BACKUP_SIZE=$(du -h "$VECTOR_BACKUP_FILE" | cut -f1)
            log "向量数据库备份成功: ${VECTOR_BACKUP_FILE} (${VECTOR_BACKUP_SIZE})"
        else
            rm -f "$VECTOR_BACKUP_FILE"
            log "警告: 向量数据库备份失败"
        fi
    else
        log "向量索引文件不存在，跳过备份"
    fi
else
    log "向量数据库目录不存在，跳过备份"
fi

# ==================== 清理旧备份 ====================

cleanup_old_backups

# ==================== 备份统计 ====================

log "=========================================="
log "备份统计:"
log "  - 备份目录: ${BACKUP_DIR}"
log "  - 保留天数: ${RETENTION_DAYS} 天"
log "  - 当前备份数量: $(ls -1 ${BACKUP_DIR}/*.gz 2>/dev/null | wc -l)"
log "  - 当前备份大小: $(du -sh ${BACKUP_DIR} 2>/dev/null | cut -f1)"
log "=========================================="
log "AIForum 数据备份完成"
log "=========================================="

exit 0
