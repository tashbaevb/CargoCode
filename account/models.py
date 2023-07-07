from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.conf import settings
import base64

TYPE_OF_CAR = (
    ('big', 'big'),
    ('middle', 'middle'),
    ('minivan', 'minivan')
)

WEEKEND = (
    ('MON', 'MON'),
    ('TUE', 'TUE'),
    ('WEN', 'WEN'),
    ('TR', 'TR'),
    ('FRI', 'FRI'),
    ('SAT', 'SAT'),
    ('SUN', 'SUN'),
)


class User1(AbstractUser):
    email = models.EmailField(unique=True)

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


# Add the related_name argument to the ManyToMany fields
User1.groups.related_name = 'custom_user_set'
User1.user_permissions.related_name = 'custom_user_set'


class Driver(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    driver_license = models.TextField(blank=True, default='')
    straxovka = models.TextField(blank=True, default='')
    car_number = models.CharField(max_length=100, blank=True, default='')
    car_title = models.CharField(max_length=100, blank=True, default='')
    car_year = models.IntegerField(blank=True, default='')
    car_type = models.CharField(choices=TYPE_OF_CAR, max_length=100, blank=True, default='big')
    bank = models.CharField(max_length=100, blank=True, default='')
    name = models.CharField(max_length=100, blank=True, default='')
    phone_number = models.CharField(max_length=100, blank=True, default='')
    per_km = models.CharField(max_length=10, blank=True, default='')
    weekends = models.CharField(max_length=10, choices=WEEKEND, blank=True, default='', help_text='Select weekends')

    # def save(self, *args, **kwargs):
    #     # При сохранении объекта Driver, если есть значения в полях driver_license и straxovka,
    #     # производим кодирование значений в формат Base64
    #     if self.driver_license:
    #         self.driver_license = base64.b64encode(self.driver_license.encode('utf-8')).decode('utf-8')
    #     if self.straxovka:
    #         self.straxovka = base64.b64encode(self.straxovka.encode('utf-8')).decode('utf-8')
    #
    #     super().save(*args, **kwargs)


class Company(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    company_name = models.CharField(max_length=100, blank=True, default='')
    dot_number = models.CharField(max_length=100, blank=True, default='')
    descriptions = models.TextField(blank=True, default='')
    bank_account = models.CharField(max_length=100, blank=True, default='')
    per_km = models.CharField(max_length=10, blank=True, default='')


class Company3ver(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    car_number = models.CharField(max_length=20, blank=True, default='')
    car_type = models.CharField(max_length=20, choices=TYPE_OF_CAR, blank=True, default='')
    car_title = models.CharField(max_length=60, blank=True, default='')
    weekends = models.CharField(max_length=10, choices=WEEKEND, blank=True, default='', help_text='Select weekends')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
