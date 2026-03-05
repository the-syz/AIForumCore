# AIForum 课题组学术交流平台

## 开发任务分解清单 - 阶段四：AI功能开发

| 文档信息 | 内容 |
|----------|------|
| 文档版本 | V1.0 |
| 创建日期 | 2026-03-04 |
| 编写人员 | 技术负责人 |

---

## 任务清单概览

| 任务编号 | 任务名称 | 预估工时 | 优先级 |
|----------|----------|----------|--------|
| T4-001 | 向量数据库搭建 | 0.5天 | P1 |
| T4-002 | API Key轮询管理 | 0.5天 | P1 |
| T4-003 | 文本向量化服务 | 0.5天 | P1 |
| T4-004 | RAG检索服务 | 1天 | P1 |
| T4-005 | AI对话API | 1天 | P1 |
| T4-006 | 知识库构建 | 0.5天 | P1 |
| T4-007 | AI对话前端组件 | 1天 | P1 |
| T4-008 | 对话历史管理 | 0.5天 | P2 |

---

## 任务详情

### T4-001: 向量数据库搭建

| 属性 | 内容 |
|------|------|
| **任务编号** | T4-001 |
| **任务名称** | 向量数据库搭建 |
| **预估工时** | 0.5天 |
| **优先级** | P1 |

**任务描述**：
搭建FAISS向量数据库，实现文本向量存储和检索功能。

**具体步骤**：
1. 安装FAISS依赖
2. 创建向量数据库管理类
3. 实现向量添加功能
4. 实现向量搜索功能
5. 实现向量删除功能
6. 实现数据持久化

**核心代码** (`backend/app/services/vector_db.py`)：
```python
import os
import pickle
import numpy as np
import faiss
from typing import List, Dict, Any

class VectorDatabase:
    def __init__(self, dimension: int = 1024, index_path: str = "data/vector_index"):
        self.dimension = dimension
        self.index_path = index_path
        self.index = None
        self.metadata = {}
        self._load_or_create_index()
    
    def _load_or_create_index(self):
        """加载或创建索引"""
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        
        index_file = f"{self.index_path}.faiss"
        metadata_file = f"{self.index_path}.pkl"
        
        if os.path.exists(index_file):
            # 加载已有索引
            self.index = faiss.read_index(index_file)
            with open(metadata_file, 'rb') as f:
                self.metadata = pickle.load(f)
        else:
            # 创建新索引
            self.index = faiss.IndexFlatIP(self.dimension)  # 内积相似度
            self.metadata = {}
    
    def add_vectors(self, vectors: np.ndarray, metadata_list: List[Dict[str, Any]]):
        """添加向量"""
        # 归一化向量
        faiss.normalize_L2(vectors)
        
        # 添加到索引
        start_id = self.index.ntotal
        self.index.add(vectors)
        
        # 保存元数据
        for i, metadata in enumerate(metadata_list):
            self.metadata[start_id + i] = metadata
        
        self._save_index()
    
    def search(self, query_vector: np.ndarray, top_k: int = 3) -> List[Dict[str, Any]]:
        """搜索相似向量"""
        # 归一化查询向量
        query_vector = query_vector.reshape(1, -1)
        faiss.normalize_L2(query_vector)
        
        # 搜索
        scores, indices = self.index.search(query_vector, top_k)
        
        # 返回结果
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1 and idx in self.metadata:
                result = self.metadata[idx].copy()
                result['score'] = float(score)
                results.append(result)
        
        return results
    
    def delete_vector(self, doc_id: str):
        """删除向量（通过重建索引实现）"""
        # FAISS不支持直接删除，需要重建索引
        # 这里简化处理，实际生产环境可以使用IDMap索引
        pass
    
    def _save_index(self):
        """保存索引"""
        faiss.write_index(self.index, f"{self.index_path}.faiss")
        with open(f"{self.index_path}.pkl", 'wb') as f:
            pickle.dump(self.metadata, f)

# 全局向量数据库实例
vector_db = VectorDatabase()
```

**依赖关系**：
- 依赖：T2-001 数据库模型设计

**验收条件**：
- [ ] FAISS安装成功
- [ ] 向量数据库类创建完成
- [ ] 向量添加功能正常
- [ ] 向量搜索功能正常
- [ ] 数据持久化正常

---

### T4-002: API Key轮询管理

| 属性 | 内容 |
|------|------|
| **任务编号** | T4-002 |
| **任务名称** | API Key轮询管理 |
| **预估工时** | 0.5天 |
| **优先级** | P1 |

**任务描述**：
实现多API Key轮询管理机制，提高API调用可靠性。

