from tortoise import fields, models

class Download(models.Model):
    """下载中心模型"""
    id = fields.IntField(pk=True, auto_increment=True)
    title = fields.CharField(max_length=255, null=False)
    description = fields.TextField(null=True)
    file_path = fields.CharField(max_length=255, null=False)
    upload_time = fields.DatetimeField(auto_now_add=True)
    download_count = fields.IntField(default=0)
    category = fields.CharField(max_length=50, null=False)
    
    # 关系
    uploader = fields.ForeignKeyField("models.User", related_name="uploads", on_delete=fields.CASCADE)
    
    class Meta:
        table = "downloads"
        indexes = [
            ("title",),
            ("category",),
            ("upload_time",),
        ]