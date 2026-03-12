#!/bin/bash

# ============================================================
# AIForum 数据恢复脚本
# 用途：从备份文件恢复MySQL数据库和上传文件
# 使用：./restore.sh <备份文件日期>
# 示例：./restore.sh 20260311_020000
# ============================================================

set -e

# ==================== 配置区域 ====================

BACKUP_DIR="/opt/backup/aiforum"
PROJECT_DIR="/opt/aiforum"
ENV_FILE="${PROJECT_DIR}/.env.prod"

# ==================== 函数定义 ====================

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

error_exit() {
    log "错误: $1"
    exit 1
}

read_env_var() {
    local var_name=$1
    local var_value=$(grep "^${var_name}=" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2-)
    echo "$var_value"
}

# ==================== 参数检查 ====================

if [ -z "$1" ]; then
    echo "用法: $0 <备份日期时间戳>"
    echo ""
    echo "可用的备份文件:"
    echo ""
    echo "数据库备份:"
    ls -lh ${BACKUP_DIR}/db_backup_*.sql.gz 2>/dev/null | awk '{print "  " $NF " (" $5 ")"}' || echo "  无"
    echo ""
    echo "文件备份:"
    ls -lh ${BACKUP_DIR}/uploads_backup_*.tar.gz 2>/dev/null | awk '{print "  " $NF " (" $5 ")"}' || echo "  无"
    echo ""
    echo "示例: $0 20260311_020000"
    exit 1
fi

BACKUP_DATE=$1

# ==================== 主程序 ====================

log "=========================================="
log "AIForum 数据恢复开始"
log "=========================================="

# 读取数据库配置
MYSQL_ROOT_PASSWORD=$(read_env_var "MYSQL_ROOT_PASSWORD")

if [ -z "$MYSQL_ROOT_PASSWORD" ]; then
    error_exit "无法读取MYSQL_ROOT_PASSWORD，请检查.env.prod文件"
fi

# ==================== 恢复MySQL数据库 ====================

DB_BACKUP_FILE="${BACKUP_DIR}/db_backup_${BACKUP_DATE}.sql.gz"

if [ -f "$DB_BACKUP_FILE" ]; then
    log "找到数据库备份文件: ${DB_BACKUP_FILE}"
    
    # 解压
    log "解压数据库备份文件..."
    gunzip -c "$DB_BACKUP_FILE" > /tmp/restore_db.sql
    
    # 恢复
    log "恢复数据库..."
    docker exec -i aiforum-mysql mysql \
        -u root \
        -p"${MYSQL_ROOT_PASSWORD}" \
        aiforum < /tmp/restore_db.sql 2>/dev/null
    
    # 清理临时文件
    rm -f /tmp/restore_db.sql
    
    log "数据库恢复成功!"
else
    log "警告: 未找到数据库备份文件 ${DB_BACKUP_FILE}"
fi

# ==================== 恢复上传文件 ====================

UPLOADS_BACKUP_FILE="${BACKUP_DIR}/uploads_backup_${BACKUP_DATE}.tar.gz"

if [ -f "$UPLOADS_BACKUP_FILE" ]; then
    log "找到文件备份: ${UPLOADS_BACKUP_FILE}"
    
    # 解压恢复
    log "恢复上传文件..."
    tar -xzf "$UPLOADS_BACKUP_FILE" -C "$PROJECT_DIR"
    
    log "上传文件恢复成功!"
else
    log "警告: 未找到文件备份 ${UPLOADS_BACKUP_FILE}"
fi

# ==================== 恢复向量数据库 ====================

VECTOR_BACKUP_FILE="${BACKUP_DIR}/vector_backup_${BACKUP_DATE}.tar.gz"

if [ -f "$VECTOR_BACKUP_FILE" ]; then
    log "找到向量数据库备份: ${VECTOR_BACKUP_FILE}"
    
    # 解压恢复
    log "恢复向量数据库..."
    tar -xzf "$VECTOR_BACKUP_FILE" -C "${PROJECT_DIR}/backend"
    
    log "向量数据库恢复成功!"
else
    log "警告: 未找到向量数据库备份 ${VECTOR_BACKUP_FILE}"
fi

log "=========================================="
log "AIForum 数据恢复完成"
log "=========================================="
log ""
log "建议: 重启后端服务以确保数据生效"
log "  docker compose -f docker-compose.prod.yml restart backend"

exit 0
