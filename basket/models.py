from django.db import models
from django.contrib.auth import get_user_model
from  product.models import Product

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    count = models.IntegerField()
