from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from api.views import BasketModelViewSet, ProductModelView

app_name = 'api'

router = routers.DefaultRouter()
router.register('products', ProductModelView)
router.register('baskets', BasketModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', obtain_auth_token)
]
