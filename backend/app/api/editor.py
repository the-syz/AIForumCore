from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request
from typing import Optional
from app.api.auth import get_current_user, oauth2_scheme
from app.models.user import User
from app.services.files import FileService
from app.core.security import decode_access_token
import json

router = APIRouter(prefix="/editor", tags=["富文本编辑器"])
file_service = FileService()

# @router.post("/upload", status_code=status.HTTP_200_OK)
# def upload_image(
#     file: UploadFile = File(...),
#     current_user: User = Depends(get_current_user)
# ):
#     """上传图片到服务器"""
#     try:
#         # 验证文件类型
#         if not file_service.validate_file(file, file_type='editor'):
#             raise HTTPException(status_code=400, detail="文件类型不支持")
#         
#         # 保存文件
#         file_path = file_service.save_file(file, "editor")
#         
#         # 构建文件URL
#         file_url = f"/uploads/editor/{file_path.split('/')[-1]}"
#         
#         # 返回UEditor需要的格式
#         return {
#             "state": "SUCCESS",
#             "url": file_url,
#             "title": file.filename,
#             "original": file.filename
#         }
#     except HTTPException:
#         raise
#     except Exception as e:
#         print(f"上传图片失败，错误: {str(e)}")
#         return {
#             "state": "ERROR",
#             "url": "",
#             "title": "",
#             "original": ""
#         }

@router.get("/config", status_code=status.HTTP_200_OK)
async def get_editor_config(request: Request):
    """获取编辑器配置"""
    action = request.query_params.get("action")
    print(f"收到GET请求: action={action}")
    print(f"Request headers: {dict(request.headers)}")
    
    # 如果有action参数，处理相应的操作
    if action and action != "config":
        return await handle_editor_action(request, action, None)
    
    config = {
        "imageActionName": "image",
        "imageFieldName": "file",
        "imageMaxSize": 2048000,
        "imageAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],
        "imageCompressEnable": True,
        "imageCompressBorder": 1600,
        "imageInsertAlign": "none",
        "imageUrlPrefix": "",
        "imagePathFormat": "/uploads/editor/{yyyy}{mm}{dd}/{time}{rand:6}",
        "scrawlActionName": "crawl",
        "scrawlFieldName": "file",
        "scrawlMaxSize": 2048000,
        "scrawlUrlPrefix": "",
        "videoActionName": "video",
        "videoFieldName": "file",
        "videoMaxSize": 102400000,
        "videoAllowFiles": [".mp4"],
        "audioActionName": "audio",
        "audioFieldName": "file",
        "audioMaxSize": 102400000,
        "audioAllowFiles": [".mp3"],
        "fileActionName": "file",
        "fileFieldName": "file",
        "fileMaxSize": 102400000,
        "fileAllowFiles": [".zip", ".pdf", ".doc", ".docx"],
        "imageManagerActionName": "listImage",
        "imageManagerListSize": 20,
        "fileManagerActionName": "listFile",
        "fileManagerListSize": 20
    }
    return config

async def get_current_user_or_none(request: Request) -> Optional[User]:
    """获取当前用户，如果没有token则返回None"""
    try:
        # 从请求头中获取token
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None
        
        # 检查Authorization头格式
        if not auth_header.startswith("Bearer "):
            return None
        
        token = auth_header[7:]  # 去掉"Bearer "前缀
        payload = decode_access_token(token)
        if payload is None:
            return None
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        user = await User.get_or_none(id=int(user_id))
        return user
    except Exception:
        return None

async def handle_editor_action(request: Request, action: str, file: Optional[UploadFile]):
    """处理编辑器操作"""
    # 尝试获取当前用户
    current_user = await get_current_user_or_none(request)
    print(f"收到编辑器操作请求: action={action}, file={file}, current_user={current_user}")
    
    if action == "image" and file:
        try:
            # 验证文件类型
            if not file_service.validate_file(file, file_type='editor'):
                return {
                    "state": "ERROR",
                    "url": "",
                    "title": "",
                    "original": ""
                }
            
            # 保存文件
            result = file_service.save_file(file, "editor")
            file_path = result["path"]
            file_name = result["name"]
            
            # 构建文件URL - 使用完整路径
            file_url = f"/{file_path}"
            
            # 检查文件是否真的保存成功
            import os
            full_path = os.path.join(os.getcwd(), file_path)
            print(f"文件保存路径: {full_path}")
            print(f"文件是否存在: {os.path.exists(full_path)}")
            print(f"文件大小: {os.path.getsize(full_path) if os.path.exists(full_path) else 0} bytes")
            
            # 返回UEditor需要的格式
            return {
                "state": "SUCCESS",
                "url": file_url,
                "title": file_name,
                "original": file_name
            }
        except Exception as e:
            print(f"上传图片失败，错误: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "state": "ERROR",
                "url": "",
                "title": "",
                "original": ""
            }
    elif action == "listImage":
        return {
            "state": "SUCCESS",
            "list": [],
            "start": 0,
            "total": 0
        }
    elif action == "listFile":
        return {
            "state": "SUCCESS",
            "list": [],
            "start": 0,
            "total": 0
        }
    elif action == "video" or action == "audio" or action == "file" or action == "crawl" or action == "catch":
        return {
            "state": "SUCCESS",
            "url": ""
        }
    return {"state": "ERROR"}

@router.post("/config", status_code=status.HTTP_200_OK)
async def handle_editor_action_post(
    request: Request,
    file: Optional[UploadFile] = File(None)
):
    """处理编辑器POST操作"""
    action = request.query_params.get("action")
    print(f"收到POST请求: action={action}")
    return await handle_editor_action(request, action, file)

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
