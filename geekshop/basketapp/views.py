from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from basketapp.models import Basket
from django.template.loader import render_to_string
from django.urls import reverse
from mainapp.models import Product
# Create your views here.


def basket(request):
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        products = Product.objects.all().values('pk', 'price')
        context = {
            'basket': basket,
            'products': products,
        }
        return render(request, 'basket.html', context)

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))

    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

        content = {
            'basket': basket_items,
        }

        result = render_to_string('inc_basket_list.html', content)

        return JsonResponse({'result': result})

