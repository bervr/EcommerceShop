from django.test import TestCase, Client

from mainapp.models import ProductCategory, Product


class TestMainSmokeTest(TestCase):
    status_code_success = 200

    def setUp(self):
        cat_1 = ProductCategory.objects.create(
            name='cat_1'
        )
        Product.objects.create(
            category=cat_1,
            name='prod_1'
        )
        self.client = Client()

    # def tearDown(self):
    #     pass

    def test_main_app_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)
