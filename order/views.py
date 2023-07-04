import rest_framework.response
from django.forms import model_to_dict
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from .serializers import FirstOrder, SecondOrder


class OrderView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.data['sender'] = request.user.pk
        return self.create(request, *args, **kwargs)


class FirstOrderView(OrderView):
    serializer_class = FirstOrder


class SecondOrderView(OrderView):
    serializer_class = SecondOrder
