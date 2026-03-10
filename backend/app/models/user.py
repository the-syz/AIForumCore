from tortoise import fields, models

class User(models.Model):
    """用户模型"""
    id = fields.IntField(pk=True, auto_increment=True)
    name = fields.CharField(max_length=50, null=False)
    student_id = fields.CharField(max_length=20, unique=True, null=False)
    grade = fields.CharField(max_length=10, null=True)
    email = fields.CharField(max_length=100, null=True)
    phone = fields.CharField(max_length=20, null=True)
    research_direction = fields.CharField(max_length=255, null=True)
    wechat = fields.CharField(max_length=50, null=True)
    password_hash = fields.CharField(max_length=255, null=False)
    # role字段扩展：master(硕士), phd(博士), graduate(毕业生), teacher(教师)
    role = fields.CharField(max_length=20, default="master")
    is_admin = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "users"
        unique_together = [
            ("student_id",),
        ]
    
    @property
    def role_display(self) -> str:
        """返回角色的中文显示名称"""
        role_map = {
            "master": "硕士研究生",
            "phd": "博士研究生", 
            "graduate": "毕业生",
            "teacher": "教师"
        }
        return role_map.get(self.role, "未知")