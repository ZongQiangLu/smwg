from tortoise import fields
from tortoise.models import Model

class Coupon(Model):
    name = fields.CharField(max_length=100)
    type = fields.IntField()
    value = fields.DecimalField(max_digits=10, decimal_places=2)
    min_amount = fields.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_time = fields.DatetimeField()
    end_time = fields.DatetimeField()
    total = fields.IntField()
    remain = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "coupons"

class UserCoupon(Model):
    user = fields.ForeignKeyField("models.User", related_name="coupons")
    coupon = fields.ForeignKeyField("models.Coupon", related_name="user_coupons")
    status = fields.IntField(default=0)
    used_time = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "user_coupons"
