import os
import uuid
from datetime import datetime
from fastapi import UploadFile
import shutil

class FileService:
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = upload_dir
    
    def save_file(self, file: UploadFile, file_type: str) -> str:
        """保存文件"""
        # 生成唯一文件名
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        ext = os.path.splitext(file.filename)[1]
        file_name = f"{timestamp}_{uuid.uuid4().hex[:8]}{ext}"
        
        # 确定存储路径
        if file_type == 'paper':
            path = f"{self.upload_dir}/papers/{datetime.now().strftime('%Y/%m')}"
        elif file_type == 'attachment':
            path = f"{self.upload_dir}/attachments/{datetime.now().strftime('%Y/%m')}"
        else:
            path = f"{self.upload_dir}/temp/{timestamp}"
        
        # 确保目录存在
        os.makedirs(path, exist_ok=True)
        
        # 保存文件
        file_path = os.path.join(path, file_name)
        with open(file_path, 'wb') as f:
            content = file.file.read()
            f.write(content)
        
        return file_path
    
    def validate_file(self, file: UploadFile, max_size: int = 50*1024*1024) -> bool:
        """验证文件"""
        # 检查文件大小
        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)
        
        if size > max_size:
            return False
        
        # 检查文件类型
        allowed_extensions = ['.pdf', '.doc', '.docx', '.md', '.txt']
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
