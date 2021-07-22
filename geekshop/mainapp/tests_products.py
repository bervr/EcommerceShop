from django.test import TestCase
from mainapp.models import Product, ProductCategory

class ProductsTestCase(TestCase):
   def setUp(self):
       category = ProductCategory.objects.create(name="стулья")
       self.product_1 = Product.objects.create(name="стул 1",
                                          category=category,
                                          price = 1999.5,
                                          quantity=150,
                                          )

       self.product_2 = Product.objects.create(name="стул 2",
                                          category=category,
                                          price=2998.1,
                                          quantity=125,
                                          is_active=False)

       self.product_3 = Product.objects.create(name="стул 3",
                                          category=category,
                                          price=998.1,
                                          quantity=115)

   def test_product_get(self):
       product_1 = Product.objects.get(name="стул 1")
       product_2 = Product.objects.get(name="стул 2")
       self.assertEqual(product_1, self.product_1)
       self.assertEqual(product_2, self.product_2)

   def test_product_print(self):
       product_1 = Product.objects.get(name="стул 1")
       product_2 = Product.objects.get(name="стул 2")
       self.assertEqual(str(product_1), 'стул 1 (стулья)')
       self.assertEqual(str(product_2), 'стул 2 (стулья)')


   def test_product_get_items(self):
       product_1 = Product.objects.get(name="стул 1")
       product_3 = Product.objects.get(name="стул 3")
       products = product_1.get_items()

       self.assertEqual(list(products), [product_1, product_3])

   def test_category_change_activity(self):
       # выбрали продукты и категорию
       product_1 = Product.objects.get(name="стул 1")
       product_2 = Product.objects.get(name="стул 2")
       category = product_1.category
       # проверяем что все ок
       self.assertTrue(product_1.is_active)
       self.assertFalse(product_2.is_active)
       self.assertTrue(category.is_active)
        # меняем активность
       category.change_activity()
       product_1.change_activity()
       product_2.change_activity()
       #
       self.assertFalse(category.is_active)
       self.assertFalse(product_1.is_active)
       self.assertFalse(product_2.is_active)
       # меняем активность обратно
       category.change_activity()
       product_1.change_activity()
       product_2.change_activity()
       #
       self.assertTrue(category.is_active)
       self.assertTrue(product_1.is_active)
       self.assertFalse(product_2.is_active)