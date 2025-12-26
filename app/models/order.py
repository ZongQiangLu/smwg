from tortoise import fields
from tortoise.models import Model

class Order(Model):
    order_no = fields.CharField(max_length=32, unique=True)
    user = fields.ForeignKeyField("models.User", related_name="orders")
    total_amount = fields.DecimalField(max_digits=10, decimal_places=2)
    pay_amount = fields.DecimalField(max_digits=10, decimal_places=2)
    coupon = fields.ForeignKeyField("models.UserCoupon", null=True)
    status = fields.IntField(default=0)
    address_snapshot = fields.JSONField()
    remark = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    paid_at = fields.DatetimeField(null=True)
    
    class Meta:
        table = "orders"

class OrderItem(Model):
    order = fields.ForeignKeyField("models.Order", related_name="items")
    sku = fields.ForeignKeyField("models.ProductSku")
    product_name = fields.CharField(max_length=200)
    product_image = fields.CharField(max_length=255)
    spec_info = fields.JSONField()
    quantity = fields.IntField()
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    is_reviewed = fields.BooleanField(default=False)
    
    class Meta:
        table = "order_items"

class OrderLogistics(Model):
    order = fields.OneToOneField("models.Order", related_name="logistics")
    company = fields.CharField(max_length=50)
    tracking_no = fields.CharField(max_length=50)
    status = fields.IntField(default=0)
    traces = fields.JSONField(default=list)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "order_logistics"
