from tortoise import fields
from tortoise.models import Model

class Category(Model):
    name = fields.CharField(max_length=50)
    icon = fields.CharField(max_length=255, null=True)
    sort_order = fields.IntField(default=0)
    
    class Meta:
        table = "categories"

class Product(Model):
    category = fields.ForeignKeyField("models.Category", related_name="products")
    name = fields.CharField(max_length=200)
    cover = fields.CharField(max_length=255)
    images = fields.JSONField(default=list)
    description = fields.TextField(null=True)
    base_price = fields.DecimalField(max_digits=10, decimal_places=2)
    sales = fields.IntField(default=0)
    status = fields.IntField(default=1)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "products"

class ProductSku(Model):
    product = fields.ForeignKeyField("models.Product", related_name="skus")
    spec_info = fields.JSONField(default=dict)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    original_price = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    stock = fields.IntField(default=0)
    sku_code = fields.CharField(max_length=50, null=True)
    image = fields.CharField(max_length=255, null=True)
    
    class Meta:
        table = "product_skus"
