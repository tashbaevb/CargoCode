import uuid

from django.db import models
from django.dispatch import receiver

from account.models import TYPE_OF_CAR
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_delete

User = settings.AUTH_USER_MODEL

ORDER_TYPES = (
    ('FT', 'FIRST'),
    ('ST', 'SECOND')
)


# ---order beginning
# while they are not picked up it shows as 'pending' on client side
# only when algorithm hove found deliveryman (individual, company driver) it shows as status 'picked' -
# - this data is put in another table (model: OrderStatus), algorithm only creates data, tracking is done by client
class Order(models.Model):
    class Meta:
        abstract = True
        unique_together = ('id',)

    type: ORDER_TYPES = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    receiver_name = models.CharField(max_length=200)
    receiver_surname = models.CharField(max_length=200)
    receiver_number = models.CharField(max_length=200)
    origin = models.FloatField()
    destination = models.FloatField()
    date_until = models.DateTimeField()
    delivery_type = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        if not self.pk:
            pass
        else:
            if type is not None:
                OrderStack.objects.create(order_id=self.pk, type=self.type, sender=self.sender)
            else:
                raise Exception('specify type of Order')

    # delete OrderStack on deletion
    def delete(self):
        order_stack = OrderStack.objects.get(order_id=self.pk)
        if order_stack is not None:
            order_stack.delete()
        super(Order, self).delete()


class FirstOrder(Order):
    car_type = models.CharField(max_length=10, choices=TYPE_OF_CAR, default='big')
    type = "FT"


class SecondOrder(Order):
    cargo_type = models.CharField(max_length=200)
    weight = models.IntegerField()
    volume_x = models.IntegerField()
    volume_y = models.IntegerField()
    volume_z = models.IntegerField()
    type = "ST"


ORDER_STATUS = (
    ('P', 'PENDING'),
    ('F', 'DRIVER_FOUND'),
    ('A', 'ADOPTED'),
    ('O', 'ON_THE_WAY'),
    ('D', 'DELIVERED'),
)

DRIVER_TYPE = (
    ('IN', 'INDIVIDUAL'),
    ('CO', 'COMPANY_DRIVER'),
)


class OrderStack(models.Model):
    order_id = models.UUIDField(unique=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    type = models.CharField(max_length=2, choices=ORDER_TYPES)
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default='P')
    driver_type = models.CharField(max_length=2, choices=DRIVER_TYPE, null=True)
    driver_id = models.IntegerField(unique=False, null=True)
