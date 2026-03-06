from tortoise import fields, models

class Paper(models.Model):
    """论文模型"""
    id = fields.IntField(pk=True, auto_increment=True)
    title = fields.CharField(max_length=255, null=False)
    authors = fields.TextField(null=True)
    abstract = fields.TextField(null=True)
    keywords = fields.CharField(max_length=255, null=True)
    doi = fields.CharField(max_length=100, null=True)
    paper_type = fields.CharField(max_length=50, default="journal")  # journal, thesis
    category = fields.CharField(max_length=100, null=True)
    file_path = fields.CharField(max_length=255, null=False)
    upload_time = fields.DatetimeField(auto_now_add=True)
    like_count = fields.IntField(default=0)
    favorite_count = fields.IntField(default=0)
    view_count = fields.IntField(default=0)
    download_count = fields.IntField(default=0)
    
    # 关系
    uploader = fields.ForeignKeyField("models.User", related_name="papers", on_delete=fields.CASCADE, db_column="uploader_id")
    
    class Meta:
        table = "papers"
        indexes = [
            ("title",),
            ("doi",),
            ("upload_time",),
        ]