from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from ordersapp.models import Order


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user = self.request.user)


class OrderUpdate(UpdateView):
    pass


class OrderCreate(CreateView):
    pass


class OrderDelete(DeleteView):
    pass


class OrderRead(DetailView):
    pass

def forming_complete():
    pass

