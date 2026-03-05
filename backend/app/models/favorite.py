from tortoise import fields, models

class Favorite(models.Model):
    """收藏模型"""
    id = fields.IntField(pk=True, auto_increment=True)
    target_type = fields.CharField(max_length=50, null=False)  # paper, post
    target_id = fields.IntField(null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    # 关系
    user = fields.ForeignKeyField("models.User", related_name="favorites", on_delete=fields.CASCADE)
    
    class Meta:
        table = "favorites"
        indexes = [
            ("user_id",),
            ("target_type",),
            ("target_id",),
        ]
        unique_together = [
            ("user_id", "target_type", "target_id"),
        ]