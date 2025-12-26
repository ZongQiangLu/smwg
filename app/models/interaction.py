from tortoise import fields
from tortoise.models import Model

class Favorite(Model):
    user = fields.ForeignKeyField("models.User", related_name="favorites")
    product = fields.ForeignKeyField("models.Product", related_name="favorites")
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "favorites"
        unique_together = (("user", "product"),)

class Footprint(Model):
    user = fields.ForeignKeyField("models.User", related_name="footprints")
    product = fields.ForeignKeyField("models.Product", related_name="footprints")
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "footprints"

class SearchHistory(Model):
    user = fields.ForeignKeyField("models.User", related_name="search_histories")
    keyword = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "search_histories"

class Review(Model):
    user = fields.ForeignKeyField("models.User", related_name="reviews")
    product = fields.ForeignKeyField("models.Product", related_name="reviews")
    order = fields.ForeignKeyField("models.Order")
    order_item = fields.ForeignKeyField("models.OrderItem")
    rating = fields.IntField()
    content = fields.TextField(null=True)
    images = fields.JSONField(default=list)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "reviews"
