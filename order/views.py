import rest_framework.response
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView

from .serializers import FirstOrder, SecondOrder, OrderStack
from . import models


class OrderView(CreateAPIView):
    #permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.data['sender'] = request.user.pk
        return self.create(request, *args, **kwargs)


class FirstOrderView(OrderView):
    serializer_class = FirstOrder


class SecondOrderView(OrderView):
    serializer_class = SecondOrder


# list of objects related to user
class OrderStackView(ListAPIView):
    #permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderStack

    def get(self, request, *args, **kwargs):
        self.queryset = models.OrderStack.objects.filter(sender=request.user.pk)
        return self.list(request, *args, **kwargs)


class GetDetailedOrder(APIView):
    #permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderStack

    def get(self, request, *args, **kwargs):
        order_serializer = None
        order_stack = models.OrderStack.objects.get(pk=request.data['id'])
        if order_stack.sender != request.user:
            return rest_framework.response.Response(status=status.HTTP_403_FORBIDDEN)

        if order_stack.type == 'FT':
            order = models.FirstOrder.objects.get(pk=order_stack.order_id)
            order_serializer = FirstOrder(order)
            pass
        elif order_stack.type == 'ST':
            order = models.SecondOrder.objects.get(pk=order_stack.order_id)
            order_serializer = SecondOrder(order)
            pass

        return rest_framework.response.Response({
            'order': {
                'stack': OrderStack(order_stack).data,
                'details': order_serializer.data
            }
        })
