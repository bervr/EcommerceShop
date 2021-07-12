import os, json

from django.core.management.base import BaseCommand
from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory

JSON_PATH = 'mainapp/json'

def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), encoding='utf-8') as f:
        return json.load(f)
#
class Command(BaseCommand):
    def handle(self, *args, **options):
        categories =  load_from_json('categories')
        ProductCategory.objects.all().delete()
        for category in categories:
            new_category = ProductCategory(**category)
            new_category.save()

        products = load_from_json('products')
        for product in products:
            category_name = product['category']
            category_obj = ProductCategory.objects.get(href = category_name)
            product['category'] = category_obj
            new_product = Product(**product)
            new_product.save()


        # ShopUser.objects.create_superuser('django', 'django@1.local', '123', age='99')
