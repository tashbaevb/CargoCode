import uuid

from rest_framework import serializers
from .models import FirstOrder as FirstOrderModel, SecondOrder as SecondOrderModel,\
    Order as OrderModel, \
    OrderStack as OrderStackModel

class Order(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = ['sender',
                  'receiver_name',
                  'receiver_surname',
                  'receiver_number',
                  'origin',
                  'destination',
                  'date_until',
                  'delivery_type']


class FirstOrder(Order):
    class Meta:
        model = FirstOrderModel
        fields = Order.Meta.fields + ['car_type']


class SecondOrder(Order):
    class Meta:
        model = SecondOrderModel
        fields = Order.Meta.fields + ['cargo_type',
                                      'weight',
                                      'volume_x',
                                      'volume_y',
                                      'volume_z', ]


class OrderStack(serializers.ModelSerializer):
    class Meta:
        model = OrderStackModel
        fields = ['id', 'order_id', 'sender', 'type', 'status', 'driver_type', 'driver_id']

