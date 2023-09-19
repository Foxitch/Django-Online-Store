from django.db import models

from orders.enums import OrderStatus
from products.models import Basket
from users.models import User


class Order(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=OrderStatus.CREATED, choices=OrderStatus.STATUSES)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def update_after_payment(self) -> None:
        baskets = Basket.objects.filter(user=self.initiator)
        self.status = OrderStatus.PAID
        self.basket_history = {
            'purchased_items': [item.de_json() for item in baskets],
            'total_sum': float(baskets.total_sum())
        }
        baskets.delete()
        self.save()

    def __str__(self) -> str:
        return f'Order #{self.id} | {self.first_name} | {self.last_name}'