**具体步骤**：
1. 创建API Key轮询管理类
2. 实现Key轮询逻辑
3. 实现故障自动切换
4. 实现使用统计
5. 集成到智谱API调用

**核心代码** (`backend/app/services/api_key_manager.py`)：
```python
import os
import itertools
from typing import List, Dict
from datetime import datetime

class APIKeyRotator:
    """API Key轮询管理器"""
    
    def __init__(self):
        self.api_keys = self._load_api_keys()
        self.key_iter = itertools.cycle(self.api_keys)
        self.key_stats = {key: {'usage': 0, 'failures': 0, 'last_used': None} 
                         for key in self.api_keys}
    
    def _load_api_keys(self) -> List[str]:
        """加载API Keys"""
        keys = []
        for i in range(1, 6):
            key = os.getenv(f'ZHIPU_API_KEY_{i}')
            if key:
                keys.append(key)
        
        # 如果没有配置多个Key，使用单个Key
        if not keys:
            key = os.getenv('ZHIPU_API_KEY')
            if key:
                keys.append(key)
        
        if not keys:
            raise ValueError("未配置智谱API Key")
        
        return keys
    
    def get_next_key(self) -> str:
        """获取下一个API Key"""
        return next(self.key_iter)
    
    def record_usage(self, key: str, success: bool = True):
        """记录API Key使用情况"""
        if key in self.key_stats:
            self.key_stats[key]['usage'] += 1
            self.key_stats[key]['last_used'] = datetime.now()
            if not success:
                self.key_stats[key]['failures'] += 1
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.key_stats
    
    def get_available_key(self) -> str:
        """获取可用的API Key（带故障转移）"""
        max_retries = len(self.api_keys)
        for _ in range(max_retries):
            key = self.get_next_key()
            # 检查失败率，如果失败率过高则跳过
            stats = self.key_stats[key]
            total = stats['usage']
            if total > 0 and stats['failures'] / total > 0.5:
                continue
            return key
        
        # 如果所有Key都不可用，返回第一个
        return self.api_keys[0]

# 全局API Key管理器
api_key_rotator = APIKeyRotator()
```

**依赖关系**：
- 依赖：T1-002 后端基础环境搭建

**验收条件**：
- [ ] API Key轮询类创建完成
- [ ] Key轮询逻辑正常
- [ ] 故障转移功能正常
- [ ] 使用统计功能正常

---

### T4-003: 文本向量化服务

| 属性 | 内容 |
|------|------|
| **任务编号** | T4-003 |
| **任务名称** | 文本向量化服务 |
| **预估工时** | 0.5天 |
| **优先级** | P1 |

**任务描述**：
实现文本向量化服务，调用智谱Embedding API将文本转换为向量。

**具体步骤**：
1. 安装智谱SDK
2. 创建文本向量化服务类
3. 实现单文本向量化
4. 实现批量文本向量化
5. 实现错误处理和重试

**核心代码** (`backend/app/services/embedding.py`)：
```python
import os
import numpy as np
from typing import List, Union
import zhipuai
from app.services.api_key_manager import api_key_rotator

class EmbeddingService:
    """文本向量化服务"""
    
    def __init__(self):
        self.model = "embedding-3"
        self.dimension = 1024
    
    def get_embedding(self, text: str) -> np.ndarray:
        """获取单个文本的向量"""
        max_retries = 3
        for attempt in range(max_retries):
            api_key = api_key_rotator.get_next_key()
            try:
                zhipuai.api_key = api_key
                response = zhipuai.model_api.invoke(
                    model=self.model,
                    prompt=text
                )
                
                if response['code'] == 200:
                    embedding = response['data']['embedding']
                    api_key_rotator.record_usage(api_key, success=True)
                    return np.array(embedding, dtype=np.float32)
                else:
                    raise Exception(f"API错误: {response['msg']}")
                    
            except Exception as e:
                api_key_rotator.record_usage(api_key, success=False)
                if attempt == max_retries - 1:
                    raise e
                continue
        
        raise Exception("获取向量失败")
    
    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        """批量获取文本向量"""
        embeddings = []
        for text in texts:
            embedding = self.get_embedding(text)
            embeddings.append(embedding)
        return np.array(embeddings)

# 全局向量化服务
embedding_service = EmbeddingService()
```

**依赖关系**：
- 依赖：T4-002 API Key轮询管理

**验收条件**：
- [ ] 智谱SDK安装成功
- [ ] 向量化服务类创建完成
- [ ] 单文本向量化正常
- [ ] 批量向量化正常
- [ ] 错误处理正常

