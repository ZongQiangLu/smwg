from tortoise import fields
from tortoise.models import Model

class User(Model):
    username = fields.CharField(max_length=50, unique=True)
    password_hash = fields.CharField(max_length=128)
    phone = fields.CharField(max_length=20, null=True)
    avatar = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "users"

class Address(Model):
    user = fields.ForeignKeyField("models.User", related_name="addresses")
    name = fields.CharField(max_length=50)
    phone = fields.CharField(max_length=20)
    province = fields.CharField(max_length=50)
    city = fields.CharField(max_length=50)
    district = fields.CharField(max_length=50)
    detail = fields.CharField(max_length=255)
    is_default = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "addresses"
