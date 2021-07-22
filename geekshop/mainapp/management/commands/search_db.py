from datetime import timedelta

from django.core.management import BaseCommand
from django.db.models import Q, F, When, Case, IntegerField, DecimalField
from ordersapp.models import OrderItem
from mainapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        action_1 = 1
        action_2 = 2
        action_3 = 3

        action_1_timedelta = timedelta(hours=12)
        action_2_timedelta = timedelta(hours=24)

        action_1_discount = 0.3
        action_2_discount = 0.15
        action_3_discount = 0.05

        action_1_condition = Q(order__updated__lte=F('order__created') + action_1_timedelta)
        action_2_condition = Q(order__updated__gt=F('order__created') + action_1_timedelta) & \
                             Q(order__updated__lte=F('order__created') + action_2_timedelta)
        action_3_condition = Q(order__updated__gt=F('order__created') + action_2_timedelta)

        action_1_order = When(action_1_condition, then=action_1)
        action_2_order = When(action_2_condition, then=action_2)
        action_3_order = When(action_3_condition, then=action_3)

        action_1_price = When(action_1_condition, then=F('product__price') * F('quantity') * action_1_discount)
        action_2_price = When(action_2_condition, then=F('product__price') * F('quantity') * action_2_discount)
        action_3_price = When(action_3_condition, then=F('product__price') * F('quantity') * action_3_discount)

        order_items = OrderItem.objects.annotate(
            action_order=Case(
                action_1_order,
                action_2_order,
                action_3_order,
                output_field=IntegerField()
            )
            ).annotate(
                total_price=Case(
                    action_1_price,
                    action_2_price,
                    action_3_price,
                    output_field=DecimalField()

            )
        ).order_by('action_order', 'total_price').select_related()

        for item in order_items:
            print(
                f'{item.action_order} order#{item.pk} discount: {item.total_price} {item.order.updated - item.order.created}')


        find_1 =Q(name = 'Стол')
        find_2 =Q(category__name= 'Дом')

        print(Product.objects.filter(find_1 | find_2))

