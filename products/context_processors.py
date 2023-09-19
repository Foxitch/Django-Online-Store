from products.models import Basket


def baskets(request) -> dict:
    user = request.user
    return {'baskets': Basket.objects.filter(user=user) if user.is_authenticated else []}
