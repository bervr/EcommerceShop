from django.shortcuts import render
from basketapp.models import Basket
from mainapp.models import Product, ProductCategory
# Create your views here.


def main(request):
    products = Product.objects.all().select_related()[:4]
    products_category = ProductCategory.objects.all().select_related()[:4]
    basket =[]
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user).select_related()
    do_active = {
        'products': products,
        'products_category': products_category,
        'basket': basket,
    }
    return render(request, 'index.html', context=do_active)


def contacts(request):
    return render(request, 'contacts.html')
