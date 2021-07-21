from django.db import models


# Create your models here.


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='имя')
    description = models.TextField(
        verbose_name='описание',
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    href = models.CharField(max_length=64, verbose_name='ссылка', default= '')
    def __str__(self):
        return self.name

    is_active = models.BooleanField(default=True)

    def change_activity(self):
        self.is_active = not self.is_active
        self.save()
        for item in self.products.select_related():
            item.change_activity()
            item.save()
        # self.save()






class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        verbose_name='категория',
        related_name="products",
    )
    name = models.CharField(
        verbose_name='имя продукта',
        max_length=128,
    )
    image = models.ImageField(
        upload_to='products_img',
        blank=True,
    )
    short_desc = models.CharField(
        max_length=256,
        verbose_name='краткое описание',
        blank=True,
    )
    description = models.TextField(
        verbose_name='Описание продукта',
        blank=True,
        max_length=500,
    )
    price = models.DecimalField(
        verbose_name='цена',
        max_digits=8,
        decimal_places=2,
        default=0,
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество на складе',
        default=0,
    )
    is_active = models.BooleanField(default=True)
    state_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} ({self.category})'

    def change_activity(self):
        print("смена активнсти категории")
        if self.category.is_active:
            self.is_active = self.state_active
            print('вернуть продукты как были')
        else:
            print('отключить продукты')
            self.state_active = self.is_active
            self.is_active = False

