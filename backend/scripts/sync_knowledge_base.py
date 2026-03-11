#!/usr/bin/env python3
"""知识库全量同步脚本 - 修正环境变量加载"""

import sys
import os
from pathlib import Path

# 第一步：加载环境变量（在导入其他模块之前！）
env_path = Path(__file__).parent.parent.parent / '.env'
print(f"正在加载环境变量: {env_path}")
from dotenv import load_dotenv
load_dotenv(env_path)
print("环境变量加载完成")
print(f"ZHIPU_API_KEY_1: {os.getenv('ZHIPU_API_KEY_1', 'NOT FOUND')[:20]}...")

# 第二步：添加路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 第三步：导入其他模块
import asyncio
import logging
from app.core.database import init_db, close_db
from app.services.knowledge_base import knowledge_base_service

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    print("=" * 60)
    print("知识库全量同步")
    print("=" * 60)
    print()
    
    await init_db()
    
    try:
        count = await knowledge_base_service.sync_all()
        
        print()
        print("=" * 60)
        print(f"同步完成！共处理 {count} 条向量")
        print("=" * 60)
        
    except Exception as e:
        print(f"同步失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        await close_db()

if __name__ == "__main__":
    asyncio.run(main())
