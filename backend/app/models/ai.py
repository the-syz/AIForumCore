from tortoise import fields, models

class AIConversation(models.Model):
    """AI对话模型"""
    id = fields.IntField(pk=True, auto_increment=True)
    topic = fields.CharField(max_length=255, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    # 关系
    user = fields.ForeignKeyField("models.User", related_name="conversations", on_delete=fields.CASCADE)
    
    class Meta:
        table = "ai_conversations"
        indexes = [
            ("user_id",),
            ("created_at",),
        ]

class AIMessage(models.Model):
    """AI消息模型"""
    id = fields.IntField(pk=True, auto_increment=True)
    role = fields.CharField(max_length=20, null=False)  # user, assistant
    content = fields.TextField(null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    # 关系
    conversation = fields.ForeignKeyField("models.AIConversation", related_name="messages", on_delete=fields.CASCADE)
    
    class Meta:
        table = "ai_messages"
        indexes = [
            ("conversation_id",),
            ("created_at",),
        ]