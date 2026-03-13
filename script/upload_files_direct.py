import sys
import os

# 添加backend目录到Python搜索路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.core.database import init_db, close_db
from app.models.user import User
from app.models.paper import Paper
from app.models.post import Post
from app.services.files import FileService
from app.services.paper_parser import PaperParser
import asyncio

async def upload_paper():
    # 初始化数据库
    await init_db()
    
    try:
        # 获取测试用户
        user = await User.get_or_none(student_id="20240010")
        if not user:
            print("测试用户不存在")
            return
        
        # 论文文件路径
        paper_path = r"f:\AIForumCore\backend\tests\126-Physics-Informed Neural networks for heat transfer problems.pdf"
        
        if not os.path.exists(paper_path):
            print(f"论文文件不存在: {paper_path}")
            return
        
        # 创建文件服务和论文解析器
        file_service = FileService()
        paper_parser = PaperParser()
        
        # 模拟UploadFile对象
        class MockUploadFile:
            def __init__(self, file_path):
                self.filename = os.path.basename(file_path)
                self.file = open(file_path, 'rb')
            
            def close(self):
                self.file.close()
        
        # 创建模拟UploadFile对象
        mock_file = MockUploadFile(paper_path)
        
        # 验证文件
        if not file_service.validate_file(mock_file):
            print("文件类型不支持或文件大小超过限制")
            mock_file.close()
            return
        
        # 保存文件
        file_path = file_service.save_file(mock_file, "paper")
        mock_file.close()
        
        # 解析论文
        metadata = paper_parser.parse(file_path)
        
        # 创建论文记录
        paper = await Paper.create(
            title="Physics-Informed Neural networks for heat transfer problems",
            authors="Unknown",
            category="人工智能",
            file_path=file_path,
            uploader_id=user.id
        )
        
        print(f"论文上传成功！论文ID: {paper.id}")
        return paper
    except Exception as e:
        print(f"上传论文失败，错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        # 关闭数据库连接
        await close_db()

async def upload_post():
    # 初始化数据库
    await init_db()
    
    try:
        # 获取测试用户
        user = await User.get_or_none(student_id="20240010")
        if not user:
            print("测试用户不存在")
            return
        
        # 经验贴文件路径
        post_path = r"f:\AIForumCore\backend\tests\vscode配置latex教程.md"
        
        if not os.path.exists(post_path):
            print(f"经验贴文件不存在: {post_path}")
            return
        
        # 读取文件内容
        with open(post_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 创建文件服务
        file_service = FileService()
        
        # 模拟UploadFile对象
        class MockUploadFile:
            def __init__(self, file_path):
                self.filename = os.path.basename(file_path)
                self.file = open(file_path, 'rb')
            
            def close(self):
                self.file.close()
        
        # 处理附件
        attachments = []
        mock_file = MockUploadFile(post_path)
        if file_service.validate_file(mock_file):
            file_path = file_service.save_file(mock_file, "attachment")
            attachments.append(file_path)
        mock_file.close()
        
        # 创建经验贴
        post = await Post.create(
            title="VSCode配置LaTeX教程",
            content=content,
            category="工具教程",
            author=user
        )
        
        print(f"经验贴上传成功！经验贴ID: {post.id}")
        return post
    except Exception as e:
        print(f"上传经验贴失败，错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        # 关闭数据库连接
        await close_db()

if __name__ == "__main__":
    # 上传论文
    asyncio.run(upload_paper())
    
    # 上传经验贴
    asyncio.run(upload_post())
