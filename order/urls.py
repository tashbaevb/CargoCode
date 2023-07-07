from django.urls import path

# from order.views import *

from .views import OrderStackView, GetDetailedOrder, FirstOrderView, SecondOrderView

urlpatterns = [
    path('api/orders/', OrderStackView.as_view(), name='orders'),
    path('api/order/details/', GetDetailedOrder.as_view(), name='order_detailed'),
    path('api/first_order/', FirstOrderView.as_view(), name='order_first'),
    path('api/second_order/', SecondOrderView.as_view(), name='order_second'),
]
