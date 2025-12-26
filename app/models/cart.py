from tortoise import fields
from tortoise.models import Model

class Cart(Model):
    user = fields.ForeignKeyField("models.User", related_name="carts")
    sku = fields.ForeignKeyField("models.ProductSku", related_name="carts")
    quantity = fields.IntField(default=1)
    selected = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "carts"
        unique_together = (("user", "sku"),)
