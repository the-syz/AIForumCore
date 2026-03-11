from typing import List, Dict, Any, Optional
from app.services.vector_db import vector_db
from app.services.embedding import embedding_service
from app.services.api_key_manager import api_key_rotator
from zhipuai import ZhipuAI
import logging

logger = logging.getLogger(__name__)

class RAGService:
    """RAG检索增强生成服务"""
    
    def __init__(self):
        self.model = "glm-4-flash"
        self.max_context_length = 3000
    
    def search_knowledge_base(self, query: str, top_k: int = 3, selected_contents: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """搜索知识库
        
        Args:
            query: 查询字符串
            top_k: 返回结果数量
            selected_contents: 选中的内容列表，用于限定搜索范围 [{type, id}]
        """
        logger.info(f"搜索知识库，查询: {query}")
        logger.info(f"当前向量库数量: {vector_db.index.ntotal if vector_db._index else 0}")
        
        if selected_contents and len(selected_contents) > 0:
            logger.info(f"限定搜索范围: {selected_contents}")
            return self._search_in_selected_contents(query, selected_contents)
        
        query_embedding = embedding_service.get_embedding(query)
        results = vector_db.search(query_embedding, top_k=top_k)
        
        logger.info(f"检索到 {len(results)} 个相关文档")
        for i, doc in enumerate(results):
            logger.info(f"  [{i+1}] {doc.get('type')} - {doc.get('title')} (相似度: {doc.get('score'):.4f})")
        
        return results
    
    def _search_in_selected_contents(self, query: str, selected_contents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """在选中的内容中搜索"""
        query_embedding = embedding_service.get_embedding(query)
        
        # 获取所有向量并筛选
        all_results = []
        for idx, metadata in vector_db.metadata.items():
            for selected in selected_contents:
                if (metadata.get('type') == selected.get('type') and 
                    metadata.get('id') == selected.get('id')):
                    # 计算相似度
                    vector = vector_db.index.reconstruct(int(idx))
                    score = self._cosine_similarity(query_embedding, vector)
                    result = metadata.copy()
                    result['score'] = float(score)
                    all_results.append(result)
                    break
        
        # 按相似度排序
        all_results.sort(key=lambda x: x['score'], reverse=True)
        
        logger.info(f"在选中内容中检索到 {len(all_results)} 个相关文档")
        for i, doc in enumerate(all_results[:5]):
            logger.info(f"  [{i+1}] {doc.get('type')} - {doc.get('title')} (相似度: {doc.get('score'):.4f})")
        
        return all_results[:5]
    
    def _cosine_similarity(self, a: Any, b: Any) -> float:
        """计算余弦相似度"""
        import numpy as np
        a = np.array(a).flatten()
        b = np.array(b).flatten()
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    def build_prompt(self, query: str, context: List[Dict[str, Any]], selected_mode: bool = False) -> str:
        """构建Prompt"""
        if not context:
            if selected_mode:
                prompt = f"""你是AIForum的智能助手，专门帮助课题组同学解答学术问题。

用户问题：{query}

用户选择了特定文章进行提问，但这些文章中没有找到与问题直接相关的内容。请基于这些文章的内容和你的知识回答。如果文章中没有相关信息，请明确说明。"""
            else:
                prompt = f"""你是AIForum的智能助手，专门帮助课题组同学解答学术问题。

用户问题：{query}

目前知识库中没有找到相关资料，请基于你的知识回答。如果问题与本论坛无关，请建议用户咨询论坛中的论文或经验贴。"""
            return prompt
        
        context_text = ""
        for i, item in enumerate(context, 1):
            doc_type = item.get('type', 'unknown')
            title = item.get('title', '未知标题')
            content = item.get('content', '')[:800]
            score = item.get('score', 0)
            context_text += f"[{i}] 【{doc_type}】{title} (相似度: {score:.2f})\n内容: {content}\n\n"
        
        selected_hint = "【限定模式】用户已选择特定文章，请主要基于以下选定资料回答：\n\n" if selected_mode else ""
        
        prompt = f"""你是AIForum的智能助手，专门帮助课题组同学解答学术问题。

{selected_hint}【重要】请务必参考以下资料回答问题，并在回答中明确引用：

{context_text}

用户问题：{query}

【回答要求】
1. 必须基于以上参考资料回答，不要编造信息
2. 每引用一个资料，请在回答中标注：[引用自：资料标题]
3. 如果资料中没有相关信息，请说明"知识库中暂未找到相关内容"
4. 回答要专业、简洁、准确

现在开始回答："""
        
        return prompt
    
    def chat(self, query: str, history: List[Dict[str, str]] = None, selected_contents: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """AI对话
        
        Args:
            query: 用户查询
            history: 历史对话
            selected_contents: 选中的内容列表 [{type, id, title}]
        """
        relevant_docs = self.search_knowledge_base(query, selected_contents=selected_contents)
        selected_mode = selected_contents is not None and len(selected_contents) > 0
        prompt = self.build_prompt(query, relevant_docs, selected_mode=selected_mode)
        
        messages = []
        if history:
            for msg in history:
                messages.append({"role": msg['role'], "content": msg['content']})
        messages.append({"role": "user", "content": prompt})
        
        max_retries = len(api_key_rotator.api_keys)
        for attempt in range(max_retries):
            api_key = api_key_rotator.get_next_key()
            try:
                client = ZhipuAI(api_key=api_key)
                response = client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )
                
                answer = response.choices[0].message.content
                api_key_rotator.record_usage(api_key, success=True)
                
                references = []
                for doc in relevant_docs:
                    references.append({
                        'type': doc.get('type'),
                        'id': doc.get('id'),
                        'title': doc.get('title'),
                        'score': doc.get('score')
                    })
                
                return {
                    'answer': answer,
                    'references': references
                }
                    
            except Exception as e:
                api_key_rotator.record_usage(api_key, success=False)
                if attempt == max_retries - 1:
                    raise e
                continue
        
        raise Exception("AI对话失败")

rag_service = RAGService()
