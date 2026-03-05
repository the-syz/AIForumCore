from tortoise import fields, models
from enum import Enum

class UserRole(str, Enum):
    STUDENT = "student"
    STUDENT_ADMIN = "student_admin"
    TEACHER = "teacher"

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
    role = fields.CharField(max_length=20, default=UserRole.STUDENT)
    is_admin = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "users"
        unique_together = [
            ("student_id",),
        ]