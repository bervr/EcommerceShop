from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
from django.utils.timezone import now
from datetime import timedelta




class ShopUser(AbstractUser):
    user_pic = models.ImageField(upload_to='user_avatar', blank=True)
    age =models.PositiveIntegerField(verbose_name='возраст', blank=True)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def is_activation_key_expired(self):
        if now() < self.activation_key_created + timedelta(hours=48):
            return False
        return True
