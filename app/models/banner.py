from tortoise import fields
from tortoise.models import Model

class Banner(Model):
    image = fields.CharField(max_length=255)
    link = fields.CharField(max_length=255, null=True)
    sort_order = fields.IntField(default=0)
    status = fields.IntField(default=1)
    
    class Meta:
        table = "banners"
