from django.db import models
from django.contrib.auth.models import User
from fruits.models import Fruits

class Order(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    sale_time = models.DateTimeField(auto_now_add=True)
    total_purchase = models.FloatField(default=0)


class Sales(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    fruit = models.ForeignKey(Fruits, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    fruit_price = models.FloatField()
    discount = models.PositiveIntegerField(default=0)
    total_price = models.FloatField()


