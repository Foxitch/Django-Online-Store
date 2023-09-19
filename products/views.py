from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


class ProductListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    title = 'Store - Каталог'
    paginate_by = 6

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')

        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data()
        categories = cache.get('categories')

        if not categories:
            context['categories'] = ProductCategory.objects.all()
            cache.set('categories', context['categories'], 30)
        else:
            context['categories'] = categories

        return context


@login_required
def basket_add(request: WSGIRequest, product_id: int) -> HttpResponseRedirect:
    Basket.create_or_update(product_id=product_id, user=request.user)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request: WSGIRequest, basket_id: int) -> HttpResponseRedirect:
    basket = Basket.objects.get(id=basket_id)
    basket.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
