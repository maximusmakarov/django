from mainapp.models import ProductCategory


def basket(request):
    if request.user.is_authenticated:
        return {
            'basket': request.user.basket.all()
        }
    else:
        return \
            {
                'basket': []
            }


def menu(request):
    if request:
        return {
            'menu': ProductCategory.objects.filter(is_active=True)
        }
