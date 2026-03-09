import os
import uuid
from datetime import datetime
from fastapi import UploadFile
import shutil

class FileService:
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = upload_dir
    
    def save_file(self, file: UploadFile, file_type: str) -> dict:
        """保存文件，返回包含路径和原始文件名的字典"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        original_name = file.filename
        ext = os.path.splitext(original_name)[1]
        file_name = f"{timestamp}_{uuid.uuid4().hex[:8]}{ext}"
        
        if file_type == 'paper':
            path = os.path.join(self.upload_dir, "papers", datetime.now().strftime('%Y'), datetime.now().strftime('%m'))
        elif file_type == 'attachment':
            path = os.path.join(self.upload_dir, "attachments", datetime.now().strftime('%Y'), datetime.now().strftime('%m'))
        elif file_type == 'editor':
            path = os.path.join(self.upload_dir, "editor", datetime.now().strftime('%Y'), datetime.now().strftime('%m'))
        else:
            path = os.path.join(self.upload_dir, "temp", timestamp)
        
        os.makedirs(path, exist_ok=True)
        
        file_path = os.path.join(path, file_name)
        
        # 确保文件指针在文件开头
        file.file.seek(0)
        
        with open(file_path, 'wb') as f:
            content = file.file.read()
            f.write(content)
        
        # 验证文件是否保存成功
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"文件保存成功: {file_path}, 大小: {file_size} bytes")
        else:
            print(f"文件保存失败: {file_path}")
        
        return {
            "path": file_path.replace(os.sep, '/'),
            "name": original_name
        }
    
    def validate_file(self, file: UploadFile, file_type: str = '', max_size: int = 50*1024*1024) -> bool:
        """验证文件"""
        # 检查文件大小
        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)
        
        if size > max_size:
            return False
        
        # 检查文件类型
        if file_type == 'editor':
            # 富文本编辑器允许的文件类型
            allowed_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        elif file_type == 'attachment':
            # 附件允许的文件类型 - 扩大范围
            allowed_extensions = [
                '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                '.txt', '.md', '.zip', '.rar', '.7z',
                '.png', '.jpg', '.jpeg', '.gif', '.bmp',
                '.mp4', '.mp3', '.wav', '.avi'
            ]
        else:
            # 其他文件类型 - 允许所有常见格式
            allowed_extensions = [
                '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                '.txt', '.md', '.zip', '.rar', '.7z',
                '.png', '.jpg', '.jpeg', '.gif', '.bmp',
                '.mp4', '.mp3', '.wav', '.avi'
            ]
        
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in allowed_extensions:
            return False
        
        return True
    
    def delete_file(self, file_path: str) -> bool:
        """删除文件"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"删除文件错误: {e}")
            return False
    
    def get_file_path(self, file_name: str, file_type: str) -> str:
        """获取文件路径"""
        # 这里需要根据实际存储结构实现
        # 暂时返回一个示例路径
        return f"{self.upload_dir}/{file_type}s/{file_name}"
