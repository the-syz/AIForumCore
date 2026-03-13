import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.core.database import TORTOISE_ORM
from tortoise import Tortoise
import asyncio

async def insert_posts():
    await Tortoise.init(config=TORTOISE_ORM)
    
    conn = Tortoise.get_connection("default")
    
    posts_data = [
        {
            "title": "如何高效学习编程语言",
            "content": """# 如何高效学习编程语言

## 前言

作为一名研究生，掌握至少一门编程语言是必备技能。本文将分享我在学习编程过程中的心得体会。

## 学习方法

### 1. 选择合适的学习资源

- **官方文档**：最权威的参考资料
- **在线课程**：Coursera、edX、B站等平台
- **开源项目**：GitHub上的优质项目

### 2. 实践为主

学习编程最重要的是动手实践：

```python
# 示例：快速排序算法
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
```

### 3. 建立知识体系

- 基础语法
- 数据结构
- 算法设计
- 项目实战

## 总结

坚持每天学习，保持好奇心，多与他人交流，你一定能掌握编程技能！""",
            "category": "学习经验",
            "author_id": 23
        },
        {
            "title": "研究生时间管理技巧",
            "content": """# 研究生时间管理技巧

## 引言

研究生阶段时间管理尤为重要，如何平衡科研、课程和生活是每个研究生都需要面对的问题。

## 核心原则

### 1. 四象限法则

将任务分为四类：
- **重要且紧急**：立即处理
- **重要不紧急**：计划处理
- **紧急不重要**：委托他人
- **不重要不紧急**：尽量避免

### 2. 番茄工作法

- 25分钟专注工作
- 5分钟休息
- 每4个番茄钟后休息15-30分钟

### 3. 每日计划

建议每天早上花10分钟规划当天任务。

## 实用工具推荐

1. **Notion** - 知识管理
2. **Todoist** - 任务管理
3. **Forest** - 专注力培养

## 结语

时间管理需要持续练习，找到适合自己的方法最重要。""",
            "category": "学习经验",
            "author_id": 25
        },
        {
            "title": "如何快速阅读学术论文",
            "content": """# 如何快速阅读学术论文

## 概述

在科研过程中，高效阅读论文是必备技能。本文介绍一种系统的论文阅读方法。

## 三遍阅读法

### 第一遍：快速浏览（5-10分钟）

1. 阅读标题、摘要和关键词
2. 查看图表和公式
3. 阅读结论部分
4. 决定是否继续深入阅读

### 第二遍：理解内容（30-60分钟）

1. 仔细阅读引言
2. 理解方法论
3. 分析实验结果
4. 记录关键问题和疑问

### 第三遍：深入分析（1-2小时）

1. 尝试复现论文结果
2. 思考可能的改进方向
3. 与相关论文对比分析

## 总结

掌握高效的论文阅读方法，可以大大提高科研效率。""",
            "category": "科研经验",
            "author_id": 38
        },
        {
            "title": "科研工具推荐：从入门到精通",
            "content": """# 科研工具推荐：从入门到精通

## 前言

工欲善其事，必先利其器。本文推荐一些实用的科研工具。

## 文献管理

### Zotero

- 免费开源
- 支持多平台同步
- 一键导入文献
- 自动生成参考文献

### EndNote

- 功能强大
- 与Word深度集成
- 适合大型文献库

## 写作工具

### LaTeX

适合撰写：
- 数学公式较多的论文
- 学位论文
- 期刊投稿

### Markdown

适合：
- 笔记整理
- 博客写作
- 文档编写

## 总结

选择适合自己的工具，持续学习，提高科研效率。""",
            "category": "科研经验",
            "author_id": 23
        },
        {
            "title": "研究生心理健康指南",
            "content": """# 研究生心理健康指南

## 引言

研究生阶段面临科研压力、就业焦虑等多重挑战，保持心理健康至关重要。

## 常见问题

### 1. 科研焦虑

**症状**：
- 担心论文写不出来
- 害怕导师批评
- 对未来迷茫

**应对方法**：
- 制定阶段性目标
- 与导师保持沟通
- 寻求同伴支持

### 2. 拖延症

**原因**：
- 完美主义倾向
- 任务过于庞大
- 缺乏动力

**解决方案**：
- 分解任务
- 设定截止日期
- 奖励机制

## 自我调节技巧

### 运动

每周至少3次，每次30分钟以上。

### 社交

- 参加学术活动
- 加入兴趣社团
- 保持与家人朋友的联系

## 结语

关注心理健康，是科研路上的重要保障。""",
            "category": "生活经验",
            "author_id": 25
        },
        {
            "title": "研究生如何保持工作生活平衡",
            "content": """# 研究生如何保持工作生活平衡

## 背景

很多研究生陷入"996"甚至"007"的工作模式，长期下来身心俱疲。如何在科研与生活之间找到平衡点？

## 核心理念

**工作是为了更好的生活，而不是生活的全部。**

## 具体建议

### 1. 设定边界

- 明确工作时间和休息时间
- 周末至少休息一天
- 下班后不看工作消息

### 2. 培养爱好

推荐活动：
- 阅读（非学术类）
- 音乐/电影
- 运动/旅行
- 烹饪/手工

### 3. 社交活动

- 定期与朋友聚会
- 参加非学术类活动
- 保持与家人的联系

## 总结

平衡不是一成不变的状态，而是动态调整的过程。找到适合自己的节奏最重要。""",
            "category": "生活经验",
            "author_id": 38
        },
        {
            "title": "实验室安全注意事项",
            "content": """# 实验室安全注意事项

## 前言

实验室安全是科研工作的基础，任何疏忽都可能造成严重后果。

## 基本规则

### 个人防护

进入实验室必须：
- 穿戴实验服
- 佩戴护目镜
- 穿封闭式鞋子
- 长发需扎起

### 化学品管理

1. **存储**
   - 分类存放
   - 标签清晰
   - 通风良好

2. **使用**
   - 了解化学品性质
   - 在通风橱中操作
   - 准备应急措施

## 应急处理

### 火灾

1. 立即报警
2. 使用灭火器
3. 有序撤离

## 总结

安全无小事，时刻保持警惕！""",
            "category": "其他",
            "author_id": 23
        },
        {
            "title": "学术会议参会指南",
            "content": """# 学术会议参会指南

## 概述

参加学术会议是研究生学术生涯的重要组成部分，本文分享参会经验。

## 会前准备

### 1. 选择会议

考虑因素：
- 会议主题相关性
- 会议级别和影响力
- 时间和地点
- 费用预算

### 2. 准备材料

- 论文/PPT
- 名片
- 个人简介
- 预约想见的学者

## 会议期间

### 听报告技巧

- 记录关键观点
- 思考与自己的研究关联
- 准备提问

### 社交建议

1. **主动交流**
   - 自我介绍简洁明了
   - 准备"电梯演讲"

2. **交换联系方式**
   - 名片
   - LinkedIn/ResearchGate

## 会后跟进

1. 整理笔记
2. 发送感谢邮件
3. 保持联系

## 总结

学术会议不仅是学习的机会，更是拓展学术网络的平台。充分准备，积极参与！""",
            "category": "其他",
            "author_id": 25
        }
    ]
    
    print("开始插入经验贴数据...")
    print("=" * 60)
    
    for i, post in enumerate(posts_data, 1):
        try:
            await conn.execute_query(
                """INSERT INTO posts 
                   (title, content, category, author_id, created_at, updated_at, is_pinned, is_draft, view_count, like_count, comment_count) 
                   VALUES (%s, %s, %s, %s, NOW(), NOW(), 0, 0, 0, 0, 0)""",
                [post["title"], post["content"], post["category"], post["author_id"]]
            )
            print(f"[{i}/8] 插入成功: {post['title']}")
            print(f"        分类: {post['category']}, 作者ID: {post['author_id']}")
        except Exception as e:
            print(f"[{i}/8] 插入失败: {str(e)}")
    
    print("\n" + "=" * 60)
    print("验证插入结果...")
    
    result = await conn.execute_query("""
        SELECT p.id, p.title, p.category, p.author_id, u.name as author_name 
        FROM posts p 
        LEFT JOIN users u ON p.author_id = u.id
        ORDER BY p.id DESC 
        LIMIT 8
    """)
    
    print("\n已插入的经验贴：")
    print("-" * 80)
    for row in result[1]:
        print(f"ID: {row['id']}, 标题: {row['title'][:25]}..., 分类: {row['category']}, 作者: {row['author_name']}")
    
    print("\n按分类统计：")
    stats = await conn.execute_query("""
        SELECT category, COUNT(*) as count
        FROM posts
        GROUP BY category
        ORDER BY count DESC
    """)
    
    for row in stats[1]:
        print(f"  {row['category']}: {row['count']}篇")
    
    await Tortoise.close_connections()
    print("\n完成！")

if __name__ == "__main__":
    asyncio.run(insert_posts())