---

### T4-004: RAG检索服务

| 属性 | 内容 |
|------|------|
| **任务编号** | T4-004 |
| **任务名称** | RAG检索服务 |
| **预估工时** | 1天 |
| **优先级** | P1 |

**任务描述**：
实现RAG（检索增强生成）服务，结合向量检索和AI生成。

**具体步骤**：
1. 创建RAG服务类
2. 实现知识库检索功能
3. 实现Prompt构建功能
4. 实现AI对话功能
5. 实现引用链接生成

**核心代码** (`backend/app/services/rag.py`)：
```python
from typing import List, Dict, Any
from app.services.vector_db import vector_db
from app.services.embedding import embedding_service
from app.services.api_key_manager import api_key_rotator
import zhipuai

class RAGService:
    """RAG检索增强生成服务"""
    
    def __init__(self):
        self.model = "glm-4.5"
        self.max_context_length = 3000
    
    def search_knowledge_base(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """搜索知识库"""
        # 1. 问题向量化
        query_embedding = embedding_service.get_embedding(query)
        
        # 2. 向量检索
        results = vector_db.search(query_embedding, top_k=top_k)
        
        return results
    
    def build_prompt(self, query: str, context: List[Dict[str, Any]]) -> str:
        """构建Prompt"""
        context_text = ""
        for i, item in enumerate(context, 1):
            content = item.get('content', '')[:500]  # 限制长度
            context_text += f"[{i}] {item.get('title', '未知标题')}: {content}\n\n"
        
        prompt = f"""你是AIForum的智能助手，专门帮助课题组同学解答学术问题。

请根据以下参考资料回答问题：

{context_text}

用户问题：{query}

请基于以上资料回答问题。如果资料中没有相关信息，请说明无法回答。
回答时请保持专业、简洁、准确。"""
        
        return prompt
    
    def chat(self, query: str, history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """AI对话"""
        # 1. 检索相关知识
        relevant_docs = self.search_knowledge_base(query)
        
        # 2. 构建Prompt
        prompt = self.build_prompt(query, relevant_docs)
        
        # 3. 调用AI API
        messages = []
        if history:
            for msg in history:
                messages.append({"role": msg['role'], "content": msg['content']})
        messages.append({"role": "user", "content": prompt})
        
        max_retries = len(api_key_rotator.api_keys)
        for attempt in range(max_retries):
            api_key = api_key_rotator.get_next_key()
            try:
                zhipuai.api_key = api_key
                response = zhipuai.model_api.invoke(
                    model=self.model,
                    prompt=messages
                )
                
                if response['code'] == 200:
                    answer = response['data']['choices'][0]['content']
                    api_key_rotator.record_usage(api_key, success=True)
                    
                    # 构建引用
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
                else:
                    raise Exception(f"API错误: {response['msg']}")
                    
            except Exception as e:
                api_key_rotator.record_usage(api_key, success=False)
                if attempt == max_retries - 1:
                    raise e
                continue
        
        raise Exception("AI对话失败")

# 全局RAG服务
rag_service = RAGService()
```

**依赖关系**：
- 依赖：T4-001 向量数据库搭建
- 依赖：T4-003 文本向量化服务

**验收条件**：
- [ ] RAG服务类创建完成
- [ ] 知识库检索功能正常
- [ ] Prompt构建功能正常
- [ ] AI对话功能正常
- [ ] 引用链接生成正常

---

### T4-005: AI对话API

| 属性 | 内容 |
|------|------|
| **任务编号** | T4-005 |
| **任务名称** | AI对话API |
| **预估工时** | 1天 |
| **优先级** | P1 |

**任务描述**：
开发AI对话相关API接口。

**具体步骤**：
1. 实现AI对话API
2. 实现知识库检索API
3. 实现对话历史保存API
4. 实现对话历史获取API
5. 实现新建对话API
6. 编写单元测试

**核心代码** (`backend/app/api/ai.py`)：
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.core.database import get_db
from app.core.security import get_current_user
from app.services.rag import rag_service
from app.models.user import User

router = APIRouter(prefix="/ai", tags=["AI"])

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    references: List[dict]

