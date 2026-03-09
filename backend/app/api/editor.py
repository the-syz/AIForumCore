from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import Optional
from app.api.auth import get_current_user
from app.models.user import User
from app.services.files import FileService
import json

router = APIRouter(prefix="/editor", tags=["富文本编辑器"])
file_service = FileService()

@router.post("/upload", status_code=status.HTTP_200_OK)
def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """上传图片到服务器"""
    try:
        # 验证文件类型
        if not file_service.validate_file(file, file_type='editor'):
            raise HTTPException(status_code=400, detail="文件类型不支持")
        
        # 保存文件
        file_path = file_service.save_file(file, "editor")
        
        # 构建文件URL
        file_url = f"/uploads/editor/{file_path.split('/')[-1]}"
        
        # 返回UEditor需要的格式
        return {
            "state": "SUCCESS",
            "url": file_url,
            "title": file.filename,
            "original": file.filename
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"上传图片失败，错误: {str(e)}")
        return {
            "state": "ERROR",
            "url": "",
            "title": "",
            "original": ""
        }

@router.get("/config", status_code=status.HTTP_200_OK)
def get_editor_config():
    """获取编辑器配置"""
    config = {
        "imageActionName": "upload",
        "imageFieldName": "file",
        "imageMaxSize": 2048000,
        "imageAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],
        "imageCompressEnable": True,
        "imageCompressBorder": 1600,
        "imageInsertAlign": "none",
        "imageUrlPrefix": "",
        "imagePathFormat": "/uploads/editor/{yyyy}{mm}{dd}/{time}{rand:6}"
    }
    return config

@router.post("/content", status_code=status.HTTP_200_OK)
def save_content(
    content: str,
    current_user: User = Depends(get_current_user)
):
    """保存富文本内容"""
    try:
        # 这里可以添加内容保存逻辑，比如存储到数据库
        # 暂时只返回成功信息
        return {"status": "success", "message": "内容保存成功"}
    except Exception as e:
        print(f"保存内容失败，错误: {str(e)}")
        raise HTTPException(status_code=500, detail="保存内容失败")

@router.get("/content/{content_id}", status_code=status.HTTP_200_OK)
def get_content(
    content_id: str,
    current_user: User = Depends(get_current_user)
):
    """获取富文本内容"""
    try:
        # 这里可以添加内容获取逻辑，比如从数据库读取
        # 暂时返回示例内容
        return {"status": "success", "content": "<p>示例内容</p>"}
    except Exception as e:
        print(f"获取内容失败，错误: {str(e)}")
        raise HTTPException(status_code=500, detail="获取内容失败")
