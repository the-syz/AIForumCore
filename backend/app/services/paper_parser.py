import os
import re
import PyPDF2
from docx import Document
import requests
from zhipuai import ZhipuAI
from app.services.api_key_manager import api_key_rotator

class PaperParser:
    def __init__(self):
        """初始化解析器"""
        self.current_api_key_index = 0
    
    def get_client(self):
        """获取智谱AI客户端"""
        try:
            api_key = api_key_rotator.get_next_key()
            return ZhipuAI(api_key=api_key)
        except Exception as e:
            return None
    
    def parse_with_ai(self, text: str) -> dict:
        """使用AI解析论文信息"""
        client = self.get_client()
        if not client:
            return {}
        
        # 检测文本语言
        is_chinese = any('\u4e00' <= char <= '\u9fff' for char in text[:1000])
        
        # 构建提示词
        if is_chinese:
            prompt = f"""
请从以下论文文本中提取以下信息，并以JSON格式返回：
- title: 论文标题
- authors: 作者列表（逗号分隔）
- abstract: 摘要
- keywords: 关键词（逗号分隔）
- doi: DOI号（如果有）
- paper_type: 论文类型（journal或thesis）

论文文本：
{text[:4000]}
"""
        else:
            prompt = f"""
Please extract the following information from the paper text below and return it in JSON format:
- title: Paper title
- authors: List of authors (comma separated)
- abstract: Abstract
- keywords: Keywords (comma separated)
- doi: DOI number (if any)
- paper_type: Paper type (journal or thesis)

Paper text:
{text[:4000]}
"""
        
        try:
            response = client.chat.completions.create(
                model="glm-4-flash",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in academic paper analysis. Please extract the requested information accurately."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            import json
            metadata = json.loads(response.choices[0].message.content)
            return metadata
        except Exception as e:
            print(f"AI解析错误: {e}")
            return {}
    
    def parse(self, file_path: str) -> dict:
        """解析论文文件"""
        print(f"开始解析文件: {file_path}")
        
        # 提取文本
        text = self.extract_text(file_path)
        print(f"提取的文本长度: {len(text) if text else 0}")
        
        # 如果文本提取失败，尝试OCR
        if not text:
            print("文本提取失败，尝试OCR")
            text = self.ocr_with_free_api(file_path)
        
        # 直接使用AI解析
        print("开始使用AI解析")
        metadata = self.parse_with_ai(text)
        print(f"AI解析结果: {metadata}")
        
        # 如果AI解析失败，使用规则-based方法作为备用
        if not metadata or not metadata.get('title'):
            print("AI解析失败，使用规则方法")
            metadata = {
                'title': self.extract_title(text),
                'authors': self.extract_authors(text),
                'abstract': self.extract_abstract(text),
                'keywords': self.extract_keywords(text),
                'doi': self.extract_doi(text),
                'paper_type': self.determine_paper_type(text)
            }
            print(f"规则解析结果: {metadata}")
        
        return metadata
    
    def extract_text(self, file_path: str) -> str:
        """提取文本内容"""
        if file_path.endswith('.pdf'):
            return self.extract_pdf_text(file_path)
        elif file_path.endswith('.docx'):
            return self.extract_docx_text(file_path)
        return ""
    
    def extract_pdf_text(self, file_path: str) -> str:
        """提取PDF文本"""
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"PDF提取错误: {e}")
            return ""
    
    def extract_docx_text(self, file_path: str) -> str:
        """提取DOCX文本"""
        try:
            doc = Document(file_path)
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text
        except Exception as e:
            print(f"DOCX提取错误: {e}")
            return ""
    
    def ocr_with_free_api(self, file_path: str) -> str:
        """使用Free OCR API进行OCR"""
        api_key = os.getenv('OCR_API_KEY')
        url = "https://api.ocr.space/parse/image"
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {
                    'apikey': api_key,
                    'language': 'eng',
                    'isOverlayRequired': False
                }
                response = requests.post(url, files=files, data=data)
                result = response.json()
                
                if result.get('IsErroredOnProcessing'):
                    return ""
                
                parsed_results = result.get('ParsedResults', [])
                if parsed_results:
                    return parsed_results[0].get('ParsedText', "")
                return ""
        except Exception as e:
            print(f"OCR错误: {e}")
            return ""
    
    def extract_title(self, text: str) -> str:
        """提取标题"""
        lines = text.strip().split('\n')
        for line in lines[:10]:  # 在前10行中查找
            line = line.strip()
            if len(line) > 10 and len(line) < 200:
                return line
        return ""
    
    def extract_authors(self, text: str) -> str:
        """提取作者"""
        lines = text.strip().split('\n')
        for i, line in enumerate(lines[1:10]):  # 在前10行中查找
            line = line.strip()
            if ',' in line or ';' in line or 'and' in line.lower():
                return line
        return ""
    
    def extract_abstract(self, text: str) -> str:
        """提取摘要"""
        abstract_patterns = ['abstract', '摘要']
        text_lower = text.lower()
        
        for pattern in abstract_patterns:
            if pattern in text_lower:
                start_idx = text_lower.find(pattern)
                if start_idx != -1:
                    # 找到摘要开始位置，提取后续内容
                    abstract_start = text[start_idx:]
                    # 找到摘要结束位置（通常是下一个标题）
                    end_patterns = ['introduction', '引言', '1. ', '一、']
                    end_idx = len(abstract_start)
                    for end_pattern in end_patterns:
                        end_pos = abstract_start.lower().find(end_pattern)
                        if end_pos != -1 and end_pos < end_idx:
                            end_idx = end_pos
                    return abstract_start[:end_idx].strip()
        return ""
    
    def extract_keywords(self, text: str) -> str:
        """提取关键词"""
        keywords_patterns = ['keywords', '关键词']
        text_lower = text.lower()
        
        for pattern in keywords_patterns:
            if pattern in text_lower:
                start_idx = text_lower.find(pattern)
                if start_idx != -1:
                    # 找到关键词开始位置，提取后续内容
                    keywords_start = text[start_idx:]
                    # 找到关键词结束位置（通常是下一个段落）
                    end_idx = keywords_start.find('\n\n')
                    if end_idx != -1:
                        return keywords_start[:end_idx].strip()
        return ""
    
    def extract_doi(self, text: str) -> str:
        """提取DOI"""
        doi_pattern = r'10\.\d{4,}/[^\s]+'
        match = re.search(doi_pattern, text)
        return match.group(0) if match else ""
    
    def determine_paper_type(self, text: str) -> str:
        """判断论文类型"""
        if 'DOI' in text or 'doi' in text:
            return 'journal'
        elif '学位论文' in text or 'thesis' in text.lower() or 'dissertation' in text.lower():
            return 'thesis'
        return 'journal'
