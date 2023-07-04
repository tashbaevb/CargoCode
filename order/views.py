from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .serializers import FirstOrder, SecondOrder


class OrderView(CreateAPIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "session": serializer.data,
        })


class FirstOrderView(OrderView):
    serializer_class = FirstOrder


class SecondOrderView(OrderView):
    serializer_class = SecondOrder

