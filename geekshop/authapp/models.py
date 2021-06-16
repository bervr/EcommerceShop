from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class ShopUser(AbstractUser):
    user_pic = models.ImageField(upload_to='user_avatar', blank=True)
    age =models.PositiveIntegerField(verbose_name='возраст', blank=True)
