from django.urls import path

from order.views import *

urlpatterns = [
    path('api/order/', OrderStackView.as_view(), name='orders'),
    path('api/order/details/', GetDetailedOrder.as_view(), name='order_detailed'),
    path('api/order/1', FirstOrderView.as_view(), name='order_first'),
    path('api/order/2', SecondOrderView.as_view(), name='order_second'),
]
