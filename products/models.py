import stripe
from _decimal import Decimal
from django.db import models
from stripe.api_resources.price import Price

from users.models import User


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None) -> None:
        if not self.stripe_product_price_id:
            self.stripe_product_price_id = self.create_stripe_product_price()['id']

        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def create_stripe_product_price(self) -> Price:
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price * 100),
            currency='byn'
        )
        return stripe_product_price

    def __str__(self) -> str:
        return f'{self.name} | {self.category}'

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'


class BasketQuerySet(models.QuerySet):

    def total_sum(self) -> float:
        return sum(basket.sum() for basket in self)

    def total_quantity(self) -> int:
        return sum(basket.quantity for basket in self)

    def create_stripe_items(self) -> list:
        line_item = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_item.append(item)

        return line_item


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def de_json(self) -> dict:
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return basket_item

    def sum(self) -> Decimal:
        return self.product.price * self.quantity

    def __str__(self) -> str:
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'

    @classmethod
    def create_or_update(cls, product_id: int, user: User) -> tuple[models.Model, bool]:
        obj = None
        baskets = Basket.objects.filter(user=user, product_id=product_id)

        if not baskets.exists():
            obj = Basket.objects.create(user=user, product_id=product_id, quantity=1)
            is_created = True
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
            is_created = False

        return obj, is_created
