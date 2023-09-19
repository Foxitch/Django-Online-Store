import stripe
from django.conf import settings
from django.contrib import admin

from products.models import Basket, Product, ProductCategory

stripe.api_key = settings.STRIPE_SECRET_KEY


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    fields = ('name', 'description')
    ordering = ('id',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', 'category')
    fields = ('name', 'description', 'price', 'image', 'quantity', 'stripe_product_price_id', 'category')
    # readonly_fields = ('stripe_product_price_id',)
    search_fields = ('name',)
    ordering = ('id',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0
