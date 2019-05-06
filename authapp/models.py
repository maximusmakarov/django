from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver



def get_key_activation_expires():
    return now() + timedelta(hours=48)


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveSmallIntegerField(verbose_name='возраст', null=True)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=get_key_activation_expires)

    def activation_key_is_valid(self):
        return now() <= self.activation_key_expires


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'МУЖСКОЙ'),
        (FEMALE, 'ЖЕНСКИЙ'),
    )

    RU = 0
    UK = 1
    BE = 2
    EN = 3
    ES = 4
    FI = 5
    DE = 6
    IT = 7

    LANGUAGE_CHOICES = (
        (RU, 'РУССКИЙ'),
        (UK, 'УКРАИНСКИЙ'),
        (BE, 'БЕЛОРУССКИЙ'),
        (EN, 'АНГЛИЙСКИЙ'),
        (ES, 'ИСПАНСКИЙ'),
        (FI, 'ФИНСКИЙ'),
        (DE, 'НЕМЕЦКИЙ'),
        (IT, 'ИТАЛЬЯРНСКИЙ'),
    )

    user = models.OneToOneField(ShopUser, primary_key=True, on_delete=models.CASCADE)
    tags = models.CharField(verbose_name='теги', max_length=128, blank=True)
    aboutMe = models.TextField(verbose_name='о себе', max_length=512, blank=True)
    gender = models.CharField(verbose_name='пол', max_length=1, choices=GENDER_CHOICES, blank=True)
    lang = models.CharField(verbose_name='язык', max_length=3, choices=LANGUAGE_CHOICES, blank=True)

    @receiver(post_save, sender=ShopUser)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)
        else:
            instance.shopuserprofile.save()
