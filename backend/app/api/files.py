from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from app.api.auth import get_current_user
from app.models.user import User
from app.services.files import FileService
import os

router = APIRouter(prefix="/upload", tags=["文件上传"])
file_service = FileService()

@router.post("/attachment")
async def upload_attachment(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """上传附件"""
    try:
        print(f"收到文件上传请求: {file.filename}, 类型: {file.content_type}")
        
        if not file_service.validate_file(file, "attachment"):
            print(f"文件验证失败: {file.filename}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="文件类型不支持或文件过大"
            )
        
        print(f"文件验证通过，开始保存: {file.filename}")
        
        result = file_service.save_file(file, "attachment")
        
        print(f"文件保存成功: {result['path']}")
        
        return {
            "file_path": result["path"],
            "file_name": result["name"],
            "file_size": file.size if hasattr(file, 'size') else 0,
            "message": "文件上传成功"
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"上传附件失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"上传附件失败: {str(e)}"
        )

@router.delete("/attachment")
async def delete_attachment(
    file_path: str,
    current_user: User = Depends(get_current_user)
):
    """删除附件"""
    try:
        # 验证文件路径
        if not file_path or not file_path.startswith("uploads/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效的文件路径"
            )
        
        # 删除文件
        if file_service.delete_file(file_path):
            return {"message": "文件删除成功"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文件不存在"
            )
    except HTTPException:
        raise
    except Exception as e:
        print(f"删除附件失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除附件失败: {str(e)}"
        )

@router.get("/download")
async def download_file(
    file_path: str,
    file_name: str = None,
    current_user: User = Depends(get_current_user)
):
    """下载文件"""
    try:
        print(f"原始文件路径: {file_path}")
        file_path = file_path.replace("\\", "/").replace("/", os.sep)
        print(f"转换后路径: {file_path}")
        print(f"当前工作目录: {os.getcwd()}")
        
        if not file_path or not file_path.startswith("uploads" + os.sep):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效的文件路径"
            )
        
        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"文件不存在"
            )
        
        from fastapi.responses import FileResponse
        download_name = file_name if file_name else os.path.basename(file_path)
        return FileResponse(
            path=file_path,
            filename=download_name,
            media_type="application/octet-stream"
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"下载文件失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"下载文件失败: {str(e)}"
        )