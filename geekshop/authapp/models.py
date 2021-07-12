from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from datetime import timedelta




class ShopUser(AbstractUser):
    user_pic = models.ImageField(upload_to='user_avatar', blank=True)
    age =models.PositiveIntegerField(verbose_name='возраст', blank=True, default=18)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def is_activation_key_expired(self):
        if now() < self.activation_key_created + timedelta(hours=48):
            return False
        return True


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'
    GENDER_CHOISES = (
        (MALE, 'М'),
        (FEMALE, 'Ж')
    )

    user = models.OneToOneField(ShopUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='теги', max_length=128, blank=True)
    about_me= models.TextField(verbose_name='обо мне', max_length=512, blank=True)
    gender = models.CharField(choices=GENDER_CHOISES, blank=True, verbose_name='пол', max_length=1)

    @receiver(post_save,sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()

