from tortoise import fields, models

class Post(models.Model):
    """经验贴模型"""
    id = fields.IntField(pk=True, auto_increment=True)
    title = fields.CharField(max_length=255, null=False)
    content = fields.TextField(null=False)
    category = fields.CharField(max_length=50, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    is_pinned = fields.BooleanField(default=False)
    is_draft = fields.BooleanField(default=False)
    view_count = fields.IntField(default=0)
    like_count = fields.IntField(default=0)
    comment_count = fields.IntField(default=0)
    attachments = fields.JSONField(default=list)
    
    # 关系
    author = fields.ForeignKeyField("models.User", related_name="posts", on_delete=fields.CASCADE)
    
    class Meta:
        table = "posts"
        indexes = [
            ("title",),
            ("category",),
            ("created_at",),
            ("is_pinned",),
        ]