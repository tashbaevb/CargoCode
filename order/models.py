from django.db import models
from account.models import User
from django.conf import settings
User = settings.AUTH_USER_MODEL

class Order(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    receiver_name = models.CharField(max_length=200)
    receiver_surname = models.CharField(max_length=200)
    receiver_number = models.CharField(max_length=200)
    origin = models.FloatField()
    destination = models.FloatField()
    date_until = models.DateTimeField()
    delivery_type = models.CharField(max_length=200)


class FirstOrder(Order):
    car_type = models.CharField(max_length=200)


class SecondOrder(Order):
    cargo_type = models.CharField(max_length=200)
    weight = models.IntegerField()
    volume_x = models.IntegerField()
    volume_y = models.IntegerField()
    volume_z = models.IntegerField()
