from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from typing import List, Optional
import os
from app.api.auth import get_current_user, get_current_admin
from app.models.user import User
from app.models.download import Download
from app.schemas.download import DownloadCreate, DownloadUpdate, DownloadResponse
from app.services.files import FileService
from app.services.knowledge_base import knowledge_base_service
from tortoise import Tortoise

router = APIRouter(tags=["下载中心"])
file_service = FileService()

@router.post("/", response_model=DownloadResponse)
async def create_download(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    category: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_admin)
):
    """上传下载资源（仅管理员）"""
    try:
        # 确保Tortoise ORM上下文是激活的
        from app.core.database import ensure_db_initialized
        await ensure_db_initialized()
        
        # 验证文件
        if not file_service.validate_file(file, "attachment"):
            raise HTTPException(status_code=400, detail="文件验证失败：文件类型或大小不符合要求")
        
        # 保存文件
        file_result = file_service.save_file(file, "attachment")
        file_path = file_result["path"]
        file_name = file.filename or "unknown"
        
        # 创建下载资源记录
        download = await Download.create(
            title=title,
            description=description,
            category=category,
            file_path=file_path,
            file_name=file_name,
            uploader=current_user
        )
        
        # 异步添加到知识库（不阻塞主流程）
        import asyncio
        try:
            asyncio.create_task(knowledge_base_service.add_download(download))
            print(f"下载资源已添加到知识库队列: {download.id}")
        except Exception as kb_error:
            print(f"添加下载资源到知识库失败: {kb_error}")
        
        return download
    except HTTPException:
        raise
    except Exception as e:
        print(f"上传下载资源失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"上传下载资源失败: {str(e)}")

@router.get("/", response_model=List[DownloadResponse])
async def list_downloads(
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 20
):
    """获取下载资源列表"""
    try:
        # 确保Tortoise ORM上下文是激活的
        from app.core.database import ensure_db_initialized
        await ensure_db_initialized()
        
        query = Download.all()
        
        if category:
            query = query.filter(category=category)
        
        # 按上传时间倒序排列
        downloads = await query.order_by("-upload_time").offset(skip).limit(limit).all()
        
        return downloads
    except Exception as e:
        print(f"获取下载资源列表失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"获取下载资源列表失败: {str(e)}")

@router.get("/{download_id}", response_model=DownloadResponse)
async def get_download(
    download_id: int
):
    """获取下载资源详情"""
    try:
        # 确保Tortoise ORM上下文是激活的
        from app.core.database import ensure_db_initialized
        await ensure_db_initialized()
        
        download = await Download.get_or_none(id=download_id)
        if not download:
            raise HTTPException(status_code=404, detail="资源不存在")
        
        return download
    except HTTPException:
        raise
    except Exception as e:
        print(f"获取下载资源详情失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"获取下载资源详情失败: {str(e)}")

@router.put("/{download_id}", response_model=DownloadResponse)
async def update_download(
    download_id: int,
    download_data: DownloadUpdate,
    current_user: User = Depends(get_current_admin)
):
    """更新下载资源（仅管理员）"""
    try:
        # 确保Tortoise ORM上下文是激活的
        from app.core.database import ensure_db_initialized
        await ensure_db_initialized()
        
        download = await Download.get_or_none(id=download_id)
        if not download:
            raise HTTPException(status_code=404, detail="资源不存在")
        
        # 更新字段
        for field, value in download_data.dict(exclude_unset=True).items():
            setattr(download, field, value)
        
        await download.save()
        
        # 异步更新知识库
        import asyncio
        try:
            asyncio.create_task(knowledge_base_service.update_download(download))
            print(f"下载资源已更新到知识库队列: {download.id}")
        except Exception as kb_error:
            print(f"更新下载资源到知识库失败: {kb_error}")
        
        return download
    except HTTPException:
        raise
    except Exception as e:
        print(f"更新下载资源失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"更新下载资源失败: {str(e)}")

@router.delete("/{download_id}")
async def delete_download(
    download_id: int,
    current_user: User = Depends(get_current_admin)
):
    """删除下载资源（仅管理员）"""
    try:
        # 确保Tortoise ORM上下文是激活的
        from app.core.database import ensure_db_initialized
        await ensure_db_initialized()
        
        download = await Download.get_or_none(id=download_id)
        if not download:
            raise HTTPException(status_code=404, detail="资源不存在")
        
        # 删除文件
        if os.path.exists(download.file_path):
            try:
                os.remove(download.file_path)
            except Exception as e:
                print(f"删除文件失败: {e}")
        
        # 异步从知识库删除
        import asyncio
        try:
            asyncio.create_task(knowledge_base_service.delete_download(download.id))
            print(f"下载资源已从知识库删除队列: {download.id}")
        except Exception as kb_error:
            print(f"从知识库删除下载资源失败: {kb_error}")
        
        # 删除记录
        await download.delete()
        
        return {"message": "资源删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"删除下载资源失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"删除下载资源失败: {str(e)}")

@router.get("/{download_id}/download")
async def download_file(
    download_id: int
):
    """下载资源文件"""
    try:
        # 确保Tortoise ORM上下文是激活的
        from app.core.database import ensure_db_initialized
        await ensure_db_initialized()
        
        download = await Download.get_or_none(id=download_id)
        if not download:
            raise HTTPException(status_code=404, detail="资源不存在")
        
        # 检查文件是否存在
        if not os.path.exists(download.file_path):
            raise HTTPException(status_code=404, detail="文件不存在")
        
        # 增加下载次数
        download.download_count += 1
        await download.save()
        
        # 返回文件
        return FileResponse(
            path=download.file_path,
            filename=os.path.basename(download.file_path),
            media_type="application/octet-stream"
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"下载资源文件失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"下载资源文件失败: {str(e)}")
