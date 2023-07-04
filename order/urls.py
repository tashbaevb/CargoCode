from django.urls import path

from order.views import FirstOrderView, SecondOrderView

urlpatterns = [
    path('api/order/1', FirstOrderView.as_view(), name='order1'),
    path('api/order/2', SecondOrderView.as_view(), name='order2'),
]
