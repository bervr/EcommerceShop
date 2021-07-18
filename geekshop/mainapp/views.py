from random import sample
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import ProductCategory, Product
from basketapp.models import Basket
from django.conf import settings
from django.core.cache import cache




def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True).select_related()
            cache.set(key, links_menu)
        else:
            return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True).select_related()

def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product_item = cache.get(key)
        if product_item is None:
            product_item = get_object_or_404(Product, pk=pk)
            cache.set(key, product_item)
        else:
            return product_item
    else:
        return get_object_or_404(Product, pk=pk)


def get_hot_product():
    products = Product.objects.all().select_related()
    return sample(list(products), 1)[0]

# def get_basket(user):
#     if user.is_authenticated:
#         return Basket.objects.filter(user=user)
#     else:
#         return []


def get_same_products(hot_products):
    same_products = Product.objects.filter(category=hot_products.category).select_related().exclude(pk=hot_products.pk)[:3]
    return same_products


def products(request, pk=None):
    title = 'продукты'
    category = ''
    products = ''

    hot_product = get_hot_product()
    categories = ProductCategory.objects.all()
    # basket = get_basket(request.user)
    same_products = get_same_products(hot_product)


    if pk is not None:
        if pk == 0:
            products = Product.objects.all().select_related().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category_id__pk=pk).select_related().order_by('price')

    context = {
        'title': title,
        'categories': categories,
        'category': category,
        'products': products,
        'links_menu':get_links_menu(),
        # 'basket': basket,
        'same_products': same_products,
        'hot_product': hot_product,
    }
    return render(request, 'products_list.html', context=context)


@login_required
def product(request, pk):
    title = 'страница продута'
    product = get_product(pk)
    context = {
        'title': title,
        'links_menu': get_links_menu(),
        'categories': ProductCategory.objects.all(),
        'product': product,
        # 'basket': get_basket(request.user),
        'same_products': get_same_products(product),
    }
    return render(request, 'product.html', context)