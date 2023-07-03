from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

TYPE_OF_CAR = (("big", "big"), ("middle", "middle"), ("minivan", "minivan"))


class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name="custom_user_set")
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_user_set"
    )
    email = models.EmailField(unique=True)

    class Meta:
        swappable = "AUTH_USER_MODEL"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


# Add the related_name argument to the ManyToMany fields
User.groups.related_name = "custom_user_set"
User.user_permissions.related_name = "custom_user_set"


class Driver(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    driver_license = models.TextField()
    straxovka = models.TextField()
    car_number = models.CharField(max_length=100)
    car_title = models.CharField(max_length=100)
    car_year = models.IntegerField()
    car_type = models.CharField(choices=TYPE_OF_CAR, max_length=100)
    bank = models.CharField(max_length=100)


class Company(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    dot_number = models.CharField(max_length=100)
    descriptions = models.TextField()
    bank_account = models.CharField(max_length=100)


class Company3ver(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car_number = models.CharField(max_length=20)
    car_type = models.CharField(max_length=20, choices=TYPE_OF_CAR)
    car_title = models.CharField(max_length=60)
