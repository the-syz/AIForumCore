from tortoise import fields, models

class Comment(models.Model):
    """评论模型"""
    id = fields.IntField(pk=True, auto_increment=True)
    content = fields.TextField(null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    # 关系
    user = fields.ForeignKeyField("models.User", related_name="comments", on_delete=fields.CASCADE)
    post = fields.ForeignKeyField("models.Post", related_name="comments", on_delete=fields.CASCADE)
    parent = fields.ForeignKeyField("models.Comment", related_name="replies", null=True, on_delete=fields.CASCADE)
    
    class Meta:
        table = "comments"
        indexes = [
            ("post_id",),
            ("user_id",),
            ("created_at",),
        ]