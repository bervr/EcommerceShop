from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemEditForm
from basketapp.models import Basket
from mainapp.models import Product


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True)


class OrderUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemEditForm, extra=1)
        if self.request.POST:
            data['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            orderitemformset = OrderFormSet(instance=self.object)
            for form in orderitemformset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
            data['orderitems'] = orderitemformset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()


        return super().form_valid(form)


class OrderCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemEditForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items.exists():
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemEditForm,
                                                     extra=basket_items.count())
                formset = OrderFormSet()
                data['user'] = "Уася"  # self.request.user
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
                # data['get_total_quantity'] = sum(list(map(lambda x: x.quantity, basket_items)))
                # data['get_total_cost'] = sum(list(map(lambda x: x.product_cost, basket_items)))
                # # form.instance.user = self.request.user
                # data['user'] = "Уася"#self.request.user
            else:
                formset = OrderFormSet()
        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
        if self.object.get_total_cost() == 0:
            self.object.delete()
        return super().form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('order:list')


class OrderRead(DetailView):
    model = Order


def forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('ordersapp:list'))


def get_product_price(request, pk):
    data = {}
    if request.is_ajax():
        product =get_object_or_404(Product, pk=pk)
        if product:
            data['price'] = product.price
            return JsonResponse(data)
        else:
            data['price'] = 0
            return JsonResponse(data)