@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """AI对话"""
    try:
        # 获取对话历史
        history = []
        if request.conversation_id:
            history = get_conversation_history(request.conversation_id)
        
        # 调用RAG服务
        result = rag_service.chat(request.message, history)
        
        # 保存对话记录
        save_chat_message(
            user_id=current_user.id,
            conversation_id=request.conversation_id,
            question=request.message,
            answer=result['answer'],
            references=result['references']
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search")
def search_knowledge_base(
    query: str,
    top_k: int = 3,
    current_user: User = Depends(get_current_user)
):
    """知识库检索"""
    try:
        results = rag_service.search_knowledge_base(query, top_k)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/new")
def new_conversation(current_user: User = Depends(get_current_user)):
    """新建对话"""
    import uuid
    conversation_id = str(uuid.uuid4())
    # 保存对话记录
    return {"conversation_id": conversation_id}

@router.get("/history")
def get_chat_history(
    conversation_id: Optional[str] = None,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取对话历史"""
    # 查询最近的历史记录
    history = get_user_chat_history(current_user.id, conversation_id, limit)
    return {"history": history}
```

**依赖关系**：
- 依赖：T4-004 RAG检索服务
- 依赖：T2-002 用户认证模块

**验收条件**：
- [ ] AI对话API正常
- [ ] 知识库检索API正常
- [ ] 对话历史API正常
- [ ] 新建对话API正常
- [ ] 单元测试通过

---

### T4-006: 知识库构建

| 属性 | 内容 |
|------|------|
| **任务编号** | T4-006 |
| **任务名称** | 知识库构建 |
| **预估工时** | 0.5天 |
| **优先级** | P1 |

**任务描述**：
构建知识库，将论文、经验贴等内容向量化并存储。

**具体步骤**：
1. 创建知识库构建脚本
2. 实现论文内容向量化
3. 实现经验贴内容向量化
4. 实现下载中心内容向量化
5. 实现增量更新机制

**核心代码** (`backend/scripts/build_knowledge_base.py`)：
```python
#!/usr/bin/env python3
"""构建知识库脚本"""

import sys
sys.path.append('..')

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.paper import Paper
from app.models.post import Post
from app.models.download import Download
from app.services.embedding import embedding_service
from app.services.vector_db import vector_db

def build_paper_vectors(db: Session):
    """构建论文向量"""
    papers = db.query(Paper).all()
    
    for paper in papers:
        # 构建文本
        text = f"{paper.title}\n{paper.authors}\n{paper.abstract}\n{paper.keywords}"
        
        # 向量化
        embedding = embedding_service.get_embedding(text)
        
        # 存储到向量数据库
        vector_db.add_vectors(
            vectors=embedding.reshape(1, -1),
            metadata_list=[{
                'type': 'paper',
                'id': paper.id,
                'title': paper.title,
                'content': paper.abstract
            }]
        )
    
    print(f"已构建 {len(papers)} 篇论文的向量")

def build_post_vectors(db: Session):
    """构建经验贴向量"""
    posts = db.query(Post).all()
    
    for post in posts:
        # 构建文本
        text = f"{post.title}\n{post.content}"
        
        # 向量化
        embedding = embedding_service.get_embedding(text)
        
        # 存储到向量数据库
        vector_db.add_vectors(
            vectors=embedding.reshape(1, -1),
            metadata_list=[{
                'type': 'post',
                'id': post.id,
                'title': post.title,
                'content': post.content[:500]
            }]
        )
    
    print(f"已构建 {len(posts)} 篇经验贴的向量")

def main():
    db = SessionLocal()
    try:
        print("开始构建知识库...")
        build_paper_vectors(db)
        build_post_vectors(db)
        print("知识库构建完成！")
    finally:
        db.close()

if __name__ == "__main__":
    main()
```

**依赖关系**：
- 依赖：T4-003 文本向量化服务
- 依赖：T4-001 向量数据库搭建

**验收条件**：
- [ ] 知识库构建脚本完成
- [ ] 论文向量化正常
- [ ] 经验贴向量化正常
- [ ] 增量更新机制正常

---

### T4-007: AI对话前端组件

| 属性 | 内容 |
|------|------|
| **任务编号** | T4-007 |
| **任务名称** | AI对话前端组件 |
| **预估工时** | 1天 |
| **优先级** | P1 |

**任务描述**：
开发AI对话侧边栏组件。

**具体步骤**：
1. 开发AI对话侧边栏组件
2. 实现消息列表显示
3. 实现消息输入框
4. 实现引用链接显示
5. 实现对话历史切换
6. 集成后端API

**核心代码** (`frontend/src/components/AIChat.vue`)：
```vue
<template>
  <div class="ai-chat-sidebar" :class="{ collapsed: isCollapsed }">
    <div class="chat-header">
      <h3>AI助手</h3>
      <el-button @click="toggleCollapse" circle>
        <el-icon><ArrowRight v-if="isCollapsed" /><ArrowLeft v-else /></el-icon>
      </el-button>
    </div>
    
    <div v-if="!isCollapsed" class="chat-content">
      <!-- 消息列表 -->
      <div class="message-list" ref="messageList">
        <div v-for="(msg, index) in messages" :key="index" 
             :class="['message', msg.role]">
          <div class="message-content" v-html="msg.content"></div>
          
          <!-- 引用链接 -->
          <div v-if="msg.references" class="references">
            <p>参考资料：</p>
            <ul>
              <li v-for="ref in msg.references" :key="ref.id">
                <router-link :to="`/${ref.type}s/${ref.id}`">
                  {{ ref.title }}
                </router-link>
              </li>
            </ul>
          </div>
        </div>
      </div>
      
      <!-- 输入框 -->
      <div class="input-area">
        <el-input
          v-model="inputMessage"
          type="textarea"
          :rows="3"
          placeholder="请输入问题..."
          @keyup.enter.ctrl="sendMessage"
        />
        <el-button type="primary" @click="sendMessage" :loading="loading">
          发送
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { sendChatMessage, getChatHistory } from '@/api/ai'

const isCollapsed = ref(false)
const messages = ref([
  { role: 'assistant', content: '你好，我是小助手，可以与我进行对话。' }
])
const inputMessage = ref('')
const loading = ref(false)
const conversationId = ref('')

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
}

const sendMessage = async () => {
  if (!inputMessage.value.trim()) return
  
  const userMessage = inputMessage.value
  messages.value.push({ role: 'user', content: userMessage })
  inputMessage.value = ''
  loading.value = true
  
  try {
    const res = await sendChatMessage({
      message: userMessage,
      conversation_id: conversationId.value
    })
    
    messages.value.push({
      role: 'assistant',
      content: res.answer,
      references: res.references
    })
  } catch (error) {
    messages.value.push({
      role: 'assistant',
      content: '抱歉，发生了错误，请稍后重试。'
    })
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  // 新建对话
  const res = await createNewConversation()
  conversationId.value = res.conversation_id
})
</script>

<style scoped>
.ai-chat-sidebar {
  width: 400px;
  height: 100%;
  border-left: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  transition: width 0.3s;
}

.ai-chat-sidebar.collapsed {
  width: 50px;
}

.chat-header {
  padding: 10px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.message {
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 8px;
}

.message.user {
  background-color: #e3f2fd;
  margin-left: 20px;
}

.message.assistant {
  background-color: #f5f5f5;
  margin-right: 20px;
}

.input-area {
  padding: 10px;
  border-top: 1px solid #e0e0e0;
}

.references {
  margin-top: 10px;
  font-size: 12px;
  color: #666;
}

.references a {
  color: #409eff;
}
</style>
```

**依赖关系**：
- 依赖：T3-001 前端基础架构搭建
- 依赖：T4-005 AI对话API

**验收条件**：
- [ ] AI对话侧边栏组件正常
- [ ] 消息列表显示正常
- [ ] 消息输入功能正常
- [ ] 引用链接显示正常
- [ ] 对话历史切换正常

---

### T4-008: 对话历史管理

| 属性 | 内容 |
|------|------|
| **任务编号** | T4-008 |
| **任务名称** | 对话历史管理 |
| **预估工时** | 0.5天 |
| **优先级** | P2 |

**任务描述**：
实现对话历史的保存和查询功能。

**具体步骤**：
1. 创建对话历史数据模型
2. 实现对话历史保存功能
3. 实现对话历史查询功能
4. 实现对话历史删除功能
5. 实现对话历史限制（最近5-10条）

**依赖关系**：
- 依赖：T2-001 数据库模型设计
- 依赖：T4-005 AI对话API

**验收条件**：
- [ ] 对话历史模型创建完成
- [ ] 对话历史保存功能正常
- [ ] 对话历史查询功能正常
- [ ] 对话历史限制功能正常

---

## 阶段四总结

| 任务 | 状态 | 工时 |
|------|------|------|
| T4-001 向量数据库搭建 | 待开始 | 0.5天 |
| T4-002 API Key轮询管理 | 待开始 | 0.5天 |
| T4-003 文本向量化服务 | 待开始 | 0.5天 |
| T4-004 RAG检索服务 | 待开始 | 1天 |
| T4-005 AI对话API | 待开始 | 1天 |
| T4-006 知识库构建 | 待开始 | 0.5天 |
| T4-007 AI对话前端组件 | 待开始 | 1天 |
| T4-008 对话历史管理 | 待开始 | 0.5天 |
| **总计** | - | **5.5天** |

---

**下一步**：进入阶段五：集成与测试
